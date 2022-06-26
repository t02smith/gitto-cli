from gitto.storage.objects import *


def template_commit(c: CommitObject) -> str:
    return f"{'-' * 36} COMMIT\n" \
           f"[bold green]commit successful[/bold green]\n" \
           f"[bold]author[/bold]: [italic]{c.author}\n[/italic]" \
           f"[bold]message[/bold]: [italic]{c.message}[/italic]"
