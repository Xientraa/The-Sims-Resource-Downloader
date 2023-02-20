import requests, time, json, os, re
from TSRUrl import TSRUrl
from logger import Logger
from exceptions import *
from typings import *

CONFIG: CONFIG_DICT = json.load(
    open(os.path.dirname(os.path.abspath(__file__)) + "/config.json", "r")
)


class TSRDownload:
    @classmethod
    def __init__(self, url: TSRUrl):
        self.session: requests.Session = requests.Session()
        self.url: TSRUrl = url
        self.ticketInitializedTime: float = -1.0
        self.__getTSRDLTicketCookie()

    @classmethod
    def download(self) -> bool:
        Logger.info(f"Starting download for: {self.url.url}")
        timeToSleep = 15000 - (time.time() * 1000 - self.ticketInitializedTime)
        if timeToSleep > 0:
            time.sleep(timeToSleep / 1000)

        downloadUrl = self.__getDownloadUrl()
        fileName = self.__getFileName(downloadUrl)

        startingBytes = (
            os.path.getsize(f"{CONFIG['downloadDirectory']}/{fileName}.part")
            if os.path.exists(f"{CONFIG['downloadDirectory']}/{fileName}.part")
            else 0
        )
        request = self.session.get(
            downloadUrl,
            stream=True,
            headers={"Range": f"bytes={startingBytes}-"},
        )
        file = open(f"{CONFIG['downloadDirectory']}/{fileName}.part", "wb")

        for chunk in request.iter_content(1024 * 1024):
            file.write(chunk)
        file.close()
        os.rename(
            f"{CONFIG['downloadDirectory']}/{fileName}.part",
            f"{CONFIG['downloadDirectory']}/{fileName}",
        )
        return True

    @classmethod
    def __getFileName(self, downloadUrl: str) -> str:
        return re.search(
            '(?<=filename=").+(?=")',
            requests.get(downloadUrl, stream=True).headers["Content-Disposition"],
        )[0]

    @classmethod
    def __getDownloadUrl(self) -> str:
        response = self.session.get(
            f"https://www.thesimsresource.com/ajax.php?c=downloads&a=getdownloadurl&ajax=1&itemid={self.url.itemId}&mid=0&lk=0",
            cookies=self.session.cookies,
        )
        responseJSON = response.json()

        if response.status_code == 200:
            if responseJSON["error"] == "":
                return responseJSON["url"]
            elif responseJSON["error"] == "Invalid download ticket":
                raise InvalidDownloadTicket(response.url, self.session.cookies)
        else:
            raise requests.exceptions.HTTPError(response)

    @classmethod
    def __getTSRDLTicketCookie(self) -> str:
        Logger.info(f"Getting 'tsrdlticket' cookie for: {self.url.url}")
        response = self.session.get(
            f"https://www.thesimsresource.com/ajax.php?c=downloads&a=initDownload&itemid={self.url.itemId}&format=zip"
        )
        self.session.get(self.url.downloadUrl)
        self.ticketInitializedTime = time.time() * 1000
        return response.cookies.get("tsrdlticket")
