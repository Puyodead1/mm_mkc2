# Source Generated with Decompyle++
# File: guiPickUpSwipeCardForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V0.4
CopyRight MovieMate, Inc.

Created 2008-11-19 Vincent
vincent.chen@cereson.com

Filename:guiPickUpSwipeCardForm.py

Change Log:

'''
from guiRobotForm import RobotForm
from mcommon import *
from control import *
log = initlog('guiPickUpSwipeCardForm')

class PickUpSwipeCardForm(RobotForm):
    
    def __init__(self):
        RobotForm.__init__(self)
        self.nextWindowID = 'PickUpDiscListForm'
        self.preWindowID = 'PickUpCodeForm'
        self.screenID = 'P1'
        self.uiErrorWindowID = 'MainForm'
        self.timeoutSec = 60

    
    def dbSync(self):
        self.connProxy.dbSyncCheckOut(self.shoppingCart)

    
    def _cancelAndBack(self):
        self.robot.cancel()
        if self.action == 'back':
            self.nextWindowID = self.preWindowID
        else:
            self.nextWindowID = self.uiErrorWindowID

    
    def _initComponents(self):
        RobotForm._initComponents(self)
        self.action = ''
        self.flash.send('swf_swipe_card', 'show', { })
        self.flash.send('%s_ctr_message_box' % self.windowID, 'close', { })

    
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
                
                eventFromFlash = self.flash.get(self.windowID, 0.1)
                if eventFromFlash:
                    ctrlID = eventFromFlash.get('cid')
                    if ctrlID == 'btn_cancel':
                        log.info('[%s] - Cancel Button Clicked.' % self.windowID)
                        self.action = 'cancel'
                    elif ctrlID == 'btn_back':
                        log.info('[%s] - Back Button Clicked.' % self.windowID)
                        self.action = 'back'
                    elif ctrlID == '%s_ctr_message_box' % self.windowID:
                        pass
                    
                    retFromRobot = None
                    break
                
            if not retFromRobot:
                self._cancelAndBack()
                break
            else:
                self._verifyRet(retFromRobot)
                errno = retFromRobot['errno']
                self.connProxy.saveCardRead(str(errno))
                if errno == ROBOT_OK:
                    pass
                elif errno == ROBOT_TIMEOUT:
                    log.error('[%s] - Card reader time out' % self.windowID)
                else:
                    log.error('[%s] - Card reader unknown error:%s' % (self.windowID, errno))
                    msg = _('Card reader fails, please retry.')
                    self.flash.send('txtbox_msg', 'setText', {
                        'text': msg })
                track1 = retFromRobot['track1']
                track2 = retFromRobot['track2']
                (ccNumber, ccName, ccExpDate) = parseTrack(track1, track2)
                customer = Customer(ccName, ccNumber, ccExpDate, track2)
                shoppingCart = ShoppingCart()
                self.connProxy.getPickUpList(shoppingCart, customer)
                log.info('[Pick Up List]: %s disc(s)' % shoppingCart.getSize())
                if shoppingCart.discs:
                    globalSession.customer = customer
                    globalSession.pickupCart = shoppingCart
                    self.nextWindowID = 'PickUpDiscListForm'
                    break
                else:
                    msg = _('Sorry, no discs have been reserved by this credit card.')
                    self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                        'message': msg,
                        'type': 'alert' })


