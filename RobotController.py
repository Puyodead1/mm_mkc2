# Source Generated with Decompyle++
# File: RobotController.pyc (Python 2.5)

from robot import *

class RobotException(Exception):
    
    def __init__(self, message, errCode):
        Exception.__init__(self, message)
        self.errCode = errCode



class NoDiscException(Exception):
    
    def __init__(self, message, errCode):
        Exception.__init__(self, message)
        self.errCode = errCode



class InsertDiscException(Exception):
    
    def __init__(self, message, errCode):
        Exception.__init__(self, message)
        self.errCode = errCode



class RobotController:
    def __init__(self, log, taskid):
        robot = Robot()
        self.robot = robot.getInstance()
        self.log = log
        self.taskid = taskid

    
    def __del__(self):
        del self.robot

    
    def _errorCheck(self, ret, actmsg, funid):
        if type(ret) != type({ }):
            self.log.error('Invalid type of ret, type: %s, ret: %s.' % (type(ret), ret))
            msg = _('Invalid Response of Robot, Please Restart the Kiosk and Retry.')
            errCode = 'RA-00R9000'
            raise RobotException(msg, errCode)
        
        if 'errno' not in ret:
            self.log.error("Invalid value of ret, no 'errno' key found, ret: %s." % ret)
            msg = _('Invalid Response of Robot, Please Restart the Kiosk and Retry.')
            errCode = 'RA-00R9000'
            raise RobotException(msg, errCode)
        
        errno = ret['errno']
        if errno == ROBOT_OK:
            pass
        elif errno == ROBOT_NO_DISC:
            msg = _('Error: %s: No Disc.') % actmsg
            errCode = self.taskid + funid + 'R' + str(errno)
            self.log.info(msg)
            raise NoDiscException(msg, errCode)
        elif errno == ROBOT_TIMEOUT:
            msg = _('Error: %s: Timeout.') % actmsg
            errCode = self.taskid + funid + 'R' + str(errno)
            self.log.info(msg)
            raise RobotException(msg, errCode)
        elif errno == ROBOT_CARRIAGE_JAM:
            msg = _('Error: %s: Carriage Jam.') % actmsg
            errCode = self.taskid + funid + 'R' + str(errno)
            self.log.info(msg)
            raise RobotException(msg, errCode)
        elif errno == ROBOT_RETRIEVE_FAIL:
            msg = _('Error: %s: Retrieve fail.') % actmsg
            errCode = self.taskid + funid + 'R' + str(errno)
            self.log.info(msg)
            raise NoDiscException(msg, errCode)
        elif errno == ROBOT_INSERT_FAIL:
            msg = _('Error: %s: Insert fail.') % actmsg
            errCode = self.taskid + funid + 'R' + str(errno)
            self.log.info(msg)
            raise InsertDiscException(msg, errCode)
        elif errno == ROBOT_INSERT_FATAL:
            msg = _('Error: %s: Insert fatal.') % actmsg
            errCode = self.taskid + funid + 'R' + str(errno)
            self.log.info(msg)
            raise RobotException(msg, errCode)
        elif errno == ROBOT_RETRIEVE_FATAL:
            msg = _('Error: %s: Retrieve fatal.') % actmsg
            errCode = self.taskid + funid + 'R' + str(errno)
            self.log.info(msg)
            raise RobotException(msg, errCode)
        else:
            msg = _('Error: %(msg)s: Unknown error: %(errno)s') % {
                'msg': actmsg,
                'errno': str(errno) }
            errCode = self.taskid + funid + 'R' + str(errno)
            self.log.info(msg)
            raise RobotException(msg, errCode)

    
    def exchangeToRack(self, slotID):
        msg = _('Put disc from exchange to slot %s') % slotID
        self.log.info(msg)
        param = {
            'slot': slotID }
        ret = self.robot.doCmdSync('exchange_to_rack', param, timeout = 300)
        self._errorCheck(ret, msg, '03')

    
    def rackToExchange(self, slotID):
        msg = _('Put disc from slot %s to exchange') % slotID
        self.log.info(msg)
        param = {
            'slot': slotID }
        ret = self.robot.doCmdSync('rack_to_exchange', param, timeout = 300)
        self._errorCheck(ret, msg, '05')

    
    def rackToRack(self, fromSlot, toSlot):
        msg = _('Put disc from slot %(fs)s to slot %(ts)s') % {
            'fs': fromSlot,
            'ts': toSlot }
        self.log.info(msg)
        param = {
            'src_slot': fromSlot,
            'dest_slot': toSlot }
        ret = self.robot.doCmdSync('rack_to_rack', param, timeout = 300)
        self._errorCheck(ret, msg, '01')

    
    def carriageToExchange(self):
        msg = _('Put disc on carriage back to exchange box')
        self.log.info(msg)
        ret = self.robot.doCmdSync('carriage_to_exchange', { }, timeout = 300)
        self._errorCheck(ret, msg, '09')

    
    def gotoExchange(self):
        msg = _('Robot goto Exchange')
        self.log.info(msg)
        param = { }
        ret = self.robot.doCmdSync('goto_exchange', param, timeout = 300)
        self._errorCheck(ret, msg, '06')

    
    def readRfid(self):
        msg = _('Read Rfid')
        self.log.info(msg)
        param = { }
        ret = self.robot.doCmdSync('read_rfid', param)
        self._errorCheck(ret, msg, '08')
        return ret['rfid']


