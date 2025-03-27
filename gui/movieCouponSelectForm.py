# Source Generated with Decompyle++
# File: movieCouponSelectForm.pyc (Python 2.5)

'''
MovieCouponSelectForm for coupon select. 
2009-07-17 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
import config
import component
from squery import socketQuery

class MovieCouponSelectForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry((768 - config.bg_kb_width) / 2, 400, config.bg_kb_width, config.bg_kb_height)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_kb_num)))
        self.setPalette(palette)
        self.sq = socketQuery()
        self.ui = QtCore.QObject(self)
        self.ui.ctr_movie_info = component.ListWidget_2(self)
        self.ui.ctr_movie_info.setGeometry(10, 20, config.bg_kb_width - 20, config.bg_kb_height - 20)
        btn_close = QtGui.QPushButton(self)
        btn_close.setIcon(QtGui.QIcon(config.pic_icon_close))
        btn_close.setIconSize(QtCore.QSize(30, 30))
        btn_close.setGeometry(config.bg_kb_width - 35, 5, 30, 30)
        QtCore.QObject.connect(self.ui.ctr_movie_info, QtCore.SIGNAL('itemClicked(QListWidgetItem*)'), self.movie_click)
        QtCore.QObject.connect(btn_close, QtCore.SIGNAL('clicked()'), self.close)

    
    def movie_click(self, item):
        rfid = item.data(self.ui.ctr_movie_info.dataType).toString()
        print(rfid)
        data = { }
        data['wid'] = 'MovieCouponSelectForm'
        data['cid'] = 'ctr_movie_info'
        data['type'] = 'EVENT'
        data['EVENT'] = 'EVENT_MOUSE_CLICK'
        data['param_info'] = { }
        data['param_info']['ctr_movie_info'] = { }
        data['param_info']['ctr_movie_info']['rfid'] = str(rfid)
        self.sq.send(data)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainf = MovieCouponSelectForm()
    data = {
        'ctr_movie_info': [
            {
                'movie_pic': 'image/tmp/m0.jpg',
                'price_plan_text': 'First 1 Hours Fee $10 \nor Each 2 Hours Fee $100',
                'rfid': 'fdasfas' },
            {
                'movie_pic': 'image/tmp/m0.jpg',
                'price_plan_text': '[2009] AKS fdsafas',
                'rfid': '1234' }],
        'selected_rfid': '1234' }
    mainf.ui.ctr_movie_info.setMovieInfo(data)
    mainf.show()
    sys.exit(app.exec_())

