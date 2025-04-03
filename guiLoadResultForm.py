# Source Generated with Decompyle++
# File: guiLoadResultForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiLoadResultForm.py
Load Result
Screen ID: L6

Change Log:
    2009-04-30 Vincent Add message box to prevent fully loaded load again

'''
import config
from mcommon import *
from guiBaseForms import UserForm
log = initlog('guiLoadResultForm')

class LoadResultForm(UserForm):
    
    def __init__(self):
        UserForm.__init__(self)
        self.screenID = 'L6'
        self.timeoutSec = 60
        self.preWindowID = 'AdminMainForm'
        self.uiErrorWindowID = 'AdminMainForm'
        self.lstResponseCtrl = [
            'btn_logout',
            'btn_finish',
            'btn_again',
            'btn_another',
            'LoadResultForm_ctr_message_box']

    
    def _initComponents(self):
        UserForm._initComponents(self)
        self.state = ''
        self.disc = globalSession.disc
        if globalSession.param.get('load_one_slot'):
            globalSession.param['load_one_slot'] = ''
        
        msg = _('The disc has been loaded. ')
        if globalSession.param.get('return_msg'):
            msg = globalSession.param.get('return_msg')
            globalSession.param['return_msg'] = ''
        
        self.flash.send('txtbox_msg', 'setText', {
            'text': msg })
        self.flash.wid = self.windowID

    
    def on_btn_logout_event(self):
        self.on_exit()

    
    def on_btn_finish_event(self):
        self.nextWindowID = 'AdminMainForm'
        self.windowJump = True

    
    def _needOverCapacityAlert(self):
        a1 = self.connProxy._getConfigByKey('over_capacity_alert_threshold')
        a2 = len(self.connProxy.getAvailableSlotIdList())
        if int(a1) >= a2:
            return True
        else:
            return False

    
    def on_btn_again_event(self):
        if self.connProxy.getAvailableSlotIdList():
            self.nextWindowID = 'LoadDiscInfoForm'
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

    
    def on_btn_another_event(self):
        if self.connProxy.getAvailableSlotIdList():
            searchKey = globalSession.param.get('load_search_key')
            if searchKey == 'genre':
                self.nextWindowID = 'LoadDiscListForm'
            elif searchKey == 'keyword':
                self.nextWindowID = 'LoadTitleEnterForm'
            elif searchKey == 'upc':
                self.nextWindowID = 'LoadUpcEnterForm'
            else:
                self.nextWindowID = 'AdminMainForm'
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

    
    def on_LoadResultForm_ctr_message_box_event(self):
        if self.state == 'threshold':
            if self._getEventParam('LoadResultForm_ctr_message_box', 'val') == 'yes':
                self.windowJump = True
            
        


