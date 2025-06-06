# Source Generated with Decompyle++
# File: backup_db_to_remote.pyc (Python 2.5)

''' Back up the mkc.db to remote server.
##
##  Change Log:
##      2010-11-12 Modified by Tim
##          Compress the log files before backup.
##      2009-11-05 Modified by Tim
##          Backup the mkc.log* to remote server.
##      2009-06-24 Modified by Tim
##          Change the host name to CName.
##      2009-02-25 Created by Tim
##
'''
import os
import time
import pexpect
import glob
import tarfile
from . import tools
from . import config
BACKUP_HOST = 'backup.cereson.com'
BACKUP_USER = 'backup'
BACKUP_PWD = 'howcute121'
log = tools.getLog('back_up_db.log', 'remote')

def compress_log(logFilePath):
    '''
    Compress the mkc log files to a tar.gz file to save the disk space of
    backup server.
    @param logFilePath(str)
    @return filepath(str): compress file path, if it is None, there is no log
            file.
    '''
    filepath = None
    files = glob.glob(logFilePath)
    if files:
        filepath = os.path.join(config.USER_ROOT, 'kiosk/tmp/mkc.log.tar.gz')
        files.sort()
        f = tarfile.open(filepath, 'w:gz')
        
        try:
            for fp in files:
                f.add(fp, 'log/%s' % os.path.basename(fp))
        finally:
            f.close()

    
    return filepath


def rsync(user, host, port, pwd, sourcePath, destPath, isDir = False, sync = False):
    ''' Rsync.
    @Params: user(str)
             host(str)
             port(str)
             sourcePath(str)
             destPath(str)
    @Return: status(int): 0: rsync failed
                          1: rsync success
             message(str)
    '''
    status = 0
    message = ''
    
    try:
        
        try:
            os.remove('/home/puyodead1/.ssh/known_hosts')
        except Exception as ex:
            log.info('Error when remove /home/puyodead1/.ssh/known_hosts: %s' % ex)

        if isDir:
            cmd = "ssh %s@%s 'mkdir -p %s'" % (user, host, destPath)
        elif sync:
            fileName = os.path.basename(sourcePath)
            filePath = os.path.dirname(sourcePath) + '/'
            cmd = 'rsync -avm --del '
            if port:
                cmd += " -e 'ssh -p %s' " % port
            else:
                cmd += ' -e ssh '
            cmd += "--include='%s' -f 'hide,! */' %s %s@%s:%s" % (fileName, filePath, user, host, destPath)
        else:
            cmd = 'rsync -avz --del '
            if port:
                cmd += " -e 'ssh -p %s' " % port
            else:
                cmd += ' -e ssh '
            cmd += '%s %s@%s:%s' % (sourcePath, user, host, destPath)
        log.info(cmd)
        child = pexpect.spawn(cmd, timeout = 30)
        y = child.expect([
            'password:',
            pexpect.TIMEOUT,
            pexpect.EOF,
            'Connection refused',
            '(yes/no)'], timeout = 30)
        if y == 4:
            msg = 'Connect the server first, and confirm the RES key.'
            log.info(msg)
            child.sendline('yes')
            y = child.expect([
                'password:',
                pexpect.TIMEOUT,
                pexpect.EOF,
                'Connection refused'], timeout = 30)
        
        if y == 0:
            for i in range(3):
                child.sendline(pwd)
                y = child.expect([
                    'password',
                    pexpect.TIMEOUT,
                    pexpect.EOF,
                    'file list ... done',
                    'receiving incremental file list'])
                if y in [
                    3,
                    4]:
                    msg = 'rsyncing ... time %s' % i
                    log.info(msg)
                    child.expect(pexpect.EOF, timeout = None)
                    before = child.before
                    log.info('Pexcept msg: %s' % before)
                    if before.find('speedup') >= 0 and before.find('total size') >= 0:
                        status = 1
                        message = ''
                        break
                    else:
                        status = 0
                        message = 'Unkown error when rsync: %s' % before
                elif y == 0:
                    msg = 'Password is incorrect: time %s' % i
                    log.error(msg)
                    message = 'Password is incorrect.'
                elif y == 1:
                    msg = 'Connection timeout: time %s' % i
                    log.error(msg)
                    message = 'Connection timeout.'
                elif isDir:
                    status = 1
                    break
                
                message = 'Unkown error when rsync: %s' % child.before
                log.error(message)
            
        elif y == 1:
            msg = 'Connection timeout...'
            log.error(msg)
            message = msg
        elif y == 3:
            msg = child.before
            log.error('Connection refused:Child before message:%s' % msg)
            message = 'Connection refused.'
        else:
            msg = child.before
            log.error('Child before message: %s' % msg)
            message = msg
        child.send('exit')
    except Exception as ex:
        status = 0
        log.error('Error in rsync(user:%s, host:%s, port:%s, sourcePath:%s, destPath:%s): %s' % (user, host, port, sourcePath, destPath, ex))
        message = 'Internal error: %s' % ex

    return (status, message)


def main():
    log.info('Begin backup db to remote.')
    
    try:
        flag = 0
        while True:
            if tools.isLocked():
                flag += 1
                time.sleep(15)
            else:
                break
            if flag >= 100:
                os.abort()
            
        kioskId = tools.getKioskId()
        (status, msg) = rsync(BACKUP_USER, BACKUP_HOST, '', BACKUP_PWD, '', '~/machines/%s/db/' % kioskId, isDir = True)
        if status == 0:
            raise Exception('Failed to make remote db dir for backup: %s' % msg)
        
        (status, msg) = rsync(BACKUP_USER, BACKUP_HOST, '', BACKUP_PWD, config.MKC_DB_PATH, '~/machines/%s/db/mkc.db' % kioskId)
        if status == 1:
            log.info('Backup db to remote successfully.')
        else:
            log.error('Backup db to remote failed: %s' % msg)
        logFilePath = os.path.join(config.USER_ROOT, 'kiosk/var/log/mkc.log*')
        logFilePath = compress_log(logFilePath)
        if logFilePath:
            (status, msg) = rsync(BACKUP_USER, BACKUP_HOST, '', BACKUP_PWD, '', '~/machines/%s/log/' % kioskId, isDir = True)
            if status == 0:
                raise Exception('Failed to make remote log dir for backup: %s' % msg)
            
            (status, msg) = rsync(BACKUP_USER, BACKUP_HOST, '', BACKUP_PWD, logFilePath, '~/machines/%s/log/' % kioskId, False)
            if status == 1:
                log.info('Backup db to remote successfully.')
            else:
                log.error('Backup db to remote failed: %s' % msg)
    except Exception as ex:
        log.error('Internal error when backup db error: %s' % ex)


if __name__ == '__main__':
    main()

