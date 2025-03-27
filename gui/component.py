# Source Generated with Decompyle++
# File: component.pyc (Python 2.5)

'''
User defined component
2009-07-13 created by Mavis <mavis.xiang@cereson.com>
'''
import sys
import os
import time
import config
import struct
import logging
import logging.handlers as logging
from PyQt4 import QtCore, QtGui
from configForm_ui import Ui_configForm
from squery import socketQuery
log = logging.getLogger('qt-component')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(message)s')
rotateHandle = logging.handlers.RotatingFileHandler('/home/mm/kiosk/var/log/qt-component.log', 'a', 1024 * 1024 * 10, 7)
rotateHandle.setFormatter(formatter)
log.addHandler(rotateHandle)

class PicTrans(QtGui.QWidget):
    
    def __init__(self, wid, parent = None, time = 10000):
        QtGui.QWidget.__init__(self, parent)
        self.wid = wid
        self.v = 0
        self.pos = 0
        self.labels = []
        self.time = time
        self.timer = QtCore.QTimer()
        self.sq = socketQuery()
        self.data = []
        self.picData = []
        self.iconSize = [
            QtCore.QSize(114, 171),
            QtCore.QSize(111, 165),
            QtCore.QSize(108, 161),
            QtCore.QSize(132, 196),
            QtCore.QSize(125, 186)]
        self.pointList = [
            QtCore.QPoint(86, 84),
            QtCore.QPoint(252, 136),
            QtCore.QPoint(433, 76),
            QtCore.QPoint(408, 279),
            QtCore.QPoint(589, 157)]
        for i in range(5):
            self.picData.insert(i, { })
            self.picData[i]['pixmap'] = QtGui.QPixmap()
            self.picData[i]['pic'] = ''
            self.picData[i]['upc'] = ''
            self.picData[i]['is_bluray'] = ''
        
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL('timeout()'), self.changePic)
        self.timerShow = QtCore.QTimer()
        self.timerShow.setInterval(30)
        self.timerClose = QtCore.QTimeLine(20)
        self.timerClose.setFrameRange(1, 20)
        QtCore.QObject.connect(self.timerShow, QtCore.SIGNAL('timeout()'), self.picShow)
        QtCore.QObject.connect(self.timerClose, QtCore.SIGNAL('frameChanged(int)'), self.picClose)
        QtCore.QObject.connect(self.timerClose, QtCore.SIGNAL('stateChanged ( QTimeLine::State)'), self.stateChange)

    
    def stateChange(self, state):
        if not state:
            self.setPicButtons()
        

    
    def picShow(self):
        self.v = self.v + 0.05
        self.repaint()
        if self.v >= 0.99999:
            self.timerShow.stop()
        

    
    def picClose(self, value):
        self.v = 1 - 0.05 * value
        self.repaint()
        if self.v <= 0.05:
            self.timerClose.stop()
        

    
    def picAppear(self):
        self.timerShow.start()

    
    def picDisappear(self):
        self.timerClose.start()

    
    def picAppear1(self):
        for i in range(20):
            self.repaint()
            self.v = self.v + 0.05
            if self.v >= 1:
                return None
            
            time.sleep(5e-06)
        

    
    def picDisappear1(self):
        for i in range(20):
            self.repaint()
            self.v = self.v - 0.05
            if self.v <= 0:
                return None
            
            time.sleep(5e-06)
        

    
    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.setOpacity(self.v)
        for i in range(5):
            painter.drawPixmap(QtCore.QRect(self.pointList[i], self.iconSize[i]), self.picData[i]['pixmap'])
            if self.picData[i]['is_bluray']:
                painter.drawPixmap(QtCore.QRect(self.pointList[i].x() + self.iconSize[i].width() - 56, self.pointList[i].y() + self.iconSize[i].height() - 22, 56, 22), QtGui.QPixmap(self.picData[i]['is_bluray']))
            
        

    
    def hideEvent(self, e):
        self.timer.stop()
        self.timerShow.stop()
        self.timerClose.stop()

    
    def mousePressEvent(self, event):
        for i in range(5):
            if QtCore.QRect(self.pointList[i], self.iconSize[i]).contains(event.pos()):
                if self.picData[i]['upc']:
                    self.picData[i]['pixmap'].fill(QtCore.Qt.transparent)
                    self.update()
                    data = { }
                    data['wid'] = self.wid
                    data['cid'] = 'ctr_movie_list'
                    data['type'] = 'EVENT'
                    data['EVENT'] = 'EVENT_MOUSE_CLICK'
                    data['param_info'] = { }
                    data['param_info']['ctr_movie_list'] = { }
                    data['param_info']['ctr_movie_list']['upc'] = self.picData[i]['upc']
                    self.sq.send(data)
                
                return None
            
        

    
    def clear(self):
        for i in range(5):
            self.picData[i]['upc'] = ''
            del self.picData[i]['pixmap']
            self.picData[i]['pixmap'] = QtGui.QPixmap()
            self.picData[i]['is_bluray'] = ''
        

    
    def setPicButtons(self):
        for i in range(5):
            self.picData[i]['pixmap'].load(self.picData[i]['pic'])
        
        self.picAppear()

    
    def changePic(self):
        self.picDisappear()
        self.pos += 1
        length = len(self.data) - 5 * self.pos
        times = length / 5
        num = length % 5
        if length <= 0:
            for i in range(5):
                self.picData[i]['pic'] = self.data[i]['movie_pic']
                self.picData[i]['upc'] = self.data[i]['upc']
                is_bluray = int(self.data[i]['is_bluray'])
                if is_bluray == 1:
                    self.picData[i]['is_bluray'] = config.pic_blueray_small
                elif is_bluray == 0:
                    self.picData[i]['is_bluray'] = config.pic_dvd_small
                else:
                    self.picData[i]['is_bluray'] = ''
            
            self.pos = 0
        elif times > 0:
            for i in range(5):
                self.picData[i]['pic'] = self.data[5 * self.pos + i]['movie_pic']
                self.picData[i]['upc'] = self.data[5 * self.pos + i]['upc']
                is_bluray = int(self.data[5 * self.pos + i]['is_bluray'])
                if is_bluray == 1:
                    self.picData[i]['is_bluray'] = config.pic_blueray_small
                elif is_bluray == 0:
                    self.picData[i]['is_bluray'] = config.pic_dvd_small
                else:
                    self.picData[i]['is_bluray'] = ''
            
        else:
            for i in range(num):
                self.picData[i]['pic'] = self.data[5 * self.pos + i]['movie_pic']
                self.picData[i]['upc'] = self.data[5 * self.pos + i]['upc']
                is_bluray = int(self.data[5 * self.pos + i]['is_bluray'])
                if is_bluray == 1:
                    self.picData[i]['is_bluray'] = config.pic_blueray_small
                elif is_bluray == 0:
                    self.picData[i]['is_bluray'] = config.pic_dvd_small
                else:
                    self.picData[i]['is_bluray'] = ''
            
            if i < 4:
                for j in range(4 - i):
                    self.picData[i + j + 1]['pic'] = self.data[5 * self.pos + i]['movie_pic']
                    self.picData[i + j + 1]['upc'] = self.data[5 * self.pos + i]['upc']
                    is_bluray = int(self.data[5 * self.pos + i]['is_bluray'])
                    if is_bluray == 1:
                        self.picData[i + j + 1]['is_bluray'] = config.pic_blueray_small
                    elif is_bluray == 0:
                        self.picData[i + j + 1]['is_bluray'] = config.pic_dvd_small
                    else:
                        self.picData[i + j + 1]['is_bluray'] = ''
                
            

    
    def setMovieList(self, data):
        if not data:
            return None
        
        data = data['ctr_movie_list']
        if data != self.data:
            self.data = data
        
        if not data:
            self.clear()
            return None
        
        self.timer.stop()
        self.pos = 0
        self.v = 1
        length = len(data)
        if length > 5:
            for i in range(5):
                self.picData[i]['pic'] = data[i]['movie_pic']
                self.picData[i]['upc'] = data[i]['upc']
                self.picData[i]['pixmap'].load(self.picData[i]['pic'])
                is_bluray = int(data[i]['is_bluray'])
                if is_bluray == 1:
                    self.picData[i]['is_bluray'] = config.pic_blueray_small
                elif is_bluray == 0:
                    self.picData[i]['is_bluray'] = config.pic_dvd_small
                else:
                    self.picData[i]['is_bluray'] = ''
            
            self.timer.start(self.time)
        else:
            i = 0
            for i in range(length):
                self.picData[i]['pic'] = data[i]['movie_pic']
                self.picData[i]['upc'] = data[i]['upc']
                is_bluray = int(data[i]['is_bluray'])
                if is_bluray == 1:
                    self.picData[i]['is_bluray'] = config.pic_blueray_small
                elif is_bluray == 0:
                    self.picData[i]['is_bluray'] = config.pic_dvd_small
                else:
                    self.picData[i]['is_bluray'] = ''
            
            if i < 4:
                for j in range(4 - i):
                    self.picData[i + j + 1]['pic'] = data[i]['movie_pic']
                    self.picData[i + j + 1]['upc'] = data[i]['upc']
                    self.picData[i + j + 1]['is_bluray'] = self.picData[i]['is_bluray']
                
            
            for i in range(5):
                self.picData[i]['pixmap'].load(self.picData[i]['pic'])
            
        self.repaint()



class picButton(QtGui.QPushButton):
    
    def __init__(self, wid, parent = None, style = ''):
        QtGui.QPushButton.__init__(self, parent)
        self.wid = wid
        self.data = ''
        self.sq = socketQuery()
        if style:
            self.setStyleSheet(style)
        

    
    def setData(self, text):
        self.data = text

    
    def mouseReleaseEvent(self, event):
        if self.data:
            data = { }
            data['wid'] = self.wid
            data['cid'] = 'ctr_movie_list'
            data['type'] = 'EVENT'
            data['EVENT'] = 'EVENT_MOUSE_CLICK'
            data['param_info'] = { }
            data['param_info']['ctr_movie_list'] = { }
            data['param_info']['ctr_movie_list']['upc'] = str(self.data)
            self.sq.send(data)
        



class movieFlower(QtGui.QWidget):
    
    def __init__(self, wid = '', parent = None, time = 10000):
        QtGui.QWidget.__init__(self, parent)
        self.time = time
        self.timer = QtCore.QTimer()
        self.pos = 0
        self.data = []
        self.picData = []
        self.iconSize = [
            QtCore.QSize(114, 171),
            QtCore.QSize(111, 165),
            QtCore.QSize(108, 161),
            QtCore.QSize(132, 196),
            QtCore.QSize(125, 186)]
        pointList = [
            QtCore.QPoint(86, 84),
            QtCore.QPoint(252, 136),
            QtCore.QPoint(433, 76),
            QtCore.QPoint(408, 279),
            QtCore.QPoint(589, 157)]
        for i in range(5):
            self.picData.insert(i, { })
            self.picData[i]['picBtn'] = picButton(wid, self)
            self.picData[i]['icon'] = QtGui.QIcon()
            self.picData[i]['picBtn'].setIconSize(self.iconSize[i])
            self.picData[i]['picBtn'].setGeometry(QtCore.QRect(pointList[i], self.iconSize[i]))
        
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL('timeout()'), self.changePic)

    
    def clear(self):
        for i in range(5):
            del self.picData[i]['icon']
            self.picData[i]['icon'] = QtGui.QIcon()
            self.picData[i]['picBtn'].setIcon(self.picData[i]['icon'])
            self.picData[i]['picBtn'].setData('')
        

    
    def setPicButtons(self):
        for i in range(5):
            del self.picData[i]['icon']
            pic = QtGui.QPixmap(self.picData[i]['pic'])
            if pic.width() < self.iconSize[i].width() or pic.height() < self.iconSize[i].height():
                pic = pic.scaled(self.iconSize[i])
            
            self.picData[i]['icon'] = QtGui.QIcon(pic)
            self.picData[i]['picBtn'].setData(self.picData[i]['upc'])
            self.picData[i]['picBtn'].setIcon(self.picData[i]['icon'])
        

    
    def changePic(self):
        self.pos += 1
        length = len(self.data) - 5 * self.pos
        times = length / 5
        num = length % 5
        if length <= 0:
            for i in range(5):
                self.picData[i]['pic'] = self.data[i]['movie_pic']
                self.picData[i]['upc'] = self.data[i]['upc']
            
            self.pos = 0
        elif times > 0:
            for i in range(5):
                self.picData[i]['pic'] = self.data[5 * self.pos + i]['movie_pic']
                self.picData[i]['upc'] = self.data[5 * self.pos + i]['upc']
            
        else:
            for i in range(num):
                self.picData[i]['pic'] = self.data[5 * self.pos + i]['movie_pic']
                self.picData[i]['upc'] = self.data[5 * self.pos + i]['upc']
            
            if i < 4:
                for j in range(4 - i):
                    self.picData[i + j + 1]['pic'] = self.data[5 * self.pos + i]['movie_pic']
                    self.picData[i + j + 1]['upc'] = self.data[5 * self.pos + i]['upc']
                
            
        self.setPicButtons()

    
    def setMovieList(self, data):
        if not data:
            return None
        
        data = data['ctr_movie_list']
        if data != self.data:
            self.data = data
        else:
            return None
        if not data:
            self.clear()
            return None
        
        self.timer.stop()
        self.pos = 0
        length = len(data)
        if length > 5:
            for i in range(5):
                self.picData[i]['pic'] = data[i]['movie_pic']
                self.picData[i]['upc'] = data[i]['upc']
            
            self.setPicButtons()
            self.timer.start(self.time)
        else:
            i = 0
            for i in range(length):
                self.picData[i]['pic'] = data[i]['movie_pic']
                self.picData[i]['upc'] = data[i]['upc']
            
            if i < 4:
                for j in range(4 - i):
                    self.picData[i + j + 1]['pic'] = data[i]['movie_pic']
                    self.picData[i + j + 1]['upc'] = data[i]['upc']
                
            
            self.setPicButtons()



class DiscOutList(QtGui.QWidget):
    
    def __init__(self, parent = None, wid = '', cid = '', rheith = 75, row = 6, col = 3, style = 'font: bold 20px; ' + config.table_bg_style):
        QtGui.QWidget.__init__(self, parent)
        self.setStyleSheet(style)
        self.parent = parent
        self.rowHeight = rheith
        self.sq = socketQuery()
        self.wid = wid
        self.cid = cid
        self.col = col
        self.btnBrush = QtGui.QBrush(QtGui.QPixmap(config.pic_btn_little))
        self.nullBrush = QtGui.QBrush()
        self.couponBrush = QtGui.QBrush(QtGui.QPixmap(config.pic_coupon))
        self.btnFont = QtGui.QFont()
        self.btnFont.setPointSize(16)
        self.btnFont.setBold(True)
        self.btnFont.setItalic(True)
        self.dataType = 1047295
        self.table = QtGui.QTableWidget(self)
        self.table.setGeometry(0, 60, config.unload_list_width, self.rowHeight * row)
        self.table.setColumnCount(col)
        self.hlabel = QtGui.QLabel(self)
        self.hlabel.setStyleSheet(config.table_title_style)
        self.hlabel.setGeometry(0, 0, config.unload_list_width + 2, 60)
        self.header = QtCore.QT_TRANSLATE_NOOP('Admin', ' Disc Pic      Disc Information ')
        colWidth = [
            120,
            380,
            120]
        self.reset()
        for i in range(col):
            self.table.setColumnWidth(i, colWidth[i])
        
        self.table.setStyleSheet(config.scroll_style)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table.setIconSize(QtCore.QSize(config.pic_width_little + 25, config.pic_height_little + 25))
        self.table.verticalHeader().setEnabled(False)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().hide()
        self.line = QtGui.QFrame(self)
        self.line.setGeometry(QtCore.QRect(0, self.table.y() + self.table.height() - 4, config.unload_list_width + 2, 16))
        self.line.setLineWidth(0)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setStyleSheet(config.table_btm_style)
        QtCore.QObject.connect(self.table, QtCore.SIGNAL('cellPressed(int, int)'), self.cell_press)

    
    def reset(self):
        self.hlabel.setText(QtGui.QApplication.translate('Admin', self.header, None, QtGui.QApplication.UnicodeUTF8))

    
    def setDiscList(self, datas):
        data = datas.get('discs')
        print(data, 'whosyourdaddy')
        if not data:
            print('[setMovieList] Error: data can not be NULL!')
            return -1
        
        self.table.clear()
        if not data:
            self.table.setRowCount(0)
            return None
        
        length = len(data)
        self.table.setRowCount(length)
        for i in range(length):
            self.table.setRowHeight(i, self.rowHeight)
        
        for i in range(length):
            movie_pic = data[i]['movie_pic']
            print(movie_pic)
            feature = data[i]['feature']
            rfid = data[i]['rfid']
            upc = data[i]['upc']
            item = QtGui.QTableWidgetItem()
            item.setIcon(QtGui.QIcon(movie_pic))
            item.setData(self.dataType, QtCore.QVariant(upc))
            self.table.setItem(i, 0, item)
            disc_info = featureList()
            disc_info.setList(feature)
            disc_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.table.setCellWidget(i, 1, disc_info)
            item = QtGui.QTableWidgetItem(QtGui.QApplication.translate('UnloadForm', 'Next', None, QtGui.QApplication.UnicodeUTF8))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setBackground(self.btnBrush)
            item.setForeground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.white)))
            item.setFont(self.btnFont)
            item.setData(self.dataType, QtCore.QVariant(rfid))
            self.table.setItem(i, 2, item)
        

    
    def cell_press(self, row, col):
        if col == 2:
            data = { }
            data['wid'] = self.wid
            data['cid'] = self.cid
            data['type'] = 'EVENT'
            data['EVENT'] = 'EVENT_MOUSE_CLICK'
            data['param_info'] = { }
            data['param_info'][self.cid] = { }
            upc = self.table.item(row, 0).data(self.dataType).toString()
            rfid = self.table.item(row, 2).data(self.dataType).toString()
            data['param_info'][self.cid]['upc'] = str(upc)
            data['param_info'][self.cid]['rfid'] = str(rfid)
            print(rfid)
            self.sq.send(data)
        



class SlotsQtnBtn(QtGui.QWidget):
    
    def __init__(self, parent = None, wid = 'showbadSlotForm', width = 400, height = 50):
        QtGui.QWidget.__init__(self, parent)
        self.wid = wid
        self.sq = socketQuery()
        label_wid = 158
        label_hei = 30
        self.label_1 = QtGui.QPushButton()
        self.label_1.setFixedSize(label_wid, label_hei)
        self.label_1.setFocusPolicy(QtCore.Qt.NoFocus)
        QtCore.QObject.connect(self.label_1, QtCore.SIGNAL('pressed()'), self.label_1_press)
        self.label_2 = QtGui.QPushButton()
        self.label_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_2.setFixedSize(label_wid, label_hei)
        QtCore.QObject.connect(self.label_2, QtCore.SIGNAL('pressed()'), self.label_2_press)
        self.label_3 = QtGui.QPushButton()
        self.label_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_3.setFixedSize(label_wid, label_hei)
        QtCore.QObject.connect(self.label_3, QtCore.SIGNAL('pressed()'), self.label_3_press)
        self.select_style = 'QPushButton{border:1px solid black;font:18px;border-radius:4px;background-color: #72bef0;}'
        self.style = 'QPushButton{border:1px solid black;font:18px;border-radius:8px;background-color:transparent;}'
        self.setStyleSheet(self.style)
        hl = QtGui.QHBoxLayout(self)
        hl.addWidget(self.label_1)
        hl.addWidget(self.label_2)
        hl.addWidget(self.label_3)
        self.setLayout(hl)

    
    def set_label_text(self, data):
        data = data['text']
        self.label_1.setText('All(%s)' % data['all'])
        self.label_2.setText('Bad(%s)' % data['bad'])
        self.label_3.setText('Empty(%s)' % data['empty'])

    
    def set_current_select(self, data):
        name = data['name']
        if name == 'all':
            self.label_1.setStyleSheet(self.select_style)
            self.label_2.setStyleSheet(self.style)
            self.label_3.setStyleSheet(self.style)
        elif name == 'bad':
            self.label_2.setStyleSheet(self.select_style)
            self.label_1.setStyleSheet(self.style)
            self.label_3.setStyleSheet(self.style)
        elif name == 'empty':
            self.label_3.setStyleSheet(self.select_style)
            self.label_2.setStyleSheet(self.style)
            self.label_1.setStyleSheet(self.style)
        

    
    def label_1_press(self):
        print(2142)
        cur = 'all'
        self.set_current_select({
            'name': cur })
        data = { }
        data['wid'] = self.wid
        data['cid'] = 'all_slot_qtn'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info']['all_slot_qtn'] = { }
        data['param_info']['all_slot_qtn']['info'] = cur
        self.sq.send(data)

    
    def label_2_press(self):
        cur = 'bad'
        self.set_current_select({
            'name': cur })
        data = { }
        data['wid'] = self.wid
        data['cid'] = 'all_slot_qtn'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info']['all_slot_qtn'] = { }
        data['param_info']['all_slot_qtn']['info'] = cur
        self.sq.send(data)

    
    def label_3_press(self):
        cur = 'empty'
        self.set_current_select({
            'name': cur })
        data = { }
        data['wid'] = self.wid
        data['cid'] = 'all_slot_qtn'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info']['all_slot_qtn'] = { }
        data['param_info']['all_slot_qtn']['info'] = cur
        self.sq.send(data)



