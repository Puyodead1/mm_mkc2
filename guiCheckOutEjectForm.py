# Source Generated with Decompyle++
# File: guiCheckOutEjectForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiCheckOutEjectForm.py
Checkout Result
Screen ID: R9

Change Log:

'''
import time
from guiBaseEjectForm import BaseEjectForm
from mcommon import *
log = initlog('guiCheckOutEjectForm')

class CheckOutEjectForm(BaseEjectForm):
    
    def __init__(self):
        BaseEjectForm.__init__(self)
        self.nextWindowID = 'CheckOutResultForm'
        self.preWindowID = 'ShoppingCartForm'
        self.resultForm = 'CheckOutResultForm'
        self.screenID = 'R8'
        self.timeoutSec = 60
        self.lstResponseCtrl.extend([
            'CheckOutEjectForm_ctr_all_keyboard',
            'CheckOutEjectForm_ctr_message_box'])

    
    def _saveStatus(self, disc):
        self.connProxy.saveTrs(self.shoppingCart, disc, globalSession.customer)
        self.umsProxy.setMonthlySubscptCount(globalSession.customer, disc)

    
    def dbSync(self):
        self.connProxy.dbSyncCheckOut(self.shoppingCart)

    
    def _getConflictRfidMsg(self, slotID, shouldBeSlotID):
        msg = ''
        pm = { }
        if shouldBeSlotID:
            msg = N_('Disc Mismatch: Please inform the kiosk operator: the disc of Slot %(s1)s should be in Slot %(s2)s')
            pm = {
                's1': slotID,
                's2': shouldBeSlotID }
        else:
            msg = N_('Disc Mismatch: Please inform the kiosk operator: the disc of Slot %(slot)s does not belong to this kiosk')
            pm = {
                'slot': slotID }
        return KioskMessage(msg, pm)

    
    def _initComponents(self):
        BaseEjectForm._initComponents(self)
        self.flash.send('%s_ctr_message_box' % self.windowID, 'hide', { })
        self.show_msg_box = True
        self.need_receive_more = False
        if globalSession.loginCustomer.isLogin:
            self.flash.send('ctr_btn_center', 'show', { })
            if globalSession.loginCustomer.gender == 'male':
                msg = _('Hello Mr. ')
            else:
                msg = _('Hello Ms. ')
            self.flash.send('ctr_btn_center', 'setText', {
                'text': msg + globalSession.loginCustomer.lastName })
            self.flash.send('ctr_btn_center', 'setDisabled', {
                'disabled': 'true' })
            self.showKeyboard = False
            self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'hide', { })
        else:
            self.flash.send('ctr_btn_center', 'hide', { })
            if not (globalSession.customer.email):
                self.showKeyboard = True
                self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', {
                    'type': 'email' })
            else:
                self.showKeyboard = False
                self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'hide', { })
        self._setProcessText('')
        self.shoppingCart = globalSession.shoppingCart
        logDisc = []
        for disc in self.shoppingCart.discs:
            tmpDisc = { }
            tmpDisc['slot_id'] = disc.slotID
            tmpDisc['rfid'] = disc.rfid
            tmpDisc['title'] = disc.title
            tmpDisc['coupon_code'] = disc.coupon.couponCode
            tmpDisc['gene'] = disc.gene
            logDisc.append(tmpDisc)
        
        log.info('CheckOut Shopping Cart:%s; Total Charged:%s' % (logDisc, self.shoppingCart.totalCharged))
        self.flash.send('txt_total', 'setText', {
            'text': str(self.shoppingCart.getSize()) })

    
    def getUserEmail(self):
        if self.showKeyboard == False and self.show_msg_box == False:
            return None
        
        log.info('Wait customer input email.')
        isUserInputting = False
        while True:
            if isUserInputting == False:
                timeout = 0.1
            else:
                timeout = self.timeoutSec
            self.event = self.flash.get(timeout = timeout)
            if self.event == None:
                continue
            
            if self.event:
                isUserInputting = True
                log.info('[UI Event]: %s.' % self.event)
            
            ctrlID = self.event.get('cid')
            self.on_event(ctrlID)
            if self.windowJump:
                break
            
        self.umsProxy.registerMember(globalSession.customer, self.need_receive_more)

    
    def on_CheckOutEjectForm_ctr_message_box_event(self):
        self.show_msg_box = False
        inputVal = self._getEventParam('CheckOutEjectForm_ctr_message_box', 'val')
        self.need_receive_more = False
        if inputVal == 'yes':
            self.need_receive_more = True
        
        log.info('Need receive more %s' % self.need_receive_more)
        self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'hide', { })
        self.nextWindowID = self.resultForm
        self.windowJump = True

    
    def on_CheckOutEjectForm_ctr_all_keyboard_event(self):
        eventType = self._getEventParam('CheckOutEjectForm_ctr_all_keyboard', 'type')
        if eventType == 'click':
            pass
        elif eventType == 'ok':
            emailAddr = self._getEventParam('CheckOutEjectForm_ctr_all_keyboard', 'val')
            log.info('GET EMAIL: %s' % emailAddr)
            globalSession.customer.email = emailAddr
        elif eventType == 'close':
            self.nextWindowID = self.resultForm
            self.windowJump = True
        

    
    def on_timeout(self):
        self.nextWindowID = self.resultForm
        self.windowJump = True
        self.flash.send('%s_ctr_message_box' % self.windowID, 'hide', { })

    
    def _run(self):
        BaseEjectForm._run(self)


