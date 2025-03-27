# Source Generated with Decompyle++
# File: kioskInfoForm.pyc (Python 2.5)

'''
KioskInfoForm 
2009-07-29 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
from configForm_ui import Ui_configForm
import config
import component
from info_component import Information

class KioskInfoForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_configForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_information)))
        self.setPalette(palette)
        self.ui.txt_config_label.setText(QtGui.QApplication.translate('Information', 'Information', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_logout = component.btnLogout(self, 'KioskInfoForm')
        self.ui.btn_logout.setGeometry(580, 20, 160, 68)
        self.ui.btn_cancel = component.btnCancel(self, 'KioskInfoForm')
        self.ui.btn_back = component.btnBack(self, 'KioskInfoForm')
        self.ui.gridlayout.addWidget(self.ui.btn_cancel, 0, 0)
        self.ui.gridlayout.addWidget(self.ui.btn_back, 0, 1)
        self.ui.gridLayout.setGeometry(QtCore.QRect(80, 920, 568, 90))
        self.ui.ctr_information = Information(self)
        self.ui.ctr_information.setGeometry(config.layout_x, config.layout_y, config.layout_width, config.layout_height * 3)
        self.ui.btn_restore = component.ctrButton(self, 'KioskInfoForm', 'btn_restore', QtGui.QApplication.translate('Information', 'Restore Factory Settings', None, QtGui.QApplication.UnicodeUTF8), 350, config.btnHeight, 'color: white; font: bold italic 23px; border-style: outset; background-image: url(' + config.pic_btn_config_red2 + ')')
        self.ui.btn_restore.setGeometry(380, config.layout_y + self.ui.ctr_information.height() + 30, 350, config.btnHeight)
        self.ui.KioskInfoForm_ctr_num_keyboard = component.numKeyboard('KioskInfoForm', self)
        self.ui.KioskInfoForm_ctr_num_keyboard.hide()
        self.ui.KioskInfoForm_ctr_message_box = component.messageBox('KioskInfoForm', self)

    
    def hideEvent(self, event):
        self.ui.KioskInfoForm_ctr_message_box.hide()
        self.ui.KioskInfoForm_ctr_num_keyboard.hide()
        self.hide()

    
    def showEvent(self, event):
        self.ui.ctr_information.retranslateUi(self)
        self.ui.txt_config_label.setText(QtGui.QApplication.translate('Information', 'Information', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_logout.reset()
        self.ui.btn_cancel.hide()
        self.ui.btn_back.reset()
        self.ui.btn_restore.setText(QtGui.QApplication.translate('Information', 'Restore Factory Settings', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_es.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = KioskInfoForm()
    mainf.show()
    data = {
        'ctr_information': {
            'kiosk_id': 'LAKSJDF09',
            'capacity': 'CASDF',
            'today': '2009-8-8',
            'firmware': 'ASDF',
            'ip': '192.168.14.1',
            'external_ip': '192.168.14.2',
            'kiosk_soft': 'ASDF',
            'mac': '2983SAFS',
            'start_time': '2009-8-8',
            'kiosk_time_zone': '2009-8-8',
            'umg_channel': 'ASDFAS' } }
    mainf.ui.ctr_information.setReport(data)
    mainf.ui.KioskInfoForm_ctr_num_keyboard.show({
        'type': 'password' })
    sys.exit(app.exec_())

