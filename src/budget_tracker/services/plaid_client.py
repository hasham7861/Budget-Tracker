"""Plaid API client implementation."""
import os
import uuid
from datetime import date

import plaid
from dotenv import load_dotenv
from plaid.api import plaid_api
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest,
)
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.transaction import Transaction
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.link_token_create_request_update import LinkTokenCreateRequestUpdate

load_dotenv()


def get_plaid_environment():
    """Get Plaid environment based on PLAID_ENV setting."""
    env = os.getenv("PLAID_ENV", "sandbox").lower()
    if env == "production":
        return plaid.Environment.Production
    elif env == "development":
        return plaid.Environment.Development
    else:
        return plaid.Environment.Sandbox


configuration = plaid.Configuration(
    host=get_plaid_environment(),
    api_key={
        "clientId": os.getenv("PLAID_CLIENT_ID"),
        "secret": os.getenv("PLAID_SECRET"),
    },
)


class PlaidClient:
    """Plaid API client for banking operations."""

    def __init__(self) -> None:
        """Initialize the Plaid client."""
        api_client = plaid.ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)

    def create_link_token(self, redirect_uri: str = None, access_token: str = None) -> dict:
        """Create a link token for account linking or update mode."""
        request_params = {
            "user": LinkTokenCreateRequestUser(
                client_user_id=str(uuid.uuid4()),
            ),
            "client_name": "Budget Tracker",
            "products": [Products("transactions")],
            "country_codes": [CountryCode("CA")],
            "language": "en",
        }

        # Add redirect_uri if provided
        if redirect_uri:
            request_params["redirect_uri"] = redirect_uri

        # Add update mode if access_token is provided
        if access_token:
            request_params["access_token"] = access_token
            # Remove products when in update mode
            del request_params["products"]

        request = LinkTokenCreateRequest(**request_params)
        response = self.client.link_token_create(request)
        link_token = response["link_token"]
        result = {
            "link_token": link_token,
        }

        # Only add hosted_link_url if we have the env var and redirect_uri
        if redirect_uri and os.getenv('PLAID_PUBLIC_TOKEN_URL'):
            result["hosted_link_url"] = f"{os.getenv('PLAID_PUBLIC_TOKEN_URL')}{link_token}"

        return result

    def exchange_public_token(self, public_token: str) -> dict:
        """Exchange public token for access token."""
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = self.client.item_public_token_exchange(request)
        access_token = response["access_token"]
        print(f"Access token: {access_token}")
        item_id = response["item_id"]
        return {
            "access_token": access_token,
            "item_id": item_id,
        }

    def get_accounts(self, access_token: str) -> list:
        """Get account information."""
        request = AccountsGetRequest(access_token=access_token)
        response = self.client.accounts_get(request)
        accounts = response["accounts"]
        return accounts

    def get_transactions(
        self, access_token: str, account_id: str, year: str, month: str
    ) -> list[Transaction]:
        """Get transactions for a date range."""

        # Convert strings to date objects
        start_date = date(int(year), int(month), 1)

        # Get last day of month
        if int(month) == 12:
            end_date = date(int(year) + 1, 1, 1) - date.resolution
        else:
            end_date = date(int(year), int(month) + 1, 1) - date.resolution

        request = TransactionsGetRequest(
            access_token=access_token, start_date=start_date, end_date=end_date
        )
        response = self.client.transactions_get(request)
        all_transactions = response["transactions"]

        filtered_transactions = [
            tx for tx in all_transactions if tx.account_id == account_id
        ]
        return filtered_transactions
