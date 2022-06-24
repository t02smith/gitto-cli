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


class TestCommitObject:

    def test_parse_no_parent(self, objects, test_tree_no_sub_trees, write_test_tree_no_sub_trees):
        data = f"{datetime(2002,1,10)}\n" \
               "t02smith\n" \
               "a test commit\n" \
               "None\n" \
               f"{test_tree_no_sub_trees.__hash__()}"
        c = parse_commit(data, obj_folder=objects)
        assert c.timestamp == datetime(2002,1,10)
        assert c.author == "t02smith"
        assert c.message == "a test commit"
        assert c.parent_hash is None
        assert c.tree.__hash__() == test_tree_no_sub_trees.__hash__()

    def test_parse_with_parent(self, objects, test_tree_no_sub_trees, write_test_tree_no_sub_trees):
        pass