# Source Generated with Decompyle++
# File: guiCheckOutSwipeDebitCardForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V0.4
CopyRight MovieMate, Inc.

Created 2009-10-20 Andrew
andrew.lu@cereson.com

Filename:guiCheckOutSwipeDebitCardForm.py

Change Log:

'''
from guiBaseForms import CustomerForm
from mcommon import *
from proxy.upg_proxy import UPGProxy
log = initlog('CheckOutSwipeDebitCardForm')

class CheckOutSwipeDebitCardForm(CustomerForm):
    
    def __init__(self):
        super(CheckOutSwipeDebitCardForm, self).__init__()
        self.nextWindowID = 'CheckOutEjectForm'
        self.preWindowID = 'CheckOutChooseCardForm'
        self.screenID = 'R11'
        self.lstResponseCtrl.extend([
            'CheckOutSwipeDebitCardForm_ctr_message_box'])

    
    def _initComponents(self):
        super(CheckOutSwipeDebitCardForm, self)._initComponents()
        self.timeoutSec = 60
        self.flash.send('ctr_btn_center', 'setDisabled', {
            'disabled': 'true' })
        self.flash.send('swf_swipe_card', 'show', { })
        self.flash.send('txt_cart_info_label', 'setText', {
            'text': _('Swipe your debit card at the side mounted Pin Pad device and enter your pin number to rent your chosen Disc(s). Obtaining card information ...') })
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
                if ctrlID == 'CheckOutSwipeDebitCardForm_ctr_message_box':
                    if self._getEventParam('CheckOutSwipeDebitCardForm_ctr_message_box', 'val') != 'yes':
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
                
        

    
    def _sendReq(self):
        msg = ''
        acctType = globalSession.param.get('acctType')
        (status, tmsg, self.seq, self.trsIdty) = self.upgProxy.sendReqForSA(self.customer, self.shoppingCart, acctType)
        if status == '0':
            return None
        elif status == '1':
            msg = N_('Internal Error: gateway config empty!')
        elif status == '2':
            msg = N_('Internal Error: gateway config invalid (port)!')
        elif status == '3':
            msg = N_('Internal error.')
        elif status == '4':
            msg = N_('Timeout when connectting to gateway.')
        elif status == '5':
            msg = N_('Connection refused when connecting to gateway.')
        elif status == '6':
            msg = N_('Internal Error: gateway config invalid (FTP username / pwd)!')
        elif status == '7':
            msg = N_('Permission denied when creating new file to ftp server.')
        else:
            msg = N_('Internal error.')
        log.error('sendReqForSA failed: %s' % msg)
        raise CardDeclinedException(msg)

    
    def _recvAns(self):
        msg = ''
        pm = { }
        (status, tmsg) = self.upgProxy.getResForSA(self.customer, self.shoppingCart, self.seq, self.trsIdty)
        if status == '0':
            return None
        elif status == '1':
            msg = N_('Internal Error: gateway config empty!')
        elif status == '2':
            msg = N_('Internal Error: gateway config invalid (port)!')
        elif status == '3':
            msg = N_('Internal error.')
        elif status == '4':
            msg = N_('Timeout when connectting to gateway.')
        elif status == '5':
            msg = N_('Connection refused when connecting to gateway.')
        elif status == '6':
            msg = N_('Internal Error: gateway config invalid (FTP username / pwd)!')
        elif status == '7':
            msg = N_('Permission denied when creating new file to ftp server.')
        elif status == '8':
            msg = N_('Card Declined, message from the bank:\n%(info)s')
            pm = {
                'info': tmsg }
        elif status == '10':
            msg = N_('Time out.')
            km = KioskMessage(msg)
            log.error('getResForSA failed: %s' % km.message)
            raise DebitCardTimeOut(msg)
        else:
            msg = N_('Internal Error: communication failed (kiosk to gateway)')
        km = KioskMessage(msg, pm)
        log.error('getResForSA failed: %s' % km.message)
        raise CardDeclinedException(msg, pm)

    
    def on_CheckOutSwipeDebitCardForm_ctr_message_box_event(self):
        if self._getEventParam('CheckOutSwipeDebitCardForm_ctr_message_box', 'val') == 'yes':
            self.on_back()
        

    
    def _run(self):
        
        try:
            self._sendReq()
            self._recvAns()
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
            globalSession.customer = self.customer
            self.nextWindowID = 'CheckOutEjectForm'
            self.windowJump = True
            return None
        except CardDeclinedException:
            ex = None
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': ex.i18nmsg,
                'type': 'alert' })
        except DebitCardTimeOut:
            ex = None
            self.timeoutSec = 0
            log.error('getResForSA reach time out')
        except ValidateCouponException:
            ex = None
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': ex.i18nmsg,
                'type': 'alert',
                'height': '250' })
        except InvalidCouponException:
            ex = None
            textlen = 333 + len(invalidUserCoupons) * 38
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': ex.i18nmsg,
                'type': 'alert',
                'height': str(textlen) })
        except InvalidMemberException:
            ex = None
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': ex.i18nmsg,
                'type': 'alert' })
        except Exception:
            ex = None
            raise 

        super(CheckOutSwipeDebitCardForm, self)._run()


