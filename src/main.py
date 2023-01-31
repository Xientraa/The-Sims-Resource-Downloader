from TSRUrl import TSRUrl


if __name__ == "__main__":
    url = TSRUrl("https://www.thesimsresource.com/downloads/download/itemId/1632083")
    print(url.getTSRDLTicketCookie())
    print(url.getDownloadWaitPageURL())
    print(url.initiatedAt)
