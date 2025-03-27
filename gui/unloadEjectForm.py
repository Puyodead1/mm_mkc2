# Source Generated with Decompyle++
# File: unloadEjectForm.pyc (Python 2.5)

'''
UnloadEjectForm for unload
2009-07-14 created by Mavis
'''
import sys
import config
from PyQt4 import QtCore, QtGui
from checkOutEjectForm_ui import Ui_checkOutEjectForm
from squery import socketQuery
from component import btnBack, SWF_vomit, SWF_robot_send, SWF_robot_take

class UnloadEjectForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_checkOutEjectForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_movie)))
        self.setPalette(palette)
        self.sq = socketQuery()
        self.ui.verticalLayout.setMinimumHeight(300)
        self.ui.txtbox_msg_11.setMaximumWidth(280)
        self.ui.swf_send_disc = SWF_robot_send(self)
        robot_y = self.ui.verticalLayout.y() + self.ui.verticalLayout.height()
        robot_h = 522
        if robot_y + 522 > 890:
            robot_h = 890 - robot_y
        
        self.ui.swf_send_disc.setGeometry(120, robot_y, 585, robot_h)
        self.ui.swf_take_dvd = SWF_robot_take(self)
        self.ui.swf_take_dvd.setGeometry(120, robot_y, 585, robot_h)
        self.ui.swf_vomit_dvd = SWF_vomit(self)
        self.ui.swf_vomit_dvd.setGeometry(140, 490, 487, 285)
        self.ui.swf_take_dvd.hide()
        self.ui.swf_send_disc.hide()
        self.ui.swf_vomit_dvd.hide()
        self.ui.btn_back = btnBack(self, 'UnloadEjectForm')
        self.ui.btn_back.setGeometry(580, 20, 160, 68)
        self.init()

    
    def showEvent(self, event):
        self.init()
        self.ui.retranslateUi(None)
        self.ui.btn_back.reset()

    
    def init(self):
        self.ui.txtbox_msg_3.clear()
        self.ui.txtbox_msg_11.setText(QtGui.QApplication.translate('Form', 'Unloading DVD(s): ', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.txt_label.setText(QtGui.QApplication.translate('Form', 'Unload', None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = UnloadEjectForm()
    translate = QtCore.QTranslator()
    translate.load('trans_sp.qm', config.transDir)
    app.installTranslator(translate)
    form.show()
    form.ui.swf_vomit_dvd.show()
    sys.exit(app.exec_())

