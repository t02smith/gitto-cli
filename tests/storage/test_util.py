import pytest
from gitto.storage.util import *
from tests.storage.fixtures import *

# TODO mock OBJECTS_FOLDER value


class TestCheckHash:

    sample_invalid_chars = ["@", "&", "^", "£", "$", "(", ")", "["]

    def test_check_hash_valid(self):
        assert check_hash("a9993e364706816aba3e25717850c26c9cd0d89d")

    def test_check_hash_invalid(self):
        assert not check_hash("asjdas")

    @pytest.mark.parametrize("c", sample_invalid_chars)
    def test_check_hash_invalid_chars(self, c):
        assert not check_hash(f"a9993e36{c}706816aba3e25717850c26c9cd0d89d")


class TestObjectExists:
    """
    Tests for the object_exists function
    """

    def test_object_exists_true(self, write_file_obj, test_file, objects):
        """
        Tests that an object can be found if it exists
        """
        assert object_exists(test_file.__hash__(), obj_folder=objects)

    def test_object_exists_false(self, test_file, objects):
        """
        Tests that a non-existent object cannot be found
        """
        assert not object_exists(test_file.__hash__(), obj_folder=objects)

    def test_object_exists_invalid_hash(self):
        with pytest.raises(ValueError):
            object_exists("@@@@@@@@")


class TestReadObject:

    def test_read_object_invalid_hash(self):
        with pytest.raises(ValueError):
            read_object("@@@@@@@@")

