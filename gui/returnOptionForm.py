# Source Generated with Decompyle++
# File: returnOptionForm.pyc (Python 2.5)

'''
ReturnOptionForm
2009-07-29 created by Mavis
'''
import sys
from PyQt4 import QtCore, QtGui
from returnResultForm_ui import Ui_returnResultForm
import config
from component import ctrButton, numKeyboard, messageBox, btnCancel

class ReturnOptionForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_returnResultForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        self.setFixedSize(768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_return)))
        self.setPalette(palette)
        styleRed = 'color: white; font: bold italic 26px; border-style: outset; background-image: url(' + config.pic_btn_config_red + ')'
        styleBlue = 'color: white; font: bold italic 26px; border-style: outset; background-image: url(' + config.pic_btn_config_blue + ')'
        self.ui.btn_try_again = ctrButton(self, 'ReturnOptionForm', 'btn_try_again', QtGui.QApplication.translate('Return', 'Try again', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, styleBlue)
        self.ui.btn_try_again.setGeometry((768 - config.btnWidth) / 2, self.ui.txt_msg.y() + self.ui.txt_msg.height(), config.btnWidth, config.btnHeight)
        self.ui.btn_by_card = ctrButton(self, 'ReturnOptionForm', 'btn_by_card', QtGui.QApplication.translate('Return', 'By Card', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, styleRed)
        self.ui.btn_by_card.setGeometry((768 - (2 * config.btnWidth + 50)) / 2, self.ui.txt_return_option.y() + self.ui.txt_return_option.height(), config.btnWidth, config.btnHeight)
        self.ui.btn_by_code = ctrButton(self, 'ReturnOptionForm', 'btn_by_code', QtGui.QApplication.translate('Return', 'By Code', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, styleRed)
        self.ui.btn_by_code.setGeometry(self.ui.btn_by_card.x() + config.btnWidth + 50, self.ui.txt_return_option.y() + self.ui.txt_return_option.height(), config.btnWidth, config.btnHeight)
        self.ui.btn_cancel = btnCancel(self, 'ReturnOptionForm')
        self.ui.btn_cancel.setGeometry(540, 920, self.ui.btn_cancel.width(), self.ui.btn_cancel.height())
        self.ui.ReturnOptionForm_ctr_num_keyboard = numKeyboard('ReturnOptionForm', self)
        self.ui.ReturnOptionForm_ctr_message_box = messageBox('ReturnOptionForm', self)

    
    def showEvent(self, event):
        self.ui.retranslateUi('')
        self.ui.btn_try_again.reset(QtCore.QT_TRANSLATE_NOOP('Form', 'Try again'))
        self.ui.btn_by_card.reset(QtCore.QT_TRANSLATE_NOOP('Form', 'By Card'))
        self.ui.btn_by_code.reset(QtCore.QT_TRANSLATE_NOOP('Form', 'By Code'))
        self.ui.btn_cancel.reset()

    
    def hideEvent(self, event):
        self.ui.ReturnOptionForm_ctr_message_box.hide()
        if self.ui.ReturnOptionForm_ctr_num_keyboard.isVisible():
            self.ui.ReturnOptionForm_ctr_num_keyboard.hide()
        
        self.hide()


if __name__ == '__main__':
    import os
    app = QtGui.QApplication(sys.argv)
    form = ReturnOptionForm()
    if os.path.isfile(config.transDir + config.transFile):
        translate = QtCore.QTranslator()
        translate.load(config.transFile, config.transDir)
        app.installTranslator(translate)
    
    form.show()
    form.ui.txt_msg.setText('ajslkdjfl\nLKAJSLDF\nkjlkjS')
    sys.exit(app.exec_())

