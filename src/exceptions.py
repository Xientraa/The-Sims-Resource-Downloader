from requests.cookies import RequestsCookieJar


class InvalidURL(Exception):
    def __init__(self, url: str):
        self.url = url


class InvalidDownloadTicket(Exception):
    def __init__(self, url: str, cookies: RequestsCookieJar):
        self.url = url
        self.cookies = cookies


class InvalidCaptchaCode(Exception):
    pass
