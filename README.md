
# Gitto CLI

The command line interface for Gitto, written in **Python** using
the *Typer* and *Rich* libraries.


![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
## API Reference

#### init

Initialises a new repository in the current working directory.

```bash
  python main.py init
```

#### commit

Generate a snapshot of your code at the current point in time.

```http
  python main.py commit [message]
```

| Parameter      | tag              | Description                       |
| :--------      | :-------         | :-------------------------------- |
| `message`      | `-m` `--message` | **Optional** Commit message       |

#### log

Prints out a table of all commits to the current repository.

```bash
  python main.py log
```


## Authors

- [Tom - t02smith](https://www.github.com/t02smith)

