# Source Generated with Decompyle++
# File: guiConfigSpeakerVolumeForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2009-06-04 Andrew
andrew.lu@cereson.com

Filename: guiVolumeForm.py
set system volume.
Screen ID: C3

Change Log:
    
'''
from mcommon import *
from guiBaseForms import ConfigForm
from linuxCmd import setSystemVolume, storeSystemVolume
log = initlog('guiConfigSpeakerVolumeForm')

class ConfigSpeakerVolumeForm(ConfigForm):
    
    def __init__(self):
        ConfigForm.__init__(self)
        self.screenID = 'C3'
        self.preWindowID = 'AdminMainForm'
        self.uiErrorWindowID = 'AdminMainForm'
        self.timeoutSec = 60
        self.lstResponseCtrl += [
            'btn_volume',
            'btn_confirm',
            'btn_speaker_off',
            'btn_speaker_on']

    
    def _initComponents(self):
        ConfigForm._initComponents(self)
        self.volume = self.connProxy._getConfigByKey('speaker_volume')
        if self.volume == '0':
            self.volume = '80'
            self.flash.send('btn_speaker_on', 'hide', { })
            self.flash.send('btn_speaker_off', 'show', { })
            self.silent = True
        else:
            self.flash.send('btn_speaker_on', 'show', { })
            self.flash.send('btn_speaker_off', 'hide', { })
            self.silent = False
        self.flash.send('btn_volume', 'setVolume', {
            'number': self.volume })

    
    def on_btn_volume_event(self):
        self.volume = self._getEventParam('btn_volume', 'volume')
        if self.silent == False:
            setSystemVolume(self.volume)
        

    
    def on_btn_confirm_event(self):
        if self.silent == True:
            self.volume = 0
        
        self.connProxy.setConfig({
            'speaker_volume': self.volume })
        storeSystemVolume(self.volume)
        self.nextWindowID = 'AdminMainForm'
        self.windowJump = True

    
    def on_btn_speaker_on_event(self):
        self.flash.send('btn_speaker_on', 'hide', { })
        self.flash.send('btn_speaker_off', 'show', { })
        self.silent = True
        setSystemVolume(0)

    
    def on_btn_speaker_off_event(self):
        self.flash.send('btn_speaker_on', 'show', { })
        self.flash.send('btn_speaker_off', 'hide', { })
        self.silent = False
        setSystemVolume(self.volume)

    
    def on_hide(self):
        volume = self.connProxy._getConfigByKey('speaker_volume')
        setSystemVolume(volume)


