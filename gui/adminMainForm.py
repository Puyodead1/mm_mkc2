# Source Generated with Decompyle++
# File: adminMainForm.pyc (Python 2.5)

'''
AdminMainForm is the main window for admin.
2009-07-20 created by Mavis
'''
import os
import sys
import config
from component import messageBox, btnLogout, ctrButton
from PyQt4 import QtCore, QtGui
from admin_ui import Ui_adminForm
from squery import socketQuery

class AdminMainForm(QtGui.QMainWindow):
    
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_adminForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        self.palette = QtGui.QPalette()
        self.palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_admin)))
        self.setPalette(self.palette)
        self.sq = socketQuery()
        self.ui.btn_manually_return = ctrButton(self, 'AdminMainForm', 'btn_manually_return', 'Manually Return', 196, 60, config.btnBlueStyle)
        self.ui.btn_manually_return.setGeometry(50, 900, 196, 60)
        self.ui.btn_manually_return.setStyleSheet(config.btnBlueStyle)
        self.ui.btn_manually_return.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.btn_manage_slots = ctrButton(self, 'AdminMainForm', 'btn_manage_slots', 'Manage Slots', 196, 60, config.btnBlueStyle)
        self.ui.btn_manage_slots.setGeometry(260, 900, 196, 60)
        self.ui.btn_manage_slots.setStyleSheet(config.btnBlueStyle)
        self.ui.btn_manage_slots.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.btn_logout = btnLogout(self, 'AdminMainForm')
        self.ui.btn_logout.setGeometry(580, 20, 160, 68)
        btnStyle = 'text-align: bottom; border-style: outset; color: #bb0000; font: bold 18px; background-image: url('
        style2 = btnStyle + config.pic_admin_icon2 + ')'
        style3 = btnStyle + config.pic_admin_icon3 + ')'
        style4 = btnStyle + config.pic_admin_icon4 + ')'
        self.ui.btn_load_new_release = bigButton(self, 'AdminMainForm', 'btn_load_new_release')
        self.ui.btn_load_upc = bigButton(self, 'AdminMainForm', 'btn_load_upc')
        self.ui.btn_load_title = bigButton(self, 'AdminMainForm', 'btn_load_title')
        self.ui.btn_quick_load = bigButton(self, 'AdminMainForm', 'btn_quick_load')
        self.ui.btn_unload_mark = bigButton(self, 'AdminMainForm', 'btn_unload_mark', style2)
        self.ui.btn_unload_slot = bigButton(self, 'AdminMainForm', 'btn_unload_slot', style2)
        self.ui.btn_unload_title = bigButton(self, 'AdminMainForm', 'btn_unload_title', style2)
        self.ui.btn_information = bigButton(self, 'AdminMainForm', 'btn_information', style3)
        self.ui.btn_report = bigButton(self, 'AdminMainForm', 'btn_report', style3)
        self.ui.btn_config = bigButton(self, 'AdminMainForm', 'btn_config', style4)
        self.ui.btn_quick_load.hide()
        self.ui.hboxlayout1.addWidget(self.ui.btn_load_new_release)
        self.ui.hboxlayout1.addWidget(self.ui.btn_load_upc)
        self.ui.hboxlayout1.addWidget(self.ui.btn_load_title)
        self.ui.hboxlayout1.addWidget(self.ui.btn_quick_load)
        self.ui.hboxlayout.addWidget(self.ui.btn_unload_mark)
        self.ui.hboxlayout.addWidget(self.ui.btn_unload_slot)
        self.ui.hboxlayout.addWidget(self.ui.btn_unload_title)
        self.ui.hboxlayout2.addWidget(self.ui.btn_information)
        self.ui.hboxlayout2.addWidget(self.ui.btn_report)
        self.ui.hboxlayout2.addWidget(self.ui.btn_config)
        self.ui.AdminMainForm_ctr_message_box = messageBox('AdminMainForm', self)
        self.init()

    
    def manually_clicked(self):
        data = { }
        data['wid'] = 'AdminMainForm'
        data['cid'] = 'btn_manually_return'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        self.sq.send(data)

    
    def hideEvent(self, event):
        self.ui.AdminMainForm_ctr_message_box.hide()
        self.hide()

    
    def showEvent(self, event):
        self.init()
        self.ui.btn_logout.reset()
        self.ui.retranslateUi(None)
        self.palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_admin)))
        self.setPalette(self.palette)

    
    def init(self):
        self.ui.btn_load_new_release.setText(QtGui.QApplication.translate('adminForm', 'New Release', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_load_upc.setText(QtGui.QApplication.translate('adminForm', 'By UPC', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_load_title.setText(QtGui.QApplication.translate('adminForm', 'By Title', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_quick_load.setText(QtGui.QApplication.translate('adminForm', 'Quick Load', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_unload_mark.setText(QtGui.QApplication.translate('adminForm', 'Marked', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_unload_slot.setText(QtGui.QApplication.translate('adminForm', 'By Slot ID', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_unload_title.setText(QtGui.QApplication.translate('adminForm', 'By Title', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_information.setText(QtGui.QApplication.translate('adminForm', 'Information', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_report.setText(QtGui.QApplication.translate('adminForm', 'Report', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_config.setText(QtGui.QApplication.translate('adminForm', 'Config', None, QtGui.QApplication.UnicodeUTF8))



class bigButton(QtGui.QPushButton):
    
    def __init__(self, parent, wid, cid, style = 'text-align: bottom; border-style: outset; color: #bb0000; font: bold 18px; background-image: url(' + config.pic_admin_icon1 + ')'):
        QtGui.QPushButton.__init__(self, parent)
        self.wid = wid
        self.cid = cid
        self.setFixedSize(149, 103)
        self.setStyleSheet(style)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sq = socketQuery()

    
    def mouseReleaseEvent(self, event):
        data = { }
        data['wid'] = self.wid
        data['cid'] = self.cid
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        self.sq.send(data)
        self.setItalic(False)

    
    def mousePressEvent(self, event):
        self.setItalic(True)

    
    def setItalic(self, enable):
        font = self.font()
        font.setItalic(enable)
        if enable:
            font.setPixelSize(19)
        else:
            font.setPixelSize(18)
        self.setFont(font)
        self.update()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainf = AdminMainForm()
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf.show()
    sys.exit(app.exec_())

