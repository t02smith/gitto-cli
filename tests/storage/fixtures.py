import pytest
from gitto.storage.objects import *
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