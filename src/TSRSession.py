import requests, webbrowser
from exceptions import InvalidCaptchaCode
from typing import Optional


class TSRSession:
    @classmethod
    def __init__(self, sessionId: Optional[str] = None) -> None:
        self.session = requests.Session()
        if sessionId is not None:
            if self.__isValidSessionId(sessionId):
                return

        self.__getTSRDLTicketCookie()
        self.__saveCaptchaImage()
        self.__openImageInBrowser()
        self.tsrdlsession = None

        captchaInput = input(">> ")
        if self.__tryCaptchaCode(captchaInput):
            self.tsrdlsession = self.session.cookies.get_dict().get("tsrdlsession")
        else:
            raise InvalidCaptchaCode

    @classmethod
    def __tryCaptchaCode(self, code: str) -> bool:
        r = self.session.post(
            "https://www.thesimsresource.com/downloads/session/itemId/1646133",
            data={"captchavalue": code},
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": "https://www.thesimsresource.com",
            },
            allow_redirects=True,
        )
        return (
            r.url == "https://www.thesimsresource.com/downloads/download/itemId/1646133"
        )

    @classmethod
    def __isValidSessionId(self, sessionId: str) -> bool:
        self.__getTSRDLTicketCookie()
        r = self.session.get(
            "https://www.thesimsresource.com/downloads/download/itemId/1646133",
            cookies={"tsrdlsession": sessionId},
        )
        return (
            r.url == "https://www.thesimsresource.com/downloads/download/itemId/1646133"
        )

    @classmethod
    def __getCaptchaImage(self) -> requests.Request:
        self.session.get(
            "https://www.thesimsresource.com/downloads/session/itemId/1646133"
        )
        return self.session.get(
            "https://www.thesimsresource.com/downloads/captcha-image"
        )

    @classmethod
    def __saveCaptchaImage(self):
        with open("./captcha.png", "wb") as f:
            for chunk in self.__getCaptchaImage().iter_content(1024 * 1024):
                f.write(chunk)

    @classmethod
    def __openImageInBrowser(self) -> None:
        webbrowser.open_new_tab("./captcha.png")

    @classmethod
    def __getTSRDLTicketCookie(self) -> str:
        response = self.session.get(
            f"https://www.thesimsresource.com/ajax.php?c=downloads&a=initDownload&itemid=1646133&format=zip"
        )
        return response.cookies.get("tsrdlticket")
