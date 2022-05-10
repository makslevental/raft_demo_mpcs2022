import logging
from threading import Lock

logging.basicConfig(
    format="%(levelname)s %(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S",
    # uncomment to get file logging
    # filename="example.log",
    # uncomment to get overwrite (of log file)
    # filemode="w",
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)

logger_lock = Lock()


def debug_print(*args):
    logger_lock.acquire()
    logger.debug(" ".join(len(args) * ["%s"]), *args)
    logger_lock.release()
