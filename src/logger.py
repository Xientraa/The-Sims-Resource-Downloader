import logging, sys, traceback
from typing import Type
from types import TracebackType


streamHandler = logging.StreamHandler(sys.stdout)
streamHandler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    filename="logs.log",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
logger.addHandler(streamHandler)


def exceptionHandler(
    type: Type[BaseException], value: BaseException, tb: TracebackType
):
    for line in traceback.TracebackException(type, value, tb).format(chain=True):
        logging.exception(line)
    logging.exception(type, value, tb)
    sys.__excepthook__(type, value, tb)


sys.excepthook = exceptionHandler
