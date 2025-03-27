# Source Generated with Decompyle++
# File: upload_video_thread.pyc (Python 2.5)

''' Upload the video to server
##
##  Change Log:
##      2012-10-10 Created by Kitch
##
'''
__version__ = '1.0.017'
import os
import sys
import threading
import http.client
import urllib.request, urllib.parse, urllib.error
import time
import socket
import glob
import pexpect
from .mda import Db
from .tools import getKioskId, getLog, getCurTime, getTimeChange, isLocked, getTimeZone
from .config import *
SLEEP_PERIOD = [
    1,
    10,
    60,
    300,
    600]

class UploadVideoThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self, name = 'UPLOAD_VIDEO_THREAD')
        self.init()

    
    def init(self):
        self.kiosk_id = getKioskId()
        self.sleep_period_index = 0
        
        try:
            self.http_timeout = DEFAULT_SOCKET_TIMEOUT
        except Exception:
            ex = None
            self.http_timeout = 300


    
    def run(self):
        '''
        Sync the record from sync.db to remote server.
        '''
        self.log = getLog('upload_video_thread.log', 'UPLOAD_VIDEO_THREAD')
        self.log.info('Thread start...')
        self.mkc_db = Db(MKC_DB_PATH)
        self.sync_db = Db(SYNC_DB_PATH)
        self.clear_videos()
        while True:
            if str(isLocked()) == '0':
                upload_list = self.get_upload_list()
                for itm in upload_list:
                    local_file = os.path.join(VIDEO_PATH, itm['video_name'])
                    if os.path.exists(local_file):
                        server_file = os.path.join(VIDEO_SERVER_PATH, itm['video_url'])
                        (status, msg) = self.rsync(VIDEO_SERVER_USER, VIDEO_SERVER_HOST, '', VIDEO_SERVER_PASSWORD, '', os.path.dirname(server_file), isDir = True)
                        if status == 0:
                            self.log.error('Failed to make remote db dir for video: %s' % msg)
                            self._increase_time_sleep()
                        else:
                            (status, msg) = self.rsync(VIDEO_SERVER_USER, VIDEO_SERVER_HOST, '', VIDEO_SERVER_PASSWORD, local_file, server_file)
                            if status == 1:
                                itm['state'] = 'closed'
                                self.add_sync(itm)
                                self.set_upload_state_by_id(itm['id'], 'closed')
                                self._reset_time_sleep()
                            else:
                                self.log.error('Failed to upload video: %s' % msg)
                                self._increase_time_sleep()
                    else:
                        self.del_upload_by_id(itm['id'])
                        self.log.warning('The video %s does not exist.' % itm['video_name'])
                    time.sleep(SLEEP_PERIOD[self.sleep_period_index])
                
                time.sleep(120)
            else:
                time.sleep(60)

    
    def get_upload_list(self):
        result = []
        sql = "SELECT id, rfid, upc, title, action_time, action_type, slot_id, cc_display, state, video_name, video_url, error_msg FROM failed_trs WHERE state='open';"
        rows = self.mkc_db.query(sql)
        for row in rows:
            data = { }
            data['id'] = row[0]
            data['rfid'] = row[1]
            data['upc'] = row[2]
            data['title'] = row[3]
            data['action_time'] = row[4]
            data['action_type'] = row[5]
            data['slot_id'] = row[6]
            data['cc_display'] = row[7]
            data['state'] = row[8]
            data['video_name'] = row[9]
            data['video_url'] = row[10]
            data['error_msg'] = row[11]
            result.append(data)
        
        return result

    
    def set_upload_state_by_id(self, upload_id, state):
        for i in range(5):
            
            try:
                sql = 'UPDATE failed_trs SET state=? WHERE id=?;'
                self.mkc_db.update(sql, (state, upload_id))
            except Exception:
                ex = None
                msg = 'Times %s: Error when set_upload_state_by_id to (%s) for %s: %s'
                self.log.error(msg % (i, state, upload_id, ex))
                if i >= 4:
                    raise 
                
            except:
                i >= 4

        

    
    def del_upload_by_id(self, upload_id):
        for i in range(5):
            
            try:
                sql = 'DELETE FROM failed_trs WHERE id=?;'
                self.mkc_db.update(sql, (upload_id,))
            except Exception:
                ex = None
                msg = 'Times %s: Error when del_upload_by_id %s: %s'
                self.log.error(msg % (i, upload_id, ex))
                if i >= 4:
                    raise 
                
            except:
                i >= 4

        

    
    def add_sync(self, params):
        for i in range(5):
            
            try:
                sql = "INSERT INTO db_sync(function_name, port_num, params, add_time) VALUES('db_sync_failed_trs', ?, ?, ?);"
                self.sync_db.update(sql, (PROXY_DATA['CONN_PROXY']['SYNC_PORT'], repr(params), getCurTime()))
            except Exception:
                ex = None
                msg = 'Times %s: Error when add_sync: %s'
                self.log.error(msg % (i, ex))
                if i >= 4:
                    raise 
                
            except:
                i >= 4

        

    
    def clear_videos(self):
        '''
        Remove the videos before 3 months
        '''
        
        try:
            rm_date = getTimeChange(getCurTime(), month = -3)
            dirs = glob.glob('%s/????-??-??' % VIDEO_PATH)
            for itm in dirs:
                if os.path.isdir(itm):
                    dir_date = itm.split('/')[-1]
                    if dir_date < rm_date:
                        os.system('rm -rf %s' % itm)
                        self.log.info('Removed dir %s' % itm)
                    
                
        except Exception:
            ex = None
            self.log.error('Error in clear_videos: %s' % ex)


    
    def rsync(self, user, host, port, pwd, sourcePath, destPath, isDir = False, sync = False):
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
                os.remove('/home/mm/.ssh/known_hosts')
            except Exception:
                ex = None
                self.log.info('Error when remove /home/mm/.ssh/known_hosts: %s' % ex)

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
            self.log.info(cmd)
            child = pexpect.spawn(cmd, timeout = 30)
            y = child.expect([
                'password:',
                pexpect.TIMEOUT,
                pexpect.EOF,
                'Connection refused',
                '(yes/no)'], timeout = 30)
            if y == 4:
                msg = 'Connect the server first, and confirm the RES key.'
                self.log.info(msg)
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
                        self.log.info(msg)
                        child.expect(pexpect.EOF, timeout = None)
                        before = child.before
                        self.log.info('Pexcept msg: %s' % before)
                        if before.find('speedup') >= 0 and before.find('total size') >= 0:
                            status = 1
                            message = ''
                            break
                        else:
                            status = 0
                            message = 'Unkown error when rsync: %s' % before
                    elif y == 0:
                        msg = 'Password is incorrect: time %s' % i
                        self.log.error(msg)
                        message = 'Password is incorrect.'
                    elif y == 1:
                        msg = 'Connection timeout: time %s' % i
                        self.log.error(msg)
                        message = 'Connection timeout.'
                    elif isDir:
                        status = 1
                        break
                    
                    message = 'Unkown error when rsync: %s' % child.before
                    self.log.error(message)
                
            elif y == 1:
                msg = 'Connection timeout...'
                self.log.error(msg)
                message = msg
            elif y == 3:
                msg = child.before
                self.log.error('Connection refused:Child before message:%s' % msg)
                message = 'Connection refused.'
            else:
                msg = child.before
                self.log.error('Child before message: %s' % msg)
                message = msg
            child.send('exit')
        except Exception:
            ex = None
            status = 0
            self.log.error('Error in rsync(user:%s, host:%s, port:%s, sourcePath:%s, destPath:%s): %s' % (user, host, port, sourcePath, destPath, ex))
            message = 'Internal error: %s' % ex

        return (status, message)

    
    def get_remote_data(self, port, funcName, params):
        '''
        Get data from Remote Server.
        '''
        url = '/api'
        return self._http_call(url, port, {
            'function_name': funcName,
            'params': params })

    
    def _http_call(self, url, port, params):
        '''Calls a remote function on a web server'''
        http = http.client.HTTPConnection(HOST, port)
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain',
            'Kiosk': self.kiosk_id }
        url_params = urllib.parse.urlencode(params)
        result = {
            'result': 'error',
            'zdata': 'Eval error' }
        
        try:
            http.request('POST', url, url_params, headers)
            http.sock.settimeout(self.http_timeout)
            r = http.getresponse()
            data = r.read()
            result = eval(data)
        except socket.timeout:
            ex = None
            result = {
                'result': 'timeout',
                'zdata': 'Connection timeout' }
        except socket.error:
            ex = None
            result = {
                'result': 'socketerror',
                'zdata': 'Connection Refused' }
        except Exception:
            ex = None
            msg = str(ex)
            self.log.error('httpCall exception: ' + msg)
            result = {
                'result': 'error',
                'zdata': 'connection error: %s' % msg }

        return result

    
    def _increase_time_sleep(self):
        self.sleep_period_index += 1
        if self.sleep_period_index > 4:
            self.sleep_period_index = 4
        

    
    def _reset_time_sleep(self):
        self.sleep_period_index = 0



def main():
    thread = UploadVideoThread()
    thread.start()

if __name__ == '__main__':
    main()

