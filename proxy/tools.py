# Source Generated with Decompyle++
# File: tools.pyc (Python 2.5)

'''
##
##  Change Log:
##      2009-09-09 Modified by Tim
##          Add lock for log.
##      2009-08-20 Modified by Tim
##          Make the log support unicode.
##      2008-01-04 Modified by Tim
##          Remove the buffering in logging.
##
'''
import os
import sys
import time
import socket
import fcntl
import struct
import traceback
import glob
import shutil
import threading
from time import strptime
from datetime import datetime, date, timedelta
from calendar import monthrange
from .config import *

class RemoteError(Exception):
    pass


class Result:
    
    def __init__(self):
        self.errno = 0
        self.message = ''



def dbDir():
    return os.path.abspath(os.curdir)
    return userRoot


def getKioskId():
    f = None
    
    try:
        f = open('/proc/sys/kernel/hostname')
        kioskId = f.read().strip()
        return kioskId
    finally:
        if hasattr(f, 'close'):
            f.close()
        



def getKioskCapacity():
    capacity = '250'
    f = None
    
    try:
        f = open('/etc/kioskcapacity')
        capacity = f.read().strip()
    except:
        pass
    finally:
        if hasattr(f, 'close'):
            f.close()
        

    return capacity


def getTimeZone():
    f = None
    timeZone = 'US/Pacific'
    
    try:
        f = open('/etc/timezone')
        timeZone = f.read().strip()
        return timeZone
    finally:
        if hasattr(f, 'close'):
            f.close()
        



def getEthMac(ifname = 'eth0'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hwaddr = ''
    
    try:
        info = fcntl.ioctl(s.fileno(), 35111, struct.pack('256s', ifname[:15]))
        for char in info[18:24]:
            hdigit = hex(ord(char))[2:]
            if len(hdigit) < 2:
                hwaddr = hwaddr + '0' + hdigit
            else:
                hwaddr = hwaddr + str(hdigit)
            hwaddr = hwaddr + ':'
    except:
        pass

    return hwaddr[:17]
    '\n    cmd = " /sbin/ifconfig |sed -n \'s/.*HWaddr\\(.*\\)/\\1/p\' "\n    write_fd,read_fd = os.popen2(cmd)\n    all = read_fd.readlines()\n    write_fd.close()\n    read_fd.close()\n    return all[0][:-1].strip()      #[:-1] rm the \'\n\'\n    '


def getEthIP(ifname = 'eth0'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    result = ''
    
    try:
        result = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 35093, struct.pack('256s', ifname[:15]))[20:24])
    except:
        result = '127.0.0.1'

    return result
    '\n    cmd = "  /sbin/ifconfig | sed -n \'s/.*inet addr:\\([^ ]*\\).*/\\1/p\' "\n    write_fd,read_fd = os.popen2(cmd)\n    all = read_fd.readlines()\n    write_fd.close()\n    read_fd.close()\n    i = 0\n    while all[i] == \'127.0.0.1\':\n        i += 1\n    return all[i][:-1].strip()\n    '


def getLinuxDate():
    return time.strftime('%a %b %d %H:%M:%S %Z %Y')
    '\n    cmd = " /bin/date "\n    write_fd,read_fd = os.popen2(cmd)\n    all = read_fd.readlines()\n    write_fd.close()\n    read_fd.close()\n    return all[0][:-1]      #[:-1] rm the \'\n\'\n    '


def getCurTime(timeFMT = '%Y-%m-%d %H:%M:%S'):
    return time.strftime(timeFMT)


def getMinuteSpan(startTime, endTime):
    ''' return span minutes between startTime and endTime '''
    result = 0
    if len(str(startTime).split(' ')) == 1:
        startTime = str(startTime) + ' 00:00:00'
    
    if len(str(endTime).split(' ')) == 1:
        endTime = str(endTime) + ' 00:00:00'
    
    dst = datetime(*time.strptime(startTime, '%Y-%m-%d %H:%M:%S')[:6])
    det = datetime(*time.strptime(endTime, '%Y-%m-%d %H:%M:%S')[:6])
    if dst and det:
        delta = det - dst
        days = delta.days
        seconds = delta.seconds
        minutes = days * 24 * 60 + seconds / 60
        result = minutes
    
    return result


