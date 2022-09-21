import os
import click
from .app import applogging
from .core import model_loader


from .core import template_render 

logger = applogging.LogManager().get_app_logger()


@click.command(name="render")
@click.option("--solution-dir", "solution_dir", default=".")
@click.option("--var-file","var_files", multiple=True)
@click.option("--var-file-dir","var_file_dirs", multiple=True)
@click.option("--var", "var_values",multiple=True)
@click.option("--template-dir", "template_dir")
@click.option("--output", "output_dir")
@click.option("--clean", "-c", "clean", default=False, is_flag=True, help="Clean output directory")
@click.option("--watch", "-w", "watch", default=False, is_flag=True, help="Watch source folder")
def command(solution_dir, 
            var_files,
            var_file_dirs, 
            var_values, 
            template_dir, 
            output_dir,
            clean,
            watch):
    logger.debug("Running Command Render")

    solution = template_render.Solution(solution_dir, output_dir, template_dir, var_file_dirs)
    
    model = model_loader.load_model(solution)
    template_render.render(solution, model)






