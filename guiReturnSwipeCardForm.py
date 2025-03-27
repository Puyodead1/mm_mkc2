# Source Generated with Decompyle++
# File: guiReturnSwipeCardForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V0.4
CopyRight MovieMate, Inc.

Created 2009-04-08 Vincent
vincent.chen@cereson.com

Filename:guiReturnSwipeCardForm.py

Change Log:

'''
import time
from guiRobotForm import RobotForm
from mcommon import *
from control import *
log = initlog('guiReturnSwipeCardForm')

class ReturnSwipeCardForm(RobotForm):
    
    def __init__(self):
        RobotForm.__init__(self)
        self.nextWindowID = 'ReturnTakeInForm'
        self.preWindowID = 'ReturnOptionForm'
        self.screenID = 'T31'
        self.timeoutSec = 60

    
    def _cancel(self):
        self.robot.cancel()
        self.nextWindowID = self.preWindowID

    
    def _initComponents(self):
        RobotForm._initComponents(self)
        self.flash.send('%s_ctr_message_box' % self.windowID, 'hide', { })

    
    def _run(self):
        while True:
            tick = time.time()
            r = self.robot.doCmdAsync('read_card', { }, self.timeoutSec)
            retFromRobot = None
            while time.time() - tick < self.timeoutSec:
                retFromRobot = self.robot.getResult(r)
                if retFromRobot:
                    log.info('[Robot Event]: %s' % logTrack(retFromRobot))
                    break
                
                eventFromFlash = self.flash.get(timeout = 0.1)
                if eventFromFlash:
                    if eventFromFlash.get('cid') == 'btn_cancel':
                        log.info('[%s] - Cancel Button Clicked.' % self.windowID)
                        retFromRobot = None
                        break
                    
                
            if not retFromRobot:
                self._cancel()
                break
            else:
                self._verifyRet(retFromRobot)
                errno = retFromRobot['errno']
                self.connProxy.saveCardRead(str(errno))
                if errno == ROBOT_OK:
                    pass
                elif errno == ROBOT_TIMEOUT:
                    log.error('[%s] - Card reader time out' % self.windowID)
                    msg = _('Card reader time out, please retry.')
                    self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                        'message': msg,
                        'type': 'alert' })
                else:
                    log.error('[%s] - Card reader unknown error:%s' % (self.windowID, errno))
                    msg = _('Card reader fails, please retry.')
                    self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                        'message': msg,
                        'type': 'alert' })
                track1 = retFromRobot['track1']
                track2 = retFromRobot['track2']
                (ccNumber, ccName, ccExpDate) = parseTrack(track1, track2)
                self.customer = Customer(ccName, ccNumber, ccExpDate, track2, track1)
                lstDiscs = self.connProxy.getOutDiscsByCcId(self.customer.ccid)
                if len(lstDiscs) == 0:
                    msg = _('No discs found rented by this card.')
                    self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                        'message': msg,
                        'type': 'alert' })
                elif len(lstDiscs) == 1:
                    globalSession.disc = lstDiscs[0]
                    self.nextWindowID = 'ReturnTakeInForm'
                    globalSession.param['return_option'] = 'card'
                    break
                else:
                    globalSession.param['disc_list'] = lstDiscs
                    self.nextWindowID = 'ReturnDiscListForm'
                    break


