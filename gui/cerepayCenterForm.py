# Source Generated with Decompyle++
# File: cerepayCenterForm.pyc (Python 2.5)

import sys
import config
from component import btnBack, ctrButton, btnCenter, CerepayCenterList
from PyQt4 import QtCore, QtGui

class CerepayCenterForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = QtCore.QObject()
        self.setGeometry(0, 0, 768, 1024)
        self.i = 0
        btn_width = 350
        btn_height = 65
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_member)))
        self.setPalette(palette)
        self.ui.ctr_btn_center = btnCenter(self, 'CerepayCenterForm')
        self.ui.btn_back = btnBack(self, 'CerepayCenterForm')
        self.ui.btn_back.setGeometry(580, 20, 160, 68)
        self.ui.info_list = CerepayCenterList(self, 'CerepayCenterForm', 'info_list')
        self.ui.info_list.setFixedHeight(384)
        self.ui.txt_msg = QtGui.QLabel(self)
        self.ui.txt_msg.setStyleSheet(config.style_membership_msg)
        self.ui.txt_msg.setMaximumHeight(50)
        self.ui.txt_msg.setWordWrap(True)
        self.label_btn = QtGui.QLabel()
        self.label_btn.setFixedHeight(4 * btn_height)
        vl = QtGui.QVBoxLayout()
        style_btn_small = 'color: white; font: bold italic 20px; border-style: outset; background-image: url(' + config.pic_btn_blue_big + ')'
        self.ui.btn_top_up = ctrButton(self, 'CerepayCenterForm', 'btn_top_up', '', btn_width, btn_height, style_btn_small)
        self.ui.btn_transactions = ctrButton(self, 'CerepayCenterForm', 'btn_transactions', '', btn_width, btn_height, style_btn_small)
        self.ui.btn_missing = ctrButton(self, 'CerepayCenterForm', 'btn_missing', '', btn_width, btn_height, style_btn_small)
        vl.addWidget(self.ui.btn_top_up, 0, QtCore.Qt.AlignLeft)
        vl.addWidget(self.ui.btn_transactions, 0, QtCore.Qt.AlignLeft)
        vl.addWidget(self.ui.btn_missing, 0, QtCore.Qt.AlignLeft)
        self.label_btn.setLayout(vl)
        self.title_label = QtGui.QLabel(self)
        self.title_label.setFixedHeight(30)
        self.title_label.setStyleSheet(config.style_membership_card)
        vlayout = QtGui.QVBoxLayout()
        vlayout.setContentsMargins(50, 120, 50, 10)
        vlayout.addWidget(self.title_label)
        vlayout.addSpacing(30)
        vlayout.addWidget(self.ui.info_list)
        vlayout.addWidget(self.ui.txt_msg)
        vlayout.addWidget(self.label_btn)
        vlayout.addStretch(1)
        self.setLayout(vlayout)

    
    def showEvent(self, event):
        self.ui.ctr_btn_center.init()
        self.ui.txt_msg.setText('please rember to logout when you leave the kiosk to protect your privacy')
        self.title_label.setText(QtGui.QApplication.translate('Form', 'My Membership Account', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_top_up.setText(QtGui.QApplication.translate('Form', 'Top Up', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_transactions.setText(QtGui.QApplication.translate('Form', 'Historical Transactions', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_missing.setText(QtGui.QApplication.translate('Form', 'Report Missing', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    import os
    form = CerepayCenterForm()
    form.ui.info_list.setCerepayCenterList({
        'info_list': [
            {
                'title': 'Card Number',
                'info': '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111' },
            {
                'title': 'Balance',
                'info': '100' },
            {
                'title': 'Card Number',
                'info': '123456789' },
            {
                'title': 'Hold Amount',
                'info': '10' },
            {
                'title': 'Actual Balance',
                'info': '90' }] })
    form.show()
    sys.exit(app.exec_())

