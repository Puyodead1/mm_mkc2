# Source Generated with Decompyle++
# File: movie_price_ui.pyc (Python 2.5)

from PyQt4 import QtCore, QtGui

class Ui_MoviePriceForm(object):
    
    def setupUi(self, MoviePriceForm):
        MoviePriceForm.setObjectName('MoviePriceForm')
        MoviePriceForm.resize(QtCore.QSize(QtCore.QRect(0, 0, 768, 1024).size()).expandedTo(MoviePriceForm.minimumSizeHint()))
        MoviePriceForm.setMinimumSize(QtCore.QSize(768, 1024))
        MoviePriceForm.setMaximumSize(QtCore.QSize(768, 1024))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        MoviePriceForm.setPalette(palette)
        MoviePriceForm.setWindowIcon(QtGui.QIcon('../../../../.designer/backup'))
        MoviePriceForm.setAutoFillBackground(True)
        self.txt_rent_label = QtGui.QLabel(MoviePriceForm)
        self.txt_rent_label.setGeometry(QtCore.QRect(50, 30, 451, 50))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.txt_rent_label.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setWeight(75)
        font.setBold(True)
        self.txt_rent_label.setFont(font)
        self.txt_rent_label.setObjectName('txt_rent_label')
        self.horizontalLayout = QtGui.QWidget(MoviePriceForm)
        self.horizontalLayout.setGeometry(QtCore.QRect(30, 910, 711, 101))
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.hboxlayout = QtGui.QHBoxLayout(self.horizontalLayout)
        self.hboxlayout.setObjectName('hboxlayout')
        self.label_15 = QtGui.QLabel(MoviePriceForm)
        self.label_15.setGeometry(QtCore.QRect(50, 430, 241, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_15.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.label_15.setFont(font)
        self.label_15.setObjectName('label_15')
        self.terms = QtGui.QTextEdit(MoviePriceForm)
        self.terms.setGeometry(QtCore.QRect(50, 470, 661, 371))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.terms.setFont(font)
        self.terms.setProperty('cursor', QtCore.QVariant(QtCore.Qt.BlankCursor))
        self.terms.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.terms.setUndoRedoEnabled(False)
        self.terms.setReadOnly(True)
        self.terms.setCursorWidth(0)
        self.terms.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.terms.setObjectName('terms')
        self.frame_2 = QtGui.QFrame(MoviePriceForm)
        self.frame_2.setGeometry(QtCore.QRect(50, 195, 661, 221))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setObjectName('frame_2')
        self.movie_title = QtGui.QLabel(MoviePriceForm)
        self.movie_title.setGeometry(QtCore.QRect(50, 111, 661, 60))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 85, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.movie_title.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setWeight(75)
        font.setBold(True)
        self.movie_title.setFont(font)
        self.movie_title.setWordWrap(True)
        self.movie_title.setObjectName('movie_title')
        self.dvd_version = QtGui.QLabel(MoviePriceForm)
        self.dvd_version.setGeometry(QtCore.QRect(65, 171, 241, 22))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 125, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.dvd_version.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.dvd_version.setFont(font)
        self.dvd_version.setObjectName('dvd_version')
        self.icon_dvd = QtGui.QLabel(MoviePriceForm)
        self.icon_dvd.setGeometry(QtCore.QRect(65, 357, 100, 54))
        self.icon_dvd.setObjectName('icon_dvd')
        self.movie_pic = QtGui.QLabel(MoviePriceForm)
        self.movie_pic.setGeometry(QtCore.QRect(65, 205, 100, 150))
        self.movie_pic.setMinimumSize(QtCore.QSize(100, 150))
        self.movie_pic.setMaximumSize(QtCore.QSize(100, 150))
        self.movie_pic.setScaledContents(True)
        self.movie_pic.setObjectName('movie_pic')
        self.retranslateUi(MoviePriceForm)
        QtCore.QMetaObject.connectSlotsByName(MoviePriceForm)

    
    def retranslateUi(self, MoviePriceForm):
        self.txt_rent_label.setText(QtGui.QApplication.translate('MoviePriceForm', 'Details', None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate('MoviePriceForm', 'Terms And Conditions', None, QtGui.QApplication.UnicodeUTF8))


