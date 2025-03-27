# Source Generated with Decompyle++
# File: pickupResultForm.pyc (Python 2.5)

'''
PickUpResultForm is the main window. 
2009-07-16 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
from pickupResultForm_ui import Ui_pickupResultForm
import config
from component import btnFinish, ctrButton, btnCenter

class PickUpResultForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_pickupResultForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        if not os.path.isfile(config.pic_bg_pickup):
            print('CAN NOT FIND THE PIC: %s' % config.pic_bg_start)
        
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_pickup)))
        self.setPalette(palette)
        self.ui.btn_finish = btnFinish(self, 'PickUpResultForm')
        self.ui.btn_finish.setGeometry(580, 920, 160, 68)
        self.ui.btn_continue_shopping = ctrButton(self, 'PickUpResultForm', 'btn_continue_shopping', QtGui.QApplication.translate('Form', 'Continue\nShopping', None, QtGui.QApplication.UnicodeUTF8), config.btn_width, config.btn_height, config.btn02Style_little)
        self.ui.btn_logout = ctrButton(self, 'PickUpResultForm', 'btn_logout', QtGui.QApplication.translate('Form', 'Finish and\nLogout', None, QtGui.QApplication.UnicodeUTF8), config.btn_width, config.btn_height, config.btn02Style_little_red)
        self.ui.hboxlayout.addWidget(self.ui.btn_continue_shopping)
        self.ui.hboxlayout.addWidget(self.ui.btn_logout)
        self.ui.btn_continue_shopping.hide()
        self.ui.btn_logout.hide()
        self.ui.ctr_btn_center = btnCenter(self, 'PickUpResultForm')
        self.ui.ctr_btn_center.hide()

    
    def showEvent(self, event):
        self.ui.ctr_btn_center.init()
        self.ui.retranslateUi('')
        self.ui.btn_finish.reset()
        self.ui.btn_continue_shopping.setText(QtGui.QApplication.translate('Form', 'Continue\nShopping', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_logout.setText(QtGui.QApplication.translate('Form', 'Finish and\nLogout', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = PickUpResultForm()
    mainf.show()
    mainf.ui.txtbox_msg.setText('Please\nasjlkfj\nLKKfkasjf\nggggA')
    sys.exit(app.exec_())

