# Source Generated with Decompyle++
# File: testResultForm.pyc (Python 2.5)

'''
TestResultForm for initial form
2009-08-26 created by Mavis
'''
import sys
import config
from PyQt4 import QtCore, QtGui
from kioskTesting_ui import Ui_kioskTest
from component import btnFinish

class TestResultForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_kioskTest()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_test)))
        self.setPalette(palette)
        label = QtGui.QLabel(self)
        label.setGeometry(100, 150, 100, 100)
        label.setPixmap(QtGui.QPixmap(config.pic_available_yes).scaled(100, 100))
        self.ui.txt_msg1 = QtGui.QLabel(QtGui.QApplication.translate('Form', 'TESTING DONE', None, QtGui.QApplication.UnicodeUTF8), self)
        self.ui.txt_msg1.setGeometry(220, 150, 468, 100)
        self.ui.txt_msg1.setStyleSheet('color: #006633; font: bold 32px')
        self.ui.txt_msg2 = QtGui.QLabel(QtGui.QApplication.translate('Form', 'All slots have been verified OK.\nClick finish to take out the disc.', None, QtGui.QApplication.UnicodeUTF8), self)
        self.ui.txt_msg2.setGeometry(100, self.ui.txt_msg1.y() + self.ui.txt_msg1.height() + 50, 568, 100)
        self.ui.txt_msg2.setStyleSheet('font: bold 26px')
        self.ui.txt_msg2.setWordWrap(True)
        self.ui.txt_msg3 = QtGui.QLabel(QtGui.QApplication.translate('Form', 'Your kiosk is ready to be used now.', None, QtGui.QApplication.UnicodeUTF8), self)
        self.ui.txt_msg3.setGeometry(100, self.ui.txt_msg2.y() + self.ui.txt_msg2.height() + 50, 568, 100)
        self.ui.txt_msg3.setStyleSheet('font: bold 26px')
        self.ui.txt_msg3.setWordWrap(True)
        self.ui.btn_finish = btnFinish(self, 'TestResultForm')
        self.ui.btn_finish.setGeometry(500, self.ui.txt_msg3.y() + self.ui.txt_msg3.height() + 70, 159, config.btn_height)

    
    def showEvent(self, event):
        self.ui.retranslateUi(None)
        self.ui.txt_msg1.setText(QtGui.QApplication.translate('Form', 'TESTING DONE', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.txt_msg2.setText(QtGui.QApplication.translate('Form', 'All slots have been verified OK.\nClick finish to take out the disc.', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.txt_msg3.setText(QtGui.QApplication.translate('Form', 'Your kiosk is ready to be used now.', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_finish.reset()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = TestResultForm()
    form.show()
    sys.exit(app.exec_())

