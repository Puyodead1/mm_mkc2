# Source Generated with Decompyle++
# File: upg_proxy.pyc (Python 2.5)

'''
    Change Log:
        2011-06-28 Modified by Tim
            remove the logic modified by 2011-06-20
        2011-06-20 Modified by Tim
            add new logic, decline the transaction which is missing the
            wallet reference
        2011-04-01 Modified by Tim
            add new api _check_black_list_for_chip_n_pin for chipNPin
        2011-02-14 Modified by Tim
            form the oid for ChipNPin with merchant subscription reference and PGTR
        2011-02-10 Modified by Tim
            change the api charge_chip_n_pin
        2011-01-28 Modified by Tim
            add a new column cerepay_uuid for table cerepay_topup
        2011-01-27 Modified by Tim
            add a new return value(trsUuid) for topup_for_cerepay
            add new api send_topup_receipt
        2011-01-12 Modified by Tim
            add a new param kioskId for syncDataRemoteKiosk
        2011-01-11 Modified by Tim
            add new apis _update_cerepay_topup_queue, _get_failed_cerepay_topup,
            _add_cerepay_topup_queue
        2010-12-23 Modified by Tim
            add new api chkNeedTrsPasswd
        2010-12-22 Modified by Tim
            add new api chkNeedTrsPasswd
        2010-12-13 Modified by Tim
            add new api chargeCerePayWithoutCard
        2010-12-07 Modified by Tim
            add new apis getCerePayCfgByAcctId, getCerePayUserInfo, 
            cerePayLogin, checkCerePayEmail, registerCerePay
        2010-11-16 Modified by Tim
            add new function getCCInfoFromCacheByCustomer
        2010-09-15 Modified by Tim
            For #2159, separate preauth for blu-ray and games.
            For #2166, new config "Preauth Method" for CerePay card
            For #2127, cc with good credibility always gets partial preauth amount.
            For #2195, charge the customer for R0 when using coupon for ALLPs.
        2010-06-01 Modified by Tim
            For CerePay, add a new optional params "passwd" for upg Trade.
        2010-05-17 Modified by Tim
            For #2095, Charge the customer for R1 when using coupon for ALLPs.
        2010-03-26 Modified by Tim
            Add msDiscType for MS.
        2010-02-22 Modified by Tim
            Change the reqType from "001", "111" to "109" for allps.
        2009-12-11 Modified by Tim
            Add keep days for the monthly subscription.
        2009-11-26 Modified by Tim
            Check if the discs could use the monthly subscription when preauth.
        2009-08-31 Modified by Tim
            Add new function getTrsShoppingCartId().
        2009-07-13 Modified by Tim
            For #1759: preauth amount 0 should skip sending UPG trs.
            For #
        2009-06-04 Modified by Tim
            For #1712:
            1. Delete the PREAUTH from preauth queue after 3 days.
            2. Decline the card if the card has declined trs in declinedq.
        2009-05-18 Modified by Tim
            1. For #1680, decline a card if it will expire in 15 days when PREAUTH.
            2. Delete the PREAUTH from preauth queue after 15 days.
        2009-04-08 Modified by Tim
            Add a params ignore_bl for preauth, postauth and sale.
        2009-03-03 Modified by Tim
            For #1598, Preauth the left amount for rental if rental and sale
            are in the same shopping cart.
            Sync the postauthq.
        2009-02-27 Modified by Tim
            Add prefix "Gateway:" for error message from bank.
        2009-01-05 Modified by Tim
            Add two params for preauthCard method, rentPrice and salePrice
        2008-12-22 Modified by Tim
            For #1519, add some info for gateway error from upg.
        2008-12-19 Modified by Tim
            If both the card number and track2 are empty, do NOT preauth.
        2008-04-17 Created by Tim:
            UPG proxy.
'''
__version__ = '0.4.6'
import base64
import logging
import socket
import http.client
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import threading
import datetime
import time
import traceback
from logging import handlers

try:
    import psyco
    psyco.full()
except:
    pass

from . import allps
from . import chip_n_pin
from .base_proxy import Proxy
from .tools import getCurTime, RemoteError, getTimeChange, getLog
from .tools import fmtMoney, sqlQuote
# from .clisitef import CliSiTef
from .mda import DatabaseError, Db
from .config import *
from .credit_card import *
from ctypes import *
PROXY_NAME = 'UPG_PROXY'

