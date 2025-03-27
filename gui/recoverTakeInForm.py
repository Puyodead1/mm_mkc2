# Source Generated with Decompyle++
# File: recoverTakeInForm.pyc (Python 2.5)

'''
RecoverTakeInForm for initial form
2009-07-14 created by Mavis
'''
import sys
import config
from PyQt4 import QtCore, QtGui
from component import SWF_robot_send

class RecoverTakeInForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = QtCore.QObject()
        self.setGeometry(0, 0, 768, 1024)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_return)))
        self.setPalette(palette)
        self.ui.txt_msg = QtGui.QLabel(self)
        self.ui.txt_msg.setGeometry(100, 120, 568, 280)
        self.ui.txt_msg.setStyleSheet('font: bold 26px')
        self.ui.txt_msg.setWordWrap(True)
        self.ui.swf_send_disc = SWF_robot_send(self)
        self.ui.swf_send_disc.setGeometry(QtCore.QRect(110, 400, 585, 522))
        self.ui.swf_send_disc.hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = RecoverTakeInForm()
    form.show()
    form.ui.txt_msg.setText('LKJSLDKF\nJALSK\nJDLFJAS\nLKDJF\naalksjdflkj')
    sys.exit(app.exec_())

