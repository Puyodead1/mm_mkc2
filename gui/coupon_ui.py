# Source Generated with Decompyle++
# File: coupon_ui.pyc (Python 2.5)

from PyQt4 import QtCore, QtGui

class Ui_couponForm(object):
    
    def setupUi(self, couponForm):
        couponForm.setObjectName('couponForm')
        couponForm.resize(QtCore.QSize(QtCore.QRect(0, 0, 768, 1024).size()).expandedTo(couponForm.minimumSizeHint()))
        couponForm.setMinimumSize(QtCore.QSize(768, 1024))
        couponForm.setMaximumSize(QtCore.QSize(768, 1024))
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
        couponForm.setPalette(palette)
        couponForm.setWindowIcon(QtGui.QIcon('../../../../.designer/backup'))
        couponForm.setAutoFillBackground(True)
        self.txt_rent_label = QtGui.QLabel(couponForm)
        self.txt_rent_label.setGeometry(QtCore.QRect(50, 30, 411, 50))
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
        font.setPointSize(26)
        font.setWeight(75)
        font.setBold(True)
        self.txt_rent_label.setFont(font)
        self.txt_rent_label.setObjectName('txt_rent_label')
        self.horizontalLayout = QtGui.QWidget(couponForm)
        self.horizontalLayout.setGeometry(QtCore.QRect(40, 910, 691, 71))
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.hboxlayout = QtGui.QHBoxLayout(self.horizontalLayout)
        self.hboxlayout.setObjectName('hboxlayout')
        self.btn_cancel = QtGui.QPushButton(self.horizontalLayout)
        self.btn_cancel.setMinimumSize(QtCore.QSize(160, 68))
        self.btn_cancel.setMaximumSize(QtCore.QSize(160, 68))
        self.btn_cancel.setIconSize(QtCore.QSize(150, 55))
        self.btn_cancel.setObjectName('btn_cancel')
        self.hboxlayout.addWidget(self.btn_cancel)
        self.btn_ok = QtGui.QPushButton(self.horizontalLayout)
        self.btn_ok.setMinimumSize(QtCore.QSize(160, 68))
        self.btn_ok.setMaximumSize(QtCore.QSize(160, 68))
        self.btn_ok.setIconSize(QtCore.QSize(150, 55))
        self.btn_ok.setObjectName('btn_ok')
        self.hboxlayout.addWidget(self.btn_ok)
        self.btn_back = QtGui.QPushButton(couponForm)
        self.btn_back.setGeometry(QtCore.QRect(580, 20, 160, 68))
        self.btn_back.setMinimumSize(QtCore.QSize(160, 68))
        self.btn_back.setMaximumSize(QtCore.QSize(160, 68))
        self.btn_back.setIconSize(QtCore.QSize(150, 55))
        self.btn_back.setObjectName('btn_back')
        self.label = QtGui.QLabel(couponForm)
        self.label.setGeometry(QtCore.QRect(50, 110, 661, 38))
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
        self.label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setScaledContents(False)
        self.label.setObjectName('label')
        self.gridLayout = QtGui.QWidget(couponForm)
        self.gridLayout.setGeometry(QtCore.QRect(50, 170, 671, 611))
        self.gridLayout.setObjectName('gridLayout')
        self.gridlayout = QtGui.QGridLayout(self.gridLayout)
        self.gridlayout.setObjectName('gridlayout')
        self.coupon_info = QtGui.QTableWidget(self.gridLayout)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.coupon_info.setFont(font)
        self.coupon_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.coupon_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.coupon_info.setIconSize(QtCore.QSize(50, 70))
        self.coupon_info.setGridStyle(QtCore.Qt.DashDotLine)
        self.coupon_info.setCornerButtonEnabled(False)
        self.coupon_info.setObjectName('coupon_info')
        self.gridlayout.addWidget(self.coupon_info, 0, 0, 1, 4)
        self.btn_add = QtGui.QPushButton(self.gridLayout)
        self.btn_add.setMinimumSize(QtCore.QSize(170, 55))
        self.btn_add.setMaximumSize(QtCore.QSize(170, 55))
        self.btn_add.setIconSize(QtCore.QSize(150, 55))
        self.btn_add.setObjectName('btn_add')
        self.gridlayout.addWidget(self.btn_add, 1, 3, 1, 1)
        self.retranslateUi(couponForm)
        QtCore.QMetaObject.connectSlotsByName(couponForm)

    
    def retranslateUi(self, couponForm):
        self.txt_rent_label.setText(QtGui.QApplication.translate('couponForm', 'Coupon Settings', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_cancel.setStyleSheet(QtGui.QApplication.translate('couponForm', 'color: white; font: bold italic 26px; border-style: outset; background-image: url(image/btn_back.png)', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_cancel.setText(QtGui.QApplication.translate('couponForm', 'Cancel', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_ok.setStyleSheet(QtGui.QApplication.translate('couponForm', 'color: white; font: bold italic 26px; border-style: outset; background-image: url(image/btn_back.png)', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_ok.setText(QtGui.QApplication.translate('couponForm', 'Ok', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_back.setStyleSheet(QtGui.QApplication.translate('couponForm', 'color: white; font: bold italic 26px; border-style: outset; background-image: url(image/btn_back.png)', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_back.setText(QtGui.QApplication.translate('couponForm', 'Back', None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate('couponForm', 'Coupon List Of Your Shopping Cart', None, QtGui.QApplication.UnicodeUTF8))
        self.coupon_info.clear()
        self.coupon_info.setColumnCount(4)
        self.coupon_info.setRowCount(0)
        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText(QtGui.QApplication.translate('couponForm', 'Coupon code', None, QtGui.QApplication.UnicodeUTF8))
        self.coupon_info.setHorizontalHeaderItem(0, headerItem)
        headerItem1 = QtGui.QTableWidgetItem()
        headerItem1.setText(QtGui.QApplication.translate('couponForm', 'Description', None, QtGui.QApplication.UnicodeUTF8))
        self.coupon_info.setHorizontalHeaderItem(1, headerItem1)
        headerItem2 = QtGui.QTableWidgetItem()
        headerItem2.setText(QtGui.QApplication.translate('couponForm', 'Apply to', None, QtGui.QApplication.UnicodeUTF8))
        self.coupon_info.setHorizontalHeaderItem(2, headerItem2)
        headerItem3 = QtGui.QTableWidgetItem()
        headerItem3.setText(QtGui.QApplication.translate('couponForm', 'Cancel', None, QtGui.QApplication.UnicodeUTF8))
        self.coupon_info.setHorizontalHeaderItem(3, headerItem3)
        self.btn_add.setStyleSheet(QtGui.QApplication.translate('couponForm', 'color: white; background-color: blue;border-radius: 8px; font: bold italic 26px; border-style: outset; border-width: 2px; border-color: white', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_add.setText(QtGui.QApplication.translate('couponForm', '+Add', None, QtGui.QApplication.UnicodeUTF8))


