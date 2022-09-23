import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

from j2tool.app.applogging import LogManager
from j2tool.core.template_render import Solution
from j2tool.core import model_loader, template_render 

class RenderEventHander(FileSystemEventHandler):

    def __init__(self, solution : Solution) -> None:
        self.solution = solution
        
        self.timer: threading.Timer = None
        self.lock = threading.Lock()

        super().__init__()

    def on_modified(self, event):
        logger = LogManager().get_app_logger()

        logger.debug(
            f"event type: {event.event_type}  path : {event.src_path}")
        if self.timer:
            logger.debug(f"cancel event")
            self.timer.cancel()
        logger.debug(f"New event")
        self.timer = threading.Timer(0.5, self.on_scheduled_build)
        self.timer.start()

    def on_scheduled_build(self):
        logger = LogManager().get_app_logger()

        self.lock.acquire()
        try:
            logger.debug(f"on_scheduled_build")
            self.timer = None
            on_watch_task(self.solution)
        finally:
            logger.debug('Released a lock')
            self.lock.release()

def on_watch_task(solution: Solution):
    logger = LogManager().get_app_logger()
    model = model_loader.load_model(solution)
    template_render.render(solution, model)

def watch_solution(solution: Solution):
    logger = LogManager().get_app_logger()

    on_watch_task(solution)
    event_handler = RenderEventHander(solution)
    observer = Observer()
    observer.schedule(event_handler, solution.solution_dir, recursive=True)
    logger.info(f"Watching {solution.solution_dir}")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
