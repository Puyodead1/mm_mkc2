# Source Generated with Decompyle++
# File: membershipProfileForm.pyc (Python 2.5)

'''
MembershipProfileForm 
2010-07-02 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
import component
import config
from squery import socketQuery

class MembershipProfileForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = QtCore.QObject()
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_member)))
        self.setPalette(palette)
        self.ui.txtbox_msg = QtGui.QLabel(self)
        self.ui.txtbox_msg.setGeometry(QtCore.QRect(60, 137, 571, 60))
        self.ui.txtbox_msg.setStyleSheet(config.style_membership_card)
        self.label_card = QtGui.QLabel('Card Number:', self)
        self.label_card.setStyleSheet(config.style_membership_msg_blue)
        self.ui.card_number = QtGui.QLabel(self)
        self.ui.card_number.setStyleSheet(config.style_membership_msg)
        self.label_email = QtGui.QLabel('Email address:', self)
        self.label_email.setStyleSheet(config.style_membership_msg_blue)
        self.ui.email = QtGui.QLabel(self)
        self.ui.email.setStyleSheet(config.style_membership_msg)
        gl = QtGui.QGridLayout()
        gl.setContentsMargins(0, 0, 0, 0)
        gl.setSpacing(10)
        gl.addWidget(self.label_card, 0, 0)
        gl.addWidget(self.ui.card_number, 0, 1, 1, 2)
        gl.addWidget(self.label_email, 1, 0)
        gl.addWidget(self.ui.email, 1, 1, 1, 2)
        self.ui.txt_msg = QtGui.QLabel(self)
        self.ui.txt_msg.setStyleSheet(config.style_membership_msg_big)
        self.ui.txt_msg.setWordWrap(True)
        self.ui.txt_msg.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.btn_back = component.btnBack(self, 'MembershipProfileForm')
        self.ui.horizontalLayout = QtGui.QWidget(self)
        self.ui.horizontalLayout.setGeometry(QtCore.QRect(50, 910, 661, 91))
        self.ui.horizontalLayout.setObjectName('horizontalLayout')
        self.ui.hboxlayout = QtGui.QHBoxLayout(self.ui.horizontalLayout)
        self.ui.hboxlayout.setSpacing(50)
        self.ui.hboxlayout.setObjectName('hboxlayout')
        self.ui.hboxlayout.addWidget(self.ui.btn_back)
        self.ui.btn_password = component.ctrButton(self, 'MembershipProfileForm', 'btn_password', '', 350, 65, config.style_btn_big)
        self.ui.ctr_btn_center = component.btnCenter(self, 'MembershipProfileForm')
        vl = QtGui.QVBoxLayout()
        vl.setContentsMargins(50, 130, 50, config.kb_all_height + 10)
        vl.addWidget(self.ui.txtbox_msg, 0, QtCore.Qt.AlignTop)
        vl.addLayout(gl)
        vl.addWidget(QtGui.QWidget(self))
        vl.addWidget(self.ui.btn_password)
        vl.addWidget(self.ui.txt_msg)
        self.setLayout(vl)
        self.ui.MembershipProfileForm_ctr_all_keyboard = component.allKeyboard('MembershipProfileForm', self, config.kb_all_height - 10)
        self.ui.MembershipProfileForm_ctr_all_keyboard.hide()

    
    def showEvent(self, event):
        self.ui.ctr_btn_center.init()
        self.ui.btn_back.reset()
        self.ui.txtbox_msg.setText(QtGui.QApplication.translate('Form', 'My Profile', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_password.setText(QtGui.QApplication.translate('Form', 'Change Password', None, QtGui.QApplication.UnicodeUTF8))
        self.label_card.setText(QtGui.QApplication.translate('Form', 'Card Number:', None, QtGui.QApplication.UnicodeUTF8))
        self.label_email.setText(QtGui.QApplication.translate('Form', 'Email address:', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = MembershipProfileForm()
    mainf.setGeometry(0, 0, 768, 1024)
    mainf.show()
    mainf.ui.card_number.setText('20937492734789')
    mainf.ui.email.setText('kajls@sjkfj.com')
    mainf.ui.txt_msg.setText('Your password has been changed successful. a')
    sys.exit(app.exec_())

