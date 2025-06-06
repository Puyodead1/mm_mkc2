# Source Generated with Decompyle++
# File: auto_reduce.pyc (Python 2.5)

'''
    Change Log:
        2009-10-23 Created by Kitch
            automatic reduction of sale price
'''
import os
import sys
import time
import threading
from .tools import getCurTime, getTimeChange, getLog, sqlQuote, fmtMoney, isLocked
from .config import *
from .conn_proxy import ConnProxy

class AutoReduction(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self, name = 'Auto_Reduction')
        self._stopEvent = threading.Event()
        self._sleepPeriod = 3600

    
    def run(self):
        self.log = getLog('auto_reduce.log', 'AUTO_REDUCE')
        self.proxy = ConnProxy.getInstance()
        while True:
            self.reduceSalePrice()
            time.sleep(self._sleepPeriod)

    
    def join(self, timeout = None):
        self._stopEvent.set()
        threading.Thread.join(self, timeout)

    
    def _getThreadLock(self):
        return isLocked()

    
    def reduceSalePrice(self):
        '''
        auto reduce the sale price
        '''
        
        try:
            lock = self._getThreadLock()
            print('lock: ', lock)
            if str(lock) == '0':
                sql = 'SELECT rfid, sales_price, reduce_formula, last_reduce_date FROM rfids WHERE enable_reduce=1;'
                rows = self.proxy.mkcDb.query(sql)
                if rows:
                    for rfid, salesPrice, reduceFormula, lastReduceDate in rows:
                        formulaPeices = reduceFormula.split(',')
                        reduceInterval = int(formulaPeices[0])
                        reduceAmount = formulaPeices[1]
                        minimalPrice = formulaPeices[2]
                        if float(salesPrice) > float(minimalPrice):
                            today = getCurTime('%Y-%m-%d')
                            if lastReduceDate == '' or getTimeChange(lastReduceDate, day = reduceInterval) <= today:
                                reducedPrice = float(salesPrice) - float(reduceAmount)
                                self.log.info('sale_price: %s, %s' % (rfid, reducedPrice))
                                if float(reducedPrice) < float(minimalPrice):
                                    reducedPrice = fmtMoney(minimalPrice)
                                else:
                                    reducedPrice = fmtMoney(reducedPrice)
                                sql = 'UPDATE rfids SET sales_price=?, last_reduce_date=? WHERE rfid=?;'
                                self.proxy.mkcDb.update(sql, (reducedPrice, today, rfid))
                                params = { }
                                params['rfid'] = rfid
                                params['sale_price'] = reducedPrice
                                params['last_reduce_date'] = today
                                self.proxy.syncData('dbSyncReduceSalePrice', params)
                            
                        
                    
                
                sql = 'SELECT rfid, sale_convert_price, reduce_formula_convert_price, last_reduce_date_convert_price FROM rfids WHERE enable_reduce_convert_price=1;'
                rows = self.proxy.mkcDb.query(sql)
                if rows:
                    for rfid, saleConvertPrice, reduceFormula, lastReduceDate in rows:
                        formulaPeices = reduceFormula.split(',')
                        reduceInterval = int(formulaPeices[0])
                        reduceAmount = formulaPeices[1]
                        minimalPrice = formulaPeices[2]
                        if float(saleConvertPrice) > float(minimalPrice):
                            today = getCurTime('%Y-%m-%d')
                            if lastReduceDate == '' or getTimeChange(lastReduceDate, day = reduceInterval) <= today:
                                reducedPrice = float(saleConvertPrice) - float(reduceAmount)
                                self.log.info('sale_convert_price: %s, %s' % (rfid, reducedPrice))
                                if float(reducedPrice) < float(minimalPrice):
                                    reducedPrice = fmtMoney(minimalPrice)
                                else:
                                    reducedPrice = fmtMoney(reducedPrice)
                                sql = 'UPDATE rfids SET sale_convert_price=?, last_reduce_date_convert_price=? WHERE rfid=?;'
                                self.proxy.mkcDb.update(sql, (reducedPrice, today, rfid))
                                params = { }
                                params['rfid'] = rfid
                                params['sale_convert_price'] = reducedPrice
                                params['last_reduce_date'] = today
                                self.proxy.syncData('dbSyncReduceSaleConvertPrice', params)
                            
                        
                    
                
        except IOError as ex:
            self.log.error('reduceSalePrice in auto_reduce(IOError): %s' % str(ex))
            if str(ex).lower().find('broken pipe') >= 0:
                sys.exit()
            
        except Exception as ex:
            self.log.error('reduceSalePrice in auto_reduce: %s' % str(ex))




def main():
    ar = AutoReduction()
    ar.start()

if __name__ == '__main__':
    main()

