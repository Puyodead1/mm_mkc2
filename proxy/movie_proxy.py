# Source Generated with Decompyle++
# File: movie_proxy.pyc (Python 2.5)

'''
    Change Log:
        2011-04-07 Modified by Tim
            change the method allowRental
        2010-11-23 Modified by Tim
            Add new function getMovieListByUpcListEspSyn.
        2010-09-20 Modified by Tim
            For #2164, change disc rating for rating_system.
        2010-05-12 Modified by Tim
            Add one attribute discType for Disc.
        2010-04-08 Modified by Tim
            For #2063, add a adulted switch for loading movies.
            Disable the remote fetching movie list.
        2009-06-15 Modified by Tim
            Add two functions canQuickLoad() and getUpcByRfidQuickLoad() for
            quick load.
        2009-06-05 Modified by Tim
            For #1708 ,Change function allowRental().
        2009-04-10 Modified by Tim
            Donot raise Exception when get movie list from remote server,
            just log it.
        2009-03-10 Modified by Tim
            For #1610, Add new function updateUpcDb() for utils update_upc.py.
        2009-03-06 Modified by Tim
            Add dvd_version for getOtherUpcList().
        2009-01-13 Created by Tim:
            New Movie proxy.
'''
import os
import sys
import md5
import time
import base64

try:
    import psyco
    psyco.full()
except:
    pass

from .base_proxy import Proxy
from .tools import getCurTime, RemoteError, getTimeChange, sqlQuote, fmtMoney, fmtNoneStr
from .config import *
from .mda import DatabaseError, Db
__version__ = '0.0.3'
PROXY_NAME = 'MOVIE_PROXY'

