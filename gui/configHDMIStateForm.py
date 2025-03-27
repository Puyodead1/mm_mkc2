# Source Generated with Decompyle++
# File: configHDMIStateForm.pyc (Python 2.5)

'''
ConfigHDMIStateForm 
2009-07-26 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
import config
import component

class ConfigHDMIStateForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = component.ConfigForm('ConfigHDMIStateForm', self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_config)))
        self.setPalette(palette)
        self.ui.txt_status = QtGui.QLabel(self)
        self.ui.txt_status.setStyleSheet('color: #0060b4; font: bold 26px;')
        self.ui.txt_status.setGeometry(config.layout_x, config.title_y, config.layout_width, 50)
        self.ui.ConfigHDMIStateForm_ctr_message_box = component.messageBox('ConfigHDMIStateForm', self)
        self.ui.ConfigHDMIStateForm_ctr_message_box.setGeometry((768 - config.messageBox_width) / 2, 410, config.messageBox_width, config.messageBox_height)
        self.ui.ConfigHDMIStateForm_ctr_message_box.hide()

    
    def hideEvent(self, event):
        self.ui.ConfigHDMIStateForm_ctr_message_box.hide()
        self.hide()

    
    def showEvent(self, event):
        self.ui.reset()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainf = ConfigHDMIStateForm()
    mainf.show()
    mainf.ui.ConfigHDMIStateForm_ctr_message_box.show({
        'message': 'Adjust btn_hdmi_off btn_hdmi_off!',
        'type': 'alert' })
    sys.exit(app.exec_())

