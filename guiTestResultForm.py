# Source Generated with Decompyle++
# File: guiTestResultForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiTestResultForm.py
Testing Result
Screen ID: KT4

Change Log:

'''
import traceback
import config
from control import *
from mcommon import *
from guiRobotForm import RobotForm
log = initlog('guiTestResultForm')

class TestResultForm(RobotForm):
    
    def __init__(self):
        RobotForm.__init__(self)
        self.screenID = 'KT4'
        self.timeoutSec = 0
        self.nextWindowID = 'MainForm'
        self.preWindowID = 'TestMainForm'

    
    def _initComponents(self):
        RobotForm._initComponents(self)
        self.flash.send('btn_finish', 'show', { })

    
    def _ejectDisc(self):
        ret = self.robot.doCmdSync('exchange_eject', { }, timeout = 10)
        self._verifyRet(ret)
        errno = ret['errno']
        if errno == ROBOT_OK:
            pass
        elif errno == ROBOT_TIMEOUT:
            displayErrCode = self.screenID + '-02R' + str(errno)
            msg = _('Error: Robot Timeout.')
            raise FatalError(msg, displayErrCode)
        

    
    def _run(self):
        while True:
            self.event = self.flash.get()
            ctrlID = self.event.get('cid')
            log.info('[UI Event]: %s.' % self.event)
            if ctrlID == 'btn_finish':
                self.flash.send('btn_finish', 'hide', { })
                self._ejectDisc()
                self.connProxy.setConfig({
                    'run_test': 'no' })
                self.nextWindowID = 'MainForm'
                break
            


