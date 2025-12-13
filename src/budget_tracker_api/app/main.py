from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

app = FastAPI(title="Budget Tracker APP")

# Get the directory containing this file
BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"

# API Routes (must be defined BEFORE static file mounting)
@app.get("/api/status")
def hello_api():
    return {"status": "api is working"}

# Add more API routes here
# @app.get("/api/transactions")
# def get_transactions():
#     return {"transactions": []}

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
    return {"error": "Frontend not built. Run: cd src/budget_tracker_api/frontend && npm run build"}


def start():
    """Entry point for poetry script"""
    import uvicorn
    uvicorn.run("budget_tracker_api.app.main:app", host="0.0.0.0", port=8000, reload=True)