class AllSlotList(QtGui.QWidget):
    
    def __init__(self, parent = None, wid = '', rheith = 75, row = 6, col = 5, style = 'font:bold 20px;' + config.table_bg_style):
        QtGui.QWidget.__init__(self, parent)
        self.setStyleSheet(style)
        self.wid = wid
        self.parent = parent
        self.rowHeight = rheith
        self.col = col
        self.sq = socketQuery()
        self.dataType = 1047295
        self.btnFont = QtGui.QFont()
        self.btnBrush = QtGui.QBrush(QtGui.QPixmap(config.pic_btn_little))
        self.GreenbtnBrush = QtGui.QBrush(QtGui.QPixmap(config.pic_btn_out_green))
        self.RedbtnBrush = QtGui.QBrush(QtGui.QPixmap(config.pic_btn_out_red))
        self.GraybtnBrush = QtGui.QBrush(QtGui.QPixmap(config.pic_btn_out_gray))
        self.btnFont.setPointSize(16)
        self.btnFont.setBold(True)
        self.btnFont.setItalic(True)
        self.table = QtGui.QTableWidget(self)
        self.table.setGeometry(0, 60, config.unload_list_width, self.rowHeight * row)
        self.table.setColumnCount(col)
        self.hlabel = QtGui.QLabel(self)
        self.hlabel.setStyleSheet(config.table_title_style)
        self.hlabel.setGeometry(0, 0, config.unload_list_width + 2, 60)
        self.hlabel.setText(QtGui.QApplication.translate('Form', ' Slot ID        Status                    Action', None, QtGui.QApplication.UnicodeUTF8))
        colWidth = [
            150,
            180,
            160,
            120,
            30]
        for i in range(col):
            self.table.setColumnWidth(i, colWidth[i])
        
        self.table.setStyleSheet(config.scroll_style)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table.setIconSize(QtCore.QSize(config.pic_width_little + 5, config.pic_height_little))
        self.table.verticalHeader().setEnabled(False)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().hide()
        self.line = QtGui.QFrame(self)
        self.line.setGeometry(QtCore.QRect(0, self.table.y() + self.table.height() - 4, config.unload_list_width + 2, 16))
        self.line.setLineWidth(0)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setStyleSheet(config.table_btm_style)
        QtCore.QObject.connect(self.table, QtCore.SIGNAL('cellPressed(int, int)'), self.cell_press)

    
    def cell_press(self, row, col):
        if col in (0, 1):
            return None
        elif col in (2, 3):
            if self.table.item(row, col):
                msg = str(self.table.item(row, col).data(self.dataType).toString())
                if msg:
                    data = { }
                    data['wid'] = self.wid
                    data['cid'] = 'ctr_slot_list'
                    data['type'] = 'EVENT'
                    data['EVENT'] = 'EVENT_MOUSE_CLICK'
                    data['param_info'] = { }
                    data['param_info']['ctr_slot_list'] = { }
                    data['param_info']['ctr_slot_list']['info'] = msg
                    self.sq.send(data)
                
            
        

    
    def setSlotList(self, data):
        if not data:
            print('[setSlotList] Error: data can not be NULL!')
            self.table.setRowCount(0)
            return -1
        
        self.table.clear()
        data = data['ctr_slot_list']
        length = len(data)
        self.table.setRowCount(length)
        for i in range(length):
            self.table.setRowHeight(i, self.rowHeight)
            slot_id = str(data[i]['slot_id'])
            status = data[i]['status']
            action_1 = data[i]['action_1']
            action_2 = data[i]['action_2']
            rfid = data[i]['rfid']
            item = QtGui.QTableWidgetItem(slot_id)
            self.table.setItem(i, 0, item)
            item = QtGui.QTableWidgetItem(status)
            self.table.setItem(i, 1, item)
            if action_1:
                item = QtGui.QTableWidgetItem(action_1)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setBackground(self.RedbtnBrush)
                item.setForeground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.white)))
                item.setFont(self.btnFont)
                item.setData(self.dataType, QtCore.QVariant('%s|%s|%s' % (slot_id, action_1.lower(), rfid)))
                self.table.setItem(i, 2, item)
            
            if action_2:
                item = QtGui.QTableWidgetItem(action_2)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                if action_2 == 'Clear':
                    item.setBackground(self.GraybtnBrush)
                    print('c')
                elif action_2 == 'Unload':
                    item.setBackground(self.btnBrush)
                    print('u')
                elif action_2 == 'Load':
                    item.setBackground(self.GreenbtnBrush)
                    print('l')
                else:
                    print('err')
                item.setForeground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.white)))
                item.setFont(self.btnFont)
                item.setData(self.dataType, QtCore.QVariant('%s|%s|%s' % (slot_id, action_2.lower(), rfid)))
                self.table.setItem(i, 3, item)
            
            item = QtGui.QTableWidgetItem()
            self.table.setItem(i, 4, item)
        



class MovieListAdmin(QtGui.QWidget):
    
    def __init__(self, parent = None, slot = 0, rheith = 75, row = 6, col = 4, style = 'font: bold 20px; ' + config.table_bg_style):
        QtGui.QWidget.__init__(self, parent)
        self.setStyleSheet(style)
        self.parent = parent
        self.slot = slot
        self.rowHeight = rheith
        self.col = col
        self.btnBrush = QtGui.QBrush(QtGui.QPixmap(config.pic_btn_little))
        self.nullBrush = QtGui.QBrush()
        self.couponBrush = QtGui.QBrush(QtGui.QPixmap(config.pic_coupon))
        self.btnFont = QtGui.QFont()
        self.btnFont.setPointSize(16)
        self.btnFont.setBold(True)
        self.btnFont.setItalic(True)
        self.dataType = 1047295
        self.table = QtGui.QTableWidget(self)
        self.table.setGeometry(0, 60, config.unload_list_width, self.rowHeight * row)
        self.table.setColumnCount(col)
        self.hlabel = QtGui.QLabel(self)
        self.hlabel.setStyleSheet(config.table_title_style)
        self.hlabel.setGeometry(0, 0, config.unload_list_width + 2, 60)
        if slot == 3:
            self.hlabel.setText(QtGui.QApplication.translate('Form', '           Title                   Price Information', None, QtGui.QApplication.UnicodeUTF8))
            colWidth = [
                260,
                260,
                100,
                56]
        elif not slot:
            self.header = QtCore.QT_TRANSLATE_NOOP('Admin', ' Slot ID     Disc Information          Price')
            colWidth = [
                115,
                280,
                120,
                120]
        elif slot == 1:
            self.header = QtCore.QT_TRANSLATE_NOOP('Admin', ' Disc Information          Slot ID     Price')
            colWidth = [
                280,
                115,
                120,
                120]
        else:
            self.header = QtCore.QT_TRANSLATE_NOOP('Admin', ' Disc Information          Slot ID     State')
            colWidth = [
                280,
                115,
                120,
                120]
        if col == 5:
            colWidth = [
                300,
                100,
                80,
                120,
                76]
        
        self.reset()
        for i in range(col):
            self.table.setColumnWidth(i, colWidth[i])
        
        self.table.setStyleSheet(config.scroll_style)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table.setIconSize(QtCore.QSize(config.pic_width_little + 5, config.pic_height_little))
        self.table.verticalHeader().setEnabled(False)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().hide()
        self.line = QtGui.QFrame(self)
        self.line.setGeometry(QtCore.QRect(0, self.table.y() + self.table.height() - 4, config.unload_list_width + 2, 16))
        self.line.setLineWidth(0)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setStyleSheet(config.table_btm_style)
        QtCore.QObject.connect(self.table, QtCore.SIGNAL('cellPressed(int, int)'), self.cell_press)
        QtCore.QObject.connect(self.table, QtCore.SIGNAL('itemClicked ( QTableWidgetItem *)'), self.cell_release)

    
    def reset(self):
        self.hlabel.setText(QtGui.QApplication.translate('Admin', self.header, None, QtGui.QApplication.UnicodeUTF8))

    
    def setMovieList(self, data):
        if not data:
            print('[setMovieList] Error: data can not be NULL!')
            return -1
        
        self.table.clear()
        data = data['ctr_movie_list']
        if not data:
            self.table.setRowCount(0)
            return None
        
        length = len(data)
        self.table.setRowCount(length)
        for i in range(length):
            self.table.setRowHeight(i, self.rowHeight)
        
        for i in range(length):
            movie_pic = data[i]['movie_pic']
            movie_title = data[i]['movie_title']
            slot_id = data[i]['slot_id']
            price = data[i]['price']
            rfid = data[i]['rfid']
            item = QtGui.QTableWidgetItem(movie_title)
            item.setIcon(QtGui.QIcon(movie_pic))
            if not (self.slot):
                self.table.setItem(i, 1, item)
            else:
                self.table.setItem(i, 0, item)
            item = QtGui.QTableWidgetItem(slot_id)
            if not (self.slot):
                self.table.setItem(i, 0, item)
            else:
                self.table.setItem(i, 1, item)
            item = QtGui.QTableWidgetItem()
            if self.slot == 2:
                item.setText(data[i]['state'])
            else:
                item.setText(config.symbol + price)
            self.table.setItem(i, 2, item)
            item = QtGui.QTableWidgetItem(QtGui.QApplication.translate('UnloadForm', 'Unload', None, QtGui.QApplication.UnicodeUTF8))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setBackground(self.btnBrush)
            item.setForeground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.white)))
            item.setFont(self.btnFont)
            item.setData(self.dataType, QtCore.QVariant(rfid))
            self.table.setItem(i, 3, item)
            if self.col == 5:
                item = QtGui.QTableWidgetItem()
                item.setIcon(QtGui.QIcon(config.pic_del))
                self.table.setItem(i, 4, item)
            
        

    
    def setCartInfo(self, data):
        if not data:
            print('[setCartInfo] Error: data can not be NULL!')
            return -1
        
        self.table.clear()
        if data['global_coupon_code'] and data['global_coupon_short_description']:
            self.parent.couponLabel.setText('    ' + data['global_coupon_short_description'])
            self.parent.couponLabel.show()
        else:
            self.parent.couponLabel.hide()
        datalist = data['ctr_cart_info']
        if not datalist:
            self.table.setRowCount(0)
            return None
        
        self.table.setRowCount(len(datalist))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        for row in range(len(datalist)):
            movie_title = datalist[row]['movie_title']
            movie_pic = datalist[row]['movie_pic']
            price_plan_text = datalist[row]['price_plan_text']
            rfid = datalist[row]['rfid']
            self.table.setRowHeight(row, self.rowHeight)
            movieItem = QtGui.QTableWidgetItem()
            movieItem.setFont(font)
            if os.path.isfile(movie_pic):
                movieItem.setIcon(QtGui.QIcon(QtGui.QPixmap(movie_pic)))
            
            movieItem.setText(movie_title)
            self.table.setItem(row, 0, movieItem)
            movieItem = QtGui.QTableWidgetItem(price_plan_text)
            movieItem.setFont(font)
            self.table.setItem(row, 1, movieItem)
            movieItem = QtGui.QTableWidgetItem()
            if datalist[row]['coupon_short_description']:
                movieItem.setBackground(self.couponBrush)
                movieItem.setText(datalist[row]['coupon_short_description'])
                movieItem.setTextAlignment(QtCore.Qt.AlignCenter)
            
            self.table.setItem(row, 2, movieItem)
            movieItem = QtGui.QTableWidgetItem(QtGui.QIcon(QtGui.QPixmap(config.pic_del)), '')
            movieItem.setData(self.dataType, QtCore.QVariant(rfid))
            self.table.setItem(row, 3, movieItem)
        

    
    def cell_press(self, row, col):
        if self.slot == 3 and col == 3:
            self.table.item(row, 3).setIcon(QtGui.QIcon())
        elif self.slot == 2 and col == 4:
            self.table.item(row, 4).setIcon(QtGui.QIcon())
        elif col == 3:
            self.table.item(row, 3).setBackground(self.nullBrush)
        

    
    def cell_release(self, item):
        row = item.row()
        col = item.column()
        if self.slot == 3 and col == 3:
            self.table.item(row, 3).setIcon(QtGui.QIcon(config.pic_del))
        elif self.slot == 2 and col == 4:
            self.table.item(row, 4).setIcon(QtGui.QIcon(config.pic_del))
        elif col == 3:
            self.table.item(row, 3).setBackground(self.btnBrush)
        



class DiscList(QtGui.QWidget):
    
    def __init__(self, wid, parent = None, rheith = 75, row = 6, col = 3, style = 'font: bold 20px;' + config.table_bg_style):
        QtGui.QWidget.__init__(self, parent)
        self.wid = wid
        self.sq = socketQuery()
        self.rowHeight = rheith
        self.btnBrush = QtGui.QBrush(QtGui.QPixmap(config.pic_btn_little))
        self.btnFont = QtGui.QFont()
        self.btnFont.setPointSize(18)
        self.btnFont.setBold(True)
        self.btnFont.setItalic(True)
        self.dataType = 1047295
        self.hlabel = QtGui.QLabel(QtGui.QApplication.translate('Form', '  Disc Information                           Rental Time', None, QtGui.QApplication.UnicodeUTF8), self)
        self.hlabel.setStyleSheet(config.style_hlabel)
        self.hlabel.setGeometry(0, 0, 686, 60)
        self.table = QtGui.QTableWidget(self)
        self.table.setGeometry(0, 60, 684, self.rowHeight * row)
        self.line = QtGui.QFrame(self)
        self.line.setGeometry(QtCore.QRect(0, 506, 686, 16))
        self.line.setLineWidth(0)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setStyleSheet('background-image: url(' + config.pic_btm_table_green + ')')
        self.table.setStyleSheet(style)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table.setIconSize(QtCore.QSize(config.pic_width_little + 5, config.pic_height_little + 5))
        self.table.verticalHeader().setEnabled(False)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().hide()
        self.table.setColumnCount(col)
        self.table.setColumnWidth(0, 390)
        self.table.setColumnWidth(1, 170)
        self.table.setColumnWidth(2, 120)
        QtCore.QObject.connect(self.table, QtCore.SIGNAL('cellClicked(int, int)'), self.cell_click)
        QtCore.QObject.connect(self.table, QtCore.SIGNAL('cellPressed(int, int)'), self.cell_press)
        self.txt_return = QtGui.QApplication.translate('Form', 'Return', None, QtGui.QApplication.UnicodeUTF8)

    
    def setDiscList(self, data):
        if not data:
            print('[setDiscList] Error: data can not be NULL!')
            return -1
        
        self.table.clear()
        data = data['ctr_disc_list']
        if not data:
            self.table.setRowCount(0)
            return None
        
        length = len(data)
        self.table.setRowCount(length)
        for i in range(length):
            self.table.setRowHeight(i, self.rowHeight)
        
        for i in range(length):
            movie_pic = data[i]['movie_pic']
            movie_title = data[i]['movie_title']
            time_out = data[i]['time_out']
            rfid = data[i]['rfid']
            item = QtGui.QTableWidgetItem(movie_title)
            item.setIcon(QtGui.QIcon(movie_pic))
            self.table.setItem(i, 0, item)
            item = QtGui.QTableWidgetItem(time_out)
            self.table.setItem(i, 1, item)
            item = QtGui.QTableWidgetItem(self.txt_return)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setBackground(self.btnBrush)
            item.setForeground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.white)))
            item.setFont(self.btnFont)
            item.setData(self.dataType, QtCore.QVariant(rfid))
            self.table.setItem(i, 2, item)
        

    
    def cell_click(self, row, col):
        if col == 2:
            data = { }
            data['wid'] = self.wid
            data['cid'] = 'ctr_disc_list'
            data['type'] = 'EVENT'
            data['EVENT'] = 'EVENT_MOUSE_CLICK'
            data['param_info'] = { }
            data['param_info']['ctr_disc_list'] = { }
            rfid = self.table.item(row, 2).data(self.dataType).toString()
            data['param_info']['ctr_disc_list']['rfid'] = str(rfid)
            self.table.item(row, 2).setBackground(self.btnBrush)
            self.sq.send(data)
        

    
    def cell_press(self, row, col):
        if col == 2:
            self.table.item(row, 2).setBackground(QtGui.QBrush())
        



class TransactionList(QtGui.QWidget):
    
    def __init__(self, parent = None, cid = 'ctr_disc_list', col = 3, rheith = 75, row = 5, style = 'font: bold 20px; ' + config.table_bg_style):
        QtGui.QWidget.__init__(self, parent)
        self.rowHeight = rheith
        self.col = col
        self.cid = cid
        self.hlabel = QtGui.QLabel(self)
        self.hlabel.setStyleSheet(config.table_title_style)
        self.hlabel.setGeometry(0, 0, 686, 60)
        self.table = QtGui.QTableWidget(self)
        self.table.setGeometry(0, 60, 684, self.rowHeight * row)
        self.line = QtGui.QFrame(self)
        self.line.setGeometry(QtCore.QRect(0, self.table.y() + self.table.height(), 686, 16))
        self.line.setLineWidth(0)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setStyleSheet(config.table_btm_style)
        self.setStyleSheet(config.table_bg_style)
        self.table.setStyleSheet('QTableView {font:bold 20px; } ' + config.scroll_style)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table.setIconSize(QtCore.QSize(config.pic_width_little + 5, config.pic_height_little + 5))
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().hide()
        self.table.setColumnCount(col)
        if col == 3:
            self.table.setColumnWidth(0, 400)
            self.table.setColumnWidth(1, 120)
        else:
            self.table.setColumnWidth(0, 200)
        self.table.horizontalHeader().setResizeMode(col - 1, QtGui.QHeaderView.Stretch)

    
    def setList(self, data):
        if not data:
            print('[setDiscList] Error: data can not be NULL!')
            return -1
        
        self.table.clear()
        data = data[self.cid]
        if not data:
            self.table.setRowCount(0)
            return None
        
        length = len(data)
        self.table.setRowCount(length)
        for i in range(length):
            self.table.setRowHeight(i, self.rowHeight)
        
        for i in range(length):
            if self.col == 3:
                movie_pic = data[i]['movie_pic']
                col_0 = data[i]['movie_title']
                col_1 = config.symbol + data[i]['price']
                state = data[i]['state']
            else:
                col_0 = data[i]['coupon_code']
                col_1 = data[i]['description']
            item = QtGui.QTableWidgetItem(col_0)
            if self.col == 3:
                item.setIcon(QtGui.QIcon(movie_pic))
            
            self.table.setItem(i, 0, item)
            item = QtGui.QTableWidgetItem(col_1)
            self.table.setItem(i, 1, item)
            if self.col == 3:
                item = QtGui.QTableWidgetItem(state)
                self.table.setItem(i, 2, item)
            
        



