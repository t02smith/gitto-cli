import pytest
from gitto.storage.objects import *
from gitto.storage.storage import *
import gitto.storage.util
import os


@pytest.fixture()
def tmpdir(tmp_path):
    """
    Creates a temporary directory
    :param tmp_path: tmp_path object where the tmpdir is located
    :return: tmp_path
    """
    gto = tmp_path / ".gto"
    gto.mkdir()
    objects = gto / "objects"
    objects.mkdir()
    return tmp_path


@pytest.fixture()
def objects(tmpdir):
    """
    Returns the object folder path
    :param tmpdir: tmpdir object
    :return: the object folder location as a string
    """
    return os.path.join(tmpdir.__str__(), ".gto", "objects")

# test file


@pytest.fixture()
def test_file(tmpdir):
    """
    Creates a test file in the temporary directory
    :param tmpdir: the temporary directory
    :return: the test file's FileObject
    """
    test_file = tmpdir / "test.txt"
    content = "this is a test file made for testing."
    test_file.write_text(content)
    return FileObject(filename=os.path.join(tmpdir.__str__(), "test.txt"),
                      _hash=sha1(bytes(content, "utf8")).hexdigest())


@pytest.fixture()
def write_file_obj(objects, test_file):
    write_file(test_file, obj_folder=objects)


@pytest.fixture()
def test_file_location(test_file, objects):
    return os.path.join(objects, test_file.__hash__()[0:2], test_file.__hash__()[2:])

# test tree


@pytest.fixture()
def test_tree_no_sub_trees(tmpdir, test_file):
    t_hash = sha1()
    t_hash.update(bytes(".", "utf8"))
    t_hash.update(bytes(test_file.__hash__(), "utf8"))

    return TreeObject(
        name=".",
        files=[test_file],
        _hash=t_hash.hexdigest()
    )


@pytest.fixture()
def write_test_tree_no_sub_trees(test_tree_no_sub_trees, objects):
    write_tree(test_tree_no_sub_trees, obj_folder=objects)


@pytest.fixture()
def test_tree_with_depth(tmpdir, test_file):
    pass