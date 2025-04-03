# Source Generated with Decompyle++
# File: guiLoadDiscInfoForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiLoadDiscInfoForm.py
Disc Load Info screen, contains all load default settings
Screen ID: A1

Change Log:
    2009-05-08 Andrew Fix bug #1683, when load a new upc
    2009-04-30 Andrew Sale convert price lable
    2009-03-06 Vincent Refresh DVD version after UPC changed

'''
import os
import traceback
import config
from mcommon import *
from guiBaseForms import UserForm
log = initlog('guiLoadDiscInfoForm')

class LoadDiscInfoForm(UserForm):
    
    def __init__(self):
        UserForm.__init__(self)
        self.screenID = 'L3'
        self.timeoutSec = 60
        self.preWindowID = 'LoadDiscListForm'
        self.uiErrorWindowID = 'AdminMainForm'
        self.lstResponseCtrl = [
            'btn_logout',
            'btn_ok',
            'btn_back',
            'btn_slot_number_edit',
            'btn_price_plan_edit',
            'btn_sale_price_edit',
            'btn_convert_price_edit',
            'btn_cost_edit',
            'btn_upc_edit',
            'btn_upc_ok']

    
    def _initComponents(self):
        UserForm._initComponents(self)
        self.disc = globalSession.disc
        settings = self.connProxy.getDefaultSettings(globalSession.disc)
        if not globalSession.param.get('load_one_slot'):
            pass
        if not globalSession.param.get('load_one_slot'):
            pass
        self.flash.send('ctr_slot_id_list', 'setList', {
            'front_slot_id': settings.get('front_slot_id'),
            'back_slot_id': settings.get('back_slot_id'),
            'check_slot_id': self.disc.slotID })
        self.flash.send('txt_price_plan', 'setText', {
            'text': self.disc.pricePlan })
        self.flash.send('txt_price_plan_id', 'setText', {
            'text': self.disc.pricePlanID })
        self.flash.send('txt_sale_price', 'setText', {
            'text': self.disc.salePrice })
        self.flash.send('txt_convert_price', 'setText', {
            'text': self.disc.saleConvertPrice })
        self.flash.send('txt_cost', 'setText', {
            'text': self.disc.cost })
        self.flash.send('txt_upc', 'setText', {
            'text': self.disc.upc })
        if str(settings.get('default_price_plan_dynamic')) == '1':
            self.flash.send('txt_special_price_plan', 'setText', {
                'text': 'yes' })
        else:
            self.flash.send('txt_special_price_plan', 'setText', {
                'text': 'no' })
        self._setDiscInfo()

    
    def _setDiscInfo(self):
        dictDisc = { }
        dictDisc['movie_title'] = self.disc.title
        dictDisc['movie_pic'] = getPicFullPath(self.disc.picture)
        dictDisc['dvd_version'] = self.disc.version
        dictDisc['genre'] = self.disc.genre
        dictDisc['dvd_release_date'] = self.disc.releaseDate
        dictDisc['starring'] = self.disc.starring
        dictDisc['directors'] = self.disc.directors
        dictDisc['rating'] = self.disc.rating
        self.flash.send('ctr_movie_info', 'setMovieDetail', {
            'ctr_movie_detail': dictDisc })

    
    def on_btn_logout_event(self):
        self.on_exit()

    
    def on_btn_ok_event(self):
        globalSession.disc.upc = self._getEventParam('btn_ok', 'upc')
        self.movieProxy.getMovieDetailByUpc(globalSession.disc)
        globalSession.disc.slotID = self._getEventParam('btn_ok', 'slot_number')
        globalSession.disc.pricePlanID = self._getEventParam('btn_ok', 'price_plan')
        globalSession.disc.salePrice = str(self._getEventParam('btn_ok', 'sale_price')).strip(globalSession.param.get('currency_symbol'))
        globalSession.disc.saleConvertPrice = str(self._getEventParam('btn_ok', 'convert_price')).strip(globalSession.param.get('currency_symbol'))
        globalSession.disc.cost = str(self._getEventParam('btn_ok', 'cost')).strip(globalSession.param.get('currency_symbol'))
        if self._getEventParam('btn_ok', 'accept_special_price_plan') == 'yes':
            globalSession.disc.dynamicPricePlan = 1
        else:
            globalSession.disc.dynamicPricePlan = 0
        self.nextWindowID = 'LoadTakeInForm'
        self.windowJump = True

    
    def on_btn_back_event(self):
        self.on_back()

    
    def on_btn_slot_number_edit_event(self):
        lstSlotID = self.connProxy.getAvailableSlotIdList()
        self.flash.send('ctr_slot_list', 'setList', {
            'slot_list': str(lstSlotID) })

    
    def on_btn_price_plan_edit_event(self):
        lstPricePlan = self.connProxy.getPricePlanList()
        self.flash.send('ctr_plan_list', 'setPlanList', {
            'ctr_plan_list': lstPricePlan })

    
    def on_btn_sale_price_edit_event(self):
        pass

    
    def on_btn_convert_price_edit_event(self):
        pass

    
    def on_btn_cost_edit_event(self):
        pass

    
    def on_btn_upc_edit_event(self):
        lstUpc = self.movieProxy.getOtherUpcList(self.disc.upc)
        self.flash.send('ctr_upc_list', 'setUPCList', {
            'ctr_upc_list': lstUpc })

    
    def on_btn_upc_ok_event(self):
        upc = self._getEventParam('btn_upc_ok', 'upc')
        log.info('Vincent %s' % upc)
        if upc:
            self.disc.upc = upc
            self.movieProxy.getMovieDetailByUpc(self.disc)
            globalSession.disc = self.disc
            self._setDiscInfo()
        


