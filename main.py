import time
from lib.logger import logger, init_watcher
from lib.sample import do_something

if __name__ == "__main__":
    observer = init_watcher()

    try:
        while True:
            time.sleep(1)
            logger.info('info - hello world')
            logger.debug('debug - hello world')
            do_something()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
