# Source Generated with Decompyle++
# File: loadTakeInForm_ui.pyc (Python 2.5)

from PyQt4 import QtCore, QtGui

class Ui_loadTakeInForm(object):
    
    def setupUi(self, loadTakeInForm):
        loadTakeInForm.setObjectName('loadTakeInForm')
        loadTakeInForm.resize(QtCore.QSize(QtCore.QRect(0, 0, 768, 649).size()).expandedTo(loadTakeInForm.minimumSizeHint()))
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
        loadTakeInForm.setPalette(palette)
        loadTakeInForm.setWindowIcon(QtGui.QIcon('../../../../.designer/backup'))
        loadTakeInForm.setAutoFillBackground(True)
        self.txtbox_msg = QtGui.QLabel(loadTakeInForm)
        self.txtbox_msg.setGeometry(QtCore.QRect(30, 0, 711, 141))
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
        font.setFamily('Sans Serif')
        font.setPointSize(20)
        font.setWeight(75)
        font.setBold(True)
        self.txtbox_msg.setFont(font)
        self.txtbox_msg.setScaledContents(False)
        self.txtbox_msg.setAlignment(QtCore.Qt.AlignCenter)
        self.txtbox_msg.setWordWrap(True)
        self.txtbox_msg.setObjectName('txtbox_msg')
        self.retranslateUi(loadTakeInForm)
        QtCore.QMetaObject.connectSlotsByName(loadTakeInForm)

    
    def retranslateUi(self, loadTakeInForm):
        pass


