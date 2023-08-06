from typing import Optional
from os.path import exists

from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QTextBrowser, QDialogButtonBox
from PyQt6.QtCore import Qt
from markdown import markdown


class ChangeLogDialog(QDialog):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.setLayout(layout)

        self.setWindowTitle("Change Log")

        self.textBrowser = QTextBrowser(self)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.addButton(QDialogButtonBox.StandardButton.Close)
        self.buttonBox.rejected.connect(self.reject)

        self.layout().addWidget(self.textBrowser)
        self.layout().addWidget(self.buttonBox)

    def setFile(self, filepath: str) -> None:
        """Loads converted MD file into text browser
        """

        if not exists(change_log := filepath):
            raise Exception(f"Unable to find change log file ({change_log})")

        html = ConvertMdToHtml(change_log)

        self.textBrowser.setText(html)

def ConvertMdToHtml(file_path: str) -> str:
        """Reads file and converts MD to Html

        Args:
            file_path (str): MD file path

        Returns:
            str: Converted Html
        """

        with open(file_path) as file:
            return markdown(file.read())