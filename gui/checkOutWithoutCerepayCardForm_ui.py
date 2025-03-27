# Source Generated with Decompyle++
# File: checkOutWithoutCerepayCardForm_ui.pyc (Python 2.5)

from PyQt4 import QtCore, QtGui

class Ui_checkOutWithoutCerepayCardForm(object):
    
    def setupUi(self, checkOutWithoutCerepayCardForm):
        checkOutWithoutCerepayCardForm.setObjectName('checkOutWithoutCerepayCardForm')
        checkOutWithoutCerepayCardForm.resize(QtCore.QSize(QtCore.QRect(0, 0, 768, 1024).size()).expandedTo(checkOutWithoutCerepayCardForm.minimumSizeHint()))
        checkOutWithoutCerepayCardForm.setMinimumSize(QtCore.QSize(768, 1024))
        checkOutWithoutCerepayCardForm.setMaximumSize(QtCore.QSize(768, 1024))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        checkOutWithoutCerepayCardForm.setPalette(palette)
        checkOutWithoutCerepayCardForm.setAutoFillBackground(True)
        self.txt_msg = QtGui.QLabel(checkOutWithoutCerepayCardForm)
        self.txt_msg.setGeometry(QtCore.QRect(90, 160, 571, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.txt_msg.setFont(font)
        self.txt_msg.setObjectName('txt_msg')
        self.horizontalLayout = QtGui.QWidget(checkOutWithoutCerepayCardForm)
        self.horizontalLayout.setGeometry(QtCore.QRect(50, 920, 671, 91))
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.hboxlayout = QtGui.QHBoxLayout(self.horizontalLayout)
        self.hboxlayout.setObjectName('hboxlayout')
        self.retranslateUi(checkOutWithoutCerepayCardForm)
        QtCore.QMetaObject.connectSlotsByName(checkOutWithoutCerepayCardForm)

    
    def retranslateUi(self, checkOutWithoutCerepayCardForm):
        self.txt_msg.setText(QtGui.QApplication.translate('checkOutWithoutCerepayCardForm', 'Please enter your email address.', None, QtGui.QApplication.UnicodeUTF8))


