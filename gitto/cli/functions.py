from os import mkdir
from gitto.repo.errors import RepoAlreadyInitialised
from gitto.storage.storage import *
from gitto.cli.templates import *
from gitto.cli.rich import console


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
