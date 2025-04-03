# Source Generated with Decompyle++
# File: guiTestMainForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiTestMainForm.py
Admin Main Form
Screen ID: KT1

Change Log:

'''
import traceback
import config
from mcommon import *
from guiBaseForms import UserForm
log = initlog('guiTestMainForm')

class TestMainForm(UserForm):
    
    def __init__(self):
        UserForm.__init__(self)
        self.screenID = 'KT1'
        self.timeoutSec = 60
        self.lstResponseCtrl = [
            'btn_yes',
            'btn_no']

    
    def _initComponents(self):
        UserForm._initComponents(self)

    
    def on_btn_yes_event(self):
        self.nextWindowID = 'TestTakeInForm'
        self.windowJump = True

    
    def on_btn_no_event(self):
        self.connProxy.setConfig({
            'run_test': 'no' })
        self.nextWindowID = 'MainForm'
        self.windowJump = True

    
    def on_timeout(self):
        self.connProxy.setConfig({
            'run_test': 'no' })
        self.nextWindowID = 'MainForm'
        self.windowJump = True


