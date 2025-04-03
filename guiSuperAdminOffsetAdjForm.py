# Source Generated with Decompyle++
# File: guiSuperAdminOffsetAdjForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2009-03-10 Vincent
vincent.chen@cereson.com

Filename: guiSuperAdminOffsetAdjForm.py
Offset Adjustment Form
Screen ID: S2

Change Log:
    2009-04-30 Vincent Go to slot 120, 520 instead of 101, 501
    2009-03-11 Vincent Fix a bug that only click [Confirm] will not re-init machine

'''
import os
import traceback
import config
from mcommon import *
from guiBaseForms import UserForm
from guiRobotForm import RobotForm
log = initlog('guiSuperAdminOffsetAdjForm')
OFFSET_250 = {
    'top_offset': ('OFFSET1XX', '120'),
    'back_offset': ('OFFSET5XX', '520'),
    'exchange_offset': ('EXCHANGE_OFFSET', ''),
    'offset2xx': ('OFFSET2XX', '230'),
    'offset6xx': ('OFFSET6XX', '620') }
OFFSET_500 = {
    'top_offset': ('OFFSET1XX', '140'),
    'back_offset': ('OFFSET5XX', '540'),
    'exchange_offset': ('EXCHANGE_OFFSET', ''),
    'offset2xx': ('OFFSET3XX', '360'),
    'offset6xx': ('OFFSET7XX', '740') }

class SuperAdminOffsetAdjForm(UserForm, RobotForm):
    
    def __init__(self):
        RobotForm.__init__(self)
        self.screenID = 'S2'
        self.preWindowID = 'SuperAdminMainForm'
        self.uiErrorWindowID = 'SuperAdminMainForm'
        self.timeoutSec = 300
        self.lstResponseCtrl = [
            'btn_up',
            'btn_down',
            'btn_try',
            'btn_confirm',
            'btn_logout',
            'btn_finish',
            'btn_cancel']

    
    def _initComponents(self):
        RobotForm._initComponents(self)
        if isS250():
            self.offset = OFFSET_250
        else:
            self.offset = OFFSET_500
        self.flash.send('btn_finish', 'hide', { })
        self.currentOffset = 'top_offset'
        self._reloadOffset()
        self.topOffset = self.connProxy._getConfigByKey('top_offset')
        self.backOffset = self.connProxy._getConfigByKey('back_offset')
        self.exchangeOffset = self.connProxy._getConfigByKey('exchange_offset')
        self.bottomOffset = self.connProxy._getConfigByKey('bottom_offset')
        self.offset2xx = self.connProxy._getConfigByKey('offset2xx')
        self.offset6xx = self.connProxy._getConfigByKey('offset6xx')

    
    def _reloadOffset(self):
        self.currentVal = float(self.connProxy._getConfigByKey(self.currentOffset))
        self.delta = self.currentVal
        self._guiConfigOffset()

    
    def on_btn_logout_event(self):
        self.on_exit()

    
    def on_btn_finish_event(self):
        self.nextWindowID = 'SuperAdminMainForm'
        self.windowJump = True

    
    def on_btn_cancel_event(self):
        self.nextWindowID = 'SuperAdminMainForm'
        self.windowJump = True

    
    def _getNextOffset(self):
        if self.currentOffset == 'top_offset':
            self.currentOffset = 'back_offset'
        elif self.currentOffset == 'back_offset':
            self.currentOffset = 'exchange_offset'
        elif self.currentOffset == 'exchange_offset':
            self.currentOffset = 'offset2xx'
        elif self.currentOffset == 'offset2xx':
            self.currentOffset = 'offset6xx'
        elif self.currentOffset == 'offset6xx':
            self.currentOffset = ''
        

    
    def _guiConfigOffset(self):
        self.flash.send('ctr_group_settings', 'show', { })
        self.flash.send('txt_process', 'hide', { })
        self.flash.send('txt_title', 'setText', {
            'text': self.offset[self.currentOffset][0] })
        self.flash.send('txt_offset', 'setText', {
            'text': str(self.currentVal) })
        self.flash.send('txt_delta', 'setText', {
            'text': str(self.delta) })

    
    def on_btn_confirm_event(self):
        self._refreshAllOffset()
        self.connProxy.setConfig({
            self.currentOffset: self.delta })
        self._getNextOffset()
        if self.currentOffset:
            self._reloadOffset()
        else:
            self.flash.send('ctr_group_settings', 'hide', { })
            self._initMachine()
            self.flash.send('btn_finish', 'show', { })
            self.flash.send('txt_process', 'show', { })
            self._setProcessText('Adjustment Done.')

    
    def _initMachine(self):
        self.flash.send('ctr_group_settings', 'hide', { })
        self.flash.send('txt_process', 'show', { })
        msg = _('Resetting Offset ...')
        self._setProcessText(msg)
        initRobot(self.topOffset, self.bottomOffset, self.exchangeOffset, self.backOffset, self.offset2xx, self.offset6xx)

    
    def _refreshAllOffset(self):
        if self.currentOffset == 'top_offset':
            self.topOffset = round(float(self.delta), 3)
        elif self.currentOffset == 'back_offset':
            self.backOffset = round(float(self.delta), 3)
        elif self.currentOffset == 'exchange_offset':
            self.exchangeOffset = round(float(self.delta), 3)
        elif self.currentOffset == 'offset2xx':
            self.offset2xx = round(float(self.delta), 3)
        elif self.currentOffset == 'offset6xx':
            self.offset6xx = round(float(self.delta), 3)
        

    
    def on_btn_try_event(self):
        self._refreshAllOffset()
        self._initMachine()
        self._goToExchange()
        slot = self.offset[self.currentOffset][1]
        if slot:
            self._goToSlotInsert(slot)
        
        self._guiConfigOffset()

    
    def on_btn_up_event(self):
        self.delta += 10
        self.flash.send('txt_delta', 'setText', {
            'text': str(self.delta) })

    
    def on_btn_down_event(self):
        self.delta -= 10
        self.flash.send('txt_delta', 'setText', {
            'text': str(self.delta) })

    
    def _setProcessText(self, msg):
        self.flash.send('txt_process', 'setText', {
            'text': msg })

    
    def _guiGoToExchange(self):
        self.flash.send('ctr_group_settings', 'hide', { })
        self.flash.send('txt_process', 'show', { })
        msg = _('Going to Exchange Box ...')
        self._setProcessText(msg)

    
    def _guiGoToSlotInsert(self, slotID):
        self.flash.send('ctr_group_settings', 'hide', { })
        self.flash.send('txt_process', 'show', { })
        msg = _('Going to Slot %s ...') % slotID
        self._setProcessText(msg)


