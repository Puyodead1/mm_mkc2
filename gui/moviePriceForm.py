# Source Generated with Decompyle++
# File: moviePriceForm.pyc (Python 2.5)

'''
DiscPriceForm for movie price detail
2009-07-03 created by Mavis
'''
import sys
import os
import config
import component
from PyQt4 import QtCore, QtGui
from movie_price_ui import Ui_MoviePriceForm
from squery import socketQuery

class DiscPriceForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MoviePriceForm()
        self.ui.setupUi(self)
        self.ui.frame_2.setStyleSheet('border: 2px solid #0153b0; border-radius: 5px')
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_movie)))
        self.setPalette(palette)
        self.ui.ctr_btn_center = component.btnCenter(self, 'DiscPriceForm')
        self.ui.ctr_btn_center.hide()
        self.ui.btn_back = component.btnBack(self, 'DiscPriceForm')
        self.ui.btn_cancel = component.btnCancel(self, 'DiscPriceForm')
        self.ui.btn_cancel.setGeometry(580, 20, 160, 68)
        self.ui.btn_buy = component.ctrButton(self, 'DiscPriceForm', 'btn_buy', QtGui.QApplication.translate('Form', 'Buy', None, QtGui.QApplication.UnicodeUTF8), 160, 68, config.btnGreenStyle + '; background-image: url(' + config.pic_btn_yellow + ')')
        self.ui.btn_rent = component.ctrButton(self, 'DiscPriceForm', 'btn_rent', QtGui.QApplication.translate('Form', 'Rent', None, QtGui.QApplication.UnicodeUTF8), 160, 68, config.btnGreenStyle)
        self.ui.hboxlayout.addWidget(self.ui.btn_back)
        self.ui.hboxlayout.addWidget(self.ui.btn_buy)
        self.ui.hboxlayout.addWidget(self.ui.btn_rent)
        self.feature = component.featureList(self)
        self.feature.setGeometry(180, 210, 532, 185)
        self.ui.terms.setStyleSheet(config.scroll_style)
        self.ui.ctr_movie_price = component.virtualComponent(self)
        self.ui.DiscPriceForm_ctr_message_box = component.messageBox('DiscPriceForm', self)
        self.sq = socketQuery()
        self.ui.DiscPriceForm_ctr_all_keyboard = component.allKeyboard('DiscPriceForm', self)
        self.ui.DiscPriceForm_ctr_all_keyboard.setGeometry(15, 250, 720, 516)
        self.ui.DiscPriceForm_ctr_all_keyboard.hide()

    
    def setMoviePrice(self, data):
        if not data['ctr_movie_price']:
            print('[setMovieDetail] Error: data can not be NULL!')
            return -1
        
        data = data['ctr_movie_price']
        self.ui.movie_title.setText(data['movie_title'])
        self.ui.dvd_version.setText(data['dvd_version'])
        self.ui.terms.setText(data['terms'])
        if os.path.isfile(data['movie_pic']):
            self.ui.movie_pic.setPixmap(QtGui.QPixmap(data['movie_pic']))
        else:
            print('[setMoviePrice] Error: movie pic not found!')
        
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


    
    def showEvent(self, event):
        self.ui.ctr_btn_center.init()
        self.ui.retranslateUi('')
        self.ui.btn_back.reset()
        self.ui.btn_cancel.reset()
        self.ui.btn_buy.setText(QtGui.QApplication.translate('Form', 'Buy', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_rent.setText(QtGui.QApplication.translate('Form', 'Rent', None, QtGui.QApplication.UnicodeUTF8))

    
    def hideEvent(self, event):
        self.ui.DiscPriceForm_ctr_message_box.hide()
        self.hide()

    
    def test_moviedetail(self):
        data = {
            'ctr_movie_price': {
                'terms': 'Terms and Conditions\nTo rent a DVD, Video Game or other product from this Automated Kiosk you must swipe your credit card.\nBy swiping your credit card you certify that you are the legal owner of the card that you are at least 18 years of age, and that you agree to all of the Terms and Conditions listed herein. If you are under the age of 18 you may only use this Kiosk with the express permission of a Parent or Guardian.\n\n1. You agree to pay the rental rates as listed on the kiosk screen.\n2. If we are required to collect Sales Taxes in your area, either on rental, purchase or applicable Maximum Replacement Cost, they are additional to the rental price and you understand and agree that they are automatically applied to your credit card over and above the value of the rental.\n3. You understand and agree that your credit card will be charged an additional period fee, as displayed on the kiosk screen, for each additional period you keep the DVD, Video Game or other product beyond the return time.\n4. The Rental Day Limit allowed for a rental is  ___  after which the rental is converted into a sale.\n                a. DVD - $30.00\n                b. Blu-Ray - $35.00\n                c. Video Game - $45.00\n5. If the rental day limit has been reached, you have purchased the DVD, or Video Game or other product and do not need to return it.  If you return the DVD, Video Game, or other product after the replacement cost has been charged, you agree and understand that no refund will be issued, but that we will mail that product to you upon written request and payment of delivery charges.\n6. If the DVD, Video Game or other product is returned Damaged, without the original box or other product or information included in the box you understand and agree that your Payment Card will be assessed additional charges up to the Maximum Replacement Cost of that DVD, Video Game or other product.\n7. If you reserve a DVD online, the reservation period begins immediately.  You have 12 hours to pick up your reserved DVD(s).  Your reservation will expire after 12 hours and you will be charged a one night rental fee for each reserved DVD.\n8. If you have questions, comments or concerns, please contact: the owner / operator.',
                'dvd_version': '(Blu-ray)',
                'movie_title': 'Night Train (2009) Automated Kiosk you must swipe your credit card.',
                'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/111207_big.jpg',
                'feature': [
                    {
                        'price_plan_text': 'First 1 Hours Fee $10\n or Each 2 Hours Fee $100' },
                    {
                        'sale_price': '39.00' },
                    {
                        'rentals_tax': '6.825%' },
                    {
                        'sales_tax': '8.25%' }],
                'is_bluray': '1' } }
        self.ui.ctr_movie_price.setMoviePrice(data)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_en.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    form = DiscPriceForm()
    form.test_moviedetail()
    form.show()
    sys.exit(app.exec_())

