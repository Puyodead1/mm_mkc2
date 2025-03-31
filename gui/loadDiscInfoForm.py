# Source Generated with Decompyle++
# File: loadDiscInfoForm.pyc (Python 2.5)

'''
LoadDiscInfoForm
2009-07-20 created by Mavis
'''
import os
import sys
import config
import component
import traceback
import re
from PyQt4 import QtCore, QtGui
from loadDiscInfoForm_ui import Ui_loadDiskInfoForm
from squery import socketQuery

def fmtMoney(money):
    newMoney = '%.2f' % round(float(money), 2)
    return newMoney


class LoadDiscInfoForm(QtGui.QMainWindow):
    
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_loadDiskInfoForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_load)))
        self.setPalette(palette)
        self.sq = socketQuery()
        self.ui.ctr_movie_info = component.virtualComponent(self)
        self.ui.btn_logout = component.btnLogout(self, 'LoadDiscInfoForm')
        self.ui.btn_logout.setGeometry(580, 20, 160, 68)
        self.ui.btn_back = component.btnBack(self, 'LoadDiscInfoForm')
        self.ui.btn_ok = QtGui.QPushButton(QtGui.QApplication.translate('Form', 'Next', None, QtGui.QApplication.UnicodeUTF8), self)
        self.ui.btn_ok.setFixedSize(159, 68)
        self.ui.btn_ok.setStyleSheet(config.btnGreenStyle)
        self.btn_confirm = QtGui.QPushButton(QtGui.QApplication.translate('Form', 'Confirm', None, QtGui.QApplication.UnicodeUTF8), self)
        self.btn_confirm.setFixedSize(159, 68)
        self.btn_confirm.setStyleSheet(config.btnGreenStyle)
        self.btn_confirm.hide()
        self.btn_back2 = QtGui.QPushButton(QtGui.QApplication.translate('Form', 'Cancel', None, QtGui.QApplication.UnicodeUTF8), self)
        self.btn_back2.setFixedSize(159, 68)
        self.btn_back2.setStyleSheet('color: white; font: bold italic 30px; border-style: outset; background-image: url(' + config.pic_btn_red + ')')
        self.btn_back2.hide()
        self.ui.hboxlayout.addWidget(self.ui.btn_back, 0)
        self.ui.hboxlayout.addWidget(self.btn_back2, 0)
        self.ui.hboxlayout.addWidget(self.ui.btn_ok, 1)
        self.ui.hboxlayout.addWidget(self.btn_confirm, 1)
        self.px = (768 - config.unload_list_width) / 2
        self.py = 390
        self.pw = config.unload_list_width
        self.ph = 480
        self.slot_number = ''
        self.accept_special_price_plan = ''
        self.plan_id = '0'
        styleBig = 'font: bold 20px; color:#bb0000'
        styleSmall = 'font: bold 16px; color:#bb0000'
        styleSlot = 'font: bold 20px; color:#0060a0'
        line = QtGui.QLabel(self)
        line.setGeometry(self.px, self.py - 20, self.pw, 5)
        line.setPixmap(QtGui.QPixmap(config.pic_btm_table))
        self.ui.ctr_slot_id_list = component.discInfo(self)
        self.ui.ctr_slot_id_list.setGeometry(self.px, self.py, self.pw, self.ph)
        lineb = QtGui.QLabel(self)
        lineb.setGeometry(self.px, self.py + self.ph - 1, self.pw, 10)
        lineb.setPixmap(QtGui.QPixmap(config.pic_btm_table))
        self.ui.txt_price_plan = QtGui.QLabel(self.ui.ctr_slot_id_list.verticalLayout)
        self.ui.txt_price_plan.setMinimumSize(self.pw - 400, self.ph / 7)
        self.ui.txt_price_plan.setStyleSheet(styleSmall)
        self.ui.ctr_slot_id_list.hboxlayout1.addWidget(self.ui.txt_price_plan)
        self.ui.txt_sale_price = QtGui.QLabel(self.ui.ctr_slot_id_list.verticalLayout)
        self.ui.txt_sale_price.setMinimumHeight(73)
        self.ui.txt_sale_price.setStyleSheet(styleBig)
        self.ui.ctr_slot_id_list.hboxlayout2.addWidget(self.ui.txt_sale_price)
        self._sale_price = ''
        self._convert_price = ''
        self._cost = ''
        self.ui.txt_convert_price = QtGui.QLabel(self.ui.ctr_slot_id_list.verticalLayout)
        self.ui.txt_convert_price.setMinimumHeight(75)
        self.ui.txt_convert_price.setStyleSheet(styleBig)
        self.ui.ctr_slot_id_list.hboxlayout3.addWidget(self.ui.txt_convert_price)
        self.ui.txt_cost = QtGui.QLabel(self.ui.ctr_slot_id_list.verticalLayout)
        self.ui.txt_cost.setStyleSheet(styleBig)
        self.ui.txt_cost.setMinimumHeight(73)
        self.ui.ctr_slot_id_list.hboxlayout4.addWidget(self.ui.txt_cost)
        self.ui.txt_upc = QtGui.QLabel(self.ui.ctr_slot_id_list.verticalLayout)
        self.ui.txt_upc.setMinimumHeight(70)
        self.ui.txt_upc.setStyleSheet(styleBig)
        self.ui.ctr_slot_id_list.hboxlayout5.addWidget(self.ui.txt_upc)
        self.ui.txt_special_price_plan = QtGui.QLabel(self)
        self.ui.txt_price_plan_id = QtGui.QLabel(self)
        self.ui.txt_special_price_plan.resize(0, 0)
        self.ui.txt_price_plan_id.resize(0, 0)
        label_h = 40
        self.layout = QtGui.QWidget(self)
        self.layout.setGeometry(QtCore.QRect(self.px, self.py, self.pw - 50, label_h))
        hbox = QtGui.QHBoxLayout(self.layout)
        self.label_left = QtGui.QLabel(self)
        self.label_left.setStyleSheet(styleSlot)
        hbox.addWidget(self.label_left)
        self.label_right = QtGui.QLabel(QtGui.QApplication.translate('Load', ' Default: ', None, QtGui.QApplication.UnicodeUTF8), self)
        self.label_right.setStyleSheet(styleSlot)
        hbox.addWidget(self.label_right)
        self.label_default = QtGui.QLabel(self)
        self.label_default.setStyleSheet(styleSlot)
        hbox.addWidget(self.label_default)
        hbox.setAlignment(self.label_right, QtCore.Qt.AlignRight)
        hbox.setAlignment(self.label_default, QtCore.Qt.AlignRight)
        self.layout.hide()
        self.numKeyb = component.numKeyboard('LoadDiscInfoForm', self, self.px, self.py + label_h)
        self.numKeyb.hide()
        self.ui.ctr_slot_list = component.TextList(self, 221, 416)
        self.ui.ctr_slot_list.setGeometry(self.px + config.bg_kb_width + 20, self.py + label_h + 4, 221, 416)
        self.ui.ctr_slot_list.hide()
        self.ui.ctr_plan_list = component.PricePlan(self)
        self.ui.ctr_plan_list.setGeometry(self.px, self.py + label_h + 4, self.pw, 75 * 5 + 60 + 2)
        self.ui.ctr_plan_list.hide()
        self.ui.ctr_upc_list = component.UpcList(self)
        self.ui.ctr_upc_list.setGeometry(self.px, self.py + label_h, self.pw, self.ph - label_h)
        self.ui.ctr_upc_list.hide()
        self.numKeyf = component.numKeyboard('LoadDiscInfoForm', self, (self.pw - config.bg_kb_width) / 2, self.py + label_h, config.bg_kb_width, config.bg_kb_height, 4, 1)
        self.numKeyf.hide()
        self.mbox = component.messageBox('LoadDiscInfoForm', self)
        self.mbox.setGeometry((768 - config.messageBox_width) / 2, self.py, config.messageBox_width, config.messageBox_height)
        QtCore.QObject.disconnect(self.numKeyf.btn_ok, QtCore.SIGNAL('clicked()'), self.numKeyf.kb_ok_click)
        QtCore.QObject.connect(self.numKeyf.btn_ok, QtCore.SIGNAL('clicked()'), self.btn_confirm_click)
        QtCore.QObject.connect(self.ui.btn_ok, QtCore.SIGNAL('clicked()'), self.btn_ok_click)
        QtCore.QObject.connect(self.ui.btn_ok, QtCore.SIGNAL('pressed()'), self.btn_ok_pressed)
        QtCore.QObject.connect(self.ui.ctr_slot_id_list.btn_0, QtCore.SIGNAL('clicked()'), self.btn_slot_number_edit_click)
        QtCore.QObject.connect(self.ui.ctr_slot_id_list.btn_1, QtCore.SIGNAL('clicked()'), self.btn_price_plan_edit_click)
        QtCore.QObject.connect(self.ui.ctr_slot_id_list.btn_2, QtCore.SIGNAL('clicked()'), self.sale_price_edit)
        QtCore.QObject.connect(self.ui.ctr_slot_id_list.btn_3, QtCore.SIGNAL('clicked()'), self.convert_price_edit)
        QtCore.QObject.connect(self.ui.ctr_slot_id_list.btn_4, QtCore.SIGNAL('clicked()'), self.cost_edit)
        QtCore.QObject.connect(self.ui.ctr_slot_id_list.btn_5, QtCore.SIGNAL('clicked()'), self.btn_upc_edit_click)
        QtCore.QObject.connect(self.ui.ctr_slot_id_list.btn_b, QtCore.SIGNAL('clicked()'), self.setChecked_b)
        QtCore.QObject.connect(self.ui.ctr_slot_id_list.btn_f, QtCore.SIGNAL('clicked()'), self.setChecked_f)
        QtCore.QObject.connect(self.btn_confirm, QtCore.SIGNAL('clicked()'), self.btn_confirm_click)
        QtCore.QObject.connect(self.btn_back2, QtCore.SIGNAL('clicked()'), self.btn_back2_click)
        QtCore.QObject.connect(self.ui.ctr_slot_list.table, QtCore.SIGNAL('itemClicked(QTableWidgetItem*)'), self.ctr_slot_list_click)
        QtCore.QObject.connect(self.numKeyb.btn_ok, QtCore.SIGNAL('clicked()'), self.btn_confirm_click)
        self.label_text = [
            QtGui.QApplication.translate('Form', ' Please select a price plan ', None, QtGui.QApplication.UnicodeUTF8),
            QtGui.QApplication.translate('Form', ' Please enter the slot ID ', None, QtGui.QApplication.UnicodeUTF8),
            QtGui.QApplication.translate('Form', ' Please enter the new price(sale) ', None, QtGui.QApplication.UnicodeUTF8),
            QtGui.QApplication.translate('Form', ' Please enter the new price(convert) ', None, QtGui.QApplication.UnicodeUTF8),
            QtGui.QApplication.translate('Form', ' Please enter the new cost ', None, QtGui.QApplication.UnicodeUTF8),
            QtGui.QApplication.translate('Form', ' Please select a UPC', None, QtGui.QApplication.UnicodeUTF8)]

    
    def btn_confirm_click(self):
        if self.edit == 0:
            if self.slot_id_confirmed() == -1:
                return None
            else:
                self.ui.ctr_slot_list.hide()
                self.numKeyb.close()
        elif self.edit == 1:
            crow = self.ui.ctr_plan_list.table.currentRow()
            self.ui.txt_price_plan.setText(self.ui.ctr_plan_list.table.item(crow, 1).text())
            self.plan_id = str(self.ui.ctr_plan_list.table.item(crow, 0).text())[5:]
            self.ui.ctr_plan_list.hide()
            if self.ui.ctr_plan_list.special:
                self.accept_special_price_plan = self.ui.ctr_plan_list.special
            
        elif self.edit == 2 and self.edit == 3 or self.edit == 4:
            p = re.compile('^\\d{1,4}(\\.\\d+)?$')
            if p.match(self.numKeyf.lineedit.text().toLocal8Bit().data()):
                self.keyb_ok_click()
            else:
                self.numKeyf.lineedit.setText('Invalid Price')
                self.numKeyf.lineedit.selectAll()
                return None
        elif self.edit == 5:
            upc = self.ui.ctr_upc_list.table.item(self.ui.ctr_upc_list.table.currentRow(), 0).text()
            self.ui.txt_upc.setText(upc)
            self.ui.ctr_upc_list.hide()
            data = { }
            data['wid'] = 'LoadDiscInfoForm'
            data['cid'] = 'btn_upc_ok'
            data['type'] = 'EVENT'
            data['EVENT'] = 'EVENT_MOUSE_CLICK'
            data['param_info'] = { }
            data['param_info']['btn_upc_ok'] = { }
            data['param_info']['btn_upc_ok']['upc'] = str(upc)
            self.sq.send(data)
        
        self.ui.ctr_slot_id_list.show()
        self.back2Main(1)

    
    def back2Main(self, back = 0):
        if back:
            self.layout.hide()
            self.btn_confirm.hide()
            self.btn_back2.hide()
            self.ui.btn_back.show()
            self.ui.btn_ok.show()
        else:
            self.layout.show()
            self.ui.btn_back.hide()
            self.ui.btn_ok.hide()
            self.btn_confirm.show()
            self.btn_back2.show()

    
    def btn_back2_click(self):
        self.ui.ctr_upc_list.hide()
        self.numKeyf.hide()
        self.numKeyb.hide()
        self.ui.ctr_slot_list.hide()
        self.ui.ctr_plan_list.hide()
        self.btn_confirm.hide()
        self.back2Main(1)
        self.ui.ctr_slot_id_list.show()

    
    def keyb_ok_click(self):
        if self.numKeyf.lineedit.text():
            data = { }
            data['wid'] = 'LoadDiscInfoForm'
            data['cid'] = 'LoadDiscInfoForm' + '_ctr_num_keyboard'
            data['type'] = 'EVENT'
            data['EVENT'] = 'EVENT_MOUSE_CLICK'
            data['param_info'] = { }
            data['param_info'][data['cid']] = { }
            data['param_info'][data['cid']]['type'] = 'ok'
            data['param_info'][data['cid']]['val'] = str(self.numKeyf.lineedit.text())
            self.sq.send(data)
            text = fmtMoney(self.numKeyf.lineedit.text())
            self.numKeyf.lineedit.clear()
            self.numKeyf.close()
            if self.edit == 2:
                self.ui.txt_sale_price.setText(config.symbol + text)
                self._sale_price = text
            elif self.edit == 3:
                self.ui.txt_convert_price.setText(config.symbol + text)
                self._convert_price = text
            elif self.edit == 4:
                self.ui.txt_cost.setText(config.symbol + text)
                self._cost = text
            
        

    
    def ctr_slot_list_click(self, item):
        text = item.text()
        self.numKeyb.lineedit.setText(text)
        self.numKeyb.data = text

    
    def slot_id_confirmed(self):
        if self.numKeyb.data:
            id = self.numKeyb.data
            if self.ui.ctr_slot_list.slotdata.find("'" + id + "'") == -1:
                self.numKeyb.clear()
                self.mbox.show({
                    'message': 'The slot ID is not valid or not empty!',
                    'type': 'alert' })
                self.numKeyb.show()
                return -1
            
            self.ui.ctr_slot_id_list.show()
            if id != self.ui.ctr_slot_id_list.btn_f.text() and id != self.ui.ctr_slot_id_list.btn_b.text():
                if self.ui.ctr_slot_id_list.checkedID == 0:
                    self.ui.ctr_slot_id_list.btn_f.setText(id)
                else:
                    self.ui.ctr_slot_id_list.btn_b.setText(id)
            elif id == self.ui.ctr_slot_id_list.btn_b.text() and self.ui.ctr_slot_id_list.checkedID == 0:
                self.ui.ctr_slot_id_list.btn_b.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_available_yes)))
                self.ui.ctr_slot_id_list.btn_f.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_unselect)))
                self.ui.ctr_slot_id_list.checkedID = 1
            elif id == self.ui.ctr_slot_id_list.btn_f.text() and self.ui.ctr_slot_id_list.checkedID != 0:
                self.ui.ctr_slot_id_list.btn_f.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_available_yes)))
                self.ui.ctr_slot_id_list.btn_b.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_unselect)))
                self.ui.ctr_slot_id_list.checkedID = 0
            
            self.slot_number = id
        

    
    def setChecked_b(self):
        if self.ui.ctr_slot_id_list.checkedID == 0:
            self.ui.ctr_slot_id_list.btn_b.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_available_yes)))
            self.ui.ctr_slot_id_list.btn_f.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_unselect)))
            self.slot_number = self.ui.ctr_slot_id_list.btn_b.text()
            self.ui.ctr_slot_id_list.checkedID = 1
        

    
    def setChecked_f(self):
        if self.ui.ctr_slot_id_list.checkedID != 0:
            self.ui.ctr_slot_id_list.btn_f.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_available_yes)))
            self.ui.ctr_slot_id_list.btn_b.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_unselect)))
            self.slot_number = self.ui.ctr_slot_id_list.btn_f.text()
            self.ui.ctr_slot_id_list.checkedID = 0
        

    
    def setMovieDetail(self, data):
        if not data['ctr_movie_detail']:
            print('[setMovieDetail] Error: data can not be NULL!')
            return -1
        
        data = data['ctr_movie_detail']
        self.ui.movie_title.setText(data['movie_title'])
        self.ui.dvd_version.setText(data['dvd_version'])
        self.ui.genre.setText(data['genre'])
        self.ui.directors.setText(data['directors'])
        self.ui.dvd_release_date.setText(data['dvd_release_date'])
        self.ui.starring.setText(data['starring'])
        self.ui.rating.setText(data['rating'])
        if os.path.isfile(data['movie_pic']):
            self.ui.movie_pic.setPixmap(QtGui.QPixmap(data['movie_pic']))
        else:
            print('[setMovieDetail] Error: movie pic not found!')
        self.setDefaultValues()

    
    def setDefaultValues(self):
        self.default_price_plan_id = self.ui.txt_price_plan_id.text()
        default_sale_price = self.ui.txt_sale_price.text()
        self.default_sale_price = fmtMoney(str(default_sale_price).strip(config.symbol))
        default_convert_price = self.ui.txt_convert_price.text()
        self.default_convert_price = fmtMoney(str(default_convert_price).strip(config.symbol))
        default_cost = self.ui.txt_cost.text()
        self.default_cost = fmtMoney(str(default_cost).strip(config.symbol))
        self.default_upc = self.ui.txt_upc.text()
        self.ui.txt_sale_price.setText(config.symbol + self.default_sale_price)
        self.ui.txt_convert_price.setText(config.symbol + self.default_convert_price)
        self.ui.txt_cost.setText(config.symbol + self.default_cost)
        self._sale_price = self.default_sale_price
        self._convert_price = self.default_convert_price
        self._cost = self.default_cost

    
    def updateLabels(self, left, default):
        self.label_left.setText(left)
        self.label_default.setText(default)
        self.layout.update()

    
    def btn_price_plan_edit_click(self):
        if str(self.plan_id) == '0':
            self.ui.ctr_plan_list.defaultPlanId = self.ui.txt_price_plan_id.text()
        else:
            self.ui.ctr_plan_list.defaultPlanId = self.plan_id
        data = { }
        data['wid'] = 'LoadDiscInfoForm'
        data['cid'] = 'btn_price_plan_edit'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        self.sq.send(data)
        if not (self.accept_special_price_plan):
            self.ui.ctr_plan_list.setSpecial(self.ui.txt_special_price_plan.text())
        
        self.ui.ctr_slot_id_list.hide()
        self.ui.ctr_plan_list.show()
        self.back2Main(0)
        self.updateLabels(self.label_text[0], 'Plan ' + self.ui.ctr_plan_list.defaultPlanId)
        self.edit = 1

    
    def btn_slot_number_edit_click(self):
        data = { }
        data['wid'] = 'LoadDiscInfoForm'
        data['cid'] = 'btn_slot_number_edit'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        self.sq.send(data)
        self.ui.ctr_slot_id_list.hide()
        self.numKeyb.show()
        self.ui.ctr_slot_list.show()
        self.back2Main(0)
        if self.ui.ctr_slot_id_list.checkedID == 0:
            text = self.ui.ctr_slot_id_list.btn_f.text()
        else:
            text = self.ui.ctr_slot_id_list.btn_b.text()
        self.updateLabels(self.label_text[1], text)
        self.edit = 0

    
    def sale_price_edit(self):
        self.ui.ctr_slot_id_list.hide()
        self.numKeyf.show()
        self.updateLabels(self.label_text[2], self.default_sale_price)
        self.back2Main(0)
        self.edit = 2

    
    def convert_price_edit(self):
        self.ui.ctr_slot_id_list.hide()
        self.numKeyf.show()
        self.updateLabels(self.label_text[3], self.default_convert_price)
        self.back2Main(0)
        self.edit = 3

    
    def cost_edit(self):
        self.ui.ctr_slot_id_list.hide()
        self.numKeyf.show()
        self.updateLabels(self.label_text[4], self.default_cost)
        self.back2Main(0)
        self.edit = 4

    
    def btn_upc_edit_click(self):
        self.ui.ctr_upc_list.defaultUpc = self.ui.txt_upc.text()
        data = { }
        data['wid'] = 'LoadDiscInfoForm'
        data['cid'] = 'btn_upc_edit'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        self.sq.send(data)
        self.ui.ctr_slot_id_list.hide()
        self.ui.ctr_upc_list.show()
        self.updateLabels(self.label_text[5], self.ui.ctr_upc_list.defaultUpc)
        self.back2Main(0)
        self.edit = 5

    
    def btn_ok_pressed(self):
        self.ui.btn_ok.setStyleSheet('background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 white, stop:0.6 #3077e0, stop:1 #f0f0f0); color: white; font: bold 30px; border-radius: 8px')

    
    def btn_ok_click(self):
        if self.ui.ctr_slot_id_list.checkedID == 0:
            self.slot_number = str(self.ui.ctr_slot_id_list.btn_f.text())
        else:
            self.slot_number = str(self.ui.ctr_slot_id_list.btn_b.text())
        if str(self.plan_id) == '0':
            self.plan_id = self.ui.txt_price_plan_id.text()
        
        data = { }
        data['wid'] = 'LoadDiscInfoForm'
        data['cid'] = 'btn_ok'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info']['btn_ok'] = { }
        data['param_info']['btn_ok']['slot_number'] = str(self.slot_number)
        data['param_info']['btn_ok']['price_plan'] = str(self.plan_id)
        data['param_info']['btn_ok']['sale_price'] = str(self._sale_price)
        data['param_info']['btn_ok']['convert_price'] = str(self._convert_price)
        data['param_info']['btn_ok']['cost'] = str(self._cost)
        data['param_info']['btn_ok']['upc'] = str(self.ui.txt_upc.text())
        if self.accept_special_price_plan:
            data['param_info']['btn_ok']['accept_special_price_plan'] = str(self.accept_special_price_plan)
        else:
            data['param_info']['btn_ok']['accept_special_price_plan'] = str(self.ui.txt_special_price_plan.text())
        self.sq.send(data)
        self.ui.btn_ok.setStyleSheet(config.btnGreenStyle)

    
    def DiscInfoClear(self):
        self.ui.ctr_slot_list.table.clear()
        self.ui.ctr_plan_list.table.clear()
        self.ui.ctr_upc_list.table.clear()

    
    def hideEvent(self, event):
        self.DiscInfoClear()
        self.btn_back2_click()
        self.mbox.close()
        self.plan_id = '0'
        self.hide()

    
    def showEvent(self, event):
        self.ui.retranslateUi('')
        self.accept_special_price_plan = ''
        self.ui.ctr_plan_list.setSpecial('')
        self.ui.btn_logout.reset()
        self.ui.btn_back.reset()
        self.ui.btn_ok.setText(QtGui.QApplication.translate('Form', 'Next', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_back2.setText(QtGui.QApplication.translate('Form', 'Cancel', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_confirm.setText(QtGui.QApplication.translate('Form', 'Confirm', None, QtGui.QApplication.UnicodeUTF8))
        self.label_right.setText(QtGui.QApplication.translate('Load', ' Default: ', None, QtGui.QApplication.UnicodeUTF8))
        self.label_text = [
            QtGui.QApplication.translate('Form', ' Please select a price plan ', None, QtGui.QApplication.UnicodeUTF8),
            QtGui.QApplication.translate('Form', ' Please enter the slot ID ', None, QtGui.QApplication.UnicodeUTF8),
            QtGui.QApplication.translate('Form', ' Please enter the new price(sale) ', None, QtGui.QApplication.UnicodeUTF8),
            QtGui.QApplication.translate('Form', ' Please enter the new price(convert) ', None, QtGui.QApplication.UnicodeUTF8),
            QtGui.QApplication.translate('Form', ' Please enter the new cost ', None, QtGui.QApplication.UnicodeUTF8),
            QtGui.QApplication.translate('Form', ' Please select a UPC', None, QtGui.QApplication.UnicodeUTF8)]
        self.ui.ctr_slot_id_list.label_header.setText(QtGui.QApplication.translate('Form', '  DVD information', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_slot_id_list.label_0.setText(QtGui.QApplication.translate('Form', 'Slot ID:', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_slot_id_list.label_1.setText(QtGui.QApplication.translate('Form', 'Price plan:', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_slot_id_list.label_2.setText(QtGui.QApplication.translate('Form', 'Sale price:', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_slot_id_list.label_3.setText(QtGui.QApplication.translate('Form', 'Sale convert price:', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_slot_id_list.label_4.setText(QtGui.QApplication.translate('Form', 'Your cost:', None, QtGui.QApplication.UnicodeUTF8))
        for i in range(6):
            exec('self.ui.ctr_slot_id_list.btn_' + str(i) + '.setText(QtGui.QApplication.translate("Form", "Edit", None, QtGui.QApplication.UnicodeUTF8))')
        
        self.ui.ctr_slot_list.lable.setText(QtGui.QApplication.translate('Form', ' All empty slots', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_plan_list.label_header.setText(QtGui.QApplication.translate('Form', ' Price Plan List ', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_plan_list.btn_special_price.setText(QtGui.QApplication.translate('Form', 'Accept special price plan', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.ctr_upc_list.label.setText(QtGui.QApplication.translate('Form', '  UPC                        Disc Version    Release Date', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = LoadDiscInfoForm()
    mainf.show()
    mainf.ui.txt_price_plan.setText('First Night Fee ￡10, \nAdditional Night Fee ￡1, \nCutoff Time 23:59:59')
    mainf.ui.txt_price_plan_id.setText('1')
    mainf.ui.txt_sale_price.setText('30.00')
    mainf.ui.txt_convert_price.setText('0.5')
    mainf.ui.txt_cost.setText('20.00')
    mainf.ui.txt_upc.setText('828970050197')
    mainf.ui.txt_special_price_plan.setText('yes')
    mainf.setMovieDetail({
        'ctr_movie_detail': {
            'rating': 'NR',
            'movie_title': 'AWOL One: 66, Vol. 2 (2006, Vol.Each 24 Hours Fee 2Each 24 Hours Fee 2Each 24 Hours Fee 2Each 24 Hours Fee 2 2 (2005)',
            'dvd_release_date': '2006-01-24',
            'directors': '',
            'dvd_version': '2008-8-8',
            'starring': 'asdfasf\nlksjaljfla',
            'genre': 'Music',
            'movie_pic': '/home/puyodead1/kiosk/var/gui/pic/default.jpg' } })
    mainf.ui.ctr_slot_id_list.setList({
        'check_slot_id': '547',
        'front_slot_id': '547',
        'back_slot_id': '606' })
    mainf.ui.ctr_upc_list.setUPCList({
        'ctr_upc_list': [
            {
                'dvd_release_date': '2005-09-27',
                'dvd_version': 'DVD',
                'upc': '828970050197' },
            {
                'dvd_release_date': '2005-09-27',
                'dvd_version': 'DVD',
                'upc': '128970050197' },
            {
                'dvd_release_date': '2005-09-27',
                'dvd_version': 'DVD',
                'upc': '228970050197' },
            {
                'dvd_release_date': '2005-09-27',
                'dvd_version': 'DVD',
                'upc': '428970050197' }] })
    mainf.ui.ctr_slot_list.setList({
        'slot_list': "['101','102','103','101','102','103','101','102','103','101','102','103','101','102','103','101','102','103','101','102','103','101','102','103','101','102','103','101','102','103','101','102','103','101','102','103']" })
    mainf.ui.ctr_plan_list.setPlanList({
        'ctr_plan_list': [
            {
                'data_text': 'First Night Fee ￡10, \nAdditional Night Fee ￡1, \nCutoff Time 23:59:59',
                'data': '\n<PRICE>\n    <FACTORS>first_night|nights</FACTORS>\n    <FACTORS_ALGORITHM>{&quot;first_night&quot;:&apos;&apos;&apos;factor = 1&apos;&apos;&apos;, &quot;nights&quot;:&apos;&apos;&apos;\noutTime = params[&quot;out_time&quot;]\ninTime = params[&quot;in_time&quot;]\nfirstCutoffTime = str(outTime).split(&quot; &quot;)[0] + &quot; 23:59:59&quot;\nif firstCutoffTime &lt; outTime:\n    firstCutoffTime = getTimeChange(firstCutoffTime, day=1)\nnights = 0\nnextCutoffTime = getTimeChange(firstCutoffTime, day=1)\nwhile nextCutoffTime &lt; inTime:\n    nights += 1\n    oldTime = nextCutoffTime\n    nextCutoffTime = getTimeChange(nextCutoffTime, day=1)\n    if oldTime == nextCutoffTime:\n        break\nfactor = nights&apos;&apos;&apos;}</FACTORS_ALGORITHM>\n    <ALGORITHM>\nfirstNight = float(factors[&quot;first_night&quot;])\nnights = float(factors[&quot;nights&quot;] )\nresult = 10 * firstNight + 1 * nights</ALGORITHM>\n    <NOTES></NOTES>\n</PRICE>',
                'id': '1' },
            {
                'data_text': 'First 24 hours Fee 1.59, \nNext per 12 hours Fee 0.99',
                'data': '\n<PRICE>\n    <FACTORS>first_24_hours|12_hours</FACTORS>\n    <FACTORS_ALGORITHM>{&quot;first_24_hours&quot;:&apos;&apos;&apos;factor = 1&apos;&apos;&apos;, &quot;12_hours&quot;:&apos;&apos;&apos;\noutTime = params[&quot;out_time&quot;]\ninTime = params[&quot;in_time&quot;]\naddiStartTime = getTimeChange(outTime, hour=24)\nif addiStartTime >= inTime:\n    addiHoursCount = 0\nelse:\n    addiHoursCount = 0\n    while addiStartTime &lt; inTime:\n        addiHoursCount += 1\n        oldTime = addiStartTime\n        addiStartTime = getTimeChange(addiStartTime, hour=12)\n        if oldTime == addiStartTime:\n            break\nfactor = addiHoursCount&apos;&apos;&apos;}</FACTORS_ALGORITHM>\n    <ALGORITHM>\nfirsthours24 = float(factors[&quot;first_24_hours&quot;])\nhours12 = float(factors[&quot;12_hours&quot;])\nresult = 1.59 * firsthours24 + 0.99 * hours12</ALGORITHM>\n    <NOTES></NOTES>\n</PRICE>',
                'id': '2' }] })
    sys.exit(app.exec_())

