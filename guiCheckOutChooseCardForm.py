# Source Generated with Decompyle++
# File: guiCheckOutChooseCardForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V0.4
CopyRight MovieMate, Inc.

Created 2009-10-20 Andrew
andrew.lu@cereson.com

Filename:guiCheckOutChooseCardForm.py

Change Log:

'''
from mcommon import *
from guiBaseForms import CustomerForm
log = initlog('CheckOutChooseCard')

class CheckOutChooseCardForm(CustomerForm):
    
    def __init__(self):
        super(CheckOutChooseCardForm, self).__init__()
        self.screenID = 'R10'
        self.timeoutSec = 60
        self.preWindowID = 'ShoppingCartForm'
        self.lstResponseCtrl.extend([
            'btn_credit_card',
            'btn_debit_card',
            'btn_save',
            'btn_current_cheque',
            'btn_cancel',
            'btn_back'])

    
    def _initComponents(self):
        super(CheckOutChooseCardForm, self)._initComponents()
        self.flash.send('btn_credit_card', 'show', { })
        self.flash.send('btn_debit_card', 'show', { })
        self.flash.send('btn_save', 'hide', { })
        self.flash.send('btn_current_cheque', 'hide', { })
        msg = _('Please choose your card type.')
        self.flash.send('txt_cart_info_label', 'setText', {
            'text': msg })

    
    def _chooseDebitCardType(self):
        self.flash.send('btn_credit_card', 'hide', { })
        self.flash.send('btn_debit_card', 'hide', { })
        self.flash.send('btn_save', 'show', { })
        self.flash.send('btn_current_cheque', 'show', { })

    
    def on_btn_credit_card_event(self):
        self.nextWindowID = 'CheckOutSwipeCardForm'
        self.windowJump = True

    
    def on_btn_debit_card_event(self):
        self._chooseDebitCardType()

    
    def on_btn_save_event(self):
        globalSession.param['acctType'] = '01'
        self.nextWindowID = 'CheckOutSwipeDebitCardForm'
        self.windowJump = True

    
    def on_btn_current_cheque_event(self):
        globalSession.param['acctType'] = '02'
        self.nextWindowID = 'CheckOutSwipeDebitCardForm'
        self.windowJump = True

    
    def on_btn_cancel_event(self):
        self.on_cancel()

    
    def on_btn_back_event(self):
        self.on_back()


