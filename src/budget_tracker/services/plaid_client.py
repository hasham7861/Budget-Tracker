"""Plaid API client implementation."""
import os
from dotenv import load_dotenv
import uuid
import plaid
from datetime import date
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from typing import Dict, Any
load_dotenv()

# TODO: Implement Plaid API integration
# This will handle all Plaid API calls (create link token, exchange token, get transactions, etc.)

configuration = plaid.Configuration(
    host=plaid.Environment.Production,
    api_key={
        'clientId': os.getenv('PLAID_CLIENT_ID'),
        'secret': os.getenv('PLAID_SECRET'),
    }
)

class PlaidClient:
    """Plaid API client for banking operations."""
    
    def __init__(self) -> None:
        """Initialize the Plaid client."""
        api_client = plaid.ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)
        
    
    def create_link_token(self) -> dict:
        """Create a link token for account linking."""
        request = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(
                client_user_id=str(uuid.uuid4()),
            ),
            client_name='Budget Tracker',
            products=[Products('transactions')],
            country_codes=[CountryCode('CA')],
            language='en',
        )
        response = self.client.link_token_create(request)
        link_token = response['link_token']
        return {
            'link_token': link_token,
            'hosted_link_url': f"{os.getenv('PLAID_PUBLIC_TOKEN_URL')}{link_token}",
        }
    
    def exchange_public_token(self, public_token: str) -> dict:
        """Exchange public token for access token."""
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = self.client.item_public_token_exchange(request)
        access_token = response['access_token']
        print(f"Access token: {access_token}")
        item_id = response['item_id']
        return {
            'access_token': access_token,
            'item_id': item_id,
        }
    
    def get_accounts(self, access_token: str) -> list:
        """Get account information."""
        request = AccountsGetRequest(access_token=access_token)
        response = self.client.accounts_get(request)
        accounts = response['accounts']
        return accounts
    
    def get_transactions(self, access_token: str, account_id: str, year: str, month: str) -> list[Dict[str, Any]]:
        """Get transactions for a date range."""
        
        # Convert strings to date objects
        start_date = date(int(year), int(month), 1)
        
        # Get last day of month
        if int(month) == 12:
            end_date = date(int(year) + 1, 1, 1) - date.resolution
        else:
            end_date = date(int(year), int(month) + 1, 1) - date.resolution
        
        request = TransactionsGetRequest(
            access_token=access_token, 
            start_date=start_date, 
            end_date=end_date
        )
        response = self.client.transactions_get(request)
        all_transactions = response['transactions']
        
        # Filter transactions by account_id and convert Transaction objects to list of dictionaries
        filtered_transactions = [tx.to_dict() for tx in all_transactions if tx.account_id == account_id]
        return filtered_transactions
