from TSRUrl import TSRUrl
from TSRDownload import TSRDownload
from logger import Logger
from exceptions import *
from typings import *
from multiprocessing import Pool
from TSRSession import TSRSession
import clipboard, time, json, os


def processTarget(url: TSRUrl):
    downloader = TSRDownload(url, session)
    if downloader.download():
        Logger.info(f"Completed download for: {url.url}")

    return url


def callback(url: TSRUrl):
    runningDownloads.remove(url.url)
    if len(runningDownloads) == 0:
        Logger.info("All downloads have been completed")


if __name__ == "__main__":
    CONFIG: CONFIG_DICT = json.load(
        open(os.path.dirname(os.path.abspath(__file__)) + "/config.json", "r")
    )
    lastPastedText = ""
    runningDownloads: list[str] = []
    downloadQueue: list[str] = []

    session = None
    while session is None:
        try:
            session = TSRSession()
        except InvalidCaptchaCode:
            pass

    while True:
        pastedText = clipboard.paste()
        if lastPastedText == pastedText:
            for url in downloadQueue:
                if len(runningDownloads) == CONFIG["maxDownloads"]:
                    break

                url = TSRUrl(url)
                runningDownloads.append(url.url)
                downloadQueue.remove(url.url)
                Logger.info(f"Moved {url.url} from queue to downloading")
                pool = Pool(1)
                pool.apply_async(processTarget, args=[url], callback=callback)

                if len(downloadQueue) == 0:
                    Logger.info("Queue is now empty")
        else:
            lastPastedText = pastedText
            if pastedText in runningDownloads:
                Logger.info(f"Url is already being downloaded: {pastedText}")
                continue
            if pastedText in downloadQueue:
                Logger.info(
                    f"Url is already in queue (#{downloadQueue.index(pastedText)}): {pastedText}"
                )

            try:
                url = TSRUrl(pastedText)
                requirements = TSRUrl.getRequiredItems(url)
                Logger.info(f"Found valid url in clipboard: {url.url}")
                if len(requirements) != 0:
                    Logger.info(f"{url.url} has {len(requirements)} requirements")

                for url in [url, *requirements]:
                    if len(runningDownloads) == CONFIG["maxDownloads"]:
                        Logger.info(
                            f"Added url to queue (#{len(downloadQueue)}): {url.url}"
                        )
                        downloadQueue.append(url.url)
                    else:
                        runningDownloads.append(url.url)
                        pool = Pool(1)
                        pool.apply_async(processTarget, args=[url], callback=callback)
            except InvalidURL:
                pass

        time.sleep(0.1)