class UPGProxy(Proxy):
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
        super(UPGProxy, self).__del__()

    
    def on_init(self):
        super(UPGProxy, self).__init__(PROXY_NAME)

    
    def __new__(cls, *args, **kwargs):
        if '_inst' not in vars(cls):
            cls._inst = object.__new__(cls, *args, **kwargs)
            cls._inst.on_init()
        
        return cls._inst

    
    def getInstance():
        return UPGProxy()

    getInstance = staticmethod(getInstance)
    
    def preauthCard(self, customer, shoppingCart, zipcode = None, trsPasswd = None):
        """
        @Params: shoppingCart(ShoppingCart Object)
                 customer(Customer Object)
                 zipcode(str): if None, do NOT validate zipcode
                 trsPasswd(str): if None, do NOT validate trsPasswd
        @Return: Success: (status, m)
                 Notes: status = '0': Preauth successfully, approved.
                        status = '1': Card declined.
                        status = '2': Credit card expire in 15 days is not accepted.
                        status = '3': This card is in black list.
                        status = '4': Can not connect upg server.
                        status = '5': Sorry, the kiosk has not set any account.
                        status = '6': payment gateway busy.
                        status = '7': Credit card has expired.
        """
        self._getTestMode()
        if self.UPG_SHOW_MODE:
            shoppingCart.totalCharged = 0
            for disc in shoppingCart.discs:
                disc.upgID = -1
            
            return ('0', '')
        
        status = '4'
        m = 'Sorry, the kiosk has communication issue.'
        
        try:
            if not (customer.ccid):
                s = self.getCCInfoByCustomer(customer)
                if s == 1:
                    raise Exception('Internal error in preauthCard when getCCInfoByCustomer.')
                elif s == 2:
                    raise RemoteError('Remote error in preauthCard when getCCInfoByCustomer.')
                
            
            rentAmount = 0
            saleAmount = 0
            shoppingCart.totalCharged = 0
            if self._getConfigByKey('good_credibility_preauth') == 'partial' and self.getClosedTrsCount(customer.ccid) > 0:
                for disc in shoppingCart.discs:
                    if disc.gene == 'rent':
                        disc.preauthAmount = fmtMoney(self._getPartialAmount(disc))
                    
                
            elif self._getConfigByKey('member_preauth') == 'partial' and customer.email is not None and customer.email != '':
                for disc in shoppingCart.discs:
                    if disc.gene == 'rent':
                        disc.preauthAmount = fmtMoney(self._getPartialAmount(disc))
                    
                
            else:
                cardSuffix = ''
                if str(customer.cardType) == '3':
                    cardSuffix = '_cp'
                
                discSuffix = {
                    'DVD': '',
                    'Blu-Ray': '_br',
                    'Games': '_game' }
                for disc in shoppingCart.discs:
                    if disc.gene == 'rent':
                        suffix = '%s%s' % (cardSuffix, discSuffix[self._UPGProxy__getDiscType(disc)])
                        method = self._getConfigByKey('preauth_method%s' % suffix).lower()
                        if method == 'custom':
                            ca = self._getConfigByKey('preauth_custom_amount%s' % suffix)
                            disc.preauthAmount = fmtMoney(ca)
                        elif method == 'partial':
                            disc.preauthAmount = fmtMoney(self._getPartialAmount(disc))
                        else:
                            disc.preauthAmount = fmtMoney(float(disc.saleConvertPrice) * (1 + float(disc.saleTax.rstrip('%')) / 100))
                    
                
            '\n            usedMonthSubs = 0 # 0: not use\n                              # 1: used\n                              # 2: partial used, error\n                              # 3: ms disc type not matched\n            invalidDiscType = set()\n            validDiscType = set()\n            rentCount = 0 # the rent count of the shopping cart\n            msExpiTime = ""\n            if customer.msID:\n                msDiscType = customer.msDiscType.upper()\n                # check the ms count and ms disc type\n                for disc in shoppingCart.discs:\n                    if disc.gene == "rent":\n                        rentCount += 1\n                        discType = self.__getDiscType(disc)\n                        if discType.upper() not in msDiscType:\n                            invalidDiscType.add(discType)\n                        else:\n                            validDiscType.add(discType)\n\n                if invalidDiscType and validDiscType:\n                    usedMonthSubs = 3\n                elif validDiscType and not invalidDiscType:\n                    usedMonthSubs = 1\n                elif invalidDiscType and not validDiscType:\n                    usedMonthSubs = 0\n\n                if usedMonthSubs in (0, 3):\n                    pass\n                elif rentCount <= customer.msCount:\n                    for disc in shoppingCart.discs:\n                        if disc.gene == "rent":\n                            disc.preauthAmount = "0"\n                            disc.msKeepDays = customer.msKeepDays\n                    msExpiTime = getTimeChange(getCurTime(), day=customer.msKeepDays)\n                    usedMonthSubs = 1\n                else:\n                    usedMonthSubs = 2\n            '
            (usedMonthSubs, msExpiTime, invalidDiscType, rentCount) = self.check_monthly_subscription(customer, shoppingCart)
            for disc in shoppingCart.discs:
                amount = round(float(disc.preauthAmount), 2)
                rentAmount += amount
            
            acctId = self.getUpgAcctId()
            expired = 0
            if customer.cardType != 3:
                expired = self.cardIsExpired(customer.ccExpDate)
            
            if usedMonthSubs == 3:
                status = '14'
                m = '%s|%s' % (', '.join(list(invalidDiscType)), customer.msDiscType)
            elif usedMonthSubs == 2:
                status = '11'
                m = '%s|%s' % (rentCount, customer.msCount)
            elif usedMonthSubs != 1 and str(expired) == '3':
                status = '9'
                m = 'Card read failed, please try again.'
            elif usedMonthSubs != 1 and str(expired) == '1':
                status = '2'
                m = 'Sorry, credit card expire in 15 days is not accepted.'
            elif usedMonthSubs != 1 and str(expired) == '2':
                status = '7'
                m = 'Sorry, credit card has expired.'
            elif usedMonthSubs != 1 and self.cardHasDeclinedTrs(customer.ccid):
                status = '10'
                m = ''
            elif rentAmount >= 0 and rentAmount <= 0:
                for disc in shoppingCart.discs:
                    disc.upgID = 0
                
                if usedMonthSubs == 1:
                    status = '12'
                    m = msExpiTime
                else:
                    status = '0'
                    m = 'Successfully preauth amount 0.'
            elif acctId:
                preauthResult = self.preauth(acctId, customer, rentAmount, zipcode, trsPasswd)
                self.log.info('Preauth result: %s' % preauthResult)
                upgId = int(preauthResult['upgId'])
                statusCode = int(preauthResult['trsCode'])
                trs_msg = preauthResult['trsMsg']
                notGatewayErr = ('INVALID ACCOUNT ID.', 'INVALID TRANSACTION TYPE.')
                if usedMonthSubs == 1:
                    if str(statusCode) == '0':
                        status = '12'
                        m = msExpiTime
                    else:
                        status = '13'
                        m = ''
                elif str(statusCode) == '0':
                    for disc in shoppingCart.discs:
                        disc.upgID = upgId
                    
                    status = '0'
                    m = ''
                elif trs_msg.strip().upper() in notGatewayErr:
                    status = '8'
                    m = 'Sorry, invalid UPG account ID: %s' % acctId
                elif str(statusCode) == '11' and trs_msg.strip().upper().find('DECLINE - BLACK LIST') >= 0:
                    status = '3'
                    m = 'Sorry, this card is in black list.'
                elif trs_msg.strip().upper().startswith('AN ERROR OCCURRED WHEN RUNNING'):
                    status = '6'
                    m = 'Sorry, payment gateway busy.'
                elif str(statusCode) != '0':
                    status = '1'
                    m = 'Gateway: %s' % trs_msg
                else:
                    status = '4'
                if str(status) != '0':
                    postMsg = 'PREAUTH Upg Error Code: %s, PREAUTH Upg error: %s, cc id: %s '
                    self.log.error(postMsg % (preauthResult.get('trsCode', ''), preauthResult.get('trsMsg', ''), customer.ccid))
                else:
                    self.log.info('Preauth successfully for cc id: %s' % customer.ccid)
            else:
                status = '5'
                m = 'Sorry, UPG account has NOT been set.'
            cartStr = 'Preauth for Shopping Cart: Status: %s; ID: %s; totalCharged: %s; coupon code: %s \nDISCS: \n%s'
            discStr = '\n\n'.join(
                'rfid: %s;\n upc: %s;\n slotID: %s;\n title: %s;\n salePrice: %s;\n '
                'preauthAmount: %s;\n reserveID: %s;\n coupon code: %s;\n gene: %s;\n '
                'outKioskID: %s;\n rentalTax: %s;\n saleTax: %s;\n pricePlanID: %s,\n '
                'upgID: %s,\n msExpiTime: %s' % (
                    str(disc.rfid), 
                    str(disc.upc), 
                    str(disc.slotID), 
                    str(disc.title),
                    str(disc.salePrice),
                    str(disc.preauthAmount),
                    str(disc.reserveID),
                    str(disc.coupon.couponCode),
                    str(disc.gene),
                    str(disc.outKioskID),
                    str(disc.rentalTax),
                    str(disc.saleTax),
                    str(disc.pricePlanID),
                    str(disc.upgID),
                    disc.msExpiTime
                )
                for disc in shoppingCart.discs
            )
            self.log.info(cartStr % (status, str(shoppingCart.id), shoppingCart.totalCharged, str(shoppingCart.coupon.couponCode), discStr))
        except DatabaseError as ex:
            errMsg = '[Local] Error occurs when preauth card (%s): %s' % (customer.ccid, ex)
            self.log.error(errMsg)
            status = '4'
            m = 'Sorry, the kiosk has communication issue.'
        except RemoteError as ex:
            errMsg = '[Remote] Error occurs when preauth card (%s): %s' % (customer.ccid, ex)
            self.log.error(errMsg)
            status = '4'
            m = 'Sorry, the kiosk has communication issue.'
        except Exception as ex:
            errMsg = '[Local] Error occurs when preauth card for ccId(%s): %s' % (customer.ccid, ex)
            self.log.error(errMsg)
            status = '4'
            m = 'Sorry, the kiosk has communication issue.'

        return (str(status), m)

    
    def sendReqForSA(self, customer, shoppingCart, acctType):
        '''
        @Params: shoppingCart(ShoppingCart Object)
                 customer(Customer Object)
                 acctType(str): "01" or "02"
                            "01": Savings
                            "02": Current/Cheque
        @Return: Success: (status, m)
                 Notes: status = \'0\': Approved.
                        status = \'1\': The payment params has NOT been set.
                        status = \'2\': The port of payment params is incorrect.
                        status = \'3\': Internal error.
                        status = \'4\': Timeout when connect to ftp server.
                        status = \'5\': Connection refused when connect to ftp server.
                        status = \'6\': Login or password incorrect for ftp server.
                        status = \'7\': Permission denied when create new file to ftp server.
        '''
        self._getTestMode()
        if self.UPG_SHOW_MODE:
            shoppingCart.totalCharged = 0
            for disc in shoppingCart.discs:
                disc.upgID = -1
            
            return ('0', '', 1, 'test-mode-trsIdty')
        
        status = '3'
        m = 'Internal error.'
        seq = 0
        trsIdty = ''
        
        try:
            self.log.info('sendReqForSA: %s' % acctType)
            para = { }
            
            try:
                para = self.getParamsForSA()
            except Exception as ex:
                para = { }
                self.log.error('Error when getParamsForSA: %s' % ex)
                status = '2'
                msg = 'Sorry, the port of payment params is incorrect.'

            if para:
                hasCoupon = False
                if shoppingCart.coupon.couponCode:
                    hasCoupon = True
                else:
                    for disc in shoppingCart.discs:
                        if disc.coupon.couponCode:
                            hasCoupon = True
                            break
                        
                    
                rentAmount = 0
                saleAmount = 0
                amount = 0
                shoppingCart.totalCharged = 0
                customer.cardType = 1
                for disc in shoppingCart.discs:
                    if disc.gene == 'sale':
                        saleAmount += round(float(disc.preauthAmount), 2)
                        amount += saleAmount
                    elif disc.gene == 'rent' and hasCoupon:
                        disc.preauthAmount = fmtMoney(0)
                        amount += 0
                        rentAmount += 0
                    elif disc.gene == 'rent' and not hasCoupon:
                        _preAmount = round(float(disc.rentalPrice) * (1 + float(disc.rentalTax.rstrip('%')) / 100), 2)
                        self.log.info('disc.rentalPrice:%s' % disc.rentalPrice)
                        self.log.info('_preAmount:%s' % _preAmount)
                        disc.preauthAmount = fmtMoney(_preAmount)
                        amount += _preAmount
                        rentAmount += _preAmount
                    
                
                self.log.info('rentAmount:%s' % rentAmount)
                self.log.info('saleAmount:%s' % saleAmount)
                self.log.info('hasCoupon:%s' % hasCoupon)
                obj = allps.Allps(para['ip'], para['port'], para['user'], para['passwd'])
                trsIdty = self.getTrsIdty()
                reqType = '109'
                self.log.info('amount:%s' % amount)
                cents = int(amount * 100 + 0.5)
                (stat, seq) = obj.setImpFile(reqType, trsIdty, acctType, cents)
                self.log.info('stat: %s, seq: %s' % (stat, seq))
                if stat == 0:
                    status = '0'
                elif stat == 1:
                    status = '3'
                    m = 'Internal error.'
                elif stat == 2:
                    status = '4'
                    m = 'Timeout when connect to ftp server.'
                elif stat == 3:
                    status = '5'
                    m = 'Connection refused when connect to ftp server.'
                elif stat == 4:
                    status = '6'
                    m = 'Login or password incorrect for ftp server.'
                elif stat == 5:
                    status = '7'
                    m = 'Permission denied when create new file to ftp server.'
                elif stat == 6:
                    status = '3'
                    m = 'Internal error.'
                
            elif status != '2':
                status = '1'
                m = 'Sorry, the payment params has NOT been set.'
        except Exception as ex:
            errMsg = '[Local] Error occurs when sendReqForSA: %s' % ex
            self.log.error(errMsg)
            status = '3'
            m = 'Internal error.'

        return (str(status), m, seq, trsIdty)

    
    def getResForSA(self, customer, shoppingCart, seq, trsIdty):
        """
        @Params: shoppingCart(ShoppingCart Object)
                 customer(Customer Object)
                 seq(int)
                 trsIdty(str)
        @Return: Success: (status, m)
                 Notes: status = '0': Approved.
                        status = '1': The payment params has NOT been set.
                        status = '2': The port of payment params is incorrect.
                        status = '3': Internal error.
                        status = '4': Timeout when connect to ftp server.
                        status = '5': Connection refused when connect to ftp server.
                        status = '6': Login or password incorrect for ftp server.
                        status = '7': Permission denied when create new file to ftp server.
                        status = '8': Card Declined
                        status = '9': communication issue.
        """
        self._getTestMode()
        if self.UPG_SHOW_MODE:
            shoppingCart.totalCharged = 0
            for disc in shoppingCart.discs:
                disc.upgID = -1
            
            return ('0', '')
        
        status = '3'
        m = 'Internal error.'
        
        try:
            para = { }
            
            try:
                para = self.getParamsForSA()
            except Exception as ex:
                para = { }
                self.log.error('Error when getParamsForSA: %s' % ex)
                status = '2'
                msg = 'Sorry, the port of payment params is incorrect.'

            if para:
                hasCoupon = False
                if shoppingCart.coupon.couponCode:
                    hasCoupon = True
                else:
                    for disc in shoppingCart.discs:
                        if disc.coupon.couponCode:
                            hasCoupon = True
                            break
                        
                    
                rentAmount = 0
                saleAmount = 0
                hasRent = False
                amount = 0
                shoppingCart.totalCharged = 0
                for disc in shoppingCart.discs:
                    if disc.gene == 'sale':
                        saleAmount += round(float(disc.preauthAmount), 2)
                        amount += saleAmount
                    elif disc.gene == 'rent' and hasCoupon:
                        hasRent = True
                        disc.preauthAmount = fmtMoney(1)
                        amount += 1
                        rentAmount += 1
                    elif disc.gene == 'rent' and not hasCoupon:
                        hasRent = True
                        _preAmount = round(float(disc.rentalPrice) * (1 + float(disc.rentalTax.rstrip('%')) / 100), 2)
                        disc.preauthAmount = fmtMoney(_preAmount)
                        amount += _preAmount
                        rentAmount += _preAmount
                    
                
                obj = allps.Allps(para['ip'], para['port'], para['user'], para['passwd'])
                (stat, cardNum, errocode, erromsg, oid) = obj.getExpFile(seq, trsIdty)
                self.log.info('stat: %s' % stat)
                if stat == 0:
                    if str(errocode) == '207':
                        customer.ccNum = cardNum
                        s = self.getCCInfoByCustomer(customer)
                        customer.cardType = 1
                        if s == 1:
                            raise Exception('Internal error in getResForSA when getCCInfoByCustomer.')
                        elif s == 2:
                            raise RemoteError('Remote error in getResForSA when getCCInfoByCustomer.')
                        
                        rentUpgId = 0
                        saleUpgId = 0
                        if hasRent:
                            rentUpgId = self.addToUpg({
                                'amount': fmtMoney(rentAmount),
                                'oid': oid,
                                'resultCode': errocode,
                                'resultMsg': erromsg,
                                'trsType': 'SALE',
                                'acctId': '',
                                'ccId': customer.ccid,
                                'pqId': '',
                                'preauthMethod': 'CUSTOMER',
                                'notes': self.kioskId })
                        elif saleAmount > 0:
                            saleUpgId = self.addToUpg({
                                'amount': fmtMoney(saleAmount),
                                'oid': oid,
                                'resultCode': errocode,
                                'resultMsg': erromsg,
                                'trsType': 'SALE',
                                'acctId': '',
                                'ccId': customer.ccid,
                                'pqId': '',
                                'preauthMethod': 'CUSTOMER',
                                'notes': self.kioskId })
                        
                        for disc in shoppingCart.discs:
                            if disc.gene == 'sale':
                                disc.upgID = saleUpgId
                            elif disc.gene == 'rent':
                                disc.upgID = rentUpgId
                            
                        
                        status = '0'
                    else:
                        status = '8'
                        m = erromsg
                elif stat == 1:
                    status = '3'
                    m = 'Internal error.'
                elif stat == 2:
                    status = '4'
                    m = 'Timeout when connect to ftp server.'
                elif stat == 3:
                    status = '5'
                    m = 'Connection refused when connect to ftp server.'
                elif stat == 4:
                    status = '6'
                    m = 'Login or password incorrect for ftp server.'
                elif stat == 5:
                    status = '7'
                    m = 'Permission denied when create new file to ftp server.'
                elif stat == 6:
                    status = '3'
                    m = 'Internal error.'
                elif stat == 7:
                    status = '10'
                    m = 'Timeout'
                elif stat == 8:
                    status = '10'
                    m = 'Timeout'
                elif stat == 9:
                    status = '10'
                    m = 'Canceled.'
                
                self.log.info('getResForSA for ccid(%s): errocode(%s), erromsg(%s)' % (customer.ccid, errocode, erromsg))
                cartStr = 'getResForSA for Shopping Cart: Status: %s; ID: %s; totalCharged: %s; coupon code: %s; \nDISCS: \n%s'
                discStr = '\n\n'.join(
                    'rfid: %s;\n upc: %s;\n slotID: %s;\n title: %s;\n salePrice: %s;\n '
                    'preauthAmount: %s;\n reserveID: %s;\n coupon code: %s;\n gene: %s;\n '
                    'outKioskID: %s;\n rentalTax: %s;\n saleTax: %s;\n pricePlanID: %s,\n '
                    'upgID: %s,\n msExpiTime: %s' % (
                        str(disc.rfid), 
                        str(disc.upc), 
                        str(disc.slotID), 
                        str(disc.title),
                        str(disc.salePrice),
                        str(disc.preauthAmount),
                        str(disc.reserveID),
                        str(disc.coupon.couponCode),
                        str(disc.gene),
                        str(disc.outKioskID),
                        str(disc.rentalTax),
                        str(disc.saleTax),
                        str(disc.pricePlanID),
                        str(disc.upgID),
                        disc.msExpiTime
                    )
                    for disc in shoppingCart.discs
                )
                self.log.info(cartStr % (status, str(shoppingCart.id), shoppingCart.totalCharged, shoppingCart.coupon.couponCode, discStr))
            elif status != '2':
                status = '1'
                m = 'Sorry, the payment params has NOT been set.'
        except DatabaseError as ex:
            errMsg = '[Local] Error occurs when preauth card (%s): %s' % (customer.ccid, ex)
            self.log.error(errMsg)
            status = '9'
            m = 'Sorry, the kiosk has communication issue.'
        except RemoteError as ex:
            errMsg = '[Remote] Error occurs when getResForSA (%s): %s' % (seq, ex)
            self.log.error(errMsg)
            status = '9'
            m = 'Sorry, the kiosk has communication issue.'
        except Exception as ex:
            errMsg = '[Local] Error occurs when getResForSA (%s): %s' % (seq, ex)
            self.log.error(errMsg)
            status = '9'
            m = 'Sorry, the kiosk has communication issue.'
        except Exception as ex:
            errMsg = '[Local] Error occurs when sendReqForSA: %s' % ex
            self.log.error(errMsg)
            status = '3'
            m = 'Internal error.'

        return (str(status), m)

    
    def getParamsForSiTef(self):
        ''' Get the params for the SiTef.
        @Params: None
        @Return: result(dict): {"ipsitef":xxx,
                                "store_id":xxx,
                                "terminal_id":xxx,
                               }
        '''
        result = { }
        para = self._getConfigByKey('payment_params')
        if para:
            (ip, store_id, terminal_id) = ('', '', '')
            tmp = para.split(',')
            if len(tmp) == 3:
                (ip, store_id, terminal_id) = tmp
            
            result['ip'] = ip
            result['store_id'] = store_id
            result['terminal_id'] = terminal_id
            result['kiosk_id'] = self.kioskId
        
        return result

    
    def getParamsForSA(self):
        ''' Get the params for the SA.
        @Params: None
        @Return: result(dict): {"user":xxx,
                                "ip":xxx,
                                "port":xxx,
                                "passwd":xxx,}
        '''
        result = { }
        para = self._getConfigByKey('payment_params')
        if para:
            (user, ip, port, passwd) = ('', '', 21, '')
            tmp = para.split(' ')
            if len(tmp) == 2:
                passwd = tmp[1]
            
            tmp = tmp[0].split(':')
            if len(tmp) == 2:
                port = int(tmp[1])
            
            tmp = tmp[0].split('@')
            if len(tmp) == 2:
                user = tmp[0]
                ip = tmp[1]
            
            result['user'] = user
            result['ip'] = ip
            result['port'] = port
            result['passwd'] = passwd
        
        return result

    
    def getTrsIdty(self):
        ''' Get the unique transaction record identity per deployed installation
        @Params: None
        @Return: trsIdty(str)
        '''
        return '%s%s' % (self.kioskId.replace('-', ''), getCurTime('%y%m%d%H%M%S'))

    
    def charge_sitef(self, customer, acctId, amount):
        '''
        Charge the amount for chip n pin.
        '''
        # status = '1'
        # m = ''
        # (server, port, baseUrl) = self._getUpgServerFromUrl(self._getConfigByKey('upg_url'))
        # para = self.getParamsForSiTef()
        # obj = CliSiTef(para, self.kioskId, server, port, baseUrl)
        # result = obj.sale(acctId, amount)
        # self.log.info('Transaction result for SiTef: %s' % result)
        # if result.get('status', '') == 0:
        #     status = '0'
        #     card_num = '%s******%s' % (result.get('six_first_num', ''), result.get('last_four_num', ''))
        #     customer.ccNum = card_num
        #     customer.ccNumSHA1 = result.get('card_sha1', '')
        #     customer.ccName = result.get('card_name', '')
        #     customer.ccExpDate = result.get('card_expdate', '')
        #     customer.ccDisplay = '%s (%s)' % (result.get('card_name', ''), result.get('last_four_num', ''))
        #     customer.cardType = 4
        #     oid = '%s--%s' % (result.get('trans_time', '')[4:], result.get('trans_doc', ''))
        #     upgId = self.addToUpg({
        #         'amount': fmtMoney(amount),
        #         'oid': oid,
        #         'resultCode': result.get('status', ''),
        #         'resultMsg': result.get('msg', ''),
        #         'trsType': 'SALE',
        #         'acctId': acctId,
        #         'ccId': customer.ccid,
        #         'pqId': '',
        #         'preauthMethod': 'CUSTOMER',
        #         'notes': self.kioskId,
        #         'additional': '' })
        #     result['upgId'] = upgId
        #     s = self.getCCInfoByCustomer(customer)
        #     if s == 1:
        #         raise Exception('Internal error in chargeForSiTef when getCCInfoByCustomer.')
        #     elif s == 2:
        #         raise RemoteError('Remote error in chargeForSiTef when getCCInfoByCustomer.')
            
        #     self.updateUpgInfoByUpgId({
        #         'upgId': upgId,
        #         'ccId': customer.ccid })
        # else:
        #     status = result.get('status', '')
        #     m = result.get('msg', '')
        # del obj
        # return (status, m, result)
        raise NotImplementedError()

    
    def chargeForSiTef(self, customer, shoppingCart):
        self._getTestMode()
        if self.UPG_SHOW_MODE:
            shoppingCart.totalCharged = 0
            for disc in shoppingCart.discs:
                disc.upgID = -1
            
            return ('0', '')
        
        status = '3'
        
        try:
            acctId = self.getUpgAcctId()
            if acctId:
                rentAmount = 0
                saleAmount = 0
                amount = 0
                shoppingCart.totalCharged = 0
                for disc in shoppingCart.discs:
                    if disc.gene == 'sale':
                        saleAmount += round(float(disc.preauthAmount), 2)
                    elif disc.gene == 'rent':
                        _preAmount = round(float(disc.rentalPrice) * (1 + float(disc.rentalTax.rstrip('%')) / 100), 2)
                        disc.preauthAmount = fmtMoney(_preAmount)
                        rentAmount += _preAmount
                    
                
                amount = rentAmount + saleAmount
                (status, m, result) = self.charge_sitef(customer, acctId, amount)
                if str(status) == '0':
                    for disc in shoppingCart.discs:
                        disc.upgID = result.get('upgId', 0)
                    
                
                self.log.info('chargeForSiTef for ccid(%s): errocode(%s), erromsg(%s)' % (customer.ccid, result.get('status', ''), result.get('message', '')))
                cartStr = 'chargeForSiTef for Shopping Cart: Status: %s; ID: %s; totalCharged: %s; coupon code: %s; \nDISCS: \n%s'
                discStr = '\n\n'.join(
                    'rfid: %s;\n upc: %s;\n slotID: %s;\n title: %s;\n salePrice: %s;\n '
                    'preauthAmount: %s;\n reserveID: %s;\n coupon code: %s;\n gene: %s;\n '
                    'outKioskID: %s;\n rentalTax: %s;\n saleTax: %s;\n pricePlanID: %s,\n '
                    'upgID: %s,\n msExpiTime: %s' % (
                        str(disc.rfid), 
                        str(disc.upc), 
                        str(disc.slotID), 
                        str(disc.title),
                        str(disc.salePrice),
                        str(disc.preauthAmount),
                        str(disc.reserveID),
                        str(disc.coupon.couponCode),
                        str(disc.gene),
                        str(disc.outKioskID),
                        str(disc.rentalTax),
                        str(disc.saleTax),
                        str(disc.pricePlanID),
                        str(disc.upgID),
                        disc.msExpiTime
                    )
                    for disc in shoppingCart.discs
                )
                self.log.info(cartStr % (status, str(shoppingCart.id), shoppingCart.totalCharged, shoppingCart.coupon.couponCode, discStr))
            else:
                status = '5'
                m = 'Sorry, the kiosk has not set any account.'
        except DatabaseError as ex:
            errMsg = '[Local] chargeForSiTef (%s): %s' % (customer.ccid, ex)
            self.log.error(errMsg)
            status = '9'
            m = 'Sorry, the kiosk has communication issue.'
        except socket.error as ex:
            errMsg = '[Local] chargeForSiTef (%s): %s' % (customer.ccid, traceback.format_exc())
            self.log.error(errMsg)
            status = '10'
            m = 'Sorry, the kiosk has communication issue.'
        except RemoteError as ex:
            errMsg = '[Remote] chargeForSiTef (%s): %s' % (customer.ccid, ex)
            self.log.error(errMsg)
            status = '9'
            m = 'Sorry, the kiosk has communication issue.'
        except Exception as ex:
            errMsg = '[Local] chargeForSiTef (%s): %s' % (customer.ccid, traceback.format_exc())
            self.log.error(errMsg)
            status = '9'
            m = 'Sorry, the kiosk has communication issue.'

        return (str(status), m)

    
    def chargeForChipNPin(self, customer, shoppingCart):
        """
        @Params: shoppingCart(ShoppingCart Object)
                 customer(Customer Object)
        @Return: Success: (status, m)
                 Notes: status = '0': Approved.
                        status = '1': Card declined.
                        status = '4': Can not connect upg server.
                        status = '5': Sorry, the kiosk has not set any account.
                        status = '6': EVT is busy.
                        status = '10': EVT has not been setup or PosServer is down.
                        status = '11': Process failed, please retry.
                        #status = '12': Empty wallet reference, declined it
        """
        self._getTestMode()
        if self.UPG_SHOW_MODE:
            shoppingCart.totalCharged = 0
            for disc in shoppingCart.discs:
                disc.upgID = -1
            
            return ('0', '')
        
        status = '3'
        m = 'Internal error.'
        
        try:
            acctId = self.getUpgAcctId()
            if acctId:
                rentAmount = 0
                saleAmount = 0
                amount = 0
                shoppingCart.totalCharged = 0
                for disc in shoppingCart.discs:
                    if disc.gene == 'sale':
                        saleAmount += round(float(disc.preauthAmount), 2)
                    elif disc.gene == 'rent':
                        _preAmount = round(float(disc.rentalPrice) * (1 + float(disc.rentalTax.rstrip('%')) / 100), 2)
                        disc.preauthAmount = fmtMoney(_preAmount)
                        rentAmount += _preAmount
                    
                
                amount = rentAmount + saleAmount
                (status, m, result) = self.charge_chip_n_pin(customer, acctId, amount)
                if str(status) == '0':
                    for disc in shoppingCart.discs:
                        disc.upgID = result.get('upgId', 0)
                    
                
                self.log.info('chargeForChipNPin for ccid(%s): errocode(%s), erromsg(%s)' % (customer.ccid, result.get('status', ''), result.get('message', '')))
                cartStr = 'chargeForChipNPin for Shopping Cart: Status: %s; ID: %s; totalCharged: %s; coupon code: %s; \nDISCS: \n%s'
                discStr = '\n\n'.join(
                    'rfid: %s;\n upc: %s;\n slotID: %s;\n title: %s;\n salePrice: %s;\n '
                    'preauthAmount: %s;\n reserveID: %s;\n coupon code: %s;\n gene: %s;\n '
                    'outKioskID: %s;\n rentalTax: %s;\n saleTax: %s;\n pricePlanID: %s,\n '
                    'upgID: %s,\n msExpiTime: %s' % (
                        str(disc.rfid), 
                        str(disc.upc), 
                        str(disc.slotID), 
                        str(disc.title),
                        str(disc.salePrice),
                        str(disc.preauthAmount),
                        str(disc.reserveID),
                        str(disc.coupon.couponCode),
                        str(disc.gene),
                        str(disc.outKioskID),
                        str(disc.rentalTax),
                        str(disc.saleTax),
                        str(disc.pricePlanID),
                        str(disc.upgID),
                        disc.msExpiTime
                    )
                    for disc in shoppingCart.discs
                )
                self.log.info(cartStr % (status, str(shoppingCart.id), shoppingCart.totalCharged, shoppingCart.coupon.couponCode, discStr))
            else:
                status = '5'
                m = 'Sorry, the kiosk has not set any account.'
        except DatabaseError as ex:
            errMsg = '[Local] chargeForChipNPin (%s): %s' % (customer.ccid, ex)
            self.log.error(errMsg)
            status = '9'
            m = 'Sorry, the kiosk has communication issue.'
        except socket.error as ex:
            errMsg = '[Local] chargeForChipNPin (%s): %s' % (customer.ccid, traceback.format_exc())
            self.log.error(errMsg)
            status = '10'
            m = 'Sorry, the kiosk has communication issue.'
        except RemoteError as ex:
            errMsg = '[Remote] chargeForChipNPin (%s): %s' % (customer.ccid, ex)
            self.log.error(errMsg)
            status = '9'
            m = 'Sorry, the kiosk has communication issue.'
        except Exception as ex:
            errMsg = '[Local] chargeForChipNPin (%s): %s' % (customer.ccid, traceback.format_exc())
            self.log.error(errMsg)
            status = '9'
            m = 'Sorry, the kiosk has communication issue.'

        return (str(status), m)

    
    def charge_chip_n_pin(self, customer, acctId, amount):
        '''
        Charge the amount for chip n pin.
        '''
        status = '1'
        m = ''
        (server, port, baseUrl) = self._getUpgServerFromUrl(self._getConfigByKey('upg_url'))
        obj = chip_n_pin.ChipNPin(self.kioskId, server, port, baseUrl)
        trsRef = self.getChipNPinTrsRef()
        result = obj.sale(acctId, trsRef, amount)
        self.log.info('Transaction result for ChipNPin: %s' % result)
        if not result['busy']:
            if result.get('status', '') == '0':
                customer.ccNum = result['card_number']
                customer.ccNumSHA1 = result['card_sha1']
                customer.ccName = result['card_name']
                customer.ccExpDate = result['card_expdate']
                customer.ccDisplay = '%s (%s)' % (result['card_name'], result['card_number'][-4:])
                customer.cardType = 2
                oid = '%s--%s' % (result['oid'], result['pgtr'])
                upgId = self.addToUpg({
                    'amount': fmtMoney(amount),
                    'oid': oid,
                    'resultCode': result['status'],
                    'resultMsg': result['message'],
                    'trsType': 'SALE',
                    'acctId': acctId,
                    'ccId': customer.ccid,
                    'pqId': '',
                    'preauthMethod': 'CUSTOMER',
                    'notes': self.kioskId,
                    'additional': '' })
                result['upgId'] = upgId
                s = self.getCCInfoByCustomer(customer)
                if s == 1:
                    raise Exception('Internal error in chargeForChipNPin when getCCInfoByCustomer.')
                elif s == 2:
                    raise RemoteError('Remote error in chargeForChipNPin when getCCInfoByCustomer.')
                
                self.updateUpgInfoByUpgId({
                    'upgId': upgId,
                    'ccId': customer.ccid })
                if self._check_black_list_for_chip_n_pin(acctId, result['card_number'], result['card_name']):
                    status = '1'
                    m = 'Decline - Black List'
                else:
                    status = '0'
            elif result.get('status', '') == '-3':
                status = '11'
                m = result['message']
            else:
                status = '1'
                m = result['status']
        else:
            status = '6'
            m = 'Busy'
        return (status, m, result)

    
    def getRemoteData(self, funcName, params, timeout = 60):
        ''' override the function getRemoteData for Proxy
        '''
        if funcName in UPG_NEED_APIS:
            url = 'https://%s/api' % LITE_UPG_HOST
            url_params = {
                'function_name': funcName,
                'params': params }
            return self._http_call(url, url_params, timeout)
        else:
            return Proxy.getRemoteData(self, funcName, params, timeout)

    
    def check_monthly_subscription(self, customer, shopping_cart):
        '''
        Check if the customer uses monthly subscription.
        @param customer: Customer object, the customer has get the information of
                         monthly subscription.
        @param shopping_cart: ShoppingCart object
        @return: status, ms_expi_time, invalid_disc_type, rent_count
                status(int): -1 internal error
                              0 not use
                              1 use successfully
                              2 partial used, error
                              3 disc type not matched, error
                ms_expi_time(str)
                invalid_disc_type(set)
                rent_count(int)
        '''
        status = -1
        ms_expi_time = ''
        invalid_disc_type = set()
        rent_count = 0
        
        try:
            status = 0
            invalid_disc_type = set()
            valid_disc_type = set()
            rent_count = 0
            ms_expi_time = ''
            if customer.msID:
                msDiscType = customer.msDiscType.upper()
                for disc in shopping_cart.discs:
                    if disc.gene == 'rent':
                        rent_count += 1
                        discType = self._UPGProxy__getDiscType(disc)
                        if discType.upper() not in msDiscType:
                            invalid_disc_type.add(discType)
                        else:
                            valid_disc_type.add(discType)
                    
                
                if invalid_disc_type and valid_disc_type:
                    status = 3
                elif valid_disc_type and not invalid_disc_type:
                    status = 1
                elif invalid_disc_type and not valid_disc_type:
                    status = 0
                
                if status in (0, 3):
                    pass
                elif rent_count <= customer.msCount:
                    for disc in shopping_cart.discs:
                        if disc.gene == 'rent':
                            if customer.cardType != 2:
                                disc.preauthAmount = '0'
                            
                            disc.msKeepDays = customer.msKeepDays
                        
                    
                    ms_expi_time = getTimeChange(getCurTime(), day = customer.msKeepDays)
                    status = 1
                else:
                    status = 2
        except Exception as ex:
            status = -1
            self.log.error('check_monthly_subscription: %s' % ex)

        return (status, ms_expi_time, invalid_disc_type, rent_count)

    
    def getChipNPinTrsRef(self):
        ''' Get the chip n pin transaction reference.
        @Return: trsRef(str)
        '''
        return self.getTrsIdty()

    
    def _check_black_list_for_chip_n_pin(self, upg_acct_id = None, card_number = '', card_name = '', card_track2 = ''):
        ''' Check if the card is in the black list for chipNPin.
        @param upg_acct_id(str)
        @param upg_acct_id(str): None as default, if it is not given, it uses
                                 the upg account ID in the config table
        @param card_number(str)
        @param card_name(str)
        @param card_track2(str)
        @return: True/False
        '''
        if upg_acct_id is None:
            upg_acct_id = self.getUpgAcctId()
        
        r = self.getRemoteData('check_black_list_for_chip_n_pin', {
            'upg_acct_id': upg_acct_id,
            'card_number': card_number,
            'card_name': card_name,
            'card_track2': card_track2 })
        if r['result'] != 'ok':
            raise RemoteError('Error when _check_black_list_for_chip_n_pin: %s' % r['zdata'])
        
        return r['zdata']

    
    def getUpgAcctId(self):
        return self._getConfigByKey('upg_acct_id')

    
    def preauth(self, acctId, customer, amount, zipcode = None, trsPasswd = None, oid = '', peauthMethod = 'full'):
        '''
        @Params: acctId(str)
                 customer(Customer object)
                 amount(float)
                 zipcode(str)
                 trsPasswd(str)
                 oid(str)
                 peauthMethod(str)
        @Return: { "upgId":12,
                   "trsCode":0,
                   "trsMsg":""}
        @Exception: RemoteError
                    DatabaseError
                    Exception
        '''
        result = { }
        
        try:
            self.upgUrl = self._getConfigByKey('upg_url')
            trsType = 'PREAUTH'
            params = { }
            params['preauthMethod'] = peauthMethod
            params['notes'] = self.kioskId
            pqInfo = { }
            if not self.cardHasDeclinedTrs(customer.ccid):
                pq = PreauthQueue(acctId, customer.ccid)
                pqInfo = pq.getByAmount(amount)
                del pq
            
            upgId = 0
            if pqInfo and pqInfo.get('upg_id', None):
                upgId = pqInfo['upg_id']
                r = self.getUpgInfoByUpgId(upgId)
                params['resultCode'] = r['resultCode']
                params['resultMsg'] = r['resultMsg']
            else:
                (server, port, baseUrl) = self._getUpgServerFromUrl(self.upgUrl)
                preauth = Preauth(self.kioskId, server, port, baseUrl)
                amount = self._getAmount(amount)
                tmp = preauth.trade(acctId, customer.ccNum, customer.ccExpDate, customer.ccName, amount, customer.track2, customer.track1, customer.oid, 0, zipcode, trsPasswd)
                if str(tmp[0]) in ('-1', '-2'):
                    raise Exception(tmp[1])
                
                params['oid'] = tmp[2]
                params['resultCode'] = tmp[0]
                params['resultMsg'] = tmp[1]
                params['pqId'] = ''
                params['acctId'] = acctId
                params['ccId'] = customer.ccid
                params['trsType'] = trsType
                params['amount'] = amount
                if str(params['resultCode']) == '0':
                    upgId = self.addToUpg(params)
                
            result['upgId'] = upgId
            result['trsCode'] = params['resultCode']
            result['trsMsg'] = params['resultMsg']
        except DatabaseError as ex:
            errMsg = ''
            raise 
        except RemoteError as ex:
            errMsg = ''
            raise 
        except Exception as ex:
            errMsg = ''
            raise 

        return result

    
    def topup_for_cerepay(self, chargeCustomer, cerepayCustomer, amount):
        '''
        Top up for CerePay account.
        @param chargeCustomer(Customer object)
        @param cerepayCustomer(Customer object)
        @param amount(float)
        @return: status(int), msg(str), trs_uuid(str), top_up_queue_id(int)
                 status: 0 topup successfully
                         1 internal error
                         2 network error
                         3 upg account do not support CerePay, or CerePay 
                           account is frozen.
                         4 CerePay config of upg account do not match
                         5 not CerePay card
                         6 charge DECLINE
                         7 member does not exist
        '''
        (status, m, trs_uuid, topup_queue_id) = (2, '', '', 0)
        
        try:
            if cerepayCustomer.cardType == 3:
                cpCfg = self.getCerePayCfg()
                if not cpCfg:
                    status = 3
                    raise Exception('UPG account DOESNOT support CerePay')
                
                cpInfo = self.getCerePayUserInfo(cpCfg['MERCHANTID'], cpCfg['PASSWORD'], cpCfg['CURRENCY'], number = cerepayCustomer.ccNum)
                if cpInfo['id']:
                    pass
                elif str(cpInfo['errCode']) == '1007':
                    status = 3
                    raise Exception(cpInfo['errMsg'])
                elif str(cpInfo['errCode']) in ('1001', '1002'):
                    status = 4
                    raise Exception(cpInfo['errMsg'])
                elif str(cpInfo['errCode']) == '1':
                    status = 1
                    raise Exception(cpInfo['errMsg'])
                elif str(cpInfo['errCode']) == '1003':
                    status = 1
                    raise Exception(cpInfo['errMsg'])
                else:
                    status = 7
                    raise Exception(cpInfo['errMsg'])
                acctId = self._getConfigByKey('upg_acct_id')
                payment = self._getConfigByKey('payment_options')
                amount = self._getAmount(amount)
                if payment == 'chipnpin':
                    (s, m, result) = self.charge_chip_n_pin(chargeCustomer, acctId, amount)
                    oid = result.get('pgtr', '')
                    upgId = result.get('upgId', 0)
                else:
                    result = self.sale(acctId, chargeCustomer.ccid, amount)
                    s = result.get('trsCode', '')
                    m = result.get('trsMsg', '')
                    oid = result.get('oid', '')
                    upgId = result.get('upgId', 0)
                if str(s) == '0':
                    
                    try:
                        res = self.topup_cerepay(cpCfg['MERCHANTID'], cpCfg['PASSWORD'], cpCfg['CURRENCY'], cpInfo['id'], amount, oid)
                        if str(res['errCode']) == '0':
                            trs_uuid = res['trsUuid']
                        
                        topup_queue_id = self._add_cerepay_topup_queue(acctId, cpInfo['id'], upgId, amount, oid, chargeCustomer.cardType, res['errCode'], res['errMsg'], trs_uuid)
                    except Exception as ex:
                        topup_queue_id = self._add_cerepay_topup_queue(acctId, cpInfo['id'], upgId, amount, oid, chargeCustomer.cardType, -1, str(ex), '')

                    status = 0
                else:
                    status = 6
            else:
                status = 5
        except Exception as ex:
            self.log.warning('topup_for_cerepay: %s' % ex)
        except RemoteError as ex:
            status = 2
            self.log.error('topup_for_cerepay(Remote): %s' % ex)
        except Exception as ex:
            status = 1
            self.log.error('topup_for_cerepay(Local): %s' % ex)

        return (status, m, trs_uuid, topup_queue_id)

    
    def get_topup_status_by_queue_id(self, topup_queue_id, timeout = 300):
        ''' Get the topup status by queue id.
        @param topup_queue_id(int)
        @param timeout(int): second
        @return: status(int), trs_uuid(str)
                status: 0 success
                        1 fail
        '''
        (status, trs_uuid) = (1, '')
        
        try:
            begin = time.time()
            while time.time() - begin < timeout:
                info = self._get_cerepay_topup_by_id(topup_queue_id)
                if str(info['state']) == '0':
                    status = 0
                    trs_uuid = info['cerepay_uuid']
                    break
                
                time.sleep(1)
        except Exception as ex:
            result = 1
            self.log.error('get_topup_status_by_queue_id: %s' % ex)

        return (status, trs_uuid)

    
    def chkNeedTrsPasswd(self, customer):
        '''
        Check if the customer should enter password.
        @param customer(Customer Object)
        @return: result(int): 0 need transaction password
                              1 donot need transaction password
                              2 network error
        '''
        result = 1
        
        try:
            if customer.cardType == 3:
                cpCfg = self.getCerePayCfg()
                if cpCfg:
                    cpInfo = self.getCerePayUserInfo(cpCfg['MERCHANTID'], cpCfg['PASSWORD'], cpCfg['CURRENCY'], number = customer.ccNum)
                    if cpInfo and cpInfo.get('needTrsPasswd', False):
                        result = 0
                    
                
            else:
                result = 1
        except RemoteError as ex:
            result = 2
            self.log.warning('chkNeedTrsPasswd: %s' % ex)
        except Exception as ex:
            result = 1
            self.log.error('chkNeedTrsPasswd: %s' % ex)

        return result

    
    def getCerePayCfg(self):
        """ Get the config of CerePay.
        @param None
        @return: result(dict): {}
                               or
                 {'CURRENCY': 'xxx', 'PASSWORD': 'xxx', 'MERCHANTID': 'xxx'}
        """
        p = {
            'upg_acct_id': self.getUpgAcctId() }
        r = self.getRemoteData('getCerePayCfgByAcctId', p)
        if r['result'] != 'ok':
            raise RemoteError('Error when getCerePayCfgByAcctId: %s' % r['zdata'])
        
        return r['zdata']

    
    def getCerePayUserInfo(self, merchantId, validationCode, currency, number = None, cpMemberId = None, cpEmail = None):
        """ Get the user information of the CerePay.
        @param merchantId(str)
        @param validationCode(str)
        @param currency(str)
        @param number(str)
        @param cpMemberId(str)
        @param cpEmail(str)
        @return: result(dict): {'validationCode': xxx, 'status': xxx,
                                'name': xxx, 'needTrsPasswd': xxx, 'passwd': xxx,
                                'number': xxx, 'errCode': xxx, 'holdingAmt': xxx,
                                'currency': xxx, 'email': xxx, 'numberList': xxx,
                                'merchantId': xxx, 'balance': xxx, 'id': xxx,
                                'errMsg': xxx, 'trsPasswd': xxx,}
        """
        p = {
            'merchant_id': merchantId,
            'validation_code': validationCode,
            'currency': currency,
            'cerepay_email': cpEmail,
            'cerepay_member_id': cpMemberId,
            'cerepay_number': number }
        r = self.getRemoteData('getCerePayUserInfo', p)
        if r['result'] != 'ok':
            raise RemoteError('Error when getCerePayUserInfo: %s' % r['zdata'])
        
        return r['zdata']

    
    def send_topup_receipt(self, trs_uuid, upg_acct_id = None):
        ''' Send the receipt for topuping of CerePay account.
        @param trs_uuid(str)
        @param upg_acct_id(str): None as default, if it is not given, it uses
                                 the upg account ID in the config table
        @return: None
        '''
        if upg_acct_id is None:
            upg_acct_id = self.getUpgAcctId()
        
        self.syncDataNoSequence('send_topup_receipt', {
            'trs_uuid': trs_uuid,
            'upg_acct_id': upg_acct_id })

    
    def checkCerePayEmail(self, merchantId, validationCode, currency, cpEmail):
        """ Get the user information of the CerePay.
        @param merchantId(str)
        @param validationCode(str)
        @param currency(str)
        @param cpEmail(str)
        @return: result(dict): {'validationCode': xxx, 'status': xxx,
                                'name': xxx, 'needTrsPasswd': xxx, 'passwd': xxx,
                                'number': xxx, 'errCode': xxx, 'holdingAmt': xxx,
                                'currency': xxx, 'email': xxx, 'numberList': xxx,
                                'merchantId': xxx, 'balance': xxx, 'id': xxx,
                                'errMsg': xxx, 'trsPasswd': xxx,}
        """
        p = {
            'merchant_id': merchantId,
            'validation_code': validationCode,
            'currency': currency,
            'cerepay_email': cpEmail }
        r = self.getRemoteData('checkCerePayEmail', p)
        if r['result'] != 'ok':
            raise RemoteError('Error when checkCerePayEmail: %s' % r['zdata'])
        
        return r['zdata']

    
    def registerCerePay(self, merchantId, validationCode, currency, cpEmail, cpNumber, cpPasswd):
        """ Register a new card of the CerePay.
        @param merchantId(str)
        @param validationCode(str)
        @param currency(str)
        @param cpEmail(str)
        @param cpNumber(str)
        @param cpPasswd(str)
        @return: result(dict): {'validationCode': xxx, 'status': xxx,
                                'name': xxx, 'needTrsPasswd': xxx, 'passwd': xxx,
                                'number': xxx, 'errCode': xxx, 'holdingAmt': xxx,
                                'currency': xxx, 'email': xxx, 'numberList': xxx,
                                'merchantId': xxx, 'balance': xxx, 'id': xxx,
                                'errMsg': xxx, 'trsPasswd': xxx,}
        """
        p = {
            'merchant_id': merchantId,
            'validation_code': validationCode,
            'currency': currency,
            'cerepay_email': cpEmail,
            'cerepay_number': cpNumber,
            'cerepay_passwd': cpPasswd }
        r = self.getRemoteData('registerCerePay', p)
        if r['result'] != 'ok':
            raise RemoteError('Error when registerCerePay: %s' % r['zdata'])
        
        return r['zdata']

    
    def topup_cerepay(self, merchantId, validationCode, currency, cpMemberId, amount, oid):
        """ .
        @param merchantId(str)
        @param validationCode(str)
        @param currency(str)
        @param cpMemberId(str): the member ID of CerePay account
        @param amount(str)
        @param oid(str)
        @return: result(dict): {'validationCode': xxx, 'status': xxx,
                                'name': xxx, 'needTrsPasswd': xxx, 'passwd': xxx,
                                'number': xxx, 'errCode': xxx, 'holdingAmt': xxx,
                                'currency': xxx, 'email': xxx, 'numberList': xxx,
                                'merchantId': xxx, 'balance': xxx, 'id': xxx,
                                'errMsg': xxx, 'trsPasswd': xxx,}
        """
        p = {
            'merchant_id': merchantId,
            'validation_code': validationCode,
            'currency': currency,
            'cerepay_member_id': cpMemberId,
            'amount': amount,
            'oid': oid }
        r = self.getRemoteData('topup_cerepay', p)
        self.log.info(r)
        if r['result'] != 'ok':
            raise RemoteError('Error when topup_cerepay: %s' % r['zdata'])
        
        return r['zdata']

    
    def _add_cerepay_topup_queue(self, upgAcctId, cpMemberId, upgId, amount, oid, cardType, state, lastMsg, cp_uuid):
        '''
        @param upgAcctId(str): upg account ID
        @param cpMemberId(str): member ID of CerePay account for topup
        @param upgId(str): upg ID of charge
        @param amount(float): topup amount
        @param oid(str): oid of charge
        @param cardType(int): card type of charged card
        @param state(int): the state of the topup
        @param lastMsg(str): the last message of topup
        @param cp_uuid(str): the uuid returned by CerePay of topup
        @return: id_(int): the ID of the queue
        '''
        id_ = 0
        
        try:
            self.log.info('add cerepay topup into the queue: %s %s %s %s %s' % (upgAcctId, cpMemberId, upgId, amount, oid))
            db = Db(MKC_DB_PATH)
            p = {
                'acct_id': upgAcctId,
                'cerepay_member_id': cpMemberId,
                'upg_id': upgId,
                'amount': amount,
                'oid': oid,
                'card_type': cardType,
                'state': state,
                'last_msg': lastMsg,
                'cur_time': getCurTime(),
                'cerepay_uuid': cp_uuid }
            sql = 'SELECT id FROM cerepay_topup WHERE cerepay_member_id=? AND upg_id=? AND oid=?;'
            if not db.query(sql, 'one', (cpMemberId, upgId, oid)):
                sql = 'INSERT INTO cerepay_topup(acct_id, cerepay_member_id, card_type, upg_id, oid, amount, state, last_msg, add_time, last_time, cerepay_uuid) VALUES(:acct_id, :cerepay_member_id, :card_type, :upg_id, :oid, :amount, :state, :last_msg, :cur_time, :cur_time, :cerepay_uuid);'
                id_ = db.update(sql, p)
                p['id'] = id_
                self.syncData('add_cerepay_topup_queue', p)
            
            del db
        except Exception as ex:
            self.log.error('_add_cerepay_topup_queue: %s' % ex)

        return id_

    
    def _get_failed_cerepay_topup(self):
        ''' Get the failed CerePay topup in the queue.
        @param: None
        @return: 
        '''
        topup = []
        
        try:
            db = Db(MKC_DB_PATH)
            sql = 'SELECT id, acct_id, cerepay_member_id, amount, oid, state FROM cerepay_topup WHERE state!=0;'
            for row in db.query(sql):
                topup.append({
                    'id': row[0],
                    'acct_id': row[1],
                    'cerepay_member_id': row[2],
                    'amount': row[3],
                    'oid': row[4],
                    'state': row[5] })
            
            del db
        except Exception as ex:
            self.log.error('_get_failed_cerepay_topup: %s' % ex)

        return topup

    
    def _get_cerepay_topup_by_id(self, queue_id):
        ''' Get the CerePay topup from the queue by id.
        @param: queue_id(int)
        @return: topup_info(dict)
        '''
        topup_info = { }
        
        try:
            db = Db(MKC_DB_PATH)
            sql = 'SELECT id, acct_id, cerepay_member_id, amount, oid, state, upg_id, last_msg, add_time, last_time, cerepay_uuid FROM cerepay_topup WHERE id=?;'
            row = db.query(sql, 'one', (queue_id,))
            if row:
                topup_info = {
                    'id': row[0],
                    'acct_id': row[1],
                    'cerepay_member_id': row[2],
                    'amount': row[3],
                    'oid': row[4],
                    'state': row[5],
                    'upg_id': row[6],
                    'last_msg': row[7],
                    'add_time': row[8],
                    'last_time': row[9],
                    'cerepay_uuid': row[10] }
            
            del db
        except Exception as ex:
            self.log.error('_get_cerepay_topup_by_id: %s' % ex)

        return topup_info

    
    def _update_cerepay_topup_queue(self, id_, state, lastMsg, cp_uuid):
        ''' Update the state and last message for the CerePay topup in the queue.
        @param id_(int)
        @param state(int)
        @param lastMsg(str)
        @param cp_uuid(str)
        @return None
        '''
        
        try:
            p = {
                'state': state,
                'last_msg': lastMsg,
                'id': id_,
                'update_time': getCurTime(),
                'cerepay_uuid': cp_uuid }
            db = Db(MKC_DB_PATH)
            sql = 'UPDATE cerepay_topup SET state=:state, last_msg=:last_msg, last_time=:update_time, cerepay_uuid=:cerepay_uuid WHERE id=:id;'
            db.update(sql, p)
            del db
            self.syncData('update_cerepay_topup_queue', p)
        except Exception as ex:
            self.log.error('_update_cerepay_topup_queue: %s' % ex)


    
    def _preauth(self, amount, upgId, declinemsg = ''):
        ''' Call it internal.
        @Params: amount(float)
        @Return: { "upgId":12,
                   "trsCode":0,
                   "trsMsg":""}
        '''
        result = { }
        
        try:
            upgInfo = self.getUpgInfoByUpgId(upgId)
            if not upgInfo:
                msg = 'Can not get upg info by id(%d)...' % upgId
                self.log.error(msg)
                raise DatabaseError(msg)
            
            if declinemsg:
                tmp = ('12', declinemsg, '')
            else:
                self.upgUrl = self._getConfigByKey('upg_url')
                trsType = 'PREAUTH'
                acctId = upgInfo['acctId']
                ccId = upgInfo['ccId']
                ccInfo = self.getCCInfoByCcId(ccId)
                if not ccInfo:
                    m = 'Get credit card info failed for ccId %s' % str(ccId)
                    raise DatabaseError(m)
                
                (server, port, baseUrl) = self._getUpgServerFromUrl(self.upgUrl)
                preauth = Preauth(self.kioskId, server, port, baseUrl)
                amount = self._getAmount(amount)
                tmp = preauth.trade(acctId, ccInfo['cc_number'], ccInfo['cc_expdate'], ccInfo['cc_name'], amount, ccInfo['cc_track2'], ccInfo['cc_track1'], '', 1)
                self.log.info('Preauth for upgId %s, amount %s, result %s' % (upgId, amount, tmp))
                if str(tmp[0]) in ('-1', '-2'):
                    raise Exception(tmp[1])
                
            if str(tmp[0]) == '0':
                params = { }
                params['preauthMethod'] = 'full'
                params['notes'] = self.kioskId
                params['oid'] = tmp[2]
                params['resultCode'] = tmp[0]
                params['resultMsg'] = tmp[1]
                params['pqId'] = ''
                params['acctId'] = acctId
                params['ccId'] = ccId
                params['trsType'] = trsType
                params['amount'] = amount
                upgId = self.addToUpg(params)
            
            result['upgId'] = upgId
            result['trsCode'] = tmp[0]
            result['trsMsg'] = tmp[1]
            result['oid'] = tmp[2]
        except RemoteError as ex:
            raise 
        except DatabaseError as ex:
            raise 
        except Exception as ex:
            raise 

        return result

    
    def postauth(self, amount, upgId, declinemsg = ''):
        '''
        @Params: amount(Float)
                 upgId(Integer)
        @Return: { "upgId":12,
                   "trsCode":0,
                   "trsMsg":""}
        @Exception: RemoteError
                    DatabaseError
                    Exception
        '''
        result = { }
        
        try:
            trsType = 'POSTAUTH'
            amount = self._getAmount(amount)
            upgInfo = self.getUpgInfoByUpgId(upgId)
            if not upgInfo:
                msg = 'Can not get upg info by id(%d)...' % upgId
                self.log.error(msg)
                raise Exception(msg)
            
            result.update(upgInfo)
            if declinemsg:
                result['trsCode'] = '12'
                result['trsMsg'] = declinemsg
                result['oid'] = upgInfo['oid']
            else:
                self.upgUrl = self._getConfigByKey('upg_url')
                acctId = upgInfo['acctId']
                ccId = upgInfo['ccId']
                ccInfo = self.getCCInfoByCcId(ccId)
                if not ccInfo:
                    m = 'Get credit card info failed for ccId %s' % str(ccId)
                    raise Exception(m)
                
                (server, port, baseUrl) = self._getUpgServerFromUrl(self.upgUrl)
                postAuth = Postauth(self.kioskId, server, port, baseUrl)
                tmp = postAuth.trade(acctId, ccInfo['cc_number'], ccInfo['cc_expdate'], ccInfo['cc_name'], amount, ccInfo['cc_track2'], ccInfo['cc_track1'], upgInfo['oid'], 1)
                del postAuth
                if str(tmp[0]) in ('-1', '-2'):
                    raise Exception(tmp[1])
                
                result['trsCode'] = tmp[0]
                result['trsMsg'] = tmp[1]
                result['oid'] = tmp[2]
                result['amount'] = amount
            result['upgId'] = upgId
            result['resultCode'] = result['trsCode']
            result['resultMsg'] = result['trsMsg']
            result['trsType'] = trsType
            upgId = self.updateUpgInfoByUpgId(result)
        except RemoteError as ex:
            raise 
        except DatabaseError as ex:
            self.log.error('database error in sale: %s' % ex)
        except Exception as ex:
            raise 

        return result

    
    def sale(self, acctId, ccId, amount, upgId = '', declinemsg = ''):
        result = { }
        
        try:
            trsType = 'SALE'
            self.upgUrl = self._getConfigByKey('upg_url')
            amount = self._getAmount(amount)
            if declinemsg:
                result['trsMsg'] = declinemsg
                result['trsCode'] = '12'
                result['oid'] = ''
                result['resultCode'] = result['trsCode']
                result['resultMsg'] = result['trsMsg']
            else:
                ccInfo = self.getCCInfoByCcId(ccId)
                if not ccInfo:
                    m = 'Get credit card info failed for ccId %s' % str(ccId)
                    raise Exception(m)
                
                (server, port, baseUrl) = self._getUpgServerFromUrl(self.upgUrl)
                sale1 = Sale(self.kioskId, server, port, baseUrl)
                tmp = sale1.trade(acctId, ccInfo['cc_number'], ccInfo['cc_expdate'], ccInfo['cc_name'], amount, ccInfo['cc_track2'], ccInfo['cc_track1'], '', 1)
                if str(tmp[0]) in ('-1', '-2'):
                    raise Exception(tmp[1])
                
                result['oid'] = tmp[2]
                result['trsCode'] = tmp[0]
                result['trsMsg'] = tmp[1]
                result['resultCode'] = result['trsCode']
                result['resultMsg'] = result['trsMsg']
                result['amount'] = amount
            result['trsType'] = trsType
            result['upgId'] = upgId
            if not upgId:
                result['acctId'] = acctId
                result['ccId'] = ccId
                result['pqId'] = ''
                result['preauthMethod'] = ''
                result['notes'] = self.kioskId
                if 'oid' not in result:
                    result['oid'] = ''
                
                if 'amount' not in result:
                    result['amount'] = amount
                
                upgId = self.addToUpg(result)
            else:
                upgId = self.updateUpgInfoByUpgId(result)
            result['upgId'] = upgId
        except DatabaseError as ex:
            self.log.error('database error in sale: %s' % ex)
        except:
            raise 

        return result

    
    def saleForRentNBuyDisc(self, disc, acctId, ccId, amount):
        ''' Sale for discs.
        @param disc(Disc object)
        @param acctId(str)
        @param ccId(int)
        @param amount(float)
        @return status(int): -1 communication error
                              0 success
                              1 declined
                msg(str)
        '''
        status = -1
        msg = ''
        
        try:
            params = { }
            trsType = 'SALE'
            self.upgUrl = self._getConfigByKey('upg_url')
            amount = self._getAmount(amount)
            ccInfo = self.getCCInfoByCcId(ccId)
            if not ccInfo:
                m = 'Get credit card info failed for ccId %s: %s' % (ccId, ccInfo)
                raise DatabaseError(m)
            
            (server, port, baseUrl) = self._getUpgServerFromUrl(self.upgUrl)
            if self._getConfigByKey('payment_options') == 'chipnpin':
                sql = 'SELECT upg_id FROM transactions WHERE id=?;'
                (upg_id,) = self.mkcDb.query(sql, 'one', (disc.trsID,))
                upg_info = self.getUpgInfoByUpgId(upg_id)
                chipNPin = chip_n_pin.ChipNPin(self.kioskId, server, port, baseUrl)
                (trsCode, trsMsg, oid) = chipNPin.postauth(acctId, ccInfo['cc_number_sha1'], ccInfo['cc_expdate'], ccInfo['cc_name'], amount, '', '', upg_info['oid'])
            else:
                sale1 = Sale(self.kioskId, server, port, baseUrl)
                (trsCode, trsMsg, oid) = sale1.trade(acctId, ccInfo['cc_number'], ccInfo['cc_expdate'], ccInfo['cc_name'], amount, ccInfo['cc_track2'], ccInfo['cc_track1'], '', 1)
            if str(trsCode) in ('-1', '-2'):
                raise Exception(trsMsg)
            
            self.log.info('saleForRentNBuyDisc for ccId(%s): amount %s result %s,%s,%s' % (ccId, amount, trsCode, trsMsg, oid))
            if str(trsCode) == '0':
                p = { }
                p['acctId'] = acctId
                p['pqId'] = ''
                p['trsType'] = trsType
                p['oid'] = oid
                p['amount'] = amount
                p['ccId'] = ccId
                p['resultCode'] = trsCode
                p['resultMsg'] = trsMsg
                p['curTime'] = getCurTime()
                p['preauthMethod'] = 'full'
                p['notes'] = self.kioskId
                if disc.outKioskID:
                    p['trs_id'] = disc.trsID
                    p['kiosk_id'] = disc.outKioskID
                    self.syncDataRemoteKiosk(disc.outKioskID, 'saleForDiscOfRemoteKiosk', p)
                else:
                    upgId = self.addToUpg(p)
                    pa = {
                        'upg_id': upgId,
                        'trs_id': disc.trsID,
                        'kiosk_id': self.kioskId }
                    sql = 'UPDATE transactions SET upg_id=:upg_id WHERE id=:trs_id;'
                    db = Db(MKC_DB_PATH)
                    db.update(sql, pa)
                    del db
                    self.syncData('updateUpgIdForTrs', pa)
                status = 0
            else:
                status = 1
                msg = trsMsg
        except Exception as ex:
            self.log.error('saleForRentNBuyDisc: %s' % ex)
            status = -1

        return (status, msg)

    
    def addToUpg(self, params):
        sql = 'INSERT INTO upg(acct_id, pq_id, type, oid, amount, cc_id, result_code, result_msg, time, preauth_method, notes'
        if 'additional' in params:
            sql += ', additional'
        
        sql += ') values(:acctId, :pqId, :trsType, :oid, :amount, :ccId, :resultCode, :resultMsg, :curTime, :preauthMethod, :notes'
        if 'additional' in params:
            sql += ', :additional'
        
        sql += ');'
        curTime = getCurTime()
        params['curTime'] = curTime
        upgId = self.mkcDb.update(sql, params)
        params['upgId'] = upgId
        params['syncType'] = 'add'
        self.syncData('dbSyncUpg', params)
        return upgId

    
    def updateUpgInfoByUpgId(self, params):
        ''' Update the upg info by upg id. '''
        sql = 'UPDATE upg set time=:curTime '
        if 'trsType' in params:
            sql += ', type=:trsType '
        
        if 'amount' in params:
            sql += ', amount=:amount '
        
        if 'oid' in params:
            sql += ', oid=:oid '
        
        if 'resultCode' in params:
            sql += ', result_code=:resultCode '
        
        if 'resultMsg' in params:
            sql += ', result_msg=:resultMsg '
        
        if 'ccId' in params:
            sql += ', cc_id=:ccId '
        
        sql += 'WHERE id=:upgId;'
        params['curTime'] = getCurTime()
        self.mkcDb.update(sql, params)
        params['syncType'] = 'update'
        self.syncData('dbSyncUpg', params)
        return params['upgId']

    
    def getUpgInfoByUpgId(self, upgId):
        result = { }
        sql = 'select pq_id, type, oid, amount, cc_id, result_code, result_msg, acct_id, time, additional from upg where id=:upgId;'
        row = self.mkcDb.query(sql, 'one', {
            'upgId': upgId })
        if row:
            (pqId, trsType, oid, amount, ccId, resultCode, resultMsg, acctId, preauthTime, additional) = row
            result['pqId'] = pqId
            result['trsType'] = trsType
            result['oid'] = oid
            result['amount'] = amount
            result['resultCode'] = resultCode
            result['resultMsg'] = resultMsg
            result['acctId'] = acctId
            result['ccId'] = ccId
            result['time'] = preauthTime
            result['additional'] = additional
        
        return result

    
    def getCCInfoByCcId(self, ccId):
        '''
        Get credit card information by credit card id.
        From upg service.
        @Params: ccId(int)
        @Return: {
                    "cc_name":"xxx",
                    "cc_number":"xxx",
                    "cc_expdate":"xxx",
                    "cc_track1":"xxx",
                    "cc_expdate":"xxx",
                    "cc_track2":"xxx",
                    "cc_display":"xxx",
                    "cc_id":"xxx",
                    "cc_number_sha1":"xxx",
                    "cc_type":"xxx",
                 }
        '''
        params = {
            'cc_id': ccId }
        result = self.getRemoteData('getCcInfoByCcId', params)
        if result['result'] == 'timeout':
            raise RemoteError('Error when _getCCInfoByCcId: %s' % result['zdata'])
        elif result['result'] != 'ok':
            raise Exception('Error when _getCCInfoByCcId: %s' % result['zdata'])
        
        return result['zdata']

    
    def getCCInfoByCustomer(self, customer):
        '''
        Get credit card information by customer.
        @Params: customer(Customer Object)
        @Return: status(int): 0 success
                              1 internal error.
                              2 remote error.
                              3 invalid customer.
        '''
        status = 1
        
        try:
            self._getTestMode()
            if self.UPG_SHOW_MODE:
                return 0
            
            status = 0
            if customer:
                if customer.ccNum or customer.track2:
                    result = self._getCcInfoByCcNum(customer.ccNum, customer.ccName, customer.ccExpDate, customer.track1, customer.track2, customer.ccNumSHA1, customer.cardType)
                    customer.ccid = result['cc_id']
                    customer.isNew = result['is_new']
                    customer.cardType = result['cc_type']
                    customer.ccDisplay = result['cc_display']
                    customer.ccName = result['cc_name']
                    customer.ccExpDate = result['cc_expdate']
                    customer.track2 = result['cc_track2']
                    customer.track1 = result['cc_track1']
                    self._saveLocalCC(result)
                else:
                    status = 1
        except RemoteError as ex:
            status = 2
            self.log.error('Remote Error in getCCInfoByCustomer: %s' % ex)
        except Exception as ex:
            status = 1
            self.log.error('Internal Error in getCCInfoByCustomer: %s' % ex)

        return status

    
    def _getCcInfoByCcNum(self, ccNum, ccName, ccExpDate, track1, track2, ccNumSHA1 = '', ccType = 0):
        '''
        Get credit card information by customer
        @Params: ccNum(str)
                 ccName(str)
                 ccExpDate(str)
                 track1(str)
                 track2(str)
        @Return: {
                    "cc_name":"xxx",
                    "cc_number":"xxx",
                    "cc_expdate":"xxx",
                    "cc_track1":"xxx",
                    "cc_track2":"xxx",
                    "cc_display":"xxx",
                    "cc_number_sha1":"xxx",
                    "cc_type":"xxx",
                    "cc_id":"xxx"
                 }
        '''
        params = { }
        params['cc_name'] = ccName
        params['cc_number'] = ccNum
        params['cc_expdate'] = ccExpDate
        params['cc_track1'] = track1
        params['cc_track2'] = track2
        params['cc_number_sha1'] = ccNumSHA1
        params['cc_type'] = ccType
        params['kiosk_id'] = self.kioskId
        result = self.getRemoteData('getCcInfoByCcNumber', params)
        if result['result'] == 'timeout':
            raise RemoteError('Error when _getCcInfoByCcNum: %s' % result['zdata'])
        elif result['result'] != 'ok':
            raise Exception('Error when _getCcInfoByCcNum: %s' % result['zdata'])
        
        return result['zdata']

    
    def getCCInfoFromCacheByCustomer(self, customer):
        '''
        Get the cc info in local mkc.db.
        @param customer(Customer Obj)
        @return: None
        '''
        sql = 'SELECT id, name, display FROM cc WHERE id=?;'
        db = Db(MKC_DB_PATH)
        row = db.query(sql, 'one', (customer.ccid,))
        del db
        if row:
            customer.ccName = row[1]
            customer.ccDisplay = row[2]
        

    
    def _saveLocalCC(self, ccInfo):
        '''
        Save the cc info in local mkc.db.
        @Params: {
                    "cc_name":"xxx",
                    "cc_number":"xxx",
                    "cc_expdate":"xxx",
                    "cc_track1":"xxx",
                    "cc_expdate":"xxx",
                    "cc_track2":"xxx",
                    "cc_display":"xxx",
                    "cc_id":"xxx"
                 }
        @Return: None
        '''
        ccId = ccInfo['cc_id']
        sql = 'SELECT id FROM cc WHERE id=?;'
        row = self.mkcDb.query(sql, 'one', (ccId,))
        if row and str(row[0]) == str(ccId):
            sql = 'UPDATE cc SET id=? '
            if ccInfo['cc_name']:
                sql += ",name='%s' " % sqlQuote(ccInfo['cc_name'])
            
            if ccInfo['cc_display']:
                sql += ",display='%s' " % sqlQuote(ccInfo['cc_display'])
            
            sql += 'WHERE id=?;'
            self.mkcDb.update(sql, (ccId, ccId))
        else:
            sql = 'INSERT INTO cc(id, name, display) VALUES(?,?,?);'
            self.mkcDb.update(sql, (ccId, ccInfo['cc_name'], ccInfo['cc_display']))

    
    def _getPartialAmount(self, disc):
        ''' Get the partial amount for the disc.
        '''
        return round(float(disc.rentalPrice) * (1 + float(disc.rentalTax.rstrip('%')) / 100), 2)

    
    def _decodeStr(self, key):
        return base64.b64decode(key)

    
    def _encodeStr(self, key):
        return base64.b64encode(key)

    
    def _getCardAmountByRfids(self, rfids):
        result = []
        sql = "select upg_id, cc_id, total(amount) from transactions where id in (select id from transactions where state='pending' and rfid in %s) group by upg_id;" % rfids
        rows = self.mkcDb.query(sql, 'all')
        for row in rows:
            (upg_id, cc_id, totalAmount) = row
            tmp = { }
            tmp['upg_id'] = upg_id
            tmp['cc_id'] = cc_id
            tmp['total_amount'] = totalAmount
            result.append(tmp)
        
        return result

    
    def _getTreadingTrsIdsByRfidByUpgId(self, rfids, upgId):
        trsIds = []
        sql = "select id from transactions where state='pending' and rfid in :rfids and upg_id=:upgId;"
        rows = self.mkcDb.query(sql, 'all', {
            'rfids': rfids,
            'upgId': upgId })
        for row in rows:
            (trsId,) = row
            trsIds.append(trsId)
        
        return trsIds

    
    def _getTrendingTrsIdsByRfids(self, rfids):
        trsIds = []
        sql = "select id from transactions where state='pending' and rfid in :rfids;"
        rows = self.mkcDb.query(sql, 'all', {
            'rfids': rfids })
        for row in rows:
            (trsId,) = row
            trsIds.append(trsId)
        
        return trsIds

    
    def _getUpgServerFromUrl(self, url):
        server = ''
        port = ''
        baseUrl = ''
        urls = url.split('/')
        serverPort = urls[0].split(':')
        if len(serverPort) == 1:
            server = serverPort[0]
        elif len(serverPort) == 2:
            server = serverPort[0]
            port = serverPort[1]
        
        baseUrl = '/'.join(urls[1:])
        if not baseUrl.startswith('/'):
            baseUrl = '/' + baseUrl
        
        return (server, port, baseUrl)

    
    def _getAmount(self, amount):
        return fmtMoney(amount)

    
    def cardIsExpired(self, cardExpDate):
        ''' Check if the card is expired or will expire in 15 days.
        @Params: cardExpDate(str): yymm
        @Return: expired(int): 0: not expired
                               1: will expired 15 days
                               2: expired
                               3: cardExpDate is empty
        '''
        if cardExpDate == '':
            return 3
        
        expired = 2
        dateNow = getCurTime('%y%m')
        if dateNow == cardExpDate.strip():
            now = datetime.datetime.now()
            if (now + datetime.timedelta(days = 15)).month == now.month:
                expired = 0
            else:
                expired = 1
        elif dateNow < cardExpDate.strip():
            expired = 0
        else:
            expired = 2
        return expired

    
    def cardHasDeclinedTrs(self, ccId):
        ''' Check if the card has declined trs in declined queue.
        @Params:
        @Return:
        '''
        has = True
        sql = 'SELECT id FROM declinedq WHERE cc_id=?;'
        rows = self.mkcDb.query(sql, 'all', (ccId,))
        if not rows:
            has = False
        
        return has

    
    def getClosedTrsCount(self, ccId):
        ''' Get the closed transaction count for cc.
        @Param ccId(int):
        @Return: trsCount
        '''
        trsCount = 0
        sql = "SELECT COUNT(id) FROM transactions WHERE cc_id=? AND state='closed';"
        row = self.mkcDb.query(sql, 'one', (ccId,))
        if row and row[0]:
            trsCount = row[0]
        
        return trsCount

    
    def getTrsShoppingCartId(self, trsList):
        ''' Get the shopping cart id for the trsList.
        @Params: trsList(list)
        @Return: result(dict): {[shopping_cart_id]: [trsList]}
        '''
        result = { }
        sql = 'SELECT DISTINCT id, shopping_cart_id FROM transactions WHERE id IN (%s);' % ','.join(str(trsId) for trsId in trsList)
        rows = self.mkcDb.query(sql)
        for trsId, shoppingCartId in rows:
            result[shoppingCartId].append(trsId)
        
        return result

    
    def __getDiscType(self, disc):
        ''' Get the shopping cart id for the trsList.
        @Params: disc(Disc)
        @Return: discType(str): DVD/Games/Blu-Ray
        '''
        discType = 'DVD'
        if disc.genre.upper() == 'GAMES':
            discType = 'Games'
        elif str(disc.isBluray) == '1':
            discType = 'Blu-Ray'
        
        return discType

    
    def _getUnusedChipNPin(self):
        ''' Get the unused chip n pin, and cancel it.
        '''
        result = []
        if self._getConfigByKey('payment_options') == 'chipnpin':
            sql = "SELECT id FROM upg WHERE id NOT IN (SELECT DISTINCT upg_id FROM transactions WHERE upg_id!='' AND upg_id!=0) AND id NOT IN (SELECT DISTINCT upg_id FROM reservations WHERE state='reserved') AND result_code=0;"
            rows = self.mkcDb.query(sql)
            for upgId, in rows:
                result.append(upgId)
            
        
        return result

    
    def checkForProsa(self):
        smartEMV = cdll.LoadLibrary('/etc/smartbt/libsmartEMV4010B.so')
        
        try:
            smartEMV.getLastErrorInfo.argtypes = [
                POINTER(c_int),
                c_char_p]
            status = '1'
            m = 'Internal error.'
            port = create_string_buffer('\x00' * 32)
            status = smartEMV.DiscoverPinpadPort(port)
            self.log.info('smartEMV DiscoverPinpadPort=====' + str(status))
            if status == 0:
                status = 11
                m = 'card_reader is not connected'
                return (str(status), m, smartEMV)
            
            smartEMV.SetTimeout(45)
            smartEMV.SetPinpadIdlePrompt('Welcome')
            _init_transaction = smartEMV.InitTransaction()
            if _init_transaction == 1:
                m = 'success'
                return (str(0), m, smartEMV)
            else:
                (errcode, errmsg) = self.showError(smartEMV)
                self.log.info('errcode---------------' + str(errcode) + ', errmsg-------------' + str(errmsg))
                status = '9'
                m = 'Denied transaction by chip'
                return (str(status), m, smartEMV)
        except Exception as ex:
            self.log.error(traceback.format_exc())
            status = 11
            m = 'card_reader is not connected'
            return (str(status), m, smartEMV)


    
    def getCardInfoFromProsa(self, customer, smartEMV):
        """
        @Params: shoppingCart(ShoppingCart Object)
                 customer(Customer Object)
        @Return: Success: (status, m)
                 Notes: status = '0': Approved.
                        status = '1': The Card Reader is not connected
                        status = '4': Can not connect upg server.
                        status = '5': Sorry, the kiosk has not set any account.
                        status = '6': EVT is busy.
                        status = '9'  Denied transaction by chip
                        status = '10': EVT has not been setup or PosServer is down.
                        status = '11': Process failed, please retry.
                        #status = '12': Empty wallet reference, declined it
        """
        emv_request = ''
        
        try:
            smartEMV.SetTransactionType(1)
            smartEMV.SetAmount('200')
            _begin_transaction = smartEMV.BeginTransaction()
            if _begin_transaction is 1:
                accountNumber = create_string_buffer('\x00' * 20)
                expirationDate = create_string_buffer('\x00' * 5)
                holderName = create_string_buffer('\x00' * 70)
                serviceCode = create_string_buffer('\x00' * 5)
                entryMode = create_string_buffer('\x00' * 4)
                trackOne = create_string_buffer('\x00' * 70)
                trackTwo = create_string_buffer('\x00' * 40)
                cryptogram = create_string_buffer('\x00' * 20)
                cryptogramType = create_string_buffer('\x00' * 5)
                
                try:
                    smartEMV.GetAccountNumber(accountNumber)
                    smartEMV.GetExpirationDate(expirationDate)
                    smartEMV.GetCardHolderName(holderName)
                    smartEMV.GetServiceCode(serviceCode)
                    smartEMV.GetEntryMode(entryMode)
                except Exception as ex:
                    self.log.error(traceback.format_exc())
                    self.log.info('entryMode=======' + str(entryMode.value))

                
                try:
                    if entryMode.value is '901' or entryMode.value is '801':
                        smartEMV.GetTrackOne(trackOne)
                    else:
                        emv_request = self.showTags(smartEMV)
                    smartEMV.GetTrackTwo(trackTwo)
                except Exception as ex:
                    self.log.error(traceback.format_exc())

                smartEMV.SetResponseCode(0)
                smartEMV.SetApprovalCode('123456')
                if smartEMV.EndTransaction() is 1:
                    smartEMV.GetCryptogram(cryptogram)
                    smartEMV.GetCryptogramType(cryptogramType)
                    if str(cryptogramType) is '000':
                        status = '9'
                        m = 'Denied transaction by chip'
                        return (str(status), m)
                    else:
                        customer.ccName = holderName.value
                        customer.ccNum = accountNumber.value
                        customer.ccExpDate = expirationDate.value
                        customer.track2 = trackTwo.value
                        customer.oid = emv_request
                        return ('0', 'Successed get Card Info by chip')
                else:
                    (errcode, errmsg) = self.showError(smartEMV)
                    self.log.info('errcode=======' + str(errcode) + ', errmsg=======' + str(errmsg))
                    status = '9'
                    m = 'Denied transaction by chip'
                    return (str(status), m)
            else:
                (errcode, errmsg) = self.showError(smartEMV)
                self.log.info('errcode..................' + str(errcode) + ', errmsg.................' + str(errmsg))
                status = '13'
                m = 'Time Out'
                return (str(status), m)
        finally:
            del smartEMV


    
    def showError(self, smartEMV):
        errorMsg = create_string_buffer('\x00' * 200)
        errorCode = c_int(10)
        smartEMV.getLastErrorInfo(errorCode, errorMsg)
        return (errorCode.value, errorMsg.value)

    
    def showTags(self, smartEMV):
        emv_request = ''
        tagValue = create_string_buffer('\x00' * 1024)
        tagNames = [
            'TAG_9F27',
            'TAG_95',
            'TAG_9F26',
            'TAG_9F02',
            'TAG_9F03',
            'TAG_82',
            'TAG_9F36',
            'TAG_9F1A',
            'TAG_5F2A',
            'TAG_9A',
            'TAG_9C',
            'TAG_9F37',
            'TAG_9F10',
            'TAG_9F1E',
            'TAG_9F33',
            'TAG_9F35',
            'TAG_9F09',
            'TAG_9F34',
            'TAG_84',
            'TAG_4F',
            'TAG_5F34',
            '']
        i = 0
        while tagNames[i] is not '' and i < tagNames.__len__():
            if smartEMV.GetTag(tagNames[i], tagValue) is 1:
                emv_request += tagNames[i]
                tag_leng = len(tagValue.value) / 2
                if tag_leng < 10:
                    tag_leng = '0' + str(tag_leng)
                
                emv_request += str(tag_leng)
                emv_request += tagValue.value
            else:
                self.log.info('Information=====%s unavailable' % tagNames[i])
            i = i + 1
        emv_request = emv_request.replace('TAG_', '')
        emv_request = emv_request.replace(' ', '')
        self.log.info('emv_request=======' + emv_request)
        return emv_request



