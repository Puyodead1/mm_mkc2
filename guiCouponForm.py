# Source Generated with Decompyle++
# File: guiCouponForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiCouponForm.py
Coupon Settings
Screen ID: R6

Change Log:
    2009-03-05 Vincent Fix a bug when [>] button is clicked to bring up movie selector
'''
import os
import traceback
from copy import deepcopy
from mcommon import *
from guiBaseForms import CustomerForm
log = initlog('guiCouponForm')

class CouponForm(CustomerForm):
    
    def __init__(self):
        super(CouponForm, self).__init__()
        self.screenID = 'R6'
        self.timeoutSec = 180
        self.preWindowID = 'ShoppingCartForm'
        self.lstResponseCtrl.extend([
            'btn_back',
            'btn_ok',
            'btn_cancel',
            'btn_add',
            'CouponForm_ctr_all_keyboard',
            'CouponForm_ctr_message_box',
            'btn_coupon_movie',
            'ctr_movie_info',
            'btn_del'])

    
    def _discCouponChange(self, disc):
        for gd in globalSession.shoppingCart.discs:
            if gd.rfid == disc.rfid:
                if gd.coupon.couponCode != disc.coupon.couponCode:
                    return True
                
            
        
        return False

    
    def _haveCouponsChange(self):
        have = False
        if self.shoppingCart.coupon.couponCode != globalSession.shoppingCart.coupon.couponCode:
            have = True
        else:
            for disc in self.shoppingCart.discs:
                if self._discCouponChange(disc) == True:
                    have = True
                    break
                
            
        return have

    
    def _displayCouponList(self):
        '''
        Parse the shopping cart data
        Display it in the ctr_coupon_info list
        '''
        params = []
        for disc in self.shoppingCart.discs:
            if disc.coupon.couponCode:
                dict = { }
                dict['coupon_code'] = disc.coupon.couponCode
                dict['description'] = disc.coupon.description
                dict['coupon_disc_pic'] = getPicFullPath(disc.picture)
                dict['rfid'] = disc.rfid
                dict['coupon_type'] = 'S'
                params.append(dict)
            
        
        if self.shoppingCart.coupon.couponCode:
            dict = { }
            dict['coupon_code'] = self.shoppingCart.coupon.couponCode
            dict['description'] = self.shoppingCart.coupon.description
            dict['coupon_disc_pic'] = ''
            dict['rfid'] = ''
            dict['coupon_type'] = 'M'
            params.append(dict)
        
        self.flash.send('ctr_coupon_info', 'setCouponInfo', {
            'ctr_coupon_info': params })
        if not params:
            self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', { })
            self.flash.send('btn_ok', 'hide', { })
        else:
            self.flash.send('btn_ok', 'show', { })

    
    def _validateCoupons(self):
        result = 0
        (status, invalidCouponList) = self.connProxy.validateCoupons(self.shoppingCart)
        log.info('[Invalid Coupon List]: %s' % invalidCouponList)
        if str(status) == '0':
            msg = _('Coupon is not available temporarily, please try later.')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'alert',
                'height': '250' })
        elif str(status) == '2':
            msg = _('Validate Coupons timeout, please try again.')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'alert' })
        elif not invalidCouponList:
            result = 1
        else:
            msg = _('Invalid Coupon(s) Found: \n')
            height = 150
            for coupon in invalidCouponList:
                msg += '    %s\n' % coupon.get('coupon_code')
                height += 50
            
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'alert',
                'height': str(height) })
        return result
        '\n            status == "3":\n            msg = _("At lease one coupon does not match the its price plan.")\n        elif status == "4":\n            msg = _("At least one coupon is conflict with others.")\n        elif status == "9":\n            msg = _("At lease one coupon is locked, please retry in 5 minutes.")\n        elif status == "99":\n            msg = _("Coupons are not available right now: 99")\n        else:\n            msg = _("Coupons not available right now: %s") % status\n        '

    
    def _validateCoupon(self, couponCode):
        coupon = Coupon(couponCode)
        status = str(self.connProxy.getCouponInfo(coupon))
        log.info('[Copuon Status]: %s %s' % (couponCode, status))
        if status == '0':
            if str(coupon.couponType).lower() == 's':
                if self.usableCouponDiscs:
                    for disc in self.shoppingCart.discs:
                        if not (disc.coupon.couponCode) and disc in self.usableCouponDiscs:
                            disc.coupon = coupon
                            self.usableCouponDiscs.remove(disc)
                            break
                        
                    
                else:
                    msg = _('No more disc is suitable to use this coupon.')
                    self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                        'message': msg,
                        'type': 'alert' })
            elif str(coupon.couponType).lower() == 'm':
                self.shoppingCart.coupon = coupon
            
        elif status == '-1':
            msg = _('<b>- COUPON SERVICE OFFLINE -</b><br/>Coupon service is currently offline, so you will not be able to use any coupon for this rental.')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'alert' })
        elif status == '1':
            msg = _('This coupon code does not exist.')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'alert' })
        elif status == '5':
            msg = _('This coupon has not been activated yet.')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'alert' })
        elif status == '6':
            msg = _('This coupon is expired.')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'alert' })
        elif status == '9':
            msg = _('We apologize for the short delay, while we verify this coupon code. Please retry in 5 minutes.')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'alert',
                'height': '250' })
        elif status == '99':
            msg = _('This coupon is not available right now: 99')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'alert' })
        else:
            msg = _('This coupon is not available right now: %s') % status
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'alert' })

    
    def _parseCouponDiscList(self, lstDisc):
        '''
        params = [
                {"price_plan_text":"First Night Fee 1.99", "movie_pic":"zdgudsgz.jpg", "rfid":"zsdgzgsg"},
                {"price_plan_text":"First Night Fee 0.99", "movie_pic":"5gdfdgfgzd.jpg", "rfid":"zsdgzgsg"},
                ]
        '''
        params = []
        for disc in lstDisc:
            dict = { }
            dict['price_plan_text'] = disc.pricePlan
            dict['movie_pic'] = getPicFullPath(disc.picture)
            dict['rfid'] = disc.rfid
            params.append(dict)
        
        return params

    
    def _initComponents(self):
        super(CouponForm, self)._initComponents()
        self.msgboxType = ''
        self.shoppingCart = deepcopy(globalSession.shoppingCart)
        self._displayCouponList()
        self.usableCouponDiscs = self.connProxy.getUsableCouponDiscs(self.shoppingCart)
        self.allUsableCouponDiscs = deepcopy(self.usableCouponDiscs)
        for disc in self.shoppingCart.discs:
            if disc.coupon.couponCode:
                self.usableCouponDiscs.remove(disc)
            
        
        self.flash.send('%s_ctr_message_box' % self.windowID, 'close', { })
        if globalSession.param.get('test_mode'):
            self.flash.send('coupon_test_mode_flag', 'show', { })
        else:
            self.flash.send('coupon_test_mode_flag', 'hide', { })

    
    def on_btn_back_event(self):
        if self._haveCouponsChange():
            msg = _('All changes will be discarded, are you sure?')
            self.msgboxType = 'back'
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'confirm',
                'height': '250' })
        else:
            self.on_back()

    
    def on_btn_ok_event(self):
        if self._validateCoupons():
            globalSession.shoppingCart = self.shoppingCart
            self.nextWindowID = 'ShoppingCartForm'
            self.windowJump = True
        

    
    def on_btn_cancel_event(self):
        self.on_exit()

    
    def on_btn_add_event(self):
        self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', { })
        self.flash.send('btn_ok', 'hide', { })

    
    def on_CouponForm_ctr_message_box_event(self):
        if self.msgboxType == 'cancel':
            if self._getEventParam('CouponForm_ctr_message_box', 'val') == 'yes':
                self.nextWindowID = 'ShoppingCartForm'
                self.windowJump = True
            
        elif self.msgboxType == 'back':
            if self._getEventParam('CouponForm_ctr_message_box', 'val') == 'yes':
                self.on_back()
            
        
        self.msgboxType = ''

    
    def on_CouponForm_ctr_all_keyboard_event(self):
        eventType = self._getEventParam('CouponForm_ctr_all_keyboard', 'type')
        if eventType == 'click':
            pass
        elif eventType == 'ok':
            couponCode = self._getEventParam('CouponForm_ctr_all_keyboard', 'val')
            self._validateCoupon(couponCode)
            self._displayCouponList()
        elif eventType == 'close':
            self.flash.send('btn_ok', 'show', { })
        

    
    def on_btn_coupon_movie_event(self):
        self.oldRfid = self._getEventParam('btn_coupon_movie', 'rfid')
        params = self._parseCouponDiscList(self.allUsableCouponDiscs)
        self.flash.send('ctr_movie_info', 'show', { })
        self.flash.send('ctr_movie_info', 'setMovieInfo', {
            'ctr_movie_info': params,
            'selected_rfid': self.oldRfid })

    
    def on_ctr_movie_info_event(self):
        self.newRfid = self._getEventParam('ctr_movie_info', 'rfid')
        if self.newRfid == self.oldRfid:
            return None
        
        oldDisc = None
        newDisc = None
        for disc in self.shoppingCart.discs:
            if disc.rfid == self.newRfid:
                newDisc = disc
            elif disc.rfid == self.oldRfid:
                oldDisc = disc
            
        
        tmpCoupon = oldDisc.coupon
        oldDisc.coupon = newDisc.coupon
        newDisc.coupon = tmpCoupon
        self.oldRfid = self.newRfid
        self._displayCouponList()

    
    def on_btn_del_event(self):
        rfid = self._getEventParam('btn_del', 'rfid')
        if rfid:
            self.shoppingCart.removeDiscCoupon(rfid)
            disc = self.shoppingCart.getDisc(rfid)
            self.usableCouponDiscs.append(disc)
        else:
            self.shoppingCart.coupon = Coupon()
        self._displayCouponList()