class couponList(QtGui.QWidget):
    
    def __init__(self, wid, parent = None, rheith = 75, row = 6, col = 6):
        QtGui.QWidget.__init__(self, parent)
        self.wid = wid
        self.sq = socketQuery()
        self.rowHeight = rheith
        self.dataType = 1047295
        self.font = QtGui.QFont()
        self.font.setPointSize(13)
        self.font.setBold(True)
        style = 'color: #015353; font: bold 23px; ' + config.table_bg_style
        self.hlabel = QtGui.QLabel(QtGui.QApplication.translate('Form', ' Coupon code       Description                   Apply to', None, QtGui.QApplication.UnicodeUTF8), self)
        self.hlabel.setStyleSheet(config.table_title_style)
        self.hlabel.setGeometry(0, 0, config.unload_list_width + 2, 60)
        self.table = QtGui.QTableWidget(self)
        self.table.setGeometry(0, 60, config.unload_list_width, self.rowHeight * row)
        self.line = QtGui.QFrame(self)
        self.line.setGeometry(QtCore.QRect(0, 506, 686, 16))
        self.line.setLineWidth(0)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setStyleSheet(config.table_btm_style)
        self.table.setStyleSheet(style)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table.setIconSize(QtCore.QSize(config.pic_width_little + 5, config.pic_height_little + 5))
        self.table.verticalHeader().setEnabled(False)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().hide()
        self.table.setColumnCount(col)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 270)
        self.table.setColumnWidth(2, 55)
        self.table.setColumnWidth(3, 30)
        self.table.setColumnWidth(4, 45)
        self.table.setColumnWidth(5, 65)
        gradient = QtGui.QRadialGradient(0, 0, 250, 0, 0)
        gradient.setColorAt(0, QtGui.QColor(1, 90, 124))
        gradient.setColorAt(1, QtGui.QColor(47, 65, 84))
        self.bg_brush = QtGui.QBrush(gradient)
        QtCore.QObject.connect(self.table, QtCore.SIGNAL('cellClicked(int, int)'), self.cell_click)
        QtCore.QObject.connect(self.table, QtCore.SIGNAL('cellPressed(int, int)'), self.cell_press)

    
    def setCouponInfo(self, data):
        if not data:
            print('[setCouponInfo] Error: data can not be NULL!')
            return -1
        
        self.table.clear()
        datalist = data['ctr_coupon_info']
        if not datalist:
            self.table.setRowCount(0)
            return None
        
        length = len(datalist)
        self.table.setRowCount(length)
        for row in range(length):
            self.table.setRowHeight(row, self.rowHeight)
            coupon_code = datalist[row]['coupon_code']
            description = datalist[row]['description']
            coupon_type = datalist[row]['coupon_type']
            coupon_disc_pic = datalist[row]['coupon_disc_pic']
            rfid = datalist[row]['rfid']
            movieItem = QtGui.QTableWidgetItem(coupon_code)
            self.table.setItem(row, 0, movieItem)
            movieItem = QtGui.QTableWidgetItem(description)
            movieItem.setFont(self.font)
            movieItem.setForeground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.black)))
            self.table.setItem(row, 1, movieItem)
            movieItem = QtGui.QTableWidgetItem()
            movieItem.setData(self.dataType, QtCore.QVariant(rfid))
            if coupon_type == 'S' and os.path.isfile(coupon_disc_pic):
                movieItem.setIcon(QtGui.QIcon(QtGui.QPixmap(coupon_disc_pic)))
            elif coupon_type == 'M':
                movieItem.setText('All')
            
            self.table.setItem(row, 2, movieItem)
            movieItem = QtGui.QTableWidgetItem()
            if coupon_type == 'S':
                movieItem.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_next)))
            
            self.table.setItem(row, 3, movieItem)
            movieItem = QtGui.QTableWidgetItem()
            self.table.setItem(row, 4, movieItem)
            movieItem = QtGui.QTableWidgetItem(QtGui.QIcon(QtGui.QPixmap(config.pic_del)), '')
            self.table.setItem(row, 5, movieItem)
        

    
    def cell_click(self, row, col):
        if col == 0 and col == 1 or col == 4:
            return None
        
        rfid = self.table.item(row, 2).data(self.dataType).toString()
        if not rfid and col != 5:
            return None
        
        data = { }
        data['wid'] = 'CouponForm'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        if col == 5:
            data['cid'] = 'btn_del'
            data['param_info']['btn_del'] = { }
            data['param_info']['btn_del']['rfid'] = str(rfid)
            self.table.item(row, 5).setIcon(QtGui.QIcon(config.pic_del))
        else:
            data['cid'] = 'btn_coupon_movie'
            data['param_info']['btn_coupon_movie'] = { }
            data['param_info']['btn_coupon_movie']['rfid'] = str(rfid)
            if col == 3:
                self.table.item(row, 3).setIcon(QtGui.QIcon(config.pic_next))
            
        self.sq.send(data)

    
    def cell_press(self, row, col):
        if col == 5 or col == 3:
            self.table.item(row, col).setIcon(QtGui.QIcon())
        



class UpcList(QtGui.QWidget):
    
    def __init__(self, parent = None, width = config.unload_list_width, height = 435, row = 5, col = 4):
        QtGui.QWidget.__init__(self, parent)
        self.defaultUpc = ''
        label_height = 60
        self.colCount = col
        self.rowHeight = (height - label_height) / row
        self.label = QtGui.QLabel(QtGui.QApplication.translate('Form', '  UPC                              Disc Version    Release Date', None, QtGui.QApplication.UnicodeUTF8), self)
        self.label.setGeometry(0, 0, width, label_height)
        self.table = QtGui.QTableWidget(self)
        self.table.setGeometry(0, label_height, width, height - label_height)
        self.line = QtGui.QFrame(self)
        self.line.setGeometry(QtCore.QRect(0, self.table.y() + self.table.height() - 2, width, 16))
        self.line.setLineWidth(0)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setStyleSheet(config.table_btm_style)
        self.label.setStyleSheet(config.table_title_style)
        self.table.setStyleSheet('QTableView {font:bold 20px; selection-background-color: #72bef0; ' + config.table_bg_style + '} ' + config.scroll_style)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.verticalHeader().setEnabled(False)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().setEnabled(False)
        self.table.horizontalHeader().hide()
        self.table.setColumnCount(self.colCount)
        self.table.setIconSize(QtCore.QSize(0.2 * width, self.rowHeight))
        self.table.setColumnWidth(0, 0.3 * width)
        self.table.setColumnWidth(1, 0.3 * width)
        self.table.setColumnWidth(2, 0.2 * width)
        self.table.setColumnWidth(3, 0.2 * width)
        QtCore.QObject.connect(self.table, QtCore.SIGNAL('currentCellChanged(int, int, int, int)'), self.selectedChange)

    
    def selectedChange(self, row, col, preRow, preCol):
        if self.table.item(preRow, 3):
            self.table.item(preRow, 3).setIcon(QtGui.QIcon(config.pic_unchecked))
        
        if self.table.item(row, 3):
            self.table.item(row, 3).setIcon(QtGui.QIcon(config.pic_checked))
        

    
    def setUPCList(self, data):
        if not data:
            return -1
        
        self.table.clear()
        data = data['ctr_upc_list']
        if not data:
            self.table.setRowCount(0)
            return None
        
        self.table.setRowCount(len(data))
        for i in range(len(data)):
            self.table.setRowHeight(i, self.rowHeight)
            upc = data[i]['upc']
            date = data[i]['dvd_version']
            release_date = data[i]['dvd_release_date']
            item = QtGui.QTableWidgetItem(upc)
            self.table.setItem(i, 0, item)
            item = QtGui.QTableWidgetItem(date)
            item.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignJustify)
            self.table.setItem(i, 1, item)
            item = QtGui.QTableWidgetItem(release_date)
            self.table.setItem(i, 2, item)
            btn = QtGui.QTableWidgetItem()
            if upc != self.defaultUpc:
                btn.setIcon(QtGui.QIcon(config.pic_unchecked))
            else:
                btn.setIcon(QtGui.QIcon(config.pic_checked))
                self.table.setCurrentCell(i, 3)
            self.table.setItem(i, 3, btn)
        



class TextList(QtGui.QWidget):
    
    def __init__(self, parent = None, width = 180 + 41, height = 480, row = 6, col = 3):
        QtGui.QWidget.__init__(self, parent)
        label_height = 50
        self.colCount = col
        self.colWidth = (width - 41) / col - 2
        self.rowHeight = (height - label_height) / row
        self.lable = QtGui.QLabel(QtGui.QApplication.translate('Form', ' All empty slots', None, QtGui.QApplication.UnicodeUTF8), self)
        self.lable.setGeometry(0, 0, width, label_height)
        self.table = QtGui.QTableWidget(self)
        self.table.setGeometry(0, label_height, width, height - label_height)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QColor(0, 96, 130)))
        self.setPalette(palette)
        self.setStyleSheet('color: white; font: bold 22px')
        self.table.setStyleSheet(config.tableView_style + config.scroll_style)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setEnabled(False)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().setEnabled(False)
        self.table.horizontalHeader().hide()
        self.table.setColumnCount(self.colCount)
        for i in range(self.colCount):
            self.table.setColumnWidth(i, self.colWidth)
        

    
    def setList(self, data):
        self.table.clear()
        self.slotdata = data['slot_list']
        if not (self.slotdata):
            self.table.setRowCount(0)
            return -1
        
        data = eval(self.slotdata)
        length = len(data)
        rowCount = (length + self.colCount - 1) / self.colCount
        self.table.setRowCount(rowCount)
        for row in range(rowCount):
            self.table.setRowHeight(row, self.rowHeight)
        
        for i in range(length):
            text = data[i]
            item = QtGui.QTableWidgetItem(text)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.table.setItem(i / self.colCount, i % self.colCount, item)
        



class TitleList(QtGui.QTableWidget):
    
    def __init__(self, parent = None, cwidth = 300, rheith = 80, col = 2, style = 'QTableView { color: #015353; font: bold 18px; background-color: transparent; } ' + config.scroll_style):
        QtGui.QTableWidget.__init__(self, parent)
        self.setStyleSheet(style)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.colCount = col
        self.colWidth = cwidth
        self.rowHeight = rheith
        self.setColumnCount(self.colCount)
        self.verticalHeader().setEnabled(False)
        self.verticalHeader().hide()
        self.horizontalHeader().setEnabled(False)
        self.horizontalHeader().hide()
        self.setFrameShape(QtGui.QFrame.NoFrame)
        for i in range(self.colCount):
            self.setColumnWidth(i, self.colWidth)
        

    
    def setMovieList(self, data):
        if not data:
            print('[setMovieList] Error: data can not be NULL!')
            return -1
        
        self.clear()
        data = data['ctr_movie_list']
        if not data:
            self.setRowCount(0)
            return None
        
        length = len(data)
        rowCount = (length + 1) / 2
        self.setRowCount(rowCount)
        for row in range(rowCount):
            self.setRowHeight(row, self.rowHeight)
        
        for i in range(length):
            text = data[i]['movie_title']
            upc = data[i]['upc']
            item = QtGui.QTableWidgetItem(text)
            item.setData(1047295, QtCore.QVariant(upc))
            item.setTextAlignment(QtCore.Qt.AlignJustify)
            if i % 2:
                self.setItem(i / 2, 1, item)
            else:
                self.setItem(i / 2, 0, item)
        



class MovieList(QtGui.QTableWidget):
    
    def __init__(self, parent = None, col = 3, cwidth = (config.movieList_width - 40) / 3, rheight = config.movieList_height / 3):
        QtGui.QTableWidget.__init__(self, parent)
        self.setStyleSheet('QTableView { background-color: transparent;} ' + config.scroll_style)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setShowGrid(False)
        self.setFrameShape(QtGui.QFrame.NoFrame)
        self.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.verticalHeader().setEnabled(False)
        self.verticalHeader().hide()
        self.horizontalHeader().setEnabled(False)
        self.horizontalHeader().hide()
        self.colCount = col
        self.colWidth = cwidth
        self.rowHeight = rheight
        self.length = 0
        self.setColumnCount(self.colCount)
        self.mlist = []
        for col in range(self.colCount):
            self.setColumnWidth(col, self.colWidth)
        
        self.sq = socketQuery()
        QtCore.QObject.connect(self.verticalScrollBar(), QtCore.SIGNAL('valueChanged(int)'), self.sendcmd)
        self.txt_count = QtGui.QApplication.translate('Form', 'Inventory', None, QtGui.QApplication.UnicodeUTF8)

    
    def sendcmd(self, row):
        for i in range(3):
            for j in range(3):
                widget = self.cellWidget(row + i, j)
                widget.set_pic()
            
        
        data = { }
        data['wid'] = 'RentMainForm'
        data['cid'] = 'movie_scroll_bar'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        self.sq.send(data)

    
    def setMovieList(self, data):
        if not data:
            print('[setMovieList] Error: data can not be NULL!')
        else:
            self.scrollToTop()
            s_time = time.time()
            data = data['ctr_movie_list']
            if not data:
                self.clear()
                self.setRowCount(0)
                self.length = 0
                return None
            
            length = len(data)
            offset = length - self.length
            if offset > 0:
                counts = self.length
            else:
                counts = length
            self.length = length
            if length % self.colCount:
                rowCount = length / self.colCount + 1
            else:
                rowCount = length / self.colCount
            self.setRowCount(rowCount)
            for i in range(rowCount):
                self.setRowHeight(i, self.rowHeight)
            
            for i in range(counts):
                movie_pic = data[i]['movie_pic']
                movie_title = data[i]['movie_title']
                count = data[i]['available_count']
                blue_ray = 0
                rfid = ''
                flag = data[i]['form']
                if 'rfid' in data[i]:
                    rfid = data[i]['rfid']
                
                if 'is_bluray' in data[i]:
                    blue_ray = int(data[i]['is_bluray'])
                
                widget = self.cellWidget(i / self.colCount, i % self.colCount)
                widget.rfid = rfid
                widget.id = data[i]['upc']
                widget.pic = movie_pic
                widget.labelp.clear()
                widget._has_pic = False
                if i < 10:
                    widget.labelp.setPixmap(QtGui.QPixmap(movie_pic))
                    widget._has_pic = True
                
                widget.labelt.setText(movie_title)
                if data[i]['sales_price'] and float(data[i]['sales_price']):
                    tr_buy = QtGui.QApplication.translate('Form', 'Buy Now', None, QtGui.QApplication.UnicodeUTF8)
                    price_with_symbol = config.symbol + data[i]['sales_price']
                    price_text = tr_buy + ': ' + price_with_symbol
                    widget.label_price.setText(price_text)
                else:
                    widget.label_price.setText('')
                if data[i]['rental_price'] and float(data[i]['rental_price']):
                    tr_rent = QtGui.QApplication.translate('Form', 'Rent', None, QtGui.QApplication.UnicodeUTF8)
                    price_with_symbol = config.symbol + data[i]['rental_price']
                    rent_text = tr_rent + ': ' + price_with_symbol
                    widget.label_rent.setText(rent_text)
                else:
                    widget.label_rent.setText('')
                
                try:
                    if int(count) > 0:
                        widget.labelc.setText(QtGui.QApplication.translate('Form', 'Available', None, QtGui.QApplication.UnicodeUTF8) + '  ' + count)
                    elif int(count) == 0:
                        widget.labelc.setText(QtGui.QApplication.translate('Form', 'Unavailable', None, QtGui.QApplication.UnicodeUTF8))
                    elif int(count) == -1:
                        widget.labelc.setText(QtGui.QApplication.translate('Form', 'Coming Soon', None, QtGui.QApplication.UnicodeUTF8))
                except:
                    widget.labelc.setText(QtGui.QApplication.translate('Form', 'Unavailable', None, QtGui.QApplication.UnicodeUTF8))

                widget.set_buy_or_rent(flag)
                widget.setLabelb(count, blue_ray)
            
            if offset > 0:
                for i in range(counts, counts + offset):
                    movie_pic = data[i]['movie_pic']
                    movie_title = data[i]['movie_title']
                    form = data[i]['form']
                    count = data[i]['available_count']
                    rfid = ''
                    blue_ray = 0
                    if 'rfid' in data[i]:
                        rfid = data[i]['rfid']
                    
                    if 'is_bluray' in data[i]:
                        blue_ray = int(data[i]['is_bluray'])
                    
                    if data[i]['sales_price'] and float(data[i]['sales_price']):
                        tr_buy = QtGui.QApplication.translate('Form', 'Buy Now', None, QtGui.QApplication.UnicodeUTF8)
                        price_with_symbol = config.symbol + data[i]['sales_price']
                        price_text = tr_buy + ': ' + price_with_symbol
                    else:
                        price_text = ''
                    if data[i]['rental_price'] and float(data[i]['rental_price']):
                        tr_rent = QtGui.QApplication.translate('Form', 'Rent', None, QtGui.QApplication.UnicodeUTF8)
                        price_with_symbol = config.symbol + data[i]['rental_price']
                        rent_text = tr_rent + ': ' + price_with_symbol
                    else:
                        rent_text = ''
                    
                    try:
                        if int(count) > 0:
                            count_txt = QtGui.QApplication.translate('Form', 'Available', None, QtGui.QApplication.UnicodeUTF8) + ' ' + count
                        elif int(count) == 0:
                            count_txt = QtGui.QApplication.translate('Form', 'Unavailable', None, QtGui.QApplication.UnicodeUTF8)
                        elif int(count) == -1:
                            count_txt = QtGui.QApplication.translate('Form', 'Coming Soon', None, QtGui.QApplication.UnicodeUTF8)
                    except:
                        count_txt = QtGui.QApplication.translate('Form', 'Unavailable', None, QtGui.QApplication.UnicodeUTF8)

                    item = labelWidget(data[i]['upc'], rfid, movie_title, form, rent_text, price_text, count_txt, movie_pic, blue_ray)
                    item.set_buy_or_rent(form)
                    item.setLabelb(count, blue_ray)
                    if i < 10:
                        item.set_pic()
                    
                    self.setCellWidget(i / self.colCount, i % self.colCount, item)
                
            else:
                for i in range(counts, counts - offset):
                    w = self.cellWidget(i / self.colCount, i % self.colCount)
                    self.removeCellWidget(i / self.colCount, i % self.colCount)
                    del w
                

    '\n    def setMovieList_old(self, data):\n        if not data:\n            print \'[setMovieList] Error: data can not be NULL!\'\n            return -1\n\n        self.clear()\n        data = data[\'ctr_movie_list\']\n        if not data:\n            self.setRowCount(0)\n            return \n\n        length = len(data)\n        rowCount = (length+self.colCount-1)/self.colCount \n\n        self.setRowCount(rowCount)\n        \n        # Set row height\n        for row in range(rowCount):\n            self.setRowHeight(row, self.rowHeight)\n\n        # Set items\n        for i in range(length):\n\n            movie_pic = data[i][\'movie_pic\']\n            movie_title = data[i][\'movie_title\']\n            count = data[i][\'available_count\']\n            if data[i].has_key("is_bluray") and data[i][\'is_bluray\'] == "1":\n                blue_ray = 1\n            else:\n                blue_ray = 0\n    \n            # create widget\n            item = labelWidget(data[i][\'upc\'], movie_title, count, movie_pic, blue_ray)\n            self.setCellWidget(i/self.colCount, i%self.colCount, item)\n    '


class labelWidget(QtGui.QWidget):
    
    def __init__(self, id, rfid = '', txt = '', form = '', rent_txt = '', price_txt = '', count = '', pic = '', blueray = 0, parent = None, wid = 'RentMainForm', width = 20 + config.pic_width, height = 20 + config.pic_height + 70):
        QtGui.QWidget.__init__(self, parent)
        self.sq = socketQuery()
        frame = QtGui.QFrame(self)
        frame.setGeometry(0, 0, width, height)
        self.wid = wid
        self.id = id
        self.rfid = rfid
        self.pic = pic
        self.setFixedSize(width, height + 10)
        margin = 5
        self.labelt = QtGui.QLabel(txt, self)
        self.labelt.setGeometry(margin, 10 + config.pic_height, width - 2 * margin, 40)
        self.labelt.setFixedSize(width - 2 * margin, 40)
        self.labelp = QtGui.QLabel(self)
        self.labelp.setScaledContents(True)
        self.labelp.setGeometry((width - config.pic_width) / 2, (width - config.pic_width) / 2, config.pic_width, config.pic_height)
        self.labelb = QtGui.QLabel(self.labelp)
        self.labelb.setGeometry(self.labelp.width() - 56, self.labelp.height() - 22, 56, 22)
        self.labelb.hide()
        self.label_rent = QtGui.QLabel(rent_txt, self)
        self.label_rent.setStyleSheet('font:bold 12px;color:yellow;')
        self.label_rent.setAlignment(QtCore.Qt.AlignCenter)
        self.label_price = QtGui.QLabel(price_txt, self)
        self.label_price.setStyleSheet('font:bold 12px;color:yellow;')
        self.label_price.setAlignment(QtCore.Qt.AlignCenter)
        self.labelc = QtGui.QLabel(count, self)
        self.labelc.setAlignment(QtCore.Qt.AlignCenter)
        self.labelc.setStyleSheet('font:12px;color:white;')
        self.labelt.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.labelt.setWordWrap(True)
        self.setStyleSheet(config.style_labelWidget)
        self.labelt.setStyleSheet('QLabel {border:0px solid red;font:bold 13px;color:white;}')
        self._has_pic = False

    
    def set_pic(self):
        if not (self._has_pic):
            self.labelp.setPixmap(QtGui.QPixmap(self.pic))
            self._has_pic = True
        

    
    def set_buy_or_rent(self, buy_or_rent):
        margin = 5
        width = 20 + config.pic_width
        height = 20 + config.pic_height + 70
        self.labelt.setStyleSheet('QLabel {font:bold 13px;color:white;}')
        self.labelc.setGeometry(5, 15 + config.pic_height + 60, width - 10, 15)
        self.labelc.setStyleSheet('font:12px;color:white;')
        self.label_price.show()
        self.label_rent.show()
        self.setFixedSize(width, height + 10)
        if buy_or_rent == 'BUY':
            self.label_price.setGeometry(margin - 2, 10 + config.pic_height + 40, width - 8, 16)
            self.label_price.setStyleSheet('font:bold 12px;color:yellow;')
            self.label_rent.setGeometry(margin - 2, 10 + config.pic_height + 52, width - 8, 18)
            self.label_rent.hide()
            self.label_rent.setStyleSheet('font:10px;color:white;')
            self.labelc.show()
        elif buy_or_rent == 'RENT':
            self.label_rent.setGeometry(margin - 2, 10 + config.pic_height + 42, width - 8, 16)
            self.label_rent.setStyleSheet('font:bold 13px;color:yellow;')
            self.label_rent.show()
            self.label_price.setGeometry(margin - 2, 10 + config.pic_height + 60, width - 8, 18)
            self.label_price.setStyleSheet('font:13px;color:white;')
            self.labelc.hide()
        else:
            self.label_price.hide()
            self.label_rent.hide()
            self.labelt.setStyleSheet('QLabel {font:bold 15px;color:white;}')
            self.labelc.setGeometry(5, 15 + config.pic_height + 45, width - 10, 20)
            self.labelc.setStyleSheet('font:14px;color:yellow;')
            self.setFixedSize(width, height)
            self.update()

    
    def setLabelb(self, count, blueray):
        if count == '0':
            self.labelb.show()
            self.labelb.setPixmap(QtGui.QPixmap(config.pic_small_notavailable))
            self.labelc.show()
            self.label_price.hide()
            self.label_rent.hide()
        elif blueray == 1:
            self.labelb.show()
            self.labelb.setPixmap(QtGui.QPixmap(config.pic_blueray_small))
        elif blueray == 0:
            self.labelb.show()
            self.labelb.setPixmap(QtGui.QPixmap(config.pic_dvd_small))
        else:
            self.labelb.hide()

    
    def mouseReleaseEvent(self, event):
        self.labelp.setFrameStyle(QtGui.QFrame.NoFrame)
        self.sendUpc()
        event.accept()

    
    def mouseMoveEvent(self, event):
        event.accept()

    
    def mousePressEvent(self, event):
        self.labelp.setLineWidth(2)
        self.labelp.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)
        event.accept()

    
    def sendUpc(self):
        data = { }
        data['wid'] = self.wid
        data['cid'] = 'ctr_movie_list'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info']['ctr_movie_list'] = { }
        data['param_info']['ctr_movie_list']['upc'] = str(self.id)
        data['param_info']['ctr_movie_list']['rfid'] = str(self.rfid)
        self.sq.send(data)



