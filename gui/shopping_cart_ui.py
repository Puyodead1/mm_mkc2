# Source Generated with Decompyle++
# File: shopping_cart_ui.pyc (Python 2.5)

from PyQt4 import QtCore, QtGui

class Ui_shoppingCartForm(object):
    
    def setupUi(self, shoppingCartForm):
        shoppingCartForm.setObjectName('shoppingCartForm')
        shoppingCartForm.resize(QtCore.QSize(QtCore.QRect(0, 0, 768, 1024).size()).expandedTo(shoppingCartForm.minimumSizeHint()))
        shoppingCartForm.setMinimumSize(QtCore.QSize(768, 1024))
        shoppingCartForm.setMaximumSize(QtCore.QSize(768, 1024))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        shoppingCartForm.setPalette(palette)
        shoppingCartForm.setWindowIcon(QtGui.QIcon('../../../../.designer/backup'))
        shoppingCartForm.setAutoFillBackground(True)
        self.txt_cart_label = QtGui.QLabel(shoppingCartForm)
        self.txt_cart_label.setGeometry(QtCore.QRect(50, 30, 411, 50))
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
        self.txt_cart_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setWeight(75)
        font.setBold(True)
        self.txt_cart_label.setFont(font)
        self.txt_cart_label.setObjectName('txt_cart_label')
        self.horizontalLayout = QtGui.QWidget(shoppingCartForm)
        self.horizontalLayout.setGeometry(QtCore.QRect(40, 910, 691, 101))
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.hboxlayout = QtGui.QHBoxLayout(self.horizontalLayout)
        self.hboxlayout.setObjectName('hboxlayout')
        self.txt_cart_info_label = QtGui.QLabel(shoppingCartForm)
        self.txt_cart_info_label.setGeometry(QtCore.QRect(50, 120, 661, 81))
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
        self.txt_cart_info_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(75)
        font.setBold(True)
        self.txt_cart_info_label.setFont(font)
        self.txt_cart_info_label.setScaledContents(False)
        self.txt_cart_info_label.setWordWrap(True)
        self.txt_cart_info_label.setObjectName('txt_cart_info_label')
        self.retranslateUi(shoppingCartForm)
        QtCore.QMetaObject.connectSlotsByName(shoppingCartForm)

    
    def retranslateUi(self, shoppingCartForm):
        self.txt_cart_label.setText(QtGui.QApplication.translate('shoppingCartForm', 'Shopping Cart', None, QtGui.QApplication.UnicodeUTF8))
        self.txt_cart_info_label.setText(QtGui.QApplication.translate('shoppingCartForm', 'Shopping Cart Items', None, QtGui.QApplication.UnicodeUTF8))


