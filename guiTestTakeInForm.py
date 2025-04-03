# Source Generated with Decompyle++
# File: guiTestTakeInForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V0.4
CopyRight MovieMate, Inc.

Created 2008-11-19 Vincent
vincent.chen@cereson.com

Filename:guiTestTakeInForm.py

Change Log:
    Vincent 2009-04-17

'''
from guiBaseTakeInForm import BaseTakeInForm
from mcommon import *
log = initlog('guiTestTakeInForm')

class TestTakeInForm(BaseTakeInForm):
    
    def __init__(self):
        BaseTakeInForm.__init__(self)
        self.nextWindowID = 'TestingForm'
        self.preWindowID = 'SuperAdminMainForm'
        self.screenID = 'KT2'
        self.resultForm = 'TestingForm'
        self.ejectDiscBackForm = 'TestMainForm'
        self.onUiErrorForm = 'MainForm'
        self.timeoutSec = 20
        self.disc = Disc()

    
    def _verifyDisc(self):
        pass

    
    def _saveStatus(self):
        pass

    
    def _retrieveFailRecovery(self, exin):
        raise exin

    
    def _insertFailRecovery(self, exin):
        raise exin

    
    def _setProcessText(self, msg):
        self.flash.send('txt_msg', 'setText', {
            'text': msg })

    
    def _initComponents(self):
        BaseTakeInForm._initComponents(self)

    
    def _run(self):
        self.disc.slotID = '101'
        
        try:
            BaseTakeInForm._run(self)
        except Exception as ex:
            
            try:
                ec = ex.errCode
            except:
                ec = '0'

            raise FatalError(ex.message, { }, ec)