class ListWidget(QtGui.QWidget):
    
    def __init__(self, parent = None, picWidth = 50, picHeight = 75, flag = 0):
        QtGui.QWidget.__init__(self, parent)
        self.setStyleSheet(config.table_bg_style)
        self.hlabel = QtGui.QLabel(QtGui.QApplication.translate('Form', '  Disc Information', None, QtGui.QApplication.UnicodeUTF8), self)
        self.hlabel.setStyleSheet(config.style_hlabel)
        if flag:
            self.hlabel.setStyleSheet(config.table_title_style)
        
        self.hlabel.setGeometry(0, 0, config.unload_list_width + 1, 60)
        self.list = QtGui.QListWidget(self)
        self.list.setGeometry(0, 60, config.unload_list_width, 75 * 5 + 4)
        self.list.setStyleSheet('QListView {font:bold 20px; } ' + config.scroll_style)
        self.line = QtGui.QFrame(self)
        self.line.setGeometry(QtCore.QRect(0, 60 + 75 * 5 + 6, config.unload_list_width + 1, 16))
        self.line.setLineWidth(0)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        if flag:
            self.line.setStyleSheet(config.table_btm_style)
        else:
            self.line.setStyleSheet('background-image: url(' + config.pic_btm_table_green + ')')
        self.list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list.setSpacing(10)
        self.list.setWordWrap(True)
        self.list.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.list.setFocusPolicy(QtCore.Qt.NoFocus)
        self.list.setFrameStyle(QtGui.QFrame.NoFrame)
        self.list.setIconSize(QtCore.QSize(picWidth, picHeight - 10))

    
    def setDVDList(self, data):
        if not data:
            print('[setDVDList] Error: data can not be NULL!')
            return -1
        
        self.list.clear()
        data = data['ctr_dvd_list']
        if not data:
            return None
        
        for item in data:
            movie_title = item['movie_title']
            movie_pic = item['movie_pic']
            widgetItem = QtGui.QListWidgetItem(self.list)
            widgetItem.setText(movie_title)
            widgetItem.setIcon(QtGui.QIcon(movie_pic))
        



class ListWidget_2(QtGui.QListWidget):
    
    def __init__(self, parent = None, picWidth = config.pic_width_little, picHeight = config.pic_height_little):
        QtGui.QListWidget.__init__(self, parent)
        self.setStyleSheet('color: white; font: bold 15px; background-color: transparent; padding: 6px')
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setSpacing(10)
        self.setWordWrap(True)
        self.setIconSize(QtCore.QSize(picWidth, picHeight))
        self.dataType = 1047295

    
    def setMovieInfo(self, data):
        if not data:
            print('[setMovieInfo] Error: data can not be NULL!')
            return -1
        
        self.clear()
        data = data['ctr_movie_info']
        if not data:
            return None
        
        for i in range(len(data)):
            text = data[i]['price_plan_text']
            pic = data[i]['movie_pic']
            rfid = data[i]['rfid']
            if text and rfid:
                widgetItem = QtGui.QListWidgetItem()
                widgetItem.setText(text)
                widgetItem.setIcon(QtGui.QIcon(pic))
                widgetItem.setData(self.dataType, QtCore.QVariant(rfid))
                widgetItem.setTextAlignment(QtCore.Qt.AlignCenter)
                widgetItem.setBackgroundColor(QtGui.QColor(0, 96, 116, 50))
                self.addItem(widgetItem)
            
        



class ListView(QtGui.QWidget):
    
    def __init__(self, parent, x, y, width = 238, height = 110):
        QtGui.QWidget.__init__(self, parent)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sq = socketQuery()
        self.label_height = 40
        self.list_height = self.label_height * 5 + 20
        listStyle = config.style_listview_list
        btnStyle = config.style_listview_btn
        self.labelStyle = config.style_listview_label
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_shopping_cart)))
        self.setPalette(palette)
        self.label = QtGui.QLabel(QtGui.QApplication.translate('Form', '  Shopping Cart', None, QtGui.QApplication.UnicodeUTF8), self)
        self.label.setStyleSheet(config.style_label)
        self.label.setGeometry(0, 0, width, 44)
        self.listWidget = QtGui.QListWidget(self)
        self.listWidget.setGeometry(QtCore.QRect(7, 44, width - 14, self.list_height))
        self.listWidget.setStyleSheet(listStyle)
        self.listWidget.setSpacing(4)
        self.listWidget.hide()
        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL('itemClicked(QListWidgetItem *)'), self.sendCmd)
        self.txt_show = QtGui.QApplication.translate('ShoppingCart', 'Show', None, QtGui.QApplication.UnicodeUTF8)
        self.txt_hide = QtGui.QApplication.translate('ShoppingCart', 'Hide', None, QtGui.QApplication.UnicodeUTF8)
        self.layout = QtGui.QWidget(self)
        self.layout.setGeometry(0, 44, width, 66)
        hboxlayout = QtGui.QHBoxLayout(self.layout)
        hboxlayout.setSpacing(0)
        self.btn_hide = QtGui.QPushButton(self.txt_show)
        self.btn_hide.setStyleSheet(btnStyle)
        self.btn_hide.setFixedSize(QtCore.QSize(100, 50))
        hboxlayout.addWidget(self.btn_hide)
        self.btn_view_cart = QtGui.QPushButton(QtGui.QApplication.translate('Form', 'View', None, QtGui.QApplication.UnicodeUTF8), self)
        self.btn_view_cart.setStyleSheet(btnStyle)
        self.btn_view_cart.setFixedSize(QtCore.QSize(100, 50))
        hboxlayout.addWidget(self.btn_view_cart)
        QtCore.QObject.connect(self.btn_hide, QtCore.SIGNAL('clicked()'), self.hide_click)
        QtCore.QObject.connect(self.btn_view_cart, QtCore.SIGNAL('clicked()'), self.sendCmd)
        self.show = 0

    
    def hideCart(self):
        self.listWidget.hide()
        self.btn_hide.setText(self.txt_show)
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.layout.setGeometry(QtCore.QRect(0, 44, self.width, 66))
        self.show = 0

    
    def showCart(self):
        self.listWidget.show()
        self.btn_hide.setText(self.txt_hide)
        self.setGeometry(self.x, self.y - self.list_height, self.width, self.height + self.list_height)
        self.layout.setGeometry(QtCore.QRect(0, 44 + self.list_height, self.width, 66))
        self.show = 1

    
    def hide_click(self):
        if not (self.show):
            self.showCart()
        else:
            self.hideCart()

    
    def setTabList(self, data):
        if not data:
            return -1
        
        self.listWidget.clear()
        data = data['ctr_shopping_cart']
        if data:
            for i in range(len(data)):
                text = data[i]['movie_title']
                item = QtGui.QListWidgetItem('', self.listWidget)
                label = QtGui.QLabel(text, self)
                label.setStyleSheet(self.labelStyle)
                self.listWidget.setItemWidget(item, label)
            
        

    
    def sendCmd(self):
        data = { }
        data['wid'] = 'RentMainForm'
        data['cid'] = 'ctr_shopping_cart'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info']['ctr_shopping_cart'] = { }
        self.sq.send(data)



