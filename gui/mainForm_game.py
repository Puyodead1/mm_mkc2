# Source Generated with Decompyle++
# File: mainForm_game.pyc (Python 2.5)

'''
MainForm is the main window for Game. 
2010-05-11 created by Mavis
'''
import sys
from PyQt4 import QtCore, QtGui
from main_ui import Ui_MainUiForm
import config
import os
from component import gifButton, ctrButton, virtualComponent
from squery import socketQuery

class MainForm(QtGui.QMainWindow):
    
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainUiForm()
        self.ui.setupUi(self)
        if not os.path.isfile(config.pic_bg_start):
            print('CAN NOT FIND THE PIC: %s' % config.pic_bg_start)
        else:
            palette = QtGui.QPalette()
            palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_start)))
            self.setPalette(palette)
        self.btn_rent = gifButton(self, 'btn_rent', config.pic_btn_rent_bg, '', 1, 238, 423)
        self.btn_return = gifButton(self, 'btn_return', config.pic_btn_return_bg, '', 1, 238, 423)
        self.btn_pickup = gifButton(self, 'btn_pickup', config.pic_btn_pickup_bg, '', 1, 238, 423)
        self.ui.hboxlayout.addWidget(self.btn_rent)
        self.ui.hboxlayout.addWidget(self.btn_return)
        self.ui.hboxlayout.addWidget(self.btn_pickup)
        self.ui.logo.setMaximumHeight(100)
        self.ui.logo.setAlignment(QtCore.Qt.AlignCenter)
        if os.path.isfile(config.pic_logo):
            pic = QtGui.QPixmap(config.pic_logo).scaled(580, 100, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.ui.logo.setPixmap(pic)
        
        self.ui.txt_msg = QtGui.QLabel()
        self.ui.txt_msg.setStyleSheet('font: bold 32px; color: white')
        self.ui.txt_msg.setMaximumHeight(60)
        self.ui.txt_msg.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.btn_wii = IconButton(config.pic_main_wii, 'btn_wii')
        self.ui.btn_ps3 = IconButton(config.pic_main_playstation, 'btn_ps3')
        self.ui.btn_xbox = IconButton(config.pic_main_xbox, 'btn_xbox')
        btnLayout = QtGui.QHBoxLayout()
        btnLayout.setContentsMargins(0, 0, 0, 0)
        btnLayout.addWidget(self.ui.btn_xbox)
        btnLayout.addWidget(self.ui.btn_ps3)
        btnLayout.addWidget(self.ui.btn_wii)
        layout = QtGui.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui.logo)
        layout.addWidget(self.ui.txt_msg)
        layout.addLayout(btnLayout)
        w = QtGui.QWidget(self)
        w.setGeometry(60, 60, 648, 410)
        w.setLayout(layout)
        self.ui.test_mode_flag = QtGui.QLabel(self)
        self.ui.test_mode_flag.setGeometry(50, 375, 678, 270)
        self.ui.test_mode_flag.setPixmap(QtGui.QPixmap(config.pic_test_flag))
        self.ui.test_mode_flag.hide()
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
        self.btn_rent.setStyleSheet('QPushButton {border-style: outset; background-image: url(' + config.pic_btn_rent_bg + '); }')
        self.btn_return.setStyleSheet('QPushButton {border-style: outset; background-image: url(' + config.pic_btn_return_bg + '); }')
        self.btn_pickup.setStyleSheet('QPushButton {border-style: outset; background-image: url(' + config.pic_btn_pickup_bg + '); }')
        self.resetLang()

    
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
            
        



class IconButton(QtGui.QPushButton):
    
    def __init__(self, icon, cid, wid = 'MainForm', parent = None, id = '', width = 200, height = 240):
        QtGui.QPushButton.__init__(self, parent)
        self.setFixedSize(width, height)
        self.setIconSize(QtCore.QSize(width, height))
        self.setIcon(QtGui.QIcon(QtGui.QPixmap(icon)))
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet('QPushButton {border-style: outset} QPushButton:pressed {background-color:qradialgradient(cx:0.5, cy:0.6, fx:0.5, fy:0.6, radius:0.4, stop:0 #f0e090, stop:1 transparent);}')
        self.sq = socketQuery()
        self.wid = wid
        self.cid = cid
        self.param = { }
        if id:
            self.param = {
                self.cid: {
                    'genre': id } }
        
        self.connect(self, QtCore.SIGNAL('clicked()'), self.sendMsg)

    
    def sendMsg(self):
        self.sq.send({
            'wid': self.wid,
            'cid': self.cid,
            'type': 'EVENT',
            'EVENT': 'EVENT_MOUSE_CLICK',
            'param_info': self.param })


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_es.qm'
    mainf = MainForm()
    mainf.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
    mainf.show()
    mainf.ui.ctr_btn_lang.initLanguage({
        'ctr_btn_lang': [
            'en',
            'fr_FR',
            'es'] })
    mainf.ui.btn_en.show()
    mainf.ui.btn_es.show()
    mainf.ui.txt_msg.setText('$2.99 Game Rentals')
    sys.exit(app.exec_())

