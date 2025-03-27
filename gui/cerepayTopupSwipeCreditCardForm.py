# Source Generated with Decompyle++
# File: cerepayTopupSwipeCreditCardForm.pyc (Python 2.5)

import os
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
import component
import config
from component import btnCancel, SWF_swipe_card, messageBox, btnCenter
_Form_Name_String = 'CerepayTopupSwipeCreditCardForm'

class CerepayTopupSwipeCreditCardForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = QtCore.QObject()
        self.setGeometry(0, 0, 768, 1024)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_movie)))
        self.setPalette(palette)
        self.ui.btn_cancel = component.btnCancel(self, _Form_Name_String)
        self.ui.btn_cancel.setGeometry(280, 930, 160, 68)
        self.ui.ctr_btn_center = component.btnCenter(self, _Form_Name_String)
        self.ui.btn_back = component.btnBack(self, _Form_Name_String)
        self.ui.btn_back.setGeometry(580, 20, 160, 68)
        self.ui.swf_swipe_card = component.SWF_sweepcard(self)
        self.ui.swf_swipe_card.setGeometry(150, 350, 471, 441)
        self.ui.swf_swipe_card.show()
        self.ui.txtbox_msg = QtGui.QLabel(self)
        self.ui.txtbox_msg.setGeometry(QtCore.QRect(90, 160, 571, 71))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.ui.txtbox_msg.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(22)
        font.setWeight(75)
        font.setBold(True)
        self.ui.txtbox_msg.setFont(font)
        self.ui.txtbox_msg.setScaledContents(False)
        self.ui.txtbox_msg.setWordWrap(True)
        self.ui.txtbox_msg.setObjectName('txtbox_msg')
        self.ui.CerepayTopupSwipeCreditCardForm_ctr_message_box = messageBox(_Form_Name_String, self)
        self.ui.CerepayTopupSwipeCreditCardForm_ctr_message_box.hide()

    
    def showEvent(self, event):
        self.ui.ctr_btn_center.init()
        self.ui.btn_back.reset()
        self.ui.btn_cancel.reset()
        self.ui.txtbox_msg.setText(QtGui.QApplication.translate('Form', 'Please swipe your credit card to top up.', None, QtGui.QApplication.UnicodeUTF8))

    
    def hideEvent(self, event):
        self.ui.CerepayTopupSwipeCreditCardForm_ctr_message_box.hide()
        self.hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = CerepayTopupSwipeCreditCardForm()
    mainf.show()
    sys.exit(app.exec_())

