# Source Generated with Decompyle++
# File: pickupResultForm_ui.pyc (Python 2.5)

from PyQt4 import QtCore, QtGui

class Ui_pickupResultForm(object):
    
    def setupUi(self, pickupResultForm):
        pickupResultForm.setObjectName('pickupResultForm')
        pickupResultForm.resize(QtCore.QSize(QtCore.QRect(0, 0, 768, 1024).size()).expandedTo(pickupResultForm.minimumSizeHint()))
        pickupResultForm.setMinimumSize(QtCore.QSize(768, 1024))
        pickupResultForm.setMaximumSize(QtCore.QSize(768, 1024))
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
        pickupResultForm.setPalette(palette)
        pickupResultForm.setWindowIcon(QtGui.QIcon('../../../../.designer/backup'))
        pickupResultForm.setAutoFillBackground(True)
        self.txt_pick_label = QtGui.QLabel(pickupResultForm)
        self.txt_pick_label.setGeometry(QtCore.QRect(50, 30, 411, 50))
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
        self.txt_pick_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setWeight(75)
        font.setBold(True)
        self.txt_pick_label.setFont(font)
        self.txt_pick_label.setObjectName('txt_pick_label')
        self.txtbox_msg = QtGui.QLabel(pickupResultForm)
        self.txtbox_msg.setGeometry(QtCore.QRect(90, 115, 601, 261))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 102, 51))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 102, 51))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.txtbox_msg.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(24)
        font.setWeight(75)
        font.setBold(True)
        self.txtbox_msg.setFont(font)
        self.txtbox_msg.setScaledContents(False)
        self.txtbox_msg.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft)
        self.txtbox_msg.setWordWrap(True)
        self.txtbox_msg.setObjectName('txtbox_msg')
        self.txtbox_msg_2 = QtGui.QLabel(pickupResultForm)
        self.txtbox_msg_2.setGeometry(QtCore.QRect(140, 390, 561, 51))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 102, 51))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 102, 51))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.txtbox_msg_2.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(24)
        font.setWeight(75)
        font.setBold(True)
        self.txtbox_msg_2.setFont(font)
        self.txtbox_msg_2.setScaledContents(False)
        self.txtbox_msg_2.setWordWrap(True)
        self.txtbox_msg_2.setObjectName('txtbox_msg_2')
        self.txt_taken = QtGui.QLabel(pickupResultForm)
        self.txt_taken.setGeometry(QtCore.QRect(90, 390, 51, 51))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 102, 51))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 102, 51))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.txt_taken.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(24)
        font.setWeight(75)
        font.setBold(True)
        self.txt_taken.setFont(font)
        self.txt_taken.setScaledContents(False)
        self.txt_taken.setWordWrap(True)
        self.txt_taken.setObjectName('txt_taken')
        self.txtbox_msg2 = QtGui.QLabel(pickupResultForm)
        self.txtbox_msg2.setGeometry(QtCore.QRect(90, 450, 591, 51))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 102, 51))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 102, 51))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.txtbox_msg2.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(24)
        font.setWeight(75)
        font.setBold(True)
        self.txtbox_msg2.setFont(font)
        self.txtbox_msg2.setScaledContents(False)
        self.txtbox_msg2.setWordWrap(True)
        self.txtbox_msg2.setObjectName('txtbox_msg2')
        self.txtbox_enjoy = QtGui.QLabel(pickupResultForm)
        self.txtbox_enjoy.setGeometry(QtCore.QRect(90, 510, 591, 51))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 102, 51))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 102, 51))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.txtbox_enjoy.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(24)
        font.setWeight(75)
        font.setBold(True)
        self.txtbox_enjoy.setFont(font)
        self.txtbox_enjoy.setScaledContents(False)
        self.txtbox_enjoy.setWordWrap(True)
        self.txtbox_enjoy.setObjectName('txtbox_enjoy')
        self.horizontalLayout = QtGui.QWidget(pickupResultForm)
        self.horizontalLayout.setGeometry(QtCore.QRect(30, 910, 711, 101))
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.hboxlayout = QtGui.QHBoxLayout(self.horizontalLayout)
        self.hboxlayout.setObjectName('hboxlayout')
        self.retranslateUi(pickupResultForm)
        QtCore.QMetaObject.connectSlotsByName(pickupResultForm)

    
    def retranslateUi(self, pickupResultForm):
        self.txt_pick_label.setText(QtGui.QApplication.translate('pickupResultForm', 'Pick Up', None, QtGui.QApplication.UnicodeUTF8))
        self.txtbox_msg.setText(QtGui.QApplication.translate('pickupResultForm', 'Your transaction is done.', None, QtGui.QApplication.UnicodeUTF8))
        self.txtbox_msg_2.setText(QtGui.QApplication.translate('pickupResultForm', 'Disc(s) have been taken out.', None, QtGui.QApplication.UnicodeUTF8))
        self.txt_taken.setText(QtGui.QApplication.translate('pickupResultForm', '2', None, QtGui.QApplication.UnicodeUTF8))
        self.txtbox_msg2.setText(QtGui.QApplication.translate('pickupResultForm', 'Thank you!', None, QtGui.QApplication.UnicodeUTF8))
        self.txtbox_enjoy.setText(QtGui.QApplication.translate('pickupResultForm', 'Enjoy!', None, QtGui.QApplication.UnicodeUTF8))


