# Source Generated with Decompyle++
# File: configPowerOffForm.pyc (Python 2.5)

'''
ConfigPowerOffForm 
2010-07-14 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
import config
import component

class ConfigPowerOffForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = component.ConfigForm('ConfigPowerOffForm', self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_config)))
        self.setPalette(palette)
        self.ui.txt_status = QtGui.QLabel(self)
        self.ui.txt_status.setStyleSheet('color: #0060b4; font: bold 26px;')
        self.ui.txt_status.setGeometry(config.layout_x, config.title_y, config.layout_width, 50)
        self.ui.ConfigPowerOffForm_ctr_message_box = component.messageBox('ConfigPowerOffForm', self)
        self.ui.ConfigPowerOffForm_ctr_message_box.setGeometry((768 - config.messageBox_width) / 2, 410, config.messageBox_width, config.messageBox_height)
        self.ui.ConfigPowerOffForm_ctr_message_box.hide()

    
    def hideEvent(self, event):
        self.ui.ConfigPowerOffForm_ctr_message_box.hide()

    
    def showEvent(self, event):
        self.ui.reset()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainf = ConfigPowerOffForm()
    mainf.show()
    sys.exit(app.exec_())

