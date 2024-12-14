from __future__ import annotations
import requests, time, os, re
from TSRUrl import TSRUrl
from logger import logger
from tqdm import tqdm
from exceptions import *


class TSRDownload:
    @classmethod
    def __init__(self, url: TSRUrl, sessionId: str):
        self.session: requests.Session = requests.Session()
        self.session.cookies.set("tsrdlsession", sessionId)

        self.url: TSRUrl = url
        self.ticketInitializedTime: float = -1.0
        self.__getTSRDLTicketCookie()

    @classmethod
    def download(self, downloadPath: str) -> str:
        logger.info(f"\n\n=== Starting download for: {self.url.url} ===")
        timeToSleep = 15000 - (time.time() * 1000 - self.ticketInitializedTime)
        if timeToSleep > 0:
            logger.info(f"Waiting for {timeToSleep / 1000:.2f} seconds before starting...")
            time.sleep(timeToSleep / 1000)

        downloadUrl = self.__getDownloadUrl()
        logger.debug(f"Got download URL: {downloadUrl}")
        fileName = self.__getFileName(downloadUrl)
        logger.debug(f"Got file name: {fileName}")

        startingBytes = (
            os.path.getsize(f"{downloadPath}/{fileName}.part")
            if os.path.exists(f"{downloadPath}/{fileName}.part")
            else 0
        )
        logger.debug(f"Starting bytes: {startingBytes}")
        request = self.session.get(
            downloadUrl,
            stream=True,
            headers={"Range": f"bytes={startingBytes}-"},
        )
        logger.debug(f"Request status: {request.status_code}")

        total_size = int(request.headers.get('content-length', 0)) + startingBytes  # Total size of the file
        with open(f"{downloadPath}/{fileName}.part", "wb") as file:
            # Initialize tqdm progress bar
            with tqdm(total=total_size, initial=startingBytes, unit='B', unit_scale=True, desc=fileName) as bar:
                for index, chunk in enumerate(request.iter_content(1024 * 128)):
                    file.write(chunk)
                    bar.update(len(chunk))  # Update progress bar

        logger.debug(f"\nRenaming .part file to: {fileName}")
        if os.path.exists(f"{downloadPath}/{fileName}"):
            logger.debug(f"{downloadPath}/{fileName} already exists! Replacing file.")
            os.replace(f"{downloadPath}/{fileName}.part", f"{downloadPath}/{fileName}")
        else:
            logger.debug(f"{downloadPath}/{fileName} doesn't exist! Renaming file.")
            os.rename(
                f"{downloadPath}/{fileName}.part",
                f"{downloadPath}/{fileName}",
            )
        
        logger.info(f"\n=== Download completed: {fileName} ===\n")
        return fileName

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
        logger.info(f"Getting 'tsrdlticket' cookie for: {self.url.url}")
        response = self.session.get(
            f"https://www.thesimsresource.com/ajax.php?c=downloads&a=initDownload&itemid={self.url.itemId}&format=zip"
        )
        self.session.get(self.url.downloadUrl)
        self.ticketInitializedTime = time.time() * 1000
        return response.cookies.get("tsrdlticket")