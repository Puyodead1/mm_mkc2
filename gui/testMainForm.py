# Source Generated with Decompyle++
# File: testMainForm.pyc (Python 2.5)

'''
TestMainForm for initial form
2009-08-26 created by Mavis
'''
import sys
import config
from PyQt4 import QtCore, QtGui
from kioskTesting_ui import Ui_kioskTest
from component import ctrButton

class TestMainForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_kioskTest()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_test)))
        self.setPalette(palette)
        self.ui.txt_msg.setText(QtGui.QApplication.translate('Form', 'Would you like to run a full test, which\n\nmay take about 2 hours?', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.txt_msg.setStyleSheet('font: bold 26px')
        btn_w = 395
        self.ui.btn_yes = ctrButton(self, 'TestMainForm', 'btn_yes', QtGui.QApplication.translate('Form', 'Yes, run it please', None, QtGui.QApplication.UnicodeUTF8), btn_w, config.btnHeight, 'color: white; font: bold italic 28px; border-style: outset; background-image: url(' + config.pic_btn_test_blue_big + ')')
        self.ui.btn_no = ctrButton(self, 'TestMainForm', 'btn_no', QtGui.QApplication.translate('Form', 'No, please skip it', None, QtGui.QApplication.UnicodeUTF8), btn_w, config.btnHeight, 'color: white; font: bold italic 28px; border-style: outset; background-image: url(' + config.pic_btn_test_red_big + ')')
        self.ui.btn_yes.setGeometry((768 - btn_w) / 2, self.ui.txt_msg.y() + self.ui.txt_msg.height() + 50, btn_w, config.btnHeight)
        self.ui.btn_no.setGeometry((768 - btn_w) / 2, self.ui.btn_yes.y() + self.ui.btn_yes.height() + 50, btn_w, config.btnHeight)

    
    def showEvent(self, event):
        self.ui.retranslateUi(None)
        self.ui.txt_msg.setText(QtGui.QApplication.translate('Form', 'Would you like to run a full test, which\n\nmay take about 2 hours?', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_yes.setText(QtGui.QApplication.translate('Form', 'Yes, run it please', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_no.setText(QtGui.QApplication.translate('Form', 'No, please skip it', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = TestMainForm()
    form.show()
    sys.exit(app.exec_())

