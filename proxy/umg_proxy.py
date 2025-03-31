# Source Generated with Decompyle++
# File: umg_proxy.pyc (Python 2.5)

'''
##  Umg Proxy.
##
##  Change Log:
##      2009-05-06 Modified by Tim
##          Add api getChannelXmlForKiosk for MKD.
##      2009-02-16 Modified by Tim
##          Add function removeMovieTrailerByUpc and getHDTrailerForKiosk.
'''
import os
import md5
import time
import threading
import logging
from logging import handlers
from .base_proxy import Proxy
from .mda import Db, DatabaseError
from .tools import getCurTime, getLog
from .config import *
PROXY_NAME = 'UMG_PROXY'

class UmgProxy(Proxy):
    '''
    All Proxy function.
    '''
    
    def __init__(self):
        pass

    
    def __del__(self):
        super(UmgProxy, self).__del__()

    
    def on_init(self):
        super(UmgProxy, self).__init__(PROXY_NAME)

    
    def __new__(cls, *args, **kwargs):
        if '_inst' not in vars(cls):
            cls._inst = object.__new__(cls, *args, **kwargs)
            cls._inst.on_init()
        
        return cls._inst

    
    def getInstance():
        return UmgProxy()

    getInstance = staticmethod(getInstance)
    
    def getMovieTrailerByUpc(self, upc):
        '''
        Get movie trailer by upc from umg.
        @Params: upc(str)
        @Return: None
        '''
        result = ''
        
        try:
            msg = 'Begin to get movie trailer for upc(%s)...'
            self.log.info(msg % upc)
            state = 'notconnect'
            tmp = self.getRemoteData('getMovieTrailerByUpc', {
                'upc': upc })
            print(tmp)
            if tmp['result'] != 'ok':
                msg = 'Error occurs when get movie trailer from UMG Server for upc(%s): %s' % (upc, tmp['zdata'])
                self.log.error(msg)
            elif tmp['zdata']:
                result = tmp['zdata']
                state = 'wait'
            else:
                msg = 'No trailer upload for upc(%s)...'
                self.log.info(msg % upc)
            mdq = MediaDownloadQueue()
            mdq.add(upc, state)
        except Exception as ex:
            result = ''
            msg = 'Error occurs when get movie trailer for upc(%s): %s'
            self.log.error(msg % (upc, str(ex)))


    
    def removeMovieTrailerByUpc(self, upc):
        '''
        Remove movie trailer by upc from umg.
        @Params: upc(str)
        @Return: None
        '''
        result = '0'
        
        try:
            msg = 'Begin to remove movie trailer for upc(%s)...'
            self.log.info(msg % upc)
            tmp = self.getRemoteData('removeMovieTrailerByUpc', {
                'upc': upc })
            print(tmp)
            if not tmp:
                msg = 'Error when remove movie trailer from UMG server for upc(%s): %s' % (upc, tmp)
                self.log.error(msg)
            elif tmp['result'] != 'ok':
                msg = 'Error occurs when remove movie trailer from UMG Server for upc(%s): %s' % (upc, tmp['zdata'])
                self.log.error(msg)
            else:
                mdq = MediaDownloadQueue()
                mdq.removeByUpc(upc)
                del mdq
                result = '1'
        except Exception as ex:
            result = '0'
            msg = 'Error in removeMovieTrailerByUpc for upc(%s): %s'
            self.log.error(msg % (upc, ex))

        return result

    
    def getHDTrailerForKiosk(self):
        '''
        Remove movie trailer by upc from umg.
        @Params: upc(str)
        @Return: None
        '''
        result = []
        
        try:
            msg = 'Begin in getHDTrailerForKiosk...'
            self.log.info(msg)
            tmp = self.getRemoteData('getHDTrailerForKiosk', { })
            print(tmp)
            if not tmp:
                msg = 'Error when getHDTrailerForKiosk from UMG server: %s' % tmp
                self.log.error(msg)
            elif tmp['result'] != 'ok':
                msg = 'Error when getHDTrailerForKiosk from UMG Server : %s' % tmp['zdata']
                self.log.error(msg)
            else:
                result = tmp['zdata']
        except Exception as ex:
            result = []
            msg = 'Error in getHDTrailerForKiosk: %s' % ex
            self.log.error(msg)

        return result

    
    def getChannelXmlForKiosk(self, channelId, channelPwd, channelMd5 = ''):
        ''' Get channel xml for kiosk from UMG Service.
        @Params: channelId(str)
                 channelPwd(str)
                 channelMd5(str)
        @Return: channelXml
        '''
        channelXml = '0'
        
        try:
            params = { }
            params['channelId'] = channelId
            params['password'] = channelPwd
            params['md5'] = channelMd5
            tmp = self.getRemoteData('getChannelXmlForKiosk', params)
            if tmp['result'] != 'ok':
                raise Exception(tmp)
            
            channelXml = tmp['zdata']
        except Exception as ex:
            self.log.error('Error in getChannelXmlForKiosk: %s' % ex)

        return channelXml



