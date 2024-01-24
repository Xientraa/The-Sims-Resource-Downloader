from __future__ import annotations
import requests, webbrowser, os
from exceptions import InvalidCaptchaCode
from typing import Optional
from logger import logger

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TSRSession:
    @classmethod
    def __init__(self, sessionId: Optional[str] = None) -> None:
        logger.debug("Creating new TSRSession")
        self.session = requests.Session()
        if sessionId is not None:
            logger.debug("SessionId is not none")
            if self.__isValidSessionId(sessionId):
                logger.debug("SessionId is valid")
                self.tsrdlsession = sessionId
                return

        self.__getTSRDLTicketCookie()
        self.__saveCaptchaImage()
        self.__openImageInBrowser()
        self.tsrdlsession = None

        print("Please enter captcha code:")
        captchaInput = input(">> ")
        if self.__tryCaptchaCode(captchaInput):
            self.tsrdlsession = self.session.cookies.get_dict().get("tsrdlsession")
        else:
            raise InvalidCaptchaCode

    @classmethod
    def __tryCaptchaCode(self, code: str) -> bool:
        logger.debug(f"Testing captcha code: {code}")
        r = self.session.post(
            "https://www.thesimsresource.com/downloads/session/itemId/1646133",
            data={"captchavalue": code},
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": "https://www.thesimsresource.com",
            },
            allow_redirects=True,
        )

        isDownloadUrl = (
            r.url == "https://www.thesimsresource.com/downloads/download/itemId/1646133"
        )
        logger.debug(f"Captcha successfully completed: {isDownloadUrl}")
        return isDownloadUrl

    @classmethod
    def __isValidSessionId(self, sessionId: str) -> bool:
        logger.debug(f"Checking if SessionId: {sessionId} is valid")
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
        logger.debug("Getting captcha image")
        self.session.get(
            "https://www.thesimsresource.com/downloads/session/itemId/1646133"
        )
        return self.session.get(
            "https://www.thesimsresource.com/downloads/captcha-image"
        )

    @classmethod
    def __saveCaptchaImage(self):
        logger.debug("Saving captcha image")
        with open(f"{CURRENT_DIR}/captcha.png", "wb") as f:
            for chunk in self.__getCaptchaImage().iter_content(1024 * 1024):
                f.write(chunk)

    @classmethod
    def __openImageInBrowser(self) -> None:
        webbrowser.open_new_tab(f"{CURRENT_DIR}/captcha.png")

    @classmethod
    def __getTSRDLTicketCookie(self) -> str:
        logger.debug("Getting TSRDLTicket cookie")
        response = self.session.get(
            f"https://www.thesimsresource.com/ajax.php?c=downloads&a=initDownload&itemid=1646133&setItems=&format=zip"
        )
        return response.cookies.get("tsrdlticket")
