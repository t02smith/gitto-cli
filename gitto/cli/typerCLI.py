import typer
from typing import Optional
from gitto.cli.GtoFunctions import *
from rich.console import Console

# SETUP

app = typer.Typer()
console = Console()


# INIT


@app.command(short_help="Initialise a new repository in the current directory")
def init() -> None:
    try:
        init_repo()
        console.print("[green]Repository successfully created[/green]")
    except Exception as e:
        console.print(f"[red]{e}[/red]")


# COMMIT

@app.command()
def commit(
        msg: Optional[str] = typer.Option("", "--message", "-m"),
        autoPush: Optional[bool] = typer.Option(False, "--auto-push", "-p")
) -> None:
    pass


# PUSH

@app.command()
def push() -> None:
    pass