class PreauthQueue(object):
    '''
    Enable a queue for preauth.
    '''
    
    def __init__(self, acctId, ccId):
        self.acctId = acctId
        self.ccId = ccId
        self.mkcDb = None
        self.mkcDb = Db(MKC_DB_PATH)

    
    def __del__(self):
        del self.mkcDb

    
    def add(self, amount, oid, upgId, preauthTime = ''):
        if upgId and str(upgId) != '0':
            sql = 'insert into preauthq(cc_id, upg_acct_id, amount, oid, preauth_time, last_access_time, state, upg_id) values(:ccId, :acctId,:amount, :oid, :preauthTime, :lastAccessTime, :state, :upg_id);'
            params = { }
            params['ccId'] = self.ccId
            params['acctId'] = self.acctId
            params['amount'] = amount
            params['oid'] = oid
            if preauthTime:
                params['preauthTime'] = preauthTime
            else:
                params['preauthTime'] = getCurTime()
            params['lastAccessTime'] = params['preauthTime']
            params['state'] = 'open'
            params['upg_id'] = upgId
            pqId = self.mkcDb.update(sql, params)
            upgProxy = UPGProxy.getInstance()
            params['preauthqId'] = pqId
            params['syncType'] = 'add'
            upgProxy.syncData('dbSyncPreauthq', params)
            return pqId
        

    
    def remove(self, pqid):
        ''' Remove from the preauth queue '''
        params = { }
        params['preauthqId'] = pqid
        for i in range(5):
            
            try:
                sql = 'delete from preauthq where id=:preauthqId;'
                self.mkcDb.update(sql, params)
            except Exception as ex:
                if i == 4:
                    raise 
                
            except:
                i == 4

        
        upgProxy = UPGProxy.getInstance()
        params['syncType'] = 'delete'
        upgProxy.syncData('dbSyncPreauthq', params)

    
    def inQueue(self, pqid):
        ''' Check if it is in queue '''
        inQueue = False
        sql = 'SELECT id from preauthq where id=:pqid;'
        row = self.mkcDb.query(sql, 'one', {
            'pqid': pqid })
        if row:
            inQueue = True
        
        return inQueue

    
    def getByAmount(self, amount):
        self.rmExpired()
        pq = { }
        sql = "SELECT id, oid, upg_id FROM preauthq WHERE cc_id=:ccId and upg_acct_id=:acctId AND amount>=:amount AND STATE='open' ORDER BY preauth_time DESC;"
        row = self.mkcDb.query(sql, 'one', {
            'ccId': self.ccId,
            'acctId': self.acctId,
            'amount': amount })
        if row:
            (pqid, oid, upgId) = row
            self._setToUsed(pqid)
            pq['pq_id'] = pqid
            pq['oid'] = oid
            pq['upg_id'] = upgId
        
        return pq

    
    def _setToUsed(self, pqid):
        ''' Set the upg to used.
        Delete it from queue.
        '''
        self.remove(pqid)

    
    def rmExpired(self):
        ''' Remove the PREAUTH before 3 days. '''
        
        try:
            expiredDay = getTimeChange(getCurTime('%Y-%m-%d 23:59:59'), day = -3)
            sql = 'SELECT preauth_time FROM preauthq WHERE preauth_time<:expiredDay;'
            if self.mkcDb.query(sql, 'all', {
                'expiredDay': expiredDay }):
                sql = 'DELETE FROM preauthq WHERE preauth_time<:expiredDay;'
                self.mkcDb.update(sql, {
                    'expiredDay': expiredDay })
                upgProxy = UPGProxy.getInstance()
                params = { }
                params['syncType'] = 'rmexpired'
                params['expiredDay'] = expiredDay
                upgProxy.syncData('dbSyncPreauthq', params)
        except Exception as ex:
            pass




