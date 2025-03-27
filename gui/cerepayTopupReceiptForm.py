# Source Generated with Decompyle++
# File: cerepayTopupReceiptForm.pyc (Python 2.5)

import os
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
import component
import config
_Form_Name_String = 'CerepayReceiptForm'

class CerepayTopupReceiptForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = QtCore.QObject()
        self.setGeometry(0, 0, 768, 1024)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_movie)))
        self.setPalette(palette)
        self.ui.ctr_btn_center = component.btnCenter(self, _Form_Name_String)
        self.ui.btn_back = component.btnBack(self, _Form_Name_String)
        self.ui.btn_back.setGeometry(580, 20, 160, 68)
        self.title_label = QtGui.QLabel(self)
        self.title_label.setFixedHeight(30)
        self.title_label.setStyleSheet(config.style_membership_card)
        self.ui.info_list = component.CerepayCenterList(self, 'CerepayCenterForm', 'info_list')
        self.ui.info_list.setFixedHeight(384)
        vlayout = QtGui.QVBoxLayout()
        vlayout.setContentsMargins(50, 120, 50, 10)
        vlayout.addWidget(self.title_label)
        vlayout.addSpacing(50)
        vlayout.addWidget(self.ui.info_list)
        vlayout.addStretch(1)
        self.setLayout(vlayout)
        self.horizontalLayout = QtGui.QWidget(self)
        self.horizontalLayout.setGeometry(QtCore.QRect(40, 910, 691, 101))
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.hboxlayout = QtGui.QHBoxLayout(self.horizontalLayout)
        self.hboxlayout.setObjectName('hboxlayout')
        self.ui.btn_email = component.ctrButton(self, _Form_Name_String, 'btn_email', 'Email Me')
        self.hboxlayout.addWidget(self.ui.btn_email)
        self.ui.btn_finish = component.btnFinish(self, _Form_Name_String)
        self.hboxlayout.addWidget(self.ui.btn_finish)

    
    def showEvent(self, event):
        self.ui.ctr_btn_center.init()
        self.title_label.setText(QtGui.QApplication.translate('Form', '  Receipt  ', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    receipt_form = CerepayTopupReceiptForm()
    receipt_form.ui.info_list.setCerepayCenterList({
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
    receipt_form.show()
    sys.exit(app.exec_())

