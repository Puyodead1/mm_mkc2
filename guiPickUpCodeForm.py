# Source Generated with Decompyle++
# File: guiPickUpCodeForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V0.4
CopyRight MovieMate, Inc.

Created 2009-10-22 Andrew
andrew.lu@cereson.com

Filename:guiPickUpCodeForm.py

Change Log:

'''
from mcommon import *
from guiBaseForms import UserForm
from proxy.upg_proxy import UPGProxy
log = initlog('PickUpCodeForm')

class PickUpCodeForm(UserForm):
    
    def __init__(self):
        super(PickUpCodeForm, self).__init__()
        self.screenID = 'P5'
        self.timeoutSec = 60
        self.preWindowID = 'MainForm'
        self.lstResponseCtrl.extend([
            'btn_swipe_card',
            'btn_pin_code',
            'PickUpCodeForm_ctr_num_keyboard',
            'btn_cancel',
            'btn_back'])

    
    def _initComponents(self):
        super(PickUpCodeForm, self)._initComponents()
        self.flash.send('%s_ctr_message_box' % self.windowID, 'close', { })
        if self.connProxy._getConfigByKey('payment_options') == 'chipnpin':
            self.flash.send('btn_swipe_card', 'hide', { })
        else:
            self.flash.send('btn_swipe_card', 'show', { })

    
    def on_btn_swipe_card_event(self):
        self.nextWindowID = 'PickUpSwipeCardForm'
        self.windowJump = True

    
    def on_btn_pin_code_event(self):
        self.flash.send('%s_ctr_num_keyboard' % self.windowID, 'show', { })

    
    def on_PickUpCodeForm_ctr_num_keyboard_event(self):
        eventType = self._getEventParam('PickUpCodeForm_ctr_num_keyboard', 'type')
        if eventType == 'click':
            pass
        elif eventType == 'ok':
            pincode = self._getEventParam('PickUpCodeForm_ctr_num_keyboard', 'val')
            shoppingCart = ShoppingCart()
            ccid = self.connProxy.getPickUpListByCode(shoppingCart, pincode)
            log.info('[Pick Up List]: %s disc(s)' % shoppingCart.getSize())
            if shoppingCart.discs:
                globalSession.pickupCart = shoppingCart
                globalSession.customer.ccid = ccid
                self.upgProxy = UPGProxy()
                self.upgProxy.getCCInfoFromCacheByCustomer(globalSession.customer)
                self.nextWindowID = 'PickUpDiscListForm'
                self.windowJump = True
            else:
                msg = _('Sorry, no discs have been reserved by this pickup code.')
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': msg,
                    'type': 'alert' })
        

    
    def on_btn_cancel_event(self):
        self.on_cancel()

    
    def on_btn_back_event(self):
        self.on_back()