class messageBox(QtGui.QWidget):
    
    def __init__(self, wid, parent, width = config.messageBox_width, height = config.messageBox_height):
        QtGui.QWidget.__init__(self)
        self.parent = parent
        self.wid = wid
        self.sq = socketQuery()
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(QtCore.Qt.X11BypassWindowManagerHint)
        self.setProperty('cursor', QtCore.QVariant(QtCore.Qt.BlankCursor))
        self.setGeometry((768 - width) / 2, (1024 - height) / 2, width, height)
        palette = QtGui.QPalette()
        '\n        gradient = QtGui.QRadialGradient(width/2, height/2, 250, width/2, height/2)\n        gradient.setColorAt(0, QtGui.QColor(1, 90, 124))\n        gradient.setColorAt(1, QtGui.QColor(47, 65, 84))\n        brush = QtGui.QBrush(gradient)\n        palette.setBrush(self.backgroundRole(), brush)\n        '
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QColor(*config.messagebox_bg)))
        self.setPalette(palette)
        self.frame = QtGui.QFrame(self)
        self.frame.setGeometry(10, 10, width - 20, height - 20)
        self.frame.setStyleSheet(config.messagebox_form)
        palettef = QtGui.QPalette()
        palettef.setColor(QtGui.QPalette.Foreground, QtGui.QColor(*config.messagebox_text))
        self.width = width
        self.height = height
        btn_height = 54
        btn_width = 124
        self.btn_height = btn_height
        self.btn_width = btn_width
        layout_x = 40
        layout_y = height - layout_x - btn_height
        layout_width = width - 2 * layout_x
        layout_height = btn_height + 20
        self.layout_x = layout_x
        self.layout_y = layout_y
        self.layout_width = layout_width
        self.layout_height = layout_height
        self.label = QtGui.QLabel(self)
        self.label.setGeometry(layout_x, layout_x, layout_width, height - layout_height - (2 * layout_x + 10))
        self.label.setFont(font)
        self.label.setPalette(palettef)
        self.label.setWordWrap(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.hBoxLayout = QtGui.QWidget(self)
        self.hBoxLayout.setGeometry(QtCore.QRect(layout_x, layout_y, layout_width, layout_height))
        layout = QtGui.QHBoxLayout(self.hBoxLayout)
        self.btn_ok_style = 'color: white; font: bold 24px; border-style: outset; background-image: url(' + config.pic_btn_kb_ok + ')'
        self.btn_cancel_style = 'color: white; font: bold 24px; border-style: outset; background-image: url(' + config.pic_btn_kb_close + ')'
        self.pressStyle = 'background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #b0cfe4, stop:0.4 #005999, stop:0.6 #005999, stop:1 #b0cfe4); color: white; font: bold 24px; border-radius: 8px; margin: 2px'
        self.btn_ok = QtGui.QPushButton(QtGui.QApplication.translate('Form', 'Ok', None, QtGui.QApplication.UnicodeUTF8), self)
        self.btn_ok.setFixedSize(btn_width, btn_height)
        self.btn_ok.setStyleSheet(self.btn_ok_style)
        self.btn_cancel = QtGui.QPushButton(QtGui.QApplication.translate('Form', 'Cancel', None, QtGui.QApplication.UnicodeUTF8), self)
        self.btn_cancel.setFixedSize(btn_width, btn_height)
        self.btn_cancel.setStyleSheet(self.btn_cancel_style)
        layout.addWidget(self.btn_cancel)
        layout.addWidget(self.btn_ok)
        self.hide()
        QtCore.QObject.connect(self.btn_ok, QtCore.SIGNAL('clicked()'), self.btn_ok_click)
        QtCore.QObject.connect(self.btn_cancel, QtCore.SIGNAL('clicked()'), self.btn_cancel_click)
        QtCore.QObject.connect(self.btn_ok, QtCore.SIGNAL('pressed()'), self.btn_ok_press)
        QtCore.QObject.connect(self.btn_cancel, QtCore.SIGNAL('pressed()'), self.btn_cancel_press)

    
    def show(self, data):
        if not data:
            return -1
        
        type = data['type']
        text = data['message']
        self.label.setText(text)
        if type != 'confirm' and type != 'continue':
            self.btn_cancel.hide()
        else:
            self.btn_cancel.show()
        self.parent.setDisabled(True)
        self.btn_ok.setText(QtGui.QApplication.translate('Form', 'Ok', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_cancel.setText(QtGui.QApplication.translate('Form', 'Cancel', None, QtGui.QApplication.UnicodeUTF8))
        if type == 'continue':
            self.btn_ok.setText(QtGui.QApplication.translate('Form', 'Continue', None, QtGui.QApplication.UnicodeUTF8))
            self.btn_cancel.setText(QtGui.QApplication.translate('Form', 'Quit', None, QtGui.QApplication.UnicodeUTF8))
            self.label.setGeometry(self.layout_x, self.layout_x - 20, self.layout_width, self.height - 40)
            self.label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            self.setFixedSize(self.width, self.height + 50)
            self.frame.setFixedSize(self.width - 20, self.height + 30)
            self.hBoxLayout.setGeometry(QtCore.QRect(self.layout_x, self.layout_y + 30, self.layout_width, self.layout_height + 70))
        else:
            self.label.setGeometry(self.layout_x, self.layout_x, self.layout_width, self.height - self.layout_height - (2 * self.layout_x + 10))
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            self.setFixedSize(self.width, self.height)
            self.frame.setFixedSize(self.width - 20, self.height - 20)
            self.hBoxLayout.setGeometry(QtCore.QRect(self.layout_x, self.layout_y, self.layout_width, self.layout_height))
        self.showNormal()

    
    def closeEvent(self, event):
        self.parent.setEnabled(True)
        self.close()

    
    def hideEvent(self, event):
        self.parent.setEnabled(True)
        self.hide()

    
    def btn_ok_click(self):
        data = { }
        data['wid'] = self.wid
        data['cid'] = self.wid + '_ctr_message_box'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info'][data['cid']] = { }
        data['param_info'][data['cid']]['val'] = 'yes'
        self.sq.send(data)
        self.btn_ok.setStyleSheet(self.btn_ok_style)
        self.close()

    
    def btn_cancel_click(self):
        data = { }
        data['wid'] = self.wid
        data['cid'] = self.wid + '_ctr_message_box'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info'][data['cid']] = { }
        data['param_info'][data['cid']]['val'] = 'no'
        self.sq.send(data)
        self.btn_cancel.setStyleSheet(self.btn_cancel_style)
        self.close()

    
    def btn_ok_press(self):
        self.btn_ok.setStyleSheet(self.pressStyle)

    
    def btn_cancel_press(self):
        self.btn_cancel.setStyleSheet(self.pressStyle)



class Return_messageBox(QtGui.QWidget):
    
    def __init__(self, wid, parent, width = config.return_messageBox_width, height = config.return_messageBox_height):
        QtGui.QWidget.__init__(self)
        self.parent = parent
        self.wid = wid
        self.sq = socketQuery()
        self.setGeometry((768 - width) / 2, (1024 - height) / 2, width, height)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.X11BypassWindowManagerHint)
        self.setWindowOpacity(0.8)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QColor(*config.messagebox_bg)))
        self.setPalette(palette)
        frame = QtGui.QFrame(self)
        frame.setGeometry(10, 10, width - 20, height - 20)
        frame.setStyleSheet(config.messagebox_form)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Foreground, QtGui.QColor(255, 255, 255))
        layout_x = 40
        layout_y = 20
        self.label = QtGui.QLabel(self)
        self.label.setGeometry(layout_x, layout_y, width - 2 * layout_x, height / 2)
        self.label.setFont(font)
        self.label.setPalette(pal)
        self.label.setWordWrap(True)
        layout_x = 80
        Vwidget = QtGui.QWidget(self)
        Vwidget.setGeometry(layout_x, 0, width - 2 * layout_x, height)
        Vwidget.setStyleSheet('background-color: transparent')
        layout = QtGui.QVBoxLayout()
        self.btn_yes = QtGui.QPushButton(QtGui.QApplication.translate('ReturnForm', 'Yes, purchase now', None, QtGui.QApplication.UnicodeUTF8), Vwidget)
        self.btn_no = QtGui.QPushButton(QtGui.QApplication.translate('ReturnForm', 'No, return only', None, QtGui.QApplication.UnicodeUTF8), Vwidget)
        self.btn_yes.setStyleSheet('QPushButton { border-radius: 10px; border-width: 1px;border-color: #FFFFFF; background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #004c22, stop:0.5 #009244, stop:1 #004c22); color: #FFFFFF; font: bold 30px; border-style: outset;} QPushButton:pressed {background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #b0cfe4, stop:0.4 #005999, stop:0.6 #005999, stop:1 #b0cfe4); color: white; font: bold 30px; border-radius: 10px;}')
        self.btn_no.setStyleSheet('QPushButton { border-radius: 10px; border-width: 1px;border-color: #FFFFFF; background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #7c2c00, stop:0.5 #c57c00, stop:1 #7c2c00); color: #FFFFFF; font: bold 30px; border-style: outset;} QPushButton:pressed {background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #b0cfe4, stop:0.4 #005999, stop:0.6 #005999, stop:1 #b0cfe4); color: white; font: bold 30px; border-radius: 10px;}')
        self.btn_yes.setFixedHeight(54)
        self.btn_no.setFixedHeight(54)
        layout.addStretch(1)
        layout.addWidget(self.btn_yes)
        layout.addSpacing(50)
        layout.addWidget(self.btn_no)
        layout.addSpacing(10)
        Vwidget.setLayout(layout)
        QtCore.QObject.connect(self.btn_yes, QtCore.SIGNAL('clicked()'), self.btn_yes_click)
        QtCore.QObject.connect(self.btn_no, QtCore.SIGNAL('clicked()'), self.btn_no_click)
        self.hide()

    
    def btn_yes_click(self):
        data = { }
        data['wid'] = self.wid
        data['cid'] = self.wid + '_ctr_message_box'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info'][data['cid']] = { }
        data['param_info'][data['cid']]['val'] = 'yes'
        self.sq.send(data)
        self.close()

    
    def btn_no_click(self):
        data = { }
        data['wid'] = self.wid
        data['cid'] = self.wid + '_ctr_message_box'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info'][data['cid']] = { }
        data['param_info'][data['cid']]['val'] = 'no'
        self.sq.send(data)
        self.close()

    
    def show(self, data):
        if not data:
            return -1
        
        type = data['type']
        text = data['message']
        self.label.setText(text)
        self.parent.setDisabled(True)
        self.btn_yes.setText(QtGui.QApplication.translate('ReturnForm', 'Yes, purchase now', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_no.setText(QtGui.QApplication.translate('ReturnForm', 'No, return only', None, QtGui.QApplication.UnicodeUTF8))
        self.showNormal()

    
    def closeEvent(self, event):
        self.parent.setEnabled(True)
        self.close()

    
    def hideEvent(self, event):
        self.parent.setEnabled(True)
        self.hide()



class virtualComponent(QtGui.QWidget):
    
    def __init__(self, parent = None, count = 5, width = 500, height = 500):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent

    
    def clearDetail(self):
        self.parent.clearDetail()

    
    def initLanguage(self, param):
        self.parent.initLanguage(param)

    
    def setMovieDetail(self, param):
        self.parent.setMovieDetail(param)

    
    def setMoviePrice(self, param):
        self.parent.setMoviePrice(param)

    
    def setCartInfo(self, param):
        self.parent.setCartInfo(param)

    
    def setCouponInfo(self, param):
        self.parent.setCouponInfo(param)

    
    def setReport(self, param):
        self.parent.setReport(param)

    
    def setMovieInfo(self, param):
        pass

    
    def setVideoVolume(self, param):
        self.parent.setVideoVolume(param)

    
    def closeTrailer(self):
        pass

    
    def play(self):
        pass

    
    def stop(self):
        pass



class CerepayCenterList(QtGui.QLabel):
    
    def __init__(self, parent, wid = '', cid = ''):
        QtGui.QLabel.__init__(self, parent)
        hlayout = QtGui.QHBoxLayout(self)
        hlayout.setContentsMargins(20, 0, 0, 0)
        self.cid = cid
        self.wid = wid
        self.parent = parent
        self.listWidget_title = QtGui.QListWidget(self)
        self.listWidget_title.setEnabled(False)
        self.listWidget_title.setFocusPolicy(QtCore.Qt.NoFocus)
        self.listWidget_title.setSpacing(3)
        self.listWidget_title.setWordWrap(True)
        self.listWidget_title.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget_title.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget_title.setResizeMode(QtGui.QListView.Adjust)
        self.listWidget_info = QtGui.QListWidget(self)
        self.listWidget_info.setEnabled(False)
        self.listWidget_info.setFocusPolicy(QtCore.Qt.NoFocus)
        self.listWidget_info.setSpacing(3)
        self.listWidget_info.setWordWrap(True)
        self.listWidget_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget_info.setResizeMode(QtGui.QListView.Adjust)
        style = 'QListView {font: 20px; border: none; background-color: transparent; selection-background-color: transparent}\n                    QListView::item {background-color: transparent;} \n                    QListView::item:selected {background-color: transparent;}'
        self.listWidget_title.setStyleSheet(style)
        hlayout.addWidget(self.listWidget_title)
        self.listWidget_info.setStyleSheet(style)
        hlayout.addWidget(self.listWidget_info, 1)

    
    def setCerepayCenterList(self, data):
        data = data['info_list']
        self.listWidget_title.clear()
        self.listWidget_info.clear()
        for i in range(len(data)):
            title = data[i]['title'] + ' :'
            info = data[i]['info']
            item_title = QtGui.QListWidgetItem(title, self.listWidget_title)
            item_title.setTextColor(QtGui.QColor(0, 96, 100))
            item_info = QtGui.QListWidgetItem(info, self.listWidget_info)
            item_info.setTextColor(QtGui.QColor(121, 0, 0))
        



class RecommendationList(QtGui.QFrame):
    
    def __init__(self, parent, wid = 'MembershipCenterForm'):
        QtGui.QWidget.__init__(self, parent)
        self.setFrameStyle(QtGui.QFrame.Box)
        self.wid = wid
        self.cid = 'ctr_movie_list'
        self.sq = socketQuery()
        self.pic_w = 40 + config.pic_width
        pic_h = config.pic_height + 70
        self.hlabel = QtGui.QLabel()
        self.hlabel.setStyleSheet(config.style_RecommendationList_hlabel)
        self.hlabel.setFixedHeight(45)
        self.table = QtGui.QTableWidget()
        self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setFrameStyle(QtGui.QFrame.NoFrame)
        self.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.table.setIconSize(QtCore.QSize(self.pic_w, pic_h))
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().hide()
        self.table.setStyleSheet(config.scroll_h)
        self.table.setFixedSize(4 * (self.pic_w + 25), pic_h + 45)
        self.setFixedHeight(self.hlabel.height() + 20 + self.table.height())
        self.table.setRowCount(1)
        self.table.setRowHeight(0, pic_h + 20)
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.addWidget(self.hlabel)
        layout.addWidget(self.table, 0, QtCore.Qt.AlignRight)

    
    def init(self):
        self.hlabel.setText(QtGui.QApplication.translate('Form', 'Recommendations', None, QtGui.QApplication.UnicodeUTF8))

    
    def setRecommendationList(self, data):
        self.table.clear()
        if not data or not data[self.cid]:
            return None
        
        list = data[self.cid]
        self.table.setColumnCount(len(list))
        for i in range(len(list)):
            pic = list[i]['movie_pic']
            movie_title = list[i]['movie_title']
            upc = str(list[i]['upc'])
            rfid = ''
            if 'rfid' in list[i]:
                rfid = list[i]['rfid']
            
            item = labelWidget(upc, rfid, movie_title, '', pic, -1, None, self.wid, self.pic_w)
            self.table.setCellWidget(0, i, item)
            self.table.setColumnWidth(i, self.pic_w + 25)
        



class btnCenter(QtGui.QWidget):
    
    def __init__(self, parent, wid):
        QtGui.QWidget.__init__(self, parent)
        width = 460 + 79
        height = 85
        self.wid = wid
        self.cid = 'ctr_btn_center'
        self.sq = socketQuery()
        self.setGeometry(20, 0, width, height)
        self.btn_center = QtGui.QPushButton(self)
        self.btn_center.setStyleSheet(config.style_membership_btn)
        self.btn_center.setFixedSize(460, 90)
        self.btn_center.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_bg = QtGui.QLabel(self.btn_center)
        self.label_bg.setGeometry(0, height - 25, self.btn_center.width(), 25)
        self.label_bg.setStyleSheet(config.style_membership_label)
        self.label_bg.setAlignment(QtCore.Qt.AlignCenter)
        self.btn_logout = QtGui.QPushButton('Logout', self)
        self.btn_logout.setStyleSheet(config.style_membership_logout)
        self.btn_logout.setFixedSize(79, 66)
        self.btn_logout.setFocusPolicy(QtCore.Qt.NoFocus)
        hlayout = QtGui.QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)
        hlayout.setSpacing(0)
        hlayout.addWidget(self.btn_center)
        hlayout.addWidget(self.btn_logout, 0, QtCore.Qt.AlignBottom)
        self.setLayout(hlayout)
        QtCore.QObject.connect(self.btn_center, QtCore.SIGNAL('clicked()'), self.gotoCenter)
        QtCore.QObject.connect(self.btn_logout, QtCore.SIGNAL('clicked()'), self.logout)

    
    def init(self):
        self.label_bg.setText(QtGui.QApplication.translate('Form', 'Click to Membership Center', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_logout.setText('\n\n' + QtGui.QApplication.translate('Form', 'Logout', None, QtGui.QApplication.UnicodeUTF8))

    
    def setText(self, text):
        self.btn_center.setText(text)

    
    def setDisabled(self, param):
        true = param['disabled']
        if true == 'true':
            self.btn_center.setDisabled(True)
            self.btn_logout.setDisabled(True)
            self.btn_center.setStyleSheet(config.style_membership_btn_disabled)
            self.btn_logout.setStyleSheet(config.style_membership_logout_disabled)
        else:
            self.btn_center.setDisabled(False)
            self.btn_logout.setDisabled(False)
            self.btn_center.setStyleSheet(config.style_membership_btn)
            self.btn_logout.setStyleSheet(config.style_membership_logout)

    
    def gotoCenter(self):
        data = { }
        data['wid'] = self.wid
        data['cid'] = self.cid
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = {
            'cmd': 'center' }
        self.sq.send(data)

    
    def logout(self):
        data = { }
        data['wid'] = self.wid
        data['cid'] = self.cid
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = {
            'cmd': 'logout' }
        self.sq.send(data)



class ctrButton(QtGui.QPushButton):
    
    def __init__(self, parent, wid, cid, text = '', width = 160, height = 68, style = config.style_ctrBtn):
        QtGui.QPushButton.__init__(self, parent)
        self.style = style
        self.txt = text
        if text:
            self.setText(text)
        
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)
        self.setStyleSheet(style)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sq = socketQuery()
        self.wid = wid
        self.cid = cid

    
    def mouseReleaseEvent(self, event):
        self.setStyleSheet(self.style)
        data = { }
        data['wid'] = self.wid
        data['cid'] = self.cid
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        self.sq.send(data)
        self.releaseMouse()

    
    def mousePressEvent(self, event):
        self.setStyleSheet('background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #b0cfe4, stop:0.4 #005999, stop:0.6 #005999, stop:1 #b0cfe4); color: white; font: bold 30px; border-radius: 8px; margin: 3px')

    
    def reset(self, text):
        self.setText(QtGui.QApplication.translate('Form', text, None, QtGui.QApplication.UnicodeUTF8))

    
    def _update_parent_ui(self):
        self.parent().parent().update()



class btnBack(ctrButton):
    
    def __init__(self, parent, wid):
        ctrButton.__init__(self, parent, wid, 'btn_back', QtGui.QApplication.translate('Component', 'Back', None, QtGui.QApplication.UnicodeUTF8))

    
    def reset(self):
        self.setText(QtGui.QApplication.translate('Component', 'Back', None, QtGui.QApplication.UnicodeUTF8))

    
    def setDisable(self, param):
        true = param['disabled']
        if true == 'true':
            self.setDisabled(True)
        else:
            self.setDisabled(False)



class btnCancel(ctrButton):
    
    def __init__(self, parent, wid):
        ctrButton.__init__(self, parent, wid, 'btn_cancel', QtGui.QApplication.translate('Component', 'Exit', None, QtGui.QApplication.UnicodeUTF8), 159, 68, config.style_btnCancel)

    
    def reset(self):
        self.setText(QtGui.QApplication.translate('Component', 'Exit', None, QtGui.QApplication.UnicodeUTF8))



class btnLogout(ctrButton):
    
    def __init__(self, parent, wid):
        ctrButton.__init__(self, parent, wid, 'btn_logout', QtGui.QApplication.translate('Component', 'Exit', None, QtGui.QApplication.UnicodeUTF8))

    
    def reset(self):
        self.setText(QtGui.QApplication.translate('Component', 'Exit', None, QtGui.QApplication.UnicodeUTF8))



class btnFinish(ctrButton):
    
    def __init__(self, parent, wid):
        ctrButton.__init__(self, parent, wid, 'btn_finish', QtGui.QApplication.translate('Component', 'Finish', None, QtGui.QApplication.UnicodeUTF8), 159, 68, config.style_btnFinish)

    
    def reset(self):
        self.setText(QtGui.QApplication.translate('Component', 'Finish', None, QtGui.QApplication.UnicodeUTF8))



class strButton(QtGui.QPushButton):
    
    def __init__(self, parent = None, text = '', width = 63, height = 58, style = ''):
        QtGui.QPushButton.__init__(self, text, parent)
        self.setText(text)
        self.t = text
        self.setFixedSize(width, height)
        self.style = style
        self.setStyleSheet(style)
        QtCore.QObject.connect(self, QtCore.SIGNAL('pressed()'), self.press)
        QtCore.QObject.connect(self, QtCore.SIGNAL('released()'), self.release)

    
    def press(self):
        self.setStyleSheet('background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #005070, stop:1 #e0e0ff); color: white; font: bold 42px; border-radius: 8px;')

    
    def release(self):
        self.setStyleSheet(self.style)
        text = self.text()
        if text:
            self.emit(QtCore.SIGNAL('mousePress(QString)'), text)
        

    
    def showEvent(self, e):
        if self.t in [
            'Del',
            'Shift',
            'Enter',
            'Space',
            'Close']:
            self.setText(QtGui.QApplication.translate('Form', self.t, None, QtGui.QApplication.UnicodeUTF8))
        



class TabList(QtGui.QWidget):
    
    def __init__(self, parent = None, width = 238, height = config.movieList_height - 130):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedSize(width, height)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_gener_list)))
        self.setPalette(palette)
        self.labelStyle = config.style_tablist_label
        self.selectedStyle = config.style_tablist_selected
        self.sq = socketQuery()
        self.txt_gener_title = QtGui.QLabel(self)
        self.txt_gener_title.setGeometry(QtCore.QRect(10, 5, width - 20, 20))
        listStyle = 'background-color: transparent; border: 0px; font: bold 24px; selection-background-color: transparent'
        self.listWidget = QtGui.QListWidget(self)
        self.listWidget.setGeometry(QtCore.QRect(10, self.txt_gener_title.height() + 5, width - 20, height - self.txt_gener_title.height() - 15))
        self.listWidget.setStyleSheet(listStyle)
        self.listWidget.setSpacing(5)
        self.listWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.preData = { }
        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL('currentItemChanged(QListWidgetItem *, QListWidgetItem *)'), self.sendCmd)

    
    def sendCmd(self, current, pre):
        if not current or not pre:
            return None
        
        data = { }
        data['wid'] = 'RentMainForm'
        data['cid'] = 'ctr_tab_list'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info']['ctr_tab_list'] = { }
        data['param_info']['ctr_tab_list']['genre'] = current.data(255).toString().toLocal8Bit().data()
        self.sq.send(data)
        pre_row = self.listWidget.row(pre)
        cur_row = self.listWidget.row(current)
        if self.preData['ctr_tab_list'][pre_row]['color']:
            self.listWidget.itemWidget(pre).setStyleSheet(self.labelStyle + ';color: #ff0000;')
        else:
            self.listWidget.itemWidget(pre).setStyleSheet(self.labelStyle)
        if self.preData['ctr_tab_list'][cur_row]['color']:
            self.listWidget.itemWidget(current).setStyleSheet(self.selectedStyle + ';background-color:qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop:0 #ff0303,stop:1 #ffd0d3);')
        else:
            self.listWidget.itemWidget(current).setStyleSheet(self.selectedStyle)

    
    def setTabList(self, data):
        if not data:
            print('[setTabList] Error: data can not be NULL!')
            return -1
        
        self.preData = data
        self.listWidget.clear()
        focus = data['focus']
        data = data['ctr_tab_list']
        if not data:
            return None
        
        for i in range(len(data)):
            item = QtGui.QListWidgetItem('', self.listWidget)
            item.setData(255, QtCore.QVariant(data[i]['id']))
            label = QtGui.QLabel(data[i]['text'], self)
            if data[i]['id'] == focus:
                self.listWidget.setCurrentRow(i)
                if data[i]['color']:
                    label.setStyleSheet(self.selectedStyle + ';background-color:qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop:0 #ff0303,stop:1 #ffd0d3);')
                else:
                    label.setStyleSheet(self.selectedStyle)
            elif data[i]['color']:
                label.setStyleSheet(self.labelStyle + ';color: #ff0000;')
            else:
                label.setStyleSheet(self.labelStyle)
            self.listWidget.setItemWidget(item, label)
        



class numKeyboard(QtGui.QWidget):
    
    def __init__(self, wid, parent = None, x = (768 - config.bg_kb_width) / 2, y = 894 - config.bg_kb_height, width = config.bg_kb_width, height = config.bg_kb_height, count = 4, flag = 0):
        QtGui.QWidget.__init__(self, parent)
        self.resize(0, 0)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_kb_num)))
        self.setPalette(palette)
        self.wid = wid
        self.x = x
        self.y = y
        self.data = ''
        self.sq = socketQuery()
        btnStyle = config.style_numK
        btnWidth = config.btn_kb_width
        btnHeight = config.btn_kb_height
        space = 10
        line_x = 30
        line_y = 20
        line_width = (btnWidth + space) * 3
        line_height = btnHeight - 20
        self.lineedit = QtGui.QLineEdit(self)
        self.lineedit.setGeometry(line_x + space + 5, line_y + space, line_width - 5, line_height)
        self.lineedit.setStyleSheet(config.style_numK_line)
        btn_close = strButton(self, '', btnWidth, line_height, 'border-style: outset; background-image: url(' + config.pic_icon_close + ')')
        btn_close.setGeometry(self.lineedit.x() + line_width + 2 * space + 4, self.lineedit.y(), btnWidth, line_height)
        layout = QtGui.QWidget(self)
        layout.setGeometry(line_x, line_y + line_height + space, line_width + 3 * space, (btnHeight + space) * 3 + space)
        grid = QtGui.QGridLayout(layout)
        grid.setVerticalSpacing(3)
        grid.setHorizontalSpacing(space + 3)
        for i in range(9):
            btn = strButton(self, str(i + 1), btnWidth, btnHeight, btnStyle)
            btn.setFixedSize(btnWidth, btnHeight)
            self.connect(btn, QtCore.SIGNAL('mousePress(QString)'), self.mousePress)
            grid.addWidget(btn, i / 3, i % 3)
        
        btn_del = strButton(self, '', btnWidth, btnHeight, config.style_numK_btndel)
        btn_del.setGeometry(btn_close.x(), layout.y() + space + 3, btnWidth, btnHeight)
        self.btn_ok = strButton(self, self.tr('Enter'), btnWidth, 3 * btnHeight + space - 3, config.style_numK_btnok)
        self.btn_ok.setGeometry(btn_close.x(), btn_del.y() + btnHeight + space, btnWidth, 3 * btnHeight + space - 3)
        if not flag:
            btn = strButton(self, '0', (btnWidth + space) * 3 - 3, btnHeight, config.style_numK_btn0)
            btn.setGeometry(line_x + space + 2, layout.y() + layout.height() - 5, (btnWidth + space) * 3 + 5, btnHeight)
            QtCore.QObject.connect(self.btn_ok, QtCore.SIGNAL('clicked()'), self.kb_ok_click)
        else:
            btn = strButton(self, '0', btnWidth, btnHeight, btnStyle)
            btn.setGeometry(line_x + space + 3, layout.y() + layout.height() - 6, btnWidth, btnHeight)
            btn_spot = strButton(self, '.', btnWidth, btnHeight, btnStyle)
            btn_spot.setGeometry(line_x + btnWidth + 3 * space, btn.y(), btnWidth, btnHeight)
            self.connect(btn_spot, QtCore.SIGNAL('mousePress(QString)'), self.mousePress)
            btn_clear = strButton(self, self.tr('Clear'), btnWidth, btnHeight, config.style_numK_btnclear)
            btn_clear.setGeometry(btn_spot.x() + btn_spot.width() + space + 8, btn.y(), btnWidth, btnHeight)
            QtCore.QObject.connect(btn_clear, QtCore.SIGNAL('clicked()'), self.lineedit.clear)
        self.connect(btn, QtCore.SIGNAL('mousePress(QString)'), self.mousePress)
        self.connect(self.lineedit, QtCore.SIGNAL('clear'), self.clear)
        self.connect(btn_del, QtCore.SIGNAL('clicked()'), self.lineedit.backspace)
        self.connect(btn_close, QtCore.SIGNAL('clicked()'), self.close_click)
        QtCore.QObject.connect(self.btn_ok, QtCore.SIGNAL('clicked()'), self.kb_ok_click)

    
    def close_click(self):
        data = { }
        data['wid'] = self.wid
        data['cid'] = self.wid + '_ctr_num_keyboard'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info'][data['cid']] = { }
        data['param_info'][data['cid']]['type'] = 'close'
        data['param_info'][data['cid']]['val'] = ''
        self.sq.send(data)
        self.close()

    
    def clear(self):
        self.data = ''
        self.lineedit.clear()

    
    def show(self, data = { }):
        if self.isVisible():
            return None
        
        self.data = ''
        if data:
            if data['type'] == 'password':
                self.lineedit.setEchoMode(QtGui.QLineEdit.Password)
            
        
        self.showNormal()
        for i in range(config.bg_kb_height):
            self.setGeometry(self.x, self.y + config.bg_kb_height - i, config.bg_kb_width, i)
            time.sleep(1e-06)
        

    
    def closeEvent(self, event):
        for i in range(config.bg_kb_height):
            self.setGeometry(self.x, self.y + i, config.bg_kb_width, config.bg_kb_height - i)
        
        self.lineedit.clear()
        self.close()

    
    def kb_ok_click(self):
        self.data = self.lineedit.text()
        if self.lineedit.text():
            data = { }
            data['wid'] = self.wid
            data['cid'] = self.wid + '_ctr_num_keyboard'
            data['type'] = 'EVENT'
            data['EVENT'] = 'EVENT_MOUSE_CLICK'
            data['param_info'] = { }
            data['param_info'][data['cid']] = { }
            data['param_info'][data['cid']]['type'] = 'ok'
            data['param_info'][data['cid']]['val'] = str(self.lineedit.text())
            log.info('keybord ok clicked!!!')
            self.sq.send(data)
            self.lineedit.clear()
            self.close()
        

    
    def mousePress(self, text):
        self.lineedit.insert(str(text))
        self.data = self.data + str(text)
        data = { }
        data['wid'] = self.wid
        data['cid'] = self.wid + '_ctr_num_keyboard'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info'][data['cid']] = { }
        data['param_info'][data['cid']]['type'] = 'click'
        data['param_info'][data['cid']]['val'] = ''
        self.sq.send(data)



