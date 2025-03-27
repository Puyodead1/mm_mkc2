# Source Generated with Decompyle++
# File: superAdminDistanceForm.pyc (Python 2.5)

'''
SuperAdminDistanceForm 
2009-07-29 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
from configForm_ui import Ui_configForm
import config
import component

class SuperAdminDistanceForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_configForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_load)))
        self.setPalette(palette)
        self.ui.txt_config_label.setText(QtGui.QApplication.translate('Form', 'Super Admin', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_logout = component.btnLogout(self, 'SuperAdminDistanceForm')
        self.ui.btn_logout.setGeometry(580, 20, 160, 68)
        self.ui.btn_ok = component.ctrButton(self, 'SuperAdminDistanceForm', 'btn_ok', QtGui.QApplication.translate('Coupon', 'Ok', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_ok.setGeometry(QtCore.QRect(580, 930, 160, 68))
        self.ui.txt_msg = QtGui.QLabel(self)
        self.ui.txt_msg.setStyleSheet('color: #0060b4; font: bold 26px;')
        self.ui.txt_msg.setGeometry(60, 338, 648, 50)
        self.ui.txt_result = QtGui.QLabel(self)
        self.ui.txt_result.setStyleSheet('color: #0060b4; font: bold 26px;')
        self.ui.txt_result.setGeometry(60, 780, 648, 50)
        self.ui.SuperAdminDistanceForm_ctr_message_box = component.messageBox('SuperAdminDistanceForm', self)

    
    def hideEvent(self, event):
        self.ui.SuperAdminDistanceForm_ctr_message_box.hide()
        self.hide()

    
    def showEvent(self, event):
        self.ui.txt_config_label.setText(QtGui.QApplication.translate('Form', 'Super Admin', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_logout.reset()
        self.ui.btn_ok.setText(QtGui.QApplication.translate('Coupon', 'Ok', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainf = SuperAdminDistanceForm()
    mainf.show()
    mainf.ui.SuperAdminDistanceForm_ctr_message_box.show({
        'message': 'jlajsldjflaksjd',
        'type': 'confirm' })
    sys.exit(app.exec_())

