import os
from dataclasses import dataclass
from gitto.repo.errors import *
from os import path
import json
from datetime import datetime


class GtoRepo:
    def __init__(self, name: str, repoId: int) -> None:
        self.name = name
        self.id = repoId
        self.files = set()
        self.commits = []

    def add(self, filename: str):
        """
        Add a new file to the repository
        :param filename: the name of the file to add
        :return: void
        """
        if filename not in self.files:
            self.files.add(filename)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        saveRepo(self)


@dataclass
class GtoCommit:
    message: str
    timestamp: datetime
    changes: str


@dataclass
class Changes:
    filename: str


# IO

def openRepo() -> GtoRepo:
    """
    Opens the current repo if it exists
    :return: the repo object
    """
    if not path.exists("./.gto"):
        raise RepoNotInitialisedError("No repository found\nRun 'gto init'")
    if not path.exists("./.gto/repo.json"):
        raise RepoError("Error loading repository")

    with open("./.gto/repo.json", "r") as file:
        data = json.loads(file.read())

    repo = GtoRepo(data["name"], data["id"])
    repo.files = data["files"]
    return repo


def saveRepo(repo: GtoRepo):
    """
    Save repo information to repo.json file
    :param repo: the repo object
    :return: void
    """
    if not path.exists("./.gto"):
        raise RepoAlreadyInitialised("No repository found\nRun 'gto init'")

    with open("./.gto/repo.json", "w") as file:
        json.dump(repo.__dict__, file)

# file IO
