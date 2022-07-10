import typer
from typing import Optional
from gitto.cli.functions import *
from rich.console import Console
from gitto.network.requests import push as push_to_remote

# SETUP

app = typer.Typer()
console = Console()


# INIT


@app.command(short_help="Initialise a new repository in the current directory")
def init(
        name: Optional[str] = typer.Option(None, "--name", "-n")
) -> None:
    try:
        init_repo(name)
        console.print("[green]Repository successfully created[/green]")
    except Exception as e:
        console.print(f"[red]{e}[/red]")


# COMMIT

@app.command()
def commit(
        msg: Optional[str] = typer.Option("", "--message", "-m"),
) -> None:
    commit_changes(msg)


# LOG

@app.command()
def log():
    log_commits()


# PUSH

@app.command()
def push():
    push_to_remote()