def getDaySpan(startTime, endTime):
    ''' return span days between startTime and endTime '''
    result = 0
    if len(str(startTime).split(' ')) == 1:
        startTime = str(startTime) + ' 00:00:00'
    
    if len(str(endTime).split(' ')) == 1:
        endTime = str(endTime) + ' 00:00:00'
    
    dst = datetime(*time.strptime(startTime, '%Y-%m-%d %H:%M:%S')[:6])
    det = datetime(*time.strptime(endTime, '%Y-%m-%d %H:%M:%S')[:6])
    if dst and det:
        days = (det - dst).days
        result = days
    
    return result


def getTimeChange(oldTime, year = 0, month = 0, day = 0, hour = 0, minute = 0, second = 0):
    if len(oldTime.split(' ')) == 2:
        FMTTIME = '%Y-%m-%d %H:%M:%S'
    elif len(oldTime.split(' ')) == 1:
        FMTTIME = '%Y-%m-%d'
    else:
        FMTTIME = '%Y-%m-%d'
    
    try:
        timeTouple = time.strptime(oldTime, FMTTIME)
        if len(timeTouple) == 9:
            year += timeTouple[0]
            month += timeTouple[1]
            day += timeTouple[2]
            hour += timeTouple[3]
            minute += timeTouple[4]
            second += timeTouple[5]
            tmp1 = timeTouple[6]
            tmp2 = timeTouple[7]
            tmp3 = timeTouple[8]
            newTimeTouple = (year, month, day, hour, minute, second, tmp1, tmp2, tmp3)
            return time.strftime(FMTTIME, time.localtime(time.mktime(newTimeTouple)))
        else:
            return oldTime
    except:
        return oldTime



def currentWeekRange():
    return getWeekRange(getCurTime('%Y-%m-%d'))


def currentMonthRange():
    currentYear = date.today().year
    currentMonth = date.today().month
    return getMonthRange(currentYear, currentMonth)


def currentYearRange():
    currentYear = date.today().year
    return getYearRange(currentYear)


def getWeekRange(dateStr):
    d = date(*strptime(dateStr, '%Y-%m-%d')[0:3])
    weekBegin = d - timedelta((d.weekday() + 1) % 7)
    weekEnd = weekBegin + timedelta(6)
    weekBeginStr = weekBegin.strftime('%Y-%m-%d')
    weekEndStr = weekEnd.strftime('%Y-%m-%d')
    return (weekBeginStr, weekEndStr)


def getDateRange(fromDateStr, toDateStr):
    """ Return every day's date between fromDate to toDate.
    """
    fromDateStr = fromDateStr.split(' ')[0]
    fromDate = date(*strptime(fromDateStr, '%Y-%m-%d')[0:3])
    toDateStr = toDateStr.split(' ')[0]
    toDate = date(*strptime(toDateStr, '%Y-%m-%d')[0:3])
    dateRange = []
    iterDate = fromDate
    while iterDate <= toDate:
        dateRange.append(iterDate.strftime('%Y-%m-%d'))
        iterDate += timedelta(1)
    return dateRange


def getWeekSpans(fromDateStr, toDateStr):
    ''' Calculate which week of month the day is in.
        '''
    
    def getWeekNo(d):
        ''' Calculate which week of month the day is in.
        '''
        firstDayInMonth = date(d.year, d.month, 1)
        v1 = int(firstDayInMonth.strftime('%U'))
        v2 = int(d.strftime('%U'))
        return (v2 - v1) + 1

    fromDateStr = fromDateStr.split(' ')[0]
    toDateStr = toDateStr.split(' ')[0]
    fromDate = date(*strptime(fromDateStr, '%Y-%m-%d')[0:3])
    toDate = date(*strptime(toDateStr, '%Y-%m-%d')[0:3])
    timeSpans = []
    iterDate = fromDate - timedelta((fromDate.weekday() + 1) % 7)
    while iterDate <= toDate:
        iterDateStr = iterDate.strftime('%Y-%m-%d')
        weekSpan = getWeekRange(iterDateStr)
        d1 = date(*strptime(weekSpan[0], '%Y-%m-%d')[0:3])
        weekNo = getWeekNo(d1)
        month = d1.strftime('%B')
        year = d1.year
        title = 'Week %s, %s, %s' % (weekNo, month, year)
        timeSpans.append((title, weekSpan))
        if weekSpan[0][5:7] != weekSpan[1][5:7]:
            d2 = date(*strptime(weekSpan[1], '%Y-%m-%d')[0:3])
            weekNo = getWeekNo(d2)
            month = d2.strftime('%B')
            year = d2.year
            title = 'Week %s, %s, %s' % (weekNo, month, year)
            timeSpans.append((title, weekSpan))
        
        iterDate = iterDate + timedelta(7)
    return timeSpans


