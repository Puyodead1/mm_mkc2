# Source Generated with Decompyle++
# File: mobject.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename:mobject.py
Contains all busniess logic classes

-- ShoppingCart
-- Disc
-- Coupon

Change Log:
    Vincent 2009-04-08 Add outTime for Disc
                       Add InvalidDiscException
    Vincent 2009-02-12 Line 264 For #1569

'''
from copy import deepcopy
import uuid
from proxy.upg_proxy import UPGProxy

class ShoppingCart(object):
    
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.discs = set()
        self.coupon = Coupon()
        self.totalCharged = ''
        self._ejectedDiscs = set()
        self._unejectedDiscs = set()
        self.couponUsed = 0

    
    def __str__(self):
        dict = deepcopy(self.__dict__)
        lstDiscs = []
        for disc in self.discs:
            lstDiscs.append(eval(str(disc)))
        
        dict['discs'] = lstDiscs
        dict['coupon'] = str(self.coupon)
        return str(dict)

    
    def getSize(self):
        return len(self.discs)

    
    def getDisc(self, rfid):
        for disc in self.discs:
            if disc.rfid == rfid:
                return disc
            
        

    
    def addDisc(self, disc):
        self.discs.add(disc)

    
    def removeDiscByRfid(self, rfid):
        for disc in self.discs:
            if disc.rfid == rfid:
                self.discs.remove(disc)
                break
            
        

    
    def removeDisc(self, disc):
        if disc in self.discs:
            self.discs.remove(disc)
        

    
    def removeDiscCoupon(self, rfid):
        for disc in self.discs:
            if disc.rfid == rfid:
                disc.coupon = Coupon()
                break
            
        

    
    def clear(self):
        self.discs = set()
        self.coupon = Coupon()
        self.totalCharged = ''
        self._ejectedDiscs = set()
        self.id = uuid.uuid4()

    
    def ejectDisc(self, rfid):
        for disc in self.discs:
            if disc.rfid == rfid:
                self._ejectedDiscs.add(disc)
            
        

    
    def getEjectedDiscs(self):
        return self._ejectedDiscs

    
    def getEjectedDiscsSize(self):
        return len(self._ejectedDiscs)

    
    def getUnejectedDiscs(self):
        return self.discs - self._ejectedDiscs

    
    def getUnEjectedDiscsSize(self):
        return len(self.discs - self._ejectedDiscs)



class Disc(object):
    
    def __init__(self, rfid = '', upc = ''):
        self.rfid = rfid
        self.upc = upc
        self.slotID = ''
        self.title = ''
        self.picture = ''
        self.genre = ''
        self.rentalPrice = ''
        self.salePrice = ''
        self.preauthAmount = ''
        self.reserveID = ''
        self.coupon = Coupon()
        self.gene = ''
        self.outKioskID = ''
        self.upgID = 0
        self.rating = ''
        self.releaseDate = ''
        self.pricePlan = ''
        self.pricePlanContent = ''
        self.dynamicPricePlan = 0
        self.rentalTax = ''
        self.saleTax = ''
        self.pricePlanID = 0
        self.cost = ''
        self.starring = ''
        self.directors = ''
        self.synopsis = ''
        self.trailerName = ''
        self.version = ''
        self.availableCount = 0
        self.expressID = ''
        self.movieID = ''
        self.saleConvertPrice = ''
        self.inTime = ''
        self.outTime = ''
        self.couponUsed = 0
        self.trsID = ''
        self.isBluray = 0
        self.discType = ''
        self.isGracePeriod = 0
        self.entrance = ''
        self.msExpiTime = ''
        self.msKeepDays = ''
        self.outAddress = ''
        self.memberPreauthAmount = ''

    
    def __str__(self):
        dict = deepcopy(self.__dict__)
        dict['coupon'] = str(self.coupon)
        return str(dict)



class Coupon(object):
    
    def __init__(self, couponCode = '', couponData = '', description = ''):
        self.couponCode = couponCode
        self.couponData = couponData
        self.description = description
        self.shortDes = ''
        self.couponType = ''

    
    def __str__(self):
        return str(self.__dict__)



class Cerepay(object):
    
    def __init__(self):
        self.id = 0
        self.email = ''
        self.passwd = ''
        self.number = ''
        self.numberList = []
        self.name = ''
        self.status = ''
        self.balance = 0
        self.holdingAmt = 0
        self.needTrsPasswd = False
        self.trsPasswd = ''



class Customer(object):
    
    def __init__(self, ccName = '', ccNumber = '', ccExpDate = '', track2 = '', track1 = ''):
        self.ccid = 0
        self.ccName = ccName
        self.ccNum = ccNumber
        self.ccExpDate = ccExpDate
        self.track2 = track2
        self.track1 = track1
        self.ccDisplay = ''
        self.age = 0
        self.email = ''
        self.level = ''
        self.memberID = ''
        self.msKeepDays = 3
        self.msCount = 0
        self.msMaxKeepDiscs = 3
        self.msDiscType = ''
        self.msID = ''
        self.isNew = 0
        self.isLogin = False
        self.isMember = False
        self.firstName = ''
        self.lastName = ''
        self.primaryCcId = ''
        self.primaryCcNumber = ''
        self.allCcIds = []
        self.gender = ''
        self.cardType = 0
        self.ccNumSHA1 = ''
        self.oid = ''
        self.cerepayCard = Cerepay()
        proxy = UPGProxy.getInstance()
        proxy.getCCInfoByCustomer(self)
        del proxy



class MessageBox(object):
    
    def __init__(self, message = '', closeForm = '', width = 0, height = 0):
        self.message = message
        self.closeForm = closeForm
        self.width = 200
        self.height = 100
        if width:
            self.width = width
        
        if height:
            self.height = height
        


'\nSingleton Implementation, borrow from Python Cook\n'

class Singleton(object):
    
    def __new__(cls, *args, **kwargs):
        if '_inst' not in vars(cls):
            cls._inst = object.__new__(cls, *args, **kwargs)
        
        return cls._inst



class GlobalSession(Singleton):
    
    def __init__(self):
        self.shoppingCart = ShoppingCart()
        self.pickupCart = ShoppingCart()
        self.error = FatalError('', { }, '')
        self.param = { }
        self.resultMsg = ''
        self.disc = Disc()
        self.customer = Customer()
        self.loginCustomer = Customer()
        self.messageBox = MessageBox()
        self.currencySymbol = ''
        self.loginTime = ''
        self.loginType = ''
        self.notifyEmail = ''
        self.firstKey = 'genre'
        self.firstGenreID = 'NEW RELEASE'
        self.cerepayTopupAmount = -1
        self.isUsingChipnPin = False
        self.isCerepayCardInfoDirty = False
        self.cerepayTopupTransactionUUID = ''

    
    def clear(self):
        self.shoppingCart.clear()
        self.pickupCart.clear()
        self.error = FatalError('', { }, '')
        self.param = { }
        self.resultMsg = ''
        self.disc = Disc()
        self.customer = Customer()
        self.loginCustomer = Customer()
        self.messageBox = MessageBox()
        self.currencySymbol = ''
        self.loginTime = ''
        self.loginType = ''
        self.notifyEmail = ''
        self.firstKey = 'genre'
        self.firstGenreID = 'NEW RELEASE'
        self.cerepayTopupAmount = -1
        self.isUsingChipnPin = False
        self.isCerepayCardInfoDirty = False
        self.cerepayTopupTransactionUUID = ''



class KioskMessage:
    '''
    This class is used to handle i18n message show in gui, log or emailAlert
    '''
    
    def __init__(self, message, param = { }):
        self.rawmsg = message
        self.param = param

    
    def __getattr__(self, name):
        msg = ''
        if name == 'i18nmsg':
            msg = _(self.rawmsg) % self.param
        elif name == 'message':
            msg = self.rawmsg % self.param
        else:
            raise AttributeError(name)
        return msg

    
    def __str__(self):
        return self.message



class BaseError(Exception):
    
    def __init__(self, message, param = { }, errCode = ''):
        Exception.__init__(self)
        self.rawmsg = message
        self.param = param
        self.errCode = errCode
        self.message = self._getRaw()

    
    def _getRaw(self):
        msg = ''
        if self.errCode:
            msg = '(%s) ' % self.errCode
        
        return msg + self.rawmsg % self.param

    
    def __getattr__(self, name):
        msg = ''
        if name == 'i18nmsg':
            if self.errCode:
                msg = '(%s) ' % self.errCode
            
            msg = msg + _(self.rawmsg) % self.param
        else:
            raise AttributeError(name)
        return msg

    
    def __str__(self):
        return self.message



class RetreiveNoDiscError(BaseError):
    pass


class RetreiveFailError(BaseError):
    pass


class WrongOutRfidError(BaseError):
    pass


class InvalidDiscRfidError(BaseError):
    pass


class WrongInRfidError(BaseError):
    pass


class FatalError(BaseError):
    
    def __init__(self, message, param, errCode, recover = True):
        BaseError.__init__(self, message, param, errCode)
        self.recover = recover



class RetrieveExchangeException(BaseError):
    pass


class InsertException(BaseError):
    pass


class CardDeclinedException(BaseError):
    pass


class CardReadException(BaseError):
    pass


class InvalidDiscException(BaseError):
    pass


class InvalidCouponException(BaseError):
    pass


class ValidateCouponException(BaseError):
    pass


class InvalidMemberException(BaseError):
    pass


class SaveStatusError(BaseError):
    pass


class DebitCardTimeOut(BaseError):
    pass


class MemberException(BaseError):
    pass


class ChinPinTopupException(BaseError):
    pass

