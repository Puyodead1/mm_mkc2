# Source Generated with Decompyle++
# File: rentForm.pyc (Python 2.5)

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
        self.ui.ctr_btn_center = component.btnCenter(self, 'RentMainForm')
        self.ui.ctr_btn_center.hide()
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
        self.ui.ctr_tab_list = component.TabList(self, width, height)
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
        self.ui.ctr_btn_center.init()
        self.ui.btn_back.reset()
        self.ui.btn_slot_id.setText(QtGui.QApplication.translate('Rent', 'Express ID', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_icon_keyboard.setIcon(QtGui.QIcon(config.pic_icon_bigKeyboard))
        self.ui.ctr_shopping_cart.label.setText(QtGui.QApplication.translate('Form', '  Shopping Cart', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_shopping_cart.txt_show = QtGui.QApplication.translate('ShoppingCart', 'Show', None, QtGui.QApplication.UnicodeUTF8)
        self.ui.ctr_shopping_cart.txt_hide = QtGui.QApplication.translate('ShoppingCart', 'Hide', None, QtGui.QApplication.UnicodeUTF8)
        self.ui.ctr_shopping_cart.btn_view_cart.setText(QtGui.QApplication.translate('Form', 'View', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_shopping_cart.btn_hide.setText(QtGui.QApplication.translate('ShoppingCart', 'Show', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_movie_list.scrollToTop()

    
    def hideEvent(self, event):
        self.ui.RentMainForm_ctr_num_keyboard.hide()
        self.ui.RentMainForm_ctr_all_keyboard.hide()
        if self.ui.ctr_shopping_cart.show:
            self.ui.ctr_shopping_cart.hideCart()
        
        self.hide()

    
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
            'focus': 0,
            'ctr_tab_list': [
                {
                    'id': 'NEW RELEASE',
                    'text': 'New Release' },
                {
                    'id': 'Music',
                    'text': 'Family' },
                {
                    'id': 'NEW RELEASE',
                    'text': 'All Movies' },
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
                    'upc': '043396196155',
                    'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/105541.jpg',
                    'movie_big_pic': '105541_big.jpg',
                    'movie_title': '30 Days Of Night (2007)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '027616906847',
                    'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/1778.jpg',
                    'movie_big_pic': '1778_big.jpg',
                    'movie_title': 'Agent Cody Banks 2: Destination London (2004)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '043396243705',
                    'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/131967.jpg',
                    'movie_big_pic': '131967_big.jpg',
                    'movie_title': 'Angels & Demons (2009)',
                    'available_count': '0' },
                {
                    'is_bluray': '0',
                    'upc': '794043127816',
                    'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/121576.jpg',
                    'movie_big_pic': '121576_big.jpg',
                    'movie_title': 'Appaloosa (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '794043602825',
                    'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/4905.jpg',
                    'movie_big_pic': '4905_big.jpg',
                    'movie_title': 'Austin Powers: Goldmember (2002)',
                    'available_count': '1' },
                {
                    'is_bluray': '2',
                    'upc': '024543563716',
                    'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/125329.jpg',
                    'movie_big_pic': '125329_big.jpg',
                    'movie_title': 'Australia (2008)',
                    'available_count': '0' },
                {
                    'is_bluray': '0',
                    'upc': '025195050135',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/132243.jpg',
                    'movie_big_pic': '132243_big.jpg',
                    'movie_title': 'Away We Go (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '025195041997',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/116194.jpg',
                    'movie_big_pic': '116194_big.jpg',
                    'movie_title': 'Baby Mama (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '025193184825',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/103670.jpg',
                    'movie_big_pic': '103670_big.jpg',
                    'movie_title': 'Balls Of Fury (2007)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '027616905147',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/5955.jpg',
                    'movie_big_pic': '5955_big.jpg',
                    'movie_title': 'Barbershop 2: Back In Business (2004)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '025193227126',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/89153.jpg',
                    'movie_big_pic': '89153_big.jpg',
                    'movie_title': 'Because I Said So (2007)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '097361323145',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/106936.jpg',
                    'movie_big_pic': '106936_big.jpg',
                    'movie_title': 'Beowulf (2007)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '786936769418',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/122303.jpg',
                    'movie_big_pic': '122303_big.jpg',
                    'movie_title': 'Beverly Hills Chihuahua (2008)',
                    'available_count': '0' },
                {
                    'is_bluray': '0',
                    'upc': '085391189947',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/122790.jpg',
                    'movie_big_pic': '122790_big.jpg',
                    'movie_title': 'Body Of Lies (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '024543434276',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/83720.jpg',
                    'movie_big_pic': '83720_big.jpg',
                    'movie_title': 'Borat: Cultural Learnings Of America For Make Benefit Glorious Nation Of Kazakhstan (2006)',
                    'available_count': '0' },
                {
                    'is_bluray': '0',
                    'upc': '786936749274',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/124305.jpg',
                    'movie_big_pic': '124305_big.jpg',
                    'movie_title': 'Boy In The Striped Pajamas (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '043396013124',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/10446.jpg',
                    'movie_big_pic': '10446_big.jpg',
                    'movie_title': "Breakin' All The Rules (2004)",
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '025192672026',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/10585.jpg',
                    'movie_big_pic': '10585_big.jpg',
                    'movie_title': 'Bridget Jones: The Edge Of Reason (2004)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '025195017107',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/136825.jpg',
                    'movie_big_pic': '136825_big.jpg',
                    'movie_title': 'Bruno (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '025195016490',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/121086.jpg',
                    'movie_big_pic': '121086_big.jpg',
                    'movie_title': 'Burn After Reading (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '025193206824',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/83779.jpg',
                    'movie_big_pic': '83779_big.jpg',
                    'movie_title': 'Catch A Fire (2006)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '025195016902',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/123711.jpg',
                    'movie_big_pic': '123711_big.jpg',
                    'movie_title': 'Changeling (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '786936735437',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/120146.jpg',
                    'movie_big_pic': '120146_big.jpg',
                    'movie_title': 'Chronicles Of Narnia: Prince Caspian (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '794043107320',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/85532.jpg',
                    'movie_big_pic': '85532_big.jpg',
                    'movie_title': 'Code Name: The Cleaner (2007)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '024543569688',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/129109.jpg',
                    'movie_big_pic': '129109_big.jpg',
                    'movie_title': 'Day The Earth Stood Still',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '031398104391',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/120466.jpg',
                    'movie_big_pic': '120466_big.jpg',
                    'movie_title': 'Disaster Movie (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '025195055338',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/132223.jpg',
                    'movie_big_pic': '132223_big.jpg',
                    'movie_title': 'Drag Me To Hell (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '097363492641',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/122019.jpg',
                    'movie_big_pic': '122019_big.jpg',
                    'movie_title': 'Eagle Eye (2008)',
                    'available_count': '0' },
                {
                    'is_bluray': '0',
                    'upc': '025192305320',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/22196.jpg',
                    'movie_big_pic': '22196_big.jpg',
                    'movie_title': 'Empire (2002)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '031398240617',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/113302.jpg',
                    'movie_big_pic': '113302_big.jpg',
                    'movie_title': 'Eye (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '796019813525',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/120208.jpg',
                    'movie_big_pic': '120208_big.jpg',
                    'movie_title': 'Fanboys (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '024543470779',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/96554.jpg',
                    'movie_big_pic': '96554_big.jpg',
                    'movie_title': 'Fantastic Four 2: Rise Of The Silver Surfer (2007)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '025192032738',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/131942.jpg',
                    'movie_big_pic': '131942_big.jpg',
                    'movie_title': 'Fighting (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '031398101093',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/116682.jpg',
                    'movie_big_pic': '116682_big.jpg',
                    'movie_title': 'Forbidden Kingdom (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '794043130113',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/125330.jpg',
                    'movie_big_pic': '125330_big.jpg',
                    'movie_title': 'Four Christmases (2008)',
                    'available_count': '0' },
                {
                    'is_bluray': '0',
                    'upc': '794043129346',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/128993.jpg',
                    'movie_big_pic': '128993_big.jpg',
                    'movie_title': 'Friday The 13th (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '025195053532',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/137906.jpg',
                    'movie_big_pic': '137906_big.jpg',
                    'movie_title': 'Funny People (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '097363439240',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/138323.jpg',
                    'movie_big_pic': '138323_big.jpg',
                    'movie_title': 'G.I. Joe: The Rise Of Cobra (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '883929048861',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/116584.jpg',
                    'movie_big_pic': '116584_big.jpg',
                    'movie_title': 'Get Smart (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '794043124921',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/131954.jpg',
                    'movie_big_pic': '131954_big.jpg',
                    'movie_title': 'Ghosts Of Girlfriends Past (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '786936727487',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/105973.jpg',
                    'movie_big_pic': '105973_big.jpg',
                    'movie_title': 'Gone Baby Gone (2007)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '786936705119',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/81471.jpg',
                    'movie_big_pic': '81471_big.jpg',
                    'movie_title': 'Guardian (2006)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '555551',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/141192.jpg',
                    'movie_big_pic': '141192_big.jpg',
                    'movie_title': 'Guitar Hero III: Legends of Rock PS3 (2007)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '883929057832',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/132240.jpg',
                    'movie_big_pic': '132240_big.jpg',
                    'movie_title': 'Hangover (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '024543532897',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/119365.jpg',
                    'movie_big_pic': '119365_big.jpg',
                    'movie_title': 'Happening (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '794043123115',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/115729.jpg',
                    'movie_big_pic': '115729_big.jpg',
                    'movie_title': 'Harold & Kumar Escape From Guantanamo Bay (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '012569593268',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/100497.jpg',
                    'movie_big_pic': '100497_big.jpg',
                    'movie_title': 'Harry Potter And The Order Of The Phoenix (2007)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '085392844524',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/30699.jpg',
                    'movie_big_pic': '30699_big.jpg',
                    'movie_title': 'Harry Potter And The Prisoner Of Azkaban (2004)',
                    'available_count': '2' },
                {
                    'is_bluray': '0',
                    'upc': '085391173670',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/102525.jpg',
                    'movie_big_pic': '102525_big.jpg',
                    'movie_title': 'Harry Potter and the Prisoner of Azkaban (2004)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '786936774078',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/120953.jpg',
                    'movie_big_pic': '120953_big.jpg',
                    'movie_title': 'High School Musical 3: Senior Year (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '024543533450',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/119042.jpg',
                    'movie_big_pic': '119042_big.jpg',
                    'movie_title': 'Horton Hears A Who! (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '043396214705',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/98591.jpg',
                    'movie_big_pic': '98591_big.jpg',
                    'movie_title': 'I Know Who Killed Me (2007)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '024543610762',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/136826.jpg',
                    'movie_big_pic': '136826_big.jpg',
                    'movie_title': 'I Love You, Beth Cooper (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '097363519249',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/131262.jpg',
                    'movie_big_pic': '131262_big.jpg',
                    'movie_title': 'I Love You, Man (2009)',
                    'available_count': '0' },
                {
                    'is_bluray': '0',
                    'upc': '796019810906',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/108813.jpg',
                    'movie_big_pic': '108813_big.jpg',
                    'movie_title': "I'm Not There (2007)",
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '014381535723',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/126498.jpg',
                    'movie_big_pic': '126498_big.jpg',
                    'movie_title': 'In The Electric Mist (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '085391176275',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/106435.jpg',
                    'movie_big_pic': '106435_big.jpg',
                    'movie_title': 'In The Valley Of Elah (2007)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '097363418641',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/119831.jpg',
                    'movie_big_pic': '119831_big.jpg',
                    'movie_title': 'Indiana Jones And The Kingdom Of The Crystal Skull (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '025192583520',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/36123.jpg',
                    'movie_big_pic': '36123_big.jpg',
                    'movie_title': 'Interpreter (2005)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '012569701380',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/108266.jpg',
                    'movie_big_pic': '108266_big.jpg',
                    'movie_title': 'Invasion (2007)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '794043123429',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/121079.jpg',
                    'movie_big_pic': '121079_big.jpg',
                    'movie_title': 'Journey To The Center Of The Earth (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '025195005920',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/104480.jpg',
                    'movie_big_pic': '104480_big.jpg',
                    'movie_title': 'Kingdom (2007)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '031885',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/131263.jpg',
                    'movie_big_pic': '131263_big.jpg',
                    'movie_title': 'Knowing (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '043396120945',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/40580.jpg',
                    'movie_big_pic': '40580_big.jpg',
                    'movie_title': 'Kung Fu Hustle (2004)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '043396253728',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/121574.jpg',
                    'movie_big_pic': '121574_big.jpg',
                    'movie_title': 'Lakeview Terrace (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '025195038935',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/132241.jpg',
                    'movie_big_pic': '132241_big.jpg',
                    'movie_title': 'Land Of The Lost (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '025192032387',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/130902.jpg',
                    'movie_big_pic': '130902_big.jpg',
                    'movie_title': 'Last House On The Left (2009)',
                    'available_count': '0' },
                {
                    'is_bluray': '0',
                    'upc': '625828418709',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/114980.jpg',
                    'movie_big_pic': '114980_big.jpg',
                    'movie_title': 'Lords Of The Streets',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '085391183785',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/116040.jpg',
                    'movie_big_pic': '116040_big.jpg',
                    'movie_title': 'Lost Boys: The Tribe (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '097361179148',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/124302.jpg',
                    'movie_big_pic': '124302_big.jpg',
                    'movie_title': 'Madagascar: Escape 2 Africa (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '014381540529',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/135764.jpg',
                    'movie_big_pic': '135764_big.jpg',
                    'movie_title': 'Management (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '024543533030',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/117560.jpg',
                    'movie_big_pic': '117560_big.jpg',
                    'movie_title': 'Meet Dave (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '097363505242',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/101049.jpg',
                    'movie_big_pic': '101049_big.jpg',
                    'movie_title': 'Mighty Heart (2007)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '025195048972',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/125332.jpg',
                    'movie_big_pic': '125332_big.jpg',
                    'movie_title': 'Milk (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '883929028788',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/120326.jpg',
                    'movie_big_pic': '120326_big.jpg',
                    'movie_title': 'Mongol (2007)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '658149798229',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/48783.jpg',
                    'movie_big_pic': '48783_big.jpg',
                    'movie_title': "Monster's Ball (2001)",
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '031398104209',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/121575.jpg',
                    'movie_big_pic': '121575_big.jpg',
                    'movie_title': "My Best Friend's Girl (2008)",
                    'available_count': '0' },
                {
                    'is_bluray': '0',
                    'upc': '097363516644',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/95303.jpg',
                    'movie_big_pic': '95303_big.jpg',
                    'movie_title': 'Next (2006)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '024543625889',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/131977.jpg',
                    'movie_big_pic': '131977_big.jpg',
                    'movie_title': 'Night At The Museum: Battle Of The Smithsonian (2009)',
                    'available_count': '0' },
                {
                    'is_bluray': '0',
                    'upc': '883929037919',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/131930.jpg',
                    'movie_big_pic': '131930_big.jpg',
                    'movie_title': 'Observe And Report (2009)',
                    'available_count': '2' },
                {
                    'is_bluray': '0',
                    'upc': '883929048694',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/137510.jpg',
                    'movie_big_pic': '137510_big.jpg',
                    'movie_title': 'Orphan (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '343394',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/118758.jpg',
                    'movie_big_pic': '118758_big.jpg',
                    'movie_title': 'PS3 - Assassins Creed (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '013138009791',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/138328.jpg',
                    'movie_big_pic': '138328_big.jpg',
                    'movie_title': 'Paper Heart (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '043396256385',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/130779.jpg',
                    'movie_big_pic': '130779_big.jpg',
                    'movie_title': 'Paul Blart: Mall Cop (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '012569740648',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/56660.jpg',
                    'movie_big_pic': '56660_big.jpg',
                    'movie_title': 'Polar Express (2004)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '786936727531',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/91267.jpg',
                    'movie_big_pic': '91267_big.jpg',
                    'movie_title': 'Primeval (2007)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '043396191181',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/115799.jpg',
                    'movie_big_pic': '115799_big.jpg',
                    'movie_title': 'Prom Night (2008)',
                    'available_count': '2' },
                {
                    'is_bluray': '0',
                    'upc': '025195044912',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/136512.jpg',
                    'movie_big_pic': '136512_big.jpg',
                    'movie_title': 'Public Enemies (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '027616093578',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/102118.jpg',
                    'movie_big_pic': '102118_big.jpg',
                    'movie_title': 'Rescue Dawn (2007)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '013138002099',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/112796.jpg',
                    'movie_big_pic': '112796_big.jpg',
                    'movie_title': 'Righteous Kill (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '097361385846',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/116115.jpg',
                    'movie_big_pic': '116115_big.jpg',
                    'movie_title': 'Ruins (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '024543556329',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/123273.jpg',
                    'movie_big_pic': '123273_big.jpg',
                    'movie_title': 'Secret Life Of Bees (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '794043112331',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/103477.jpg',
                    'movie_big_pic': '103477_big.jpg',
                    'movie_title': "Shoot 'Em Up (2007)",
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '043396158641',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/65090.jpg',
                    'movie_big_pic': '65090_big.jpg',
                    'movie_title': 'Silent Hill (2006)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '097363494447',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/131940.jpg',
                    'movie_big_pic': '131940_big.jpg',
                    'movie_title': 'Soloist (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '031398108436',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/126741.jpg',
                    'movie_big_pic': '126741_big.jpg',
                    'movie_title': 'Spirit (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '097363485049',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/67781.jpg',
                    'movie_big_pic': '67781_big.jpg',
                    'movie_title': 'Star Trek (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '485049',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/142809.jpg',
                    'movie_big_pic': '142809_big.jpg',
                    'movie_title': 'Star Trek (2009)',
                    'available_count': '0' },
                {
                    'is_bluray': '0',
                    'upc': '883929023653',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/119596.jpg',
                    'movie_big_pic': '119596_big.jpg',
                    'movie_title': 'Star Wars: The Clone Wars (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '025195040075',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/131934.jpg',
                    'movie_big_pic': '131934_big.jpg',
                    'movie_title': 'State Of Play (2009)',
                    'available_count': '3' },
                {
                    'is_bluray': '0',
                    'upc': '013138003393',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/135105.jpg',
                    'movie_big_pic': '135105_big.jpg',
                    'movie_title': 'Sunshine Cleaning (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '1',
                    'upc': '013138306289',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/121957.jpg',
                    'movie_big_pic': '121957_big.jpg',
                    'movie_title': 'Surfer, Dude (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '025195021395',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/105869.jpg',
                    'movie_big_pic': '105869_big.jpg',
                    'movie_title': 'Sydney White (2007)',
                    'available_count': '0' },
                {
                    'is_bluray': '0',
                    'upc': '043396289963',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/123716.jpg',
                    'movie_big_pic': '123716_big.jpg',
                    'movie_title': 'Synecdoche, New York (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '043396253391',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/135568.jpg',
                    'movie_big_pic': '135568_big.jpg',
                    'movie_title': 'Taking Of Pelham 1 2 3 (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '883929038275',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/131975.jpg',
                    'movie_big_pic': '131975_big.jpg',
                    'movie_title': 'Terminator Salvation (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '120600',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/141190.jpg',
                    'movie_big_pic': '141190_big.jpg',
                    'movie_title': 'The Elder Scrolls IV: Oblivion PS3 (2007)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '013138001290',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/112845.jpg',
                    'movie_big_pic': '112845_big.jpg',
                    'movie_title': 'Traitor (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '097363532149',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/136072.jpg',
                    'movie_big_pic': '136072_big.jpg',
                    'movie_title': 'Transformers: Revenge Of The Fallen (2009)',
                    'available_count': '0' },
                {
                    'is_bluray': '0',
                    'upc': '043396275232',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/137511.jpg',
                    'movie_big_pic': '137511_big.jpg',
                    'movie_title': 'Ugly Truth (2009)',
                    'available_count': '0' },
                {
                    'is_bluray': '0',
                    'upc': '043396274433',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/124579.jpg',
                    'movie_big_pic': '124579_big.jpg',
                    'movie_title': 'Vacancy 2: The First Cut (2009)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '796019816724',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/119597.jpg',
                    'movie_big_pic': '119597_big.jpg',
                    'movie_title': 'Vicky Cristina Barcelona (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '990506',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/137902.jpg',
                    'movie_big_pic': '137902_big.jpg',
                    'movie_title': 'WWE Smackdown vs. Raw 2009 (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '025195017381',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/116887.jpg',
                    'movie_big_pic': '116887_big.jpg',
                    'movie_title': 'Wanted (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '687797121998',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/112549.jpg',
                    'movie_big_pic': '112549_big.jpg',
                    'movie_title': 'War, Inc. (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '024543528722',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/117536.jpg',
                    'movie_big_pic': '117536_big.jpg',
                    'movie_title': 'What Happens In Vegas (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '014633155457',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/119616.jpg',
                    'movie_big_pic': '119616_big.jpg',
                    'movie_title': 'Wii Madden NFL 09 All Play (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '786936727463',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/92398.jpg',
                    'movie_big_pic': '92398_big.jpg',
                    'movie_title': 'Wild Hogs (2007)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '346684',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/114116.jpg',
                    'movie_big_pic': '114116_big.jpg',
                    'movie_title': 'World Trade Center (2006)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '024543543510',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/122011.jpg',
                    'movie_big_pic': '122011_big.jpg',
                    'movie_title': 'X-Files: I Want To Believe (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '550496',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/132076.jpg',
                    'movie_big_pic': '132076_big.jpg',
                    'movie_title': 'XBOX 360 - Smackdown vs Raw 2009 (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '0300601',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/139974.jpg',
                    'movie_big_pic': '139974_big.jpg',
                    'movie_title': 'XBOX 360 Pro Evolution Soccer 2007 (2006)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '550229',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/132045.jpg',
                    'movie_big_pic': '132045_big.jpg',
                    'movie_title': 'XBOX360 - Conan (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '0',
                    'upc': '832718',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/138299.jpg',
                    'movie_big_pic': '138299_big.jpg',
                    'movie_title': 'Xbox 360 - Quantum of Solace (2008)',
                    'available_count': '1' },
                {
                    'is_bluray': '1',
                    'upc': '043396277465',
                    'movie_pic': '\\/home\\/mm\\/kiosk\\/var\\/gui\\/pic\\/118168.jpg',
                    'movie_big_pic': '118168_big.jpg',
                    'movie_title': "You Don't Mess With The Zohan (2008)",
                    'available_count': '1' }] }
        self.ui.ctr_movie_list.setMovieList(data)

    
    def test_shopping_cart(self):
        data = {
            'focus': 0,
            'ctr_shopping_cart': [
                {
                    'movie_title': 'Night Train ing The Green(2009)' },
                {
                    'movie_title': 'Chasing The Green (2009)' },
                {
                    'movie_title': 'Chasing The Green (2009)' }] }
        self.ui.ctr_shopping_cart.setTabList(data)


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
    form.ui.txt_rent_label.setText('$6 New Release by Date Searching')
    sys.exit(app.exec_())