def getMonthRange(year, month):
    monthBegin = date(year, month, 1)
    lastDay = monthrange(year, month)[1]
    monthEnd = date(year, month, lastDay)
    monthBeginStr = monthBegin.strftime('%Y-%m-%d')
    monthEndStr = monthEnd.strftime('%Y-%m-%d')
    return (monthBeginStr, monthEndStr)


def getMonthSpans(fromDateStr, toDateStr):
    ''' Give the time spans of the months from fromDateStr to toDateStr
        each span contains title and a tuple (fromDate, toDate)
    '''
    fromDateStr = fromDateStr.split(' ')[0]
    toDateStr = toDateStr.split(' ')[0]
    fromDate = date(*strptime(fromDateStr, '%Y-%m-%d')[0:3])
    toDate = date(*strptime(toDateStr, '%Y-%m-%d')[0:3])
    iterDate = fromDate
    y = 0
    m = 0
    monthSpans = []
    while iterDate < toDate:
        if y != iterDate.year or m != iterDate.month:
            y = iterDate.year
            m = iterDate.month
            monthRange = getMonthRange(y, m)
            title = iterDate.strftime('%B, %Y')
            monthSpans.append((title, monthRange))
        
        iterDate += timedelta(days = 1)
    if y != toDate.year and m != toDate.month:
        title = toDate.strftime('%B, %Y')
        monthRange = getMonthRange(toDate.year, toDate.month)
        monthSpans.append((title, monthRange))
    
    return monthSpans


def getYearRange(year):
    yearBegin = date(year, 1, 1)
    yearEnd = date(year, 12, 31)
    yearBeginStr = yearBegin.strftime('%Y-%m-%d')
    yearEndStr = yearEnd.strftime('%Y-%m-%d')
    return (yearBeginStr, yearEndStr)


def getYearSpans(fromDateStr, toDateStr):
    '''
        Get the time spans of years from fromDateStr to toDateStr. The time span
        consists of first day and last day of the year.
        output: (title, (first day, last day))
        title is a string like the "2006", "2007", etc.
    '''
    fromDateStr = fromDateStr.split(' ')[0]
    toDateStr = toDateStr.split(' ')[0]
    fromDate = date(*strptime(fromDateStr, '%Y-%m-%d')[0:3])
    toDate = date(*strptime(toDateStr, '%Y-%m-%d')[0:3])
    fromYear = fromDate.year
    toYear = toDate.year
    yearSpans = []
    for year in range(fromYear, toYear + 1):
        title = str(year)
        yearSpans.append((title, getYearRange(year)))
    
    return yearSpans


def getTimeSpanRange(fromDateSpan, toDateSpan):
    ''' Return a tuple contains fromDateSpan days before today and toDateSpan days after today '''
    result = ('', '')
    fromDateDelta = timedelta(fromDateSpan)
    toDateDelta = timedelta(toDateSpan)
    today = date.today()
    fromDate = (today + fromDateDelta).strftime('%Y-%m-%d')
    toDate = (today + toDateDelta).strftime('%Y-%m-%d')
    result = (fromDate, toDate)
    return result


def getWeekday(dateStr):
    if len(dateStr.split(' ')) == 2:
        FMTTIME = '%Y-%m-%d %H:%M:%S'
    elif len(dateStr.split(' ')) == 1:
        FMTTIME = '%Y-%m-%d'
    else:
        FMTTIME = '%Y-%m-%d'
    return date.weekday(date(*time.strptime(dateStr, FMTTIME)[:3]))


def getLog(fileName = 'proxy.log', loggerName = 'PROXY', rotateType = 'SIZE', maxBytes = 0, maxCount = 0):
    '''
    Get log object.
    '''
    log = Log(os.path.join(COMMON_LOG_FILE_PATH, fileName), loggerName, rotateType, maxBytes, maxCount)
    return log


def fmtMoney(money):
    newMoney = '%.2f' % round(float(money), 2)
    return newMoney


def sqlQuote(value):
    return str(value).replace("'", "''")


def fmtNoneStr(value):
    if str(value).lower() == 'none':
        value = ''
    
    return value


