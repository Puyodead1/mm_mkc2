# Source Generated with Decompyle++
# File: registerMainForm.pyc (Python 2.5)

import sys
import config
from component import btnBack, ctrButton, allKeyboard, messageBox, btnCancel
from PyQt4 import QtCore, QtGui
from registerMainForm_ui import Ui_registerMainForm

class RegisterMainForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_registerMainForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_load)))
        self.setPalette(palette)
        self.ui.RegisterMainForm_ctr_all_keyboard = allKeyboard('RegisterMainForm', self)
        self.ui.RegisterMainForm_ctr_all_keyboard.setGeometry((768 - config.kb_all_width) / 2, (1024 - config.kb_all_height) / 2, config.kb_all_width, config.kb_all_height)
        self.ui.RegisterMainForm_ctr_all_keyboard.hide()
        self.ui.btn_cancel = btnCancel(self, 'RegisterMainForm')
        self.ui.hboxlayout.addWidget(self.ui.btn_cancel, 1, QtCore.Qt.AlignCenter)
        self.ui.RegisterMainForm_ctr_message_box = messageBox('RegisterMainForm', self)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = RegisterMainForm()
    form.show()
    sys.exit(app.exec_())

