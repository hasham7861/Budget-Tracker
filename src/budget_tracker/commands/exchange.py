"""Exchange public token command."""

import typer
from budget_tracker.services.plaid_client import PlaidClient
from budget_tracker.utils.storage import save_access_token

def exchange_public_token(public_token: str) -> None:
    """Exchange public token for access token."""
    try:
        typer.echo("Exchanging public token...")
        
        plaid_client = PlaidClient()
        result = plaid_client.exchange_public_token(public_token)
        
        # Save the access token
        save_access_token(result['access_token'], result['item_id'])
        
        typer.echo("✅ Success! Your RBC account is now linked and ready to use.")
        typer.echo(f"Item ID: {result['item_id']}")
        typer.echo("\n🎉 You can now pull your statements with: budget-tracker pull")
        
    except Exception as error:
        typer.echo(f"❌ Failed to exchange token: {error}")