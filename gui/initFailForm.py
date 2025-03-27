# Source Generated with Decompyle++
# File: initFailForm.pyc (Python 2.5)

'''
InitFailForm for initial fail form
2009-07-14 created by Mavis
'''
import sys
import config
from PyQt4 import QtCore, QtGui

class InitFailForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(0, 0, 768, 1024)
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_init_failed)))
        self.setPalette(palette)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = InitFailForm()
    form.show()
    sys.exit(app.exec_())

