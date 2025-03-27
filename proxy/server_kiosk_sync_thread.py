# Source Generated with Decompyle++
# File: server_kiosk_sync_thread.pyc (Python 2.5)

''' Sync data from remote server to kiosk.

Change Log:
    2011-03-09 Modified by Kitch
        add util: markUnloadDiscs
    2010-06-24 Modified by Kitch
        add util: setDefaultPricePlan, setPricePlan
    2009-12-21 Modified by Kitch

'''
__version__ = '0.5.3'
import os
import sys
import time
from .mda import Db
from .conn_proxy import ConnProxy
from .tools import getKioskId, getLog, getCurTime, getTimeChange, isLocked, sqlQuote
from .config import *

class ServerKioskSyncThread(object):
    
    def __init__(self):
        self.log = getLog('server_kiosk_sync_thread.log', 'SERVER_KIOSK_SYNC_THREAD')
        self.syncDb = Db(SYNC_DB_PATH)
        self.proxy = ConnProxy.getInstance()
        self.needResync = False

    
    def __del__(self):
        del self.log
        del self.syncDb
        del self.proxy

    
    def run(self):
        self.log.info('Thread start...')
        time.sleep(300)
        while True:
            self._checkTableServerQueue()
            self._downloadServerQueue()
            sequence = True
            cId = 0
            queue = self._getNeedSyncQueueOne(sequence, cId)
            while queue:
                if not self._getThreadLock():
                    print(queue)
                    if self._syncOneQueue(queue):
                        self._setSyncQueueStateById(1, queue['id'])
                    elif str(queue['sequence_sensitive']) == '0' and sequence == True:
                        cId = queue['id']
                    else:
                        sequence = False
                        cId = queue['id']
                    time.sleep(1)
                    queue = self._getNeedSyncQueueOne(sequence, cId)
                else:
                    print('Kiosk is busy. Wait 5 minutes...')
                    time.sleep(300)
            if self.needResync:
                
                try:
                    sql = "UPDATE db_sync SET state=1 WHERE function_name<>'setMonthlySubscptForKiosk';"
                    self.syncDb.update(sql)
                    for i in range(5):
                        result = self.proxy.getRemoteData('resyncDb', { }, 180)
                        if result['result'] == 'ok':
                            self.needResync = False
                            break
                        else:
                            print('Something wrong. Please try again.')
                            self.log.error('remote: %s' % result['zdata'])
                except Exception:
                    ex = None
                    self.log.error('resync db: %s' % str(ex))

            
            time.sleep(600)

    
    def _getThreadLock(self):
        return isLocked()

    
    def _checkTableServerQueue(self):
        ''' check if the table server_queue exists; if not, create
        @Params: None
        @Return: None
        '''
        
        try:
            exist = 0
            sql = "SELECT COUNT(*) FROM sqlite_master WHERE name='server_queue'"
            row = self.syncDb.query(sql, 'one')
            if row:
                (exist,) = row
            
            if not exist:
                sql = 'CREATE TABLE server_queue\n(\n    id INTEGER,\n    type TEXT,\n    api TEXT,\n    params TEXT,\n    sequence_sensitive INTEGER,\n    add_time TEXT,\n    sync_time TEXT,\n    state INTEGER\n);'
                self.syncDb.update(sql)
        except Exception:
            ex = None
            msg = '_checkTableServerQueue: %s' % str(ex)
            self.log.error(msg)


    
    def _downloadServerQueue(self):
        ''' download the queue from server
        @Params: None
        @Return: None
        '''
        
        try:
            sql = 'SELECT MAX(id) FROM server_queue;'
            maxId = 0
            row = self.syncDb.query(sql, 'one')
            if row:
                (maxId,) = row
                if maxId is None:
                    maxId = 0
                
            
            funcName = 'downloadSyncQueue'
            params = {
                'max_id': maxId }
            resultDic = self.proxy.getRemoteData(funcName, params)
            if str(resultDic.get('result', '')).lower() == 'ok':
                queueList = resultDic['zdata']
                sql = 'INSERT INTO server_queue(id, type, api, params, sequence_sensitive, add_time, state) VALUES(:id, :type, :api, :params, :sequence_sensitive, :add_time, 0);'
                for queue in queueList:
                    self.syncDb.update(sql, queue)
                
            else:
                self.log.error('_downloadServerQueue: %s' % resultDic['zdata'])
        except IOError:
            ex = None
            if str(ex).lower().find('broken pipe') > -1:
                self.log.critical('_downloadServerQueue IOError: %s' % str(ex))
                sys.exit()
            
        except Exception:
            ex = None
            msg = '_downloadServerQueue: %s' % str(ex)
            self.log.error(msg)


    
    def _getNeedSyncQueueOne(self, sequence = True, cId = 0):
        ''' get one need sync queue
        @Params: None
        @Return: queue (dict)
        '''
        queue = { }
        
        try:
            strWhere = 'WHERE state=0 '
            if not sequence:
                strWhere += 'AND sequence_sensitive=0 '
            
            if cId:
                strWhere += "AND id>'%s' " % cId
            
            sql = 'SELECT id, type, api, params, sequence_sensitive FROM server_queue %s ORDER BY id LIMIT 1;' % strWhere
            row = self.syncDb.query(sql, 'one')
            if row:
                (qId, qType, api, params, sequenceSensitive) = row
                queue['id'] = qId
                queue['type'] = qType
                queue['api'] = api
                queue['params'] = params
                queue['sequence_sensitive'] = sequenceSensitive
        except IOError:
            ex = None
            if str(ex).lower().find('broken pipe') > -1:
                self.log.critical('_getNeedSyncQueueOne IOError: %s' % str(ex))
                sys.exit()
            
        except Exception:
            ex = None
            msg = '_getNeedSyncQueueOne: %s' % str(ex)
            self.log.error(msg)

        return queue

    
    def _syncOneQueue(self, queue):
        ''' sync one queue
        @Params: queue (dict)
        @Return: 1 or 0
        '''
        result = 0
        
        try:
            funcName = queue['api']
            params = eval(queue['params'])
            print(funcName, params)
            kioskUtil = KioskUtils()
            func = getattr(kioskUtil, funcName, None)
            del kioskUtil
            if func is not None:
                if hasattr(func, '__call__'):
                    
                    try:
                        res = func(*params)
                        if str(queue['type']).lower() == 'data':
                            self.needResync = True
                        
                        self.log.info('success: %s' % queue['id'])
                        result = 1
                    except Exception:
                        ex = None
                        self.log.error('error(%s): %s' % (queue['id'], str(ex)))

                else:
                    self.log.error('No such method.')
            else:
                self.log.error('No such method.')
        except IOError:
            ex = None
            if str(ex).lower().find('broken pipe') > -1:
                self.log.critical('_syncOneQueue IOError: %s' % str(ex))
                sys.exit()
            
        except Exception:
            ex = None
            msg = '_syncOneQueue: %s' % str(ex)
            self.log.error(msg)

        return result

    
    def _setSyncQueueStateById(self, state, syncId):
        for i in range(5):
            
            try:
                if str(state) == '1':
                    sql = "update server_queue set state=?, sync_time=DATETIME('now', 'localtime') where id=?;"
                else:
                    sql = 'update server_queue set state=? where id=?;'
                self.syncDb.update(sql, (state, syncId))
            except IOError:
                ex = None
                if str(ex).lower().find('broken pipe') > -1:
                    self.log.critical('_setSyncQueueStateById IOError: %s' % str(ex))
                    sys.exit()
                
            except Exception:
                ex = None
                msg = 'Times %s: Error when setSyncQueueStateById to (%s) for %s: %s'
                self.log.error(msg % (i, state, syncId, ex))
                if i >= 4:
                    raise 
                
            except:
                i >= 4

        



