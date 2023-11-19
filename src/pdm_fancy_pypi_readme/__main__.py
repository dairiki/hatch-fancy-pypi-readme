# SPDX-FileCopyrightText: 2022 Hynek Schlawack <hs@ox.cx>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import argparse
import sys

from contextlib import closing
from pathlib import Path
from typing import TextIO

from ._cli import cli_run


if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a README from a pyproject.toml."
    )
    parser.add_argument(
        "pyproject_path",
        nargs="?",
        metavar="PATH-TO-PYPROJECT.TOML",
        default="pyproject.toml",
        help="Path to the pyproject.toml to use for rendering. "
        "Default: pyproject.toml in current directory.",
    )
    parser.add_argument(
        "-o",
        help="Target file for output. Default: standard out.",
        metavar="TARGET-FILE-PATH",
    )
    args = parser.parse_args()

    pyproject = tomllib.loads(Path(args.pyproject_path).read_text())

    out: TextIO
    out = Path(args.o).open("w") if args.o else sys.stdout  # noqa: SIM115

    with closing(out):
        cli_run(pyproject, out)


if __name__ == "__main__":
    main()
