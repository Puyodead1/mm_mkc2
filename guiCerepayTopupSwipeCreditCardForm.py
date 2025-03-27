# Source Generated with Decompyle++
# File: guiCerepayTopupSwipeCreditCardForm.pyc (Python 2.5)

from guiCerepayTopupSwipeCardBaseForm import *
from guiCerepayTopupSwipeCardBaseForm import _object2dict, _topup_status_dict
from mcommon import *
from control import *
from proxy.upg_proxy import UPGProxy
log = initlog('CerepayTopupSwipeCreditCardForm')

class CerepayTopupSwipeCreditCardForm(CerepayTopupSwipeCardBaseForm):
    
    def __init__(self):
        super(CerepayTopupSwipeCreditCardForm, self).__init__()
        robot = Robot()
        self.timeoutSec = 60
        self.robot = robot.getInstance()
        self.screenID = 'M9'
        self.action = ''
        self._CerepayTopupSwipeCreditCardForm__upg_proxy = UPGProxy()
        self.fail = False

    
    def _verifyRet(self, ret):
        errCode = self.screenID + '-00R9000'
        if type(ret) != type({ }):
            log.error('Invalid type of ret, type: %s, ret: %s.' % (type(ret), ret))
            msg = N_('Invalid Response of Robot, Please Restart the Kiosk and Retry.')
            km = KioskMessage(msg, { })
            raise FatalError(msg, { }, errCode)
        
        if 'errno' not in ret:
            log.error("Invalid value of ret, no 'errno' key found, ret: %s." % ret)
            msg = N_('Invalid Response of Robot, Please Restart the Kiosk and Retry.')
            km = KioskMessage(msg, { })
            raise FatalError(msg, { }, errCode)
        

    
    def __read_card(self):
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
                
            self.flash.send('ctr_btn_center', 'setDisabled', {
                'disabled': 'false' })
            
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
                        elif cid == 'ctr_btn_center':
                            cmd = eventFromFlash.get('param_info').get('cmd')
                            if cmd == 'logout':
                                log.info('[%s] - Logout Clicked.' % self.windowID)
                                self.action = 'logout'
                            else:
                                log.info('[%s] - Membership Clicked.' % self.windowID)
                                self.action = 'login'
                            retFromRobot = None
                            break
                        elif cid == 'btn_no_card':
                            log.info('[%s] - No Card Button Clicked.' % self.windowID)
                            retFromRobot = None
                            self.action = 'no_card'
                            break
                        elif cid == 'btn_back':
                            retFromRobot = None
                            self.action = 'back'
                            break
                        else:
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
                    self.flash.send('btn_no_card', 'hide', { })
                    self.flash.send('ctr_btn_center', 'setDisabled', {
                        'disabled': 'true' })
                    track1 = retFromRobot['track1']
                    track2 = retFromRobot['track2']
                    (ccNumber, ccName, ccExpDate) = parseTrack(track1, track2)
                    return Customer(ccName, ccNumber, ccExpDate, track2, track1)
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
            except InvalidCouponException:
                ex = None
                textlen = 333 + len(invalidUserCoupons) * 38
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': ex.i18nmsg,
                    'type': 'alert',
                    'height': str(textlen) })
                self.fail = True
            except InvalidMemberException:
                ex = None
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': ex.i18nmsg,
                    'type': 'alert' })
                self.fail = True
            except ValidateCouponException:
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
                    'text': _('Please swipe Your Credit Card or MemberShip Card') })


    
    def _topup_cerepay_card(self):
        log.info('entering topup_cerepay_card_from_chin_pin')
        credit_card = self._CerepayTopupSwipeCreditCardForm__read_card()
        cerepay_customer = Customer(ccNumber = globalSession.loginCustomer.cerepayCard.number)
        log.info('Credit Card Number : ' + str(cerepay_customer.ccNum))
        log.info('Topup amount is : ' + str(globalSession.cerepayTopupAmount))
        log.info('Cerepay customer is : ' + str(_object2dict(cerepay_customer)))
        (status, msg, trs_uuid, queue_id) = self._CerepayTopupSwipeCreditCardForm__upg_proxy.topup_for_cerepay(chargeCustomer = credit_card, cerepayCustomer = cerepay_customer, amount = globalSession.cerepayTopupAmount)
        log.info('topup_for_cerepay return value is : (%s,%s,%s,%s)' % (status, msg, trs_uuid, queue_id))
        if str(status) != '0':
            raise ChinPinTopupException(N_(msg))
        elif trs_uuid:
            globalSession.cerepayTopupTransactionUUID = trs_uuid
        else:
            globalSession.cerepayTopupQueueID = queue_id
            raise CerepayError

    
    def on_CerepayTopupSwipeCreditCardForm_ctr_message_box_event(self):
        if self._getEventParam(self._ctr_msg_box_string, 'val') == 'yes':
            self.on_back()
        


