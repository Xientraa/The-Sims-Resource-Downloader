import requests, re, time


class TSRUrl:
    def __init__(self, url: str):
        self.url = url
        self.tsrdlTicketCookie = ""
        self.initiatedAt = -1

    def getTSRDLTicketCookie(self) -> str:
        r = requests.session().get(
            f"https://www.thesimsresource.com/ajax.php?c=downloads&a=initDownload&itemid={self.getItemIdFromURL()}&format=zip"
        )
        self.tsrdlTicketCookie = r.cookies.get("tsrdlticket")
        self.initiatedAt = time.time() * 1000
        return self.tsrdlTicketCookie

    def getItemIdFromURL(self) -> int | None:
        itemIdSearch = re.search(
            "(?<=thesimsresource.com/downloads/download/itemId/)[\d]+", self.url
        )
        return int(itemIdSearch[0]) if itemIdSearch != None else None

    def getDownloadWaitPageURL(self) -> str:
        return f"https://www.thesimsresource.com/downloads/download/itemId/{self.getItemIdFromURL()}"

    def isItemURL(self) -> bool:
        return "thesimsresource.com/downloads/download/itemId/" in self.url
