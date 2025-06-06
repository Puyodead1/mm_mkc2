# Source Generated with Decompyle++
# File: upc_db_updation_thread.pyc (Python 2.5)

''' Manage the updation of upc db.
##
##  Change Log:
##      2010-12-06 Modified by Tim
##          Add the limitation of bandwidth for downloading.
##      2010-11-18 Modified by Tim
##          Verify the follow INDEX after every _verifySchema.
##          CREATE INDEX idx_upc_cid ON upc(cid);
##          CREATE INDEX idx_upc_dvd_release_date ON upc(dvd_release_date);
##          CREATE INDEX idx_upc_movie_release_year ON upc(movie_release_year);
##          CREATE INDEX idx_upc_title ON upc(title);
##          CREATE INDEX idx_upc_upc ON upc(upc);
##      2010-09-20 Modified by Tim
##          correct the international_rating for all upcs
##      2010-08-19 Modified by Tim
##          Verify the schema of the downloaded upc.db and the new_upc.db of
##          the kiosk, if not matched, change the schema of the kiosk to match
##          the incoming database.
##      2010-05-13 Modified by Tim
##          Update the genre for table rfids.
##      2010-05-10 Modified by Tim
##          Add columns game_genre, ext1, ext2, ext3, ext4, ext5 for upc table.
##      2010-01-15 Modified by Tim
##          Add column is_adult_content for upc table.
##      2010-01-06 Created by Tim
##
'''
import os
import re
import hashlib
import time
import random
import datetime
import tarfile
import shutil
import threading
from .mda import Db
from .movie_proxy import MovieProxy
from .tools import getKioskId, getLog, getCurTime
from .config import *
NEW_UPC_DB_PATH = os.path.join(USER_ROOT, 'kiosk/var/db/new_upc.db')
NEW_PIC_PATH = os.path.join(USER_ROOT, 'kiosk/var/gui/newpic/')
SQL_DIVIDER = '--------------------'

class UpcDbUpdationThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self, name = 'UPC_DB_UPDATION_THREAD')
        self.init()

    
    def init(self):
        '''
        Init some params for the thread.
        @Params: None
        @Return: None
        '''
        self.kioskId = getKioskId()
        self.lastAccessTime = getCurTime('%H:%M')
        self.accessTime = getCurTime('%H:%M')
        self.UPDATE_TIME = self._getUpdateTime()
        self.log = getLog('upc_db_updation_thread.log', 'UPDATION')

    
    def run(self):
        '''
        Update the upc db for the kiosks.
        '''
        self.log = getLog('upc_db_updation_thread.log', 'UPDATION')
        self.log.info('Thread start...')
        self.log.info('Update time: %s' % self.UPDATE_TIME)
        while True:
            self.accessTime = getCurTime('%H:%M')
            if self.UPDATE_TIME <= self.UPDATE_TIME:
                pass
            elif self.UPDATE_TIME <= self.accessTime:
                if self._upToDate() == 0:
                    time.sleep(10)
                    continue
                
            
            if self._getRealtimeRequest():
                if self._updateRt() == 0:
                    time.sleep(10)
                    continue
                
            
            time.sleep(300)
            self.lastAccessTime = self.accessTime
        self.log.info('Thread end...')
        del self.log

    
    def _upToDate(self, integrate = True):
        ''' Keep the upc db up to date.
        @Params: integrate(bool): True: need integrate
                                  False: need not integrate
        @Return: state(int): 1: success
                             0: failed
        '''
        state = 0
        
        try:
            versions = self._getUpdateVersions()
            limit = self._getBandwithLimitation()
            for ver in versions:
                (s, init) = self._updateToVersion(ver, limit)
                if s == 0:
                    raise Exception('Failed to update to version %s' % ver['version'])
                
                if not init:
                    updateT = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
                    self._updateUpdateInfo({
                        'version': ver['version'],
                        'realtime': 0,
                        'realtime_id': 0,
                        'success': 1,
                        'update_time': updateT })
                
            
            if integrate and versions:
                self._integrateUpcDb()
            
            state = 1
        except Exception as ex:
            state = 0
            self.log.error('_upToDate: %s' % ex)

        return state

    
    def _updateRt(self):
        ''' Update for realtime request.
        @Params: None
        @Return: state(int): 1: success
                             0: failed
        '''
        state = 0
        
        try:
            rtReq = self._getRealtimeRequest()
            j = 0
            limit = self._getBandwithLimitation()
            while j < 10 and rtReq:
                if self._upToDate(False) == 0:
                    return state
                
                verInfo = self._getRealtimeVersions({
                    'kiosk_id': self.kioskId,
                    'realtime_id': rtReq[0]['realtime_id'] })
                if not verInfo:
                    time.sleep(10)
                    continue
                
                for req in rtReq:
                    self._updateUpdateInfo({
                        'version': verInfo['version'],
                        'realtime': req['realtime'],
                        'realtime_id': verInfo['realtime_id'],
                        'uiid': req['uiid'],
                        'success': req['success'],
                        'update_time': '' })
                
                i = 0
                params = {
                    'kiosk_id': self.kioskId,
                    'realtime_id': verInfo['realtime_id'] }
                while i < 100 and str(verInfo.get('status', 0)) == '0':
                    verInfo = self._getRealtimeVersions(params)
                    i += 1
                    time.sleep(60)
                if str(verInfo.get('status', 0)) == '0':
                    time.sleep(10)
                    continue
                
                rtReq = self._getRealtimeRequest()
                (s, init) = self._updateToVersion(verInfo, limit)
                if s == 1:
                    updateT = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
                    for req in rtReq:
                        self._updateUpdateInfo({
                            'version': verInfo['version'],
                            'realtime': req['realtime'],
                            'realtime_id': verInfo['realtime_id'],
                            'uiid': req['uiid'],
                            'success': 1,
                            'update_time': updateT })
                    
                    rtReq = []
                    break
                
            if not rtReq:
                self._integrateUpcDb()
                state = 1
        except Exception as ex:
            state = 0
            self.log.error('_updateRt: %s' % ex)

        return state

    
    def _updateToVersion(self, ver, bandwithLimit = 0):
        ''' Update the upc db to the ver.
        @Params: ver(dict): {"id": xxx,
                             "version": xxx,
                             "ver_type": xxx,
                             "req_type": xxx,
                             "db_url": xxx,
                             "db_md5": xxx,
                             "pic_url": xxx,
                             "pic_md5": xxx,
                             "notes": xxx,
                             "update_time": xxx,}
                 bandwithLimit(float): 0 no limit, otherwise limit with the
                                       bandwith which has been given
        @Return: state(int): 0/1: 0: error
                                  1: success
        '''
        state = 0
        init = False
        
        try:
            if not ver['db_url']:
                return (1, init)
            
            filePath = os.path.join(USER_ROOT, 'kiosk/tmp/')
            dbName = os.path.basename(ver['db_url'])
            status = self._download(ver['db_url'], dbName, ver['db_md5'], filePath, bandwithLimit)
            if status != 'success':
                raise Exception('download upc db failed')
            
            dbDir = self._uncompress(os.path.join(filePath, dbName), False)
            if not os.path.exists(dbDir):
                raise Exception('No upc db(%s) found' % dbDir)
            
            picDir = ''
            if ver['pic_url']:
                picName = os.path.basename(ver['pic_url'])
                status = self._download(ver['pic_url'], picName, ver['pic_md5'], filePath, bandwithLimit)
                if status != 'success':
                    raise Exception('download pic failed')
                
                picDir = self._uncompress(os.path.join(filePath, picName), True)
            
            if picDir:
                os.system('rsync -avz %s %s' % (picDir + os.path.sep, NEW_PIC_PATH))
            
            if self._isInit(dbDir):
                init = True
                shutil.copy(dbDir, NEW_UPC_DB_PATH)
            else:
                self._confirmUpcDb(dbDir)
            os.remove(os.path.join(filePath, dbName))
            os.remove(dbDir)
            if picDir:
                os.remove(os.path.join(filePath, picName))
                shutil.rmtree(picDir)
            
            state = 1
        except Exception as ex:
            state = 0
            self.log.error('_updateToVersion(%s): %s' % (ver, ex))

        return (state, init)

    
    def _confirmUpcDb(self, dbDir):
        ''' confirm the upc db '''
        db = None
        
        try:
            self._verifySchema(dbDir)
            db = Db(NEW_UPC_DB_PATH)
            tmpdb = Db(dbDir)
            schTools = SchemaTools(tmpdb.con)
            tbls = schTools.getAllTbls()
            sql = "ATTACH DATABASE '%s' AS newcoming;" % dbDir
            db.update(sql)
            for tbl in list(tbls.keys()):
                cols = schTools.getTableFields(tbls[tbl])
                pk = schTools.getTablePrimaryKey(tbls[tbl])
                if pk:
                    sql = 'UPDATE %s SET %s=(SELECT %s FROM newcoming.%s AS NEW WHERE NEW.%s=%s.%s),' % (tbl, pk, pk, tbl, pk, tbl, pk)
                    for col in cols:
                        sql += '%s=(SELECT %s FROM newcoming.%s AS NEW WHERE NEW.%s=%s.%s),' % (col, col, tbl, pk, tbl, pk)
                    
                    sql = sql.strip(',') + ' '
                    sql += 'WHERE %s.%s IN (SELECT %s FROM newcoming.%s);' % (tbl, pk, pk, tbl)
                    db.update(sql)
                
                colstr = ','.join(cols)
                sql = 'INSERT INTO %s(%s) SELECT %s FROM newcoming.%s AS NEW WHERE NEW.%s NOT IN (SELECT %s FROM %s);' % (tbl, colstr, colstr, tbl, pk, pk, tbl)
                db.update(sql)
            
            sql = 'DETACH DATABASE newcoming;'
            db.update(sql)
        finally:
            del db


    
    def _addColumn(self):
        ''' add column for upc table. '''
        db = Db(NEW_UPC_DB_PATH)
        
        try:
            sqls = []
            sql = "ALTER TABLE upc ADD COLUMN game_genre TEXT DEFAULT '';"
            sqls.append(sql)
            sql = "ALTER TABLE upc ADD COLUMN ext1 TEXT DEFAULT '';"
            sqls.append(sql)
            sql = "ALTER TABLE upc ADD COLUMN ext2 TEXT DEFAULT '';"
            sqls.append(sql)
            sql = "ALTER TABLE upc ADD COLUMN ext3 TEXT DEFAULT '';"
            sqls.append(sql)
            sql = "ALTER TABLE upc ADD COLUMN ext4 TEXT DEFAULT '';"
            sqls.append(sql)
            sql = "ALTER TABLE upc ADD COLUMN ext5 TEXT DEFAULT '';"
            sqls.append(sql)
            sql = "ALTER TABLE new_release_cache ADD COLUMN game_genre TEXT DEFAULT '';"
            sqls.append(sql)
            sql = "ALTER TABLE new_release_cache ADD COLUMN ext1 TEXT DEFAULT '';"
            sqls.append(sql)
            sql = "ALTER TABLE new_release_cache ADD COLUMN ext2 TEXT DEFAULT '';"
            sqls.append(sql)
            sql = "ALTER TABLE new_release_cache ADD COLUMN ext3 TEXT DEFAULT '';"
            sqls.append(sql)
            sql = "ALTER TABLE new_release_cache ADD COLUMN ext4 TEXT DEFAULT '';"
            sqls.append(sql)
            sql = "ALTER TABLE new_release_cache ADD COLUMN ext5 TEXT DEFAULT '';"
            sqls.append(sql)
            db.updateTrs(sqls)
        except Exception as ex:
            pass

        del db

    
    def _isInit(self, dbDir):
        ''' Check if it is init. '''
        init = False
        db = None
        
        try:
            db = Db(dbDir)
            if db.query('SELECT COUNT(id) FROM update_info;', 'one'):
                init = True
        except Exception as ex:
            self.log.warning('_isInit: %s' % ex)

        del db
        return init

    
    def _getUpdateVersions(self):
        ''' Get the versions list which need update. '''
        versions = []
        
        try:
            latest = self._getLatestVersion()
            result = self._getRemoteData('getUpcUpdateForKiosk', {
                'kiosk_id': self.kioskId,
                'version': latest })
            if result['result'] == 'ok':
                versions = result['zdata']
            else:
                self.log.error('_getUpdateVersions: %s' % result)
        except Exception as ex:
            self.log.error('_getUpdateVersions: %s' % ex)

        return versions

    
    def _getRealtimeVersions(self, params):
        ''' '''
        verInfo = { }
        
        try:
            result = self._getRemoteData('getRtUpcUpdateForKiosk', params)
            if result['result'] == 'ok':
                verInfo = result['zdata']
            else:
                self.log.error('_getRealtimeVersions: %s' % result)
        except Exception as ex:
            self.log.error('_getRealtimeVersions: %s' % ex)

        return verInfo

    
    def _updateUpdateInfo(self, info):
        '''  '''
        db = Db(NEW_UPC_DB_PATH)
        
        try:
            if info.get('uiid', None):
                sql = 'UPDATE update_info SET version=:version, realtime=:realtime, realtime_id=:realtime_id, success=:success, update_time=:update_time WHERE id=:uiid;'
            else:
                sql = 'INSERT INTO update_info(version, realtime, realtime_id,success, update_time) VALUES(:version, :realtime, :realtime_id, :success, :update_time);'
            db.update(sql, info)
        finally:
            del db


    
    def _getLatestVersion(self):
        ''' Get the local latest version. '''
        latest = ''
        db = None
        
        try:
            db = Db(NEW_UPC_DB_PATH)
            sql = 'SELECT MAX(version) FROM update_info WHERE realtime=0;'
            row = db.query(sql, 'one')
            if row:
                (latest,) = row
        except Exception as ex:
            self.log.error('_getLatestVersion: %s' % ex)

        del db
        return latest

    
    def _getRealtimeRequest(self):
        ''' Get realtime request. '''
        result = []
        
        try:
            db = Db(NEW_UPC_DB_PATH)
            sql = 'SELECT id, version, realtime, realtime_id, success FROM update_info WHERE success=0 AND realtime=1 ORDER BY id;'
            rows = db.query(sql)
            for row in rows:
                (uiid, version, realtime, realtime_id, success) = row
                tmp = { }
                tmp['uiid'] = uiid
                tmp['version'] = version
                tmp['realtime'] = realtime
                tmp['realtime_id'] = realtime_id
                tmp['success'] = success
                result.append(tmp)
        except Exception as ex:
            self.log.error('_getRealtimeRequest: %s' % ex)

        return result

    
    def _getUpdateTime(self):
        ''' Get update time.
        @Params: None
        @Return: hdTime(str)
        '''
        hdTime = '02:00'
        
        try:
            now = datetime.datetime.now()
            minTime = datetime.datetime(now.year, now.month, now.day, 1, 1, 0)
            maxTime = datetime.datetime(now.year, now.month, now.day, 4, 59, 0)
            if now < minTime or now > maxTime:
                now = minTime
            
            diff = maxTime - now
            if diff.seconds > 60:
                hd = now + datetime.timedelta(seconds = random.randint(60, diff.seconds))
            else:
                hd = now + datetime.timedelta(seconds = 60)
            hdTime = hd.strftime('%H:%M')
        except Exception as ex:
            print('Error in getUpdateTime: %s' % ex)

        return hdTime

    
    def _download(self, downloadUrl, fileName, fileMd5, filePath, bandwithLimit):
        ''' Sync one record to remote server.
        @Params: downloadUrl(str)
                 fileName(str)
                 fileMd5(str)
                 filePath(str)
                 bandwithLimit(float)
        @Return: state(str)
        '''
        state = 'failed'
        
        try:
            limit = ''
            if bandwithLimit > 0:
                limit = '--limit-rate=%sk' % bandwithLimit
            
            if not os.path.isdir(filePath):
                os.makedirs(filePath)
            
            url = downloadUrl
            flPath = os.path.join(filePath, fileName)
            logPath = os.path.join(USER_ROOT, 'kiosk/var/log/wget.log')
            cmd = 'wget %s --timeout=64 --tries=3 -c %s -O %s -o %s' % (limit, url, flPath, logPath)
            self.log.info('Download cmd: %s' % cmd)
            downloaded = False
            for i in range(5):
                rev = os.system(cmd)
                if rev != 0:
                    self.log.error('Download error cmd: %s' % cmd)
                    if os.path.exists(flPath):
                        os.remove(flPath)
                    
                    continue
                
                if not os.path.exists(flPath):
                    self.log.error('Downloaded file doesnot exist: %s' % cmd)
                    continue
                
                downloaded = True
                flMd5 = self._getFileMd5(flPath)
                if fileMd5 == flMd5:
                    state = 'success'
                    break
                else:
                    os.remove(flPath)
                    m = 'Download file md5: %s, original file md5: %s'
                    self.log.error(m % (flMd5, fileMd5))
        except Exception as ex:
            state = 'failed'
            msg = 'Error when download media (%s) to path %s: %s'
            self.log.error(msg % (fileName, filePath, ex))

        return state

    
    def _getFileMd5(self, filePath):
        ''' Get the md5 of the file.
        @Params: filePath(str)
        @Return: fileMd5(str)
        '''
        fileMd5 = ''
        
        try:
            mf = hashlib.md5()
            f = open(filePath)
            mf.update(f.read())
            f.close()
            fileMd5 = mf.hexdigest()
        except Exception as ex:
            m = 'Error when get the md5 for the file %s: %s' % (filePath, ex)
            self.log.error(m)

        return fileMd5

    
    def _getRemoteData(self, funcName, params, timeout = 60):
        ''' Get the remote data according to the proxy. '''
        proxy = MovieProxy.getInstance()
        result = proxy.getRemoteData(funcName, params, timeout)
        del proxy
        return result

    
    def _uncompress(self, filePath, pic = True):
        ''' Uncompress the files in the file list to compressed file name.
        '''
        result = ''
        fileDir = os.path.dirname(filePath)
        tf = tarfile.open(filePath, 'r:gz')
        
        try:
            for m in tf.getmembers():
                if pic:
                    if m.isdir():
                        result = os.path.join(fileDir, m.name)
                    
                else:
                    result = os.path.join(fileDir, m.name)
                tf.extract(m, fileDir)
        finally:
            tf.close()

        return result

    
    def _integrateUpcDb(self):
        ''' '''
        db = None
        
        try:
            db = Db(NEW_UPC_DB_PATH)
            schTools = SchemaTools(db.con)
            columns = schTools.getTableFields(schTools.getTableSch('upc'))
            allFields = ','.join(columns)
            del schTools
            self.log.info('Begin to form new_release_cache for new upc.')
            thisYear = datetime.datetime.now().year
            yearRange = '(%s)' % ','.join(f"'{i}'" for i in range(thisYear - 1, thisYear + 1))
            dayBefore15 = (datetime.datetime.now() + datetime.timedelta(days = -15)).strftime('%Y-%m-%d')
            dayAfter15 = (datetime.datetime.now() + datetime.timedelta(days = 15)).strftime('%Y-%m-%d')
            self.log.info('Insert the data into table new_release_cache of  new upc.')
            sql = 'DELETE FROM new_release_cache;'
            db.update(sql)
            sql = 'INSERT INTO new_release_cache(%s) SELECT %s ' % (allFields, allFields)
            sql += "FROM upc WHERE title IN (SELECT title FROM upc WHERE dvd_release_date>'%s' AND dvd_release_date<'%s' AND has_pic=1 AND genre NOT IN ('Late Night', 'Documentary', 'Music', 'TV Classics', 'Special Interest', 'Anime', 'Sports', 'Exercise') AND movie_release_year IN %s) AND dvd_release_date>'%s' AND dvd_release_date<'%s' AND has_pic=1 AND movie_release_year IN %s GROUP BY title ORDER BY title;"
            sql = sql % (dayBefore15, dayAfter15, yearRange, dayBefore15, dayAfter15, yearRange)
            db.update(sql)
            self.log.info('Form new_release_cache for new_upc.db successfully.')
            self.log.info('Begin to form bluray_upc for new_upc.db.')
            sql = "INSERT INTO bluray_upc(upc, dvd_version) SELECT upc, dvd_version FROM upc WHERE upc NOT IN (SELECT upc FROM bluray_upc) AND dvd_version LIKE '%blu%' AND dvd_version LIKE '%ray%';"
            db.update(sql)
            sql = "DELETE FROM bluray_upc WHERE upc NOT IN (SELECT upc FROM upc WHERE dvd_version LIKE '%blu_ray%');"
            db.update(sql)
            self.log.info('Correct the international rating for all movies.')
            self._correctInternationalRating()
            sql = 'REINDEX bluray_upc;'
            db.update(sql)
            self.log.info('Form bluray_upc for new_upc.db successfully.')
            
            try:
                self.log.info('Update movie id for rfids.')
                sql = 'UPDATE mkcdb.rfids SET movie_id=(SELECT movie_id FROM upc WHERE upc=mkcdb.rfids.upc), genre=(SELECT genre FROM upc WHERE upc=mkcdb.rfids.upc);'
                sqls = []
                sqls.append("ATTACH DATABASE '%s' AS mkcdb;" % os.path.join(USER_ROOT, 'kiosk/var/db/mkc.db'))
                sqls.append(sql)
                sqls.append('DETACH DATABASE mkcdb;')
                db.updateTrs(sqls)
            except Exception as ex:
                self.log.error('Failed to update movie id for rfids.')

        finally:
            del db


    
    def _correctInternationalRating(self):
        ''' Correct the international rating for all movies.
        @param None
        @return: None
        '''
        
        try:
            result = self._getRemoteData('getAllInternationalRatingForKiosk', '{}')
            if result['result'] != 'ok':
                raise Exception(result['zdata'])
            
            sql = 'UPDATE upc SET international_rating=? WHERE upc=?;'
            db = Db(NEW_UPC_DB_PATH)
            db.updateMany(sql, result['zdata'])
            del db
        except Exception as ex:
            self.log.warning('_correctInternationalRating: %s' % ex)


    
    def _verifySchema(self, incomingDbPath):
        ''' Verify the schema of the upc.db. '''
        
        try:
            schemas = []
            fromdb = Db(incomingDbPath)
            sql = "SELECT name, sql FROM sqlite_master WHERE type IN ('index', 'table', 'trigger') AND name NOT LIKE 'sqlite%';"
            db = Db(NEW_UPC_DB_PATH)
            schTools = SchemaTools(db.con)
            TRIES = 5
            for name, sch in fromdb.query(sql):
                i = 0
                while i < TRIES:
                    
                    try:
                        schTools.fortify(sch)
                        if name == 'upc':
                            sch = re.sub(re.compile('upc\\s*\\(', re.I), 'new_release_cache\n(', sch)
                            schTools.fortifyTable(sch)
                        
                    except Exception as ex:
                        self.log.error('_verifySchema: %s %s' % (name, ex))
                        if i >= TRIES - 1:
                            raise 
                        
                    except:
                        i >= TRIES - 1

            
            indexes = [
                'CREATE INDEX idx_upc_cid ON upc(cid);',
                'CREATE INDEX idx_upc_dvd_release_date ON upc(dvd_release_date);',
                'CREATE INDEX idx_upc_movie_release_year ON upc(movie_release_year);',
                'CREATE INDEX idx_upc_title ON upc(title);',
                'CREATE INDEX idx_upc_upc ON upc(upc);']
            for ind in indexes:
                
                try:
                    schTools.fortifyIndex(ind)
                except Exception as ex:
                    self.log.warning('fortifyIndex ind: %s' % ex)

            
            del db
        except Exception as ex:
            self.log.warning('_verifySchema: %s' % ex)
            raise 


    
    def _getBandwithLimitation(self):
        ''' Get the bandwith limitation from the config. '''
        limit = 0
        
        try:
            proxy = MovieProxy.getInstance()
            result = proxy._getConfigByKey('bandwidth_limit')
            del proxy
            if result:
                limit = float(result)
        except Exception as ex:
            self.log.warning('_getBandwithLimitation: %s' % ex)

        return limit



