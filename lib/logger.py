import logging
import logging.config
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import time
from datetime import datetime, timedelta

config_path = './dynamic-config'
config_file = 'logging.conf'
logging_config_file = f'{config_path}/{config_file}'
logger = None
lock = threading.Lock()

def build_logger() -> logging.Logger:
    global logger
    lock.acquire()
    logging.config.fileConfig(logging_config_file)
    logger = logging.getLogger()
    lock.release()

class ConfigChangeEventHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_modified = datetime.now()

    def on_any_event(self, event):
        print(f'{event.event_type} on {event.src_path}')

    def on_modified(self, event):
        if datetime.now() - self.last_modified < timedelta(seconds=5):
            return
        else:
            self.last_modified = datetime.now()

        # when using vi to change the file, the main file may not be
        # there when other events such as those for .swp is triggered
        time.sleep(5)
        build_logger()

def init_watcher() -> Observer:
    event_handler = ConfigChangeEventHandler()
    observer = Observer()
    observer.schedule(event_handler, config_path)
    observer.start()
    return observer

if logger is None:
    build_logger()

logger    
