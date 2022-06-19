import os
from dataclasses import dataclass, field
from datetime import datetime
from hashlib import sha1
from gitto.storage.util import read_object

"""
All data stored by gitto will need to be turned into some
kind of object that will be compressed and stored in the
.gto/objects folder

"""

BUFFER_SIZE = 65536  # 64kb buffer

"""

Files:
the compressed contents of a committed file at the time it was committed
file format: none

"""


@dataclass
class FileObject:
    """
    Represents the contents of a file stored
    """
    filename: str
    _last_updated: datetime
    _hash: str

    def __init__(self, filename: str, _hash: str = None):
        if not os.path.exists(filename):
            raise FileNotFoundError

        self.filename = filename
        self._last_updated = datetime.fromtimestamp(os.stat(filename).st_mtime)
        self._hash = _hash

    def __hash__(self):
        """
        The hash is a sha1 hash of the files contents
        :return: hash
        """
        if self._hash is not None:
            timestamp = datetime.fromtimestamp(os.stat(self.filename).st_mtime)
            if timestamp > self._last_updated:
                self._last_updated = timestamp
            else:
                return self._hash

        hasher = sha1()
        with open(self.filename, "rb") as f:
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                hasher.update(data)

        self._hash = hasher.hexdigest()
        return self._hash


"""

Trees:
the directory structure at the time of a given commit 
includes references to file and tree objects where appropriate
file format: (x files, y sub-dirs)
    1.    folder name from repo root
    2.    file file_hash file_name
    ....
    x+1.  file file_hash file_name
    x+2   tree tree_hash tree_dir_name
    x+y+2 tree tree_hash tree_dir_name

"""


@dataclass
class TreeObject:
    """
    A tree represents a directory and contains
    files and references to other trees (sub-dirs)
    """

    name: str
    files: list[FileObject] = field(default_factory=list)
    trees: list["TreeObject"] = field(default_factory=list)
    _hash: str = None

    def __hash__(self):
        """
        The hash is composed of the hashes from
        the file list and tree list
        :return: hash
        """
        if self._hash is not None:
            return self._hash

        hasher = sha1()
        hasher.update(bytes(self.name, "utf8"))

        for f in self.files:
            hasher.update(bytes(f.__hash__(), "utf8"))

        for t in self.trees:
            hasher.update(bytes(t.__hash__(), "utf8"))

        self._hash = hasher.hexdigest()
        return self._hash


def parse_tree(tree_hash: str, data: str) -> TreeObject:
    """
    uses data from a tree object file and generates a TreeObject
    will recursively load other trees
    :param tree_hash: current tree's hash
    :param data: data from tree object file
    :return: the given tree object
    """
    lines = data.splitlines()

    t = TreeObject(name=lines[0], _hash=tree_hash)
    for lineNo, line in enumerate(lines, start=1):
        cols = line.split(" ")
        match cols[0]:
            case "file":
                t.files.append(FileObject(filename=cols[2], _hash=cols[1]))
            case "tree":
                t.trees.append(parse_tree(cols[2],read_object(cols[1])))

    return t


@dataclass
class CommitObject:
    """
    Represents a snapshot of the code at a given point in time
    """

    author: str
    message: str
    parent_hash: str
    timestamp: datetime
    tree_hash: str
    _hash: str = None

    def __hash__(self):
        """
        The hash is composed of the object's attributes
        and the hash of the tree
        :return: hash
        """
        if self._hash is not None:
            return self._hash

        hasher = sha1()
        hasher.update(bytes(self.author, "utf8"))
        hasher.update(bytes(self.message, "utf8"))
        hasher.update(bytes(self.parent_hash, "utf8"))
        hasher.update(self.timestamp)
        hasher.update(bytes(self.tree_hash, "utf8"))

        self._hash = hasher.hexdigest()
        return self._hash


def parse_commit(data: str):
    # TODO parse commit file
    pass