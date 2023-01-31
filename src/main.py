from TSRUrl import TSRUrl
from TSRDownload import TSRDownload
from time import sleep


if __name__ == "__main__":
    url = TSRUrl("https://www.thesimsresource.com/downloads/details/id/1632083")
    downloader = TSRDownload(url)
    # downloader.download()
    print(url.itemId, url.url)
