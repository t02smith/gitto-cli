import pytest
from gitto.storage.storage import *
from tests.storage.fixtures import *
from zlib import decompress
import os


class TestWriteFile:
    """
    Tests for the write_file function
    """

    def test_write_file_none_file(self, objects):
        """
        Test a TypeError is thrown when a None FileObject is passed
        """
        with pytest.raises(TypeError):
            write_file(None, obj_folder=objects)

    def test_write_file_exists(self, write_file_obj, test_file_location):
        """
        Test that an object with the correct hash is created
        """
        assert os.path.exists(test_file_location)

    def test_write_file_directory_created(self, write_file_obj, objects, test_file):
        """
        Test that the directory with the first two characters of the hash is created
        """
        assert os.path.isdir(os.path.join(objects, test_file.__hash__()[0:2]))

    def test_write_file_content_written(self, write_file_obj, test_file_location):
        """
        Tests that the content written to the object file is correct
        """
        with open(test_file_location, "rb") as f:
            data = decompress(f.read()).decode()

        assert data == "this is a test file made for testing."

    def test_write_file_does_not_exist(self):
        """
        Tests that a FileNotFoundError is thrown if a file doesn't exist
        """
        with pytest.raises(FileNotFoundError):
            write_file(FileObject(filename="fake.exe"))

    def test_write_file_same_content_produces_same_hash_file(self, write_file_obj, objects, test_file):
        """
        Tests that a file that already has a hash isn't overwritten
        """
        timestamp = datetime.fromtimestamp(os.stat(
            os.path.join(objects, test_file.__hash__()[0:2], test_file.__hash__()[2:])).st_mtime)

        sleep = [x for x in range(100)]  # using time.sleep has weird effect on output
        write_file(test_file, obj_folder=objects)
        new_timestamp = datetime.fromtimestamp(os.stat(
            os.path.join(objects, test_file.__hash__()[0:2], test_file.__hash__()[2:])).st_mtime)

        assert new_timestamp == timestamp


class TestWriteTree:

    def test_write_tree_none(self):
        with pytest.raises(TypeError):
            write_tree(None)

    def test_write_tree_tree_exists(self, objects, test_tree_no_sub_trees, write_test_tree_no_sub_trees):
        assert os.path.exists(
            os.path.join(objects, test_tree_no_sub_trees.__hash__()[0:2], test_tree_no_sub_trees.__hash__()[2:]))

    def test_write_tree_file_exists(self, objects, test_file_location, write_test_tree_no_sub_trees):
        assert os.path.exists(test_file_location)

    def test_write_tree_content_no_depth(self, objects, test_file,
                                         test_tree_no_sub_trees, write_test_tree_no_sub_trees):
        content = read_object(test_tree_no_sub_trees.__hash__(), obj_folder=objects).splitlines()
        assert content[0] == "."
        assert content[1] == f"file {test_file.__hash__()} {test_file.filename}"
