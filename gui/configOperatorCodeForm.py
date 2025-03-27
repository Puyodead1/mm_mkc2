# Source Generated with Decompyle++
# File: configOperatorCodeForm.pyc (Python 2.5)

'''
ConfigOperatorCodeForm 
2009-07-26 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
import config
from squery import socketQuery
import component

class ConfigOperatorCodeForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = component.ConfigForm('ConfigOperatorCodeForm', self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_config)))
        self.setPalette(palette)
        self.sq = socketQuery()
        self.ui.btn_finish = component.ctrButton(self, 'ConfigOperatorCodeForm', 'btn_finish', QtGui.QApplication.translate('configForm', 'Finish', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnRedStyle)
        self.ui.btn_retry = component.ctrButton(self, 'ConfigOperatorCodeForm', 'btn_retry', QtGui.QApplication.translate('configForm', 'Retry', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnRedStyle)
        self.ui.btn_finish.setGeometry((768 - config.btnWidth) / 2, 780, config.btnWidth, config.btnHeight)
        self.ui.btn_retry.setGeometry((768 - config.btnWidth) / 2, 780, config.btnWidth, config.btnHeight)
        self.ui.btn_retry.hide()
        self.ui.txt_title = QtGui.QLabel(QtGui.QApplication.translate('configForm', 'Operator Code', None, QtGui.QApplication.UnicodeUTF8), self)
        self.ui.txt_title.setStyleSheet('color: #0060b4; font: bold 26px;')
        self.ui.txt_title.setGeometry(config.layout_x, config.title_y, config.layout_width, 50)
        self.ui.txt_msg = QtGui.QLabel(QtGui.QApplication.translate('configForm', 'Please input the new password', None, QtGui.QApplication.UnicodeUTF8), self)
        self.ui.txt_msg.setStyleSheet('color: #bb0000; font: bold 22px;')
        self.ui.txt_msg.setGeometry(config.layout_x, config.title_y + 50 + config.pic_step_height, config.layout_width, 50)
        self.ui.swf_step1 = QtGui.QLabel(self)
        self.ui.swf_step1.setPixmap(QtGui.QPixmap(config.pic_step1))
        self.ui.swf_step1.setGeometry(config.layout_x, config.title_y + 50, config.pic_step_width, config.pic_step_height)
        self.ui.swf_step2 = QtGui.QLabel(self)
        self.ui.swf_step2.setPixmap(QtGui.QPixmap(config.pic_step2))
        self.ui.swf_step2.setGeometry(config.layout_x, config.title_y + 50, config.pic_step_width, config.pic_step_height)
        self.ui.swf_step3 = QtGui.QLabel(self)
        self.ui.swf_step3.setPixmap(QtGui.QPixmap(config.pic_step3))
        self.ui.swf_step3.setGeometry(config.layout_x, config.title_y + 50, config.pic_step_width, config.pic_step_height)
        self.ui.ConfigOperatorCodeForm_ctr_all_keyboard = component.allKeyboard('ConfigOperatorCodeForm', self, self.ui.txt_msg.y() + self.ui.txt_msg.height())
        self.ui.ConfigOperatorCodeForm_ctr_all_keyboard.hide()

    
    def showEvent(self, event):
        self.ui.reset()
        self.ui.btn_finish.setText(QtGui.QApplication.translate('configForm', 'Finish', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_retry.setText(QtGui.QApplication.translate('configForm', 'Retry', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.txt_title.setText(QtGui.QApplication.translate('configForm', 'Operator Code', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.txt_msg.setText(QtGui.QApplication.translate('configForm', 'Please input the new password', None, QtGui.QApplication.UnicodeUTF8))

    
    def hideEvent(self, event):
        self.ui.ConfigOperatorCodeForm_ctr_all_keyboard.hide()
        self.hide()

    
    def kb_ok_click(self):
        if not self.ui.ConfigOperatorCodeForm_ctr_all_keyboard.lineedit.text():
            return None
        
        data = { }
        data['wid'] = 'ConfigOperatorCodeForm'
        data['cid'] = 'ConfigOperatorCodeForm_ctr_all_keyboard'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info']['ConfigOperatorCodeForm_ctr_all_keyboard'] = { }
        data['param_info']['ConfigOperatorCodeForm_ctr_all_keyboard']['type'] = 'ok'
        data['param_info']['ConfigOperatorCodeForm_ctr_all_keyboard']['val'] = str(self.ui.ConfigOperatorCodeForm_ctr_all_keyboard.lineedit.text())
        self.sq.send(data)
        self.ui.ConfigOperatorCodeForm_ctr_all_keyboard.lineedit.clear()
        self.ui.ConfigOperatorCodeForm_ctr_all_keyboard.hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainf = ConfigOperatorCodeForm()
    mainf.show()
    mainf.ui.ConfigOperatorCodeForm_ctr_all_keyboard.show()
    sys.exit(app.exec_())

