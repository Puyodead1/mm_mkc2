# Source Generated with Decompyle++
# File: registerSwipeCardForm_ui.pyc (Python 2.5)

from PyQt4 import QtCore, QtGui

class Ui_registerCrerepayCardForm(object):
    
    def setupUi(self, registerCerepayCardForm):
        registerCerepayCardForm.setObjectName('registerCerepayCardForm')
        registerCerepayCardForm.resize(QtCore.QSize(QtCore.QRect(0, 0, 768, 1024).size()).expandedTo(registerCerepayCardForm.minimumSizeHint()))
        registerCerepayCardForm.setMinimumSize(QtCore.QSize(768, 1024))
        registerCerepayCardForm.setMaximumSize(QtCore.QSize(768, 1024))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        registerCerepayCardForm.setPalette(palette)
        registerCerepayCardForm.setAutoFillBackground(True)
        self.txtbox_msg = QtGui.QLabel(registerCerepayCardForm)
        self.txtbox_msg.setGeometry(QtCore.QRect(90, 160, 571, 71))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.txtbox_msg.setPalette(palette)
        self.txt_card_label = QtGui.QLabel(registerCerepayCardForm)
        self.txt_card_label.setGeometry(QtCore.QRect(50, 30, 520, 50))
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
        self.txt_card_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.txtbox_msg.setFont(font)
        self.txtbox_msg.setObjectName('txtbox_msg')
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setWeight(75)
        font.setBold(True)
        self.txt_card_label.setFont(font)
        self.txt_card_label.setObjectName('txt_card_label')
        self.swf_credit_cars = QtGui.QLabel(registerCerepayCardForm)
        self.swf_credit_cars.setGeometry(QtCore.QRect(103, 260, 541, 101))
        self.swf_credit_cars.setObjectName('swf_credit_cars')
        self.horizontalLayout = QtGui.QWidget(registerCerepayCardForm)
        self.horizontalLayout.setGeometry(QtCore.QRect(50, 920, 671, 91))
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.hboxlayout = QtGui.QHBoxLayout(self.horizontalLayout)
        self.hboxlayout.setObjectName('hboxlayout')
        self.retranslateUi(registerCerepayCardForm)
        QtCore.QMetaObject.connectSlotsByName(registerCerepayCardForm)

    
    def retranslateUi(self, registerCerepayCardForm):
        self.txt_card_label.setText(QtGui.QApplication.translate('registerCerepayCardForm', 'Membership Card Registration', None, QtGui.QApplication.UnicodeUTF8))
        self.txtbox_msg.setText(QtGui.QApplication.translate('registerCerepayCardForm', 'Please swipe your cerepay card', None, QtGui.QApplication.UnicodeUTF8))


