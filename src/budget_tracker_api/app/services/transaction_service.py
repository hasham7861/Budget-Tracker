"""Service layer for transaction operations."""
import logging
import os

from budget_tracker_api.app.services.plaid_client import PlaidClient
from budget_tracker_api.app.utils.storage import (
    get_access_token,
    get_cached_transactions,
    save_cached_transactions,
)

logger = logging.getLogger(__name__)


class TransactionService:
    """High-level service for transaction operations."""

    def __init__(self):
        self.client = PlaidClient()

    def get_transactions(self, year: str, month: str) -> tuple[list, int, str]:
        """
        Get transactions for specified year and month.
        Returns: (transactions, status_code, error_message)
        """
        try:
            access_token = get_access_token()
            if not access_token:
                return (
                    None,
                    404,
                    "No access token found. Please link an account first.",
                )

            # Get accounts
            accounts = self.client.get_accounts(access_token)

            # Find the account to filter
            account_filter = os.getenv("ACCOUNT_TO_FILTER")
            account = next(
                (acc for acc in accounts if acc["name"] == account_filter),
                None,
            )

            if not account:
                logger.error(f"Account '{account_filter}' not found")
                available = [acc["name"] for acc in accounts]
                logger.error(f"Available accounts: {available}")
                return (
                    None,
                    404,
                    f"Account '{account_filter}' not found. "
                    f"Available accounts: {available}",
                )

            # Check cache first
            transactions = get_cached_transactions(account["name"], year, month)

            if not transactions:
                # Fetch from Plaid if not cached
                logger.info(f"Fetching transactions from Plaid for {year}-{month}")
                transactions = self.client.get_transactions(
                    access_token, account["account_id"], year, month
                )
                transactions = [tx.to_dict() for tx in transactions]
                save_cached_transactions(account["name"], year, month, transactions)
            else:
                count = len(transactions)
                logger.info(f"Using cached transactions: {count} transactions")

            return transactions, 200, None

        except Exception as e:
            logger.error(f"Failed to fetch transactions: {e}", exc_info=True)
            return None, 500, str(e)
