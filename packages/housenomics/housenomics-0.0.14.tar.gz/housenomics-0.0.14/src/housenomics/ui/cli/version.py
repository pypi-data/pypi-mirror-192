from housenomics.ui.cli.main import housenomics_cli
from toolbox.cli import cli_echo


def version():
    cli_echo("0.0.14")


class CommandVersion:
    name = "version"
    help = "Shows current version"
    handler = version


housenomics_cli.register_command(CommandVersion)
