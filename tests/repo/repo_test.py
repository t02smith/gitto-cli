import pytest

from gitto.repo.repo import *


class TestGtoRepo:
    def test_add_new_file(self):
        """
        Asserts that a correct file is successfully added
        :return: void
        """
        repo = GtoRepo("test", 100)
        repo.add("../data/test.txt")
        assert "../data/test.txt" in repo.files

    def test_add_file_twice(self):
        """
        Asserts that a correct file will only be added once
        :return:
        """
        repo = GtoRepo("test", 100)
        repo.add("../data/test.txt")
        repo.add("../data/test.txt")
        assert "../data/test.txt" in repo.files and len(repo.files) == 1

    def test_add_invalid_file(self):
        """
        Asserts that only files that exist can be added
        :return: void
        """
        repo = GtoRepo("test", 100)
        with pytest.raises(FileNotFoundError):
            repo.add("doesnt_exist.txt")

