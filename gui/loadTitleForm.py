# Source Generated with Decompyle++
# File: loadTitleForm.pyc (Python 2.5)

'''
LoadTitleEnterForm
2009-07-20 created by Mavis
'''
import os
import sys
import config
from component import allKeyboard, btnLogout, btnBack, btnCancel
from PyQt4 import QtCore, QtGui
from load_title_ui import Ui_loadTitleForm
from squery import socketQuery

class LoadTitleEnterForm(QtGui.QMainWindow):
    
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_loadTitleForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_load)))
        self.setPalette(palette)
        self.ui.btn_logout = btnLogout(self, 'LoadTitleEnterForm')
        self.ui.btn_logout.setGeometry(580, 20, 160, 68)
        self.ui.btn_cancel = btnCancel(self, 'LoadTitleEnterForm')
        self.ui.btn_back = btnBack(self, 'LoadTitleEnterForm')
        self.ui.hboxlayout.addWidget(self.ui.btn_cancel)
        self.ui.hboxlayout.addWidget(self.ui.btn_back)
        self.sq = socketQuery()
        self.ui.LoadTitleEnterForm_ctr_all_keyboard = allKeyboard('LoadTitleEnterForm', self)

    
    def showEvent(self, event):
        self.ui.retranslateUi('')
        self.ui.btn_logout.reset()
        self.ui.btn_cancel.hide()
        self.ui.btn_back.reset()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = LoadTitleEnterForm()
    mainf.show()
    sys.exit(app.exec_())

