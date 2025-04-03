# Source Generated with Decompyle++
# File: guiFatalErrorForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiFatalErrorForm.py
Fatal Error From
Screen ID: F1

Change Log:
    2009-05-15 Andrew some error can not recover
    2009-05-06 Andrew "recoverme" will jump to RecoverTakeInForm
'''
import base64
import control
from mcommon import *
from guiBaseForms import UserForm
from proxy.tools import unlock
log = initlog('guiFatalErrorForm')

class FatalErrorForm(UserForm):
    
    def __init__(self):
        UserForm.__init__(self)
        self.screenID = 'F1'
        self.timeoutSec = None
        self.lstResponseCtrl.extend([
            'btn_icon_keyboard',
            'FatalErrorForm_ctr_all_keyboard'])

    
    def _initComponents(self):
        UserForm._initComponents(self)
        unlock()
        self.sync_inactive_information('fatal error')
        msg = str(self.connProxy._getConfigByKey('error_message'))
        self.flash.send('txtbox_msg', 'setText', {
            'text': base64.b64decode(msg) })
        errcode = globalSession.error.errCode
        msg = '%(errcode)s:\n%(msg)s' % {
            'errcode': errcode,
            'msg': globalSession.error.i18nmsg }
        techSupportContact = _('Please contact: ') + str(self.connProxy._getConfigByKey('tech_support_contact'))
        self.flash.send('txtbox_tech_support', 'setText', {
            'text': techSupportContact })
        msg = '%(msg)s' % {
            'msg': globalSession.error.message }
        
        try:
            i = errcode.index('R')
            code = int(errcode[i + 1:])
            if code == control.ROBOT_CARRIAGE_JAM:
                (rerr, rmsg) = initRobot()
                if rerr != control.ROBOT_OK:
                    msg += '\nInitMachine return:\n%s' % rmsg
                
        except:
            pass

        self.connProxy.emailAlert('PUBLIC', msg, critical = self.connProxy.CRITICAL)
        if globalSession.error.recover == True:
            self.flash.send('btn_icon_keyboard', 'show', { })
        else:
            self.flash.send('btn_icon_keyboard', 'hide', { })

    
    def on_btn_icon_keyboard_event(self):
        self.flash.send('FatalErrorForm_ctr_all_keyboard', 'show', { })

    
    def on_FatalErrorForm_ctr_all_keyboard_event(self):
        eventType = self._getEventParam('FatalErrorForm_ctr_all_keyboard', 'type')
        if eventType == 'click':
            pass
        elif eventType == 'ok':
            passcode = self._getEventParam('FatalErrorForm_ctr_all_keyboard', 'val')
            recoverPassCode = 'recoverme'
            restartPassCode = 'restartme'
            if passcode.lower() == recoverPassCode:
                self.nextWindowID = 'RecoverTakeInForm'
                self.windowJump = True
                sync_active_information(self.connProxy, 'kiosk recoverme')
            
            if passcode.lower() == 'log':
                errcode = globalSession.error.errCode
                msg = '%(errcode)s:\n%(msg)s' % {
                    'errcode': errcode,
                    'msg': globalSession.error.i18nmsg }
                self.flash.send('txtbox_msg', 'setText', {
                    'text': msg })
            
        

    
    def on_timeout(self):
        pass


