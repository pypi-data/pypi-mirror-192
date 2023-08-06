# gitflux

A command-line utility to help you manage repositories hosted on [GitHub][1].

## Installation

There are two options to install `gitflux` command.

1. Download compiled executable binary file from [Releases][2].

2. Install package `gitflux` via `pip` command:

    ```shell
    pip install gitflux
    ```

## Usage

```
Usage: gitflux [OPTIONS] COMMAND [ARGS]...

  A command-line utility to help you manage repositories hosted on GitHub.

Options:
  --version  Show version information.
  --init     Initialize configurations.
  --help     Show this message and exit.

Commands:
  create-repos  Create remote repositories.
  delete-repos  Delete an existing repository.
  list-repos    List all remote repositories.
  sync-repos    Synchronize repositories with remote.
```

## License

Copyright (C) 2022 HE Yaowen <he.yaowen@hotmail.com>

The GNU General Public License (GPL) version 3, see [LICENSE](./LICENSE).

[1]: https://github.com

[2]: https://github.com/he-yaowen/gitflux/releases
