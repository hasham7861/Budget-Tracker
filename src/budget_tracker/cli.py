"""Main CLI entry point for Budget Tracker."""

import typer
from typing import Optional
from budget_tracker.commands.link import link_account
from budget_tracker.commands.exchange import exchange_public_token
from budget_tracker.commands.pull import pull_statements
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = typer.Typer(
    name="budget-tracker",
    help="Budget Tracker CLI - Connect to RBC via Plaid API",
    add_completion=False,
)

@app.command()
def link() -> None:
    """Link your RBC bank account.""" 
    typer.echo("This will create public token for account linking.")
    link_account()


@app.command()
def exchange(public_token: str) -> None:
    """Exchange public token for access token."""
    exchange_public_token(public_token)


@app.command()
def pull(
    month: Optional[str] = typer.Option(
        None, 
        "--month", 
        "-m", 
        help="Month to pull (YYYY-MM format)"
    ),
    format: str = typer.Option(
        "json", 
        "--format", 
        "-f", 
        help="Output format (json or csv)"
    ),
) -> None:
    """Pull monthly statements (placeholder for now)."""
    typer.echo(f"📊 Pull command - Coming soon!")
    typer.echo(f"Month: {month or 'current'}")
    typer.echo(f"Format: {format}")

    if month:
        year, month = month.split('-')
    else:
        year = datetime.now().year
        month = datetime.now().month
    
    pull_statements(year, month, format)


def main() -> None:
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
