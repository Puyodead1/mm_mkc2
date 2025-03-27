# Source Generated with Decompyle++
# File: upg_postauth_thread.pyc (Python 2.5)

'''
    Change Log:
        2012-08-01 Modified by Tim
            for #1978, Develop a protection task to ensure only one postauth thread is running
        2011-06-09 Modified by Tim
            for #410, add upg_oid for transactions
        2011-02-14 Modified by Tim
            form the oid for ChipNPin with merchant subscription reference and PGTR
        2010-12-08 Modified by Tim
            check the thread lock before process the transaction from postauth
            queue or declined queue
        2010-09-14 Modified by Tim
            use one config for declined transaction,
            every _ days for total _ times
        2010-07-27 Modified by Tim
            check if someone is using kiosk when _refundUnuseChipNPin,
            if someone is using, donot refund
        2010-06-07 Modified by Tim
            Add a new gateway chipNPin, and card type is 2.
        2010-05-13 Modified by Tim
            Add a cache for the prcoess for one CC in memory, one CC can only
            SALE only 3 times in one day whether success or fail.
            The cache object like {
                                    "[DATE]": {
                                                "[CC_ID]_[AMOUNT]": {
                                                        "all":1,
                                                        "sale":0,
                                                        "preauth":0,
                                                        "refund":0,
                                                        "postauth":1,
                                                                    }
                                              },
                                  }.
        2010-04-06 Modified by Tim
            For #2061,add table trs_process for the processing successful queue.
        2009-12-22 Modified by Tim
            Format the money before comparing.
        2009-08-28 Modified by Tim
            Send a receipt email after charged successfully.
        2009-04-22 Modified by Tim
            SALE for reopened transactions, instead of postauth.
        2009-04-10 Modified by Tim
            If failed in declinedq, remove it instead of changing the
            status to "closed"
        2009-03-03 Modified by Tim
            For #1598, Preauth the left amount for rental if rental and sale
            are in the same shopping cart.
        2009-02-19 Modified by Tim
            Add isLocked().
        2008-04-22 Created by Tim:
            Postauth Thread.
'''
import os
import sys
import time
import signal
import threading
import logging
from logging import handlers
import traceback
import random
import subprocess
from . import chip_n_pin
from . import clisitef
from .tools import getCurTime, RemoteError, getTimeChange, getLog, isLocked, getKioskId
from .mda import DatabaseError, Db
from .config import *
from .upg_proxy import UPGProxy, PostauthQueue, DeclinedQueue
from .upg_proxy import TrsProcessQueue
from .conn_proxy import ConnProxy
from .ums_proxy import UmsProxy
__version__ = '0.5.6'
POSTAUTH_QUEUE_LOCK_PATH = os.path.join(USER_ROOT, 'kiosk', 'tmp', 'UPGQ.LOCK')