class NumberKeyboardWithDot(QtGui.QWidget):
    
    def __init__(self, wid, parent = None, x = (768 - config.bg_kb_width) / 2, y = 894 - config.bg_kb_height, width = config.bg_kb_width, height = config.bg_kb_height, count = 4, flag = 0):
        QtGui.QWidget.__init__(self, parent)
        self.resize(0, 0)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_kb_num)))
        self.setPalette(palette)
        self.wid = wid
        self.x = x
        self.y = y
        self.data = ''
        self._socketQuery = socketQuery()
        btnStyle = config.style_numK
        btnWidth = config.btn_kb_width
        btnHeight = config.btn_kb_height
        space = 10
        line_x = 30
        line_y = 20
        line_width = (btnWidth + space) * 3
        line_height = btnHeight - 20
        self.lineedit = QtGui.QLineEdit(self)
        self.lineedit.setGeometry(line_x + space + 5, line_y + space, line_width - 5, line_height)
        self.lineedit.setStyleSheet(config.style_numK_line)
        btn_close = strButton(self, '', btnWidth, line_height, 'border-style: outset; background-image: url(' + config.pic_icon_close + ')')
        btn_close.setGeometry(self.lineedit.x() + line_width + 2 * space + 4, self.lineedit.y(), btnWidth, line_height)
        layout = QtGui.QWidget(self)
        layout.setGeometry(line_x, line_y + line_height + space, line_width + 3 * space, (btnHeight + space) * 3 + space)
        grid = QtGui.QGridLayout(layout)
        grid.setVerticalSpacing(3)
        grid.setHorizontalSpacing(space + 3)
        for i in range(9):
            btn = strButton(self, str(i + 1), btnWidth, btnHeight, btnStyle)
            btn.setFixedSize(btnWidth, btnHeight)
            self.connect(btn, QtCore.SIGNAL('mousePress(QString)'), self.mousePress)
            grid.addWidget(btn, i / 3, i % 3)
        
        btn_del = strButton(self, '', btnWidth, btnHeight, config.style_numK_btndel)
        btn_del.setGeometry(btn_close.x(), layout.y() + space + 3, btnWidth, btnHeight)
        self.btn_ok = strButton(self, self.tr('Enter'), btnWidth, 3 * btnHeight + space - 3, config.style_numK_btnok)
        self.btn_ok.setGeometry(btn_close.x(), btn_del.y() + btnHeight + space, btnWidth, 3 * btnHeight + space - 3)
        btn = strButton(self, '0', btnWidth, btnHeight, btnStyle)
        btn.setGeometry(line_x + space + 3, layout.y() + layout.height() - 6, btnWidth, btnHeight)
        btn_spot = strButton(self, '.', btnWidth, btnHeight, btnStyle)
        btn_spot.setGeometry(line_x + btnWidth + 3 * space, btn.y(), btnWidth, btnHeight)
        self.connect(btn_spot, QtCore.SIGNAL('mousePress(QString)'), self.mousePress)
        btn_clear = strButton(self, self.tr('Clear'), btnWidth, btnHeight, config.style_numK_btnclear)
        btn_clear.setGeometry(btn_spot.x() + btn_spot.width() + space + 8, btn.y(), btnWidth, btnHeight)
        QtCore.QObject.connect(btn_clear, QtCore.SIGNAL('clicked()'), self.lineedit.clear)
        QtCore.QObject.connect(self.btn_ok, QtCore.SIGNAL('clicked()'), self.kb_ok_click)
        self.connect(btn, QtCore.SIGNAL('mousePress(QString)'), self.mousePress)
        self.connect(self.lineedit, QtCore.SIGNAL('clear'), self.clear)
        self.connect(btn_del, QtCore.SIGNAL('clicked()'), self.lineedit.backspace)
        self.connect(btn_close, QtCore.SIGNAL('clicked()'), self.close)

    
    def clear(self):
        self.data = ''
        self.lineedit.clear()

    
    def show(self, data = { }):
        if self.isVisible():
            return None
        
        self.data = ''
        if data:
            if data['type'] == 'password':
                self.lineedit.setEchoMode(QtGui.QLineEdit.Password)
            
        
        self.showNormal()
        for i in range(config.bg_kb_height):
            self.setGeometry(self.x, self.y + config.bg_kb_height - i, config.bg_kb_width, i)
            time.sleep(1e-06)
        

    
    def closeEvent(self, event):
        for i in range(config.bg_kb_height):
            self.setGeometry(self.x, self.y + i, config.bg_kb_width, config.bg_kb_height - i)
        
        data = { }
        data['wid'] = self.wid
        data['cid'] = self.wid + '_ctr_num_keyboard'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info'][data['cid']] = { }
        data['param_info'][data['cid']]['type'] = 'close'
        self._socketQuery.send(data)
        self.lineedit.clear()
        self.close()

    
    def kb_ok_click(self):
        self.data = self.lineedit.text()
        if self.lineedit.text():
            data = { }
            data['wid'] = self.wid
            data['cid'] = self.wid + '_ctr_num_keyboard'
            data['type'] = 'EVENT'
            data['EVENT'] = 'EVENT_MOUSE_CLICK'
            data['param_info'] = { }
            data['param_info'][data['cid']] = { }
            data['param_info'][data['cid']]['type'] = 'ok'
            data['param_info'][data['cid']]['val'] = str(self.lineedit.text())
            self._socketQuery.send(data)
            self.lineedit.clear()
            self.close()
        

    
    def mousePress(self, text):
        self.lineedit.insert(str(text))
        self.data = self.data + str(text)
        data = { }
        data['wid'] = self.wid
        data['cid'] = self.wid + '_ctr_num_keyboard'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info'][data['cid']] = { }
        data['param_info'][data['cid']]['type'] = 'click'
        data['param_info'][data['cid']]['val'] = ''
        self._socketQuery.send(data)



class numKeyboard_old(QtGui.QWidget):
    
    def __init__(self, wid, parent = None, width = config.bg_kb_width, height = config.bg_kb_height, count = 4, flag = 0):
        QtGui.QWidget.__init__(self, parent)
        self.setAutoFillBackground(True)
        self.setGeometry((768 - width) / 2, (1024 - height) / 2, width, height)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_kb_num)))
        self.setPalette(palette)
        self.wid = wid
        self.sq = socketQuery()
        if flag:
            self.keyValue = [
                [
                    '1',
                    '2',
                    '3'],
                [
                    '4',
                    '5',
                    '6',
                    '0'],
                [
                    '7',
                    '8',
                    '9',
                    '.']]
        else:
            self.keyValue = [
                [
                    '1',
                    '2',
                    '3'],
                [
                    '4',
                    '5',
                    '6',
                    '0'],
                [
                    '7',
                    '8',
                    '9']]
        btnStyle = 'color: white; font: bold 28px; border-style: outset; background-image: url(' + config.pic_btn_kb + ')'
        btnWidth = config.btn_kb_width
        btnHeight = config.btn_kb_height
        self.layout = QtGui.QWidget(self)
        self.layout.setGeometry(QtCore.QRect(10, 10, width - 20, height - 20))
        self.vlayout = QtGui.QVBoxLayout(self.layout)
        self.hlayout = QtGui.QHBoxLayout()
        self.lineedit = QtGui.QLineEdit()
        self.lineedit.setMinimumSize(QtCore.QSize(btnWidth * 3, btnHeight - 4))
        self.lineedit.setMaximumSize(QtCore.QSize(btnWidth * 3, btnHeight - 4))
        self.lineedit.setStyleSheet('color: white; font: bold 22px; border: 2px solid white; background-color: #015353')
        self.hlayout.addWidget(self.lineedit)
        self.btn_ok = QtGui.QPushButton('OK')
        self.btn_ok.setMinimumSize(btnWidth, btnHeight - 5)
        self.btn_ok.setStyleSheet('color: white; font: bold italic 24px; border: 2px solid white; border-radius: 8px; background-color: #006633')
        self.hlayout.addWidget(self.btn_ok)
        self.vlayout.addLayout(self.hlayout, 0)
        self.hlayout = QtGui.QHBoxLayout()
        for i in range(count - 1):
            btn = strButton(self, self.keyValue[0][i], btnWidth, btnHeight, btnStyle)
            self.connect(btn, QtCore.SIGNAL('mousePress(QString)'), self.mousePress)
            self.hlayout.addWidget(btn)
        
        self.btn_del = QtGui.QPushButton(self.tr('Del'))
        self.btn_del.setMinimumSize(btnWidth, btnHeight)
        self.btn_del.setMaximumSize(btnWidth, btnHeight)
        self.btn_del.setStyleSheet(btnStyle)
        self.connect(self.btn_del, QtCore.SIGNAL('clicked()'), self.lineedit.backspace)
        self.hlayout.addWidget(self.btn_del)
        self.vlayout.addLayout(self.hlayout, 1)
        self.hlayout = QtGui.QHBoxLayout()
        for i in range(count):
            btn = strButton(self, self.keyValue[1][i], btnWidth, btnHeight, btnStyle)
            self.connect(btn, QtCore.SIGNAL('mousePress(QString)'), self.mousePress)
            self.hlayout.addWidget(btn)
        
        self.vlayout.addLayout(self.hlayout, 2)
        self.hlayout = QtGui.QHBoxLayout()
        for i in range(count - 1):
            btn = strButton(self, self.keyValue[2][i], btnWidth, btnHeight, btnStyle)
            self.connect(btn, QtCore.SIGNAL('mousePress(QString)'), self.mousePress)
            self.hlayout.addWidget(btn)
        
        if flag:
            btn = strButton(self, self.keyValue[2][i + 1], btnWidth, btnHeight, btnStyle)
            self.connect(btn, QtCore.SIGNAL('mousePress(QString)'), self.mousePress)
            self.hlayout.addWidget(btn)
        else:
            self.btn_close = QtGui.QPushButton('Close')
            self.btn_close.setMinimumSize(btnWidth, btnHeight - 5)
            self.btn_close.setMaximumSize(btnWidth, btnHeight - 5)
            self.btn_close.setStyleSheet('color: white; font: bold italic 24px; border: 2px solid white; border-radius: 8px; background-color: #006633')
            self.connect(self.btn_close, QtCore.SIGNAL('clicked()'), self.close)
            self.hlayout.addWidget(self.btn_close)
            QtCore.QObject.connect(self.btn_ok, QtCore.SIGNAL('clicked()'), self.kb_ok_click)
        self.vlayout.addLayout(self.hlayout, 3)

    
    def show(self, data = { }):
        self.lineedit.clear()
        if data:
            if data['type'] == 'password':
                self.lineedit.setEchoMode(QtGui.QLineEdit.Password)
            
        
        self.showNormal()

    
    def kb_ok_click(self):
        if self.lineedit.text():
            data = { }
            data['wid'] = self.wid
            data['cid'] = self.wid + '_ctr_num_keyboard'
            data['type'] = 'EVENT'
            data['EVENT'] = 'EVENT_MOUSE_CLICK'
            data['param_info'] = { }
            data['param_info'][data['cid']] = { }
            data['param_info'][data['cid']]['type'] = 'ok'
            data['param_info'][data['cid']]['val'] = str(self.lineedit.text())
            self.sq.send(data)
        

    
    def mousePress(self, text):
        self.lineedit.insert(str(text))



class allKeyboard(QtGui.QWidget):
    
    def __init__(self, wid, parent = None, y = 0, width = config.kb_all_width, height = config.kb_all_height, count = 10):
        QtGui.QWidget.__init__(self, parent)
        self.wid = wid
        self.y = y
        self.sq = socketQuery()
        self.keyValue = [
            [
                '1',
                '2',
                '3',
                '4',
                '5',
                '6',
                '7',
                '8',
                '9',
                '0'],
            [
                'q',
                'w',
                'e',
                'r',
                't',
                'y',
                'u',
                'i',
                'o',
                'p'],
            [
                'a',
                's',
                'd',
                'f',
                'g',
                'h',
                'j',
                'k',
                'l'],
            [
                'z',
                'x',
                'c',
                'v',
                'b',
                'n',
                'm'],
            [
                '@',
                '-',
                '_',
                '.',
                ',',
                '<',
                '>',
                '?',
                '"',
                ':']]
        self.symbolValue = [
            '$',
            '+',
            '%',
            '*',
            '(',
            ')',
            '#',
            '!',
            "'",
            ';']
        btnStyle = config.style_allK_btn
        btnWidth = config.btn_kb_all_width
        btnHeight = config.btn_kb_all_height
        self.setAutoFillBackground(True)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.X11BypassWindowManagerHint)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_kb)))
        self.setPalette(palette)
        self.layout = QtGui.QWidget(self)
        self.layout.setGeometry(QtCore.QRect(18, 11, width - 40, height - 30))
        self.vlayout = QtGui.QVBoxLayout(self.layout)
        self.vlayout.setSpacing(1)
        self.hlayout = QtGui.QHBoxLayout()
        self.hlayout.setSpacing(4)
        self.lineedit = QtGui.QLineEdit()
        self.lineedit.setFixedSize(QtCore.QSize(config.btn_kb_all_width * 8, config.btn_kb_all_height - 12))
        self.lineedit.setStyleSheet(config.style_allK_line)
        self.hlayout.addWidget(self.lineedit)
        self.style_ok = config.style_allK_ok
        self.btn_clear = strButton(self, 'OK', 124, 54, self.style_ok)
        self.hlayout.addWidget(self.btn_clear)
        self.vlayout.addLayout(self.hlayout, 0)
        for j in range(2):
            self.hlayout = QtGui.QHBoxLayout()
            for i in range(count):
                btn = strButton(self, self.keyValue[j][i], btnWidth, btnHeight, btnStyle)
                self.connect(btn, QtCore.SIGNAL('mousePress(QString)'), self.mousePress)
                self.hlayout.addWidget(btn)
            
            self.vlayout.addLayout(self.hlayout, j + 1)
        
        self.hlayout = QtGui.QHBoxLayout()
        for i in range(count - 1):
            btn = strButton(self, self.keyValue[2][i], btnWidth, btnHeight, btnStyle)
            self.connect(btn, QtCore.SIGNAL('mousePress(QString)'), self.mousePress)
            self.hlayout.addWidget(btn)
        
        self.style_del = 'border-style: outset; background-image: url(' + config.pic_btn_del + ')'
        self.btn_del = strButton(self, '', config.btn_kb_all_width, config.btn_kb_all_height, self.style_del)
        self.hlayout.addWidget(self.btn_del)
        self.vlayout.addLayout(self.hlayout, 3)
        self.hlayout = QtGui.QHBoxLayout()
        for i in range(count - 3):
            btn = strButton(self, self.keyValue[3][i], btnWidth, btnHeight, btnStyle)
            self.connect(btn, QtCore.SIGNAL('mousePress(QString)'), self.mousePress)
            self.hlayout.addWidget(btn)
        
        self.style_enter = config.style_allK_enter
        self.btn_ok = strButton(self, QtGui.QApplication.translate('Form', self.tr('Enter'), None, QtGui.QApplication.UnicodeUTF8), 192, config.btn_kb_all_height, self.style_enter)
        self.hlayout.addWidget(self.btn_ok)
        self.vlayout.addLayout(self.hlayout, 4)
        self.hlayout = QtGui.QHBoxLayout()
        for i in range(count):
            btn = strButton(self, self.keyValue[4][i], btnWidth, btnHeight, btnStyle)
            self.connect(btn, QtCore.SIGNAL('mousePress(QString)'), self.mousePress)
            self.hlayout.addWidget(btn)
        
        self.vlayout.addLayout(self.hlayout, 5)
        self.hlayout = QtGui.QHBoxLayout()
        self.style_shift = config.style_allK_shift
        self.btn_shift = strButton(self, QtGui.QApplication.translate('Form', self.tr('Shift'), None, QtGui.QApplication.UnicodeUTF8), 192, config.btn_kb_all_height, self.style_shift)
        self.hlayout.addWidget(self.btn_shift)
        self.style_space = config.style_allK_space
        self.btn_space = strButton(self, QtGui.QApplication.translate('Form', self.tr('Space'), None, QtGui.QApplication.UnicodeUTF8), 329, config.btn_kb_all_height, self.style_space)
        self.hlayout.addWidget(self.btn_space)
        self.style_close = config.style_allK_close
        self.btn_close = strButton(self, QtGui.QApplication.translate('Form', self.tr('Close'), None, QtGui.QApplication.UnicodeUTF8), 124, 54, self.style_close)
        self.hlayout.addWidget(self.btn_close)
        self.vlayout.addLayout(self.hlayout, 6)
        self.shift = 0
        self.connect(self.btn_clear, QtCore.SIGNAL('clicked()'), self.btn_ok.click)
        self.connect(self.btn_del, QtCore.SIGNAL('clicked()'), self.lineedit.backspace)
        self.connect(self.btn_ok, QtCore.SIGNAL('clicked()'), self.kb_ok_click)
        self.connect(self.btn_shift, QtCore.SIGNAL('clicked()'), self.btn_shift_click)
        self.connect(self.btn_close, QtCore.SIGNAL('clicked()'), self.close_click)
        self.connect(self.btn_space, QtCore.SIGNAL('clicked()'), self.btn_space_click)
        self.verify = 0
        self.hide()

    
    def kb_ok_click(self):
        if self.lineedit.text():
            text = str(self.lineedit.text())
            if self.verify:
                if self.verifyEmail(text):
                    self.verify = 0
                    self.sendOk(text)
                else:
                    self.lineedit.setText(QtGui.QApplication.translate('Form', 'Please input valid email address!', None, QtGui.QApplication.UnicodeUTF8))
                    self.lineedit.selectAll()
            else:
                self.sendOk(text)
        

    
    def verifyEmail(self, text):
        if len(text) < 40 and text.find('@') != -1 and text.count('@') == 1:
            head = text.split('@')[0]
            tail = text.split('@')[1]
            if tail.replace('.', '').replace('-', '').isalnum() and head.replace('.', '').replace('-', '').replace('_', '').replace('!', '').replace('$', '').replace('&', '').replace('*', '').replace('+', '').replace('=', '').replace('{', '').replace('|', '').replace('}', '').replace('~', '').isalnum():
                return True
            
        
        return False

    
    def sendOk(self, text):
        data = { }
        data['wid'] = self.wid
        data['cid'] = self.wid + '_ctr_all_keyboard'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info'][data['cid']] = { }
        data['param_info'][data['cid']]['type'] = 'ok'
        data['param_info'][data['cid']]['val'] = str(text)
        self.sq.send(data)
        self.lineedit.clear()
        self.close()

    
    def close_click(self):
        data = { }
        data['wid'] = self.wid
        data['cid'] = self.wid + '_ctr_all_keyboard'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info'][data['cid']] = { }
        data['param_info'][data['cid']]['type'] = 'close'
        data['param_info'][data['cid']]['val'] = ''
        self.sq.send(data)
        self.lineedit.clear()
        self.close()

    
    def setType(self, data):
        if data:
            
            try:
                type = data['type']
            except Exception:
                ex = None
                print('[setType] Error: type can NOT be NULL! %s' % ex)

            if type == 'password':
                self.lineedit.setEchoMode(QtGui.QLineEdit.Password)
            else:
                self.lineedit.setEchoMode(QtGui.QLineEdit.Normal)
        

    
    def mousePress(self, text):
        self.lineedit.insert(str(text))
        data = { }
        data['wid'] = self.wid
        data['cid'] = self.wid + '_ctr_all_keyboard'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info'][data['cid']] = { }
        data['param_info'][data['cid']]['type'] = 'click'
        data['param_info'][data['cid']]['val'] = str(text)
        self.sq.send(data)

    
    def btn_space_click(self):
        self.lineedit.insert(' ')

    
    def btn_shift_click(self):
        self.shift = not (self.shift)
        for line in range(2):
            hl = self.vlayout.itemAt(2 + line).layout()
            for i in range(10 - line):
                btn = hl.itemAt(i).widget()
                text = btn.text()
                text = str(text).swapcase()
                btn.setText(text)
            
        
        hl = self.vlayout.itemAt(2 + line + 1).layout()
        for i in range(7):
            btn = hl.itemAt(i).widget()
            text = btn.text()
            text = str(text).swapcase()
            btn.setText(text)
        
        hl = self.vlayout.itemAt(4 + line).layout()
        for i in range(10):
            btn = hl.itemAt(i).widget()
            if self.shift:
                btn.setText(self.symbolValue[i])
            else:
                btn.setText(self.keyValue[4][i])
        

    
    def show(self, param = { }):
        self.lineedit.clear()
        if self.isVisible():
            return None
        
        if param and 'type' in param and param['type']:
            type = param['type']
            if type == 'password':
                self.lineedit.setEchoMode(QtGui.QLineEdit.Password)
                self.verify = 0
            elif type == 'email':
                self.lineedit.setText(QtGui.QApplication.translate('Form', 'Please enter your email address to receive receipt.', None, QtGui.QApplication.UnicodeUTF8))
                self.lineedit.selectAll()
                self.lineedit.setEchoMode(QtGui.QLineEdit.Normal)
                self.verify = 1
            else:
                self.lineedit.setEchoMode(QtGui.QLineEdit.Normal)
                self.verify = 0
        else:
            self.lineedit.setEchoMode(QtGui.QLineEdit.Normal)
            self.verify = 0
        self.showNormal()
        r = config.kb_all_height / 4
        if not (self.y):
            for i in range(r):
                self.setGeometry(19 + r - i, 894 - 3 * r - i, (config.kb_all_width - config.kb_all_height) + 4 * i, 4 * i)
            
        else:
            for i in range(r):
                self.setGeometry(19 + r - i, 1024 - 3 * r - i, (config.kb_all_width - config.kb_all_height) + 4 * i, 4 * i)
            

    '\n    def showEvent(self, event):\n        self.lineedit.clear()\n        r = config.kb_all_height/4\n        if not self.y:\n            ## Animated effect show from bottom\n            #for i in range(config.kb_all_height):\n            #   self.setGeometry(19, 894-i, config.kb_all_width, i)\n            ## Animated effect show from center\n            #for i in range(config.kb_all_height/2):\n            #   self.setGeometry(19+config.kb_all_height/2-i, 894-config.kb_all_height/2-i, config.kb_all_width-config.kb_all_height+2*i, 2*i)\n            for i in range(r):\n                self.setGeometry(19+r-i, 894-(3*r)-i, config.kb_all_width-config.kb_all_height+4*i, 4*i)\n        else: ## Specified position\n            #for i in range(config.kb_all_height):\n            #   self.setGeometry(19, self.y+config.kb_all_height-i, config.kb_all_width, i)\n            #for i in range(config.kb_all_height/2):\n            #   self.setGeometry(19+config.kb_all_height/2-i, 1024-config.kb_all_height/2-i, config.kb_all_width-config.kb_all_height+2*i, 2*i)\n            for i in range(r):\n                self.setGeometry(19+r-i, 1024-(3*r)-i, config.kb_all_width-config.kb_all_height+4*i, 4*i)\n    '
    
    def closeEvent(self, event):
        r = config.kb_all_height / 4
        if not (self.y):
            for i in range(r):
                self.setGeometry(19, (894 - config.kb_all_height) + 4 * i, config.kb_all_width, config.kb_all_height - 4 * i)
            
        else:
            for i in range(r):
                self.setGeometry(19, self.y + 4 * i, config.kb_all_width, config.kb_all_height - 4 * i)
            



