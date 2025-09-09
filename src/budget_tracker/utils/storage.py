"""Storage utilities for tokens and data."""

from pathlib import Path
from typing import Optional, Dict, Any
import json
import os
import orjson
import csv

CONFIG_DIR = Path.home()
ACCESS_TOKEN_FILE = CONFIG_DIR / ".budget-tracker" / "access-token.json"
CACHE_DIR = CONFIG_DIR / "desktop" / "budget-tracker"


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

def get_cached_transactions(accountName: str, year: str, month: str) -> Optional[list[Dict[str, Any]]]:
    """Get cached transactions from local storage."""
    
    CACHE_DIR.mkdir(exist_ok=True)
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
        with open(cache_file, 'rb') as f:
            return orjson.loads(f.read())
    except orjson.JSONDecodeError:
        print(f"⚠️  Corrupt cache file found, removing: {cache_file}")
        os.remove(cache_file)
        return None

def save_cached_transactions(accountName: str, year: str, month: str, transactions: list[Dict[str, Any]]) -> None:
    """Save cached transactions to local storage."""

    if not transactions:
        return

    CACHE_DIR.mkdir(exist_ok=True)
    with open(CACHE_DIR / f"transactions_{accountName}_{year}_{month}.json", 'wb') as f:
        f.write(orjson.dumps(transactions, option=orjson.OPT_INDENT_2))
    
def save_cached_transactions_csv(accountName: str, year: str, month: str, transactions: list[Dict[str, Any]], summaryData: dict[str, Any]) -> None:
    """Save cached transactions to local storage as CSV."""
    if not transactions:
        return

    CACHE_DIR.mkdir(exist_ok=True)
    with open(CACHE_DIR / f"transactions_{accountName}_{year}_{month}.csv", 'w') as f:
        writer = csv.writer(f)

        writer.writerow([''])
        writer.writerow(['Summary'])
        # add summary data to the csv
        for key, value in summaryData.items():
            if key == 'totalSpendingByCategory':
                writer.writerow(['Category', 'Total Spending', 'Total Transactions'])
                for category, spending in value.items():
                    writer.writerow([category, spending, summaryData['totalTransactionsCountByCategory'][category]])
            elif key == 'totalTransactionsCountByCategory':
                continue # skip this key as it is already in the totalSpendingByCategory
            else:
                writer.writerow([key, value])

        writer.writerow([''])
        writer.writerow(['Transactions'])
        
        writer.writerow(transactions[0].keys())
        for transaction in transactions:
            writer.writerow(transaction.values())




       
       
        
def get_cached_transactions_csv(accountName: str, year: str, month: str) -> Optional[list[Dict[str, Any]]]:
    """Get cached transactions from local storage as CSV."""

    CACHE_DIR.mkdir(exist_ok=True)
    cache_file = CACHE_DIR / f"transactions_{accountName}_{year}_{month}.csv"
    
    if not os.path.exists(cache_file):
        return None
    
    with open(cache_file, 'r') as f:
        return list(csv.reader(f))