
from os import path, mkdir, getcwd
from gitto.repo.GtoRepo import GtoRepo
from gitto.repo.GtoErrors import RepoAlreadyInitialised


def init_repo():
    """
    Initialise a gto repository
    :return: void
    """
    if path.exists("./.gto"):
        raise RepoAlreadyInitialised("Repository already initialised")

    mkdir(".gto")
    with GtoRepo(path.split(getcwd())[-1], -1):
        pass


def commit(message: str, autoPush: bool):
    """
    Store all changes since last commit
    :param message: description of changes
    :param autoPush: whether to automatically push to remote
    :return: void
    """
    pass
