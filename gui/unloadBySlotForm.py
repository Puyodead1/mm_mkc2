# Source Generated with Decompyle++
# File: unloadBySlotForm.pyc (Python 2.5)

'''
UnloadBySlotForm 
2009-07-26 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
from unloadBySlotForm_ui import Ui_unloadBySlotForm
import config
import component
from squery import socketQuery

class UnloadBySlotForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_unloadBySlotForm()
        self.ui.setupUi(self)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_load)))
        self.setPalette(palette)
        self.sq = socketQuery()
        self.ui.ctr_movie_list = component.MovieListAdmin(self)
        self.ui.ctr_movie_list.setGeometry(config.layout_x, config.unload_list_y, config.unload_list_width, config.unload_list_height)
        self.ui.btn_logout = component.btnLogout(self, 'UnloadBySlotForm')
        self.ui.btn_logout.setGeometry(580, 20, 160, 68)
        self.ui.btn_cancel = component.btnCancel(self, 'UnloadBySlotForm')
        self.ui.hboxlayout.addWidget(self.ui.btn_cancel)
        self.ui.btn_back = component.btnBack(self, 'UnloadBySlotForm')
        self.ui.hboxlayout.addWidget(self.ui.btn_back)
        self.ui.btn_icon_keyboard = component.ctrButton(self, 'UnloadBySlotForm', 'btn_icon_keyboard', QtGui.QApplication.translate('Form', 'Search by Slot ID', None, QtGui.QApplication.UnicodeUTF8), 161, 95, 'background-color: transparent; border-style: outset; font: bold 15px; color: #0060b4;')
        self.ui.btn_icon_keyboard.setGeometry(450, 780, 300, 66)
        self.ui.btn_icon_keyboard.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ui.btn_icon_keyboard.setIcon(QtGui.QIcon(config.pic_icon_keyboard))
        self.ui.btn_icon_keyboard.setIconSize(QtCore.QSize(127, 66))
        self.ui.UnloadBySlotForm_ctr_num_keyboard = component.numKeyboard('UnloadBySlotForm', self)
        self.ui.UnloadBySlotForm_ctr_message_box = component.messageBox('UnloadBySlotForm', self)
        QtCore.QObject.connect(self.ui.ctr_movie_list.table, QtCore.SIGNAL('cellClicked(int, int)'), self.unload)

    
    def hideEvent(self, event):
        self.ui.UnloadBySlotForm_ctr_message_box.hide()
        self.ui.UnloadBySlotForm_ctr_num_keyboard.close()
        self.hide()

    
    def showEvent(self, event):
        self.ui.retranslateUi(None)
        self.ui.btn_logout.reset()
        self.ui.btn_cancel.hide()
        self.ui.btn_back.reset()
        self.ui.btn_icon_keyboard.setText(QtGui.QApplication.translate('Form', 'Search by Slot ID', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_movie_list.reset()

    
    def unload(self, row, col):
        if col == 3:
            data = { }
            data['wid'] = 'UnloadBySlotForm'
            data['cid'] = 'ctr_movie_list'
            data['type'] = 'EVENT'
            data['EVENT'] = 'EVENT_MOUSE_CLICK'
            data['param_info'] = { }
            data['param_info']['ctr_movie_list'] = { }
            data['param_info']['ctr_movie_list']['slot_id'] = str(self.ui.ctr_movie_list.table.item(row, 0).text())
            rfid = self.ui.ctr_movie_list.table.item(row, 3).data(self.ui.ctr_movie_list.dataType).toString()
            data['param_info']['ctr_movie_list']['rfid'] = str(rfid)
            self.sq.send(data)
        elif col == 4:
            self.ui.ctr_movie_list.table.removeRow(row)
        


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainf = UnloadBySlotForm()
    if os.path.isfile(config.transDir + 'trans_sp.qm'):
        translate = QtCore.QTranslator()
        translate.load('trans_sp.qm', config.transDir)
        app.installTranslator(translate)
    
    data = {
        'ctr_movie_list': [
            {
                'price': '39.00',
                'rfid': '009FBD2730000104E0',
                'upc': '013131137491',
                'state': 'in',
                'slot_id': '101',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/36986.jpg',
                'movie_title': 'Jake Speed (1986)' },
            {
                'price': '39.00',
                'rfid': '00E9C42730000104E0',
                'upc': '013137800092',
                'state': 'in',
                'slot_id': '102',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/132343.jpg',
                'movie_title': 'Acolytes (2008)' }] }
    mainf.show()
    mainf.ui.ctr_movie_list.setMovieList(data)
    sys.exit(app.exec_())

