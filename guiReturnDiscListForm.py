# Source Generated with Decompyle++
# File: guiReturnDiscListForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2009-04-09 Vincent
vincent.chen@cereson.com

Filename: guiReturnDiscListForm.py
Screen ID: T4

Change Log:
'''
import os
import traceback
from mcommon import *
from guiBaseForms import UserForm
from proxy.tools import getCurTime
log = initlog('guiReturnDiscListForm')

class ReturnDiscListForm(UserForm):
    
    def __init__(self):
        super(ReturnDiscListForm, self).__init__()
        self.screenID = 'T4'
        self.preWindowID = 'ReturnOptionForm'
        self.timeoutSec = 60
        self.lstResponseCtrl.extend([
            'ctr_disc_list',
            'btn_back'])

    
    def _initComponents(self):
        super(ReturnDiscListForm, self)._initComponents()
        self._setDiscList()
        self.flash.send('txt_time_now', 'setText', {
            'text': getCurTime() })

    
    def _setDiscList(self):
        lstDisc = globalSession.param['disc_list']
        discList = []
        for disc in lstDisc:
            dic = { }
            dic['movie_title'] = disc.title
            dic['movie_pic'] = getPicFullPath(disc.picture)
            dic['time_out'] = disc.outTime
            dic['rfid'] = disc.rfid
            discList.append(dic)
        
        self.flash.send('ctr_disc_list', 'setDiscList', {
            'ctr_disc_list': discList })

    
    def on_ctr_disc_list_event(self):
        rfid = self._getEventParam('ctr_disc_list', 'rfid')
        if rfid:
            globalSession.disc.rfid = rfid
            globalSession.param['return_option'] = 'card'
            self.nextWindowID = 'ReturnTakeInForm'
            self.windowJump = True
        

    
    def on_btn_back_event(self):
        self.on_back()


