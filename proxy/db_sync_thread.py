# Source Generated with Decompyle++
# File: db_sync_thread.pyc (Python 2.5)

''' Sync data to remote service.
##
##  Change Log:
##      2011-01-12 Modified by Tim
##          change the syncRemoteKioskData for a new column kiosk_id
##      2010-09-27 Modified by Tim
##          Add new sync method db_sync_no_sequence.
##      2009-11-30 Modified by Tim
##          Do not add kiosk time for the public message.
##      2009-06-22 Modified by Tim
##          For #1741, add kiosk time into the mail for kioskSendEmail.
##      2009-04-08 Modified by Tim
##          Add a new function syncNonRealTimeDataImme.
##      2009-03-05 Modified by Tim
##          Delete the sync records 3 months ago.
##
'''
__version__ = '1.0.015'
import os
import sys
import threading
import http.client
import urllib.request, urllib.parse, urllib.error
import time
import socket
import logging
from logging import handlers
from .mda import Db
from .tools import getKioskId, getLog, getCurTime, getTimeChange, isLocked, getTimeZone
from .config import *
HOST = '127.0.0.1'
SLEEP_PERIOD = [
    1,
    10,
    60,
    300,
    600]

class DbSyncThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self, name = 'DB_SYNC_THREAD')
        self.init()

    
    def init(self):
        self.kioskId = getKioskId()
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
        self.log = getLog('db_sync_thread.log', 'DB_SYNC_THREAD')
        self.log.info('Thread start...')
        self.syncDb = Db(SYNC_DB_PATH)
        self.lastError = ''
        self.rmSyncBefore3Month()
        while True:
            if str(isLocked()) == '0':
                self.syncNoSequenceData(funcList = [
                    'kioskSendEmail'])
                self.syncRemoteKioskData()
                record = None
                
                try:
                    record = self.getOneRecord()
                except IOError:
                    ex = None
                    if str(ex).lower().find('broken pipe') > -1:
                        self.log.critical('Critical error in get one record: %s' % str(ex))
                        sys.exit()
                    else:
                        self.log.error('Error occurs when get one record: %s' % str(ex))
                except Exception:
                    ex = None
                    msg = 'Error occurs when get one record: %s'
                    self.log.error(msg % str(ex))
                    continue

                if record:
                    self.syncOneRecord(record)
                else:
                    self.syncNoSequenceData()
                    time.sleep(60)
                time.sleep(SLEEP_PERIOD[self.sleep_period_index])
            else:
                time.sleep(60)

    
    def syncOneRecord(self, record):
        ''' Sync one record to remote server.
        @Params: record(Dict): {"id":12, "funcName":"funcName", "port":121,
                                "params":"{}", "state":0}
        @Return: None
        '''
        
        try:
            syncId = record['id']
            port = record['port']
            funcName = record['funcName']
            paramsStr = record['params']
            addTime = record['add_time']
            
            try:
                params = eval(paramsStr)
            except Exception:
                ex = None
                msg = 'Error when eval the params(%s): %s'
                raise Exception(msg % (paramsStr, str(ex)))

            params['syncId'] = syncId
            params['sync_add_time'] = addTime
            params['sync_kiosk_time_zone'] = getTimeZone()
            result = self.getRemoteData(port, funcName, params)
            if result['result'].lower() == 'ok':
                state = 1
                self.setSyncStateById(state, syncId)
                msg = '%s ok'
                self._reset_time_sleep()
                self.log.info(msg % str(syncId))
            elif result['result'].lower() == 'timeout':
                time.sleep(60)
                result = self.getRemoteData(port, 'checkSyncId', {
                    'syncId': syncId })
                if result['result'].lower() == 'ok':
                    state = 1
                    self.setSyncStateById(state, syncId)
                    msg = '%s ok' % syncId
                    self._reset_time_sleep()
                    self.log.info(msg)
                else:
                    self._increase_time_sleep()
                    msg = '%s: %s' % (syncId, result['zdata'])
                    if self.lastError != msg:
                        self.log.error(msg)
                        self.lastError = msg
                    
            elif result['result'].lower() == 'socketerror':
                self._increase_time_sleep()
                msg = '%s: %s' % (syncId, result['zdata'])
                if self.lastError != msg:
                    self.log.critical(msg)
                    self.lastError = msg
                
            else:
                self._increase_time_sleep()
                msg = '%s: %s' % (syncId, result['zdata'])
                if self.lastError != msg:
                    self.log.error(msg)
                    self.lastError = msg
        except IOError:
            ex = None
            if str(ex).lower().find('broken pipe') > -1:
                self.log.critical('Critical error in syncOneRecord: %s' % ex)
                sys.exit()
            else:
                self.log.error('Error occurs when syncOneRecord: %s' % ex)
        except Exception:
            ex = None
            self._increase_time_sleep()
            msg = 'Error when syncOneRecord for (%s): %s'
            self.log.error(msg % (record, ex))
        


    
    def syncNoSequenceData(self, funcList = []):
        ''' Sync no sequence of non-real time data to service.
        @param funcList(list): only sync data of the function list
        @return: None
        '''
        
        try:
            sql = 'SELECT id, function_name, port_num, params, state,add_time FROM db_sync_no_sequence WHERE '
            if len(funcList) > 1:
                sql += 'function_name IN %s AND ' % tuple(funcList)
            elif len(funcList) == 1:
                sql += "function_name='%s' AND " % funcList[0]
            
            sql += 'state=0;'
            rows = self.syncDb.query(sql)
            for row in rows:
                
                try:
                    syncId = row[0]
                    funcName = row[1]
                    port = row[2]
                    params = eval(row[3])
                    addTime = row[5]
                    
                    try:
                        if funcName.upper() == 'KIOSKSENDEMAIL' and params['msg_type'].upper() != 'PUBLIC':
                            msg = params['message']
                            msg += '<br /><br />Kiosk Time: %s' % addTime
                            params['message'] = msg
                    except Exception:
                        ex = None
                        m = 'Error when change msg in syncNoSequenceData : %s' % ex
                        self.log.error(m)

                    params['syncId'] = syncId
                    params['sync_add_time'] = addTime
                    params['sync_kiosk_time_zone'] = getTimeZone()
                    result = self.getRemoteData(port, funcName, params)
                    if result['result'].lower() == 'ok':
                        state = 1
                        sql = "update db_sync_no_sequence set state=%s, sync_time=DATETIME('now','localtime') where id=%s;" % (state, syncId)
                        self.syncDb.update(sql)
                        self._reset_time_sleep()
                        self.log.info('NS %s ok' % syncId)
                    else:
                        self._increase_time_sleep()
                        if self.lastError != result:
                            self.lastError = result
                            self.log.error('NS %s: %s' % (syncId, result))
                except Exception:
                    ex = None
                    m = 'Error when syncNoSequenceData : %s' % str(ex)
                    self.log.error(m)
                    self._increase_time_sleep()
                

                time.sleep(SLEEP_PERIOD[self.sleep_period_index])
        except IOError:
            ex = None
            if str(ex).lower().find('broken pipe') > -1:
                self.log.critical('Critical error in syncNoSequenceData: %s' % ex)
                sys.exit()
            else:
                self.log.error('Error in syncNoSequenceData: %s' % ex)
        except Exception:
            ex = None
            m = 'Error when syncNoSequenceData: %s' % ex
            self.log.error(m)


    
    def syncRemoteKioskData(self):
        ''' Sync sequence data of non-real time to service.
        @param None
        @return: None
        '''
        
        try:
            sql = 'SELECT DISTINCT remote_kiosk_id FROM db_sync_remote_kiosk WHERE state=0;'
            kioskIds = self.syncDb.query(sql)
            for kioskId, in kioskIds:
                
                try:
                    sql = 'SELECT id, function_name, port_num, params, state, add_time FROM db_sync_remote_kiosk WHERE state=0 AND remote_kiosk_id=?;'
                    rows = self.syncDb.query(sql, 'all', (kioskId,))
                    for row in rows:
                        
                        try:
                            syncId = row[0]
                            funcName = row[1]
                            port = row[2]
                            params = eval(row[3])
                            addTime = row[5]
                            params['syncId'] = syncId
                            params['sync_add_time'] = addTime
                            params['sync_kiosk_time_zone'] = getTimeZone()
                            result = self.getRemoteData(port, funcName, params)
                            if result['result'].lower() == 'ok':
                                state = 1
                                sql = "UPDATE db_sync_remote_kiosk SET state=%s, sync_time=DATETIME('now','localtime') WHERE id=%s;" % (state, syncId)
                                self.syncDb.update(sql)
                                self._reset_time_sleep()
                                self.log.info('RK %s %s ok' % (funcName, syncId))
                            else:
                                self._increase_time_sleep()
                                if self.lastError != result:
                                    self.lastError = result
                                    self.log.error('RK %s: %s' % (syncId, result))
                                
                        except Exception:
                            ex = None
                            m = 'syncRemoteKioskData: %s' % ex
                            self.log.error(m)
                            self._increase_time_sleep()

                        time.sleep(SLEEP_PERIOD[self.sleep_period_index])
                except Exception:
                    ex = None
                    m = 'syncRemoteKioskData(%s): %s' % (kioskId, ex)
                    self.log.error(m)

        except IOError:
            ex = None
            if str(ex).lower().find('broken pipe') > -1:
                self.log.critical('Critical error in syncRemoteKioskData: %s' % ex)
                sys.exit()
            else:
                self.log.error('Error in syncRemoteKioskData: %s' % ex)
        except Exception:
            ex = None
            self.log.error('Error in syncRemoteKioskData: %s' % ex)


    
    def getOneRecord(self):
        result = { }
        sql = 'select id, function_name, port_num, params, add_time, state from db_sync where id in (select min(id) from db_sync where state=0);'
        row = self.syncDb.query(sql, 'one')
        if row:
            (id, funcName, port, params, addTime, state) = row
            result['id'] = id
            result['funcName'] = funcName
            result['port'] = port
            result['params'] = params
            result['add_time'] = addTime
            result['state'] = state
        
        return result

    
    def setSyncStateById(self, state, syncId):
        for i in range(5):
            
            try:
                if str(state) == '1':
                    sql = "update db_sync set state=:state, sync_time=DATETIME('now', 'localtime') where id=:syncId;"
                else:
                    sql = 'update db_sync set state=:state where id=:syncId;'
                self.syncDb.update(sql, {
                    'state': state,
                    'syncId': syncId })
            except Exception:
                ex = None
                msg = 'Time %s: Error when setSyncStateById to (%s) for %s: %s'
                self.log.error(msg % (i, state, syncId, ex))
                if i >= 4:
                    raise 
                
            except:
                i >= 4

        

    
    def rmSyncBefore3Month(self):
        '''
        Remove the succeful sync records before 3 months.
        '''
        
        try:
            syncDate = getTimeChange(getCurTime(), month = -3)
            sql = 'DELETE FROM db_sync WHERE state=1 AND sync_time<?;'
            self.syncDb.update(sql, (syncDate,))
            sql = 'DELETE FROM db_sync_remote_kiosk WHERE state=1 AND sync_time<?;'
            self.syncDb.update(sql, (syncDate,))
            sql = 'DELETE FROM db_sync_no_sequence WHERE state=1 AND sync_time<?;'
            self.syncDb.update(sql, (syncDate,))
        except Exception:
            ex = None
            self.log.error('Error in rmSyncBefore3Month: %s' % ex)


    
    def getRemoteData(self, port, funcName, params):
        '''
        Get data from Remote Server.
        '''
        url = '/api'
        return self._httpCall(url, port, {
            'function_name': funcName,
            'params': params })

    
    def _httpCall(self, url, port, params):
        '''Calls a remote function on a web server'''
        http = http.client.HTTPConnection(HOST, port)
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain',
            'Kiosk': self.kioskId }
        urlParams = urllib.parse.urlencode(params)
        result = {
            'result': 'error',
            'zdata': 'Eval error' }
        
        try:
            http.request('POST', url, urlParams, headers)
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
    syncThread = DbSyncThread()
    syncThread.start()

if __name__ == '__main__':
    main()

