# Source Generated with Decompyle++
# File: cerepayTopupErrorForm.pyc (Python 2.5)

import os
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
import component
import config
_Form_Name_String = 'CerepayTopupErrorForm'

class CerepayTopupErrorForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = QtCore.QObject()
        self.setGeometry(0, 0, 768, 1024)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_movie)))
        self.setPalette(palette)
        self.ui.ctr_btn_center = component.btnCenter(self, _Form_Name_String)
        self.ui.btn_back = component.btnBack(self, _Form_Name_String)
        self.ui.btn_back.setGeometry(580, 20, 160, 68)
        '\n        self.ui.title_label = QtGui.QLabel(self)\n        self.ui.title_label.setGeometry(QtCore.QRect(50,30,411,50))\n        \n        palette = QtGui.QPalette()\n\n        brush = QtGui.QBrush(QtGui.QColor(255,255,255))\n        brush.setStyle(QtCore.Qt.SolidPattern)\n        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.WindowText,brush)\n\n        brush = QtGui.QBrush(QtGui.QColor(255,255,255))\n        brush.setStyle(QtCore.Qt.SolidPattern)\n        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.WindowText,brush)\n\n        brush = QtGui.QBrush(QtGui.QColor(127,125,123))\n        brush.setStyle(QtCore.Qt.SolidPattern)\n        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.WindowText,brush)\n        self.ui.title_label.setPalette(palette)\n        \n        font = QtGui.QFont()\n        font.setPointSize(30)\n        font.setWeight(75)\n        font.setBold(True)\n        self.ui.title_label.setFont(font)\n        '
        self.title_label = QtGui.QLabel(self)
        self.title_label.setFixedHeight(30)
        self.title_label.setStyleSheet(config.style_membership_card)
        self.ui.txt_process_label = QtGui.QLabel(self)
        self.ui.txt_process_label.setFixedHeight(30)
        self.ui.txt_process_label.setStyleSheet(config.style_membership_msg_blue + 'color: black;')
        self.ui.txt_msg = QtGui.QLabel(self)
        self.ui.txt_msg.setMaximumHeight(50)
        self.ui.txt_msg.setWordWrap(True)
        self.ui.txt_msg.setStyleSheet(config.style_membership_card + 'color:#bb0000;')
        self.ui.txt_msg_detail = QtGui.QLabel(self)
        self.ui.txt_msg_detail.setMaximumHeight(50)
        self.ui.txt_msg_detail.setWordWrap(True)
        self.ui.txt_msg_detail.setStyleSheet(config.style_membership_msg_blue + 'color: black;')
        vlayout = QtGui.QVBoxLayout()
        vlayout.setContentsMargins(80, 150, 80, 10)
        vlayout.addWidget(self.ui.txt_process_label)
        vlayout.addSpacing(150)
        vlayout.addWidget(self.ui.txt_msg)
        vlayout.addSpacing(100)
        vlayout.addWidget(self.ui.txt_msg_detail)
        vlayout.addStretch(1)
        self.setLayout(vlayout)

    
    def showEvent(self, event):
        self.ui.ctr_btn_center.init()
        self.ui.txt_process_label.setText(QtGui.QApplication.translate('Form', 'Processing ... ', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.txt_msg.setText(QtGui.QApplication.translate('Form', 'DO NOT POWER OFF THE KIOSK', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.txt_msg_detail.setText(QtGui.QApplication.translate('Form', 'If the kiosk stops responding for more than 15 minutes, please contact our tech support.', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = CerepayTopupErrorForm()
    mainf.show()
    sys.exit(app.exec_())

