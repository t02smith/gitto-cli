
from enum import Enum
from os import mkdir, path
import hashlib
from zlib import compress, decompress




def write_file(filename: str):
    """
    Writes a file to a blob
    :param filename: the name of the file
    :return: the blob's hash
    """
    hash_value = hash_file(filename)
    if not path.isdir(f".gto/objects/{hash_value[:2]}"):
        mkdir(f".gto/objects/{hash_value[:2]}")

    if path.exists(f".gto/objects/{hash_value[:2]}/{hash_value[2:]}"):
        return

    with open(filename, "rb") as readFrom:
        with open(f".gto/objects/{hash_value[:2]}/{hash_value[2:]}", "xb") as writeTo:
            while True:
                data = readFrom.read(65536)
                if not data:
                    break
                writeTo.write(compress(data, 5))

    return hash_value


def read_file(hash_value: str):
    """
    Reads a given file blob and returns the contents
    :param hash_value: the given blob
    :return: the blobs contents
    """
    output = ""
    with open(f".gto/objects/{hash_value[:2]}/{hash_value[2:]}", "rb") as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            output += decompress(data).decode()
    return output


def hash_file(filename: str):
    # check file is in repo ...

    # read file bytes
    buffer_size = 65536  # 64kb buffer size
    hasher = hashlib.sha256()
    with open(filename, "rb") as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            hasher.update(data)

    hash_value = hasher.hexdigest()
    return hash_value

