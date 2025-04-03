# Source Generated with Decompyle++
# File: guiCheckOutSwipeSiTefForm.pyc (Python 2.5)

'''
Created on 2012-7-30
@author: tavis.wang@cereson.com
'''
import time
import datetime
from guiBaseForms import CustomerForm
from mcommon import *
from proxy.upg_proxy import UPGProxy
log = initlog('CheckOutSwipeSiTefForm')

class CheckOutSwipeSiTefForm(CustomerForm):
    
    def __init__(self):
        super(CheckOutSwipeSiTefForm, self).__init__()
        self.nextWindowID = 'CheckOutEjectForm'
        self.preWindowID = 'ShoppingCartForm'
        self.screenID = 'R12'
        self.lstResponseCtrl.extend([
            'CheckOutSwipeSiTefForm_ctr_message_box'])

    
    def _initComponents(self):
        super(CheckOutSwipeSiTefForm, self)._initComponents()
        self.timeoutSec = 60
        self.flash.send('ctr_btn_center', 'setDisabled', {
            'disabled': 'true' })
        self.flash.send('swf_insert_card', 'show', { })
        self.flash.send('txt_cart_info_label', 'setText', {
            'text': _('Insert your Debit or Credit Card into the Card Reader to side of kiosk and enter your PIN to complete transaction') })
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
                if ctrlID == 'CheckOutSwipeSiTefForm_ctr_message_box':
                    if self._getEventParam('CheckOutSwipeSiTefForm_ctr_message_box', 'val') != 'yes':
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
                
        

    
    def charge(self):
        msg = ''
        pm = { }
        (status, m) = self.upgProxy.chargeForSiTef(self.customer, globalSession.shoppingCart)
        if status == '0':
            log.info('get card information,charge success')
            return None
        else:
            log.info('%s %s' % (status, m))
            msg = m
        raise CardDeclinedException(msg, pm)

    
    def _check_monthly_subscription(self):
        (status, ms_expire_time, invalid_disc_type, rent_count) = self.upgProxy.check_monthly_subscription(self.customer, globalSession.shoppingCart)
        if status == 1:
            msg = _('Monthly subscription activated, please return these discs before %(time)s.')
            tt = datetime.datetime(*time.strptime(ms_expire_time, '%Y-%m-%d %H:%M:%S')[:6]).strftime('%H:00 on %b %d, %Y')
            pm = {
                'time': tt }
            globalSession.param['month_subs'] = msg % pm
        elif status == 0:
            return None
        elif status == 2:
            msg = N_('Max discs exceeded for your monthly subscription, please remove at least %(del_num)s discs from your shopping cart and retry.')
            raise CardDeclinedException(msg, {
                'del_num': int(rent_count) - self.customer.msCount })
        elif status == 3:
            msg = N_('Only %(type2)s disc(s) can apply to your monthly subscription plan, but %(type1)s disc(s) found in your shopping cart. Please remove it/them and retry.')
            raise CardDeclinedException(msg, {
                'type1': ', '.join(list(invalid_disc_type)),
                'type2': self.customer.msDiscType })
        else:
            msg = N_('Unknown error.')
            raise CardDeclinedException(msg)

    
    def on_CheckOutSwipeSiTefForm_ctr_message_box_event(self):
        if self._getEventParam('CheckOutSwipeSiTefForm_ctr_message_box', 'val') == 'yes':
            self.on_back()
        

    
    def _run(self):
        
        try:
            log.info('wait customer swipe card')
            self.charge()
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
                    'user': 'Customer',
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
            self._checkMemberDetail()
            self._check_monthly_subscription()
            globalSession.customer = self.customer
            self.nextWindowID = 'CheckOutEjectForm'
            self.windowJump = True
            return None
        except CardDeclinedException as ex:
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': ex.i18nmsg,
                'type': 'alert' })
        except DebitCardTimeOut as ex:
            self.timeoutSec = 0
            log.error('getResForSA reach time out')
        except ValidateCouponException as ex:
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': ex.i18nmsg,
                'type': 'alert',
                'height': '250' })
        except InvalidCouponException as ex:
            textlen = 333 + len(invalidUserCoupons) * 38
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': ex.i18nmsg,
                'type': 'alert',
                'height': str(textlen) })
        except InvalidMemberException as ex:
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': ex.i18nmsg,
                'type': 'alert' })
        except Exception as ex:
            raise 

        super(CheckOutSwipeSiTefForm, self)._run()


