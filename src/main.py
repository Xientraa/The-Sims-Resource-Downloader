from TSRUrl import TSRUrl
from TSRDownload import TSRDownload
from exceptions import *
import clipboard, time

if __name__ == "__main__":
    lastPastedText = ""
    while True:
        pastedText = clipboard.paste()
        if lastPastedText != pastedText:
            lastPastedText = pastedText
            try:
                url = TSRUrl(pastedText)
                print(f"[INFO] Found valid url in clipboard: {url.url}")
                print(f"[INFO] Getting 'tsrdlticket' cookie for: {url.url}")
                downloader = TSRDownload(url)
                print(f"[INFO] Starting download for: {url.url}")
                if downloader.download():
                    print(f"[INFO] Completed download for: {url.url}")
            except InvalidURL:
                pass

        time.sleep(0.5)
