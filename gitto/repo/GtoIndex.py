from dataclasses import dataclass
from enum import Enum


class ObjectType(Enum):
    FILE = 0
    COMMIT = 1


class Blob:
    type: ObjectType
    hash: str
    