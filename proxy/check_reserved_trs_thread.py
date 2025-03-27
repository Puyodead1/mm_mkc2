# Source Generated with Decompyle++
# File: check_reserved_trs_thread.pyc (Python 2.5)

'''
    Change Log:
        2009-11-25 Modified by Kitch
            check Monthly Subscription
        2009-06-10 Modified by Kitch
            add fields upc, title, genre, price_plan, price_plan_text,
            coupon_code, coupon_plan, coupon_text to table reservations
        2009-01-04 Modified by Kitch
            Add sale convert price
        2008-12-24 Modified by Kitch
            Add thread: check auto convert sale transactions
        2008-10-30 Modified by Kitch
            Charge the member if the reservation expires after 12 hours 
        2008-08-01 Created by Kitch
            check reserved thread.
'''
import os
import sys
import time
from . import uuid
import threading
from .tools import getCurTime, getTimeChange, getLog, sqlQuote, fmtMoney, isLocked
from .config import *
from .conn_proxy import ConnProxy
from .ums_proxy import UmsProxy
from .price_coupon_kiosk import PricePlanEngine
RESERVE_SYNC_FAILED_RFID_FILE = os.path.join(USER_ROOT, 'kiosk/tmp/RESERVE-SYNC-FAILED-RFID')

class CheckReservedTrsThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self, name = 'Check_Reserved')
        self._stopEvent = threading.Event()
        self._sleepPeriod = CHECK_RESERVED_SLEEP_PERIOD

    
    def run(self):
        self.log = getLog('check_reserved_trs_thread.log', 'CHECK_RESERVED_TRS_THREAD')
        self.proxy = ConnProxy.getInstance()
        
        try:
            if os.path.exists(RESERVE_SYNC_FAILED_RFID_FILE):
                f = open(RESERVE_SYNC_FAILED_RFID_FILE)
                rfid = f.read()
                f.close()
                if rfid:
                    params = { }
                    trsInfo = self.proxy._getTrsInfoByRfidState(rfid, 'pending')
                    shoppingCartInfo = self.proxy._getShoppingCartInfoById(trsInfo['shopping_cart_id'])
                    params['shopping_cart_info'] = shoppingCartInfo
                    params['trs_info'] = trsInfo
                    self.proxy.syncData('dbSyncReserveExpired', params)
                    os.remove(RESERVE_SYNC_FAILED_RFID_FILE)
                
        except:
            pass

        while True:
            self.checkReserved()
            self.checkSaleConvertTrs()
            self.clearOverCapacity()
            time.sleep(self._sleepPeriod)

    
    def join(self, timeout = None):
        self._stopEvent.set()
        threading.Thread.join(self, timeout)

    
    def _getThreadLock(self):
        return isLocked()

    
    def checkReserved(self):
        '''
        check reserved
        '''
        rfid = None
        
        try:
            lock = self._getThreadLock()
            print('lock: ', lock)
            if str(lock) == '0':
                expirationTime = 0
                
                try:
                    expirationTime = int(self.proxy._getConfigByKey('reservation_expiration'))
                except:
                    pass

                if not expirationTime:
                    expirationTime = 720
                
                print('expirationTime: ', expirationTime)
                print('get reserve info...')
                sql = "SELECT R.id, R.rfid, R.upc, R.title, R.genre, R.cc_id, R.upg_id, R.reserve_time, R.price_plan, R.price_plan_text, R.coupon_code, R.coupon_plan, R.coupon_text, R.state, R.ms_keep_days, R.ms_id, C.display FROM reservations AS R, cc AS C WHERE R.state='reserved' AND R.cc_id=C.id;"
                rows = self.proxy.mkcDb.query(sql)
                if rows:
                    for row in rows:
                        (reserveId, rfid, upc, title, genre, ccId, upgId, reserveTime, pricePlan, pricePlanText, couponCode, couponPlan, couponText, state, msKeepDays, msId, ccDisplay) = row
                        curTime = getCurTime()
                        validReserveTime = getTimeChange(curTime, minute = -expirationTime)
                        if reserveTime < validReserveTime:
                            print('Expired: ', rfid)
                            sqlList = []
                            sqlUpdate = "UPDATE rfids SET state='in' WHERE state='reserved' AND rfid='%s';"
                            sqlList.append(sqlUpdate % sqlQuote(rfid))
                            sqlUpdate = "UPDATE reservations SET state='expired' WHERE state='reserved' AND rfid='%s';"
                            sqlList.append(sqlUpdate % sqlQuote(rfid))
                            shcrtId = str(uuid.uuid4())
                            sql = "INSERT INTO shopping_carts(id, cc_id, time_open, coupon_code, coupon_plan) VALUES('%s', '%s', '%s', '', '');"
                            sqlList.append(sql % (sqlQuote(shcrtId), ccId, curTime))
                            salesTax = self.proxy._getConfigByKey('sales_tax')
                            rentalTax = self.proxy._getConfigByKey('rentals_tax')
                            slotId = self.proxy._getSlotIdByRfid(rfid)
                            rfidInfo = self.proxy._getRfidInfoByRfid(rfid)
                            salesPrice = float(rfidInfo['sale_convert_price'])
                            salesPrice = fmtMoney(salesPrice * (1 + float(salesTax) / 100))
                            outTime = curTime
                            inTime = getTimeChange(curTime, second = 1)
                            if not pricePlan:
                                pricePlanId = rfidInfo['price_plan_id']
                                priceInfo = self.proxy._getPricePlanById(pricePlanId)
                                pricePlan = priceInfo['data']
                                pricePlanText = priceInfo['data_text']
                            
                            upgAccountId = self.proxy._getConfigByKey('upg_acct_id')
                            sql = 'SELECT display FROM cc WHERE id=?;'
                            ccDisplay = ''
                            
                            try:
                                (ccDisplay,) = self.proxy.mkcDb.query(sql, 'one', (ccId,))
                            except:
                                pass

                            if msKeepDays:
                                amount = fmtMoney(0)
                                msExpiTime = getTimeChange(outTime, day = int(msKeepDays))
                            else:
                                ppe = PricePlanEngine(pricePlan, {
                                    'out_time': outTime,
                                    'in_time': inTime })
                                amount = ppe.calculate()
                                amount = amount * (1 + float(rentalTax) / 100)
                                sp = float(rfidInfo['sales_price']) * (1 + float(salesTax) / 100)
                                if amount >= sp and sp > 0:
                                    amount = sp
                                
                                amount = fmtMoney(amount)
                                msExpiTime = ''
                            sql = "INSERT INTO transactions(rfid, upc, title, genre, amount, sales_tax, out_time, in_time, state, gene, slot_id, cc_id, sale_price, price_plan, price_plan_text, coupon_code, coupon_plan, coupon_text, coupon_usage_state, upg_id, shopping_cart_id, reserve_id, upg_account_id, in_kiosk, ms_expi_time, cc_display) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 'pending', 'rent', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '', '%s', '%s', '%s', '%s', '%s', '%s', '%s');"
                            params = (rfid, upc, sqlQuote(title), sqlQuote(genre), amount, rentalTax, outTime, inTime, slotId, ccId, salesPrice, sqlQuote(pricePlan), sqlQuote(pricePlanText), couponCode, sqlQuote(couponPlan), sqlQuote(couponText), upgId, sqlQuote(shcrtId), reserveId, upgAccountId, sqlQuote(self.proxy.kioskId), sqlQuote(msExpiTime), sqlQuote(ccDisplay))
                            sqlList.append(sql % params)
                            self.proxy.mkcDb.updateTrs(sqlList)
                            
                            try:
                                params = { }
                                trsInfo = self.proxy._getTrsInfoByRfidState(rfid, 'pending')
                                shoppingCartInfo = self.proxy._getShoppingCartInfoById(shcrtId)
                                params['shopping_cart_info'] = shoppingCartInfo
                                params['trs_info'] = trsInfo
                                self.proxy.syncData('dbSyncReserveExpiredV4', params)
                                if msExpiTime and msExpiTime >= curTime:
                                    umsProxy = UmsProxy.getInstance()
                                    umsProxy._setMonthlySubscptCount(msId, trsInfo['id'], outTime, ccId, ccDisplay)
                            except Exception:
                                ex = None
                                f = open(RESERVE_SYNC_FAILED_RFID_FILE, 'w')
                                f.write(str(rfid))
                                f.close()
                                self.log.error('checkReserved in check_reserved(dbSync): %s' % str(ex))

                            self.proxy._checkShoppingCartClosed(shcrtId, inTime)
                        
                    
                
        except IOError:
            ex = None
            if rfid:
                f = open(RESERVE_SYNC_FAILED_RFID_FILE, 'w')
                f.write(str(rfid))
                f.close()
            
            self.log.error('checkReserved in check_reserved(IOError): %s' % str(ex))
            if str(ex).lower().find('broken pipe') >= 0:
                sys.exit()
            
        except Exception:
            ex = None
            self.log.error('checkReserved in check_reserved: %s' % str(ex))


    
    def checkSaleConvertTrs(self):
        '''
        check auto convert sale transactions
        '''
        
        try:
            lock = self._getThreadLock()
            print('lock: ', lock)
            if str(lock) == '0':
                saleConvertDays = 0
                
                try:
                    saleConvertDays = int(self.proxy._getConfigByKey('sale_convert_days'))
                except:
                    saleConvertDays = 14

                print('saleConvertDays: ', saleConvertDays)
                saleTax = self.proxy._getConfigByKey('sales_tax')
                saleTax = str(saleTax).replace("'", "''")
                print('get trs info...')
                sqlSelect = "SELECT id, rfid, upc, title, sales_tax, out_time, sale_price, price_plan, ms_expi_time FROM transactions WHERE state='open';"
                rows = self.proxy.mkcDb.query(sqlSelect)
                convertList = []
                rfidList = []
                if rows:
                    sql1 = "UPDATE transactions SET in_time='%s', amount='%s', sales_tax='%s', gene='sale', state='pending' WHERE id='%s';"
                    sql2 = "UPDATE slots SET rfid='', state='empty' WHERE rfid='%s';"
                    sql3 = "DELETE FROM rfids WHERE rfid='%s';"
                    sql4 = "DELETE FROM over_capacity_rfids WHERE rfid='%s';"
                    for trsId, rfid, upc, title, rentalTax, outTime, salePrice, pricePlan, msExpiTime in rows:
                        curTime = getCurTime()
                        if msExpiTime:
                            outTime = msExpiTime
                        
                        if saleConvertDays > 0:
                            validRentTime = getTimeChange(curTime, day = -saleConvertDays)
                            if outTime < validRentTime:
                                print('convert: ', trsId, rfid)
                                sqlList = []
                                sqlList.append(sql1 % (curTime, salePrice, saleTax, trsId))
                                sqlList.append(sql2 % rfid.replace("'", "''"))
                                sqlList.append(sql3 % rfid.replace("'", "''"))
                                sqlList.append(sql4 % rfid.replace("'", "''"))
                                self.proxy.mkcDb.updateTrs(sqlList)
                                convertList.append((curTime, salePrice, saleTax, trsId))
                                rfidList.append(rfid)
                                self.proxy.checkUPCStock(upc, title)
                            
                        else:
                            ppe = PricePlanEngine(pricePlan, {
                                'out_time': outTime,
                                'in_time': curTime })
                            rentalPrice = ppe.calculate()
                            rentalPrice = rentalPrice * (1 + float(rentalTax) / 100)
                            if float(rentalPrice) >= float(salePrice):
                                print('convert: ', trsId, rfid)
                                sqlList = []
                                sqlList.append(sql1 % (curTime, salePrice, saleTax, trsId))
                                sqlList.append(sql2 % rfid.replace("'", "''"))
                                sqlList.append(sql3 % rfid.replace("'", "''"))
                                sqlList.append(sql4 % rfid.replace("'", "''"))
                                self.proxy.mkcDb.updateTrs(sqlList)
                                convertList.append((curTime, salePrice, saleTax, trsId))
                                rfidList.append(rfid)
                                self.proxy.checkUPCStock(upc, title)
                            
                    
                
                if convertList:
                    for i in range(5):
                        
                        try:
                            params = {
                                'convert_list': convertList,
                                'rfid_list': rfidList }
                            self.proxy.syncData('dbSyncSaleConvertV2', params)
                        except Exception:
                            ex = None
                            self.log.error('checkSaleConvertTrs in check_reserved(%s): %s' % (i, str(ex)))
                            print(str(ex))
                            time.sleep(5)

                    
                
        except IOError:
            ex = None
            if str(ex).lower().find('broken pipe') >= 0:
                sys.exit()
            
        except Exception:
            ex = None
            self.log.error('checkSaleConvertTrs in check_reserved: %s' % str(ex))
            print(str(ex))


    
    def clearOverCapacity(self):
        ''' move over capacity rfids to empty slots if there is any empty slot
        '''
        emptySlots = self.proxy.getSlotIds(stateList = [
            'empty'])
        while emptySlots:
            sql = 'SELECT rfid FROM over_capacity_rfids LIMIT 1;'
            row = self.proxy.mkcDb.query(sql, 'one')
            if not row:
                break
            else:
                (rfid,) = row
                slotId = emptySlots[0]
                sqlList = []
                sql = "UPDATE slots SET rfid='%s', state='occupied' WHERE id='%s';"
                sqlList.append(sql % (rfid.replace("'", "''"), slotId))
                sql = "DELETE FROM over_capacity_rfids WHERE rfid='%s';"
                sqlList.append(sql % (rfid.replace("'", "''"),))
                self.proxy.mkcDb.updateTrs(sqlList)
                params = {
                    'rfid': rfid,
                    'slot_id': slotId }
                self.proxy.syncData('dbSyncMoveOverCapacity', params)
                emptySlots = self.proxy.getSlotIds(stateList = [
                    'empty'])



def main():
    crs = CheckReservedTrsThread()
    crs.start()

if __name__ == '__main__':
    main()

