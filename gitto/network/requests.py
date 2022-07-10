import json
import requests

from gitto.storage.objects import latest_commit
from gitto.storage.info import read_info
from gitto.cli.rich import console

API_PATH = "http://localhost:8080/api/v1"


def push():
    # payload to send to remote
    commit = latest_commit().toDict()
    info = read_info()

    console.print(f"[blue]Attempting to push commit [bold]{commit['hash']}[/bold][/blue]")

    try:
        res = requests.post(url=f"{API_PATH}/{info.repo_name}/commit", json=commit)

        console.print("[green]Commit pushed successfully![/green]")
        return res
    except requests.ConnectionError:
        console.print(f"[red bold]Failed to connect to remote server :([/red bold]")
