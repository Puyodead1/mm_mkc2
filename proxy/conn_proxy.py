# Source Generated with Decompyle++
# File: conn_proxy.pyc (Python 2.5)

'''
connection proxy for kiosk

Modules:
    mda,
    config
    base_proxy
    tools
    base64
    price_coupon_kiosk

Change Log:
    2012-02-20  Modified by Tim
        add function calculate_price_without_coupon, save_rental_movie_out_status
        modified the function checkRfidAndSaveTrs
    2012-02-03  Modified by Kitch
        add method saveAIStatus
    2012-01-10  Modified by Helo
        add critical in alertEmail Method
    2012-01-04  Modified by Kitch
        change getPriceInfoByRfid for game & Blu-ray preauth_method
    2011-06-03  Modified by Kitch
        movie search enhancement for getAvailableMovieListByTitle
    2011-01-30  Modified by Kitch
        change logic for S500 in methods: _getLoadSlotId, checkRfidAndSaveTrs, 
                                          getAvailableReturnSlotId, setKioskInfo, 
                                          getKioskInfo, moveSlot, getSlotIds, 
                                          getSmartLoadSlotId
    2011-01-12  Modified by Kitch
        add params remoteKioskId for method syncDataRemoteKiosk
    2010-11-11  Modified by Kitch
        Remove disc from selling when its sale price is 0
    2009-11-24  Modified by Kitch
        1. new method getAutoUpdateLatestVersion
        2. add field ms_expi_time(monthly subscription expired time) to table transactions
    2009-11-19  Modified by Kitch
        new method downloadServerDB
    2009-10-29  Modified by Kitch
        add category logic in getPriceInfoByRfid, saveTrs
    2009-10-23  Modified by Kitch
        Change "All Movies" label in Genre to "All Discs"
    2009-09-17  Modified by Kitch
        add a status in checkRfidAndSaveTrs: Disc remembered as unloaded
    2009-07-22  Modified by Kitch
        add setExternalIP
    2009-07-07  Modified by Kitch
        add setBadSlot
    2009-06-10  Modified by Kitch
        add isPickup to method saveTrs
    2009-06-09  Modified by Kitch
        add field coupon_text
    2009-06-05  Modified by Kitch
        add field price_plan_dynamic in rfids and upc_load_config
    2009-05-18  Modified by Kitch
        1. add method getInDiscs
        2. add method logMkcEvent
    2009-05-04  Modified by Kitch
        add gracePeriod
    2009-04-28  Modified by Kitch
        max dvd out and buy limit: 0 means no limit
    2009-04-27  Modified by Kitch
        add getArrangementPlan, moveSlot, finishArrangement
    2009-04-08  Modified by Kitch
        add getOutDiscsByCode, getOutDiscsByCcId
    2009-04-01  Modified by Kitch
        check and download kiosk logo from server
    2009-03-05  Modified by Kitch
        add verifyDb, getLatestVersion
    2009-01-12  Created by Kitch
'''
import re
import os
from . import config
from . import price_coupon_kiosk
from .mda import Db, DatabaseError
from .base_proxy import Proxy
from .tools import *
from base64 import b64encode, b64decode

try:
    import psyco
    psyco.full()
except:
    pass

import sys
sys.path.append(config.MKC_PATH)
from mobject import *
__version__ = '0.5.9'
VERSION_FILE = os.path.join(config.USER_ROOT, 'kiosk/var/version.ini')
PROXY_NAME = 'CONN_PROXY'
OVER_CAPACITY = 'over_capacity'
(CRITICAL, MINICRITICAL, UNCRITICAL) = ('CRITICAL', 'UNCRITICAL', '')

