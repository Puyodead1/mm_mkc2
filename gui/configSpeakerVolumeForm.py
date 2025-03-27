# Source Generated with Decompyle++
# File: configSpeakerVolumeForm.pyc (Python 2.5)

'''
ConfigSpeakerVolumeForm 
2009-07-26 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
import config
import component

class ConfigSpeakerVolumeForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = component.ConfigForm('ConfigSpeakerVolumeForm', self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_config)))
        self.setPalette(palette)
        self.ui.txt_status = QtGui.QLabel(QtGui.QApplication.translate('configForm', 'Speaker Volume Control', None, QtGui.QApplication.UnicodeUTF8), self)
        self.ui.txt_status.setStyleSheet('color: #0060b4; font: bold 26px;')
        self.ui.txt_status.setGeometry(config.layout_x, config.title_y, config.layout_width, 50)
        self.ui.txt_message = QtGui.QLabel(QtGui.QApplication.translate('configForm', 'Click the slider to Control the Volume.', None, QtGui.QApplication.UnicodeUTF8), self)
        self.ui.txt_message.setStyleSheet('color: #bb0000; font: bold 22px;')
        self.ui.txt_message.setGeometry(config.layout_x, self.ui.txt_status.y() + 50, config.layout_width, 50)
        speakerWidth = 102
        speakerHeight = 100
        speakerStyle = 'border-style: outset; background-image: url(' + config.pic_btn_icon_speaker + ')'
        speakerOffStyle = 'border-style: outset; background-image: url(' + config.pic_btn_icon_speaker_off + ')'
        self.ui.btn_speaker_off = component.ctrButton(self, 'ConfigSpeakerVolumeForm', 'btn_speaker_off', '', speakerWidth, speakerHeight, speakerOffStyle)
        self.ui.btn_speaker_off.setGeometry(config.layout_x, self.ui.txt_message.y() + self.ui.txt_message.height() + 30, speakerWidth, speakerHeight)
        self.ui.btn_speaker_off.hide()
        self.ui.btn_speaker_on = component.ctrButton(self, 'ConfigSpeakerVolumeForm', 'btn_speaker_on', '', speakerWidth, speakerHeight, speakerStyle)
        self.ui.btn_speaker_on.setGeometry(config.layout_x, self.ui.txt_message.y() + self.ui.txt_message.height() + 30, speakerWidth, speakerHeight)
        self.ui.btn_confirm = component.ctrButton(self, 'ConfigSpeakerVolumeForm', 'btn_confirm', QtGui.QApplication.translate('configForm', 'Confirm', None, QtGui.QApplication.UnicodeUTF8), config.btnWidth, config.btnHeight, config.btnRedStyle)
        self.ui.btn_confirm.setGeometry((768 - config.btnWidth) / 2, 780, config.btnWidth, config.btnHeight)
        self.ui.btn_volume = component.Slider('ConfigSpeakerVolumeForm', 'btn_volume', self)
        self.ui.btn_volume.setGeometry(config.layout_x + speakerWidth + 20, self.ui.btn_speaker_on.y(), 463, speakerHeight)
        self.ui.ConfigSpeakerVolumeForm_ctr_message_box = component.messageBox('ConfigSpeakerVolumeForm', self)
        self.ui.ConfigSpeakerVolumeForm_ctr_message_box.hide()

    
    def showEvent(self, event):
        self.ui.reset()
        self.ui.txt_status.setText(QtGui.QApplication.translate('configForm', 'Speaker Volume Control', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.txt_message.setText(QtGui.QApplication.translate('configForm', 'Click the slider to Control the Volume.', None, QtGui.QApplication.UnicodeUTF8))
        self.ui.btn_confirm.setText(QtGui.QApplication.translate('configForm', 'Confirm', None, QtGui.QApplication.UnicodeUTF8))

    
    def hideEvent(self, event):
        self.ui.ConfigSpeakerVolumeForm_ctr_message_box.hide()
        self.hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainf = ConfigSpeakerVolumeForm()
    mainf.show()
    sys.exit(app.exec_())

