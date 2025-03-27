# Source Generated with Decompyle++
# File: returnManuallyTakeInForm.pyc (Python 2.5)

'''
ReturnTakeInForm
2009-07-29 created by Mavis
'''
import sys
from PyQt4 import QtCore, QtGui
from return_manually_ui import Ui_return_manually_Form
import config
from component import btnBack, btnCancel, btnFinish, SWF_insert, SWF_vomit, SWF_robot_send, Return_messageBox, ctrButton, featureList, numKeyboard, virtualComponent, messageBox, DiscOutList
from squery import socketQuery
import os
import trace

class ReturnManuallyTakeInForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_return_manually_Form()
        self.ui.setupUi(self)
        self.ui.frame.setStyleSheet('border: 2px solid #0153b0; border-radius: 5px')
        self.setGeometry(0, 0, 768, 1024)
        self.setFixedSize(768, 1024)
        self.sq = socketQuery()
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_return)))
        self.setPalette(palette)
        lw = QtGui.QWidget(self)
        lw.setGeometry(91, self.ui.txt_return_label.y() + self.ui.txt_return_label.height() + 50, 586, 860)
        self.ui.swf_send_disc = SWF_robot_send(lw)
        self.ui.swf_insert = SWF_insert(lw)
        self.ui.swf_vomit_dvd = SWF_vomit(lw)
        self.ui.swf_vomit_dvd.hide()
        self.ui.swf_send_disc.hide()
        self.ui.swf_insert.hide()
        style = 'color: white; font: bold italic 30px; border-style: outset; background-image: url(' + config.pic_btn_config_red + ')'
        style_btn_frame = 'QPushButton{border-style: outset; border-width: 2px; border-radius: 4px;font:16px; border-color: #2d78a0; padding: 4px; }QPushButton:disabled{border-color:gray;}'
        style_title = 'font: bold 20px; color: black'
        self.ui.btn_cancel = btnCancel(self, 'ReturnManuallyTakeInForm')
        self.ui.btn_submit = ctrButton(self, 'ReturnManuallyTakeInForm', 'btn_submit', QtGui.QApplication.translate('Form', 'Submit', None, QtGui.QApplication.UnicodeUTF8), 159, 68, config.style_ctrBtn)
        self.ui.ReturnTakeInForm_ctr_message_box = Return_messageBox('ReturnManuallyTakeInForm', self)
        self.feature = featureList(self)
        self.feature.setGeometry(QtCore.QRect(160, 190, 532, 200))
        self.feature.setFixedSize(532, 180)
        self.icon_dvd = QtGui.QLabel(self)
        self.icon_dvd.setGeometry(QtCore.QRect(60, 360, 100, 45))
        self.icon_dvd.setObjectName('icon_dvd')
        self.ui.movie_pic = QtGui.QLabel(self)
        self.ui.movie_pic.setGeometry(QtCore.QRect(60, 190, 100, 150))
        self.ui.movie_pic.setMinimumSize(QtCore.QSize(100, 150))
        self.ui.movie_pic.setMaximumSize(QtCore.QSize(100, 150))
        self.ui.movie_pic.setScaledContents(True)
        self.ui.movie_pic.setObjectName('movie_pic')
        self.ui.ctr_movie_detail = virtualComponent(self)
        self.group = QtGui.QGroupBox(self)
        style_group = 'QGroupBox {                              border-width:2px;                              border-style:solid;                              border-color:#0153b0;                              margin-top: 1.0ex;                              padding:6px;                              font:bold 20px;                              }                              QGroupBox::title {                              subcontrol-origin: margin;                              subcontrol-position: top left;                              left:25px;                              margin-left: 0px;                              padding:1px;                              } '
        self.group.setStyleSheet(style_group)
        self.group.setFlat(True)
        self.group.setTitle(QtGui.QApplication.translate('Form', 'Charge', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.disc_out_list = DiscOutList(self, 'ReturnManuallyTakeInForm', 'disc_out_list')
        self.ui.radio_by_day = QtGui.QPushButton(QtGui.QApplication.translate('Form', 'By Day', None, QtGui.QApplication.UnicodeUTF8))
        style_radio_button = 'background:transparent;font:bold 20px;border:none;'
        self.ui.radio_by_day.setStyleSheet(style_radio_button)
        QtCore.QObject.connect(self.ui.radio_by_day, QtCore.SIGNAL('clicked()'), self.by_day_click)
        self.ui.radio_by_day.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.radio_by_amount = QtGui.QPushButton(QtGui.QApplication.translate('Form', 'By Amount', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.radio_by_amount.setStyleSheet(style_radio_button)
        QtCore.QObject.connect(self.ui.radio_by_amount, QtCore.SIGNAL('clicked()'), self.by_amount_click)
        self.ui.radio_by_amount.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.day = QtGui.QPushButton()
        self.ui.day.setStyleSheet(style_btn_frame + style_title)
        self.ui.day.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.ui.day, QtCore.SIGNAL('clicked()'), self.dayClicked)
        self.ui.amount = QtGui.QPushButton()
        self.ui.amount.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.amount.setStyleSheet(style_btn_frame + style_title)
        QtCore.QObject.connect(self.ui.amount, QtCore.SIGNAL('clicked()'), self.amountClicked)
        self.ui.day_msg = QtGui.QLabel('(Amount:$0)')
        self.ui.day_msg.setStyleSheet('font:16px;')
        self.ui.amount_msg = QtGui.QLabel('(Include Tax)')
        self.ui.amount_msg.setStyleSheet('font:16px;')
        layout = QtGui.QVBoxLayout(lw)
        layout.addSpacing(100)
        layout.addWidget(self.ui.swf_send_disc, 1)
        layout.addWidget(self.ui.swf_insert, 1)
        layout.addWidget(self.ui.swf_vomit_dvd, 1)
        layout.setAlignment(self.ui.swf_send_disc, QtCore.Qt.AlignCenter)
        layout.setAlignment(self.ui.swf_insert, QtCore.Qt.AlignCenter)
        layout.setAlignment(self.ui.swf_vomit_dvd, QtCore.Qt.AlignCenter)
        lw.setLayout(layout)
        self.ui.txtbox_msg.setGeometry(90, 120, 569, 200)
        grid = QtGui.QGridLayout(self.group)
        grid.addWidget(self.ui.radio_by_day, 0, 0, QtCore.Qt.AlignLeft)
        grid.addWidget(self.ui.day, 0, 1)
        grid.addWidget(self.ui.day_msg, 0, 2)
        grid.addWidget(self.ui.radio_by_amount, 1, 0, QtCore.Qt.AlignLeft)
        grid.addWidget(self.ui.amount, 1, 1)
        grid.addWidget(self.ui.amount_msg, 1, 2)
        self.group.setLayout(grid)
        self.group.setGeometry(50, 440, 660, 190)
        self.ui.disc_out_list.move(30, 320)
        self.ui.disc_out_list.hide()
        self.ui.btn_cancel.setGeometry(580, 20, 160, 68)
        self.ui.btn_submit.setGeometry(500, 900, 159, 68)
        self.keyboard_1 = numKeyboard('ReturnManuallyTakeInForm', self, flag = 0)
        self.keyboard_1.hide()
        self.keyboard_2 = numKeyboard('ReturnManuallyTakeInForm', self, flag = 1)
        self.keyboard_2.hide()
        self.ui.ReturnManuallyTakeInForm_ctr_message_box = messageBox('ReturnManuallyTakeInForm', self)
        self.ui.ReturnManuallyTakeInForm_ctr_message_box.hide()

    
    def clearDetail(self):
        self.feature.setList([])
        self.icon_dvd.setPixmap(QtGui.QPixmap(''))
        self.ui.movie_pic.setPixmap(QtGui.QPixmap(''))
        self.ui.frame.setStyleSheet('border: 2px solid white; border-radius: 5px')
        self.ui.frame.hide()
        self.group.hide()
        self.update()

    
    def setMovieDetail(self, data):
        if not data:
            print('[setMovieDetail] Error: data can not be NULL!')
            return -1
        
        
        try:
            self.feature.setList(data['feature'])
            self.ui.frame.setStyleSheet('border: 2px solid #0153b0; border-radius: 5px')
            self.ui.frame.show()
            self.group.show()
        except Exception:
            ex = None
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
                
            
            self.icon_dvd.setPixmap(QtGui.QPixmap(pixmap))
        except Exception:
            ex = None
            print(ex)

        if os.path.isfile(data['movie_pic']):
            self.ui.movie_pic.setPixmap(QtGui.QPixmap(data['movie_pic']))
        else:
            print('[setMovieDetail] Warrning: pic not found!')

    
    def by_day_click(self):
        self.ui.radio_by_day.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_available_yes)))
        self.ui.radio_by_amount.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_unselect)))
        self.ui.amount.setDisabled(True)
        self.ui.day.setDisabled(False)
        self.keyboard_2.close()
        data = { }
        data['wid'] = 'ReturnManuallyTakeInForm'
        data['cid'] = 'radio_by_day'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        self.sq.send(data)

    
    def by_amount_click(self):
        self.ui.day.setDisabled(True)
        self.ui.amount.setDisabled(False)
        self.ui.radio_by_amount.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_available_yes)))
        self.ui.radio_by_day.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_unselect)))
        self.keyboard_1.close()
        data = { }
        data['wid'] = 'ReturnManuallyTakeInForm'
        data['cid'] = 'radio_by_amount'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        self.sq.send(data)

    
    def dayClicked(self):
        self.keyboard_1.show()
        self.keyboard_2.hide()

    
    def amountClicked(self):
        self.keyboard_2.show()
        self.keyboard_1.hide()

    
    def hideEvent(self, event):
        self.ui.ReturnManuallyTakeInForm_ctr_message_box.hide()
        self.keyboard_1.close()
        self.keyboard_2.close()
        self.hide()

    
    def showEvent(self, event):
        self.ui.retranslateUi('')
        self.ui.btn_cancel.reset()
        self.ui.radio_by_day.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_unselect)))
        self.ui.radio_by_amount.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_unselect)))
        self.ui.radio_by_day.setChecked(True)
        self.by_day_click()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    import os
    config.transFile = 'trans_es.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
    
    form = ReturnManuallyTakeInForm()
    form.show()
    data = [
        {
            'feature': [
                {
                    'name': 'sk' },
                {
                    'time': '2012' },
                {
                    'aa': 'a' }],
            'rfid': '1',
            'movie_pic': '/home/mm/var/images/goodsrec/images/735.jpg',
            'is_bluray': '2' },
        {
            'feature': [
                {
                    'name': 'st' },
                {
                    'time': '2013' },
                {
                    'aa': 'b' }],
            'rfid': '1',
            'movie_pic': '/home/mm/var/images/goodsrec/images/737.jpg',
            'is_bluray': '2' },
        {
            'feature': [
                {
                    'name': 'sw' },
                {
                    'time': '2014' },
                {
                    'aa': 'c' }],
            'rfid': '1',
            'movie_pic': '/home/mm/var/images/goodsrec/images/738.jpg',
            'is_bluray': '2' },
        {
            'feature': [
                {
                    'name': 'sw' },
                {
                    'time': '2014' },
                {
                    'aa': 'd' }],
            'rfid': '1',
            'movie_pic': '/home/mm/var/images/goodsrec/images/738.jpg',
            'is_bluray': '2' },
        {
            'feature': [
                {
                    'name': 'sw' },
                {
                    'time': '2014' },
                {
                    'aa': 'e' }],
            'rfid': '1',
            'movie_pic': '/home/mm/var/images/goodsrec/images/738.jpg',
            'is_bluray': '2' },
        {
            'feature': [
                {
                    'name': 'sj' },
                {
                    'time': '2015' },
                {
                    'aa': 'f' }],
            'rfid': '1',
            'movie_pic': '/home/mm/var/images/goodsrec/images/740.jpg',
            'is_bluray': '2' }]
    form.ui.disc_out_list.setDiscList(data)
    sys.exit(app.exec_())

