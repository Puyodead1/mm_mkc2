# Source Generated with Decompyle++
# File: ums_proxy.pyc (Python 2.5)

''' Ums Proxy.
##
##  Change Log:
##      2010-12-08 Modified by Tim
##          add new functions checkEmailForCerePay, getCardInfoForCerePay, 
##          registerCerePayCard
##      2010-09-27 Modified by Tim
##          Change the syncDataRemoteKiosk to syncDataNoSequence
##      2010-07-15 Modified by Tim
##          Add new api getMemberCouponForKiosk, getMemberRecommendationForKiosk
##      2010-07-13 Modified by Tim
##          Add two api changeMemberPasswdForKiosk, setMemberDetailByEmail
##          change the api setMemberDetail
##      2010-03-26 Modified by Tim
##          Add msDiscType for MS.
##      2010-02-05 Modified by Tim
##          Add msKeepCount for MS.
##      2009-11-24 Modified by Tim
##          For #1942, S250 Monthly Subscription Integration.
##      2009-09-04 Modified by Tim
##          Change function setMemberDetail(), only filter the need remove
##          discs, doNOT remove the discs from shopping cart.
##      2009-09-01 Modified by Tim
##          Add new function sendChargedReceipt().
##      2009-01-07 Modified by Tim
##          Add function getMemberMailByCc.
##      2008-12-23 Modified by Tim
##          Add a param shoppingCardId for registerToUms.
##      2008-11-06 Created by Tim
##
'''
import os
import re
import time
import base64
import datetime
from .base_proxy import Proxy
from .mda import Db, DatabaseError
from .config import *
from .tools import RemoteError, getCurTime
from .upg_proxy import UPGProxy
PROXY_NAME = 'UMS_PROXY'