def formatEI(maxTBlevel = 5):
    (cla, exc, trbk) = sys.exc_info()
    excName = cla.__name__
    
    try:
        excArgs = exc.__dict__['args']
    except KeyError:
        excArgs = '<no args>'

    excTb = traceback.format_tb(trbk, maxTBlevel)
    return (excName, excArgs, excTb)


class Log:
    glock = threading.Lock()
    
    def __init__(self, logPath, logUser = 'SYSTEM', rotateType = 'SIZE', maxBytes = 0, maxCount = 0):
        self.filePath = logPath
        self.user = logUser
        self.rotateType = rotateType
        if self.rotateType == 'DATE':
            rotateAtToday = time.mktime(time.strptime(self._getCurrTime('%Y-%m-%d 23:59:59'), '%Y-%m-%d %H:%M:%S'))
            rotateAtYesterday = rotateAtToday - 60 * 60 * 24
            ctime = rotateAtToday
            if os.path.exists(self.filePath):
                ctime = os.path.getctime(self.filePath)
            
            if ctime <= rotateAtYesterday:
                self.rotateAt = rotateAtYesterday
            else:
                self.rotateAt = rotateAtToday
        else:
            self.rotateAt = None
        if maxBytes == 0:
            self.maxBytes = COMMON_LOG_FILE_SIZE
        else:
            self.maxBytes = maxBytes
        if maxCount == 0:
            self.maxCount = COMMON_LOG_FILE_COUNT
        else:
            self.maxCount = maxCount
        self.file = open(self.filePath, 'a')
        self._lock = threading.Lock()

    
    def __del__(self):
        if hasattr(self.file, 'close'):
            self.file.close()
        
        del self.file

    
    def info(self, msg = ''):
        self._log('INFO', msg)

    
    def warning(self, msg = ''):
        self._log('WARNING', msg)

    
    def error(self, msg = ''):
        self._log('ERROR', msg)

    
    def fatal(self, msg = ''):
        self._log('FATAL', msg)

    
    def critical(self, msg = ''):
        self._log('CRITICAL', msg)

    
    def debug(self, msg = ''):
        
        try:
            pass
        except:
            pass


    
    def _log(self, logType = 'INFO', msg = ''):
        print(msg)
        logTime = self._getCurrTime('%y-%m-%d %H:%M:%S')
        logMsg = '%-18s%9s %10s %s\n' % (logTime, logType, self.user, msg)
        self._writeToFile(logMsg)

    
    def _getCurrTime(self, FMT = '%Y-%m-%d %H:%M:%S'):
        return time.strftime(FMT)

    
    def _writeToFile(self, logMsg = ''):
        
        try:
            logMsg = logMsg.encode(sys.getfilesystemencoding())
            self._lock.acquire()
            
            try:
                if self._shouldRotate():
                    self._fileRotate()
                
                self.file.write(logMsg)
                self.file.flush()
            finally:
                self._lock.release()

            print(logMsg)
        except:
            pass


    
    def _shouldRotate(self):
        ''' Check if the file should rotate. '''
        self.should = 0
        Log.glock.acquire()
        
        try:
            if self.rotateType.upper() == 'DATE':
                self.should = self._shouldRotateDate()
            
            if self.should == 0:
                self.should = self._shouldRotateSize()
        finally:
            Log.glock.release()

        return self.should

    
    def _shouldRotateSize(self):
        ''' Check if the file should rotate. '''
        should = 0
        
        try:
            if self.maxBytes > 0:
                self.file.seek(0, 2)
                if self.file.tell() >= self.maxBytes:
                    should = 2
                
            else:
                raise Exception('maxByte is %s' % str(self.maxBytes))
        except Exception as ex:
            print('Error in _shouldRotateSize: ', str(ex))

        return should

    
    def _shouldRotateDate(self):
        ''' Check if the file should rotate. '''
        should = 0
        
        try:
            if time.time() > self.rotateAt:
                should = 1
        except Exception as ex:
            print('Error in _shouldRotateDate: ', str(ex))

        return should

    
    def _fileRotate(self):
        ''' File rotate. '''
        Log.glock.acquire()
        
        try:
            if self.rotateType.upper() == 'SIZE':
                self._fileRotateSize()
            else:
                self._fileRotateDate()
        finally:
            Log.glock.release()


    
    def _clearLog(self):
        if self.rotateType.upper() == 'DATE':
            s = glob.glob(self.filePath + '.2?*')
            while len(s) > self.maxCount - 1:
                s.sort()
                os.remove(s[0])
                s = glob.glob(self.filePath + '.2?*')
        

    
    def _fileRotateSize(self):
        ''' File rotate. '''
        
        try:
            if self.maxCount > 0:
                self.file.close()
                for i in range(self.maxCount - 1, 0, -1):
                    sfd = '%s.%d' % (self.filePath, i)
                    dfd = '%s.%d' % (self.filePath, i + 1)
                    if os.path.exists(sfd):
                        if os.path.exists(dfd):
                            os.remove(dfd)
                        
                        os.rename(sfd, dfd)
                    
                
                dfd = '%s.1' % self.filePath
                if os.path.exists(dfd):
                    os.remove(dfd)
                
                os.rename(self.filePath, dfd)
                self.file = open(self.filePath, 'a')
            else:
                raise Exception('maxCount is %s' % str(self.maxCount))
        except Exception as ex:
            print('Error in _fileRotateSize: ', str(ex))


    
    def _fileRotateDate(self):
        ''' File rotate. '''
        
        try:
            if self.maxCount > 0:
                self.file.close()
                self._clearLog()
                if self.should == 2:
                    todayFile = self.filePath + '.' + time.strftime('%Y-%m-%d')
                    for i in range(self.maxCount - 1, 0, -1):
                        sfd = '%s.%d' % (todayFile, i)
                        dfd = '%s.%d' % (todayFile, i + 1)
                        if os.path.exists(sfd):
                            if os.path.exists(dfd):
                                os.remove(dfd)
                            
                            os.rename(sfd, dfd)
                        
                    
                    dfd = '%s.1' % todayFile
                    if os.path.exists(dfd):
                        os.remove(dfd)
                    
                    os.rename(self.filePath, dfd)
                else:
                    dfn = self.filePath + '.' + time.strftime('%Y-%m-%d', time.localtime(self.rotateAt))
                    temp = '%s.1' % dfn
                    if os.path.exists(temp):
                        dfn = '%s.0' % dfn
                    
                    if not os.path.exists(dfn):
                        os.rename(self.filePath, dfn)
                    
                self.file = open(self.filePath, 'a')
                self.rotateAt = time.mktime(time.strptime(self._getCurrTime('%Y-%m-%d 23:59:59'), '%Y-%m-%d %H:%M:%S'))
            else:
                raise Exception('maxCount is %s' % str(self.maxCount))
        except Exception as ex:
            print('Error in _fileRotateDate: ', str(ex))




