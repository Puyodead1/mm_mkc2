# Source Generated with Decompyle++
# File: guiUnloadByTitleForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiUnloadByTitleForm.py
Unload By Title
Screen ID: U13

Change Log:
    2009-04-30 Vincent Add "Unload All" button

'''
import os
import traceback
import config
from mcommon import *
from guiBaseForms import UserForm
log = initlog('guiUnloadByTitleForm')

class UnloadByTitleForm(UserForm):
    
    def __init__(self):
        UserForm.__init__(self)
        self.nextWindowID = 'AdminMainForm'
        self.screenID = 'U13'
        self.timeoutSec = 60
        self.preWindowID = 'AdminMainForm'
        self.uiErrorWindowID = 'AdminMainForm'
        self.unloadMethod = ''
        self.lstResponseCtrl = [
            'btn_logout',
            'btn_unload_all',
            'btn_back',
            'btn_icon_keyboard',
            'UnloadByTitleForm_ctr_all_keyboard',
            'ctr_movie_list',
            'UnloadByTitleForm_ctr_message_box']

    
    def _initComponents(self):
        UserForm._initComponents(self)
        lstMovie = self.connProxy.getUnloadMovieList('keyword', '')
        for mv in lstMovie:
            mv['movie_pic'] = getPicFullPath(mv.get('movie_pic'))
        
        self.flash.send('ctr_movie_list', 'setMovieList', {
            'ctr_movie_list': lstMovie })
        self.flash.send('txt_found', 'setText', {
            'text': str(len(lstMovie)) })
        globalSession.param['unload_entry_form'] = self.windowID
        globalSession.shoppingCart.clear()
        self.flash.send('btn_unload_all', 'hide', { })
        self.flash.send('UnloadByTitleForm_ctr_all_keyboard', 'close', { })
        self.flash.send('UnloadByTitleForm_ctr_message_box', 'close', { })
        self.unloadMethod = ''

    
    def on_btn_logout_event(self):
        self.on_exit()

    
    def on_btn_back_event(self):
        self.on_back()

    
    def on_btn_cancel_event(self):
        self.on_cancel()

    
    def on_btn_icon_keyboard_event(self):
        self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', { })

    
    def on_UnloadByTitleForm_ctr_all_keyboard_event(self):
        eventType = self._getEventParam('UnloadByTitleForm_ctr_all_keyboard', 'type')
        if eventType == 'click':
            pass
        elif eventType == 'ok':
            keyword = self._getEventParam('UnloadByTitleForm_ctr_all_keyboard', 'val')
            self.lstMovie = self.connProxy.getUnloadMovieList('keyword', keyword)
            for mv in self.lstMovie:
                mv['movie_pic'] = getPicFullPath(mv.get('movie_pic'))
            
            self.flash.send('ctr_movie_list', 'setMovieList', {
                'ctr_movie_list': self.lstMovie })
            self.flash.send('txt_found', 'setText', {
                'text': str(len(self.lstMovie)) })
            if len(self.lstMovie) == 1:
                globalSession.disc = Disc()
                globalSession.disc.slotID = self.lstMovie[0].get('slot_id')
                globalSession.disc.title = self.lstMovie[0].get('title')
                globalSession.disc.upc = self.lstMovie[0].get('upc')
                globalSession.disc.rfid = self.lstMovie[0].get('rfid')
                self.unloadMethod = 'one'
                msg = _('Are you sure to unload this disc?')
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': msg,
                    'type': 'confirm' })
            elif not (self.lstMovie):
                self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', { })
            else:
                self.flash.send('btn_unload_all', 'show', { })
        

    
    def on_ctr_movie_list_event(self):
        rfid = self._getEventParam('ctr_movie_list', 'rfid')
        if rfid:
            self.unloadMethod = 'one'
            globalSession.disc = Disc()
            globalSession.disc.rfid = rfid
            globalSession.disc.slotID = self._getEventParam('ctr_movie_list', 'slot_id')
            msg = _('Are you sure to unload this disc?')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'confirm' })
        

    
    def on_UnloadByTitleForm_ctr_message_box_event(self):
        if self._getEventParam('UnloadByTitleForm_ctr_message_box', 'val') == 'yes':
            if self.unloadMethod == 'one':
                globalSession.shoppingCart.addDisc(globalSession.disc)
            elif self.unloadMethod == 'all':
                for d in self.lstMovie:
                    disc = Disc()
                    disc.rfid = d.get('rfid')
                    disc.slotID = d.get('slot_id')
                    globalSession.shoppingCart.addDisc(disc)
                
            
            self.nextWindowID = 'UnloadEjectForm'
            self.windowJump = True
        

    
    def on_btn_unload_all_event(self):
        if self.lstMovie:
            self.unloadMethod = 'all'
            c = len(self.lstMovie)
            msg = _('Are you sure to unload ALL %s discs?') % c
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'confirm' })
        


