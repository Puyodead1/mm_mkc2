# Source Generated with Decompyle++
# File: guiUnloadResultForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiUnloadResultForm.py
Load Result
Screen ID: L6

Change Log:

'''
import config
from mcommon import *
from guiBaseForms import UserForm
log = initlog('guiUnloadResultForm')

class UnloadResultForm(UserForm):
    
    def __init__(self):
        UserForm.__init__(self)
        self.screenID = 'U5'
        self.timeoutSec = 60
        self.preWindowID = 'AdminMainForm'
        self.uiErrorWindowID = 'AdminMainForm'
        self.lstResponseCtrl = [
            'btn_logout',
            'btn_another',
            'btn_finish']

    
    def _initComponents(self):
        UserForm._initComponents(self)
        msg = _('The disc(s) has been unloaded.')
        if globalSession.param.get('eject_result'):
            msg = globalSession.param.get('eject_result')
        
        self.flash.send('txtbox_msg', 'setText', {
            'text': msg })

    
    def on_btn_logout_event(self):
        self.on_exit()

    
    def on_btn_finish_event(self):
        self.nextWindowID = 'AdminMainForm'
        self.windowJump = True

    
    def on_btn_another_event(self):
        self.nextWindowID = globalSession.param.get('unload_entry_form')
        self.windowJump = True


