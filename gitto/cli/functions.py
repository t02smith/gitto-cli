from os import mkdir
from rich.table import Table
from gitto.repo.errors import RepoAlreadyInitialised
from gitto.storage.storage import *
from gitto.cli.templates import *
from gitto.cli.rich import console
from gitto.storage.info import *


def init_repo():
    """
    Initialise a gto repository
    :return: void
    """
    if path.exists("./.gto"):
        raise RepoAlreadyInitialised("Repository already initialised")

    mkdir(".gto")
    mkdir(".gto/objects")


def commit_changes(message: str):
    """
    Store all changes since last commit
    :param message: description of changes
    :return: void
    """
    console.print(template_commit(generate_commit("t02smith", message)))


def log_commits():
    """
    Output a list of commits from the most current one
    :return: void
    """
    info = read_info()
    commit = parse_commit(read_object(info.last_commit))
    if commit is None:
        console.print("[bold red]No commits found[/bold red]")

    table = Table(title="Commit History")
    table.add_column("[green bold]Date[/green bold]", width=10)
    table.add_column("[green bold]Time[/green bold]", width=10)
    table.add_column("[red bold]author[/red bold]", width=12)
    table.add_column("[blue bold]message[/blue bold]", width=50)

    def get_date(timestamp: datetime):
        return f"{timestamp.day}/{timestamp.month}/{timestamp.year}"

    def get_time(timestamp: datetime):
        return f"{str(timestamp.hour).rjust(2, '0')}:{str(timestamp.minute).rjust(2, '0')}"

    table.add_row(get_date(commit.timestamp), get_time(commit.timestamp), commit.author, commit.message)
    while commit.parent_hash is not None:
        commit = parse_commit(read_object(commit.parent_hash))
        table.add_row(get_date(commit.timestamp), get_time(commit.timestamp), commit.author, commit.message)

    console.print(table)
