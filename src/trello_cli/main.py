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

@app.command()
def labels(
    board_id: Annotated[str, typer.Option("--board-id", "-b", help="ID of the Trello board")],
    api_key: Annotated[str, typer.Option("--api-key", envvar="TRELLO_API_KEY")] = None,
    token: Annotated[str, typer.Option("--token", envvar="TRELLO_TOKEN")] = None
):
    """List all labels in a specific Trello board."""
    trello = get_trello_client(api_key, token)
    
    try:
        label_list = trello.get_labels_in_board(board_id)
        
        table = Table(title=f"Labels in Board {board_id}")
        table.add_column("Name", style="cyan")
        table.add_column("Label ID", style="magenta")
        table.add_column("Color", style="green")
        
        for label in label_list:
            table.add_row(label['name'], label['id'], label['color'])
        
        console.print(table)
    except Exception as e:
        typer.echo(f"Error retrieving labels: {str(e)}")
        raise typer.Exit(1)

@app.command()
def view_cards(
    list_id: Annotated[str, typer.Option("--list-id", "-l", help="ID of the Trello list")],
    api_key: Annotated[str, typer.Option("--api-key", envvar="TRELLO_API_KEY")] = None,
    token: Annotated[str, typer.Option("--token", envvar="TRELLO_TOKEN")] = None
):
    """View all the cards in a specific list."""
    trello = get_trello_client(api_key, token)

    try:
        cards = trello.get_cards_in_list(list_id)

        if not cards:
            typer.echo("The list does not contain any cards yet")
            return

        table = Table(title=f"Cards in list: {trello.get_list_name(list_id)}[{list_id}]")
        table.add_column("Card ID", style="cyan")   
        table.add_column("Name", style="magenta")   
        table.add_column("URL", style="green")

        for card in cards:
            table.add_row(card['id'], card['name'], card['shortUrl'])
        console.print(table)

    except Exception as e:
        typer.echo(f"Error displaying the cards in list: {str(e)}")
        raise typer.Exit(1)

@app.command()
def search(
    query: Annotated[str, typer.Option("--query", "-q", help="Query string to search for")],
    api_key: Annotated[str, typer.Option("--api-key", envvar="TRELLO_API_KEY")] = None,
    token: Annotated[str, typer.Option("--token", envvar="TRELLO_TOKEN")] = None
):
    """Search for a card using a query string across all your boards"""
    trello = get_trello_client(api_key, token)

    try:
        search_results = trello.search_cards(query)

        if not search_results:
            typer.echo(f"No cards found for the query string: {query}")
            return

        table = Table(title=f"Card results for the query string: {query}")
        table.add_column("Card ID", style="cyan")   
        table.add_column("Name", style="magenta")   
        table.add_column("URL", style="green")

        for result in search_results:
            table.add_row(result['id'], result['name'], result['shortUrl'])
        
        console.print(table)
    except Exception as e:
        typer.echo(f"Error retrieving search results: {str(e)}")
        raise typer.Exit(1)   

@app.command()
def add_card(
    list_id: Annotated[str, typer.Option("--list-id", "-l", help="ID of the Trello list")],
    name: Annotated[str, typer.Option("--name", "-n", help="Name of the card")],
    labels: Annotated[List[str], typer.Option("--label", "-lb", help="Label IDs to add to the card")] = None,
    comment: Annotated[str, typer.Option("--comment", "-c", help="Comment to add to the card")] = None,
    api_key: Annotated[str, typer.Option("--api-key", envvar="TRELLO_API_KEY")] = None,
    token: Annotated[str, typer.Option("--token", envvar="TRELLO_TOKEN")] = None
):
    """Add a new card to a Trello list with optional labels and comment."""
    trello = get_trello_client(api_key, token)

    try:
        card = trello.create_card(list_id, name, labels, comment)
        typer.echo(f"Successfully created card: {card['shortUrl']}")
    except Exception as e:
        typer.echo(f"Error creating card: {str(e)}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()