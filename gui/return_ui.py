# Source Generated with Decompyle++
# File: return_ui.pyc (Python 2.5)

from PyQt4 import QtCore, QtGui
from config import pic_info2

class Ui_returnForm(object):
    
    def setupUi(self, returnForm):
        returnForm.setObjectName('returnForm')
        returnForm.resize(QtCore.QSize(QtCore.QRect(0, 0, 768, 983).size()).expandedTo(returnForm.minimumSizeHint()))
        returnForm.setAutoFillBackground(True)
        self.txt_return_label = QtGui.QLabel(returnForm)
        self.txt_return_label.setGeometry(QtCore.QRect(60, 40, 641, 50))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.txt_return_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setWeight(75)
        font.setBold(True)
        self.txt_return_label.setFont(font)
        self.txt_return_label.setObjectName('txt_return_label')
        self.txtbox_msg = QtGui.QLabel(returnForm)
        self.txtbox_msg.setGeometry(QtCore.QRect(90, 120, 591, 120))
        self.txtbox_msg2 = QtGui.QLabel(returnForm)
        self.txtbox_msg2.setGeometry(QtCore.QRect(84, 240, 600, 630))
        self.txtbox_msg2.setAlignment(QtCore.Qt.AlignTop)
        self.txtbox_msg2.setContentsMargins(5, 5, 5, 5)
        self.txtbox_msg2.setStyleSheet('border:1px solid red; border-radius: 5px; background:#f8f4cf; font: bold 30px; color: black; padding:5px; padding-left:65px; background-image:url(' + pic_info2 + '); background-repeat:no-repeat; background-position:top left;')
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.txtbox_msg.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setWeight(75)
        font.setBold(True)
        self.txtbox_msg.setFont(font)
        self.txtbox_msg.setScaledContents(False)
        self.txtbox_msg.setWordWrap(True)
        self.txtbox_msg.setObjectName('txtbox_msg')
        self.txtbox_msg2.setWordWrap(True)
        self.txtbox_msg2.setObjectName('txtbox_msg2')
        self.retranslateUi(returnForm)
        QtCore.QMetaObject.connectSlotsByName(returnForm)

    
    def retranslateUi(self, returnForm):
        self.txt_return_label.setText(QtGui.QApplication.translate('returnForm', 'Return Disc', None, QtGui.QApplication.UnicodeUTF8))
        self.txtbox_msg.setText(QtGui.QApplication.translate('returnForm', 'To ensure a completed transaction: \nPlease close the dvd case completely before inserting. ', None, QtGui.QApplication.UnicodeUTF8))
        self.txtbox_msg2.setText(QtGui.QApplication.translate('returnForm', 'Any open case can cause a jam and result in an incomplete rental.', None, QtGui.QApplication.UnicodeUTF8))


