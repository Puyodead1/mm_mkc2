# Source Generated with Decompyle++
# File: configNetworkDiagnosisForm.pyc (Python 2.5)

'''
ConfigNetworkDiagnosisForm 
2009-07-26 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
from configForm_ui import Ui_configForm
import config
import component

class ConfigNetworkDiagnosisForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = component.ConfigForm('ConfigNetworkDiagnosisForm', self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_config)))
        self.setPalette(palette)
        self.ui.txt_status = QtGui.QTextEdit(self)
        self.ui.txt_status.setFrameShape(QtGui.QFrame.NoFrame)
        self.ui.txt_status.setEnabled(False)
        self.ui.txt_status.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.txt_status.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.txt_status.setStyleSheet('color: #0060b4; font: bold 17px; background-color:transparent; selection-background-color: transparent; selection-color: #0060b4')
        self.ui.txt_status.setGeometry(config.layout_x + 30, config.title_y, config.layout_width - 60, 580)
        self.ui.ConfigNetworkDiagnosisForm_ctr_message_box = component.messageBox('ConfigNetworkDiagnosisForm', self)
        self.ui.ConfigNetworkDiagnosisForm_ctr_message_box.setGeometry((768 - config.messageBox_width) / 2, 410, config.messageBox_width, config.messageBox_height)

    
    def showEvent(self, event):
        self.ui.reset()

    
    def hideEvent(self, event):
        self.ui.ConfigNetworkDiagnosisForm_ctr_message_box.close()
        self.hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainf = ConfigNetworkDiagnosisForm()
    mainf.show()
    mainf.ui.txt_status.setText('ksjalkfj\nLKAjalkfj\nLKAJSIOEF\nkjaslkjdfkFASDF\nlaksldfelf.uijalkfj\nLKAJSIOEF\nkjaslkjdfkFASDF\nlaksldfelf.uijalkfj\nLKAJSIOEF\nkjaslkjdfkFASDF\nlaksldfelf.uijalkfj\nLKAJSIOEF\nkjaslkjdfkFASDF\nlaksldfelf.uijalkfj\nLKAJSIOEF\nkjaslkjdfkFASDF\nlaksldfelf.uijalkfj\nLKAJSIOEF\nkjaslkjdfkFASDF\nlaksldfelf.uijalkfj\nLKAJSIOEF\nkjaslkjdfkFASDF\nlaksldfelf.uijalkfj\nLKAJSIOEF\nkjaslkjdfkFASDF\nlaksldfelf.uijalkfj\nLKAJSIOEF\nkjaslkjdfkFASDF\nlaksldfelf.uijalkfj\nLKAJSIOEF\nkjaslkjdfkFASDF\nlaksldfelf.uijalkfj\nLKAJSIOEF\nkjaslkjdfkFASDF\nlaksldfelf.uiJSIOEF\nkjaslkjdfkFASDF\nlaksldfelf.ui.gridlayout.addWidget (self.ui.btn_test_mode_off, 0, 0) elf.ui.gridlayout.addWidget (self.ui.btn_test_mode_off, 0, 0) elf.ui.gridlayout.addWidget (self.ui.btn_test_mode_off, 0, 0) elf.ui.gridlayout.addWidget (self.ui.btn_test_mode_off, 0, 0) elf.ui.gridlayout.addWidget (self.ui.btn_test_mode_off, 0, 0)')
    mainf.ui.ConfigNetworkDiagnosisForm_ctr_message_box.show({
        'message': 'Adjust btn_hdmi_off btn_hdmi_off!',
        'type': 'alert' })
    sys.exit(app.exec_())

