# Source Generated with Decompyle++
# File: guiTestingForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiTestingForm.py
Testing Processing
Screen ID: KT3

Change Log:
    2009-04-28 Vincent: Fix a bug when test multiple times
                        Make flash wait forever when error happens
    2009-04-27 Vincent: Run 1000 times
    2009-04-07 Vincent: Expand needTestSlot with 570, 670

'''
import traceback
import time
import config
from mcommon import *
from guiRobotForm import RobotForm
from control import *
log = initlog('guiTestingForm')
NEED_INIT_COUNT = 50

class TestingForm(RobotForm):
    
    def __init__(self):
        RobotForm.__init__(self)
        self.screenID = 'KT3'
        self.nextWindowID = 'TestResultForm'

    
    def _initComponents(self):
        RobotForm._initComponents(self)
        self.lastCmd = ''
        self.blankRfidCount = 0
        self.loopCount = 1

    
    def _setProcessText(self, msg):
        self.flash.send('txt_msg3', 'setText', {
            'text': msg })

    
    def _init_vertical(self):
        ''' init vertical for reseting
        '''
        self.lastCmd = 'init_vertical'
        r = self.robot.doCmdSync('init_vertical')
        self._verifyRet(r)
        errno = r['errno']
        if errno == ROBOT_OK:
            log.info('Initial Vertical Done')
            return None
        elif errno == ROBOT_TIMEOUT:
            msg = _('Error: Initial Vertical Time Out.')
        else:
            msg = _('Error: Unknown Error. %s') % errno
        raise FatalError(msg, { }, errno)

    
    def _init_machine(self):
        ''' init machine for reseting
        '''
        self.lastCmd = 'init_machine'
        r = self.robot.doCmdSync('init_machine')
        self._verifyRet(r)
        errno = r['errno']
        if errno == ROBOT_OK:
            log.info('Initial Machine Done')
            return None
        elif errno == ROBOT_TIMEOUT:
            msg = _('Error: Initial Machine Time Out.')
        else:
            msg = _('Error: Unknown Error. %s') % errno
        raise FatalError(msg, { }, errno)

    
    def _carriage_to_exchange(self):
        ''' carriage to exchange
        '''
        self.lastCmd = 'carriage_to_exchange'
        r = self.robot.doCmdSync('carriage_to_exchange')
        self._verifyRet(r)
        errno = r['errno']
        if errno == ROBOT_OK:
            log.info('Carriage To Exchange Done')
            return None
        elif errno == ROBOT_TIMEOUT:
            msg = _('Error: Carriage To Exchange Time Out.')
        elif errno == ROBOT_CARRIAGE_JAM:
            msg = _('Error: Carriage Jam. Please check the DVD rack for any discs sticking out or obstructions')
        else:
            msg = _('Error: Unknown Error. %s') % errno
        raise FatalError(msg, { }, errno)

    
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
            log.info('Exchange_To_Rack %s Done' % slotID)
            return None
        elif errno == ROBOT_NO_DISC:
            msg = _('Error: No Disc Found in Exchange Box.')
        elif errno == ROBOT_TIMEOUT:
            msg = _('Error: Exchange TO Rack Time Out.')
        elif errno == ROBOT_CARRIAGE_JAM:
            msg = _('Error: Carriage Jam. Please check the DVD rack for any discs sticking out or obstructions')
        else:
            msg = _('Error: Unknown Error. %s') % errno
        raise FatalError(msg, { }, errno)

    
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
            log.info('Read_RFID Done')
            return None
        elif errno == ROBOT_TIMEOUT:
            msg = _('Error: RFID Read Time Out.')
        else:
            msg = _('Error: Unknown Error %s') % errno
        raise FatalError(msg, { }, errno)

    
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
            log.info('Rack_To_Exchange %s Done' % slotID)
            return None
        elif errno == ROBOT_NO_DISC:
            msg = _('Error: No Disc.')
        elif errno == ROBOT_TIMEOUT:
            msg = _('Error: Retrieve From Slot failed. The disc was unable to be retrieved from the the slot, please check the slot for any physical issues.')
        elif errno == ROBOT_CARRIAGE_JAM:
            msg = _('Error: Carriage Jam. Please check the DVD rack for any discs sticking out or obstructions')
        else:
            msg = _('Error: Unknown error %s') % errno
        raise FatalError(msg, { }, errno)

    
    def _doorOpen(self):
        msg = _('Opening Exchange box ...')
        self._setProcessText(msg)
        log.info(msg)
        self.lastCmd = 'exchange_open'
        r = self.robot.doCmdSync('exchange_open', { })
        self._verifyRet(r)
        errno = r['errno']
        if errno == ROBOT_OK:
            log.info('Exchange Box opened')
            return None
        elif errno == ROBOT_TIMEOUT:
            msg = _('Error: Open Exchange Box timeout')
        elif errno == ROBOT_CARRIAGE_JAM:
            msg = _('Error: Open Exchange Box jam.')
        else:
            msg = _('Error: Unknown error %s') % errno
        raise FatalError(msg, { }, errno)

    
    def _doorClose(self):
        msg = _('Closing Exchange box ...')
        self._setProcessText(msg)
        log.info(msg)
        self.lastCmd = 'exchange_close'
        r = self.robot.doCmdSync('exchange_close', { })
        self._verifyRet(r)
        errno = r['errno']
        if errno == ROBOT_OK:
            log.info('Exchange Box Closed')
            return None
        elif errno == ROBOT_TIMEOUT:
            msg = _('Error: Close Exchange Box timeout')
        elif errno == ROBOT_CARRIAGE_JAM:
            msg = _('Error: Close Exchange Box jam.')
        else:
            msg = _('Error: Unknown error %s') % errno
        raise FatalError(msg, { }, errno)

    
    def _lrSensorTest(self):
        msg = _('LR Sensor testing ...')
        self._setProcessText(msg)
        log.info(msg)
        self.lastCmd = 'lr sensor_test'
        r = self.robot.doCmdSync('carriage_lr_sensor_usage', { })
        self._verifyRet(r)
        errno = r['errno']
        if errno == ROBOT_OK:
            log.info('lr sensor OK.bit=%s' % r['bit'])
            return None
        elif errno == ROBOT_TIMEOUT:
            msg = _('Error: test lr sensor timeout')
        else:
            msg = _('Error: Unknown error %s') % errno
        raise FatalError(msg, { }, errno)

    
    def _fbSensorTest(self):
        msg = _('FB Sensor testing ...')
        self._setProcessText(msg)
        log.info(msg)
        self.lastCmd = 'fb sensor_test'
        r = self.robot.doCmdSync('carriage_fb_sensor_usage', { })
        self._verifyRet(r)
        errno = r['errno']
        if errno == ROBOT_OK:
            log.info('fb sensor OK.value=%s' % r['value'])
            return None
        elif errno == ROBOT_TIMEOUT:
            msg = _('Error: test fb sensor timeout')
        else:
            msg = _('Error: Unknown error %s') % errno
        raise FatalError(msg, { }, errno)

    
    def _lrSensorDetect(self):
        msg = _('LR Sensor detect ...')
        self._setProcessText(msg)
        log.info(msg)
        self.lastCmd = 'lr sensor_test'
        r = self.robot.doCmdSync('carriage_lr_detect', { })
        self._verifyRet(r)
        errno = r['errno']
        if errno == ROBOT_OK:
            log.info('lr sensor OK.value=%s' % r['value'])
            return None
        elif errno == ROBOT_TIMEOUT:
            msg = _('Error: test lr sensor timeout')
        else:
            msg = _('Error: Unknown error %s') % errno
        raise FatalError(msg, { }, errno)

    
    def _sensorTest(self):
        self._lrSensorTest()
        self._fbSensorTest()
        self._lrSensorDetect()

    
    def _testOneSlot(self, slotID):
        if self.loopCount % NEED_INIT_COUNT == 0:
            self._init_vertical()
        
        self._sensorTest()
        self._exchangeToRack(slotID)
        self._rackToExchange(slotID)
        self._readRfid()
        self._doorOpen()
        self._doorClose()
        self.loopCount += 1

    
    def _run(self):
        '''
        1. Run a loop to test from slot 101 - 170,  228 - 270, 501 - 569, 601 - 669
        2. Deliver the disc out
        3. self.connProxy.setConfig({"run_test":"no"})
        '''
        if isS250():
            rankA = list(range(102, 171))
            rankB = list(range(228, 271))
            rankC = list(range(501, 571))
            rankD = list(range(601, 671))
        else:
            rankA = list(range(102, 241))
            rankB = list(range(354, 441))
            rankC = list(range(501, 639))
            rankD = list(range(701, 839))
        needTestSlotList = rankA + rankB + rankC + rankD
        
        try:
            for i in range(1, 1000):
                self._rackToExchange(101)
                self._readRfid()
                self._doorOpen()
                self._doorClose()
                for slotID in needTestSlotList:
                    self._testOneSlot(slotID)
                
                self._exchangeToRack(101)
            
            self.nextWindowID = 'TestResultForm'
        except FatalError:
            ex = None
            msg = _('Error happened when testing ... \n%s, %s\nLast Command: %s') % (ex.errCode, ex.message, self.lastCmd)
            self._setProcessText(msg)
            log.info(msg)
            log.info('[FatalError Happend] Wait forever.\n%s' % traceback.format_exc())
            while True:
                self.flash.get()



