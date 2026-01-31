"""Storage utilities for tokens and data."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import orjson

# Use local .data directory in the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / ".data"
ACCESS_TOKEN_FILE = DATA_DIR / "access-token.json"
CACHE_DIR = DATA_DIR / "transactions"


def save_access_token(access_token: str, item_id: str) -> None:
    """Save access token to local storage."""
    ACCESS_TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)

    data = {"access_token": access_token, "item_id": item_id}

    with open(ACCESS_TOKEN_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"💾 Access token saved to {ACCESS_TOKEN_FILE}")


def get_access_token() -> Optional[str]:
    """Get access token from local storage."""
    if not ACCESS_TOKEN_FILE.exists():
        return None

    try:
        with open(ACCESS_TOKEN_FILE, "r") as f:
            data = json.load(f)
        return data.get("access_token")
    except (json.JSONDecodeError, FileNotFoundError):
        return None


def get_cached_transactions(
    accountName: str, year: str, month: str
) -> Optional[list[Dict[str, Any]]]:
    """Get cached transactions from local storage."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"transactions_{accountName}_{year}_{month}.json"

    if not os.path.exists(cache_file):
        return None

    # Check if file is empty (corrupt cache)
    if os.path.getsize(cache_file) == 0:
        print(f"⚠️  Empty cache file found, removing: {cache_file}")
        os.remove(cache_file)
        return None

    print(f"Getting transactions for cache: {accountName} from {year}-{month}")

    try:
        with open(cache_file, "rb") as f:
            return orjson.loads(f.read())
    except orjson.JSONDecodeError:
        print(f"⚠️  Corrupt cache file found, removing: {cache_file}")
        os.remove(cache_file)
        return None


def save_cached_transactions(
    accountName: str, year: str, month: str, transactions: list[Dict[str, Any]]
) -> None:
    """Save cached transactions to local storage."""
    if not transactions:
        return

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(CACHE_DIR / f"transactions_{accountName}_{year}_{month}.json", "wb") as f:
        f.write(orjson.dumps(transactions, option=orjson.OPT_INDENT_2))
