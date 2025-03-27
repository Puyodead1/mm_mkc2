# Source Generated with Decompyle++
# File: returnResultForm.pyc (Python 2.5)

'''
ReturnResultForm
2009-07-29 created by Mavis
'''
import sys
from PyQt4 import QtCore, QtGui
from returnResultForm_ui import Ui_returnResultForm
import config
from component import ctrButton, btnFinish, messageBox

class ReturnResultForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_returnResultForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_returnb)))
        self.setPalette(palette)
        style_another = 'color: white; font: bold italic 21px; border-style: outset; background-image: url(' + config.pic_btn_blue_02 + ')'
        style_rent = 'color: white; font: bold italic 21px; border-style: outset; background-image: url(' + config.pic_btn_green_02 + ')'
        style_finish = 'color: white; font: bold italic 21px; border-style: outset; background-image: url(' + config.pic_btn_red_02 + ')'
        self.ui.btn_another = ctrButton(self, 'ReturnResultForm', 'btn_another', QtGui.QApplication.translate('Return', 'Another', None, QtGui.QApplication.UnicodeUTF8), 205, 68, style = style_another)
        self.ui.btn_finish = ctrButton(self, 'ReturnResultForm', 'btn_finish', QtGui.QApplication.translate('Component', 'Finish', None, QtGui.QApplication.UnicodeUTF8), 205, 68, style = style_finish)
        self.ui.btn_returnagain = ctrButton(self, 'ReturnResultForm', 'btn_returnagain', QtGui.QApplication.translate('Return', 'Rent Again', None, QtGui.QApplication.UnicodeUTF8), 205, 68, style = style_rent)
        self.ui.hboxlayout.addWidget(self.ui.btn_another)
        self.ui.hboxlayout.addWidget(self.ui.btn_returnagain)
        self.ui.hboxlayout.addWidget(self.ui.btn_finish)
        self.ui.ReturnResultForm_ctr_message_box = messageBox('ReturnResultForm', self)

    
    def showEvent(self, event):
        self.ui.retranslateUi('')
        self.ui.btn_another.setText(QtGui.QApplication.translate('Return', 'Another', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_returnagain.setText(QtGui.QApplication.translate('Return', 'Rent Again', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_finish.setText(QtGui.QApplication.translate('Return', 'Finish', None, QtGui.QApplication.UnicodeUTF8))

    
    def hideEvent(self, event):
        self.ui.ReturnResultForm_ctr_message_box.hide()
        self.hide()


if __name__ == '__main__':
    import os
    app = QtGui.QApplication(sys.argv)
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    form = ReturnResultForm()
    form.show()
    sys.exit(app.exec_())

