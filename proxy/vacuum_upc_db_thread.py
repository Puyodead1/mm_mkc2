# Source Generated with Decompyle++
# File: vacuum_upc_db_thread.pyc (Python 2.5)

''' Vacuum the upc database monthly to improve the retrieve speed.
##
##  Change Log:
##      2011-02-15 Created by Tim
##
'''
import os
import time
import datetime
import threading
from .mda import Db
from .tools import isLocked, getLog
from .config import USER_ROOT
NEW_UPC_DB_PATH = os.path.join(USER_ROOT, 'kiosk/var/db/new_upc.db')
VACUUM_TIME_PATH = os.path.join(USER_ROOT, 'kiosk/var/db/.vacuum_upc_db_time')

class VacuumUpcDbThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self, name = 'VACUUM_UPC_DB_THREAD')
        self.init()

    
    def init(self):
        '''
        Init some params for the thread.
        @Params: None
        @Return: None
        '''
        self.last_access_time = datetime.datetime.now()
        self.access_time = self.last_access_time
        self.last_vacuum_time = None

    
    def run(self):
        '''
        Update the upc db for the kiosks.
        '''
        self.log = getLog('vacuum_upc_db_thread.log', 'UPDATION')
        self.log.info('Thread start...')
        self.last_vacuum_time = self._get_last_vacuum_time()
        while True:
            self.access_time = datetime.datetime.now()
            if not None if 2 <= 2 else 2 < self.access_time.hour:
                time.sleep(300)
                self.last_access_time = self.access_time
                continue
            
            if not self._need_vacuum():
                time.sleep(300)
                self.last_access_time = self.access_time
                continue
            
            tries = 0
            MAX_TRIES = 30
            while True:
                tries += 1
                if isLocked():
                    if tries >= MAX_TRIES:
                        break
                    
                    time.sleep(30)
                else:
                    
                    try:
                        self._vacuum()
                        self._set_last_vacuum_time(str(int(time.time())))
                        time.sleep(3600)
                    except Exception:
                        ex = None
                        self.log.error('vacuum failed: %s' % ex)

        self.log.info('Thread end...')
        del self.log

    
    def _get_last_vacuum_time(self):
        ''' get last vacuum time, return None if the time is not set
        '''
        vacuum_time = None
        fd = None
        
        try:
            fd = open(VACUUM_TIME_PATH)
            vacuum_time = int(fd.read().strip())
        except Exception:
            ex = None
            self.log.warning('_get_last_vacuum_time: %s' % ex)
        finally:
            if fd:
                fd.close()
            

        return vacuum_time

    
    def _set_last_vacuum_time(self, vacuum_time):
        ''' set last vacuum time
        '''
        fd = None
        
        try:
            fd = open(VACUUM_TIME_PATH, 'w')
            fd.write(str(vacuum_time))
        except Exception:
            ex = None
            self.log.warning('_set_last_vacuum_time: %s' % ex)
        finally:
            if fd:
                fd.close()
            


    
    def _vacuum(self):
        ''' vacuum the database to speed up the query of the database
        '''
        db = Db(NEW_UPC_DB_PATH)
        self.log.info('vacuum begin')
        db.update('vacuum;')
        self.log.info('vacuum end')
        del db

    
    def _need_vacuum(self):
        ''' check if the kiosk need to vacuum
        '''
        need = True
        
        try:
            last_vacuum_time = self._get_last_vacuum_time()
            if last_vacuum_time:
                vacuum_time_obj = datetime.datetime(*list(time.localtime(last_vacuum_time))[:-2])
                if vacuum_time_obj.strftime('%Y-%m') >= self.access_time.strftime('%Y-%m'):
                    need = False
                
        except Exception:
            ex = None
            self.log.warning('_need_vacuum: %s' % ex)

        return need



def main():
    vacuumThread = VacuumUpcDbThread()
    vacuumThread.start()

if __name__ == '__main__':
    main()

