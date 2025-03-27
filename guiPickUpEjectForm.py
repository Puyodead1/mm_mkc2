# Source Generated with Decompyle++
# File: guiPickUpEjectForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiPickUpEjectForm.py
Pick Up Eject
Screen ID: P3

Change Log:

'''
import time
from guiBaseEjectForm import BaseEjectForm
from mcommon import *
log = initlog('guiPickUpEjectForm')

class PickUpEjectForm(BaseEjectForm):
    
    def __init__(self):
        BaseEjectForm.__init__(self)
        self.nextWindowID = 'PickUpResultForm'
        self.preWindowID = 'PickUpDiscListForm'
        self.resultForm = 'PickUpResultForm'
        self.screenID = 'P3'

    
    def _saveStatus(self, disc):
        self.connProxy.updateDiscStatePickup(disc)
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
        else:
            self.flash.send('ctr_btn_center', 'hide', { })
        self._setProcessText('')
        self.shoppingCart = globalSession.pickupCart
        logDisc = []
        for disc in self.shoppingCart.discs:
            tmpDisc = { }
            tmpDisc['slot_id'] = disc.slotID
            tmpDisc['rfid'] = disc.rfid
            tmpDisc['title'] = disc.title
            tmpDisc['coupon_code'] = disc.coupon.couponCode
            logDisc.append(tmpDisc)
        
        log.info('Pick Up Shopping Cart:%s' % logDisc)
        self.flash.send('txt_total', 'setText', {
            'text': str(self.shoppingCart.getSize()) })

    
    def _run(self):
        BaseEjectForm._run(self)


