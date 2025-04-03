# Source Generated with Decompyle++
# File: RfidChecker.pyc (Python 2.5)

import sys
import os
import traceback
from mcommon import *
from proxy.conn_proxy import ConnProxy
from RobotController import *
from config import KIOSK_HOME
import proxy.tools as ptools

class SlotInfo:
    
    def __init__(self, hasdisc = False, rfid = ''):
        self.dbHasDisc = hasdisc
        self.realHasDisc = False
        self.dbRfid = rfid
        self.realRfid = ''
        self.check = ''

    
    def __str__(self):
        if self.dbHasDisc == self.realHasDisc and self.dbRfid == self.realRfid:
            x = 'PASS'
        else:
            x = 'FAIL'
        return '%s | %s | %s | %s | %s' % (str(self.dbHasDisc).ljust(8), str(self.realHasDisc).ljust(8), self.dbRfid.ljust(18), self.realRfid.ljust(18), x)



class RfidChecker:
    
    def __init__(self):
        self.log = ptools.getLog('checkRfid.log', 'checkRack', 'DATE', maxCount = 7)
        self.proxy = ConnProxy.getInstance()
        self.controller = RobotController(self.log, 'CR-')
        self.statistics = { }

    
    def lockMkc(self):
        ptools._saveThreadLock(1)

    
    def unlockMkc(self):
        ptools._saveThreadLock(0)

    
    def stopMkc(self):
        self.log.info('Stop MKC.')
        os.system('cd /home/puyodead1/kiosk/mkc2;./mkc.py stop')

    
    def startMkc(self):
        self.log.info('Start MKC.')
        os.system('cd /home/puyodead1/kiosk/mkc2;./mkc.py start')

    
    def start(self):
        self.log.info('===================== Start Check RFID =======================')
        self.log.info('===================== **************** =======================')
        self.starttime = time.strftime('%Y-%m-%d %H:%M:%S')
        self.log.info('============== Start time : %s' % self.starttime)

    
    def end(self):
        self.log.info('============================ END =============================')
        self.endtime = time.strftime('%Y-%m-%d %H:%M:%S')
        self.log.info('============== End time : %s' % self.endtime)

    
    def doCheck(self):
        self.start()
        self.log.info('Query DB to get kiosk information.')
        allslots = self.proxy.getSlotIds()
        for slot in allslots:
            self.statistics[slot] = SlotInfo()
        
        rows = self.proxy.getInDiscs()
        for row in rows:
            discInfo = self.statistics[row[0]]
            discInfo.dbHasDisc = True
            discInfo.dbRfid = row[1]
        
        
        try:
            slots = list(self.statistics.keys())
            slots.sort()
            for slot in slots:
                info = self.statistics[slot]
                self._checkOneDisc(slot, info)
            
            self.finish()
        except NoDiscException as ex:
            self.log.error(ex.message)
        except RobotException as ex:
            self.log.error(ex.message)
        except Exception:
            msg = 'Unknown exception raised.'
            self.log.error('%s ----> %s' % (msg, traceback.format_exc()))
        finally:
            self.end()


    
    def finish(self):
        self.controller.gotoExchange()

    
    def _checkOneDisc(self, slotid, discinfo):
        logstr = '* * * * * * Check slot %s, ' % slotid
        if discinfo.dbHasDisc == True:
            logstr += 'should has disc with RFID %s' % discinfo.dbRfid
        else:
            logstr += 'should be empty'
        self.log.info(logstr)
        
        try:
            self.controller.rackToExchange(slotid)
            
            try:
                discinfo.realHasDisc = True
                discinfo.realRfid = self.controller.readRfid()
            except:
                discinfo.realRfid = 'RFID Fail'
                self.log.error('Read rfid failed.')
                self.log.error(traceback.format_exc())

        except NoDiscException:
            discinfo.realHasDisc = False
            discinfo.realRfid = ''
            if discinfo.dbHasDisc == True:
                self.log.error('There is no disc in slot %d.' % slotid)
            
            return None
        except:
            self.log.error(traceback.format_exc())
            sys.exit(-1)

        
        try:
            self.controller.exchangeToRack(slotid)
        except:
            self.log.error(traceback.format_exc())
            sys.exit(-1)


    
    def dostatis(self):
        filestr = os.path.join(KIOSK_HOME, 'kiosk/var/log/rfid')
        file = open(filestr, 'a')
        file.write('================= RFID Check Start : %s =================\n' % self.starttime)
        xstr = 'SLOT'.ljust(4) + '| ' + 'DB DISC'.center(8) + ' | ' + 'REAL DISC'.center(8) + '| ' + 'DB RFID'.center(18) + ' | ' + 'REAL RFID'.center(18) + ' | ' + 'PASS\n'
        file.write(xstr)
        slots = list(self.statistics.keys())
        slots.sort()
        for slot in slots:
            info = self.statistics[slot]
            file.write('%s| %s\n' % (str(slot).ljust(4), str(info)))
        
        file.write('===================== END Time : %s =====================\n' % self.endtime)
        file.write('\n\n\n')
        file.close()


if __name__ == '__main__':
    rc = RfidChecker()
    rc.stopMkc()
    rc.lockMkc()
    rc.doCheck()
    rc.dostatis()
    rc.unlockMkc()
    rc.startMkc()
    os._exit(0)

