# Source Generated with Decompyle++
# File: credit_card.pyc (Python 2.5)

'''
##  Change Log:
##      2010-12-13 Modified by Tim
##          change the param passwd to trsPasswd
'''
import urllib.request, urllib.parse, urllib.error
import socket
import urllib.request, urllib.error, urllib.parse
from .tools import getLog

class UpgInternalError(Exception):
    pass


class Trade(object):
    ''' Trade class '''
    
    def __init__(self, machineId, upgServer, upgPort, upgBaseUrl, upgTrsMode):
        self.log = None
        self.machineId = machineId
        self.server = upgServer
        self.port = upgPort
        self.upgBaseUrl = upgBaseUrl
        self.upgTrsMode = upgTrsMode
        self.init()
        
        try:
            socket.setdefaulttimeout(300)
        except:
            pass


    
    def __del__(self):
        del self.log

    
    def init(self):
        self.log = getLog()

    
    def trade(self, acctId, trsType, cardNum, expDate, nameOnCard, amount, track2 = '', track1 = '', oid = '', ignore_bl = 0, zipcode = None, passwd = None):
        ''' '''
        params = { }
        params['acctId'] = acctId
        params['trsType'] = trsType
        params['cardNum'] = cardNum
        params['cardExpDate'] = expDate
        params['nameOnCard'] = nameOnCard
        params['amount'] = amount
        params['trsComment'] = self.machineId
        params['oid'] = oid
        params['trsMode'] = self.upgTrsMode
        params['track2'] = track2
        params['track1'] = track1
        params['ignore_bl'] = ignore_bl
        if zipcode is not None:
            params['zipcode'] = zipcode
        
        if passwd is not None:
            params['trsPasswd'] = passwd
        
        result = self._httpCall(urllib.parse.urlencode(params))
        r = result.split('|')
        if len(r) != 3:
            raise UpgInternalError('Error response from upg: %s' % result)
        
        return r

    
    def _httpCall(self, params):
        ''' Get the result from url. '''
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain' }
        data = ''
        
        try:
            url = 'https://%s' % str(self.server)
            if self.port:
                url += ':%s' % str(self.port)
            
            if not self.upgBaseUrl.startswith('/'):
                self.upgBaseUrl = '/' + self.upgBaseUrl
            
            url += self.upgBaseUrl
            print(url)
            r = urllib.request.urlopen(url, params)
            data = r.read()
            print(data)
            r.close()
        except socket.timeout as ex:
            m = 'Time out when trade for machine %s: %s' % (self.machineId, str(ex))
            data = m
            self.log.error(m)
        except Exception as ex:
            m = 'http call exception for UPG: %s' % str(ex)
            data = m
            self.log.error(m)

        return data


