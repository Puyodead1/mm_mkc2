# Source Generated with Decompyle++
# File: rentForm_game.pyc (Python 2.5)

'''
RentMainForm for rent
2009-07-02 created by Mavis
'''
import sys
from PyQt4 import QtCore, QtGui
import config
from squery import socketQuery
import component

class RentMainForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = QtCore.QObject()
        self.setGeometry(0, 0, 768, 1024)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_rent)))
        self.setPalette(palette)
        self.sq = socketQuery()
        self.ui.txt_rent_label = QtGui.QLabel(self)
        self.ui.txt_rent_label.setStyleSheet('color: white; font: bold 28px;')
        self.ui.txt_rent_label.setWordWrap(True)
        self.ui.txt_rent_label.setGeometry(30, 15, 540, 68)
        self.ui.btn_icon_keyboard = QtGui.QPushButton(self)
        self.ui.btn_icon_keyboard.setGeometry(20, 910, 130, 85)
        self.ui.btn_back = component.btnCancel(self, 'RentMainForm')
        self.ui.btn_back.setGeometry(580, 20, 160, 68)
        self.ui.btn_slot_id = component.ctrButton(self, 'RentMainForm', 'btn_slot_id', QtGui.QApplication.translate('Rent', 'Express ID', None, QtGui.QApplication.UnicodeUTF8), config.btn_width, config.btn_height, config.btn02Style)
        self.ui.btn_slot_id.setGeometry(540, 920, config.btn_width, config.btn_height)
        self.ui.btn_icon_keyboard.setStyleSheet('background-color: transparent; border: 0px')
        self.ui.btn_icon_keyboard.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.btn_icon_keyboard.setIcon(QtGui.QIcon(config.pic_icon_bigKeyboard))
        self.ui.btn_icon_keyboard.setIconSize(QtCore.QSize(130, 85))
        self.ui.ctr_movie_list = component.MovieList(self)
        self.ui.ctr_movie_list.setGeometry(config.movieList_x, config.movieList_y, config.movieList_width + 7, config.movieList_height - 12)
        x = config.movieList_x + config.movieList_width + 30
        width = 238
        height = config.movieList_height - 110
        self.ui.ctr_tab_list = TabListGame(self, width, height)
        self.ui.ctr_tab_list.setGeometry(x, config.movieList_y, width, height)
        self.ui.ctr_shopping_cart = component.ListView(self, x, config.movieList_y + height + 8)
        self.ui.ctr_shopping_cart.setGeometry(x, config.movieList_y + height + 8, 238, 110)
        self.ui.RentMainForm_ctr_num_keyboard = component.numKeyboard('RentMainForm', self)
        self.ui.RentMainForm_ctr_num_keyboard.setGeometry(169, 282, 440, 430)
        self.ui.RentMainForm_ctr_num_keyboard.hide()
        self.ui.RentMainForm_ctr_all_keyboard = component.allKeyboard('RentMainForm', self)
        self.ui.RentMainForm_ctr_all_keyboard.hide()
        QtCore.QObject.connect(self.ui.btn_icon_keyboard, QtCore.SIGNAL('clicked()'), self.btn_icon_keyboard_click)
        QtCore.QObject.connect(self.ui.btn_icon_keyboard, QtCore.SIGNAL('pressed()'), self.btn_icon_press)

    
    def btn_icon_press(self):
        self.ui.btn_icon_keyboard.setIconSize(QtCore.QSize(120, 75))

    
    def showEvent(self, event):
        self.ui.btn_back.reset()
        self.ui.btn_slot_id.setText(QtGui.QApplication.translate('Rent', 'Express ID', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_icon_keyboard.setIcon(QtGui.QIcon(config.pic_icon_bigKeyboard))
        self.ui.ctr_shopping_cart.label.setText(QtGui.QApplication.translate('Form', '  Shopping Cart', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_shopping_cart.txt_show = QtGui.QApplication.translate('ShoppingCart', 'Show', None, QtGui.QApplication.UnicodeUTF8)
        self.ui.ctr_shopping_cart.txt_hide = QtGui.QApplication.translate('ShoppingCart', 'Hide', None, QtGui.QApplication.UnicodeUTF8)
        self.ui.ctr_shopping_cart.btn_view_cart.setText(QtGui.QApplication.translate('Form', 'View', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_shopping_cart.btn_hide.setText(QtGui.QApplication.translate('ShoppingCart', 'Show', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_movie_list.scrollToTop()
        self.ui.ctr_tab_list.init()

    
    def hideEvent(self, event):
        self.ui.RentMainForm_ctr_num_keyboard.hide()
        self.ui.RentMainForm_ctr_all_keyboard.hide()
        if self.ui.ctr_shopping_cart.show:
            self.ui.ctr_shopping_cart.hideCart()
        

    
    def btn_icon_keyboard_click(self):
        data = { }
        data['wid'] = 'RentMainForm'
        data['cid'] = 'btn_icon_keyboard'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        self.sq.send(data)
        self.ui.btn_icon_keyboard.setIconSize(QtCore.QSize(130, 85))

    
    def test_tablist(self):
        data = {
            'ctr_tab_list': [
                {
                    'id': 'NEW RELEASE',
                    'text': 'New Release' },
                {
                    'id': 'CATEGORY',
                    'text': 'New Release' },
                {
                    'id': 'ON SALE',
                    'text': 'New Release' },
                {
                    'id': 'PS3',
                    'text': 'PlayStation3' },
                {
                    'id': 'WII',
                    'text': 'WII' },
                {
                    'id': '(Action)',
                    'text': 'Action' },
                {
                    'id': '(Comedy)',
                    'text': 'Comedy' },
                {
                    'id': 'Music',
                    'text': 'ALKASDJFLAKJ' },
                {
                    'id': '(Action)',
                    'text': 'Family' },
                {
                    'id': '(Action)',
                    'text': 'Action/Animator' },
                {
                    'text': 'SciFi',
                    'id': "('SciFi')" },
                {
                    'text': 'War',
                    'id': "('War')" },
                {
                    'text': 'Animation',
                    'id': "('Animation')" },
                {
                    'text': 'Others',
                    'id': "('Thriller', 'Suspense/Thriller', 'Comedy/Drama', 'Documentary', 'Fantasy', 'Mystery/Suspense', 'Music')" },
                {
                    'text': 'Blu-ray',
                    'id': 'BLU-RAY' },
                {
                    'text': 'All Movies',
                    'id': 'ALL MOVIES' }] }
        self.ui.ctr_tab_list.setTabList(data)

    
    def test_movielist(self):
        data = {
            'ctr_movie_list': [
                {
                    'is_bluray': '0',
                    'upc': '794043125041',
                    'movie_pic': '/home/mm/kiosk/mkc2/gui/image/trailer.jpg',
                    'movie_big_pic': '131932_big.jpg',
                    'movie_title': '17 Again (2009)',
                    'available_count': '1' }] }
        self.ui.ctr_movie_list.setMovieList(data)

    
    def test_shopping_cart(self):
        data = {
            'ctr_shopping_cart': [
                {
                    'movie_title': 'Night Train ing The Green(2009)' },
                {
                    'movie_title': 'Chasing The Green (2009)' },
                {
                    'movie_title': 'Chasing The Green (2009)' }] }
        self.ui.ctr_shopping_cart.setTabList(data)



class styleButton(QtGui.QPushButton):
    
    def __init__(self, id, w = 234, h = 60, parent = None, wid = 'RentMainForm', cid = 'ctr_tab_list'):
        QtGui.QPushButton.__init__(self, parent)
        self.setFixedSize(w, h)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet(config.style_tablist_btn)
        self.sq = socketQuery()
        self.wid = wid
        self.cid = cid
        self.param = {
            self.cid: {
                'genre': id } }
        self.connect(self, QtCore.SIGNAL('clicked()'), self.sendMsg)

    
    def sendMsg(self):
        data = { }
        data['wid'] = self.wid
        data['cid'] = self.cid
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = self.param
        self.sq.send(data)



class TabListGame(QtGui.QWidget):
    
    def __init__(self, parent, width, height):
        QtGui.QWidget.__init__(self, parent)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_gener_list)))
        self.setPalette(palette)
        btn_wii = styleButton('WII', 160, 130)
        btn_ps3 = styleButton('PS3', 160, 130)
        btn_xbox = styleButton('XBOX360', 160, 130)
        btn_wii.setStyleSheet(config.style_tablist_btn_wii)
        btn_ps3.setStyleSheet(config.style_tablist_btn_ps3)
        btn_xbox.setStyleSheet(config.style_tablist_btn_xbox)
        self.btn_on_sale = styleButton('ON SALE')
        self.btn_new_release = styleButton('NEW RELEASE')
        self.btn_category = styleButton('CATEGORY')
        w = QtGui.QWidget(self)
        w.setMaximumHeight(450)
        layoutp = QtGui.QVBoxLayout(w)
        layoutp.addWidget(btn_xbox, 0, QtCore.Qt.AlignCenter)
        layoutp.addWidget(btn_ps3, 0, QtCore.Qt.AlignCenter)
        layoutp.addWidget(btn_wii, 0, QtCore.Qt.AlignCenter)
        wb = QtGui.QWidget(self)
        wb.setFixedHeight(config.movieList_height - 110 - 450 - 20)
        layoutb = QtGui.QVBoxLayout(wb)
        layoutb.setContentsMargins(0, 0, 0, 0)
        layoutb.addWidget(self.btn_on_sale, 0, QtCore.Qt.AlignTop)
        layoutb.addWidget(self.btn_new_release, 0, QtCore.Qt.AlignTop)
        layoutb.addWidget(self.btn_category, 0, QtCore.Qt.AlignTop)
        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.addWidget(w)
        layout.addWidget(wb)
        self.setLayout(layout)

    
    def init(self):
        self.btn_on_sale.hide()
        self.btn_new_release.hide()
        self.btn_category.hide()

    
    def setTabList(self, data):
        if not data:
            print('[setTabList] Error: data can not be NULL!')
            return -1
        
        data = data['ctr_tab_list']
        if not data:
            return None
        
        for item in data:
            id = item['id']
            if id == 'ON SALE':
                self.btn_on_sale.setText(item['text'])
                self.btn_on_sale.show()
            elif id == 'NEW RELEASE':
                self.btn_new_release.setText(item['text'])
                self.btn_new_release.show()
            elif id == 'CATEGORY':
                self.btn_category.setText(item['text'])
                self.btn_category.show()
            
        


if __name__ == '__main__':
    import os
    app = QtGui.QApplication(sys.argv)
    form = RentMainForm()
    config.transFile = 'trans_en.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    form.show()
    form.test_tablist()
    form.test_shopping_cart()
    form.test_movielist()
    form.ui.txt_rent_label.setText('$6 New Release by Date Searching alaskjdfalskjdfkjslklksjdlfkj')
    sys.exit(app.exec_())

