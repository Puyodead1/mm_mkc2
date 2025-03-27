# Source Generated with Decompyle++
# File: rent_ui.pyc (Python 2.5)

from PyQt4 import QtCore, QtGui

class Ui_RentMainForm(object):
    
    def setupUi(self, RentMainForm):
        RentMainForm.setObjectName('RentMainForm')
        RentMainForm.resize(QtCore.QSize(QtCore.QRect(0, 0, 768, 1024).size()).expandedTo(RentMainForm.minimumSizeHint()))
        RentMainForm.setMinimumSize(QtCore.QSize(768, 1024))
        RentMainForm.setMaximumSize(QtCore.QSize(768, 1024))
        RentMainForm.setAutoFillBackground(True)
        self.txt_rent_label = QtGui.QLabel(RentMainForm)
        self.txt_rent_label.setGeometry(QtCore.QRect(30, 15, 531, 60))
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
        self.txt_rent_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setWeight(75)
        font.setBold(True)
        self.txt_rent_label.setFont(font)
        self.txt_rent_label.setWordWrap(True)
        self.txt_rent_label.setObjectName('txt_rent_label')
        self.btn_icon_keyboard = QtGui.QPushButton(RentMainForm)
        self.btn_icon_keyboard.setGeometry(QtCore.QRect(20, 910, 161, 95))
        self.btn_icon_keyboard.setObjectName('btn_icon_keyboard')
        self.retranslateUi(RentMainForm)
        QtCore.QMetaObject.connectSlotsByName(RentMainForm)

    
    def retranslateUi(self, RentMainForm):
        pass


