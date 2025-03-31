# Source Generated with Decompyle++
# File: movieDetailForm.pyc (Python 2.5)

'''
DiscDetailForm for movie detail
2009-07-03 created by Mavis
2010-06-29 changed by Mavis:
\t\t   Add ctr_btn_center for membership.
'''
import sys
import os
import config
import component
from PyQt4 import QtCore, QtGui
from movie_detail_ui import Ui_MovieDetailForm
from squery import socketQuery

class DiscDetailForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MovieDetailForm()
        self.ui.setupUi(self)
        self.ui.frame_2.setStyleSheet('border: 2px solid #0153b0; border-radius: 5px')
        self.ui.frame_3.setStyleSheet('border: 2px solid #0153b0; border-radius: 5px')
        self.setGeometry(0, 0, 768, 1024)
        self.palette = QtGui.QPalette()
        self.palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_movie)))
        self.setPalette(self.palette)
        self.sq = socketQuery()
        self.ui.synopsis.setStyleSheet(config.scroll_style)
        self.ui.ctr_btn_center = component.btnCenter(self, 'DiscDetailForm')
        self.ui.ctr_btn_center.hide()
        self.ui.btn_back = component.btnBack(self, 'DiscDetailForm')
        self.ui.btn_cancel = component.btnCancel(self, 'DiscDetailForm')
        self.ui.btn_cancel.setGeometry(580, 20, 160, 68)
        self.ui.btn_next = component.ctrButton(self, 'DiscDetailForm', 'btn_next', QtGui.QApplication.translate('Form', 'Next', None, QtGui.QApplication.UnicodeUTF8), 159, 68, config.btnGreenStyle)
        self.ui.btn_available_notice = component.ctrButton(self, 'DiscDetailForm', 'btn_available_notice', QtGui.QApplication.translate('Form', 'Available\nNotice', None, QtGui.QApplication.UnicodeUTF8), 159, 68, 'color: white; font: bold italic 20px; border-style: outset; background-image: url(' + config.pic_btn_yellow + '); ')
        self.ui.btn_available_notice.hide()
        self.ui.hboxlayout.addWidget(self.ui.btn_back)
        self.ui.hboxlayout.addWidget(self.ui.btn_next)
        self.ui.hboxlayout.addWidget(self.ui.btn_available_notice)
        self.feature = component.featureList(self)
        self.feature.setGeometry(180, 208, 532, 175)
        self.ui.label_available = QtGui.QLabel(self)
        self.ui.label_available.setGeometry(QtCore.QRect(220, 380, 141, 23))
        self.ui.img_available_yes = QtGui.QLabel(self)
        self.ui.img_available_yes.setGeometry(QtCore.QRect(180, 375, 31, 25))
        self.ui.img_available_yes.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.mask_coming_soon_flag.setPixmap(QtGui.QPixmap(config.pic_coming_soon))
        self.ui.mask_coming_soon_flag.hide()
        self.ui.img_available_yes.setPixmap(QtGui.QPixmap(config.pic_available_yes))
        self.ui.ctr_movie_detail = component.virtualComponent(self)
        self.label = QtGui.QLabel('Loading ...', self.ui.frame)
        self.label.setStyleSheet('font: bold 16px')
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setGeometry(4, 4, self.ui.frame.width() - 6, self.ui.frame.height() - 6)
        self.container = QtGui.QX11EmbedContainer(self.label)
        self.container.setGeometry(0, 0, self.ui.frame.width() - 6, self.ui.frame.height() - 6)
        self.player = component.Player(self.container.winId(), self.ui.frame)
        self.trailer = 0
        self.txt_available = QtGui.QApplication.translate('Rent', 'Now Available', None, QtGui.QApplication.UnicodeUTF8)
        self.txt_not_available = QtGui.QApplication.translate('Rent', 'NOT Available', None, QtGui.QApplication.UnicodeUTF8)

    
    def hideEvent(self, event):
        if self.trailer:
            self.player.stop()
            self.trailer = 0
        
        self.ui.btn_available_notice.hide()
        self.ui.btn_next.hide()
        self.hide()

    
    def showEvent(self, event):
        self.ui.retranslateUi('')
        self.ui.btn_back.reset()
        self.ui.btn_cancel.reset()
        self.ui.btn_next.reset(QtCore.QT_TRANSLATE_NOOP('Form', 'Next'))
        self.ui.btn_available_notice.setText(QtGui.QApplication.translate('Form', 'Available\nNotice', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.mask_coming_soon_flag.setPixmap(QtGui.QPixmap(config.pic_coming_soon))
        self.label.setText(QtGui.QApplication.translate('Form', 'Loading ...', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_btn_center.hide()
        self.ui.ctr_btn_center.init()

    
    def setVideoVolume(self, param):
        if not param or not param['volume']:
            return None
        
        if param['volume'] == 'off':
            self.player.setVolume(0)
        else:
            self.player.setVolume(1)

    
    def setMovieDetail(self, data):
        if not data['ctr_movie_detail']:
            print('[setMovieDetail] Error: data can not be NULL!')
            return -1
        
        data = data['ctr_movie_detail']
        self.ui.movie_title.setText(data['movie_title'])
        self.ui.dvd_version.setText(data['dvd_version'])
        
        try:
            self.feature.setList(data['feature'])
        except Exception as ex:
            print(ex)

        
        try:
            pixmap = config.pic_dvd
            if 'is_bluray' in data and data['is_bluray']:
                icon_flag = int(data['is_bluray'])
                if icon_flag == 1:
                    pixmap = config.pic_bluray
                elif icon_flag == 2:
                    pixmap = config.pic_icon_wii
                elif icon_flag == 3:
                    pixmap = config.pic_icon_xbox
                elif icon_flag == 4:
                    pixmap = config.pic_icon_playstation
                
            
            self.ui.icon_dvd.setPixmap(QtGui.QPixmap(pixmap))
        except Exception as ex:
            print(ex)

        self.ui.synopsis.setText(data['synopsis'])
        self.ui.rent_price.setText(config.symbol + data['rent_price'])
        
        try:
            if not data['buy_price'] or data['buy_price'] == '0.0':
                self.ui.label_buy.hide()
                self.ui.buy_price.hide()
            else:
                self.ui.label_buy.show()
                self.ui.buy_price.show()
                self.ui.buy_price.setText(config.symbol + data['buy_price'])
        except Exception as ex:
            print(ex)

        
        try:
            if data['is_available']:
                if data['is_available'] == '1':
                    self.ui.label_available.setText(QtGui.QApplication.translate('Rent', 'Now Available', None, QtGui.QApplication.UnicodeUTF8))
                    self.ui.label_available.setStyleSheet('color: green; font: bold 18px;')
                    self.ui.img_available_yes.setPixmap(QtGui.QPixmap(config.pic_available_yes))
                else:
                    self.ui.img_available_yes.setPixmap(QtGui.QPixmap(config.pic_available_no))
                    self.ui.label_available.setText(QtGui.QApplication.translate('Rent', 'NOT Available', None, QtGui.QApplication.UnicodeUTF8))
                    self.ui.label_available.setStyleSheet('color: #bb0000; font: bold 18px;')
        except Exception as ex:
            print(ex)

        if os.path.isfile(data['movie_pic']):
            self.ui.movie_pic.setPixmap(QtGui.QPixmap(data['movie_pic']))
        else:
            print('[setMovieDetail] Warrning: pic not found!')
        
        try:
            trailer_name = data['trailer_name']
            if trailer_name.endswith('default.flv'):
                self.trailer = 0
                self.ui.synopsis.resize(661, self.ui.synopsis.height())
                self.ui.frame.hide()
            elif os.path.isfile(trailer_name) and trailer_name.endswith('flv'):
                self.ui.synopsis.resize(321, self.ui.synopsis.height())
                self.ui.frame.show()
                if self.player.go(trailer_name):
                    self.trailer = 1
                elif self.player.go(trailer_name):
                    self.trailer = 1
                else:
                    self.trailer = 0
            else:
                self.ui.synopsis.resize(661, self.ui.synopsis.height())
                self.ui.frame.hide()
                self.trailer = 0
                print('[setMovieDetail] Warrning: No trailer!')
        except Exception as ex:
            print(ex)


    
    def test_moviedetail(self):
        data = {
            'ctr_movie_detail': {
                'rating': 'NR',
                'dvd_version': '(HD)',
                'trailer_name': '/home/puyodead1/kiosk/var/gui/trailer/1015.flv',
                'is_available': '1',
                'dvd_release_date': '2009-07-07',
                'synopsis': 'ALKSNDFLKAJS, kjlskjdfl,KAJSKLDJFKLAJSLKDFJAS, laskdjflajsdkfj,sd,fjsl,kajlskdfjlskLAKSJDLKFJAALKSNDFLKAJS, kjlskjdfl,KAJSKLDJFKLAJSLKDFJAS, laskdjflajsdkfj,sd,fjsl,kajlskdfjlskLAKSJDLKFJAALKSNDFLKAJS, kjlskjdfl,KAJSKLDJFKLAJSLKDFJAS, laskdjflajsdkfj,sd,fjsl,kajlskdfjlskLAKSJDLKFJAALKSNDFLKAJS, kjlskjdfl,KAJSKLDJFKLAJSLKDFJAS, laskdjflajsdkfj,sd,fjsl,kajlskdfjlskLAKSJDLKFJAALKSNDFLKAJS, kjlskjdfl,KAJSKLDJFKLAJSLKDFJAS, laskdjflajsdkfj,sd,fjsl,kajlskdfjlskLAKSJDLKFJAALKSNDFLKAJS, kjlskjdfl,KAJSKLDJFKLAJSLKDFJAS, laskdjflajsdkfj,sd,fjsl,kajlskdfjlskLAKSJDLKFJALAKSJDLKFJALKSNDFLKAJS, kjlskjdfl,KAJSKLDJFKLAJSLKDFJAS, laskdjflajsdkfj,sd,fjsl,kajlskdfjlskLAKSJDLKFJALKSNDFLKAJS, kjlskjdfl,KAJSKLDJFKLAJSLKDFJAS, laskdjflajsdkfj,sd,fjsl,kajlskdfjlsk',
                'buy_price': '',
                'rent_price': '30.00',
                'directors': 'John Wayne Stevenson, Mark Randolph',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/36986.jpg',
                'starring': 'LAKSJDLKFJALKSNDFLKAJS, kjlskjdfl,KAJSKLDJFKLAJSLKDFJAS, laskdjflajsdkfj,sd,fjsl,kajlskdfjlsk',
                'genre': 'Action/Adventure',
                'movie_title': 'Border Town (2009)NDFLKAJjdfl,KAJSKLDJFKLAJS',
                'feature': [
                    {
                        'Réalisateurs': 'Lee Daniels' },
                    {
                        'Classification': 'R' },
                    {
                        'Genre': 'Drama' },
                    {
                        'Date de sortie': '2010-03-09' },
                    {
                        'Rôles principaux': "Mo'Nique , Paula Patton, Mariah Carey, Gabourey Sidibe, Sherri Shepherd,  Sherri Shepherd, Sherri Shepherd, Sherri Shepherd" }],
                'is_bluray': '1' } }
        self.ui.ctr_movie_detail.setMovieDetail(data)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_en.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    form = DiscDetailForm()
    form.test_moviedetail()
    form.show()
    form.ui.mask_coming_soon_flag.show()
    sys.exit(app.exec_())

