# Source Generated with Decompyle++
# File: configForm_ui.pyc (Python 2.5)

from PyQt4 import QtCore, QtGui

class Ui_configForm(object):
    
    def setupUi(self, configForm):
        configForm.setObjectName('configForm')
        configForm.resize(QtCore.QSize(QtCore.QRect(0, 0, 768, 1024).size()).expandedTo(configForm.minimumSizeHint()))
        configForm.setMinimumSize(QtCore.QSize(768, 1024))
        configForm.setMaximumSize(QtCore.QSize(768, 1024))
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
        configForm.setPalette(palette)
        configForm.setWindowIcon(QtGui.QIcon('../../../../.designer/backup'))
        configForm.setAutoFillBackground(True)
        self.txt_config_label = QtGui.QLabel(configForm)
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
        self.gridLayout = QtGui.QWidget(configForm)
        self.gridLayout.setGeometry(QtCore.QRect(80, 140, 591, 181))
        self.gridLayout.setObjectName('gridLayout')
        self.gridlayout = QtGui.QGridLayout(self.gridLayout)
        self.gridlayout.setObjectName('gridlayout')
        self.retranslateUi(configForm)
        QtCore.QMetaObject.connectSlotsByName(configForm)

    
    def retranslateUi(self, configForm):
        self.txt_config_label.setText(QtGui.QApplication.translate('configForm', 'Config', None, QtGui.QApplication.UnicodeUTF8))


