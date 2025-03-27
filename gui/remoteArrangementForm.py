# Source Generated with Decompyle++
# File: remoteArrangementForm.pyc (Python 2.5)

'''
RemoteArrangementForm 
2009-08-13 created by Mavis
'''
import sys
from PyQt4 import QtCore, QtGui
import config
from component import SWF_robot_send

class RemoteArrangementForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = QtCore.QObject(self)
        self.setGeometry(0, 0, 768, 1024)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_return)))
        self.setPalette(palette)
        self.ui.txt_msg = QtGui.QLabel(self)
        self.ui.txt_msg.setStyleSheet('color: #0060b4; font: bold 30px;')
        self.ui.txt_msg.setGeometry(90, 160, 571, 71)
        self.ui.swf_send_disc = SWF_robot_send(self)
        self.ui.swf_send_disc.setGeometry(110, 280, 585, 522)
        self.ui.swf_send_disc.hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = RemoteArrangementForm()
    form.show()
    form.ui.txt_msg.setText('aklsjdklfjlakj')
    sys.exit(app.exec_())

