# Source Generated with Decompyle++
# File: guiPickUpDiscListForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiPickUpDiscListForm.py
Pick Up Disc List
Screen ID: P2

Change Log:

'''
import os
import traceback
from mcommon import *
from guiBaseForms import CustomerForm
log = initlog('guiPickUpDiscListForm')

class PickUpDiscListForm(CustomerForm):
    
    def __init__(self):
        super(PickUpDiscListForm, self).__init__()
        self.preWindowID = 'PickUpCodeForm'
        self.nextWindowID = 'PickUpEjectForm'
        self.screenID = 'P2'
        self.timeoutSec = 120
        self.lstResponseCtrl.extend([
            'btn_cancel',
            'btn_back',
            'btn_take_all'])

    
    def _initComponents(self):
        super(PickUpDiscListForm, self)._initComponents()
        if globalSession.loginCustomer.isLogin:
            if globalSession.loginCustomer.ccNum:
                text = globalSession.loginCustomer.ccNum[-4:]
            else:
                i = globalSession.loginCustomer.email.index('@')
                text = globalSession.loginCustomer.email[:i]
        else:
            text = ''
        self.flash.send('txt_msg', 'setText', {
            'text': text })
        self.shoppingCart = globalSession.pickupCart
        lstDisc = []
        for disc in self.shoppingCart.discs:
            dict = { }
            dict['movie_title'] = disc.title
            dict['movie_pic'] = getPicFullPath(disc.picture)
            dict['rfid'] = disc.rfid
            lstDisc.append(dict)
        
        self.flash.send('ctr_dvd_list', 'setDVDList', {
            'ctr_dvd_list': lstDisc })
        if self.shoppingCart.discs:
            self.flash.send('btn_take_all', 'show', { })
        else:
            self.flash.send('btn_take_all', 'hide', { })

    
    def on_btn_cancel_event(self):
        self.on_cancel()

    
    def on_btn_back_event(self):
        if globalSession.loginCustomer.isLogin:
            self.nextWindowID = 'MembershipCenterForm'
        else:
            self.nextWindowID = self.preWindowID
        self.windowJump = True

    
    def on_btn_take_all_event(self):
        self.nextWindowID = 'PickUpEjectForm'
        self.windowJump = True


