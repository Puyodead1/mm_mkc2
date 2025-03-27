# Source Generated with Decompyle++
# File: kioskTesting_ui.pyc (Python 2.5)

from PyQt4 import QtCore, QtGui

class Ui_kioskTest(object):
    
    def setupUi(self, kioskTest):
        kioskTest.setObjectName('kioskTest')
        kioskTest.resize(QtCore.QSize(QtCore.QRect(0, 0, 768, 1024).size()).expandedTo(kioskTest.minimumSizeHint()))
        kioskTest.setMinimumSize(QtCore.QSize(768, 1024))
        kioskTest.setMaximumSize(QtCore.QSize(768, 1024))
        kioskTest.setAutoFillBackground(True)
        self.txt_config_label = QtGui.QLabel(kioskTest)
        self.txt_config_label.setGeometry(QtCore.QRect(50, 30, 411, 50))
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
        self.txt_config_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setWeight(75)
        font.setBold(True)
        self.txt_config_label.setFont(font)
        self.txt_config_label.setObjectName('txt_config_label')
        self.txt_msg = QtGui.QLabel(kioskTest)
        self.txt_msg.setGeometry(QtCore.QRect(100, 150, 568, 180))
        self.txt_msg.setWordWrap(True)
        self.txt_msg.setObjectName('txt_msg')
        self.retranslateUi(kioskTest)
        QtCore.QMetaObject.connectSlotsByName(kioskTest)

    
    def retranslateUi(self, kioskTest):
        self.txt_config_label.setText(QtGui.QApplication.translate('kioskTest', 'Kiosk Testing', None, QtGui.QApplication.UnicodeUTF8))