class ConnProxy(Proxy):
    
    def __init__(self):
        self.CRITICAL = 'CRITICAL'
        self.MINICRITICAL = 'UNCRITICAL'
        self.UNCRITICAL = ''

    
    def on_init(self):
        super(ConnProxy, self).__init__(PROXY_NAME)

    
    def __del__(self):
        super(ConnProxy, self).__del__()

    
    def __new__(cls, *args, **kwargs):
        if '_inst' not in vars(cls):
            cls._inst = object.__new__(cls, *args, **kwargs)
            cls._inst.on_init()
        
        return cls._inst

    
    def getInstance() -> 'ConnProxy':
        return ConnProxy()

    getInstance = staticmethod(getInstance)
    
    def getOperatorCode(self):
        """
        @Params: None
        @Return: operatorCode (string): e.g. 'this machine is great'

        get the Operator Code
        """
        return self._getConfigByKey('operator_code')

    
    def getDefaultSettings(self, disc):
        '''
        @Params: upc (string)
        @Return: {"slot_id":"XXX",
                  "front_slot_id":"XXX",
                  "back_slot_id":"XXX",
                  "default_price_plan_id":"XXX",
                  "default_price_plan_text":"XXX",
                  "default_price_plan_dynamic": "XXX",
                  "default_sale_price":"XXX",
                  "default_sale_convert_price":"XXX",
                  "default_cost":"XXX"} (dict)

        get the default settings: slotId, defaultPricePlan, defaultPricePlanDynamic
        defaultSalePrice, defaultCost, frontSlotId, backSlotId
        '''
        conf = { }
        slotId = self._getLoadSlotId(disc.upc)
        (frontSlotId, backSlotId) = self._get2SlotsForLoad()
        priceInfo = self._getUpcPriceInfoByUpc(disc.upc)
        if priceInfo:
            defaultPricePlanId = priceInfo['price_plan_id']
            defaultPricePlanDynamic = priceInfo['price_plan_dynamic']
            defaultSalePrice = priceInfo['sale_price']
            defaultSaleConvertPrice = priceInfo['sale_convert_price']
            defaultCost = priceInfo['cost']
        else:
            defaultPricePlanId = self._getConfigByKey('default_price_plan')
            defaultPricePlanDynamic = '1'
            defaultSalePrice = self._getConfigByKey('default_sale_price')
            defaultSaleConvertPrice = self._getConfigByKey('sale_convert_price')
            defaultCost = self._getConfigByKey('default_cost')
        pricePlanInfo = self._getPricePlanById(defaultPricePlanId)
        defaultPricePlanText = pricePlanInfo['data_text']
        defaultSalePrice = fmtMoney(defaultSalePrice)
        defaultCost = fmtMoney(defaultCost)
        conf = {
            'slot_id': slotId,
            'front_slot_id': frontSlotId,
            'back_slot_id': backSlotId,
            'default_price_plan_id': defaultPricePlanId,
            'default_sale_price': defaultSalePrice,
            'default_sale_convert_price': defaultSaleConvertPrice,
            'default_cost': defaultCost,
            'default_price_plan_text': defaultPricePlanText,
            'default_price_plan_dynamic': defaultPricePlanDynamic }
        disc.slotID = slotId
        disc.pricePlanID = defaultPricePlanId
        disc.dynamicPricePlan = defaultPricePlanDynamic
        disc.pricePlan = defaultPricePlanText
        disc.salePrice = defaultSalePrice
        disc.saleConvertPrice = defaultSaleConvertPrice
        disc.cost = defaultCost
        return conf

    
    def _hasWeeklyPricePlan(self):
        exist = 0
        sql = "SELECT COUNT(id) FROM price_plans_week WHERE price_plan!='' AND price_plan IS NOT NULL;"
        row = self.mkcDb.query(sql, 'one')
        if row:
            (exist,) = row
        
        return str(exist)

    
    def getDefaultCurrencySymbol(self):
        """
        @Params: None
        @Return: currencySymbol (string): e.g. '$'

        get the default currency symbol
        """
        result = '$'
        sql = "SELECT value FROM config WHERE variable='currency_symbol';"
        row = self.mkcDb.query(sql, 'one')
        if row:
            (result,) = row
        
        return str(result, 'utf-8')

    
    def _getLoadSlotId(self, upc):
        '''
        return the loaded slotId,
        get slotId from remote server recommended,
        if None, get from local db
        '''
        slotId = ''
        sql = 'SELECT COUNT(*) FROM slots AS S, rfids AS R WHERE S.rfid=R.rfid AND R.upc=? AND S.id<500;'
        (exist,) = self.mkcDb.query(sql, 'one', (upc,))
        if exist:
            sql = "SELECT MAX(id) FROM slots WHERE state='empty';"
        else:
            sql = "SELECT MIN(id) FROM slots WHERE state='empty';"
        
        try:
            result = self.mkcDb.query(sql, 'one')
            if result:
                (slotId,) = result
        except Exception as ex:
            self.log.error('_getLoadSlotId: ' + str(ex))

        if not slotId and self._checkOverCapacityCount():
            if exist:
                sql = "SELECT MAX(S.id) FROM slots AS S, rfids AS R WHERE S.rfid=R.rfid AND R.state='out';"
            else:
                sql = "SELECT MIN(S.id) FROM slots AS S, rfids AS R WHERE S.rfid=R.rfid AND R.state='out';"
            
            try:
                result = self.mkcDb.query(sql, 'one')
                if result:
                    (slotId,) = result
            except Exception as ex:
                self.log.error('_getLoadSlotId: ' + str(ex))

        
        slotId = str(slotId)
        return slotId

    
    def _get2SlotsForLoad(self):
        '''
        get 2 recommendation slots for Load:
        front slot and back slot
        '''
        frontSlotId = ''
        backSlotId = ''
        sql = "SELECT (SELECT MIN(id) FROM slots WHERE state='empty') AS f_slot, (SELECT MAX(id) FROM slots WHERE state='empty') AS b_slot;"
        result = self.mkcDb.query(sql, 'one')
        if result:
            (frontSlotId, backSlotId) = result
        
        if (not frontSlotId or not backSlotId) and self._checkOverCapacityCount():
            sql = "SELECT (SELECT MIN(S.id) FROM slots AS S, rfids AS R WHERE S.rfid=R.rfid AND R.state='out') AS f_slot, (SELECT MAX(S.id) FROM slots AS S, rfids AS R WHERE S.rfid=R.rfid AND R.state='out') AS b_slot;"
            result = self.mkcDb.query(sql, 'one')
            if result:
                (frontSlotId, backSlotId) = result
            
        
        return (str(frontSlotId), str(backSlotId))

    
    def _checkOverCapacityCount(self):
        """
        check if the disc can be loaded to 'out' slot
        return True or False
        """
        
        try:
            overCapacitySlotsLimit = int(self._getConfigByKey('over_capacity_slots_limit'))
        except:
            overCapacitySlotsLimit = 0

        sql = 'SELECT COUNT(id) FROM over_capacity_rfids;'
        row = self.mkcDb.query(sql, 'one')
        if row:
            overCapacityRfidCount = int(row[0])
        else:
            overCapacityRfidCount = 0
        return overCapacityRfidCount < overCapacitySlotsLimit

    
    def _getPricePlanById(self, pricePlanId):
        '''
        get price plan data and text by id
        '''
        pricePlanInfo = { }
        sql = 'SELECT id, data, data_text FROM price_plans WHERE id=?;'
        result = self.mkcDb.query(sql, 'one', (pricePlanId,))
        if result:
            (id, data, data_text) = result
            pricePlanInfo['id'] = str(id)
            pricePlanInfo['data'] = str(data)
            pricePlanInfo['data_text'] = self._fmt_price_plan_text(str(data_text))
        
        return pricePlanInfo

    
    def _fmt_price_plan_text(self, plan_text):
        ''' replace the "Cut Offtime" with "Return Time"
        
        if the return_time in config is not None, replace it
        '''
        if not plan_text:
            plan_text = ''
        
        data_text = plan_text.replace('Cutoff Time', 'Return Time')
        return_time = self._getConfigByKey('return_time')
        if return_time:
            reobj = re.compile('(([0-1][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]))')
            data_text = reobj.sub(return_time, data_text)
        
        return data_text

    
    def getAvailableSlotIdList(self):
        '''
        @Params: None
        @Return: [XXX, XXX, XXX,...] (list)

        get all empty / out slots list
        '''
        slotIds = []
        sql = "SELECT id FROM slots WHERE state='empty';"
        rows = self.mkcDb.query(sql)
        if rows:
            for slotId, in rows:
                slotIds.append(str(slotId))
            
        
        if self._checkOverCapacityCount():
            sql = "SELECT S.id FROM slots AS S, rfids AS R WHERE S.rfid=R.rfid AND R.state='out';"
            rows = self.mkcDb.query(sql)
            if rows:
                for slotId, in rows:
                    slotIds.append(str(slotId))
                
            
        
        slotIds.sort()
        return slotIds

    
    def getPricePlanList(self):
        '''
        @Params: None
        @Return: [{"id":XXX, "data":XXX, "data_text":XXX},
                  {"id":XXX, "data":XXX, "data_text":XXX}, ...] (list[dict])

        get all price plan list
        '''
        pricePlanList = []
        sql = 'SELECT id, data, data_text FROM price_plans;'
        rows = self.mkcDb.query(sql)
        if rows:
            for id, data, dataText in rows:
                pricePlanList.append({
                    'id': str(id),
                    'data': str(data),
                    'data_text': self._fmt_price_plan_text(str(dataText)) })
            
        
        self.log.info('Succeed to get price plan list.')
        return pricePlanList

    
    def _getRfidInfoByRfid(self, rfid):
        '''
        get rfid info by rfid
        '''
        rfidInfo = { }
        sql = 'SELECT rfid, upc, movie_id, title, genre, sales_price, sale_convert_price, price_plan_id, price_plan_dynamic, enable_reduce, reduce_formula, last_reduce_date, enable_reduce_convert_price, reduce_formula_convert_price, last_reduce_date_convert_price, category_id, state FROM rfids WHERE rfid=?;'
        result = self.mkcDb.query(sql, 'one', (rfid,))
        if result:
            (rfid, upc, movieId, title, genre, salesPrice, saleConvertPrice, pricePlanId, pricePlanDynamic, enablReduce, reduceFormula, lastReduceDate, enablReduceConvertPrice, reduceFormulaConvertPrice, lastReduceDateConvertPrice, categoryId, state) = result
            rfidInfo['rfid'] = str(rfid)
            rfidInfo['upc'] = str(upc)
            rfidInfo['movie_id'] = str(movieId)
            rfidInfo['title'] = str(title)
            rfidInfo['genre'] = str(genre)
            rfidInfo['sales_price'] = str(salesPrice)
            rfidInfo['sale_convert_price'] = str(saleConvertPrice)
            rfidInfo['price_plan_id'] = str(pricePlanId)
            rfidInfo['price_plan_dynamic'] = str(pricePlanDynamic)
            rfidInfo['enable_reduce'] = str(enablReduce)
            rfidInfo['reduce_formula'] = str(reduceFormula)
            rfidInfo['last_reduce_date'] = str(lastReduceDate)
            rfidInfo['enable_reduce_convert_price'] = str(enablReduceConvertPrice)
            rfidInfo['reduce_formula_convert_price'] = str(reduceFormulaConvertPrice)
            rfidInfo['last_reduce_date_convert_price'] = str(lastReduceDateConvertPrice)
            rfidInfo['category_id'] = str(categoryId)
            rfidInfo['state'] = str(state)
        
        return rfidInfo

    
    def getSlotIdByRfid(self, rfid):
        '''
        @Params: rfid (string)
        @Return: slotId (string)

        get slot id by rfid
        '''
        return self._getSlotIdByRfid(rfid)

    
    def _getCostByRfid(self, rfid):
        '''
        get cost by rfid
        '''
        dvdCost = ''
        sql = 'SELECT cost FROM rfid_cost WHERE rfid=?;'
        result = self.mkcDb.query(sql, 'one', (rfid,))
        if result:
            (dvdCost,) = result
        
        dvdCost = str(dvdCost)
        return dvdCost

    
    def _getUpcPriceInfoByUpc(self, upc):
        '''
        get price plan and sale price by upc
        '''
        priceInfo = { }
        sql = 'SELECT upc, price_plan_id, price_plan_dynamic, sale_price, sale_convert_price, cost FROM upc_load_config WHERE upc=?;'
        result = self.mkcDb.query(sql, 'one', (upc,))
        if result:
            (upc, price_plan_id, price_plan_dynamic, sale_price, sale_convert_price, cost) = result
            priceInfo['upc'] = str(upc)
            priceInfo['price_plan_id'] = str(price_plan_id)
            priceInfo['price_plan_dynamic'] = str(price_plan_dynamic)
            priceInfo['sale_price'] = str(sale_price)
            priceInfo['sale_convert_price'] = str(sale_convert_price)
            priceInfo['cost'] = str(cost)
        
        return priceInfo

    
    def _getPricePlanDataByUpc(self, upc):
        '''
        get price plan data by upc
        '''
        pricePlanData = ''
        pricePlanDataText = ''
        sql = 'SELECT data, data_text FROM price_plans WHERE id IN (SELECT price_plan_id FROM upc_load_config WHERE upc=? LIMIT 1);'
        result = self.mkcDb.query(sql, 'one', (upc,))
        if result:
            (pricePlanData, pricePlanDataText) = result
        
        return (pricePlanData, self._fmt_price_plan_text(pricePlanDataText))

    
    def _getEventByEventId(self, eventId):
        '''
        get event info by eventId
        '''
        eventInfo = { }
        sql = 'SELECT category, action, data1, data2, data3, data4, data5, result, time_recorded, time_updated, state FROM events WHERE id=?;'
        result = self.mkcDb.query(sql, 'one', (eventId,))
        if result:
            (category, action, data1, data2, data3, data4, data5, result, time_recorded, time_updated, state) = result
            eventInfo['id'] = str(eventId)
            eventInfo['category'] = str(category)
            eventInfo['action'] = str(action)
            eventInfo['data1'] = str(data1)
            eventInfo['data2'] = str(data2)
            eventInfo['data3'] = str(data3)
            eventInfo['data4'] = str(data4)
            eventInfo['data5'] = str(data5)
            eventInfo['result'] = str(result)
            eventInfo['time_recorded'] = str(time_recorded)
            eventInfo['time_updated'] = str(time_updated)
            eventInfo['state'] = str(state)
        
        return eventInfo

    
    def isRfidLoadable(self, disc):
        """
        @Params: disc (object)
        @Return: statusCode (int): 0 -> error
                                   1 -> normal load
                                   2 -> RFID status 'in', 'reserved', 'unload'
                                   3 -> RFID status 'out'

        get slot id by rfid
        """
        statusCode = 0
        state = self._getDiscState(disc.rfid)
        if not state:
            statusCode = 1
        elif str(state) in ('in', 'reserved', 'unload', 'bad'):
            statusCode = 2
            disc.slotID = self._getSlotIdByRfid(disc.rfid)
        elif str(state) in 'out':
            statusCode = 3
            disc.slotID = self._getSlotIdByRfid(disc.rfid)
        
        self.log.info('load: %s, %s' % (statusCode, disc.rfid))
        return statusCode

    
    def _getDiscState(self, rfid):
        '''
        get disc state by rfid
        '''
        state = ''
        sql = 'SELECT state FROM rfids WHERE rfid=?;'
        result = self.mkcDb.query(sql, 'one', (rfid,))
        if result:
            (state,) = result
        
        return state

    
    def _getSlotIdByRfid(self, rfid):
        '''
        get slotId by rfid
        '''
        slotId = ''
        sql = 'SELECT id FROM slots WHERE rfid=?;'
        result = self.mkcDb.query(sql, 'one', (rfid,))
        if result:
            (slotId,) = result
        else:
            sql = 'SELECT COUNT(id) FROM over_capacity_rfids WHERE rfid=?;'
            row = self.mkcDb.query(sql, 'one', (rfid,))
            if row and row[0] > 0:
                slotId = OVER_CAPACITY
            
        slotId = str(slotId)
        return slotId

    
    def saveLoadStatus(self, disc):
        '''
        @Params: None
        @Return: None

        save load status
        '''
        self.log.info(disc)
        sqlList = []
        sqlUpcExist = 'SELECT COUNT(*) FROM upc_load_config WHERE upc=?;'
        (upcExist,) = self.mkcDb.query(sqlUpcExist, 'one', (sqlQuote(disc.upc),))
        if upcExist:
            sql = "UPDATE upc_load_config SET price_plan_id='%s', price_plan_dynamic='%s', sale_price='%s', sale_convert_price='%s', cost='%s' WHERE upc='%s';"
            sql = sql % (sqlQuote(disc.pricePlanID), sqlQuote(disc.dynamicPricePlan), sqlQuote(disc.salePrice), sqlQuote(disc.saleConvertPrice), sqlQuote(disc.cost), sqlQuote(disc.upc))
        else:
            sql = "INSERT INTO upc_load_config(upc, price_plan_id, price_plan_dynamic, sale_price, sale_convert_price, cost) VALUES('%s', '%s', '%s', '%s', '%s', '%s');"
            sql = sql % (sqlQuote(disc.upc), sqlQuote(disc.pricePlanID), sqlQuote(disc.dynamicPricePlan), sqlQuote(disc.salePrice), sqlQuote(disc.saleConvertPrice), sqlQuote(disc.cost))
        sqlList.append(sql)
        sqlRfidExist = 'SELECT COUNT(*) FROM rfid_cost WHERE rfid=?;'
        (rfidExist,) = self.mkcDb.query(sqlRfidExist, 'one', (sqlQuote(disc.rfid),))
        if rfidExist:
            sql = "UPDATE rfid_cost SET cost='%s' WHERE rfid='%s';"
            sql = sql % (sqlQuote(disc.cost), sqlQuote(disc.rfid))
        else:
            sql = "INSERT INTO rfid_cost(rfid, cost) VALUES('%s', '%s');"
            sql = sql % (sqlQuote(disc.rfid), sqlQuote(disc.cost))
        sqlList.append(sql)
        slotInfo = self._getSlotInfoBySlotId(disc.slotID)
        if slotInfo.get('rfid') and slotInfo.get('rfid', '') != disc.rfid:
            sqlEmptyExist = "SELECT id FROM slots WHERE state='empty' LIMIT 1;"
            row = self.mkcDb.query(sqlEmptyExist, 'one')
            if row and row[0]:
                sql = "UPDATE slots SET rfid='%s', state='occupied' WHERE id='%s';"
                sql = sql % (sqlQuote(slotInfo['rfid']), sqlQuote(row[0]))
                sqlList.append(sql)
            else:
                sql = "INSERT INTO over_capacity_rfids(rfid, add_time) VALUES('%s', DATETIME('now', 'localtime'));"
                sql = sql % (sqlQuote(slotInfo['rfid']),)
                sqlList.append(sql)
        
        sql = "UPDATE slots SET rfid='%s', state='occupied' WHERE id='%s';"
        sql = sql % (sqlQuote(disc.rfid), sqlQuote(disc.slotID))
        sqlList.append(sql)
        state = self._getDiscState(disc.rfid)
        if state:
            sql = "UPDATE rfids SET upc='%s', movie_id='%s', title='%s', genre='%s', state='in' WHERE rfid='%s';"
            sql = sql % (sqlQuote(disc.upc), sqlQuote(disc.movieID), sqlQuote(disc.title), sqlQuote(disc.genre), sqlQuote(disc.rfid))
        else:
            sql = "INSERT INTO rfids(rfid, upc, movie_id, title, genre, sales_price, sale_convert_price, price_plan_id, price_plan_dynamic, state) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 'in');"
            sql = sql % (sqlQuote(disc.rfid), sqlQuote(disc.upc), sqlQuote(disc.movieID), sqlQuote(disc.title), sqlQuote(disc.genre), sqlQuote(disc.salePrice), sqlQuote(disc.saleConvertPrice), sqlQuote(disc.pricePlanID), sqlQuote(disc.dynamicPricePlan))
        sqlList.append(sql)
        if not (disc.outKioskID):
            disc.outKioskID = self.kioskId
        
        eventId = self.logEvent(category = 'operation', action = 'load', data1 = disc.slotID, data2 = disc.rfid, data3 = disc.upc, data4 = disc.title, data5 = disc.outKioskID)
        
        try:
            self.mkcDb.updateTrs(sqlList)
            syncInfo = { }
            syncInfo['rfid'] = disc.rfid
            syncInfo['upc'] = disc.upc
            syncInfo['movie_id'] = disc.movieID
            syncInfo['title'] = disc.title
            syncInfo['genre'] = disc.genre
            syncInfo['slotId'] = disc.slotID
            syncInfo['cost'] = disc.cost
            syncInfo['price_plan_id'] = disc.pricePlanID
            syncInfo['sale_price'] = disc.salePrice
            syncInfo['sale_convert_price'] = disc.saleConvertPrice
            syncInfo['price_plan_dynamic'] = disc.dynamicPricePlan
            eventInfo = self._getEventByEventId(eventId)
            syncInfo['event_id'] = eventInfo['id']
            syncInfo['time_recorded'] = eventInfo['time_recorded']
            syncInfo['time_updated'] = eventInfo['time_updated']
            syncInfo['from_kiosk'] = eventInfo['data5']
            self.syncData('dbSyncLoadV4', syncInfo)
            self.log.info('Save dbSyncLoadV4 to sync db: ' + str(syncInfo))
        except:
            sql = 'DELETE FROM events WHERE id=?;'
            self.mkcDb.update(sql, (eventId,))
            raise 


    
    def getAllGenreList(self, theme):
        '''
        @Params: None
        @Return: [{"id":"NEW RELEASE", "text":"New Release"},
                  {"id":"(\'familly\')", "text":\'familly\'}, ...
                  {"id":"(\'action\', \'genre1\')", "text":\'Other\'},
                  {"id":\'ALL DISCS\', "text":\'All Discs\'}](List)
        '''
        if str(theme).lower() == 'game':
            return self._getAllGenreListGame()
        else:
            return self._getAllGenreListMovie()

    
    def _getAllGenreListMovie(self):
        result = []
        upcs = self._getAvailableUpcList()
        upcs = self._filterBluray(upcs)
        sql = 'SELECT id, category_name FROM category;'
        categoryId = ''
        categoryName = ''
        row = self.mkcDb.query(sql, 'one')
        if row:
            (categoryId, categoryName) = row
        
        categoryCount = 0
        if categoryId:
            sql = 'SELECT COUNT(rfid) FROM rfids WHERE category_id=?;'
            row = self.mkcDb.query(sql, 'one', (categoryId,))
            if row:
                (categoryCount,) = row
            
        
        sql = "SELECT COUNT(rfid) FROM rfids WHERE genre='Games' AND state IN ('in', 'unload', 'out');"
        gameCount = 0
        row = self.mkcDb.query(sql, 'one')
        if row:
            (gameCount,) = row
        
        result.append({
            'id': 'NEW RELEASE',
            'text': 'New Release' })
        sql = "SELECT genre, COUNT(upc) AS upcCount FROM rfids WHERE state IN ('in', 'unload', 'out') AND genre<>'Games' GROUP BY genre ORDER BY upcCount DESC;"
        rows = self.mkcDb.query(sql)
        GENRE_LIMIT_COUNT = config.GENRE_LIMIT_COUNT
        GENRE_LIMIT_COUNT = GENRE_LIMIT_COUNT - 1
        if len(upcs):
            GENRE_LIMIT_COUNT = GENRE_LIMIT_COUNT - 1
        
        if gameCount > 0:
            GENRE_LIMIT_COUNT = GENRE_LIMIT_COUNT - 1
        
        if categoryCount > 0:
            GENRE_LIMIT_COUNT = GENRE_LIMIT_COUNT - 1
        
        if len(rows) > GENRE_LIMIT_COUNT:
            i = 0
            other = []
            for row in rows:
                (genre, movieCount) = row
                i += 1
                if i <= GENRE_LIMIT_COUNT - 1:
                    tmp = { }
                    key = "('%s')" % genre.replace("'", "''")
                    tmp['id'] = key
                    tmp['text'] = genre
                    result.append(tmp)
                else:
                    other.append(genre)
            
            if gameCount > 0:
                result.append({
                    'id': "('Games')",
                    'text': 'Games' })
            
            tmp = {
                'id': "(%s)" % ", ".join(["'%s'" % sqlQuote(tmpGenre) for tmpGenre in other]),
                'text': 'Others'
            }
            result.append(tmp)
        else:
            for row in rows:
                (genre, movieCount) = row
                tmp = { }
                key = "('%s')" % sqlQuote(genre)
                tmp['id'] = key
                tmp['text'] = genre
                result.append(tmp)
            
            if gameCount > 0:
                result.append({
                    'id': "('Games')",
                    'text': 'Games' })
            
        if len(upcs):
            result.append({
                'id': 'BLU-RAY',
                'text': 'Blu-ray' })
        
        if categoryCount > 0:
            result.append({
                'id': 'CATEGORY',
                'text': str(categoryName, 'utf-8') })
        
        result.append({
            'id': 'ON SALE',
            'text': 'Clearance Discs' })
        result.append({
            'id': 'ALL DISCS',
            'text': 'All Discs' })
        return result

    
    def _getAllGenreListGame(self):
        result = []
        result.append({
            'id': 'XBOX360',
            'text': 'XBOX 360' })
        result.append({
            'id': 'PS3',
            'text': 'PlayStation 3' })
        result.append({
            'id': 'WII',
            'text': 'Nintendo Wii' })
        result.append({
            'id': 'ON SALE',
            'text': 'Clearance Games' })
        result.append({
            'id': 'NEW RELEASE',
            'text': 'All Games' })
        sql = 'SELECT id, category_name FROM category;'
        categoryId = ''
        categoryName = ''
        row = self.mkcDb.query(sql, 'one')
        if row:
            (categoryId, categoryName) = row
        
        categoryCount = 0
        if categoryId:
            sql = 'SELECT COUNT(rfid) FROM rfids WHERE category_id=?;'
            row = self.mkcDb.query(sql, 'one', (categoryId,))
            if row:
                (categoryCount,) = row
            
        
        if categoryCount:
            result.append({
                'id': 'CATEGORY',
                'text': categoryName })
        
        return result

    
    def _getAvailableUpcList(self):
        '''
        get available upc list in kiosk
        @Params: None
        @Return: upcList (list)
        '''
        upcList = []
        sql = "SELECT DISTINCT upc FROM rfids WHERE state IN ('in', 'unload', 'out');"
        rows = self.mkcDb.query(sql)
        return upcList

    
    def getAvailableMovieList(self, key, val):
        '''
        Get available movie list.
        @Params: key(str): "genre" | "keyword"
                 val(str): "(COMEDY)" | "dark"
        @Return: [
                    {"movie_pic":"x.jpg", "movie_title":"x",
                     "upc":"xxx", "available_count":"20",
                     "is_bluray":1},
                    {"movie_pic":"x.jpg", "movie_title":"x",
                     "upc":"xxx", "available_count":"3",
                     "is_bluray":1},
                 ]
        '''
        if key.lower() == 'genre':
            return self.getAvailableMovieListByGenre(val)
        elif key.lower() == 'keyword':
            return self.getAvailableMovieListByTitle(val)
        else:
            raise Exception('Invalid key %s' % key)

    
    def getAvailableMovieListByGenre(self, genre):
        '''
        @Params: genre(String)
        @Return: [{"movie_title":"ABC (2005)",
                   "movie_pic":"347.jpg",
                   "movie_big_pic":"347_big.jpg",
                   "available_count":4,
                   "upc":"",
                   "is_bluray":1}](List)
        '''
        movieList = []
        if genre.upper() == 'NEW RELEASE':
            movieList = self.getAvailableMovieListNewRelease()
        elif genre.upper() == 'ALL DISCS':
            movieList = self.getAvailableMovieListByTitle('')
        elif genre.upper() == 'BLU-RAY':
            movieList = self.getAvailableMovieListBluray()
        elif genre.upper() == 'CATEGORY':
            movieList = self.getAvailableMovieListCategory()
        elif genre.upper() in ('WII', 'XBOX360', 'PS3'):
            movieList = self.getAvailableGameList(genre.upper())
        elif genre.upper() == 'ON SALE':
            movieList = self.getAvailableMovieListOnSale()
        else:
            blurayUpcs = self._getBlurayUpcs()
            sql = "SELECT title, movie_id, upc, sales_price FROM rfids WHERE state IN ('in', 'unload', 'out') AND genre IN %s GROUP BY upc ORDER BY title ASC;" % genre
            rows = self.mkcDb.query(sql)
            for row in rows:
                (title, movieId, upc, sales_price) = row
                tmp = { }
                tmp['upc'] = str(upc)
                tmp['movie_title'] = title
                tmp['movie_pic'] = self._formPicName(movieId)
                tmp['movie_big_pic'] = self._formBigPicName(movieId)
                tmp['available_count'] = self._getAvailableCountByUpc(upc)
                tmp['is_bluray'] = (tmp['upc'] in blurayUpcs) & 1
                tmp['sales_price'] = sales_price
                movieList.append(tmp)
            
        return movieList

    
    def getAvailableMovieListByTitle(self, keyword):
        '''
        @Params: keyword(String)
        @Return: [{"movie_title":"ABC (2005)",
                   "movie_pic":"347.jpg",
                   "movie_big_pic":"347_big.jpg",
                   "available_count":4,
                   "upc":"",
                   "is_bluray":1}](List)
        '''
        movieList = []
        strWhere = "WHERE state IN ('in', 'unload', 'out') "
        if len(keyword) == 1 and keyword.isalnum():
            strWhere += "AND title LIKE '%s' " % (sqlQuote(keyword) + '%')
        else:
            keys = keyword.split()
            for key in keys:
                strWhere += "AND title LIKE '%s' " % ('%' + sqlQuote(key) + '%')
            
        blurayUpcs = self._getBlurayUpcs()
        sql = 'SELECT title, movie_id, upc, sales_price FROM rfids %s GROUP BY upc ORDER BY title ASC;' % strWhere
        rows = self.mkcDb.query(sql)
        for row in rows:
            (title, movieId, upc, sales_price) = row
            tmp = { }
            tmp['upc'] = str(upc)
            tmp['movie_title'] = title
            tmp['movie_pic'] = self._formPicName(movieId)
            tmp['movie_big_pic'] = self._formBigPicName(movieId)
            tmp['available_count'] = self._getAvailableCountByUpc(upc)
            tmp['is_bluray'] = (tmp['upc'] in blurayUpcs) & 1
            tmp['sales_price'] = sales_price
            movieList.append(tmp)
        
        return movieList

    
    def getAvailableMovieListNewRelease(self):
        '''
        @Params: None
        @Return: [{"movie_title":"ABC (2005)",
                   "movie_pic":"347.jpg",
                   "movie_big_pic":"347_big.jpg",
                   "available_count":4,
                   "upc":"",
                   "is_bluray":1}](List)
        '''
        movieList = []
        
        try:
            sql = "ATTACH DATABASE '%s' AS UPCDB;" % config.UPC_DB_PATH
            self.mkcDb.update(sql)
        except Exception as ex:
            pass

        blurayUpcs = self._getBlurayUpcs()
        sql = "SELECT title, movie_id, upc, (SELECT dvd_release_date FROM UPCDB.upc AS U WHERE U.upc=R.upc) AS release_date,sales_price FROM rfids AS R WHERE state IN ('in', 'unload', 'out') GROUP BY upc ORDER BY release_date DESC, title ASC;"
        rows = self.mkcDb.query(sql)
        for row in rows:
            (title, movieId, upc, releaseDate, sales_price) = row
            tmp = { }
            tmp['upc'] = str(upc)
            tmp['movie_title'] = title
            tmp['movie_pic'] = self._formPicName(movieId)
            tmp['movie_big_pic'] = self._formBigPicName(movieId)
            tmp['available_count'] = self._getAvailableCountByUpc(upc)
            tmp['is_bluray'] = (tmp['upc'] in blurayUpcs) & 1
            tmp['sales_price'] = sales_price
            movieList.append(tmp)
        
        
        try:
            sql = 'DETACH DATABASE UPCDB;'
            self.mkcDb.update(sql)
        except Exception as ex:
            pass

        return movieList

    
    def getAvailableMovieListBluray(self):
        '''
        @Params: None
        @Return: [{"movie_title":"ABC (2005)",
                   "movie_pic":"347.jpg",
                   "movie_big_pic":"347_big.jpg",
                   "available_count":4,
                   "upc":"",
                   "is_bluray":1}](List)
        '''
        movieList = []
        upcs = self._getAvailableUpcList()
        upcs = self._filterBluray(upcs)
        if len(upcs) == 1:
            strUpcs = "('" + str(upcs[0]) + "')"
        else:
            strUpcs = str(tuple(upcs))
        sql = 'SELECT title, movie_id, upc, sales_price FROM rfids WHERE upc IN %s GROUP BY upc ORDER BY title ASC;' % strUpcs
        rows = self.mkcDb.query(sql)
        for row in rows:
            (title, movieId, upc, sales_price) = row
            tmp = { }
            tmp['upc'] = str(upc)
            tmp['movie_title'] = title
            tmp['movie_pic'] = self._formPicName(movieId)
            tmp['movie_big_pic'] = self._formBigPicName(movieId)
            tmp['available_count'] = self._getAvailableCountByUpc(upc)
            tmp['is_bluray'] = 1
            tmp['sales_price'] = sales_price
            movieList.append(tmp)
        
        return movieList

    
    def getAvailableMovieListCategory(self):
        '''
        @Params: None
        @Return: [{"movie_title":"ABC (2005)",
                   "movie_pic":"347.jpg",
                   "movie_big_pic":"347_big.jpg",
                   "available_count":4,
                   "upc":"",
                   "is_bluray":1}](List)
        '''
        movieList = []
        blurayUpcs = self._getBlurayUpcs()
        sql = "SELECT title, movie_id, upc, sales_price FROM rfids WHERE state IN ('in', 'unload', 'out') AND category_id<>'' GROUP BY upc ORDER BY title ASC;"
        rows = self.mkcDb.query(sql)
        for row in rows:
            (title, movieId, upc, sales_price) = row
            tmp = { }
            tmp['upc'] = str(upc)
            tmp['movie_title'] = title
            tmp['movie_pic'] = self._formPicName(movieId)
            tmp['movie_big_pic'] = self._formBigPicName(movieId)
            tmp['available_count'] = self._getAvailableCountByUpc(upc, entrance = 'category')
            tmp['is_bluray'] = (tmp['upc'] in blurayUpcs) & 1
            tmp['sales_price'] = sales_price
            movieList.append(tmp)
        
        return movieList

    
    def getAvailableGameList(self, platform):
        '''
        @Params: platform: WII, XBOX360, PS3
        @Return: [{"movie_title":"ABC (2005)",
                   "movie_pic":"347.jpg",
                   "movie_big_pic":"347_big.jpg",
                   "available_count":4,
                   "upc":""}](List)
        '''
        gameList = []
        upcs = self._getAvailableUpcList()
        upcs = self._getDiscTypeByUpcList(upcs)
        sql = "SELECT title, movie_id, upc, sales_price FROM rfids WHERE state IN ('in', 'unload', 'out') GROUP BY upc ORDER BY title ASC;"
        rows = self.mkcDb.query(sql)
        for row in rows:
            (title, movieId, upc, sales_price) = row
            if str(upcs.get(upc)).upper() == str(platform).upper():
                tmp = { }
                tmp['upc'] = str(upc)
                tmp['movie_title'] = title
                tmp['movie_pic'] = self._formPicName(movieId)
                tmp['movie_big_pic'] = self._formBigPicName(movieId)
                tmp['available_count'] = self._getAvailableCountByUpc(upc)
                tmp['sales_price'] = sales_price
                gameList.append(tmp)
            
        
        return gameList

    
    def getAvailableMovieListOnSale(self):
        '''
        @Params: None
        @Return: [{"movie_title":"ABC (2005)",
                   "movie_pic":"347.jpg",
                   "movie_big_pic":"347_big.jpg",
                   "available_count":4,
                   "upc":"",
                   "is_bluray":1}](List)
        '''
        movieList = []
        blurayUpcs = self._getBlurayUpcs()
        sql = "SELECT rfid, title, movie_id, upc, sales_price, state FROM rfids WHERE state IN ('in', 'unload', 'out');"
        rows = self.mkcDb.query(sql)
        for row in rows:
            (rfid, title, movieId, upc, salesPrice, state) = row
            if salesPrice and float(salesPrice):
                tmp = { }
                tmp['rfid'] = rfid
                tmp['upc'] = str(upc)
                tmp['movie_title'] = title
                tmp['sales_price'] = salesPrice
                tmp['movie_pic'] = self._formPicName(movieId)
                tmp['movie_big_pic'] = self._formBigPicName(movieId)
                if state == 'out':
                    tmp['available_count'] = 0
                else:
                    tmp['available_count'] = 1
                tmp['is_bluray'] = (tmp['upc'] in blurayUpcs) & 1
                movieList.append(tmp)
            
        
        movieList.sort(cmp = (lambda x, y: cmp(float(x['sales_price']), float(y['sales_price']))))
        return movieList

    
    def loadDiscInfo(self, disc, rfid = None):
        if not (disc.upc):
            upc = self._getUpcBySlotId(disc.expressID, "('in', 'unload')")
            if upc:
                disc.upc = upc
            else:
                return None
        
        gene = 'rent'
        if disc.expressID:
            geneBy = 'express_id'
        elif disc.entrance.lower() == 'category':
            geneBy = 'category'
        else:
            geneBy = 'title'
        if rfid:
            infoRfid = rfid
        else:
            slotId = self.getCOSlotIdByUpcGene(disc.upc, gene, geneBy, disc.expressID)
            if slotId:
                infoRfid = self._getRfidBySlotId(slotId)
            else:
                sql = 'SELECT rfid FROM rfids WHERE upc=? LIMIT 1;'
                (infoRfid,) = self.mkcDb.query(sql, 'one', (disc.upc,))
        priceInfo = self.getPriceInfoByRfid(infoRfid)
        disc.salePrice = fmtMoney(priceInfo['sale_price'])
        disc.saleConvertPrice = priceInfo['sale_convert_price']
        disc.preauthAmount = priceInfo['deposit_amount']
        disc.memberPreauthAmount = priceInfo['member_deposit_amount']
        disc.pricePlan = priceInfo['price_plan_text']
        disc.rentalTax = priceInfo['rentals_tax']
        disc.saleTax = priceInfo['sales_tax']
        disc.pricePlanID = priceInfo['price_plan_id']
        outTime = getCurTime()
        inTime = getTimeChange(outTime, second = 1)
        ppe = price_coupon_kiosk.PricePlanEngine(priceInfo['price_plan'], {
            'out_time': outTime,
            'in_time': inTime })
        rentalPrice = ppe.calculate()
        disc.rentalPrice = fmtMoney(rentalPrice)
        disc.availableCount = self._getAvailableCountByUpc(disc.upc)
        if disc.expressID and not rfid:
            rfidInfo = self._getRfidBySlotId(disc.expressID)
            priceInfo = self.getPriceInfoByRfid(rfidInfo)
            disc.salePrice = fmtMoney(priceInfo['sale_price'])
        

    
    def _getAvailableCountByUpc(self, upc, entrance = ''):
        if str(entrance).lower() == 'category':
            sql = "SELECT COUNT(*) FROM rfids WHERE upc=? AND category_id<>'' AND state IN ('in', 'unload');"
        else:
            sql = "SELECT COUNT(*) FROM rfids WHERE upc=? AND state IN ('in', 'unload');"
        (count,) = self.mkcDb.query(sql, 'one', (upc,))
        return count

    
    def checkAddAnotherDisc(self, shoppingCart):
        '''
        @Params: shoppingCart (object)
        @Return: state: True or False

        check add disc to shopping cart
        '''
        state = True
        
        try:
            maxDvdOut = int(self._getConfigByKey('max_dvd_out'))
        except:
            maxDvdOut = 3

        
        try:
            buyLimit = int(self._getConfigByKey('buy_limit'))
        except:
            buyLimit = 1

        totalLimit = maxDvdOut + buyLimit
        if maxDvdOut != 0 and buyLimit != 0 and shoppingCart.getSize() >= totalLimit or shoppingCart.getSize() >= 5:
            state = False
        
        return state

    
    def addDiscToShoppingCart(self, shoppingCart, disc):
        '''
        @Params: shoppingCart (object), disc (object)
        @Return: statusCode: 0 -> OK
                             1 -> not available
                             2 -> shopping cart full

        add disc to shopping cart
        update rfid state to "XXX_pending"
        '''
        statusCode = 0
        
        try:
            maxDvdOut = int(self._getConfigByKey('max_dvd_out'))
        except:
            maxDvdOut = 3

        
        try:
            buyLimit = int(self._getConfigByKey('buy_limit'))
        except:
            buyLimit = 1

        rentCount = 0
        saleCount = 0
        for itm in shoppingCart.discs:
            if itm.gene.lower() == 'sale':
                saleCount += 1
            else:
                rentCount += 1
        
        if buyLimit != 0 and saleCount >= buyLimit and str(disc.gene).lower() == 'sale':
            statusCode = 2
        elif maxDvdOut != 0 and rentCount >= maxDvdOut and str(disc.gene).lower() == 'rent':
            statusCode = 2
        elif shoppingCart.getSize() >= 5:
            statusCode = 2
        else:
            sql = "SELECT COUNT(*) FROM rfids WHERE upc=? AND state IN ('in', 'unload');"
            (exist,) = self.mkcDb.query(sql, 'one', (disc.upc,))
            if exist:
                statusCode = 0
                if disc.expressID:
                    geneBy = 'express_id'
                elif disc.entrance.lower() == 'category':
                    geneBy = 'category'
                else:
                    geneBy = 'title'
                disc.slotID = self.getCOSlotIdByUpcGene(disc.upc, disc.gene, geneBy, disc.expressID, True)
                disc.rfid = self._getRfidBySlotId(disc.slotID)
                self.loadDiscInfo(disc, disc.rfid)
                if disc.gene.lower() == 'sale':
                    disc.preauthAmount = fmtMoney(float(disc.salePrice) * (1 + float(disc.saleTax.strip('%')) / 100))
                
                state = self._getDiscState(disc.rfid)
                if not state.endswith('_pending'):
                    state += '_pending'
                
                sql = 'UPDATE rfids SET state=? WHERE rfid=?;'
                self.mkcDb.update(sql, (state, disc.rfid))
            else:
                statusCode = 1
        return statusCode

    
    def removeDiscsFromShoppingCart(self, discs):
        '''
        @Params: discs (List of Disc Object)
        @Return: None

        remove discs from shopping cart
        update rfid state to "XXX" (remove "_pending")
        '''
        rfidList = []
        for disc in discs:
            rfidList.append(disc.rfid)
        
        if len(rfidList) == 1:
            strRfidList = "('" + str(rfidList[0]) + "')"
        else:
            strRfidList = str(tuple(rfidList))
        sql = "UPDATE rfids SET state=substr(state, 0, length(state)-8) WHERE rfid in %s AND state LIKE '%%_pending';"
        sql = sql % strRfidList
        self.mkcDb.update(sql)

    
    def resetAll(self):
        '''
        @Params: None
        @Return: None

        remove dvd from shopping cart
        update rfid state to "XXX" (remove "_pending")
        release the lock of discs (remove "_lock")

        unlock coupon session
        '''
        
        try:
            sqlList = []
            sql = "UPDATE rfids SET state=substr(state, 0, length(state)-8) WHERE state LIKE '%_pending';"
            sqlList.append(sql)
            sql = "UPDATE rfids SET lock_by='', lock_time='', state=substr(state, 0, length(state)-5) WHERE lock_time<>'' AND lock_time IS NOT NULL AND state LIKE '%_lock' AND lock_time<STRFTIME('%Y-%m-%d %H:%M:%S', DATETIME('now', 'localtime'), '-10 minutes');"
            sqlList.append(sql)
            self.mkcDb.updateTrs(sqlList)
        except Exception as ex:
            self.log.error('resetAll: %s' % str(ex))


    
    def getCouponInfo(self, coupon):
        '''
        @Params: coupon (object)
        @Return: statusCode (int)

        get coupon info from server
        '''
        statusCode = 1
        if self.SHOW_MODE:
            if coupon.couponCode == '':
                statusCode = 0
            elif coupon.couponCode in ('444444441', '444444440'):
                statusCode = 0
                coupon.couponData = '\n                <COUPON>\n                        <FACTORS></FACTORS>\n                        <TYPE>S</TYPE>\n                        <CONDITIONS>result = True</CONDITIONS>\n                        <ALGORITHM>\noutTime = transaction["out_time"]\ninTime = transaction["in_time"]\n\npricePlanData = transaction["price_plan"]\nparams = {"out_time":outTime, "in_time":inTime}\nppe = PricePlanEngine(pricePlanData, params)\n\nprice = ppe.calculate()\nprice = price - 1\nif price &lt; 0:\n    price = 0</ALGORITHM>\n                        <EXCLUSIVENESS></EXCLUSIVENESS>\n                        <ACCUMULATIVE>0</ACCUMULATIVE>\n                        <NOTES></NOTES>\n                </COUPON>\n                '
                coupon.couponType = 'S'
                coupon.description = 'Test Single Coupon'
                coupon.shortDes = 'tsc'
            elif coupon.couponCode == '444444442':
                statusCode = 0
                coupon.couponData = '\n                <COUPON>\n                        <FACTORS></FACTORS>\n                        <TYPE>M</TYPE>\n                        <CONDITIONS>result = True</CONDITIONS>\n                        <ALGORITHM></ALGORITHM>\n                        <EXCLUSIVENESS></EXCLUSIVENESS>\n                        <ACCUMULATIVE>0</ACCUMULATIVE>\n                        <NOTES></NOTES>\n                </COUPON>\n                '
                coupon.couponType = 'M'
                coupon.description = 'Test Multiple Coupon'
                coupon.shortDes = 'tmc'
            else:
                statusCode = 1
        elif coupon.couponCode:
            funcName = 'getCouponInfo'
            params = { }
            params['coupon_code'] = coupon.couponCode
            params['session_id'] = self.kioskId
            resultDic = self.getRemoteData(funcName, params)
            if resultDic:
                if resultDic['result'].lower() == 'ok':
                    statusCode = resultDic['zdata']['valid']
                    coupon.couponData = resultDic['zdata']['coupon_plan_data']
                    coupon.couponType = resultDic['zdata']['coupon_type']
                    coupon.description = resultDic['zdata']['coupon_description']
                    coupon.shortDes = resultDic['zdata']['coupon_short_description']
                    self.log.info('getCouponInfo from remote server: ' + str(resultDic['zdata']))
                else:
                    statusCode = -1
                    self.log.error('getCouponInfo error: ' + str(resultDic['zdata']))
            else:
                statusCode = -1
        else:
            statusCode = 0
        return statusCode

    
    def validateCoupons(self, shoppingCart):
        '''
        @Params: shoppingCart (object)
        @Return: {"rfid":XXX, "status_code":XXX, "coupon_code":XXX} (dict)

        validate coupons from remote server
        '''
        status = 1
        invalidCouponlist = []
        if not (self.SHOW_MODE):
            newShoppingCart = { }
            newShoppingCart['transactions'] = { }
            for disc in shoppingCart.discs:
                discRfid = disc.rfid
                rfidInfo = self._getRfidInfoByRfid(discRfid)
                pricePlanId = rfidInfo['price_plan_id']
                pricePlanInfo = self._getPricePlanById(pricePlanId)
                pricePlanData = pricePlanInfo['data']
                newShoppingCart['coupon_code'] = shoppingCart.coupon.couponCode
                newShoppingCart['transactions'][discRfid] = { }
                newShoppingCart['transactions'][discRfid]['coupon_code'] = disc.coupon.couponCode
                newShoppingCart['transactions'][discRfid]['price_plan'] = pricePlanData
            
            funcName = 'validateCoupon'
            params = { }
            params['shopping_cart'] = newShoppingCart
            resultDic = self.getRemoteData(funcName, params)
            if resultDic:
                if resultDic['result'].lower() == 'ok':
                    status = 1
                    invalidCouponlist = resultDic['zdata']
                    self.log.info('Validate coupons from remote server: ' + str(invalidCouponlist))
                elif resultDic['result'].lower() == 'timeout':
                    status = 2
                    self.log.error('Error to validate coupons from remote server: ' + str(resultDic['zdata']))
                else:
                    status = 0
                    self.log.error('Error to validate coupons from remote server: ' + str(resultDic['zdata']))
            
        
        return (status, invalidCouponlist)

    
    def validateUserCoupons(self, customer, shoppingCart):
        '''
        @Params: customer (object), shoppingCart (object)
        @Return: [couponCode, couponCode, ...] (list)

        validate coupon user limit from remote server
        '''
        status = 1
        invalidCouponlist = []
        if not (self.SHOW_MODE):
            funcName = 'validateUserCoupons'
            params = { }
            couponCodeList = []
            if shoppingCart.coupon.couponCode:
                couponCodeList.append(shoppingCart.coupon.couponCode)
            
            for disc in shoppingCart.discs:
                if disc.coupon.couponCode:
                    couponCodeList.append(disc.coupon.couponCode)
                
            
            params['coupon_code_list'] = couponCodeList
            params['cc_id'] = customer.ccid
            if couponCodeList:
                resultDic = self.getRemoteData(funcName, params)
                if resultDic:
                    if resultDic['result'].lower() == 'ok':
                        status = 1
                        invalidCouponlist = resultDic['zdata']
                        self.log.info('Validate User coupons from remote server: ' + str(invalidCouponlist))
                    elif resultDic['result'].lower() == 'timeout':
                        status = 2
                        self.log.error('Error to validate user coupons from remote server: ' + str(resultDic['zdata']))
                    else:
                        status = 0
                        self.log.error('Error to validate user coupons from remote server: ' + str(resultDic['zdata']))
                
            else:
                status = 1
        
        return (status, invalidCouponlist)

    
    def getUsableCouponDiscs(self, shoppingCart):
        '''
        @Params: shoppingCart (object)
        @Return: [disc] (list of disc object)

        get usable coupon discs
        '''
        discs = []
        for disc in shoppingCart.discs:
            if disc.gene == 'rent':
                discs.append(disc)
            
        
        return discs

    
    def _unlockCouponSession(self):
        '''
        @Params: couponCode (string)
        @Return: True or False (bool)

        delete coupon session by coupon code
        '''
        if not (self.SHOW_MODE):
            funcName = 'unlockCouponSession'
            params = { }
            resultDic = self.getRemoteData(funcName, params)
            if resultDic:
                if resultDic['result'].lower() == 'ok':
                    self.log.info('Unlock coupon session on remote server: %s.' % resultDic['zdata'])
                else:
                    self.log.error('Error to unlock coupon session on remote server: %s.' % resultDic['zdata'])
            
        

    
    def validateTrsLimit(self, customer, shoppingCart):
        '''
        @Params: customer (object), shoppingCart (object)
        @Return: status (int)
                 1 - OK
                 2 - Rental Limit Exceed
                 3 - Buy Limit Exceed
                 4 - Both Limit Exceed
                 5 - All Client Kiosks Rental Limit Exceed

        validate coupon user limit from remote server
        '''
        status = 1
        
        try:
            maxDvdOut = int(self._getConfigByKey('max_dvd_out'))
        except:
            maxDvdOut = 3

        
        try:
            buyLimit = int(self._getConfigByKey('buy_limit'))
        except:
            buyLimit = 1

        rentCount = self._getOutDiscCountByCcId(customer.ccid)
        msRentCount = self._getMSOutDiscCountByCcId(customer.ccid)
        saleCount = self._getBuyCountByCcId(customer.ccid)
        shoppingCartRentCount = 0
        shoppingCartSaleCount = 0
        for disc in shoppingCart.discs:
            if disc.gene.lower() == 'rent':
                rentCount += 1
                msRentCount += 1
                shoppingCartRentCount += 1
            else:
                saleCount += 1
                shoppingCartSaleCount += 1
        
        rentalLimitExceed = 0
        buyLimitExceed = 0
        allRentalLimitExceed = 0
        if customer.msCount:
            if customer.msMaxKeepDiscs != 0 and msRentCount > customer.msMaxKeepDiscs:
                rentalLimitExceed = 1
                allRentalLimitExceed = 1
            
            ' remove the client level\n           elif customer.msMaxKeepDiscs != 0:\n               if (not int(customer.isNew)) and                   (not self._checkClientMSDiscOutByCcId(customer.msMaxKeepDiscs, customer.ccid, shoppingCartRentCount)):\n                   allRentalLimitExceed = 1\n           '
        elif maxDvdOut != 0 and rentCount > maxDvdOut:
            rentalLimitExceed = 1
            allRentalLimitExceed = 1
        
        ' remove the client level\n            elif maxDvdOut != 0:\n                if (not int(customer.isNew)) and                    (not self._checkClientDiscOutByCcId(maxDvdOut, customer.ccid, shoppingCartRentCount)):\n                    allRentalLimitExceed = 1\n            '
        if buyLimit != 0 and shoppingCartSaleCount and saleCount > buyLimit:
            buyLimitExceed = 1
        
        if (rentalLimitExceed or allRentalLimitExceed) and buyLimitExceed:
            status = 4
        elif rentalLimitExceed:
            status = 2
        elif allRentalLimitExceed:
            status = 5
        elif buyLimitExceed:
            status = 3
        
        return status

    
    def _checkClientDiscOutByCcId(self, maxDvdOut, ccId, shoppingCartRentCount):
        status = 1
        if not (self.SHOW_MODE):
            funcName = 'checkClientDiscOutByCcId'
            params = { }
            params['max_dvd_out'] = maxDvdOut
            params['cc_id'] = ccId
            params['shopping_cart_rent_count'] = shoppingCartRentCount
            resultDic = self.getRemoteData(funcName, params)
            if str(resultDic.get('result')).lower() == 'ok':
                status = int(resultDic['zdata'])
                self.log.info('_checkClientDiscOutByCcId: ' + str(status))
            else:
                self.log.error('_checkClientDiscOutByCcId: ' + str(resultDic.get('zdata', '')))
        
        return status

    
    def _checkClientMSDiscOutByCcId(self, maxDvdOut, ccId, shoppingCartRentCount):
        status = 1
        if not (self.SHOW_MODE):
            funcName = 'checkClientMSDiscOutByCcId'
            params = { }
            params['max_dvd_out'] = maxDvdOut
            params['cc_id'] = ccId
            params['shopping_cart_rent_count'] = shoppingCartRentCount
            resultDic = self.getRemoteData(funcName, params)
            if str(resultDic.get('result')).lower() == 'ok':
                status = int(resultDic['zdata'])
                self.log.info('_checkClientMSDiscOutByCcId: ' + str(status))
            else:
                self.log.error('_checkClientMSDiscOutByCcId: ' + str(resultDic.get('zdata', '')))
        
        return status

    
    def _getMSOutDiscCountByCcId(self, ccId):
        count = 0
        sql = "SELECT (SELECT COUNT(id) FROM transactions WHERE cc_id=? AND gene='rent' AND upg_id>=0 AND state='open' AND ms_expi_time!='') + (SELECT COUNT(id) FROM reservations WHERE cc_id=? AND state='reserved' AND ms_id!='');"
        row = self.mkcDb.query(sql, 'one', (ccId, ccId))
        if row:
            (count,) = row
        
        return count

    
    def _getOutDiscCountByCcId(self, ccId):
        count = 0
        sql = "SELECT (SELECT COUNT(id) FROM transactions WHERE cc_id=? AND gene='rent' AND upg_id>=0 AND state='open') + (SELECT COUNT(id) FROM reservations WHERE cc_id=? AND state='reserved');"
        row = self.mkcDb.query(sql, 'one', (ccId, ccId))
        if row:
            (count,) = row
        
        return count

    
    def _getBuyCountByCcId(self, ccId):
        count = 0
        sql = "SELECT COUNT(*) FROM transactions WHERE cc_id=? AND gene='sale' AND upg_id>=0 AND DATE(out_time)=?;"
        row = self.mkcDb.query(sql, 'one', (ccId, getCurTime('%Y-%m-%d')))
        if row:
            (count,) = row
        
        return count

    
    def getPriceInfoByRfid(self, rfid):
        '''
        @Params: rfid (string)
        @Return: {"sale_price":XXX, "price_plan":XXX, "price_plan_text":XXX,
                  "sales_tax":XXX, "rentals_tax":XXX, "deposit_amount": XXX,
                  "member_deposit_amount":XXX} (dict)

        get sale price and price plan by rfid
        '''
        rfidInfo = self._getRfidInfoByRfid(rfid)
        blurayUpcs = self._getBlurayUpcs()
        priceInfo = { }
        salesTax = self._getConfigByKey('sales_tax')
        rentalsTax = self._getConfigByKey('rentals_tax')
        preauth_method = 'preauth_method'
        preauth_custom_amount = 'preauth_custom_amount'
        if str(rfidInfo['genre']).lower() in ('games', 'game'):
            preauth_method = 'preauth_method_game'
            preauth_custom_amount = 'preauth_custom_amount_game'
        elif rfidInfo['upc'] in blurayUpcs:
            preauth_method = 'preauth_method_br'
            preauth_custom_amount = 'preauth_custom_amount_br'
        
        preauthMethod = self._getConfigByKey(preauth_method)
        preauthCustomAmount = self._getConfigByKey(preauth_custom_amount)
        memberPreauthMethod = self._getConfigByKey('member_preauth')
        sql = 'SELECT r.sales_price, r.sale_convert_price, p.id, p.data, p.data_text FROM rfids as r, price_plans as p WHERE rfid=? AND r.price_plan_id=p.id;'
        row = self.mkcDb.query(sql, 'one', (rfid,))
        (salePrice, saleConvertPrice, pricePlanId, pricePlan, pricePlanText) = row
        priceInfo['price_plan_id'] = pricePlanId
        priceInfo['sales_tax'] = str(salesTax) + '%'
        priceInfo['rentals_tax'] = str(rentalsTax) + '%'
        priceInfo['sale_price'] = salePrice
        priceInfo['sale_convert_price'] = saleConvertPrice
        priceInfo['price_plan'] = pricePlan
        priceInfo['price_plan_text'] = self._fmt_price_plan_text(pricePlanText)
        categoryInfo = { }
        if str(rfidInfo['category_id']) != '':
            categoryInfo = self._getCategotyById(rfidInfo['category_id'])
        
        if str(categoryInfo.get('sale_price', '')) != '':
            priceInfo['sale_price'] = categoryInfo['sale_price']
        
        if str(categoryInfo.get('sale_convert_price', '')) != '':
            priceInfo['sale_convert_price'] = categoryInfo['sale_convert_price']
        
        if str(categoryInfo.get('price_plan_id', '')) != '':
            priceInfo['price_plan_id'] = categoryInfo['price_plan_id']
            ppInfo = self._getPricePlanById(categoryInfo['price_plan_id'])
            priceInfo['price_plan'] = ppInfo['data']
            priceInfo['price_plan_text'] = ppInfo['data_text']
        elif str(rfidInfo['price_plan_dynamic']) != '0':
            todayPricePlan = self._getTodayPricePlan()
            if str(rfidInfo['genre']).lower() in ('games', 'game'):
                if todayPricePlan['price_plan_game'] and todayPricePlan['price_plan_text_game']:
                    priceInfo['price_plan'] = todayPricePlan['price_plan_game']
                    priceInfo['price_plan_text'] = todayPricePlan['price_plan_text_game']
                
            elif rfidInfo['upc'] in blurayUpcs:
                if todayPricePlan['price_plan_br'] and todayPricePlan['price_plan_text_br']:
                    priceInfo['price_plan'] = todayPricePlan['price_plan_br']
                    priceInfo['price_plan_text'] = todayPricePlan['price_plan_text_br']
                
            elif todayPricePlan['price_plan'] and todayPricePlan['price_plan_text']:
                priceInfo['price_plan'] = todayPricePlan['price_plan']
                priceInfo['price_plan_text'] = todayPricePlan['price_plan_text']
            
        
        if str(preauthMethod).lower() == 'full':
            depositAmount = fmtMoney(float(salePrice) * (1 + float(salesTax) / 100))
        elif str(preauthMethod).lower() == 'partial':
            outTime = getCurTime()
            inTime = getTimeChange(outTime, second = 1)
            ppe = price_coupon_kiosk.PricePlanEngine(pricePlan, {
                'out_time': outTime,
                'in_time': inTime })
            depositAmount = ppe.calculate()
            depositAmount = fmtMoney(float(depositAmount) * (1 + float(rentalsTax) / 100))
        else:
            depositAmount = fmtMoney(preauthCustomAmount)
        priceInfo['deposit_amount'] = depositAmount
        priceInfo['member_deposit_amount'] = priceInfo['deposit_amount']
        if str(memberPreauthMethod).lower() == 'partial':
            outTime = getCurTime()
            inTime = getTimeChange(outTime, second = 1)
            ppe = price_coupon_kiosk.PricePlanEngine(pricePlan, {
                'out_time': outTime,
                'in_time': inTime })
            depositAmount = ppe.calculate()
            depositAmount = fmtMoney(float(depositAmount) * (1 + float(rentalsTax) / 100))
            priceInfo['member_deposit_amount'] = depositAmount
        
        return priceInfo

    
    def _getCategotyById(self, categoryId):
        category = { }
        sql = 'SELECT category_name, sale_price, sale_convert_price, price_plan_id, notes FROM category WHERE id=?;'
        row = self.mkcDb.query(sql, 'one', (categoryId,))
        if row:
            (categoryName, salePrice, saleConvertPrice, pricePlanId, notes) = row
            category['category_name'] = categoryName
            category['sale_price'] = salePrice
            category['sale_convert_price'] = saleConvertPrice
            category['price_plan_id'] = pricePlanId
            category['notes'] = notes
        
        return category

    
    def _getTodayPricePlan(self):
        priceInfo = { }
        weekday = getCurTime('%A')
        sql = 'SELECT price_plan, price_plan_text, price_plan_br, price_plan_text_br, price_plan_game, price_plan_text_game FROM price_plans_week WHERE title LIKE ?;'
        row = self.mkcDb.query(sql, 'one', (weekday,))
        if row:
            (pricePlan, pricePlanText, pricePlanBR, pricePlanTextBR, pricePlanGame, pricePlanTextGame) = row
            priceInfo['price_plan'] = pricePlan
            priceInfo['price_plan_text'] = self._fmt_price_plan_text(pricePlanText)
            priceInfo['price_plan_br'] = pricePlanBR
            priceInfo['price_plan_text_br'] = self._fmt_price_plan_text(pricePlanTextBR)
            priceInfo['price_plan_game'] = pricePlanGame
            priceInfo['price_plan_text_game'] = self._fmt_price_plan_text(pricePlanTextGame)
        
        return priceInfo

    
    def getCOSlotIdByUpcGene(self, upc, gene, geneBy, expressId = '', noOut = False):
        """
        @Params: upc (string),
                 gene: 'rent', 'sale' (string),
                 geneBy: 'express_id', 'title' (string), 'category' (string)
                 expressId: if geneBy='express_id', expressId can NOT be empty (string)
        @Return: slotId (string)

        get check out slotId by upc, gene and geneBy
        """
        slotId = ''
        if noOut:
            state = "('in', 'unload')"
        else:
            state = "('in', 'unload', 'out')"
        if str(gene).lower() == 'sale' and str(geneBy).lower() == 'express_id':
            sql = 'SELECT COUNT(*) FROM slots AS S, rfids AS R WHERE S.rfid=R.rfid AND R.state IN %s AND S.id=?;'
            sql = sql % state
            (exist,) = self.mkcDb.query(sql, 'one', (expressId,))
            if exist:
                slotId = expressId
            
        elif str(geneBy).lower() == 'category':
            sql = "SELECT S.id FROM slots AS S, rfids AS R WHERE S.rfid=R.rfid AND R.upc=? AND R.category_id<>'' AND R.state IN %s ORDER BY S.id DESC LIMIT 1;"
            sql = sql % state
            row = self.mkcDb.query(sql, 'one', (upc,))
            if row:
                (slotId,) = row
            
        
        if not slotId:
            sql = 'SELECT S.id FROM slots AS S, rfids AS R WHERE S.rfid=R.rfid AND R.upc=? AND R.state IN %s ORDER BY S.id DESC LIMIT 1;'
            sql = sql % state
            row = self.mkcDb.query(sql, 'one', (upc,))
            if row:
                (slotId,) = row
            
        
        self.log.info('getCOSlotIdByUpcGene: %s' % slotId)
        return slotId

    
    def _getUpcBySlotId(self, slotId, state):
        '''
        get upc by slotId
        '''
        upc = ''
        sql = "SELECT upc FROM rfids WHERE state IN %s AND rfid=(SELECT rfid FROM slots WHERE id='%s' LIMIT 1);"
        sql = sql % (state, slotId)
        result = self.mkcDb.query(sql, 'one')
        if result:
            (upc,) = result
        
        return upc

    
    def _getRfidBySlotId(self, slotId):
        '''
        get rfid by slotId
        '''
        rfid = ''
        sql = "SELECT rfid FROM slots WHERE id='%s';"
        sql = sql % slotId
        result = self.mkcDb.query(sql, 'one')
        if result:
            (rfid,) = result
        
        return rfid

    
    def getRfidBySlotId(self, slotId):
        '''
        get rfid by slotId
        '''
        return self._getRfidBySlotId(slotId)

    
    def saveTrs(self, shoppingCart, disc, customer):
        '''
        @Params: shoppingCart (object)
                 disc (object)
                 customer (object)
        @Return: None

        if rent:
            update rfid state
        if sale:
            update slots state, delete rfid from rfids table
        '''
        sqlList = []
        shoppingCartId = shoppingCart.id
        trsTime = getCurTime()
        ccId = customer.ccid
        ccDisplay = customer.ccDisplay
        couponCode = shoppingCart.coupon.couponCode
        couponPlan = shoppingCart.coupon.couponData
        couponText = shoppingCart.coupon.shortDes
        self._saveShoppingCart(shoppingCartId, trsTime, ccId, couponCode, couponPlan, couponText)
        rfid = disc.rfid
        gene = str(disc.gene).lower()
        reserveId = disc.reserveID
        amount = disc.preauthAmount
        trsUpgId = disc.upgID
        sql = 'SELECT oid FROM upg WHERE id=?;'
        
        try:
            (trsUpgOid,) = self.mkcDb.query(sql, 'one', (trsUpgId,))
        except:
            trsUpgOid = ''

        if disc.msKeepDays:
            disc.msExpiTime = getTimeChange(trsTime, day = int(disc.msKeepDays))
        
        pricePlanId = disc.pricePlanID
        priceInfo = self._getPricePlanById(pricePlanId)
        pricePlan = priceInfo['data']
        pricePlanDataText = priceInfo['data_text']
        rfidInfo = self._getRfidInfoByRfid(rfid)
        categoryInfo = { }
        if str(rfidInfo['category_id']) != '':
            categoryInfo = self._getCategotyById(rfidInfo['category_id'])
        
        if str(categoryInfo.get('sale_price', '')) != '':
            disc.salePrice = categoryInfo['sale_price']
        
        if str(categoryInfo.get('sale_convert_price', '')) != '':
            disc.saleConvertPrice = categoryInfo['sale_convert_price']
        
        if str(gene).lower() == 'sale':
            tax = disc.saleTax.strip('%')
            salePrice = fmtMoney(float(disc.salePrice) * (1 + float(tax) / 100))
            state = 'pending'
            if str(customer.cardType) == '1':
                state = 'closed'
            
            
            try:
                totalCharged = float(shoppingCart.totalCharged)
            except:
                totalCharged = 0

            totalCharged += float(salePrice)
            shoppingCart.totalCharged = fmtMoney(totalCharged)
        else:
            tax = disc.rentalTax.strip('%')
            salePrice = fmtMoney(float(disc.saleConvertPrice) * (1 + float(disc.saleTax.strip('%')) / 100))
            state = 'open'
        trsCouponCode = disc.coupon.couponCode
        trsCouponPlan = disc.coupon.couponData
        trsCouponText = disc.coupon.shortDes
        slotId = disc.slotID
        upc = disc.upc
        title = disc.title
        genre = disc.genre
        upgAccountId = self._getConfigByKey('upg_acct_id')
        if str(categoryInfo.get('price_plan_id', '')) != '':
            ppInfo = self._getPricePlanById(categoryInfo['price_plan_id'])
            pricePlan = ppInfo['data']
            pricePlanDataText = ppInfo['data_text']
        elif str(rfidInfo['price_plan_dynamic']) != '0':
            todayPricePlan = self._getTodayPricePlan()
            if str(genre).lower() in ('games', 'game'):
                if todayPricePlan['price_plan_game'] and todayPricePlan['price_plan_text_game']:
                    pricePlan = todayPricePlan['price_plan_game']
                    pricePlanDataText = todayPricePlan['price_plan_text_game']
                
            elif disc.isBluray:
                if todayPricePlan['price_plan_br'] and todayPricePlan['price_plan_text_br']:
                    pricePlan = todayPricePlan['price_plan_br']
                    pricePlanDataText = todayPricePlan['price_plan_text_br']
                
            elif todayPricePlan['price_plan'] and todayPricePlan['price_plan_text']:
                pricePlan = todayPricePlan['price_plan']
                pricePlanDataText = todayPricePlan['price_plan_text']
            
        
        if reserveId:
            sql = 'SELECT price_plan, price_plan_text, cc_id, upg_id FROM reservations WHERE id=?;'
            row = self.mkcDb.query(sql, 'one', (reserveId,))
            if row:
                ccId = row[2]
                trsUpgId = row[3]
                if row[0] and row[1]:
                    pricePlan = row[0]
                    pricePlanDataText = row[1]
                
            
            if str(gene).lower() == 'sale':
                amount = salePrice
            
        
        sql = "INSERT INTO transactions(rfid, upc, title, genre, amount, sales_tax, out_time, state, gene, slot_id, cc_id, sale_price, price_plan, price_plan_text, coupon_code, coupon_plan, coupon_text, upg_id, shopping_cart_id, reserve_id, upg_account_id, card_type, ms_expi_time, cc_display, sc_coupon_text, upg_oid) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');"
        sql = sql % (sqlQuote(rfid), sqlQuote(upc), sqlQuote(title), sqlQuote(genre), sqlQuote(amount), sqlQuote(tax), sqlQuote(trsTime), sqlQuote(state), sqlQuote(gene), sqlQuote(slotId), sqlQuote(ccId), sqlQuote(salePrice), sqlQuote(pricePlan), sqlQuote(pricePlanDataText), sqlQuote(trsCouponCode), sqlQuote(trsCouponPlan), sqlQuote(trsCouponText), sqlQuote(trsUpgId), sqlQuote(shoppingCartId), sqlQuote(reserveId), sqlQuote(upgAccountId), sqlQuote(customer.cardType), sqlQuote(disc.msExpiTime), sqlQuote(ccDisplay), sqlQuote(couponText), sqlQuote(trsUpgOid))
        sqlList.append(sql)
        if str(gene).lower() == 'sale':
            sql = "DELETE FROM rfids WHERE rfid='%s';" % sqlQuote(rfid)
            sqlList.append(sql)
            sql = "UPDATE slots SET state='empty', rfid='' WHERE rfid='%s';" % sqlQuote(rfid)
            sqlList.append(sql)
        else:
            sql = "UPDATE rfids SET state='out' WHERE rfid='%s';" % sqlQuote(rfid)
            sqlList.append(sql)
        self.mkcDb.updateTrs(sqlList)
        if str(gene).lower() == 'sale':
            self.checkUPCStock(upc, title)
        
        if str(gene).lower() == 'sale':
            trsInfo = self._getTrsInfoBySaleRfid(rfid)
            disc.trsID = trsInfo['id']
        else:
            trsInfo = self._getTrsInfoByRfidState(rfid, 'open')
            disc.trsID = trsInfo['id']

    
    def _saveShoppingCart(self, shoppingCartId, timeNow, ccId, couponCode, couponPlan, couponText):
        '''
        save shopping cart info
        return shoppingCartId
        '''
        sql = 'SELECT COUNT(*) FROM shopping_carts WHERE id=?;'
        exist = 0
        row = self.mkcDb.query(sql, 'one', (str(shoppingCartId),))
        if row:
            (exist,) = row
        
        if not exist:
            sql = 'INSERT INTO shopping_carts(id, cc_id, time_open, coupon_code, coupon_plan, coupon_text) VALUES(?, ?, ?, ?, ?, ?);'
            params = (str(shoppingCartId), ccId, timeNow, couponCode, couponPlan, couponText)
            self.mkcDb.update(sql, params)
        
        return shoppingCartId

    
    def checkUPCStock(self, upc, title):
        ''' check the stock of the UPC
        
        if the inventory goes to 0, send alert
        @param upc: the disc UPC
        @param title: the disc title
        @return: None
        '''
        
        try:
            sql = 'SELECT COUNT(rfid) FROM rfids WHERE upc=?;'
            exist = 0
            row = self.mkcDb.query(sql, 'one', (upc,))
            if row:
                (exist,) = row
            
            if not exist:
                movie = self._getMovieInfo(upc)
                days = getDaySpan(movie['dvd_release_date'], getCurTime())
                if days <= 60:
                    subject = 'Notification - %s - New Release Stockout' % self.kioskId
                    message = " <p><b> Warning - Out of Stock </b></p>\n<p>You are receiving this email because kiosk <B>%s</B> is stockout of new release title <b>%s</b>.</p>\n<p>This is not an urgent situation but may require a replenishment of the title.</p>\n<p><b>NOTE - This message is just an informational warning, \nit's important to remember that the kiosk is still functioning normally at this time.</b></p>"
                    message = message % (self.kioskId, title)
                    self.emailAlert('CLIENT', message, '', subject, MINICRITICAL)
                    self.log.info('send stockout alert for %s, %s' % (upc, title))
                
        except Exception as ex:
            self.log.error('checkUPCStock: %s' % str(ex))


    
    def getSaleConvertDay(self):
        '''
        @Params: None
        @Return: convertDay (string)
        '''
        convertDay = ''
        saleConvertDays = self._getConfigByKey('sale_convert_days')
        saleConvertDays = int(saleConvertDays)
        if saleConvertDays:
            timeNow = getCurTime()
            convertDay = getTimeChange(timeNow, day = saleConvertDays)
        
        return convertDay

    
    def dbSyncCheckOut(self, shoppingCart):
        '''
        @Params: shoppingCart (object)
        @Return: None

        synchronize the "check out" info to server, save to sync_db
        '''
        shoppingCartInfo = self._getShoppingCartInfoById(str(shoppingCart.id))
        trsInfoList = []
        for disc in shoppingCart.getEjectedDiscs():
            if str(disc.gene).lower() == 'rent':
                trsInfo = self._getTrsInfoByRfidState(disc.rfid, 'open')
            else:
                trsInfo = self._getTrsInfoBySaleRfid(disc.rfid)
            if trsInfo:
                trsInfoList.append(trsInfo)
            
        
        if shoppingCartInfo and trsInfoList:
            params = { }
            params['shopping_cart_info'] = shoppingCartInfo
            params['trs_info_list'] = trsInfoList
            self.syncData('dbSyncCheckOutV6', params)
            self.log.info('Save dbSyncCheckOutV6 to sync db: ' + str(params))
        

    
    def _getShoppingCartInfoById(self, shoppingCartId):
        '''
        get shopping cart info by shoppingCartId
        '''
        shoppingCartInfo = { }
        sql = 'SELECT cc_id, upg_id, time_open, time_close, coupon_code, coupon_plan, coupon_text FROM shopping_carts WHERE id=?;'
        result = self.mkcDb.query(sql, 'one', (shoppingCartId,))
        if result:
            (ccId, upgId, timeOpen, timeClose, couponCode, couponPlan, couponText) = result
            shoppingCartInfo['id'] = shoppingCartId
            shoppingCartInfo['cc_id'] = ccId
            shoppingCartInfo['upg_id'] = upgId
            shoppingCartInfo['time_open'] = timeOpen
            shoppingCartInfo['time_close'] = timeClose
            shoppingCartInfo['coupon_code'] = couponCode
            shoppingCartInfo['coupon_plan'] = couponPlan
            shoppingCartInfo['coupon_text'] = couponText
        
        return shoppingCartInfo

    
    def _getTrsInfoById(self, trsId):
        '''
        get transaction info by trsId
        '''
        trsInfo = { }
        sql = 'SELECT rfid, upc, title, genre, amount, sales_tax, out_time, in_time, notes, state, gene, cc_id, sale_price, price_plan, coupon_code, coupon_plan, coupon_usage_state, upg_id, shopping_cart_id, reserve_id, slot_id, in_kiosk, price_plan_text, upg_account_id, coupon_text, card_type, ms_expi_time, cc_display, sc_coupon_text, upg_oid FROM transactions WHERE id=?;'
        result = self.mkcDb.query(sql, 'one', (trsId,))
        if result:
            trsInfo['id'] = trsId
            trsInfo['rfid'] = result[0]
            trsInfo['upc'] = result[1]
            trsInfo['title'] = result[2]
            trsInfo['genre'] = result[3]
            trsInfo['amount'] = result[4]
            trsInfo['sales_tax'] = result[5]
            trsInfo['out_time'] = result[6]
            trsInfo['in_time'] = result[7]
            trsInfo['notes'] = result[8]
            trsInfo['state'] = result[9]
            trsInfo['gene'] = result[10]
            trsInfo['cc_id'] = result[11]
            trsInfo['sale_price'] = result[12]
            trsInfo['price_plan'] = result[13]
            trsInfo['coupon_code'] = result[14]
            trsInfo['coupon_plan'] = result[15]
            trsInfo['coupon_usage_state'] = result[16]
            trsInfo['upg_id'] = result[17]
            trsInfo['shopping_cart_id'] = result[18]
            trsInfo['reserve_id'] = result[19]
            trsInfo['slot_id'] = result[20]
            trsInfo['in_kiosk'] = result[21]
            trsInfo['price_plan_text'] = result[22]
            trsInfo['upg_account_id'] = result[23]
            trsInfo['coupon_text'] = result[24]
            trsInfo['card_type'] = result[25]
            trsInfo['ms_expi_time'] = result[26]
            trsInfo['cc_display'] = result[27]
            trsInfo['sc_coupon_text'] = result[28]
            trsInfo['upg_oid'] = result[29]
        
        return trsInfo

    
    def _getTrsInfoByRfidState(self, rfid, state):
        '''
        get transaction info by rfid and state
        '''
        trsInfo = { }
        sql = 'SELECT id, rfid, upc, title, genre, amount, sales_tax, out_time, in_time, notes, state, gene, cc_id, sale_price, price_plan, coupon_code, coupon_plan, coupon_usage_state, upg_id, shopping_cart_id, reserve_id, slot_id, in_kiosk, price_plan_text, upg_account_id, coupon_text, card_type, ms_expi_time, cc_display, sc_coupon_text, upg_oid FROM transactions WHERE rfid=? and state=? ORDER BY id DESC LIMIT 1;'
        result = self.mkcDb.query(sql, 'one', (rfid, state))
        if result:
            trsInfo['id'] = result[0]
            trsInfo['rfid'] = result[1]
            trsInfo['upc'] = result[2]
            trsInfo['title'] = result[3]
            trsInfo['genre'] = result[4]
            trsInfo['amount'] = result[5]
            trsInfo['sales_tax'] = result[6]
            trsInfo['out_time'] = result[7]
            trsInfo['in_time'] = result[8]
            trsInfo['notes'] = result[9]
            trsInfo['state'] = result[10]
            trsInfo['gene'] = result[11]
            trsInfo['cc_id'] = result[12]
            trsInfo['sale_price'] = result[13]
            trsInfo['price_plan'] = result[14]
            trsInfo['coupon_code'] = result[15]
            trsInfo['coupon_plan'] = result[16]
            trsInfo['coupon_usage_state'] = result[17]
            trsInfo['upg_id'] = result[18]
            trsInfo['shopping_cart_id'] = result[19]
            trsInfo['reserve_id'] = result[20]
            trsInfo['slot_id'] = result[21]
            trsInfo['in_kiosk'] = result[22]
            trsInfo['price_plan_text'] = result[23]
            trsInfo['upg_account_id'] = result[24]
            trsInfo['coupon_text'] = result[25]
            trsInfo['card_type'] = result[26]
            trsInfo['ms_expi_time'] = result[27]
            trsInfo['cc_display'] = result[28]
            trsInfo['sc_coupon_text'] = result[29]
            trsInfo['upg_oid'] = result[30]
        
        return trsInfo

    
    def _getTrsInfoBySaleRfid(self, rfid):
        '''
        get transaction info by sale rfid
        '''
        trsInfo = { }
        sql = "SELECT id, rfid, upc, title, genre, amount, sales_tax, out_time, in_time, notes, state, gene, cc_id, sale_price, price_plan, coupon_code, coupon_plan, coupon_usage_state, upg_id, shopping_cart_id, reserve_id, slot_id, in_kiosk, price_plan_text, upg_account_id, coupon_text, card_type, ms_expi_time, cc_display, sc_coupon_text, upg_oid FROM transactions WHERE rfid=? and gene='sale' ORDER BY id DESC LIMIT 1;"
        result = self.mkcDb.query(sql, 'one', (rfid,))
        if result:
            trsInfo['id'] = result[0]
            trsInfo['rfid'] = result[1]
            trsInfo['upc'] = result[2]
            trsInfo['title'] = result[3]
            trsInfo['genre'] = result[4]
            trsInfo['amount'] = result[5]
            trsInfo['sales_tax'] = result[6]
            trsInfo['out_time'] = result[7]
            trsInfo['in_time'] = result[8]
            trsInfo['notes'] = result[9]
            trsInfo['state'] = result[10]
            trsInfo['gene'] = result[11]
            trsInfo['cc_id'] = result[12]
            trsInfo['sale_price'] = result[13]
            trsInfo['price_plan'] = result[14]
            trsInfo['coupon_code'] = result[15]
            trsInfo['coupon_plan'] = result[16]
            trsInfo['coupon_usage_state'] = result[17]
            trsInfo['upg_id'] = result[18]
            trsInfo['shopping_cart_id'] = result[19]
            trsInfo['reserve_id'] = result[20]
            trsInfo['slot_id'] = result[21]
            trsInfo['in_kiosk'] = result[22]
            trsInfo['price_plan_text'] = result[23]
            trsInfo['upg_account_id'] = result[24]
            trsInfo['coupon_text'] = result[25]
            trsInfo['card_type'] = result[26]
            trsInfo['ms_expi_time'] = result[27]
            trsInfo['cc_display'] = result[28]
            trsInfo['sc_coupon_text'] = result[29]
            trsInfo['upg_oid'] = result[30]
        
        return trsInfo

    
    def getOutDiscsByCode(self, code):
        '''
        @Params: code (string)
        @Return: [Disc(), Disc()] (a blank list if no match)
        '''
        outDiscs = []
        self.log.info('Out Discs, code: %s' % code)
        sql = "SELECT R.rfid, R.upc, R.title, R.movie_id, R.genre, T.out_time, T.cc_display FROM rfids AS R, transactions AS T WHERE R.rfid=T.rfid AND T.state='open' AND T.cc_id IN (SELECT id FROM cc WHERE display LIKE ?);"
        rows = self.mkcDb.query(sql, params = ('%' + str(code) + ')',))
        self.log.info('Out Discs, count: %s' % len(rows))
        if rows:
            for row in rows:
                (rfid, upc, title, movieId, genre, outTime, cc_display) = row
                picName = self._formPicName(movieId)
                disc = Disc()
                disc.rfid = rfid
                disc.upc = upc
                disc.title = title
                disc.picture = picName
                disc.genre = genre
                disc.outTime = outTime
                disc.cc_display = cc_display
                outDiscs.append(disc)
            
        
        return outDiscs

    
    def getOutDiscsByCcId(self, ccId):
        '''
        @Params: ccId (string)
        @Return: [Disc(), Disc()] (a blank list if no match)
        '''
        outDiscs = []
        self.log.info('Out Discs, ccId: %s' % ccId)
        sql = "SELECT R.rfid, R.upc, R.title, R.movie_id, R.genre, T.out_time FROM rfids AS R, transactions AS T WHERE R.rfid=T.rfid AND T.state='open' AND T.cc_id=?;"
        rows = self.mkcDb.query(sql, params = (ccId,))
        self.log.info('Out Discs, count: %s' % len(rows))
        if rows:
            for row in rows:
                (rfid, upc, title, movieId, genre, outTime) = row
                picName = self._formPicName(movieId)
                disc = Disc()
                disc.rfid = rfid
                disc.upc = upc
                disc.title = title
                disc.picture = picName
                disc.genre = genre
                disc.outTime = outTime
                outDiscs.append(disc)
            
        
        return outDiscs

    
    def _getPhysicalEmptySlots(self):
        emptySlotsCount = self.getSlotsCountByState('empty')
        outSlotsCount = 0
        sql = "SELECT COUNT(S.id) FROM slots AS S, rfids AS R WHERE S.rfid=R.rfid AND R.state='out';"
        row = self.mkcDb.query(sql, 'one')
        if row:
            (outSlotsCount,) = row
        
        return int(emptySlotsCount) + int(outSlotsCount)

    
    def checkRfidAndSaveTrs(self, disc, shoppingCart):
        '''
        @Params: disc (object)
        @Return: statusCode: 0: can not return (invalid)
                             1: can return (from this kiosk)
                             2: can return (from another kiosk)
                             3: can not return (no empty slots)
                             4: already existing (with open transaction)
                             5: already existing (without open transaction)
                             6: purchased disc
                             7: convert to sale right now (local)
                             8: convert to sale right now (remote)
                             9: return and load
                             10: disc remembered as unloaded
                             11: manually cleared
                             12: can not return (from another client)
                             13: can not return (250 & 500)

        get return status code by rfid
        '''
        
        try:
            sql = "UPDATE rfids SET state=substr(state, 0, length(state)-8) WHERE state LIKE '%_pending';"
            self.mkcDb.update(sql)
        except:
            pass

        statusCode = 0
        rfid = disc.rfid
        rfidInfo = self._getRfidInfoByRfid(rfid)
        disc.upc = rfidInfo.get('upc', '')
        disc.gene = 'rent'
        discState = self._getDiscState(rfid)
        if discState.lower() == 'out':
            if not (self._getPhysicalEmptySlots() > 0):
                statusCode = 3
            else:
                statusCode = 1
                disc.outKioskID = self.kioskId
                slotId = self.getAvailableReturnSlotId(rfid)
                disc.slotID = slotId
                self._calculatePrice(disc, shoppingCart)
                if self._checkConvertToSale(disc):
                    statusCode = 7
                
                self._updateReturnInfo(disc)
                self._update_disc_info_by_trs_info(disc, self._getTrsInfoById(disc.trsID))
        elif discState.lower() in [
            'in',
            'unload',
            'reserved',
            'bad']:
            exist = 0
            sql = "SELECT COUNT(id) FROM TRANSACTIONS WHERE rfid=? AND state='open';"
            row = self.mkcDb.query(sql, 'one', (rfid,))
            if row:
                (exist,) = row
            
            if exist:
                if not (self._getPhysicalEmptySlots() > 0):
                    statusCode = 3
                else:
                    statusCode = 4
                    disc.outKioskID = self.kioskId
                    slotId = self.getAvailableReturnSlotId(rfid)
                    disc.slotID = slotId
                    self._calculatePrice(disc, shoppingCart)
                    if self._checkConvertToSale(disc):
                        statusCode = 7
                    
                    self._updateReturnInfo(disc)
                    self._update_disc_info_by_trs_info(disc, self._getTrsInfoById(disc.trsID))
            else:
                statusCode = 5
                disc.slotID = self.getSlotIdByRfid(rfid)
                sql = 'SELECT title FROM rfids WHERE rfid=?;'
                row = self.mkcDb.query(sql, 'one', (rfid,))
                if row:
                    (disc.title,) = row
                
        else:
            gene = ''
            state = ''
            sql = 'SELECT gene, state FROM transactions WHERE rfid=? ORDER BY id DESC;'
            row = self.mkcDb.query(sql, 'one', (rfid,))
            if row:
                (gene, state) = row
            
            if gene.lower() == 'sale':
                statusCode = 6
                disc.outKioskID = self.kioskId
            elif state.lower() == 'open':
                if not (self._getPhysicalEmptySlots() > 0):
                    statusCode = 3
                else:
                    statusCode = 9
                    disc.outKioskID = self.kioskId
                    trsInfo = self._getTrsInfoByRfidState(rfid, 'open')
                    disc.upc = trsInfo['upc']
                    movieInfo = self._getMovieInfo(disc.upc)
                    disc.movieID = movieInfo['movie_id']
                    disc.title = movieInfo['movie_title']
                    disc.genre = movieInfo['genre']
                    self.getDefaultSettings(disc)
                    if disc.slotID:
                        self._calculatePrice(disc, shoppingCart)
                        if self._checkConvertToSale(disc):
                            statusCode = 7
                        
                        self._updateReturnInfo(disc)
                        self._update_disc_info_by_trs_info(disc, self._getTrsInfoById(disc.trsID))
                    else:
                        statusCode = 3
            else:
                emptySlotsCount = self.getSlotsCountByState('empty')
                outSlotsCount = 0
                sql = "SELECT COUNT(S.id) FROM slots AS S, rfids AS R WHERE S.rfid=R.rfid AND R.state='out';"
                row = self.mkcDb.query(sql, 'one')
                if row:
                    (outSlotsCount,) = row
                
                if emptySlotsCount and outSlotsCount and self._checkOverCapacityCount():
                    if not (self.SHOW_MODE):
                        funcName = 'getKioskByInKioskRfidV2'
                        params = { }
                        params['rfid'] = rfid
                        params['inKioskId'] = self.kioskId
                        resultDic = self.getRemoteData(funcName, params)
                        if resultDic.get('result', '').lower() == 'ok':
                            data = resultDic['zdata']
                            if str(data.get('status', '')) == '3':
                                statusCode = 13
                            elif str(data.get('status', '')) == '2':
                                disc.outAddress = str(data['out_location'], 'utf8')
                                statusCode = 12
                            elif str(data.get('status', '')) == '1':
                                disc.outKioskID = data['out_kiosk_id']
                                priceInfo = self.getRetrunToAnotherPrice(rfid, disc.outKioskID)
                                if priceInfo:
                                    disc.trsID = priceInfo['trs_info']['id']
                                    disc.rentalPrice = priceInfo['trs_info']['amount']
                                    disc.upc = priceInfo['trs_info']['upc']
                                    disc.movieID = priceInfo['trs_info']['movie_id']
                                    disc.title = priceInfo['trs_info']['title']
                                    disc.genre = priceInfo['trs_info']['genre']
                                    disc.msExpiTime = priceInfo['trs_info']['ms_expi_time']
                                    self.getDefaultSettings(disc)
                                    disc.pricePlan = priceInfo['trs_info']['price_plan_text']
                                    disc.pricePlanContent = priceInfo['trs_info']['price_plan']
                                    disc.outTime = priceInfo['trs_info']['out_time']
                                    disc.salePrice = priceInfo['trs_info']['sale_price']
                                    disc.rentalTax = priceInfo['trs_info']['sales_tax']
                                    if str(priceInfo['status']) in ('1', '3'):
                                        statusCode = 2
                                        if str(priceInfo['status']) == '3':
                                            disc.isGracePeriod = 1
                                        
                                    elif str(priceInfo['status']) == '2':
                                        statusCode = 8
                                    
                                
                            else:
                                sql = "SELECT action FROM events WHERE action IN ('unload', 'clear') AND data2=? AND (data5='' OR data5 IS NULL);"
                                action = ''
                                row = self.mkcDb.query(sql, 'one', (rfid,))
                                if row:
                                    (action,) = row
                                
                                if action == 'unload':
                                    statusCode = 10
                                    disc.outKioskID = self.kioskId
                                elif action == 'clear':
                                    statusCode = 11
                                    disc.outKioskID = self.kioskId
                                
                        else:
                            self.log.error('getReturnState (remote): ' + str(resultDic.get('zdata', '')))
                    
                else:
                    statusCode = 3
        self.log.info('return: %s, %s' % (statusCode, rfid))
        return statusCode

    
    def _update_disc_info_by_trs_info(self, disc, trs_info):
        '''
        @param disc(object): the disc object you want to update
        @param trs_info(dict): the transaction info
        @return: None
        '''
        disc.trsID = trs_info.get('id', '')
        disc.upc = trs_info.get('upc', '')
        disc.title = trs_info.get('title', '')
        disc.genre = trs_info.get('genre', '')
        disc.rentalTax = trs_info.get('sales_tax', '')
        disc.outTime = trs_info.get('out_time', '')
        disc.salePrice = trs_info.get('sale_price', '')
        disc.pricePlan = trs_info.get('price_plan_text', '')
        disc.pricePlanContent = trs_info.get('price_plan', '')
        disc.rentalPrice = trs_info.get('amount', 0)

    
    def checkRentalPurchaseConfirm(self, disc, statusCode):
        '''
        @Params: disc(object), statusCode(int)
        @Return: status(int), amount(float), trsId(int), ccId(int), accountId(string)
                 status: 0 -> not prompt
                         1 -> prompt

        check if prompt the Rental-Purchase confirmation
            statusCode(only):
            1: can return (from this kiosk)
            2: can return (from another kiosk)
            4: already existing (with open transaction)
            9: return and load

            credit card only(card_type == 0)
        '''
        status = 0
        amount = 0
        trsId = 0
        ccId = 0
        accountId = ''
        if str(statusCode) in ('1', '2', '4', '9'):
            if int(statusCode) == 2:
                funcName = 'checkRentalPurchaseConfirmOutKiosk'
                params = { }
                params['rfid'] = disc.rfid
                params['trs_id'] = disc.trsID
                params['rental_price'] = disc.rentalPrice
                params['out_kiosk_id'] = disc.outKioskID
                resultDic = self.getRemoteData(funcName, params)
                if resultDic.get('result', '').lower() == 'ok':
                    data = resultDic['zdata']
                    trsId = disc.trsID
                    status = data['status']
                    amount = data['amount']
                    ccId = data['cc_id']
                    accountId = data['upg_account_id']
                
            else:
                trsInfo = self._getTrsInfoById(disc.trsID)
                if str(trsInfo['card_type']) == '0':
                    allowRentalPurchase = self._getConfigByKey('allow_rental_purchase')
                    
                    try:
                        allowRentalPurchase = int(allowRentalPurchase)
                    except:
                        allowRentalPurchase = 100

                    if allowRentalPurchase != 100:
                        rfidInfo = self._getRfidInfoByRfid(disc.rfid)
                        salePrice = rfidInfo.get('sales_price', 0)
                        saleTax = self._getConfigByKey('sales_tax')
                        amount = float(salePrice) * (1 + float(saleTax) / 100)
                        if amount and float(disc.rentalPrice) / amount > allowRentalPurchase / 100:
                            status = 1
                            trsId = disc.trsID
                            ccId = trsInfo['cc_id']
                            accountId = trsInfo['upg_account_id']
                        
                    
                
        
        return (status, amount, trsId, ccId, accountId)

    
    def saveRentalPurchaseStatus(self, disc, statusCode, amount):
        '''
        @Params: disc(object), statusCode(int), amount(float)
        @Return: None

        save the Rental-Purchase status
        '''
        self.log.info('saveRentalPurchaseStatus: %s, %s, %s' % (disc.rfid, statusCode, amount))
        if int(statusCode) == 2:
            funcName = 'dbSyncRentalPurchaseRemotely'
            params = { }
            params['out_kiosk_id'] = disc.outKioskID
            params['rfid'] = disc.rfid
            params['trs_id'] = disc.trsID
            params['amount'] = amount
            self.syncDataRemoteKiosk(disc.outKioskID, funcName, params)
        else:
            sqlList = []
            amount = fmtMoney(amount)
            saleTax = self._getConfigByKey('sales_tax')
            sql = "UPDATE transactions SET amount='%s', sales_tax='%s', gene='sale', state='closed' WHERE id='%s';"
            sqlList.append(sql % (amount, saleTax, disc.trsID))
            sql = "DELETE FROM rfids WHERE rfid='%s';"
            sqlList.append(sql % disc.rfid)
            sql = "DELETE FROM over_capacity_rfids WHERE rfid='%s';"
            sqlList.append(sql % disc.rfid)
            sql = "UPDATE slots SET rfid='', state='empty' WHERE rfid='%s';"
            sqlList.append(sql % disc.rfid)
            self.mkcDb.updateTrs(sqlList)
            funcName = 'dbSyncRentalPurchaseLocally'
            params = { }
            params['rfid'] = disc.rfid
            params['trs_id'] = disc.trsID
            params['amount'] = amount
            params['sale_tax'] = saleTax
            self.syncData(funcName, params)

    
    def save_rental_movie_out_status(self, disc, status_code):
        '''
        @Params: disc(object), status_code(str)
        @Return: None

        save the rental movie out status
        '''
        self.log.info('save_rental_movie_out_status: %s, %s, %s' % (disc.rfid, status_code, disc.rentalPrice))
        if str(status_code) in ('2', '8'):
            funcName = 'dbSyncRentalMovieOutRemotely'
            params = { }
            params['out_kiosk_id'] = disc.outKioskID
            params['rfid'] = disc.rfid
            params['trs_id'] = disc.trsID
            params['amount'] = disc.rentalPrice
            params['in_time'] = disc.inTime
            params['gene'] = 'rent'
            params['sales_tax'] = disc.rentalTax
            self.syncDataRemoteKiosk(disc.outKioskID, funcName, params)
        else:
            amount = fmtMoney(disc.rentalPrice)
            sql = "UPDATE transactions SET amount='%s', sales_tax='%s', gene='rent', state='pending', in_time='%s' WHERE id='%s';"
            sql = sql % (amount, disc.rentalTax, disc.inTime, disc.trsID)
            self.mkcDb.update(sql)
            funcName = 'dbSyncRentalMovieOutLocally'
            params = { }
            params['rfid'] = disc.rfid
            params['trs_id'] = disc.trsID
            params['amount'] = amount
            params['sale_tax'] = disc.rentalTax
            params['in_time'] = disc.inTime
            params['gene'] = 'rent'
            self.syncData(funcName, params)

    
    def getAvailableReturnSlotId(self, rfid):
        '''
        @Params: rfid (string)
        @Return: slotId (string)

        get the return slotId,
        get slotId from remote server recommended,
        if None, get from local db
        '''
        slotId = ''
        returnSlot = self._getConfigByKey('return_slot')
        if str(returnSlot).lower() == 'original':
            slotId = self._getSlotIdByRfid(rfid)
            if slotId == OVER_CAPACITY:
                slotId = ''
            
        
        upc = ''
        sql = 'SELECT upc FROM rfids WHERE rfid=?;'
        row = self.mkcDb.query(sql, 'one', (rfid,))
        if row:
            (upc,) = row
        
        sql = "SELECT COUNT(*) FROM slots AS S, rfids AS R WHERE S.rfid=R.rfid AND R.upc=? AND S.id<500 AND R.state='in';"
        (exist,) = self.mkcDb.query(sql, 'one', (upc,))
        if not slotId:
            if exist:
                sql = "SELECT MAX(id) FROM slots WHERE state='empty' OR (state='occupied' AND rfid=?);"
            else:
                sql = "SELECT MIN(id) FROM slots WHERE state='empty' OR (state='occupied' AND rfid=?);"
            row = self.mkcDb.query(sql, 'one', (rfid,))
            if row:
                (slotId,) = row
            
        
        if not slotId:
            if exist:
                sql = "SELECT MAX(S.id) FROM slots AS S, rfids AS R WHERE S.rfid=R.rfid AND R.state='out';"
            else:
                sql = "SELECT MIN(S.id) FROM slots AS S, rfids AS R WHERE S.rfid=R.rfid AND R.state='out';"
            row = self.mkcDb.query(sql, 'one')
            if row:
                (slotId,) = row
            
        
        slotId = str(slotId)
        return slotId

    
    def getRetrunToAnotherPrice(self, rfid, outKioskId):
        '''
        @Params: rfid (string), outKioskId (string)
        @Return: {"status":XXX (int), "trs_info":XXX (disc)}
                 status: 0: can not return
                         1: normal rent
                         2: rent to sale
                         3: grace period

        get return status code by rfid
        '''
        priceInfo = { }
        if not (self.SHOW_MODE):
            funcName = 'getReturnTrsInfoV3'
            params = { }
            params['rfid'] = rfid
            params['out_kiosk_id'] = outKioskId
            resultDic = self.getRemoteData(funcName, params)
            if resultDic:
                if resultDic['result'].lower() == 'ok':
                    data = resultDic['zdata']
                    self.log.info('getRetrunToAnotherPrice(remote): ' + str(data))
                    if data:
                        priceInfo = data
                        funcName = 'dbSyncReturnToAnother'
                        params = { }
                        params['out_kiosk_id'] = outKioskId
                        params['trs_info'] = data['trs_info']
                        params['already_in_list'] = data['already_in_list']
                        syncId = self.syncDataRemoteKiosk(outKioskId, funcName, params)
                        self.log.info('getRetrunToAnotherPrice(sync): %s' % syncId)
                    
                else:
                    self.log.error('getRetrunToAnotherPrice error: ' + str(resultDic['zdata']))
            
        
        return priceInfo

    
    def _calculatePrice(self, disc, cart):
        '''
        @Params: disc (object), shoppingCart (object)
        @Return: None

        calculate price
        '''
        price = 0
        trsInfoList = { }
        priceInfo = { }
        timeNow = getCurTime()
        disc.inTime = timeNow
        rfidList = self._getSameShrtTrsRfids(disc.rfid)
        shcrtId = ''
        shoppingCart = { }
        shoppingCart['transactions'] = []
        for trsId, rfid in rfidList:
            trsInfo = self._getTrsInfoById(trsId)
            if rfid == disc.rfid:
                trsInfo['in_time'] = timeNow
            
            if trsInfo['ms_expi_time'] and trsInfo['ms_expi_time'] < trsInfo['in_time']:
                trsInfo['out_time'] = trsInfo['ms_expi_time']
            
            shcrtId = trsInfo['shopping_cart_id']
            shoppingCart['transactions'].append(trsInfo)
            trsInfoList[rfid] = trsInfo
        
        shcrtInfo = self._getShoppingCartInfoById(shcrtId)
        cart.coupon.couponCode = shcrtInfo['coupon_code']
        couponCode = shcrtInfo['coupon_code']
        couponPlan = shcrtInfo['coupon_plan']
        shoppingCart['coupon_plan'] = couponPlan
        params = {
            'shopping_cart': shoppingCart }
        priceInfo = price_coupon_kiosk.calculatePrice(params)
        cart.couponUsed = int(priceInfo['shopping_cart_coupon_used'])
        self.log.info('price info for shopping cart id %s: %s' % (shcrtId, priceInfo))
        gracePeriod = self._getConfigByKey('grace_period')
        
        try:
            gracePeriod = int(gracePeriod)
        except:
            gracePeriod = 0

        for trsId, rfid in rfidList:
            rentalsTax = trsInfoList[rfid]['sales_tax']
            amount = float(fmtMoney(float(priceInfo[rfid]['price']) * (1 + float(rentalsTax) / 100)))
            if amount >= float(trsInfoList[rfid]['sale_price']):
                amount = trsInfoList[rfid]['sale_price']
            
            self.log.info('amount for rfid(%s) is: %s' % (rfid, amount))
            if rfid == disc.rfid:
                disc.trsID = trsId
                disc.rentalPrice = fmtMoney(amount)
                disc.couponUsed = priceInfo[rfid]['coupon_used']
                spanMinutes = getMinuteSpan(trsInfoList[rfid]['out_time'], disc.inTime)
                if int(spanMinutes) < int(gracePeriod):
                    disc.rentalPrice = fmtMoney(0)
                    disc.couponUsed = 0
                    disc.isGracePeriod = 1
                
                if trsInfoList[rfid]['ms_expi_time'] and trsInfoList[rfid]['ms_expi_time'] >= trsInfoList[rfid]['in_time']:
                    disc.rentalPrice = fmtMoney(0)
                    disc.couponUsed = 0
                    disc.msExpiTime = trsInfoList[rfid]['ms_expi_time']
                else:
                    disc.msExpiTime = ''
            else:
                spanMinutes = getMinuteSpan(trsInfoList[rfid]['out_time'], trsInfoList[rfid]['in_time'])
                if int(spanMinutes) < int(gracePeriod):
                    amount = fmtMoney(0)
                    priceInfo[rfid]['coupon_used'] = 0
                
                if trsInfoList[rfid]['ms_expi_time'] and trsInfoList[rfid]['ms_expi_time'] >= trsInfoList[rfid]['in_time']:
                    amount = fmtMoney(0)
                    priceInfo[rfid]['coupon_used'] = 0
                
                sql = 'UPDATE transactions SET amount=?, coupon_usage_state=? WHERE id=?;'
                self.mkcDb.update(sql, (amount, priceInfo[rfid]['coupon_used'], trsInfoList[rfid]['id']))
                params = { }
                params['changes'] = {
                    'amount': amount,
                    'coupon_usage_state': priceInfo[rfid]['coupon_used'] }
                params['trs_list'] = [
                    trsInfoList[rfid]['id']]
                self.syncData('dbSyncPostauth', params)
                self.log.info('Save dbSyncPostauth to sync db: ' + str(params))
        
        self.log.info('_calculatePrice(%s): %s' % (rfid, disc.rentalPrice))

    
    def calculate_price_without_coupon(self, disc):
        '''
        @param disc(object): the disc object
        '''
        if not (disc.inTime):
            disc.inTime = getCurTime()
        
        ppe = price_coupon_kiosk.PricePlanEngine(disc.pricePlanContent, {
            'in_time': disc.inTime,
            'out_time': disc.outTime })
        fee = ppe.calculate()
        fee = fmtMoney(fee * (1 + float(disc.rentalTax) / 100))
        sale_price = fmtMoney(disc.salePrice)
        if float(fee) > float(sale_price):
            fee = sale_price
        
        disc.rentalPrice = fee

    
    def _getSameShrtTrsRfids(self, rfid):
        '''
        get same shopping cart transactions rfids list
        '''
        rfidList = []
        sql = "SELECT id, rfid FROM transactions WHERE shopping_cart_id=(SELECT shopping_cart_id FROM transactions WHERE rfid=? AND state='open' LIMIT 1) AND state='pending' AND gene='rent' ORDER BY in_time;"
        rfidList = self.mkcDb.query(sql, 'all', (rfid,))
        sql = "SELECT id, rfid FROM transactions WHERE rfid=? AND state='open' ORDER BY id DESC;"
        rfidList.append(self.mkcDb.query(sql, 'one', (rfid,)))
        return rfidList

    
    def _checkConvertToSale(self, disc):
        '''
        @Params: disc (object)
        @Return: True or False

        check automatic rent to sale
        '''
        result = False
        saleConvertDays = self._getConfigByKey('sale_convert_days')
        saleConvertDays = int(saleConvertDays)
        timeNow = getCurTime()
        trsInfo = self._getTrsInfoByRfidState(disc.rfid, 'open')
        if trsInfo['ms_expi_time'] and trsInfo['ms_expi_time'] < disc.inTime:
            trsInfo['out_time'] = trsInfo['ms_expi_time']
        
        salePrice = float(trsInfo['sale_price'])
        if int(saleConvertDays) > 0:
            dvdTimeOut = trsInfo['out_time']
            days = getDaySpan(dvdTimeOut, timeNow)
            if days >= saleConvertDays:
                result = True
                disc.rentalPrice = salePrice
                disc.gene = 'sale'
            
        else:
            amount = float(disc.rentalPrice)
            if amount >= salePrice:
                result = True
                disc.rentalPrice = salePrice
                disc.gene = 'sale'
            
        self.log.info('_checkConvertToSale(%s): %s' % (disc.rfid, result))
        return result

    
    def _updateReturnInfo(self, disc):
        '''
        @Params: disc (object)
        @Return: None

        update the return info
        '''
        sqlList = []
        rfid = disc.rfid
        slotId = disc.slotID
        gene = str(disc.gene).lower()
        amount = disc.rentalPrice
        inTime = disc.inTime
        couponUsed = disc.couponUsed
        saleTax = self._getConfigByKey('sales_tax')
        trsInfo = self._getTrsInfoByRfidState(rfid, 'open')
        trsId = trsInfo['id']
        disc.trsID = trsId
        salePrice = trsInfo['sale_price']
        tax = trsInfo['sales_tax']
        originalSlotId = self._getSlotIdByRfid(rfid)
        if str(gene).lower() == 'sale':
            sql = "UPDATE slots SET state='empty', rfid='' WHERE rfid='%s';" % sqlQuote(rfid)
            sqlList.append(sql)
            sql = "DELETE FROM rfids WHERE rfid='%s';" % sqlQuote(rfid)
            sqlList.append(sql)
        else:
            sql = "UPDATE rfids SET state='in' WHERE rfid='%s';" % sqlQuote(rfid)
            sqlList.append(sql)
            if str(slotId) != str(originalSlotId) and originalSlotId != OVER_CAPACITY:
                sql = "UPDATE slots SET rfid='', state='empty' WHERE id='%s' AND rfid='%s';"
                sql = sql % (sqlQuote(originalSlotId), sqlQuote(rfid))
                sqlList.append(sql)
            
            slotInfo = self._getSlotInfoBySlotId(slotId)
            if slotInfo.get('rfid') and slotInfo.get('rfid', '') != rfid:
                sql = "INSERT INTO over_capacity_rfids(rfid, add_time) VALUES('%s', '%s');"
                sql = sql % (sqlQuote(slotInfo['rfid']), sqlQuote(inTime))
                sqlList.append(sql)
            
            sql = "UPDATE slots SET rfid='%s', state='occupied' WHERE id='%s';"
            sql = sql % (sqlQuote(rfid), sqlQuote(slotId))
            sqlList.append(sql)
        if originalSlotId == OVER_CAPACITY:
            sql = "DELETE FROM over_capacity_rfids WHERE rfid='%s';" % sqlQuote(rfid)
            sqlList.append(sql)
        
        if float(salePrice) == float(amount):
            tax = saleTax
        
        state = 'pending'
        if str(trsInfo['upg_id']) == '-1':
            state = 'closed'
        
        sql = "UPDATE transactions SET gene='%s', state='%s', sales_tax='%s', amount='%s', coupon_usage_state='%s', in_time='%s', in_kiosk='%s' WHERE id='%s';"
        sql = sql % (gene, state, tax, amount, couponUsed, inTime, self.kioskId, trsId)
        sqlList.append(sql)
        self.mkcDb.updateTrs(sqlList)
        trsInfoList = []
        trsInfo = self._getTrsInfoById(trsId)
        trsInfoList.append(trsInfo)
        newShoppingCart = []
        newShoppingCart.append({
            'rfid': rfid,
            'slot_id': slotId })
        params = { }
        params['shopping_cart'] = newShoppingCart
        params['trs_info_list'] = trsInfoList
        params['original_slot_id'] = originalSlotId
        self.syncData('dbSyncReturnV2', params)
        self.log.info('Save dbSyncReturnV2 to sync db: ' + str(params))
        self._checkShoppingCartClosed(trsInfo['shopping_cart_id'], trsInfo['in_time'])

    
    def _checkShoppingCartClosed(self, cartId, timeClose):
        '''
        check if the shopping cart closed
        '''
        exist = 0
        sql = "SELECT COUNT(*) FROM transactions WHERE state='open' AND shopping_cart_id=?;"
        row = self.mkcDb.query(sql, 'one', (cartId,))
        if row:
            (exist,) = row
            if not exist:
                sql = 'UPDATE shopping_carts SET time_close=? WHERE id=?;'
                self.mkcDb.update(sql, (timeClose, cartId))
            
        

    
    def saveReturnStatus(self, statusCode, disc):
        '''
        @Params: statusCode (int), disc (object)
        @Return: None

        1. load disc if needed
        2. check reduce
        '''
        print(statusCode)
        rentalCount = 0
        sql = 'SELECT COUNT(id) FROM transactions WHERE rfid=?;'
        row = self.mkcDb.query(sql, 'one', (disc.rfid,))
        if row:
            (rentalCount,) = row
            rentalCount = int(rentalCount)
        
        if rentalCount > 0:
            rfidInfo = self._getRfidInfoByRfid(disc.rfid)
            if rfidInfo and str(rfidInfo['enable_reduce']) == '2':
                reduceFormula = rfidInfo['reduce_formula']
                salePrice = rfidInfo['sales_price']
                formulaPeices = reduceFormula.split(',')
                reduceInterval = int(formulaPeices[0])
                reduceAmount = formulaPeices[1]
                minimalPrice = formulaPeices[2]
                if float(salePrice) > float(minimalPrice) and reduceInterval > 0 and rentalCount % reduceInterval == 0:
                    reducedPrice = float(salePrice) - float(reduceAmount)
                    self.log.info('reduce(sale_price): %s, %s' % (disc.rfid, reducedPrice))
                    if float(reducedPrice) < float(minimalPrice):
                        reducedPrice = fmtMoney(minimalPrice)
                    else:
                        reducedPrice = fmtMoney(reducedPrice)
                    today = getCurTime('%Y-%m-%d')
                    sql = 'UPDATE rfids SET sales_price=?, last_reduce_date=? WHERE rfid=?;'
                    self.mkcDb.update(sql, (reducedPrice, today, disc.rfid))
                    params = { }
                    params['rfid'] = disc.rfid
                    params['sale_price'] = reducedPrice
                    params['last_reduce_date'] = today
                    self.syncData('dbSyncReduceSalePrice', params)
                
            
            if rfidInfo and str(rfidInfo['enable_reduce_convert_price']) == '2':
                reduceFormula = rfidInfo['reduce_formula_convert_price']
                saleConvertPrice = rfidInfo['sale_convert_price']
                formulaPeices = reduceFormula.split(',')
                reduceInterval = int(formulaPeices[0])
                reduceAmount = formulaPeices[1]
                minimalPrice = formulaPeices[2]
                if float(saleConvertPrice) > float(minimalPrice) and reduceInterval > 0 and rentalCount % reduceInterval == 0:
                    reducedPrice = float(saleConvertPrice) - float(reduceAmount)
                    self.log.info('reduce(sale_convert_price): %s, %s' % (disc.rfid, reducedPrice))
                    if float(reducedPrice) < float(minimalPrice):
                        reducedPrice = fmtMoney(minimalPrice)
                    else:
                        reducedPrice = fmtMoney(reducedPrice)
                    today = getCurTime('%Y-%m-%d')
                    sql = 'UPDATE rfids SET sale_convert_price=?, last_reduce_date_convert_price=? WHERE rfid=?;'
                    self.mkcDb.update(sql, (reducedPrice, today, disc.rfid))
                    params = { }
                    params['rfid'] = disc.rfid
                    params['sale_convert_price'] = reducedPrice
                    params['last_reduce_date'] = today
                    self.syncData('dbSyncReduceSaleConvertPrice', params)
                
            
        
        if str(statusCode) in ('2', '9'):
            if str(self.isRfidLoadable(disc)) == '1':
                self.getDefaultSettings(disc)
                self.saveLoadStatus(disc)
            
        
        
        try:
            overCapacitySlotsLimit = int(self._getConfigByKey('over_capacity_slots_limit'))
        except:
            overCapacitySlotsLimit = 0

        if overCapacitySlotsLimit:
            physicalEmptySlots = self._getPhysicalEmptySlots()
            
            try:
                overCapacityAlertThreshold = int(self._getConfigByKey('over_capacity_alert_threshold'))
            except:
                overCapacityAlertThreshold = 0

            if physicalEmptySlots == 0:
                subject = 'Notification - %s Slots Empty Out All' % self.kioskId
                message = "<p><b> Warning - Kiosk Running low on Available Slots </b></p><br\\><p>You are receiving this email because kiosk <B>%s</B> is running low on empty slots. To avoid any interruption to the service of your kiosk we suggest the following:</p><p>1.  Unload some discs to free up some slots.</p><p>2. Reduce the price of some discs to drive inventry turn-over.</p><br\\><p><b>NOTE - This message is just an informational warning, it's important to remember that the kiosk is still functioning normally at this time.</b></p>"
                message = message % self.kioskId
                self.emailAlert('PUBLIC', message, subject = subject, critical = MINICRITICAL)
            elif physicalEmptySlots == overCapacityAlertThreshold:
                subject = 'Notification - %s Empty Slots Alert' % self.kioskId
                message = "<p><b> Warning - Empty Slot Threshold Reached</b></p><br\\><p>You are receiving this email because your kiosk <B>%s</B> available slots has reached the alert level. To ensure there is always slots available for your customers to return discs we suggest the following:</p><p>1. Unload some discs to free up some slots.</p><p>2. Reduce the price of some discs to drive inventry turn-over.</p><p>If you're ok with running low on available slots you can manually adjust the alert threshold through Connections. Simply navigate to the config page of the kiosk and look for the config variable 'Over Capacity Alert Threshold' and change it to something more appropriate. The Default alert level is 10.</p><p><b>NOTE - This message is just an informational warning, it's important to remember that the kiosk is still functioning normally at this time.</b></p>"
                message = message % self.kioskId
                self.emailAlert('PUBLIC', message, subject = subject, critical = MINICRITICAL)
            
        

    
    def getUnloadMovieList(self, key, val = ''):
        '''
        Get movie list for unloading.
        @Params: key(str): "genre" | "slot" | "keyword"
                 val(str): "unload|bad" | "101" | "dark"
        @Return: [
                    {"movie_pic":"x.jpg", "movie_title":"x", "slot_id":"xxx",
                     "price":"xx", "upc":"xxx", "rfid":"xx"},
                 ]
        '''
        movieList = []
        if key.lower() == 'keyword':
            if len(val) == 1 and val.isalnum():
                keyword = val + '%'
            else:
                keyword = '%' + val + '%'
            sql = "SELECT R.rfid, R.title, R.movie_id, R.upc, R.sales_price, R.state, S.id FROM rfids AS R, slots AS S WHERE R.rfid=S.rfid AND R.state NOT IN ('out', 'reserved') AND R.title LIKE '%s' ORDER BY R.title ASC;" % sqlQuote(keyword)
        elif key.lower() == 'slot':
            keyword = '%' + val + '%'
            sql = "SELECT R.rfid, R.title, R.movie_id, R.upc, R.sales_price, R.state, S.id FROM rfids AS R, slots AS S WHERE R.rfid=S.rfid AND R.state NOT IN ('out', 'reserved') AND S.id LIKE '%s' ORDER BY S.id ASC;" % sqlQuote(keyword)
        elif key.lower() == 'genre':
            stateList = val.split('|')
            if len(stateList) == 1:
                strStateList = "('" + str(stateList[0]) + "')"
            else:
                strStateList = str(tuple(stateList))
            sql = 'SELECT R.rfid, R.title, R.movie_id, R.upc, R.sales_price, R.state, S.id FROM rfids AS R, slots AS S WHERE R.rfid=S.rfid AND R.state IN %s;' % strStateList
        else:
            msg = 'Invalid key(%s) for getUnloadMovieList' % key
            self.log.error(msg)
            raise Exception(msg)
        rows = self.mkcDb.query(sql)
        for row in rows:
            (rfid, title, movieId, upc, salePrice, state, slotId) = row
            tmp = { }
            tmp['rfid'] = rfid
            tmp['upc'] = str(upc)
            tmp['movie_title'] = title
            tmp['movie_pic'] = self._formPicName(movieId)
            tmp['price'] = salePrice
            tmp['state'] = state
            tmp['slot_id'] = str(slotId)
            movieList.append(tmp)
        
        return movieList

    
    def lockDiscState(self, disc):
        '''
        @Params: disc (object)
        @Return: statusCode: 0 -> OK
                             1 -> not available

        update rfid state to "XXX_pending"
        '''
        statusCode = 0
        sql = "SELECT COUNT(*) FROM rfids WHERE rfid=? AND state IN ('in', 'unload');"
        (exist,) = self.mkcDb.query(sql, 'one', (disc.rfid,))
        if exist:
            statusCode = 0
            state = self._getDiscState(disc.rfid)
            if not state.endswith('_pending'):
                state += '_pending'
            
            sql = 'UPDATE rfids SET state=? WHERE rfid=?;'
            self.mkcDb.update(sql, (state, disc.rfid))
        else:
            statusCode = 1
        return statusCode

    
    def saveUnloadStatus(self, disc):
        '''
        @Params: rfid (object)
        @Return: None

        synchronize the "check out" info to server, save to sync_db
        '''
        rfidInfo = self._getRfidInfoByRfid(disc.rfid)
        sqlList = []
        sql = "UPDATE slots SET state='empty', rfid='' WHERE rfid='%s';" % sqlQuote(disc.rfid)
        sqlList.append(sql)
        sql = "DELETE FROM rfids WHERE rfid='%s';" % sqlQuote(disc.rfid)
        sqlList.append(sql)
        eventId = self.logEvent(category = 'operation', action = 'unload', data1 = disc.slotID, data2 = disc.rfid, data3 = rfidInfo.get('upc', ''), data4 = rfidInfo.get('title', ''))
        
        try:
            self.mkcDb.updateTrs(sqlList)
            eventInfo = self._getEventByEventId(eventId)
            params = { }
            params['rfid_list'] = [
                disc.rfid]
            params['event_info_list'] = [
                eventInfo]
            self.syncData('dbSyncUnload', params)
            self.log.info('Save dbSyncUnload to sync db: ' + str(params))
        except:
            sql = 'DELETE FROM events WHERE id=?;'
            self.mkcDb.update(sql, (eventId,))
            raise 


    
    def getPickUpList(self, shoppingCart, customer):
        '''
        @Params: shoppingCart (object), customer (object)
        @Return: None

        get pick up list by ccNum
        '''
        pickUpList = []
        ccId = customer.ccid
        self.log.info('pick up, ccid: %s' % ccId)
        sql = "SELECT S.id, V.id, R.rfid, R.upc, R.title, R.genre, R.movie_id, V.gene, V.cc_id, V.upg_id, V.price_plan, V.price_plan_text, V.coupon_code, V.coupon_plan, V.coupon_text, V.ms_keep_days FROM rfids AS R, reservations AS V, slots AS S WHERE R.rfid=V.rfid AND S.rfid=R.rfid AND V.state='reserved' AND R.state='reserved' AND V.cc_id=?;"
        rows = self.mkcDb.query(sql, params = (ccId,))
        self.log.info('pick up, count: %s' % len(rows))
        if rows:
            for row in rows:
                (slotId, id, rfid, upc, title, genre, movieId, gene, ccId, upgId, pricePlan, pricePlanText, couponCode, couponPlan, couponText, msKeepDays) = row
                picName = self._formPicName(movieId)
                disc = Disc()
                disc.reserveID = id
                disc.rfid = rfid
                disc.upc = upc
                disc.title = title
                disc.genre = genre
                disc.picture = picName
                disc.slotID = slotId
                disc.gene = gene
                disc.upgID = upgId
                disc.msKeepDays = msKeepDays
                disc.coupon.couponCode = couponCode
                disc.coupon.couponData = couponPlan
                disc.coupon.shortDes = couponText
                self.loadDiscInfo(disc, rfid)
                shoppingCart.addDisc(disc)
            
        

    
    def getPickUpListByCode(self, shoppingCart, code):
        '''
        @Params: shoppingCart (object), code (string)
        @Return: ccId

        get pick up list by pickup code
        '''
        pickUpList = []
        ccId = ''
        self.log.info('pick up, code: %s' % code)
        sql = "SELECT S.id, V.id, R.rfid, R.upc, R.title, R.genre, R.movie_id, V.gene, V.cc_id, V.upg_id, V.price_plan, V.price_plan_text, V.coupon_code, V.coupon_plan, V.coupon_text, V.ms_keep_days FROM rfids AS R, reservations AS V, slots AS S WHERE R.rfid=V.rfid AND S.rfid=R.rfid AND V.state='reserved' AND R.state='reserved' AND V.pickup_code=?;"
        rows = self.mkcDb.query(sql, params = (code,))
        self.log.info('pick up, count: %s' % len(rows))
        if rows:
            for row in rows:
                (slotId, id, rfid, upc, title, genre, movieId, gene, ccId, upgId, pricePlan, pricePlanText, couponCode, couponPlan, couponText, msKeepDays) = row
                picName = self._formPicName(movieId)
                disc = Disc()
                disc.reserveID = id
                disc.rfid = rfid
                disc.upc = upc
                disc.title = title
                disc.genre = genre
                disc.picture = picName
                disc.slotID = slotId
                disc.gene = gene
                disc.upgID = upgId
                disc.msKeepDays = msKeepDays
                disc.coupon.couponCode = couponCode
                disc.coupon.couponData = couponPlan
                disc.coupon.shortDes = couponText
                self.loadDiscInfo(disc, rfid)
                shoppingCart.addDisc(disc)
            
        
        return ccId

    
    def updateDiscStatePickup(self, disc):
        '''
        @Params: disc (object)
        @Return: None

        update pick up dvd state by rfid
        '''
        sqlList = []
        sql = "UPDATE rfids SET state='in' WHERE state='reserved' AND rfid='%s';" % sqlQuote(disc.rfid)
        sqlList.append(sql)
        sql = "UPDATE reservations SET state='picked' WHERE state='reserved' AND rfid='%s';" % sqlQuote(disc.rfid)
        sqlList.append(sql)
        self.mkcDb.updateTrs(sqlList)
        self.syncData('dbSyncPickUp', {
            'rfid': disc.rfid })

    
    def getSlotsCountByState(self, state = 'all'):
        '''
        @Params: state (string): "all"(default), "empty", "occupied"
        @Return: count (int)

        get slots count by state
        '''
        count = 0
        strWhere = 'WHERE 1=1'
        if state != 'all':
            strWhere += " AND state='%s'" % state.replace("'", "''")
        
        sql = 'SELECT COUNT(*) FROM slots %s;' % strWhere
        result = self.mkcDb.query(sql, 'one')
        if result:
            (count,) = result
        
        return count

    
    def getDvdsCountByState(self, state = 'all'):
        '''
        @Params: state (string): "all"(default), "in", "out", "reserved"
        @Return: count (int)

        get slots count by state
        '''
        count = 0
        strWhere = 'WHERE 1=1'
        if state != 'all':
            strWhere += " AND state='%s'" % state.replace("'", "''")
        
        sql = 'SELECT COUNT(*) FROM rfids %s;' % strWhere
        result = self.mkcDb.query(sql, 'one')
        if result:
            (count,) = result
        
        return count

    
    def getSimpleReportData(self):
        '''
        @Params: None
        @Return: report (Dict): {"kiosk_id":XXX, "capacity":XXX,
                                 "today":XXX, "completed_rentals":XXX,
                                 "rental_income":XXX, "initial_rentals":XXX,
                                 "sale_count":XXX, "sale_income":XXX,
                                 "total_income":XXX, "total_tax":XXX,
                                 "total_loaded_dvd":XXX, "total_empty_slots":XXX,
                                 "total_dvds_in":XXX, "total_dvds_out":XXX,
                                 "total_dvds_reserved":XXX, "completed_rentals_week":XXX,
                                 "rental_income_week":XXX, "initial_rentals_week":XXX,
                                 "sale_count_week":XXX, "sale_income_week":XXX,
                                 "completed_rentals_month":XXX, "rental_income_month":XXX,
                                 "initial_rentals_month":XXX, "sale_count_month":XXX,
                                 "sale_income_month":XXX, "completed_rentals_year":XXX,
                                 "rental_income_year":XXX, "initial_rentals_year":XXX,
                                 "sale_count_year":XXX, "sale_income_year":XXX}

        get simple report data
        '''
        report = { }
        report['kiosk_id'] = str(self.kioskId)
        report['today'] = str(getCurTime('%Y-%m-%d'))
        
        try:
            overCapacitySlotsLimit = int(self._getConfigByKey('over_capacity_slots_limit'))
        except:
            overCapacitySlotsLimit = 0

        if overCapacitySlotsLimit > 0:
            report['capacity'] = '%s + %s' % (self.getSlotsCountByState(), overCapacitySlotsLimit)
        else:
            report['capacity'] = str(self.getSlotsCountByState())
        report['total_loaded_dvd'] = str(self.getDvdsCountByState('all'))
        report['total_empty_slots'] = str(int(self.getSlotsCountByState('empty')) + int(self.getDvdsCountByState('out')))
        report['total_dvds_in'] = str(self.getDvdsCountByState('in'))
        report['total_dvds_out'] = str(self.getDvdsCountByState('out'))
        report['total_dvds_reserved'] = str(self.getDvdsCountByState('reserved'))
        todayReport = self._getSimpleReportByDate(report['today'], report['today'])
        report['completed_rentals'] = str(todayReport['completed_rental_count'])
        report['rental_income'] = str(todayReport['total_rental_amount'])
        report['initial_rentals'] = str(todayReport['total_initial_rental_count'])
        report['sale_count'] = str(todayReport['total_sale_count'])
        report['sale_income'] = str(todayReport['total_sale_amount'])
        report['total_income'] = str(todayReport['total_income'])
        report['total_tax'] = str(todayReport['total_tax'])
        (fromDate, endDate) = currentWeekRange()
        weekReport = self._getSimpleReportByDate(fromDate, endDate)
        report['completed_rentals_week'] = str(weekReport['completed_rental_count'])
        report['rental_income_week'] = str(weekReport['total_rental_amount'])
        report['initial_rentals_week'] = str(weekReport['total_initial_rental_count'])
        report['sale_count_week'] = str(weekReport['total_sale_count'])
        report['sale_income_week'] = str(weekReport['total_sale_amount'])
        (fromDate, endDate) = currentMonthRange()
        monthReport = self._getSimpleReportByDate(fromDate, endDate)
        report['completed_rentals_month'] = str(monthReport['completed_rental_count'])
        report['rental_income_month'] = str(monthReport['total_rental_amount'])
        report['initial_rentals_month'] = str(monthReport['total_initial_rental_count'])
        report['sale_count_month'] = str(monthReport['total_sale_count'])
        report['sale_income_month'] = str(monthReport['total_sale_amount'])
        (fromDate, endDate) = currentYearRange()
        yearReport = self._getSimpleReportByDate(fromDate, endDate)
        report['completed_rentals_year'] = str(yearReport['completed_rental_count'])
        report['rental_income_year'] = str(yearReport['total_rental_amount'])
        report['initial_rentals_year'] = str(yearReport['total_initial_rental_count'])
        report['sale_count_year'] = str(yearReport['total_sale_count'])
        report['sale_income_year'] = str(yearReport['total_sale_amount'])
        return report

    
    def getKioskInfo(self):
        '''
        @Params: None
        @Return: info (Dict): {"kiosk_id":XXX, "ip":XXX,
                               "mac":XXX, "kiosk_soft":XXX,
                               "firmware":XXX, "start_time":XXX,
                               "capacity":XXX, "kiosk_time_zone":XXX
                               "today":XXX}

        get kiosk info
        '''
        info = { }
        info['today'] = str(getCurTime('%Y-%m-%d'))
        info['capacity'] = str(self.getSlotsCountByState())
        info['kiosk_id'] = str(self._getKioskInfoByKey('KioskID'))
        info['ip'] = str(self._getKioskInfoByKey('IP'))
        info['mac'] = str(self._getKioskInfoByKey('MAC'))
        info['kiosk_soft'] = str(self._getKioskInfoByKey('KioskSoft'))
        info['firmware'] = str(self._getKioskInfoByKey('Firmware'))
        info['start_time'] = str(self._getKioskInfoByKey('StartTime'))
        info['kiosk_time_zone'] = str(self._getKioskInfoByKey('KioskTimeZone'))
        info['umg_channel'] = str(self._getKioskInfoByKey('UMGChannel'))
        return info

    
    def _getSimpleReportByDate(self, startDate, endDate):
        '''
        get simple report: completed rentals, rental income, initial rentals,
                           sale count, sale income, total income(include tax), total tax
        '''
        report = { }
        params = {
            'fromDate': startDate,
            'toDate': endDate }
        addtion = "AND upg_id>=0 AND state=='closed'"
        sql = "SELECT COUNT(*), TOTAL(amount), TOTAL(amount / (1 + sales_tax/100.0)) FROM transactions WHERE gene='sale' AND ((DATE(out_time)>=:fromDate AND DATE(out_time)<=:toDate AND (in_time='' OR in_time IS NULL)) OR (DATE(in_time)>=:fromDate AND DATE(in_time)<=:toDate AND in_time<>'' AND in_time IS NOT NULL)) %s;"
        sql = sql % addtion
        row = self.mkcDb.query(sql, 'one', params = params)
        (totalSaleCount, totalSaleAmount, salesIncomeNoTax) = row
        if not totalSaleCount:
            totalSaleCount = 0
        
        if not totalSaleAmount:
            totalSaleAmount = 0
        
        if not salesIncomeNoTax:
            salesIncomeNoTax = 0
        
        report['total_sale_count'] = totalSaleCount
        report['total_sale_amount'] = fmtMoney(totalSaleAmount)
        sql = "SELECT COUNT(*), SUM(amount), TOTAL(amount / (1 + sales_tax/100.0)) FROM transactions WHERE DATE(in_time) >= :fromDate AND DATE(in_time) <= :toDate AND gene<>'sale' %s;"
        sql = sql % addtion
        row = self.mkcDb.query(sql, 'one', params = params)
        (completedRentalCount, totalRentalAmount, rentalIncomeNoTax) = row
        if completedRentalCount is None:
            completedRentalCount = 0
        
        if totalRentalAmount is None:
            totalRentalAmount = 0
        
        if rentalIncomeNoTax is None:
            rentalIncomeNoTax = 0
        
        report['completed_rental_count'] = completedRentalCount
        report['total_rental_amount'] = fmtMoney(totalRentalAmount)
        sql = "SELECT COUNT(*) FROM transactions WHERE DATE(out_time) >= :fromDate AND DATE(out_time) <= :toDate AND gene='rent' AND upg_id>=0;"
        row = self.mkcDb.query(sql, 'one', params = params)
        (totalInitialRentalCount,) = row
        if totalInitialRentalCount is None:
            totalInitialRentalCount = 0
        
        report['total_initial_rental_count'] = totalInitialRentalCount
        totalIncomeNoTax = salesIncomeNoTax + rentalIncomeNoTax
        totalIncome = totalRentalAmount + totalSaleAmount
        totalTax = totalIncome - totalIncomeNoTax
        report['total_income'] = fmtMoney(totalIncome)
        report['total_tax'] = fmtMoney(totalTax)
        return report

    
    def _getKioskInfoByKey(self, key):
        '''
        get kiosk info by key name
        e.g. SELECT value FROM info WHERE variable=key;
        '''
        info = ''
        sql = 'SELECT value FROM info WHERE variable=?;'
        result = self.mkcDb.query(sql, 'one', (key,))
        if result:
            (info,) = result
        
        self.log.info('Succeed to get info(%s): %s' % (key, info))
        info = str(info)
        return info

    
    def loadRecoverRfidInfo(self, statusCode, disc):
        '''
        @Params: statusCode (int), disc (object)
        @Return: None

        load recover rfid info
        '''
        if str(statusCode) in ('6', '7'):
            trsInfo = self._getTrsInfoBySaleRfid(disc.rfid)
            disc.upc = trsInfo['upc']
            movieInfo = self._getMovieInfo(disc.upc)
            disc.movieID = movieInfo['movie_id']
            disc.title = movieInfo['movie_title']
            disc.genre = movieInfo['genre']
            self.getDefaultSettings(disc)
        elif str(statusCode) == '10':
            sql = "SELECT data3 FROM events WHERE action='unload' AND data2=?;"
            row = self.mkcDb.query(sql, 'one', (disc.rfid,))
            if row:
                disc.upc = row[0]
                movieInfo = self._getMovieInfo(disc.upc)
                disc.movieID = movieInfo['movie_id']
                disc.title = movieInfo['movie_title']
                disc.genre = movieInfo['genre']
            else:
                disc.upc = '000000000000'
                disc.movieID = '0000'
                disc.title = 'Unknown Title'
                disc.genre = 'Unknown'
            self.getDefaultSettings(disc)
        elif str(statusCode) == '11':
            sql = "SELECT data3 FROM events WHERE action='clear' AND data2=?;"
            row = self.mkcDb.query(sql, 'one', (disc.rfid,))
            if row:
                disc.upc = row[0]
                movieInfo = self._getMovieInfo(disc.upc)
                disc.movieID = movieInfo['movie_id']
                disc.title = movieInfo['movie_title']
                disc.genre = movieInfo['genre']
            else:
                disc.upc = '000000000000'
                disc.movieID = '0000'
                disc.title = 'Unknown Title'
                disc.genre = 'Unknown'
            self.getDefaultSettings(disc)
        elif str(statusCode) == '0':
            disc.upc = '000000000000'
            disc.movieID = '0000'
            disc.title = 'Unknown Title'
            disc.genre = 'Unknown'
            self.getDefaultSettings(disc)
        
        self.log.info('recover: %s, %s' % (statusCode, disc.rfid))

    
    def saveRecoverStatus(self, statusCode, disc):
        '''
        @Params: statusCode (int), disc (object)
        @Return: None

        load disc if need
        '''
        self.log.info('saveRecoverStatus: %s, %s' % (statusCode, disc.rfid))
        print(statusCode)
        if str(statusCode) in ('0', '2', '6', '7', '8', '9', '10', '11'):
            if str(self.isRfidLoadable(disc)) == '1':
                self.saveLoadStatus(disc)
                if str(statusCode) in ('0', '6', '7', '8'):
                    self.setBadRfid(disc.rfid)
                
            
        

    
    def saveAIStatus(self, status, description):
        ''' save the active / inactive status to server

        @param status: active or inactive
        @param description: the active / inactive description
        @return: None
        '''
        funcName = 'dbSyncAIStatus'
        params = { }
        params['status'] = status
        params['description'] = description
        self.syncData(funcName, params)

    
    def getKioskOwnership(self):
        '''
        @Params: None
        @Return: {"host_id":XXX, "client_id":XXX}
        '''
        
        try:
            data = self.getRemoteData('getMachineOwnerShipInfo', {
                'machine_id': self.kioskId })
            if data['result'].lower() == 'ok':
                return data['zdata']
            else:
                return {
                    'host_id': '',
                    'client_id': '' }
        except:
            return {
                'host_id': '',
                'client_id': '' }


    
    def setIP(self):
        '''
        @Params: None
        @Return: None

        set machine info: IP
        '''
        ip = str(getEthIP()).strip()
        sql = "UPDATE info SET value=? WHERE variable='IP';"
        self.mkcDb.update(sql, (ip,))
        changes = {
            'IP': ip }
        self.syncData('dbSyncInfo', {
            'changes': changes })

    
    def setKioskInfo(self):
        '''
        @Params: None
        @Return: None

        set machine info: KioskID, IP, MAC, KioskSoft,
                          Firmware, StartTime, KioskTimeZone,
                          CapacityType
        '''
        ip = str(getEthIP()).strip()
        mac = str(getEthMac()).strip()
        
        try:
            kiosksoft = str(open(VERSION_FILE).readline()).strip()
            if kiosksoft:
                if not kiosksoft.startswith('V'):
                    kiosksoft = 'V' + kiosksoft
                
            else:
                kiosksoft = str(config.KIOSKSOFT).strip()
        except:
            kiosksoft = str(config.KIOSKSOFT).strip()

        firmware = str(config.FIRMWARE).strip()
        startTime = str(getLinuxDate()).strip()
        kioskTimeZone = str(getTimeZone()).strip()
        capacityType = str(getKioskCapacity())
        print(firmware)
        print(startTime)
        print(kioskTimeZone)
        print(capacityType)
        sql = "UPDATE info SET value=? WHERE variable='KioskID';"
        self.mkcDb.update(sql, (self.kioskId,))
        sql = "UPDATE info SET value=? WHERE variable='IP';"
        self.mkcDb.update(sql, (ip,))
        sql = "UPDATE info SET value=? WHERE variable='MAC';"
        self.mkcDb.update(sql, (mac,))
        sql = "UPDATE info SET value=? WHERE variable='KioskSoft';"
        self.mkcDb.update(sql, (kiosksoft,))
        sql = "UPDATE info SET value=? WHERE variable='Firmware';"
        self.mkcDb.update(sql, (firmware,))
        sql = "UPDATE info SET value=? WHERE variable='StartTime';"
        self.mkcDb.update(sql, (startTime,))
        sql = "UPDATE info SET value=? WHERE variable='KioskTimeZone';"
        self.mkcDb.update(sql, (kioskTimeZone,))
        sql = "UPDATE info SET value=? WHERE variable='CapacityType';"
        self.mkcDb.update(sql, (capacityType,))
        params = { }
        params['KioskID'] = self.kioskId
        params['IP'] = ip
        params['MAC'] = mac
        params['KioskSoft'] = kiosksoft
        params['Firmware'] = firmware
        params['StartTime'] = startTime
        params['KioskTimeZone'] = kioskTimeZone
        params['CapacityType'] = capacityType
        self.syncData('dbSyncKioskInfo', params)

    
    def isTestMode(self):
        '''
        @Params: None
        @Return: True or False

        check if it is test mode
        '''
        result = False
        upgShowMode = self._getConfigByKey('upg_show_mode')
        if str(upgShowMode).lower() == 'yes':
            result = True
        
        return result

    
    def setTestMode(self):
        '''
        @Params: None
        @Return: None

        turn on / off the test mode
        '''
        upgShowMode = self._getConfigByKey('upg_show_mode')
        if str(upgShowMode).lower() == 'yes':
            upgShowMode = 'no'
            self.SHOW_MODE = False
        else:
            upgShowMode = 'yes'
            self.SHOW_MODE = True
        self.log.info('self.SHOW_MODE: %s' % self.SHOW_MODE)
        changes = {
            'upg_show_mode': upgShowMode,
            'show_mode': upgShowMode }
        self._setConfig(changes)
        params = { }
        params['changes'] = changes
        self.syncData('dbSyncConfig', params)

    
    def setConfig(self, changes):
        '''
        @Params: changes (dict)
        @Return: None

        '''
        self._setConfig(changes)
        params = { }
        params['changes'] = changes
        self.syncData('dbSyncConfig', params)

    
    def updateTransactionsPostauth(self, trsList, changes):
        """
        @Params: trsList (list), changes (dict)
        @Return: None

        set trs's state and upgId after postauth
        """
        if changes:
            if len(trsList) == 1:
                strTrsList = "('" + str(trsList[0]) + "')"
            else:
                strTrsList = str(tuple(trsList))
            sql = 'UPDATE transactions SET '
            for key in list(changes.keys()):
                sql += "%s='%s', " % (key, str(changes[key]).replace("'", "''"))
            
            sql = sql.strip(', ')
            sql += ' WHERE id in %s;' % strTrsList
            self.mkcDb.update(sql)
            params = { }
            params['trs_list'] = trsList
            params['changes'] = changes
            self.syncData('dbSyncPostauth', params)
        

    
    def getKioskLogo(self):
        '''
        @Params: None
        @Return: filename (string)

        get the logo filename
        '''
        filename = os.path.join(config.USER_ROOT, 'kiosk/var/gui/sys/kiosk_logo.png')
        defaultFileName = config.UI_PATH + 'default_logo.png'
        
        try:
            funcName = 'getClientConfigByKeyKioskId'
            params = {
                'key': 'kiosk_logo_md5' }
            resultDic = self.getRemoteData(funcName, params)
            if resultDic and resultDic.get('result', '').lower() == 'ok':
                md5Server = resultDic['zdata']
                md5Local = self._getConfigByKey('kiosk_logo_md5')
                if md5Server and md5Server != md5Local:
                    funcName = 'getClientConfigByKeyKioskId'
                    params = {
                        'key': 'kiosk_logo' }
                    resultDic = self.getRemoteData(funcName, params)
                    if resultDic and resultDic.get('result', '').lower() == 'ok':
                        logo = resultDic['zdata']
                        self.setConfig({
                            'kiosk_logo': logo,
                            'kiosk_logo_md5': md5Server })
                    
                
        except Exception as ex:
            self.log.error('getKioskLogo(remote): %s' % str(ex))

        logo = self._getConfigByKey('kiosk_logo')
        if logo:
            logo = b64decode(logo)
            f = open(filename, 'w')
            f.write(logo)
            f.close()
        else:
            import shutil
            shutil.copy(defaultFileName, filename)
        return filename

    
    def getShoppingCartMessage(self):
        '''
        @Params: None
        @Return: message (string)

        get the shopping cart message from server
        '''
        message = ''
        
        try:
            message = self._getConfigByKey('shopping_cart_message')
        except Exception as ex:
            self.log.error('getShoppingCartMessage: %s' % str(ex))

        return message

    
    def initDb(self, passcode):
        '''
        @Params: passcode (string)
        @Return: statusCode (int)
        statusCode: 0. failed
                    1. success
                    2. error passcode

        init the mkc.db and sync.db
        '''
        statusCode = 0
        if str(passcode) != '121':
            statusCode = 2
        else:
            from . import init_mkcdb
            init_mkcdb.initDb()
            statusCode = 1
        return statusCode

    
    def emailAlert(self, msgType, message, receiver = '', subject = '', critical = UNCRITICAL):
        '''
        @Params: msgType (string), message (string), receiver (string)
        @Return: none

        send email to us or clients
        '''
        funcName = 'kioskSendEmail'
        params = { }
        params['msg_type'] = msgType
        params['message'] = message
        params['receiver'] = receiver
        params['mail_level'] = critical
        if not subject:
            subject = 'Notification - %s ' % self.kioskId
        
        params['subject'] = subject
        count = 0
        
        try:
            sql = "SELECT COUNT(id) FROM db_sync_remote_kiosk WHERE function_name='kioskSendEmail' AND params=? AND add_time>DATE('now', 'localtime');"
            row = self.syncDb.query(sql, 'one', (str(params),))
            if row:
                (count,) = row
        except:
            pass

        if count < 5 or msgType.upper() in ('PUBLIC', 'CLIENT'):
            
            try:
                self.syncDataNoSequence(funcName, params)
            except Exception as ex:
                self.log.error('emailAlert: %s' % str(ex))

        

    
    def verifyDb(self):
        try:
            from . import db
            db.verifyDb()
        except Exception as ex:
            self.log.error('verifyDb: %s' % str(ex))


    
    def getLatestVersion(self):
        latestVersion = ''
        
        try:
            funcName = 'getLatestVersion'
            params = { }
            resultDic = self.getRemoteData(funcName, params)
            if resultDic:
                if resultDic['result'].lower() == 'ok':
                    data = resultDic['zdata']
                    if data:
                        latestVersion = data['version']
                    
                
        except Exception as ex:
            self.log.error('when getLatestVersion: ' + str(ex))

        return latestVersion

    
    def getAutoUpdateLatestVersion(self, currVersion):
        versionInfo = {
            'latest_version': '',
            'host': '',
            'port': '',
            'un': '',
            'pwd': '' }
        
        try:
            funcName = 'getAutoUpdateLatestVersion'
            params = {
                'curr_version': currVersion }
            resultDic = self.getRemoteData(funcName, params)
            if resultDic:
                if resultDic['result'].lower() == 'ok':
                    versionInfo = resultDic['zdata']
                
        except Exception as ex:
            self.log.error('when getAutoUpdateLatestVersion: ' + str(ex))

        return versionInfo

    
    def setBadRfid(self, rfid):
        '''
        @Params: rfid (string)
        @Return: statusCode (string)

        set the rfid state to "bad"
        '''
        statusCode = '1'
        
        try:
            sql = "UPDATE rfids SET state='bad' WHERE rfid=?;"
            self.mkcDb.update(sql, (rfid,))
            params = {
                'rfid': rfid }
            self.syncData('dbSyncSetBadRfid', params)
        except Exception as ex:
            statusCode = '0'
            self.log.error('when setBadRfid: ' + str(ex))

        return statusCode

    
    def setBadSlot(self, slotId):
        '''
        @Params: slotId (string)
        @Return: statusCode (string)

        set the slot state to "bad"
        '''
        statusCode = '1'
        
        try:
            sql = "UPDATE slots SET state='bad' WHERE id=?;"
            self.mkcDb.update(sql, (slotId,))
            params = {
                'slot_id': slotId }
            self.syncData('dbSyncSetBadSlot', params)
        except Exception as ex:
            statusCode = '0'
            self.log.error('when setBadSlot: ' + str(ex))

        return statusCode

    
    def getArrangementPlan(self):
        '''
        @Params: None
        @Return: plan (list)

        get arrangement plan
        '''
        plan = []
        
        try:
            now = getCurTime()
            sql = "SELECT id, data FROM commands WHERE state='active' AND command='arrange_slots' AND time_begin<=?;"
            row = self.mkcDb.query(sql, 'one', (now,))
            if row:
                (cid, data) = row
                data = eval(data)
                if data:
                    target = { }
                    targetSlotIds = []
                    for slotId, rfid in data:
                        targetSlotIds.append(slotId)
                        if rfid:
                            target[rfid] = slotId
                        
                    
                    targetSlotIds.sort()
                    sql = 'SELECT S.id, S.state, R.rfid, R.state FROM slots AS S LEFT JOIN rfids AS R ON S.rfid=R.rfid ORDER BY S.id ASC;'
                    rows = self.mkcDb.query(sql)
                    current = { }
                    currentSlotIds = []
                    for slotId, slotState, rfid, rfidState in rows:
                        if slotState == 'occupied':
                            state = rfidState
                        else:
                            state = slotState
                        currentSlotIds.append(slotId)
                        if not 1 and rfid:
                            pass
                        current[slotId] = ('', state)
                    
                    currentSlotIds.sort()
                    if targetSlotIds != currentSlotIds:
                        self.finishArrangement()
                    else:
                        blanks = []
                        moves = []
                        plan = []
                        STATE = 1
                        RFID = 0
                        for key in list(current.keys()):
                            if current[key][STATE] in ('empty', 'out'):
                                blanks.append(key)
                                current.pop(key)
                            elif current[key][STATE] not in ('in', 'reserved'):
                                current.pop(key)
                            
                        
                        if len(blanks) == 0:
                            print('no empty slots')
                            blanks.append(1000)
                            print('use exchange as empty slot for swapping')
                        else:
                            print('empty slots %d' % (len(blanks),))
                        stage = 0
                        while list(current.keys()):
                            key = list(current.keys())[0]
                            slot = current[key]
                            if stage == 0:
                                if slot[RFID] in target:
                                    if target[slot[RFID]] == key:
                                        current.pop(key)
                                    else:
                                        moves.append(key)
                                        current.pop(key)
                                        key = target[slot[RFID]]
                                        stage = 1
                                else:
                                    current.pop(key)
                            
                            while stage != 0:
                                if key in blanks:
                                    moves.append(key)
                                    blanks.pop(blanks.index(key))
                                    blanks.append(moves[0])
                                    blanks.sort()
                                    moves.reverse()
                                    plan.append(moves)
                                    moves = []
                                    stage = 0
                                elif key in current:
                                    slot = current[key]
                                    if slot[RFID] in target:
                                        if target[slot[RFID]] == key:
                                            current.pop(key)
                                            moves = []
                                            stage = 0
                                        else:
                                            moves.append(key)
                                            current.pop(key)
                                            key = target[slot[RFID]]
                                    else:
                                        current.pop(key)
                                elif key == moves[0]:
                                    tmp = blanks[min(list(range(len(blanks))), key=lambda x: abs(x - key))]
                                    moves.append(tmp)
                                    moves.insert(0, tmp)
                                    moves.reverse()
                                    plan.append(moves)
                                    moves = []
                                    stage = 0
                                else:
                                    moves = []
                                    stage = 0
                        self.log.info('Plan: ' + str(plan))
                        if not plan:
                            self.finishArrangement()
                        
                
        except Exception as ex:
            self.log.error('when getArrangementPlan: ' + str(ex))

        return plan

    
    def moveSlot(self, orig, dest):
        '''
        @Params: orig(string), dest(string)
        @Return: None

        move disc from orig to dest
        '''
        now = getCurTime()
        sql = 'SELECT rfid FROM slots WHERE id=?;'
        origRfid = ''
        row = self.mkcDb.query(sql, 'one', (orig,))
        if row:
            (origRfid,) = row
            if str(origRfid) == 'None':
                origRfid = ''
            
        
        destRfid = ''
        row = self.mkcDb.query(sql, 'one', (dest,))
        if row:
            (destRfid,) = row
            if str(destRfid) == 'None':
                destRfid = ''
            
        
        sqlList = []
        if str(dest) == '1000':
            rfidInfo = self._getRfidInfoByRfid(origRfid)
            sql = "INSERT INTO events(category, action, data1, data2, data3, data4, data5, time_recorded, time_updated) VALUES('auto', 'move', '%s', 'Exchange', '%s', '%s', '%s', '%s', '%s');"
            sql = sql % (sqlQuote(orig), sqlQuote(origRfid), sqlQuote(rfidInfo['upc']), sqlQuote(rfidInfo['title']), sqlQuote(now), sqlQuote(now))
            sqlList.append(sql)
        elif str(orig) == '1000':
            rfidInfo = self._getRfidInfoByRfid(destRfid)
            sql = "INSERT INTO events(category, action, data1, data2, data3, data4, data5, time_recorded, time_updated) VALUES('auto', 'move', 'Exchange', '%s', '%s', '%s', '%s', '%s', '%s');"
            sql = sql % (sqlQuote(dest), sqlQuote(destRfid), sqlQuote(rfidInfo['upc']), sqlQuote(rfidInfo['title']), sqlQuote(now), sqlQuote(now))
            sqlList.append(sql)
        else:
            oSlotInfo = self._getSlotInfoBySlotId(orig)
            dSlotInfo = self._getSlotInfoBySlotId(dest)
            oRfidInfo = self._getRfidInfoByRfid(origRfid)
            dRfidInfo = self._getRfidInfoByRfid(destRfid)
            if oRfidInfo:
                sql = "UPDATE slots SET rfid='%s', state='%s' WHERE id='%s';"
                sql = sql % (sqlQuote(origRfid), sqlQuote(oSlotInfo['state']), sqlQuote(dest))
                sqlList.append(sql)
                sql = "UPDATE slots SET rfid='%s', state='%s' WHERE id='%s';"
                sql = sql % (sqlQuote(destRfid), sqlQuote(dSlotInfo['state']), sqlQuote(orig))
                sqlList.append(sql)
                sql = "INSERT INTO events(category, action, data1, data2, data3, data4, data5, time_recorded, time_updated) VALUES('auto', 'move', '%s', '%s', '%s', '%s', '%s', '%s', '%s');"
                sql = sql % (sqlQuote(orig), sqlQuote(dest), sqlQuote(origRfid), sqlQuote(oRfidInfo['upc']), sqlQuote(oRfidInfo['title']), sqlQuote(now), sqlQuote(now))
                sqlList.append(sql)
                if str(oRfidInfo.get('state', '')).lower() == 'out':
                    sql = "UPDATE transactions SET slot_id='%s' WHERE rfid='%s' AND state='open';"
                    sql = sql % (sqlQuote(dest), sqlQuote(origRfid))
                    sqlList.append(sql)
                
                if dRfidInfo and str(dRfidInfo.get('state', '')).lower() == 'out':
                    sql = "UPDATE transactions SET slot_id='%s' WHERE rfid='%s' AND state='open';"
                    sql = sql % (sqlQuote(orig), sqlQuote(destRfid))
                    sqlList.append(sql)
                
            
        if sqlList:
            self.mkcDb.updateTrs(sqlList)
            funcName = 'dbSyncScript'
            dbFile = 'machines/%s.db' % self.kioskId
            params = {
                'scripts': '\n'.join(sqlList),
                'db_file': dbFile }
            self.syncData(funcName, params)
        

    
    def finishArrangement(self):
        '''
        @Params: None
        @Return: None

        close arrangement
        '''
        now = getCurTime()
        sql = "SELECT id FROM commands WHERE state='active' AND command='arrange_slots' AND time_begin<=? LIMIT 1;"
        row = self.mkcDb.query(sql, 'one', (now,))
        if row:
            (cid,) = row
            sql = "UPDATE commands SET time_end='%s', state='closed' WHERE id='%s';"
            sql = sql % (sqlQuote(now), sqlQuote(cid))
            self.mkcDb.update(sql)
            funcName = 'dbSyncScript'
            dbFile = 'machines/%s.db' % self.kioskId
            params = {
                'scripts': sql,
                'db_file': dbFile }
            self.syncData(funcName, params)
        

    
    def _getSlotInfoBySlotId(self, slotId):
        slotInfo = { }
        sql = 'SELECT rank, rfid, state FROM slots WHERE id=?;'
        row = self.mkcDb.query(sql, 'one', (slotId,))
        if row:
            (rank, rfid, state) = row
            if str(rfid).lower() == 'none':
                rfid = ''
            
            slotInfo['rank'] = rank
            slotInfo['rfid'] = rfid
            slotInfo['state'] = state
        
        return slotInfo

    
    def getChannelForMachine(self):
        channelInfo = { }
        
        try:
            funcName = 'getMachineChannelInfo'
            params = { }
            resultDic = self.getRemoteData(funcName, params)
            if resultDic:
                if resultDic['result'].lower() == 'ok':
                    channelInfo = resultDic['zdata']
                    channelId = channelInfo.get('channel_id')
                    if channelId:
                        if channelInfo.get('default'):
                            channelId = 'Default Channel'
                        
                        dbChannelId = str(self._getKioskInfoByKey('UMGChannel'))
                        if channelId != dbChannelId:
                            sql = "UPDATE info SET value='%s' WHERE variable='UMGChannel';"
                            sql = sql % sqlQuote(channelId)
                            self.mkcDb.update(sql)
                            funcName = 'dbSyncScript'
                            dbFile = 'machines/%s.db' % self.kioskId
                            params = {
                                'scripts': sql,
                                'db_file': dbFile }
                            self.syncData(funcName, params)
                        
                    
                else:
                    self.log.error('error in getChannelForMachine(remote): %s' % resultDic['zdata'])
        except Exception as ex:
            self.log.error('error in getChannelForMachine: %s' % str(ex))

        return channelInfo

    
    def getInDiscs(self):
        return self._getDiscsByDiscState("('in')")

    
    def _getDiscsByDiscState(self, discState):
        sql = 'SELECT S.id, S.rfid FROM slots AS S, rfids AS R WHERE S.rfid=R.rfid and R.state IN %s;'
        sql = sql % discState
        rows = self.mkcDb.query(sql)
        return rows

    
    def logMkcEvent(self, **params):
        category = params.get('category', '')
        action = params.get('action', '')
        data1 = params.get('data1', '')
        data2 = params.get('data2', '')
        data3 = params.get('data3', '')
        data4 = params.get('data4', '')
        data5 = params.get('data5', '')
        result = params.get('result', '')
        state = params.get('state', 'open')
        eventId = self.logEvent(category = category, action = action, data1 = data1, data2 = data2, data3 = data3, data4 = data4, data5 = data5, result = result, state = state)
        eventInfo = self._getEventByEventId(eventId)
        self.syncData('dbSyncLogEvent', {
            'event_info': eventInfo })

    
    def getSlotIds(self, column = '', stateList = []):
        '''
        @Params: column(string): "" -> All
                                 "1" -> 101~170 / 101~240
                                 "2" -> 228~270 / 354~440
                                 "5" -> 501~570 / 501~640
                                 "6" -> 601~670 / 701~840
                                 "front" -> 101~270(all front slots) / 101~440
                                 "back" -> 501~670(all back slots) / 501~840
                 stateList(list)
        @Return: slotIds(list)

        get slot ids by column
        '''
        slotIds = []
        sql = 'SELECT id FROM slots %s;'
        strWhere = 'WHERE 1=1'
        if column:
            if str(column).isdigit():
                capacityType = str(getKioskCapacity())
                if capacityType == '250':
                    strWhere += " AND id LIKE '%s%%'" % column
                elif str(column) == '1':
                    strWhere += ' AND id<300'
                elif str(column) == '2':
                    strWhere += ' AND id>300 AND id<500'
                elif str(column) == '5':
                    strWhere += ' AND id>500 AND id<700'
                elif str(column) == '6':
                    strWhere += ' AND id>700 AND id<900'
                
            elif str(column).lower() == 'front':
                strWhere += ' AND id<500'
            elif str(column).lower() == 'back':
                strWhere += ' AND id>500'
            
        
        if stateList:
            if len(stateList) == 1:
                strStateList = "('" + str(stateList[0]) + "')"
            else:
                strStateList = str(tuple(stateList))
            strWhere += ' AND state IN %s' % strStateList
        
        sql = sql % strWhere
        rows = self.mkcDb.query(sql)
        slotIds = [ itm[0] for itm in rows ]
        return slotIds

    
    def getSmartLoadSlotId(self, oSlotId):
        '''
        @Params: oSlotId(string)
        @Return: slotId(string)

        get smart load slot id
        '''
        slotId = oSlotId
        sql = "SELECT MIN(id) FROM slots WHERE id<500 AND state='empty' LIMIT 1;"
        row = self.mkcDb.query(sql, 'one')
        if row:
            (slotId,) = row
        
        if not slotId:
            slotId = oSlotId
        
        return slotId

    
    def setKioskOffsetSettingsFromServer(self):
        '''
        @Params: None
        @Return: None

        set kiosk offset settings from server
        distinct1, distinct2, top_offset, back_offset, exchange_offset
        '''
        errorMsg = ''
        
        try:
            funcName = 'getKioskOffsetSettings'
            params = { }
            resultDic = self.getRemoteData(funcName, params)
            if resultDic:
                if resultDic['result'].lower() == 'ok':
                    settings = resultDic['zdata']
                    if settings:
                        self.setConfig(settings)
                    
                else:
                    self.log.error('error in getKioskOffsetSettings(remote): %s' % resultDic['zdata'])
                    errorMsg = 'Fetching kiosk offset settings from server failed: %s' % resultDic['zdata']
        except Exception as ex:
            self.log.error('error in getKioskOffsetSettings: %s' % str(ex))
            errorMsg = 'Fetching kiosk offset settings from server failed: %s' % str(ex)

        if errorMsg:
            
            try:
                self.emailAlert(self, 'PRIVATE', errorMsg, critical = UNCRITICAL)
            except:
                pass

        

    
    def setExternalIP(self, externalIP):
        '''
        @Params: externalIP (string)
        @Return: None

        set machine info: ExternalIP
        '''
        
        try:
            sql = "UPDATE info SET value=? WHERE variable='ExternalIP';"
            self.mkcDb.update(sql, (externalIP,))
            changes = {
                'ExternalIP': externalIP }
            self.syncData('dbSyncInfo', {
                'changes': changes })
        except Exception as ex:
            self.log.error('error in setExternalIP: %s' % str(ex))


    
    def setHDMI(self, status):
        '''
        @Params: status (string): on / off
        @Return: None

        set machine info: HDMI
        '''
        
        try:
            sql = "UPDATE info SET value=? WHERE variable='HDMI';"
            self.mkcDb.update(sql, (status,))
            self.syncData('dbSyncHDMI', {
                'status': status })
        except Exception as ex:
            self.log.error('error in setHDMI: %s' % str(ex))


    
    def saveCustomterBehavior(self, operateType, startTime, endTime):
        '''
        @Params: operateType (string), startTime (string), endTime (string)
        @Return: None

        '''
        
        try:
            sql = 'INSERT INTO customer_behavior(operate_type, start_time, end_time) VALUES(?, ?, ?);'
            self.mkcDb.update(sql, (operateType, startTime, endTime))
            funcName = 'dbSyncCustomerBehavior'
            params = { }
            params['operate_type'] = operateType
            params['start_time'] = startTime
            params['end_time'] = endTime
            self.syncData(funcName, params)
        except Exception as ex:
            self.log.error('error in saveCustomterBehavior: %s' % str(ex))


    
    def saveCardRead(self, readState):
        '''
        @Params: readState (string)
        @Return: None

        '''
        
        try:
            sql = "INSERT INTO card_read(read_time, state) VALUES(DATETIME('now', 'localtime'), ?);"
            self.mkcDb.update(sql, (readState,))
        except Exception as ex:
            self.log.error('error in saveCardRead: %s' % str(ex))


    
    def downloadServerDB(self, kioskId):
        '''
        @Params: kioskId (string)
        @Return: None

        '''
        
        try:
            self.getRemoteData('downloadServerDB', {
                'mac': getEthMac() })
        except Exception as ex:
            self.log.error('error in downloadServerDB: %s' % str(ex))


    
    def getPickUpListForMember(self, shoppingCart, ccIds):
        '''
        @Params: shoppingCart (object), ccIds (list)
        @Return: None

        get pick up list by ccId list(for a member)
        '''
        pickUpList = []
        self.log.info('pick up, ccids: %s' % str(ccIds))
        if len(ccIds) == 1:
            strCcIds = "('%s')" % ccIds[0]
        else:
            strCcIds = str(tuple(ccIds))
        sql = "SELECT S.id, V.id, R.rfid, R.upc, R.title, R.genre, R.movie_id, V.gene, V.cc_id, V.upg_id, V.price_plan, V.price_plan_text, V.coupon_code, V.coupon_plan, V.coupon_text, V.ms_keep_days FROM rfids AS R, reservations AS V, slots AS S WHERE R.rfid=V.rfid AND S.rfid=R.rfid AND V.state='reserved' AND R.state='reserved' AND V.cc_id IN %s;"
        sql = sql % strCcIds
        rows = self.mkcDb.query(sql)
        self.log.info('pick up, count: %s' % len(rows))
        ccId = ''
        if rows:
            for row in rows:
                (slotId, id, rfid, upc, title, genre, movieId, gene, ccId, upgId, pricePlan, pricePlanText, couponCode, couponPlan, couponText, msKeepDays) = row
                picName = self._formPicName(movieId)
                disc = Disc()
                disc.reserveID = id
                disc.rfid = rfid
                disc.upc = upc
                disc.title = title
                disc.genre = genre
                disc.picture = picName
                disc.slotID = slotId
                disc.gene = gene
                disc.upgID = upgId
                disc.msKeepDays = msKeepDays
                disc.coupon.couponCode = couponCode
                disc.coupon.couponData = couponPlan
                disc.coupon.shortDes = couponText
                self.loadDiscInfo(disc, rfid)
                shoppingCart.addDisc(disc)
            
        
        return ccId

    
    def getTransactionListForMember(self, ccIds):
        '''
        @Params: ccIds (list)
        @Return: trsList (list[dict])

        get transaction list by ccId list(for a member)
        '''
        trsList = []
        self.log.info('trs list, ccids: %s' % str(ccIds))
        if len(ccIds) == 1:
            strCcIds = "('%s')" % ccIds[0]
        else:
            strCcIds = str(tuple(ccIds))
        sql = 'SELECT id, title, upc, amount, out_time, in_time, state, gene, price_plan_text FROM transactions WHERE cc_id IN %s;'
        sql = sql % strCcIds
        rows = self.mkcDb.query(sql)
        self.log.info('trs list, count: %s' % len(rows))
        if rows:
            for row in rows:
                data = { }
                data['id'] = row[0]
                data['movie_title'] = row[1]
                data['upc'] = row[2]
                movieInfo = self._getMovieInfo(row[2])
                data['movie_pic'] = movieInfo.get('movie_pic')
                data['price'] = row[3]
                data['out_time'] = row[4]
                data['in_time'] = row[5]
                data['state'] = row[6]
                data['type'] = row[7]
                data['price_plan_text'] = row[8]
                trsList.append(data)
            
        
        return trsList

    
    def update_failed_trs(self, params):
        title = params['title']
        rfid = params['rfid']
        upc = params['upc']
        action_time = params['action_time']
        action_type = params['action_type']
        slot_id = params['slot_id']
        cc_display = params['cc_display']
        state = 'open'
        video_name = params['video_name']
        video_url = params['video_url']
        error_msg = params['error_msg']
        self.log.info('failed_trs: title: %s,slot: %s, video_url: %s' % (title, slot_id, video_url))
        sql = 'INSERT INTO failed_trs(rfid, upc, title, action_time, action_type, slot_id, cc_display, state,video_name, video_url, error_msg) VALUES(?,?,?,?,?,?,?,?,?,?,?);'
        self.mkcDb.update(sql, (rfid, upc, title, action_time, action_type, slot_id, cc_display, state, video_name, video_url, error_msg))

    
    def change_slots_state(self, action, slot_id):
        self.log.info('change slots state %s  %s' % (slot_id, action))
        if action == 'mark as bad':
            sql = 'SELECT rfid,state FROM slots WHERE id = ?;'
            row = self.mkcDb.query(sql, 'one', (slot_id,))
            if row:
                result = row
            
            if result[1] == 'empty':
                sql = "UPDATE slots SET state = 'bad' WHERE id = ?;"
                self.mkcDb.update(sql, (slot_id,))
            elif result[1] == 'occupied':
                sql = "UPDATE rfids SET state = 'bad' WHERE rfid = ?;"
                self.mkcDb.update(sql, (result[0],))
            
        elif action == 'clear':
            sql = "UPDATE slots SET state = 'empty' WHERE id = ?;"
            self.mkcDb.update(sql, (slot_id,))
        

    
    def get_all_slots_status(self, _filter = 'all', current_code = 'admin'):
        '''
        _filter ["all","bad","empty", slot_id]
        slots state {empty, occupied, bad}
        rfid state {in, out, bad, unload, reserved}
        return [{"slot_id":"","status":"","action_1":"","action_2":""},...]
        '''
        self.log.info('get slot status %s' % _filter)
        zdata = []
        s_qtn = {
            'all': 0,
            'bad': 0,
            'empty': 0 }
        sql = 'SELECT id,rfid,state FROM slots;'
        rows = self.mkcDb.query(sql)
        sql = 'SELECT rfid,state FROM rfids;'
        rfid_rows = self.mkcDb.query(sql)
        rd = dict(rfid_rows)
        if rows:
            for row in rows:
                data = { }
                data['slot_id'] = row[0]
                data['status'] = ''
                data['action_1'] = ''
                data['action_2'] = ''
                data['rfid'] = ''
                s_qtn['all'] += 1
                if row[2] == 'bad':
                    data['status'] = 'bad empty slot'
                    data['action_2'] = 'Clear'
                    s_qtn['bad'] += 1
                elif row[2] == 'empty':
                    data['status'] = 'empty'
                    data['action_1'] = 'Mark as Bad'
                    if current_code == 'admin':
                        data['action_2'] = 'Load'
                    
                    s_qtn['empty'] += 1
                elif row[2] == 'occupied':
                    rf_state = rd[row[1]]
                    data['rfid'] = row[1]
                    if row[1] in rd:
                        if rf_state == 'in':
                            data['status'] = 'in'
                            data['action_1'] = 'Mark as Bad'
                            data['action_2'] = 'Unload'
                        elif rf_state == 'unload':
                            data['status'] = 'in'
                            data['action_1'] = 'Mark as Bad'
                            data['action_2'] = 'Unload'
                        elif rf_state in ('out', 'reserved'):
                            data['status'] = rf_state
                        elif rf_state == 'bad':
                            data['status'] = 'bad rfid'
                            data['action_2'] = 'Unload'
                            s_qtn['bad'] += 1
                        
                    else:
                        data['status'] = 'bad'
                        self.log.error('get_all_slots_status error, slot %s no rfid found in rfids' % row[2])
                
                if _filter == 'bad' and data['status'] in [
                    'bad empty slot',
                    'bad rfid']:
                    zdata.append(data)
                elif _filter == 'empty' and data['status'] == 'empty':
                    zdata.append(data)
                elif _filter == 'all':
                    zdata.append(data)
                elif str(data['slot_id']) == _filter:
                    zdata.append(data)
                
            
        
        print(zdata)
        self.log.info('get slot status lengh %s' % len(zdata))
        return (s_qtn, zdata)


