# Source Generated with Decompyle++
# File: superAdminOffsetAdjForm.pyc (Python 2.5)

'''
SuperAdminOffsetAdjForm 
2009-07-29 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
from superAdminOffsetAdj_ui import Ui_superAdminOffsetAdjForm
import config
import component

class SuperAdminOffsetAdjForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_superAdminOffsetAdjForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_load)))
        self.setPalette(palette)
        self.ui.txt_process.hide()
        btnUpWidth = 81
        btnUpHeight = 71
        self.ui.btn_logout = component.btnLogout(self, 'SuperAdminOffsetAdjForm')
        self.ui.btn_logout.setGeometry(580, 20, 160, 68)
        self.ui.btn_cancel = component.btnCancel(self, 'SuperAdminOffsetAdjForm')
        self.ui.btn_cancel.setGeometry(QtCore.QRect(520, 930, 160, 68))
        self.ui.btn_up = component.ctrButton(self, 'SuperAdminOffsetAdjForm', 'btn_up', '', btnUpWidth, btnUpHeight, config.btnUpStyle)
        self.ui.btn_down = component.ctrButton(self, 'SuperAdminOffsetAdjForm', 'btn_down', '', btnUpWidth, btnUpHeight, config.btnDownStyle)
        self.ui.btn_try = component.ctrButton(self, 'SuperAdminOffsetAdjForm', 'btn_try', QtGui.QApplication.translate('Super', 'Try It', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnRedStyle)
        self.ui.btn_confirm = component.ctrButton(self, 'SuperAdminOffsetAdjForm', 'btn_confirm', QtGui.QApplication.translate('Super', 'Confirm Offset', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.ui.btn_finish = component.btnFinish(self, 'SuperAdminOffsetAdjForm')
        self.ui.btn_finish.hide()
        self.ui.hboxlayout.addWidget(self.ui.btn_try)
        self.ui.hboxlayout.addWidget(self.ui.btn_confirm)
        self.ui.hboxlayout.addWidget(self.ui.btn_finish)
        self.ui.hboxlayout1.addWidget(self.ui.btn_up)
        self.ui.hboxlayout1.addWidget(self.ui.btn_down)
        self.ui.ctr_group_settings = group(self)

    
    def showEvent(self, event):
        self.ui.retranslateUi(None)
        self.ui.btn_logout.reset()
        self.ui.btn_cancel.reset()
        self.ui.btn_finish.reset()
        self.ui.btn_try.setText(QtGui.QApplication.translate('Super', 'Try It', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_confirm.setText(QtGui.QApplication.translate('Super', 'Confirm Offset', None, QtGui.QApplication.UnicodeUTF8))



class group(SuperAdminOffsetAdjForm):
    
    def __init__(self, parent):
        self.parent = parent

    
    def show(self):
        self.parent.ui.txt_label.show()
        self.parent.ui.txt_title.show()
        self.parent.ui.txt_offset_label.show()
        self.parent.ui.txt_offset.show()
        self.parent.ui.txt_delta_label.show()
        self.parent.ui.txt_delta.show()
        self.parent.ui.txt_up_label.show()
        self.parent.ui.txt_down_label.show()
        self.parent.ui.btn_down.show()
        self.parent.ui.btn_up.show()
        self.parent.ui.btn_try.show()
        self.parent.ui.btn_confirm.show()

    
    def hide(self):
        self.parent.ui.txt_label.hide()
        self.parent.ui.txt_title.hide()
        self.parent.ui.txt_offset_label.hide()
        self.parent.ui.txt_offset.hide()
        self.parent.ui.txt_delta_label.hide()
        self.parent.ui.txt_delta.hide()
        self.parent.ui.txt_up_label.hide()
        self.parent.ui.txt_down_label.hide()
        self.parent.ui.btn_down.hide()
        self.parent.ui.btn_up.hide()
        self.parent.ui.btn_try.hide()
        self.parent.ui.btn_confirm.hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainf = SuperAdminOffsetAdjForm()
    mainf.show()
    sys.exit(app.exec_())

