# Source Generated with Decompyle++
# File: returnSwipeCardForm.pyc (Python 2.5)

'''
ReturnSwipeCardForm
2009-07-29 created by Mavis
'''
import sys
from PyQt4 import QtCore, QtGui
from return_ui import Ui_returnForm
import config
from component import btnCancel, messageBox, SWF_sweepcard, SWF_robot_send

class ReturnSwipeCardForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_returnForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_return)))
        self.setPalette(palette)
        self.ui.swf_send_disc = SWF_robot_send(self)
        self.ui.swf_send_disc.setGeometry(self.ui.txtbox_msg.x() + 10, self.ui.txtbox_msg.y() + 30 + self.ui.txtbox_msg.height(), 585, 522)
        self.ui.swf_swipe_card = SWF_sweepcard(self)
        self.ui.swf_swipe_card.setGeometry(self.ui.swf_send_disc.x() + 30, self.ui.swf_send_disc.y() + 30, self.ui.swf_send_disc.width(), self.ui.swf_send_disc.height())
        self.ui.swf_swipe_card.hide()
        self.ui.swf_send_disc.hide()
        self.ui.txtbox_msg.setText(QtGui.QApplication.translate('ReturnSwipeCardForm', 'Please swipe the credit card you used to rent the disc.', None, QtGui.QApplication.UnicodeUTF8))
        style = 'color: white; font: bold italic 26px; border-style: outset; background-image: url(' + config.pic_btn_config_red + ')'
        self.ui.btn_cancel = btnCancel(self, 'ReturnSwipeCardForm')
        self.ui.btn_cancel.setGeometry(500, self.ui.swf_send_disc.y() + self.ui.swf_send_disc.height(), 159, 68)
        self.ui.ReturnSwipeCardForm_ctr_message_box = messageBox('ReturnSwipeCardForm', self)

    
    def showEvent(self, event):
        self.ui.retranslateUi('')
        self.ui.txtbox_msg.setText(QtGui.QApplication.translate('ReturnSwipeCardForm', 'Please swipe the credit card you used to rent the disc.', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_cancel.reset()

    
    def hideEvent(self, event):
        self.ui.ReturnSwipeCardForm_ctr_message_box.hide()
        self.hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    import os
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    form = ReturnSwipeCardForm()
    form.show()
    sys.exit(app.exec_())

