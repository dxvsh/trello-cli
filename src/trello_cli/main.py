import os
import typer
from typing import List, Optional
from typing_extensions import Annotated
from rich.console import Console
from rich.table import Table
from .trello_api import TrelloAPI


app = typer.Typer(
    name="trello-cli",
    help="CLI tool for managing Trello cards and boards",
)
console = Console()

def get_trello_client(api_key: Optional[str], token: Optional[str]) -> TrelloAPI:
    """Helper function to create TrelloAPI client with error handling."""
    # Use provided values or fall back to environment variables
    final_api_key = api_key or os.getenv("TRELLO_API_KEY")
    final_token = token or os.getenv("TRELLO_TOKEN")
    
    if not final_api_key or not final_token:
        typer.echo(
            "Error: API key and token are required. Either:\n"
            "1. Set them via environment variables (.bashrc/.zshrc/etc):\n"
            "   TRELLO_API_KEY=your_key\n"
            "   TRELLO_TOKEN=your_token\n"
            "2. Or provide them as command line options:\n"
            "   --api-key and --token"
        )
        raise typer.Exit(1)
    
    return TrelloAPI(final_api_key, final_token)


@app.command()
def boards(
    api_key: Annotated[str, typer.Option("--api-key", envvar="TRELLO_API_KEY")] = None,
    token: Annotated[str, typer.Option("--token", envvar="TRELLO_TOKEN")] = None
):
    """List all Trello boards for the current user."""
    trello = get_trello_client(api_key, token)
    
    try:
        board_list = trello.get_boards()
        
        # Use rich for nice formatting
        table = Table(title="Your Trello Boards")
        table.add_column("Name", style="cyan")
        table.add_column("Board ID", style="magenta")
        
        for board in board_list:
            table.add_row(board['name'], board['id'])
        
        console.print(table)
    except Exception as e:
        typer.echo(f"Error retrieving boards: {str(e)}")
        raise typer.Exit(1)

@app.command()
def lists(
    board_id: Annotated[str, typer.Option("--board-id", "-b", help="ID of the Trello board")],
    api_key: Annotated[str, typer.Option("--api-key", envvar="TRELLO_API_KEY")] = None,
    token: Annotated[str, typer.Option("--token", envvar="TRELLO_TOKEN")] = None
):
    """List all lists in a specific Trello board."""
    trello = get_trello_client(api_key, token)
    
    try:
        board_lists = trello.get_lists_in_board(board_id)
        
        table = Table(title=f"Lists in Board {board_id}")
        table.add_column("Name", style="cyan")
        table.add_column("List ID", style="magenta")
        
        for lst in board_lists:
            table.add_row(lst['name'], lst['id'])
        
        console.print(table)
    except Exception as e:
        typer.echo(f"Error retrieving lists: {str(e)}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()