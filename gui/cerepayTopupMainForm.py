# Source Generated with Decompyle++
# File: cerepayTopupMainForm.pyc (Python 2.5)

import os
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
import component
import config
_Form_Name_String = 'CerepayTopupMainForm'

class CerepayTopupMainForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = QtCore.QObject()
        self.setGeometry(0, 0, 768, 1024)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_movie)))
        self.setPalette(palette)
        self.ui.btn_cancel = component.btnCancel(self, _Form_Name_String)
        self.ui.btn_cancel.setGeometry(280, 930, 160, 68)
        self.ui.CerepayTopupMainForm_ctr_num_keyboard = component.NumberKeyboardWithDot(_Form_Name_String, self)
        self.ui.CerepayTopupMainForm_ctr_num_keyboard.hide()
        self.ui.ctr_btn_center = component.btnCenter(self, _Form_Name_String)
        self.ui.btn_back = component.btnBack(self, _Form_Name_String)
        self.ui.btn_back.setGeometry(580, 20, 160, 68)
        self.title_label = QtGui.QLabel(self)
        self.title_label.setFixedHeight(30)
        self.title_label.setStyleSheet(config.style_membership_card)
        self.ui.txt_msg = QtGui.QLabel(self)
        self.ui.txt_msg.setMaximumHeight(50)
        self.ui.txt_msg.setWordWrap(True)
        self.ui.txt_msg.setStyleSheet(config.style_membership_msg)
        vlayout = QtGui.QVBoxLayout()
        vlayout.setContentsMargins(50, 150, 50, 10)
        vlayout.addWidget(self.title_label)
        vlayout.addSpacing(150)
        vlayout.addWidget(self.ui.txt_msg)
        vlayout.addStretch(1)
        self.setLayout(vlayout)

    
    def showEvent(self, event):
        self.ui.ctr_btn_center.init()
        self.ui.btn_back.reset()
        self.ui.btn_cancel.reset()
        self.title_label.setText(QtGui.QApplication.translate('Form', 'Top Up', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.txt_msg.setText(QtGui.QApplication.translate('Form', 'Please input the amount you want to top up.', None, QtGui.QApplication.UnicodeUTF8))

    
    def hideEvent(self, event):
        self.ui.CerepayTopupMainForm_ctr_num_keyboard.hide()
        self.hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = CerepayTopupMainForm()
    mainf.show()
    sys.exit(app.exec_())

