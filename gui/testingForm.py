# Source Generated with Decompyle++
# File: testingForm.pyc (Python 2.5)

'''
TestingForm for initial form
2009-08-26 created by Mavis
'''
import sys
import config
from PyQt4 import QtCore, QtGui
from kioskTesting_ui import Ui_kioskTest
from component import SWF_process

class TestingForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_kioskTest()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_test)))
        self.setPalette(palette)
        self.ui.txt_msg1 = QtGui.QLabel(QtGui.QApplication.translate('Form', 'Processing ....', None, QtGui.QApplication.UnicodeUTF8), self)
        self.ui.txt_msg1.setGeometry(100, 150, 568, 70)
        self.ui.txt_msg1.setStyleSheet('font: bold 26px')
        self.ui.txt_msg2 = QtGui.QLabel(QtGui.QApplication.translate('Form', 'DO NOT POWER OFF THE KIOSK', None, QtGui.QApplication.UnicodeUTF8), self)
        self.ui.txt_msg2.setGeometry(100, self.ui.txt_msg1.y() + self.ui.txt_msg1.height() + 50, 568, 70)
        self.ui.txt_msg2.setStyleSheet('color: #bb0000; font: bold 32px')
        self.ui.txt_msg3 = QtGui.QLabel(QtGui.QApplication.translate('Form', 'If the kiosk stops responding for more\nthan 15 minutes, please contact our tech\nsupport.', None, QtGui.QApplication.UnicodeUTF8), self)
        self.ui.txt_msg3.setGeometry(100, self.ui.txt_msg2.y() + self.ui.txt_msg2.height() + 50, 568, 180)
        self.ui.txt_msg3.setStyleSheet('font: bold 26px')
        self.ui.txt_msg3.setWordWrap(True)
        bar_w = 660
        bar_h = 85
        self.ui.swf_process_bar = SWF_process(self)
        self.ui.swf_process_bar.setGeometry((768 - bar_w) / 2, self.ui.txt_msg3.y() + self.ui.txt_msg3.height() + 80, bar_w, bar_h)

    
    def showEvent(self, event):
        self.ui.retranslateUi(None)
        self.ui.txt_msg1.setText(QtGui.QApplication.translate('Form', 'Processing ....', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.txt_msg2.setText(QtGui.QApplication.translate('Form', 'DO NOT POWER OFF THE KIOSK', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.txt_msg3.setText(QtGui.QApplication.translate('Form', 'If the kiosk stops responding for more\nthan 15 minutes, please contact our tech\nsupport.', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = TestingForm()
    form.show()
    sys.exit(app.exec_())

