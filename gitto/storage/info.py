from dataclasses import dataclass
from os import path
from json import dump, loads


@dataclass
class StorageInfo:
    """
    Stores info relevant to the repository
    to track attributes about it
    """
    last_commit: str = None
    remote_location: str = None


def read_info():
    """
    Will read the info file if it exists
    :return: the info file or nothing
    """
    if not path.isfile(".gto/info.json"):
        return StorageInfo()

    with open(".gto/info.json", "r") as f:
        info = loads(f.read())

    return StorageInfo(
        last_commit=info["last_commit"],
        remote_location=info["remote_location"]
    )


def write_info(info: StorageInfo):
    """
    Writes to the info file
    all None fields will be ignored and kept the same
    :param info: the changes
    :return: void
    """
    curr_info = read_info()
    changes = False

    if curr_info is not None:
        if info.last_commit is None or info.last_commit != curr_info.last_commit:
            changes = True
            curr_info.last_commit = info.last_commit

        if info.remote_location is None or info.remote_location != curr_info.remote_location:
            changes = True
            curr_info.remote_location = info.remote_location
    else:
        changes = True

    if changes:
        with open(".gto/info.json", "w") as f:
            dump(curr_info.__dict__ if curr_info is not None else info.__dict__, f)
