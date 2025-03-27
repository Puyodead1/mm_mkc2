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
import proxy.tools as ptools
from mobject import *
'\n# =================================================================\n# =    ROBOT Const (For Tesing Only)\n# -----------------------------------------------------------------\nROBOT_OK = "0"\nROBOT_TIMEOUT = "1"\nROBOT_EXCHANGE_JAM = "2"\nROBOT_CARRIAGE_JAM = "3"\nROBOT_NO_DISC = "4"\n'

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
        except Exception:
            ex = None
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
    startHdmi = startHdmi
    import linuxCmd
    startHdmi()


def stopHdmi():
    stopHdmi = stopHdmi
    import linuxCmd
    stopHdmi()
    "\n    2009-04-24 Commented out by Vincent: \n    flproxy.py will restart the flash itself\n    stopHdmi()    \n    \n    # Start Flash Screen\n    FLASH_PLAYER = '~/bin/flashplayer'\n    FLASH_PROG = '~/kiosk/mkc2/screen/mkt.swf'\n    cmd = FLASH_PLAYER+' '+FLASH_PROG+' --display :0 2>/dev/null &'\n    os.system(cmd)\n\n    time.sleep(5)\n\n    startHdmi()    \n    "


def initRobot(top_offset = None, bottom_offset = None, exchange_offset = None, back_offset = None, offset2xx = None, offset6xx = None):
    Robot = Robot
    import control
    ConnProxy = ConnProxy
    import proxy.conn_proxy
    robot1 = Robot()
    robot = robot1.getInstance()
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
    Robot = Robot
    ROBOT_OK = ROBOT_OK
    ROBOT_TIMEOUT = ROBOT_TIMEOUT
    import control
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
        language]).install(str = True)
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
        fd = open('/home/mm/kiosk/tmp/.active_information', 'r')
        information = fd.read().strip()
        fd.close()
    except:
        pass

    return information


def set_active_information(active_information = ''):
    fd = open('/home/mm/kiosk/tmp/.active_information', 'wb')
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
'\nSteps to form a resource file\n1. xgettext -o test.pot --keyword="_" test.py\n2. msginit -l es_ES.UTF-8 -o test.po -i test.pot\n3. mv test.po ./locale/es/LC_MESSAGES;cd ./locale/es/LC_MESSAGES\n4. msgfmt -c -v -o test.mo test.po\n'
