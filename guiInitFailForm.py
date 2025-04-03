# Source Generated with Decompyle++
# File: guiInitFailForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2009-07-02 Andrew
andrew.lu@cereson.com

Filename: guiInitFailForm.py
InitMachine Fail From
Screen ID: F2

Change Log:
    
'''
from mcommon import *
from guiBaseForms import UserForm
log = initlog('guiInitFailForm')

class InitFailForm(UserForm):
    
    def __init__(self):
        UserForm.__init__(self)
        self.screenID = 'F2'
        self.timeoutSec = 0

    
    def _initComponents(self):
        self.sync_inactive_information('init error')
        UserForm._initComponents(self)
        msg = 'Kiosk init failed.<br>POWER OFF THE KIOSK. Make sure you unscrew the SIX locking-screws inside the kiosk before power on.'
        self.connProxy.emailAlert('PRIVATE', msg, critical = self.connProxy.UNCRITICAL)

    
    def on_timeout(self):
        pass


