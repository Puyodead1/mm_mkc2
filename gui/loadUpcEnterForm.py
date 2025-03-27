# Source Generated with Decompyle++
# File: loadUpcEnterForm.pyc (Python 2.5)

'''
LoadUpcEnterForm
2009-07-20 created by Mavis
'''
import os
import sys
import config
from component import numKeyboard, btnLogout, btnCancel, btnBack
from PyQt4 import QtCore, QtGui
from load_title_ui import Ui_loadTitleForm

class LoadUpcEnterForm(QtGui.QMainWindow):
    
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_loadTitleForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_load)))
        self.setPalette(palette)
        self.ui.txtbox_msg.setText(QtGui.QApplication.translate('Form', 'Please enter the UPC', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_logout = btnLogout(self, 'LoadUpcEnterForm')
        self.ui.btn_logout.setGeometry(580, 20, 160, 68)
        self.ui.btn_cancel = btnCancel(self, 'LoadUpcEnterForm')
        self.ui.btn_back = btnBack(self, 'LoadUpcEnterForm')
        self.ui.hboxlayout.addWidget(self.ui.btn_cancel)
        self.ui.hboxlayout.addWidget(self.ui.btn_back)
        self.ui.LoadUpcEnterForm_ctr_num_keyboard = numKeyboard('LoadUpcEnterForm', self, (768 - config.bg_kb_width) / 2, self.ui.txtbox_msg.y() + self.ui.txtbox_msg.height() + 50)
        self.ui.LoadUpcEnterForm_ctr_num_keyboard.hide()

    
    def showEvent(self, event):
        self.ui.retranslateUi('')
        self.ui.btn_logout.reset()
        self.ui.btn_cancel.hide()
        self.ui.btn_back.reset()
        self.ui.txtbox_msg.setText(QtGui.QApplication.translate('Form', 'Please enter the UPC', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = LoadUpcEnterForm()
    mainf.show()
    mainf.ui.LoadUpcEnterForm_ctr_num_keyboard.show()
    sys.exit(app.exec_())

