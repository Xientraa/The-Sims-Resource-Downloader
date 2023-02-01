from TSRUrl import TSRUrl
from TSRDownload import TSRDownload
from exceptions import *
from typings import *
from multiprocessing import Pool
import clipboard, time, json, os

if __name__ == "__main__":
    CONFIG: CONFIG_DICT = json.load(
        open(os.path.dirname(os.path.abspath(__file__)) + "/config.json", "r")
    )
    lastPastedText = ""
    runningDownloads: list[str] = []
    downloadQueue: list[str] = []

    def processTarget(url: TSRUrl):
        print(f"[INFO] Getting 'tsrdlticket' cookie for: {url.url}")
        downloader = TSRDownload(url)
        print(f"[INFO] Starting download for: {url.url}")
        if downloader.download():
            print(f"[INFO] Completed download for: {url.url}")

        return url

    def callback(url: TSRUrl):
        runningDownloads.remove(url.url)
        if len(runningDownloads) == 0:
            print("[INFO] All downloads have been completed")

    while True:
        pastedText = clipboard.paste()
        if lastPastedText == pastedText:
            for url in downloadQueue:
                if len(runningDownloads) == CONFIG["maxDownloads"]:
                    break

                url = TSRUrl(url)
                runningDownloads.append(url.url)
                downloadQueue.remove(url.url)
                print(f"[INFO] Moved {url.url} from queue to downloading")
                pool = Pool(1)
                pool.apply_async(processTarget, args=[url], callback=callback)

                if len(downloadQueue) == 0:
                    print("[INFO] Queue is now empty")
        else:
            lastPastedText = pastedText
            if pastedText in runningDownloads:
                print(f"[INFO] Url is already being downloaded: {pastedText}")
                continue
            if pastedText in downloadQueue:
                print(
                    f"[INFO] Url is already in queue (#{downloadQueue.index(pastedText)}): {pastedText}"
                )

            try:
                url = TSRUrl(pastedText)
                print(f"[INFO] Found valid url in clipboard: {url.url}")
                if len(runningDownloads) == CONFIG["maxDownloads"]:
                    print(
                        f"[INFO] Added url to queue (#{len(downloadQueue)}): {url.url}"
                    )
                    downloadQueue.append(url.url)
                else:
                    runningDownloads.append(url.url)
                    pool = Pool(1)
                    pool.apply_async(processTarget, args=[url], callback=callback)
            except InvalidURL:
                pass

        time.sleep(0.1)
