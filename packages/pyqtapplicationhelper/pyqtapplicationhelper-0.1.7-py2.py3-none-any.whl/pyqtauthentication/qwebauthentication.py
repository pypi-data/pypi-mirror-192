from PyQt6.QtWidgets import QWidget
from .qabstractauthentication import QAbstactAuthenticationDialog
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import pyqtSignal, QUrl, Qt

from urllib.parse import urlparse, parse_qs


class QWebAuthenticationDialog(QAbstactAuthenticationDialog):

    redirected = pyqtSignal()
    autherror = pyqtSignal()
    userClosed = pyqtSignal()

    def __init__(
        self,
        parent: QWidget = None,
        redirect_url: str = None,
        **kwargs,
    ) -> None:
        """_summary_

        Args:
            parent (QWidget, optional): _description_. Defaults to None.
        """

        super().__init__(parent, **kwargs)

        self.redirect_url = redirect_url
        self.setWindowTitle("Sign In")
        self.web = QWebEngineView(self)
        self.setWindowFlags(Qt.WindowType.Dialog)
        self.web.urlChanged.connect(self.isRedirected)
        self.redirected.connect(self.accept)
        self.autherror.connect(self.reject)
        self.accepted.connect(lambda: print("accept"))

    def setURL(
        self,
        url: str
    ) -> None:
        """_summary_

        Args:
            url (str): _description_
        """
        self.web.setUrl(QUrl(url))

    def isRedirected(
        self,
        url: QUrl
    ) -> None:
        """_summary_

        Args:
            url (QUrl): _description_
        """
        if self.redirect_url in str(url):
            return_info = parse_redirect_url(url.toString())
            if 'error' in return_info.keys():
                self.autherror.emit()
            else:
                self.redirected.emit()


def parse_redirect_url(URL: str) -> dict:
    parsed_url = urlparse(URL)
    return parse_qs(parsed_url.query)
