# Source Generated with Decompyle++
# File: guiRobotForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V0.4
CopyRight MovieMate, Inc.

Created 2009-02-12 Vincent
vincent.chen@cereson.com

Filename:guiRobotForm.py
Base Form for all Eject, TakeIn Forms

Change Log:
    2009-05-13 Andrew give function id "01" to _rackToRack()
    2009-05-08 Vincent Fix the error code bug
    2009-05-05 Andrew add api _readRfid()
    2009-04-30 Vincent  exchangeToRack NO_DISC will eject disk back
    2009-04-09 Vincent, Change the vomit disc\'s exception
    2009-02-24 Vincent, Change e_2_r, r_2_e timeout to 300 seconds
'''
from guiBaseForms import MMForm
from mcommon import *
from control import *
from dvr import start_record, stop_record
log = initlog('guiRobotForm')

class RobotForm(MMForm):
    
    def __init__(self):
        MMForm.__init__(self)
        robot = Robot()
        self.robot = robot.getInstance()
        self.enable_webcam = True
        self._stop_record()

    
    def _initComponents(self):
        MMForm._initComponents(self)

    
    def _verifyRet(self, ret):
        errCode = self.screenID + '-00R9000'
        if type(ret) != type({ }):
            log.error('Invalid type of ret, type: %s, ret: %s.' % (type(ret), ret))
            msg = N_('Invalid Response of Robot, Please Restart the Kiosk and Retry.')
            km = KioskMessage(msg, { })
            self.logEvent('error', errCode, km.message)
            raise FatalError(msg, { }, errCode)
        
        if 'errno' not in ret:
            log.error("Invalid value of ret, no 'errno' key found, ret: %s." % ret)
            msg = N_('Invalid Response of Robot, Please Restart the Kiosk and Retry.')
            km = KioskMessage(msg, { })
            self.logEvent('error', errCode, km.message)
            raise FatalError(msg, { }, errCode)
        

    
    def _exchangeEject(self):
        log.info('[%s] - Begin to _ejectDisk' % self.windowID)
        self._guiExchangeEject()
        ret = self.robot.doCmdSync('exchange_eject', { })
        self._verifyRet(ret)
        errno = ret['errno']
        displayErrCode = self.screenID + '-02R' + str(errno)
        if errno == ROBOT_OK:
            pass
        elif errno == ROBOT_TIMEOUT:
            msg = N_('Eject disc from Exchange Box time out, Please restart kiosk and retry.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)
        elif errno == ROBOT_EXCHANGE_JAM:
            msg = N_('Exchange Box Jam when ejecting disc, please check the exchange box for a jammed disc, once the jam is clear reboot the kiosk')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)
        else:
            msg = N_('Exchange Box Unknown Error, Please contact our tech support.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)
        log.info('[%s] - _ejectDisk finished.' % self.windowID)

    
    def _exchangeToRack(self):
        '''
        When return, if the code goes to this part,
        the status has already been changed (trs closed)
        We need to consider if we should just show the FatalErrorForm to block any more customers,
        or just showing the result page and give the customer a warning, 
        let new customers continue to use.
        '''
        slotID = self.disc.slotID
        param = {
            'slot': slotID }
        log.info('[%s] - Start to put disc back to slot %s' % (self.windowID, slotID))
        self._guiExchangeToRack()
        ret = self.robot.doCmdSync('exchange_to_rack', param, timeout = 300)
        self._verifyRet(ret)
        errno = ret['errno']
        displayErrCode = self.screenID + '-03R' + str(errno)
        if errno == ROBOT_OK:
            pass
        elif errno == ROBOT_NO_DISC:
            msg = N_('No Disc Found in Exchange Box, the disc might be dropped.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise RetrieveExchangeException(msg, { }, displayErrCode)
        elif errno == ROBOT_TIMEOUT:
            msg = N_('Robot Time Out when sending disc from exchange to slot, Please Contact our Tech Support.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)
        elif errno == ROBOT_CARRIAGE_JAM:
            msg = N_('Carriage Jam, Please check the DVD rack for any discs sticking out or obstructions.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)
        elif errno == ROBOT_RETRIEVE_FAIL:
            msg = N_('Retrieve disc from exchange failed. The disc was unable to be retrieved from the exchange box, please check the exchange box for any physical issues.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise RetrieveExchangeException(msg, { }, displayErrCode)
        elif errno == ROBOT_RETRIEVE_FATAL:
            msg = N_('Retrieve disc from exchange failed. The disc was unable to be retrieved from the exchange box, please check the exchange box for any physical issues.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)
        elif errno == ROBOT_INSERT_FAIL:
            msg = N_('Insert into Slot %(slot)s failed. Insert Failed.The disc was unable to be inserted, please check the slot for any physical issues.')
            pm = {
                'slot': slotID }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise InsertException(msg, pm, displayErrCode)
        elif errno == ROBOT_INSERT_FATAL:
            msg = N_('Insert into Slot %(slot)s failed. Insert Failed.The disc was unable to be inserted, please check the slot for any physical issues.')
            pm = {
                'slot': slotID }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        else:
            msg = N_('Retrieve from exchange box unknown error. Please restart the kiosk try again later.If you still experience issues contact Tech Supportt')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)
        log.info('[%s] - Put disc back to slot %s Finished.' % (self.windowID, slotID))

    
    def _vomitDisc(self):
        
        try:
            self._vomitDiscOnce()
        except WrongOutRfidError:
            ex = None
            log.error('WrongOutRfidError, retry')
            self._vomitDiscOnce()


    
    def _vomitDiscOnce(self):
        rfid = self.disc.rfid
        slotID = self.disc.slotID
        log.info('[%s] - [Vomit Disc Start]------------------------------------' % self.windowID)
        param = {
            'rfid': rfid }
        self._guiVomitDisc()
        ret = self.robot.doCmdSync('vomit_disc', param)
        log.info(' ****************************** [Vomit Disc Result]: %s' % ret)
        self._verifyRet(ret)
        errno = ret['errno']
        if errno == ROBOT_OK:
            pass
        elif errno == ROBOT_TIMEOUT:
            msg = N_('Robot time out when ejecting disc.')
            km = KioskMessage(msg, { })
            self.logEvent('warning', '', km.message, self.disc)
            raise WrongOutRfidError(msg, { })
        elif errno == ROBOT_INVALID_RFID:
            rfidRead = str(ret.get('rfid'))
            shouldBeSlotID = self.connProxy.getSlotIdByRfid(rfidRead)
            msg = N_('RFID mismatch: slot %(s1)s should have %(r1)s. RFID read out is %(r2)s, should in slot %(s2)s')
            pm = {
                's1': slotID,
                'r1': rfid,
                'r2': rfidRead,
                's2': shouldBeSlotID }
            km = KioskMessage(msg, pm)
            log.error(km.message)
            self.logEvent('warning', '', km.message, self.disc)
            akm = self._getConflictRfidMsg(slotID, shouldBeSlotID)
            raise WrongOutRfidError(akm.rawmsg, akm.param)
        elif errno == ROBOT_RFID_READ_ERROR:
            log.error('RFID Read Error')
            msg = N_('RFID read failed, the disc has been sent back to its slot.')
            km = KioskMessage(msg, { })
            self.logEvent('warning', '', km.message, self.disc)
            raise InvalidDiscException(msg, { })
        else:
            displayErrCode = self.screenID + '-04R' + str(errno)
            msg = N_('Eject disc from exchange box failed: Unknown error.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)
        log.info('[%s] - [Vomit Disc End]------------------------------------' % self.windowID)

    
    def _rackToExchange(self):
        slotID = self.disc.slotID
        rfid = self.disc.rfid
        param = {
            'slot': slotID }
        log.info('[%s] - [Retrieve From Slot Start]------------------------------------' % self.windowID)
        log.info('[%s] - Start to Retrieve the disc %s from slot %s' % (self.windowID, rfid, slotID))
        self._guiRackToExchange()
        ret = self.robot.doCmdSync('rack_to_exchange', param, timeout = 300)
        self._verifyRet(ret)
        errno = ret['errno']
        if errno == ROBOT_OK:
            log.info('[%s] - Retrieve from slot %s OK.' % (self.windowID, slotID))
        elif errno == ROBOT_NO_DISC:
            displayErrCode = self.screenID + '-05R' + str(errno)
            msg = N_('Retrieve from slot %(slot)s failed: No Disc.')
            pm = {
                'errCode': displayErrCode,
                'slot': slotID }
            km = KioskMessage(msg, pm)
            self.logEvent('warning', displayErrCode, km.message, self.disc)
            raise RetreiveNoDiscError(msg, pm, displayErrCode)
        elif errno == ROBOT_TIMEOUT:
            displayErrCode = self.screenID + '-05R' + str(errno)
            msg = N_('Retrieve from slot %(slot)s failed: Time out.')
            pm = {
                'slot': slotID }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        elif errno == ROBOT_CARRIAGE_JAM:
            displayErrCode = self.screenID + '-05R' + str(errno)
            msg = N_('Retrieve disc from slot %(slot)s to Exchange failed: Carriage jam.')
            pm = {
                'slot': slotID }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        elif errno == ROBOT_RETRIEVE_FAIL:
            displayErrCode = self.screenID + '-05R' + str(errno)
            msg = N_('Retrieve from slot %(slot)s failed. Insert or Retrieve failure.')
            pm = {
                'slot': slotID }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise RetreiveFailError(msg, pm, displayErrCode)
        elif errno == ROBOT_RETRIEVE_FATAL:
            displayErrCode = self.screenID + '-05R' + str(errno)
            msg = N_('Retrieve disc from slot %(slot)s failed. Insert or Retrieve failure.')
            pm = {
                'slot': slotID }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        elif errno == ROBOT_INSERT_FAIL:
            displayErrCode = self.screenID + '-05R' + str(errno)
            msg = N_('Error: Retrieve from slot %(slot)s failed: Insert Failed.The disc was unable to be inserted, please check the slot for any physical issues.')
            pm = {
                'slot': slotID }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise InsertException(msg, pm, displayErrCode)
        elif errno == ROBOT_INSERT_FATAL:
            displayErrCode = self.screenID + '-05R' + str(errno)
            msg = N_('Retrieve disc from slot %(slot)s to exchange failed: Insert to Exchange failed. Please try restart the kiosk.')
            pm = {
                'slot': slotID }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        else:
            displayErrCode = self.screenID + '-05R' + str(errno)
            msg = N_('Retrieve from slot %(slot)s failed: Unknown error: %(err)s')
            pm = {
                'slot': slotID,
                'err': errno }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        log.info('[%s] - [Retrieve From Slot End]------------------------------------' % self.windowID)

    
    def _goToExchange(self):
        log.info('[%s] - [goToExchange Start]------------------------------------' % self.windowID)
        self._guiGoToExchange()
        ret = self.robot.doCmdSync('goto_exchange', timeout = 300)
        self._verifyRet(ret)
        errno = ret['errno']
        if errno == ROBOT_OK:
            log.info('[%s] - goto_exchange OK.' % self.windowID)
        elif errno == ROBOT_TIMEOUT:
            displayErrCode = self.screenID + '-06R' + str(errno)
            msg = N_('Move carriage to Exchange failed: Time out. Please try restart the kiosk.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)
        elif errno == ROBOT_CARRIAGE_JAM:
            displayErrCode = self.screenID + '-06R' + str(errno)
            msg = N_('Move carriage to Exchange failed: carriage jam.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)
        else:
            displayErrCode = self.screenID + '-06R' + str(errno)
            msg = N_('Move carriage to Exchange failed: Unknown error: %(err)s. Please try restart the kiosk.')
            pm = {
                'err': errno }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        log.info('[%s] - [goToExchange End]------------------------------------' % self.windowID)

    
    def _goToSlotInsert(self, slotID):
        param = {
            'slot': slotID }
        log.info('[%s] - Start to goToSlotInsert %s' % (self.windowID, slotID))
        self._guiGoToSlotInsert(slotID)
        ret = self.robot.doCmdSync('goto_slot_insert', param)
        self._verifyRet(ret)
        errno = ret['errno']
        if errno == ROBOT_OK:
            log.info('[%s] - goToSlotInsert %s OK.' % (self.windowID, slotID))
        elif errno == ROBOT_TIMEOUT:
            displayErrCode = self.screenID + '-07R' + str(ROBOT_TIMEOUT)
            msg = N_('Insert disc to Slot %(slot)s failed: Time out. Please try restart the kiosk')
            pm = {
                'slot': slotID }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        elif errno == ROBOT_CARRIAGE_JAM:
            displayErrCode = self.screenID + '-07R' + str(ROBOT_CARRIAGE_JAM)
            msg = N_('Insert disc to Slot %(slot)s failed: Carriage jam.')
            pm = {
                'slot': slotID }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        else:
            displayErrCode = self.screenID + '-07R' + str(errno)
            msg = N_('Insert disc to Slot %(slot)s failed: Unknown error: %(err)s. Please try restart the kiosk.')
            pm = {
                'slot': slotID,
                'err': errno }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        log.info('[%s] - [goToSlotInsert End]------------------------------------' % self.windowID)

    
    def _rackToRack(self, fromSlot, toSlot):
        log.info('[%s] Put disc from slot %s to slot %s' % (self.windowID, fromSlot, toSlot))
        param = {
            'src_slot': fromSlot,
            'dest_slot': toSlot }
        ret = self.robot.doCmdSync('rack_to_rack', param, timeout = 300)
        self._verifyRet(ret)
        errno = ret['errno']
        if errno == ROBOT_OK:
            pass
        elif errno == ROBOT_TIMEOUT:
            displayErrCode = self.screenID + '-01R' + str(errno)
            msg = N_('Retrieve from slot %(fs)s to slot %(ts)s failed: Time out.')
            pm = {
                'fs': fromSlot,
                'ts': toSlot }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        elif errno == ROBOT_CARRIAGE_JAM:
            displayErrCode = self.screenID + '-01R' + str(errno)
            msg = N_('Error: Carriage Jam. Please check the DVD rack for any discs sticking out or obstructions.')
            pm = {
                'fs': fromSlot,
                'ts': toSlot }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        elif errno == ROBOT_NO_DISC:
            displayErrCode = self.screenID + '-01R' + str(errno)
            msg = N_('Retrieve from slot %(fromSlot)s to slot %(toSlot)s failed: No Disc.')
            pm = {
                'fromSlot': fromSlot,
                'toSlot': toSlot }
            km = KioskMessage(msg, pm)
            self.logEvent('error', '', km.message, self.disc)
            raise RetreiveNoDiscError(msg, pm, displayErrCode)
        elif errno == ROBOT_INSERT_FAIL:
            displayErrCode = self.screenID + '-01R' + str(errno)
            msg = N_('Retrieve from slot %(fs)s to slot %(ts)s failed: Insert Fail.')
            pm = {
                'fs': fromSlot,
                'ts': toSlot }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise InsertException(msg, pm, displayErrCode)
        elif errno == ROBOT_INSERT_FATAL:
            displayErrCode = self.screenID + '-01R' + str(errno)
            msg = N_('Retrieve from slot %(fs)s to slot %(ts)s failed: Insert failure. Please try restart the kiosk.')
            pm = {
                'fs': fromSlot,
                'ts': toSlot }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        elif errno == ROBOT_RETRIEVE_FAIL:
            displayErrCode = self.screenID + '-01R' + str(errno)
            msg = N_('Retrieve from slot %(fs)s to slot %(ts)s failed: Retrieve Fail.')
            pm = {
                'fs': fromSlot,
                'ts': toSlot }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise RetreiveFailError(msg, pm, displayErrCode)
        elif errno == ROBOT_RETRIEVE_FATAL:
            displayErrCode = self.screenID + '-01R' + str(errno)
            msg = N_('Retrieve from slot %(fs)s to slot %(ts)s failed: Retrieve Fatal.')
            pm = {
                'fs': fromSlot,
                'ts': toSlot }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        else:
            displayErrCode = self.screenID + '-01R' + str(errno)
            msg = N_('Retrieve from slot %(fs)s to slot %(ts)s failed: Unknown Error.')
            pm = {
                'fs': fromSlot,
                'ts': toSlot }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        log.info('[%s] - [RackToRack End]------------------------------------' % self.windowID)

    
    def _carriageToExchange(self):
        log.info('[%s] - [Take the disc on carriage back to exchange box]-----------------------' % self.windowID)
        param = {
            'slot': '-1' }
        ret = self.robot.doCmdSync('rack_to_exchange', param, timeout = 300)
        self._verifyRet(ret)
        errno = ret['errno']
        if errno == ROBOT_OK:
            log.info('[%s] - carriage to exchange finish.' % self.windowID)
        elif errno == ROBOT_NO_DISC:
            displayErrCode = self.screenID + '-09R' + str(errno)
            msg = N_('Carriage to Exchange failed: No Disc.')
            km = KioskMessage(msg, { })
            self.logEvent('warning', displayErrCode, km.message, self.disc)
            raise RetreiveNoDiscError(msg, { }, displayErrCode)
        elif errno == ROBOT_TIMEOUT:
            displayErrCode = self.screenID + '-09R' + str(errno)
            msg = N_('Send disc from Carriage to Exchange failed: Time out.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)
        elif errno == ROBOT_CARRIAGE_JAM:
            displayErrCode = self.screenID + '-09R' + str(errno)
            msg = N_('Send disc from Carriage to Exchange failed: Carriage jam.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)
        elif errno == ROBOT_RETRIEVE_FAIL:
            displayErrCode = self.screenID + '-09R' + str(errno)
            msg = N_('Send disc from Carriage to Exchange failed: Retrieve failure.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise RetrieveExchangeException(msg, { }, displayErrCode)
        elif errno == ROBOT_RETRIEVE_FATAL:
            displayErrCode = self.screenID + '-09R' + str(errno)
            msg = N_('Send disc from Carriage to Exchange failed: Retrieve failure. Please try restart the kiosk.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)
        elif errno == ROBOT_INSERT_FAIL:
            displayErrCode = self.screenID + '-09R' + str(errno)
            msg = N_('Send disc from Carriage to Exchange failed:The disc was unable to be inserted into the exchange box.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise InsertException(msg, { }, displayErrCode)
        elif errno == ROBOT_INSERT_FATAL:
            displayErrCode = self.screenID + '-09R' + str(errno)
            msg = N_('Send disc from Carriage to Exchange failed: The kiosk has experienced a jam, please clear the jam and reboot the kiosk')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)
        else:
            displayErrCode = self.screenID + '-09R' + str(errno)
            msg = N_('Send disc from Carriage to Exchange failed: Unknown error: %(err)s.')
            pm = {
                'err': errno }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        log.info('[%s] - [Carriage to Exchange End]------------------------------------' % self.windowID)

    
    def _carriageToRack(self):
        slotID = self.disc.slotID
        log.info('[%s] Put disc on carriage to slot %s' % (self.windowID, slotID))
        param = {
            'src_slot': '-1',
            'dest_slot': slotID }
        ret = self.robot.doCmdSync('rack_to_rack', param, timeout = 300)
        self._verifyRet(ret)
        errno = ret['errno']
        if errno == ROBOT_OK:
            pass
        elif errno == ROBOT_TIMEOUT:
            displayErrCode = self.screenID + '-09R' + str(errno)
            msg = N_('Put disc from carriage to slot %(slot)s failed: Time out.')
            pm = {
                'slot': slotID }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        elif errno == ROBOT_CARRIAGE_JAM:
            displayErrCode = self.screenID + '-09R' + str(errno)
            msg = N_('Put disc from carriage to slot %(slot)s failed: Carriage Jam.')
            pm = {
                'slot': slotID }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        elif errno == ROBOT_NO_DISC:
            displayErrCode = self.screenID + '-09R' + str(errno)
            msg = N_('Put disc from carriage to slot %(slot)s failed: No Disc.')
            pm = {
                'slot': slotID }
            km = KioskMessage(msg, pm)
            self.logEvent('error', '', km.message, self.disc)
            raise RetreiveNoDiscError(msg, pm, displayErrCode)
        elif errno == ROBOT_INSERT_FAIL:
            displayErrCode = self.screenID + '-09R' + str(errno)
            msg = N_('Put disc from carriage to slot %(slot)s failed: Insert Fail.')
            pm = {
                'slot': slotID }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise InsertException(msg, pm, displayErrCode)
        elif errno == ROBOT_INSERT_FATAL:
            displayErrCode = self.screenID + '-09R' + str(errno)
            msg = N_('Put disc from carriage to slot %(slot)s failed: Insert Fatal.')
            pm = {
                'slot': slotID }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        elif errno == ROBOT_RETRIEVE_FAIL:
            displayErrCode = self.screenID + '-09R' + str(errno)
            msg = N_('Put disc from carriage to slot %(slot)s failed: Retrieve Fail.')
            pm = {
                'slot': slotID }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise RetreiveFailError(msg, pm, displayErrCode)
        elif errno == ROBOT_RETRIEVE_FATAL:
            displayErrCode = self.screenID + '-09R' + str(errno)
            msg = N_('Put disc from carriage to slot %(slot)s failed: Retrieve Fatal.')
            pm = {
                'slot': slotID }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        else:
            displayErrCode = self.screenID + '-09R' + str(errno)
            msg = N_('Put disc from carriage to slot %(slot)s failed: Unknown Error.')
            pm = {
                'slot': slotID }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        log.info('[%s] - [CarriageToRack End]------------------------------------' % self.windowID)

    
    def _cancel(self, r):
        self.robot.cancel()
        log.info('[Robot Cancel Called]')
        self._guiCancel()
        retFromRobot = self.robot.getResult(r, timeout = 600)
        if retFromRobot:
            self._verifyRet(retFromRobot)
            errno = retFromRobot['errno']
            if errno == ROBOT_OK:
                pass
            elif errno == ROBOT_TIMEOUT:
                log.warning('Cancel Time Out')
            
        else:
            log.warning('Cancel Time Out, None return')
        self.nextWindowID = self.preWindowID

    
    def _compareRfid(self, retFromRobot):
        self._verifyRet(retFromRobot)
        errno = retFromRobot['errno']
        self.disc.rfid = retFromRobot.get('rfid')
        if errno == ROBOT_OK:
            pass
        elif errno == ROBOT_TIMEOUT:
            msg = N_('Security Tag Read Failed\nPlease take the disc back.')
            km = KioskMessage(msg, { })
            self.logEvent('warning', '', km.message, self.disc)
            raise WrongInRfidError(msg)
        elif errno == ROBOT_INVALID_RFID:
            msg = N_('Invalid Security Tag\nPlease take the disc back.')
            km = KioskMessage(msg, { })
            self.logEvent('warning', '', km.message, self.disc)
            raise InvalidDiscException(msg)
        elif errno == ROBOT_RFID_READ_ERROR:
            msg = N_('Read Rfid failed\nPlease take the disc back.')
            km = KioskMessage(msg, { })
            self.logEvent('warning', '', km.message, self.disc)
            raise InvalidDiscException(msg)
        elif errno == ROBOT_INVALID_LABEL:
            msg = N_('Invalid Label\nPlease take the disc back.')
            km = KioskMessage(msg, { })
            self.logEvent('warning', '', km.message, self.disc)
            raise WrongInRfidError(msg)
        else:
            msg = N_('Invalid Disc: Unknown Error\nPlease take the disc back.')
            km = KioskMessage(msg, { })
            self.logEvent('warning', '', km.message, self.disc)
            raise WrongInRfidError(msg)
        self._verifyDisc()
        msg = _('Please Wait \nwhile the disk is checked and reloaded back into the inventory.')
        km = KioskMessage(msg, { })
        self._setProcessText(km.i18nmsg)

    
    def _setProcessText(self, msg):
        self.flash.send('txtbox_msg', 'setText', {
            'text': msg })

    
    def _guiExchangeEject(self):
        pass

    
    def _guiExchangeToRack(self):
        pass

    
    def _guiRackToExchange(self):
        pass

    
    def _guiVomitDisc(self):
        pass

    
    def _guiGoToExchange(self):
        pass

    
    def _guiGoToSlotInsert(self, slotID):
        pass

    
    def _guiCancel(self):
        pass

    
    def _insertLoop(self):
        lstSlotID = self.connProxy.getAvailableSlotIdList()
        oldSlot = self.disc.slotID
        success = False
        for newslot in lstSlotID:
            if str(newslot) == str(oldSlot):
                continue
            
            if self.disc.slotID:
                self.connProxy.moveSlot(self.disc.slotID, newslot)
                self.connProxy.setBadSlot(self.disc.slotID)
                msg = N_('Insert disc into slot %(slot)s failed, slot %(slot)s is set to bad. Disc will be insert into slot %(ns)s.') % {
                    'slot': self.disc.slotID,
                    'ns': newslot }
                log.error(msg)
                self.addAlert(WARNING, msg)
                self.connProxy.emailAlert('PRIVATE', msg, critical = self.connProxy.UNCRITICAL)
            
            self.disc.slotID = newslot
            
            try:
                self._carriageToRack()
            except InsertException:
                ex = None
                log.error(str(ex))
                continue

            success = True
        
        if success == False:
            displayErrCode = self.screenID + '-ilR' + '0000'
            tmpmsg = N_('Insert disc into slot %(slot)s failed and there is NO EMPTY SLOT to insert disc.')
            pm = {
                'slot': self.disc.slotID }
            msg = KioskMessage(tmpmsg, pm)
            self.addAlert(ERROR, msg.message)
            self.logEvent('error', displayErrCode, msg.message, self.disc)
            raise FatalError(msg.rawmsg, msg.param, displayErrCode)
        

    
    def on_cancel(self):
        pass

    
    def _readRfid(self):
        ret = self.robot.doCmdSync('read_rfid', { })
        self._verifyRet(ret)
        errno = ret['errno']
        self.disc.rfid = ret.get('rfid')
        if errno == ROBOT_OK:
            pass
        elif errno == ROBOT_TIMEOUT:
            displayErrCode = self.screenID + '-08R' + str(errno)
            msg = N_('RFID Read Time Out.')
            km = KioskMessage(msg, { })
            if self.windowID != 'RecoverTakeInForm':
                self.logEvent('warning', displayErrCode, km.message, self.disc)
            
            raise WrongOutRfidError(msg)
        elif errno == ROBOT_RFID_READ_ERROR:
            displayErrCode = self.screenID + '-08R' + str(errno)
            msg = N_('RFID Read Error.')
            km = KioskMessage(msg, { })
            if self.windowID != 'RecoverTakeInForm':
                self.logEvent('warning', displayErrCode, km.message, self.disc)
            
            raise WrongOutRfidError(msg)
        elif errno == ROBOT_INVALID_RFID:
            displayErrCode = self.screenID + '-08R' + str(errno)
            msg = N_('Invalid Rfid.')
            km = KioskMessage(msg, { })
            if self.windowID != 'RecoverTakeInForm':
                self.logEvent('warning', displayErrCode, km.message, self.disc)
            
            raise InvalidDiscRfidError(msg)
        else:
            displayErrCode = self.screenID + '-08R' + str(errno)
            msg = N_('Read rfid unknown Error %(err)s')
            pm = {
                'err': errno }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)

    
    def logEvent(self, logtype, errcode, errmsg, disc = None):
        if not disc:
            disc = Disc()
        
        if disc.rfid and not (disc.upc):
            dict = self.connProxy._getRfidInfoByRfid(disc.rfid)
            if not dict.get('upc'):
                pass
            disc.upc = ''
            if not dict.get('title'):
                pass
            disc.title = ''
        
        if not errcode:
            d5 = errmsg
        else:
            d5 = '%s:%s' % (errcode, errmsg)
        self.connProxy.logMkcEvent(category = 'system', action = logtype, data1 = disc.slotID, data2 = disc.rfid, data3 = disc.upc, data4 = disc.title, data5 = d5)

    
    def _need_not_record(self):
        return self.windowID not in [
            'ReturnTakeInForm',
            'CheckOutEjectForm']

    
    def let_lamp(self, status):
        if status not in [
            'on',
            'off']:
            return None
        else:
            for i in range(3):
                sts = self.robot._do_cmd('robot io illumination %s' % status)
                if sts[0] == 'ok':
                    break
                
            

    
    def _start_record(self, path):
        if self._need_not_record():
            return None
        
        if self.connProxy._getConfigByKey('enable_webcam') == 'no':
            self.enable_webcam = False
            return None
        else:
            self.enable_webcam = True
        self.let_lamp('on')
        for i in range(3):
            ret = start_record(path)
            if ret == 0:
                break
            else:
                stop_record()
        

    
    def _stop_record(self):
        if self._need_not_record():
            return None
        
        if not (self.enable_webcam):
            return None
        
        stop_record()
        self.let_lamp('off')

    
    def save_failed_trs(self, disc, err_msg, action_time, action_type, today, vname, kiosk_id):
        if self._need_not_record():
            return None
        
        if not (self.enable_webcam):
            return None
        
        params = { }
        params['title'] = disc.title
        params['rfid'] = disc.rfid
        params['upc'] = disc.upc
        params['action_time'] = action_time
        params['action_type'] = action_type
        params['slot_id'] = disc.slotID
        params['cc_display'] = globalSession.customer.ccDisplay
        params['video_name'] = os.path.join(today, vname)
        params['video_url'] = os.path.join(today, kiosk_id, vname)
        params['error_msg'] = err_msg
        self.connProxy.update_failed_trs(params)


