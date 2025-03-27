# Source Generated with Decompyle++
# File: returnDiscListForm.pyc (Python 2.5)

'''
ReturnDiscListForm
2009-07-29 created by Mavis
'''
import sys
from PyQt4 import QtCore, QtGui
from returnDiscListForm_ui import Ui_returnDiscListForm
import config
from component import DiscList, messageBox, btnBack

class ReturnDiscListForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_returnDiscListForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_returnb)))
        self.setPalette(palette)
        self.ui.btn_back = btnBack(self, 'ReturnDiscListForm')
        self.ui.btn_back.setGeometry(580, 20, 160, 68)
        self.ui.ctr_disc_list = DiscList('ReturnDiscListForm', self)
        self.ui.ctr_disc_list.setGeometry(config.layout_x, self.ui.txt_title.y() + self.ui.txt_title.height(), config.unload_list_width, config.unload_list_height)
        self.ui.ReturnDiscListForm_ctr_message_box = messageBox('ReturnDiscListForm', self)

    
    def showEvent(self, event):
        self.ui.retranslateUi('')
        self.ui.btn_back.reset()
        self.ui.ctr_disc_list.hlabel.setText(QtGui.QApplication.translate('Form', '  Disc Information                           Rental Time', None, QtGui.QApplication.UnicodeUTF8))

    
    def hideEvent(self, event):
        self.ui.ReturnDiscListForm_ctr_message_box.hide()
        self.hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    import os
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    form = ReturnDiscListForm()
    form.show()
    sys.exit(app.exec_())

