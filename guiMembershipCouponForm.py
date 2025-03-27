# Source Generated with Decompyle++
# File: guiMembershipCouponForm.pyc (Python 2.5)

'''
Created on 2010-7-9
@author: andrew.lu@cereson.com
'''
from mcommon import *
from guiBaseForms import CustomerForm
log = initlog('MembershipCouponForm')

class MembershipCouponForm(CustomerForm):
    
    def __init__(self):
        super(MembershipCouponForm, self).__init__()
        self.screenID = 'M5'
        self.preWindowID = 'MembershipCenterForm'
        self.uiErrorWindowID = 'MainForm'
        self.timeoutSec = 180
        self.lstResponseCtrl.extend([
            'btn_back'])

    
    def _initComponents(self):
        super(MembershipCouponForm, self)._initComponents()
        if globalSession.loginCustomer.ccNum:
            text = globalSession.loginCustomer.ccNum[-4:]
        else:
            i = globalSession.loginCustomer.email.index('@')
            text = globalSession.loginCustomer.email[:i]
        self.flash.send('txt_msg', 'setText', {
            'text': text })
        (status, coupons) = self.umsProxy.getMemberCouponForKiosk(globalSession.loginCustomer)
        if status != '0':
            log.error('getMemberCouponForKiosk failed %s' % status)
            return None
        
        allCoupons = []
        for coupon in coupons:
            data = { }
            data['coupon_code'] = coupon['coupon_code']
            data['description'] = coupon['desc']
            data['description']
            allCoupons.append(data)
        
        self.flash.send('ctr_coupon_list', 'setList', {
            'ctr_coupon_list': allCoupons })

    
    def on_btn_back_event(self):
        self.on_back()


