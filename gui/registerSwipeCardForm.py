# Source Generated with Decompyle++
# File: registerSwipeCardForm.pyc (Python 2.5)

import sys
import config
from component import btnCancel, btnBack, ctrButton, SWF_sweepcard, messageBox
from PyQt4 import QtCore, QtGui
from registerSwipeCardForm_ui import Ui_registerCrerepayCardForm

class RegisterSwipeCardForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_registerCrerepayCardForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_load)))
        self.setPalette(palette)
        self.ui.btn_back = btnBack(self, 'RegisterSwipeCardForm')
        self.ui.swf_swipe_card = SWF_sweepcard(self)
        self.ui.swf_swipe_card.setGeometry(150, 380, 471, 441)
        self.ui.RegisterSwipeCardForm_ctr_message_box = messageBox('RegisterSwipeCardForm', self)
        self.ui.btn_cancel = btnCancel(self, 'RegisterSwipeCardForm')
        self.ui.btn_cancel.setGeometry(580, 20, 160, 68)
        self.ui.hboxlayout.addWidget(self.ui.btn_back, 1, QtCore.Qt.AlignCenter)

    
    def showEvent(self, event):
        self.ui.btn_back.reset()
        self.ui.btn_cancel.reset()
        self.ui.txt_card_label.setText(QtGui.QApplication.translate('Form', 'Membership Card Registration', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    import os
    form = RegisterSwipeCardForm()
    form.show()
    sys.exit(app.exec_())

