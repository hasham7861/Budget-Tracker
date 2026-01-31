import logging
from pathlib import Path

from budget_tracker_api.app.services.plaid_service import PlaidService
from budget_tracker_api.app.services.transaction_service import TransactionService
from budget_tracker_api.app.utils.database import init_db, save_note, get_note
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Budget Tracker APP")

# Initialize database on startup
init_db()

# Configure logger
logger = logging.getLogger(__name__)

# Get the directory containing this file
BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"
TEMPLATES_DIR = BASE_DIR / "assets" / "templates"

# Initialize services
plaid_service = PlaidService()
transaction_service = TransactionService()

# API Routes (must be defined BEFORE static file mounting)
@app.get("/api/status")
def hello_api():
    return {"status": "api is working"}

# Plaid Link API Routes
@app.get("/api/plaid/create-link-token")
def create_link_token():
    """Create a Plaid link token for account linking."""
    return plaid_service.create_link_token()

@app.get("/link")
def link_page():
    """Serve a page to link bank accounts using Plaid Link SDK."""
    return FileResponse(TEMPLATES_DIR / "link.html")


@app.post("/api/plaid/exchange")
async def exchange_token(request: Request):
    """Exchange public token for access token."""
    data = await request.json()
    result, status_code, error = plaid_service.exchange_public_token(
        data.get("public_token")
    )

    if error:
        raise HTTPException(status_code=status_code, detail=error)
    return result


@app.get("/api/plaid/create-update-link-token")
def create_update_link_token():
    """Create a Plaid link token for re-authentication (update mode)."""
    result, status_code, error = plaid_service.create_update_link_token()

    if error:
        raise HTTPException(status_code=status_code, detail=error)
    return result


@app.get("/update")
def update_page():
    """Re-authenticate bank accounts using Plaid Link SDK (update mode)."""
    return FileResponse(TEMPLATES_DIR / "update.html")


# Add more API routes here
@app.get("/api/transactions")
def get_transactions(year: str = "2025", month: str = "12"):
    """
    Get list of transactions from plaid api for specified year and month.
    Query params: year (default: 2025), month (default: 12)
    """
    transactions, status_code, error = transaction_service.get_transactions(
        year, month
    )

    if error:
        raise HTTPException(status_code=status_code, detail=error)
    return {"transactions": transactions}


@app.get("/api/notes")
def get_notes(year: str, month: str):
    """Get notes for a specific year and month."""
    notes = get_note(year, month)
    return {"notes": notes or ""}


@app.post("/api/notes")
async def save_notes(request: Request):
    """Save notes for a specific year and month."""
    data = await request.json()
    year = data.get("year")
    month = data.get("month")
    notes = data.get("notes", "")

    if not year or not month:
        raise HTTPException(status_code=400, detail="year and month are required")

    save_note(year, month, notes)
    return {"success": True}

# Mount static files (JS, CSS, images)
# This serves files from /public/assets/* as /assets/*
if PUBLIC_DIR.exists() and (PUBLIC_DIR / "assets").exists():
    app.mount(
        "/assets",
        StaticFiles(directory=str(PUBLIC_DIR / "assets")),
        name="static"
    )

# Catch-all route for React Router (client-side routing)
# This must be LAST to avoid catching API routes
@app.get("/{full_path:path}")
def serve_react_app(full_path: str):
    """
    Serves the React app for all non-API routes.
    This enables client-side routing in React.
    """
    # If requesting a file that exists, serve it
    file_path = PUBLIC_DIR / full_path
    if file_path.is_file():
        return FileResponse(file_path)

    # Otherwise, serve index.html (for React Router)
    index_path = PUBLIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)

    # Fallback if build doesn't exist yet
    return {
        "error": (
            "Frontend not built. "
            "Run: cd src/budget_tracker_api/frontend && npm run build"
        )
    }

def start():
    """Entry point for poetry script"""
    import uvicorn

    uvicorn.run(
        "budget_tracker_api.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
