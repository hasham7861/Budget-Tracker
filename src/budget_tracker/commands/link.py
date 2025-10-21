"""Link bank account command."""

import webbrowser

import typer

from budget_tracker.services.plaid_client import PlaidClient


def link_account() -> None:
    """Link RBC bank account via Plaid."""
    try:
        typer.echo("Creating link token for RBC connection...")

        # Create Plaid client and get link token (no callback needed)
        plaid_client = PlaidClient()
        link_token_response = plaid_client.create_link_token()
        link_token = link_token_response["link_token"]
        link_url = link_token_response["hosted_link_url"]

        typer.echo("\n🔗 Link Token Created Successfully!")
        typer.echo(f"Link Token: {link_token}")

        typer.echo("\n📋 Next Steps:")
        typer.echo(f"1. Go to: {link_url}")
        typer.echo("2. Select 'Royal Bank of Canada' from the institution list")
        typer.echo("3. For SANDBOX testing, use these credentials:")
        typer.echo("   Username: user_good")
        typer.echo("   Password: pass_good")
        typer.echo("4. Complete the linking process")
        typer.echo("5. Copy the public_token from the browser network tab")
        typer.echo("6. Use it with: budget-tracker exchange <public_token>")

        # Open browser
        typer.echo("\n🌐 Opening Plaid Link in your browser...")
        webbrowser.open(link_url)

    except Exception as error:
        typer.echo(f"❌ Failed to create link token: {error}")
