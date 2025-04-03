# Source Generated with Decompyle++
# File: guiCheckOutSwipeProsaForm.pyc (Python 2.5)

'''
Created on 2010-6-7
@author: andrew.lu@cereson.com
'''
import time
import datetime
from control import *
from guiBaseForms import CustomerForm
from mcommon import *
from proxy.upg_proxy import UPGProxy
from guiRobotForm import RobotForm
from proxy.tools import fmtMoney, checkDNS
import sys
import serial
import config
log = initlog('CheckOutSwipeProsaForm')

class CheckOutSwipeProsaForm(CustomerForm):
    
    def __init__(self):
        super(CheckOutSwipeProsaForm, self).__init__()
        self.nextWindowID = 'CheckOutEjectForm'
        self.preWindowID = 'ShoppingCartForm'
        self.screenID = 'R15'
        self.lstResponseCtrl.extend([
            'CheckOutSwipeProsaForm_ctr_message_box',
            'btn_member_card',
            'btn_credit_card',
            'swf_swipe_card',
            'swf_insert_card',
            'pic_card_member',
            'pic_card_credit',
            'swf_credit_cars',
            'btn_back'])
        robot = Robot()
        self.robot = robot.getInstance()
        self.robotForm = RobotForm()
        self.robotForm.screenID = 'R15'
        self.card_type = ''

    
    def _initComponents(self):
        super(CheckOutSwipeProsaForm, self)._initComponents()
        self.timeoutSec = 60
        self.card_type = ''
        self.flash.send('btn_member_card', 'show', { })
        self.flash.send('btn_credit_card', 'show', { })
        self.flash.send('swf_swipe_card', 'hide', { })
        self.flash.send('swf_insert_card', 'hide', { })
        self.flash.send('pic_card_member', 'show', { })
        self.flash.send('pic_card_credit', 'show', { })
        self.flash.send('swf_credit_cars', 'hide', { })
        self.flash.send('btn_back', 'show', { })
        self.flash.send('btn_back', 'setDisable', {
            'disabled': 'false' })
        self.flash.send('txt_cart_info_label', 'setText', {
            'text': _('Please select payment method') })
        self.shoppingCart = globalSession.shoppingCart
        self.upgProxy = UPGProxy()
        self.customer = Customer()
        self.flash.send('%s_ctr_message_box' % self.windowID, 'close', { })

    
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
                if ctrlID == 'CheckOutSwipeProsaForm_ctr_message_box':
                    if self._getEventParam('CheckOutSwipeProsaForm_ctr_message_box', 'val') != 'yes':
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
                
        

    
    def _cancel(self):
        self.robot.cancel()
        self.nextWindowID = self.preWindowID
        self.windowJump = True

    
    def on_btn_back_event(self):
        self._cancel()

    
    def _get_card_info(self):
        if self.card_type == 'credit':
            msg = ''
            pm = { }
            self.customer.oid = ''
            smartEMV = None
            tick = time.time()
            while time.time() - tick < self.timeoutSec:
                (status, m, smartEMV) = self.upgProxy.checkForProsa()
                log.info('[card reader connected status and  m]: %s %s' % (status, m))
                eventFromFlash = self.flash.get(timeout = 0.1)
                if eventFromFlash:
                    cid = eventFromFlash.get('cid')
                    if cid == 'btn_back':
                        log.info('checking For Prosa [%s] - back Button Clicked.' % self.windowID)
                        self._cancel()
                        break
                    
                
                if status != '0':
                    msg = N_(m)
                    raise CardDeclinedException(msg, pm)
                else:
                    self.flash.send('txt_cart_info_label', 'clear', { })
                    self.flash.send('txt_cart_info_label', 'setText', {
                        'text': _('Please insert your card. ') })
                    (status, m) = self.upgProxy.getCardInfoFromProsa(self.customer, smartEMV)
                    log.info('[card reader returned status and  m]: %s %s' % (status, m))
                    if status == '0':
                        log.info('[ccNum and track2 and oid]: %s %s %s' % (self.customer.ccNum, self.customer.track2, self.customer.oid))
                        log.info('get card information')
                        return None
                    elif status == '1':
                        msg = N_('Card Declined, error code from the gateway:%(errcode)s')
                        pm = {
                            'errcode': m }
                    elif status == '5':
                        msg = N_('Sorry, the kiosk has not set any account.')
                    elif status == '6':
                        msg = N_('Gateway is busy, please retry.')
                    elif status == '10':
                        msg = N_('EVT has not been setup or PosServer is down.')
                    elif status == '11':
                        msg = N_('Process failed, please retry.')
                    elif status == '12':
                        msg = N_('Gateway error: Wallet Reference is missing.')
                    elif status == '13':
                        msg = N_('Time Out.')
                        log.error('getResForPROSA failed: %s' % msg)
                        raise DebitCardTimeOut(msg)
                    else:
                        msg = N_('Unknown error.')
                    raise CardDeclinedException(msg, pm)
        elif self.card_type == 'membership':
            
            try:
                log.info('get info membership card')
                tick = time.time()
                r = self.robot.doCmdAsync('read_card', { }, self.timeoutSec)
                retFromRobot = None
                while time.time() - tick < self.timeoutSec:
                    log.info('polling time %s' % (time.time() - tick))
                    retFromRobot = self.robot.getResult(r)
                    if retFromRobot:
                        log.info('[Robot Event]: %s' % logTrack(retFromRobot))
                        break
                    
                    eventFromFlash = self.flash.get(timeout = 0.1)
                    if eventFromFlash:
                        cid = eventFromFlash.get('cid')
                        if cid == 'btn_back':
                            log.info('[%s] - back Button Clicked.' % self.windowID)
                            retFromRobot = None
                            self._cancel()
                            return None
                        
                    
                if not retFromRobot:
                    log.debug('not retFromRobot')
                    self._cancel()
                    return None
                else:
                    log.debug('verify retFromRobot')
                    self.robotForm._verifyRet(retFromRobot)
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
                        'disabled': 'True' })
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
                        log.debug('password false')
                        return None
                    
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
            except Exception as ex:
                log.error('get card info %s' % ex)
                raise 
            


    
    def _chargeForProsa(self):
        msg = ''
        pm = { }
        (status, m) = self.upgProxy.chargeForProsa(self.customer, globalSession.shoppingCart)

    
    def _checkTrsPassword(self):
        self.password = None
        ret = self.upgProxy.chkNeedTrsPasswd(self.customer)
        log.info('chkNeedTrsPasswd return %s' % ret)
        if ret == 1:
            return True
        elif ret == 2:
            msg = N_('<b>- CREDIT CARD PROCESSING OFFLINE -</b><br/>Credit card processing is currently offline, please try again later.')
            raise CardDeclinedException(msg)
        
        self.flash.send('txt_cart_info_label', 'setText', {
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
            if ctrlID == 'CheckOutSwipeProsaForm_ctr_num_keyboard':
                eventType = self._getEventParam('CheckOutSwipeProsaForm_ctr_num_keyboard', 'type')
                if eventType == 'ok':
                    self.password = self._getEventParam('CheckOutSwipeProsaForm_ctr_num_keyboard', 'val')
                    return True
                elif eventType == 'close':
                    return False
                
            elif ctrlID is None:
                return False
            

    
    def _chargeCard(self):
        self.flash.send('txt_cart_info_label', 'clear', { })
        self.flash.send('txt_cart_info_label', 'setText', {
            'text': _('Authenticating ...') })
        (status, proxyMsg) = self.upgProxy.preauthCard(self.customer, globalSession.shoppingCart)
        if self.customer.cardType == 3:
            cerepayConfig = self.upgProxy.getCerePayCfg()
            userInfo = self.upgProxy.getCerePayUserInfo(cerepayConfig['MERCHANTID'], cerepayConfig['PASSWORD'], cerepayConfig['CURRENCY'], self.customer.ccNum)
            ccDisplay = userInfo.get('name', '')
            if not ccDisplay or str(ccDisplay).lower() == 'none':
                ccDisplay = 'CEREPAY CARD'
            
            ccDisplay += ' (%s)' % str(self.customer.ccNum[-4:])
            self.customer.ccDisplay = ccDisplay
        
        log.info('[UPG Charge Card]: %s --------------%s' % (status, proxyMsg))
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
            msg = N_('Sorry, the kiosk has communication issue, Please retry.')
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
            msg = N_('Sorry, payment gateway busy, Please retry.')
            raise CardDeclinedException(msg)

    
    def on_CheckOutSwipeProsaForm_ctr_message_box_event(self):
        if self._getEventParam('CheckOutSwipeProsaForm_ctr_message_box', 'val') == 'yes':
            self.on_back()
        

    
    def on_btn_member_card_event(self):
        self.flash.send('swf_swipe_card', 'show', { })
        self.flash.send('swf_insert_card', 'hide', { })
        self.flash.send('btn_credit_card', 'hide', { })
        self.flash.send('btn_member_card', 'hide', { })
        self.flash.send('pic_card_member', 'hide', { })
        self.flash.send('pic_card_credit', 'hide', { })
        self.flash.send('btn_back', 'show', { })
        self.flash.send('txt_cart_info_label', 'setText', {
            'text': _('Please swipe your Membership Card to take your Disc(s)') })
        log.info('btn_member clicked')
        self.card_type = 'membership'

    
    def on_btn_credit_card_event(self):
        log.info('btn_credit clicked')
        self.flash.send('btn_credit_card', 'hide', { })
        self.flash.send('btn_member_card', 'hide', { })
        self.flash.send('swf_swipe_card', 'hide', { })
        self.flash.send('swf_credit_cars', 'show', { })
        self.flash.send('swf_insert_card', 'show', { })
        self.flash.send('pic_card_member', 'hide', { })
        self.flash.send('pic_card_credit', 'hide', { })
        self.flash.send('btn_back', 'hide', { })
        self.flash.send('txt_cart_info_label', 'setText', {
            'text': _('Please insert your Credit Card to take your Disc(s)') })
        self.card_type = 'credit'

    
    def _run(self):
        
        try:
            log.info('wait customer swipe card')
            while not (self.card_type):
                self.event = self.flash.get(timeout = self.timeoutSec)
                if self.event == None:
                    continue
                
                if self.event:
                    log.info('[UI Event]: %s.' % self.event)
                
                ctrlID = self.event.get('cid')
                if ctrlID == 'btn_back':
                    log.info('btn back !!')
                    self._cancel()
                    break
                
                self.on_event(ctrlID)
                if self.windowJump:
                    return None
                
                if self.card_type:
                    break
                
            self._get_card_info()
            if self._checkMemberDetail() == False:
                self.nextWindowID = self.preWindowID
            
            self.flash.send('btn_back', 'setDisable', {
                'disabled': 'true' })
            if self.windowJump:
                return None
            
            self._chargeCard()
            globalSession.customer = self.customer
            self.nextWindowID = 'CheckOutEjectForm'
            self.windowJump = True
            return None
        except CardReadException as ex:
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': ex.i18nmsg,
                'type': 'alert' })
        except CardDeclinedException as ex:
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': ex.i18nmsg,
                'type': 'alert' })
        except DebitCardTimeOut as ex:
            self.timeoutSec = 0
            log.error('getResForSA reach time out')
            self.nextWindowID = 'ShoppingCartForm'
            self.windowJump = True
            return None
        except InvalidMemberException as ex:
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': ex.i18nmsg,
                'type': 'alert' })
        except Exception as ex:
            raise 
        finally:
            self.robot.resetSerial()

        super(CheckOutSwipeProsaForm, self)._run()