if __name__ == '__main__':
    p = ConnProxy.getInstance()
    customer = Customer()
    customer.ccid = 1
    coupon = Coupon()
    coupon.couponCode = '333333333'
    disc = Disc()
    disc.rfid = '00FDB12730000104E0'
    disc.upc = '043396292154'
    disc.movieID = 12345
    disc.slotID = '120'
    disc.title = 'Wackness (2008)'
    disc.genre = 'Comedy'
    disc.preauthAmount = '10'
    disc.rentalPrice = '0'
    disc.salePrice = '30'
    disc.saleConvertPrice = '35'
    disc.saleTax = '10%'
    disc.rentalTax = '20%'
    disc.preauthAnoubt = '30'
    disc.reserveID = ''
    disc.coupon = coupon
    disc.gene = 'rent'
    disc.outKioskID = 'S250-A912'
    disc.upgID = '-1'
    disc.pricePlanID = '1'
    disc.cost = '20'
    shoppingCart = ShoppingCart()
    shoppingCart.addDisc(disc)
    '\n    import copy\n    shoppingCart.addDisc(copy.deepcopy(disc))\n    shoppingCart.addDisc(copy.deepcopy(disc))\n    shoppingCart.addDisc(copy.deepcopy(disc))\n    shoppingCart.addDisc(copy.deepcopy(disc))\n    '
    print(coupon)
    print(shoppingCart)
    del p

