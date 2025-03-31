# Source Generated with Decompyle++
# File: manage_kiosk_thread.pyc (Python 2.5)

'''
##  Thread management for kiosk.
##
##  Change Log:
##      2012-01-10 Modified by Tim
##          add the frequentness of the backup to remote service
##      2009-03-06 Created by Tim
##
'''
import threading
import datetime
import time
import os
from .tools import getLog
from . import backup_db_to_local
from . import backup_db_to_remote
from . import conn_proxy

class BakupDbThread(threading.Thread):
    
    def __init__(self, bakType, runTime):
        threading.Thread.__init__(self, name = 'BACKUP_DB_THREAD')
        self.bakType = bakType
        self.runTime = runTime

    
    def run(self):
        log = getLog('kiosk_thread.log', 'thread')
        
        try:
            log.info('BakupDbThread::Begin to run for %s:%s' % (self.bakType, self.runTime))
            if self.bakType == 'remote':
                backup_db_to_remote.main()
            elif self.bakType == 'local':
                backup_db_to_local.main()
            
            log.info('BakupDbThread::End to run for %s:%s' % (self.bakType, self.runTime))
        except Exception as ex:
            log.error('BakupDbThread::Error when run report for %s:%s:%s' % (self.bakType, self.runTime, ex))




class ManageThread(object):
    
    def __init__(self):
        self.log = getLog('kiosk_thread.log', 'manager')
        self.anotherDay = False
        self.lastCheckTime = datetime.datetime.now()
        self.count = 0
        self.interval_second = 300
        self.remote_interval = self.get_backup_remote_interval()

    
    def get_backup_remote_interval(self):
        ''' get the frequentness of the backup to remote server
        '''
        interval = 72
        
        try:
            _proxy = conn_proxy.ConnProxy.getInstance()
            conf = _proxy._getConfigByKey('backup_db_interval_hour')
            interval = int(float(conf) * 3600 / self.interval_second)
        except:
            import traceback
            self.log.warning(traceback.format_exc())

        return interval

    
    def run(self):
        self.log.info('Thread start run .....')
        while True:
            
            try:
                now = datetime.datetime.now()
                if '06:00:00' <= '06:00:00':
                    pass
                elif '06:00:00' <= now.strftime('%H:%M:%S'):
                    self.log.info('Thread end to run .....')
                    os.abort()
                
                if '02:00' <= '02:00':
                    pass
                elif '02:00' <= now.strftime('%H:%M:%S'):
                    bakup = BakupDbThread('local', str(now))
                    bakup.run()
                
                if self.count % self.remote_interval == 0:
                    bakup = BakupDbThread('remote', str(now))
                    bakup.run()
                
                if self.count % 6 == 0:
                    pass
                
                self.lastCheckTime = now
                self.count += 1
                if self.count >= 8640:
                    self.count = 0
            except IOError as ex:
                if str(ex).lower().find('broken pipe') > -1:
                    self.log.error('ManageThread(%s)::Fatal error: %s' % (self.count, ex))
                    os.abort()
                else:
                    self.log.error('ManageThread::Error when running ManageThread(%s):%s' % (self.count, ex))
            except Exception as ex:
                self.log.error('ManageThread::Error when running ManageThread(%s):%s' % (self.count, ex))

            time.sleep(self.interval_second)


if __name__ == '__main__':
    t = ManageThread()
    t.run()

