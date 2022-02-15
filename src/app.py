import sys
import pydicomviewer_rc
from PySide2.QtWidgets import QApplication
from .mainwindow import MainWindow
                                                     
def run():
    app = QApplication([])                              
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())