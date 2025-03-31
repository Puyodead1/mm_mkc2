# Source Generated with Decompyle++
# File: guiCheckOutWithoutCerepayCardForm.pyc (Python 2.5)

'''
Created on 2010-12-13
@author: andrew.lu@cereson.com
'''
import datetime
from mcommon import *
from guiBaseForms import CustomerForm
from proxy.upg_proxy import UPGProxy

class CheckOutWithoutCerepayCardForm(CustomerForm):
    
    def __init__(self):
        super(CheckOutWithoutCerepayCardForm, self).__init__()
        self.screenID = 'R13'
        self.preWindowID = 'ShoppingCartForm'
        self.uiErrorWindowID = 'MainForm'
        self.timeoutSec = 180
        self.lstResponseCtrl.extend([
            'btn_back',
            'CheckOutWithoutCerepayCardForm_ctr_message_box',
            'CheckOutWithoutCerepayCardForm_ctr_all_keyboard'])

    
    def _initComponents(self):
        super(CheckOutWithoutCerepayCardForm, self)._initComponents()
        self.zipcode = ''
        self.password = ''
        self.fail = False
        self.upgProxy = UPGProxy()
        msg = _('Please enter your transaction password.')
        self.flash.send('txt_msg', 'setText', {
            'text': msg })
        if globalSession.loginCustomer.cerepayCard.needTrsPasswd:
            self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', {
                'type': 'password' })
            self.flash.send('%s_ctr_message_box' % self.windowID, 'hide', { })
        else:
            self.fail = True
            msg = N_('Transaction password is not enabled.')
            self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'hide', { })
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'alert' })

    
    def _chargeCard(self):
        (status, proxyMsg) = self.upgProxy.preauthCard(self.customer, globalSession.shoppingCart, self.zipcode, self.password)
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
                
        
        return True

    
    def _processCheckout(self):
        
        try:
            self.fail = False
            self.flash.send('txt_msg', 'setText', {
                'text': _('Authenticating ...') })
            (status, invalidUserCoupons) = self.connProxy.validateUserCoupons(self.customer, globalSession.shoppingCart)
            if str(status) == '0':
                msg = N_('Coupon is not available temporarily, please try later.')
                raise ValidateCouponException(msg)
            elif str(status) == '2':
                msg = N_('Validate Coupons timeout, please try again.')
                raise ValidateCouponException(msg)
            
            if invalidUserCoupons:
                msg = N_('Dear %(user)s:\nThese coupons are detected invalid. \nPlease change them to valid ones, or simply remove them to continue.\n%(list)s')
                pm = {
                    'user': globalSession.loginCustomer.lastName,
                    'list': '\n'.join(invalidUserCoupons) }
                raise InvalidCouponException(msg, pm)
            
            if self._checkMemberDetail() == False:
                self.nextWindowID = self.preWindowID
                self.windowJump = True
                return None
            
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
                
                raise InvalidMemberexcept ion(msg, pm)
            self._chargeCard()
            globalSession.customer = self.customer
            self.nextWindowID = 'CheckOutEjectForm'
            self.windowJump = True
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


    
    def on_CheckOutWithoutCerepayCardForm_ctr_message_box_event(self):
        choice = self._getEventParam('CheckOutWithoutCerepayCardForm_ctr_message_box', 'val')
        if choice == 'yes' and self.fail:
            self.on_back()
        

    
    def on_CheckOutWithoutCerepayCardForm_ctr_all_keyboard_event(self):
        eventType = self._getEventParam('CheckOutWithoutCerepayCardForm_ctr_all_keyboard', 'type')
        if eventType == 'click':
            pass
        elif eventType == 'ok':
            self.password = self._getEventParam('CheckOutWithoutCerepayCardForm_ctr_all_keyboard', 'val')
            self.customer = Customer()
            self.customer.ccNum = globalSession.loginCustomer.cerepayCard.number
            self._processCheckout()
        elif eventType == 'close':
            self.nextWindowID = self.preWindowID
            self.windowJump = True
        


