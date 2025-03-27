# Source Generated with Decompyle++
# File: checkOutResultForm.pyc (Python 2.5)

'''
CheckOutResultForm for checkout
2009-07-14 created by Mavis
'''
import sys
import config
from PyQt4 import QtCore, QtGui
from checkOutResultForm_ui import Ui_checkOutResultForm
from squery import socketQuery
from component import btnFinish, ctrButton, allKeyboard, btnCenter

class CheckOutResultForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_checkOutResultForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_movie)))
        self.setPalette(palette)
        self.sq = socketQuery()
        self.ui.ctr_btn_center = btnCenter(self, 'CheckOutResultForm')
        self.ui.ctr_btn_center.hide()
        self.ui.btn_finish = btnFinish(self, 'CheckOutResultForm')
        self.ui.btn_finish.setGeometry(580, 930, 160, 68)
        self.ui.btn_print = ctrButton(self, 'CheckOutResultForm', 'btn_print', QtGui.QApplication.translate('Form', 'Print Receipt', None, QtGui.QApplication.UnicodeUTF8), config.btn_width, config.btn_height, config.btn02Style)
        self.ui.btn_print.setGeometry(28, 930, config.btn_width, config.btn_height)
        self.ui.btn_print.hide()
        self.ui.CheckOutResultForm_ctr_all_keyboard = allKeyboard('CheckOutResultForm', self)
        self.ui.CheckOutResultForm_ctr_all_keyboard.hide()

    
    def showEvent(self, event):
        self.ui.ctr_btn_center.init()
        self.ui.retranslateUi(None)
        self.ui.btn_finish.reset()
        self.ui.btn_print.setText(QtGui.QApplication.translate('Form', 'Print Receipt', None, QtGui.QApplication.UnicodeUTF8))

    
    def hideEvent(self, event):
        self.ui.CheckOutResultForm_ctr_all_keyboard.hide()
        self.hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    import os
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    form = CheckOutResultForm()
    form.show()
    form.ui.txt_sale_price.setText('')
    form.ui.txt_taken.setText('0 DVD(s) have been taken out. Not all of the discs have been ejected.\n(R8-05R6) Retrieve from slot 104 failed: Insert Failed.\n(R8-05R7) Retrieve from slot 101 failed: No Disc.\n')
    form.ui.txt_input_label.setText('Please enter your Email to get receipts')
    form.ui.txt_thank1.show()
    form.ui.txt_thank1.setText('The rent operation failed, please try another one.')
    form.ui.CheckOutResultForm_ctr_all_keyboard.show({
        'type': 'email' })
    sys.exit(app.exec_())

