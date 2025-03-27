# Source Generated with Decompyle++
# File: maintainForm.pyc (Python 2.5)

'''
MainForm is the main window. 
2009-07-02 created by Mavis
'''
import sys
from PyQt4 import QtCore, QtGui
from main_ui import Ui_MainUiForm
import config
import os
from component import gifButton, PicTrans, ctrButton, virtualComponent
from squery import socketQuery

class MainForm(QtGui.QMainWindow):
    
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainUiForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 2024)
        self.setFixedSize(768, 2024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('/home/mm/kiosk/var/gui/sys/remotely_maintaining.jpg')))
        self.setPalette(palette)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = MainForm()
    mainf.show()
    sys.exit(app.exec_())

