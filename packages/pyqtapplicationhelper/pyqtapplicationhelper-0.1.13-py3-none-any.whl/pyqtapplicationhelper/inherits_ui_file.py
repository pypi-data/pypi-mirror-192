from os.path import join
from PyQt6.QtCore import QFile
from PyQt6 import uic
from PyQt6.QtCore import QIODevice


def load_ui_from_file(name: str, dir_path: str):
    """
    Returns a tuple from uic.loadUiType(), loading the ui file with the given name.
    :param name:
    :return:
    """
    ui_file = _get_ui_qfile(name, dir_path)
    try:
        base_type = uic.loadUiType(ui_file)
    finally:
        ui_file.close()
    return base_type


def _get_ui_qfile(name: str, dir_path: str) -> QFile:
    """
    Returns an opened, read-only QFile for the given QtDesigner UI file name. Expects a plain name like "centralwidget".
    The file ending and resource path is added automatically.
    Raises FileNotFoundError, if the given ui file does not exist.
    :param name:
    :return:
    """
    file_path = join(dir_path,f"{name}.ui")
    file = QFile(file_path)
    if not file.exists():
        raise FileNotFoundError("UI file not found: " + file_path)
    file.open(QIODevice.OpenModeFlag.ReadOnly)
    return file


"""
This renamed function is supposed to be used during class definition to make the intention clear.
Usage example:
class SomeWidget(*inherits_from_ui_file_with_name("SomeWidgetUiFileName")):
    def __init__(self, parent):
        super(SomeWidget, self).__init__(parent)
        self.setupUi(self)
"""
inherits_from_ui_file_with_name = load_ui_from_file