class SchemaTools(object):
    '''
    Tools that help to fortify a db with a new schema
    '''
    
    def __init__(self, con):
        self.con = con

    
    def fortify(self, schema):
        schema = schema.strip()
        
        try:
            entityType = self.getEntityType(schema).upper()
        except:
            entityType = 'invalid'

        if entityType == 'TABLE':
            return self.fortifyTable(schema)
        elif entityType == 'TRIGGER':
            return self.fortifyTrigger(schema)
        elif entityType == 'INDEX':
            return self.fortifyIndex(schema)
        else:
            return 'invalid'

    
    def fortifyTable(self, schema, tableName = ''):
        '''creates/updates a table with schema'''
        if not tableName:
            tableName = self.getEntityName(schema)
        
        row = self.con.execute("SELECT sql FROM sqlite_master WHERE type='table' and name='%s';" % (tableName,)).fetchone()
        if row:
            oldSchema = row[0].strip(';')
            newSchema = schema.strip(';')
            if oldSchema == newSchema:
                return 'original'
            else:
                oldFields = self.getTableFields(oldSchema)
                newFields = self.getTableFields(newSchema)
                commonFields = [field for field in newFields if field in oldFields]
                sql = 'ALTER TABLE %s RENAME TO temp;' % (tableName,)
                self.con.execute(sql)
                self.con.execute(schema)
                fieldsStr = ','.join(commonFields)
                sql = 'INSERT INTO %s(%s) SELECT %s FROM temp;' % (tableName, fieldsStr, fieldsStr)
                self.con.execute(sql)
                sql = 'DROP TABLE temp;'
                self.con.execute(sql)
                self.con.commit()
                return 'altered'
        else:
            self.con.execute(schema)
            self.con.commit()
            return 'new'

    
    def fortifyTrigger(self, schema):
        triggerName = self.getEntityName(schema)
        row = self.con.execute("SELECT sql FROM sqlite_master WHERE type='trigger' and name='%s';" % (triggerName,)).fetchone()
        if row:
            oldSchema = row[0].strip(';')
            newSchema = schema.strip(';')
            if oldSchema == newSchema:
                return 'original'
            else:
                self.con.execute('DROP TRIGGER %s;' % (triggerName,))
                self.con.execute(schema)
                self.con.commit()
                return 'altered'
        else:
            self.con.execute(schema)
            self.con.commit()
            return 'new'

    
    def fortifyIndex(self, schema):
        indexName = self.getEntityName(schema)
        row = self.con.execute("SELECT sql FROM sqlite_master WHERE type='index' and name='%s';" % (indexName,)).fetchone()
        if row:
            oldSchema = row[0].strip(';')
            newSchema = schema.strip(';')
            if oldSchema == newSchema:
                return 'original'
            else:
                self.con.execute('DROP INDEX %s;' % (indexName,))
                self.con.execute(schema)
                self.con.commit()
                return 'altered'
        else:
            self.con.execute(schema)
            self.con.commit()
            return 'new'

    
    def getEntityType(self, schema):
        regex = re.compile('^\\s*create\\s+((?:table)|(?:index)|(?:trigger))', re.I)
        result = regex.findall(schema)
        if len(result) > 0:
            return result[0].lower()
        else:
            return None

    
    def getEntityName(self, schema):
        regex = re.compile("^\\s*create\\s+(?:(?:table)|(?:index)|(?:trigger))\\s+[\\[\\']?(\\w+)[\\[\\']?", re.I)
        result = regex.findall(schema)
        if len(result) > 0:
            return result[0].lower()
        else:
            return None

    
    def getTableFields(self, schema):
        regex = re.compile('.*\\((.*)\\).*', re.I | re.S)
        result = regex.findall(schema)
        fields = []
        if len(result) > 0:
            for s in result[0].split(','):
                field = s.strip()
                if field:
                    fields.append(field.split()[0])
                
            
        
        return fields

    
    def getTablePrimaryKey(self, schema):
        ''' Get the primary key of the table. '''
        regex = re.compile('.*\\((.*)\\).*', re.I | re.S)
        result = regex.findall(schema)
        primaryKey = ''
        if len(result) > 0:
            for s in result[0].split(','):
                field = re.sub('\\s+', ' ', s.strip())
                if field.upper().find('PRIMARY KEY') > -1:
                    if not primaryKey:
                        primaryKey = field.split()[0]
                    else:
                        primaryKey = ''
                        break
                
            
        
        return primaryKey

    
    def getTableSch(self, tblName):
        ''' Get the table schema. '''
        sql = "SELECT sql FROM sqlite_master WHERE type='table' AND name=?;"
        return self.con.execute(sql, (tblName,)).fetchone()[0]

    
    def getAllTbls(self):
        ''' Get all table names and schema. '''
        tbls = { }
        sql = "SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite%';"
        for name, sch in self.con.execute(sql).fetchall():
            tbls[name] = sch
        
        return tbls

    
    def fortifyMany(self, sql):
        '''fortify multiple schemas'''
        schemas = sql.split(SQL_DIVIDER)
        for schema in schemas:
            if schema.strip(' \n'):
                self.fortify(schema)
            
        



def main():
    updationThread = UpcDbUpdationThread()
    updationThread.start()

if __name__ == '__main__':
    main()