class MediaDownloadQueue(object):
    ''' Download the trailer.
    '''
    
    def __init__(self):
        self.mediaDb = None
        self.log = None
        self.mediaDb = Db(MEDIA_DB_PATH)
        self.log = getLog('media_download_thread.log', 'MEDIA_DOWNLOAD_THREAD')

    
    def __del__(self):
        del self.mediaDb
        del self.log

    
    def add(self, upc, state):
        ''' Add to media download queue.
        @Params: upc(str)
        @Return: None
        '''
        if not self._isInQueue(upc):
            self.log.info('Add upc(%s) to media download queue.' % upc)
            sql = "insert into media(upc, state, create_time) values('%s', '%s', DATETIME('now', 'localtime'));" % (str(upc), state)
            self.mediaDb.update(sql)
        else:
            self.log.info('Upc(%s) is already in the queue.' % upc)
            sql = "update media set state='%s' where upc='%s';" % (state, str(upc))
            self.mediaDb.update(sql)

    
    def setMediaName(self, mdqId, mediaName):
        ''' Set the mediaName for trailer queue. 
        @Params: mediaName(str)
        @Return: None
        '''
        mediaName = str(mediaName)
        m = 'Set the media name to %s for media download queue %s' % (mediaName, str(mdqId))
        self.log.info(m)
        sql = "update media set media_name='%s' where id=%s;" % (mediaName, str(mdqId))
        self.mediaDb.update(sql)

    
    def setState(self, mdqId, state):
        ''' Set the state for trailer queue. 
        state: "wait" not found in UMG (default state)
               "found" found in UMG, can download(changed by UMG Service).
               "failed" download failed.
               "success" download successfully.
        '''
        state = str(state)
        m = 'Set the state to %s for media download queue %s' % (state, str(mdqId))
        self.log.info(m)
        sql = "update media set state='%s' where id=%s;" % (state, str(mdqId))
        self.mediaDb.update(sql)

    
    def remove(self, mdqId):
        ''' Remove the media from queue. '''
        m = 'Remove mdqId=%s from trailer queue.' % str(mdqId)
        self.log.info(m)
        sql = 'delete from media where id=%s;' % str(mdqId)
        self.mediaDb.update(sql)

    
    def removeByUpc(self, upc):
        ''' Remove the media from queue by upc. '''
        m = 'Remove upc=%s from trailer queue.' % upc
        self.log.info(m)
        sql = "DELETE FROM media WHERE upc='%s';" % upc
        self.mediaDb.update(sql)

    
    def getAll(self):
        ''' Get records from media download queue.
        @Params: None
        @Return: result(list(dict))[{"mdqId":xxx,
                                     "upc":xxx,
                                     "mediaName":xxx,
                                     "mediaMd5":xxx,
                                     "inTime":xxx,
                                     "state":xxx,
                                     "downloadUrl":xxx}]
        '''
        return self._get({ })

    
    def getByUpc(self, upc):
        ''' Get records from media download queue.
        @Params: upc(str)
        @Return: result(list(dict))[{"mdqId":xxx,
                                     "upc":xxx,
                                     "mediaName":xxx,
                                     "mediaMd5":xxx,
                                     "inTime":xxx,
                                     "state":xxx,
                                     "downloadUrl":xxx}]
        '''
        return self._get({
            'upc': upc })

    
    def getById(self, mdqId):
        ''' Get records from media download queue.
        @Params: mdqId(int)
        @Return: result(list(dict))[{"mdqId":xxx,
                                     "upc":xxx,
                                     "mediaName":xxx,
                                     "mediaMd5":xxx,
                                     "inTime":xxx,
                                     "state":xxx,
                                     "downloadUrl":xxx}]
        '''
        return self._get({
            'mdqId': mdqId })

    
    def getByState(self, state):
        ''' Get records from media download queue.
        @Params: state(str)
        @Return: result(list(dict))[{"mdqId":xxx,
                                     "upc":xxx,
                                     "mediaName":xxx,
                                     "mediaMd5":xxx,
                                     "inTime":xxx,
                                     "state":xxx,
                                     "downloadUrl":xxx}]
        '''
        return self._get({
            'state': state })

    
    def getByStateMediaMd5(self, mediaMd5, state = None):
        ''' Get records from media download queue.
        @Params: mediaMd5(str)
                 state(str)
        @Return: result(list(dict))[{"mdqId":xxx,
                                     "upc":xxx,
                                     "mediaName":xxx,
                                     "mediaMd5":xxx,
                                     "inTime":xxx,
                                     "state":xxx,
                                     "downloadUrl":xxx}]
        '''
        p = { }
        p['mediaMd5'] = mediaMd5
        if state is not None:
            p['state'] = state
        
        return self._get(p)

    
    def _get(self, params):
        ''' Get records from media download queue.
        @Params: params(dict): {"state":xxx, "mdqId":xxx, "upc":xxx}
        @Return: result(list(dict))[{"mdqId":xxx,
                                     "upc":xxx,
                                     "mediaName":xxx,
                                     "mediaMd5":xxx,
                                     "inTime":xxx,
                                     "state":xxx,
                                     "downloadUrl":xxx}]
        '''
        result = []
        sql = 'select id, upc, media_name, media_md5, create_time, state, download_url from media where 1=1'
        if 'state' in params:
            sql += " and state='%s'" % params.get('state', '')
        
        if 'mdqId' in params:
            sql += ' and id=%s' % str(params.get('mdqId', ''))
        
        if 'upc' in params:
            sql += " and upc='%s'" % str(params.get('upc', ''))
        
        if 'mediaMd5' in params:
            sql += " and media_md5='%s'" % str(params.get('mediaMd5', ''))
        
        sql += ';'
        rows = self.mediaDb.query(sql)
        for row in rows:
            (mdqId, upc, mediaName, mediaMd5, inTime, state, downloadUrl) = row
            tmp = { }
            tmp['mdqId'] = mdqId
            tmp['upc'] = upc
            tmp['mediaName'] = mediaName
            tmp['mediaMd5'] = mediaMd5
            tmp['inTime'] = inTime
            tmp['state'] = state
            tmp['downloadUrl'] = downloadUrl
            result.append(tmp)
        
        return result

    
    def _isInQueue(self, upc):
        ''' Check if the upc is in the queue. '''
        if self._get({
            'upc': upc }):
            return True
        else:
            return False



def testGetMovieTrailerByUpc():
    up = UmgProxy.getInstance()
    print('testGetMovieTrailerByUpc')
    upc = '025193251428'
    print('upc', upc)
    print(up.getMovieTrailerByUpc(upc))


def testMediaDownloadQueue():
    md = MediaDownloadQueue()
    md.add('779836155191', 'wait')
    md.add('025193251428', 'wait')
    md.add('025193251329', 'wait')


def testRemoveMovieTrailerByUpc():
    up = UmgProxy.getInstance()
    print('testRemoveMovieTrailerByUpc')
    upc = '025193251428'
    print('upc', upc)
    print(up.removeMovieTrailerByUpc(upc))


def testGetHDTrailerForKiosk():
    up = UmgProxy.getInstance()
    print('testGetHDTrailerForKiosk')
    print(up.getHDTrailerForKiosk())


def test():
    testGetMovieTrailerByUpc()
    testRemoveMovieTrailerByUpc()
    testGetHDTrailerForKiosk()

if __name__ == '__main__':
    test()

