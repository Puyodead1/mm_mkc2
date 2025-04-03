# Source Generated with Decompyle++
# File: guiUnloadMarkedForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2009-04-30 Vincent
vincent.chen@cereson.com

Filename: guiUnloadMarkedForm.py
Unload By Marked
Screen ID: U3

Change Log:    

'''
import traceback
import config
from mcommon import *
from guiBaseForms import UserForm
log = initlog('guiUnloadMarkedForm')

class UnloadMarkedForm(UserForm):
    
    def __init__(self):
        UserForm.__init__(self)
        self.nextWindowID = 'AdminMainForm'
        self.screenID = 'U3'
        self.timeoutSec = 60
        self.preWindowID = 'AdminMainForm'
        self.uiErrorWindowID = 'AdminMainForm'
        self.lstResponseCtrl = [
            'btn_logout',
            'btn_back',
            'btn_cancel',
            'ctr_movie_list',
            'UnloadMarkedForm_ctr_message_box',
            'btn_unload_all']

    
    def _initComponents(self):
        UserForm._initComponents(self)
        self.lstMovie = self.connProxy.getUnloadMovieList('genre', 'unload|bad')
        for mv in self.lstMovie:
            mv['movie_pic'] = getPicFullPath(mv.get('movie_pic'))
        
        self.flash.send('ctr_movie_list', 'setMovieList', {
            'ctr_movie_list': self.lstMovie })
        self.flash.send('txt_found', 'setText', {
            'text': str(len(self.lstMovie)) })
        globalSession.param['unload_entry_form'] = self.windowID
        globalSession.shoppingCart.clear()
        self.flash.send('UnloadMarkedForm_ctr_message_box', 'close', { })

    
    def on_btn_logout_event(self):
        self.on_exit()

    
    def on_btn_back_event(self):
        self.on_back()

    
    def on_btn_cancel_event(self):
        self.on_cancel()

    
    def on_btn_unload_all_event(self):
        if self.lstMovie:
            for d in self.lstMovie:
                disc = Disc()
                disc.rfid = d.get('rfid')
                disc.slotID = d.get('slot_id')
                globalSession.shoppingCart.addDisc(disc)
            
            self.nextWindowID = 'UnloadEjectForm'
            self.windowJump = True
        

    
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
        

    
    def on_UnloadMarkedForm_ctr_message_box_event(self):
        if self._getEventParam('UnloadMarkedForm_ctr_message_box', 'val') == 'yes':
            globalSession.shoppingCart.addDisc(globalSession.disc)
            self.nextWindowID = 'UnloadEjectForm'
            self.windowJump = True
        


