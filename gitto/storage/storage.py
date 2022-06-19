import datetime
import os
import pathspec
from gitto.storage.objects import *
from zlib import compress
from gitto.storage.storage_info import *
from gitto.storage.util import *

OBJECTS_FOLDER = ".gto/objects"

# Writer functions


def write_file(file: FileObject, obj_folder: str = OBJECTS_FOLDER):
    """
    Writes a FileObject to the object folder
    :param obj_folder: location of objects folder
    :param file: the file to be written
    :return: void
    """
    if file is None:
        raise TypeError("Cannot write None file object")

    file_hash = file.__hash__()
    if object_exists(file_hash):
        return

    os.mkdir(os.path.join(obj_folder, file_hash[:2]))

    with open(file.filename, "rb") as readFrom:
        with open(os.path.join(obj_folder, file_hash[:2], file_hash[2:]), "xb") as writeTo:
            while True:
                data = readFrom.read(BUFFER_SIZE)
                if not data:
                    break
                writeTo.write(compress(data, 9))


def write_tree(tree: TreeObject, obj_folder: str = OBJECTS_FOLDER):
    tree_hash = tree.__hash__()
    if object_exists(tree_hash):
        return

    with open(f"{obj_folder}/{tree_hash[:2]}/{tree_hash[2:]}", "xb") as writeTo:

        data = tree.name
        for f in tree.files:
            data += f"\nfile {f.__hash__()} {f.filename}"

        for t in tree.trees:
            data += f"\ntree {t.__hash__()} {t.name}"

        writeTo.write(compress(bytes(data, "utf8"), 9))

    for f in tree.files:
        write_file(f)

    for t in tree.trees:
        write_tree(t)


def write_commit(commit: CommitObject, obj_folder: str = OBJECTS_FOLDER):
    c_hash = commit.__hash__()
    if object_exists(c_hash):
        return

    # TODO write a commit to storage
    with open(f"{obj_folder}/{c_hash[:2]}/{c_hash[2:]}", "xb") as writeTo:
        pass


# Generator functions

def generate_commit(author: str, message: str = None):
    info = read_info()

    ts = datetime.datetime.now()
    # find parent tree
    if info is not None and info.last_commit is not None:
        parent = read_object(info.last_commit)

    # generate tree
    tree = generate_tree()

    # find changes
    pass


def generate_tree():
    """
    Generate a list of tree and file objects
    Reads the contents of the .gtoignore file
    :return: the root tree object
    """

    # read .ignore file
    if os.path.exists(".gtoignore"):
        with open(".gtoignore", "r") as g:
            spec = pathspec.PathSpec.from_lines("gitwildmatch", g.readlines())
        return _generate_tree(".", spec)

    return _generate_tree(".")


def _generate_tree(root_dir: str, spec: pathspec.PathSpec = None) -> TreeObject:
    """
    Recursively generate a tree object
    !! should only be used via the generate_objects function
    :param root_dir: the directory to generate the tree from
    :param spec: the spec to ignore any ignored files
    :return: a tree of the cwd
    """
    tree = TreeObject(name=root_dir)

    # discover valid directories and files in cwd
    objects = set(os.listdir(root_dir))

    for o in objects:
        path = os.path.join(root_dir, o)
        if spec is None or not spec.match_file(path):
            if os.path.isdir(path):
                tree.trees.append(_generate_tree(path, spec))
            else:
                tree.files.append(
                    FileObject(filename=path))

    return tree
