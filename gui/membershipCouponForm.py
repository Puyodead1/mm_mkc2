# Source Generated with Decompyle++
# File: membershipCouponForm.pyc (Python 2.5)

'''
MembershipCouponForm 
2010-07-02 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
import component
import config
from squery import socketQuery

class MembershipCouponForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = QtCore.QObject()
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_member)))
        self.setPalette(palette)
        self.ui.txtbox_msg = QtGui.QLabel(self)
        self.ui.txtbox_msg.setGeometry(QtCore.QRect(60, 137, 571, 60))
        self.ui.txtbox_msg.setStyleSheet(config.style_membership_card)
        self.ui.txt_msg = QtGui.QLabel(self)
        self.ui.txt_msg.setStyleSheet(config.style_membership_msg)
        self.ui.txt_msg.setAlignment(QtCore.Qt.AlignRight)
        self.ui.txt_msg.setGeometry(config.layout_x, self.ui.txtbox_msg.y() + self.ui.txtbox_msg.height(), config.unload_list_width, 40)
        self.ui.ctr_coupon_list = component.TransactionList(self, 'ctr_coupon_list', 2)
        self.ui.ctr_coupon_list.setGeometry(config.layout_x, self.ui.txt_msg.y() + self.ui.txt_msg.height() + 10, config.unload_list_width, 5 * 75 + 76)
        self.ui.btn_back = component.btnBack(self, 'MembershipCouponForm')
        self.ui.ctr_btn_center = component.btnCenter(self, 'MembershipCouponForm')
        self.ui.horizontalLayout = QtGui.QWidget(self)
        self.ui.horizontalLayout.setGeometry(QtCore.QRect(50, 910, 661, 91))
        self.ui.horizontalLayout.setObjectName('horizontalLayout')
        self.ui.hboxlayout = QtGui.QHBoxLayout(self.ui.horizontalLayout)
        self.ui.hboxlayout.setSpacing(50)
        self.ui.hboxlayout.setObjectName('hboxlayout')
        self.ui.hboxlayout.addWidget(self.ui.btn_back)

    
    def showEvent(self, event):
        self.ui.ctr_btn_center.init()
        self.ui.btn_back.reset()
        self.ui.ctr_coupon_list.hlabel.setText(QtGui.QApplication.translate('Form', ' Coupon                  Description', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.txtbox_msg.setText(QtGui.QApplication.translate('Form', 'Coupons', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = MembershipCouponForm()
    data = {
        'ctr_coupon_list': [
            {
                'coupon_code': '$1.99',
                'state': 'Close',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/90990_big.jpg',
                'description': 'Chasing The Green (2009)' },
            {
                'coupon_code': '$1.99',
                'state': 'Close',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/90990_big.jpg',
                'description': 'Applause For Miss E (2009)' },
            {
                'coupon_code': '$1.99',
                'state': 'Close',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/90990_big.jpg',
                'description': 'Applause For Miss E (2009)' },
            {
                'coupon_code': '$1.99',
                'state': 'Close',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/90990_big.jpg',
                'description': 'Applause For Miss E (2009)' },
            {
                'coupon_code': '$1.99',
                'state': 'Close',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/90990_big.jpg',
                'description': 'Applause For Miss E (2009)' },
            {
                'coupon_code': '$1.99',
                'state': 'Close',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/90990_big.jpg',
                'description': 'Applause For Miss E (2009)' }] }
    mainf.ui.ctr_coupon_list.setList(data)
    mainf.setGeometry(0, 0, 768, 1024)
    mainf.show()
    mainf.ui.txt_msg.setText('laksdfj@lksjlkfj.com')
    sys.exit(app.exec_())

