# Source Generated with Decompyle++
# File: mainForm.pyc (Python 2.5)

'''
MainForm is the main window. 
2009-07-02 created by Mavis
'''
import sys
from PyQt4 import QtCore, QtGui
from main_ui import Ui_MainUiForm
import config
import os
from component import gifButton, PicTrans, ctrButton, virtualComponent
from squery import socketQuery

class MainForm(QtGui.QMainWindow):
    
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainUiForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        self.setFixedSize(768, 1024)
        if not os.path.isfile(config.pic_bg_start):
            print('CAN NOT FIND THE PIC: %s' % config.pic_bg_start)
        else:
            palette = QtGui.QPalette()
            palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_start)))
            self.setPalette(palette)
        self.sq = socketQuery()
        self.btn_rent = gifButton(self, 'btn_rent', config.pic_btn_rent_bg, config.pic_btn_rent_bg_on)
        self.btn_return = gifButton(self, 'btn_return', config.pic_btn_return_bg, config.pic_btn_return_bg_on, 0, 213, 210)
        self.btn_buy = gifButton(self, 'btn_buy', config.pic_btn_buy, config.pic_btn_buy_on)
        self.btn_buy.bg.move(10, 90)
        self.btn_buy.gg.move(13, 90 + 2)
        self.btn_login = gifButton(self, 'btn_login', config.pic_btn_login, config.pic_btn_login_on)
        self.btn_pickup = gifButton(self, 'btn_pickup', config.pic_btn_pickup_bg, config.pic_btn_pickup_bg_on)
        self.btn_pickup.bg.move(10, 90)
        self.btn_pickup.gg.move(13, 90 + 2)
        self.btn_active = gifButton(self, 'btn_active', config.pic_btn_active, config.pic_btn_active_on, 0, 213, 210)
        self.btn_active.bg.move(10, 90)
        self.btn_active.gg.move(13, 90 + 2)
        vlayout_l = QtGui.QVBoxLayout()
        vlayout_l.addWidget(self.btn_rent)
        vlayout_l.addWidget(self.btn_buy)
        vlayout_m = QtGui.QVBoxLayout()
        vlayout_m.addWidget(self.btn_return)
        vlayout_m.addWidget(self.btn_active)
        vlayout_r = QtGui.QVBoxLayout()
        vlayout_r.addWidget(self.btn_login)
        vlayout_r.addWidget(self.btn_pickup)
        self.ui.hboxlayout.addLayout(vlayout_l)
        self.ui.hboxlayout.addLayout(vlayout_m)
        self.ui.hboxlayout.addLayout(vlayout_r)
        self.ui.logo.setGeometry(QtCore.QRect(54, 354, 225, 120))
        self.logo = config.pic_logo
        if os.path.isfile(config.pic_logo):
            pic = QtGui.QPixmap(config.pic_logo).scaled(225, 120, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.ui.logo.setPixmap(pic)
        
        self.ui.ctr_movie_list = PicTrans('MainForm', self)
        self.ui.ctr_movie_list.setGeometry(0, 0, 768, 479)
        self.ui.test_mode_flag = QtGui.QLabel(self)
        self.ui.test_mode_flag.setGeometry(50, 375, 678, 270)
        self.ui.test_mode_flag.setPixmap(QtGui.QPixmap(config.pic_test_flag))
        self.ui.test_mode_flag.hide()
        '\n\t\tstyle_en = "border: 0px; image: url("+config.pic_btn_en+")"\n\t\tself.ui.btn_en = ctrButton(self, "MainForm", "btn_en", "", config.btn_lang_width, config.btn_lang_height, style_en)\n\t\tself.label_en = QtGui.QLabel(self.ui.btn_en)\n\t\tself.label_en.setGeometry(0, 0, config.btn_lang_width, config.btn_lang_height)\n\t\tself.ui.hboxlayout1.addWidget(self.ui.btn_en)\n\t\t'
        self.language = []
        self.ui.ctr_btn_lang = virtualComponent(self)

    
    def initLanguage(self, data):
        if not data or not data['ctr_btn_lang']:
            return None
        
        data = data['ctr_btn_lang']
        self.language = data
        if config.transFile:
            language = config.transFile.split('.')[0].split('trans_')[1]
        else:
            language = 'en'
        pic = ''
        for lang in data:
            exec('pic = config.pic_btn_' + lang)
            exec('self.ui.btn_' + lang + ' = ctrButton(self, "MainForm", "btn_' + lang + '", "", config.btn_lang_width, config.btn_lang_height, "border: 0px; image: url(' + pic + ')")')
            exec('self.label_' + lang + ' = QtGui.QLabel(self.ui.btn_' + lang + ')')
            exec('self.ui.hboxlayout1.addWidget(self.ui.btn_' + lang + ')')
            if language == lang:
                exec('self.label_' + lang + '.setPixmap(QtGui.QPixmap(config.pic_btn_language_on))')
            else:
                exec('self.label_' + lang + '.setPixmap(QtGui.QPixmap(config.pic_btn_language_out))')
        

    
    def showEvent(self, event):
        if self.logo != config.pic_logo:
            self.logo = config.pic_logo
            self.ui.logo.setPixmap(QtGui.QPixmap(config.pic_logo).scaled(225, 120, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        
        self.resetLang()
        self.btn_rent.cg.setText(QtGui.QApplication.translate('Form', 'Rent', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_return.cg.setText(QtGui.QApplication.translate('Form', 'Return', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_pickup.cg.setText(QtGui.QApplication.translate('Form', 'Pick Up', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_buy.cg.setText(QtGui.QApplication.translate('Form', 'Buy', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_login.cg.setText(QtGui.QApplication.translate('Form', 'Membership Center', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_active.cg.setText(QtGui.QApplication.translate('Form', 'Activate', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_rent.fg.setText(self.btn_rent.cg.text())
        self.btn_return.fg.setText(self.btn_return.cg.text())
        self.btn_pickup.fg.setText(self.btn_pickup.cg.text())
        self.btn_buy.fg.setText(self.btn_buy.cg.text())
        self.btn_login.fg.setText(self.btn_login.cg.text())
        self.btn_active.fg.setText(self.btn_active.cg.text())
        self.btn_rent.bg.setText(QtGui.QApplication.translate('Form', 'Touch here to select your rental discs', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_return.bg.setText(QtGui.QApplication.translate('Form', 'Touch here to return discs', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_pickup.bg.setText(QtGui.QApplication.translate('Form', 'Touch here to pick up your online orders', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_buy.bg.setText(QtGui.QApplication.translate('Form', 'Touch here to purchase discs', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_login.bg.setText(QtGui.QApplication.translate('Form', 'Touch here to login to your membership account', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_active.bg.setText(QtGui.QApplication.translate('Form', 'Touch here to activate a membership card', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_rent.gg.setText(self.btn_rent.bg.text())
        self.btn_return.gg.setText(self.btn_return.bg.text())
        self.btn_pickup.gg.setText(self.btn_pickup.bg.text())
        self.btn_buy.gg.setText(self.btn_buy.bg.text())
        self.btn_login.gg.setText(self.btn_login.bg.text())
        self.btn_active.gg.setText(self.btn_active.bg.text())

    
    def resetLang(self):
        if self.language:
            if config.transFile:
                language = config.transFile.split('.')[0].split('trans_')[1]
            else:
                language = 'en'
            for lang in self.language:
                if language == lang:
                    exec('self.label_' + lang + '.setPixmap(QtGui.QPixmap(config.pic_btn_language_on))')
                else:
                    exec('self.label_' + lang + '.setPixmap(QtGui.QPixmap(config.pic_btn_language_out))')
            
        


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = MainForm()
    data = {
        'ctr_movie_list': [
            {
                'upc': '502190',
                'movie_pic': '/home/jojo/images/bg.png',
                'is_bluray': 1 },
            {
                'upc': '502194',
                'movie_pic': '/home/jojo/images/bg_language.png',
                'is_bluray': 1 },
            {
                'upc': '502194',
                'movie_pic': '/home/jojo/images/cancel.png',
                'is_bluray': 0 },
            {
                'upc': '502194',
                'movie_pic': '/home/jojo/images/machine.png',
                'is_bluray': 0 },
            {
                'upc': '502194',
                'movie_pic': '/home/jojo/images/mask.png',
                'is_bluray': 0 },
            {
                'upc': '502194',
                'movie_pic': '/home/jojo/images/bg_pic.png',
                'is_bluray': 2 },
            {
                'upc': '502194',
                'movie_pic': '/home/jojo/images/bg_map.png',
                'is_bluray': 2 },
            {
                'upc': '502194',
                'movie_pic': '/home/jojo/images/arow_less1.png',
                'is_bluray': 1 },
            {
                'upc': '502194',
                'movie_pic': '/home/jojo/images/arow_more1.png',
                'is_bluray': 0 },
            {
                'upc': '302194',
                'movie_pic': '/home/jojo/images/arrow_down_out.png',
                'is_bluray': 1 },
            {
                'upc': '502194',
                'movie_pic': '/home/jojo/images/arrow_up_out.png',
                'is_bluray': 0 },
            {
                'upc': '502194',
                'movie_pic': '/home/jojo/images/btn_back.png',
                'is_bluray': 1 },
            {
                'upc': '502194',
                'movie_pic': '/home/jojo/images/btn_next.png',
                'is_bluray': 1 },
            {
                'upc': '402194',
                'movie_pic': '/home/jojo/images/Firefox_wallpaper.png',
                'is_bluray': 0 }] }
    mainf.ui.ctr_movie_list.setMovieList(data)
    mainf.show()
    mainf.ui.ctr_btn_lang.initLanguage({
        'ctr_btn_lang': [
            'en',
            'fr_FR',
            'es'] })
    sys.exit(app.exec_())

