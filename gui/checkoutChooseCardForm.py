# Source Generated with Decompyle++
# File: checkoutChooseCardForm.pyc (Python 2.5)

'''
CheckOutChooseCardForm for movie price detail
2009-07-06 created by Mavis
'''
import sys
import config
import component
from PyQt4 import QtCore, QtGui
from shopping_cart_ui import Ui_shoppingCartForm

class CheckOutChooseCardForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_shoppingCartForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        self.palette = QtGui.QPalette()
        self.palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_movie)))
        self.setPalette(self.palette)
        self.ui.txt_cart_label.setText('Choosing Card')
        self.ui.ctr_btn_center = component.btnCenter(self, 'CheckOutChooseCardForm')
        self.ui.ctr_btn_center.hide()
        self.ui.btn_back = component.btnBack(self, 'CheckOutChooseCardForm')
        self.ui.btn_back.setGeometry(580, 20, 160, 68)
        self.ui.btn_cancel = component.btnCancel(self, 'CheckOutChooseCardForm')
        self.ui.hboxlayout.addWidget(self.ui.btn_cancel)
        horizontalLayout = QtGui.QWidget(self)
        horizontalLayout.setGeometry(QtCore.QRect(40, self.ui.txt_cart_label.y() + self.ui.txt_cart_label.height() + 100, 691, 201))
        hboxlayout = QtGui.QHBoxLayout(horizontalLayout)
        self.ui.btn_credit_card = component.ctrButton(self, 'CheckOutChooseCardForm', 'btn_credit_card', 'Credit Card', config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.ui.btn_debit_card = component.ctrButton(self, 'CheckOutChooseCardForm', 'btn_debit_card', 'Debit Card', config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.ui.btn_save = component.ctrButton(self, 'CheckOutChooseCardForm', 'btn_save', 'Saving', config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.ui.btn_current_cheque = component.ctrButton(self, 'CheckOutChooseCardForm', 'btn_current_cheque', 'Current/Cheque', config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.ui.btn_save.hide()
        self.ui.btn_current_cheque.hide()
        hboxlayout.addWidget(self.ui.btn_credit_card)
        hboxlayout.addWidget(self.ui.btn_debit_card)
        hboxlayout.addWidget(self.ui.btn_save)
        hboxlayout.addWidget(self.ui.btn_current_cheque)

    
    def showEvent(self, e):
        self.ui.ctr_btn_center.init()
        self.ui.retranslateUi('')
        self.ui.txt_cart_label.setText(QtGui.QApplication.translate('Form', 'Choosing Card', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_credit_card.setText(QtGui.QApplication.translate('Form', 'Credit Card', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_debit_card.setText(QtGui.QApplication.translate('Form', 'Debit Card', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_save.setText(QtGui.QApplication.translate('Form', 'Saving', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_current_cheque.setText(QtGui.QApplication.translate('Form', 'Current/Cheque', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_back.reset()
        self.ui.btn_cancel.reset()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = CheckOutChooseCardForm()
    form.show()
    sys.exit(app.exec_())

