# Source Generated with Decompyle++
# File: pickupCodeForm.pyc (Python 2.5)

'''
PickUpCodeForm. 
2009-07-16 created by Mavis
'''
import sys
from PyQt4 import QtGui
from pickupDiscListForm_ui import Ui_pickupDiskInfoForm
import component
import config

class PickUpCodeForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_pickupDiskInfoForm()
        self.ui.setupUi(self)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_pickup)))
        self.setPalette(palette)
        self.ui.btn_swipe_card = component.ctrButton(self, 'PickUpCodeForm', 'btn_swipe_card', 'Swipe Card', config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.ui.btn_pin_code = component.ctrButton(self, 'PickUpCodeForm', 'btn_pin_code', 'Pickup Code', config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.ui.btn_swipe_card.setGeometry(120, self.ui.txtbox_msg.y() + self.ui.txtbox_msg.height() + 50, config.btnWidth, config.btnHeight)
        self.ui.btn_pin_code.setGeometry(768 - 120 - config.btnWidth, self.ui.txtbox_msg.y() + self.ui.txtbox_msg.height() + 50, config.btnWidth, config.btnHeight)
        self.ui.btn_back = component.btnBack(self, 'PickUpCodeForm')
        self.ui.btn_cancel = component.btnCancel(self, 'PickUpCodeForm')
        self.ui.btn_cancel.setGeometry(580, 20, 160, 68)
        self.ui.hboxlayout.addWidget(self.ui.btn_back)
        self.ui.PickUpCodeForm_ctr_num_keyboard = component.numKeyboard('PickUpCodeForm', self)
        self.ui.PickUpCodeForm_ctr_num_keyboard.hide()
        self.ui.PickUpCodeForm_ctr_message_box = component.messageBox('PickUpCodeForm', self)

    
    def showEvent(self, event):
        self.ui.retranslateUi('')
        self.ui.btn_swipe_card.setText(QtGui.QApplication.translate('Form', 'Swipe Card', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_pin_code.setText(QtGui.QApplication.translate('Form', 'Pickup Code', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_back.reset()
        self.ui.btn_cancel.reset()

    
    def hideEvent(self, event):
        self.ui.PickUpCodeForm_ctr_num_keyboard.hide()
        self.ui.PickUpCodeForm_ctr_message_box.hide()
        self.hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    import os
    from PyQt4 import QtCore
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = PickUpCodeForm()
    mainf.show()
    sys.exit(app.exec_())

