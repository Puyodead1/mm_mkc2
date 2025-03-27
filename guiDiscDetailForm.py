# Source Generated with Decompyle++
# File: guiDiscDetailForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiDiscDetailForm.py
Disc detail screen with movie information, synopsis and trailers
Screen ID: R3

Change Log:
    Vincent 2009-03-18 Add Blu ray icon
'''
from mcommon import *
from config import KIOSK_HOME, HDMI_CONNECT
from guiBaseForms import CustomerForm
log = initlog('guiDiscDetailForm')

class DiscDetailForm(CustomerForm):
    
    def __init__(self):
        super(DiscDetailForm, self).__init__()
        self.screenID = 'R3'
        self.preWindowID = 'RentMainForm'
        self.timeoutSec = 180
        self.lstResponseCtrl.extend([
            'btn_back',
            'btn_cancel',
            'btn_next',
            'btn_available_notice'])

    
    def _initComponents(self):
        super(DiscDetailForm, self)._initComponents()
        self.disc = globalSession.disc
        self.movieProxy.getMovieDetailByUpc(self.disc)
        release = self.movieProxy.allowRental(self.disc)
        if release == '1':
            self.flash.send('mask_coming_soon_flag', 'show', { })
        else:
            self.flash.send('mask_coming_soon_flag', 'hide', { })
        dictDisc = { }
        dictDisc['movie_title'] = self.disc.title
        dictDisc['movie_pic'] = getPicFullPath(self.disc.picture)
        if MKC_THEME == 'game':
            dictDisc['dvd_version'] = ''
        else:
            dictDisc['dvd_version'] = self.disc.version
        dictDisc['synopsis'] = self.disc.synopsis
        dictDisc['trailer_name'] = self.disc.trailerName
        dictDisc['rent_price'] = self.disc.rentalPrice
        if '%.2f' % round(float(self.disc.salePrice), 2) == '0.00':
            dictDisc['buy_price'] = ''
        else:
            dictDisc['buy_price'] = self.disc.salePrice
        feature = []
        if MKC_THEME == 'game':
            feature.append({
                _('Console/System'): self.disc.version.strip('()') })
            feature.append({
                _('Release Date'): self.disc.releaseDate })
            feature.append({
                _('Rating'): self.disc.rating })
        else:
            feature.append({
                _('Directors'): self.disc.directors })
            feature.append({
                _('Rating'): self.disc.rating })
            feature.append({
                _('Genre'): self.disc.genre })
            feature.append({
                _('Release Date'): self.disc.releaseDate })
            feature.append({
                _('Starring'): self.disc.starring })
        dictDisc['feature'] = feature
        if release != '1' and self.disc.availableCount > 0:
            dictDisc['is_available'] = '1'
            self.flash.send('btn_next', 'show', { })
            self.flash.send('btn_available_notice', 'hide', { })
        else:
            dictDisc['is_available'] = '0'
            self.flash.send('btn_next', 'hide', { })
            if self.connProxy._getConfigByKey('show_available_notice') == 'yes':
                self.flash.send('btn_available_notice', 'show', { })
            else:
                self.flash.send('btn_available_notice', 'hide', { })
        if self.disc.isBluray:
            dictDisc['is_bluray'] = '1'
        elif self.disc.discType == 'WII':
            dictDisc['is_bluray'] = '2'
        elif self.disc.discType == 'XBOX360':
            dictDisc['is_bluray'] = '3'
        elif self.disc.discType == 'PS3':
            dictDisc['is_bluray'] = '4'
        else:
            dictDisc['is_bluray'] = '0'
        if self._has_hdmi():
            self.flash.send('ctr_movie_detail', 'setVideoVolume', {
                'volume': 'off' })
        else:
            self.flash.send('ctr_movie_detail', 'setVideoVolume', {
                'volume': 'on' })
        self.flash.send('ctr_movie_detail', 'setMovieDetail', {
            'ctr_movie_detail': dictDisc })
        self.flash.wid = self.windowID

    
    def _has_hdmi(self):
        return os.path.isfile(HDMI_CONNECT)

    
    def on_btn_back_event(self):
        self.on_back()

    
    def on_btn_cancel_event(self):
        self.on_cancel()

    
    def on_btn_next_event(self):
        self.nextWindowID = 'DiscPriceForm'
        self.windowJump = True

    
    def on_btn_available_notice_event(self):
        self.nextWindowID = 'DiscAvailableNoticeForm'
        self.windowJump = True


