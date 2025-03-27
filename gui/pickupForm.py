# Source Generated with Decompyle++
# File: pickupForm.pyc (Python 2.5)

'''
PickUpSwipeCardForm is the first window in pick up. 
2009-07-16 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
from pickup_ui import Ui_pickupForm
import component
import config
from squery import socketQuery

class PickUpSwipeCardForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_pickupForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        if not os.path.isfile(config.pic_bg_pickup):
            print('CAN NOT FIND THE PIC: %s' % config.pic_bg_start)
        
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_pickup)))
        self.setPalette(palette)
        self.ui.swf_credit_cars.setPixmap(QtGui.QPixmap(config.pic_creditcard))
        self.ui.swf_swipe_card = component.SWF_sweepcard(self)
        self.ui.swf_swipe_card.setGeometry(self.ui.swf_credit_cars.x() + 30, self.ui.swf_credit_cars.y() + self.ui.swf_credit_cars.height() + 20, 400, 441)
        self.ui.swf_swipe_card.hide()
        self.ui.PickUpSwipeCardForm_ctr_message_box = component.messageBox('PickUpSwipeCardForm', self)
        self.ui.btn_back = component.btnBack(self, 'PickUpSwipeCardForm')
        self.ui.btn_cancel = component.btnCancel(self, 'PickUpSwipeCardForm')
        self.ui.btn_cancel.setGeometry(580, 20, 160, 68)
        self.ui.hboxlayout.addWidget(self.ui.btn_back)

    
    def showEvent(self, event):
        self.ui.retranslateUi('')
        self.ui.btn_back.reset()
        self.ui.btn_cancel.reset()

    
    def hideEvent(self, event):
        self.ui.PickUpSwipeCardForm_ctr_message_box.hide()
        self.hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = PickUpSwipeCardForm()
    mainf.show()
    sys.exit(app.exec_())

