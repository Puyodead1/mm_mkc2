# Source Generated with Decompyle++
# File: guiLoadTakeInForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V0.4
CopyRight MovieMate, Inc.

Created 2008-11-19 Vincent
vincent.chen@cereson.com

Filename:guiLoadTakeInForm.py

Change Log:

'''
from guiBaseTakeInForm import BaseTakeInForm
from mcommon import *
log = initlog('guiLoadTakeInForm')

class LoadTakeInForm(BaseTakeInForm):
    
    def __init__(self):
        BaseTakeInForm.__init__(self)
        self.nextWindowID = 'LoadResultForm'
        self.preWindowID = 'LoadDiscInfoForm'
        self.screenID = 'L5'
        self.resultForm = 'LoadResultForm'
        self.ejectDiscBackForm = 'LoadResultForm'
        self.uiErrorWindowID = 'AdminMainForm'
        self.timeoutSec = 20

    
    def _saveStatus(self):
        
        try:
            if self.loadSucess == True:
                self.connProxy.saveLoadStatus(self.disc)
        except Exception as ex:
            log.error('[%s] Conn Proxy SAVE Status Error:\n%s' % (self.windowID, traceback.format_exc()))
            msg = N_('DB operation failed, please manually take the disc back from slot %(slot)s, and retry in 5 minutes')
            pm = {
                'slot': self.disc.slotID }
            raise SaveStatusError(msg, pm)


    
    def on_dberror(self):
        pass

    
    def _guiVomitDisc(self):
        pass

    
    def _getConflictRfidMsg(self, slotID, shouldBeSlotID):
        pass

    
    def _retrieveFailRecovery(self, exin):
        msg = _('Sorry, we are unable to load this disc to slot %s, please close the disc case tight and try again.') % self.disc.slotID
        self._setProcessText(msg)
        globalSession.param['return_msg'] = msg
        self.loadSucess = False
        self._vomitDisc()

    
    def _insertFailRecovery(self, exin):
        msg = _('Sorry, we are unable to load this disc to slot %(slot)s, please check slot %(slot)s and try again.') % {
            'slot': self.disc.slotID }
        self._setProcessText(msg)
        globalSession.param['return_msg'] = msg
        self.loadSucess = False
        self._carriageToExchange()
        self._vomitDisc()

    
    def _verifyDisc(self):
        
        try:
            returnType = str(self.connProxy.isRfidLoadable(self.disc))
        except Exception as ex:
            log.error('[%s] Conn Proxy isRfidLoadable Error:\n%s' % (self.windowID, traceback.format_exc()))
            msg = N_('DB operation failed, please manually take the disc from the exchange box, and retry in 5 minutes.')
            raise SaveStatusError(msg)

        log.info('[isRfidLoadable returnType]: %s' % returnType)
        "\n        Status Code:\n        1. Normal Load\n        2. Conflict Detected, loaded already: RFID status 'in', 'reserved', 'unload'\n        3. Conflict Detected, RFID status 'out'\n        "
        if returnType == '1':
            pass
        elif returnType == '2':
            msg = N_('Load failed, the disc appears to have been loaded already. Please manually put it back to slot %(slot)s.If slot %(slot)s is occupied by another disc already, unload it to check which slot it should belong to.')
            pm = {
                'slot': self.disc.slotID }
            raise WrongInRfidError(msg, pm)
        elif returnType == '3':
            msg = N_('Load failed, the disc appears to have been rented out. Please take it back and check the transaction history of RFID %(rfid)s. ')
            pm = {
                'rfid': self.disc.rfid }
            raise WrongInRfidError(msg, pm)
        

    
    def _initComponents(self):
        BaseTakeInForm._initComponents(self)
        self.loadSucess = True
        self.disc = globalSession.disc
        log.info('[Loading Disc]: %s' % self.disc)
        self.flash.wid = self.windowID

    
    def _run(self):
        BaseTakeInForm._run(self)


