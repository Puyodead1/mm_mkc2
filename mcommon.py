# Source Generated with Decompyle++
# File: mcommon.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-10-06 Vincent
vincent.chen@cereson.com

Filename:mcommon.py
Infrastructures and common utilities

Change Log:
    2009-05-15 Andrew add return code for initRobot() #1691
    2009-04-24 Vincent Remove the code for start flash, flash_proxy will do it
               Add distance1, distance2 to initMachine
    2009-03-12 Vincent Remove the code of initRobot when restart screen
    2009-02-25 Vincent Change initlog to Singleton
'''
import gettext
import threading
import traceback
import os
import time
import re
from queue import *
from random import choice
from time import strftime
import config
import proxy.config as pconfig
from proxy.conn_proxy import ConnProxy
import proxy.tools as ptools
from mobject import *
import linuxCmd
from rserial import RSerial
# =================================================================
# =    ROBOT Const (For Tesing Only)
# -----------------------------------------------------------------
# ROBOT_OK = "0"
# ROBOT_TIMEOUT = "1"
# ROBOT_EXCHANGE_JAM = "2"
# ROBOT_CARRIAGE_JAM = "3"
# ROBOT_NO_DISC = "4"

class Log(Singleton):
    def getInstance(name, comName):
        '''
        log = logging.getLogger(name)
        log.setLevel(logging.DEBUG)
        
        hConsole = logging.StreamHandler()
        hConsole.setLevel(logging.DEBUG)
        hConsole.setFormatter(logging.Formatter(config.LOGGING_STREAM_FORMAT))
        log.addHandler(hConsole)
        
        hFile = handlers.TimedRotatingFileHandler(config.LOGGING_LOG_FILE, \'D\', 1, 3)
        if not comName == "mkc":
            hFile = handlers.TimedRotatingFileHandler("log/%s.log" % comName, \'D\', 1, 3)
        hFile.setLevel(logging.INFO)
        hFile.setFormatter(logging.Formatter(config.LOGGING_FILE_FORMAT))
        log.addHandler(hFile)
        '''
        log = ptools.getLog('%s.log' % comName, name, 'DATE', maxCount = 500)
        return log

    getInstance = staticmethod(getInstance)


def initlog(name, comName = 'mkc'):
    return Log.getInstance(name, comName)

log = initlog('mcommon')

def N_(message):
    return message

(INFO, WARNING, ERROR) = list(range(3))

class QItem(object):
    
    def __init__(self, _type, _identity, _timestamp, _param):
        self.itemType = _type.upper()
        self.identity = self._getId(_identity)
        self.timestamp = self._getTimestamp(_timestamp)
        self.param = _param

    
    def _getId(self, _identity):
        result = _identity
        if not _identity:
            result = getRandomString(6)
        
        return result

    
    def _getTimestamp(self, _timestamp):
        result = _timestamp
        if not _timestamp:
            result = strftime(config.FMTTIME)
        
        return result

    
    def __str__(self):
        return '%s:%s:%s:%s' % (self.itemType, self.identity, self.timestamp, self.param)



class SmartQueue(Queue):
    
    def __init__(self):
        Queue.__init__(self)

    
    def get(self, itemType = '', identity = '', param = { }, block = True, timeout = None):
        '''
        if has no condition: return the QItem from Queue;
        if has condition: return QItem("", "", "", {}) for timeout
                          return None for count out
        '''
        ret = None
        condition = ''
        if itemType:
            condition = '(result.itemType.upper() == itemType.upper()) and '
        
        if identity:
            condition += '(result.identity.upper() == identity.upper()) and '
        
        for key in list(param.keys()):
            if param[key]:
                condition += '(result.param["%s"].upper() == param["%s"].upper()) and ' % (key, key)
            
        
        condition = condition.rstrip(' and')
        if not condition:
            return Queue.get(self, block, timeout)
        
        remaining = timeout
        endtime = time.time()
        if block == True and timeout:
            endtime = time.time() + timeout
        
        for i in range(config.Q_UNEXPECTED_MAX_SIZE):
            result = Queue.get(self, block, remaining)
            if block == True and timeout:
                remaining = endtime - time.time()
            
            if eval(condition):
                ret = result
                break
            elif block == True and timeout and remaining <= 0:
                ret = QItem('', '', '', { })
                break
            
        
        return ret

    
    def put(self, item, block = True, timeout = None):
        
        try:
            Queue.put(self, item, block, timeout)
        except Exception as ex:
            msg = '[SmartQueue - put] %s with ID %s: %s' % (item.itemType, item.identity, str(ex))
            log.error(msg)
            raise Exception(msg)




class FlashChannel:
    
    def __init__(self, wid, timeout = None):
        self.wid = wid
        self.timeout = timeout

    
    def send(self, ctrlId, command, info):
        
        try:
            param = {
                'wid': self.wid,
                'cid': ctrlId,
                'cmd': command,
                'param_info': info }
            qi = QItem('COMMAND', '', '', param)
            F_Q_SEND.put(qi, timeout = 1)
        except Exception:
            msg = '[FlashChannel - send] error when sending %s to %s:%s' % (command, ctrlId, traceback.format_exc())
            log.error(msg)


    
    def get(self, wid = '', timeout = None):
        result = None
        
        try:
            expectedItemType = 'EVENT'
            if timeout is None:
                timeout = self.timeout
            
            if wid == '':
                expectedParam = { }
            else:
                expectedParam = {
                    'wid': wid }
            res = F_Q_RECEIVE.get(expectedItemType, param = expectedParam, timeout = timeout)
            if res:
                if 'cid' in res.param:
                    result = res.param
                else:
                    result = { }
                    log.info('=.=! ==== MKC GET Timeout Event!%s' % res)
        except Empty:
            result = { }
        except Exception:
            log.error('[FlashChannel - get] error:%s' % traceback.format_exc())

        return result



class TimerThread(threading.Thread):
    
    def __init__(self, sleepPeriod, timeOutFunc):
        self._stopEvent = threading.Event()
        self._sleepPeriod = sleepPeriod
        threading.Thread.__init__(self, name = 'TimerThread')
        self.timeOutFunc = timeOutFunc

    
    def run(self):
        '''
        overload of threading.thread.run()
        main control loop
        '''
        while not self._stopEvent.isSet():
            self.timeOutFunc()
            self._stopEvent.wait(self._sleepPeriod)

    
    def join(self, timeout = None):
        '''
        Stop the thread
        '''
        self._stopEvent.set()
        threading.Thread.join(self, timeout)



def getRandomString(length):
    result = ''
    lstAphl = 'abcdefghijklmnopqrstuvwxyz'
    lstNum = '0123456789'
    lstAll = lstAphl * 5 + lstNum * 13
    for i in range(0, length):
        result += choice(lstAll)
    
    return result


def startHdmi():
    linuxCmd.startHdmi()


def stopHdmi():
    linuxCmd.stopHdmi()
    # 2009-04-24 Commented out by Vincent: 
    # flproxy.py will restart the flash itself
    # stopHdmi()    
    
    # # Start Flash Screen
    # FLASH_PLAYER = '~/bin/flashplayer'
    # FLASH_PROG = '~/kiosk/mkc2/screen/mkt.swf'
    # cmd = FLASH_PLAYER+' '+FLASH_PROG+' --display :0 2>/dev/null &'
    # os.system(cmd)

    # time.sleep(5)

    # startHdmi()    


def initRobot(top_offset = None, bottom_offset = None, exchange_offset = None, back_offset = None, offset2xx = None, offset6xx = None):
    robot = Robot.getInstance()
    connProxy = ConnProxy.getInstance()
    if top_offset is None:
        top_offset = connProxy._getConfigByKey('top_offset')
    
    if bottom_offset is None:
        bottom_offset = connProxy._getConfigByKey('bottom_offset')
    
    if exchange_offset is None:
        exchange_offset = connProxy._getConfigByKey('exchange_offset')
    
    if back_offset is None:
        back_offset = connProxy._getConfigByKey('back_offset')
    
    pulses_per_slot = connProxy._getConfigByKey('pulses_per_slot')
    distance1 = connProxy._getConfigByKey('distance1')
    distance2 = connProxy._getConfigByKey('distance2')
    retry = connProxy._getConfigByKey('robot_retry')
    if offset2xx is None:
        offset2xx = connProxy._getConfigByKey('offset2xx')
    
    if offset6xx is None:
        offset6xx = connProxy._getConfigByKey('offset6xx')
    
    log.info('Init Machine to [%s], [%s], [%s], [%s], [%s], [%s], [%s], [%s], [%s], [%s]' % (top_offset, bottom_offset, exchange_offset, back_offset, pulses_per_slot, distance1, distance2, retry, offset2xx, offset6xx))
    return robot.initMachine(top_offset, back_offset, exchange_offset, pulses_per_slot, bottom_offset, distance1, distance2, retry, offset2xx, offset6xx)


def sensorDetect():
    robot1 = Robot()
    robot = robot1.getInstance()
    ec = 0
    msg = ''
    r = robot.doCmdSync('carriage_lr_sensor_usage', { })
    errno = r['errno']
    if errno == ROBOT_OK:
        msg = 'test lr sensor OK.bit=%s. ' % r['bit']
    elif errno == ROBOT_TIMEOUT:
        msg = 'Error: test lr sensor Timeout. '
        ec = 1
    else:
        msg = 'Error: test lr sensor Unknown error %s. ' % errno
        ec = 1
    r = robot.doCmdSync('carriage_fb_sensor_usage', { })
    errno = r['errno']
    if errno == ROBOT_OK:
        msg += 'test fb sensor OK.value=%s. ' % r['value']
    elif errno == ROBOT_TIMEOUT:
        msg += 'Error: test fb sensor Timeout. '
        ec = 1
    else:
        msg += 'Error: test fb sensor Unknown error %s. ' % errno
        ec = 1
    r = robot.doCmdSync('carriage_lr_detect', { })
    errno = r['errno']
    if errno == ROBOT_OK:
        msg += 'lr sensor OK.value=%s.' % r['value']
    elif errno == ROBOT_TIMEOUT:
        msg += 'Error: test lr sensor timeout.'
        ec = 1
    else:
        msg += 'Error: Unknown error %s.' % errno
        ec = 1
    return (ec, msg)


def getPicFullPath(picName):
    fullPath = '%s%s' % (pconfig.MOVIE_PICTURE_PATH, picName)
    if not os.path.isfile(fullPath):
        fullPath = '%s%s' % (pconfig.MOVIE_PICTURE_PATH, pconfig.MOVIE_DEFAULT_PIC_NAME)
    
    return fullPath


def parseTrack(track1, track2):
    '''
    T1:%B379014336027929^RECIPIENT/GIFT CARD       ^08121010510535320000000000000000?.65
    T2:%379014336027929^081210105105353200000?.2A
    T1:%B4988820004558168^LU/PIN*LU ^0908101100000000085000000?.F2\r

    '''
    (ccNumber, ccName, ccExpDate) = ('', '', '')
    lines = track1.split('^')
    if not (len(lines) != 3):
        ccNumber = lines[0][1:]
        ccName = lines[1].strip().replace("'", '')
        ccExpDate = lines[2][:4]
    
    return (ccNumber, ccName, ccExpDate)


def _maskCardNomber(track, start_pos, end_token):
    msg = ''
    
    try:
        if track:
            i = track.index(end_token, start_pos)
            number = track[start_pos:i]
            if len(number) > 10:
                l = len(number[6:-4])
                number = number[:6] + '*' * l + number[-4:]
            
            i2 = track.index(end_token, i + 1)
            name = track[i + 1:i2]
            ol = len(track[i2 + 1:])
            msg = track[:start_pos] + number + end_token + name + end_token + '*' * ol
    except:
        log.error(traceback.format_exc())

    return msg


def logTrack(robotRet):
    """
    'errno': 0
    'track1': 'B6222310348520562^MR.WANG SHI WANG          ^1303101005040000000000258000000'
    'track2': '6222310348520562=13031010050425899999'
    """
    errno = robotRet.get('errno')
    return 'errno:%s, track1:%s' % (errno, _maskCardNomber(robotRet.get('track1'), 1, '^'))


def isValidEmail(email):
    p = re.compile('^[\\w-]+(\\.[\\w-]+)*@[\\w-]+(\\.[\\w-]+)+$')
    if p.match(email):
        return True
    else:
        return False


def maskCard(number):
    if len(number) > 8:
        l = len(number[4:-4])
        number = number[:4] + '*' * l + number[-4:]
    
    return number


def isS250():
    if os.path.isfile('/etc/kioskcapacity'):
        file = open('/etc/kioskcapacity', 'r')
        capacity = file.readline().strip()
        if capacity == '500':
            return False
        
    
    return True


def setLanguage(language):
    LAN_LIST = [
        'en',
        'fr_FR',
        'es',
        'no',
        'nl',
        'pt_BR']
    language = str(language)
    if language not in LAN_LIST:
        log.info('Invalid language, set to en.')
        language = 'en'
    
    gettext.translation(config.LOCALE_MODULE, config.LOCALE_PATH, languages = [
        language]).install()
    return language


def startFlag():
    
    try:
        file = open(config.MKC_FLAG, 'w')
        file.close()
    except Exception:
        log.info('can not set mkc start flag.\n%s' % traceback.format_exc())

    log.info('==========================================================================================')
    log.info('==================================== MKC START HERE ======================================')
    log.info('==========================================================================================')


def startSuccess():
    
    try:
        os.remove(config.MKC_FLAG)
    except Exception:
        log.info('can not remove mkc start flag.\n%s' % traceback.format_exc())



def get_active_information():
    information = ''
    
    try:
        fd = open('/home/puyodead1/kiosk/tmp/.active_information', 'r')
        information = fd.read().strip()
        fd.close()
    except:
        pass

    return information


def set_active_information(active_information = ''):
    fd = open('/home/puyodead1/kiosk/tmp/.active_information', 'wb')
    fd.write(active_information)
    fd.close()


def sync_active_information(connProxy, msg = 'kiosk restart'):
    active_info = get_active_information()
    log.debug('sync_active_information %s' % active_info)
    if active_info != 'active':
        connProxy.saveAIStatus('active', msg)
        set_active_information('active')
    

Q_UNEXPECTED = Queue()
F_Q_RECEIVE = SmartQueue()
F_Q_SEND = SmartQueue()
C_Q_RECEIVE = SmartQueue()
C_Q_SEND = SmartQueue()
globalSession = GlobalSession()
# Steps to form a resource file
# 1. xgettext -o test.pot --keyword="_" test.py
# 2. msginit -l es_ES.UTF-8 -o test.po -i test.pot
# 3. mv test.po ./locale/es/LC_MESSAGES;cd ./locale/es/LC_MESSAGES
# 4. msgfmt -c -v -o test.mo test.po


mlog = initlog('CONTROL')
ROBOT_UNKNOWN_COMMAND = 255
ROBOT_OK = 0
ROBOT_TIMEOUT = 1
ROBOT_INVALID_RFID = 2
ROBOT_RFID_READ_ERROR = 12
ROBOT_INVALID_LABEL = 3
ROBOT_EXCHANGE_JAM = 4
ROBOT_RETRIEVE_FAIL = 5
ROBOT_RETRIEVE_FATAL = 37
ROBOT_INSERT_FAIL = 6
ROBOT_INSERT_FATAL = 38
ROBOT_NO_DISC = 7
ROBOT_CARRIAGE_JAM = 8
ROBOT_BUSY = 9
ROBOT_CANCELED = 10
ROBOT_INVALID_INPUT = 11
ROBOT_ERROR_UNKNOWN = 16
ROBOT_FATAL_ERROR = 33
ROBOT_OPERATION_TIMEOUT = 49
# commands:
# reboot
# cancel 
# suck_disc
# vomit_disc
# rack_to_exchange
# excahnge_to_rack
# rack_to_rack
# goto_exchange
# exchange_eject
# exchange_close
# exchange_open
# read_card
# read_rfid


class Robot(threading.Thread):
    def on_init(self):
        threading.Thread.__init__(self, name = 'robot')
        ser = RSerial(serPort = '/dev/pts/10')
        self.ser = ser
        self._cancel = 0
        self.ser.resultCallback = self.resultCallback
        self.ser.eventCallback = self.eventCallback
        self.current = None
        self.got = False
        self.resultQ = { }
        self.cardInfo = []
        self.lock = threading.Lock()
        self.ulock = threading.Lock()
        self.clock = threading.Lock()
        self.userQ = { }
        self.cmdQ = []
        self.ser.handshake()
        # self._do_cmd("robot carriage home_back")
        # self._do_cmd("robot carriage home_left")
        # self._do_cmd("robot control goto_exchange")
        # self._do_cmd("robot io lamp flush_off")
        # self._do_cmd('robot cancel', _async=True)
        # self._do_cmd("robot exchange door_close")
        self.clearResultQ()
        self.start()

    
    def resetSerial(self):
        self.ser.resetSerial()

    
    def initMachine(self, top_offset, back_offset, exchange_offset, pulses_per_slot, bottom_offset, distance1 = 0, distance2 = 0, retry = 0, offset2xx = 0, offset6xx = 0):
        while True:
            r = self._do_cmd('robot ping', _async = False, tout = 5)
            if r and r[0] == 'ok':
                break
            
            time.sleep(5)
        self._do_cmd('robot control offset2xx ' + str(offset2xx))
        self._do_cmd('robot control offset6xx ' + str(offset6xx))
        self._do_cmd('robot control top_offset ' + str(top_offset))
        self._do_cmd('robot control back_offset ' + str(back_offset))
        self._do_cmd('robot control exchange_offset ' + str(exchange_offset))
        self._do_cmd('robot control bottom_offset ' + str(bottom_offset))
        self._do_cmd('robot control pulses_per_slot ' + str(pulses_per_slot))
        self._do_cmd('robot control set_retry ' + str(retry))
        if distance1:
            self._do_cmd('robot control sensor_distance ' + str(distance1))
        
        if distance2:
            self._do_cmd('robot control sensor_distance2 ' + str(distance2))
        
        status = self._do_cmd('robot control recover', _async = False, tout = 120)
        if len(status) > 0 and status[0] == 'ok':
            return (ROBOT_OK, '')
        
        msg = 'robot init error'
        if len(status) > 2:
            msg = status[2]
        
        return (ROBOT_FATAL_ERROR, msg)

    
    def run(self):
        while True:
            r = self.getCmdQ()
            if r:
                cmd = r['cmd']
                id = r['id']
                params = r['params']
                timeout = r['timeout']
                retry = r['retry']
                result_obj = { }
                rrr = { }
                if cmd == 'reboot':
                    rrr = self.reboot(result_obj)
                elif cmd == 'cancel':
                    self.cancel()
                    rrr = {
                        'errno': ROBOT_OK }
                elif cmd == 'suck_disc':
                    rrr = self.suck_disc(result_obj)
                elif cmd == 'vomit_disc':
                    if 'rfid' not in params:
                        rrr = {
                            'errno': ROBOT_INVALID_INPUT }
                    else:
                        rrr = self.vomit_disc(params['rfid'], result_obj)
                elif cmd == 'rack_to_exchange':
                    if 'slot' not in params:
                        rrr = {
                            'errno': ROBOT_INVALID_INPUT }
                    else:
                        rrr = self.rack_to_exchange(params['slot'], result_obj, timeout = timeout)
                elif cmd == 'carriage_to_exchange':
                    rrr = self.carriage_to_exchange(result_obj, timeout = timeout)
                elif cmd == 'exchange_to_carriage':
                    rrr = self.exchange_to_carriage(result_obj, timeout = timeout)
                elif cmd == 'slot_to_dispense':
                    if 'slot' not in params:
                        rrr = {
                            'errno': ROBOT_INVALID_INPUT }
                    else:
                        rrr = self.slot_to_dispense(params['slot'], result_obj, timeout = timeout)
                elif cmd == 'exchange_to_rack':
                    if 'slot' not in params:
                        rrr = {
                            'errno': ROBOT_INVALID_INPUT }
                    else:
                        rrr = self.exchange_to_rack(params['slot'], result_obj, timeout = timeout)
                elif cmd == 'goto_slot_retrieve':
                    if 'slot' not in params:
                        rrr = {
                            'errno': ROBOT_INVALID_INPUT }
                    else:
                        rrr = self.goto_slot_retrieve(params['slot'], result_obj, timeout = timeout)
                elif cmd == 'goto_slot_insert':
                    if 'slot' not in params:
                        rrr = {
                            'errno': ROBOT_INVALID_INPUT }
                    else:
                        rrr = self.goto_slot_insert(params['slot'], result_obj, timeout = timeout)
                elif cmd == 'carriage_insert':
                    rrr = self.carriage_insert(result_obj, timeout = timeout)
                elif cmd == 'carriage_retrieve':
                    rrr = self.carriage_retrieve(result_obj, timeout = timeout)
                elif cmd == 'rack_to_rack':
                    if 'src_slot' not in params or 'dest_slot' not in params:
                        rrr = {
                            'errno': ROBOT_INVALID_INPUT }
                    else:
                        rrr = self.slot_to_slot(params['src_slot'], params['dest_slot'], result_obj, timeout = timeout)
                elif cmd == 'goto_exchange':
                    rrr = self.goto_exchange(result_obj, timeout = timeout)
                elif cmd == 'vqd':
                    rrr = self.vqd(result_obj)
                elif cmd == 'exchange_eject':
                    self.exchange_eject2()
                    rrr = {
                        'errno': ROBOT_OK }
                elif cmd == 'exchange_close':
                    rrr = self.exchange_close(result_obj)
                elif cmd == 'exchange_open':
                    self._exchange_open()
                    rrr = {
                        'errno': ROBOT_OK }
                elif cmd == 'read_card':
                    self.cardInfo = []
                    rrr = self.read_card(result_obj, timeout = timeout)
                elif cmd == 'read_rfid':
                    rrr = self.read_rfid(result_obj)
                elif cmd == 'distance1':
                    rrr = self.sensor_distance(result_obj)
                elif cmd == 'distance2':
                    rrr = self.sensor_distance2(result_obj)
                elif cmd == 'carriage_lr_sensor_usage':
                    rrr = self.carriage_lr_sensor_usage(result_obj)
                elif cmd == 'carriage_fb_sensor_usage':
                    rrr = self.carriage_fb_sensor_usage(result_obj)
                elif cmd == 'carriage_lr_detect':
                    rrr = self.carriage_lr_detect(result_obj)
                elif cmd == 'init_vertical':
                    rrr = self.init_vertical(result_obj)
                elif cmd == 'init_machine':
                    rrr = self.init_machine(result_obj)
                else:
                    rrr = {
                        'errno': ROBOT_UNKNOWN_COMMAND }
                self.putUserQ(id, rrr)
            
            time.sleep(0.1)

    
    def carriage_lr_sensor_usage(self, result_obj):
        status = self._do_cmd('robot carriage lr_sensor_usage', _async = False, tout = 300)
        if len(status) > 2 and status[0] == 'ok':
            result_obj = {
                'errno': ROBOT_OK,
                'bit': status[2] }
        else:
            result_obj = {
                'errno': ROBOT_TIMEOUT }
        return result_obj

    
    def carriage_fb_sensor_usage(self, result_obj):
        status = self._do_cmd('robot carriage fb_sensor_usage', _async = False, tout = 300)
        if len(status) > 2 and status[0] == 'ok':
            result_obj = {
                'errno': ROBOT_OK,
                'value': status[2] }
        else:
            result_obj = {
                'errno': ROBOT_TIMEOUT }
        return result_obj

    
    def carriage_lr_detect(self, result_obj):
        status = self._do_cmd('robot carriage lr_detect', _async = False, tout = 300)
        if len(status) > 2 and status[0] == 'ok':
            result_obj = {
                'errno': ROBOT_OK,
                'value': status[2] }
        else:
            result_obj = {
                'errno': ROBOT_TIMEOUT }
        return result_obj

    
    def putUserQ(self, id, obj):
        self.ulock.acquire()
        
        try:
            self.userQ[str(id)] = obj
        finally:
            self.ulock.release()

        time.sleep(0)

    
    def getUserQ(self, id):
        r = None
        self.ulock.acquire()
        
        try:
            if str(id) in self.userQ:
                r = self.userQ.pop(str(id))
                return r
        finally:
            self.ulock.release()

        return r

    
    def putCmdQ(self, obj):
        self.clock.acquire()
        
        try:
            self.cmdQ.append(obj)
        finally:
            self.clock.release()

        time.sleep(0)

    
    def getCmdQ(self):
        r = None
        self.clock.acquire()
        
        try:
            if len(self.cmdQ) > 0:
                r = self.cmdQ.pop()
        finally:
            self.clock.release()

        return r

    
    def eventCallback(self, data):
        s = ''
        for i in range(0, len(data)):
            s = s + data[i]
        
        self.cardInfo = self.parseData(s, cry = True)

    
    def resultCallback(self, seq, data):
        s = ''
        self.lock.acquire()
        
        try:
            for i in range(0, len(data)):
                s = s + data[i]
            
            p = self.parseData(s)
            self.resultQ[seq] = p
        except Exception as ex:
            pass
        finally:
            self.lock.release()


    
    def _getResultQ(self, seq, timeout = 5):
        r = None
        if timeout == -1:
            timeout = 60 * 5
        
        tick = time.time()
        while time.time() - tick < timeout:
            
            try:
                self.lock.acquire()
                if seq in self.resultQ:
                    r = self.resultQ.pop(seq)
                    break
            finally:
                self.lock.release()

            time.sleep(0.05)
        return r

    
    def _do_cmd(self, command, _async = False, tout = 60):
        current = self.ser.sendDataSync(command)
        if _async:
            return current
        
        r = None
        r = self._getResultQ(current, timeout = tout)
        if not r:
            r = ('err', 'TIMEOUT')
        
        return r

    
    def getResult(self, id, timeout = 0.1):
        start = time.time()
        while time.time() - start < timeout:
            ret = self.getUserQ(id)
            if ret:
                return ret
            
            time.sleep(0.1)

    
    def __new__(cls, *args, **kwargs):
        if '_inst' not in vars(cls):
            cls._inst = object.__new__(cls, *args, **kwargs)
            cls._inst.on_init()
        
        return cls._inst

    
    def getInstance():
        return Robot()

    getInstance = staticmethod(getInstance)
    
    def doCmdSync(self, cmd, input_params = { }, timeout = -1, retry = 1, one_way = False):
        self._cancel = 0
        r = { }
        r['timeout'] = timeout
        r['cmd'] = cmd
        r['params'] = input_params
        r['retry'] = retry
        r['id'] = uuid.uuid4()
        self.putCmdQ(r)
        while True:
            ret = self.getUserQ(r['id'])
            if ret:
                return ret
            
            time.sleep(0.1)

    
    def doCmdAsync(self, cmd, input_params = { }, timeout = -1, retry = 1, one_way = False):
        self._cancel = 0
        r = { }
        r['timeout'] = timeout
        r['cmd'] = cmd
        r['params'] = input_params
        r['retry'] = retry
        r['id'] = uuid.uuid4()
        self.putCmdQ(r)
        return r['id']

    
    def clearResultQ(self):
        self.lock.acquire()
        
        try:
            self.resultQ = { }
        finally:
            self.lock.release()


    
    def parseData(self, data, cry = False):
        
        try:
            if not cry:
                mlog.info('raw reply from rabbit: %s ' % str(data))
            
            r = None
            data = data.split('|')
            filed = data[0].strip()
            if filed == '+ok':
                if len(data) > 2:
                    r = ('ok', data[1].strip(), data[2].strip())
                elif len(data) > 1:
                    r = ('ok', data[1].strip())
                else:
                    r = ('ok', '')
            elif filed == '+err' or filed == '-err':
                if len(data) > 2:
                    r = ('err', data[1].strip(), data[2].strip())
                elif len(data) > 1:
                    r = ('err', data[1].strip())
                else:
                    r = ('err', '')
            elif filed == 'card':
                if data[1].strip() != 'pending':
                    return data
                
            else:
                r = ('exception', '')
        except Exception as ex:
            r = ('err', ex)

        return r

    
    def _parse_card_info(self, t1, t2):
        (ccNumber, ccName, ccExpDate) = parseTrack(t1, t2)
        if not ccNumber:
            return None
        
        validator = CCValidator()
        rev = validator.check(ccNumber)
        mlog.info('validator return %s' % rev)
        if rev is False:
            return None
        else:
            return (repr(ccNumber), repr(ccName), repr(ccExpDate), t1, t2)

    
    def read_rfid(self, result_obj):
        success = False
        for i in range(3):
            status = self._do_cmd('robot exchange rfid', _async = False, tout = 10)
            if status[0] == 'ok':
                mlog.info('read rfid ok')
                success = True
                break
            
        
        if len(status) > 2 and success:
            if status[2][2:].lower() == 'FFFFFFFFFFFFFFFF':
                result_obj = {
                    'errno': ROBOT_INVALID_RFID,
                    'rfid': status[2] }
            else:
                result_obj = {
                    'errno': ROBOT_OK,
                    'rfid': status[2] }
        elif status:
            result_obj = {
                'errno': ROBOT_RFID_READ_ERROR,
                'rfid': '' }
        else:
            result_obj = {
                'errno': ROBOT_TIMEOUT,
                'rfid': status[1] }
        return result_obj

    
    def sensor_distance(self, result_obj):
        status = self._do_cmd('robot control sensor_distance', _async = False, tout = 300)
        if len(status) > 2 and status[0] == 'ok':
            result_obj = {
                'errno': ROBOT_OK,
                'distance': status[2] }
        else:
            result_obj = {
                'errno': ROBOT_TIMEOUT }
        return result_obj

    
    def sensor_distance2(self, result_obj):
        status = self._do_cmd('robot control sensor_distance2', _async = False, tout = 300)
        if len(status) > 2 and status[0] == 'ok':
            result_obj = {
                'errno': ROBOT_OK,
                'distance': status[2] }
        else:
            result_obj = {
                'errno': ROBOT_TIMEOUT }
        return result_obj

    
    def vqd(self, result_obj):
        success = False
        status = self._do_cmd('robot control vqd ', _async = False, tout = 10)
        if status[0] == 'ok':
            result_obj = {
                'errno': ROBOT_OK,
                'vertical': status[2] }
        else:
            result_obj = {
                'errno': ROBOT_TIMEOUT,
                'vertical': '' }
        return result_obj

    
    def read_card(self, result_obj, timeout):
        r = None
        err = 0
        start = time.time()
        while time.time() - start < timeout and not (self._cancel):
            if self.cardInfo:
                if self.cardInfo[1].strip() == 'fail':
                    err = 1
                    break
                
                
                try:
                    r = self._parse_card_info(self.cardInfo[2].strip(), self.cardInfo[3].strip())
                    if r:
                        break
                    else:
                        err = 1
                        break
                    
                    try:
                        mlog.info('got card reader info:***%i %s' % (len(str(self.cardInfo[2])), str(self.cardInfo[2])[:-3]))
                    except:
                        pass

                except Exception as ex:
                    mlog.info('read_card error: ' + str(ex))
                    err = 1
                    break

                self.cardInfo = []
            
            time.sleep(0.01)
        if err == 1:
            result_obj = {
                'errno': ROBOT_ERROR_UNKNOWN,
                'track1': '',
                'track2': '' }
            return result_obj
        
        if r:
            result_obj = {
                'errno': ROBOT_OK,
                'track1': r[3],
                'track2': r[4] }
        else:
            result_obj = {
                'errno': ROBOT_TIMEOUT }
        return result_obj

    
    def cancel(self):
        self._cancel = 1

    
    def _cancel_cmd(self):
        while True:
            status = self._do_cmd('robot cancel', _async = False, tout = 5)
            status = self._do_cmd('robot ping', _async = False, tout = 5)
            if status and status[0] == 'ok':
                break
            
            time.sleep(2)

    
    def _exchange_close(self):
        while True:
            
            try:
                status = self._do_cmd('robot exchange door_close', _async = False, tout = 5)
                mlog.info('door_close :' + str(status[0]))
                if status[0] != 'ok':
                    status = self._do_cmd('robot exchange door_open', _async = False, tout = 10)
            except Exception as ex:
                mlog.info('door_close error :' + str(ex))


    
    def _exchange_open(self):
        while True:
            
            try:
                status = self._do_cmd('robot exchange door_open', _async = False, tout = 10)
                mlog.info('door_open :' + str(status[0]))
                if status[0] != 'ok':
                    status = self._do_cmd('robot exchange door_close', _async = False, tout = 10)
            except Exception as ex:
                mlog.info('door_open error :' + str(ex))


    
    def suck_disc(self, result_obj):
        '''
        run "move exchange_accept", open exchange door, wait for user insert disc
        '''
        mlog.info('[suck_disc] sendData:exchange accept')
        r = self._do_cmd('robot exchange accept', _async = True)
        tick = time.time()
        while True:
            
            try:
                status = self._getResultQ(r, 0.2)
                if self._cancel:
                #    while (time.time()- tick) < 2:
                #        time.sleep(0.2)
                    mlog.info('[suck_disc] canceled')
                    self._cancel_cmd()
                    status = self._getResultQ(r, 3)
                    self.clearResultQ()
                    self.exchange_eject2()
                    result_obj = {
                        'errno': ROBOT_CANCELED,
                        'msg': '' }
                    return result_obj
                
                if status:
                    break
            except Exception as ex:
                status[0] = 'err'
                status[1] = 'timeout'

        mlog.info('got exchange accept return ' + str(status))
        if status[0] == 'ok':
            success = False
            self._exchange_close()
            self.clearResultQ()
            for i in range(3):
                status = self._do_cmd('robot exchange rfid', _async = False, tout = 10)
                if self._cancel:
                    self._cancel_cmd()
                    self.clearResultQ()
                    self.exchange_eject2()
                    result_obj = {
                        'errno': ROBOT_CANCELED,
                        'msg': '' }
                    return result_obj
                
                if status[0] == 'ok':
                    mlog.info('[suck_disc] read rfid ok')
                    success = True
                    break
                
            
            if not success:
                mlog.error('[suck_disc] cannot read rfid')
                result_obj = {
                    'errno': ROBOT_RFID_READ_ERROR,
                    'msg': '' }
                return result_obj
            else:
                result_obj = {
                    'errno': ROBOT_OK,
                    'rfid': status[2] }
                return result_obj
        elif status[1] == 'TIMEOUT':
            self._cancel_cmd()
            mlog.info('[suck_disc] timeout')
            result_obj = {
                'errno': ROBOT_TIMEOUT,
                'msg': '' }
            return result_obj
        elif status[1] == 'OPERATION_TIMEOUT':
            self._cancel_cmd()
            mlog.info('[suck_disc] operation timeout')
            result_obj = {
                'errno': ROBOT_OPERATION_TIMEOUT,
                'msg': '' }
            return result_obj
        else:
            mlog.info('[suck_disc] invalid label')
            result_obj = {
                'errno': ROBOT_INVALID_LABEL,
                'msg': '' }
            return result_obj

    
    def goto_slot_insert(self, slot_no, result_obj, timeout = 120):
        self.clearResultQ()
        mlog.info('[goto_slot_insert] parameters %s' % slot_no)
        status = self._do_cmd('robot control goto_slot_insert %s' % str(slot_no), _async = False, tout = timeout)
        if status[0] == 'ok':
            result_obj = {
                'errno': ROBOT_OK,
                'msg': '' }
            return result_obj
        elif status[1] == 'TIMEOUT':
            mlog.info('[goto_slot_insert] timeout')
            result_obj = {
                'errno': ROBOT_TIMEOUT,
                'msg': '' }
            return result_obj
        elif status[1] == 'GOTO_COL':
            mlog.info('[goto_slot_insert] carriage jam')
            result_obj = {
                'errno': ROBOT_CARRIAGE_JAM,
                'msg': '' }
            return result_obj
        else:
            mlog.info('[goto_slot_insert] unknown')
            result_obj = {
                'errno': ROBOT_ERROR_UNKNOWN,
                'msg': '' }
            return result_obj

    
    def goto_slot_retrieve(self, slot_no, result_obj, timeout = 120):
        self.clearResultQ()
        mlog.info('[goto_slot_retrieve] parameters %s' % slot_no)
        status = self._do_cmd('robot control goto_slot_retrieve %s' % str(slot_no), _async = False, tout = timeout)
        if status[0] == 'ok':
            result_obj = {
                'errno': ROBOT_OK,
                'msg': '' }
            return result_obj
        elif status[1] == 'TIMEOUT':
            mlog.info('[goto_slot_retrieve] timeout')
            result_obj = {
                'errno': ROBOT_TIMEOUT,
                'msg': '' }
            return result_obj
        elif status[1] == 'GOTO_COL':
            mlog.info('[goto_slot_retrieve] carriage jam')
            result_obj = {
                'errno': ROBOT_CARRIAGE_JAM,
                'msg': '' }
            return result_obj
        else:
            mlog.info('[goto_slot_retrieve] unknown')
            result_obj = {
                'errno': ROBOT_ERROR_UNKNOWN,
                'msg': '' }
            return result_obj

    
    def carriage_insert(self, result_obj, timeout = 120):
        self.clearResultQ()
        mlog.info('[carriage_insert]')
        status = self._do_cmd('robot carriage insert', _async = False, tout = timeout)
        if status[0] == 'ok':
            result_obj = {
                'errno': ROBOT_OK,
                'msg': '' }
            return result_obj
        elif status[1] == 'INSERT_JAM' or status[1] == 'INSERT_TRY':
            pos = ''
            if len(status) >= 3:
                pos = status[2]
            
            mlog.info('[carriage_insert] insert  jam, info:' + pos)
            result_obj = {
                'errno': ROBOT_INSERT_FAIL,
                'msg': '' }
            return result_obj
        elif status[1] == 'INSERT_FATAL':
            pos = ''
            if len(status) >= 3:
                pos = status[2]
            
            mlog.info('[carriage_insert] insert  fatal error, info:' + pos)
            result_obj = {
                'errno': ROBOT_INSERT_FATAL,
                'msg': '' }
            return result_obj
        else:
            mlog.info('[carriage_insert] unknown')
            result_obj = {
                'errno': ROBOT_ERROR_UNKNOWN,
                'msg': '' }
            return result_obj

    
    def carriage_retrieve(self, result_obj, timeout = 120):
        self.clearResultQ()
        mlog.info('[carriage_retrieve]')
        status = self._do_cmd('robot carriage_retrieve', _async = False, tout = timeout)
        if status[0] == 'ok':
            result_obj = {
                'errno': ROBOT_OK,
                'msg': '' }
            return result_obj
        elif status[1] == 'RETRIEVE_JAM' or status[1] == 'RETRIEVE_TRY':
            pos = ''
            if len(status) >= 3:
                pos = status[2]
            
            mlog.info('[carriage_retrieve] retrieve  jam, info:' + pos)
            result_obj = {
                'errno': ROBOT_RETRIEVE_FAIL,
                'msg': '' }
            return result_obj
        
        if status[1] == 'RETRIEVE_FATAL':
            pos = ''
            if len(status) >= 3:
                pos = status[2]
            
            mlog.info('[carriage_retrieve] retrieve  fatal error, info:' + pos)
            result_obj = {
                'errno': ROBOT_RETRIEVE_FATAL,
                'msg': '' }
            return result_obj
        elif status[1] == 'NO_DISC':
            mlog.info('[carriage_retrieve] no disc')
            result_obj = {
                'errno': ROBOT_NO_DISC,
                'msg': '' }
            return result_obj
        else:
            mlog.info('[carriage_retrieve] unknown')
            result_obj = {
                'errno': ROBOT_ERROR_UNKNOWN,
                'msg': '' }
            return result_obj

    
    def exchange_to_rack(self, slot_no, result_obj, timeout = 120):
        self.clearResultQ()
        mlog.info('[exchange_to_rack] parameters %s' % slot_no)
        status = self._do_cmd('robot control exchange_to_rack %s' % str(slot_no), _async = False, tout = timeout)
        if status[0] == 'ok':
            result_obj = {
                'errno': ROBOT_OK,
                'msg': '' }
            return result_obj
        else:
            self._do_cmd('robot control vqd', tout = 10)
            if status[1] == 'TIMEOUT':
                mlog.info('[exchange_to_rack] timeout')
                result_obj = {
                    'errno': ROBOT_TIMEOUT,
                    'msg': '' }
                return result_obj
            elif status[1] == 'INSERT_TRY' or status[1] == 'INSERT_JAM':
                pos = ''
                if len(status) >= 3:
                    pos = status[2]
                
                mlog.info('[exchange_to_rack] insert  jam, info:' + pos)
                result_obj = {
                    'errno': ROBOT_INSERT_FAIL,
                    'msg': '' }
                return result_obj
            elif status[1] == 'INSERT_FATAL':
                pos = ''
                if len(status) >= 3:
                    pos = status[2]
                
                mlog.info('[exchange_to_rack] insert fatal error, info:' + pos)
                result_obj = {
                    'errno': ROBOT_INSERT_FATAL,
                    'msg': '' }
                return result_obj
            elif status[1] == 'RETRIEVE_JAM' or status[1] == 'RETRIEVE_TRY':
                pos = ''
                if len(status) >= 3:
                    pos = status[2]
                
                mlog.info('[exchange_to_rack] retrieve  jam, pos:' + pos)
                result_obj = {
                    'errno': ROBOT_RETRIEVE_FAIL,
                    'msg': '' }
                return result_obj
            elif status[1] == 'RETRIEVE_FATAL':
                pos = ''
                if len(status) >= 3:
                    pos = status[2]
                
                mlog.info('[exchange_to_rack] retrieve  fatal error, pos:' + pos)
                result_obj = {
                    'errno': ROBOT_RETRIEVE_FATAL,
                    'msg': '' }
                return result_obj
            elif status[1] == 'GOTO_COL':
                mlog.info('[exchange_to_rack] carriage jam')
                result_obj = {
                    'errno': ROBOT_CARRIAGE_JAM,
                    'msg': '' }
                return result_obj
            elif status[1] == 'NO_DISC':
                mlog.info('[exchange_to_rack] no disc')
                result_obj = {
                    'errno': ROBOT_NO_DISC,
                    'msg': '' }
                return result_obj
            else:
                mlog.info('[exchange_to_rack] unknown')
                result_obj = {
                    'errno': ROBOT_ERROR_UNKNOWN,
                    'msg': '' }
                return result_obj

    
    def slot_to_dispense(self, slot, result_obj, timeout = 120):
        r = self.slot_to_slot(slot, 270, result_obj, timeout = timeout)
        if r['errno'] != ROBOT_OK:
            return r
        
        status = self._do_cmd('robot control dispense_out', tout = 60)
        if status[0] == 'ok':
            result_obj = {
                'errno': ROBOT_OK,
                'msg': '' }
            return result_obj
        else:
            result_obj = {
                'errno': ROBOT_TIMEOUT,
                'msg': '' }
            return result_obj

    
    def slot_to_slot(self, src, dest, result_obj, timeout = 120):
        self.clearResultQ()
        status = self._do_cmd('robot control slot_to_slot %s %s' % (str(src), str(dest)), _async = False, tout = timeout)
        mlog.info('status:' + str(status))
        if status[0] == 'ok':
            result_obj = {
                'errno': ROBOT_OK,
                'msg': '' }
            return result_obj
        else:
            self._do_cmd('robot control vqd', tout = 10)
            if status[1] == 'TIMEOUT':
                mlog.info('[slot_to_slot] insert jam, cannot fix')
                result_obj = {
                    'errno': ROBOT_TIMEOUT,
                    'msg': '' }
                return result_obj
            elif status[1] == 'INSERT_JAM' or status[1] == 'INSERT_TRY':
                pos = ''
                if len(status) >= 3:
                    pos = status[2]
                
                mlog.info('[slot_to_slot] insert  jam, info:' + pos)
                result_obj = {
                    'errno': ROBOT_INSERT_FAIL,
                    'msg': '' }
                return result_obj
            elif status[1] == 'INSERT_FATAL':
                pos = ''
                if len(status) >= 3:
                    pos = status[2]
                
                mlog.info('[slot_to_slot] insert fatal error, info:' + pos)
                result_obj = {
                    'errno': ROBOT_INSERT_FATAL,
                    'msg': '' }
                return result_obj
            elif status[1] == 'RETRIEVE_JAM' or status[1] == 'RETRIEVE_TRY':
                pos = ''
                if len(status) >= 3:
                    pos = status[2]
                
                mlog.info('[rack_to_exchange] retrieve  jam, info:' + pos)
                result_obj = {
                    'errno': ROBOT_RETRIEVE_FAIL,
                    'msg': '' }
                return result_obj
            elif status[1] == 'RETRIEVE_FATAL':
                pos = ''
                if len(status) >= 3:
                    pos = status[2]
                
                mlog.info('[rack_to_exchange] retrieve  fatal error, info:' + pos)
                result_obj = {
                    'errno': ROBOT_RETRIEVE_FATAL,
                    'msg': '' }
                return result_obj
            elif status[1] == 'GOTO_COL':
                mlog.info('[slot_to_slot] carriage jam')
                result_obj = {
                    'errno': ROBOT_CARRIAGE_JAM,
                    'msg': '' }
                return result_obj
            elif status[1] == 'NO_DISC':
                mlog.info('[slot_to_slot] no disc')
                result_obj = {
                    'errno': ROBOT_NO_DISC,
                    'msg': '' }
                return result_obj
            else:
                mlog.info('[slot_to_slot] unknown')
                result_obj = {
                    'errno': ROBOT_ERROR_UNKNOWN,
                    'msg': '' }
                return result_obj

    
    def carriage_to_exchange(self, result_obj, timeout = 120):
        self.clearResultQ()
        status = self._do_cmd('robot control carriage_to_exchange')
        mlog.info('status:' + str(status))
        if status[0] == 'ok':
            result_obj = {
                'errno': ROBOT_OK,
                'msg': '' }
            return result_obj
        elif status[1] == 'TIMEOUT':
            mlog.info('[carriage_to_exchange] insert jam, cannot fix')
            result_obj = {
                'errno': ROBOT_TIMEOUT,
                'msg': '' }
            return result_obj
        elif status[1] == 'INSERT_JAM' or status[1] == 'INSERT_TRY':
            pos = ''
            if len(status) >= 3:
                pos = status[2]
            
            mlog.info('[carriage_to_exchange] insert  jam, info:' + pos)
            result_obj = {
                'errno': ROBOT_INSERT_FAIL,
                'msg': '' }
            return result_obj
        elif status[1] == 'INSERT_FATAL':
            pos = ''
            if len(status) >= 3:
                pos = status[2]
            
            mlog.info('[carriage_to_exchange] insert  fatal error, info:' + pos)
            result_obj = {
                'errno': ROBOT_INSERT_FATAL,
                'msg': '' }
            return result_obj
        elif status[1] == 'RETRIEVE_JAM' and status[1] == 'RETRIEVE_TRY' or status[1] == 'RETRIEVE_DISC_FLY':
            pos = ''
            if len(status) >= 3:
                pos = status[2]
            
            mlog.info('[carriage_to_exchange] retrieve  jam, info:' + pos)
            result_obj = {
                'errno': ROBOT_RETRIEVE_FAIL,
                'msg': '' }
            return result_obj
        elif status[1] == 'RETRIEVE_FATAL':
            pos = ''
            if len(status) >= 3:
                pos = status[2]
            
            mlog.info('[carriage_to_exchange] retrieve  fatal error, info:' + pos)
            result_obj = {
                'errno': ROBOT_RETRIEVE_FATAL,
                'msg': '' }
            return result_obj
        elif status[1] == 'GOTO_COL':
            mlog.info('[carriage_to_exchange] carriage jam')
            result_obj = {
                'errno': ROBOT_CARRIAGE_JAM,
                'msg': '' }
            return result_obj
        elif status[1] == 'NO_DISC':
            mlog.info('[carriage_to_exchange] no disc')
            result_obj = {
                'errno': ROBOT_NO_DISC,
                'msg': '' }
            return result_obj
        else:
            mlog.info('[carriage_to_exchange] unknown')
            result_obj = {
                'errno': ROBOT_ERROR_UNKNOWN,
                'msg': '' }
            return result_obj

    
    def exchange_to_carriage(self, result_obj, timeout = 120):
        self.clearResultQ()
        status = self._do_cmd('robot control exchange_to_carriage')
        mlog.info('status:' + str(status))
        if status[0] == 'ok':
            result_obj = {
                'errno': ROBOT_OK,
                'msg': '' }
            return result_obj
        elif status[1] == 'TIMEOUT':
            mlog.info('[exchange_to_carriage] insert jam, cannot fix')
            result_obj = {
                'errno': ROBOT_TIMEOUT,
                'msg': '' }
            return result_obj
        elif status[1] == 'INSERT_JAM' or status[1] == 'INSERT_TRY':
            pos = ''
            if len(status) >= 3:
                pos = status[2]
            
            mlog.info('[exchange_to_carriage] insert  jam, info:' + pos)
            result_obj = {
                'errno': ROBOT_INSERT_FAIL,
                'msg': '' }
            return result_obj
        elif status[1] == 'INSERT_FATAL':
            pos = ''
            if len(status) >= 3:
                pos = status[2]
            
            mlog.info('[exchange_to_carriage] insert  fatal error, info:' + pos)
            result_obj = {
                'errno': ROBOT_INSERT_FATAL,
                'msg': '' }
            return result_obj
        elif status[1] == 'RETRIEVE_JAM' or status[1] == 'RETRIEVE_TRY':
            pos = ''
            if len(status) >= 3:
                pos = status[2]
            
            mlog.info('[exchange_to_carriage] retrieve  jam, info:' + pos)
            result_obj = {
                'errno': ROBOT_RETRIEVE_FAIL,
                'msg': '' }
            return result_obj
        elif status[1] == 'RETRIEVE_FATAL':
            pos = ''
            if len(status) >= 3:
                pos = status[2]
            
            mlog.info('[exchange_to_carriage] retrieve  fatal error, info:' + pos)
            result_obj = {
                'errno': ROBOT_RETRIEVE_FATAL,
                'msg': '' }
            return result_obj
        elif status[1] == 'GOTO_COL':
            mlog.info('[exchange_to_carriage] carriage jam')
            result_obj = {
                'errno': ROBOT_CARRIAGE_JAM,
                'msg': '' }
            return result_obj
        elif status[1] == 'NO_DISC':
            mlog.info('[exchange_to_carriage] no disc')
            result_obj = {
                'errno': ROBOT_NO_DISC,
                'msg': '' }
            return result_obj
        else:
            mlog.info('[exchange_to_carriage] unknown')
            result_obj = {
                'errno': ROBOT_ERROR_UNKNOWN,
                'msg': '' }
            return result_obj

    
    def rack_to_exchange(self, slot_no, result_obj, timeout = 120):
        self.clearResultQ()
        status = self._do_cmd('robot control rack_to_exchange %s' % str(slot_no), _async = False, tout = timeout)
        mlog.info('status:' + str(status))
        if status[0] == 'ok':
            result_obj = {
                'errno': ROBOT_OK,
                'msg': '' }
            return result_obj
        elif status[1] == 'TIMEOUT':
            mlog.info('[rack_to_exchange] timeout')
            result_obj = {
                'errno': ROBOT_TIMEOUT,
                'msg': '' }
            return result_obj
        elif status[1] == 'INSERT_JAM' or status[1] == 'INSERT_TRY':
            pos = ''
            if len(status) >= 3:
                pos = status[2]
            
            mlog.info('[rack_to_exchange] insert  jam, info:' + pos)
            result_obj = {
                'errno': ROBOT_INSERT_FAIL,
                'msg': '' }
            return result_obj
        elif status[1] == 'INSERT_FATAL':
            pos = ''
            if len(status) >= 3:
                pos = status[2]
            
            mlog.info('[rack_to_exchange] insert  fatal error, info:' + pos)
            result_obj = {
                'errno': ROBOT_INSERT_FATAL,
                'msg': '' }
            return result_obj
        elif status[1] == 'RETRIEVE_JAM' or status[1] == 'RETRIEVE_TRY':
            pos = ''
            if len(status) >= 3:
                pos = status[2]
            
            mlog.info('[rack_to_exchange] retrieve  jam, info:' + pos)
            result_obj = {
                'errno': ROBOT_RETRIEVE_FAIL,
                'msg': '' }
            return result_obj
        elif status[1] == 'RETRIEVE_FATAL':
            pos = ''
            if len(status) >= 3:
                pos = status[2]
            
            mlog.info('[rack_to_exchange] retrieve  fatal error, info:' + pos)
            result_obj = {
                'errno': ROBOT_RETRIEVE_FATAL,
                'msg': '' }
            return result_obj
        elif status[1] == 'GOTO_COL':
            mlog.info('[rack_to_exchange] carriage jam')
            result_obj = {
                'errno': ROBOT_CARRIAGE_JAM,
                'msg': '' }
            return result_obj
        elif status[1] == 'NO_DISC':
            mlog.info('[rack_to_exchange] no disc')
            result_obj = {
                'errno': ROBOT_NO_DISC,
                'msg': '' }
            return result_obj
        else:
            mlog.info('[rack_to_exchange] unknown')
            result_obj = {
                'errno': ROBOT_ERROR_UNKNOWN,
                'msg': '' }
            return result_obj

    
    def vomit_disc(self, rfid, result_obj):
        self.clearResultQ()
        success = False
        for i in range(3):
            status = self._do_cmd('robot exchange rfid')
            if not status:
                continue
            
            if status[0] == 'ok':
                mlog.info('read rfid ok' + str(status))
                success = True
                break
            else:
                mlog.info('read rfid error:%s' % str(status))
        
        if not success:
            mlog.info('[vomit_disc] rfid misread')
            result_obj = {
                'errno': ROBOT_RFID_READ_ERROR,
                'msg': 'read rfid error',
                'rfid': '' }
            return result_obj
        elif rfid != status[2]:
            rfid_read = status[2]
            mlog.info('[vomit_disc] rfid unmatched')
            result_obj = {
                'errno': ROBOT_INVALID_RFID,
                'msg': 'read rfid error',
                'rfid': rfid_read }
            return result_obj
        else:
            mlog.info('[vomit_disc] eject ...')
            self.exchange_eject2()
            result_obj = {
                'errno': ROBOT_OK,
                'msg': '',
                'rfid': '' }
            return result_obj

    
    def reboot(self, result_obj):
        status = self._do_cmd('reboot', _async = False, tout = 5)
        result_obj = {
            'errno': ROBOT_OK }

    # def check_se_sensor(self):
    #   #  self._clear_status()
    #     r=self.rser.sendDataSync('robot exchange sensor dvd_full')
    #     s1 = self._get_status(r,10)
        
    #     #self._clear_status()
    #     r=self.rser.sendDataSync('robot exchange sensor dvd_mid')
    #     s2 = self._get_status(r,10)

    #     if int(s1[1])<200 and int(s2[1])<200:
    #         return True
    #     else:
    #         return False
    
    def exchange_eject2(self):
        while True:
            mlog.info('exchange_eject2')
            self.clearResultQ()
            status = self._do_cmd('robot exchange eject', _async = False, tout = 90)
            if status and status[0] == 'ok':
                break
            elif status and status[1].find('BUSY') != -1:
                self._cancel_cmd()
            

    
    def seek_zero(self, result_obj):
        status = self._do_cmd('robot control seek_top')
        status = self._do_cmd('robot control goto_exchange')

    
    def goto_exchange(self, result_obj, timeout = 60):
        status = self._do_cmd('robot control goto_exchange', tout = timeout)
        if status and status[0] == 'ok':
            result_obj = {
                'errno': ROBOT_OK,
                'msg': '' }
            return result_obj
        else:
            result_obj = {
                'errno': ROBOT_TIMEOUT,
                'msg': '' }
            return result_obj

    
    def exchange_close(self, result_obj):
        self._exchange_close()
        result_obj = {
            'errno': ROBOT_OK,
            'msg': '' }
        return result_obj

    
    def init_vertical(self, result_obj, timeout = 60):
        mlog.info('[init_vertical] begin')
        status = self._do_cmd('robot control init_vertical', tout = timeout)
        mlog.info('[init_vertical] result %s' % repr(status))
        if status:
            if status[0] == 'ok':
                result_obj = {
                    'errno': ROBOT_OK,
                    'msg': '' }
                return result_obj
            else:
                return {
                    'errno': status[0],
                    'msg': '' }
        else:
            result_obj = {
                'errno': ROBOT_TIMEOUT,
                'msg': '' }
            return result_obj

    
    def init_machine(self, result_obj, timeout = 120):
        mlog.info('init_machine begin')
        status = self._do_cmd('robot control init_machine', tout = timeout)
        mlog.info('[init_machine] result %s' % repr(status))
        if status:
            if status[0] == 'ok':
                result_obj = {
                    'errno': ROBOT_OK,
                    'msg': '' }
                return result_obj
            else:
                return {
                    'errno': status[0],
                    'msg': '' }
        else:
            result_obj = {
                'errno': ROBOT_TIMEOUT,
                'msg': '' }
            return result_obj