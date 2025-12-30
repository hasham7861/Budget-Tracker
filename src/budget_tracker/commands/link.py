"""Link bank account command."""

import webbrowser

import typer


def link_account() -> None:
    """Link bank account via Plaid."""
    try:
        typer.echo("🔗 Starting Plaid Link flow...")
        typer.echo("\n📋 Instructions:")
        typer.echo("1. Your browser will open with the Plaid Link interface")
        typer.echo("2. Select your bank from the institution list")
        typer.echo("3. Enter your bank credentials")
        typer.echo("4. Complete the linking process")
        typer.echo("5. The page will automatically exchange and save your token")

        # Open browser to the link page
        link_url = "http://localhost:8000/link"
        typer.echo(f"\n🌐 Opening Plaid Link in your browser...")
        typer.echo(f"If it doesn't open automatically, visit: {link_url}")

        webbrowser.open(link_url)

        typer.echo("\n✅ Browser opened! Complete the linking in your browser.")

    except Exception as error:
        typer.echo(f"❌ Failed to open link: {error}")
        typer.echo("\nManual option: Visit http://localhost:8000/link in your browser")
