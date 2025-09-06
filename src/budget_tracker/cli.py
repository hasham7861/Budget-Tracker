"""Main CLI entry point for Budget Tracker."""

import typer
from typing import Optional
from budget_tracker.commands.link import link_account
from dotenv import load_dotenv

load_dotenv()

# Create the main CLI app
app = typer.Typer(
    name="budget-tracker",
    help="Budget Tracker CLI - Connect to RBC via Plaid API",
    add_completion=False,
)

@app.command()
def link() -> None:
    """Link your RBC bank account (placeholder for now)."""
    typer.echo("🔗 Link command - Coming soon!")
    typer.echo("This will connect to your RBC account via Plaid.")
    link_account()


@app.command()
def exchange(public_token: str) -> None:
    """Exchange public token for access token (placeholder for now)."""
    typer.echo(f"🔄 Exchange command - Coming soon!")
    typer.echo(f"Public token received: {public_token[:20]}...")


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


def main() -> None:
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
