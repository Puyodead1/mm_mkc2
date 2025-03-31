# Source Generated with Decompyle++
# File: guiMembershipLoginSwipeCardForm.pyc (Python 2.5)

'''
Created on 2010-7-8
@author: andrew.lu@cereson.com
'''
from mcommon import *
from control import *
from guiRobotForm import RobotForm
log = initlog('MembershipLoginSwipeCardForm')

class MembershipLoginSwipeCardForm(RobotForm):
    
    def __init__(self):
        super(MembershipLoginSwipeCardForm, self).__init__()
        self.screenID = 'M1'
        self.nextWindowID = 'MembershipCenterForm'
        self.preWindowID = 'MainForm'
        self.uiErrorWindowID = 'MainForm'
        self.timeoutSec = 180
        self.lstResponseCtrl.extend([
            'MembershipLoginSwipeCardForm_ctr_message_box'])

    
    def _cancelAndBack(self):
        self.robot.cancel()
        if self.action == 'back':
            self.nextWindowID = self.preWindowID
        elif self.action == 'email':
            self.nextWindowID = 'MembershipLoginPasswordForm'
        else:
            self.nextWindowID = self.uiErrorWindowID

    
    def _initComponents(self):
        super(MembershipLoginSwipeCardForm, self)._initComponents()
        self.action = ''
        self.fail = False
        self.flash.send('txtbox_msg', 'setText', {
            'text': _('Please swipe Your Credit Card or MemberShip Card') })
        self.flash.send('swf_swipe_card', 'show', { })
        self.flash.send('%s_ctr_message_box' % self.windowID, 'close', { })

    
    def on_MembershipLoginSwipeCardForm_ctr_message_box_event(self):
        if self._getEventParam('MembershipLoginSwipeCardForm_ctr_message_box', 'val') == 'yes' and self.fail:
            self.on_back()
        

    
    def _checkMemberDetail(self):
        cart = ShoppingCart()
        (status, _) = self.umsProxy.setMemberDetail(self.customer, cart)
        if status in [
            '0',
            '1']:
            if self.customer.isMember:
                self.customer.isLogin = True
                globalSession.loginCustomer = self.customer
            else:
                msg = N_('This card is not registered.')
                raise InvalidMemberException(msg)
        elif status in [
            '2',
            '3']:
            msg = N_('Failed to get member information, please retry.')
            raise MemberException(msg)
        elif status == '4':
            msg = N_('CerePay card does NOT bind to any CerePay account.')
            raise InvalidMemberException(msg)
        elif status == '5':
            msg = N_('missing CerePay card.')
            raise InvalidMemberException(msg)
        elif status == '6':
            msg = N_('CerePay account has been suspended or frozen.')
            raise InvalidMemberException(msg)
        else:
            raise InvalidMemberException('unknown error.')

    
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
                
            self.flash.send('btn_cancel', 'show', { })
            self.flash.send('btn_back', 'show', { })
            self.flash.send('btn_email', 'show', { })
            
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
                            self.action = 'back'
                            break
                        elif cid == 'btn_back':
                            log.info('[%s] - Back Button Clicked.' % self.windowID)
                            retFromRobot = None
                            self.action = 'back'
                            break
                        elif cid == 'btn_email':
                            log.info('[%s] - Email Button Clicked.' % self.windowID)
                            retFromRobot = None
                            self.action = 'email'
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
                        msg = N_('Card reader time out, please retry.')
                        raise CardDeclinedException(msg)
                    else:
                        log.error('[%s] - Card reader unknown error:%s' % (self.windowID, errno))
                        msg = N_('Card reader fails, please retry.')
                        raise CardReadException(msg)
                    self.flash.send('btn_cancel', 'hide', { })
                    self.flash.send('btn_back', 'hide', { })
                    self.flash.send('btn_email', 'hide', { })
                    track1 = retFromRobot['track1']
                    track2 = retFromRobot['track2']
                    (ccNumber, ccName, ccExpDate) = parseTrack(track1, track2)
                    self.customer = Customer(ccName, ccNumber, ccExpDate, track2, track1)
                    tick = time.time()
                    self.flash.send('txtbox_msg', 'setText', {
                        'text': _('Authenticating ...') })
                    self._checkMemberDetail()
                    self.nextWindowID = 'MembershipCenterForm'
            except CardReadException as ex:
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': ex.i18nmsg,
                    'type': 'alert' })
            except MemberException as ex:
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': ex.i18nmsg,
                    'type': 'alert' })
            except CardDeclinedException as ex:
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': ex.i18nmsg,
                    'type': 'alert',
                    'height': '250' })
                self.fail = True
            except InvalidMemberException as ex:
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': ex.i18nmsg,
                    'type': 'alert' })
                self.fail = True
            except Exception as ex:
                raise 
            finally:
                self.flash.send('txtbox_msg', 'setText', {
                    'text': _('Please swipe Your Credit Card or MemberShip Card') })



