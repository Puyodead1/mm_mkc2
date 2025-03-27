# Source Generated with Decompyle++
# File: fatalErrorForm.pyc (Python 2.5)

'''
FatalErrorForm 
2009-07-26 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
from configForm_ui import Ui_configForm
import config
import component
from squery import socketQuery

class FatalErrorForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_configForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_fatal)))
        self.setPalette(palette)
        self.sq = socketQuery()
        '\n        self.ui.txt_config_label.setText(QtGui.QApplication.translate("Form", "Maintenance", None, QtGui.QApplication.UnicodeUTF8))\n        self.ui.txt_config_label.setStyleSheet("color: #bb0000; font: bold 56px; text-align:center")\n        self.ui.txt_config_label.setGeometry(config.layout_x+10, config.layout_y+10, config.layout_width, 64)\n\n        self.ui.txt_config_label.setText(QtGui.QApplication.translate("Form", "Mode", None, QtGui.QApplication.UnicodeUTF8))\n        self.ui.txt_config_label.setStyleSheet("color: #bb0000; font: bold 56px; text-align:center")\n        self.ui.txt_config_label.setGeometry(config.layout_x+10, config.layout_y+10+64, config.layout_width, 64)\n        '
        self.ui.txtbox_msg = QtGui.QLabel(self)
        self.ui.txtbox_msg.setStyleSheet('font: bold 26px; vertical-align:text-top;')
        self.ui.txtbox_msg.setGeometry(config.layout_x + 10, config.layout_y + 200, config.layout_width, 500)
        self.ui.txtbox_msg.setWordWrap(True)
        self.ui.txtbox_msg.setAlignment(QtCore.Qt.AlignTop)
        self.ui.txtbox_tech_support = QtGui.QLabel(self)
        self.ui.txtbox_tech_support.setStyleSheet('color: #bb0000; font: bold 26px;')
        self.ui.txtbox_tech_support.setGeometry(40, (1024 - config.kb_all_height) / 2 + config.kb_all_height, 640, 50)
        self.ui.btn_icon_keyboard = QtGui.QPushButton(self)
        self.ui.btn_icon_keyboard.setGeometry(config.layout_x, 920, 130, 75)
        self.ui.btn_icon_keyboard.setStyleSheet('background-color: transparent; border: 0px')
        self.ui.btn_icon_keyboard.setIcon(QtGui.QIcon(config.pic_icon_keyboard))
        self.ui.btn_icon_keyboard.setIconSize(QtCore.QSize(127, 66))
        self.ui.FatalErrorForm_ctr_all_keyboard = component.allKeyboard('FatalErrorForm', self)
        self.ui.FatalErrorForm_ctr_all_keyboard.hide()
        QtCore.QObject.connect(self.ui.btn_icon_keyboard, QtCore.SIGNAL('clicked()'), self.btn_icon_keyboard_click)
        QtCore.QObject.connect(self.ui.btn_icon_keyboard, QtCore.SIGNAL('pressed()'), self.btn_icon_press)

    
    def showEvent(self, event):
        self.ui.txt_config_label.setText(QtGui.QApplication.translate('Form', ' ', None, QtGui.QApplication.UnicodeUTF8))

    
    def hideEvent(self, event):
        self.ui.FatalErrorForm_ctr_all_keyboard.hide()
        self.hide()

    
    def btn_icon_press(self):
        self.ui.btn_icon_keyboard.setIconSize(QtCore.QSize(120, 60))

    
    def btn_icon_keyboard_click(self):
        data = { }
        data['wid'] = 'FatalErrorForm'
        data['cid'] = 'btn_icon_keyboard'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        self.sq.send(data)
        self.ui.btn_icon_keyboard.setIconSize(QtCore.QSize(127, 66))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainf = FatalErrorForm()
    mainf.show()
    mainf.ui.txtbox_tech_support.setText('farrin@themoviemachine.net')
    sys.exit(app.exec_())

