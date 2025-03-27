# Source Generated with Decompyle++
# File: configTestModeForm.pyc (Python 2.5)

'''
ConfigTestModeForm 
2009-07-26 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
import config
import component

class ConfigTestModeForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = component.ConfigForm('ConfigTestModeForm', self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_config)))
        self.setPalette(palette)
        self.ui.txt_status = QtGui.QLabel(self)
        self.ui.txt_status.setStyleSheet('color: #0060b4; font: bold 26px;')
        self.ui.txt_status.setGeometry(config.layout_x, config.title_y, config.layout_width, 50)
        self.ui.txt_message = QtGui.QLabel(self)
        self.ui.txt_message.setStyleSheet('color: #bb0000; font: bold 22px;')
        self.ui.txt_message.setGeometry(config.layout_x, self.ui.txt_status.y() + 50, config.layout_width, 50)
        self.ui.ConfigTestModeForm_ctr_num_keyboard = component.numKeyboard('ConfigTestModeForm', self)
        self.ui.ConfigTestModeForm_ctr_num_keyboard.setGeometry((768 - config.bg_kb_width) / 2, self.ui.txt_message.y() + 60, config.bg_kb_width, config.bg_kb_height)
        self.ui.ConfigTestModeForm_ctr_message_box = component.messageBox('ConfigTestModeForm', self)

    
    def showEvent(self, event):
        self.ui.reset()

    
    def hideEvent(self, event):
        self.ui.ConfigTestModeForm_ctr_num_keyboard.hide()
        self.ui.ConfigTestModeForm_ctr_message_box.hide()
        self.hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainf = ConfigTestModeForm()
    mainf.show()
    sys.exit(app.exec_())

