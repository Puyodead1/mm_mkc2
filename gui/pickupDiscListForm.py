# Source Generated with Decompyle++
# File: pickupDiscListForm.pyc (Python 2.5)

'''
PickUpDiscListForm list disc that can pick up. 
2009-07-16 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
from pickupDiscListForm_ui import Ui_pickupDiskInfoForm
import component
import config
from squery import socketQuery

class PickUpDiscListForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_pickupDiskInfoForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        if not os.path.isfile(config.pic_bg_pickup):
            print('CAN NOT FIND THE PIC: %s' % config.pic_bg_start)
        
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_pickup)))
        self.setPalette(palette)
        self.ui.txt_msg = QtGui.QLabel(self)
        self.ui.txt_msg.setStyleSheet(config.style_membership_msg)
        self.ui.txt_msg.setAlignment(QtCore.Qt.AlignRight)
        self.ui.txt_msg.setGeometry(config.layout_x, self.ui.txtbox_msg.y() + self.ui.txtbox_msg.height(), config.unload_list_width, 40)
        self.ui.ctr_dvd_list = component.ListWidget(self, config.pic_width_little, config.pic_height_little)
        self.ui.ctr_dvd_list.setGeometry(config.layout_x, self.ui.txt_msg.y() + self.ui.txt_msg.height() + 10, config.unload_list_width, 5 * 75 + 76)
        self.sq = socketQuery()
        self.ui.ctr_btn_center = component.btnCenter(self, 'PickUpDiscListForm')
        self.ui.ctr_btn_center.hide()
        self.ui.btn_back = component.btnBack(self, 'PickUpDiscListForm')
        self.ui.btn_cancel = component.btnCancel(self, 'PickUpDiscListForm')
        self.ui.btn_cancel.setGeometry(580, 20, 160, 68)
        self.ui.btn_take_all = component.ctrButton(self, 'PickUpDiscListForm', 'btn_take_all', QtGui.QApplication.translate('Form', 'Take All', None, QtGui.QApplication.UnicodeUTF8), 160, 68, 'color: white; font: bold italic 30px; border-style: outset; background-image: url(' + config.pic_btn_blue + ')')
        self.ui.hboxlayout.addWidget(self.ui.btn_back)
        self.ui.hboxlayout.addWidget(self.ui.btn_take_all)

    
    def showEvent(self, event):
        self.ui.ctr_btn_center.init()
        self.ui.retranslateUi('')
        self.ui.btn_back.reset()
        self.ui.btn_cancel.reset()
        self.ui.btn_take_all.setText(QtGui.QApplication.translate('Form', 'Take All', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_dvd_list.hlabel.setText(QtGui.QApplication.translate('Form', '  Disc Information', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = PickUpDiscListForm()
    data = {
        'ctr_dvd_list': [
            {
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/90990_big.jpg',
                'movie_title': 'Chasing The Green (2009)' },
            {
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/90990_big.jpg',
                'movie_title': 'Applause For Miss E (2009)' }] }
    mainf.ui.ctr_dvd_list.setDVDList(data)
    mainf.show()
    sys.exit(app.exec_())

