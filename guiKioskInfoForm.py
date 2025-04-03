# Source Generated with Decompyle++
# File: guiKioskInfoForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiKioskInfoForm.py
Kiosk Info Form with "Restore Factory Settings" btn
Screen ID: I1

Change Log:
    2009-05-07 Andrew: Add external ip
    2009-03-30 Vincent: Add setIP
    2009-03-06 Vincent: Stop HDMI before touch screen adjust shows
    2009-02-24 Vincent: Add Touch screen adjust script
'''
import os
import re
import http.client
import config
from mcommon import *
from guiBaseForms import UserForm
log = initlog('guiKioskInfoForm')
URL1 = 'cereson.mydvdkiosks.net'
URL2 = '/api/getIp'
IP_RE = '^((\\d|[1-9]\\d|1\\d\\d|2[0-4]\\d|25[0-5])\\.){3}(\\d|[1-9]\\d|1\\d\\d|2[0-4]\\d|25[0-5])$'

class KioskInfoForm(UserForm):
    
    def __init__(self):
        UserForm.__init__(self)
        self.nextWindowID = 'AdminMainForm'
        self.preWindowID = 'AdminMainForm'
        self.screenID = 'I1'
        self.uiErrorWindowID = 'AdminMainForm'
        self.timeoutSec = 120
        self.lstResponseCtrl = [
            'btn_logout',
            'btn_back',
            'btn_cancel',
            'btn_restore',
            'KioskInfoForm_ctr_message_box',
            'KioskInfoForm_ctr_num_keyboard']

    
    def _initComponents(self):
        UserForm._initComponents(self)
        self.connProxy.setIP()
        kioskInfo = self.connProxy.getKioskInfo()
        kioskInfo['external_ip'] = 'fetching...'
        self.flash.send('btn_logout', 'hide', { })
        self.flash.send('btn_back', 'hide', { })
        self.flash.send('btn_restore', 'hide', { })
        self.flash.send('ctr_information', 'setReport', {
            'ctr_information': kioskInfo })
        kioskInfo['external_ip'] = self._getExternalIP()
        self.flash.send('ctr_information', 'setReport', {
            'ctr_information': kioskInfo })
        self.flash.send('btn_logout', 'show', { })
        self.flash.send('btn_back', 'show', { })
        self.flash.send('btn_restore', 'show', { })

    
    def _getExternalIP(self):
        
        try:
            http = http.client.HTTPConnection(URL1)
            http.request('GET', URL2)
            http.sock.settimeout(5)
            res = http.getresponse()
            if res.status == 200:
                ip = res.read()
                if not re.match(IP_RE, ip):
                    log.info('invalid IP: %s' % ip)
                    ip = ''
                
                self.connProxy.setExternalIP(ip)
            else:
                log.info('Failed to reach the server. %d %s' % (res.status, res.reason))
                ip = ''
        except Exception:
            log.info('Failed to reach the server. Unknown error')
            ip = ''

        return ip

    
    def on_btn_logout_event(self):
        self.on_exit()

    
    def on_btn_back_event(self):
        self.on_back()

    
    def on_btn_cancel_event(self):
        self.on_cancel()

    
    def on_btn_restore_event(self):
        msg = _('All data will be restored to factory settings!\n\nAre you sure?')
        self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
            'message': msg,
            'type': 'confirm',
            'height': '300' })

    
    def on_KioskInfoForm_ctr_message_box_event(self):
        if self._getEventParam('KioskInfoForm_ctr_message_box', 'val') == 'yes':
            self.flash.send('%s_ctr_num_keyboard' % self.windowID, 'show', {
                'type': 'password' })
        

    
    def on_KioskInfoForm_ctr_num_keyboard_event(self):
        eventType = self._getEventParam('KioskInfoForm_ctr_num_keyboard', 'type')
        if eventType == 'click':
            pass
        elif eventType == 'ok':
            passcode = self._getEventParam('KioskInfoForm_ctr_num_keyboard', 'val')
            status = str(self.connProxy.initDb(passcode))
            log.info('[initDb status]: %s' % status)
            if status == '0':
                pass
            elif status == '1':
                stopHdmi()
                os.system('cd /elo;echo howcute121|sudo -S DISPLAY=:0.0 ./elova -u')
                startHdmi()
                self.nextWindowID = 'MainForm'
                self.windowJump = True
            elif status == '2':
                pass
            
        


