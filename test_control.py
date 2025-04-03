# Source Generated with Decompyle++
# File: test_control.pyc (Python 2.5)

import time
from mcommon import getRandomString
ROBOT_UNKNOWN_COMMAND = 255
ROBOT_OK = 0
ROBOT_TIMEOUT = 1
ROBOT_INVALID_RFID = 2
ROBOT_RFID_READ_ERROR = 12
ROBOT_INVALID_LABEL = 3
ROBOT_EXCHANGE_JAM = 4
ROBOT_RETRIEVE_FAIL = 5
ROBOT_INSERT_FAIL = 6
ROBOT_NO_DISC = 7
ROBOT_CARRIAGE_JAM = 8
ROBOT_BUSY = 9
ROBOT_CANCELED = 10
ROBOT_INVALID_INPUT = 11
ROBOT_ERROR_UNKNOWN = 16

class Robot:
    
    def __init__(self):
        self.returnTime = 2
        self.returnParam = {
            'errno': 0 }
        self.command = ''

    
    def getInstance(self):
        return self

    
    def _getFakeRfid(self):
        rfid = ''
        
        try:
            f = open('../test_control.rfid')
            rfid = f.readline().strip()
            f.close()
        except:
            pass

        if rfid:
            return rfid
        else:
            return getRandomString(16)

    
    def doCmdAsync(self, cmd, param, timeout = ''):
        self.command = cmd
        if cmd == 'suck_disc':
            rfid = self._getFakeRfid()
            self.returnTime = 1
            self.returnParam = {
                'errno': 0,
                'rfid': rfid }
        elif cmd == 'read_card':
            self.returnTime = 2
            self.returnParam = {
                'errno': 0,
                'track1': 'B4988820004558168^LU/PIN*LU ^0908101100000000085000000',
                'track2': '' }
        

    
    def doCmdSync(self, cmd, param = { }, timeout = ''):
        self.command = cmd
        if cmd == 'rack_to_exchange':
            time.sleep(5)
            self.returnParam = {
                'errno': 0 }
        elif cmd == 'vomit_disc':
            time.sleep(1)
            self.returnParam = {
                'errno': 0 }
        elif cmd == 'exchange_to_rack':
            time.sleep(5)
            self.returnParam = {
                'errno': 0 }
        elif cmd == 'read_rfid':
            time.sleep(1)
            self.returnParam = {
                'errno': 1 }
        elif cmd == 'goto_slot_insert':
            time.sleep(1)
            self.returnParam = {
                'errno': 0 }
        elif cmd == 'goto_exchange':
            time.sleep(1)
            self.returnParam = {
                'errno': 0 }
        
        return self.returnParam

    
    def getResult(self, r):
        time.sleep(self.returnTime)
        return self.returnParam

    
    def cancel(self):
        pass


