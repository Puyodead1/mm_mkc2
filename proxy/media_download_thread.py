# Source Generated with Decompyle++
# File: media_download_thread.pyc (Python 2.5)

'''
##  Manage trailer downloading and HD trailer downloading.
##
##  Change Log:
##      2010-12-06 Modified by Tim
##          Add the limitation of bandwidth for downloading.
##      2009-06-23 Modified by Tim
##          1. Remove HD trailer download, instead by mkd.
##          2. Change the wget.log to new folder "kiosk/var/log/".
##          3. Change the trailer to new folder "kiosk/var/gui/traielr/".
##      2009-02-16 Modified by Tim
##          Manage HD trailer downloading.
##
'''
import os
import sys
import md5
import threading
import time
import shutil
import random
import datetime
from . import tools
from .mda import Db
from .umg_proxy import MediaDownloadQueue, UmgProxy
from .tools import getKioskId, getLog, getCurTime, getTimeChange
from .config import *
MAX_TRIES = 5
DELETE_DELAY_MEDIA_DAY = 30
HD_TRAILER_PATH = os.path.join(USER_ROOT, 'videos/')
HD_TRAILER_TMP_PATH = os.path.join(USER_ROOT, 'kiosk/tmp/')

class MediaDownloadThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self, name = 'MEDIA_DOWNLOAD_THREAD')
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
        self.HD_TIME = self.getHDTime()

    
    def run(self):
        '''
        Sync the record from sync.db to remote server.
        # The media state: notconnect: Not connect to UMG service.
                           wait:    Not found trailer.
                           found:   Found trailer.
                           failed:  Download failed.
                           success: Download successfully.
        '''
        self.log = getLog('media_download_thread.log', 'MEDIA_DOWNLOAD_THREAD')
        self.log.info('Thread start...')
        self.log.info('Mange HD(High Definition) trailers time: %s' % self.HD_TIME)
        while True:
            
            try:
                print('lastAccessTime', self.lastAccessTime)
                print('accessTime', self.accessTime)
                self.mediaDb = Db(self._getDbPath())
                mdq = MediaDownloadQueue()
                proxy = UmgProxy.getInstance()
                self._delUnavailableUpc()
                upclist = self._getAvailableUpc()
                for upc in upclist:
                    proxy.getMovieTrailerByUpc(upc)
                
                rows = mdq.getByState('notconnect')
                for row in rows:
                    upc = row['upc']
                    proxy.getMovieTrailerByUpc(upc)
                
                del proxy
                rows = mdq.getByState('found')
                rows.extend(mdq.getByState('failed'))
                for row in rows:
                    
                    try:
                        mdqId = row['mdqId']
                        mediaMd5 = row['mediaMd5']
                        recs = mdq.getByStateMediaMd5(mediaMd5, 'success')
                        mediaName = ''
                        state = ''
                        if not recs:
                            downloadUrl = row['downloadUrl']
                            mediaName = os.path.basename(downloadUrl)
                            state = self.download(downloadUrl, mediaName, mediaMd5, MEDIA_PATH)
                        else:
                            mediaName = recs[0]['mediaName']
                            state = recs[0]['state']
                        if state != 'success':
                            mediaName = ''
                        
                        upcs = '(%s)' % str(row['upc'])
                        mdq.setMediaName(mdqId, mediaName)
                        mdq.setState(mdqId, state)
                    except IOError:
                        ex = None
                        if str(ex).lower().find('broken pipe') > -1:
                            self.log.critical('Critical error in media_download_thread: %s' % str(ex))
                            sys.exit()
                        else:
                            self.log.error('Error in media_download_thread: %s' % str(ex))
                    except Exception:
                        ex = None
                        m = 'Error when download media for %s: %s' % (str(row), str(ex))
                        self.log.error(m)

                
                del mdq
                self.log.debug('No download task.')
                self.rmMedia()
                del self.mediaDb
                time.sleep(300)
                self.lastAccessTime = self.accessTime
                self.accessTime = getCurTime('%H:%M')
            except IOError:
                ex = None
                if str(ex).lower().find('broken pipe') > -1:
                    self.log.critical('Critical error in media_download_thread: %s' % ex)
                    sys.exit()
                else:
                    self.log.error('Error in media_download_thread: %s' % str(ex))
            except:
                str(ex).lower().find('broken pipe') > -1

        self.log.info('Thread end...')
        del self.log

    
    def _delUnavailableUpc(self):
        ''' Delete all unavailable upc from media.
        '''
        
        try:
            self._attachMkcDb()
            sql = "SELECT upc FROM media WHERE upc NOT IN (SELECT DISTINCT upc FROM attached.rfids) AND state!='success';"
            rows = self.mediaDb.query(sql)
            proxy = UmgProxy.getInstance()
            for upc, in rows:
                result = proxy.removeMovieTrailerByUpc(upc)
                if str(result) == '0':
                    self.log.error('Error when _delUnavailableUpc(%s)' % upc)
                else:
                    self.log.info('Successfully delete %s in _delUnavailableUpc.' % upc)
            
            del proxy
        except Exception:
            ex = None
            self.log.error('Error when delete unavailable upc: %s' % ex)


    
    def _getAvailableUpc(self):
        ''' Get the upc list who is not in media table but in table rfids
        of mkc db.
        '''
        upcList = []
        
        try:
            self._attachMkcDb()
            sql = 'SELECT upc FROM attached.rfids WHERE upc NOT IN (SELECT DISTINCT upc FROM media);'
            rows = self.mediaDb.query(sql)
            for upc, in rows:
                upcList.append(upc)
        except Exception:
            ex = None
            self.log.error('Error when get available upc: %s' % ex)

        return upcList

    
    def rmMedia(self):
        ''' Remove media whose last access time is up to 30 days.
        '''
        if self.HD_TIME <= self.HD_TIME:
            pass
        elif self.HD_TIME <= self.accessTime:
            self.log.info('Remove the unnecessary media (The last access time is before more than 30 days ago).')
            media = self.getNeedRmMedia()
            for m in media:
                self._rmOneMedia(m)
            
            
            try:
                self.log.info('Correct all needed download media.')
                sql = "UPDATE media SET state='notconnect' WHERE state NOT IN ('success', 'found');"
                self.mediaDb.update(sql)
            except Exception:
                ex = None
                self.log.error('Error when correct all needed download media: %s' % ex)

        

    
    def manageHDTrailers(self):
        ''' Manage the HD(High definition) trailers. '''
        if self.HD_TIME <= self.HD_TIME:
            pass
        elif self.HD_TIME <= self.accessTime:
            self.log.info('Manage HD Trailers...')
            hdTraielrs = []
            
            try:
                proxy = UmgProxy.getInstance()
                hdTrailers = proxy.getHDTrailerForKiosk()
                del proxy
            except Exception:
                ex = None
                self.log.error('Error when getHDTrailerForKiosk: %s' % ex)

            if hdTrailers:
                self.log.info('HD Trailer list: %s' % hdTrailers)
                fileList = []
                for trailer in hdTrailers:
                    
                    try:
                        url = trailer['url']
                        fileMd5 = trailer['md5']
                        fileName = os.path.basename(url)
                        fileList.append(fileName)
                        needPath = os.path.join(HD_TRAILER_PATH, fileName)
                        if os.path.exists(needPath) and self._getFileMd5(needPath) == fileMd5:
                            self.log.info('HD Trailer %s exists, do NOT download.' % fileName)
                        else:
                            tmpPath = os.path.join(HD_TRAILER_TMP_PATH, fileName)
                            state = self.download(url, fileName, fileMd5, HD_TRAILER_TMP_PATH)
                            if state != 'success':
                                self.log.info('Download HD trailer %s failed.' % url)
                            else:
                                shutil.move(tmpPath, needPath)
                                self.log.info('Download HD trailer %s successfully.' % url)
                    except Exception:
                        ex = None
                        self.log.error('Error when download the HD trailer(%s): %s' % (trailer, ex))
                    

                
                allFiles = os.listdir(HD_TRAILER_PATH)
                for fileName in allFiles:
                    
                    try:
                        filePath = os.path.join(HD_TRAILER_PATH, fileName)
                        if fileName not in fileList and os.path.isfile(filePath) and '.'.join(fileName.split('.')[:-1]).isdigit():
                            self.log.info('Remove HD Trailer %s' % filePath)
                            os.remove(filePath)
                    except Exception:
                        ex = None
                        self.log.error('Error when remove HD Trailer %s: %s' % (fileName, ex))

                
            else:
                self.log.info('NOT set any HD trailers for the kiosk.')
        

    
    def getHDTime(self):
        ''' Get high definition manage time.
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
        except Exception:
            ex = None
            print('Error in getHDTime: %s' % ex)

        return hdTime

    
    def _rmOneMedia(self, mediaName):
        
        try:
            params = { }
            params['mediaName'] = mediaName
            sql = 'delete from media where media_name=:mediaName;'
            self.mediaDb.update(sql, params)
            os.remove(os.path.join(MEDIA_PATH, mediaName))
        except Exception:
            ex = None
            msg = 'Error when remove the media(%s) in _rmOneMedia: %s'
            self.log.error(msg % (mediaName, str(ex)))


    
    def download(self, downloadUrl, mediaName, mediaMd5, mediaPath):
        ''' Sync one record to remote server.
        @Params: downloadUrl(str)
                 mediaName(str)
                 mediaMd5(str)
        @Return: state(str)
                 mediaName(str)
        '''
        state = 'failed'
        
        try:
            if not os.path.isdir(mediaPath):
                os.makedirs(mediaPath)
            
            url = downloadUrl
            filePath = os.path.join(mediaPath, mediaName)
            logPath = os.path.join(USER_ROOT, 'kiosk/var/log/wget.log')
            limit = ''
            bwl = self._getBandwithLimitation()
            if bwl > 0:
                limit = '--limit-rate=%sk' % bwl
            
            cmd = 'wget %s --timeout=64 --tries=3 -c %s -O %s -o %s' % (limit, url, filePath, logPath)
            self.log.info('Download cmd: %s' % cmd)
            downloaded = False
            state = 'success'
            for i in range(5):
                rev = os.system(cmd)
                if rev != 0:
                    self.log.error('Download error cmd: %s' % cmd)
                    if os.path.exists(filePath):
                        os.remove(filePath)
                    
                    continue
                
                if not os.path.exists(filePath):
                    self.log.error('Downloaded file doesnot exist: %s' % cmd)
                    continue
                
                if os.path.getsize(filePath) <= 10240:
                    os.remove(filePath)
                    self.log.info('Download a null file, remove it.')
                    continue
                
                downloaded = True
                fileMd5 = self._getFileMd5(filePath)
                if fileMd5 == mediaMd5:
                    state = 'success'
                    break
                else:
                    os.remove(filePath)
                    m = 'Download file md5: %s, original file md5: %s'
                    self.log.error(m % (fileMd5, mediaMd5))
        except Exception:
            ex = None
            state = 'failed'
            msg = 'Error when download media (%s) to path %s: %s'
            self.log.error(msg % (mediaName, mediaPath, ex))

        return state

    
    def _getAllMedia(self):
        ''' Get all media from media dir.
        '''
        media = []
        tmp = os.listdir(MEDIA_PATH)
        for m in tmp:
            if os.path.isfile(os.path.join(MEDIA_PATH, m)):
                media.append(m)
            
        
        return media

    
    def getNeedRmMedia(self):
        ''' Get need remove media.
        '''
        media = []
        
        try:
            mediaInDir = self._getAllMedia()
            mediaInDb = self._getUnavailableMedia()
            tmp = list(set(mediaInDir).intersection(set(mediaInDb)))
            for m in tmp:
                lastATime = os.path.getatime(os.path.join(MEDIA_PATH, m))
                lastATime = time.strftime('%Y-%m-%d', time.localtime(lastATime))
                before30Days = getTimeChange(getCurTime('%Y-%m-%d'), day = -30)
                if lastATime <= before30Days:
                    media.append(m)
                
        except Exception:
            ex = None
            self.log.error('Error when get media which need remove: %s' % str(ex))

        return media

    
    def _getUnavailableMedia(self):
        ''' Get unavailable media which is also in download queue.
        '''
        media = []
        
        try:
            self._attachMkcDb()
            sql = 'SELECT DISTINCT media_name FROM media WHERE upc NOT IN (SELECT DISTINCT upc FROM attached.rfids);'
            rows = self.mediaDb.query(sql)
            for mediaName, in rows:
                media.append(mediaName)
        except Exception:
            ex = None
            self.log.error('Error when get unavailable media: %s' % str(ex))

        return media

    
    def _attachMkcDb(self):
        ''' Attach database upc db for getting need remove media.
        '''
        
        try:
            sql = "ATTACH DATABASE '%s' AS attached;" % MKC_DB_PATH
            self.mediaDb.update(sql)
        except:
            pass


    
    def _getFileMd5(self, filePath):
        ''' Get the md5 of the file.
        @Params: filePath(str)
        @Return: fileMd5(str)
        '''
        fileMd5 = ''
        
        try:
            mf = md5.new()
            f = open(filePath)
            mf.update(f.read())
            f.close()
            fileMd5 = mf.hexdigest()
        except Exception:
            ex = None
            m = 'Error when get the md5 for the file %s: %s' % (filePath, str(ex))
            self.log.error(m)

        return fileMd5

    
    def _getDbPath(self):
        ''' Get manage trailer db path.
        @Params: None
        @Return: dbPath
        '''
        dbPath = MEDIA_DB_PATH
        
        try:
            db = Db(MKC_DB_PATH)
            sql = "SELECT value FROM info WHERE variable='KioskSoft';"
            row = db.query(sql, 'one')
            if row and row[0].upper() < 'V0.4':
                dbPath = UPC_DB_PATH
        except Exception:
            ex = None
            self.log.info('Error in _getDbPath: %s' % ex)

        return dbPath

    
    def _getBandwithLimitation(self):
        ''' Get bandwith limitation.
        @Params: None
        @Return: limit
        '''
        limit = 0
        
        try:
            proxy = UmgProxy.getInstance()
            result = proxy._getConfigByKey('bandwidth_limit')
            del proxy
            if result:
                limit = float(result)
        except Exception:
            ex = None
            self.log.warning('_getBandwithLimitation: %s' % ex)

        return limit



def main():
    downloadThread = MediaDownloadThread()
    downloadThread.start()

if __name__ == '__main__':
    main()

