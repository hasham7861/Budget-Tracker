"""List accounts command."""

from budget_tracker.services.plaid_client import PlaidClient
from budget_tracker.utils.storage import get_access_token


def list_accounts() -> None:
    """List all linked bank accounts."""
    access_token = get_access_token()

    if not access_token:
        print("❌ No access token found. Please run 'budget-tracker link' first.")
        return

    try:
        plaid_client = PlaidClient()
        accounts = plaid_client.get_accounts(access_token)

        print(f"\n✅ Found {len(accounts)} account(s):\n")

        for idx, account in enumerate(accounts, 1):
            print(f"{idx}. Account Name: {account['name']}")
            print(f"   Account ID: {account['account_id']}")
            print(f"   Type: {account['type']}")
            print(f"   Subtype: {account.get('subtype', 'N/A')}")

            if 'balances' in account:
                balances = account['balances']
                current = balances.get('current')
                available = balances.get('available')
                currency = balances.get('iso_currency_code', 'CAD')

                if current is not None:
                    print(f"   Current Balance: {current} {currency}")
                if available is not None:
                    print(f"   Available Balance: {available} {currency}")

            print()

        print("\n💡 Tip: Copy one of the account names above and set it in your .env file:")
        print('   ACCOUNT_TO_FILTER="<account-name>"')

    except Exception as error:
        print(f"❌ Failed to list accounts: {error}")
