# Source Generated with Decompyle++
# File: shoppingCartForm.pyc (Python 2.5)

'''
ShoppingCartForm for movie price detail
2009-07-06 created by Mavis
'''
import sys
import os
import config
import component
from squery import socketQuery
from PyQt4 import QtCore, QtGui
from shopping_cart_ui import Ui_shoppingCartForm

class ShoppingCartForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_shoppingCartForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        self.palette = QtGui.QPalette()
        self.palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_movie)))
        self.setPalette(self.palette)
        self.picHeight = 80
        self.picWidth = 50
        self.priceWidth = 240
        self.rowHeight = self.picHeight + 20
        self.column = 4
        self.sq = socketQuery()
        self.ui.ctr_cart_info = component.MovieListAdmin(self, 3)
        self.ui.ctr_cart_info.setGeometry(config.layout_x, config.unload_list_y, config.unload_list_width, config.unload_list_height)
        self.ui.ctr_btn_center = component.btnCenter(self, 'ShoppingCartForm')
        self.ui.ctr_btn_center.hide()
        horizontalLayout = QtGui.QWidget(self)
        horizontalLayout.setStyleSheet('background-image: url(' + config.pic_cart_info_bg + ')')
        horizontalLayout.setGeometry(QtCore.QRect(self.ui.ctr_cart_info.x(), self.ui.ctr_cart_info.y() + self.ui.ctr_cart_info.height() - 2, self.ui.ctr_cart_info.width(), 80))
        hboxlayout = QtGui.QHBoxLayout(horizontalLayout)
        self.ui.btn_back = component.btnBack(self, 'ShoppingCartForm')
        self.ui.btn_back.setGeometry(580, 20, 160, 68)
        self.ui.btn_cancel = component.btnCancel(self, 'ShoppingCartForm')
        self.ui.btn_cancel.setGeometry(580, 20, 160, 68)
        self.couponLabel = QtGui.QLabel(self)
        self.couponLabel.setFixedSize(150, 74)
        self.couponLabel.setStyleSheet('background-image: url(' + config.pic_coupon + '); font: bold 20px')
        self.couponLabel.hide()
        self.ui.btn_coupon = component.ctrButton(self, 'ShoppingCartForm', 'btn_coupon', QtGui.QApplication.translate('Coupon', 'Coupon', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.ui.btn_clear_all_dvd = component.ctrButton(self, 'ShoppingCartForm', 'btn_clear_all_dvd', QtGui.QApplication.translate('Coupon', 'Clear Cart', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnRedStyle)
        hboxlayout.addWidget(self.couponLabel)
        hboxlayout.addWidget(self.ui.btn_coupon)
        hboxlayout.addWidget(self.ui.btn_clear_all_dvd)
        line = QtGui.QLabel(self)
        line.setPixmap(QtGui.QPixmap(config.pic_line_btm))
        line.setGeometry(config.layout_x, horizontalLayout.y() + horizontalLayout.height(), config.unload_list_width, 15)
        self.ui.infoLabel = QtGui.QLabel(self)
        self.ui.infoLabel.setPixmap(QtGui.QPixmap(config.pic_info))
        self.ui.infoLabel.setGeometry(line.x(), line.y() + line.height() + 10, 50, 50)
        self.ui.infoLabel.hide()
        self.ui.txtbox_msg = QtGui.QLabel(self)
        self.ui.txtbox_msg.setStyleSheet('color: red; font: bold 20px')
        self.ui.txtbox_msg.setWordWrap(True)
        self.ui.txtbox_msg.setGeometry(line.x() + 50, line.y() + line.height(), line.width() - 50, 80)
        self.ui.btn_add_another = component.ctrButton(self, 'ShoppingCartForm', 'btn_add_another', QtGui.QApplication.translate('Coupon', 'Add Other', None, QtGui.QApplication.UnicodeUTF8), config.btn_width, config.btn_height, config.btn02Style)
        self.ui.btn_checkout = component.ctrButton(self, 'ShoppingCartForm', 'btn_checkout', QtGui.QApplication.translate('Coupon', 'Check Out', None, QtGui.QApplication.UnicodeUTF8), config.btn_width, config.btn_height, config.btn02Style)
        self.ui.hboxlayout.addWidget(self.ui.btn_back)
        self.ui.hboxlayout.addWidget(self.ui.btn_add_another)
        self.ui.hboxlayout.addWidget(self.ui.btn_checkout)
        QtCore.QObject.connect(self.ui.ctr_cart_info.table, QtCore.SIGNAL('cellClicked(int, int)'), self.cancel_click)
        self.ui.ShoppingCartForm_ctr_message_box = component.messageBox('ShoppingCartForm', self)

    
    def showEvent(self, event):
        self.ui.ctr_btn_center.init()
        self.ui.retranslateUi('')
        self.ui.ctr_cart_info.hlabel.setText(QtGui.QApplication.translate('Form', '           Title                   Price Information', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_back.reset()
        self.ui.btn_cancel.reset()
        self.ui.btn_coupon.setText(QtGui.QApplication.translate('Coupon', 'Coupon', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_clear_all_dvd.setText(QtGui.QApplication.translate('Coupon', 'Clear Cart', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_add_another.setText(QtGui.QApplication.translate('Coupon', 'Add Other', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_checkout.setText(QtGui.QApplication.translate('Coupon', 'Check Out', None, QtGui.QApplication.UnicodeUTF8))

    
    def hideEvent(self, event):
        self.ui.ShoppingCartForm_ctr_message_box.hide()
        self.ui.txtbox_msg.clear()
        self.hide()

    
    def cancel_click(self, row, column):
        if column == 3:
            data = { }
            data['wid'] = 'ShoppingCartForm'
            data['cid'] = 'ctr_cart_info'
            data['EVENT'] = 'EVENT_MOUSE_CLICK'
            data['type'] = 'EVENT'
            data['param_info'] = { }
            data['param_info']['ctr_cart_info'] = { }
            rfid = self.ui.ctr_cart_info.table.item(row, 3).data(self.ui.ctr_cart_info.dataType).toString()
            data['param_info']['ctr_cart_info']['rfid'] = str(rfid)
            self.sq.send(data)
        

    
    def test(self):
        data = {
            'ctr_cart_info': [
                {
                    'rfid': '00B4D32730000104E0',
                    'coupon_short_description': '28off',
                    'coupon_code': '',
                    'movie_title': 'Night Train (2009)',
                    'price_plan_text': 'Traditional First Night Fee R0.01, \nAdditional Night Fee R0.10, \nCutoff Time 19:00:00',
                    'movie_pic': 'image/tmp/m0.jpg' },
                {
                    'rfid': '00B4D32730000104E0',
                    'coupon_short_description': '28off',
                    'coupon_code': '',
                    'movie_title': 'Night Train (2009)',
                    'price_plan_text': 'Traditional First Night Fee R0.01, \nAdditional Night Fee R0.10, \nCutoff Time 19:00:00',
                    'movie_pic': 'image/tmp/m0.jpg' },
                {
                    'rfid': '00B4D32730000104E0',
                    'coupon_short_description': '28off',
                    'coupon_code': '',
                    'movie_title': 'Night Train (2009)',
                    'price_plan_text': 'Traditional First Night Fee R0.01, \nAdditional Night Fee R0.10, \nCutoff Time 19:00:00',
                    'movie_pic': 'image/tmp/m0.jpg' },
                {
                    'rfid': '00B4D32730000104E0',
                    'coupon_short_description': '28off',
                    'coupon_code': '',
                    'movie_title': 'Night Train (2009)',
                    'price_plan_text': 'Traditional First Night Fee R0.01, \nAdditional Night Fee R0.10, \nCutoff Time 19:00:00',
                    'movie_pic': 'image/tmp/m0.jpg' },
                {
                    'rfid': '00B4D32730000104E0',
                    'coupon_short_description': '28off',
                    'coupon_code': '',
                    'movie_title': 'Night Train (2009)',
                    'price_plan_text': 'Traditional First Night Fee R0.01, \nAdditional Night Fee R0.10, \nCutoff Time 19:00:00',
                    'movie_pic': 'image/tmp/m0.jpg' }],
            'global_coupon_code': 'a',
            'global_coupon_short_description': '28off' }
        self.ui.ctr_cart_info.setCartInfo(data)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    '\n\tif os.path.isfile(config.transDir+"trans_sp.qm"):\n\t\ttranslate = QtCore.QTranslator()\n\t\ttranslate.load("trans_sp.qm", config.transDir)\n\t\tapp.installTranslator(translate)\n\t'
    form = ShoppingCartForm()
    form.show()
    form.test()
    form.ui.txtbox_msg.setText('LKSasdfJDsadfKLFask GGGGGGGGGG GGGGGGGGGG GGGGGGGGGG')
    sys.exit(app.exec_())

