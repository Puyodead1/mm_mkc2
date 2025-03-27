# Source Generated with Decompyle++
# File: checkOutSwipeProsaForm.pyc (Python 2.5)

'''
CheckOutSwipeProsaForm for movie price detail
2012-02-25 created by Helo
'''
import sys
import config
from component import btnCancel, SWF_swipecard_member, messageBox, btnCenter, SWF_insert_card, ctrButton, numKeyboard, btnBack
from PyQt4 import QtCore, QtGui
from shopping_cart_ui import Ui_shoppingCartForm

class CheckOutSwipeProsaForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_shoppingCartForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        self.palette = QtGui.QPalette()
        self.palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_movie)))
        self.setPalette(self.palette)
        self.ui.ctr_btn_center = btnCenter(self, 'CheckOutSwipeProsaForm')
        self.ui.ctr_btn_center.hide()
        self.ui.btn_back = btnBack(self, 'CheckOutSwipeProsaForm')
        self.ui.hboxlayout.addWidget(self.ui.btn_back, QtCore.Qt.AlignRight)
        self.ui.txt_cart_label.setText('Swipe Card')
        self.ui.txt_cart_info_label.resize(self.ui.txt_cart_info_label.width(), self.ui.txt_cart_info_label.height() + 60)
        self.ui.btn_member_card = ctrButton(self, 'CheckOutSwipeProsaForm', 'btn_member_card', 'Membership Card', config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.ui.btn_credit_card = ctrButton(self, 'CheckOutSwipeProsaForm', 'btn_credit_card', 'Credit Card', config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.ui.btn_member_card.setGeometry(120, self.ui.txt_cart_info_label.y() + self.ui.txt_cart_info_label.height() + 50, config.btnWidth, config.btnHeight)
        self.ui.btn_credit_card.setGeometry(768 - 120 - config.btnWidth, self.ui.txt_cart_info_label.y() + self.ui.txt_cart_info_label.height() + 50, config.btnWidth, config.btnHeight)
        self.ui.pic_card_member = QtGui.QLabel(self)
        self.ui.pic_card_member.setPixmap(QtGui.QPixmap(config.pic_card_member))
        self.ui.pic_card_member.setGeometry(120, self.ui.btn_member_card.y() + config.btnHeight + 10, 200, 130)
        self.ui.pic_card_member.hide()
        self.ui.pic_card_credit = QtGui.QLabel(self)
        self.ui.pic_card_credit.setPixmap(QtGui.QPixmap(config.pic_card_credit))
        self.ui.pic_card_credit.setGeometry(768 - 120 - config.btnWidth, self.ui.btn_credit_card.y() + config.btnHeight + 10, 200, 130)
        self.ui.pic_card_credit.hide()
        self.ui.swf_credit_cars = QtGui.QLabel(self)
        self.ui.swf_credit_cars.setPixmap(QtGui.QPixmap(config.pic_creditcard))
        self.ui.swf_credit_cars.setGeometry(QtCore.QRect(103, 260, 541, 101))
        self.ui.swf_credit_cars.hide()
        self.ui.swf_swipe_card = SWF_swipecard_member(self)
        self.ui.swf_swipe_card.setGeometry((768 - 585) / 2, 20 + self.ui.swf_credit_cars.y() + self.ui.swf_credit_cars.height(), 585, 520)
        self.ui.swf_swipe_card.hide()
        self.ui.swf_insert_card = SWF_insert_card(self)
        self.ui.swf_insert_card.setGeometry((768 - 585) / 2, 10 + self.ui.swf_credit_cars.y() + self.ui.swf_credit_cars.height(), 585, 520)
        self.ui.swf_insert_card.hide()
        self.ui.CheckOutSwipeProsaForm_ctr_message_box = messageBox('CheckOutSwipeProsaForm', self)
        self.ui.CheckOutSwipeProsaForm_ctr_message_box.hide()
        self.ui.CheckOutSwipeProsaForm_ctr_num_keyboard = numKeyboard('CheckOutSwipeProsaForm', self)
        self.ui.CheckOutSwipeProsaForm_ctr_num_keyboard.hide()

    
    def showEvent(self, event):
        self.ui.ctr_btn_center.init()
        self.ui.txt_cart_label.setText(QtGui.QApplication.translate('Form', 'Swipe Card', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_member_card.setText(QtGui.QApplication.translate('Form', 'Membership Card', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_credit_card.setText(QtGui.QApplication.translate('Form', 'Credit Card', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_back.reset()

    
    def hideEvent(self, event):
        self.ui.CheckOutSwipeProsaForm_ctr_message_box.hide()
        self.hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = CheckOutSwipeProsaForm()
    form.show()
    form.ui.swf_swipe_card.show()
    form.ui.txt_cart_info_label.setText('Please swipe your debit card.\n Please swipe your debit card\n Please swipe your debit card.')
    sys.exit(app.exec_())

