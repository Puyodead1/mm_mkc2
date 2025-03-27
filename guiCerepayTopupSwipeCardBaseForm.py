# Source Generated with Decompyle++
# File: guiCerepayTopupSwipeCardBaseForm.pyc (Python 2.5)

import traceback
from guiBaseForms import CustomerForm
from mcommon import *
from proxy.upg_proxy import UPGProxy
log = initlog('CerepayTopupSwipeCardBaseForm')
_text = _('Insert your Debit or Credit Card into the Card Reader to side of kiosk and enter your PIN to complete transaction')
_topup_status_dict = {
    '0': N_('Topup Successfully'),
    '1': N_('Internal Error'),
    '2': N_('Network Error'),
    '3': N_('UPG account do not support CerePay, or CerePay account is frozen.'),
    '4': N_('CerePay config of upg account do not match'),
    '5': N_('Not CerePay card'),
    '6': N_('Charge DECLINE'),
    '7': N_('Member does not exis') }

def _object2dict(obj):
    return {x: str(getattr(obj, x)) for x in dir(obj) if not x.startswith('_')}


class CerepayError(Exception):
    pass


class CerepayTopupSwipeCardBaseForm(CustomerForm):
    
    def __init__(self):
        super(CerepayTopupSwipeCardBaseForm, self).__init__()
        self.nextWindowID = 'CerepayCenterForm'
        self.preWindowID = 'CerepayTopupMainForm'
        self.lstResponseCtrl.extend([
            self._ctr_msg_box_string])

    
    def _initComponents(self):
        super(CerepayTopupSwipeCardBaseForm, self)._initComponents()
        self.timeoutSec = 120
        self.flash.send('ctr_btn_center', 'setDisabled', {
            'disabled': 'true' })
        self.flash.send('swf_swipe_card', 'show', { })
        self.flash.send('txt_cart_info_label', 'setText', {
            'text': _text })
        self._CerepayTopupSwipeCardBaseForm__upg_proxy = UPGProxy()
        self._CerepayTopupSwipeCardBaseForm__close_message_box()

    
    def _ctr_msg_box_string(self):
        return '%s_ctr_message_box' % self.windowID

    _ctr_msg_box_string = property(_ctr_msg_box_string)
    
    def __close_message_box(self):
        self.flash.send(self._ctr_msg_box_string, 'close', { })

    
    def __show_message_box(self, msg_dict = { }):
        self.flash.send(self._ctr_msg_box_string, 'show', msg_dict)

    
    def _topup_cerepay_card(self):
        log.info('entering topup_cerepay_card_from_chin_pin')
        cerepay_customer = Customer(ccNumber = globalSession.loginCustomer.cerepayCard.number)
        log.info('Cerepay Card Number : ' + str(cerepay_customer.ccNum))
        log.info('Topup amount is : ' + str(globalSession.cerepayTopupAmount))
        log.info('Cerepay customer is : ' + str(_object2dict(cerepay_customer)))
        (status, msg, trs_uuid, queue_id) = self._CerepayTopupSwipeCardBaseForm__upg_proxy.topup_for_cerepay(chargeCustomer = Customer(), cerepayCustomer = cerepay_customer, amount = globalSession.cerepayTopupAmount)
        log.info('topup_for_cerepay return value is : (%s,%s,%s,%s)' % (status, msg, trs_uuid, queue_id))
        if str(status) != '0':
            raise ChinPinTopupException(_topup_status_dict.get(str(status), N_('Unknown error.')))
        elif trs_uuid:
            globalSession.cerepayTopupTransactionUUID = trs_uuid
        else:
            globalSession.cerepayTopupQueueID = queue_id
            raise CerepayError

    
    def _run(self):
        
        try:
            log.info('wait customer swipe card')
            self._topup_cerepay_card()
            self.nextWindowID = 'CerepayTopupReceiptForm'
            self.windowJump = True
            globalSession.isCerepayCardInfoDirty = True
            return None
        except CerepayError:
            ex = None
            self.nextWindowID = 'CerepayTopupErrorForm'
            self.windowJump = True
            globalSession.isCerepayCardInfoDirty = True
            return None
        except ChinPinTopupException:
            ex = None
            log.error(str(ex.message))
            log.error(traceback.format_exc())
            self._CerepayTopupSwipeCardBaseForm__show_message_box({
                'message': ex.i18nmsg,
                'type': 'alert' })
        except DebitCardTimeOut:
            ex = None
            self.timeoutSec = 0
            log.error('getResForSA reach time out')
        except Exception:
            ex = None
            log.error(str(ex))
            log.error(traceback.format_exc())
            self._CerepayTopupSwipeCardBaseForm__show_message_box({
                'message': str(ex),
                'type': 'alert' })

        super(CerepayTopupSwipeCardBaseForm, self)._run()

    
    def on_btn_cancel_event(self):
        self.nextWindowID = 'CerepayCenterForm'
        self.windowJump = True

    
    def on_btn_back_event(self):
        self.nextWindowID = 'CerepayTopupMainForm'
        self.windowJump = True


