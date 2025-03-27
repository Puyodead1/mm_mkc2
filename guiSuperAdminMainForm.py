# Source Generated with Decompyle++
# File: guiSuperAdminMainForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2009-03-10 Vincent
vincent.chen@cereson.com

Filename: guiSuperAdminMainForm.py
Super Admin Main Form
Screen ID: S1

Change Log:
    2009-04-30 Vincent Add support of distance1, distance2

'''
import os
import traceback
import config
from mcommon import *
from guiBaseForms import UserForm
log = initlog('guiSuperAdminMainForm')

class SuperAdminMainForm(UserForm):
    
    def __init__(self):
        UserForm.__init__(self)
        self.screenID = 'S1'
        self.preWindowID = 'MainForm'
        self.uiErrorWindowID = 'MainForm'
        self.timeoutSec = 60
        self.lstResponseCtrl = [
            'btn_logout',
            'btn_vertical_adj',
            'btn_offset_adj',
            'btn_test',
            'btn_distance1',
            'btn_distance2']

    
    def _initComponents(self):
        UserForm._initComponents(self)

    
    def on_btn_logout_event(self):
        self.on_exit()

    
    def on_btn_vertical_adj_event(self):
        self.nextWindowID = 'SuperAdminVerticalAdjForm'
        self.windowJump = True

    
    def on_btn_offset_adj_event(self):
        self.nextWindowID = 'SuperAdminOffsetAdjForm'
        self.windowJump = True

    
    def on_btn_test_event(self):
        self.nextWindowID = 'TestMainForm'
        self.windowJump = True

    
    def on_btn_distance1_event(self):
        globalSession.param['distance'] = 1
        self.nextWindowID = 'SuperAdminDistanceForm'
        self.windowJump = True

    
    def on_btn_distance2_event(self):
        globalSession.param['distance'] = 2
        self.nextWindowID = 'SuperAdminDistanceForm'
        self.windowJump = True