class MovieProxy(Proxy):
    '''
    MoveProxy class, inherit from Proxy.

    @Exception: DatabaseError(Error code=1)
                RemoteError(Error code=2)
                InternalError(Error code=3)
    '''
    
    def __init__(self):
        ''' Initialize class, constructor.
        '''
        pass

    
    def __del__(self):
        ''' Destructor.
        '''
        super(MovieProxy, self).__del__()

    
    def on_init(self):
        ''' Initialize class, constructor.
        '''
        super(MovieProxy, self).__init__(PROXY_NAME)

    
    def __new__(cls, *args, **kwargs):
        if '_inst' not in vars(cls):
            cls._inst = object.__new__(cls, *args, **kwargs)
            cls._inst.on_init()
        
        return cls._inst

    
    def getInstance():
        return MovieProxy()

    getInstance = staticmethod(getInstance)
    
    def getMovieDetailByUpc(self, disc):
        '''
        Get disc detail by upc.
        @Params: disc(Disc Object)
        @Return: None
        '''
        upc = disc.upc
        self._getTestMode()
        if upc:
            info = { }
            info = self._getMovieInfoFromCache(upc)
            if not (self.SHOW_MODE) and not info:
                info = self._getMovieInfoFromRemote(upc)
            
            if not info:
                self.log.error('Can not get movie detail for upc %s' % upc)
                raise Exception('Invalid upc %s' % upc)
            
            disc.title = info['movie_title']
            disc.picture = info['movie_pic']
            disc.genre = info['genre']
            disc.rating = Proxy._getRatingByUpc(self, upc)
            disc.releaseDate = info['dvd_release_date']
            disc.starring = info['starring']
            disc.directors = info['directors']
            disc.synopsis = info['synopsis']
            disc.version = info['dvd_version']
            disc.movieID = info['movie_id']
            disc.trailerName = self._getTrailerNameByUpc(upc)
            disc.isBluray = (upc in self._filterBluray(upc)) & 1
            disc.discType = self._getDiscType(info['dvd_version'])
        else:
            self.log.error('The upc of the disc is empty.')
            raise Exception('The upc of the disc is empty.')

    
    def getMovieList(self, key, val = ''):
        '''
        Get movie list for loading.
        @Params: key(str): "upc" | "keyword" | "genre"
                 val(str): "101101" | "dark" | "new release"
        @Return: [
                    {"movie_pic":"x.jpg", "movie_title":"x",
                     "upc":"xxx", "movie_release_year":xx},
                    {"movie_pic":"x.jpg", "movie_title":"x",
                     "upc":"xxxx", "movie_release_year":xx},
                 ]
        '''
        if key.lower() == 'upc':
            return self.getMovieListByUpc(val)
        elif key.lower() == 'keyword':
            return self.getMovieListByTitle(val)
        elif key.lower() == 'genre':
            return self.getMovieListByGenre(val)
        else:
            msg = 'Invalid key(%s) for getMovieList' % key
            self.log.error(msg)
            raise Exception(msg)

    
    def allowRental(self, disc):
        '''
        Check if the disc can be rented or purchased.
        Cross check "rental_lock" in config and dvd release date
        Check "enable_disc_out" in config.
        @Params: disc(Disc Object)
        @Return: allow(str): \'0\': can rent
                             \'1\': is coming soon
                             \'2\': in sale prevent days
        '''
        allow = '0'
        curTime = getCurTime('%Y-%m-%d')
        if self._isRentalLock():
            if disc.releaseDate and disc.releaseDate > curTime:
                allow = '1'
            
        
        if allow == '0':
            sale_prevent_days = 0
            
            try:
                sale_prevent_days = int(self._getConfigByKey('sale_prevent_days'))
            except:
                pass

            if disc.releaseDate and getTimeChange(disc.releaseDate, day = sale_prevent_days) > curTime:
                allow = '2'
            
        
        return allow

    
    def getMovieListByTitle(self, keyword):
        '''
        Get movie list by title.
        @Params: keyword(String)
        @Return: [
                    {"movie_title":"xxx (2005)", "upc":"xxx",
                     "movie_pic":"347.jpg", "movie_release_year":2005},
                 ](List)
        '''
        movieList = []
        self._getTestMode()
        if keyword:
            movieList = self._getMovieListByTitleFromCache(keyword)
        
        return movieList

    
    def getMovieListByUpc(self, upc):
        '''
        @Params: upc(String)
        @Return: [
                    {"movie_title":"xxx (2005)", "upc":"xxx",
                     "movie_pic":"347.jpg", "movie_release_year":2005},
                 ](List)
        '''
        movieList = []
        self._getTestMode()
        if upc:
            movieList = self._getMovieListByUpcFromCache(upc)
        
        return movieList

    
    def getMovieListByGenre(self, genre):
        '''
        Get movie list by genre.
        @Parmas: genre(str)
        @Return: [
                    {"movie_title":"xxx (2005)", "upc":"xxx",
                     "movie_pic":"347.jpg", "movie_release_year":2005},
                 ](List)
        '''
        if genre.lower() == 'new release':
            return self.getMovieListNewRelease()
        else:
            return []

    
    def getMovieListNewRelease(self):
        '''
        @Params: None
        @Return: [
                    {"movie_title":"xxx (2005)", "upc":"xxx",
                     "movie_pic":"347.jpg", "movie_release_year":2005},
                 ](List)
        '''
        newRelease = []
        self.log.debug('Get new release movies from cache...')
        adultedSql = ' '
        if self._isAdultedLock() == 1:
            adultedSql = 'AND is_adult_content=0 '
        
        sql = 'SELECT upc, title, pic_name, movie_release_year, big_pic_name, movie_id FROM new_release_cache WHERE 1=1 %s;' % adultedSql
        rows = []
        upcDb = Db(UPC_DB_PATH)
        
        try:
            print('from cache ....')
            rows = upcDb.query(sql)
        except Exception as ex:
            self.log.error('Error when get new release from cache table: %s' % ex)

        if not rows:
            print('from upc table ...')
            thisYear = int(getCurTime('%Y'))
            yearRange = '(%s)' % ','.join(f"'{i}'" for i in range(thisYear - 1, thisYear + 1))
            curDate = getCurTime('%Y-%m-%d')
            dayBefore15 = getTimeChange(curDate, day = -15)
            dayAfter15 = getTimeChange(curDate, day = 15)
            sql = "SELECT upc, title, pic_name, movie_release_year, big_pic_name, movie_id FROM upc WHERE title IN (SELECT title FROM upc WHERE dvd_release_date>'%s' AND dvd_release_date<'%s' AND has_pic=1 AND genre NOT IN ('Late Night', 'Documentary', 'Music', 'TV Classics', 'Special Interest', 'Anime', 'Sports', 'Exercise') AND movie_release_year IN %s) AND dvd_release_date>'%s' AND dvd_release_date<'%s' AND has_pic=1 AND movie_release_year IN %s %s GROUP BY title ORDER BY title;" % (dayBefore15, dayAfter15, yearRange, dayBefore15, dayAfter15, yearRange, adultedSql)
            rows = upcDb.query(sql)
        
        del upcDb
        for row in rows:
            (upc, title, pic_name, movie_release_year, big_pic_name, movie_id) = row
            tmp = { }
            tmp['upc'] = upc
            tmp['movie_title'] = self._getMovieTitle(title, movie_release_year)
            tmp['movie_release_year'] = fmtNoneStr(movie_release_year)
            tmp['movie_pic'] = self._formPicName(movie_id)
            newRelease.append(tmp)
        
        return newRelease

    
    def getOtherUpcList(self, upc):
        '''
        @Params: upc(str)
        @Return: [{"upc":"xxx",
                   "dvd_release_date":xxx,
                   "dvd_version":xxx}](list)
        '''
        movieList = []
        sql = 'SELECT u.upc,u.dvd_release_date,u.dvd_version FROM upc as u,(SELECT title, movie_release_year FROM upc WHERE upc=?) as t WHERE u.title=t.title AND u.movie_release_year=t.movie_release_year;'
        upcDb = Db(UPC_DB_PATH)
        rows = upcDb.query(sql, 'all', (upc,))
        del upcDb
        for upc, dvd_release_date, dvd_version in rows:
            tmp = { }
            tmp['upc'] = upc
            tmp['dvd_release_date'] = self._getDvdReleaseDate(dvd_release_date)
            tmp['dvd_version'] = 'DVD'
            if dvd_version:
                tmp['dvd_version'] = dvd_version
            
            movieList.append(tmp)
        
        return movieList

    
    def canQuickLoad(self):
        ''' Check if it can quick load.
        @Params: None
        @Return: status(str): "1": Enable quick load.
                              "0": Disenable quick load.
        '''
        status = '0'
        sql = 'SELECT COUNT(1) FROM quick_load;'
        upcDb = Db(UPC_DB_PATH)
        row = upcDb.query(sql, 'one')
        del upcDb
        if row and row[0]:
            status = '1'
        
        return status

    
    def getUpcByRfidQuickLoad(self, rfid):
        '''
        @Parmas: rfid(str)
        @Renturn: upc(str)
        '''
        upc = ''
        sql = 'SELECT upc FROM quick_load WHERE rfid=?;'
        upcDb = Db(UPC_DB_PATH)
        row = upcDb.query(sql, 'one', (rfid,))
        del upcDb
        if row:
            (upc,) = row
        
        return upc

    
    def updateUpcDb(self):
        '''
        @Params: None
        @Return: None
        '''
        
        try:
            sql = 'INSERT INTO update_info(success, realtime) VALUES(0, 1);'
            upcDb = Db(UPC_DB_PATH)
            upcDb.update(sql)
            del upcDb
        except Exception as ex:
            pass


    
    def getMovieListByUpcListEspSyn(self, upcList):
        ''' Get movie list by upc list eccept synopsis.
        @Params: upcList(list): [upc, upc]
        @Return: result(dict)
        '''
        result = []
        
        try:
            upcStr = ','.join(f"'{u}'" for u in upcList)
            sql = 'SELECT movie_id,title,genre,movie_release_year,old_movie_id, directors, starring, pic_name, big_pic_name, rating, upc, dvd_release_date,dvd_version FROM upc WHERE upc IN (%s);' % upcStr
            upcDb = Db(UPC_DB_PATH)
            rows = upcDb.query(sql)
            result = [ {
                'movie_id': r[0],
                'title': r[1],
                'movie_title': r[1],
                'genre': r[2],
                'running_time': '',
                'movie_release_year': r[3],
                'movie_release_date': r[3],
                'movie_old_id': r[4],
                'us_box_office': '0',
                'director': r[5],
                'directors': r[5],
                'starring': r[6],
                'small_pic_name': r[7],
                'movie_pic': r[7],
                'big_pic_name': r[8],
                'movie_big_pic': r[8],
                'rating': r[9],
                'upc': r[10],
                'dvd_release_date': self._getDvdReleaseDate(r[11]),
                'dvd_version': r[12],
                'international_rating': '' } for r in rows ]
        except Exception as ex:
            self.log.error('getMovieListByUpcListEspSyn: %s' % ex)
            raise 

        return result

    
    def _getMovieInfoFromCache(self, upc):
        '''
        Get movie info from cache.
        @Params: upc(str)
        @Return: result(dict)
        '''
        return Proxy._getMovieInfo(self, upc)

    
    def _getMovieInfoFromRemote(self, upc):
        '''
        Get movie info from cache.
        @Params: upc(str)
        @Return: result(dict)
        '''
        result = { }
        msg = 'Begin to get movie info by upc(%s) from movie server..' % upc
        self.log.info(msg)
        tmp = self.getRemoteData('getMovieInfoByUpc', {
            'upc': upc })
        if tmp['result'] != 'ok':
            msg = 'Error occurs when get movie info by upc(%s) from movie server: %s' % (upc, tmp['zdata'])
            self.log.error(msg)
            return result
        
        if tmp['zdata'] and len(tmp['zdata']) > 0:
            t = tmp['zdata'][0]
            title = t['title']
            movie_release_year = t['movie_release_year']
            result['upc'] = upc
            t['synopsis'] = t['synopsis'].encode('utf-8')
            t['starring'] = t['starring'].encode('utf-8')
            t['directors'] = t['directors'].encode('utf-8')
            result['movie_title'] = self._getMovieTitle(title, movie_release_year)
            result['genre'] = fmtNoneStr(t['genre'])
            result['movie_release_year'] = fmtNoneStr(movie_release_year)
            result['dvd_release_date'] = self._getDvdReleaseDate(t['dvd_release_date'])
            result['rating'] = fmtNoneStr(t['rating'])
            result['starring'] = fmtNoneStr(t['starring'])
            result['directors'] = fmtNoneStr(t['directors'])
            result['synopsis'] = fmtNoneStr(t['synopsis'])
            result['movie_pic'] = self._formPicName(t['movie_id'])
            result['movie_big_pic'] = self._formBigPicName(t['movie_id'])
            result['pic_md5'] = ''
            result['dvd_version'] = self._getDvdVersion(t['dvd_version'])
            result['movie_id'] = t['movie_id']
            result['international_rating'] = t['international_rating']
        
        return result

    
    def _getMovieListByTitleFromCache(self, keyword):
        ''' Get movie list by title from cache.
        @Params: keyword(str)
        @Return: [
                    {"movie_title":"xxx (2005)", "upc":"xxx",
                     "movie_pic":"347.jpg", "movie_release_year":2005},
                 ](List)
        '''
        print('_getMovieListByTitleFromCache start... ')
        movieList = []
        tmp = keyword
        if len(keyword) == 1 and keyword.isalnum():
            tmp = keyword + '%'
        else:
            tmp = '%' + keyword + '%'
        adultedSql = ' '
        if self._isAdultedLock() == 1:
            adultedSql = 'AND is_adult_content=0 '
        
        sql = 'SELECT upc, title, pic_name, movie_release_year, movie_id FROM upc WHERE title IN (SELECT title FROM upc WHERE title like :keyword %s ORDER BY has_pic DESC LIMIT 200) GROUP BY title, movie_release_year ORDER BY has_pic DESC,title LIMIT 200;' % adultedSql
        upcDb = Db(UPC_DB_PATH)
        rows = upcDb.query(sql, 'all', {
            'keyword': tmp })
        '\n        sql = "SELECT upc, title, pic_name, movie_release_year, movie_id "               "FROM upc_has_pic WHERE title LIKE :keyword GROUP BY title, "               "movie_release_year ORDER BY title LIMIT 200;"\n        print time.time()\n        rows = upcDb.query(sql, "all", {"keyword":tmp})\n        '
        del upcDb
        print(time.time())
        for row in rows:
            (upc, title, pic_name, movie_release_year, movie_id) = row
            tmp = { }
            tmp['upc'] = upc
            tmp['movie_title'] = self._getMovieTitle(title, movie_release_year)
            tmp['movie_release_year'] = fmtNoneStr(movie_release_year)
            tmp['movie_pic'] = self._formPicName(movie_id)
            movieList.append(tmp)
        
        if not movieList:
            msg = 'No data found when get movies by title(%s) from cache...'
            self.log.info(msg % keyword)
        
        print('_getMovieListByTitleFromCache end... ')
        return movieList

    
    def _getMovieListByTitleFromRemote(self, keyword):
        '''
        Get movie list by title from cache.
        @Params: keyword(str)
        @Return: [
                    {"movie_title":"xxx (2005)", "upc":"xxx",
                     "movie_pic":"347.jpg", "movie_release_year":2005},
                 ](List)
        '''
        movieList = []
        msg = 'Get movie list by title(%s) from remote server.'
        self.log.info(msg % keyword)
        tmp = self.getRemoteData('getMovieListByTitle', {
            'keyword': keyword })
        if tmp['result'] != 'ok':
            msg = 'Error when get movie list by title(%s) from remote server: %s' % (keyword, tmp['zdata'])
            self.log.error(msg)
            return movieList
        
        tmpMovieList = tmp['zdata']
        for tmp in tmpMovieList:
            t = { }
            t['upc'] = tmp['upc']
            t['movie_title'] = self._getMovieTitle(tmp['title'], tmp['movie_release_year'])
            
            try:
                (picMd5, picName) = self._savePicToDisk(tmp['picture'], tmp['movie_id'])
            except Exception as ex:
                picName = self._formPicName(tmp['movie_id'])

            t['movie_release_year'] = fmtNoneStr(tmp['movie_release_year'])
            t['movie_pic'] = picName
            movieList.append(t)
        
        del tmpMovieList
        return movieList

    
    def _getMovieListByUpcFromCache(self, upc):
        ''' Get movie list by upc or cid.
        @Params: upc(str)
        @Return: [
                    {"movie_title":"xxx (2005)", "upc":"xxx",
                     "movie_pic":"347.jpg", "movie_release_year":2005},
                 ](List)
        '''
        result = []
        adultedSql = ' '
        if self._isAdultedLock() == 1:
            adultedSql = 'AND is_adult_content=0 '
        
        sql = 'SELECT upc, title, pic_name, movie_release_year, movie_id FROM upc WHERE (upc=:upc OR cid=:upc) %s ORDER BY has_pic DESC LIMIT 30;' % adultedSql
        upcDb = Db(UPC_DB_PATH)
        rows = upcDb.query(sql, 'all', {
            'upc': upc })
        del upcDb
        for row in rows:
            (upc, title, pic_name, movie_release_year, movie_id) = row
            tmp = { }
            tmp['upc'] = upc
            tmp['movie_title'] = self._getMovieTitle(title, movie_release_year)
            tmp['movie_release_year'] = fmtNoneStr(movie_release_year)
            tmp['movie_pic'] = self._formPicName(movie_id)
            result.append(tmp)
        
        return result

    
    def _getMovieListByUpcFromRemote(self, upc):
        ''' Get movie list by upc or cid.
        @Params: upc(str)
        @Return: [
                    {"movie_title":"xxx (2005)", "upc":"xxx",
                     "movie_pic":"347.jpg", "movie_release_year":2005},
                 ](List)
        '''
        result = []
        msg = 'Begin to get movie list by upc(%s) from Movie Server...'
        self.log.info(msg % upc)
        tmp = self.getRemoteData('getMovieListByUpc', {
            'upc': upc })
        if tmp['result'] != 'ok':
            msg = 'Error occurs when get movie list by upc(%s) from Movie Server: %s' % (upc, tmp['zdata'])
            self.log.error(msg)
            return result
        
        tmpMovieList = tmp['zdata']
        for tmp in tmpMovieList:
            t = { }
            t['upc'] = tmp['upc']
            t['movie_title'] = self._getMovieTitle(tmp['title'], tmp['movie_release_year'])
            
            try:
                (picMd5, picName) = self._savePicToDisk(tmp['picture'], tmp['movie_id'])
            except Exception as ex:
                picName = self._formPicName(tmp['movie_id'])

            t['movie_release_year'] = fmtNoneStr(tmp['movie_release_year'])
            t['movie_pic'] = picName
            result.append(t)
        
        del tmpMovieList
        return result

    
    def _savePicToDisk(self, pic, movieId):
        ''' Save the picture to disk.
        '''
        f = None
        
        try:
            if pic:
                pic = base64.b64decode(pic)
                picMd5 = self._getFileMd5(pic)
                picName = self._formPicName(movieId)
                picPath = MOVIE_PICTURE_PATH + picName
                if not os.path.exists(picPath):
                    f = open(MOVIE_PICTURE_PATH + picName, 'w')
                    f.write(pic)
                
                return (picMd5, picName)
            else:
                raise Exception('No picture.')
        finally:
            if hasattr(f, 'close'):
                f.close()
            


    
    def _getTrailerNameByUpc(self, upc):
        '''
        Get trailer name by upc.
        @Params: upc(str)
        @Return: trailerName(str)
        '''
        self.log.info('Get trailer name for upc %s' % upc)
        trailerName = ''
        db = Db(MEDIA_DB_PATH)
        sql = 'SELECT media_name FROM media WHERE upc=?;'
        row = db.query(sql, 'one', (upc,))
        del db
        if row:
            (trailerName,) = row
        
        trailerName = fmtNoneStr(trailerName)
        if trailerName:
            trailerName = os.path.join(MEDIA_PATH, trailerName)
        else:
            trailerName = os.path.join(MEDIA_PATH, MEDIA_DEFAULT_FILE_NAME)
        return trailerName

    
    def _isRentalLock(self):
        isLock = True
        rentalLock = self._getConfigByKey('rental_lock')
        if rentalLock and rentalLock == 'no':
            isLock = False
        
        return isLock

    
    def _isAdultedLock(self):
        '''
        1. check if the upc db has column is_adult_content
        2. check if the adulted switch is off
        @Params: None
        @Return: adultedLock(int) - 1: no need adult filter
                                    0: need adult filter
        '''
        adultedLock = 0
        adult = self._getConfigByKey('receive_adult_content')
        if adult and adult == 'no':
            upcDb = None
            
            try:
                sql = 'SELECT is_adult_content FROM upc LIMIT 1;'
                upcDb = Db(UPC_DB_PATH)
                upcDb.query(sql, 'one')
                adultedLock = 1
            except:
                adultedLock = 0

            if hasattr(upcDb, 'close'):
                upcDb.close()
            
        
        return adultedLock



