# Source Generated with Decompyle++
# File: showAllSlotForm.pyc (Python 2.5)

'''
UnloadBySlotForm 
2009-07-26 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
from showAllSlotForm_ui import Ui_showAllSlotForm
import config
import component
from squery import socketQuery

class ShowAllSlotForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.wid = self.__class__.__name__
        self.ui = Ui_showAllSlotForm()
        self.ui.setupUi(self)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_load)))
        self.setPalette(palette)
        self.sq = socketQuery()
        self.ui.all_slot_qtn = component.SlotsQtnBtn(self, self.wid)
        self.ui.all_slot_qtn.setGeometry(20, 130, 480, 50)
        self.ui.ctr_slot_list = component.AllSlotList(self, self.wid)
        self.ui.ctr_slot_list.setGeometry(config.layout_x, config.unload_list_y, config.unload_list_width, config.unload_list_height)
        self.ui.btn_logout = component.btnLogout(self, self.wid)
        self.ui.btn_logout.setGeometry(580, 20, 160, 68)
        self.ui.btn_cancel = component.btnCancel(self, self.wid)
        self.ui.hboxlayout.addWidget(self.ui.btn_cancel)
        self.ui.btn_back = component.btnBack(self, self.wid)
        self.ui.hboxlayout.addWidget(self.ui.btn_back)
        self.ui.btn_icon_keyboard = component.ctrButton(self, self.wid, 'btn_icon_keyboard', QtGui.QApplication.translate('Form', 'Search by Slot ID', None, QtGui.QApplication.UnicodeUTF8), 161, 95, 'background-color: transparent; border-style: outset; font: bold 15px; color: #0060b4;')
        self.ui.btn_icon_keyboard.setGeometry(450, 780, 300, 66)
        self.ui.btn_icon_keyboard.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ui.btn_icon_keyboard.setIcon(QtGui.QIcon(config.pic_icon_keyboard))
        self.ui.btn_icon_keyboard.setIconSize(QtCore.QSize(127, 66))
        self.ui.ShowAllSlotForm_ctr_num_keyboard = component.numKeyboard(self.wid, self)
        self.ui.ShowAllSlotForm_ctr_message_box = component.messageBox(self.wid, self)

    
    def hideEvent(self, event):
        self.ui.ShowAllSlotForm_ctr_message_box.hide()
        self.ui.ShowAllSlotForm_ctr_num_keyboard.close()
        self.hide()

    
    def showEvent(self, event):
        self.ui.retranslateUi(None)
        self.ui.btn_logout.reset()
        self.ui.btn_cancel.hide()
        self.ui.btn_back.reset()
        self.ui.btn_icon_keyboard.setText(QtGui.QApplication.translate('Form', 'Search by Slot ID', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainf = ShowAllSlotForm()
    if os.path.isfile(config.transDir + 'trans_sp.qm'):
        translate = QtCore.QTranslator()
        translate.load('trans_sp.qm', config.transDir)
        app.installTranslator(translate)
    
    data = {
        'ctr_slot_list': [
            {
                'slot_id': '102',
                'rfid': '',
                'status': 'in',
                'action_1': 'Mark as Bad',
                'action_2': 'Unload' },
            {
                'slot_id': '102',
                'rfid': '',
                'status': 'in',
                'action_1': 'Mark as Bad',
                'action_2': 'Unload' },
            {
                'slot_id': '102',
                'rfid': '',
                'status': 'in',
                'action_1': 'Mark as Bad',
                'action_2': 'Unload' },
            {
                'slot_id': '102',
                'rfid': '',
                'status': 'in',
                'action_1': 'Mark as Bad',
                'action_2': 'Unload' },
            {
                'slot_id': '102',
                'rfid': '',
                'status': 'in',
                'action_1': 'Mark as Bad',
                'action_2': 'Unload' },
            {
                'slot_id': '102',
                'rfid': '',
                'status': 'in',
                'action_1': 'Mark as Bad',
                'action_2': 'Unload' },
            {
                'slot_id': '102',
                'rfid': '',
                'status': 'bad rfid',
                'action_1': 'Mark as Bad',
                'action_2': 'Unload' },
            {
                'slot_id': '102',
                'rfid': '',
                'status': 'in',
                'action_1': 'Mark as Bad',
                'action_2': 'Unload' },
            {
                'slot_id': '102',
                'rfid': '',
                'status': 'in',
                'action_1': 'Mark as Bad',
                'action_2': 'Unload' },
            {
                'slot_id': '102',
                'rfid': '',
                'status': 'in',
                'action_1': 'Mark as Bad',
                'action_2': 'Unload' },
            {
                'slot_id': '102',
                'rfid': '',
                'status': 'in',
                'action_1': 'Mark as Bad',
                'action_2': 'Load' },
            {
                'slot_id': '103',
                'rfid': '',
                'status': 'bad empty slot',
                'action_1': '',
                'action_2': 'Clear' },
            {
                'slot_id': '102',
                'rfid': '',
                'status': 'in',
                'action_1': 'Mark as Bad',
                'action_2': 'Unload' },
            {
                'slot_id': '102',
                'rfid': '',
                'status': 'in',
                'action_1': 'Mark as Bad',
                'action_2': 'Unload' }] }
    mainf.ui.ctr_slot_list.setSlotList(data)
    mainf.ui.all_slot_qtn.set_label_text({
        'text': {
            'all': 99,
            'bad': 56,
            'empty': 56 } })
    mainf.show()
    sys.exit(app.exec_())

