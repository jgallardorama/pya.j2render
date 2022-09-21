import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading


class BuildEventHander(FileSystemEventHandler):

    def __init__(self, source_dir, output_dir) -> None:
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.timer: threading.Timer = None
        self.lock = threading.Lock()

        super().__init__()

    def on_modified(self, event):
        logger = applogging.LogManager().get_app_logger()

        logger.debug(
            f"event type: {event.event_type}  path : {event.src_path}")
        if self.timer:
            logger.debug(f"cancel event")
            self.timer.cancel()
        logger.debug(f"New event")
        self.timer = threading.Timer(0.5, self.on_scheduled_build)
        self.timer.start()

    def on_scheduled_build(self):
        logger = applogging.LogManager().get_app_logger()

        self.lock.acquire()
        try:
            logger.debug(f"on_scheduled_build")
            self.timer = None
            watch_task(self.source_dir, self.output_dir)
        finally:
            logger.debug('Released a lock')
            self.lock.release()

def watch_task(source_dir, output_dir):
    logger = applogging.LogManager().get_app_logger()


def watch_build_envs(source_dir, output_dir):
    logger = applogging.LogManager().get_app_logger()

    watch_task(source_dir, output_dir)
    event_handler = BuildEventHander(source_dir, output_dir)
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=True)
    logger.info(f"Watching {source_dir}")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
