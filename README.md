# Trello CLI

`trello-cli` is a simple CLI tool for managing your Trello cards. It allows you to create cards, add labels, and include comments directly from your terminal without needing to access the Trello web interface.

-----

## Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Workflow Example](#workflow-example)
- [Help & References](#help--references)

## Features

- Card Search: Search for cards across all your boards
- Create Cards: Add new cards to any list with labels and comments
- Board Discovery: View all your Trello boards with their IDs
- List Discovery: View all lists within a board
- Label Discovery: View all available labels in a board
- Environment Variable Support: Configure your Trello credentials via environment variables or command-line options
- Rich Terminal Output: Beautifully formatted output for better readability using `rich`
- Command Help System: Each subcommand has detailed help information available via the `--help` flag

## Installation

1. Change to the trello-cli directory:

```bash
cd trello-cli
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install the package:

```bash
pip install .
```

To install the package in editable mode, use the `-e` option:

```bash
pip install -e .
```

## Configuration

You can provide your Trello API credentials in two ways:

- Using Environment Variables:

Create the following environment variables (by adding them to your `.bashrc`/`.zshrc` or other appropriate file):

```bash
export TRELLO_API_KEY=your_api_key
export TRELLO_TOKEN=your_token
```

- Command-Line Options:

You can also provide credentials with each command using `--api-key` and `--token` options


## Usage

The CLI provides several commands to help you manage your Trello boards and cards. Each command has detailed help information available via the `--help` flag. Its really helpful in telling you what options are available and how to use them.

- View All Commands and General Help

```bash
trello-cli --help
```

- List Your Boards

```bash
trello-cli boards
trello-cli boards --help # for more information
```

- View Lists in a Board

```bash
trello-cli lists --board-id <board_id>
trello-cli lists -b <board_id> # short form
trello-cli lists --help # for more information
```

- View Labels in a Board

```bash
trello-cli labels --board-id <board_id>
trello-cli labels -b <board_id> # short form
trello-cli labels --help # for more information
```

- Search for Cards using a query string

```bash
trello-cli search --query <search_term>
trello-cli search --help # for more information
```

- Create a new Card

```bash
trello-cli add-card --list-id <list_id> --name "Card Name"
trello-cli add-card --help  # for more information
```

- Create a new Card with Labels and Comment

```bash
trello-cli add-card --list-id <list_id> --name "Card Name" --label <label_id_1>,<label_id_2> --comment "Card Comment"
```

## Workflow Example

1. Find your board ID:

```bash
trello-cli boards
```

2. Find the desired list ID:

```bash
trello-cli lists --board-id <board_id>
```

3. Check available labels:

```bash
trello-cli labels --board-id <board_id>
```

4. Create a new card:

```bash
trello-cli add-card --list-id <list_id> --name "New Feature" --label <label_id> --comment "Priority task for sprint"
```

## Help & References

I was unfamiliar with building installable packages in Python and it seemed fitting that a CLI tool should be `pip` installable. The following resources helped me a lot in understanding the process:

- [PyOpenScience Packaging Guide](https://www.pyopensci.org/python-package-guide/tutorials/installable-code.html)
- [Setuptools Entry Points](https://setuptools.pypa.io/en/latest/userguide/entry_point.html)
- [The Complete Guide to pyproject.toml](https://devsjc.github.io/blog/20240627-the-complete-guide-to-pyproject-toml/)

Also, I can't skip mentioning the excellent docs for [Typer](https://typer.tiangolo.com/). It was a great learning experience building the CLI using it.

## License

`trello-cli` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
