# Source Generated with Decompyle++
# File: guiShoppingCartForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiShoppingCartForm.py
Shopping Cart
Screen ID: R5

Change Log:
    Andrew  2009-05-12 Change for MaxDvdOut and BuyLimit
    Vincent 2009-03-05 For max_dvd_out and buy_limit

'''
import os
import traceback
from mcommon import *
from guiBaseForms import CustomerForm
log = initlog('guiShoppingCartForm')

class ShoppingCartForm(CustomerForm):
    
    def __init__(self):
        super(ShoppingCartForm, self).__init__()
        self.preWindowID = 'RentMainForm'
        self.screenID = 'R5'
        self.timeoutSec = 120
        self.lstResponseCtrl.extend([
            'btn_back',
            'btn_cancel',
            'btn_add_another',
            'btn_checkout',
            'btn_coupon',
            'ShoppingCartForm_ctr_message_box',
            'btn_clear_all_dvd',
            'ctr_cart_info'])

    
    def _displayShoppingCart(self):
        lstShoppingCart = []
        for disc in self.shoppingCart.discs:
            dict = { }
            dict['rfid'] = disc.rfid
            dict['movie_pic'] = getPicFullPath(disc.picture)
            dict['movie_title'] = disc.title
            dict['price_plan_text'] = disc.pricePlan
            if disc.gene == 'sale':
                dict['price_plan_text'] = '%s %s' % (globalSession.param.get('currency_symbol'), disc.salePrice)
            
            dict['coupon_code'] = disc.coupon.couponCode
            dict['coupon_short_description'] = disc.coupon.shortDes
            lstShoppingCart.append(dict)
        
        self.flash.send('ctr_cart_info', 'setCartInfo', {
            'ctr_cart_info': lstShoppingCart,
            'global_coupon_code': self.shoppingCart.coupon.couponCode,
            'global_coupon_short_description': self.shoppingCart.coupon.shortDes })

    
    def _initComponents(self):
        super(ShoppingCartForm, self)._initComponents()
        self.shoppingCart = globalSession.shoppingCart
        self._displayShoppingCart()
        self.confirmBox = ''
        promotionMsg = self.connProxy.getShoppingCartMessage()
        if promotionMsg:
            self.flash.send('infoLabel', 'show', { })
            self.flash.send('txtbox_msg', 'setText', {
                'text': promotionMsg })
        else:
            self.flash.send('infoLabel', 'hide', { })
            self.flash.send('txtbox_msg', 'setText', {
                'text': '' })

    
    def on_btn_back_event(self):
        self.on_back()

    
    def on_btn_cancel_event(self):
        self.on_cancel()

    
    def on_btn_add_another_event(self):
        if self.connProxy.checkAddAnotherDisc(self.shoppingCart) == False:
            msg = _('Shopping cart full, click [Back] on the top to browse another disc.')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'alert' })
        else:
            self.nextWindowID = 'RentMainForm'
            self.windowJump = True

    
    def _checkMcoupon(self):
        if globalSession.shoppingCart.coupon.couponCode:
            if globalSession.shoppingCart.coupon.shortDes == 'r1f1':
                msg = _('Your coupon has been activated. The 2nd movie will be discounted to %(cur)s0 when both movies are returned together.') % {
                    'cur': globalSession.param['currency_symbol'] }
            else:
                msg = _('Multiple discs coupon detected, please return all discs in the same time to activate it.')
            self.confirmBox = 'confirm_M_coupon'
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'confirm' })
        

    
    def _gotoCheckOut(self):
        option = self.connProxy._getConfigByKey('payment_options')
        if option == 'intecon':
            self.nextWindowID = 'CheckOutChooseCardForm'
        elif option == 'chipnpin':
            self.nextWindowID = 'CheckOutSwipeChipPinForm'
        elif option == 'prosa':
            self.nextWindowID = 'CheckOutSwipeProsaForm'
        elif option == 'sitef':
            self.nextWindowID = 'CheckOutSwipeSiTefForm'
        else:
            self.nextWindowID = 'CheckOutSwipeCardForm'
        self.windowJump = True

    
    def on_btn_checkout_event(self):
        if globalSession.shoppingCart.discs:
            if globalSession.shoppingCart.coupon.couponCode:
                self._checkMcoupon()
            else:
                self._gotoCheckOut()
        

    
    def on_btn_coupon_event(self):
        if globalSession.shoppingCart.discs:
            self.nextWindowID = 'CouponForm'
            self.windowJump = True
        

    
    def on_ShoppingCartForm_ctr_message_box_event(self):
        inputVal = self._getEventParam('ShoppingCartForm_ctr_message_box', 'val')
        if inputVal == 'yes':
            if self.confirmBox == 'clear_shopping_cart':
                self.connProxy.removeDiscsFromShoppingCart(self.shoppingCart.discs)
                globalSession.shoppingCart.clear()
                self._displayShoppingCart()
            elif self.confirmBox == 'confirm_M_coupon':
                self._gotoCheckOut()
            
        
        self.confirmBox = ''

    
    def on_btn_clear_all_dvd_event(self):
        msg = _('Are you sure to empty the shopping cart?')
        self.confirmBox = 'clear_shopping_cart'
        self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
            'message': msg,
            'type': 'confirm' })

    
    def on_ctr_cart_info_event(self):
        rfid = self._getEventParam('ctr_cart_info', 'rfid')
        for disc in self.shoppingCart.discs:
            if disc.rfid == rfid:
                globalSession.shoppingCart.removeDiscByRfid(rfid)
                self.connProxy.removeDiscsFromShoppingCart([
                    disc])
                log.info('[Shopping Cart]: %s' % globalSession.shoppingCart.getSize())
                break
            
        
        self._displayShoppingCart()


