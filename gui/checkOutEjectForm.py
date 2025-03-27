# Source Generated with Decompyle++
# File: checkOutEjectForm.pyc (Python 2.5)

'''
CheckOutEjectForm for checkout
2009-07-14 created by Mavis
'''
import sys
import config
from PyQt4 import QtCore, QtGui
from checkOutEjectForm_ui import Ui_checkOutEjectForm
from component import btnBack, SWF_vomit, SWF_robot_send, SWF_robot_take, btnCenter, allKeyboard, messageBox

class CheckOutEjectForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_checkOutEjectForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_movie)))
        self.setPalette(palette)
        self.ui.swf_send_disc = SWF_robot_send(self)
        self.ui.swf_send_disc.setGeometry(92, 365, 585, 522)
        self.ui.swf_take_dvd = SWF_robot_take(self)
        self.ui.swf_take_dvd.setGeometry(QtCore.QRect(92, 365, 585, 522))
        self.ui.swf_vomit_dvd = SWF_vomit(self)
        self.ui.swf_vomit_dvd.setGeometry(QtCore.QRect(140, 490, 487, 290))
        self.ui.swf_send_disc.hide()
        self.ui.swf_take_dvd.hide()
        self.ui.swf_vomit_dvd.hide()
        self.ui.ctr_btn_center = btnCenter(self, 'CheckOutEjectForm')
        self.ui.ctr_btn_center.hide()
        self.ui.CheckOutEjectForm_ctr_all_keyboard = allKeyboard('CheckOutEjectForm')
        self.ui.CheckOutEjectForm_ctr_all_keyboard.hide()
        self.ui.CheckOutEjectForm_ctr_message_box = messageBox('CheckOutEjectForm', self)
        self.ui.CheckOutEjectForm_ctr_message_box = messageBox('CheckOutEjectForm', self)
        QtCore.QObject.connect(self.ui.CheckOutEjectForm_ctr_all_keyboard.btn_ok, QtCore.SIGNAL('clicked()'), self.showMsg)

    
    def showMsg(self):
        if not self.ui.CheckOutEjectForm_ctr_all_keyboard.lineedit.text():
            msg = QtCore.QT_TRANSLATE_NOOP('CheckOutEjectForm', 'Would you like to receive emails on upcoming releases, promotions, and free rentals offers?')
            self.ui.CheckOutEjectForm_ctr_message_box.show({
                'message': QtGui.QApplication.translate('CheckOutEjectForm', msg, None, QtGui.QApplication.UnicodeUTF8),
                'type': 'confirm' })
        

    
    def showEvent(self, e):
        self.ui.ctr_btn_center.init()
        self.ui.retranslateUi('')

    
    def hideEvent(self, e):
        self.ui.CheckOutEjectForm_ctr_all_keyboard.hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    import os
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    form = CheckOutEjectForm()
    form.show()
    form.ui.CheckOutEjectForm_ctr_all_keyboard.show()
    form.ui.swf_vomit_dvd.show()
    sys.exit(app.exec_())

