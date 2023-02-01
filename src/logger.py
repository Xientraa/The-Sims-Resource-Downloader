import logging
from typing import Optional

logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    filename="logs.log",
    level=logging.DEBUG,
)


class Logger:
    @staticmethod
    def info(message: str, silent: Optional[bool] = None):
        logging.info(message)
        if not silent:
            print(f"[INFO] {message}")

    @staticmethod
    def error(message: str, silent: Optional[bool] = None):
        logging.error(message)
        if not silent:
            print(f"[ERROR] {message}")

    @staticmethod
    def warn(message: str, silent: Optional[bool] = None):
        logging.warn(message)
        if not silent:
            print(f"[WARN] {message}")

    @staticmethod
    def exception(message: str, silent: Optional[bool] = None):
        logging.exception(message)
        if not silent:
            print(f"[EXCEPTION] {message}")