class PostauthThread(threading.Thread):
    '''
    This thread is running all along.
    '''
    
    def __init__(self):
        self._chkPQLock()
        threading.Thread.__init__(self, name = 'POSTAUTH_THREAD')
        self._sleepPeriod = POSTAUTH_SLEEP_PERIOD
        self._process_cache = { }
        self._MAX_PROCESS_COUNT = 3
        self.kioskId = getKioskId()

    
    def init(self):
        pass

    
    def getLogger(self):
        ''' Get logger.
        @Params: None
        @Return: log(Log Handler)
        '''
        return getLog('postauth_thread.log', 'Postauth_Thread')

    
    def run(self):
        self.log = self.getLogger()
        self.log.info('Thread start....')
        while True:
            self._chkPQLock()
            curTime = getCurTime()
            self._refundUnuseChipNPin()
            self.processPendingTrs(curTime)
            self.processDeclinedTrs(curTime)
            time.sleep(self._sleepPeriod)
        del self.log

    
    def canPostauth(self):
        '''
        Check if it can postuath.
        @Params: None
        @Return: can(Boolean)
        '''
        can = True
        if str(isLocked()) == '1':
            can = False
        
        return can

    
    def processPendingTrs(self, curTime):
        
        try:
            needPendingTrs = self.getNeedPendingTrs(curTime)
            while needPendingTrs:
                if not self.canPostauth():
                    time.sleep(30)
                    continue
                
                trsQ = False
                for trs in needPendingTrs:
                    if self._chkTrsQueue(trs['trs_ids']) == 1:
                        trsQ = True
                        time.sleep(30)
                        continue
                    
                    self.log.info('Begin to process pending trs: %s' % str(trs))
                    self.processOnePendingTrs(trs)
                    time.sleep(10)
                
                needPendingTrs = []
                if not trsQ:
                    needPendingTrs = self.getNeedPendingTrs(curTime)
                
        except IOError:
            ex = None
            if str(ex).lower().find('broken pipe') > -1:
                self.log.critical('Critical error in processPendingTrs: %s' % str(ex))
            else:
                self.log.error('Error occurs when get declined trs: %s' % str(ex))
        except DatabaseError:
            ex = None
            if str(ex).find('database disk image is malformed') > -1:
                self._setPQLock(str(ex))
            
            self.log.error('Error occurs when get pending trs: %s' % str(ex))
        except Exception:
            ex = None
            self.log.error('Error occurs when process pending trs: %s' % traceback.format_exc())


    
    def processDeclinedTrs(self, curTime):
        
        try:
            declinedTrs = self.getDeclinedTrs(curTime)
            while declinedTrs:
                if not self.canPostauth():
                    time.sleep(30)
                    continue
                
                trsQ = False
                for trs in declinedTrs:
                    if self._chkTrsQueue(trs['trs_ids']) == 1:
                        trsQ = True
                        time.sleep(30)
                        continue
                    
                    self.log.info('Begin to prcoess declined trs: %s' % str(trs))
                    self.processOneDeclinedTrs(trs)
                    time.sleep(10)
                
                declinedTrs = []
                if not trsQ:
                    declinedTrs = self.getDeclinedTrs(curTime)
                
        except IOError:
            ex = None
            if str(ex).lower().find('broken pipe') > -1:
                self.log.critical('Critical error in processDeclinedTrs: %s' % str(ex))
            else:
                self.log.error('Error occurs when get declined trs: %s' % str(ex))
        except DatabaseError:
            ex = None
            if str(ex).find('database disk image is malformed') > -1:
                self._setPQLock(str(ex))
            
            self.log.error('Error occurs when get declined trs: %s' % str(ex))
        except Exception:
            ex = None
            self.log.error('Error occurs when process declined trs: %s' % traceback.format_exc())


    
    def processOnePendingTrs(self, trs):
        '''
        @Params: trs(Dict):
                    {"upg_id":upg_id,
                     "amount":0,
                     "trs_ids":[],
                     "cc_id":cc_id,
                     "acct_id":acct_id,
                     "card_type": card_type,
                     "data":[{"postauthqId": postauthqId,
                             "transaction_id": transaction_id,
                             "upg_id": upg_id,
                             "add_time": add_time,
                             "amount": amount,
                             "cc_id": cc_id,
                             "state": state,
                             "acct_id": acct_id],}}
        @Return: None
        '''
        
        try:
            upg_proxy = UPGProxy.getInstance()
            payment = upg_proxy._getConfigByKey('payment_options')
            if str(trs['card_type']) == '1':
                self.processPendingSADebit(trs)
            elif str(payment) == 'chipnpin':
                self.processPendingChipNPin(trs)
            elif str(payment) == 'sitef':
                self.processPendingSiTef(trs)
            else:
                self.processPendingCredit(trs)
            del upg_proxy
            for trs_id in trs['trs_ids']:
                self._remove_charge_cache(trs_id)
        except IOError:
            ex = None
            raise 
        except DatabaseError:
            ex = None
            if str(ex).find('database disk image is malformed') > -1:
                self._setPQLock(str(ex))
            
            msg = 'Error occurs when process pending trs(%s): %s'
            self.log.error(msg % (trs, ex))
        except RemoteError:
            ex = None
            msg = 'Error occurs when process pending trs(%s): %s'
            self.log.error(msg % (trs, ex))
        except Exception:
            ex = None
            msg = 'Error occurs when process pending trs(%s): %s'
            self.log.error(msg % (trs, traceback.format_exc()))


    
    def processPendingSiTef(self, trs):
        ''' Process the pending transaction of SiTef.
        @Params: trs(Dict):{"postauthqId":12,
                            "transaction_id":xx,
                            "upg_id":xxx,
                            "cc_id":23,
                            "shopping_cart_id":xxx,
                            "add_time":xxx,
                            "state":xxx,
                            "amount":12.21}
        @Return: None
        '''
        upgProxy = UPGProxy.getInstance()
        postauthq = PostauthQueue()
        declinedq = DeclinedQueue()
        setTrsList = postauthq.getOtherTrsIsByUpgIdV2(trs['upg_id'], trs['trs_ids'])
        if not setTrsList:
            not_charge_trs = self._get_not_charged_cache(trs['trs_ids'])
            if len(not_charge_trs) == len(trs['trs_ids']):
                (server, port, baseUrl) = upgProxy._getUpgServerFromUrl(upgProxy._getConfigByKey('upg_url'))
                SiTef = clisitef.CliSiTef({ }, self.kioskId, server, port, baseUrl)
                upgInfo = upgProxy.getUpgInfoByUpgId(trs['upg_id'])
                state = 'pending'
                ccInfo = upgProxy.getCCInfoByCcId(trs['cc_id'])
                if not ccInfo:
                    m = 'Get credit card info failed for ccId %s' % str(trs['cc_id'])
                    raise DatabaseError(m)
                
                realAmount = self._fmtCompareMoney(trs['amount'])
                chargedAmount = self._fmtCompareMoney(upgInfo['amount'])
                if realAmount > chargedAmount:
                    print('pending charge more')
                    amount = self._fmtMoney((realAmount - chargedAmount) / 100)
                    cpc = self._chkProcessCache(trs['cc_id'], amount, 'SALE')
                    if not cpc:
                        self._setProcessCache(trs['cc_id'], amount, 'SALE')
                        self.log.info('SiTef begin to SALE for upg id: %s, amount: %s' % (trs['upg_id'], amount))
                        (trsCode, trsMsg, oid) = SiTef._extracharge(upgInfo['acctId'], ccInfo['cc_number_sha1'], ccInfo['cc_expdate'], ccInfo['cc_name'], amount, '', '')
                        self.log.info('SiTef SALE result for %s: trsCode: %s, trsMsg: %s,' % (trs['upg_id'], trsCode, trsMsg))
                        if str(trsCode) == '0':
                            state = 'closed'
                        else:
                            upgProxy.updateUpgInfoByUpgId({
                                'upgId': trs['upg_id'],
                                'resultMsg': trsMsg })
                    else:
                        upgProxy.updateUpgInfoByUpgId({
                            'upgId': trs['upg_id'],
                            'resultMsg': cpc })
                elif realAmount < chargedAmount:
                    amount = self._fmtMoney((chargedAmount - realAmount) / 100)
                    cpc = self._chkProcessCache(trs['cc_id'], amount, 'refund')
                    if not cpc:
                        self._setProcessCache(trs['cc_id'], amount, 'refund')
                        self.log.info('SiTef begin to refund for upg id: %s, amount: %s' % (trs['upg_id'], amount))
                        oid = upgInfo['oid']
                        (trsCode, trsMsg) = SiTef.refund(upgInfo['acctId'], ccInfo['cc_number_sha1'], ccInfo['cc_expdate'], ccInfo['cc_name'], upgInfo['amount'], amount, upgInfo['resultCode'], oid)
                        self.log.info('SiTef refund result for %s: trsCode: %s, trsMsg:%s, oid: %s' % (trs['upg_id'], trsCode, trsMsg, oid))
                        if str(trsCode) == '0':
                            state = 'closed'
                        else:
                            upgProxy.updateUpgInfoByUpgId({
                                'upgId': trs['upg_id'],
                                'resultCode': trsCode,
                                'resultMsg': trsMsg })
                    else:
                        upgProxy.updateUpgInfoByUpgId({
                            'upgId': trs['upg_id'],
                            'resultMsg': cpc })
                elif realAmount == chargedAmount:
                    self.log.info("realamount equal chargedAmount,needn't do anything")
                    state = 'closed'
                else:
                    raise Exception('Invalid transaction type.')
            else:
                state = 'closed'
            if state == 'closed':
                for trs_id in trs['trs_ids']:
                    self._set_charge_cache(trs_id, state)
                
                self._addTrsQueue(trs['trs_ids'])
                self.setStateForTrs({
                    'state': 'closed' }, trs['trs_ids'])
                self.sendChargedReceipt(trs['cc_id'], trs['trs_ids'])
            else:
                (dayRate, totalDays) = self.getReprocessDeclinedConfig()
                p = { }
                curTime = getCurTime()
                nextTime = getTimeChange(curTime, day = dayRate)
                p['upg_id'] = trs['upg_id']
                p['cc_id'] = trs['cc_id']
                p['process_time'] = curTime
                p['next_process_time'] = nextTime
                p['process_count'] = 1
                p['state'] = 'open'
                p['acct_id'] = trs['acct_id']
                p['card_type'] = trs['card_type']
                for oneTrs in trs['data']:
                    p['transaction_id'] = oneTrs['transaction_id']
                    p['amount'] = oneTrs['amount']
                    declinedq.add(p)
                
            postauthq.removeByTrsIds(trs['trs_ids'])
        else:
            postauthq.updateAddTimeByTrsIds(getCurTime(), trs['trs_ids'])
        del upgProxy
        del postauthq
        del declinedq

    
    def processPendingCredit(self, trs):
        '''
        @Params: trs(Dict):
                    {"upg_id":upg_id,
                     "amount":0,
                     "trs_ids":[],
                     "cc_id":cc_id,
                     "acct_id":acct_id,
                     "card_type": card_type,
                     "data":[{"postauthqId": postauthqId,
                             "transaction_id": transaction_id,
                             "upg_id": upg_id,
                             "add_time": add_time,
                             "amount": amount,
                             "cc_id": cc_id,
                             "state": state,
                             "acct_id": acct_id],}}
        @Return: None
        '''
        upgProxy = UPGProxy.getInstance()
        postauthq = PostauthQueue()
        declinedq = DeclinedQueue()
        if trs['upg_id'] != '' and trs['upg_id'] != 0:
            trsIds = trs['trs_ids']
            upgInfo = upgProxy.getUpgInfoByUpgId(trs['upg_id'])
            setTrsList = postauthq.getOtherTrsIsByUpgIdV2(trs['upg_id'], trsIds)
            if self._fmtCompareMoney(trs['amount']) >= 0 and self._fmtCompareMoney(trs['amount']) <= 0 and upgInfo['trsType'].upper() == 'PREAUTH':
                self.setStateForTrs({
                    'state': 'closed',
                    'upg_id': 0,
                    'upg_oid': '' }, trsIds)
                self.sendChargedReceipt(upgInfo['ccId'], trsIds)
                self._addTrsQueue(trsIds)
            else:
                result = { }
                state = 'pending'
                not_charge_trs = self._get_not_charged_cache(trs['trs_ids'])
                if len(not_charge_trs) == len(trs['trs_ids']):
                    if self._fmtCompareMoney(trs['amount']) > self._fmtCompareMoney(upgInfo['amount']) and upgInfo['trsType'].upper() == 'PREAUTH':
                        cpc = self._chkProcessCache(trs['cc_id'], trs['amount'], 'sale')
                        
                        try:
                            result = upgProxy.sale(trs['acct_id'], trs['cc_id'], trs['amount'], '', cpc)
                            self._setProcessCache(trs['cc_id'], trs['amount'], 'sale')
                        except Exception:
                            ex = None
                            if str(ex).find('_getCCInfoByCcId') == -1 and not cpc:
                                self._setProcessCache(trs['cc_id'], trs['amount'], 'sale')
                            
                            raise 

                    elif upgInfo['trsType'].upper() == 'PREAUTH':
                        cpc = self._chkProcessCache(trs['cc_id'], trs['amount'], 'postauth')
                        
                        try:
                            result = upgProxy.postauth(trs['amount'], trs['upg_id'], cpc)
                            self._setProcessCache(trs['cc_id'], trs['amount'], 'postauth')
                        except Exception:
                            ex = None
                            if str(ex).find('_getCCInfoByCcId') == -1 and not cpc:
                                self._setProcessCache(trs['cc_id'], trs['amount'], 'postauth')
                            
                            raise 

                        if setTrsList:
                            setTrsIds = [trs['trs_id'] for trs in setTrsList]
                            
                            try:
                                preUpgId = 0
                                oid = ''
                                self.setStateForTrs({
                                    'upg_id': preUpgId,
                                    'upg_oid': oid }, setTrsIds)
                            except Exception:
                                []
                                ex = []
                                []
                                m = 'Preauth failed for %s: %s' % (setTrsList, ex)
                                self.log.error(m)
                                self.setStateForTrs({
                                    'upg_id': 0 }, setTrsIds)
                            except:
                                []

                        
                    else:
                        cpc = self._chkProcessCache(trs['cc_id'], trs['amount'], 'sale')
                        
                        try:
                            result = upgProxy.sale(trs['acct_id'], trs['cc_id'], trs['amount'], '', cpc)
                            self._setProcessCache(trs['cc_id'], trs['amount'], 'sale')
                        except Exception:
                            ex = None
                            if str(ex).find('_getCCInfoByCcId') == -1 and not cpc:
                                self._setProcessCache(trs['cc_id'], trs['amount'], 'sale')
                            
                            raise 

                    if str(result['trsCode']) == '0':
                        for trs_id in trs['trs_ids']:
                            self._set_charge_cache(trs_id, result)
                        
                    
                else:
                    self.setStateForTrs({
                        'upg_id': 0 }, not_charge_trs)
                    for trs_id in not_charge_trs:
                        if trs_id in trs['trs_ids']:
                            trs['trs_ids'].pop(trs_id)
                        
                        for dd in trs['data']:
                            if str(dd['transaction_id']) == str(trs_id):
                                trs['data'].pop(dd)
                                break
                            
                        
                        result = self._get_charge_cache(trs_id)
                    
                if str(result['trsCode']) == '0':
                    state = 'closed'
                else:
                    (dayRate, totalDays) = self.getReprocessDeclinedConfig()
                    p = { }
                    curTime = getCurTime()
                    nextTime = getTimeChange(curTime, day = dayRate)
                    p['upg_id'] = result['upgId']
                    p['cc_id'] = trs['cc_id']
                    p['process_time'] = curTime
                    p['next_process_time'] = nextTime
                    p['process_count'] = 1
                    p['state'] = 'open'
                    p['acct_id'] = trs['acct_id']
                    p['card_type'] = trs['card_type']
                    for oneTrs in trs['data']:
                        p['transaction_id'] = oneTrs['transaction_id']
                        p['amount'] = oneTrs['amount']
                        declinedq.add(p)
                    
                self.setStateForTrs({
                    'state': state,
                    'upg_id': result['upgId'],
                    'upg_oid': result['oid'] }, trsIds)
                if state == 'closed':
                    self.sendChargedReceipt(trs['cc_id'], trsIds)
                    self._addTrsQueue(trsIds)
                
        elif self._fmtCompareMoney(trs['amount']) >= 0 and self._fmtCompareMoney(trs['amount']) <= 0:
            self.setStateForTrs({
                'state': 'closed',
                'upg_id': trs['upg_id'] }, trs['trs_ids'])
            self.sendChargedReceipt(trs['cc_id'], trs['trs_ids'])
            self._addTrsQueue(trs['trs_ids'])
        else:
            not_charge_trs = self._get_not_charged_cache(trs['trs_ids'])
            if len(not_charge_trs) == len(trs['trs_ids']):
                cpc = self._chkProcessCache(trs['cc_id'], trs['amount'], 'sale')
                
                try:
                    result = upgProxy.sale(trs['acct_id'], trs['cc_id'], trs['amount'], trs['upg_id'], cpc)
                    self._setProcessCache(trs['cc_id'], trs['amount'], 'sale')
                except Exception:
                    ex = None
                    if str(ex).find('_getCCInfoByCcId') == -1 and not cpc:
                        self._setProcessCache(trs['cc_id'], trs['amount'], 'sale')
                    
                    raise 

                if str(result['trsCode']) == '0':
                    for trs_id in trs['trs_ids']:
                        self._set_charge_cache(trs_id, result)
                    
                
            else:
                self.setStateForTrs({
                    'upg_id': 0 }, not_charge_trs)
                for trs_id in not_charge_trs:
                    if trs_id in trs['trs_ids']:
                        trs['trs_ids'].pop(trs_id)
                    
                    for dd in trs['data']:
                        if str(dd['transaction_id']) == str(trs_id):
                            trs['data'].pop(dd)
                            break
                        
                    
                    result = self._get_charge_cache(trs_id)
                
            state = 'pending'
            if str(result['trsCode']) == '0':
                state = 'closed'
            else:
                (dayRate, totalDays) = self.getReprocessDeclinedConfig()
                p = { }
                curTime = getCurTime()
                nextTime = getTimeChange(curTime, day = dayRate)
                p['upg_id'] = result['upgId']
                p['cc_id'] = trs['cc_id']
                p['process_time'] = curTime
                p['next_process_time'] = nextTime
                p['process_count'] = 1
                p['state'] = 'open'
                p['acct_id'] = trs['acct_id']
                p['card_type'] = trs['card_type']
                for oneTrs in trs['data']:
                    p['transaction_id'] = oneTrs['transaction_id']
                    p['amount'] = oneTrs['amount']
                    declinedq.add(p)
                
                state = 'pending'
            self.setStateForTrs({
                'state': state,
                'upg_id': result['upgId'],
                'upg_oid': result['oid'] }, trs['trs_ids'])
            if state == 'closed':
                self.sendChargedReceipt(trs['cc_id'], trs['trs_ids'])
                self._addTrsQueue(trs['trs_ids'])
            
        postauthq.removeByTrsIds(trs['trs_ids'])
        del upgProxy
        del postauthq
        del declinedq

    
    def processPendingSADebit(self, trs):
        '''
        @Params: trs(Dict):{"postauthqId":12,
                            "transaction_id":xx,
                            "upg_id":xxx,
                            "cc_id":23,
                            "shopping_cart_id":xxx,
                            "add_time":xxx,
                            "state":xxx,
                            "amount":12.21}
        @Return: None
        '''
        upgProxy = UPGProxy.getInstance()
        postauthq = PostauthQueue()
        declinedq = DeclinedQueue()
        trsIds = trs['trs_ids']
        setTrsList = postauthq.getOtherTrsIsByUpgIdV2(trs['upg_id'], trsIds)
        if not setTrsList:
            upgInfo = upgProxy.getUpgInfoByUpgId(trs['upg_id'])
            if self._fmtCompareMoney(trs['amount']) >= self._fmtCompareMoney(upgInfo['amount']) and self._fmtCompareMoney(trs['amount']) <= self._fmtCompareMoney(upgInfo['amount']):
                self.setStateForTrs({
                    'state': 'closed' }, trs['trs_ids'])
                self.sendChargedReceipt(trs['cc_id'], trs['trs_ids'])
                self._addTrsQueue(trs['trs_ids'])
            else:
                p = { }
                curTime = getCurTime()
                p['upg_id'] = trs['upg_id']
                p['cc_id'] = trs['cc_id']
                p['process_time'] = curTime
                p['next_process_time'] = ''
                p['process_count'] = 2
                p['state'] = 'open'
                p['acct_id'] = trs['acct_id']
                p['card_type'] = trs['card_type']
                for oneTrs in trs['data']:
                    p['transaction_id'] = oneTrs['transaction_id']
                    p['amount'] = oneTrs['amount']
                    declinedq.add(p)
                
            postauthq.removeByTrsIds(trs['trs_ids'])
        else:
            newTime = getTimeChange(getCurTime(), hour = 1)
            postauthq.updateAddTimeByTrsIds(newTime, trs['trs_ids'])
        del upgProxy
        del postauthq
        del declinedq

    
    def processPendingChipNPin(self, trs):
        ''' Process the pending transaction of ChipNPin.
        @Params: trs(Dict):{"postauthqId":12,
                            "transaction_id":xx,
                            "upg_id":xxx,
                            "cc_id":23,
                            "shopping_cart_id":xxx,
                            "add_time":xxx,
                            "state":xxx,
                            "amount":12.21}
        @Return: None
        '''
        upgProxy = UPGProxy.getInstance()
        postauthq = PostauthQueue()
        declinedq = DeclinedQueue()
        chipNPin = None
        setTrsList = postauthq.getOtherTrsIsByUpgIdV2(trs['upg_id'], trs['trs_ids'])
        if not setTrsList:
            not_charge_trs = self._get_not_charged_cache(trs['trs_ids'])
            if len(not_charge_trs) == len(trs['trs_ids']):
                (server, port, baseUrl) = upgProxy._getUpgServerFromUrl(upgProxy._getConfigByKey('upg_url'))
                chipNPin = chip_n_pin.ChipNPin(self.kioskId, server, port, baseUrl)
                upgInfo = upgProxy.getUpgInfoByUpgId(trs['upg_id'])
                state = 'pending'
                ccInfo = upgProxy.getCCInfoByCcId(trs['cc_id'])
                if not ccInfo:
                    m = 'Get credit card info failed for ccId %s' % str(trs['cc_id'])
                    raise DatabaseError(m)
                
                realAmount = self._fmtCompareMoney(trs['amount'])
                chargedAmount = self._fmtCompareMoney(upgInfo['amount'])
                if realAmount > chargedAmount and upgInfo['trsType'].upper() in ('SALE', 'PREAUTH'):
                    amount = self._fmtMoney((realAmount - chargedAmount) / 100)
                    cpc = self._chkProcessCache(trs['cc_id'], amount, 'postauth')
                    if not cpc:
                        self._setProcessCache(trs['cc_id'], amount, 'postauth')
                        self.log.info('begin to postauth for upg id: %s, amount: %s' % (trs['upg_id'], amount))
                        (trsCode, trsMsg, oid) = chipNPin.postauth(upgInfo['acctId'], '%s|%s' % (ccInfo['cc_number_sha1'], ccInfo['cc_number']), ccInfo['cc_expdate'], ccInfo['cc_name'], amount, '', '', upgInfo['oid'])
                        self.log.info('postauth result for %s: trsCode: %s, trsMsg: %s, oid: %s' % (trs['upg_id'], trsCode, trsMsg, oid))
                        if str(trsCode) == '0':
                            state = 'closed'
                        else:
                            upgProxy.updateUpgInfoByUpgId({
                                'upgId': trs['upg_id'],
                                'resultMsg': trsMsg })
                    else:
                        upgProxy.updateUpgInfoByUpgId({
                            'upgId': trs['upg_id'],
                            'resultMsg': cpc })
                elif realAmount < chargedAmount and upgInfo['trsType'].upper() in ('SALE', 'PREAUTH'):
                    amount = self._fmtMoney((chargedAmount - realAmount) / 100)
                    cpc = self._chkProcessCache(trs['cc_id'], amount, 'refund')
                    if not cpc:
                        self._setProcessCache(trs['cc_id'], amount, 'refund')
                        self.log.info('begin to refund for upg id: %s, amount: %s' % (trs['upg_id'], amount))
                        pgtr = upgInfo['oid']
                        if str(upgInfo['oid']).find('--') == -1:
                            (trsRef, pgtr) = upgInfo['additional'].split('|||')
                        
                        (trsCode, trsMsg, oid) = chipNPin.refund(upgInfo['acctId'], ccInfo['cc_number_sha1'], ccInfo['cc_expdate'], ccInfo['cc_name'], amount, '', '', pgtr)
                        self.log.info('refund result for %s: trsCode: %s, trsMsg: %s, oid: %s' % (trs['upg_id'], trsCode, trsMsg, oid))
                        if str(trsCode) == '0':
                            state = 'closed'
                        else:
                            upgProxy.updateUpgInfoByUpgId({
                                'upgId': trs['upg_id'],
                                'resultMsg': trsMsg })
                    else:
                        upgProxy.updateUpgInfoByUpgId({
                            'upgId': trs['upg_id'],
                            'resultMsg': cpc })
                elif realAmount == chargedAmount and upgInfo['trsType'].upper() in ('SALE', 'PREAUTH'):
                    state = 'closed'
                else:
                    raise Exception('Invalid transaction type.')
            else:
                state = 'closed'
            if state == 'closed':
                for trs_id in trs['trs_ids']:
                    self._set_charge_cache(trs_id, state)
                
                self._addTrsQueue(trs['trs_ids'])
                self.setStateForTrs({
                    'state': 'closed' }, trs['trs_ids'])
                self.sendChargedReceipt(trs['cc_id'], trs['trs_ids'])
            else:
                (dayRate, totalDays) = self.getReprocessDeclinedConfig()
                p = { }
                curTime = getCurTime()
                nextTime = getTimeChange(curTime, day = dayRate)
                p['upg_id'] = trs['upg_id']
                p['cc_id'] = trs['cc_id']
                p['process_time'] = curTime
                p['next_process_time'] = nextTime
                p['process_count'] = 1
                p['state'] = 'open'
                p['acct_id'] = trs['acct_id']
                p['card_type'] = trs['card_type']
                for oneTrs in trs['data']:
                    p['transaction_id'] = oneTrs['transaction_id']
                    p['amount'] = oneTrs['amount']
                    declinedq.add(p)
                
            postauthq.removeByTrsIds(trs['trs_ids'])
        else:
            postauthq.updateAddTimeByTrsIds(getCurTime(), trs['trs_ids'])
        del upgProxy
        del chipNPin
        del postauthq
        del declinedq

    
    def setStateForTrs(self, params, trsIds):
        '''
        @Params: params(dict): {"state": "closed/failed/pending",
                                "upg_id": xx,
                                "upg_oid": xxx,}
                 trsIds(String): "[1, 3]"
        @Return: None
        '''
        
        try:
            if params.get('state', '') == 'pending':
                params.pop('state')
            
            if not params:
                return None
            
            connProxy = ConnProxy.getInstance()
            while True:
                
                try:
                    connProxy.updateTransactionsPostauth(trsIds, params)
                except Exception:
                    ex = None
                    if str(ex).find('database is locked') == -1:
                        raise 
                    
                    time.sleep(random.randint(1, 30))

            del connProxy
        except DatabaseError:
            ex = None
            if str(ex).startswith('setStateForTrs') or str(ex).find('database disk image is malformed') > -1:
                self._setPQLock(str(ex))
            else:
                msg = 'Error in setStateForTrs(state:%s, trsIds: %s): %s'
                raise DatabaseError(msg % (params.get('state', ''), trsIds, str(ex)))
        except:
            str(ex).find('database disk image is malformed') > -1


    
    def processOneDeclinedTrs(self, trs):
        '''
        @Params: trs(Dict):{"postauthqId":1, "upgId":12, "ccId":12,
                            "transactionIds":"(1,3,4)", "processCount":1,
                            "nextProcessTime":"2008-08-08 08:08:08",
                            "amount":12.12}
        @Return: None
        '''
        
        try:
            upg_proxy = UPGProxy.getInstance()
            payment = upg_proxy._getConfigByKey('payment_options')
            if str(trs['card_type']) == '1':
                self.processDeclinedSADebit(trs)
            
            if str(payment) == 'chipnpin':
                self.processDeclinedChipNPin(trs)
            
            if str(payment) == 'sitef':
                self.processDeclinedSiTef(trs)
            else:
                self.processDeclinedCredit(trs)
            del upg_proxy
            for trs_id in trs['trs_ids']:
                self._remove_charge_cache(trs_id)
        except IOError:
            ex = None
            raise 
        except DatabaseError:
            ex = None
            if str(ex).find('database disk image is malformed') > -1:
                self._setPQLock(str(ex))
            
            msg = 'Error occurs when postauth for declined trs(%s): %s'
            self.log.error(msg % (str(trs), str(ex)))
        except RemoteError:
            ex = None
            msg = 'Error occurs when postauth for declined trs(%s): %s'
            self.log.error(msg % (str(trs), str(ex)))
        except Exception:
            ex = None
            msg = 'Error occurs when process for declined trs(%s): %s'
            self.log.error(msg % (str(trs), str(ex)))


    
    def processDeclinedSiTef(self, trs):
        ''' Process one declined sitef.
        '''
        declinedq = DeclinedQueue()
        postauthq = PostauthQueue()
        upgProxy = UPGProxy.getInstance()
        setTrsList = postauthq.getOtherTrsIsByUpgIdV2(trs['upg_id'], trs['trs_ids'])
        if not setTrsList:
            not_charge_trs = self._get_not_charged_cache(trs['trs_ids'])
            if len(not_charge_trs) == len(trs['trs_ids']):
                (server, port, baseUrl) = upgProxy._getUpgServerFromUrl(upgProxy._getConfigByKey('upg_url'))
                SiTef = clisitef.CliSiTef({ }, self.kioskId, server, port, baseUrl)
                upgInfo = upgProxy.getUpgInfoByUpgId(trs['upg_id'])
                ccInfo = upgProxy.getCCInfoByCcId(trs['cc_id'])
                if not ccInfo:
                    m = 'Get credit card info failed for ccId %s' % str(trs['cc_id'])
                    raise DatabaseError(m)
                
                state = 'pending'
                realAmount = self._fmtCompareMoney(trs['amount'])
                chargedAmount = self._fmtCompareMoney(upgInfo['amount'])
                if realAmount > chargedAmount:
                    amount = self._fmtMoney((realAmount - chargedAmount) / 100)
                    cpc = self._chkProcessCache(trs['cc_id'], amount, 'SALE')
                    if not cpc:
                        self._setProcessCache(trs['cc_id'], amount, 'SALE')
                        self.log.info('decline SiTef begin to SALE for upg id: %s, amount: %s' % (trs['upg_id'], amount))
                        (trsCode, trsMsg, oid) = SiTef._extracharge(upgInfo['acctId'], ccInfo['cc_number_sha1'], ccInfo['cc_expdate'], ccInfo['cc_name'], amount, '', '')
                        self.log.info('decline SiTef SALE result for %s: trsCode: %s, trsMsg: %s,' % (trs['upg_id'], trsCode, trsMsg))
                        if str(trsCode) == '0':
                            state = 'closed'
                        else:
                            upgProxy.updateUpgInfoByUpgId({
                                'upgId': trs['upg_id'],
                                'resultMsg': trsMsg })
                    else:
                        upgProxy.updateUpgInfoByUpgId({
                            'upgId': trs['upg_id'],
                            'resultMsg': cpc })
                elif realAmount < chargedAmount:
                    amount = self._fmtMoney((chargedAmount - realAmount) / 100)
                    cpc = self._chkProcessCache(trs['cc_id'], amount, 'refund')
                    if not cpc:
                        self._setProcessCache(trs['cc_id'], amount, 'refund')
                        self.log.info('Decline SiTef begin to refund for upg id: %s, amount: %s' % (trs['upg_id'], amount))
                        oid = upgInfo['oid']
                        (trsCode, trsMsg) = SiTef.refund(upgInfo['acctId'], ccInfo['cc_number_sha1'], ccInfo['cc_expdate'], ccInfo['cc_name'], upgInfo['amount'], amount, upgInfo['resultCode'], oid)
                        self.log.info('Decline SiTef refund result for %s: trsCode: %s, trsMsg: %s, oid: %s' % (trs['upg_id'], trsCode, trsMsg, oid))
                        if str(trsCode) == '0':
                            state = 'closed'
                        else:
                            upgProxy.updateUpgInfoByUpgId({
                                'upgId': trs['upg_id'],
                                'resultCode': trsCode,
                                'resultMsg': trsMsg })
                    else:
                        upgProxy.updateUpgInfoByUpgId({
                            'upgId': trs['upg_id'],
                            'resultMsg': cpc })
                elif realAmount == chargedAmount:
                    state = 'closed'
                else:
                    raise Exception('Invalid transaction type.')
            else:
                state = 'closed'
            if str(state) == 'closed':
                for trs_id in trs['trs_ids']:
                    self._set_charge_cache(trs_id, state)
                
                declinedq.removeByTrsIds(trs['trs_ids'])
                state = 'closed'
                self._addTrsQueue(trs['trs_ids'])
                self.setStateForTrs({
                    'state': state }, trs['trs_ids'])
                self.sendChargedReceipt(trs['cc_id'], trs['trs_ids'])
            else:
                (dayRate, totalDays) = self.getReprocessDeclinedConfig()
                processTime = getCurTime()
                nextProcessTime = getTimeChange(processTime, day = dayRate)
                if trs['process_count'] >= totalDays - 1:
                    state = 'failed'
                    self.setStateForTrs({
                        'state': state,
                        'upg_id': trs['upg_id'] }, trs['trs_ids'])
                    declinedq.removeByTrsIds(trs['trs_ids'])
                else:
                    p = { }
                    p['state'] = 'open'
                    p['process_time'] = processTime
                    p['next_process_time'] = nextProcessTime
                    p['process_count'] = trs['process_count'] + 1
                    p['acct_id'] = trs['acct_id']
                    for t in trs['data']:
                        p['amount'] = t['amount']
                        p['declinedqId'] = t['declinedqId']
                        declinedq.update(p)
                    
        
        del upgProxy
        del declinedq
        del postauthq

    
    def processDeclinedSADebit(self, trs):
        ''' Process one declined debit card of SA. '''
        (dayRate, totalDays) = self.getReprocessDeclinedConfig()
        declinedq = DeclinedQueue()
        processTime = getCurTime()
        nextProcessTime = getTimeChange(processTime, day = dayRate)
        p = { }
        p['state'] = 'open'
        p['process_time'] = processTime
        p['next_process_time'] = nextProcessTime
        p['process_count'] = trs['process_count']
        p['acct_id'] = trs['acct_id']
        for t in trs['data']:
            p['amount'] = t['amount']
            p['declinedqId'] = t['declinedqId']
            declinedq.update(p)
        
        del declinedq

    
    def processDeclinedCredit(self, trs):
        ''' Process one declined credit card.
        '''
        declinedq = DeclinedQueue()
        upgProxy = UPGProxy.getInstance()
        not_charge_trs = self._get_not_charged_cache(trs['trs_ids'])
        if len(not_charge_trs) == len(trs['trs_ids']):
            cpc = self._chkProcessCache(trs['cc_id'], trs['amount'], 'sale')
            
            try:
                result = upgProxy.sale(trs['acct_id'], trs['cc_id'], trs['amount'], trs['upg_id'], cpc)
                self._setProcessCache(trs['cc_id'], trs['amount'], 'sale')
            except Exception:
                ex = None
                if str(ex).find('_getCCInfoByCcId') == -1 and not cpc:
                    self._setProcessCache(trs['cc_id'], trs['amount'], 'sale')
                
                raise 

            if str(result['trsCode']) == '0':
                for trs_id in trs['trs_ids']:
                    self._set_charge_cache(trs_id, result)
                
            
        else:
            self.setStateForTrs({
                'upg_id': 0 }, not_charge_trs)
            for trs_id in not_charge_trs:
                if trs_id in trs['trs_ids']:
                    trs['trs_ids'].pop(trs_id)
                
                for dd in trs['data']:
                    if str(dd['transaction_id']) == str(trs_id):
                        trs['data'].pop(dd)
                        break
                    
                
                result = self._get_charge_cache(trs_id)
            
        if str(result['trsCode']) == '0':
            declinedq.removeByTrsIds(trs['trs_ids'])
            state = 'closed'
            self.setStateForTrs({
                'state': state,
                'upg_id': result['upgId'],
                'upg_oid': result['oid'] }, trs['trs_ids'])
            self.sendChargedReceipt(trs['cc_id'], trs['trs_ids'])
            self._addTrsQueue(trs['trs_ids'])
        else:
            (dayRate, totalDays) = self.getReprocessDeclinedConfig()
            processTime = getCurTime()
            nextProcessTime = getTimeChange(processTime, day = dayRate)
            if trs['process_count'] >= totalDays - 1:
                state = 'failed'
                self.setStateForTrs({
                    'state': state,
                    'upg_id': result['upgId'],
                    'upg_oid': result['oid'] }, trs['trs_ids'])
                declinedq.removeByTrsIds(trs['trs_ids'])
                '\n                p = {}\n                p["state"] = "closed"\n                p["process_time"] = processTime\n                p["next_process_time"] = nextProcessTime\n                p["process_count"] = 7\n                p["acct_id"] = trs["acct_id"]\n                for t in trs["data"]:\n                    p["amount"] = t["amount"]\n                    p["declinedqId"] = t["declinedqId"]\n                    declinedq.update(p)\n                '
            else:
                p = { }
                p['state'] = 'open'
                p['process_time'] = processTime
                p['next_process_time'] = nextProcessTime
                p['process_count'] = trs['process_count'] + 1
                p['acct_id'] = trs['acct_id']
                for t in trs['data']:
                    p['amount'] = t['amount']
                    p['declinedqId'] = t['declinedqId']
                    declinedq.update(p)
                
                self.setStateForTrs({
                    'upg_id': result['upgId'],
                    'upg_oid': result['oid'] }, trs['trs_ids'])
        del upgProxy
        del declinedq

    
    def processDeclinedChipNPin(self, trs):
        ''' Process one declined chip n pin.
        '''
        declinedq = DeclinedQueue()
        postauthq = PostauthQueue()
        upgProxy = UPGProxy.getInstance()
        setTrsList = postauthq.getOtherTrsIsByUpgIdV2(trs['upg_id'], trs['trs_ids'])
        if not setTrsList:
            not_charge_trs = self._get_not_charged_cache(trs['trs_ids'])
            if len(not_charge_trs) == len(trs['trs_ids']):
                (server, port, baseUrl) = upgProxy._getUpgServerFromUrl(upgProxy._getConfigByKey('upg_url'))
                chipNPin = chip_n_pin.ChipNPin(self.kioskId, server, port, baseUrl)
                upgInfo = upgProxy.getUpgInfoByUpgId(trs['upg_id'])
                ccInfo = upgProxy.getCCInfoByCcId(trs['cc_id'])
                if not ccInfo:
                    m = 'Get credit card info failed for ccId %s' % str(trs['cc_id'])
                    raise DatabaseError(m)
                
                state = 'pending'
                realAmount = self._fmtCompareMoney(trs['amount'])
                chargedAmount = self._fmtCompareMoney(upgInfo['amount'])
                if realAmount > chargedAmount and upgInfo['trsType'].upper() in ('SALE', 'PREAUTH'):
                    amount = self._fmtMoney((realAmount - chargedAmount) / 100)
                    cpc = self._chkProcessCache(trs['cc_id'], amount, 'postauth')
                    if not cpc:
                        self._setProcessCache(trs['cc_id'], amount, 'postauth')
                        self.log.info('begin to postauth for upg id: %s, amount: %s' % (trs['upg_id'], amount))
                        (trsCode, trsMsg, oid) = chipNPin.postauth(upgInfo['acctId'], '%s|%s' % (ccInfo['cc_number_sha1'], ccInfo['cc_number']), ccInfo['cc_expdate'], ccInfo['cc_name'], amount, '', '', upgInfo['oid'])
                        self.log.info('postauth result for %s: trsCode: %s, trsMsg: %s, oid: %s' % (trs['upg_id'], trsCode, trsMsg, oid))
                        if str(trsCode) == '0':
                            state = 'closed'
                        else:
                            upgProxy.updateUpgInfoByUpgId({
                                'upgId': trs['upg_id'],
                                'resultMsg': trsMsg })
                    else:
                        upgProxy.updateUpgInfoByUpgId({
                            'upgId': trs['upg_id'],
                            'resultMsg': cpc })
                elif realAmount < chargedAmount and upgInfo['trsType'].upper() in ('SALE', 'PREAUTH'):
                    amount = self._fmtMoney((chargedAmount - realAmount) / 100)
                    cpc = self._chkProcessCache(trs['cc_id'], amount, 'refund')
                    if not cpc:
                        self._setProcessCache(trs['cc_id'], amount, 'refund')
                        self.log.info('begin to refund for upg id: %s, amount: %s' % (trs['upg_id'], amount))
                        pgtr = upgInfo['oid']
                        if upgInfo['oid'].find('--') == -1:
                            (sub_ref, pgtr) = upgInfo['additional'].split('|||')
                        
                        (trsCode, trsMsg, oid) = chipNPin.refund(upgInfo['acctId'], ccInfo['cc_number_sha1'], ccInfo['cc_expdate'], ccInfo['cc_name'], amount, '', '', pgtr)
                        self.log.info('refund result for %s: trsCode: %s, trsMsg: %s, oid: %s' % (trs['upg_id'], trsCode, trsMsg, oid))
                        if str(trsCode) == '0':
                            state = 'closed'
                        else:
                            upgProxy.updateUpgInfoByUpgId({
                                'upgId': trs['upg_id'],
                                'resultMsg': trsMsg })
                    else:
                        upgProxy.updateUpgInfoByUpgId({
                            'upgId': trs['upg_id'],
                            'resultMsg': cpc })
                elif realAmount == chargedAmount and upgInfo['trsType'].upper() in ('SALE', 'PREAUTH'):
                    state = 'closed'
                else:
                    raise Exception('Invalid transaction type.')
            else:
                state = 'closed'
            if str(state) == 'closed':
                for trs_id in trs['trs_ids']:
                    self._set_charge_cache(trs_id, state)
                
                declinedq.removeByTrsIds(trs['trs_ids'])
                state = 'closed'
                self._addTrsQueue(trs['trs_ids'])
                self.setStateForTrs({
                    'state': state }, trs['trs_ids'])
                self.sendChargedReceipt(trs['cc_id'], trs['trs_ids'])
            else:
                (dayRate, totalDays) = self.getReprocessDeclinedConfig()
                processTime = getCurTime()
                nextProcessTime = getTimeChange(processTime, day = dayRate)
                if trs['process_count'] >= totalDays - 1:
                    state = 'failed'
                    self.setStateForTrs({
                        'state': state,
                        'upg_id': trs['upg_id'] }, trs['trs_ids'])
                    declinedq.removeByTrsIds(trs['trs_ids'])
                else:
                    p = { }
                    p['state'] = 'open'
                    p['process_time'] = processTime
                    p['next_process_time'] = nextProcessTime
                    p['process_count'] = trs['process_count'] + 1
                    p['acct_id'] = trs['acct_id']
                    for t in trs['data']:
                        p['amount'] = t['amount']
                        p['declinedqId'] = t['declinedqId']
                        declinedq.update(p)
                    
        
        del upgProxy
        del declinedq
        del postauthq

    
    def getNeedPendingTrs(self, curTime):
        '''
        @Params: curTime(String): "2008-08-08 08:08:08"
        @Return: [{"upgId":12,
                   "ccId":12,
                   "amount":12.12}]
        '''
        result = []
        
        try:
            while not self.canPostauth():
                time.sleep(30)
            postauthq = PostauthQueue()
            postauthq.add()
            result = postauthq.getNeedPostauth(delayHours = POSTAUTH_DELAY_HOURS)
            del postauthq
        except IOError:
            ex = None
            if str(ex).lower().find('broken pipe') > -1:
                self.log.critical('Critical error in getNeedPendingTrs: %s' % str(ex))
                sys.exit()
            else:
                self.log.error('Error occurs when get pending trs: %s' % str(ex))
        except DatabaseError:
            ex = None
            if str(ex).find('database disk image is malformed') > -1:
                self._setPQLock(str(ex))
            
            msg = 'Error in getNeedPendingTrs(%s): %s'
            raise DatabaseError(msg % (str(curTime), str(ex)))

        return result

    
    def formTrsIds(self, trsIds):
        '''
        @Params: trsIds(List): [1, 2, 3]
        @Return: "(1,2,3)"
        '''
        return '(%s)' % ','.join(str(trsId) for trsId in trsIds)

    
    def splitTrsIds(self, trsIds):
        '''
        @Params: trsIds(String): "(1,2,3)"
        @Return: [1, 2, 3]
        '''
        return trsIds.replace('(', '').replace(')', '').split(',')

    
    def getDeclinedTrs(self, curTime):
        '''
        @Params: curTime(String): "2008-08-08 08:08:08"
        @Return: [{"postauthqId":12,
                   "upgId":12,
                   "ccId":12,
                   "transactionIds":"(1,2)",
                   "processCount":2,
                   "nextProcessTime":"2008-08-08 08:08:07",
                   "amount":12.12}]
        '''
        result = []
        
        try:
            while not self.canPostauth():
                time.sleep(30)
            declinedq = DeclinedQueue()
            (dayRate, totalDays) = self.getReprocessDeclinedConfig()
            result = declinedq.getDeclinedTrs(curTime, totalDays)
            del declinedq
        except IOError:
            ex = None
            if str(ex).lower().find('broken pipe') > -1:
                self.log.critical('Critical error in getDeclinedTrs: %s' % ex)
                sys.exit()
            else:
                self.log.error('Error occurs when get declined trs: %s' % str(ex))
        except DatabaseError:
            ex = None
            if str(ex).find('database disk image is malformed') > -1:
                self._setPQLock(str(ex))
            
            msg = 'Error in getDeclinedTrs(%s): %s'
            raise DatabaseError(msg % (str(curTime), str(ex)))

        return result

    
    def sendChargedReceipt(self, ccId, trsList):
        ''' Sent the charged receipt for the shopping cart.
        @Params: ccId(int)
                 shoppingCartId(str)
                 trsList(list)
        @Return: None
        '''
        if not trsList:
            return None
        
        for i in range(10):
            
            try:
                upgProxy = UPGProxy.getInstance()
                result = upgProxy.getTrsShoppingCartId(trsList)
                umsProxy = UmsProxy.getInstance()
                for shoppingCartId in result:
                    for j in range(10):
                        
                        try:
                            status = umsProxy.sendChargedReceipt(ccId, shoppingCartId, result[shoppingCartId])
                            if str(status) == '1':
                                break
                            else:
                                raise Exception('Check ums proxy log.')
                        except Exception:
                            ex = None
                            self.log.error('Time %s >> Error when sendChargedReceipt for %s on %s: %s' % (j + 1, result[shoppingCartId], ccId, ex))

                    
                
            except Exception:
                ex = None
                self.log.error('Time %s >> Error when sendChargedReceipt for %s on %s: %s' % (i + 1, trsList, ccId, ex))

        

    
    def _fmtCompareMoney(self, money):
        ''' Format the money.
        @Params: money(float)
        @Return: result(int)
        '''
        return int('%.0f' % float(money) * 100)

    
    def _fmtMoney(self, money):
        ''' Format the money.
        @Params: money(float)
        @Return: result(str)
        '''
        return '%.2f' % round(float(money), 2)

    
    def _chkTrsQueue(self, trsIds):
        ''' Format the money.
        @Params: trsIds(list)
        @Return: result(int) - 0: not processed
                               1: processed
        '''
        result = 0
        tpq = TrsProcessQueue()
        dup = []
        for trsId in trsIds:
            tpqCount = tpq.getCount(trsId)
            if tpqCount >= 2:
                result = 1
            elif tpqCount == 1:
                result = 1
                tpq.add(trsId)
                dup.append(str(trsId))
            
        
        if dup:
            msg = 'Duplicate processing for the transactions %s, please check the postauth thread of the kiosk.' % ','.join(dup)
            self._sendMailFromLocal(msg)
            self._sendMailFromUmsProxy('alert@mydvdkiosks.net', [
                'developers@cereson.com'], 'Duplicate transaction for %s' % self.kioskId, msg)
        
        del tpq
        return result

    
    def _addTrsQueue(self, trsIds):
        ''' Format the money.
        @Params: trsIds(list)
        @Return: None
        '''
        tpq = TrsProcessQueue()
        for trsId in trsIds:
            while True:
                
                try:
                    tpqCount = tpq.add(trsId)
                except DatabaseError:
                    ex = None
                    if str(ex).find('database is locked') == -1:
                        raise 
                    
                    time.sleep(random.randint(1, 30))

        
        del tpq
        return None

    
    def _setProcessCache(self, ccId, amount, trsType, success = True):
        ''' Set process cache for the transaction.
        @params ccId(int)
        @params amount(float)
        @params trsType(str)
        @params success(bool)
        @return: None
        '''
        self.log.info('Add to process cache: ccId(%s) amount(%s) trsType(%s)' % (ccId, amount, trsType))
        today = getCurTime('%Y-%m-%d')
        trsType = trsType.lower()
        for k in list(self._process_cache.keys()):
            if k != today:
                self._process_cache.pop(k)
            
        
        key = self._formProcessKey(ccId, amount)
        if today not in self._process_cache:
            self._process_cache[today] = { }
        
        if key not in self._process_cache[today]:
            self._process_cache[today][key] = {
                'all': 0,
                'success': 0,
                'sale': 0,
                'preauth': 0,
                'postauth': 0,
                'refund': 0 }
        
        self._process_cache[today][key]['all'] += 1
        self._process_cache[today][key][trsType] += 1
        if success:
            self._process_cache[today][key]['success'] += 1
        

    
    def _chkProcessCache(self, ccId, amount, trsType):
        ''' Check the process cache for the transaction.
        If invalid, decline it and return decline message,
        else pass it.
        @params ccId(int)
        @params amount(float)
        @params trsType(str)
        @return: msg
        '''
        msg = ''
        today = getCurTime('%Y-%m-%d')
        key = self._formProcessKey(ccId, amount)
        trsType = trsType.lower()
        trsCount = self._process_cache.get(today, { }).get(key, { }).get(trsType, 0)
        if trsCount >= self._MAX_PROCESS_COUNT:
            msg = 'Decline - MAX %s in one day(kiosk)' % self._MAX_PROCESS_COUNT
            m = 'Duplicate transaction may be found for kiosk %s, ccId: %s, trsType: %s, amount %s: %s'
            m = m % (self.kioskId, ccId, trsType, amount, msg)
            self._sendMailFromUmsProxy('alert@mydvdkiosks.net', [
                'developers@cereson.com'], 'Duplicate transaction for %s' % self.kioskId, m)
            self._sendMailFromLocal(m)
        
        return msg

    
    def _formProcessKey(self, ccId, amount):
        '''
        @params ccId(int)
        @params amount(float)
        @return: key
        '''
        return '%s_%s' % (ccId, self._fmtCompareMoney(amount))

    
    def _chkPQLock(self):
        ''' Check the POSTAUTH_QUEUE_LOCK, if exists, exit the thread.
        '''
        if os.path.exists(POSTAUTH_QUEUE_LOCK_PATH):
            sys.exit()
        

    
    def _setPQLock(self, m):
        ''' Set the POSTAUTH_QUEUE_LOCK.
        '''
        f = open(POSTAUTH_QUEUE_LOCK_PATH, 'w')
        
        try:
            f.write('1')
        finally:
            f.close()

        msg = 'The mkc.db of %s may be broken.' % self.kioskId
        if m:
            msg += 'The error message is %s' % m
        
        self._sendMailFromUmsProxy('alert@mydvdkiosks.net', [
            'developers@cereson.com'], 'mkc.db of %s may be broken' % self.kioskId, msg)
        self._sendMailFromLocal(msg)

    
    def _sendMailFromUmsProxy(self, _from, _to, subject, content):
        ''' Send email from ums proxy.
        '''
        
        try:
            umsProxy = UmsProxy.getInstance()
            p = { }
            p['from'] = _from
            p['to'] = _to
            p['subject'] = subject
            p['content'] = content
            self.log.info(content)
            (status, msg) = umsProxy.getRemoteData('sendMailUtils', p)
        except Exception:
            ex = None
            self.log.error('error when _sendMailFromUmsProxy: %s' % ex)


    
    def _sendMailFromLocal(self, content):
        
        try:
            connProxy = ConnProxy.getInstance()
            self.log.info(content)
            connProxy.emailAlert('PRIVATE', content, 'developers@cereson.com', critical = connProxy.UNCRITICAL)
            del connProxy
        except Exception:
            ex = None
            self.log.error('error when _sendMailFromLocal: %s' % ex)


    
    def _refundUnuseChipNPin(self):
        ''' Cancel the unused chip n pin transactions.
        @Params: None
        @Return: None
        '''
        upgProxy = UPGProxy.getInstance()
        
        try:
            upgIds = upgProxy._getUnusedChipNPin()
            for upgId in upgIds:
                if not self.canPostauth():
                    break
                
                
                try:
                    self.log.info('begin refund for unused ChipNPin upg ID %s' % upgId)
                    upgInfo = upgProxy.getUpgInfoByUpgId(upgId)
                    if str(upgInfo['ccId']) == '0':
                        ccInfo = { }
                        ccInfo['cc_number_sha1'] = ''
                        ccInfo['cc_expdate'] = ''
                        ccInfo['cc_name'] = ''
                        ccInfo['cc_number'] = ''
                    else:
                        ccInfo = upgProxy.getCCInfoByCcId(upgInfo['ccId'])
                    pgtr = upgInfo['oid']
                    if str(upgInfo['oid']).find('--') == -1:
                        (trsRef, pgtr) = upgInfo['additional'].split('|||')
                    
                    if pgtr:
                        (server, port, baseUrl) = upgProxy._getUpgServerFromUrl(upgProxy._getConfigByKey('upg_url'))
                        chipNPin = chip_n_pin.ChipNPin(self.kioskId, server, port, baseUrl)
                        result = chipNPin.refund(upgInfo['acctId'], ccInfo['cc_number_sha1'], ccInfo['cc_expdate'], ccInfo['cc_name'], upgInfo['amount'], '', '', pgtr)
                        self.log.info('refund result for unused ChipNPin upg ID %s: %s' % (upgId, result))
                    else:
                        result = ('0', '', '')
                    if str(result[0]) == '0' or str(result[1]).strip().find('34020') >= 0:
                        while True:
                            
                            try:
                                upgProxy.updateUpgInfoByUpgId({
                                    'resultCode': '-1',
                                    'upgId': upgId })
                            except Exception:
                                ex = None
                                self.log.error('_refundUnuseChipNPin update: %s' % ex)
                                if str(ex).find('database is locked') == -1:
                                    raise 
                                
                                time.sleep(random.randint(1, 30))

                except Exception:
                    ex = None
                    self.log.error('_refundUnuseChipNPin %s: %s' % (upgId, traceback.format_exc()))

        except Exception:
            ex = None
            self.log.error('_refundUnuseChipNPin: %s' % ex)


    
    def getReprocessDeclinedConfig(self):
        ''' Get the configuration of declined reprocessing.
        @params None
        @return: dayRate(int), totalDays(int)
        '''
        upgProxy = UPGProxy.getInstance()
        dayRate = 1
        totalDays = 7
        
        try:
            dayRate = int(upgProxy._getConfigByKey('reprocessing_interval'))
            if dayRate < 1:
                dayRate = 1
            
            totalDays = int(upgProxy._getConfigByKey('reprocessing_count'))
            if totalDays < 7:
                totalDays = 7
            
            del upgProxy
        except Exception:
            ex = None
            self.log.error('getReprocessDeclinedConfig: %s' % ex)

        return (dayRate, totalDays)

    
    def _get_not_charged_cache(self, trs_ids):
        ''' get not charged cache
        '''
        trs = []
        for trs_id in trs_ids:
            if not self._get_charge_cache(trs_id):
                trs.append(trs_id)
            
        
        return trs

    
    def _set_charge_cache(self, trs_id, params):
        ''' set the charge cache into a file for one transactions
        @param trs_id(int): transaction ID
        @param params(dict): upg charged informations
        '''
        file_path = os.path.join(self._get_charge_cache_dir(), str(trs_id))
        fd = open(file_path, 'wb')
        
        try:
            fd.write(str(params))
        finally:
            fd.close()


    
    def _get_charge_cache(self, trs_id):
        ''' get the charge cache for the transaction
        @param trs_id(int): 
        @return: the cached charge if it does, else return None
        @rtype: {}
        '''
        file_path = os.path.join(self._get_charge_cache_dir(), str(trs_id))
        if os.path.exists(file_path):
            fd = open(file_path, 'rb')
            
            try:
                result = fd.read()
            finally:
                fd.close()

            return eval(result)
        else:
            return None

    
    def _remove_charge_cache(self, trs_id):
        ''' remove the charge cache
        @param trs_id(int): 
        '''
        file_path = os.path.join(self._get_charge_cache_dir(), str(trs_id))
        if os.path.exists(file_path):
            os.remove(file_path)
        

    
    def _get_charge_cache_dir(self):
        ''' get the charge cache dir, if the dir is not created, create it
        @return: the charge cache dir path
        '''
        file_path = os.path.join(USER_ROOT, 'kiosk', 'var', 'charge_cache')
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        
        return file_path



def check_one_thread():
    ''' check if it has another process, if it need exit 
    '''
    file_name = 'upg_postauth_thread.pyc'
    cmd = 'ps -eo pid,command | grep %s | grep python | grep -v grep' % file_name
    result = subprocess.getoutput(cmd)
    if result:
        pid = str(os.getpid())
        for row in result.split('\n'):
            msg = row.split()
            if msg and msg[0] != pid:
                print('other thread %s is running, this thread %s exit' % (msg[0], pid))
                os.abort()
                return None
            
        
    


def main():
    check_one_thread()
    pt = PostauthThread()
    pt.start()

if __name__ == '__main__':
    main()

