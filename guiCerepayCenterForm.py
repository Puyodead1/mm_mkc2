# Source Generated with Decompyle++
# File: guiCerepayCenterForm.pyc (Python 2.5)

'''
Created on 2010-12-13
@author: andrew.lu@cereson.com
'''
from mcommon import *
from guiBaseForms import CustomerForm
log = initlog('CerepayCenterForm')

class CerepayCenterForm(CustomerForm):
    
    def __init__(self):
        super(CerepayCenterForm, self).__init__()
        self.screenID = 'M6'
        self.preWindowID = 'MembershipCenterForm'
        self.uiErrorWindowID = 'MainForm'
        self.timeoutSec = 180
        self.lstResponseCtrl.extend([
            'btn_back',
            'btn_top_up',
            'btn_transactions',
            'btn_missing'])

    
    def __is_using_chipnpin(self):
        return self.connProxy._getConfigByKey('payment_options') == 'chipnpin'

    __is_using_chipnpin = property(__is_using_chipnpin)
    
    def _initComponents(self):
        super(CerepayCenterForm, self)._initComponents()
        if globalSession.isCerepayCardInfoDirty:
            cerepay_customer = Customer(ccNumber = globalSession.loginCustomer.cerepayCard.number)
            (status, __) = self.umsProxy.setMemberDetail(cerepay_customer, ShoppingCart())
            if status in ('0', '1') and cerepay_customer.isMember:
                globalSession.loginCustomer.cerepayCard = cerepay_customer.cerepayCard
            
            globalSession.isCerepayCardInfoDirty = False
        
        cerepayCard = globalSession.loginCustomer.cerepayCard
        currencySymbol = self.connProxy.getDefaultCurrencySymbol()
        info = []
        info.append({
            'title': _('Card Number'),
            'info': maskCard(cerepayCard.number) })
        info.append({
            'title': _('Balance'),
            'info': '%s%.2f' % (currencySymbol, round(cerepayCard.balance, 2)) })
        info.append({
            'title': _('Hold Amount'),
            'info': '%s%.2f' % (currencySymbol, round(cerepayCard.holdingAmt, 2)) })
        info.append({
            'title': _('Actual Balance'),
            'info': '%s%.2f' % (currencySymbol, round(cerepayCard.balance - cerepayCard.holdingAmt, 2)) })
        self.flash.send('info_list', 'setCerepayCenterList', {
            'info_list': info })
        msg = _('Please remember to logout when you leave the kiosk to protect your privacy.')
        self.flash.send('txt_msg', 'setText', {
            'text': msg })
        self.flash.send('btn_transactions', 'hide', { })
        self.flash.send('btn_missing', 'hide', { })

    
    def on_btn_back_event(self):
        self.on_back()

    
    def on_btn_top_up_event(self):
        if self._CerepayCenterForm__is_using_chipnpin:
            globalSession.isUsingChipnPin = True
        else:
            globalSession.isUsingChipnPin = False
        self.nextWindowID = 'CerepayTopupMainForm'
        self.windowJump = True

    
    def on_btn_transactions_event(self):
        pass

    
    def on_btn_missing_event(self):
        pass


