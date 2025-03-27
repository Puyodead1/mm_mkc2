# Source Generated with Decompyle++
# File: unloadResultForm.pyc (Python 2.5)

'''
UnloadResultForm 
2009-07-26 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
from unloadResultForm_ui import Ui_unloadResultForm
import config
from squery import socketQuery
from component import ctrButton, btnLogout, btnFinish

class UnloadResultForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_unloadResultForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_load)))
        self.setPalette(palette)
        self.ui.btn_logout = btnLogout(self, 'UnloadResultForm')
        self.ui.btn_logout.setGeometry(580, 20, 160, 68)
        self.ui.btn_another = ctrButton(self, 'UnloadResultForm', 'btn_another', QtGui.QApplication.translate('UnloadByTitleForm', 'Unload Another', None, QtGui.QApplication.UnicodeUTF8), config.btn_width, config.btn_height, 'color: white; font: bold italic 24px; border-style: outset; background-image: url(' + config.pic_btn_blue_02 + ')')
        self.ui.btn_finish = btnFinish(self, 'UnloadResultForm')
        self.ui.hboxlayout.addWidget(self.ui.btn_another)
        self.ui.hboxlayout.addWidget(self.ui.btn_finish)

    
    def showEvent(self, event):
        self.ui.retranslateUi(None)
        self.ui.btn_logout.reset()
        self.ui.btn_finish.reset()
        self.ui.btn_another.setText(QtGui.QApplication.translate('UnloadByTitleForm', 'Unload Another', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    if os.path.isfile(config.transDir + 'trans_sp.qm'):
        translate = QtCore.QTranslator()
        translate.load('trans_sp.qm', config.transDir)
        app.installTranslator(translate)
    
    mainf = UnloadResultForm()
    mainf.show()
    mainf.ui.txtbox_msg.setText('ALSasd\nKJasdfa\nDasd\nfjlaskjd\nasdf\nasdfGg\nlaksjdflakjs\nlkdjf;aoiwueiofjjf')
    sys.exit(app.exec_())