class PostauthQueue(object):
    '''
    Enable a queue for postauth.
    '''
    
    def __init__(self):
        self.mkcDb = None
        self.mkcDb = Db(MKC_DB_PATH)

    
    def __del__(self):
        del self.mkcDb

    
    def add(self):
        ''' Add pending trs into postauthq, for delay postauth. '''
        sql = "SELECT id, upg_id, shopping_cart_id, in_time, out_time, amount, cc_id, 'open' as state, upg_account_id, card_type FROM transactions WHERE id NOT IN (SELECT DISTINCT transaction_id FROM postauthq) AND id NOT IN (SELECT DISTINCT transaction_id FROM declinedq) AND state LIKE '%pending' AND (upg_id>=0 OR upg_id='');"
        rows = self.mkcDb.query(sql)
        postList = []
        curTime = getCurTime()
        for row in rows:
            (trs_id, upg_id, shopping_cart_id, in_time, out_time, amount, cc_id, state, upg_account_id, card_type) = row
            trsTime = curTime
            if in_time:
                trsTime = in_time
            elif out_time:
                trsTime = out_time
            
            postList.append((trs_id, upg_id, shopping_cart_id, trsTime, amount, cc_id, state, upg_account_id, card_type))
        
        if postList:
            sql = 'INSERT INTO postauthq(transaction_id,upg_id,shopping_cart_id,add_time,amount,cc_id,state,acct_id,card_type) VALUES(?,?,?,?,?,?,?,?,?);'
            self.mkcDb.updateMany(sql, postList)
            params = { }
            params['syncType'] = 'add'
            params['postList'] = postList
            upgProxy = UPGProxy.getInstance()
            upgProxy.syncData('dbSyncPostauthqV3', params)
        
        '\n        sql = "insert into postauthq(transaction_id, upg_id, shopping_cart_id,"               "add_time, amount, cc_id, state, acct_id) select id, upg_id, "               "shopping_cart_id, in_time, amount, cc_id, \'open\' as state,"               "upg_account_id "               "FROM transactions WHERE in_time IS NOT NULL AND in_time!=\'\' "               "AND id NOT IN (SELECT DISTINCT transaction_id FROM postauthq) "               "AND id NOT IN (SELECT DISTINCT transaction_id FROM declinedq) "               "AND state LIKE \'%pending\' AND (upg_id>=0 OR upg_id=\'\');"\n        self.mkcDb.update(sql)\n\n        # Rental auto to sale.\n        # Test mode, upg_id=-1, do not need postauth.\n        curTime = getCurTime()\n        sql = "insert into postauthq(transaction_id, upg_id, shopping_cart_id,"               "add_time, amount, cc_id, state, acct_id) select id, upg_id, "               "shopping_cart_id, ? as inTime, amount, cc_id, \'open\' as state,"               "upg_account_id "               "FROM transactions WHERE (in_time IS NULL OR in_time=\'\') "               "AND id NOT IN (SELECT DISTINCT transaction_id FROM postauthq) "               "AND id NOT IN (SELECT DISTINCT transaction_id FROM declinedq) "               "AND state LIKE \'%pending\' AND (upg_id>=0 OR upg_id=\'\');"\n        self.mkcDb.update(sql, (curTime, ))\n        '
        return None

    
    def getNeedPostauth(self, delayHours = 1):
        ''' Get need postauth trs. '''
        cutoffTime = getTimeChange(getCurTime(), hour = -delayHours)
        sql = "SELECT id,transaction_id,upg_id,add_time,cc_id,state,acct_id, (SELECT amount FROM transactions WHERE id=postauthq.transaction_id) ,card_type FROM postauthq WHERE upg_id IN (SELECT upg_id FROM postauthq WHERE upg_id>0 AND upg_id!='' AND upg_id IS NOT NULL AND add_time<=? GROUP BY upg_id ORDER BY MIN(add_time));"
        rows = self.mkcDb.query(sql, 'all', (cutoffTime,))
        result = []
        tmpResult = { }
        for row in rows:
            (postauthqId, transaction_id, upg_id, add_time, cc_id, state, acct_id, amount, card_type) = row
            tmp = { }
            tmp['postauthqId'] = postauthqId
            tmp['transaction_id'] = transaction_id
            tmp['upg_id'] = upg_id
            tmp['add_time'] = add_time
            tmp['amount'] = amount
            tmp['cc_id'] = cc_id
            tmp['state'] = state
            tmp['acct_id'] = acct_id
            if upg_id not in tmpResult:
                t = {
                    'upg_id': upg_id,
                    'amount': 0,
                    'trs_ids': [],
                    'data': [],
                    'cc_id': cc_id,
                    'acct_id': acct_id,
                    'card_type': card_type }
                tmpResult[upg_id] = t
            
            tmpResult[upg_id]['amount'] = tmpResult[upg_id]['amount'] + amount
            tmpResult[upg_id]['trs_ids'].append(transaction_id)
            tmpResult[upg_id]['data'].append(tmp)
        
        result = list(tmpResult.values())
        if not result:
            tmpResult = { }
            sql = "SELECT id, transaction_id, upg_id, add_time, cc_id,state, acct_id, shopping_cart_id, card_type,(SELECT amount FROM transactions WHERE id=postauthq.transaction_id) FROM postauthq WHERE shopping_cart_id IN (SELECT shopping_cart_id FROM postauthq WHERE (upg_id IS NULL OR upg_id=0 OR upg_id='') AND add_time<=? GROUP BY shopping_cart_id ORDER BY MIN(add_time) limit 1);"
            rows = self.mkcDb.query(sql, 'all', (cutoffTime,))
            for row in rows:
                (postauthqId, transaction_id, upg_id, add_time, cc_id, state, acct_id, shopping_cart_id, card_type, amount) = row
                tmp = { }
                tmp['postauthqId'] = postauthqId
                tmp['transaction_id'] = transaction_id
                tmp['upg_id'] = upg_id
                tmp['add_time'] = add_time
                tmp['amount'] = amount
                tmp['cc_id'] = cc_id
                tmp['state'] = state
                tmp['acct_id'] = acct_id
                if shopping_cart_id not in tmpResult:
                    t = {
                        'upg_id': upg_id,
                        'amount': 0,
                        'trs_ids': [],
                        'data': [],
                        'cc_id': cc_id,
                        'acct_id': acct_id,
                        'card_type': card_type }
                    tmpResult[shopping_cart_id] = t
                
                tmpResult[shopping_cart_id]['amount'] = tmpResult[shopping_cart_id]['amount'] + amount
                tmpResult[shopping_cart_id]['trs_ids'].append(transaction_id)
                tmpResult[shopping_cart_id]['data'].append(tmp)
            
            result.extend(list(tmpResult.values()))
        
        return result

    
    def getOtherTrsIsByUpgId(self, upgId, trsIds):
        ''' '''
        trsIdsStr = '(%s)' % ','.join(str(trsId) for trsId in trsIds)
        sql = "SELECT id FROM transactions WHERE upg_id=? AND state!='closed' AND id NOT IN %s;" % trsIdsStr
        rows = self.mkcDb.query(sql, 'all', (upgId,))
        result = []
        for row in rows:
            (trsId,) = row
            result.append(trsId)
        
        return result

    
    def getOtherTrsIsByUpgIdV2(self, upgId, trsIds):
        ''' '''
        trsIdsStr = '(%s)' % ','.join(str(trsId) for trsId in trsIds)
        sql = "SELECT id, amount FROM transactions WHERE upg_id=? AND state!='closed' AND id NOT IN %s;" % trsIdsStr
        rows = self.mkcDb.query(sql, 'all', (upgId,))
        result = []
        for row in rows:
            (trsId, amount) = row
            result.append({
                'trs_id': trsId,
                'amount': amount })
        
        return result

    
    def removeByTrsIds(self, trsIds):
        ''' Remove from the postauth queue by trsIds. '''
        print(trsIds)
        trsIdsStr = '(%s)' % ','.join(str(trsId) for trsId in trsIds)
        print(trsIdsStr)
        for i in range(5):
            
            try:
                sql = 'delete from postauthq where transaction_id IN %s;' % trsIdsStr
                print(sql)
                self.mkcDb.update(sql)
                params = { }
                params['syncType'] = 'deleteByTrsIds'
                params['trsIds'] = trsIds
                upgProxy = UPGProxy.getInstance()
                upgProxy.syncData('dbSyncPostauthqV3', params)
            except Exception as ex:
                if i == 4:
                    raise 
                
            except:
                i == 4

        

    
    def updateAddTimeByTrsIds(self, newTime, trsIds):
        ''' Update the add time, for debit card of ZA. '''
        trsIdsStr = '(%s)' % ','.join(str(trsId) for trsId in trsIds)
        sql = 'UPDATE postauthq SET add_time=? WHERE transaction_id IN %s;' % trsIdsStr
        self.mkcDb.update(sql, (newTime,))
        params = { }
        params['syncType'] = 'updateAddTimeByTrsIds'
        params['trsIds'] = trsIds
        params['newTime'] = newTime
        upgProxy = UPGProxy.getInstance()
        upgProxy.syncData('dbSyncPostauthqV3', params)



