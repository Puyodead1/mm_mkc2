# Source Generated with Decompyle++
# File: checkoutSwipeCardForm.pyc (Python 2.5)

'''
CheckOutSwipeCardForm for checkout
2009-07-14 created by Mavis
'''
import sys
import config
from component import messageBox, btnCancel, SWF_sweepcard, allKeyboard, btnCenter, ctrButton, numKeyboard, btnBack
from PyQt4 import QtCore, QtGui
from swipecard_ui import Ui_checkoutSwipeCardForm
from squery import socketQuery

class CheckOutSwipeCardForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        btn_width = 350
        btn_height = 65
        self.ui = Ui_checkoutSwipeCardForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_movie)))
        self.setPalette(palette)
        self.ui.swf_credit_cars.setPixmap(QtGui.QPixmap(config.pic_creditcard))
        self.ui.swf_swipe_card = SWF_sweepcard(self)
        self.ui.swf_swipe_card.setGeometry(150, 380, 471, 441)
        self.ui.swf_swipe_card.hide()
        self.ui.CheckOutSwipeCardForm_ctr_message_box = messageBox('CheckOutSwipeCardForm', self)
        self.ui.CheckOutSwipeCardForm_ctr_all_keyboard = allKeyboard('CheckOutSwipeCardForm', self)
        self.ui.CheckOutSwipeCardForm_ctr_all_keyboard.hide()
        self.ui.CheckOutSwipeCardForm_ctr_num_keyboard = numKeyboard('CheckOutSwipeCardForm', self)
        self.ui.CheckOutSwipeCardForm_ctr_num_keyboard.hide()
        for i in range(1, 5):
            exec('self.ui.txt_flag' + str(i) + '.hide()')
        
        self.sq = socketQuery()
        self.ui.ctr_btn_center = btnCenter(self, 'CheckOutSwipeCardForm')
        self.ui.ctr_btn_center.hide()
        self.ui.btn_cancel = btnCancel(self, 'CheckOutSwipeCardForm')
        self.ui.btn_cancel.setGeometry(580, 20, 160, 68)
        self.ui.btn_back = btnBack(self, 'CheckOutSwipeCardForm')
        self.ui.hboxlayout.addWidget(self.ui.btn_back, 0, QtCore.Qt.AlignRight)

    
    def btn_cancel_click(self):
        data = { }
        data['wid'] = 'CheckOutSwipeCardForm'
        data['cid'] = 'btn_cancel'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        self.sq.send(data)

    
    def hideEvent(self, event):
        self.ui.CheckOutSwipeCardForm_ctr_message_box.hide()
        self.ui.CheckOutSwipeCardForm_ctr_all_keyboard.hide()
        self.ui.swf_swipe_card.hide()
        self.hide()

    
    def showEvent(self, event):
        self.ui.ctr_btn_center.init()
        self.ui.btn_cancel.reset()
        self.ui.btn_back.reset()
        self.ui.retranslateUi('')


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    import os
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    form = CheckOutSwipeCardForm()
    form.show()
    form.ui.txt_flag1.show()
    form.ui.txt_flag2.show()
    form.ui.txt_flag3.show()
    form.ui.txt_flag4.show()
    sys.exit(app.exec_())

