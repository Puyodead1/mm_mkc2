# Source Generated with Decompyle++
# File: guiQuickLoadForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V0.4
CopyRight MovieMate, Inc.

Created 2008-11-19 Vincent
vincent.chen@cereson.com

Filename:guiQuickLoadForm.py

Change Log:

'''
from guiRobotForm import RobotForm
from mcommon import *
from control import *
log = initlog('guiQuickLoadForm')

class QuickLoadForm(RobotForm):
    
    def __init__(self):
        RobotForm.__init__(self)
        self.nextWindowID = 'AdminMainForm'
        self.preWindowID = 'AdminMainForm'
        self.screenID = 'Q1'
        self.uiErrorWindowID = 'AdminMainForm'

    
    def _saveStatus(self):
        self.connProxy.saveLoadStatus(self.disc)

    
    def _initComponents(self):
        RobotForm._initComponents(self)
        self.lastCmd = ''
        self.blankRfidCount = 0
        self.loopCount = 1

    
    def _setProcessText(self, msg):
        self.flash.send('txtbox_msg', 'setText', {
            'text': msg })

    
    def _exchangeToRack(self, slotID):
        msg = _('Sending Disc To Slot %s ...') % slotID
        self._setProcessText(msg)
        log.info(msg)
        self.lastCmd = 'exchange_to_rack: %s' % slotID
        r = self.robot.doCmdSync('exchange_to_rack', {
            'slot': slotID })
        self._verifyRet(r)
        errno = r['errno']
        if errno == ROBOT_OK:
            pass
        elif errno == ROBOT_NO_DISC:
            msg = N_('Error: No Disc Found in Exchange Box.')
            raise FatalError(msg)
        elif errno == ROBOT_TIMEOUT:
            msg = N_('Error: Exchange TO Rack Time Out. Please try again later')
            raise FatalError(msg)
        elif errno == ROBOT_CARRIAGE_JAM:
            msg = N_('Error: Carriage Jam. Please check if there is anything stuck in the route. Then please contact our Tech Support.')
            raise FatalError(msg)
        else:
            msg = N_('Error: Unknown Error. %(err)s. Please restart the kiosk and try again.')
            pm = {
                'err': errno }
            raise FatalError(msg, pm)
        log.info('Exchange_To_Rack %s Done' % slotID)

    
    def _readRfid(self):
        self.lastCmd = 'read_rfid'
        msg = _('Reading RFID ... ')
        log.info(msg)
        self._setProcessText(msg)
        r = self.robot.doCmdSync('read_rfid', { })
        log.info('[Read RFID Result]: %s' % r)
        self._verifyRet(r)
        errno = r['errno']
        if errno == ROBOT_OK:
            pass
        elif errno == ROBOT_TIMEOUT:
            msg = N_('Error: RFID Read Time Out. Please try again later. If still not work, please restart the kiosk.')
            raise FatalError(msg)
        else:
            msg = N_('Error: Unknown Error %(err)s. Please restart the kiosk and try again.')
            pm = {
                'err': errno }
            raise FatalError(msg, pm)
        log.info('Read_RFID Done')

    
    def _rackToExchange(self, slotID):
        msg = _('Fetching Disc From Slot %s ...') % slotID
        self._setProcessText(msg)
        log.info(msg)
        self.lastCmd = 'rack_to_exchange: %s' % slotID
        r = self.robot.doCmdSync('rack_to_exchange', {
            'slot': slotID })
        self._verifyRet(r)
        errno = r['errno']
        if errno == ROBOT_OK:
            pass
        elif errno == ROBOT_NO_DISC:
            msg = _('Error: No Disc.')
        elif errno == ROBOT_TIMEOUT:
            msg = N_('Error: Retrieve From Slot failed. Please try again and observe the mechanical action for the possible cause.')
            raise FatalError(msg)
        elif errno == ROBOT_CARRIAGE_JAM:
            msg = N_('Error: Carriage jam. Please check if there is anything stuck in the route. Then please contact our Tech Support.')
            raise FatalError(msg)
        else:
            msg = N_('Error: Unknown error %(err)s. Please restart the kiosk and try again.')
            pm = {
                'err': errno }
            raise FatalError(msg, pm)
        log.info('Rack_To_Exchange %s Done' % slotID)

    
    def _loadOneSlot(self, slotID):
        self._rackToExchange(slotID)
        self._readRfid()
        self._exchangeToRack(slotID)
        self.loopCount += 1

    
    def _run(self):
        rankC = list(range(501, 570))
        rankD = list(range(601, 670))
        needLoadSlotList = rankC + rankD
        
        try:
            for slotID in needLoadSlotList:
                self._testOneSlot(slotID)
            
            self.nextWindowID = 'QuickLoadResultForm'
        except FatalError as ex:
            msg = _('Error happened when testing ... \n%s\nLast Command: %s') % (ex.i18nmsg, self.lastCmd)
            self._setProcessText(msg)
            log.info('[FatalError Happend]')
            self.flash.get()



