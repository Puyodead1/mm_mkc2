# Source Generated with Decompyle++
# File: superAdminMainForm.pyc (Python 2.5)

'''
SuperAdminMainForm 
2009-07-29 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
from configForm_ui import Ui_configForm
import config
import component

class SuperAdminMainForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_configForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_config)))
        self.setPalette(palette)
        self.ui.txt_config_label.setText(QtGui.QApplication.translate('Form', 'Super Admin', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_logout = component.btnLogout(self, 'SuperAdminMainForm')
        self.ui.btn_logout.setGeometry(580, 20, 160, 68)
        self.ui.btn_test = component.ctrButton(self, 'SuperAdminMainForm', 'btn_test', QtGui.QApplication.translate('Super', 'Self Test', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.ui.btn_offset_adj = component.ctrButton(self, 'SuperAdminMainForm', 'btn_offset_adj', QtGui.QApplication.translate('Super', 'Offset\nAdjustment', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.ui.btn_distance1 = component.ctrButton(self, 'SuperAdminMainForm', 'btn_distance1', QtGui.QApplication.translate('Super', 'Distance1', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.ui.btn_distance2 = component.ctrButton(self, 'SuperAdminMainForm', 'btn_distance2', QtGui.QApplication.translate('Super', 'Distance2', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.ui.gridLayout.setGeometry(QtCore.QRect(config.layout_x, config.layout_y, config.layout_width, config.layout_height + 20))
        self.ui.gridlayout.addWidget(self.ui.btn_test, 0, 0)
        self.ui.gridlayout.addWidget(self.ui.btn_offset_adj, 0, 1)
        self.ui.gridlayout.addWidget(self.ui.btn_distance1, 0, 2)
        self.ui.gridlayout.addWidget(self.ui.btn_distance2, 1, 0)

    
    def showEvent(self, event):
        self.ui.txt_config_label.setText(QtGui.QApplication.translate('Form', 'Super Admin', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_logout.reset()
        self.ui.btn_test.setText(QtGui.QApplication.translate('Super', 'Self Test', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_offset_adj.setText(QtGui.QApplication.translate('Super', 'Offset\nAdjustment', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_distance1.setText(QtGui.QApplication.translate('Super', 'Distance1', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_distance2.setText(QtGui.QApplication.translate('Super', 'Distance2', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainf = SuperAdminMainForm()
    mainf.show()
    sys.exit(app.exec_())

