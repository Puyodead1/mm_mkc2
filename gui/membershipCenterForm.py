# Source Generated with Decompyle++
# File: membershipCenterForm.pyc (Python 2.5)

'''
MembershipCenterForm for membership center
2010-06-25 created by Mavis
'''
import sys
import config
from component import messageBox, btnBack, ctrButton, btnCenter, RecommendationList
from PyQt4 import QtCore, QtGui

class MembershipCenterForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = QtCore.QObject()
        self.setGeometry(0, 0, 768, 1024)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_member)))
        self.setPalette(palette)
        self.ui.ctr_btn_center = btnCenter(self, 'MembershipCenterForm')
        btn_width = 350
        btn_height = 65
        self.ui.btn_transactions = ctrButton(self, 'MembershipCenterForm', 'btn_transactions', '', btn_width, btn_height, config.style_btn_big)
        self.ui.btn_coupons = ctrButton(self, 'MembershipCenterForm', 'btn_coupons', '', btn_width, btn_height, config.style_btn_big)
        self.ui.btn_profile = ctrButton(self, 'MembershipCenterForm', 'btn_profile', '', btn_width, btn_height, config.style_btn_big)
        self.ui.btn_browse = ctrButton(self, 'MembershipCenterForm', 'btn_browse', '', btn_width, btn_height, config.style_btn_big)
        self.ui.btn_reserved = ctrButton(self, 'MembershipCenterForm', 'btn_reserved', '', btn_width, btn_height, config.style_btn_big)
        self.ui.btn_cerepay = ctrButton(self, 'MembershipCenterForm', 'btn_cerepay', '', btn_width, btn_height, config.style_btn_big)
        label_0 = QtGui.QLabel(self)
        label_0.setFixedWidth(130)
        label_1 = QtGui.QLabel(self)
        label_1.setFixedWidth(50)
        label_2 = QtGui.QLabel(self)
        label_2.setFixedWidth(50)
        label_3 = QtGui.QLabel(self)
        label_3.setFixedWidth(130)
        hl_0 = QtGui.QHBoxLayout()
        hl_0.setAlignment(QtCore.Qt.AlignRight)
        hl_0.addWidget(self.ui.btn_transactions)
        hl_0.addWidget(label_0)
        hl_1 = QtGui.QHBoxLayout()
        hl_1.setAlignment(QtCore.Qt.AlignRight)
        hl_1.addWidget(self.ui.btn_coupons)
        hl_1.addWidget(label_1)
        hl_2 = QtGui.QHBoxLayout()
        hl_2.setAlignment(QtCore.Qt.AlignRight)
        hl_2.addWidget(self.ui.btn_reserved)
        hl_2.addWidget(label_2)
        hl_3 = QtGui.QHBoxLayout()
        hl_3.setAlignment(QtCore.Qt.AlignRight)
        hl_3.addWidget(self.ui.btn_cerepay)
        hl_3.addWidget(label_3)
        self.label_card = QtGui.QLabel(self)
        self.label_card.setStyleSheet(config.style_membership_card)
        self.label_card.setFixedHeight(30)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        self.label_card.setSizePolicy(sizePolicy)
        self.label_welcome = QtGui.QLabel()
        self.label_welcome.setAlignment(QtCore.Qt.AlignCenter)
        self.label_welcome.setWordWrap(True)
        font = QtGui.QFont()
        font.setFamily('Mukti Narrow')
        font.setPixelSize(34)
        font.setBold(True)
        self.label_welcome.setFont(font)
        palette_l = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 96, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette_l.setBrush(QtGui.QPalette.WindowText, brush)
        self.label_welcome.setPalette(palette_l)
        self.ui.card_number = QtGui.QLabel(self)
        self.ui.card_number.setFixedHeight(30)
        self.ui.card_number.setStyleSheet(config.style_membership_card)
        self.ui.txt_msg = QtGui.QLabel(self)
        self.ui.txt_msg.setStyleSheet(config.style_membership_msg)
        self.ui.txt_msg.setMaximumHeight(50)
        self.ui.txt_msg.setWordWrap(True)
        self.ui.ctr_movie_list = RecommendationList(self)
        hl = QtGui.QHBoxLayout()
        hl.addWidget(self.label_card, 0, QtCore.Qt.AlignLeft)
        hl.addWidget(self.ui.card_number, 2, QtCore.Qt.AlignLeft)
        w = QtGui.QWidget()
        w.setMaximumSize(768 - 80, 6 * (btn_height + 10) + 20)
        w.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(w.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_membership_center)))
        w.setPalette(palette)
        vl = QtGui.QVBoxLayout()
        vl.setContentsMargins(0, 10, 0, 10)
        vl.setSpacing(10)
        vl.addLayout(hl_0)
        vl.addLayout(hl_1)
        vl.addWidget(self.ui.btn_profile, 0, QtCore.Qt.AlignRight)
        vl.addWidget(self.ui.btn_browse, 0, QtCore.Qt.AlignRight)
        vl.addLayout(hl_2)
        vl.addLayout(hl_3)
        hl_w = QtGui.QHBoxLayout(w)
        hl_w.addWidget(self.label_welcome)
        hl_w.addLayout(vl)
        vlayout = QtGui.QVBoxLayout()
        vlayout.setContentsMargins(40, 120, 40, 10)
        vlayout.addLayout(hl)
        vlayout.addWidget(self.ui.txt_msg)
        vlayout.addWidget(w)
        vlayout.addWidget(self.ui.ctr_movie_list)
        self.setLayout(vlayout)
        self.ui.MembershipCenterForm_ctr_message_box = messageBox('MembershipCenterForm', self)
        self.ui.MembershipCenterForm_ctr_message_box.hide()

    
    def hideEvent(self, event):
        self.ui.MembershipCenterForm_ctr_message_box.hide()

    
    def showEvent(self, event):
        self.ui.ctr_btn_center.init()
        self.ui.ctr_movie_list.init()
        self.label_card.setText(QtGui.QApplication.translate('Form', 'Card Number:', None, QtGui.QApplication.UnicodeUTF8))
        self.label_welcome.setText(QtGui.QApplication.translate('Form', 'Welcome to Membership Center', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_transactions.setText(QtGui.QApplication.translate('Form', 'Historical Transactions', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_coupons.setText(QtGui.QApplication.translate('Form', 'Coupons', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_profile.setText(QtGui.QApplication.translate('Form', 'My Profile', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_browse.setText(QtGui.QApplication.translate('Form', 'Browse Discs', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_reserved.setText(QtGui.QApplication.translate('Form', 'Disc(s) You Reserved', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_cerepay.setText(QtGui.QApplication.translate('Form', 'My Membership Account', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    import os
    config.transFile = 'trans_en.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    form = MembershipCenterForm()
    form.show()
    form.ui.txt_msg.setText('Please vvvvvvvvv Welcome to Membership Center Welcome to Membership Center Welcome to Membership Center ...')
    form.ui.card_number.setText('97190273487987874')
    form.ui.ctr_movie_list.setRecommendationList({
        'ctr_movie_list': [
            {
                'upc': '23421345',
                'movie_title': '30 MAN MNL LKJL Days Of Night (2007)',
                'movie_pic': '/home/mm/kiosk/var/gui/pic/78268.jpg' },
            {
                'upc': '502194',
                'movie_title': 'Agent Cody Banks 2 Destination London (2004)',
                'movie_pic': '/home/mm/kiosk/var/gui/pic/23875.jpg' },
            {
                'upc': '23421345',
                'movie_title': 'Agent Cody Banks 2 Destination London (2004)',
                'movie_pic': '/home/mm/kiosk/var/gui/pic/78268.jpg' },
            {
                'upc': '502194',
                'movie_title': 'Appaloosa (2008)',
                'movie_pic': '/home/mm/kiosk/var/gui/pic/23875.jpg' },
            {
                'upc': '502194',
                'movie_title': 'Appaloosa (2008)',
                'movie_pic': '/home/mm/kiosk/var/gui/pic/23875.jpg' }] })
    form.ui.ctr_movie_list.show()
    sys.exit(app.exec_())