def lock():
    _saveThreadLock(1)


def unlock():
    _saveThreadLock(0)


def _saveThreadLock(val):
    f = None
    
    try:
        f = open(LOCK_FILE_PATH, 'w', False)
        f.write(str(val))
    except:
        pass
    finally:
        if hasattr(f, 'close'):
            f.close()
        



def isLocked():
    lock = 0
    f = None
    
    try:
        f = open(LOCK_FILE_PATH)
        lock = int(f.read().strip())
    except:
        pass
    finally:
        if hasattr(f, 'close'):
            f.close()
        

    return lock


def checkDNS():
    ''' check if the dns is ok.
    
    @param None
    @return: is_ok(bool) 
    '''
    
    try:
        socket.setdefaulttimeout(5)
        socket.gethostbyname('upg.cereson.com')
        return True
    except:
        return False



def testLog():
    log = getLog('test.log', 'TEST', 'DATE', 3000, 5)
    for i in range(22222):
        log.info('info')
        log.error('error')
        log.debug('debug')
        log.fatal('fatal')
        log.critical('critical')
        log.warning('warning')
        time.sleep(0.5)
    


def _testTime():
    startTime = '2008-01-02 01:00:00'
    endTime = '2008-01-03 01:00:01'
    print(getDaySpan(startTime, endTime))
    print(getMinuteSpan(startTime, endTime))
    print(getWeekday('2008-01-03'))


def _testDateRange():
    print(currentWeekRange())
    print(currentMonthRange())
    print(currentYearRange())
    print(getDateRange('2008-01-02 12:12:12', '2008-02-02 12:12:12'))
    print(getWeekSpans('2008-01-02 12:12:12', '2008-02-02 12:12:12'))
    print(getMonthSpans('2008-01-02 12:12:12', '2008-02-02 12:12:12'))
    print(getYearSpans('2008-01-02 12:12:12', '2008-02-02 12:12:12'))

if __name__ == '__main__':
    testLog()

