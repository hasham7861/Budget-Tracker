"""Pull command implementation."""

from typing import Optional
from budget_tracker.services.plaid_client import PlaidClient
from budget_tracker.utils.storage import get_access_token
import os
# TODO: Implement the pull functionality
# This will fetch transactions from Plaid and format them

def pull_statements(year: Optional[str] = None, month: Optional[str] = None, format: str = "json") -> None:
    """Pull monthly bank statements."""
    print(f"Month: {month or 'current'}, Format: {format}")
    
    plaid_client = PlaidClient()
    access_token = get_access_token()
    accounts = plaid_client.get_accounts(access_token)

    accountFindByName = next((account for account in accounts if account['name'] == os.getenv('ACCOUNT_TO_FILTER')), None)
   
    print(f"Account found: {accountFindByName}")

    if not accountFindByName:
        print("❌ Account not found! Check your ACCOUNT_TO_FILTER environment variable.")
        return

    transactions = plaid_client.get_transactions(access_token, accountFindByName['account_id'], year, month)
    print(f"Transactions: {transactions}")
