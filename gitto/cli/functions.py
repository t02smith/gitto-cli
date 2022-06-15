import datetime
from os import path, mkdir, getcwd
from gitto.repo.repo import GtoRepo, openRepo, GtoCommit
from gitto.repo.errors import RepoAlreadyInitialised


def init_repo():
    """
    Initialise a gto repository
    :return: void
    """
    if path.exists("./.gto"):
        raise RepoAlreadyInitialised("Repository already initialised")

    mkdir(".gto")
    mkdir(".gto/objects")


def commit(message: str, autoPush: bool):
    """
    Store all changes since last commit
    :param message: description of changes
    :param autoPush: whether to automatically push to remote
    :return: void
    """
    with openRepo() as repo:
        curr_commit = GtoCommit()
        curr_commit.message = message
        curr_commit.message = datetime.datetime.now()

        # auto add files

        # check for changes
