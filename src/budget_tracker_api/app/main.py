import logging
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from budget_tracker.services import PlaidClient
from budget_tracker.commands import pull_statements
from budget_tracker.utils.storage import save_access_token, get_access_token

app = FastAPI(title="Budget Tracker APP")

# Configure logger
logger = logging.getLogger(__name__)

# Get the directory containing this file
BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"

plaid_client = PlaidClient()

# API Routes (must be defined BEFORE static file mounting)
@app.get("/api/status")
def hello_api():
    return {"status": "api is working"}

# Plaid Link API Routes
@app.get("/api/plaid/create-link-token")
def create_link_token():
    """Create a Plaid link token for account linking."""
    try:
        # Don't use redirect_uri for localhost - use the SDK instead
        response = plaid_client.create_link_token(redirect_uri=None)
        return response
    except Exception as e:
        logger.error(f"Failed to create link token: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create link token")

@app.get("/link")
def link_page():
    """Serve a page to link bank accounts using Plaid Link SDK."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Link Your Bank Account</title>
        <script src="https://cdn.plaid.com/link/v2/stable/link-initialize.js"></script>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .status {
                font-size: 18px;
                margin: 20px 0;
                padding: 15px;
                border-radius: 4px;
            }
            .loading {
                background-color: #fff3cd;
                color: #856404;
            }
            .success {
                background-color: #d4edda;
                color: #155724;
            }
            .error {
                background-color: #f8d7da;
                color: #721c24;
            }
            button {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 18px;
                margin: 10px 0;
            }
            button:hover {
                background-color: #0056b3;
            }
            button:disabled {
                background-color: #6c757d;
                cursor: not-allowed;
            }
            .token-box {
                background-color: #f0f0f0;
                padding: 15px;
                border-radius: 4px;
                margin: 20px 0;
                word-break: break-all;
                font-family: monospace;
                font-size: 12px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Link Your Bank Account</h1>

            <div class="status loading" id="status">
                Initializing...
            </div>

            <button id="linkButton" onclick="startPlaidLink()" style="display:none;">
                Open Plaid Link
            </button>

            <div id="resultSection" style="display:none;">
                <h2>Public Token Received:</h2>
                <div class="token-box" id="tokenDisplay"></div>
                <button onclick="autoExchange()" id="exchangeBtn" style="background-color: #28a745;">
                    Exchange & Save Token
                </button>
                <div class="status" id="exchangeStatus" style="display:none;"></div>
            </div>
        </div>

        <script>
            let plaidHandler = null;
            let publicToken = null;

            // Initialize on page load
            async function initializePage() {
                try {
                    document.getElementById('status').textContent = 'Loading Plaid Link...';

                    const response = await fetch('/api/plaid/create-link-token');
                    const data = await response.json();

                    plaidHandler = Plaid.create({
                        token: data.link_token,
                        onSuccess: async (public_token, metadata) => {
                            console.log('Success! Public token:', public_token);
                            console.log('Metadata:', metadata);
                            publicToken = public_token;
                            showToken(public_token);
                        },
                        onExit: (err, metadata) => {
                            if (err) {
                                document.getElementById('status').innerHTML = '❌ Error: ' + err.error_message;
                                document.getElementById('status').className = 'status error';
                            } else {
                                document.getElementById('status').innerHTML = 'Link flow exited. Click the button to try again.';
                                document.getElementById('status').className = 'status loading';
                            }
                        },
                        onEvent: (eventName, metadata) => {
                            console.log('Event:', eventName, metadata);
                        }
                    });

                    document.getElementById('status').innerHTML = '✅ Ready to link your account!';
                    document.getElementById('status').className = 'status success';
                    document.getElementById('linkButton').style.display = 'block';

                    // Auto-open Plaid Link
                    startPlaidLink();
                } catch (error) {
                    document.getElementById('status').innerHTML = '❌ Failed to initialize: ' + error.message;
                    document.getElementById('status').className = 'status error';
                }
            }

            function startPlaidLink() {
                if (plaidHandler) {
                    plaidHandler.open();
                    document.getElementById('status').innerHTML = 'Complete the bank linking in the popup...';
                    document.getElementById('status').className = 'status loading';
                }
            }

            function showToken(token) {
                document.getElementById('status').innerHTML = '✅ Account linked successfully!';
                document.getElementById('status').className = 'status success';
                document.getElementById('tokenDisplay').textContent = token;
                document.getElementById('resultSection').style.display = 'block';
                document.getElementById('linkButton').style.display = 'none';
            }

            async function autoExchange() {
                const statusDiv = document.getElementById('exchangeStatus');
                const exchangeBtn = document.getElementById('exchangeBtn');

                statusDiv.style.display = 'block';
                statusDiv.innerHTML = '🔄 Exchanging token and saving...';
                statusDiv.className = 'status loading';
                exchangeBtn.disabled = true;

                try {
                    const response = await fetch('/api/plaid/exchange', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ public_token: publicToken })
                    });

                    const result = await response.json();

                    if (response.ok) {
                        statusDiv.innerHTML = '✅ Success! Access token saved.<br>Item ID: ' + result.item_id;
                        statusDiv.className = 'status success';
                        exchangeBtn.textContent = 'Saved ✓';
                    } else {
                        statusDiv.innerHTML = '❌ Error: ' + (result.detail || 'Unknown error');
                        statusDiv.className = 'status error';
                        exchangeBtn.disabled = false;
                    }
                } catch (error) {
                    statusDiv.innerHTML = '❌ Network error: ' + error.message;
                    statusDiv.className = 'status error';
                    exchangeBtn.disabled = false;
                }
            }

            // Initialize when page loads
            window.onload = initializePage;
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/api/plaid/exchange")
async def exchange_token(request: Request):
    """Exchange public token for access token."""
    try:
        data = await request.json()
        public_token = data.get("public_token")

        if not public_token:
            raise HTTPException(status_code=400, detail="public_token is required")

        # Exchange the token
        result = plaid_client.exchange_public_token(public_token)

        # Save the access token
        save_access_token(result["access_token"], result["item_id"])

        return {"success": True, "item_id": result["item_id"], "access_token": result["access_token"]}
    except Exception as e:
        logger.error(f"Failed to exchange token: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/plaid/create-update-link-token")
def create_update_link_token():
    """Create a Plaid link token for re-authentication (update mode)."""
    try:
        # Get the existing access token
        access_token = get_access_token()
        if not access_token:
            raise HTTPException(status_code=404, detail="No access token found. Please link an account first at /link")

        # Create link token in update mode
        response = plaid_client.create_link_token(redirect_uri=None, access_token=access_token)
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create update link token: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create update link token")


@app.get("/update")
def update_page():
    """Serve a page to re-authenticate bank accounts using Plaid Link SDK (update mode)."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Re-authenticate Your Bank Account</title>
        <script src="https://cdn.plaid.com/link/v2/stable/link-initialize.js"></script>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .status {
                font-size: 18px;
                margin: 20px 0;
                padding: 15px;
                border-radius: 4px;
            }
            .loading {
                background-color: #fff3cd;
                color: #856404;
            }
            .success {
                background-color: #d4edda;
                color: #155724;
            }
            .error {
                background-color: #f8d7da;
                color: #721c24;
            }
            button {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 18px;
                margin: 10px 0;
            }
            button:hover {
                background-color: #0056b3;
            }
            button:disabled {
                background-color: #6c757d;
                cursor: not-allowed;
            }
            .info-box {
                background-color: #e7f3ff;
                border-left: 4px solid #007bff;
                padding: 15px;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Re-authenticate Your Bank Account</h1>

            <div class="info-box">
                <strong>Note:</strong> This will re-authenticate your existing bank connection.
                Your account link requires updated credentials or additional verification.
            </div>

            <div class="status loading" id="status">
                Initializing...
            </div>

            <button id="linkButton" onclick="startPlaidLink()" style="display:none;">
                Re-authenticate Bank Account
            </button>
        </div>

        <script>
            let plaidHandler = null;

            // Initialize on page load
            async function initializePage() {
                try {
                    document.getElementById('status').textContent = 'Loading Plaid Link...';

                    const response = await fetch('/api/plaid/create-update-link-token');

                    if (!response.ok) {
                        const error = await response.json();
                        throw new Error(error.detail || 'Failed to create link token');
                    }

                    const data = await response.json();

                    plaidHandler = Plaid.create({
                        token: data.link_token,
                        onSuccess: async (public_token, metadata) => {
                            console.log('Re-authentication successful!');
                            console.log('Metadata:', metadata);
                            document.getElementById('status').innerHTML = '✅ Re-authentication successful!<br><br>Your bank account connection has been restored. You can now close this page.';
                            document.getElementById('status').className = 'status success';
                            document.getElementById('linkButton').style.display = 'none';
                        },
                        onExit: (err, metadata) => {
                            if (err) {
                                document.getElementById('status').innerHTML = '❌ Error: ' + err.error_message;
                                document.getElementById('status').className = 'status error';
                            } else {
                                document.getElementById('status').innerHTML = 'Update flow exited. Click the button to try again.';
                                document.getElementById('status').className = 'status loading';
                            }
                        },
                        onEvent: (eventName, metadata) => {
                            console.log('Event:', eventName, metadata);
                        }
                    });

                    document.getElementById('status').innerHTML = '✅ Ready to re-authenticate!';
                    document.getElementById('status').className = 'status success';
                    document.getElementById('linkButton').style.display = 'block';

                    // Auto-open Plaid Link
                    startPlaidLink();
                } catch (error) {
                    document.getElementById('status').innerHTML = '❌ Failed to initialize: ' + error.message;
                    document.getElementById('status').className = 'status error';
                }
            }

            function startPlaidLink() {
                if (plaidHandler) {
                    plaidHandler.open();
                    document.getElementById('status').innerHTML = 'Complete the re-authentication in the popup...';
                    document.getElementById('status').className = 'status loading';
                }
            }

            // Initialize when page loads
            window.onload = initializePage;
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# Add more API routes here
@app.get("/api/transactions")
def get_transactions(year: str = "2025", month: str = "12"):
    """
    Get list of transactions from plaid api for specified year and month.
    Query params: year (default: 2025), month (default: 12)
    """
    statements = None
    try:
        statements = pull_statements(year, month, format="json")
        logger.info("statements logging", statements)
    except Exception as e:
        logger.error(f"Failed to fetch transactions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch transactions")
    return {"transactions": statements}

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
