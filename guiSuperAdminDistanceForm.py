# Source Generated with Decompyle++
# File: guiSuperAdminDistanceForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2009-04-30 Vincent
vincent.chen@cereson.com

Filename: guiSuperAdminDistanceForm.py
Distance1 Form
Screen ID: S3

Change Log:   

'''
import os
import traceback
import config
from mcommon import *
from guiBaseForms import UserForm
from guiRobotForm import RobotForm
log = initlog('guiSuperAdminDistanceForm')

class SuperAdminDistanceForm(UserForm, RobotForm):
    
    def __init__(self):
        RobotForm.__init__(self)
        self.screenID = 'S3'
        self.preWindowID = 'SuperAdminMainForm'
        self.uiErrorWindowID = 'SuperAdminMainForm'
        self.timeoutSec = 300
        self.lstResponseCtrl = [
            'btn_ok',
            'SuperAdminDistanceForm_ctr_message_box']

    
    def _initComponents(self):
        RobotForm._initComponents(self)
        self.flash.send('txt_msg', 'setText', {
            'text': '' })
        self.flash.send('txt_result', 'setText', {
            'text': '' })
        self.flash.send('btn_ok', 'hide', { })
        self.flash.send('btn_logout', 'hide', { })
        if globalSession.param.get('distance') == 1:
            self._distance1()
        elif globalSession.param.get('distance') == 2:
            msg = _('Metal Stick Ready?')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'confirm' })
        
        globalSession.param['distance'] = 0

    
    def on_SuperAdminDistanceForm_ctr_message_box_event(self):
        inputVal = self._getEventParam('SuperAdminDistanceForm_ctr_message_box', 'val')
        if str(inputVal).lower() == 'yes':
            self._distance2()
        else:
            self.on_back()

    
    def on_btn_ok_event(self):
        self.nextWindowID = 'SuperAdminMainForm'
        self.windowJump = True

    
    def _distance1(self):
        log.info('[%s] - [Distance 1]------------------------------------' % self.windowID)
        msg = _('Calculating distance 1 .....')
        self.flash.send('txt_msg', 'setText', {
            'text': msg })
        ret = self.robot.doCmdSync('distance1', timeout = 300)
        log.info(' ****************************** [Distance 1 Result]: %s' % ret)
        self._verifyRet(ret)
        errno = ret['errno']
        if errno == 0:
            pass
        
        log.info('[%s] - [Distance 1]------------------------------------' % self.windowID)
        distance1 = ret.get('distance')
        if distance1:
            msg = _('Distance 1: %s') % distance1
            params = {
                'distance1': distance1 }
            self.connProxy.setConfig(params)
        else:
            msg = _('No value, robot result: %s') % ret
        self.flash.send('txt_msg', 'setText', {
            'text': '' })
        self.flash.send('txt_result', 'setText', {
            'text': msg })
        self.flash.send('btn_ok', 'show', { })

    
    def _distance2(self):
        log.info('[%s] - [Distance 2]------------------------------------' % self.windowID)
        msg = _('Calculating distance 2 .....')
        self.flash.send('txt_msg', 'setText', {
            'text': msg })
        ret = self.robot.doCmdSync('distance2', timeout = 300)
        log.info(' ****************************** [Distance 2 Result]: %s' % ret)
        self._verifyRet(ret)
        errno = ret['errno']
        if errno == 0:
            pass
        
        log.info('[%s] - [Distance 2]------------------------------------' % self.windowID)
        distance2 = ret.get('distance')
        if distance2:
            msg = _('Distance 2: %s') % distance2
            params = {
                'distance2': distance2 }
            self.connProxy.setConfig(params)
        else:
            msg = _('No value, robot result: %s') % ret
        self.flash.send('txt_result', 'setText', {
            'text': msg })
        self.flash.send('btn_ok', 'show', { })