class DeclinedQueue(object):
    '''
    Enable a queue for declined.
    '''
    
    def __init__(self):
        self.mkcDb = None
        self.mkcDb = Db(MKC_DB_PATH)

    
    def __del__(self):
        del self.mkcDb

    
    def add(self, params):
        ''' Add declined trs into declinedq. '''
        sql = 'SELECT transaction_id FROM declinedq WHERE transaction_id=:transaction_id;'
        if not self.mkcDb.query(sql, 'one', params):
            sql = 'INSERT INTO declinedq(transaction_id, upg_id, cc_id, amount, process_time, next_process_time, process_count, state, acct_id , card_type) VALUES(:transaction_id, :upg_id, :cc_id, :amount, :process_time, :next_process_time, :process_count, :state, :acct_id, :card_type);'
            self.mkcDb.update(sql, params)
            upgProxy = UPGProxy.getInstance()
            params['syncType'] = 'add'
            upgProxy.syncData('dbSyncDeclinedqV3', params)
            return None
        

    
    def remove(self, declinedqId):
        ''' Remove from the declinedq queue '''
        params = { }
        params['declinedqId'] = declinedqId
        tries = 5
        for i in range(tries):
            
            try:
                sql = 'delete from declinedq where id=:declinedqId;'
                self.mkcDb.update(sql, params)
            except Exception as ex:
                if i == tries - 1:
                    raise 
                
            except:
                i == tries - 1

        
        upgProxy = UPGProxy.getInstance()
        params['syncType'] = 'delete'
        upgProxy.syncData('dbSyncDeclinedqV3', params)

    
    def removeByTrsIds(self, trsIds):
        ''' Remove from the declinedq queue '''
        trsIdsStr = '(%s)' % ','.join(str(trsId) for trsId in trsIds)
        tries = 5
        for i in range(tries):
            
            try:
                sql = 'delete from declinedq where transaction_id IN %s;' % trsIdsStr
                self.mkcDb.update(sql)
            except Exception as ex:
                if i == tries - 1:
                    raise 
                
            except:
                i == tries - 1

        
        upgProxy = UPGProxy.getInstance()
        params = { }
        params['syncType'] = 'deletebytrsids'
        params['trsIds'] = trsIds
        upgProxy.syncData('dbSyncDeclinedqV3', params)

    
    def getDeclinedTrs(self, cutoffTime, processCountLimit = 7):
        ''' Get declined trs. '''
        sql = "SELECT id, transaction_id, upg_id, cc_id, process_time, next_process_time, process_count, state, acct_id, card_type,(SELECT amount FROM transactions WHERE id=declinedq.transaction_id) FROM declinedq WHERE upg_id IN (SELECT upg_id FROM declinedq WHERE next_process_time<=? AND state='open' GROUP BY upg_id ORDER BY MIN(next_process_time) );"
        rows = self.mkcDb.query(sql, 'all', (cutoffTime,))
        result = []
        tmpResult = { }
        for row in rows:
            (declinedqId, transaction_id, upg_id, cc_id, process_time, next_process_time, process_count, state, acct_id, card_type, amount) = row
            tmp = { }
            tmp['declinedqId'] = declinedqId
            tmp['transaction_id'] = transaction_id
            tmp['upg_id'] = upg_id
            tmp['cc_id'] = cc_id
            tmp['amount'] = amount
            tmp['process_time'] = process_time
            tmp['next_process_time'] = next_process_time
            tmp['process_count'] = process_count
            tmp['state'] = state
            tmp['acct_id'] = acct_id
            if upg_id not in tmpResult:
                t = {
                    'upg_id': upg_id,
                    'amount': 0,
                    'trs_ids': [],
                    'data': [],
                    'cc_id': cc_id,
                    'acct_id': acct_id,
                    'process_count': process_count,
                    'card_type': card_type }
                tmpResult[upg_id] = t
            
            tmpResult[upg_id]['amount'] = tmpResult[upg_id]['amount'] + amount
            tmpResult[upg_id]['trs_ids'].append(transaction_id)
            tmpResult[upg_id]['data'].append(tmp)
        
        result = list(tmpResult.values())
        return result

    
    def update(self, params):
        ''' Update from the declinedq queue by trsIds. '''
        for i in range(5):
            
            try:
                sql = 'update declinedq set amount=:amount, process_time=:process_time, next_process_time=:next_process_time, process_count=:process_count, state=:state, acct_id=:acct_id where id=:declinedqId;'
                self.mkcDb.update(sql, params)
            except Exception as ex:
                if i == 4:
                    raise 
                
            except:
                i == 4

        
        upgProxy = UPGProxy.getInstance()
        params['syncType'] = 'update'
        upgProxy.syncData('dbSyncDeclinedqV3', params)



