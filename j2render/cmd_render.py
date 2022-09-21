import os
import click
from .app import applogging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler
import time
import jinja2
from .core import template_render 

logger = applogging.LogManager().get_app_logger()

class MyEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        logger.debug(f"Any change in {event.src_path}")        
        output_dir = "sample/output"
        norm_output_dir = os.path.normpath(output_dir)


        
@click.command(name="render")
@click.option("--solution-dir", "solution_dir", default=".")
@click.option("--var-file","var_files", multiple=True)
@click.option("--var", "var_values",multiple=True)
@click.option("--template-dir", "template_dir")
@click.option("--output", "output_dir")
@click.option("--clean", "-c", "clean", default=False, is_flag=True, help="Clean output directory")
@click.option("--watch", "-w", "watch", default=False, is_flag=True, help="Watch source folder")
def command(solution_dir, 
            var_files, 
            var_values, 
            template_dir, 
            output_dir,
            clean,
            watch):
    logger.debug("Running Command Render")

    var_file_dirs = ["sample/data"]
    output_dir = "sample/output"
    template_dir = "sample/template"
    solution = template_render.Solution(output_dir, template_dir, var_file_dirs)
    
    template_render.render(solution)


    # try:
 
    #     watchdog_dir = "sample"
    #     logger.info(f"Watching {watchdog_dir}. Click any key to stop")
    #     event_handler = MyEventHandler()
    #     observer = Observer()
    #     observer.schedule(event_handler, watchdog_dir, recursive=True)
    #     observer.start()
    #     try:
    #         while True:
    #             time.sleep(1)
    #     except KeyboardInterrupt:
    #         observer.stop()
    #     observer.join()

    # except:
    #     logger.exception("ERROR ")