class discInfo(QtGui.QWidget):
    
    def __init__(self, parent = None, width = config.unload_list_width, height = 480, lines = 6):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedSize(width, height)
        self.lines = lines
        self.label_header = QtGui.QLabel(self)
        self.label_header.setStyleSheet(config.table_title_style)
        self.label_header.setText(QtGui.QApplication.translate('Form', '  DVD information', None, QtGui.QApplication.UnicodeUTF8))
        self.label_header.setGeometry(0, 0, width, 60)
        self.verticalLayout = QtGui.QWidget(self)
        self.verticalLayout.setGeometry(QtCore.QRect(0, 60, width, 70 * 6))
        self.verticalLayout.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_cart_info_bg)))
        self.verticalLayout.setPalette(palette)
        self.vboxlayout = QtGui.QVBoxLayout(self.verticalLayout)
        self.vboxlayout.setSpacing(15)
        self.label_0 = QtGui.QLabel(QtGui.QApplication.translate('Form', 'Slot ID:', None, QtGui.QApplication.UnicodeUTF8))
        self.label_1 = QtGui.QLabel(QtGui.QApplication.translate('Form', 'Price plan:', None, QtGui.QApplication.UnicodeUTF8))
        self.label_2 = QtGui.QLabel(QtGui.QApplication.translate('Form', 'Sale price:', None, QtGui.QApplication.UnicodeUTF8))
        self.label_3 = QtGui.QLabel(QtGui.QApplication.translate('Form', 'Sale convert price:', None, QtGui.QApplication.UnicodeUTF8))
        self.label_4 = QtGui.QLabel(QtGui.QApplication.translate('Form', 'Your cost:', None, QtGui.QApplication.UnicodeUTF8))
        self.label_5 = QtGui.QLabel(QtGui.QApplication.translate('Form', 'UPC:', None, QtGui.QApplication.UnicodeUTF8))
        for i in range(lines):
            exec('self.label_' + str(i) + ".setStyleSheet('color: #0060b4; font: bold 20px')")
            exec('self.label_' + str(i) + '.setFixedSize(180, 75)')
            exec('self.hboxlayout' + str(i) + ' = QtGui.QHBoxLayout()')
            exec('self.hboxlayout' + str(i) + '.addWidget(self.label_' + str(i) + ')')
            exec('self.vboxlayout.addLayout(self.hboxlayout' + str(i) + ')')
            exec('self.btn_' + str(i) + ' = btnEdit(self.verticalLayout)')
        
        self.btn_f = QtGui.QPushButton(self.verticalLayout)
        self.btn_f.setMaximumWidth(65)
        self.btn_f.setStyleSheet('background-color: transparent; border-style: outset; font: bold 20px; color:#bb0000')
        self.hboxlayout0.addWidget(self.btn_f)
        self.btn_b = QtGui.QPushButton(self.verticalLayout)
        self.btn_b.setStyleSheet('background-color: transparent; border-style: outset; font: bold 20px; color:#bb0000')
        self.hboxlayout0.addWidget(self.btn_b)

    
    def setList(self, data):
        for i in range(self.lines):
            exec('self.hboxlayout' + str(i) + '.addWidget(self.btn_' + str(i) + ')')
        
        if not data:
            print('[setList] Error: data can not be NULL!')
            return -1
        
        self.btn_f.setText(data['front_slot_id'])
        self.btn_b.setText(data['back_slot_id'])
        if data['front_slot_id'] == data['check_slot_id']:
            self.btn_f.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_available_yes)))
            self.btn_b.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_unselect)))
            self.checkedID = 0
        else:
            self.btn_b.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_available_yes)))
            self.btn_f.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_unselect)))
            self.checkedID = 1



class btnEdit(QtGui.QPushButton):
    
    def __init__(self, parent, text = ''):
        QtGui.QPushButton.__init__(self, parent)
        if text:
            self.setText(QtGui.QApplication.translate('Form', text, None, QtGui.QApplication.UnicodeUTF8))
        else:
            self.setText(QtGui.QApplication.translate('Form', 'Edit', None, QtGui.QApplication.UnicodeUTF8))
        self.setFixedSize(QtCore.QSize(124, 60))
        self.btnStyle = config.style_btnEdit
        self.pressStyle = 'background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 white, stop:0.6 #3077e0, stop:1 #f0f0f0); font: bold 30px; color: white; border-radius: 7px;'
        self.setStyleSheet(self.btnStyle)
        QtCore.QObject.connect(self, QtCore.SIGNAL('pressed()'), self.press)
        QtCore.QObject.connect(self, QtCore.SIGNAL('released()'), self.release)

    
    def press(self):
        self.setStyleSheet(self.pressStyle)

    
    def release(self):
        self.setStyleSheet(self.btnStyle)



class PricePlan(QtGui.QWidget):
    
    def __init__(self, parent = None, rheith = 75, row = 5):
        QtGui.QWidget.__init__(self, parent)
        self.setStyleSheet('color: #0060b4; font: bold 20px; background-color: transparent;')
        self.rowHeight = rheith
        self.special = ''
        self.pre = 0
        self.defaultPlanId = '1'
        header = QtGui.QWidget(self)
        header.setGeometry(0, 0, config.unload_list_width, 60)
        header.setStyleSheet(config.table_title_style)
        hboxlayout = QtGui.QHBoxLayout(header)
        self.label_header = QtGui.QLabel(QtGui.QApplication.translate('Form', ' Price Plan List ', None, QtGui.QApplication.UnicodeUTF8), header)
        self.label_header.setStyleSheet('background: transparent;')
        hboxlayout.addWidget(self.label_header)
        self.btn_special_price = QtGui.QPushButton(QtGui.QApplication.translate('Form', 'Accept special price plan', None, QtGui.QApplication.UnicodeUTF8), self)
        self.btn_special_price.setStyleSheet('border-style: outset; background: transparent; font: bold 18px; color: white;')
        self.btn_special_price.setIconSize(QtCore.QSize(40, 42))
        self.btn_special_price.setIcon(QtGui.QIcon(QtGui.QPixmap(config.pic_available_yes_white)))
        hboxlayout.addWidget(self.btn_special_price)
        self.table = QtGui.QTableWidget(self)
        self.table.setGeometry(0, 60, config.unload_list_width, self.rowHeight * row)
        self.table.setStyleSheet(config.table_bg_style)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table.setIconSize(QtCore.QSize(75, rheith - 5))
        self.table.verticalHeader().setEnabled(False)
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().hide()
        self.table.setColumnCount(3)
        self.table.setColumnWidth(0, 120)
        self.table.setColumnWidth(1, config.unload_list_width - 200 - 10)
        self.table.setColumnWidth(2, 80)
        self.pFont = QtGui.QFont()
        self.pFont.setPointSize(12)
        self.pFont.setBold(True)
        QtCore.QObject.connect(self.btn_special_price, QtCore.SIGNAL('clicked()'), self.btn_special_price_click)
        QtCore.QObject.connect(self.table, QtCore.SIGNAL('currentCellChanged(int, int, int, int)'), self.selectedChange)

    
    def selectedChange(self, row, col, preRow, preCol):
        if row != preRow:
            if self.table.item(preRow, 2):
                self.table.item(preRow, 2).setIcon(QtGui.QIcon(config.pic_unchecked))
            
            if self.table.item(row, 2):
                self.table.item(row, 2).setIcon(QtGui.QIcon(config.pic_checked))
            
        

    
    def btn_special_price_click(self):
        if self.special != 'yes':
            self.btn_special_price.setIcon(QtGui.QIcon(config.pic_available_yes_white))
            self.special = 'yes'
        else:
            self.btn_special_price.setIcon(QtGui.QIcon(config.pic_unselect_white))
            self.special = 'no'

    
    def setPlanList(self, data):
        if not data:
            print('GUI DEBUG: [setPlanList] No data, list will be cleared.')
            return None
        
        self.table.clear()
        data = data['ctr_plan_list']
        if not data:
            self.table.setRowCount(0)
            return None
        
        length = len(data)
        self.table.setRowCount(length)
        for i in range(length):
            id = 'Plan ' + data[i]['id']
            text = data[i]['data_text']
            text = repr(text)
            self.table.setRowHeight(i, self.rowHeight)
            item = QtGui.QTableWidgetItem(id)
            self.table.setItem(i, 0, item)
            item = QtGui.QTableWidgetItem()
            exec('item.setText(' + text + ')')
            item.setFont(self.pFont)
            self.table.setItem(i, 1, item)
            item = QtGui.QTableWidgetItem()
            if data[i]['id'] != self.defaultPlanId:
                item.setIcon(QtGui.QIcon(config.pic_unchecked))
            else:
                item.setIcon(QtGui.QIcon(config.pic_checked))
                self.table.setCurrentCell(i, 2)
            self.table.setItem(i, 2, item)
        

    
    def setSpecial(self, special):
        self.special = special
        if special == 'yes':
            self.btn_special_price.setIcon(QtGui.QIcon(config.pic_available_yes_white))
        else:
            self.btn_special_price.setIcon(QtGui.QIcon(config.pic_unselect_white))



class MovieCouponSelectForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_kb_num)))
        self.setPalette(palette)
        self.sq = socketQuery()
        self.ctr_movie_info = ListWidget_2(self)
        self.ctr_movie_info.setGeometry(10, 20, config.bg_kb_width - 20, config.bg_kb_height - 20)
        btn_close = QtGui.QPushButton(self)
        btn_close.setIcon(QtGui.QIcon(config.pic_icon_close))
        btn_close.setIconSize(QtCore.QSize(30, 30))
        btn_close.setGeometry(config.bg_kb_width - 35, 5, 30, 30)
        QtCore.QObject.connect(self.ctr_movie_info, QtCore.SIGNAL('itemClicked(QListWidgetItem*)'), self.movie_click)
        QtCore.QObject.connect(btn_close, QtCore.SIGNAL('clicked()'), self.close)

    
    def setMovieInfo(self, data):
        self.ctr_movie_info.setMovieInfo(data)

    
    def movie_click(self, item):
        rfid = item.data(self.ctr_movie_info.dataType).toString()
        print(rfid)
        data = { }
        data['wid'] = 'CouponForm'
        data['cid'] = 'ctr_movie_info'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info']['ctr_movie_info'] = { }
        data['param_info']['ctr_movie_info']['rfid'] = str(rfid)
        self.sq.send(data)
        self.close()