class TrsProcessQueue(object):
    '''
    Enable a queue for transaction process.
    One transaction has been processed successfully, add it into the queue,
    if the
    '''
    
    def __init__(self):
        self.mkcDb = None
        self.mkcDb = Db(MKC_DB_PATH)

    
    def __del__(self):
        del self.mkcDb

    
    def add(self, trsId):
        ''' Add processed trs into queue.
        @Params: trsId(int)
        @Return: None
        '''
        status = 0
        sql = 'INSERT INTO trs_process(transaction_id, process_time) VALUES(:transaction_id, :process_time);'
        p = {
            'transaction_id': trsId,
            'process_time': getCurTime() }
        self.mkcDb.update(sql, p)
        return None

    
    def getCount(self, trsId):
        ''' Get the process count if the transaction is processed.
        @Params: trsId(int)
        @Return: qCount(int)
        '''
        curDate = getCurTime('%Y-%m-%d')
        sql = 'SELECT COUNT(id) FROM trs_process WHERE transaction_id=:transaction_id AND process_time>=:start AND process_time<=:end;'
        p = { }
        p['transaction_id'] = trsId
        p['start'] = '%s 00:00:00' % curDate
        p['end'] = '%s 23:59:59' % curDate
        row = self.mkcDb.query(sql, 'one', p)
        qCount = 0
        if row:
            (qCount,) = row
        
        return qCount



