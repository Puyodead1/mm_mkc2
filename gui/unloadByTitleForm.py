# Source Generated with Decompyle++
# File: unloadByTitleForm.pyc (Python 2.5)

'''
LoadResultForm 
2009-07-26 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
from unloadByTitleForm_ui import Ui_unloadByTitleForm
import config
import component
from squery import socketQuery

class UnloadByTitleForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_unloadByTitleForm()
        self.ui.setupUi(self)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_load)))
        self.setPalette(palette)
        self.sq = socketQuery()
        self.ui.ctr_movie_list = component.MovieListAdmin(self, 1)
        self.ui.ctr_movie_list.setGeometry(config.layout_x, config.unload_list_y, config.unload_list_width, config.unload_list_height)
        self.ui.btn_logout = component.btnLogout(self, 'UnloadByTitleForm')
        self.ui.btn_logout.setGeometry(580, 20, 160, 68)
        self.ui.btn_cancel = component.btnBack(self, 'UnloadByTitleForm')
        self.ui.hboxlayout.addWidget(self.ui.btn_cancel)
        self.ui.btn_unload_all = component.ctrButton(self, 'UnloadByTitleForm', 'btn_unload_all', QtGui.QApplication.translate('UnloadByTitleForm', 'Unload All', None, QtGui.QApplication.UnicodeUTF8), 159, 68, 'color: white; font: bold italic 26px; border-style: outset; background-image: url(' + config.pic_btn_green + ')')
        self.ui.btn_unload_all.hide()
        self.ui.hboxlayout.addWidget(self.ui.btn_unload_all)
        self.ui.btn_icon_keyboard = component.ctrButton(self, 'UnloadByTitleForm', 'btn_icon_keyboard', QtGui.QApplication.translate('Form', 'Search by Title', None, QtGui.QApplication.UnicodeUTF8), 161, 95, 'background-color: transparent; border-style: outset; font: bold 15px; color: #0060b4;')
        self.ui.btn_icon_keyboard.setGeometry(460, 800, 270, 66)
        self.ui.btn_icon_keyboard.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ui.btn_icon_keyboard.setIcon(QtGui.QIcon(config.pic_icon_keyboard))
        self.ui.btn_icon_keyboard.setIconSize(QtCore.QSize(127, 66))
        self.ui.UnloadByTitleForm_ctr_all_keyboard = component.allKeyboard('UnloadByTitleForm', self)
        self.ui.UnloadByTitleForm_ctr_all_keyboard.setGeometry((768 - config.kb_all_width) / 2, (1024 - config.kb_all_height) / 2, config.kb_all_width, config.kb_all_height)
        self.ui.UnloadByTitleForm_ctr_all_keyboard.hide()
        self.ui.UnloadByTitleForm_ctr_message_box = component.messageBox('UnloadByTitleForm', self)
        QtCore.QObject.connect(self.ui.ctr_movie_list.table, QtCore.SIGNAL('cellClicked(int, int)'), self.unload)

    
    def showEvent(self, event):
        self.ui.retranslateUi(None)
        self.ui.btn_logout.reset()
        self.ui.btn_cancel.reset()
        self.ui.btn_unload_all.setText(QtGui.QApplication.translate('UnloadByTitleForm', 'Unload All', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_icon_keyboard.setText(QtGui.QApplication.translate('Form', 'Search by Title', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_movie_list.reset()

    
    def hideEvent(self, event):
        self.ui.UnloadByTitleForm_ctr_message_box.hide()
        self.ui.UnloadByTitleForm_ctr_all_keyboard.hide()
        self.hide()

    
    def unload(self, row, col):
        if col == 3:
            data = { }
            data['wid'] = 'UnloadByTitleForm'
            data['cid'] = 'ctr_movie_list'
            data['type'] = 'EVENT'
            data['EVENT'] = 'EVENT_MOUSE_CLICK'
            data['param_info'] = { }
            data['param_info']['ctr_movie_list'] = { }
            data['param_info']['ctr_movie_list']['slot_id'] = str(self.ui.ctr_movie_list.table.item(row, 1).text())
            rfid = self.ui.ctr_movie_list.table.item(row, 3).data(self.ui.ctr_movie_list.dataType).toString()
            data['param_info']['ctr_movie_list']['rfid'] = str(rfid)
            self.sq.send(data)
        elif col == 4:
            self.ui.ctr_movie_list.table.removeRow(row)
        


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainf = UnloadByTitleForm()
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
                'movie_pic': '/home/mm/kiosk/var/gui/pic/36986.jpg',
                'movie_title': 'Jake Speed (1986)' },
            {
                'price': '39.00',
                'rfid': '009FBD2730000104E0',
                'upc': '013131137491',
                'state': 'in',
                'slot_id': '101',
                'movie_pic': '/home/mm/kiosk/var/gui/pic/36986.jpg',
                'movie_title': 'Jake Speed (1986)' },
            {
                'price': '39.00',
                'rfid': '009FBD2730000104E0',
                'upc': '013131137491',
                'state': 'in',
                'slot_id': '101',
                'movie_pic': '/home/mm/kiosk/var/gui/pic/36986.jpg',
                'movie_title': 'Jake Speed (1986)' },
            {
                'price': '39.00',
                'rfid': '009FBD2730000104E0',
                'upc': '013131137491',
                'state': 'in',
                'slot_id': '101',
                'movie_pic': '/home/mm/kiosk/var/gui/pic/36986.jpg',
                'movie_title': 'Jake Speed (1986)' },
            {
                'price': '39.00',
                'rfid': '009FBD2730000104E0',
                'upc': '013131137491',
                'state': 'in',
                'slot_id': '101',
                'movie_pic': '/home/mm/kiosk/var/gui/pic/36986.jpg',
                'movie_title': 'Jake Speed (1986)' },
            {
                'price': '39.00',
                'rfid': '00E9C42730000104E0',
                'upc': '013137800092',
                'state': 'in',
                'slot_id': '102',
                'movie_pic': '/home/mm/kiosk/var/gui/pic/132343.jpg',
                'movie_title': 'Acolytes (2008)' }] }
    mainf.show()
    mainf.ui.ctr_movie_list.setMovieList(data)
    sys.exit(app.exec_())

