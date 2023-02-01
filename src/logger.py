import logging
from typing import Optional

logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    filename="logs.log",
    level=logging.DEBUG,
)


class Logger:
    @staticmethod
    def info(message: str, silent: Optional[bool]):
        logging.info(message)
        if not silent:
            print(f"[INFO] {message}")

    @staticmethod
    def error(message: str, silent: Optional[bool]):
        logging.error(message)
        if not silent:
            print(f"[ERROR] {message}")

    @staticmethod
    def warn(message: str, silent: Optional[bool]):
        logging.warn(message)
        if not silent:
            print(f"[WARN] {message}")

    @staticmethod
    def exception(message: str, silent: Optional[bool]):
        logging.exception(message)
        if not silent:
            print(f"[EXCEPTION] {message}")