class Preauth(Trade):
    ''' Preauth class '''
    
    def __init__(self, kioskId, upgServer, upgPort, upgBaseUrl, upgTrsMode = 'LIVE'):
        ''' '''
        super(Preauth, self).__init__(kioskId, upgServer, upgPort, upgBaseUrl, upgTrsMode)

    
    def trade(self, acctId, cardNum, expDate, nameOnCard, amount, track2 = '', track1 = '', oid = '', ignore_bl = 0, zipcode = None, trsPasswd = None):
        trsCode = ''
        trsMsg = ''
        
        try:
            trsType = 'PREAUTH'
            r = Trade.trade(self, acctId, trsType, cardNum, expDate, nameOnCard, amount, track2, track1, oid, ignore_bl, zipcode, trsPasswd)
            (trsCode, trsMsg, oid) = r
        except UpgInternalError as ex:
            trsCode = '-1'
            m = 'Internal Error when preauth from UPG: %s' % ex
            trsMsg = m
            self.log.error(m)
        except Exception as ex:
            trsCode = '-2'
            m = 'Local Error when preauth from UPG: %s' % ex
            trsMsg = m
            self.log.error(m)

        return (trsCode, trsMsg, oid)



class Postauth(Trade):
    ''' Preauth class '''
    
    def __init__(self, kioskId, upgServer, upgPort, upgBaseUrl, upgTrsMode = 'LIVE'):
        ''' '''
        super(Postauth, self).__init__(kioskId, upgServer, upgPort, upgBaseUrl, upgTrsMode)

    
    def trade(self, acctId, cardNum, expDate, nameOnCard, amount, track2 = '', track1 = '', oid = '', ignore_bl = 0):
        trsCode = ''
        trsMsg = ''
        
        try:
            trsType = 'POSTAUTH'
            r = Trade.trade(self, acctId, trsType, cardNum, expDate, nameOnCard, amount, track2, track1, oid, ignore_bl)
            (trsCode, trsMsg, oid) = r
        except UpgInternalError as ex:
            trsCode = '-1'
            m = 'Internal Error when preauth from UPG: %s' % ex
            trsMsg = m
            self.log.error(m)
        except Exception as ex:
            trsCode = '-2'
            m = 'Local Error when preauth from UPG: %s' % ex
            trsMsg = m
            self.log.error(m)

        return (trsCode, trsMsg, oid)



