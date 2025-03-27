# Source Generated with Decompyle++
# File: returnTakeInForm.pyc (Python 2.5)

'''
ReturnTakeInForm
2009-07-29 created by Mavis
'''
import sys
from PyQt4 import QtCore, QtGui
from return_ui import Ui_returnForm
import config
from component import btnCancel, btnFinish, ctrButton, SWF_insert, SWF_insert_h, SWF_vomit, SWF_robot_send, Return_messageBox

class ReturnTakeInForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_returnForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        self.setFixedSize(768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_return)))
        self.setPalette(palette)
        lw = QtGui.QWidget(self)
        lw.setGeometry(91, self.ui.txt_return_label.y() + self.ui.txt_return_label.height() + 50, 586, 820)
        self.ui.swf_send_disc = SWF_robot_send(lw)
        self.ui.swf_insert = SWF_insert(lw)
        self.ui.swf_insert_h = SWF_insert_h(lw)
        self.ui.swf_vomit_dvd = SWF_vomit(lw)
        self.ui.swf_vomit_dvd.hide()
        self.ui.swf_send_disc.hide()
        self.ui.swf_insert.hide()
        style = 'color: white; font: bold italic 30px; border-style: outset; background-image: url(' + config.pic_btn_config_red + ')'
        self.ui.btn_cancel = btnCancel(self, 'ReturnTakeInForm')
        self.ui.btn_finish = btnFinish(self, 'ReturnTakeInForm')
        self.ui.btn_finish.hide()
        self.ui.btn_continue = ctrButton(self, 'ReturnTakeInForm', 'btn_continue', QtGui.QApplication.translate('Form', 'Continue', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.ui.ReturnTakeInForm_ctr_message_box = Return_messageBox('ReturnTakeInForm', self)
        layout = QtGui.QVBoxLayout(lw)
        layout.setSpacing(5)
        layout.addSpacing(180)
        layout.addWidget(self.ui.swf_send_disc, 1)
        layout.addWidget(self.ui.swf_insert, 1)
        layout.addWidget(self.ui.swf_insert_h, 1)
        layout.addWidget(self.ui.swf_vomit_dvd, 1)
        layout.setAlignment(self.ui.swf_send_disc, QtCore.Qt.AlignCenter)
        layout.setAlignment(self.ui.swf_insert, QtCore.Qt.AlignCenter)
        layout.setAlignment(self.ui.swf_vomit_dvd, QtCore.Qt.AlignCenter)
        btnlay = QtGui.QHBoxLayout()
        frame = QtGui.QFrame()
        btnlay.addWidget(frame)
        btnlay.addWidget(self.ui.btn_continue, QtCore.Qt.AlignLeft)
        btnlay.addSpacing(360)
        btnlay.addWidget(self.ui.btn_cancel, QtCore.Qt.AlignRight)
        btnlay.addWidget(self.ui.btn_finish, QtCore.Qt.AlignRight)
        layout.addLayout(btnlay)

    
    def hideEvent(self, event):
        self.ui.ReturnTakeInForm_ctr_message_box.hide()
        self.hide()

    
    def showEvent(self, event):
        self.ui.retranslateUi('')
        self.ui.btn_cancel.reset()
        self.ui.btn_finish.reset()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    import os
    config.transFile = 'trans_es.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    form = ReturnTakeInForm()
    form.show()
    form.ui.swf_send_disc.show()
    form.ui.btn_cancel.show()
    sys.exit(app.exec_())

