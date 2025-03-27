# Source Generated with Decompyle++
# File: movieAvailableNoticeForm.pyc (Python 2.5)

'''
DiscAvailableNoticeForm for checkout
2009-07-14 created by Mavis
'''
import sys
import config
from PyQt4 import QtCore, QtGui
from squery import socketQuery
from unloadResultForm_ui import Ui_unloadResultForm
from component import btnBack, btnCancel, btnFinish, allKeyboard, btnCenter

class DiscAvailableNoticeForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_unloadResultForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_movie)))
        self.setPalette(palette)
        self.sq = socketQuery()
        self.ui.txt_unload_label.setText(QtGui.QApplication.translate('Form', 'Available Notice', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_btn_center = btnCenter(self, 'DiscAvailableNoticeForm')
        self.ui.ctr_btn_center.hide()
        self.ui.btn_back = btnBack(self, 'DiscAvailableNoticeForm')
        self.ui.btn_back.setGeometry(580, 20, 160, 68)
        self.ui.btn_cancel = btnCancel(self, 'DiscAvailableNoticeForm')
        self.ui.btn_finish = btnFinish(self, 'DiscAvailableNoticeForm')
        self.ui.hboxlayout.addWidget(self.ui.btn_cancel)
        self.ui.hboxlayout.addWidget(self.ui.btn_finish)
        self.ui.DiscAvailableNoticeForm_ctr_all_keyboard = allKeyboard('DiscAvailableNoticeForm', self)
        self.ui.DiscAvailableNoticeForm_ctr_all_keyboard.hide()

    
    def hideEvent(self, event):
        self.ui.DiscAvailableNoticeForm_ctr_all_keyboard.hide()
        self.hide()

    
    def showEvent(self, event):
        self.ui.ctr_btn_center.init()
        self.ui.txt_unload_label.setText(QtGui.QApplication.translate('Form', 'Available Notice', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_back.reset()
        self.ui.btn_cancel.reset()
        self.ui.btn_finish.reset()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    import os
    config.transFile = 'trans_en.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    form = DiscAvailableNoticeForm()
    form.show()
    sys.exit(app.exec_())

