# Source Generated with Decompyle++
# File: guiAdminMainForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiAdminMainForm.py
Admin Main Form
Screen ID: A1

Change Log:
    2009-04-30 Vincent Add fully loaded check
                       Add unload mark list

'''
from mcommon import *
from guiBaseForms import UserForm
log = initlog('guiAdminMainForm')

class AdminMainForm(UserForm):
    
    def __init__(self):
        UserForm.__init__(self)
        self.screenID = 'A1'
        self.preWindowID = 'MainForm'
        self.uiErrorWindowID = 'MainForm'
        self.timeoutSec = 60
        self.lstResponseCtrl = [
            'btn_logout',
            'btn_load_new_release',
            'btn_load_upc',
            'btn_load_title',
            'btn_unload_slot',
            'btn_unload_title',
            'btn_information',
            'btn_report',
            'btn_config',
            'AdminMainForm_ctr_message_box',
            'btn_unload_mark',
            'btn_manually_return',
            'btn_manage_slots']

    
    def _initComponents(self):
        UserForm._initComponents(self)
        globalSession.shoppingCart.clear()
        self.state = ''
        if globalSession.param.get('priv') == 'load' or globalSession.param.get('load_one_slot'):
            self.lstResponseCtrl = [
                'btn_logout',
                'btn_load_new_release',
                'btn_load_upc',
                'btn_load_title',
                'btn_manually_return',
                'btn_manage_slots']
            self.flash.send('btn_load_new_release', 'show', { })
            self.flash.send('btn_load_upc', 'show', { })
            self.flash.send('btn_load_title', 'show', { })
            self.flash.send('btn_quick_load', 'hide', { })
            self.flash.send('btn_unload_mark', 'hide', { })
            self.flash.send('btn_unload_slot', 'hide', { })
            self.flash.send('btn_unload_title', 'hide', { })
            self.flash.send('btn_report', 'hide', { })
            self.flash.send('btn_information', 'hide', { })
            self.flash.send('btn_config', 'hide', { })
            if globalSession.param.get('load_one_slot'):
                self.flash.send('btn_manage_slots', 'hide', { })
            else:
                self.flash.send('btn_manage_slots', 'hide', { })
        elif globalSession.param.get('priv') == 'admin':
            self.lstResponseCtrl = [
                'btn_logout',
                'btn_load_new_release',
                'btn_load_upc',
                'btn_load_title',
                'btn_unload_slot',
                'btn_unload_title',
                'btn_information',
                'btn_report',
                'btn_config',
                'AdminMainForm_ctr_message_box',
                'btn_unload_mark',
                'btn_manually_return',
                'btn_manage_slots']
            self.flash.send('btn_load_new_release', 'show', { })
            self.flash.send('btn_load_upc', 'show', { })
            self.flash.send('btn_load_title', 'show', { })
            self.flash.send('btn_quick_load', 'hide', { })
            self.flash.send('btn_unload_mark', 'show', { })
            self.flash.send('btn_unload_slot', 'show', { })
            self.flash.send('btn_unload_title', 'show', { })
            self.flash.send('btn_report', 'show', { })
            self.flash.send('btn_information', 'show', { })
            self.flash.send('btn_config', 'show', { })
            self.flash.send('btn_manage_slots', 'hide', { })
        elif globalSession.param.get('priv') == 'unload':
            self.lstResponseCtrl = [
                'btn_logout',
                'btn_unload_slot',
                'btn_unload_title',
                'btn_unload_mark',
                'btn_manually_return',
                'btn_manage_slots']
            self.flash.send('btn_unload_mark', 'show', { })
            self.flash.send('btn_unload_slot', 'show', { })
            self.flash.send('btn_unload_title', 'show', { })
            self.flash.send('btn_quick_load', 'hide', { })
            self.flash.send('btn_load_new_release', 'hide', { })
            self.flash.send('btn_load_upc', 'hide', { })
            self.flash.send('btn_load_title', 'hide', { })
            self.flash.send('btn_report', 'hide', { })
            self.flash.send('btn_information', 'hide', { })
            self.flash.send('btn_config', 'hide', { })
            self.flash.send('btn_manage_slots', 'hide', { })
        else:
            raise Exception('AdminMainForm load, unload or admin?')

    
    def on_btn_logout_event(self):
        if globalSession.param.get('load_one_slot'):
            globalSession.param['load_one_slot'] = ''
        
        self.on_exit()

    
    def on_btn_unload_mark_event(self):
        self.nextWindowID = 'UnloadMarkedForm'
        self.windowJump = True

    
    def _needOverCapacityAlert(self):
        a1 = self.connProxy._getConfigByKey('over_capacity_alert_threshold')
        a2 = len(self.connProxy.getAvailableSlotIdList())
        if int(a1) >= a2:
            return True
        else:
            return False

    
    def on_btn_load_new_release_event(self):
        if self.connProxy.getAvailableSlotIdList():
            globalSession.param['load_search_key'] = 'genre'
            globalSession.param['load_search_val'] = 'NEW RELEASE'
            self.nextWindowID = 'LoadDiscListForm'
            if self._needOverCapacityAlert():
                msg = _('Current empty slots are less than Empty Slots Alert Threshold, are you sure you want to continue?')
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': msg,
                    'type': 'confirm' })
                self.state = 'threshold'
            else:
                self.windowJump = True
        else:
            msg = _('No more empty slots on this kiosk.')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'alert' })
            self.state = 'empty'

    
    def on_btn_load_upc_event(self):
        if self.connProxy.getAvailableSlotIdList():
            self.nextWindowID = 'LoadUpcEnterForm'
            if self._needOverCapacityAlert():
                msg = _('Current empty slots are less than Empty Slots Alert Threshold, are you sure you want to continue?')
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': msg,
                    'type': 'confirm' })
                self.state = 'threshold'
            else:
                self.windowJump = True
        else:
            msg = _('No more empty slots on this kiosk.')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'alert' })
            self.state = 'empty'

    
    def on_btn_load_title_event(self):
        if self.connProxy.getAvailableSlotIdList():
            self.nextWindowID = 'LoadTitleEnterForm'
            if self._needOverCapacityAlert():
                msg = _('Current empty slots are less than Empty Slots Alert Threshold, are you sure you want to continue?')
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': msg,
                    'type': 'confirm' })
                self.state = 'threshold'
            else:
                self.windowJump = True
        else:
            msg = _('No more empty slots on this kiosk.')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'alert' })
            self.state = 'empty'

    
    def on_btn_unload_slot_event(self):
        self.nextWindowID = 'UnloadBySlotForm'
        self.windowJump = True

    
    def on_btn_unload_title_event(self):
        self.nextWindowID = 'UnloadByTitleForm'
        self.windowJump = True

    
    def on_btn_information_event(self):
        self.nextWindowID = 'KioskInfoForm'
        self.windowJump = True

    
    def on_btn_report_event(self):
        self.nextWindowID = 'ReportForm'
        self.windowJump = True

    
    def on_btn_manually_return_event(self):
        self.nextWindowID = 'ReturnManuallyTakeInForm'
        self.windowJump = True

    
    def on_btn_manage_slots_event(self):
        self.nextWindowID = 'ShowAllSlotForm'
        self.windowJump = True

    
    def on_btn_config_event(self):
        self.nextWindowID = 'ConfigTestModeForm'
        self.windowJump = True

    
    def on_AdminMainForm_ctr_message_box_event(self):
        if self.state == 'threshold':
            if self._getEventParam('AdminMainForm_ctr_message_box', 'val') == 'yes':
                self.windowJump = True
            
        


