# Source Generated with Decompyle++
# File: backup_db_to_local.pyc (Python 2.5)

''' Backup mkc.db to local.
##
##  Change Log:
##      2009-06-24 Modified by Tim
##          Change the backupPath.
##      2009-02-25 Created by Tim
##
'''
import shutil
import os
import time
import datetime
from . import tools
from . import config
log = tools.getLog('back_up_db.log', 'local')

def backup(sourcePath, destPath):
    (status, msg) = (0, '')
    
    try:
        destDirs = os.path.dirname(destPath)
        if not os.path.exists(destDirs):
            os.makedirs(destDirs)
        
        shutil.copy(sourcePath, destPath)
        status = 1
    except Exception:
        ex = None
        msg = 'Error in backup: %s' % ex

    return (status, msg)


def main():
    log.info('Begin to backup db to local.')
    
    try:
        while True:
            if tools.isLocked():
                time.sleep(15)
            else:
                break
        weekOfDay = datetime.datetime.now().isoweekday()
        backupPath = os.path.join(config.USER_ROOT, 'backup/data/mkc.db.%s' % weekOfDay)
        (status, msg) = backup(config.MKC_DB_PATH, backupPath)
        if status == 1:
            log.info('Backup db to local successfully.')
        else:
            log.info('Backup db to local failed: %s' % msg)
    except Exception:
        ex = None
        log.error('Error when backup: %s' % ex)


if __name__ == '__main__':
    main()

