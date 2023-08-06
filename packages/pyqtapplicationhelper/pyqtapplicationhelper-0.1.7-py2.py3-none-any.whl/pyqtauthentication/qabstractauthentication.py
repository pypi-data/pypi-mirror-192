from PyQt6.QtWidgets import QDialog, QWidget


class QAbstactAuthenticationDialog(QDialog):
    def __init__(
        self,
        parent: QWidget = None,
        **kwargs
    ) -> None:
        """_summary_

        Args:
            parent (QWidget, optional): _description_. Defaults to None.
        """

        super().__init__(parent, **kwargs)
