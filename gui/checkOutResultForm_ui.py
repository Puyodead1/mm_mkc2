# Source Generated with Decompyle++
# File: checkOutResultForm_ui.pyc (Python 2.5)

from PyQt4 import QtCore, QtGui

class Ui_checkOutResultForm(object):
    
    def setupUi(self, checkOutResultForm):
        checkOutResultForm.setObjectName('checkOutResultForm')
        checkOutResultForm.resize(QtCore.QSize(QtCore.QRect(0, 0, 768, 1024).size()).expandedTo(checkOutResultForm.minimumSizeHint()))
        checkOutResultForm.setMinimumSize(QtCore.QSize(768, 1024))
        checkOutResultForm.setMaximumSize(QtCore.QSize(768, 1024))
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
        checkOutResultForm.setPalette(palette)
        checkOutResultForm.setWindowIcon(QtGui.QIcon('../../../../.designer/backup'))
        checkOutResultForm.setAutoFillBackground(True)
        self.txt_result_label = QtGui.QLabel(checkOutResultForm)
        self.txt_result_label.setGeometry(QtCore.QRect(50, 30, 411, 50))
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
        self.txt_result_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setWeight(75)
        font.setBold(True)
        self.txt_result_label.setFont(font)
        self.txt_result_label.setObjectName('txt_result_label')
        self.txt_taken = QtGui.QLabel(checkOutResultForm)
        self.txt_taken.setGeometry(QtCore.QRect(89, 130, 601, 181))
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
        self.txt_taken.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(20)
        font.setWeight(75)
        font.setBold(True)
        self.txt_taken.setFont(font)
        self.txt_taken.setScaledContents(False)
        self.txt_taken.setWordWrap(True)
        self.txt_taken.setObjectName('txt_taken')
        self.txt_thank1 = QtGui.QLabel(checkOutResultForm)
        self.txt_thank1.setGeometry(QtCore.QRect(90, 400, 601, 431))
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
        self.txt_thank1.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(20)
        font.setWeight(75)
        font.setBold(True)
        self.txt_thank1.setFont(font)
        self.txt_thank1.setScaledContents(False)
        self.txt_thank1.setWordWrap(True)
        self.txt_thank1.setObjectName('txt_thank1')
        self.txt_input_label = QtGui.QLabel(checkOutResultForm)
        self.txt_input_label.setGeometry(QtCore.QRect(40, 337, 691, 38))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(187, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(187, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.txt_input_label.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(20)
        font.setWeight(75)
        font.setBold(True)
        self.txt_input_label.setFont(font)
        self.txt_input_label.setScaledContents(False)
        self.txt_input_label.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_input_label.setWordWrap(True)
        self.txt_input_label.setObjectName('txt_input_label')
        self.txt_sale_price = QtGui.QLabel(checkOutResultForm)
        self.txt_sale_price.setGeometry(QtCore.QRect(90, 300, 601, 38))
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
        self.txt_sale_price.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(20)
        font.setWeight(75)
        font.setBold(True)
        self.txt_sale_price.setFont(font)
        self.txt_sale_price.setScaledContents(False)
        self.txt_sale_price.setWordWrap(True)
        self.txt_sale_price.setObjectName('txt_sale_price')
        self.retranslateUi(checkOutResultForm)
        QtCore.QMetaObject.connectSlotsByName(checkOutResultForm)

    
    def retranslateUi(self, checkOutResultForm):
        self.txt_result_label.setText(QtGui.QApplication.translate('checkOutResultForm', 'Result', None, QtGui.QApplication.UnicodeUTF8))
        self.txt_input_label.setText(QtGui.QApplication.translate('checkOutResultForm', 'Please enter your Email to get receipts.', None, QtGui.QApplication.UnicodeUTF8))


