from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Budget Tracker APP")

@app.get("/api/status")
def hello_api():
    return {"status": "api is working"}

@app.get("/")
def render_frontend_root():
    html_path = os.path.join(os.path.dirname(__file__), "public/index.html")
    return FileResponse(html_path)
    

def start():
    """Entry point for poetry script"""
    import uvicorn
    uvicorn.run("budget_tracker_api.app.main:app", host="0.0.0.0", port=8000, reload=True)