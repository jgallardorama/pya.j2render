import os
import shutil
import click
from .app import applogging
import j2tool

logger = applogging.LogManager().get_app_logger()


@click.command(name="init")
@click.option("--solution-dir", "solution_dir", default=".")
def command(solution_dir):
    logger.debug(f"Running Command Init <{solution_dir}>")

    j2tool_dir = os.path.dirname(j2tool.__file__)
    data_dir = os.path.join(j2tool_dir, "data/sln")

    os.makedirs(solution_dir, exist_ok=True)

    shutil.copytree(
        data_dir,
        solution_dir,
        symlinks=False,
        ignore=None,
        copy_function=shutil.copy2,
        ignore_dangling_symlinks=False,
        dirs_exist_ok=True,
    )
