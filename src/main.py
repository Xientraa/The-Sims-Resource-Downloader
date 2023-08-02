from __future__ import annotations
from TSRUrl import TSRUrl
from TSRDownload import TSRDownload
from logger import logger
from exceptions import *
from multiprocessing import Pool
from TSRSession import TSRSession
from config import CONFIG, CURRENT_DIR
import clipboard, time, os


def processTarget(url: TSRUrl, tsrdlsession: str, downloadPath: str):
    downloader = TSRDownload(url, tsrdlsession)
    downloader.download(downloadPath)
    logger.info(f"Completed download for: {url.url}")

    return url


def callback(url: TSRUrl):
    logger.debug(f"Removing {url.url} from queue")
    runningDownloads.remove(url.url)
    updateUrlFile()
    if len(runningDownloads) == 0:
        logger.info("All downloads have been completed")


def updateUrlFile():
    if CONFIG["saveDownloadQueue"]:
        open(CURRENT_DIR + "/urls.txt", "w").write(
            "\n".join([*runningDownloads, *downloadQueue])
        )


if __name__ == "__main__":
    lastPastedText = ""
    runningDownloads: list[str] = []
    downloadQueue: list[str] = []

    logger.debug(f'downloadDirectory: {CONFIG["downloadDirectory"]}')
    logger.debug(f'maxActiveDownloads: {CONFIG["maxActiveDownloads"]}')
    logger.debug(f'saveDownloadQueue: {CONFIG["saveDownloadQueue"]}')
    logger.debug(f'debug: {CONFIG["debug"]}')

    if not os.path.exists(CONFIG["downloadDirectory"]):
        raise FileNotFoundError(
            f"The directory: {CONFIG['downloadDirectory']} does not exist! Please make sure the directory exists or the directory is set correctly in the config."
        )

    session = None
    sessionId = None
    if os.path.exists(CURRENT_DIR + "/session"):
        sessionId = open(CURRENT_DIR + "/session", "r").read()

    while session is None:
        try:
            session = TSRSession(sessionId)
            if hasattr(session, "tsrdlsession"):
                open(CURRENT_DIR + "/session", "w").write(session.tsrdlsession)
                logger.info("Session with captcha successfully created")
        except InvalidCaptchaCode:
            logger.error(
                "Invalid captcha code entered, please make sure the code is correct"
            )
            sessionId = None

    if os.path.exists(CURRENT_DIR + "/urls.txt") and CONFIG["saveDownloadQueue"]:
        for url in open(CURRENT_DIR + "/urls.txt", "r").read().split("\n"):
            if url.strip() == "" or url in downloadQueue:
                continue
            downloadQueue.append(url.strip())

    while True:
        pastedText = clipboard.paste()
        if lastPastedText == pastedText:
            for url in downloadQueue:
                if len(runningDownloads) == CONFIG["maxActiveDownloads"]:
                    break

                url = TSRUrl(url)
                runningDownloads.append(url.url)
                downloadQueue.remove(url.url)
                logger.info(f"Moved {url.url} from queue to downloading")
                pool = Pool(1)
                pool.apply_async(
                    processTarget,
                    args=[
                        url,
                        session.tsrdlsession,
                        CONFIG["downloadDirectory"],
                    ],
                    callback=callback,
                )

                if len(downloadQueue) == 0:
                    logger.info("Queue is now empty")
        else:
            lastPastedText = pastedText
            for line in pastedText.split("\n"):
                if line in runningDownloads:
                    logger.info(f"Url is already being downloaded: {line}")
                    continue
                if line in downloadQueue:
                    logger.info(
                        f"Url is already in queue (#{downloadQueue.index(line)}): {line}"
                    )

                try:
                    url = TSRUrl(line)
                    requirements = TSRUrl.getRequiredItems(url)
                    logger.info(f"Found valid url in clipboard: {url.url}")
                    if len(requirements) != 0:
                        logger.info(f"{url.url} has {len(requirements)} requirements")

                    for url in [url, *requirements]:
                        if url.url in runningDownloads:
                            logger.info(f"Url is already being downloaded: {url.url}")
                            continue
                        if url.url in downloadQueue:
                            logger.info(
                                f"Url is already in queue (#{downloadQueue.index(url.url)}): {url.url}"
                            )
                            continue

                        if len(runningDownloads) == CONFIG["maxActiveDownloads"]:
                            logger.info(
                                f"Added url to queue (#{len(downloadQueue)}): {url.url}"
                            )
                            downloadQueue.append(url.url)
                        else:
                            runningDownloads.append(url.url)
                            pool = Pool(1)
                            pool.apply_async(
                                processTarget,
                                args=[
                                    url,
                                    session.tsrdlsession,
                                    CONFIG["downloadDirectory"],
                                ],
                                callback=callback,
                            )
                    updateUrlFile()
                except InvalidURL:
                    pass

        time.sleep(0.1)
