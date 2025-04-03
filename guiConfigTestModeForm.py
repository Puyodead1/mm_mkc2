# Source Generated with Decompyle++
# File: guiConfigTestModeForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2009-03-06 Vincent
vincent.chen@cereson.com

Filename: guiConfigTestModeForm.py
Config Form for switching TEST MODE
Screen ID: C1

Change Log:

'''
from mcommon import *
from guiBaseForms import ConfigForm
log = initlog('guiConfigTestModeForm')

class ConfigTestModeForm(ConfigForm):
    
    def __init__(self):
        ConfigForm.__init__(self)
        self.screenID = 'C1'
        self.preWindowID = 'AdminMainForm'
        self.uiErrorWindowID = 'AdminMainForm'
        self.timeoutSec = 60
        self.lstResponseCtrl += [
            'ConfigTestModeForm_ctr_num_keyboard',
            'ConfigTestModeForm_ctr_message_box']

    
    def _initComponents(self):
        ConfigForm._initComponents(self)
        self._setTestMode()

    
    def _setTestMode(self):
        if globalSession.param['test_mode']:
            self._on_test_mode_on()
        else:
            self._on_test_mode_off()

    
    def _on_test_mode_on(self):
        self.flash.send('txt_status', 'setText', {
            'text': _('TEST MODE on') })
        self.flash.send('txt_message', 'setText', {
            'text': '' })
        msg = _('Would you like to turn OFF test mode?')
        self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
            'message': msg,
            'type': 'confirm' })
        self.flash.send('%s_ctr_num_keyboard' % self.windowID, 'close', { })

    
    def _on_test_mode_off(self):
        self.flash.send('txt_status', 'setText', {
            'text': _('TEST MODE off') })
        self.flash.send('txt_message', 'setText', {
            'text': _('Please input the password to turn ON test mode') })
        self.flash.send('%s_ctr_message_box' % self.windowID, 'close', { })
        self.flash.send('%s_ctr_num_keyboard' % self.windowID, 'show', {
            'type': 'password' })

    
    def on_btn_test_mode_off_event(self):
        self._on_test_mode_off()

    
    def on_btn_test_mode_on_event(self):
        self._on_test_mode_on()

    
    def on_ConfigTestModeForm_ctr_num_keyboard_event(self):
        eventType = self._getEventParam('ConfigTestModeForm_ctr_num_keyboard', 'type')
        if eventType == 'click':
            pass
        elif eventType == 'ok':
            inputVal = self._getEventParam('ConfigTestModeForm_ctr_num_keyboard', 'val')
            if inputVal == self.connProxy._getConfigByKey('show_mode_passcode'):
                self.connProxy.setTestMode()
                globalSession.param['test_mode'] = True
                self._setTestModeButton()
                self.flash.send('txt_status', 'setText', {
                    'text': _('TEST MODE on') })
                self.flash.send('txt_message', 'setText', {
                    'text': '' })
                self.flash.send('%s_ctr_message_box' % self.windowID, 'close', { })
                self.flash.send('%s_ctr_num_keyboard' % self.windowID, 'close', { })
            else:
                self.flash.send('txt_message', 'setText', {
                    'text': _('Invalid password') })
                self.flash.send('%s_ctr_num_keyboard' % self.windowID, 'show', {
                    'type': 'password' })
        

    
    def on_ConfigTestModeForm_ctr_message_box_event(self):
        inputVal = self._getEventParam('ConfigTestModeForm_ctr_message_box', 'val')
        if str(inputVal).lower() == 'yes':
            self.connProxy.setTestMode()
            globalSession.param['test_mode'] = False
            self._setTestModeButton()
            self.flash.send('txt_status', 'setText', {
                'text': _('TEST MODE off') })
            self.flash.send('txt_message', 'setText', {
                'text': '' })
            self.flash.send('%s_ctr_message_box' % self.windowID, 'close', { })
            self.flash.send('%s_ctr_num_keyboard' % self.windowID, 'close', { })
        


