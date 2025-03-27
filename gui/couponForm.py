# Source Generated with Decompyle++
# File: couponForm.pyc (Python 2.5)

'''
CouponForm for rent
2009-07-02 created by Mavis
'''
import sys
import os
import config
import component
from squery import socketQuery
from PyQt4 import QtCore, QtGui
from shopping_cart_ui import Ui_shoppingCartForm

class CouponForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_shoppingCartForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_movie)))
        self.setPalette(palette)
        self.ui.txt_cart_label.setText(QtGui.QApplication.translate('CouponForm', 'Shopping Cart', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.txt_cart_info_label.setText(QtGui.QApplication.translate('CouponForm', 'Shopping Cart Coupons', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_btn_center = component.btnCenter(self, 'CouponForm')
        self.ui.ctr_btn_center.hide()
        self.ui.btn_back = component.btnBack(self, 'CouponForm')
        self.ui.btn_cancel = component.btnCancel(self, 'CouponForm')
        self.ui.btn_cancel.setGeometry(580, 20, 160, 68)
        self.ui.btn_ok = component.ctrButton(self, 'CouponForm', 'btn_ok', QtGui.QApplication.translate('CouponForm', 'Ok', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.hboxlayout.addWidget(self.ui.btn_back)
        self.ui.hboxlayout.addWidget(self.ui.btn_ok)
        self.picHeight = 80
        self.picWidth = 50
        self.priceWidth = 240
        self.rowHeight = self.picHeight + 20
        self.column = 4
        self.dataType = 1047294
        self.sq = socketQuery()
        self.ui.ctr_coupon_info = component.couponList('CouponForm', self)
        self.ui.ctr_coupon_info.setGeometry(config.layout_x, config.unload_list_y, config.unload_list_width, config.unload_list_height)
        self.ui.coupon_test_mode_flag = QtGui.QLabel(QtGui.QApplication.translate('CouponForm', 'TEST MODE', None, QtGui.QApplication.UnicodeUTF8), self)
        self.ui.coupon_test_mode_flag.setGeometry(50, 750, 400, 140)
        self.ui.coupon_test_mode_flag.setStyleSheet('color: #C88080; font: bold 40px')
        self.ui.btn_add = component.ctrButton(self, 'CouponForm', 'btn_add', QtGui.QApplication.translate('CouponForm', '+Add', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.ui.btn_add.setGeometry(500, config.unload_list_y + config.unload_list_height + 10, config.btnWidth, config.btnHeight)
        self.ui.CouponForm_ctr_all_keyboard = component.allKeyboard('CouponForm', self)
        self.ui.CouponForm_ctr_all_keyboard.hide()
        self.ui.ctr_movie_info = component.MovieCouponSelectForm(self)
        self.ui.ctr_movie_info.setGeometry((768 - config.bg_kb_width) / 2, 400, config.bg_kb_width, config.bg_kb_height)
        self.ui.ctr_movie_info.hide()
        self.ui.CouponForm_ctr_message_box = component.messageBox('CouponForm', self)

    
    def hideEvent(self, event):
        self.ui.CouponForm_ctr_message_box.close()
        self.ui.ctr_movie_info.close()
        self.ui.CouponForm_ctr_all_keyboard.close()
        self.hide()

    
    def showEvent(self, event):
        self.ui.ctr_btn_center.init()
        self.ui.txt_cart_label.setText(QtGui.QApplication.translate('CouponForm', 'Shopping Cart', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.txt_cart_info_label.setText(QtGui.QApplication.translate('CouponForm', 'Shopping Cart Coupons', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_back.reset()
        self.ui.btn_cancel.reset()
        self.ui.btn_ok.setText(QtGui.QApplication.translate('CouponForm', 'Ok', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.coupon_test_mode_flag.setText(QtGui.QApplication.translate('CouponForm', 'TEST MODE', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_coupon_info.hlabel.setText(QtGui.QApplication.translate('Form', ' Coupon code       Description                   Apply to', None, QtGui.QApplication.UnicodeUTF8))

    
    def test(self):
        data = {
            'ctr_coupon_info': [
                {
                    'coupon_code': '55615632',
                    'description': 'First Night Free',
                    'coupon_disc_pic': '/home/mm/kiosk/var/gui/pic/110228.jpg',
                    'rfid': 'dszfdzshd',
                    'coupon_type': 'S' },
                {
                    'coupon_code': '999999',
                    'description': '1 Dollar Free',
                    'coupon_disc_pic': '',
                    'rfid': '',
                    'coupon_type': 'M' },
                {
                    'coupon_code': '111112',
                    'rfid': '008CFC9415000104E0',
                    'coupon_disc_pic': '/home/mm/kiosk/var/gui/pic/110255.jpg',
                    'description': 'First Night 50% Off\nLast Day Free\n7.8% Off',
                    'coupon_type': 'S' }] }
        self.ui.ctr_coupon_info.setCouponInfo(data)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_en.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    form = CouponForm()
    form.show()
    form.test()
    sys.exit(app.exec_())

