# Source Generated with Decompyle++
# File: guiCheckOutResultForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiCheckOutResultForm.py
Checkout Result
Screen ID: R9

Change Log:
    2011-11-14 Tim: #999, fix bug for the not working printer
    2009-04-29 Vincent Change the page time out value to 300 second

'''
import config
from mcommon import *
from guiBaseForms import CustomerForm
from printer import Printer, PrinterException
log = initlog('guiCheckOutResultForm')

class CheckOutResultForm(CustomerForm):
    
    def __init__(self):
        super(CheckOutResultForm, self).__init__()
        self.screenID = 'R9'
        self.timeoutSec = 60
        self.preWindowID = 'MainForm'
        self.lstResponseCtrl.extend([
            'btn_finish',
            'CheckOutResultForm_ctr_all_keyboard',
            'btn_print'])
        self.printer = None
        if self.connProxy._getConfigByKey('payment_options') == 'chipnpin':
            self._initPrinter()
        

    
    def _initPrinter(self):
        
        try:
            self.printer = Printer(config.PRINTER)
            self.printer.init()
            if self.printer.ser.isOpen() == False:
                self.printer = None
                msg = 'failed to open printer'
                log.error(msg)
        except:
            self.printer = None
            import traceback
            log.warning(traceback.format_exc())


    
    def _initComponents(self):
        super(CheckOutResultForm, self)._initComponents()
        self.shoppingCart = globalSession.shoppingCart
        globalSession.shoppingCart = ShoppingCart()
        if self.printer and self.connProxy._getConfigByKey('payment_options') == 'chipnpin':
            self.flash.send('btn_print', 'show', { })
        else:
            self.flash.send('btn_print', 'hide', { })
        self.printed = False
        msg = ''
        if self.shoppingCart.totalCharged:
            msg = _('%(cur)s%(money)s has been charged.') % {
                'cur': globalSession.param['currency_symbol'],
                'money': self.shoppingCart.totalCharged }
        
        self.flash.send('txt_sale_price', 'setText', {
            'text': msg })
        total = self.shoppingCart.getEjectedDiscsSize()
        msg = _('%s Disc(s) have been taken out.') % str(total)
        if globalSession.param.get('month_subs') and total > 0:
            msg += '\n%s\n' % globalSession.param.get('month_subs')
        
        if globalSession.param.get('eject_result'):
            msg += ' %s' % globalSession.param.get('eject_result')
        
        self.flash.send('txt_taken', 'setText', {
            'text': msg })
        if not (globalSession.customer.email) and total > 0:
            self.flash.send('txt_input_label', 'hide', { })
            self.flash.send('txt_thank1', 'hide', { })
        else:
            self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'hide', { })
            self.flash.send('txt_input_label', 'hide', { })
            self.flash.send('txt_thank1', 'show', { })
            if total == 0:
                msg = _('The rent operation failed, please try another one.')
                self.flash.send('txt_thank1', 'setText', {
                    'text': msg })
            else:
                msg = _('Dear Member: The receipt will be sent to your registered email within 24 hours.')
                self.flash.send('txt_thank1', 'setText', {
                    'text': msg })
                self.umsProxy.sendReceipt(globalSession.customer, self.shoppingCart)

    
    def printReceipt(self):
        self.flash.send('btn_print', 'hide', { })
        if not (self.printer):
            return None
        
        
        try:
            (door, paper) = self.printer.getPrinterStatus()
        except PrinterException:
            self.flash.send('txt_input_label', 'setText', {
                'text': 'Print failed, the receipt will be sent to your registered email within 24 hours.' })
            return None

        if door == 0:
            pass
        if not (paper == 0):
            self.flash.send('txt_input_label', 'setText', {
                'text': 'Print failed, the receipt will be sent to your registered email within 24 hours.' })
            return None
        
        tc = self.umsProxy.getAbbrTermsAndConditions()
        self.printer.printReceipt(config.getKioskId(), self.shoppingCart, globalSession.customer, tc)
        self.printed = True

    
    def on_btn_finish_event(self):
        self.on_cancel()
        if globalSession.loginCustomer.isLogin:
            globalSession.param['preWindowID'] = 'MembershipCenterForm'
        

    
    def on_btn_print_event(self):
        log.info('print receipt')
        self.printReceipt()

    
    def on_CheckOutResultForm_ctr_all_keyboard_event(self):
        eventType = self._getEventParam('CheckOutResultForm_ctr_all_keyboard', 'type')
        if eventType == 'click':
            pass
        elif eventType == 'ok':
            emailAddr = self._getEventParam('CheckOutResultForm_ctr_all_keyboard', 'val')
            if isValidEmail(emailAddr) == False:
                self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', { })
            else:
                globalSession.customer.email = emailAddr
                self.umsProxy.registerMember(globalSession.customer)
                self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'hide', { })
                self.flash.send('txt_input_label', 'hide', { })
                self.flash.send('txt_thank1', 'show', { })
                msg = _('Please check your email box for the receipt within 24 hours.\nWe have also sent you a registration email. \nYou can follow the instructions to register as our member \nfor online reservations and coupons. \nThanks for choosing us, enjoy!')
                self.flash.send('txt_thank1', 'setText', {
                    'text': msg })
                self.umsProxy.sendReceipt(globalSession.customer, self.shoppingCart)
        


