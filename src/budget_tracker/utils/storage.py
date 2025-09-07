"""Storage utilities for tokens and data."""

from pathlib import Path
from typing import Optional
import json
import os

# TODO: Implement storage functionality
# This will handle saving/loading access tokens and caching data

CONFIG_DIR = Path.home() / ".budget-tracker"
ACCESS_TOKEN_FILE = CONFIG_DIR / "access-token.json"


def save_access_token(access_token: str, item_id: str) -> None:
    """Save access token to local storage."""
    CONFIG_DIR.mkdir(exist_ok=True)
    
    data = {
        "access_token": access_token,
        "item_id": item_id
    }
    
    with open(ACCESS_TOKEN_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"💾 Access token saved to {ACCESS_TOKEN_FILE}")


def get_access_token() -> Optional[str]:
    """Get access token from local storage."""
    if not ACCESS_TOKEN_FILE.exists():
        return None
    
    try:
        with open(ACCESS_TOKEN_FILE, 'r') as f:
            data = json.load(f)
        return data.get("access_token")
    except (json.JSONDecodeError, FileNotFoundError):
        return None


def has_access_token() -> bool:
    """Check if access token exists."""
    return get_access_token() is not None
