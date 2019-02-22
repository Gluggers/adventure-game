import logging
from multiprocessing import Lock

# Wrapper methods.
def debug(logger, message, lock):
    lock.acquire()
    try:
        logger.debug(message)
    finally:
        lock.release()

def info(logger, message, lock):
    lock.acquire()
    try:
        logger.info(message)
    finally:
        lock.release()

def warn(logger, message, lock):
    lock.acquire()
    try:
        logger.warn(message)
    finally:
        lock.release()

def error(logger, message, lock):
    lock.acquire()
    try:
        logger.error(message)
    finally:
        lock.release()

def critical(logger, message, lock):
    lock.acquire()
    try:
        logger.critical(message)
    finally:
        lock.release()

class Locked_Logger():
    lock = None

    def __init__(self, name, level):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

    def debug(self, message):
        pass

    @classmethod
    def get_logger(name, level):
        return Locked_Logger(name, level)

    # Must get called first.
    @classmethod
    def init_locked_loggers(cls):
        #logging.basicConfig(level=logging.INFO)
        cls.lock = Lock()
