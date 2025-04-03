# Source Generated with Decompyle++
# File: guiLoadUpcEnterForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiLoadUpcEnterForm.py
Contains only one num keyboard
Screen ID: L12

Change Log:

'''
import os
import traceback
import config
from mcommon import *
from guiBaseForms import UserForm
log = initlog('guiLoadUpcEnterForm')

class LoadUpcEnterForm(UserForm):
    
    def __init__(self):
        UserForm.__init__(self)
        self.screenID = 'L12'
        self.timeoutSec = 60
        self.preWindowID = 'AdminMainForm'
        self.uiErrorWindowID = 'AdminMainForm'
        self.lstResponseCtrl = [
            'btn_logout',
            'btn_back',
            'btn_cancel',
            'LoadUpcEnterForm_ctr_num_keyboard']

    
    def _initComponents(self):
        UserForm._initComponents(self)
        self.flash.send('%s_ctr_num_keyboard' % self.windowID, 'show', { })
        globalSession.param['load_entry_form'] = self.windowID

    
    def on_hide(self):
        UserForm.on_hide(self)
        self.flash.send('%s_ctr_num_keyboard' % self.windowID, 'close', { })

    
    def on_btn_logout_event(self):
        self.on_exit()

    
    def on_btn_back_event(self):
        self.on_back()

    
    def on_btn_cancel_event(self):
        self.on_cancel()

    
    def on_LoadUpcEnterForm_ctr_num_keyboard_event(self):
        eventType = self._getEventParam('LoadUpcEnterForm_ctr_num_keyboard', 'type')
        if eventType == 'click':
            keyword = self._getEventParam('LoadUpcEnterForm_ctr_num_keyboard', 'val')
            if keyword == 'close':
                self.nextWindowID = 'AdminMainForm'
                self.windowJump = True
            
        elif eventType == 'ok':
            upc = self._getEventParam('LoadUpcEnterForm_ctr_num_keyboard', 'val')
            globalSession.param['load_search_key'] = 'upc'
            globalSession.param['load_search_val'] = upc
            self.nextWindowID = 'LoadDiscListForm'
            self.windowJump = True
        