class ConfigForm(QtGui.QWidget):
    
    def __init__(self, wid, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_configForm()
        self.ui.setupUi(self)
        self.setupButtons(wid)

    
    def reset(self):
        self.btn_cancel.reset()
        self.btn_test_mode_off.setText(QtGui.QApplication.translate('configForm', 'Test Mode\nOff', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_test_mode_on.setText(QtGui.QApplication.translate('configForm', 'Test Mode\nOn', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_speaker_volume.setText(QtGui.QApplication.translate('configForm', 'Speaker\nVolume', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_operator_code.setText(QtGui.QApplication.translate('configForm', 'Operator\nCode', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_poweroff.setText(QtGui.QApplication.translate('configForm', 'Power Off', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_network_diagnosis.setText(QtGui.QApplication.translate('configForm', 'Network\nDiagnosis', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_hdmi_on.setText(QtGui.QApplication.translate('configForm', 'HDMI\nConnected', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_hdmi_off.setText(QtGui.QApplication.translate('configForm', 'HDMI\nDisconnected', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_hdmi_on_disabled.setText(QtGui.QApplication.translate('configForm', 'HDMI\nConnected', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_hdmi_off_disabled.setText(QtGui.QApplication.translate('configForm', 'HDMI\nDisconnected', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_test_mode_on_disabled.setText(QtGui.QApplication.translate('configForm', 'Test Mode\nOn', None, QtGui.QApplication.UnicodeUTF8))
        self.btn_test_mode_off_disabled.setText(QtGui.QApplication.translate('configForm', 'Test Mode\nOff', None, QtGui.QApplication.UnicodeUTF8))

    
    def setupButtons(self, wid):
        self.btn_cancel = btnCancel(self, wid)
        self.btn_cancel.setGeometry(580, 20, 160, 68)
        self.btn_test_mode_off = ctrButton(self, wid, 'btn_test_mode_off', QtGui.QApplication.translate('configForm', 'Test Mode\nOff', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnRedStyle)
        self.btn_test_mode_on = ctrButton(self, wid, 'btn_test_mode_on', QtGui.QApplication.translate('configForm', 'Test Mode\nOn', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.btn_test_mode_on.hide()
        self.btn_speaker_volume = ctrButton(self, wid, 'btn_speaker_volume', QtGui.QApplication.translate('configForm', 'Speaker\nVolume', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.btn_operator_code = ctrButton(self, wid, 'btn_operator_code', QtGui.QApplication.translate('configForm', 'Operator\nCode', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.btn_poweroff = ctrButton(self, wid, 'btn_poweroff', QtGui.QApplication.translate('configForm', 'Power Off', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnRedStyle)
        self.btn_network_diagnosis = ctrButton(self, wid, 'btn_network_diagnosis', QtGui.QApplication.translate('configForm', 'Network\nDiagnosis', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.btn_hdmi_on = ctrButton(self, wid, 'btn_hdmi_on', QtGui.QApplication.translate('configForm', 'HDMI\nConnected', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnHdmiOnStyle)
        self.btn_hdmi_off = ctrButton(self, wid, 'btn_hdmi_off', QtGui.QApplication.translate('configForm', 'HDMI\nDisconnected', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnHdmiOffStyle)
        self.btn_hdmi_off.hide()
        self.btn_hdmi_on_disabled = ctrButton(self, wid, 'btn_hdmi_on_disabled', QtGui.QApplication.translate('configForm', 'HDMI\nConnected', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, 'color: white; font: bold italic 22px; border-style: outset; background-image: url(' + config.pic_btn_config_gray + ')')
        self.btn_hdmi_off_disabled = ctrButton(self, wid, 'btn_hdmi_off_disabled', QtGui.QApplication.translate('configForm', 'HDMI\nDisconnected', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, 'color: white; font: bold italic 22px; border-style: outset; background-image: url(' + config.pic_btn_config_gray + ')')
        self.btn_test_mode_on_disabled = ctrButton(self, wid, 'btn_test_mode_on_disabled', QtGui.QApplication.translate('configForm', 'Test Mode\nOn', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, 'color: white; font: bold italic 22px; border-style: outset; background-image: url(' + config.pic_btn_config_gray + ')')
        self.btn_test_mode_off_disabled = ctrButton(self, wid, 'btn_test_mode_off_disabled', QtGui.QApplication.translate('configForm', 'Test Mode\nOff', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, 'color: white; font: bold italic 22px; border-style: outset; background-image: url(' + config.pic_btn_config_gray + ')')
        self.btn_smart_load = ctrButton(self, wid, 'btn_smart_load', QtGui.QApplication.translate('configForm', 'Smart\nLoad', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnBlueStyle)
        self.btn_smart_load.hide()
        self.btn_test_mode_on_disabled.hide()
        self.btn_test_mode_off_disabled.hide()
        self.btn_hdmi_on_disabled.hide()
        self.btn_hdmi_off_disabled.hide()
        self.ui.gridLayout.setGeometry(QtCore.QRect(config.layout_x, config.layout_y, config.layout_width, config.layout_height))
        self.ui.gridlayout.addWidget(self.btn_test_mode_off, 0, 0)
        self.ui.gridlayout.addWidget(self.btn_test_mode_on, 0, 0)
        self.ui.gridlayout.addWidget(self.btn_speaker_volume, 0, 1)
        self.ui.gridlayout.addWidget(self.btn_operator_code, 0, 2)
        self.ui.gridlayout.addWidget(self.btn_poweroff, 1, 0)
        self.ui.gridlayout.addWidget(self.btn_network_diagnosis, 1, 1)
        self.ui.gridlayout.addWidget(self.btn_hdmi_on, 1, 2)
        self.ui.gridlayout.addWidget(self.btn_hdmi_off, 1, 2)
        self.ui.gridlayout.addWidget(self.btn_test_mode_on_disabled, 0, 0)
        self.ui.gridlayout.addWidget(self.btn_test_mode_off_disabled, 0, 0)
        self.ui.gridlayout.addWidget(self.btn_hdmi_on_disabled, 1, 2)
        self.ui.gridlayout.addWidget(self.btn_hdmi_off_disabled, 1, 2)



class Slider(QtGui.QWidget):
    
    def __init__(self, wid, cid, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.slider = QtGui.QSlider(self)
        self.slider.setGeometry(0, 0, 463, 100)
        self.wid = wid
        self.cid = cid
        self.sq = socketQuery()
        style = 'QSlider::groove:horizontal { height: 90px; background-image: url(' + config.pic_volum_range + '); margin: 2px 0; }     QSlider::handle:horizontal { image: url(' + config.pic_volum_slider + '); width: 45px; margin: -2px 0; border-radius: 3px; }'
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setStyleSheet(style)
        self.slider.setRange(60, 100)
        self.slider.setPageStep(5)
        self.slider.setSingleStep(1)
        self.connect(self.slider, QtCore.SIGNAL('valueChanged(int)'), self.sendValue)

    
    def sendValue(self, value):
        data = { }
        data['wid'] = self.wid
        data['cid'] = self.cid
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info']['btn_volume'] = { }
        data['param_info']['btn_volume']['volume'] = str(value)
        self.sq.send(data)

    
    def setVolume(self, data):
        if not data:
            print('[setVolume] Error: data can not be NULL!')
            return -1
        
        number = int(data['number'])
        if number >= 80 and number <= 100:
            print(number)
            self.slider.setValue(number)
        



class Slider1(QtGui.QSlider):
    
    def __init__(self, wid, cid, parent = None):
        QtGui.QSlider.__init__(self, parent)
        self.wid = wid
        self.cid = cid
        self.sq = socketQuery()
        style = 'QSlider::groove:horizontal { height: 90px; background-image: url(' + config.pic_volum_range + '); margin: 2px 0; }     QSlider::handle:horizontal { image: url(' + config.pic_volum_slider + '); width: 45px; margin: -2px 0; border-radius: 3px; }'
        self.setOrientation(QtCore.Qt.Horizontal)
        self.setStyleSheet(style)
        self.setRange(80, 100)
        self.setPageStep(2)
        self.setSingleStep(1)

    
    def mouseReleaseEvent(self, event):
        self.sendValue(self.value())

    
    def sendValue(self, value):
        data = { }
        data['wid'] = self.wid
        data['cid'] = self.cid
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info']['btn_volume'] = { }
        data['param_info']['btn_volume']['volume'] = str(value)
        self.sq.send(data)

    
    def setVolume(self, data):
        if not data:
            print('[setVolume] Error: data can not be NULL!')
            return -1
        
        number = int(data['number'])
        if number >= 80 and number <= 100:
            print(number)
            self.setValue(number)
        



class Flash(QtGui.QWidget):
    
    def __init__(self, parent, width, height, file1, file2 = ''):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedSize(width, height)
        if file2:
            pic = QtGui.QLabel(self)
            pic.setGeometry(QtCore.QRect(0, 0, width, height))
            pic.setPixmap(QtGui.QPixmap(file2))
        
        label = QtGui.QLabel(self)
        label.setGeometry(0, 0, width, height)
        self.movie = QtGui.QMovie(self)
        self.movie.setFileName(file1)
        label.setMovie(self.movie)

    
    def showEvent(self, event):
        self.movie.start()

    
    def hideEvent(self, event):
        self.movie.stop()



class SWF_insert(Flash):
    
    def __init__(self, parent):
        Flash.__init__(self, parent, 487, 285, config.pic_insert_dvd_gif, config.pic_insert_dvd)



class SWF_insert_h(Flash):
    
    def __init__(self, parent):
        Flash.__init__(self, parent, 487, 520, config.pic_insert_dvd_h_gif)



class SWF_vomit(Flash):
    
    def __init__(self, parent):
        Flash.__init__(self, parent, 487, 285, config.pic_vomit_dvd_gif, config.pic_insert_dvd)



class SWF_sweepcard(Flash):
    
    def __init__(self, parent):
        Flash.__init__(self, parent, 400, 441, config.pic_checkout_gif, config.pic_checkout)



class SWF_swipecard_member(Flash):
    
    def __init__(self, parent):
        Flash.__init__(self, parent, 400, 441, config.pic_checkout_member, config.pic_checkout)



class SWF_swipe_card(Flash):
    
    def __init__(self, parent):
        Flash.__init__(self, parent, 585, 520, config.PICDIR + 'swipe_card.gif')



class SWF_insert_card(Flash):
    
    def __init__(self, parent):
        Flash.__init__(self, parent, 585, 520, config.PICDIR + 'insert_card.gif')



class SWF_robot_take(Flash):
    
    def __init__(self, parent):
        Flash.__init__(self, parent, 585, 522, config.pic_take_dvd_gif)



class SWF_robot_send(Flash):
    
    def __init__(self, parent):
        Flash.__init__(self, parent, 585, 522, config.pic_send_dvd_gif)



class SWF_process(Flash):
    
    def __init__(self, parent):
        Flash.__init__(self, parent, 660, 85, config.pic_btm_bar)



class gifButton(QtGui.QPushButton):
    
    def __init__(self, parent, cid, background, bg_pressed = '', flag = 0, width = 256, height = 208):
        QtGui.QWidget.__init__(self, parent)
        self.cid = cid
        self.sq = socketQuery()
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setFixedSize(width, height)
        self.setStyleSheet('QPushButton {border-style: outset; background-image: url(' + background + '); } QPushButton:pressed { background-image: url(' + bg_pressed + ') }')
        y = 100
        if bg_pressed:
            self.cg = QtGui.QLabel(self)
            self.cg.setGeometry(14, 3, width - 20, y)
            self.cg.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
            self.cg.setWordWrap(True)
            self.cg.setStyleSheet(config.style_main_btn_bg)
            self.fg = QtGui.QLabel(self)
            self.fg.setGeometry(10, 0, width - 20, y)
            self.fg.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
            self.fg.setWordWrap(True)
            self.fg.setStyleSheet(config.style_main_btn)
            self.gg = QtGui.QLabel(self)
            self.gg.setGeometry(13, y + 2, width - 20, height - y)
            self.gg.setAlignment(QtCore.Qt.AlignTop)
            self.gg.setWordWrap(True)
            self.gg.setStyleSheet(config.style_main_gg)
        
        self.bg = QtGui.QLabel(self)
        self.bg.setGeometry(10, y, width - 20, height - y)
        self.bg.setAlignment(QtCore.Qt.AlignTop)
        self.bg.setWordWrap(True)
        self.bg.setStyleSheet(config.style_main_bg)
        self.connect(self, QtCore.SIGNAL('clicked()'), self.sendMsg)
        self.flag = flag
        if flag:
            label = QtGui.QLabel(self.bg)
            label.setGeometry(20, 80, 160, 150)
            self.movie = QtGui.QMovie()
            self.movie.setFileName(config.pic_hand_gif)
            label.setMovie(self.movie)
        

    
    def showEvent(self, event):
        if self.flag:
            self.movie.start()
        

    
    def hideEvent(self, event):
        if self.flag:
            self.movie.stop()
        

    
    def sendMsg(self):
        data = { }
        data['wid'] = 'MainForm'
        data['cid'] = self.cid
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        self.sq.send(data)



class Player(QtCore.QObject):
    
    def __init__(self, wid, gui):
        QtCore.QObject.__init__(self)
        self.gui = gui
        self.opt_list = ()
        self.opt_list = [
            '',
            '-wid',
            str(wid),
            '-quiet',
            '-slave',
            '-loop',
            '0',
            '',
            '']
        self.proc = QtCore.QProcess()
        self.connect(self.proc, QtCore.SIGNAL('readyReadStandardOutput()'), self._clear_mp_buff)
        self.connect(self.proc, QtCore.SIGNAL('finished(int, QProcess::ExitStatus)'), self.finished)
        self.connect(self.proc, QtCore.SIGNAL('error(QProcess::ProcessError)'), self.error_handler)

    
    def go(self, file):
        if self.proc.state() != QtCore.QProcess.NotRunning:
            print('\nmplayer process close\n')
            self.proc.close()
        
        self.opt_list[0] = file
        
        try:
            self.proc.start('mplayer', self.opt_list)
            if self.proc.waitForStarted(1000):
                return True
            else:
                print('[Error] mplayer can not start: %s' % self.opt_list)
                self.proc.terminate()
                return False
        except Exception:
            ex = None
            print('[Player] [Error] when start mplayer %s: %s' % (self.opt_list, ex))


    
    def stop(self):
        self.proc.terminate()

    
    def end(self, argv):
        print(argv)
        if argv == 0:
            print('\nmplayer NotRunning\n')
        elif argv == 1:
            print('\nmplayer Starting\n')
        elif argv == 2:
            print('\nmplayer Running\n')
        

    
    def _clear_mp_buff(self):
        self.proc.readAllStandardOutput()

    
    def finished(self, code, status):
        self.proc.close()
        print('\nmplayer finished.\n')

    
    def error_handler(self, error):
        print('\nmplayer ERROR!!!!!!!!!!!!!!!!!!!! %s\n' % error)

    
    def setVolume(self, vol):
        if not vol:
            self.opt_list[7] = '-ao'
            self.opt_list[8] = 'null'
        else:
            self.opt_list[7] = ''
            self.opt_list[8] = ''


'\nclass SymbolLabel(QtGui.QLabel):\n    def __init__(self, parent=None):\n        QtGui.QLabel.__init__(self, parent=None)\n        self.symbol = ""\n\n    def setSymbol(self, symbol):\n        self.symbol = symbol\n\n    def showSymbol(self):\n        self.setText(self.symbol+self.text())\n\n    def setText(self, text):\n        self.text = text\n        QtGui.QLabel.setText(text)\n\n    def text(self):\n        return self.text\n'

class featureList(QtGui.QTableWidget):
    
    def __init__(self, parent = None):
        QtGui.QTableWidget.__init__(self, parent)
        self.setStyleSheet(config.scroll_style_little + config.tableView_style)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setFrameStyle(QtGui.QFrame.NoFrame)
        self.setLineWidth(0)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.setShowGrid(False)
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        self.setColumnCount(2)
        self.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        self.keyFont = QtGui.QFont()
        self.keyFont.setBold(True)
        self.keyFont.setPointSize(12)
        self.valFont = QtGui.QFont()
        self.valFont.setPointSize(12)
        self.fbrush = QtGui.QBrush(QtGui.QColor(170, 0, 0))

    
    def setList(self, data):
        
        try:
            self.clear()
            self.setRowCount(len(data))
            for d in data:
                i = data.index(d)
                key = list(d.keys())[0]
                value = list(d.values())[0]
                self.setRowHeight(i, 25)
                item = QtGui.QTableWidgetItem(key + ' : ')
                item.setFont(self.keyFont)
                item.setForeground(self.fbrush)
                item.setTextAlignment(QtCore.Qt.AlignTop)
                self.setItem(i, 0, item)
                item_v = QtGui.QTableWidgetItem(value)
                item_v.setFont(self.valFont)
                self.setItem(i, 1, item_v)
            
            self.resizeColumnToContents(0)
            self.resizeRowsToContents()
        except Exception:
            ex = None
            print(ex)




class myForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(0, 0, 768, 1000)
        palette = QtGui.QPalette()
        self.setPalette(palette)

    
    def test_btn(self):
        btn = strButton(self, '@')
        btn.setGeometry(100, 550, 63, 58)
        self.connect(btn, QtCore.SIGNAL('mousePress(QString)'), self.mousePress)

    
    def mousePress(self, text):
        print(text)

    
    def test_allKeyboard(self):
        btn = QtGui.QPushButton('Show', self)
        btn.setGeometry(10, 10, 100, 30)
        kb = allKeyboard('aa', self)
        QtCore.QObject.connect(btn, QtCore.SIGNAL('clicked()'), kb.show)

    
    def test(self):
        movieList = MovieList(self)
        data = {
            'ctr_movie_list': [
                {
                    'movie_pic': 'image/tmp/m0.jpg',
                    'movie_title': 'Chasing The Green (2009)',
                    'upc': '891514001993',
                    'available_count': '1',
                    'movie_big_pic': '132852_big.jpg' },
                {
                    'movie_pic': 'image/tmp/m0.jpg',
                    'movie_title': 'Applause For Miss E (2009)',
                    'upc': '014381532227',
                    'available_count': '1',
                    'movie_big_pic': '132213_big.jpg' },
                {
                    'movie_pic': 'image/tmp/m0.jpg',
                    'movie_title': 'Border Town (2009)',
                    'upc': '824355531725',
                    'available_count': '1',
                    'movie_big_pic': '132752_big.jpg' },
                {
                    'movie_pic': 'image/tmp/m0.jpg',
                    'movie_title': 'De Rodillas (2008)',
                    'upc': '812320010344',
                    'available_count': '1',
                    'movie_big_pic': '133032_big.jpg' },
                {
                    'movie_pic': 'image/tmp/m0.jpg',
                    'movie_title': 'Night Train (2009)',
                    'upc': '774212101403',
                    'available_count': '1',
                    'movie_big_pic': '134468_big.jpg' },
                {
                    'movie_pic': 'image/tmp/m0.jpg',
                    'movie_title': '12 Rounds (2009)',
                    'upc': '024543589013',
                    'available_count': '1',
                    'movie_big_pic': '131608_big.jpg' },
                {
                    'movie_pic': 'image/tmp/m0.jpg',
                    'movie_title': 'Dragon Hunters (2008)',
                    'upc': '625828457203',
                    'available_count': '1',
                    'movie_big_pic': '131020_big.jpg' }] }
        movieList.setMovieList(data)
        movieList.setGeometry(0, 50, 500, 750)
        tabList = TabList(self)
        data = {
            'ctr_tab_list': [
                {
                    'text': 'New Release',
                    'id': 'NEW RELEASE' },
                {
                    'text': 'Action/Adventure',
                    'id': "('Action/Adventure')" },
                {
                    'text': 'Action',
                    'id': "('Action')" },
                {
                    'text': 'Animation',
                    'id': "('Animation')" },
                {
                    'text': 'Comedy',
                    'id': "('Comedy')" },
                {
                    'text': 'Drama',
                    'id': "('Drama')" },
                {
                    'text': 'Foreign',
                    'id': "('Foreign')" },
                {
                    'text': 'Blu-ray',
                    'id': 'BLU-RAY' },
                {
                    'text': 'All Movies',
                    'id': 'ALL MOVIES' }] }
        tabList.setTabList(data)
        tabList.setGeometry(510, 50, 200, 40)
        data = {
            'ctr_dvd_list': [
                {
                    'movie_pic': 'image/tmp/m0.jpg',
                    'movie_title': 'Chasing The Green (2009)' },
                {
                    'movie_pic': 'image/tmp/m0.jpg',
                    'movie_title': 'Applause For Miss E (2009)' }] }
        listwidget = ListWidget(self)
        listwidget.setGeometry(200, 760, 500, 240)
        listwidget.setDVDList(data)

    
    def test_keyb(self):
        keyboard = numKeyboard('aa', self)
        keyboard.show()

    
    def test_buttonList(self):
        blist = TabList(self)
        blist.setGeometry(500, 220, 218, 500)
        data = {
            'ctr_tab_list': [
                {
                    'text': 'New Release',
                    'id': 'NEW RELEASE' },
                {
                    'text': 'Foreign',
                    'id': "('Foreign')" },
                {
                    'text': 'Western',
                    'id': "('Western')" },
                {
                    'text': 'All Movies',
                    'id': 'ALL MOVIES' }] }
        blist.setTabList(data)
        self.connect(blist, QtCore.SIGNAL('btnListPress(QString)'), self.btnPress)

    
    def btnPress(self, text):
        print('btnPress ' + text)

    
    def test_TitleList(self):
        tlist = PricePlan(self)
        tlist.setGeometry(40, 190, 684, 625)
        data = {
            'ctr_plan_list': [
                {
                    'data_text': 'First Night Fee 1.99, \nAdditional Night Fee 0.99, \nCutoff Time 23:59:59',
                    'id': '1' },
                {
                    'data_text': 'First 12 Hours Fee 1.99 \nor Each 24 Hours Fee 2.99',
                    'id': '2' },
                {
                    'data_text': 'First 12 Hours Fee 1.99 \nor Each 24 Hours Fee 2.99',
                    'id': '2' },
                {
                    'data_text': 'First 12 Hours Fee 1.99 \nor Each 24 Hours Fee 2.99',
                    'id': '2' },
                {
                    'data_text': 'First 12 Hours Fee 1.99 \nor Each 24 Hours Fee 2.99',
                    'id': '2' }] }
        tlist.setPlanList(data)

    
    def test_discInfo(self):
        t = discInfo(self)
        t.setGeometry(0, 0, 660, 480)
        data = {
            'front_slot_id': '101',
            'back_slot_id': '669',
            'check_slot_id': '669' }
        t.setList(data)
        t.txt_price_plan.setText('Chasing The Green ear asing The Green asing The GreenChasing The Green ear asing The Green asing The Green')

    
    def test_TextList(self):
        t = TextList(self)
        t.setGeometry(0, 0, 180, 480)
        data = {
            'slot_list': "['101', '105', '106', '107', '108', '109', '110', '112', '113']" }
        t.setList(data)

    
    def test_messagebox(self):
        mb = messageBox(self, 'aa')
        btn = QtGui.QPushButton('Show', self)
        btn.setGeometry(10, 10, 100, 30)
        QtCore.QObject.connect(btn, QtCore.SIGNAL('clicked()'), self.showmsg)
        self.mb = messageBox('aa', self)
        self.mb.setGeometry(50, 150, config.messageBox_width, config.messageBox_height)
        self.mb.hide()
        kb = allKeyboard('aa', self)
        kb.setGeometry(30, 200, config.messageBox_width, config.messageBox_height)
        kb.hide()
        QtCore.QObject.connect(btn, QtCore.SIGNAL('clicked()'), kb.show)

    
    def showmsg(self):
        self.mb.show({
            'message': 'Dear customer,\nWe detected some connection issue. So if you have purchased Monthly Subscription it might not work this time.\nYou can choose to quit this rental from here.\nIf you have no Monthly Subscription, please feel free to go on.',
            'type': 'continue' })

    
    def test_MovieListAdmin(self):
        ml = MovieListAdmin(self, 1, 75, 6, 5)
        ml.setGeometry(config.layout_x, config.unload_list_y, config.unload_list_width, config.unload_list_height)
        data = {
            'ctr_movie_list': [
                {
                    'price': '39.00',
                    'rfid': '009FBD2730000104E0',
                    'upc': '013131137491',
                    'state': 'in',
                    'slot_id': '2012-02-02 12:12',
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
        ml.setMovieList(data)

    
    def test_Slider(self):
        slider = Slider('ConfigSpeakerVolumeForm', 'btn_volume', self)
        slider.setGeometry(0, 0, 463, 100)
        data = {
            'number': '85' }
        slider.setVolume(data)

    
    def test_DiscList(self):
        dl = DiscList('Main', self)
        dl.setGeometry(0, 0, config.unload_list_width, config.unload_list_height + 16)
        data = {
            'ctr_disc_list': [
                {
                    'movie_pic': 'path/xxx.jpg',
                    'rfid': '5189710231247',
                    'movie_title': 'xxxx',
                    'time_out': '2' },
                {
                    'movie_pic': 'path/xxx.jpg',
                    'rfid': '5189710231247',
                    'movie_title': 'xxxx',
                    'time_out': '2' },
                {
                    'movie_pic': 'path/xxx.jpg',
                    'rfid': '5189710231247',
                    'movie_title': 'xxxx',
                    'time_out': '2' },
                {
                    'movie_pic': 'path/xxx.jpg',
                    'rfid': '5189710231247',
                    'movie_title': 'xxxx',
                    'time_out': '2' }] }
        dl.setDiscList(data)

    
    def test_shoppingcart(self):
        data = {
            'ctr_shopping_cart': [
                {
                    'movie_title': 'Night Train (2009)' },
                {
                    'movie_title': 'Chasing The Green (2009)' }] }
        listview = ListView(self, 510, 300)
        listview.setTabList(data)
        listview.setGeometry(510, 300, 202, 102)

    
    def test_movieFlower(self):
        mf = movieFlower('MainForm', self)
        mf.setGeometry(0, 0, 768, 500)
        data = {
            'ctr_movie_list': [
                {
                    'upc': '502192',
                    'movie_pic': '/home/mm/kiosk/var/gui/pic/78268_big.jpg' },
                {
                    'upc': '502194',
                    'movie_pic': '/home/mm/kiosk/var/gui/pic/23875_big.jpg' },
                {
                    'upc': '502194',
                    'movie_pic': '/home/mm/kiosk/var/gui/pic/117153_big.jpg' },
                {
                    'upc': '502194',
                    'movie_pic': '/home/mm/kiosk/var/gui/pic/105002_big.jpg' },
                {
                    'upc': '502194',
                    'movie_pic': '/home/mm/kiosk/var/gui/pic/104899_big.jpg' },
                {
                    'upc': '502194',
                    'movie_pic': '/home/mm/kiosk/var/gui/pic/90990_big.jpg' },
                {
                    'upc': '502194',
                    'movie_pic': '/home/mm/kiosk/var/gui/pic/116983_big.jpg' },
                {
                    'upc': '502194',
                    'movie_pic': '/home/mm/kiosk/var/gui/pic/19748_big.jpg' },
                {
                    'upc': '502194',
                    'movie_pic': '/home/mm/kiosk/var/gui/pic/103867_big.jpg' },
                {
                    'upc': '502194',
                    'movie_pic': '/home/mm/kiosk/var/gui/pic/116412_big.jpg' },
                {
                    'upc': '502194',
                    'movie_pic': '/home/mm/kiosk/var/gui/pic/74337_big.jpg' }] }
        mf.setMovieList(data)
        mf.show()

    
    def test_DiscOutList(self):
        ds = DiscOutList(self)
        ds.setGeometry(0, 10, 768, 700)
        data = [
            {
                'feature': [
                    {
                        'Title': 'sk' },
                    {
                        'Rental Time': '2010-11-11 08:23:45' },
                    {
                        'CC Name': 'John' }],
                'rfid': 1,
                'movie_pic': '/home/mm/var/images/goodsrec/images/735.jpg',
                'is_bluray': '2' },
            {
                'feature': [
                    {
                        'Title': 'st' },
                    {
                        'Rental Time': '2010-11-11 08:24:45' },
                    {
                        'CC Name': 'Alice' }],
                'rfid': 2,
                'movie_pic': '/home/mm/var/images/goodsrec/images/737.jpg',
                'is_bluray': '2' },
            {
                'feature': [
                    {
                        'Title': 'sw' },
                    {
                        'Rental Time': '2010-11-11 08:25:45' },
                    {
                        'CC Name': 'Hely' }],
                'rfid': 3,
                'movie_pic': '/home/mm/var/images/goodsrec/images/738.jpg',
                'is_bluray': '2' },
            {
                'feature': [
                    {
                        'Title': 'sw' },
                    {
                        'Rental Time': '2010-11-11 08:27:45' },
                    {
                        'CC Name': 'Vivi' }],
                'rfid': 3,
                'movie_pic': '/home/mm/var/images/goodsrec/images/738.jpg',
                'is_bluray': '2' },
            {
                'feature': [
                    {
                        'Title': 'sw' },
                    {
                        'Rental Time': '2010-11-11 08:21:45' },
                    {
                        'CC Name': 'Linken' }],
                'rfid': 4,
                'movie_pic': '/home/mm/var/images/goodsrec/images/738.jpg',
                'is_bluray': '2' },
            {
                'feature': [
                    {
                        'Title': 'sj' },
                    {
                        'Rental Time': '2010-11-11 08:22:45' },
                    {
                        'CC Name': 'Yoki' }],
                'rfid': '6',
                'movie_pic': '/home/mm/var/images/goodsrec/images/740.jpg',
                'is_bluray': '2' }]
        data_1 = [
            {
                'feature': [
                    {
                        'name': 'sk' },
                    {
                        'time': '2012' },
                    {
                        'aa': 'bb' }],
                'movie_pic': '/home/mm/var/images/goodsrec/images/735.jpg',
                'is_bluray': '2' }]
        ds.setDiscList(data)

    
    def test_qtn_btn(self):
        t = SlotsQtnBtn(self)
        data = {
            'text': {
                'all': '324',
                'bad': '343',
                'empty': '55' } }
        t.set_label_text(data)
        t.show()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainf = myForm()
    mainf.test_qtn_btn()
    mainf.show()
    sys.exit(app.exec_())

