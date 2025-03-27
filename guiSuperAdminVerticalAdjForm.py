# Source Generated with Decompyle++
# File: guiSuperAdminVerticalAdjForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2009-03-06 Vincent
vincent.chen@cereson.com

Filename: guiSuperAdminVerticalAdjForm.py
Vertical Adjustment Form
Screen ID: S2

Change Log:

'''
import os
import traceback
import config
from mcommon import *
from control import *
from guiBaseForms import UserForm
log = initlog('guiSuperAdminVerticalAdjForm')

class SuperAdminVerticalAdjForm(UserForm):
    
    def __init__(self):
        UserForm.__init__(self)
        self.screenID = 'S2'
        self.preWindowID = 'SuperAdminMainForm'
        self.uiErrorWindowID = 'SuperAdminMainForm'
        self.timeoutSec = 300
        self.lstResponseCtrl = [
            'btn_cancel',
            'btn_next_step1',
            'btn_next_step2',
            'btn_next_step3',
            'btn_finish_step4']
        robot = Robot()
        self.robot = robot.getInstance()

    
    def _initComponents(self):
        UserForm._initComponents(self)
        msg = _('Please disconnect the power cable first.')
        self.flash.send('txt_step1', 'setText', {
            'text': msg })
        self.flash.send('ctr_group_step1', 'show', { })
        self.flash.send('ctr_group_step2', 'hide', { })
        self.flash.send('ctr_group_step3', 'hide', { })
        self.flash.send('ctr_group_step4', 'hide', { })

    
    def on_btn_cancel_event(self):
        self.on_cancel()

    
    def _getVqd(self):
        ret = self.robot.doCmdSync('vqd')
        log.info('vqd cmd result: [%s]' % ret)
        errno = ret.get('errno')
        vqd = ret.get('vertical')
        return int(vqd)

    
    def on_btn_next_step1_event(self):
        msg = _('Raise the carriage to the top, verify its height, then click [Next]')
        self.flash.send('txt_step2', 'setText', {
            'text': msg })
        self.flash.send('ctr_group_step1', 'hide', { })
        self.flash.send('ctr_group_step2', 'show', { })
        self.flash.send('ctr_group_step3', 'hide', { })
        self.flash.send('ctr_group_step4', 'hide', { })

    
    def on_btn_next_step2_event(self):
        self.flash.send('btn_next_step2', 'hide', { })
        self.flash.send('txt_step2', 'setText', {
            'text': _('Getting height ...') })
        self.qd1 = self._getVqd()
        self.flash.send('btn_next_step2', 'show', { })
        self.flash.send('txt_step2', 'setText', {
            'text': '' })
        msg = _('Push the carriage to the bottom, verify its height, then click [Next]')
        self.flash.send('txt_step3', 'setText', {
            'text': msg })
        self.flash.send('ctr_group_step1', 'hide', { })
        self.flash.send('ctr_group_step2', 'hide', { })
        self.flash.send('ctr_group_step3', 'show', { })
        self.flash.send('ctr_group_step4', 'hide', { })

    
    def on_btn_next_step3_event(self):
        self.flash.send('btn_next_step3', 'hide', { })
        self.flash.send('txt_step3', 'setText', {
            'text': _('Getting height ...') })
        self.qd2 = self._getVqd()
        self.flash.send('btn_next_step3', 'show', { })
        self.flash.send('txt_step3', 'setText', {
            'text': '' })
        pulses_per_slot = round(abs(self.qd2 - self.qd1) / 69, 3)
        log.info('Save pulses_per_slot to [%s]' % pulses_per_slot)
        self.connProxy.setConfig({
            'pulses_per_slot': pulses_per_slot })
        msg = _('Vertical data saved. Please reconnect the power cable.')
        self.flash.send('txt_step4', 'setText', {
            'text': msg })
        self.flash.send('ctr_group_step1', 'hide', { })
        self.flash.send('ctr_group_step2', 'hide', { })
        self.flash.send('ctr_group_step3', 'hide', { })
        self.flash.send('ctr_group_step4', 'show', { })

    
    def on_btn_finish_step4_event(self):
        self.flash.send('ctr_group_step1', 'hide', { })
        self.flash.send('ctr_group_step2', 'hide', { })
        self.flash.send('ctr_group_step3', 'hide', { })
        self.flash.send('ctr_group_step4', 'show', { })
        self.flash.send('btn_finish_step4', 'hide', { })
        self.flash.send('demo_step4', 'hide', { })
        msg = _('Adjustment Finished. ')
        self.flash.send('txt_step4', 'setText', {
            'text': msg })


