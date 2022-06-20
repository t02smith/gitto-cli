import os.path
from zlib import decompress
from os.path import exists, join
import re

OBJECTS_FOLDER = os.path.join(".gto", "objects")


def check_hash(obj_hash: str):
    """
    Checks that a given sha1 hash matches the expected format
    :param obj_hash: the hash to be checked
    :return: whether it is valid
    """
    return len(re.findall("[a-zA-Z\\d]{40}", obj_hash)) == 1


def object_exists(obj_hash: str, obj_folder: str = OBJECTS_FOLDER):
    """
    Checks whether an object is stored
    :param obj_hash: the object's hash
    :param obj_folder: the location of the objects
    :return: whether it exists
    """
    if check_hash(obj_hash):
        return exists(join(obj_folder, obj_hash[:2], obj_hash[2:]))
    else:
        raise ValueError("Invalid sha1 hash")


def read_object(obj_hash: str, obj_folder: str = OBJECTS_FOLDER):
    """
    Reads an object from the object folder
    :param obj_folder: location of objects
    :param obj_hash: the hash of the desired object
    :return: the plaintext of the object
    """
    if not check_hash(obj_hash):
        raise ValueError("Invalid sha1 hash")

    output = ""
    with open(os.path.join(obj_folder, obj_hash[:2], obj_hash[2:]), "rb") as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            output += decompress(data).decode()
    return output
