from __future__ import annotations
from exceptions import InvalidURL
from logger import logger
import re, requests


class TSRUrl:
    def __init__(self, url: str):
        if self.__isValidUrl(url):
            self.url = url
            self.itemId = self.__getItemId(url)
            self.downloadUrl = f"https://www.thesimsresource.com/downloads/download/itemId/{self.itemId}"
        else:
            raise InvalidURL(url)

    @classmethod
    def __getItemId(self, url: str) -> int | None:
        itemId = (
            re.search("(?<=/id/)[\d]+", url)
            or re.search("(?<=/itemId/)[\d]+", url)
            or re.search("(?<=.com/downloads/)[\d]+", url)
        )
        logger.debug(
            f"Got ItemId: {itemId[0] if itemId is not None else 'None'} from Url: {url}"
        )
        return None if itemId == None else int(itemId[0])

    @classmethod
    def __isValidUrl(self, url: str) -> bool:
        isUrlValid = (
            re.search("thesimsresource.com/", url) != None
            and self.__getItemId(url) != None
        )
        logger.debug(f"Is url valid: {isUrlValid}")
        return isUrlValid

    def isVipExclusive(self) -> bool:
        r = requests.get(self.url)
        return "VIP Exclusive" in r.text

    @staticmethod
    def getRequiredItems(url: "TSRUrl") -> list["TSRUrl"]:
        def convertHrefToTSRUrl(href: str) -> TSRUrl:
            logger.debug(f"Converting {href} to TSRUrl")
            return TSRUrl(f"https://www.thesimsresource.com{href}")

        logger.debug(f"Getting required items for {url.url}")
        r = requests.get(f"https://www.thesimsresource.com/downloads/{url.itemId}")
        return list(
            map(
                convertHrefToTSRUrl,
                re.findall(
                    '(?<=<li class="required-download-item"><a href=")/downloads/[\d]+(?=")',
                    r.text,
                ),
            )
        )
