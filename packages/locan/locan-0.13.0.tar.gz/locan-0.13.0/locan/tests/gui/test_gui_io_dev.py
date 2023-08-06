"""

This module contains tests that need gui interactions.

"""
import pytest

from locan import ROOT_DIR
from locan.dependencies import HAS_DEPENDENCY
from locan.gui.io import file_dialog


pytestmark = pytest.mark.qt


def test_file_dialog_no_qt():
    if not HAS_DEPENDENCY["qt"]:
        with pytest.raises(ImportError):
            file_dialog()


@pytest.mark.gui
@pytest.mark.skipif(not HAS_DEPENDENCY["qt"], reason="requires qt_binding.")
def test_file_dialog():
    file_path = ROOT_DIR / "tests/test_data/rapidSTORM_dstorm_data.txt"
    result = file_dialog(directory=file_path, message="Select single file")
    # result = file_dialog()
    print(result)
    assert len(result) == 1
    assert result == str(file_path)


@pytest.mark.gui
@pytest.mark.skipif(not HAS_DEPENDENCY["qt"], reason="requires qt_binding.")
def test_file_dialog():
    file_path = ROOT_DIR / "tests/test_data/rapidSTORM_dstorm_data.txt"
    result = file_dialog(directory=file_path, message="Select single file")
    # result = file_dialog()
    print(result)
    assert len(result) == 1
    assert result == str(file_path)

##########################
@pytest.mark.gui
@pytest.mark.skipif(not HAS_DEPENDENCY["qt"], reason="requires qt_binding.")
def test_qtbot():
    from qtpy.QtWidgets import QApplication
    #app = QApplication([])
    directory = ROOT_DIR / "tests/test_data/rapidSTORM_dstorm_data.txt"
    result = file_dialog(directory=directory, message="Select single file")
    #print(app.allWidgets())


@pytest.mark.gui
@pytest.mark.skipif(not HAS_DEPENDENCY["qt"], reason="requires qt_binding.")
def test_qtbot_(qtbot):
    from qtpy.QtWidgets import QWidget, QApplication
    from qtpy.QtCore import Qt
    app = QApplication([])
    app.exec_()
    widget = QWidget()
    qtbot.addWidget(widget)
    qtbot.mouseClick(widget.findButton, Qt.LeftButton)


@pytest.mark.gui
@pytest.mark.skipif(not HAS_DEPENDENCY["qt"], reason="requires qt_binding.")
def test_qtbot__(qtbot):
    from qtpy.QtWidgets import QWidget, QApplication
    from qtpy.QtCore import Qt
    app = QApplication([])
    directory = ROOT_DIR / "tests/test_data/rapidSTORM_dstorm_data.txt"
    result = file_dialog(directory=directory, message="Select single file")
    widget = QApplication.activePopupWidget()
    print(widget)
    # qtbot.addWidget(widget)
    # qtbot.mouseClick(widget.findButton, Qt.LeftButton)
