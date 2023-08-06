import typer

# app = typer.Typer(add_completion=False, help=application_help)


class CLIApplication:
    application_help: str = ""

    def __init__(self) -> None:
        # self.commands = []

        self.app = typer.Typer(add_completion=False, help=self.application_help)

    def register_command(self, command):
        # self.commands.append(command)
        cmd = self.app.command(name=command.name, help=command.help)
        cmd(command.handler)


def cli_echo(text: str):
    typer.echo(text)
