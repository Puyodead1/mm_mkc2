# Source Generated with Decompyle++
# File: testTakeInForm.pyc (Python 2.5)

'''
TestTakeInForm for initial form
2009-08-26 created by Mavis
'''
import sys
import config
from PyQt4 import QtCore, QtGui
from kioskTesting_ui import Ui_kioskTest
from component import btnCancel, SWF_insert, SWF_robot_send, SWF_vomit

class TestTakeInForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_kioskTest()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_test)))
        self.setPalette(palette)
        self.ui.txt_msg.setText(QtGui.QApplication.translate('Form', 'Please insert a disc', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.txt_msg.setStyleSheet('font: bold 26px')
        self.ui.swf_insert = SWF_insert(self)
        self.ui.swf_insert.setGeometry(self.ui.txt_msg.x() + 30, self.ui.txt_msg.y() + self.ui.txt_msg.height() + 50, 487, 290)
        self.ui.swf_insert.hide()
        self.ui.swf_send_disc = SWF_robot_send(self)
        self.ui.swf_send_disc.setGeometry(self.ui.txt_msg.x() + 30, self.ui.txt_msg.y() + self.ui.txt_msg.height(), 585, 522)
        self.ui.swf_send_disc.hide()
        self.ui.swf_vomit_dvd = SWF_vomit(self)
        self.ui.swf_vomit_dvd.setGeometry(self.ui.txt_msg.x() + 30, self.ui.txt_msg.y() + self.ui.txt_msg.height() + 50, 487, 290)
        self.ui.swf_vomit_dvd.hide()
        self.ui.btn_cancel = btnCancel(self, 'TestTakeInForm')
        self.ui.btn_cancel.setGeometry(500, self.ui.swf_send_disc.y() + self.ui.swf_send_disc.height() + 20, 159, config.btn_height)

    
    def showEvent(self, event):
        self.ui.retranslateUi(None)
        self.ui.txt_msg.setText(QtGui.QApplication.translate('Form', 'Please insert a disc', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_cancel.reset()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = TestTakeInForm()
    form.show()
    sys.exit(app.exec_())

