from TSRUrl import TSRUrl
from TSRDownload import TSRDownload
from exceptions import *
from multiprocessing import Pool
import clipboard, time

if __name__ == "__main__":
    lastPastedText = ""
    runningDownloads = []
    while True:
        pastedText = clipboard.paste()
        if lastPastedText != pastedText:
            lastPastedText = pastedText
            if lastPastedText in runningDownloads:
                print(f"[INFO] Url is already being downloaded: {pastedText}")
                continue

            def processTarget(url: TSRUrl):
                print(f"[INFO] Getting 'tsrdlticket' cookie for: {url.url}")
                downloader = TSRDownload(url)
                print(f"[INFO] Starting download for: {url.url}")
                if downloader.download():
                    print(f"[INFO] Completed download for: {url.url}")

                return url

            def callback(url: TSRUrl):
                runningDownloads.remove(url.url)

            try:
                url = TSRUrl(pastedText)
                runningDownloads.append(url.url)
                print(f"[INFO] Found valid url in clipboard: {url.url}")
                pool = Pool(1)
                pool.apply_async(processTarget, args=[url], callback=callback)
            except InvalidURL:
                pass

        time.sleep(0.5)
