# Source Generated with Decompyle++
# File: checkOutEjectForm_ui.pyc (Python 2.5)

from PyQt4 import QtCore, QtGui

class Ui_checkOutEjectForm(object):
    
    def setupUi(self, checkOutEjectForm):
        checkOutEjectForm.setObjectName('checkOutEjectForm')
        checkOutEjectForm.resize(QtCore.QSize(QtCore.QRect(0, 0, 768, 1024).size()).expandedTo(checkOutEjectForm.minimumSizeHint()))
        checkOutEjectForm.setMinimumSize(QtCore.QSize(768, 1024))
        checkOutEjectForm.setMaximumSize(QtCore.QSize(768, 1024))
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
        checkOutEjectForm.setPalette(palette)
        checkOutEjectForm.setAutoFillBackground(True)
        self.txt_label = QtGui.QLabel(checkOutEjectForm)
        self.txt_label.setGeometry(QtCore.QRect(50, 30, 411, 50))
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
        self.txt_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setWeight(75)
        font.setBold(True)
        self.txt_label.setFont(font)
        self.txt_label.setObjectName('txt_label')
        self.verticalLayout = QtGui.QWidget(checkOutEjectForm)
        self.verticalLayout.setGeometry(QtCore.QRect(80, 120, 611, 241))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.verticalLayout.setFont(font)
        self.verticalLayout.setObjectName('verticalLayout')
        self.vboxlayout = QtGui.QVBoxLayout(self.verticalLayout)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setObjectName('vboxlayout')
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName('hboxlayout')
        self.txtbox_msg_11 = QtGui.QLabel(self.verticalLayout)
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
        self.txtbox_msg_11.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(22)
        font.setWeight(75)
        font.setBold(True)
        self.txtbox_msg_11.setFont(font)
        self.txtbox_msg_11.setScaledContents(False)
        self.txtbox_msg_11.setWordWrap(True)
        self.txtbox_msg_11.setObjectName('txtbox_msg_11')
        self.hboxlayout.addWidget(self.txtbox_msg_11)
        self.txt_total = QtGui.QLabel(self.verticalLayout)
        self.txt_total.setMaximumSize(QtCore.QSize(50, 16777215))
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
        self.txt_total.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(22)
        font.setWeight(75)
        font.setBold(True)
        self.txt_total.setFont(font)
        self.txt_total.setScaledContents(False)
        self.txt_total.setWordWrap(True)
        self.txt_total.setObjectName('txt_total')
        self.hboxlayout.addWidget(self.txt_total)
        self.txtbox_msg_3 = QtGui.QLabel(self.verticalLayout)
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
        self.txtbox_msg_3.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(22)
        font.setWeight(75)
        font.setBold(True)
        self.txtbox_msg_3.setFont(font)
        self.txtbox_msg_3.setScaledContents(False)
        self.txtbox_msg_3.setWordWrap(True)
        self.txtbox_msg_3.setObjectName('txtbox_msg_3')
        self.hboxlayout.addWidget(self.txtbox_msg_3)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName('hboxlayout1')
        self.txtbox_msg_4 = QtGui.QLabel(self.verticalLayout)
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
        self.txtbox_msg_4.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(22)
        font.setWeight(75)
        font.setBold(True)
        self.txtbox_msg_4.setFont(font)
        self.txtbox_msg_4.setScaledContents(False)
        self.txtbox_msg_4.setWordWrap(True)
        self.txtbox_msg_4.setObjectName('txtbox_msg_4')
        self.hboxlayout1.addWidget(self.txtbox_msg_4)
        self.txt_taked = QtGui.QLabel(self.verticalLayout)
        self.txt_taked.setMaximumSize(QtCore.QSize(50, 16777215))
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
        self.txt_taked.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(22)
        font.setWeight(75)
        font.setBold(True)
        self.txt_taked.setFont(font)
        self.txt_taked.setScaledContents(False)
        self.txt_taked.setWordWrap(True)
        self.txt_taked.setObjectName('txt_taked')
        self.hboxlayout1.addWidget(self.txt_taked)
        self.txtbox_msg_6 = QtGui.QLabel(self.verticalLayout)
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
        self.txtbox_msg_6.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(22)
        font.setWeight(75)
        font.setBold(True)
        self.txtbox_msg_6.setFont(font)
        self.txtbox_msg_6.setScaledContents(False)
        self.txtbox_msg_6.setWordWrap(True)
        self.txtbox_msg_6.setObjectName('txtbox_msg_6')
        self.hboxlayout1.addWidget(self.txtbox_msg_6)
        self.vboxlayout.addLayout(self.hboxlayout1)
        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName('hboxlayout2')
        self.txt_processing = QtGui.QLabel(self.verticalLayout)
        self.txt_processing.setMaximumSize(QtCore.QSize(50, 16777215))
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
        self.txt_processing.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(22)
        font.setWeight(75)
        font.setBold(True)
        self.txt_processing.setFont(font)
        self.txt_processing.setScaledContents(False)
        self.txt_processing.setWordWrap(True)
        self.txt_processing.setObjectName('txt_processing')
        self.hboxlayout2.addWidget(self.txt_processing)
        self.txtbox_msg_7 = QtGui.QLabel(self.verticalLayout)
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
        self.txtbox_msg_7.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(22)
        font.setWeight(75)
        font.setBold(True)
        self.txtbox_msg_7.setFont(font)
        self.txtbox_msg_7.setScaledContents(False)
        self.txtbox_msg_7.setWordWrap(True)
        self.txtbox_msg_7.setObjectName('txtbox_msg_7')
        self.hboxlayout2.addWidget(self.txtbox_msg_7)
        self.vboxlayout.addLayout(self.hboxlayout2)
        self.txtbox_msg = QtGui.QLabel(self.verticalLayout)
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
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(22)
        font.setWeight(75)
        font.setBold(True)
        self.txtbox_msg.setFont(font)
        self.txtbox_msg.setScaledContents(False)
        self.txtbox_msg.setWordWrap(True)
        self.txtbox_msg.setObjectName('txtbox_msg')
        self.vboxlayout.addWidget(self.txtbox_msg)
        self.retranslateUi(checkOutEjectForm)
        QtCore.QMetaObject.connectSlotsByName(checkOutEjectForm)

    
    def retranslateUi(self, checkOutEjectForm):
        self.txt_label.setText(QtGui.QApplication.translate('checkOutEjectForm', 'Result', None, QtGui.QApplication.UnicodeUTF8))
        self.txtbox_msg_11.setText(QtGui.QApplication.translate('checkOutEjectForm', 'Total:', None, QtGui.QApplication.UnicodeUTF8))
        self.txt_total.setText(QtGui.QApplication.translate('checkOutEjectForm', '1', None, QtGui.QApplication.UnicodeUTF8))
        self.txtbox_msg_3.setText(QtGui.QApplication.translate('checkOutEjectForm', 'Disc(s)', None, QtGui.QApplication.UnicodeUTF8))
        self.txtbox_msg_4.setText(QtGui.QApplication.translate('checkOutEjectForm', 'You have taken ', None, QtGui.QApplication.UnicodeUTF8))
        self.txt_taked.setText(QtGui.QApplication.translate('checkOutEjectForm', '1', None, QtGui.QApplication.UnicodeUTF8))
        self.txtbox_msg_6.setText(QtGui.QApplication.translate('checkOutEjectForm', 'Disc(s)', None, QtGui.QApplication.UnicodeUTF8))
        self.txt_processing.setText(QtGui.QApplication.translate('checkOutEjectForm', '1', None, QtGui.QApplication.UnicodeUTF8))
        self.txtbox_msg_7.setText(QtGui.QApplication.translate('checkOutEjectForm', 'Disc(s) is processing', None, QtGui.QApplication.UnicodeUTF8))
        self.txtbox_msg.setText(QtGui.QApplication.translate('checkOutEjectForm', 'Please wait for next one', None, QtGui.QApplication.UnicodeUTF8))


