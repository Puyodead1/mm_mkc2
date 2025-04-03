# Source Generated with Decompyle++
# File: guiConfigOperatorCodeForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2009-06-10 Andrew
andrew.lu@cereson.com

Filename: guiConfigOperatorCodeForm.py
reset operator code
Screen ID: C2

Change Log:
    
'''
from mcommon import *
from guiBaseForms import ConfigForm
log = initlog('ConfigOperatorCodeForm')
(OK, AUTH_FAIL, CONFIRM_FAIL) = list(range(3))

class ConfigOperatorCodeForm(ConfigForm):
    
    def __init__(self):
        ConfigForm.__init__(self)
        self.screenID = 'C2'
        self.preWindowID = 'AdminMainForm'
        self.uiErrorWindowID = 'AdminMainForm'
        self.timeoutSec = 60
        self.lstResponseCtrl += [
            'btn_finish',
            'btn_retry',
            'ConfigOperatorCodeForm_ctr_all_keyboard']

    
    def _initComponents(self):
        ConfigForm._initComponents(self)
        self.success = OK
        self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'setType', {
            'type': 'password' })
        self._gotoStep(1)

    
    def _gotoStep(self, st):
        self.step = st
        if self.step == 1:
            msg = _('Please Input the Old Password')
            self.flash.send('swf_step1', 'show', { })
            self.flash.send('swf_step2', 'hide', { })
            self.flash.send('swf_step3', 'hide', { })
            self.flash.send('btn_finish', 'hide', { })
            self.flash.send('btn_retry', 'hide', { })
            self.flash.send('txt_msg', 'setText', {
                'text': msg })
            self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', { })
        elif self.step == 2:
            msg = _('Please Input the New Password')
            self.flash.send('swf_step1', 'hide', { })
            self.flash.send('swf_step2', 'show', { })
            self.flash.send('swf_step3', 'hide', { })
            self.flash.send('txt_msg', 'setText', {
                'text': msg })
            self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', { })
        elif self.step == 3:
            msg = _('Please Confirm the New Password')
            self.flash.send('swf_step1', 'hide', { })
            self.flash.send('swf_step2', 'hide', { })
            self.flash.send('swf_step3', 'show', { })
            self.flash.send('txt_msg', 'setText', {
                'text': msg })
            self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', { })
        elif self.step == 4:
            self.flash.send('swf_step1', 'hide', { })
            self.flash.send('swf_step2', 'hide', { })
            self.flash.send('swf_step3', 'hide', { })
            self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'hide', { })
            if self.success == OK:
                msg = _('The New Password has been updated')
                self.flash.send('txt_msg', 'setText', {
                    'text': msg })
                self.flash.send('btn_finish', 'show', { })
                self.flash.send('btn_retry', 'hide', { })
            elif self.success == AUTH_FAIL:
                msg = _('Password Authentication failed')
                self.flash.send('txt_msg', 'setText', {
                    'text': msg })
                self.flash.send('btn_finish', 'hide', { })
                self.flash.send('btn_retry', 'show', { })
            elif self.success == CONFIRM_FAIL:
                msg = _('The New Password input error')
                self.flash.send('txt_msg', 'setText', {
                    'text': msg })
                self.flash.send('btn_finish', 'hide', { })
                self.flash.send('btn_retry', 'show', { })
            
        

    
    def on_btn_finish_event(self):
        self.nextWindowID = 'AdminMainForm'
        self.windowJump = True

    
    def on_btn_retry_event(self):
        self._initComponents()

    
    def on_ConfigOperatorCodeForm_ctr_all_keyboard_event(self):
        eventType = self._getEventParam('ConfigOperatorCodeForm_ctr_all_keyboard', 'type')
        if eventType == 'click':
            pass
        elif eventType == 'ok':
            inputVal = self._getEventParam('ConfigOperatorCodeForm_ctr_all_keyboard', 'val')
            if self.step == 1:
                if inputVal == self.connProxy._getConfigByKey('operator_code'):
                    self._gotoStep(2)
                else:
                    self.success = AUTH_FAIL
                    self._gotoStep(4)
            elif self.step == 2:
                self.newCode = inputVal
                self._gotoStep(3)
            elif self.step == 3:
                if inputVal == self.newCode:
                    self.success = OK
                    self.connProxy.setConfig({
                        'operator_code': self.newCode })
                else:
                    self.success = CONFIRM_FAIL
                self._gotoStep(4)
            
        


