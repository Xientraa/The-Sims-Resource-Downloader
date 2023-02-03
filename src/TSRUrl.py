from exceptions import InvalidURL
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
        return None if itemId == None else int(itemId[0])

    @classmethod
    def __isValidUrl(self, url: str) -> bool:
        return (
            re.search("thesimsresource.com/", url) != None
            and self.__getItemId(url) != None
        )

    @staticmethod
    def getRequiredItems(url: "TSRUrl") -> list["TSRUrl"]:
        def convertHrefToTSRUrl(href: str) -> TSRUrl:
            return TSRUrl(f"https://www.thesimsresource.com{href}")

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
