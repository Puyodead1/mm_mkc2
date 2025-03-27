# Source Generated with Decompyle++
# File: loadResultForm.pyc (Python 2.5)

'''
LoadResultForm 
2009-07-26 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
from loadResultForm_ui import Ui_loadResultForm
import config
from squery import socketQuery
from component import messageBox, ctrButton, btnFinish

class LoadResultForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_loadResultForm()
        self.ui.setupUi(self)
        self.parent = parent
        self.setGeometry(0, 1024 - 649, 768, 649)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_load2)))
        self.setPalette(palette)
        self.sq = socketQuery()
        style = 'color: white; font: bold italic 23px; border-style: outset; background-image: url(' + config.pic_btn_blue + ')'
        self.ui.btn_again = ctrButton(self, 'LoadResultForm', 'btn_again', QtGui.QApplication.translate('Form', 'Load Again', None, QtGui.QApplication.UnicodeUTF8), 160, 68, style)
        self.ui.btn_another = ctrButton(self, 'LoadResultForm', 'btn_another', QtGui.QApplication.translate('Form', 'Load New', None, QtGui.QApplication.UnicodeUTF8), 160, 68, style)
        self.ui.btn_finish = btnFinish(self, 'LoadResultForm')
        self.ui.hboxlayout.addWidget(self.ui.btn_again)
        self.ui.hboxlayout.addWidget(self.ui.btn_another)
        self.ui.hboxlayout.addWidget(self.ui.btn_finish)
        self.ui.LoadResultForm_ctr_message_box = messageBox('LoadResultForm', self)

    
    def hideEvent(self, event):
        self.ui.LoadResultForm_ctr_message_box.hide()
        self.hide()
        if self.parent:
            self.parent.hide()
        

    
    def showEvent(self, event):
        self.ui.btn_finish.reset()
        self.ui.btn_again.setText(QtGui.QApplication.translate('Form', 'Load Again', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_another.setText(QtGui.QApplication.translate('Form', 'Load New', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = LoadResultForm()
    mainf.show()
    mainf.ui.txtbox_msg.setText('Chargement \xe9chou\xe9, il semble que le disque a \xe9t\xe9 d\xe9j\xe0 charg\xe9. Svp remettez-le manuellement dans le slot 101. Si le slot 101 est d\xe9j\xe0 occup\xe9 par un autre disc, d\xe9chargez-le et v\xe9rifiez \xe0 quel slot il appartient.')
    sys.exit(app.exec_())

