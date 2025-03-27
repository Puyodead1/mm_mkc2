# Source Generated with Decompyle++
# File: registerResultForm.pyc (Python 2.5)

import sys
import config
from component import btnBack, ctrButton, allKeyboard, btnCenter, btnFinish
from PyQt4 import QtCore, QtGui

class RegisterResultForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = QtCore.QObject()
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_load)))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.ui.ctr_btn_center = btnCenter(self, 'RegisterResultForm')
        self.txtbox_msg = QtGui.QLabel(self)
        self.txtbox_msg.setGeometry(90, 160, 571, 720)
        self.txtbox_msg.setAlignment(QtCore.Qt.AlignTop)
        self.txtbox_msg.setWordWrap(True)
        self.ui.ctr_btn_finish = btnFinish(self, 'RegisterResultForm')
        btn_widget = QtGui.QWidget(self)
        btn_widget.setGeometry(QtCore.QRect(50, 920, 671, 91))
        hboxlayout = QtGui.QHBoxLayout(btn_widget)
        hboxlayout.addWidget(self.ui.ctr_btn_finish, 1, QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.txtbox_msg.setFont(font)

    
    def showEvent(self, event):
        self.ui.ctr_btn_center.label_bg.setText(QtGui.QApplication.translate('Form', 'Hello, xxxxxxxxxxxxxxxxxxxxxxxx', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_btn_center.btn_logout.setText('\n\n' + QtGui.QApplication.translate('Form', 'Logout', None, QtGui.QApplication.UnicodeUTF8))
        self.txtbox_msg.setText('Thank you for registration. \n\nThe system will send two activate links to your email.\nPlease click on them to activate both of your cerepay and membership account for more service.')


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = RegisterResultForm()
    form.show()
    sys.exit(app.exec_())

