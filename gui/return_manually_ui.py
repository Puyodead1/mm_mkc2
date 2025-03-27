# Source Generated with Decompyle++
# File: return_manually_ui.pyc (Python 2.5)

from PyQt4 import QtCore, QtGui
from config import pic_info2

class Ui_return_manually_Form(object):
    
    def setupUi(self, return_manually_Form):
        return_manually_Form.setObjectName('returnManuallyForm')
        return_manually_Form.resize(QtCore.QSize(QtCore.QRect(0, 0, 768, 983).size()).expandedTo(return_manually_Form.minimumSizeHint()))
        return_manually_Form.setAutoFillBackground(True)
        self.txt_return_label = QtGui.QLabel(return_manually_Form)
        self.txt_return_label.setGeometry(QtCore.QRect(60, 40, 641, 50))
        self.frame = QtGui.QFrame(return_manually_Form)
        self.frame.setGeometry(QtCore.QRect(50, 170, 661, 260))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setObjectName('frame')
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
        self.txtbox_msg = QtGui.QLabel(return_manually_Form)
        self.txtbox_msg.setMaximumSize(591, 208)
        self.txtbox_msg.setWordWrap(True)
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
        self.retranslateUi(return_manually_Form)
        QtCore.QMetaObject.connectSlotsByName(return_manually_Form)

    
    def retranslateUi(self, return_manually_Form):
        self.txt_return_label.setText(QtGui.QApplication.translate('return_manually_Form', 'Manually Return', None, QtGui.QApplication.UnicodeUTF8))


