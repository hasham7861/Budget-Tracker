"""Pull command implementation."""

import os
from typing import Optional

from budget_tracker.services.plaid_client import PlaidClient
from budget_tracker.utils.storage import (
    get_access_token,
    get_cached_transactions,
    save_cached_transactions,
    save_cached_transactions_csv,
)


def pull_statements(
    year: Optional[str] = None, month: Optional[str] = None, format: str = "json"
) -> None:
    """Pull monthly bank statements."""
    print(f"Month: {month or 'current'}, Format: {format}")

    plaid_client = PlaidClient()
    access_token = get_access_token()
    accounts = plaid_client.get_accounts(access_token)

    accountFindByName = next(
        (
            account
            for account in accounts
            if account["name"] == os.getenv("ACCOUNT_TO_FILTER")
        ),
        None,
    )

    if not accountFindByName:
        print(
            "❌ Account not found! Check your ACCOUNT_TO_FILTER environment variable."
        )
        return

    transactions = get_cached_transactions(accountFindByName["name"], year, month)
    if transactions:
        print(f"✅ Found cached transactions: {len(transactions)} transactions")
    else:
        print("❌ No cached transactions found")
        transactions = plaid_client.get_transactions(
            access_token, accountFindByName["account_id"], year, month
        )
        transactions = [tx.to_dict() for tx in transactions]
        save_cached_transactions(accountFindByName["name"], year, month, transactions)

        transactionsPartialData = []
        for tx in transactions:
            if tx and tx.get("amount", 0) > 0:
                pfc = tx.get("personal_finance_category") or {}
                transactionsPartialData.append(
                    {
                        "date": tx["date"],
                        "description": tx["name"],
                        "amount": tx["amount"],
                        "category": pfc.get("primary", "Unknown"),
                        "subcategory": pfc.get("detailed", "Unknown"),
                        "category_confidence": pfc.get("confidence_level", "Unknown"),
                    }
                )

        categories = set(tx["category"] for tx in transactionsPartialData)
        summaryData = {
            "totalSpending": sum(
                transaction["amount"]
                for transaction in transactions
                if transaction and transaction.get("amount", 0) > 0
            ),
            "transactionCount": len(transactions),
            "totalSpendingByCategory": {
                category: sum(
                    transaction["amount"]
                    for transaction in transactions
                    if transaction
                    and transaction.get("amount", 0) > 0
                    and (transaction.get("personal_finance_category") or {}).get(
                        "primary"
                    )
                    == category
                )
                for category in categories
            },
            "totalTransactionsCountByCategory": {
                category: sum(
                    1
                    for transaction in transactions
                    if transaction
                    and transaction.get("amount", 0) > 0
                    and (transaction.get("personal_finance_category") or {}).get(
                        "primary"
                    )
                    == category
                )
                for category in categories
            },
        }

        save_cached_transactions_csv(
            accountFindByName["name"], year, month, transactionsPartialData, summaryData
        )

    totalSpending = sum(
        transaction["amount"]
        for transaction in transactions
        if transaction["amount"] > 0
    )
    print(f"Total spending: {totalSpending}")
