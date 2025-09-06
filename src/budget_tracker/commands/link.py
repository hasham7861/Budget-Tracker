"""Link command implementation."""

# TODO: Implement the link functionality
# This will create a Plaid link token and provide the URL for account linking

from budget_tracker.services.plaid_client import PlaidClient
import typer


def link_account() -> None:
    """Link RBC bank account via Plaid."""
    plaid_client = PlaidClient()
    link_token = plaid_client.create_link_token()
    typer.echo(f"Public link token: {link_token['link_token']}")
