# Source Generated with Decompyle++
# File: pickup_ui.pyc (Python 2.5)

from PyQt4 import QtCore, QtGui

class Ui_pickupForm(object):
    
    def setupUi(self, pickupForm):
        pickupForm.setObjectName('pickupForm')
        pickupForm.resize(QtCore.QSize(QtCore.QRect(0, 0, 768, 1024).size()).expandedTo(pickupForm.minimumSizeHint()))
        pickupForm.setMinimumSize(QtCore.QSize(768, 1024))
        pickupForm.setMaximumSize(QtCore.QSize(768, 1024))
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
        pickupForm.setPalette(palette)
        pickupForm.setWindowIcon(QtGui.QIcon('../../../../.designer/backup'))
        pickupForm.setAutoFillBackground(True)
        self.txt_pick_label = QtGui.QLabel(pickupForm)
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
        self.horizontalLayout = QtGui.QWidget(pickupForm)
        self.horizontalLayout.setGeometry(QtCore.QRect(40, 920, 691, 91))
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.hboxlayout = QtGui.QHBoxLayout(self.horizontalLayout)
        self.hboxlayout.setObjectName('hboxlayout')
        self.txtbox_msg = QtGui.QLabel(pickupForm)
        self.txtbox_msg.setGeometry(QtCore.QRect(90, 160, 571, 81))
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
        font.setPointSize(22)
        font.setWeight(75)
        font.setBold(True)
        self.txtbox_msg.setFont(font)
        self.txtbox_msg.setScaledContents(False)
        self.txtbox_msg.setWordWrap(True)
        self.txtbox_msg.setObjectName('txtbox_msg')
        self.swf_credit_cars = QtGui.QLabel(pickupForm)
        self.swf_credit_cars.setGeometry(QtCore.QRect(103, 280, 541, 101))
        self.swf_credit_cars.setObjectName('swf_credit_cars')
        self.retranslateUi(pickupForm)
        QtCore.QMetaObject.connectSlotsByName(pickupForm)

    
    def retranslateUi(self, pickupForm):
        self.txt_pick_label.setText(QtGui.QApplication.translate('pickupForm', 'Pick Up', None, QtGui.QApplication.UnicodeUTF8))
        self.txtbox_msg.setText(QtGui.QApplication.translate('pickupForm', 'Please swipe your credit card to take your DVD(s)', None, QtGui.QApplication.UnicodeUTF8))


