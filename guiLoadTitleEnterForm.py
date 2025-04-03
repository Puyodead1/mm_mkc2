# Source Generated with Decompyle++
# File: guiLoadTitleEnterForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiLoadTitleEnterForm.py
Contains only one all keyboard
Screen ID: L13

Change Log:

'''
import os
import traceback
import config
from mcommon import *
from guiBaseForms import UserForm
log = initlog('guiLoadTitleEnterForm')

class LoadTitleEnterForm(UserForm):
    
    def __init__(self):
        UserForm.__init__(self)
        self.screenID = 'L13'
        self.timeoutSec = 60
        self.preWindowID = 'AdminMainForm'
        self.uiErrorWindowID = 'AdminMainForm'
        self.lstResponseCtrl = [
            'btn_logout',
            'btn_back',
            'btn_cancel',
            'LoadTitleEnterForm_ctr_all_keyboard']

    
    def _initComponents(self):
        UserForm._initComponents(self)
        self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', { })
        globalSession.param['load_entry_form'] = self.windowID

    
    def on_btn_logout_event(self):
        self.on_exit()

    
    def on_btn_back_event(self):
        self.on_back()

    
    def on_btn_cancel_event(self):
        self.on_cancel()

    
    def on_LoadTitleEnterForm_ctr_all_keyboard_event(self):
        eventType = self._getEventParam('LoadTitleEnterForm_ctr_all_keyboard', 'type')
        if eventType == 'click':
            keyword = self._getEventParam('LoadTitleEnterForm_ctr_all_keyboard', 'val')
            if keyword == 'close':
                self.nextWindowID = 'AdminMainForm'
                self.windowJump = True
            
        elif eventType == 'ok':
            keyword = self._getEventParam('LoadTitleEnterForm_ctr_all_keyboard', 'val')
            globalSession.param['load_search_key'] = 'keyword'
            globalSession.param['load_search_val'] = keyword
            self.nextWindowID = 'LoadDiscListForm'
            self.windowJump = True
        


