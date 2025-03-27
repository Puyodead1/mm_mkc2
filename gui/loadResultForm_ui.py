# Source Generated with Decompyle++
# File: loadResultForm_ui.pyc (Python 2.5)

from PyQt4 import QtCore, QtGui

class Ui_loadResultForm(object):
    
    def setupUi(self, loadResultForm):
        loadResultForm.setObjectName('loadResultForm')
        loadResultForm.resize(QtCore.QSize(QtCore.QRect(0, 0, 768, 649).size()).expandedTo(loadResultForm.minimumSizeHint()))
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
        loadResultForm.setPalette(palette)
        loadResultForm.setWindowIcon(QtGui.QIcon('../../../../.designer/backup'))
        loadResultForm.setAutoFillBackground(True)
        self.txtbox_msg = QtGui.QLabel(loadResultForm)
        self.txtbox_msg.setGeometry(QtCore.QRect(60, 9, 651, 271))
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
        font.setPointSize(22)
        font.setWeight(75)
        font.setBold(True)
        self.txtbox_msg.setFont(font)
        self.txtbox_msg.setScaledContents(False)
        self.txtbox_msg.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.txtbox_msg.setWordWrap(True)
        self.txtbox_msg.setObjectName('txtbox_msg')
        self.horizontalLayout = QtGui.QWidget(loadResultForm)
        self.horizontalLayout.setGeometry(QtCore.QRect(50, 530, 661, 101))
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.hboxlayout = QtGui.QHBoxLayout(self.horizontalLayout)
        self.hboxlayout.setObjectName('hboxlayout')
        self.retranslateUi(loadResultForm)
        QtCore.QMetaObject.connectSlotsByName(loadResultForm)

    
    def retranslateUi(self, loadResultForm):
        pass


