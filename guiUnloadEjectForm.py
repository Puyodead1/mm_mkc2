# Source Generated with Decompyle++
# File: guiUnloadEjectForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiUnloadEjectForm.py
Unload Ejecting
Screen ID: U4

Change Log:
    2009-04-09 Vincent For make bad rfid discs unloadable

'''
import os
import traceback
from guiBaseEjectForm import BaseEjectForm
from mcommon import *
log = initlog('guiUnloadEjectForm')

class UnloadEjectForm(BaseEjectForm):
    
    def __init__(self):
        BaseEjectForm.__init__(self)
        self.nextWindowID = 'UnloadResultForm'
        self.preWindowID = 'AdminMainForm'
        self.uiErrorWindowID = 'AdminMainForm'
        self.resultForm = 'UnloadResultForm'
        self.screenID = 'U4'

    
    def _saveStatus(self, disc):
        
        try:
            self.connProxy.saveUnloadStatus(disc)
        except Exception as ex:
            log.error('[%s] Conn Proxy SAVE Status Error:\n%s' % (self.windowID, traceback.format_exc()))
            msg = N_('Operation failed, please manually put the disc back to slot %(slot)s , and retry in 5 minutes.')
            pm = {
                'slot': disc.slotID }
            raise SaveStatusError(msg, pm)


    
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
        msg = ''
        pm = { }
        if shouldBeSlotID:
            msg = N_('Unload Failed: Disc mismatch, please manually take out the disc of Slot %(s1)s, put it into Slot %(s2)s. \nIf Slot %(s2)s is occupied by another disc already, unload it to check which slot it should belong to.')
            pm = {
                's1': slotID,
                's2': shouldBeSlotID }
        else:
            msg = N_('Unload Failed: Disc mismatch, the disc of Slot %(slot)s does not belong to this kiosk, please manually take it out.')
            pm = {
                'slot': slotID }
        return KioskMessage(msg, pm)

    
    def on_invalidDiscException(self, ex):
        msg = _('RFID read failed, please change the RFID tag.')
        globalSession.param['eject_result'] += msg + '\n'
        self._exchangeEject()
        self.shoppingCart.ejectDisc(self.disc.rfid)
        self._saveStatus(self.disc)

    
    def _initComponents(self):
        BaseEjectForm._initComponents(self)
        self.shoppingCart = globalSession.shoppingCart
        logDisc = []
        for disc in self.shoppingCart.discs:
            tmpDisc = { }
            tmpDisc['slot_id'] = disc.slotID
            tmpDisc['rfid'] = disc.rfid
            tmpDisc['title'] = disc.title
            tmpDisc['coupon_code'] = disc.coupon.couponCode
            logDisc.append(tmpDisc)
        
        log.info('Unload Shopping Cart:%s' % logDisc)
        msg = _('Please wait for the disc to be ejected.')
        self.flash.send('txtbox_msg', 'setText', {
            'text': msg })
        total = str(self.shoppingCart.getSize())
        self.flash.send('txt_total', 'setText', {
            'text': total })

    
    def _run(self):
        BaseEjectForm._run(self)


