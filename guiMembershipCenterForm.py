# Source Generated with Decompyle++
# File: guiMembershipCenterForm.pyc (Python 2.5)

'''
Created on 2010-7-9
@author: andrew.lu@cereson.com
'''
from mcommon import *
from guiBaseForms import CustomerForm
from proxy.upg_proxy import UPGProxy
log = initlog('MembershipCenterForm')

class MembershipCenterForm(CustomerForm):
    
    def __init__(self):
        super(MembershipCenterForm, self).__init__()
        self.screenID = 'M3'
        self.preWindowID = 'MainForm'
        self.uiErrorWindowID = 'MainForm'
        self.timeoutSec = 180
        self.lstResponseCtrl.extend([
            'btn_transactions',
            'btn_coupons',
            'btn_profile',
            'btn_browse',
            'btn_reserved',
            'btn_cerepay',
            'ctr_movie_list'])

    
    def _initComponents(self):
        super(MembershipCenterForm, self)._initComponents()
        if globalSession.loginCustomer.ccNum:
            num = globalSession.loginCustomer.ccNum
        else:
            num = globalSession.loginCustomer.primaryCcNumber
        self.flash.send('card_number', 'setText', {
            'text': maskCard(num) })
        if globalSession.loginCustomer.cerepayCard.id == 0:
            self.flash.send('btn_cerepay', 'hide', { })
        else:
            self.flash.send('btn_cerepay', 'show', { })
        (status, discs) = self.umsProxy.getMemberRecommendationForKiosk(globalSession.loginCustomer)
        if status != '0':
            log.error('getMemberRecommendationForKiosk failed %s' % status)
            return None
        
        allDiscs = []
        for disc in discs:
            data = { }
            data['movie_pic'] = getPicFullPath(disc['movie_pic'])
            data['upc'] = disc['upc']
            data['rfid'] = ''
            data['movie_title'] = disc['movie_title']
            allDiscs.append(data)
        
        self.flash.send('ctr_movie_list', 'setRecommendationList', {
            'ctr_movie_list': allDiscs })

    
    def on_btn_transactions_event(self):
        self.nextWindowID = 'MembershipTransactionForm'
        self.windowJump = True

    
    def on_btn_coupons_event(self):
        self.nextWindowID = 'MembershipCouponForm'
        self.windowJump = True

    
    def on_btn_profile_event(self):
        self.nextWindowID = 'MembershipProfileForm'
        self.windowJump = True

    
    def on_btn_browse_event(self):
        self.nextWindowID = 'RentMainForm'
        self.windowJump = True

    
    def on_btn_reserved_event(self):
        globalSession.pickupCart.clear()
        ccid = self.connProxy.getPickUpListForMember(globalSession.pickupCart, globalSession.loginCustomer.allCcIds)
        globalSession.customer.ccid = ccid
        self.upgProxy = UPGProxy()
        self.upgProxy.getCCInfoFromCacheByCustomer(globalSession.customer)
        self.nextWindowID = 'PickUpDiscListForm'
        self.windowJump = True

    
    def on_btn_cerepay_event(self):
        self.nextWindowID = 'CerepayCenterForm'
        self.windowJump = True

    
    def on_ctr_movie_list_event(self):
        upc = self._getEventParam('ctr_movie_list', 'upc')
        rfid = self._getEventParam('ctr_movie_list', 'rfid')
        if upc:
            disc = Disc()
            disc.upc = upc
            disc.rfid = rfid
            disc.entrance = ''
            globalSession.disc = disc
            self.connProxy.loadDiscInfo(globalSession.disc, rfid)
            self.nextWindowID = 'DiscDetailForm'
            self.windowJump = True
        


