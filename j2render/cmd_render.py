import os
import click
from . import log_manager
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler
import time
import jinja2
from . import template_render 

logger = log_manager.get_logger(__name__)
output_filename = "output.txt"

class MyEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        logger.debug(f"Any change in {event.src_path}")        
        output_dir = "sample/output"
        output_file = os.path.normpath(os.path.join(output_dir, output_filename))

        if event.src_path == output_file:
            return
        template_render.render(output_file)
        
@click.command(name="render")
def command():

    logger.debug("Running Command Render")

    try:
 
        watchdog_dir = "sample"
        logger.info(f"Watching {watchdog_dir}. Click any key to stop")
        event_handler = MyEventHandler()
        observer = Observer()
        observer.schedule(event_handler, watchdog_dir, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    except:
        logger.exception("ERROR ")





