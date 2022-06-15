from dataclasses import dataclass
from datetime import datetime
from hashlib import sha1
from functools import lru_cache

"""
All data stored by gitto will need to be turned into some
kind of object that will be compressed and stored in the
.gto/objects folder

"""

BUFFER_SIZE = 65536  # 64kb buffer


@dataclass
class FileObject:
    """
    Represents the contents of a file stored
    """

    filename: str
    hash: str = None

    def __hash__(self):
        """
        The hash is a sha1 hash of the files contents
        :return: hash
        """
        if self.hash is not None:
            return self.hash

        hasher = sha1()
        with open(self.filename, "rb") as f:
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                hasher.update(data)

        self.hash = hasher.hexdigest()
        return self.hash


@dataclass
class TreeObject:
    """
    A tree represents a directory and contains
    files and references to other trees (sub-dirs)
    """

    name: str
    files: list[FileObject]
    trees: list["TreeObject"]
    hash: str = None

    def __hash__(self):
        """
        The hash is composed of the hashes from
        the file list and tree list
        :return: hash
        """
        if self.hash is not None:
            return self.hash

        hasher = sha1()
        hasher.update(bytes(self.name, "utf8"))

        for f in self.files:
            hasher.update(bytes(f.__hash__(), "utf8"))

        for t in self.trees:
            hasher.update(bytes(t.__hash__(), "utf8"))

        self.hash = hasher.hexdigest()
        return self.hash


@dataclass
class CommitObject:
    """

    """

    author: str
    message: str
    parent_hash: str
    timestamp: datetime
    tree_hash: str
    hash: str = None

    def __hash__(self):
        """
        The hash is composed of the object's attributes
        and the hash of the tree
        :return: hash
        """
        if self.hash is not None:
            return self.hash

        hasher = sha1()
        hasher.update(bytes(self.author, "utf8"))
        hasher.update(bytes(self.message, "utf8"))
        hasher.update(bytes(self.parent_hash, "utf8"))
        hasher.update(self.timestamp)
        hasher.update(bytes(self.tree_hash, "utf8"))

        self.hash = hasher.hexdigest()
        return self.hash
