from gitto.cli.cli import app
from gitto.storage.storage import *
from gitto.storage.storage_info import *

from rich.console import Console

console = Console()

if __name__ == "__main__":
    # app()
    t = generate_tree()
    write_tree(t)
    console.print(parse_tree(t.__hash__(), read_object(t.__hash__())))

# TODO write_tree will generate many objects even with unchanged files
