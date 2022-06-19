from zlib import decompress


def read_object(obj_hash: str):
    """
    Reads an object from the object folder
    :param obj_hash: the hash of the desired object
    :return: the plaintext of the object
    """
    output = ""
    with open(f".gto/objects/{obj_hash[:2]}/{obj_hash[2:]}", "rb") as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            output += decompress(data).decode()
    return output
