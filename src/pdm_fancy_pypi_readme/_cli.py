# SPDX-FileCopyrightText: 2022 Hynek Schlawack <hs@ox.cx>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import sys

from typing import Any, NoReturn, TextIO

from fancy_pypi_readme import (
    ConfigurationError,
    build_text,
    load_and_validate_config,
)


CONFIG_KEY = "tool.pdm.build.hooks.fancy-pypi-readme"


def cli_run(
    pyproject: dict[str, Any],
    out: TextIO,
) -> None:
    """
    Best-effort verify config and print resulting PyPI readme.
    """
    if "readme" not in _get_dotted(pyproject, "project.dynamic", ()):
        _fail("You must add 'readme' to 'project.dynamic'.")

    config_data = _get_dotted(pyproject, CONFIG_KEY)

    if config_data is None:
        _fail(f"Missing configuration (`[{CONFIG_KEY}]` in pyproject.toml)")

    try:
        config = load_and_validate_config(config_data, base=f"{CONFIG_KEY}.")
    except ConfigurationError as e:
        _fail(
            "Configuration has errors:\n\n"
            + "\n".join(f"- {msg}" for msg in e.errors),
        )

    print(build_text(config.fragments, config.substitutions), file=out)


def _get_dotted(
    data: dict[str, Any], dotted_key: str, default: Any = None
) -> Any:
    try:
        for key in dotted_key.split("."):
            data = data[key]
    except KeyError:
        return default
    return data


def _fail(msg: str) -> NoReturn:
    print(msg, file=sys.stderr)
    sys.exit(1)
