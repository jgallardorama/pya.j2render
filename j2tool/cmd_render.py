import os
import click

from j2tool import watcher
from .app import applogging
from .core import model_loader, template_render 

logger = applogging.LogManager().get_app_logger()


@click.command(name="render")
@click.option("--solution-dir", "solution_dir", default=".")
@click.option("--var-file","var_files", multiple=True)
@click.option("--var-file-dir","var_file_dirs", multiple=True)
@click.option("--var", "var_values",multiple=True)
@click.option("--template-dir", "template_dir")
@click.option("--output", "output_dir", default="output")
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
    
    if not template_dir:
        template_dir = os.path.join(solution_dir, "templates")
    
    if not var_file_dirs:
        data_dir = os.path.join(solution_dir, "data")
        var_file_dirs = [data_dir]

    solution = template_render.Solution(solution_dir, output_dir, template_dir, var_file_dirs)
    
    if watch:
        watcher.watch_solution(solution)
    else:         
        model = model_loader.load_model(solution)
        template_render.render(solution, model)






