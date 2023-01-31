from exceptions import InvalidURL
import re


class TSRUrl:
    def __init__(self, url: str):
        if self.__isValidUrl(url):
            self.url = url
            self.itemId = int(re.search("(?<=id/)[\d]+", url)[0])
            self.downloadUrl = f"https://www.thesimsresource.com/downloads/download/itemId/{self.itemId}"
        else:
            raise InvalidURL(url)

    @classmethod
    def __isValidUrl(self, url: str) -> bool:
        return re.search("thesimsresource.com/downloads/details/id/[\d]+", url) != None
