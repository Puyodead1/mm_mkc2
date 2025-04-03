# Source Generated with Decompyle++
# File: guiReturnResultForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiReturnResultForm.py
Return Result
Screen ID: T2

Change Log:

'''
import config
from mcommon import *
from guiBaseForms import UserForm
log = initlog('guiReturnResultForm')

class ReturnResultForm(UserForm):
    
    def __init__(self):
        super(ReturnResultForm, self).__init__()
        self.screenID = 'T2'
        self.timeoutSec = 60
        self.preWindowID = 'MainForm'
        self.lstResponseCtrl.extend([
            'btn_finish',
            'btn_another',
            'btn_returnagain'])

    
    def _initComponents(self):
        super(ReturnResultForm, self)._initComponents()
        msg = globalSession.param.get('return_msg')
        self.flash.send('txt_msg', 'setText', {
            'text': msg })
        self.flash.send('txt_msg', 'show', { })

    
    def on_btn_finish_event(self):
        self.nextWindowID = 'MainForm'
        self.windowJump = True

    
    def on_btn_another_event(self):
        self.nextWindowID = 'ReturnTakeInForm'
        self.windowJump = True

    
    def on_btn_returnagain_event(self):
        self.nextWindowID = 'RentMainForm'
        self.windowJump = True


