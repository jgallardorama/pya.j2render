import os
from j2tool import cmd_render
import click
import yaml
import logging

from .version import __version__

from . import cmd_render
from .app.appconfig import ConfigManager
from .app import applogging

@click.group()
@click.version_option(__version__)
@click.option("-v", "--verbose", count=True, default=0)
@click.option("-c", "--configfile", default="")
@click.option(
    "-n",
    "--no-color",
    "no_color",
    is_flag=True,
    default=False,
    help="Disables terminal formatting sequences in the output. ",
)
def main_command(
    verbose: int, no_color = True, debug = False, configfile: str = ""
):
    result = 0
    cm = ConfigManager()
    cm.set_config_value("verbose", verbose)
    cm.set_config_value("no_color", no_color)
    cm.set_config_value("debug", debug)

    lm = applogging.LogManager()
    lm.clear()
    logger = lm.get_app_logger()
    logger.info(f"verbose {verbose}")
    try:

        if configfile and os.path.isfile(configfile):
            logger.info(f"Load configuration from <{configfile}>")
            cm.load(configfile)

        # if config_items:
        #     for key, value in list(config_items):
        #         if key:
        #             cm.set_config_value(key, value)

        config_dump_string = yaml.safe_dump(cm.config)
        logger.debug(f"Configuration\n{config_dump_string}")

    except SystemExit as e:
        result = e.code
        if result != 0:
            logger.info("Error command")
            logger.debug(f"System Exit: {result}")

    except Exception as e:
        logger.info("Error command")
        logger.debug(e)
        result = 65

    return result


main_command.add_command(cmd_render.command)

def start():
    main_command()


if __name__ == "__main__":
    start()