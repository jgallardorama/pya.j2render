from j2render import cmd_render
import click
import logging

from .version import __version__

from . import cmd_render
from .app.appconfig import ConfigManager
from .app import applogging

@click.group()
@click.version_option(__version__)
@click.option("-v", "--verbose", count=True, default=0)
@click.option("-c", "--configfile", default="")
def main_command(
    verbose: int,
    configfile: str = "",
):
    cm = ConfigManager()
    cm.verbose = verbose
    logger = applogging.init_log(__name__)
    logger.info(f"verbose {verbose}")

    if configfile != "":
        cm.load(configfile)


main_command.add_command(cmd_render.command)

def start():
    main_command()


if __name__ == "__main__":
    start()