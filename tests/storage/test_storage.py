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

    def test_write_file_exists(self, objects, test_file):
        """
        Test that an object with the correct hash is created
        """
        write_file(test_file, obj_folder=objects)
        assert os.path.exists(os.path.join(objects, test_file.__hash__()[0:2], test_file.__hash__()[2:]))

    def test_write_file_directory_created(self, objects, test_file):
        """
        Test that the directory with the first two characters of the hash is created
        """
        write_file(test_file, obj_folder=objects)
        assert os.path.isdir(os.path.join(objects, test_file.__hash__()[0:2]))

    def test_write_file_content_written(self, objects, test_file):
        """
        Tests that the content written to the object file is correct
        """
        write_file(test_file, obj_folder=objects)
        with open(os.path.join(objects, test_file.__hash__()[0:2], test_file.__hash__()[2:]), "rb") as f:
            data = decompress(f.read()).decode()

        assert data == "this is a test file made for testing."

    def test_write_file_does_not_exist(self):
        """
        Tests that a FileNotFoundError is thrown if a file doesn't exist
        """
        with pytest.raises(FileNotFoundError):
            write_file(FileObject(filename="fake.exe"))
