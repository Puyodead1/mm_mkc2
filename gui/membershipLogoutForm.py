# Source Generated with Decompyle++
# File: membershipLogoutForm.pyc (Python 2.5)

'''
MembershipLogoutForm 
2010-08-18 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
from component import ctrButton
import config

class MembershipLogoutForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = QtCore.QObject()
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_member)))
        self.setPalette(palette)
        self.txtbox_msg = QtGui.QLabel(self)
        self.txtbox_msg.setGeometry(QtCore.QRect(60, 137, 571, 60))
        self.txtbox_msg.setStyleSheet(config.style_membership_card)
        self.ui.txt_msg = QtGui.QLabel(self)
        self.ui.txt_msg.setStyleSheet(config.style_membership_msg_blue)
        self.btn_yes = ctrButton(self, 'MembershipLogoutForm', 'btn_yes', QtGui.QApplication.translate('Form', 'Yes', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.btn_no = ctrButton(self, 'MembershipLogoutForm', 'btn_no', QtGui.QApplication.translate('Form', 'No', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnBlueStyle)
        hl = QtGui.QHBoxLayout()
        hl.addWidget(self.btn_yes)
        hl.addWidget(self.btn_no)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.ui.txt_msg)
        layout.addLayout(hl)
        w = QtGui.QWidget(self)
        w.setGeometry(60, 137 + 60 + 10, 768 - 120, 300)
        w.setLayout(layout)

    
    def showEvent(self, event):
        self.btn_yes.setText(QtGui.QApplication.translate('Form', 'Yes', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_no.setText(QtGui.QApplication.translate('Form', 'No', None, QtGui.QApplication.UnicodeUTF8))
        self.txtbox_msg.setText(QtGui.QApplication.translate('Form', 'Logout', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_en.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = MembershipLogoutForm()
    mainf.setGeometry(0, 0, 768, 1024)
    mainf.show()
    sys.exit(app.exec_())