class Sale(Trade):
    ''' Preauth class '''
    
    def __init__(self, kioskId, upgServer, upgPort, upgBaseUrl, upgTrsMode = 'LIVE'):
        ''' '''
        super(Sale, self).__init__(kioskId, upgServer, upgPort, upgBaseUrl, upgTrsMode)

    
    def trade(self, acctId, cardNum, expDate, nameOnCard, amount, track2 = '', track1 = '', oid = '', ignore_bl = 0):
        trsCode = ''
        trsMsg = ''
        
        try:
            trsType = 'SALE'
            r = Trade.trade(self, acctId, trsType, cardNum, expDate, nameOnCard, amount, track2, track1, oid, ignore_bl)
            (trsCode, trsMsg, oid) = r
        except UpgInternalError as ex:
            trsCode = '-1'
            m = 'Internal Error when preauth from UPG: %s' % ex
            trsMsg = m
            self.log.error(m)
        except Exception as ex:
            trsCode = '-2'
            m = 'Local Error when preauth from UPG: %s' % ex
            trsMsg = m
            self.log.error(m)

        return (trsCode, trsMsg, oid)



def testPreauthCard():
    print('testPreauthCard')
    import sys
    sys.path.append(MKC_PATH)
    import mobject
    customer = mobject.Customer()
    customer.ccName = 'LU/PIN*LU'
    customer.ccNum = '4988820004558168'
    customer.ccExpDate = '0908'
    customer.track1 = 'B4988820004558168^LU/PIN*LU ^0908101100000000085000000'
    customer.track2 = ''
    shoppingCart = mobject.ShoppingCart()
    disc = mobject.Disc()
    disc.gene = 'rent'
    disc.preauthAmount = '12'
    disc.rfid = '0010BF2730000104E0'
    disc.upc = '043396321595'
    disc.slotID = '105'
    disc.title = 'Fired Up! (2009)'
    disc.salePrice = '39'
    disc.pricePlan = 'First Night Fee \xef\xbf\xbd1.99,\nAdditional Night Fee \xef\xbf\xbd1.99,\nCutoff Time 23:59:59;'
    shoppingCart.addDisc(disc)
    upgP = UPGProxy.getInstance()
    print(upgP.preauthCard(customer, shoppingCart))


def testPostauth():
    '''
    Postauth method will be used in postauth thread.
    '''
    print('testPostauth')
    acctId = '2006'
    kioskId = 'sky'
    ccId = 3
    trade = Trade(acctId, kioskId, ccId)
    '\n    # Total amount passed is more than the PreAuth amount.\n    # It will failed because amount is more than preauth, test successfully.\n    amount = 0.02\n    upgId = 11\n    autoToSale = False\n    msg = "Total amount passed is more than the PreAuth amount."\n    print msg\n    print trade.postauth(amount, upgId, autoToSale)\n    '
    '\n    # Successful to postauth.\n    # It will success, test successfully.\n    amount = 0.01\n    upgId = 11\n    autoToSale = False\n    print trade.postauth(amount, upgId, autoToSale)\n    '
    amount = 0.02
    upgId = 12
    autoToSale = True
    print(trade.postauth(amount, upgId, autoToSale))
    '\n    # TODO: Test some overdue oid, there is no overdue oid to test.amount = 0.02\n    upgId = 12\n    autoToSale = True\n    print trade.postauth(amount, upgId, autoToSale)\n    '


def testGetCcInfoByCustomer():
    import sys
    sys.path.append(MKC_PATH)
    import mobject
    customer = mobject.Customer()
    customer.ccName = 'LU/PIN*LU'
    customer.ccNum = '4988820004558168'
    customer.ccExpDate = '0908'
    customer.track1 = 'B4988820004558168^LU/PIN*LU ^0908101100000000085000000'
    customer.track2 = ''
    upgP = UPGProxy.getInstance()
    print(upgP.getCCInfoByCustomer(customer))
    print(customer)
    del upgP


def testSitefSale():
    import sys
    sys.path.append(MKC_PATH)
    import mobject
    customer = mobject.Customer()
    customer.ccName = 'LU/PIN*LU'
    customer.ccNum = '4988820004558168'
    customer.ccExpDate = '0908'
    customer.track1 = 'B4988820004558168^LU/PIN*LU ^0908101100000000085000000'
    customer.track2 = ''
    upgP = UPGProxy.getInstance()
    print(upgP.charge_sitef(customer, '', 3))


def testGetCCInfoByCcId():
    upgP = UPGProxy.getInstance()
    print(upgP.getCCInfoByCcId(1))
    del upgP


def test():
    testPreauthCard()

if __name__ == '__main__':
    upgP = UPGProxy.getInstance()
    upgP.checkForProsa()

