from TSRUrl import TSRUrl
from TSRDownload import TSRDownload
from logger import logger
from exceptions import *
from typings import *
from multiprocessing import Pool
from TSRSession import TSRSession
import clipboard, time, json, os


def processTarget(url: TSRUrl, tsrdlsession: str, downloadPath: str):
    downloader = TSRDownload(url, tsrdlsession)
    downloader.download(downloadPath)
    logger.info(f"Completed download for: {url.url}")

    return url


def callback(url: TSRUrl):
    runningDownloads.remove(url.url)
    if len(runningDownloads) == 0:
        logger.info("All downloads have been completed")


if __name__ == "__main__":
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG: CONFIG_DICT = json.load(open(CURRENT_DIR + "/config.json", "r"))
    lastPastedText = ""
    runningDownloads: list[str] = []
    downloadQueue: list[str] = []

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
            if pastedText in runningDownloads:
                logger.info(f"Url is already being downloaded: {pastedText}")
                continue
            if pastedText in downloadQueue:
                logger.info(
                    f"Url is already in queue (#{downloadQueue.index(pastedText)}): {pastedText}"
                )

            try:
                url = TSRUrl(pastedText)
                requirements = TSRUrl.getRequiredItems(url)
                logger.info(f"Found valid url in clipboard: {url.url}")
                if len(requirements) != 0:
                    logger.info(f"{url.url} has {len(requirements)} requirements")

                for url in [url, *requirements]:
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
            except InvalidURL:
                pass

        time.sleep(0.1)
