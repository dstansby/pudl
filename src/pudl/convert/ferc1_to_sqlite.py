"""A script for cloning the FERC Form 1 database into SQLite.

This script generates a SQLite database that is a clone/mirror of the original
FERC Form1 database. We use this cloned database as the starting point for the
main PUDL ETL process. The underlying work in the script is being done in
:mod:`pudl.extract.ferc1`.
"""
import argparse
import pathlib
import sys
from pathlib import Path

import yaml

import pudl
from pudl.helpers import configure_root_logger, get_logger
from pudl.settings import Ferc1DbfToSqliteSettings, Ferc1XbrlToSqliteSettings
from pudl.workspace.datastore import Datastore

# Create a logger to output any messages we might have...
logger = get_logger(__name__)


def parse_command_line(argv):
    """Parse command line arguments. See the -h option.

    Args:
        argv (str): Command line arguments, including caller filename.

    Returns:
        dict: Dictionary of command line arguments and their parsed values.

    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "settings_file", type=str, default="", help="path to YAML settings file."
    )
    parser.add_argument(
        "--logfile",
        default=None,
        type=str,
        help="If specified, write logs to this file.",
    )
    parser.add_argument(
        "-c",
        "--clobber",
        action="store_true",
        help="""Clobber existing sqlite database if it exists. If clobber is
        not included but the sqlite databse already exists the _build will
        fail.""",
        default=False,
    )
    parser.add_argument(
        "--sandbox",
        action="store_true",
        default=False,
        help="Use the Zenodo sandbox rather than production",
    )

    arguments = parser.parse_args(argv[1:])
    return arguments


def main():  # noqa: C901
    """Clone the FERC Form 1 FoxPro database into SQLite."""
    # Display logged output from the PUDL package:
    args = parse_command_line(sys.argv)
    configure_root_logger(args.logfile)

    with pathlib.Path(args.settings_file).open() as f:
        script_settings = yaml.safe_load(f)

    defaults = pudl.workspace.setup.get_defaults()
    pudl_in = script_settings.get("pudl_in", defaults["pudl_in"])
    pudl_out = script_settings.get("pudl_out", defaults["pudl_out"])

    pudl_settings = pudl.workspace.setup.derive_paths(
        pudl_in=pudl_in, pudl_out=pudl_out
    )

    dbf_settings = Ferc1DbfToSqliteSettings().parse_obj(
        script_settings["ferc1_dbf_to_sqlite_settings"]
    )

    pudl_settings["sandbox"] = args.sandbox
    pudl.extract.ferc1.dbf2sqlite(
        ferc1_to_sqlite_settings=dbf_settings,
        pudl_settings=pudl_settings,
        clobber=args.clobber,
        datastore=Datastore(
            local_cache_path=(Path(pudl_in) / "data"), sandbox=args.sandbox
        ),
    )

    xbrl_settings = Ferc1XbrlToSqliteSettings().parse_obj(
        script_settings["ferc1_xbrl_to_sqlite_settings"]
    )

    pudl.extract.ferc1.xbrl2sqlite(
        ferc1_to_sqlite_settings=xbrl_settings,
        pudl_settings=pudl_settings,
        clobber=args.clobber,
        datastore=Datastore(local_cache_path=(Path(pudl_in) / "data"), sandbox=True),
    )


if __name__ == "__main__":
    sys.exit(main())
