# Source Generated with Decompyle++
# File: loadTakeInForm.pyc (Python 2.5)

'''
LoadTakeInForm 
2009-07-26 created by Mavis
'''
import os
import sys
import config
from PyQt4 import QtCore, QtGui
from squery import socketQuery
from component import btnCancel, SWF_insert, SWF_vomit, SWF_robot_send

class LoadTakeInForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = QtCore.QObject()
        self.setAutoFillBackground(True)
        self.parent = parent
        self.setGeometry(0, 1024 - 649, 768, 649)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_load2)))
        self.setPalette(palette)
        self.sq = socketQuery()
        self.ui.btn_cancel = btnCancel(self, 'LoadTakeInForm')
        self.ui.btn_cancel.setGeometry(560, 550, 160, 68)
        self.ui.swf_send_disc = SWF_robot_send(self)
        self.ui.swf_send_disc.setGeometry(110, 110, 585, 410)
        self.ui.swf_send_disc.movie.setScaledSize(QtCore.QSize(585, 410))
        self.ui.swf_insert = SWF_insert(self)
        self.ui.swf_insert.setGeometry(140, 210, 487, 285)
        self.ui.swf_vomit_dvd = SWF_vomit(self)
        self.ui.swf_vomit_dvd.setGeometry(QtCore.QRect(self.ui.swf_insert.x(), self.ui.swf_insert.y(), 487, 285))
        self.ui.swf_vomit_dvd.hide()
        self.ui.swf_send_disc.hide()
        self.ui.swf_insert.hide()
        self.ui.txtbox_msg = QtGui.QLabel('asdfasfd', self)
        self.ui.txtbox_msg.setGeometry(QtCore.QRect(60, 9, 648, 271))
        font = QtGui.QFont()
        font.setFamily('Sans Serif')
        font.setPointSize(22)
        font.setWeight(75)
        font.setBold(True)
        self.ui.txtbox_msg.setFont(font)
        self.ui.txtbox_msg.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.ui.txtbox_msg.setWordWrap(True)
        brush = QtGui.QBrush(QtGui.QColor(0, 96, 180))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        self.ui.txtbox_msg.setPalette(palette)

    
    def showEvent(self, event):
        self.ui.btn_cancel.reset()

    
    def hideEvent(self, event):
        self.hide()
        if self.parent:
            self.parent.hide()
        


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = LoadTakeInForm()
    mainf.show()
    mainf.ui.txtbox_msg.setText('Chargement semble que le disque a')
    mainf.ui.swf_send_disc.show()
    sys.exit(app.exec_())

