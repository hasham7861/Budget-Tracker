"""Service layer for Plaid operations."""
from budget_tracker_api.app.services.plaid_client import PlaidClient
from budget_tracker_api.app.utils.storage import get_access_token, save_access_token


class PlaidService:
    """High-level service for Plaid operations."""

    def __init__(self):
        self.client = PlaidClient()

    def create_link_token(self) -> dict:
        """Create a link token for account linking."""
        return self.client.create_link_token(redirect_uri=None)

    def create_update_link_token(self) -> tuple[dict, int, str]:
        """
        Create a link token for re-authentication (update mode).
        Returns: (response_data, status_code, error_message)
        """
        access_token = get_access_token()
        if not access_token:
            return (
                None,
                404,
                "No access token found. Please link an account first at /link",
            )

        try:
            response = self.client.create_link_token(
                redirect_uri=None, access_token=access_token
            )
            return response, 200, None
        except Exception as e:
            return None, 500, str(e)

    def exchange_public_token(self, public_token: str) -> tuple[dict, int, str]:
        """
        Exchange public token for access token and save it.
        Returns: (response_data, status_code, error_message)
        """
        if not public_token:
            return None, 400, "public_token is required"

        try:
            result = self.client.exchange_public_token(public_token)
            save_access_token(result["access_token"], result["item_id"])
            return {
                "success": True,
                "item_id": result["item_id"],
                "access_token": result["access_token"]
            }, 200, None
        except Exception as e:
            return None, 500, str(e)