class LinuxCmd(object):
    ''' Execute Linux Command.
    e.g. lc = LinuxCmd()
         lc.execute("ls") # Return the result of ls.
         lc.execute("pkill python", True)  # Return \'0\' or \'1\'.
    '''
    
    def __init__(self):
        pass

    
    def execute(self, cmd, noResult = False):
        ''' Execute a linux command line.
        @Params: cmd(String): Command line
                 noResult(Boolean): True: Return \'0\'(Success) or \'1\'(Failure)
                                    False: Return the result of cmd.
        @Return: \'0\', \'1\', "success" or "".
        '''
        w = None
        r = None
        result = ''
        
        try:
            if noResult:
                result = os.system(cmd)
                result = str(result)
            else:
                (w, r) = os.popen2(cmd)
                result = r.read()
        except Exception:
            ex = None
            result = 'Error when execute cmd(%s): %s' % (cmd, str(ex))

        if hasattr(w, 'close'):
            w.close()
        
        if hasattr(r, 'close'):
            r.close()
        
        return result



class KioskUtils(object):
    
    def __init__(self):
        pass

    
    def __del__(self):
        pass

    
    def _getDbPath(self, dbName):
        dbPaths = {
            'mkc': MKC_DB_PATH,
            'upc': UPC_DB_PATH,
            'newupc': NEW_UPC_DB_PATH,
            'media': MEDIA_DB_PATH,
            'sync': SYNC_DB_PATH }
        return dbPaths[dbName.lower()]

    
    def query(self, dbName, sql, fetch = 'all', params = ()):
        db = Db(self._getDbPath(dbName))
        result = db.query(sql, fetch, params)
        del db
        return result

    
    def update(self, dbName, sql, params = ()):
        db = Db(self._getDbPath(dbName))
        newId = db.update(sql, params)
        del db
        return newId

    
    def updateMany(self, dbName, sql, params = []):
        db = Db(self._getDbPath(dbName))
        db.updateMany(sql, params)
        del db
        return None

    
    def updateTrs(self, dbName, sqlList = []):
        db = Db(self._getDbPath(dbName))
        db.updateTrs(sqlList)
        del db
        return None

    
    def executeScript(self, dbName, sql):
        db = Db(self._getDbPath(dbName))
        db.executeScript(sql)
        del db
        return None

    
    def _execCmd(self, cmd, noResult = False):
        lc = LinuxCmd()
        return lc.execute(cmd, noResult)

    
    def upgradeSoftware(self):
        cmd = 'touch %s' % os.path.join(USER_ROOT, 'kiosk/tmp/need_update')
        self._execCmd(cmd)
        return 1

    
    def rebootKiosk(self):
        cmd = 'python %s' % os.path.join(USER_ROOT, 'kiosk/utilities/kioskReboot.py')
        self._execCmd(cmd)
        return 1

    
    def setKioskLogo(self):
        proxy = ConnProxy.getInstance()
        proxy.getKioskLogo()
        del proxy

    
    def resyncDb(self):
        pass

    
    def setDefaultPricePlan(self, pricePlanId):
        db = Db(self._getDbPath('mkc'))
        exist = 0
        sql = 'SELECT COUNT(id) FROM price_plans WHERE id=?;'
        row = db.query(sql, 'one', (pricePlanId,))
        if row:
            (exist,) = row
        
        if exist:
            sql = "UPDATE config SET value=? WHERE variable='default_price_plan';"
            db.update(sql, (pricePlanId,))
        
        del db

    
    def setPricePlan(self, pricePlanId):
        proxy = ConnProxy.getInstance()
        result = proxy.getRemoteData('getClientPricePlanByIdForKiosk', {
            'pp_id': pricePlanId })
        if result['result'] == 'ok':
            data = result['zdata']
            if data:
                db = Db(self._getDbPath('mkc'))
                sqlList = []
                sql = "DELETE FROM price_plans WHERE id='%s';"
                sql = sql % sqlQuote(pricePlanId)
                sqlList.append(sql)
                sql = "INSERT INTO price_plans(id, data, data_text) VALUES('%s', '%s', '%s');"
                sql = sql % (sqlQuote(pricePlanId), sqlQuote(data['data']), sqlQuote(data['data_text']))
                sqlList.append(sql)
                db.updateTrs(sqlList)
                del db
            
        else:
            raise Exception(result['zdata'])

    
    def downloadPricePlans(self):
        proxy = ConnProxy.getInstance()
        result = proxy.getRemoteData('getClientPricePlanListForKiosk', { })
        if result['result'] == 'ok':
            data = result['zdata']
            if data:
                db = Db(self._getDbPath('mkc'))
                sqlList = []
                sql = 'DELETE FROM price_plans;'
                sqlList.append(sql)
                sql = "INSERT INTO price_plans(id, data, data_text) VALUES('%s', '%s', '%s');"
                for itm in data:
                    sqlList.append(sql % (sqlQuote(itm['id']), sqlQuote(itm['data']), sqlQuote(itm['data_text'])))
                
                db.updateTrs(sqlList)
                del db
            
        else:
            raise Exception(result['zdata'])

    
    def copyWeeklyPricePlan(self, fromKiosk, copyDay):
        proxy = ConnProxy.getInstance()
        result = proxy.getRemoteData('getMachineWeeklyPricePlansV2', {
            'machine_id': fromKiosk })
        if result['result'] == 'ok':
            data = result['zdata']
            if data:
                db = Db(self._getDbPath('mkc'))
                if copyDay:
                    for itm in data:
                        if itm['title'] == copyDay:
                            sql = 'UPDATE price_plans_week SET price_plan=?, price_plan_text=?, price_plan_br=?, price_plan_text_br=?, price_plan_game=?, price_plan_text_game=? WHERE title=?;'
                            db.update(sql, (itm['price_plan'], itm['price_plan_text'], itm['price_plan_br'], itm['price_plan_text_br'], itm['price_plan_game'], itm['price_plan_text_game'], itm['title']))
                            break
                        
                    
                else:
                    sqlList = []
                    sql = "UPDATE price_plans_week SET price_plan='%s', price_plan_text='%s', price_plan_br='%s', price_plan_text_br='%s', price_plan_game='%s', price_plan_text_game='%s' WHERE title='%s';"
                    for itm in data:
                        sqlList.append(sql % (sqlQuote(itm['price_plan']), sqlQuote(itm['price_plan_text']), sqlQuote(itm['price_plan_br']), sqlQuote(itm['price_plan_text_br']), sqlQuote(itm['price_plan_game']), sqlQuote(itm['price_plan_text_game']), sqlQuote(itm['title'])))
                    
                    db.updateTrs(sqlList)
                del db
            
        else:
            raise Exception(result['zdata'])

    
    def markUnloadDiscs(self, upcs, leftNumber):
        ''' mark discs to unload state

        @param upcs: str, fmt: "(\'1212\', \'3434\', ...)" or "(\'1212\')"
        @param leftNumber: int, the left number of the upc
        '''
        db = Db(self._getDbPath('mkc'))
        leftNumber = int(leftNumber)
        if leftNumber == 0:
            sql = "UPDATE rfids SET state='unload' WHERE state='in' AND upc IN %s;" % upcs
            db.update(sql)
        else:
            upcs = eval(upcs)
            if type(upcs) == type(''):
                upcs = (upcs,)
            
            sql = "UPDATE rfids SET state='unload' WHERE upc=? AND state='in' AND rfid NOT IN (SELECT rfid FROM rfids WHERE upc=? AND state='in' LIMIT %s);"
            sql = sql % leftNumber
            for upc in upcs:
                db.update(sql, (upc, upc))
            

    
    def markUnloadDiscsV2(self, upcs, leftNumber, noRentalDays):
        ''' mark discs to unload state

        @param upcs: str, fmt: "(\'1212\', \'3434\', ...)" or "(\'1212\')"
        @param leftNumber: int, the left number of the upc
        @param noRentalDays: int, unload those have not been rented in noRentalDays
        '''
        db = Db(self._getDbPath('mkc'))
        leftNumber = int(leftNumber)
        noRentalDays = int(noRentalDays)
        sql = 'SELECT upc, MAX(out_time) FROM transactions WHERE upc IN %s GROUP BY upc;' % upcs
        rows = db.query(sql)
        upcOutTime = { }
        for upc, out_time in rows:
            upcOutTime[upc] = out_time
        
        sql = "SELECT data3, MIN(time_recorded) FROM events WHERE action='load' AND data3 IN %s GROUP BY data3;" % upcs
        rows = db.query(sql)
        upcLoadTime = { }
        for upc, load_time in rows:
            upcLoadTime[upc] = load_time
        
        unloadUpcs = []
        upcs = eval(upcs)
        if type(upcs) == type(''):
            upcs = (upcs,)
        
        for upc in upcs:
            if upc in upcOutTime:
                noRentalTime = upcOutTime[upc]
            else:
                noRentalTime = upcLoadTime.get(upc, '')
            if noRentalTime < getTimeChange(getCurTime(), day = -noRentalDays):
                unloadUpcs.append(upc)
            
        
        strUpcs = '(%s)' % ','.join(f"'{itm}'" for itm in unloadUpcs)

        if leftNumber == 0:
            sql = f"UPDATE rfids SET state='unload' WHERE state='in' AND upc IN {strUpcs};"
            db.update(sql)
        else:
            sql = f"UPDATE rfids SET state='unload' WHERE upc=? AND state='in' AND rfid NOT IN (SELECT rfid FROM rfids WHERE upc=? AND state='in' LIMIT {leftNumber});"
            for upc in unloadUpcs:
                db.update(sql, (upc, upc))



def main():
    syncThread = ServerKioskSyncThread()
    syncThread.run()

if __name__ == '__main__':
    main()

