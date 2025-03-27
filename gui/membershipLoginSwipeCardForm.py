# Source Generated with Decompyle++
# File: membershipLoginSwipeCardForm.pyc (Python 2.5)

'''
MembershipLoginSwipeCardForm for membership login
2010-06-25 created by Mavis
'''
import sys
import config
from component import messageBox, btnCancel, btnBack, ctrButton, SWF_sweepcard, allKeyboard
from PyQt4 import QtCore, QtGui
from swipecard_ui import Ui_checkoutSwipeCardForm

class MembershipLoginSwipeCardForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_checkoutSwipeCardForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_load)))
        self.setPalette(palette)
        self.ui.swf_credit_cars.setPixmap(QtGui.QPixmap(config.pic_creditcard))
        self.ui.swf_swipe_card = SWF_sweepcard(self)
        self.ui.swf_swipe_card.setGeometry(150, 380, 471, 441)
        self.ui.swf_swipe_card.hide()
        for i in range(1, 5):
            exec('self.ui.txt_flag' + str(i) + '.hide()')
        
        self.ui.btn_back = btnBack(self, 'MembershipLoginSwipeCardForm')
        self.ui.btn_cancel = btnCancel(self, 'MembershipLoginSwipeCardForm')
        self.ui.btn_cancel.setGeometry(580, 20, 160, 68)
        self.ui.btn_email = ctrButton(self, 'MembershipLoginSwipeCardForm', 'btn_email', QtGui.QApplication.translate('Form', 'Login By Email', None, QtGui.QApplication.UnicodeUTF8), config.btn_width, config.btn_height, config.btn02Style_little)
        self.ui.hboxlayout.addWidget(self.ui.btn_back)
        self.ui.hboxlayout.addWidget(self.ui.btn_email)
        self.ui.MembershipLoginSwipeCardForm_ctr_message_box = messageBox('MembershipLoginSwipeCardForm', self)
        self.ui.MembershipLoginSwipeCardForm_ctr_message_box.hide()

    
    def hideEvent(self, event):
        self.ui.MembershipLoginSwipeCardForm_ctr_message_box.hide()
        self.ui.swf_swipe_card.hide()
        self.hide()

    
    def showEvent(self, event):
        self.ui.txt_card_label.setText(QtGui.QApplication.translate('Form', 'Membership Login', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_cancel.reset()
        self.ui.btn_back.reset()
        self.ui.btn_email.setText(QtGui.QApplication.translate('Form', 'Login By Email', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    import os
    config.transFile = 'trans_en.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    form = MembershipLoginSwipeCardForm()
    form.show()
    form.ui.swf_swipe_card.show()
    sys.exit(app.exec_())

