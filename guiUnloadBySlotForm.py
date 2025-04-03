# Source Generated with Decompyle++
# File: guiUnloadBySlotForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiUnloadBySlotForm.py
Unload By Slot
Screen ID: U12

Change Log:

'''
import os
import traceback
import config
from mcommon import *
from guiBaseForms import UserForm
log = initlog('guiUnloadBySlotForm')

class UnloadBySlotForm(UserForm):
    
    def __init__(self):
        UserForm.__init__(self)
        self.nextWindowID = 'AdminMainForm'
        self.screenID = 'U12'
        self.timeoutSec = 60
        self.preWindowID = 'AdminMainForm'
        self.uiErrorWindowID = 'AdminMainForm'
        self.lstResponseCtrl = [
            'btn_logout',
            'btn_back',
            'btn_cancel',
            'btn_icon_keyboard',
            'UnloadBySlotForm_ctr_num_keyboard',
            'ctr_movie_list',
            'UnloadBySlotForm_ctr_message_box']

    
    def _initComponents(self):
        UserForm._initComponents(self)
        lstMovie = self.connProxy.getUnloadMovieList('slot', '')
        for mv in lstMovie:
            mv['movie_pic'] = getPicFullPath(mv.get('movie_pic'))
        
        self.flash.send('ctr_movie_list', 'setMovieList', {
            'ctr_movie_list': lstMovie })
        self.flash.send('txt_found', 'setText', {
            'text': str(len(lstMovie)) })
        globalSession.param['unload_entry_form'] = self.windowID
        globalSession.shoppingCart.clear()

    
    def on_btn_logout_event(self):
        self.on_exit()

    
    def on_btn_back_event(self):
        self.on_back()

    
    def on_btn_cancel_event(self):
        self.on_cancel()

    
    def on_btn_icon_keyboard_event(self):
        self.flash.send('%s_ctr_num_keyboard' % self.windowID, 'show', { })

    
    def on_UnloadBySlotForm_ctr_num_keyboard_event(self):
        eventType = self._getEventParam('UnloadBySlotForm_ctr_num_keyboard', 'type')
        if eventType == 'click':
            pass
        elif eventType == 'ok':
            slotID = self._getEventParam('UnloadBySlotForm_ctr_num_keyboard', 'val')
            lstMovie = self.connProxy.getUnloadMovieList('slot', slotID)
            for mv in lstMovie:
                mv['movie_pic'] = getPicFullPath(mv.get('movie_pic'))
            
            self.flash.send('ctr_movie_list', 'setMovieList', {
                'ctr_movie_list': lstMovie })
            self.flash.send('txt_found', 'setText', {
                'text': str(len(lstMovie)) })
            if len(lstMovie) == 1:
                globalSession.disc = Disc()
                globalSession.disc.slotID = lstMovie[0].get('slot_id')
                globalSession.disc.title = lstMovie[0].get('movie_title')
                globalSession.disc.upc = lstMovie[0].get('upc')
                globalSession.disc.rfid = lstMovie[0].get('rfid')
                msg = _('Are you sure to unload this disc?')
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': msg,
                    'type': 'confirm' })
            elif not lstMovie:
                self.flash.send('%s_ctr_num_keyboard' % self.windowID, 'show', { })
            
        

    
    def on_ctr_movie_list_event(self):
        rfid = self._getEventParam('ctr_movie_list', 'rfid')
        if rfid:
            globalSession.disc = Disc()
            globalSession.disc.rfid = rfid
            globalSession.disc.slotID = self._getEventParam('ctr_movie_list', 'slot_id')
            msg = _('Are you sure to unload this disc?')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'confirm' })
        

    
    def on_UnloadBySlotForm_ctr_message_box_event(self):
        if self._getEventParam('UnloadBySlotForm_ctr_message_box', 'val') == 'yes':
            globalSession.shoppingCart.addDisc(globalSession.disc)
            self.nextWindowID = 'UnloadEjectForm'
            self.windowJump = True
        


