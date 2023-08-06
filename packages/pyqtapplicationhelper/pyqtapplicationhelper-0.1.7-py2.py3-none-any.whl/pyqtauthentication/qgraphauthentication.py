from .qwebauthentication import QWebAuthenticationDialog

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import pyqtSignal, QUrl, Qt
from PyQt6.QtWidgets import QWidget

class QGraphAuthenticationDialog(QWebAuthenticationDialog):

    def __init__(
        self,
        parent: QWidget = None,
        **kwargs,
    ) -> None:
        """_summary_

        Args:
            parent (QWidget, optional): _description_. Defaults to None.
        """

        super().__init__(parent, **kwargs)

        self.setWindowTitle("Sign In")
        self.web.setFixedWidth(500)
        self.web.setFixedHeight(500)