class UmsProxy(Proxy):
    '''
    All Proxy function.
    '''
    
    def __init__(self):
        pass

    
    def __del__(self):
        super(UmsProxy, self).__del__()

    
    def on_init(self):
        super(UmsProxy, self).__init__(PROXY_NAME)

    
    def __new__(cls, *args, **kwargs):
        if '_inst' not in vars(cls):
            cls._inst = object.__new__(cls, *args, **kwargs)
            cls._inst.on_init()
        
        return cls._inst

    
    def getInstance():
        return UmsProxy()

    getInstance = staticmethod(getInstance)
    
    def registerMember(self, customer, need_receive_news = False):
        ''' Register from ums, the password id the last 4 digits of
        the credit number.
        @Params: customer(Customer Object)
        @Return: status(str)
        '''
        status = 0
        mailAddr = customer.email
        ccId = customer.ccid
        ccNum = customer.ccNum
        self.log.info('Register to ums for mail:%s cc: %s...need_receive_news:%s' % (mailAddr, ccId, need_receive_news))
        params = { }
        params['email'] = mailAddr
        params['cc_id'] = ccId
        params['cc_number'] = ccNum
        params['need_receive_news'] = need_receive_news
        if params['email']:
            self.syncDataNoSequence('registerMemberForKiosk', params)
        
        status = 1
        self.log.info('Successfully add into the delay queue for mail(%s).' % mailAddr)
        return str(status)

    
    def sendReceipt(self, customer, shoppingCart):
        '''
        Send receipt if not in test mode.
        @Params: customer(Customer Object)
                 shoppingCart(ShoppingCart Object)
        @Return: status(str)
        '''
        status = 0
        scId = str(shoppingCart.id)
        mailAddr = str(customer.email)
        self.log.info('Send receipt for shopping cart: %s to %s...' % (scId, mailAddr))
        params = { }
        params['email'] = mailAddr
        params['shopping_cart_id'] = scId
        self.syncDataNoSequence('sendReceiptForKiosk', params)
        status = 1
        self.log.info('Successfully add into the delay queue for mail(%s) shoppingCartId %s.' % (mailAddr, scId))
        return str(status)

    
    def sendChargedReceipt(self, ccId, shoppingCardId, trsList = []):
        '''
        Send receipt if not in test mode for charged transactions.
        @Params: ccId(int)
                 shoppingCardId(str)
                 trsList(list): list of transaction ids.
        @Return: status(str)
        '''
        status = 0
        
        try:
            self.log.info('Charged Receipt for %s on %s' % (trsList, shoppingCardId))
            params = { }
            params['kiosk_id'] = self.kioskId
            params['cc_id'] = ccId
            params['shopping_cart_id'] = shoppingCardId
            params['trs_list'] = trsList
            self.syncDataNoSequence('sendChargedReceiptForKiosk', params)
            status = 1
        except Exception as ex:
            self.log.error('Error in sendChargedReceipt for %s on %s: %s' % (trsList, shoppingCardId, ex))

        return str(status)

    
    def getMemberInfoByCustomer(self, customer):
        ''' Get mail from the api from service.
        @Params: ccId(int):
        @Return: mail
        '''
        info = { }
        self._getTestMode()
        if self.UPG_SHOW_MODE:
            return info
        
        ccId = customer.ccid
        self.log.info('Get member information for cc %s' % ccId)
        number = customer.ccNum
        params = { }
        params['cc_id'] = ccId
        params['card_number'] = number
        tmp = self.getRemoteData('getInfoForKioskByCc', params)
        if tmp['result'] != 'ok':
            raise RemoteError(tmp['zdata'])
        else:
            info = tmp['zdata']
        return info

    
    def getInfoForKioskByEmail(self, email, passwd):
        ''' Get member information from the api from service.
        @Params: email(str):
                 passwd(str):
        @Return: {}
        '''
        info = { }
        self._getTestMode()
        if self.UPG_SHOW_MODE:
            return info
        
        self.log.info('Get member information for email %s' % email)
        params = { }
        params['email'] = email
        params['passwd'] = passwd
        tmp = self.getRemoteData('getInfoForKioskByEmail', params)
        if tmp['result'] != 'ok':
            raise RemoteError(tmp['zdata'])
        else:
            info = tmp['zdata']
        return info

    
    def getMemberInfoByMail(self, mail, passwd):
        ''' Get member info by mail.
        @Params: mail(str):
        @Return: info(dict): {}
        '''
        info = { }
        self._getTestMode()
        if self.UPG_SHOW_MODE:
            return info
        
        self.log.info('Get member info for mail %s' % mail)
        params = { }
        params['email'] = mail
        tmp = self.getRemoteData('getMemberInfoForKioskByMail', params)
        if tmp['result'] != 'ok':
            self.log.error('getMemberInfoByMail(%s): %s' % (mail, tmp))
        else:
            info = tmp['zdata']
        return info

    
    def changeMemberPasswdForKiosk(self, customer, oldPasswd, newPasswd):
        ''' Get member info by mail.
        @Params: customer(Customer):
                 oldPasswd(str):
                 newPasswd(str):
        @Return: result(dict): {}
            status: 0: success
                    1: old password is incorrect
                    2: the format of new password is incorrect
                    3: internal error
        '''
        result = { }
        self._getTestMode()
        if self.UPG_SHOW_MODE:
            return result
        
        self.log.info('changeMemberPasswdForKiosk %s' % customer.email)
        params = { }
        params['email'] = customer.email
        params['member_id'] = customer.memberID
        params['old_passwd'] = oldPasswd
        params['new_passwd'] = newPasswd
        tmp = self.getRemoteData('changeMemberPasswdForKiosk', params)
        if tmp['result'] != 'ok':
            self.log.error('changeMemberPasswdForKiosk(%s): %s' % (customer.email, tmp))
        else:
            result = tmp['zdata']
        return str(result.get('status', 3))

    
    def addWannaSeeForKiosk(self, mail, upc):
        ''' Get member info by mail.
        @Params: mail(str):
                 upc(str):
        @Return: status(int):
        '''
        status = 0
        
        try:
            params = { }
            params['email'] = mail
            params['upc'] = upc
            self.syncDataNoSequence('addWannaSeeForKiosk', params)
            self.log.info('addWannaSeeForKiosk %s, %s' % (mail, upc))
            status = 1
        except Exception as ex:
            self.log.error('Failed add wanna see for %s, %s: %s' % (mail, upc, ex))

        return str(status)

    
    def setMemberDetail(self, customer, shoppingCart):
        '''
        Set the customer information, full in all attribute of "customer"
        remove the disc by rating of the shopping cart.
        Set the "preauthAmount" of discs in shopping cart due to customer\'s level.
        @return: status(str), needRemove(list)
                    status: 0 get successfully
                            1 get successfully and R rating reached
                            2 network error
                            3 internal error
                            4 CerePay card does NOT bind to any CerePay account
                            5 missing CerePay card
                            6 CerePay account has been suspended or frozen
        '''
        status = '0'
        needRemove = []
        
        try:
            if not (customer.ccid):
                proxy = UPGProxy.getInstance()
                s = proxy.getCCInfoByCustomer(customer)
                del proxy
                if s == 1:
                    raise Exception('Internal error in setMemberDetail when getCCInfoByCustomer.')
                elif s == 2:
                    raise RemoteError('Remote error in setMemberDetail when getCCInfoByCustomer.')
                
            
            info = self.getMemberInfoByCustomer(customer)
            self.log.info('setMemberDetail %s: %s' % (customer.ccid, info.get('email', '')))
            if not info:
                info = { }
            
            email = info.get('email', '')
            age = self.getAge(info.get('birth_year', ''))
            memberRating = info.get('member_rating', '')
            memberID = info.get('member_id', '')
            firstName = info.get('first_name', '')
            lastName = info.get('last_name', '')
            cerepay = info.get('cerepay', { })
            primaryCcId = customer.ccid
            primaryCcNumber = customer.ccNum
            allCcIds = [
                customer.ccid]
            gender = info.get('gender', '')
            isMember = False
            if email:
                isMember = True
            elif str(customer.cardType) == '3':
                if str(cerepay.get('errCode', '')) == '0':
                    status = '4'
                elif str(cerepay.get('errCode', '')) == '1015':
                    status = '5'
                elif str(cerepay.get('acctState', '')) in ('suspended', 'frozen'):
                    status = '6'
                
            
            customer.email = email
            customer.age = age
            customer.level = memberRating
            customer.memberID = memberID
            customer.isMember = isMember
            customer.firstName = firstName
            customer.lastName = lastName
            customer.primaryCcId = primaryCcId
            customer.primaryCcNumber = primaryCcNumber
            customer.allCcIds = allCcIds
            customer.gender = gender
            self._setCustomerCerePayInfo(customer, cerepay)
            if self.isRatingLock() and age < 17:
                for disc in shoppingCart.discs:
                    if disc.rating.upper().strip() in ('R',):
                        status = '1'
                        needRemove.append(disc)
                    
                
            
            self.chkMemberRating(memberRating, shoppingCart)
            self.setMonthlySubscptForMember(customer, info.get('month_subs', { }))
        except RemoteError as ex:
            status = '2'
            self.log.error('Remote Error when setMemberDetail: %s' % ex)
        except Exception as ex:
            status = '3'
            self.log.error('Internal Error when setMemberDetail: %s' % ex)

        return (status, needRemove)

    
    def setMemberDetailByEmail(self, customer, passwd):
        '''
        Set the customer information, full in all attribute of "customer"
        status:
         0: success
         1: member does not exist
         2: member is inactived
         3: member is removed
         4: member is locked
         5: password is incorrect
         6: remote error
         7: internal error
        '''
        status = '7'
        
        try:
            info = self.getInfoForKioskByEmail(customer.email, passwd)
            self.log.info('setMemberDetailByEmail: %s' % info)
            status = info.get('result_status', '7')
            email = info.get('email', '')
            age = self.getAge(info.get('birth_year', ''))
            memberRating = info.get('member_rating', '')
            memberID = info.get('member_id', '')
            firstName = info.get('first_name', '')
            lastName = info.get('last_name', '')
            primaryCcId = info.get('primary_cc_id', '')
            primaryCcNumber = info.get('primary_cc_number', '')
            allCcIds = info.get('all_cc_ids', [])
            gender = info.get('gender', '')
            cerepay = info.get('cerepay', { })
            isMember = False
            if email:
                isMember = True
            
            if cerepay.get('errCode', -1) != 0:
                cerepay = { }
            
            customer.email = email
            customer.age = age
            customer.level = memberRating
            customer.memberID = memberID
            customer.isMember = isMember
            customer.firstName = firstName
            customer.lastName = lastName
            customer.primaryCcId = primaryCcId
            customer.primaryCcNumber = primaryCcNumber
            customer.allCcIds = allCcIds
            customer.gender = gender
            self._setCustomerCerePayInfo(customer, cerepay)
            self.setMonthlySubscptForMember(customer, info.get('month_subs', { }))
        except RemoteError as ex:
            status = '6'
            self.log.error('Remote Error when setMemberDetailByEmail: %s' % ex)
        except Exception as ex:
            status = '7'
            self.log.error('Internal Error when setMemberDetailByEmail: %s' % ex)

        return str(status)

    
    def getMemberCouponForKiosk(self, customer):
        '''
        Get the exchanged coupons for the member.
        @param customer(Customer):
        @return: status(str)
                 coupons(list)
                 status: 0: success
                         1: remote error
                         2: internal error
                 coupons:[{"id": id, "coupon_code": coupon_code,
                           "total_usage_limit": total_usage_limit,
                           "per_cc_usage_limit": per_cc_usage_limit,
                           "effective_date": effective_date,
                           "expiration_date": expiration_date,
                           "user_limit": user_limit,
                           "desc": desc,
                           "total_used_count": xx,
                           "cc_used_count": xx,
                           "status": "0" available
                                     "1" used
                                     "2" total limitation reached
                                     "4" expired
                                     "5" not available}]
        '''
        status = 2
        coupons = []
        
        try:
            params = { }
            params['member_id'] = customer.memberID
            params['cc_ids'] = [
                customer.primaryCcId]
            tmp = self.getRemoteData('getMemberCouponForKiosk', params)
            tmpcoupons = { }
            if tmp['result'] != 'ok':
                raise RemoteError(tmp['zdata'])
            else:
                tmpcoupons = tmp['zdata']
            curdate = getCurTime('%Y-%m-%d')
            for coupon in list(tmpcoupons.values()):
                coupon['status'] = '0'
                if coupon['effective_date'] > curdate:
                    coupon['status'] = '5'
                
                if coupon['expiration_date'] < curdate:
                    coupon['status'] = '4'
                
                if coupon['cc_used_count'] >= coupon['per_cc_usage_limit']:
                    coupon['status'] = '1'
                
                if coupon['total_used_count'] >= coupon['total_usage_limit']:
                    coupon['status'] = '2'
                
                coupons.append(coupon)
            
            status = 0
        except RemoteError as ex:
            status = 1
            self.log.error('getMemberCouponForKiosk remote error(%s): %s' % (customer.email, ex))
        except Exception as ex:
            status = 2
            self.log.error('getMemberCouponForKiosk internal error(%s): %s' % (customer.email, ex))

        return (str(status), coupons)

    
    def getMemberRecommendationForKiosk(self, customer, reccount = 4):
        '''
        Get the recommendation movies for the member.
        @param customer(Customer):
               reccount(int)
        @return: status(str)
                 coupons(list)
                 status: 0: success
                         1: remote error
                         2: internal error
                 recommendation:[{"upc": xxx, "movie_title": xxx,
                                  "movie_pic": xxx,
                                  "movie_big_pic": xxx,
                                  "is_bluray": 1/0,}]
        '''
        status = 2
        recommendation = []
        
        try:
            params = { }
            params['member_id'] = customer.memberID
            params['cc_id'] = customer.primaryCcId
            tmp = self.getRemoteData('getMemberRecommendationForKiosk', params)
            rec = []
            if tmp['result'] != 'ok':
                raise RemoteError(tmp['zdata'])
            else:
                rec = tmp['zdata']
            tmp = []
            sql = "SELECT upc, title, movie_id, SUM((SELECT COUNT(id) FROM transactions AS T WHERE T.upc=rfids.upc)) AS rc FROM rfids WHERE state IN ('in', 'unload') "
            sql += 'GROUP BY upc, movie_id ORDER BY rc DESC LIMIT ?;'
            db = Db(MKC_DB_PATH)
            for rec1 in db.query(sql, 'all', (reccount,)):
                tmp.append(rec1)
            
            blurayUpcs = self._getBlurayUpcs()
            for upc, title, movie_id, trsCount in tmp:
                recommendation.append({
                    'upc': upc,
                    'movie_title': title,
                    'movie_pic': self._formPicName(movie_id),
                    'movie_big_pic': self._formBigPicName(movie_id),
                    'is_bluray': (upc in blurayUpcs) & 1 })
            
            status = 0
        except RemoteError as ex:
            status = 1
            self.log.error('getMemberRecommendationForKiosk remote error(%s): %s' % (customer.email, ex))
        except Exception as ex:
            status = 2
            self.log.error('getMemberRecommendationForKiosk internal error(%s): %s' % (customer.email, ex))

        return (str(status), recommendation)

    
    def chkMemberRating(self, memberRating, shoppingCart):
        '''
        Check member rating and set the preauth amount of the shopping cart.
        @Params: memberRating(str)
                 shoppingCart(Shopping Cart)
        @Return: None
        '''
        pass

    
    def setMonthlySubscptForMember(self, customer, subscptInfo):
        '''
        Set the property of member for monthly subscription.
        @Params: customer(Customer object)
                 subscptInfo(dict)
        @Return: None
        '''
        if subscptInfo:
            self.log.info('%s: %s' % (customer.ccid, subscptInfo))
            totalCount = int(subscptInfo.get('total_count', '0'))
            usedCount = int(subscptInfo.get('used_count', '0'))
            customer.msID = subscptInfo.get('ms_id', '')
            customer.msKeepDays = int(subscptInfo.get('keep_days', ''))
            customer.msMaxKeepDiscs = int(subscptInfo.get('keep_count', ''))
            customer.msCount = totalCount - usedCount
            customer.msDiscType = subscptInfo.get('apply_disc_types', '')
        

    
    def setMonthlySubscptCount(self, customer, disc):
        ''' Set the monthly subscription count for the disc.
        @Params: customer(Customer object)
        @Return: disc(Disc object)
        '''
        if disc.msExpiTime:
            if not (customer.msID):
                sql = 'SELECT ms_id FROM reservations WHERE rfid=? ORDER BY id DESC LIMIT 1;'
                row = self.mkcDb.query(sql, 'one', (disc.rfid,))
                if row and row[0]:
                    customer.msID = row[0]
                    customer.memberID = ''
                
            
            sql = "SELECT id, out_time, (SELECT display FROM cc WHERE id=trs.cc_id) FROM transactions AS trs WHERE rfid=? AND state='open' ORDER BY id DESC LIMIT 1;"
            row = self.mkcDb.query(sql, 'one', (disc.rfid,))
            if not row:
                self.log.error('No opening trs(%s) for setMonthlySubscptCount' % disc.rfid)
                return None
            
            (trsId, trsTime, ccDisplay) = row
            self._setMonthlySubscptCount(customer.msID, trsId, trsTime, customer.ccid, ccDisplay, customer.memberID)
        

    
    def checkEmailForCerePay(self, customer):
        ''' Check the email for CerePay.
        @param customer(Customer object)
        @return: status(int): 0 the email can be used
                              1 internal error
                              2 network error
                              3 upg account do not support CerePay, 
                                or CerePay account is frozen.
                              4 CerePay config of upg account do not match
                              5 email can not be used, CerePay uses it
                              6 email can not be used, UMS uses it
                              7 invalid email
        '''
        status = 1
        
        try:
            proxy = UPGProxy.getInstance()
            cpCfg = proxy.getCerePayCfg()
            if cpCfg:
                result = proxy.checkCerePayEmail(cpCfg['MERCHANTID'], cpCfg['PASSWORD'], cpCfg['CURRENCY'], customer.email)
                errCode = str(result['errCode'])
                self.log.info('checkCerePayEmail: %s' % result)
                if errCode == '0':
                    result = self._getMemberCerePayInfoForKiosk(customer.email)
                    if result['status'] == 3:
                        raise RemoteError('error in service %s' % result)
                    elif result['status'] in (0, 2):
                        status = 0
                    else:
                        status = 6
                elif errCode == '1007':
                    status = 3
                elif errCode in ('1001', '1002'):
                    status = 4
                elif errCode == '1008':
                    status = 5
                elif errCode == '1012':
                    status = 7
                else:
                    raise RemoteError('error in checkCerePayEmail: %s' % result)
            else:
                status = 3
            del proxy
        except RemoteError as ex:
            status = 2
            self.log.error('checkEmailForCerePay: %s' % ex)
        except Exception as ex:
            status = 1
            self.log.error('checkEmailForCerePay: %s' % ex)

        return status

    
    def getCardInfoForCerePay(self, customer):
        '''
        Get the card information for CerePay card.
        @param customer(Customer object): customer with one card number
        @return: status(int), cardInfo(dict)
                 status: 0 new card
                         1 internal error
                         2 network error
                         3 upg account do not support CerePay, or CerePay 
                           account is frozen.
                         4 CerePay config of upg account do not match
                         5 not CerePay card
                         6 missing card
                         7 used card 
        '''
        self.log.info('getCardInfoForCerePay begin')
        status = 1
        cardInfo = { }
        
        try:
            proxy = UPGProxy.getInstance()
            if not (customer.ccid):
                s = proxy.getCCInfoByCustomer(customer)
                if s == 1:
                    raise Exception('Internal error in getCardInfoForCerePay when getCCInfoByCustomer.')
                elif s == 2:
                    raise RemoteError('Remote error in getCardInfoForCerePay when getCCInfoByCustomer.')
                
            
            if customer.cardType == 3:
                cpCfg = proxy.getCerePayCfg()
                if cpCfg:
                    cpInfo = proxy.getCerePayUserInfo(cpCfg['MERCHANTID'], cpCfg['PASSWORD'], cpCfg['CURRENCY'], number = customer.ccNum)
                    errCode = str(cpInfo['errCode'])
                    if errCode == '1004':
                        status = 0
                    elif errCode == '1007':
                        status = 3
                    elif errCode in ('1001', '1002'):
                        status = 4
                    elif errCode == '1015':
                        status = 6
                    elif errCode == '1005':
                        status = 5
                    elif errCode == '0':
                        status = 7
                        cardInfo = cpInfo
                    else:
                        raise RemoteError('Error from CerePay %s' % cpInfo)
                else:
                    status = 3
            else:
                status = 5
            del proxy
        except RemoteError as ex:
            status = 2
            self.log.error('getCardInfoForCerePay: %s' % ex)
        except Exception as ex:
            status = 1
            self.log.error('getCardInfoForCerePay: %s' % ex)

        return (status, cardInfo)

    
    def registerCerePayCard(self, customer, passwd):
        '''
        Register a CerePay card and bound the CerePay card on a register
        MemberShip account.
        @param customer(Customer object)
        @param passwd(str)
        @return: status(int)
                 status: 0 register successfully
                         1 internal error
                         2 network error
                         3 upg account do not support CerePay, or CerePay 
                           account is frozen.
                         4 CerePay config of upg account do not match
                         5 not CerePay card
                         6 missing card
                         7 account exist
                         8 invalid email address
                         9 invalid password
        '''
        status = 1
        
        try:
            self.log.info('registerCerePayCard for %s %s' % (customer.email, customer.ccid))
            proxy = UPGProxy.getInstance()
            if not (customer.ccid):
                s = proxy.getCCInfoByCustomer(customer)
                if s == 1:
                    raise Exception('Internal error in getCardInfoForCerePay when getCCInfoByCustomer.')
                elif s == 2:
                    raise RemoteError('Remote error in getCardInfoForCerePay when getCCInfoByCustomer.')
                
            
            if customer.cardType == 3:
                cpCfg = proxy.getCerePayCfg()
                if cpCfg:
                    cpInfo = proxy.registerCerePay(cpCfg['MERCHANTID'], cpCfg['PASSWORD'], cpCfg['CURRENCY'], cpEmail = customer.email, cpNumber = customer.ccNum, cpPasswd = passwd)
                    errCode = str(cpInfo['errCode'])
                    if errCode == '0':
                        p = { }
                        p['email'] = customer.email
                        p['cc_id'] = customer.ccid
                        p['cc_number'] = customer.ccNum
                        p['passwd'] = passwd
                        p['cerepay_member_id'] = cpInfo['id']
                        p['cerepay_email'] = customer.email
                        p['cerepay_merchant_id'] = cpCfg['MERCHANTID']
                        p['cerepay_validation_code'] = cpCfg['PASSWORD']
                        p['cerepay_currency'] = cpCfg['CURRENCY']
                        res = self.getRemoteData('registerMemberForKiosk', p)
                        if str(res['zdata']) == '1':
                            status = 0
                        else:
                            status = 2
                    elif errCode == '1007':
                        status = 3
                    elif errCode in ('1001', '1002'):
                        status = 4
                    elif errCode == '1015':
                        status = 6
                    elif errCode == '1005':
                        status = 5
                    elif errCode == '1008':
                        status = 7
                    elif errCode == '1012':
                        status = 8
                    elif errCode == '1013':
                        status = 9
                    else:
                        raise RemoteError('Error from CerePay %s' % cpInfo)
                else:
                    status = 3
            else:
                status = 5
            del proxy
        except RemoteError as ex:
            status = 2
            self.log.error('registerCerePayCard: %s' % ex)
        except Exception as ex:
            self.log.error('registerCerePayCard: %s' % ex)
            status = 1

        return status

    
    def _setMonthlySubscptCount(self, msId, trsId, trsTime, ccId, ccDisplay, memberId = None):
        ''' Set the monthly subscription count.
        @Params: msId(int): monthly subscription id
                 trsId(int): transaction id
                 trsTime(str): transaction time
                 ccId(int): credit card id
                 ccDisplay(str): credit card display
                 memberId(int): member id
        @Return: None
        '''
        sql = 'SELECT title, upc, rfid, genre, reserve_id, ms_expi_time FROM transactions WHERE id=? LIMIT 1;'
        row = self.mkcDb.query(sql, 'one', (trsId,))
        (title, upc, rfid, genre, reserve_id, ms_expi_time) = ('', '', '', '', '', '')
        if row:
            (title, upc, rfid, genre, reserve_id, ms_expi_time) = row
        
        params = { }
        params['kiosk_id'] = self.kioskId
        params['time'] = trsTime
        params['trs_id'] = trsId
        params['ms_id'] = msId
        params['cc_id'] = ccId
        params['cc_display'] = ccDisplay
        params['title'] = title
        params['upc'] = upc
        params['rfid'] = rfid
        params['genre'] = genre
        params['reserve_id'] = reserve_id
        params['expire_time'] = ms_expi_time
        if memberId:
            params['member_id'] = memberId
        
        for i in range(2):
            
            try:
                self.syncData('setMonthlySubscptForKiosk', params)
            except Exception as ex:
                if i == 1:
                    self.log.error('error in _setMonthlySubscptCount for %s: %s' % (trsId, ex))
                    raise 
                
            except:
                i == 1

        

    
    def isRatingLock(self):
        '''
        Check if kiosk is rating lock.
        @Params: None
        @Return: isLock(Boolean)
        '''
        isLock = False
        ratingLock = self._getConfigByKey('rating_lock')
        if ratingLock and ratingLock.lower() == 'yes':
            isLock = True
        
        return isLock

    
    def getAge(self, birthYear):
        age = 0
        
        try:
            year = datetime.datetime.now().year
            age = year - int(birthYear)
        except Exception as ex:
            self.log.error('Error when getAge: %s' % ex)

        return age

    
    def getAbbrTermsAndConditions(self):
        ''' Get mail from the api from service.
        @Params: ccId(int):
        @Return: mail
        '''
        tc = ''
        self._getTestMode()
        if self.UPG_SHOW_MODE:
            return tc
        
        params = { }
        params['kioskID'] = self.kioskId
        tmp = self.getRemoteData('getAbbrTermsAndConditionsByKioskID', params)
        if tmp['result'] != 'ok':
            raise RemoteError(tmp['zdata'])
        else:
            tc = tmp['zdata']
        return tc

    
    def _getMemberCerePayInfoForKiosk(self, email):
        ''' Get mail from the api from service.
        @param email(str)
        @return: {"status": xxx, "member_id": xxx, "cerepay_member_id": xxx}
                  status: 0 user not exist
                          1 user can not be used, bound CerePay
                          2 user can be used, not bound CerePay
                          3 unkown error
        '''
        result = {
            'status': 2,
            'member_id': 0,
            'cerepay_member_id': 0 }
        self._getTestMode()
        if self.UPG_SHOW_MODE:
            return result
        
        params = { }
        params['kiosk_id'] = self.kioskId
        params['email'] = email
        tmp = self.getRemoteData('getMemberCerePayInfoForKiosk', params)
        if tmp['result'] != 'ok':
            raise RemoteError(tmp['zdata'])
        else:
            result = tmp['zdata']
        self.log.info('_getMemberCerePayInfoForKiosk: %s' % tmp)
        return result

    
    def _setCustomerCerePayInfo(self, customer, cerepay):
        ''' Set the CerePay information for the customer.
        @param customer(Customer Object)
        @param cerepay(dict)
        @return: None
        '''
        if cerepay:
            customer.cerepayCard.id = cerepay.get('id', 0)
            customer.cerepayCard.email = cerepay.get('email', '')
            customer.cerepayCard.passwd = cerepay.get('passwd', '')
            customer.cerepayCard.number = cerepay.get('number', '')
            customer.cerepayCard.numberList = cerepay.get('numberList', [])
            customer.cerepayCard.name = cerepay.get('name', '')
            customer.cerepayCard.status = cerepay.get('status', '')
            customer.cerepayCard.balance = cerepay.get('balance', 0)
            customer.cerepayCard.holdingAmt = cerepay.get('holdingAmt', 0)
            customer.cerepayCard.needTrsPasswd = cerepay.get('needTrsPasswd', False)
            customer.cerepayCard.trsPasswd = cerepay.get('trsPasswd', '')
        



def testRegisterToUms():
    mailAddr = 'tim.guo@cereson.com'
    ccId = 2
    scId = 32
    umsProxy = UmsProxy.getInstance()
    print(umsProxy.registerToUms(mailAddr, ccId, scId))
    del umsProxy


def testSetMemberDetail():
    import sys
    sys.path.append(MKC_PATH)
    import mobject
    ccId = 1
    umsProxy = UmsProxy.getInstance()
    customer = mobject.Customer()
    customer.ccName = 'LU/PIN*LU'
    customer.ccNum = '4988820004558168'
    customer.ccExpDate = '0908'
    customer.track1 = 'B4988820004558168^LU/PIN*LU ^0908101100000000085000000'
    customer.track2 = ''
    shoppingCart = mobject.ShoppingCart()
    print(umsProxy.setMemberDetail(customer, shoppingCart))
    print(customer.__dict__)
    del umsProxy


def test():
    testSetMemberDetail()

if __name__ == '__main__':
    test()

