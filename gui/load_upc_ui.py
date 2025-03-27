# Source Generated with Decompyle++
# File: load_upc_ui.pyc (Python 2.5)

from PyQt4 import QtCore, QtGui

class Ui_loadUPCForm(object):
    
    def setupUi(self, loadUPCForm):
        loadUPCForm.setObjectName('loadUPCForm')
        loadUPCForm.resize(QtCore.QSize(QtCore.QRect(0, 0, 768, 1024).size()).expandedTo(loadUPCForm.minimumSizeHint()))
        loadUPCForm.setMinimumSize(QtCore.QSize(768, 1024))
        loadUPCForm.setMaximumSize(QtCore.QSize(768, 1024))
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
        loadUPCForm.setPalette(palette)
        loadUPCForm.setWindowIcon(QtGui.QIcon('../../../../.designer/backup'))
        loadUPCForm.setAutoFillBackground(True)
        self.txt_load_label = QtGui.QLabel(loadUPCForm)
        self.txt_load_label.setGeometry(QtCore.QRect(50, 30, 411, 50))
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
        self.txt_load_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setWeight(75)
        font.setBold(True)
        self.txt_load_label.setFont(font)
        self.txt_load_label.setObjectName('txt_load_label')
        self.horizontalLayout = QtGui.QWidget(loadUPCForm)
        self.horizontalLayout.setGeometry(QtCore.QRect(40, 910, 691, 91))
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.hboxlayout = QtGui.QHBoxLayout(self.horizontalLayout)
        self.hboxlayout.setObjectName('hboxlayout')
        self.btn_cancel = QtGui.QPushButton(self.horizontalLayout)
        self.btn_cancel.setMinimumSize(QtCore.QSize(160, 68))
        self.btn_cancel.setMaximumSize(QtCore.QSize(160, 68))
        self.btn_cancel.setIconSize(QtCore.QSize(150, 55))
        self.btn_cancel.setObjectName('btn_cancel')
        self.hboxlayout.addWidget(self.btn_cancel)
        self.btn_back = QtGui.QPushButton(self.horizontalLayout)
        self.btn_back.setMinimumSize(QtCore.QSize(160, 68))
        self.btn_back.setMaximumSize(QtCore.QSize(160, 68))
        self.btn_back.setIconSize(QtCore.QSize(150, 55))
        self.btn_back.setObjectName('btn_back')
        self.hboxlayout.addWidget(self.btn_back)
        self.btn_logout = QtGui.QPushButton(loadUPCForm)
        self.btn_logout.setGeometry(QtCore.QRect(580, 20, 160, 68))
        self.btn_logout.setMinimumSize(QtCore.QSize(160, 68))
        self.btn_logout.setMaximumSize(QtCore.QSize(160, 68))
        self.btn_logout.setIconSize(QtCore.QSize(150, 55))
        self.btn_logout.setObjectName('btn_logout')
        self.txtbox_msg = QtGui.QLabel(loadUPCForm)
        self.txtbox_msg.setGeometry(QtCore.QRect(140, 240, 501, 38))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 96, 180))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 96, 180))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.txtbox_msg.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(75)
        font.setBold(True)
        self.txtbox_msg.setFont(font)
        self.txtbox_msg.setScaledContents(False)
        self.txtbox_msg.setAlignment(QtCore.Qt.AlignCenter)
        self.txtbox_msg.setObjectName('txtbox_msg')
        self.retranslateUi(loadUPCForm)
        QtCore.QMetaObject.connectSlotsByName(loadUPCForm)

    
    def retranslateUi(self, loadUPCForm):
        self.txt_load_label.setText(QtGui.QApplication.translate('loadUPCForm', 'Load', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_cancel.setStyleSheet(QtGui.QApplication.translate('loadUPCForm', 'color: white; font: bold italic 26px; border-style: outset; background-image: url(image/btn_back.png)', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_cancel.setText(QtGui.QApplication.translate('loadUPCForm', 'Cancel', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_back.setStyleSheet(QtGui.QApplication.translate('loadUPCForm', 'color: white; font: bold italic 26px; border-style: outset; background-image: url(image/btn_back.png)', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_back.setText(QtGui.QApplication.translate('loadUPCForm', 'Back', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_logout.setStyleSheet(QtGui.QApplication.translate('loadUPCForm', 'color: white; font: bold italic 26px; border-style: outset; background-image: url(image/btn_back.png)', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_logout.setText(QtGui.QApplication.translate('loadUPCForm', 'Exit', None, QtGui.QApplication.UnicodeUTF8))
        self.txtbox_msg.setText(QtGui.QApplication.translate('loadUPCForm', 'Please enter the UPC', None, QtGui.QApplication.UnicodeUTF8))