def test():
    import sys
    sys.path.append(MKC_PATH)
    import mobject
    HELP = {
        'getMovieList': "python movie_proxy.py getMovieList genre|upc|keyword 'new release'|[upc]|dark",
        'getMovieDetailByUpc': 'python movie_proxy.py getMovieDetailByUpc [upc]',
        'allowRental': 'python movie_proxy.py allowRental [upc]',
        'getOtherUpcList': 'python movie_proxy.py getOtherUpcList [upc]',
        '_isRentalLock': 'python movie_proxy.py _isRentalLock',
        '_getTrailerNameByUpc': 'python movie_proxy.py _getTrailerNameByUpc [upc]',
        'getUpcByRfidQuickLoad': 'python movie_proxy.py getUpcByRfidQuickLoad [rfid]',
        'updateUpcDb': 'python movie_proxy.py updateUpcDb',
        'canQuickLoad': 'python movie_proxy.py canQuickLoad',
        'getUpcByRfidQuickLoad': 'python movie_proxy.py getUpcByRfidQuickLoad [upc]',
        'getMovieListByUpcListEspSyn': 'python movie_proxy.py getMovieListByUpcListEspSyn [upc] [upc]' }
    paramsList = sys.argv
    print(paramsList)
    if len(paramsList) >= 2:
        funcName = paramsList[1]
        params = paramsList[2:]
        proxy = MovieProxy.getInstance()
        func = None
        if hasattr(proxy, funcName):
            func = getattr(proxy, funcName, None)
            if not hasattr(func, '__call__'):
                func = None
            
        
        if not func:
            print('Invalid function name %s' % funcName)
            print() 
            print('function list: \n\t', '\n\t'.join(list(HELP.keys())))
            print() 
            sys.exit()
        
        
        try:
            if funcName == 'getMovieDetailByUpc':
                '\n                python movie_proxy.py getMovieDetailByUpc 123123123123\n                '
                upc = params[0]
                disc = mobject.Disc(upc = upc)
                print('init disc: ', disc)
                print(func(disc))
                print('get disc deatil: ', disc)
                del disc
            elif funcName == 'allowRental':
                '\n                python movie_proxy.py allowRental 123123123123\n                '
                upc = params[0]
                disc = mobject.Disc(upc = upc)
                print('init disc: ', disc)
                proxy.getMovieDetailByUpc(disc)
                print('get disc detail: ', disc)
                print(func(disc))
                del disc
            elif funcName == 'getMovieListByUpcListEspSyn':
                '\n                python movie_proxy.py getMovieListByUpcListEspSyn 1,2,3\n                '
                print(func(params))
            else:
                '\n                python movie_proxy.py functionName [params, [params]...]\n                '
                print(func(*params))
        except Exception as ex:
            print('=' * 12)
            print('Exception: ', ex)
            print('=' * 12)
            print() 
            if funcName in HELP:
                print('HELP: \t', HELP.get(funcName))
            else:
                print('Invalid function: ', funcName)
                print() 
                print('function list: \n\t', '\n\t'.join(list(HELP.keys())))
                print() 
            print() 

        del func
        del proxy
    else:
        print('python movie_proxy.py functionName [params, [params]...]')
        print() 
        print('function list: \n\t', '\n\t'.join(list(HELP.keys())))
        print() 

if __name__ == '__main__':
    test()

