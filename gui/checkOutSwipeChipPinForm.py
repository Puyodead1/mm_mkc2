# Source Generated with Decompyle++
# File: checkOutSwipeChipPinForm.pyc (Python 2.5)

'''
CheckOutSwipeChipPinForm for movie price detail
2009-07-06 created by Mavis
'''
import sys
import config
from component import btnCancel, SWF_swipe_card, messageBox, btnCenter
from PyQt4 import QtCore, QtGui
from shopping_cart_ui import Ui_shoppingCartForm

class CheckOutSwipeChipPinForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_shoppingCartForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        self.palette = QtGui.QPalette()
        self.palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_movie)))
        self.setPalette(self.palette)
        self.ui.ctr_btn_center = btnCenter(self, 'CheckOutSwipeChipPinForm')
        self.ui.ctr_btn_center.hide()
        self.ui.txt_cart_label.setText('Swipe Card')
        self.ui.txt_cart_info_label.resize(self.ui.txt_cart_info_label.width(), self.ui.txt_cart_info_label.height() + 60)
        self.ui.swf_swipe_card = SWF_swipe_card(self)
        self.ui.swf_swipe_card.setGeometry((768 - 585) / 2, 20 + self.ui.txt_cart_info_label.y() + self.ui.txt_cart_info_label.height(), 585, 520)
        self.ui.swf_swipe_card.hide()
        self.ui.CheckOutSwipeChipPinForm_ctr_message_box = messageBox('CheckOutSwipeChipPinForm', self)
        self.ui.CheckOutSwipeChipPinForm_ctr_message_box.hide()

    
    def showEvent(self, event):
        self.ui.ctr_btn_center.init()
        self.ui.txt_cart_label.setText(QtGui.QApplication.translate('Form', 'Swipe Card', None, QtGui.QApplication.UnicodeUTF8))

    
    def hideEvent(self, event):
        self.ui.CheckOutSwipeChipPinForm_ctr_message_box.hide()
        self.hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = CheckOutSwipeChipPinForm()
    form.show()
    form.ui.swf_swipe_card.show()
    form.ui.txt_cart_info_label.setText('Please swipe your debit card.\n Please swipe your debit card\n Please swipe your debit card.')
    sys.exit(app.exec_())

