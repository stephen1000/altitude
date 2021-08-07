#!/usr/bin/env python3
"""
Processes an altitude server configuration file with values from the environment.
"""

import argparse
import os
from pathlib import Path
from typing import List

from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_parser() -> argparse.ArgumentParser:
    """ Fetches a ``argparse.ArgumentParser`` """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "config_folder", help="folder containing configuration file to parse"
    )
    parser.add_argument(
        "config_file",
        help="path to configuration file to parse (relative to `config_folder`)",
    )
    parser.add_argument(
        "output_file", help="file to output to (will be in `config_folder`)."
    )
    return parser


def get_jinja_env(config_folder: str) -> Environment:
    """ Builds a Jinja environment """
    return Environment(
        loader=FileSystemLoader(config_folder), autoescape=select_autoescape()
    )


def get_environment_values(prefix: str) -> List[str]:
    """ Returns all values in the environment beginning with ``prefix`` """
    vals = {key: val for key, val in os.environ.items() if key.startswith(prefix)}
    return vals


def listify(vars_dict: dict, key: str) -> dict:
    """
    Converts value of `key` in `vars` to a list via string split on "," character.
    If `key` is not present in `vars_dict`, an empty list is set as its value.
    """
    vars_dict[key] = vars_dict.get(key, "").split(",")
    return vars_dict


def handle():
    """ CLI entrypoint """
    args = get_parser().parse_args()

    jinja_env = get_jinja_env(config_folder=args.config_folder)
    template_vars = get_environment_values("ALTITUDE")
    template_vars = listify(template_vars, "ALTITUDE_ADMIN_UUIDS")
    template_vars = listify(template_vars, "ALTITUDE_MAP_LIST")
    template_vars = listify(template_vars, "ALTITUDE_MAP_ROTATION")

    template = jinja_env.get_template(args.config_file)
    outpath = Path(args.output_file)
    outpath.write_text(template.render(**template_vars))


if __name__ == "__main__":
    handle()
