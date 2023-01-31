class InvalidURL(Exception):
    def __init__(self, url):
        self.url = url


class InvalidDownloadTicket(Exception):
    def __init__(self, url):
        self.url = url
