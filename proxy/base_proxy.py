# Source Generated with Decompyle++
# File: base_proxy.pyc (Python 2.5)

'''
##
##  Change Log:
##      2011-01-12  Modified by Kitch
##          add params remoteKioskId for method syncDataRemoteKiosk
##      2010-11-24 Modified by Tim
##          change _getRatingByUpc for international rating
##      2010-09-27 Modified by Tim
##          Add function syncDataNoSequence.
##      2010-09-20 Modified by Tim
##          Add function _getRatingByUpc for rating_system.
##      2010-05-10 Modified by Tim
##          Add function _getDiscTypeByUpcList().
##      2009-08-11 Modified by Tim
##          Add function _getBlurayUpcs().
##      2009-03-17 Modified by Tim
##          Add function _filterBluray().
##
'''
import os
import logging
import socket
from logging import handlers
import http.client
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import types
from PIL import Image
from .tools import getKioskId, getCurTime, formatEI, Log, fmtNoneStr
from .mda import Db
from .config import *

class Proxy(object):
    '''
    All proxy base class.
    '''
    
    def __init__(self, proxyName):
        self.proxyName = proxyName
        self.log = None
        self.mkcDb = None
        self.upcDb = None
        self.syncDb = None
        self.kioskId = None
        self.errorResult = None
        self.SHOW_MODE = True
        self.UPG_SHOW_MODE = True
        self.init()
        
        try:
            self.http_timeout = DEFAULT_SOCKET_TIMEOUT
        except:
            self.http_timeout = 10


    
    def __del__(self):
        del self.mkcDb
        del self.upcDb
        del self.syncDb
        del self.log

    
    def init(self):
        '''
        '''
        self.config = self._getConfig()
        self.log = self._getLog()
        self.mkcDb = Db(MKC_DB_PATH)
        self.upcDb = Db(UPC_DB_PATH)
        self.syncDb = Db(SYNC_DB_PATH)
        self.kioskId = self._getKioskId()
        self._getTestMode()

    
    def _getTestMode(self):
        
        try:
            if self._getConfigByKey('show_mode').lower() == 'no':
                self.SHOW_MODE = False
            else:
                self.SHOW_MODE = True
            if self._getConfigByKey('upg_show_mode').lower() == 'no':
                self.UPG_SHOW_MODE = False
            else:
                self.UPG_SHOW_MODE = True
        except Exception as ex:
            m = 'Error when get show_mode, upg_show_mode from config table: %s' % ex
            self.log.error(m)


    
    def _getConfigByKey(self, key):
        '''
        get config by key name
        e.g. SELECT value FROM config WHERE variable=key;
        '''
        conf = None
        sql = 'SELECT value FROM config WHERE variable=?;'
        result = self.mkcDb.query(sql, 'one', (key,))
        (conf,) = result
        conf = str(conf)
        return conf

    
    def _setConfig(self, params):
        '''
        set config by key and value
        '''
        sql = 'UPDATE config SET value=? WHERE variable=?;'
        params = [(value, key) for key, value in list(params.items())]
        self.mkcDb.updateMany(sql, params)

    
    def _formPicName(self, movieId):
        picFormat = '.jpg'
        newPicFormat = ''
        picName = str(movieId) + picFormat
        picPath = MOVIE_PICTURE_PATH + picName
        if os.path.isfile(picPath):
            
            try:
                im = Image.open(picPath, 'r')
                if im.format != 'JPEG':
                    newPicFormat = '.' + im.format.lower()
                    newPicPath = picPath + newPicFormat
                    if os.path.isfile(newPicPath) != True:
                        os.system('cp -f %s %s' % (picPath, newPicPath))
                    
                
                del im
            except:
                pass

        
        return str(movieId) + '.jpg' + newPicFormat

    
    def _formBigPicName(self, movieId):
        picFormat = '_big.jpg'
        newPicFormat = ''
        picName = str(movieId) + picFormat
        picPath = MOVIE_PICTURE_PATH + picName
        if os.path.isfile(picPath):
            im = Image.open(picPath, 'r')
            if im.format != 'JPEG':
                newPicFormat = '.' + im.format.lower()
                newPicPath = picPath + newPicFormat
                if os.path.isfile(newPicPath) != True:
                    os.system('cp -f %s %s' % (picPath, newPicPath))
                
            
            del im
        
        return str(movieId) + '_big.jpg' + newPicFormat

    
    def _getMovieInfo(self, upc):
        '''
        Get movie info from cache.
        @Params: upc(str)
        @Return: result(dict)
        '''
        sql = 'SELECT upc, title, genre, movie_release_year, movie_id, dvd_release_date, rating, starring, directors, pic_name, pic_md5, synopsis, big_pic_name, dvd_version from upc where upc=:upc;'
        upcDb = Db(UPC_DB_PATH)
        row = upcDb.query(sql, 'one', {
            'upc': upc })
        del upcDb
        result = { }
        if row:
            (upc, title, genre, movie_release_year, movie_id, dvd_release_date, rating, starring, directors, pic_name, pic_md5, synopsis, big_pic_name, dvd_version) = row
            result['upc'] = upc
            result['movie_title'] = self._getMovieTitle(title, movie_release_year)
            result['genre'] = fmtNoneStr(genre)
            result['movie_release_year'] = fmtNoneStr(movie_release_year)
            result['dvd_release_date'] = self._getDvdReleaseDate(dvd_release_date)
            result['rating'] = fmtNoneStr(rating)
            result['starring'] = fmtNoneStr(starring)
            result['directors'] = fmtNoneStr(directors)
            result['synopsis'] = fmtNoneStr(synopsis)
            result['movie_pic'] = self._formPicName(movie_id)
            result['movie_big_pic'] = self._formBigPicName(movie_id)
            result['pic_md5'] = pic_md5
            result['movie_id'] = movie_id
            result['dvd_version'] = self._getDvdVersion(dvd_version)
        else:
            msg = 'No cache for movie upc(%s)...'
            self.log.error(msg % upc)
        return result

    
    def _getRatingByUpc(self, upc):
        ''' Get the rating which needs to display.
        @param upc(str)
        @return: rating
        '''
        rating = ''
        ratingSystem = ''
        upcDb = Db(UPC_DB_PATH)
        
        try:
            ratingSystem = self._getConfigByKey('rating_system')
            sql = 'SELECT international_rating FROM upc WHERE upc=?;'
            row = upcDb.query(sql, 'one', (upc,))
            if row and row[0]:
                rating = eval(row[0]).get(ratingSystem, '')
        except:
            pass

        if not rating and str(ratingSystem).lower() in ('', 'none', 'usa'):
            
            try:
                sql = 'SELECT rating FROM upc WHERE upc=?;'
                row = upcDb.query(sql, 'one', (upc,))
                if row and row[0]:
                    rating = row[0]
            except:
                pass

        
        return rating

    
    def _getDiscTypeByUpcList(self, upcList):
        ''' Get the disc type by upc list.
        The disc type is like, DVD, BLURAY, WII, XBOX360, PS3
        @params upcList: list
        @return: {"upc": xxx}
        '''
        upcstr = "(%s)" % ",".join(["'%s'" % upc for upc in upcList])
        sql = 'SELECT upc, dvd_version FROM upc WHERE upc IN %s;' % upcstr
        upcDb = Db(UPC_DB_PATH)
        rows = upcDb.query(sql)
        result = { }
        for upc, dvd_version in rows:
            result[str(upc)] = self._getDiscType(dvd_version)
        
        return result

    
    def _getDiscType(self, dvdVersion):
        ''' Get the disc type by dvd version.
        The disc type is like, DVD, BLURAY, WII, XBOX360, PS3
        @params dvdVersion: string
        @return: discType
        '''
        discType = 'DVD'
        dv = dvdVersion.upper().replace(' ', '')
        if dv.find('WII') > -1:
            discType = 'WII'
        elif dv.find('PS3') > -1 or dv.find('PLAYSTATION3') > -1:
            discType = 'PS3'
        elif dv.find('XBOX360') > -1:
            discType = 'XBOX360'
        elif dv.find('BLURAY') > -1 and dv.find('BLU-RAY') > -1 or dv.find('BLU_RAY') > -1:
            discType = 'BLURAY'
        
        return discType

    
    def _getMovieTitle(self, title, movieReleaseYear = ''):
        ''' Form movie title.
        '''
        if movieReleaseYear and str(movieReleaseYear) != 'None':
            if len(str(movieReleaseYear)) > 4:
                movieReleaseYear = movieReleaseYear.split('-')[0]
            
            return '%s (%s)' % (title, movieReleaseYear)
        else:
            return title

    
    def _getDvdReleaseDate(self, releaseDate):
        ''' Form dvd release date.
        '''
        if releaseDate and str(releaseDate) != 'None':
            return releaseDate.split(' ')[0]
        else:
            return ''

    
    def _getDvdVersion(self, dvd_version):
        ''' Form dvd release date.
        '''
        dvd_version = fmtNoneStr(dvd_version)
        if dvd_version:
            dvd_version = '(%s)' % dvd_version
        
        return dvd_version

    
    def _filterBluray(self, upcs):
        ''' Filter the bluray upc.
        @Params: upcs(list or str)
        @Return: blurays(list)
        '''
        blurays = []
        upcstr = '()'
        if type(upcs) in (str,):
            upcstr = "('%s')" % upcs
        elif type(upcs) == int:
            upcstr = "('%s')" % upcs
        elif type(upcs) in (list, tuple):
            upcstr = '(%s)' % ','.join("'%s'" % upc for upc in upcs)
        else:
            raise ValueError('Param upcs error.')
        rows = []
        upcDb = Db(UPC_DB_PATH)
        
        try:
            sql = 'SELECT upc FROM bluray_upc WHERE upc IN %s;' % upcstr
            rows = upcDb.query(sql)
        except Exception as ex:
            self.log.error('Error when get bluray upc from table bluray_upc: %s' % ex)
            sql = "SELECT upc FROM upc WHERE upc IN %s AND dvd_version like '%%blu%%' and dvd_version like '%%ray%%';" % upcstr
            rows = upcDb.query(sql)

        del upcDb
        for upc, in rows:
            blurays.append(upc)
        
        return blurays

    
    def _getBlurayUpcs(self):
        ''' Get all bluray upcs.
        @Params: None
        @Return: blurays(tuple)
        '''
        blurays = ()
        tmp = []
        rows = []
        upcDb = Db(UPC_DB_PATH)
        
        try:
            sql = 'SELECT upc FROM bluray_upc;'
            rows = upcDb.query(sql)
        except Exception as ex:
            self.log.error('Error when _getBlurayUpcs: %s' % ex)
            sql = "SELECT upc FROM upc WHERE dvd_version like '%%blu%%' and dvd_version like '%%ray%%';"
            rows = upcDb.query(sql)

        del upcDb
        for upc, in rows:
            tmp.append(upc)
        
        if len(tmp) == 1:
            blurays = "('%s')" % tmp[0]
        else:
            blurays = tuple(tmp)
        return blurays

    
    def _getKioskId(self):
        ''' Get kiosk id.
        '''
        
        try:
            return getKioskId()
        except Exception as ex:
            self.log.error('Failed to get kiosk id:' + str(ex))
            raise 


    
    def _getConfig(self):
        '''
        Get the config from config file.
        '''
        return PROXY_DATA[self.proxyName]

    
    def _getLog(self):
        '''
        Get log object.
        '''
        log = Log(self.config['LOG_FILE_PATH'], self.proxyName)
        return log

    
    def syncData(self, funcName, params):
        '''
        Synchronize the data between cache and Remote Server.
        '''
        syncId = 0
        sql = "insert into db_sync(function_name, port_num, params, add_time) values(:funcName, :portNum, :params, DATETIME('now', 'localtime'));"
        syncId = self.syncDb.update(sql, {
            'funcName': funcName,
            'portNum': self.config['SYNC_PORT'],
            'params': str(params) })
        return syncId

    
    def syncDataRemoteKiosk(self, remoteKioskId, funcName, params):
        '''
        Synchronize the data between cache and another kiosk.
        '''
        syncId = 0
        sql = "INSERT INTO db_sync_remote_kiosk(remote_kiosk_id, function_name, port_num, params, add_time) VALUES(:remoteKioskId, :funcName, :portNum, :params, DATETIME('now', 'localtime'));"
        syncId = self.syncDb.update(sql, {
            'remoteKioskId': remoteKioskId,
            'funcName': funcName,
            'portNum': self.config['SYNC_PORT'],
            'params': str(params) })
        return syncId

    
    def syncDataNoSequence(self, funcName, params):
        '''
        Synchronize the data between cache and another kiosk.
        '''
        syncId = 0
        sql = "insert into db_sync_no_sequence(function_name, port_num, params, add_time) values(:funcName, :portNum, :params, DATETIME('now', 'localtime'));"
        syncId = self.syncDb.update(sql, {
            'funcName': funcName,
            'portNum': self.config['SYNC_PORT'],
            'params': str(params) })
        return syncId

    
    def getRemoteData(self, funcName, params, timeout = 60):
        '''
        Get data from Remote Server.
        '''
        url = '/api'
        return self._httpCall(url, {
            'function_name': funcName,
            'params': params }, timeout)

    
    def _httpCall(self, url, params, timeout = 60):
        '''Calls a remote function on a web server'''
        http = http.client.HTTPConnection(self.config['SYNC_HOST'], self.config['SYNC_PORT'])
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain',
            'Kiosk': self.kioskId }
        urlParams = urllib.parse.urlencode(params)
        result = {
            'result': 'error',
            'zdata': 'Eval error' }
        
        try:
            for i in range(2):
                http.request('POST', url, urlParams, headers)
                http.sock.settimeout(timeout)
                r = http.getresponse()
                self.log.info((r.status, r.reason))
                data = r.read()
                
                try:
                    result = eval(data)
                except Exception as ex:
                    pass

        except socket.timeout:
            result = {
                'result': 'timeout',
                'zdata': 'Connection timeout' }
        except Exception as ex:
            msg = str(ex)
            self.log.error('httpCall exception: ' + msg)
            result = {
                'result': 'error',
                'zdata': 'connection error: %s' % msg }

        return result

    
    def _http_call(self, url, params, timeout = 60):
        '''Calls a remote function on a web server'''
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain',
            'Kiosk': self.kioskId }
        urlParams = urllib.parse.urlencode(params)
        result = {
            'result': 'error',
            'zdata': 'Eval error' }
        
        try:
            socket.setdefaulttimeout(timeout)
            for i in range(2):
                request = urllib.request.Request(url, urlParams, headers)
                opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
                urllib.request.install_opener(opener)
                data = opener.open(request).read()
                
                try:
                    result = eval(data)
                except Exception as ex:
                    pass

        except socket.timeout:
            result = {
                'result': 'timeout',
                'zdata': 'Connection timeout' }
        except Exception as ex:
            msg = str(ex)
            self.log.error('httpCall exception: ' + msg)
            result = {
                'result': 'error',
                'zdata': 'connection error: %s' % msg }

        return result

    
    def logEvent(self, **params):
        '''
        params.keys ==> fields of events
        '''
        maxRowId = None
        timeNow = getCurTime()
        time_recorded = timeNow
        time_updated = timeNow
        category = params.get('category', '')
        action = params.get('action', '')
        data1 = params.get('data1', '')
        data2 = params.get('data2', '')
        data3 = params.get('data3', '')
        data4 = params.get('data4', '')
        data5 = params.get('data5', '')
        result = params.get('result', '')
        state = params.get('state', 'open')
        sql = 'INSERT INTO events(category, action, data1, data2, data3, data4, data5, result, time_recorded, time_updated, state) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
        params = (category, action, data1, data2, data3, data4, data5, result, time_recorded, time_updated, state)
        maxRowId = self.mkcDb.update(sql, params)
        maxRowId = str(maxRowId)
        return maxRowId


