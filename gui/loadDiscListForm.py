# Source Generated with Decompyle++
# File: loadDiscListForm.pyc (Python 2.5)

'''
LoadDiscListForm
2009-07-20 created by Mavis
'''
import os
import sys
import config
import component
from PyQt4 import QtCore, QtGui
from loadDiscListForm_ui import Ui_loadDiscListForm
from squery import socketQuery

class LoadDiscListForm(QtGui.QMainWindow):
    
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_loadDiscListForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_load)))
        self.setPalette(palette)
        self.sq = socketQuery()
        self.ui.ctr_movie_list = component.TitleList(self, 627 / 2, 80)
        self.ui.ctr_movie_list.setGeometry(50, 190, 668, 625)
        self.ui.btn_logout = component.btnLogout(self, 'LoadDiscListForm')
        self.ui.btn_logout.setGeometry(580, 20, 160, 68)
        self.ui.btn_back = component.btnBack(self, 'LoadDiscListForm')
        self.ui.btn_cancel = component.btnCancel(self, 'LoadDiscListForm')
        self.ui.hboxlayout.addWidget(self.ui.btn_cancel)
        self.ui.hboxlayout.addWidget(self.ui.btn_back)
        QtCore.QObject.connect(self.ui.ctr_movie_list, QtCore.SIGNAL('itemClicked(QTableWidgetItem*)'), self.ctr_movie_list_click)

    
    def ctr_movie_list_click(self, item):
        upc = item.data(1047295).toString()
        data = { }
        data['wid'] = 'LoadDiscListForm'
        data['cid'] = 'ctr_movie_list'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info']['ctr_movie_list'] = { }
        data['param_info']['ctr_movie_list']['upc'] = str(upc)
        self.sq.send(data)

    
    def showEvent(self, event):
        self.ui.retranslateUi('')
        self.ui.btn_logout.reset()
        self.ui.btn_back.reset()
        self.ui.btn_cancel.hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = LoadDiscListForm()
    mainf.show()
    data = {
        'ctr_movie_list': [
            {
                'movie_title': 'Adam Ferrara: Funny As Hell (2009)',
                'movie_release_year': '2009',
                'upc': '014381533224',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/127810.jpg' },
            {
                'movie_title': 'Bled (2009)',
                'movie_release_year': '2009',
                'upc': '031398108276',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/128124.jpg' },
            {
                'movie_title': 'Boys Of Ghost Town (2008)',
                'movie_release_year': '2008',
                'upc': '735978440663',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/130536.jpg' },
            {
                'movie_title': 'Bride Wars (2009)',
                'movie_release_year': '2009',
                'upc': '024543579472',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/127538.jpg' },
            {
                'movie_title': 'Burrowers (2008)',
                'movie_release_year': '2008',
                'upc': '031398108375',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/128521.jpg' },
            {
                'movie_title': 'Caller (2008)',
                'movie_release_year': '2008',
                'upc': '829567060421',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/127841.jpg' },
            {
                'movie_title': 'Caprica (2009)',
                'movie_release_year': '2009',
                'upc': '025192019753',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/128790.jpg' },
            {
                'movie_title': 'Chandi Chowk To China (2009)',
                'movie_release_year': '2009',
                'upc': '883929049806',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/126376.jpg' },
            {
                'movie_title': 'Cloverfield (2008)',
                'movie_release_year': '2008',
                'upc': '032429061973',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/111207.jpg' },
            {
                'movie_title': 'Curious Case Of Benjamin Button (2008)',
                'movie_release_year': '2008',
                'upc': '097361430744',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/126739.jpg' },
            {
                'movie_title': 'Dante 01 (2008)',
                'movie_release_year': '2008',
                'upc': '796019817073',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/128539.jpg' },
            {
                'movie_title': 'Fired Up! (2009)',
                'movie_release_year': '2009',
                'upc': '043396272866',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/129404.jpg' },
            {
                'movie_title': 'Florence Nightingale (2008)',
                'movie_release_year': '2008',
                'upc': '043396272071',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/129529.jpg' }] }
    mainf.ui.ctr_movie_list.setMovieList(data)
    sys.exit(app.exec_())

