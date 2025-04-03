# Source Generated with Decompyle++
# File: guiDiscPriceForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiDiscDetailForm.py
Disc detail screen with rental / sale price, tax; and Terms and Conditions
Screen ID: R4

Change Log:
    Tim     2011-04-07 Check 
    Vincent 2009-03-18 Add Blu ray icon
    Vincent 2009-03-03 Purchase confirm
    Vincent 2009-02-24 For Disc price form message box not closed.
'''
import os
import traceback
from mcommon import *
from guiBaseForms import CustomerForm
log = initlog('guiDiscPriceForm')

class DiscPriceForm(CustomerForm):
    
    def __init__(self):
        super(DiscPriceForm, self).__init__()
        self.preWindowID = 'DiscDetailForm'
        self.screenID = 'R4'
        self.timeoutSec = 180
        self.lstResponseCtrl.extend([
            'btn_back',
            'btn_cancel',
            'btn_rent',
            'btn_buy',
            'DiscPriceForm_ctr_message_box',
            'btn_rent_disabled'])

    
    def _initComponents(self):
        super(DiscPriceForm, self)._initComponents()
        self.disc = globalSession.disc
        tnc = self.connProxy._getConfigByKey('terms_and_conditions')
        self.canRent = self.connProxy._getConfigByKey('enable_disc_out')
        if self.canRent == 'yes':
            self.flash.send('btn_rent', 'show', { })
        else:
            self.flash.send('btn_rent', 'hide', { })
        discPriceInfo = { }
        discPriceInfo['terms'] = tnc
        discPriceInfo['movie_title'] = self.disc.title
        if MKC_THEME == 'game':
            discPriceInfo['dvd_version'] = ''
        else:
            discPriceInfo['dvd_version'] = self.disc.version
        discPriceInfo['movie_pic'] = getPicFullPath(self.disc.picture)
        feature = []
        feature.append({
            _('Rental Price'): self.disc.pricePlan })
        if '%.2f' % round(float(self.disc.rentalTax.strip('%')), 2) != '0.00':
            feature.append({
                _('Rental Tax'): self.disc.rentalTax })
        
        if '%.2f' % round(float(self.disc.salePrice), 2) == '0.00':
            self.flash.send('btn_buy', 'hide', { })
        else:
            feature.append({
                _('Sales Price'): self.disc.salePrice })
            self.flash.send('btn_buy', 'show', { })
            if '%.2f' % round(float(self.disc.saleTax.strip('%')), 2) != '0.00':
                feature.append({
                    _('Sales Tax'): self.disc.saleTax })
            
        release = self.movieProxy.allowRental(self.disc)
        if release == '2':
            self.flash.send('btn_buy', 'hide', { })
        
        showDepositAmount = self.connProxy._getConfigByKey('show_deposit_amount')
        if str(showDepositAmount) == 'yes':
            deposit_amount = { }
            currencySymbol = self.connProxy.getDefaultCurrencySymbol()
            if self.disc.preauthAmount == self.disc.memberPreauthAmount:
                deposit_amount[_('Deposit Amount')] = '%s%s' % (currencySymbol, self.disc.preauthAmount)
            else:
                deposit_amount[_('Deposit Amount')] = '%s%s (Member Amount: %s%s)' % (currencySymbol, self.disc.preauthAmount, currencySymbol, self.disc.memberPreauthAmount)
            feature.append(deposit_amount)
        
        discPriceInfo['feature'] = feature
        if self.disc.isBluray:
            discPriceInfo['is_bluray'] = '1'
        elif self.disc.discType == 'WII':
            discPriceInfo['is_bluray'] = '2'
        elif self.disc.discType == 'XBOX360':
            discPriceInfo['is_bluray'] = '3'
        elif self.disc.discType == 'PS3':
            discPriceInfo['is_bluray'] = '4'
        else:
            discPriceInfo['is_bluray'] = '0'
        self.flash.send('ctr_movie_price', 'setMoviePrice', {
            'ctr_movie_price': discPriceInfo })
        self.flash.wid = self.windowID
        self.confirmBox = ''

    
    def _addDisc(self):
        status = str(self.connProxy.addDiscToShoppingCart(globalSession.shoppingCart, self.disc))
        log.info('[ConnProxy addDiscToShoppingCart result]: %s' % status)
        if status == '0':
            globalSession.shoppingCart.addDisc(self.disc)
            self.nextWindowID = 'ShoppingCartForm'
            self.windowJump = True
        elif status == '1':
            msg = _('Disc unavailable. ')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'alert' })
        elif status == '2':
            msg = _('Shopping cart full. ')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'alert' })
        

    
    def on_hide(self):
        super(DiscPriceForm, self).on_hide()
        self.flash.wid = self.windowID
        self.flash.send('%s_ctr_message_box' % self.windowID, 'close', { })

    
    def on_btn_back_event(self):
        self.on_back()

    
    def on_btn_cancel_event(self):
        self.on_cancel()

    
    def on_DiscPriceForm_ctr_message_box_event(self):
        if self.confirmBox == 'purchase_confirm':
            if self._getEventParam('DiscPriceForm_ctr_message_box', 'val') == 'yes':
                self._addDisc()
            
        
        self.confirmBox = ''

    
    def on_btn_buy_event(self):
        self.disc.gene = 'sale'
        slot_id = self.connProxy.getSlotIdByRfid(self.disc.rfid)
        self.disc.expressID = slot_id
        globalSession.disc.expressID = slot_id
        msg = ''
        if self.connProxy._getConfigByKey('payment_options') == 'chipnpin':
            msg = _('Do you agree with the Terms & Conditions and want to buy the disc?')
        else:
            msg = _('Are you sure you want to buy this disc?')
        if self.connProxy._getConfigByKey('bluray_warning') == 'yes' and self.disc.isBluray:
            msg = msg + _('You have selected a Blu-ray disc which will NOT play on a standard DVD player. Please click cancel to select another disk or click OK to proceed.')
        
        self.confirmBox = 'purchase_confirm'
        self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
            'message': msg,
            'type': 'confirm' })

    
    def on_btn_rent_event(self):
        self.disc.gene = 'rent'
        msg = ''
        if self.connProxy._getConfigByKey('payment_options') == 'chipnpin':
            msg = _('Do you agree with the Terms & Conditions?')
        
        if self.connProxy._getConfigByKey('bluray_warning') == 'yes' and self.disc.isBluray:
            tm = _('You have selected a Blu-ray disc which will NOT play on a standard DVD player. Please click cancel to select another disk or click OK to proceed.')
            if msg:
                msg = msg + '\n' + tm
            else:
                msg = tm
        
        if msg:
            self.confirmBox = 'purchase_confirm'
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'confirm' })
        else:
            self._addDisc()

    
    def on_btn_rent_disabled_event(self):
        if self.canRent == 'yes':
            pass
        else:
            msg = _('Disc Out has been disabled.')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'alert' })


