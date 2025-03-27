# Source Generated with Decompyle++
# File: pickupEjectForm.pyc (Python 2.5)

'''
PickUpEjectForm is for pickup. 
2009-07-16 created by Mavis
'''
import sys
import config
from PyQt4 import QtCore, QtGui
from checkOutEjectForm_ui import Ui_checkOutEjectForm
from component import SWF_robot_send, SWF_robot_take, SWF_vomit

class PickUpEjectForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_checkOutEjectForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_pickup)))
        self.setPalette(palette)
        self.ui.swf_send_disc = SWF_robot_send(self)
        self.ui.swf_send_disc.setGeometry(110, 360, 585, 522)
        self.ui.swf_take_dvd = SWF_robot_take(self)
        self.ui.swf_take_dvd.setGeometry(QtCore.QRect(110, 360, 585, 522))
        self.ui.swf_vomit_dvd = SWF_vomit(self)
        self.ui.swf_vomit_dvd.setGeometry(QtCore.QRect(140, 490, 487, 290))
        self.ui.swf_send_disc.hide()
        self.ui.swf_take_dvd.hide()
        self.ui.swf_vomit_dvd.hide()
        self.ui.txt_label.setText(QtGui.QApplication.translate('Form', 'Pick Up', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.verticalLayout.setStyleSheet('QLabel {color: #006633; font: bold 28px}')

    
    def showEvent(self, event):
        self.ui.retranslateUi(None)
        self.ui.txt_label.setText(QtGui.QApplication.translate('Form', 'Pick Up', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    import os
    config.transFile = 'trans_sp.qm'
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    mainf = PickUpEjectForm()
    mainf.show()
    sys.exit(app.exec_())

