import datetime
import pathspec
from gitto.storage.objects import *
from zlib import compress
from gitto.storage.info import *
from gitto.storage.util import *
from gitto.cli.rich import console

# Writer functions


def write_file(file: FileObject, obj_folder: str = OBJECTS_FOLDER):
    """
    Writes a FileObject to the object folder
    :param obj_folder: locations of objects folder
    :param file: the file to be written
    :return: void
    """
    if file is None:
        raise TypeError("Cannot write None file object")

    file_hash = file.__hash__()
    if object_exists(file_hash, obj_folder=obj_folder):
        return

    if not os.path.exists(os.path.join(obj_folder, file_hash[:2])):
        os.mkdir(os.path.join(obj_folder, file_hash[:2]))

    console.print(f"[green]Writing file: {file.__hash__()} {file.filename}[/green]")

    with open(file.filename, "rb") as readFrom:
        with open(os.path.join(obj_folder, file_hash[:2], file_hash[2:]), "xb") as writeTo:
            while True:
                data = readFrom.read(BUFFER_SIZE)
                if not data:
                    break
                writeTo.write(compress(data, 9))


def write_tree(tree: TreeObject, obj_folder: str = OBJECTS_FOLDER):
    if tree is None:
        raise TypeError("Cannot write None file object")

    tree_hash = tree.__hash__()
    if object_exists(tree_hash):
        return

    if not os.path.exists(os.path.join(obj_folder, tree_hash[:2])):
        os.mkdir(os.path.join(obj_folder, tree_hash[:2]))

    console.print(f"[blue]Writing tree: {tree.__hash__()} {tree.name}[/blue]")

    with open(os.path.join(obj_folder, tree_hash[0:2], tree_hash[2:]), "xb") as writeTo:

        data = tree.name
        for f in tree.files:
            data += f"\nfile {f.__hash__()} {f.filename}"

        for t in tree.trees:
            data += f"\ntree {t.__hash__()} {t.name}"

        writeTo.write(compress(bytes(data, "utf8"), 9))

    for f in tree.files:
        write_file(f, obj_folder=obj_folder)

    for t in tree.trees:
        write_tree(t, obj_folder=obj_folder)


def write_commit(commit: CommitObject, obj_folder: str = OBJECTS_FOLDER):
    """
    Write a commit to an object file
    :param commit: commit to write
    :param obj_folder: where objects are stored
    :return: void
    """
    c_hash = commit.__hash__()
    if object_exists(c_hash):
        return

    if not os.path.exists(os.path.join(obj_folder, c_hash[:2])):
        os.mkdir(os.path.join(obj_folder, c_hash[:2]))

    with open(os.path.join(obj_folder, c_hash[0:2], c_hash[2:]), "xb") as writeTo:
        data = f"{commit.timestamp.isoformat()}\n" \
               f"{commit.author}\n" \
               f"{'None' if commit.parent_hash is None else commit.parent_hash}\n" \
               f"{commit.tree.__hash__()}\n" \
               f"{commit.message}"
        writeTo.write(compress(bytes(data, "utf8"), 5))

# Generator functions


def generate_commit(author: str, message: str = None):
    """
    Generates a commit given the current working directory
    :param author: who wrote the code
    :param message: the contextual message
    :return: Commit object
    """
    info = read_info()

    c = CommitObject(
        author=author,
        message=message,
        parent_hash=None if info.last_commit is None else info.last_commit,
        timestamp=datetime.now(),
        tree=generate_tree())

    write_tree(c.tree)
    write_commit(c)

    info.last_commit = c.__hash__()
    write_info(info)

    return c


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
        filepath = os.path.join(root_dir, o)
        if spec is None or not spec.match_file(filepath):
            if os.path.isdir(filepath):
                tree.trees.append(_generate_tree(filepath, spec))
            else:
                tree.files.append(
                    FileObject(filename=filepath))

    return tree


def diff(blob: FileObject, new:  FileObject, show_unchanged: bool = True):
    """
    Shows differences between two (of the same) files
    :param blob: the original copy
    :param new: the new copy of the file
    :param show_unchanged: whether to print only the changed files or not
    :return: void
    """
    with open(os.path.join(OBJECTS_FOLDER, blob.__hash__()[:2], blob.__hash__()[2:]), "rb") as f:
        blob_data = decompress(f.read()).decode().splitlines()

    with open(new.filename, "r") as f:
        new_data = f.read().splitlines()

    insertions = 0
    removals = 0

    for i in range(max(len(blob_data), len(new_data))):
        if i >= len(blob_data):
            console.print(f"{str(i + 1).ljust(4, ' ')} [green]{new_data[i]}[/green]")
            insertions += 1
        elif i > len(new_data):
            console.print(f"{str(i + 1).ljust(4, ' ')} [red]{blob_data[i]}[/red]")
            removals += 1
        elif blob_data[i] != new_data[i]:
            console.print(f"{str(i+1).ljust(4, ' ')} [red]{blob_data[i]}[/red]")
            console.print(f"{str(i+1).ljust(4, ' ')} [green]{new_data[i]}[/green]")
            insertions += 1
            removals += 1
        elif show_unchanged:
            console.print(f"{str(i+1).ljust(4, ' ')} {blob_data[i]}")

    console.print(f"\n[red]lines removed: {removals}[/red]")
    console.print(f"[green]lines added: {insertions}[/green]")