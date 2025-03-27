# Source Generated with Decompyle++
# File: checkoutSwipeDebitCardForm.pyc (Python 2.5)

'''
CheckOutSwipeDebitCardForm for movie price detail
2009-07-06 created by Mavis
'''
import sys
import config
from component import btnCancel, messageBox, btnCenter
from PyQt4 import QtCore, QtGui
from shopping_cart_ui import Ui_shoppingCartForm

class CheckOutSwipeDebitCardForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_shoppingCartForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        self.palette = QtGui.QPalette()
        self.palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_movie)))
        self.setPalette(self.palette)
        self.ui.txt_cart_label.setText('Swipe Card')
        self.ui.txt_cart_info_label.resize(self.ui.txt_cart_info_label.width(), self.ui.txt_cart_info_label.height() + 60)
        self.ui.txt_cart_info_label.clear()
        self.ui.ctr_btn_center = btnCenter(self, 'CheckOutSwipeDebitCardForm')
        self.ui.ctr_btn_center.hide()
        self.ui.CheckOutSwipeDebitCardForm_ctr_message_box = messageBox('CheckOutSwipeDebitCardForm', self)
        self.ui.CheckOutSwipeDebitCardForm_ctr_message_box.hide()

    
    def showEvent(self, event):
        self.ui.ctr_btn_center.init()
        self.ui.txt_cart_label.setText(QtGui.QApplication.translate('Form', 'Swipe Card', None, QtGui.QApplication.UnicodeUTF8))

    
    def hideEvent(self, event):
        self.ui.CheckOutSwipeDebitCardForm_ctr_message_box.hide()
        self.hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = CheckOutSwipeDebitCardForm()
    form.show()
    sys.exit(app.exec_())

