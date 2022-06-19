from tests.storage.fixtures import *


class TestFileObject:

    def test_file_hash(self, test_file):
        """
        Tests whether the FileObject calculates the correct hash
        """
        expected_hash = test_file.__hash__()
        test_file._hash = None
        assert expected_hash == test_file.__hash__()

    def test_file_invalid_file(self):
        """
        Tests whether a file object will fail to hash a nonexistent file
        """
        with pytest.raises(FileNotFoundError):
            FileObject("fake_file.exe")

    def test_file_hash_changes_with_file_contents(self, tmpdir, test_file):
        """
        Tests whether the file's hash changes if its contents changes
        """
        old_hash = test_file.__hash__()
        test_file._last_updated = datetime(2000, 1, 1)
        with open(os.path.join(tmpdir.__str__(), test_file.filename), "w") as f:
            f.write("i've changed this test file")
        assert old_hash != test_file.__hash__()