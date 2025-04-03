# Source Generated with Decompyle++
# File: guiCheckOutSwipeCardForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V0.4
CopyRight MovieMate, Inc.

Created 2008-11-19 Vincent
vincent.chen@cereson.com

Filename:guiCheckOutSwipeCardForm.py

Change Log:
    Vincent 2009-04-02 Increase the height of message box
    Vincent 2009-03-30 For #1625 join bug
    Vincent 2009-03-05 For Max dvd out and buy limit
    Kitch 2011-04-07 Add card name for cerepay card

'''
import datetime
import time
from guiRobotForm import RobotForm
from mcommon import *
from control import *
from proxy.upg_proxy import UPGProxy
from proxy.ums_proxy import UmsProxy
from proxy.tools import fmtMoney, checkDNS
log = initlog('CheckOutSwipeCard')

class CheckOutSwipeCardForm(RobotForm):
    
    def __init__(self):
        RobotForm.__init__(self)
        self.nextWindowID = 'CheckOutEjectForm'
        self.preWindowID = 'ShoppingCartForm'
        self.screenID = 'R7'
        self.timeoutSec = 60
        self.lstResponseCtrl.extend([
            'CheckOutSwipeCardForm_ctr_message_box',
            'CheckOutSwipeCardForm_ctr_all_keyboard'])

    
    def _cancel(self):
        self.robot.cancel()
        if self.action == 'back':
            self.nextWindowID = self.preWindowID
        elif self.action == 'cancel':
            if globalSession.loginCustomer.isLogin:
                globalSession.param['preWindowID'] = self.windowID
                self.nextWindowID = 'MembershipLogoutForm'
            else:
                self.nextWindowID = self.uiErrorWindowID
        elif self.action == 'login':
            self.nextWindowID = 'MembershipCenterForm'
        elif self.action == 'logout':
            globalSession.param['preWindowID'] = self.windowID
            self.nextWindowID = 'MembershipLogoutForm'
        elif self.action == 'no_card':
            self.nextWindowID = 'CheckOutWithoutCerepayCardForm'
        else:
            self.nextWindowID = self.uiErrorWindowID

    
    def _chargeCard(self):
        (status, proxyMsg) = self.upgProxy.preauthCard(self.customer, globalSession.shoppingCart, self.zipcode, self.password)
        if self.customer.cardType == 3:
            cerepayConfig = self.upgProxy.getCerePayCfg()
            userInfo = self.upgProxy.getCerePayUserInfo(cerepayConfig['MERCHANTID'], cerepayConfig['PASSWORD'], cerepayConfig['CURRENCY'], self.customer.ccNum)
            ccDisplay = userInfo.get('name', '')
            if not ccDisplay or str(ccDisplay).lower() == 'none':
                ccDisplay = 'CEREPAY CARD'
            
            ccDisplay += ' (%s)' % str(self.customer.ccNum[-4:])
            self.customer.ccDisplay = ccDisplay
        
        log.info('[UPG Charge Card]: %s %s' % (status, proxyMsg))
        if status == '0':
            pass
        elif status == '12':
            msg = _('Monthly subscription activated, please return these discs before %(time)s.')
            tt = datetime.datetime(*time.strptime(proxyMsg, '%Y-%m-%d %H:%M:%S')[:6]).strftime('%H:00 on %b %d, %Y')
            pm = {
                'time': tt }
            globalSession.param['month_subs'] = msg % pm
        elif status == '1':
            msg = N_('Card Declined, message from the bank:\n%(info)s')
            pm = {
                'info': proxyMsg }
            raise CardDeclinedException(msg, pm)
        elif status == '2':
            msg = N_('Sorry, credit card expire in 15 days is not accepted.')
            raise CardDeclinedException(msg)
        elif status == '3':
            msg = N_('Sorry, this card is in black list.')
            raise CardDeclinedException(msg)
        elif status == '4':
            msg = N_('<b>- CREDIT CARD PROCESSING OFFLINE -</b><br/>Credit card processing is currently offline, please try again later.')
            raise CardDeclinedException(msg)
        elif status == '5':
            msg = N_('Sorry, UPG account has NOT been set.')
            raise CardDeclinedException(msg)
        elif status == '7':
            msg = N_('Sorry, credit card has expired.')
            raise CardDeclinedException(msg)
        elif status == '8':
            msg = N_('%(info)s')
            pm = {
                'info': proxyMsg }
            raise CardDeclinedException(msg, pm)
        elif status == '9':
            msg = N_('Card read failed, please try again.')
            raise CardReadException(msg)
        elif status == '10':
            msg = N_('Declined: Outstanding payment for previous rental needed.')
            raise CardDeclinedException(msg)
        elif status == '11':
            count = proxyMsg.split('|')
            msg = N_('Max discs exceeded for your monthly subscription, please remove at least %(del_num)s discs from your shopping cart and retry.')
            pm = {
                'del_num': int(count[0]) - int(count[1]) }
            raise CardDeclinedException(msg, pm)
        elif status == '13':
            msg = N_('The monthly subscription does not support sale discs, please remove sale discs from your shopping cart and retry.')
            raise CardDeclinedException(msg)
        elif status == '14':
            data = proxyMsg.split('|')
            msg = N_('Only %(type2)s disc(s) can apply to your monthly subscription plan, but %(type1)s disc(s) found in your shopping cart. Please remove it/them and retry.')
            pm = {
                'type1': data[0],
                'type2': data[1] }
            raise CardDeclinedException(msg, pm)
        else:
            msg = N_('<b>- CREDIT CARD PROCESSING OFFLINE -</b><br/>Credit card processing is currently offline, please try again later.')
            raise CardDeclinedException(msg)

    
    def _checkMemberDetail(self):
        (status, disclist) = self.umsProxy.setMemberDetail(self.customer, globalSession.shoppingCart)
        if status == '0':
            pass
        elif status == '1':
            msg = _('R rating disc(s) found. Under 17 requires accompanying parent or adult guardian. Are you sure you want to rent/buy?')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'confirm' })
            while True:
                self.event = self.flash.get(timeout = self.timeoutSec)
                if self.event == None:
                    continue
                
                if self.event:
                    log.info('[UI Event]: %s.' % self.event)
                
                ctrlID = self.event.get('cid')
                if ctrlID == 'CheckOutSwipeCardForm_ctr_message_box':
                    if self._getEventParam('CheckOutSwipeCardForm_ctr_message_box', 'val') != 'yes':
                        self.connProxy.removeDiscsFromShoppingCart(disclist)
                        for disc in disclist:
                            globalSession.shoppingCart.removeDisc(disc)
                        
                        msg = N_('R rating disc(s) found. They have been removed from your shopping cart. Please Check Out again.')
                        log.info(msg)
                        raise InvalidMemberException(msg)
                    else:
                        break
                elif ctrlID is None:
                    return False
                
        else:
            msg = N_('<b>- MEMBERSHIP SERVICE OFFLINE -</b><br/>Membership Services are currently offline, if you are subscribed to the monthly membership plan you will be charged for this rental.')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'continue' })
            while True:
                self.event = self.flash.get(timeout = self.timeoutSec)
                if self.event == None:
                    continue
                
                if self.event:
                    log.info('[UI Event]: %s.' % self.event)
                
                ctrlID = self.event.get('cid')
                if ctrlID == 'CheckOutSwipeCardForm_ctr_message_box':
                    if self._getEventParam('CheckOutSwipeCardForm_ctr_message_box', 'val') != 'yes':
                        return False
                    else:
                        break
                
        return True

    
    def _initComponents(self):
        RobotForm._initComponents(self)
        if globalSession.loginCustomer.isLogin:
            self.flash.send('ctr_btn_center', 'show', { })
            if globalSession.loginCustomer.gender == 'male':
                msg = _('Hello Mr. ')
            else:
                msg = _('Hello Ms. ')
            self.flash.send('ctr_btn_center', 'setText', {
                'text': msg + globalSession.loginCustomer.lastName })
            self.flash.send('btn_no_card', 'show', { })
        else:
            self.flash.send('ctr_btn_center', 'hide', { })
            self.flash.send('btn_no_card', 'hide', { })
        self.action = ''
        self.fail = False
        self.zipcode = None
        self.flash.send('swf_swipe_card', 'show', { })
        self.flash.send('btn_cancel', 'show', { })
        self.flash.send('txtbox_msg', 'setText', {
            'text': _('Please swipe Your Credit Card or MemberShip Card') })
        self.shoppingCart = globalSession.shoppingCart
        self.upgProxy = UPGProxy()
        self.umsProxy = UmsProxy()
        if globalSession.param.get('test_mode'):
            self.flash.send('txt_flag1', 'show', { })
            self.flash.send('txt_flag2', 'show', { })
            self.flash.send('txt_flag3', 'show', { })
            self.flash.send('txt_flag4', 'show', { })
        else:
            self.flash.send('txt_flag1', 'hide', { })
            self.flash.send('txt_flag2', 'hide', { })
            self.flash.send('txt_flag3', 'hide', { })
            self.flash.send('txt_flag4', 'hide', { })
        self.flash.send('%s_ctr_message_box' % self.windowID, 'close', { })
        self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'hide', { })
        self.flash.send('%s_ctr_num_keyboard' % self.windowID, 'hide', { })
        deposit_txt = ''
        if self.upgProxy._getConfigByKey('show_deposit_amount') == 'yes':
            deposit_amount = 0
            for disc in self.shoppingCart.discs:
                deposit_amount += float(disc.preauthAmount)
            
            deposit_amount = fmtMoney(deposit_amount)
            deposit_txt = _('Deposit Amount: %(cur_symbol)s %(amount)s (The actual amount might be less if you are a member)')
            deposit_txt = deposit_txt % {
                'cur_symbol': self.connProxy.getDefaultCurrencySymbol(),
                'amount': deposit_amount }
        
        self.flash.send('txt_deposit_amount_label', 'setText', {
            'text': deposit_txt })

    
    def on_CheckOutSwipeCardForm_ctr_message_box_event(self):
        if self._getEventParam('CheckOutSwipeCardForm_ctr_message_box', 'val') == 'yes' and self.fail:
            self.on_back()
        

    
    def _getZipcode(self):
        self.flash.send('txtbox_msg', 'setText', {
            'text': _('Please Input Zipcode') })
        self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', { })
        while True:
            self.event = self.flash.get(timeout = self.timeoutSec)
            if self.event == None:
                continue
            
            if self.event:
                log.info('[UI Event]: %s.' % self.event)
            
            ctrlID = self.event.get('cid')
            if ctrlID == 'CheckOutSwipeCardForm_ctr_all_keyboard':
                eventType = self._getEventParam('CheckOutSwipeCardForm_ctr_all_keyboard', 'type')
                if eventType == 'ok':
                    self.zipcode = self._getEventParam('CheckOutSwipeCardForm_ctr_all_keyboard', 'val')
                    return True
                elif eventType == 'close':
                    return False
                
            elif ctrlID is None:
                return False
            

    
    def _checkTrsPassword(self):
        self.password = None
        ret = self.upgProxy.chkNeedTrsPasswd(self.customer)
        log.info('chkNeedTrsPasswd return %s' % ret)
        if ret == 1:
            return True
        elif ret == 2:
            msg = N_('<b>- CREDIT CARD PROCESSING OFFLINE -</b><br/>Credit card processing is currently offline, please try again later.')
            raise CardDeclinedException(msg)
        
        self.flash.send('txtbox_msg', 'setText', {
            'text': _('Please input transaction password.') })
        self.flash.send('%s_ctr_num_keyboard' % self.windowID, 'show', {
            'type': 'password' })
        while True:
            self.event = self.flash.get(timeout = self.timeoutSec)
            if self.event == None:
                continue
            
            if self.event:
                log.info('[UI Event]: %s.' % self.event)
            
            ctrlID = self.event.get('cid')
            if ctrlID == 'CheckOutSwipeCardForm_ctr_num_keyboard':
                eventType = self._getEventParam('CheckOutSwipeCardForm_ctr_num_keyboard', 'type')
                if eventType == 'ok':
                    self.password = self._getEventParam('CheckOutSwipeCardForm_ctr_num_keyboard', 'val')
                    return True
                elif eventType == 'close':
                    return False
                
            elif ctrlID is None:
                return False
            

    
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
                    if checkDNS() == False:
                        msg = N_('<b>- COMMUNICATION ERROR -</b><br/>This kiosk is currently offline and unable to process your credit card.\nPlease contact the kiosk host for more information.')
                        self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                            'message': msg,
                            'type': 'alert' })
                        raise CardDeclinedException(msg)
                    
                    self.customer = Customer(ccName, ccNumber, ccExpDate, track2, track1)
                    if self._checkTrsPassword() == False:
                        self.nextWindowID = self.preWindowID
                        break
                    
                    ret = self.connProxy._getConfigByKey('enable_avs')
                    if ret == 'yes':
                        if self._getZipcode() == False:
                            self.nextWindowID = self.preWindowID
                            break
                        
                    else:
                        self.zipcode = None
                    tick = time.time()
                    self.flash.send('txtbox_msg', 'setText', {
                        'text': _('Authenticating ...') })
                    (status, invalidUserCoupons) = self.connProxy.validateUserCoupons(self.customer, globalSession.shoppingCart)
                    if str(status) == '0':
                        msg = N_('<b>- COUPON SERVICE OFFLINE -</b><br/>Coupon service is currently offline, so you will not be able to use any coupon for this rental.')
                        raise ValidateCouponException(msg)
                    elif str(status) == '2':
                        msg = N_('Validate Coupons timeout, please try again.')
                        raise ValidateCouponException(msg)
                    
                    if invalidUserCoupons:
                        msg = N_('Dear %(user)s:\nThese coupons are detected invalid. \nPlease change them to valid ones, or simply remove them to continue.\n%(list)s')
                        pm = {
                            'user': ccName,
                            'list': '\n'.join(invalidUserCoupons) }
                        raise InvalidCouponException(msg, pm)
                    
                    if self._checkMemberDetail() == False:
                        self.nextWindowID = self.preWindowID
                        break
                    
                    discCountErrorCode = str(self.connProxy.validateTrsLimit(self.customer, globalSession.shoppingCart))
                    if discCountErrorCode == '1':
                        pass
                    else:
                        msg = N_('Internal Error, please try again. [%(err)s]')
                        pm = {
                            'err': discCountErrorCode }
                        if discCountErrorCode == '2':
                            msg = N_('Max rental count reached.')
                            pm = { }
                        elif discCountErrorCode == '3':
                            msg = N_('Max purchase count reached.')
                            pm = { }
                        elif discCountErrorCode == '4':
                            msg = N_('Max rental and purchase count reached.')
                            pm = { }
                        elif discCountErrorCode == '5':
                            msg = N_('Max rental count reached.')
                            pm = { }
                        
                        raise InvalidMemberException(msg, pm)
                    self._chargeCard()
                    globalSession.customer = self.customer
                    self.nextWindowID = 'CheckOutEjectForm'
            except CardReadException as ex:
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': ex.i18nmsg,
                    'type': 'alert' })
            except CardDeclinedException as ex:
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': ex.i18nmsg,
                    'type': 'alert',
                    'height': '250' })
                self.fail = True
            except InvalidCouponException as ex:
                textlen = 333 + len(invalidUserCoupons) * 38
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': ex.i18nmsg,
                    'type': 'alert',
                    'height': str(textlen) })
                self.fail = True
            except InvalidMemberException as ex:
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': ex.i18nmsg,
                    'type': 'alert' })
                self.fail = True
            except ValidateCouponException as ex:
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': ex.i18nmsg,
                    'type': 'alert',
                    'height': '250' })
                self.fail = True
            except Exception as ex:
                raise 
            finally:
                self.flash.send('txtbox_msg', 'setText', {
                    'text': _('Please swipe Your Credit Card or MemberShip Card') })



