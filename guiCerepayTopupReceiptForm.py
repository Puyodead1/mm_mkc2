# Source Generated with Decompyle++
# File: guiCerepayTopupReceiptForm.pyc (Python 2.5)

import traceback
from guiBaseForms import CustomerForm
from mcommon import *
from proxy.upg_proxy import UPGProxy
log = initlog('CerepayTopupReceiptForm')

class CerepayTopupReceiptForm(CustomerForm):
    
    def __init__(self):
        super(CerepayTopupReceiptForm, self).__init__()
        self.nextWindowID = 'CerepayCenterForm'
        self.preWindowID = 'CerepayTopupSwipeChinPinForm'
        self.uiErrorWindowID = 'CerepayCenterForm'
        self.timeoutSec = 180
        self.screenID = 'M10'
        self.lstResponseCtrl.extend([
            'btn_back',
            'btn_finish',
            'btn_email'])

    
    def _initComponents(self):
        super(CerepayTopupReceiptForm, self)._initComponents()
        cerepay_customer = Customer(ccNumber = globalSession.loginCustomer.cerepayCard.number)
        (status, __) = self.umsProxy.setMemberDetail(cerepay_customer, ShoppingCart())
        if status in ('0', '1') and cerepay_customer.isMember:
            cerepayCard = cerepay_customer.cerepayCard
        else:
            cerepayCard = globalSession.loginCustomer.cerepayCard
        amount_fmt = self.connProxy.getDefaultCurrencySymbol() + '%.2f'
        transaction_uuid = globalSession.cerepayTopupTransactionUUID
        info = []
        info.append({
            'title': N_('Transaction Type'),
            'info': 'TOP UP' })
        info.append({
            'title': N_('Transaction UUID'),
            'info': transaction_uuid })
        info.append({
            'title': _('Card Number'),
            'info': maskCard(cerepayCard.number) })
        info.append({
            'title': N_('Topup Amount'),
            'info': amount_fmt % globalSession.cerepayTopupAmount })
        info.append({
            'title': _('Balance'),
            'info': amount_fmt % cerepayCard.balance })
        info.append({
            'title': _('Hold Amount'),
            'info': amount_fmt % cerepayCard.holdingAmt })
        info.append({
            'title': _('Actual Balance'),
            'info': amount_fmt % (cerepayCard.balance - cerepayCard.holdingAmt) })
        info.append({
            'title': N_('Cerepay Account'),
            'info': '%s' % cerepayCard.email })
        if globalSession.isUsingChipnPin:
            info.append({
                'title': N_('Topup Method'),
                'info': 'Chin and Pin' })
        else:
            info.append({
                'title': N_('Topup Method'),
                'info': 'Credit Card' })
        self.flash.send('info_list', 'setCerepayCenterList', {
            'info_list': info })

    
    def on_btn_email_event(self):
        
        try:
            upg_proxy = UPGProxy()
            upg_proxy.send_topup_receipt(globalSession.cerepayTopupTransactionUUID)
        except Exception:
            ex = None
            log.error(str(ex))
            log.error(traceback.format_exc())

        self.nextWindowID = 'CerepayCenterForm'
        self.windowJump = True

    
    def on_btn_finish_event(self):
        self.nextWindowID = 'CerepayCenterForm'
        self.windowJump = True


