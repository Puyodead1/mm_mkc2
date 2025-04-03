# Source Generated with Decompyle++
# File: guiReportForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiReportForm.py
Simple Report Form
Screen ID: I1

Change Log:

'''
import os
import traceback
import config
from mcommon import *
from guiBaseForms import UserForm
log = initlog('guiReportForm')

class ReportForm(UserForm):
    
    def __init__(self):
        UserForm.__init__(self)
        self.nextWindowID = 'AdminMainForm'
        self.screenID = 'I1'
        self.timeoutSec = 180
        self.preWindowID = 'AdminMainForm'
        self.uiErrorWindowID = 'AdminMainForm'
        self.lstResponseCtrl = [
            'btn_logout',
            'btn_cancel',
            'btn_back']

    
    def _initComponents(self):
        UserForm._initComponents(self)
        reportData = self.connProxy.getSimpleReportData()
        self.flash.send('ctr_report', 'setReport', {
            'ctr_report': reportData })

    
    def on_btn_logout_event(self):
        self.on_exit()

    
    def on_btn_back_event(self):
        self.on_back()

    
    def on_btn_cancel_event(self):
        self.on_cancel()


