
from gitto.storage.objects import *
from os.path import isdir, exists
from os import mkdir
from zlib import compress, decompress


def object_exists(obj_hash: str):

    # check if identical object exists
    if exists(f".gto/objects/{obj_hash[:2]}/{obj_hash[2:]}"):
        return True

    # create object directory
    if not isdir(f".gto/objects/{obj_hash[:2]}"):
        mkdir(f".gto/objects/{obj_hash[:2]}")

    return False


# Writer functions


def write_file(file: FileObject):
    """
    Writes a FileObject to the object folder
    :param file: the file to be written
    :return: void
    """
    file_hash = file.__hash__()
    if object_exists(file_hash):
        return

    with open(file.filename, "rb") as readFrom:
        with open(f".gto/objects/{file_hash[:2]}/{file_hash[2:]}", "xb") as writeTo:
            while True:
                data = readFrom.read(BUFFER_SIZE)
                if not data:
                    break
                writeTo.write(compress(data, 9))


def write_tree(tree: TreeObject):
    tree_hash = tree.__hash__()
    if object_exists(tree_hash):
        return

    with open(f".gto/objects/{tree_hash[:2]}/{tree_hash[2:]}", "xb") as writeTo:

        data = tree.name
        for f in tree.files:
            data += f"\nfile {f.__hash__()} {f.filename}"

        for t in tree.trees:
            data += f"\ntree {t.__hash__()} {t.name}\n"

        writeTo.write(compress(bytes(data, "utf8"), 9))


def write_commit(commit: CommitObject):
    c_hash = commit.__hash__()
    if object_exists(c_hash):
        return

    with open(f".gto/objects/{c_hash[:2]}/{c_hash[2:]}", "xb") as writeTo:
        pass


# Reader function

def read_object(obj_hash: str):
    output = ""
    with open(f".gto/objects/{obj_hash[:2]}/{obj_hash[2:]}", "rb") as f:
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            output += decompress(data).decode()
    return output
