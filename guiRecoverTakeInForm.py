# Source Generated with Decompyle++
# File: guiRecoverTakeInForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V0.4
CopyRight MovieMate, Inc.

Created 2009-04-30 Vincent
vincent.chen@cereson.com

Filename:guiRecoverTakeInForm.py

Change Log:
    Andrew 2009-05-06 Finish class RecoverTakeInForm
    2011-02-10  Kitch
        add statusCode 13 to checkRfidAndSaveTrs
'''
from guiRobotForm import RobotForm
from mcommon import *
log = initlog('guiRecoverTakeInForm')
(INVALID, TORETURN, TOLOAD, TOERROR) = list(range(4))

class RecoverTakeInForm(RobotForm):
    
    def __init__(self):
        RobotForm.__init__(self)
        self.nextWindowID = 'MainForm'
        self.preWindowID = 'MainForm'
        self.screenID = 'V1'
        self.resultForm = 'MainForm'
        self.ejectDiscBackForm = 'MainForm'
        self.uiErrorWindowID = 'MainForm'
        self.timeoutSec = 20
        self.checkFlag = True

    
    def _saveStatus(self):
        
        try:
            log.info('[%s] save recovery status.' % self.windowID)
            self.connProxy.saveRecoverStatus(self.returnType, self.disc)
        except Exception:
            log.error('[%s] Conn Proxy SAVE Status Error:\n%s' % (self.windowID, traceback.format_exc()))
            msg = N_('Save recover status to DB failed.')
            raise SaveStatusError(msg)


    
    def _checkRfid(self):
        
        try:
            cart = ShoppingCart()
            self.returnType = str(self.connProxy.checkRfidAndSaveTrs(self.disc, cart))
            self.connProxy.loadRecoverRfidInfo(self.returnType, self.disc)
        except Exception:
            log.error('[%s] Conn Proxy _verifyDisc Error:\n%s' % (self.windowID, traceback.format_exc()))
            msg = N_('Conn proxy get Disc information from DB failed.')
            raise SaveStatusError(msg)

        log.info('[Return Type]: %s' % self.returnType)
        '\n        statusCode: \n        0: can not return (invalid)\n        1: can return (from this kiosk)\n        2: can return (from another kiosk)\n        3: can not return (no empty slots)\n        4: already existing (with open transaction)\n        5: already existing (without open transaction)\n        6: purchased disc (Buy-it-Now / Converted to sale already)\n        7: convert to sale right now (local)\n        8: convert to sale right now (remote)\n        9. return and load\n        10: disc remembered as unloaded\n        11: manually cleared\n        12: can not return (from another client)\n        13: can not return (250 & 500)\n\n        return: 1, 2, 4, 5, 9\n        load: 0, 6, 7, 8, 10, 11\n        exception: 3, 12, 13\n        \n        Important Notice:\n        1. If a disc is returned remotely, but has been converted to "SALE" already\n           "0" will return: "Can not return this Disc."\n        2. checkRfidAndSaveTrs() will do:\n           "verify rfid"\n           "set transaction to pending"\n           "set slot state to in"\n        '
        ret = INVALID
        if self.returnType in ('1', '2', '4', '5', '9'):
            msg = N_('A disc is found in exchange box when kiosk startup, it is put to slot %(slot)s.')
            pm = {
                'slot': self.disc.slotID }
            self.alertmsg = KioskMessage(msg, pm)
            ret = TORETURN
        elif self.returnType in ('6', '7', '8'):
            msg = N_('A disc which has been already sold is found in exchange box when kiosk startup, it is put to slot %(slot)s.')
            pm = {
                'slot': self.disc.slotID }
            self.alertmsg = KioskMessage(msg, pm)
            ret = TOLOAD
        elif self.returnType == '10':
            msg = N_('An unloaded disc is found in exchange box, it is put to slot %(slot)s.')
            pm = {
                'slot': self.disc.slotID }
            self.alertmsg = KioskMessage(msg, pm)
            ret = TOLOAD
        elif self.returnType == '11':
            msg = N_('A manually cleared disc is found in exchange box, it is put to slot %(slot)s.')
            pm = {
                'slot': self.disc.slotID }
            self.alertmsg = KioskMessage(msg, pm)
            ret = TOLOAD
        elif self.returnType == '0':
            msg = N_('An unknown disc is found in exchange box when kiosk startup, it is put to slot %(slot)s.')
            pm = {
                'slot': self.disc.slotID }
            self.alertmsg = KioskMessage(msg, pm)
            ret = TOLOAD
        elif self.returnType == '3':
            msg = N_('A disc is found in exchange box when kiosk startup, but kiosk has no empty slot for it.')
            self.alertmsg = KioskMessage(msg)
            ret = TOERROR
        elif self.returnType == '12':
            msg = N_("A disc is found in exchange box when kiosk startup, but this disc does not belong to this kiosk's owner.")
            self.alertmsg = KioskMessage(msg)
            ret = TOERROR
        elif self.returnType == '13':
            msg = N_('A disc is found in exchange box when kiosk startup, but this disc is not recognized.')
            self.alertmsg = KioskMessage(msg)
            ret = TOERROR
        
        return ret

    
    def _initComponents(self):
        if self.checkFlag == True:
            startSuccess()
            self.checkFlag = False
        
        RobotForm._initComponents(self)
        log.info('================ Recover Taken in Form starting ================')
        self.nextWindowID = 'MainForm'
        self.flash.send('txt_msg', 'setText', {
            'text': _('System initializing ...') })
        self.flash.send('swf_send_disc', 'hide', { })

    
    def _run(self):
        
        try:
            self.disc = Disc()
            
            try:
                self._readRfid()
            except WrongOutRfidError:
                ex = None
                log.info('[%s] - Read RFID failed.' % self.windowID)
                return self.nextWindowID
            except InvalidDiscRfidError:
                log.info('[%s] - get invalid rfid.' % self.windowID)

            ret = self._checkRfid()
            log.info('[%s] - %s' % (self.windowID, self.alertmsg))
            if ret == TORETURN:
                self.addAlert(INFO, self.alertmsg.message)
            elif ret == TOLOAD:
                self.addAlert(WARNING, self.alertmsg.message)
            elif ret == TOERROR:
                self.addAlert(ERROR, self.alertmsg.message)
                raise FatalError(self.alertmsg.rawmsg, self.alertmsg.param)
            
            self.flash.send('txt_msg', 'setText', {
                'text': self.alertmsg.i18nmsg })
            self.flash.send('swf_send_disc', 'show', { })
            
            try:
                self._exchangeToRack()
            except InsertException:
                ex = None
                self._insertLoop()

            self._saveStatus()
        except SaveStatusError:
            ex = None
            self.connProxy.emailAlert('PRIVATE', ex.message, critical = self.connProxy.UNCRITICAL)
            log.error('[%s] SaveStatusError:\n%s' % (self.windowID, traceback.format_exc()))
        except FatalError:
            ex = None
            log.info('[%s] FatalError:\n%s' % (self.windowID, traceback.format_exc()))
            raise 
        except Exception:
            ex = None
            log.info('[%s] Exception:\n%s' % (self.windowID, traceback.format_exc()))

        return self.nextWindowID


