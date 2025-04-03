# Source Generated with Decompyle++
# File: guiLoadDiscListForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiLoadDiscListForm.py
Admin Main Form
Screen ID: A1

Change Log:

'''
import os
import traceback
import config
from mcommon import *
from guiBaseForms import UserForm
log = initlog('guiLoadDiscListForm')

class LoadDiscListForm(UserForm):
    
    def __init__(self):
        UserForm.__init__(self)
        self.screenID = 'L2'
        self.timeoutSec = 60
        self.preWindowID = 'AdminMainForm'
        self.uiErrorWindowID = 'AdminMainForm'
        self.lstResponseCtrl = [
            'btn_logout',
            'btn_back',
            'btn_cancel',
            'ctr_movie_list']

    
    def _setMovieList(self):
        for mv in self.mvlist:
            mv['movie_pic'] = getPicFullPath(mv.get('movie_pic'))
        
        self.flash.send('ctr_movie_list', 'setMovieList', {
            'ctr_movie_list': self.mvlist })
        totalCount = str(len(self.mvlist))
        self.flash.send('txt_found_label', 'show', { })
        self.flash.send('txt_found', 'show', { })
        self.flash.send('txt_found', 'setText', {
            'text': totalCount })

    
    def _displayDiscList(self):
        searchKey = globalSession.param.get('load_search_key')
        searchVal = globalSession.param.get('load_search_val')
        self.mvlist = self.movieProxy.getMovieList(searchKey, searchVal)
        if searchKey == 'genre':
            searchVal = _('New Release')
        elif searchKey == 'upc':
            searchVal = _('UPC %s') % searchVal
        
        self._setMovieList()
        self.flash.send('txtbox_key', 'setText', {
            'text': searchVal })

    
    def _initComponents(self):
        UserForm._initComponents(self)
        self.flash.send('txtbox_key', 'setText', {
            'text': _('Loading ......') })
        self.flash.send('ctr_movie_list', 'setMovieList', {
            'ctr_movie_list': [] })
        self.flash.send('txt_found', 'hide', { })
        self.flash.send('txt_found_label', 'hide', { })
        self._displayDiscList()

    
    def on_btn_logout_event(self):
        self.on_exit()

    
    def on_btn_back_event(self):
        self.on_back()

    
    def on_btn_cancel_event(self):
        self.on_cancel()

    
    def on_ctr_movie_list_event(self):
        upc = self._getEventParam('ctr_movie_list', 'upc')
        if upc:
            disc = Disc()
            disc.upc = upc
            self.movieProxy.getMovieDetailByUpc(disc)
            globalSession.disc = disc
            self.nextWindowID = 'LoadDiscInfoForm'
            self.windowJump = True
        


