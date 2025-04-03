# Source Generated with Decompyle++
# File: guiConfigHDMIStateForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2009-07-23 Andrew
andrew.lu@cereson.com

Filename: guiConfigHDMIStateForm.py
Config Form for HDMI connection
Screen ID: C6

Change Log:

'''
import fcntl
from mcommon import *
from config import HDMI_CONNECT, HDMI_LOCK_FILE, VGA_PORT
from linuxCmd import get_hdmi_port
from guiBaseForms import ConfigForm
log = initlog('guiConfigHDMIStateForm')

class ConfigHDMIStateForm(ConfigForm):
    
    def __init__(self):
        ConfigForm.__init__(self)
        self.screenID = 'C6'
        self.preWindowID = 'AdminMainForm'
        self.uiErrorWindowID = 'AdminMainForm'
        self.timeoutSec = 60
        self.lstResponseCtrl += [
            'ConfigHDMIStateForm_ctr_message_box']

    
    def _initComponents(self):
        ConfigForm._initComponents(self)
        self._showHdmiStatus()

    
    def _showHdmiStatus(self):
        self.connected = os.path.isfile(HDMI_CONNECT)
        if self.connected == True:
            self._hdmi_on()
        else:
            self._hdmi_off()

    
    def _hdmi_on(self):
        self.flash.send('txt_status', 'setText', {
            'text': _('HDMI Connected') })
        msg = _('Would you like to DISCONNECT the HDMI?')
        self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
            'message': msg,
            'type': 'confirm' })

    
    def _hdmi_off(self):
        self.flash.send('txt_status', 'setText', {
            'text': _('HDMI Disconnected') })
        msg = _('Would you like to CONNECT the HDMI?')
        self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
            'message': msg,
            'type': 'confirm' })

    
    def on_btn_hdmi_off_event(self):
        self._hdmi_off()

    
    def on_btn_hdmi_on_event(self):
        self._hdmi_on()

    
    def _open_hdmi_lock_file(self):
        self.lockfile = open(HDMI_LOCK_FILE, 'w')

    
    def _close_hdmi_lock_file(self):
        self.lockfile.close()

    
    def _lock_hdmi(self):
        for i in range(10):
            
            try:
                fcntl.lockf(self.lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except:
                time.sleep(0.5)

        

    
    def _unlock_hdmi(self):
        fcntl.lockf(self.lockfile, fcntl.LOCK_UN)

    
    def on_ConfigHDMIStateForm_ctr_message_box_event(self):
        inputVal = self._getEventParam('ConfigHDMIStateForm_ctr_message_box', 'val')
        if str(inputVal).lower() == 'yes':
            self._open_hdmi_lock_file()
            self._lock_hdmi()
            hdmi_port = get_hdmi_port()
            if self.connected == True:
                self.flash.send('txt_status', 'setText', {
                    'text': _('HDMI Disconnected') })
                self.connected = False
                os.system('rm %s' % HDMI_CONNECT)
                os.system('pkill mplayer')
                os.system('DISPLAY=:0.0 /usr/bin/xrandr --output HDMI-1 --off')
                os.system('DISPLAY=:0.0 /usr/bin/xrandr --output HDMI-2 --off')
                self.connProxy.setHDMI('off')
            else:
                os.system('DISPLAY=:0.0 /usr/bin/xrandr --output %s --auto' % hdmi_port)
                time.sleep(1)
                os.system('DISPLAY=:0.0 /usr/bin/xrandr --output %s --left-of %s' % (VGA_PORT, hdmi_port))
                os.system('touch %s' % HDMI_CONNECT)
                self.flash.send('txt_status', 'setText', {
                    'text': _('HDMI Connected') })
                self.connected = True
                self.connProxy.setHDMI('on')
            self._unlock_hdmi()
            self._close_hdmi_lock_file()
            self._setHDMIButton()
            self.flash.send('%s_ctr_message_box' % self.windowID, 'close', { })
        


