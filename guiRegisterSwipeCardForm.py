# Source Generated with Decompyle++
# File: guiRegisterSwipeCardForm.pyc (Python 2.5)

'''
Created on 2010-11-25
@author: andrew.lu@cereson.com
'''
from mcommon import *
from control import *
from guiRobotForm import RobotForm
log = initlog('RegisterSwipeCardForm')

class RegisterSwipeCardForm(RobotForm):
    
    def __init__(self):
        RobotForm.__init__(self)
        self.nextWindowID = 'RegisterMainForm'
        self.preWindowID = 'MainForm'
        self.screenID = 'M9'
        self.timeoutSec = 60
        self.lstResponseCtrl.extend([
            'RegisterSwipeCardForm_ctr_message_box'])

    
    def _cancel(self):
        self.robot.cancel()
        if self.action == 'back':
            self.nextWindowID = self.preWindowID
        else:
            self.nextWindowID = self.uiErrorWindowID

    
    def _initComponents(self):
        RobotForm._initComponents(self)
        self.action = ''
        self.fail = False
        self.flash.send('swf_swipe_card', 'show', { })
        self.flash.send('btn_cancel', 'show', { })
        self.flash.send('btn_back', 'show', { })
        self.flash.send('%s_ctr_message_box' % self.windowID, 'close', { })
        self.flash.send('txtbox_msg', 'setText', {
            'text': _('Please swipe your membership card') })

    
    def _checkCerepayCard(self):
        (status, _) = self.umsProxy.getCardInfoForCerePay(self.customer)
        log.info('getCardInfoForCerePay return %d' % status)
        if status == 0:
            pass
        elif status == 2:
            msg = N_('Sorry, the kiosk has communication issue, Please retry.')
            raise CardDeclinedException(msg)
        elif status in (3, 4):
            msg = N_('Invalid membership card, please contact with the card offers.')
            raise CardDeclinedException(msg)
        elif status == 5:
            msg = N_('This card is not a membership card.')
            raise CardDeclinedException(msg)
        elif status == 6:
            msg = N_('This card is reported missing.')
            raise CardDeclinedException(msg)
        elif status == 7:
            msg = N_('This card is registered.')
            raise CardDeclinedException(msg)
        else:
            msg = N_('unknown error.')
            raise CardDeclinedException(msg)

    
    def on_RegisterSwipeCardForm_ctr_message_box_event(self):
        if self._getEventParam('RegisterSwipeCardForm_ctr_message_box', 'val') == 'yes' and self.fail:
            self.on_back()
        

    
    def _run(self):
        while True:
            while self.fail == True:
                self.event = self.flash.get(timeout = self.timeoutSec)
                if self.event == None:
                    continue
                
                if self.event:
                    log.info('[UI Event]: %s.' % self.event)
                
                ctrlID = self.event.get('cid')
                self.on_event(ctrlID)
                if self.windowJump:
                    return None
                
            
            try:
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
                        cid = eventFromFlash.get('cid')
                        if cid == 'btn_cancel':
                            log.info('[%s] - Cancel Button Clicked.' % self.windowID)
                            retFromRobot = None
                            self.action = 'cancel'
                            break
                        elif cid == 'btn_back':
                            log.info('[%s] - Back Button Clicked.' % self.windowID)
                            retFromRobot = None
                            self.action = 'back'
                            break
                        else:
                            log.info('[UI Event]: %s.' % eventFromFlash)
                            log.info('[%s] - Unknown Clicked.' % self.windowID)
                    
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
                        msg = N_('Card reader time out, please retry.')
                        raise CardDeclinedException(msg)
                    else:
                        log.error('[%s] - Card reader unknown error:%s' % (self.windowID, errno))
                        msg = N_('Card reader fails, please retry.')
                        raise CardReadException(msg)
                    self.flash.send('btn_cancel', 'hide', { })
                    self.flash.send('btn_back', 'hide', { })
                    track1 = retFromRobot['track1']
                    track2 = retFromRobot['track2']
                    (ccNumber, ccName, ccExpDate) = parseTrack(track1, track2)
                    self.customer = Customer(ccName, ccNumber, ccExpDate, track2, track1)
                    globalSession.customer = self.customer
                    self._checkCerepayCard()
                    self.nextWindowID = 'RegisterMainForm'
            except CardReadException:
                ex = None
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': ex.i18nmsg,
                    'type': 'alert' })
            except CardDeclinedException:
                ex = None
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': ex.i18nmsg,
                    'type': 'alert',
                    'height': '250' })
                self.fail = True
            except Exception:
                ex = None
                raise 
            finally:
                self.flash.send('txtbox_msg', 'setText', {
                    'text': _('Please swipe your membership card') })



