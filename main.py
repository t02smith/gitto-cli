from gitto.cli.cli import app
from gitto.storage.storage import *
from gitto.storage.info import *

from rich.console import Console

if __name__ == "__main__":
    app()


# TODO write_tree will generate many objects even with unchanged files
