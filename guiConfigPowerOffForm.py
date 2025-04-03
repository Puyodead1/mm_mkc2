# Source Generated with Decompyle++
# File: guiConfigPowerOffForm.pyc (Python 2.5)

'''
Created on 2010-7-16
@author: andrew.lu@cereson.com
'''
from mcommon import *
from guiBaseForms import ConfigForm
log = initlog('ConfigPowerOffForm')

class ConfigPowerOffForm(ConfigForm):
    
    def __init__(self):
        super(ConfigPowerOffForm, self).__init__()
        self.screenID = 'C8'
        self.preWindowID = 'AdminMainForm'
        self.uiErrorWindowID = 'AdminMainForm'
        self.timeoutSec = 60
        self.lstResponseCtrl += [
            'ConfigPowerOffForm_ctr_message_box']
        self.services = [
            'db_sync_thread.py',
            'media_download_thread.py',
            'upg_postauth_thread.py',
            'check_reserved_trs_thread.py',
            'manage_kiosk_thread.py',
            'auto_reduce.py',
            'server_kiosk_sync_thread.py',
            'upc_db_updation_thread.py']

    
    def _initComponents(self):
        super(ConfigPowerOffForm, self)._initComponents()
        self.flash.send('txt_status', 'setText', {
            'text': '' })
        msg = _('Are you sure to power off the kiosk?')
        self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
            'message': msg,
            'type': 'confirm' })

    
    def on_ConfigPowerOffForm_ctr_message_box_event(self):
        inputVal = self._getEventParam('ConfigPowerOffForm_ctr_message_box', 'val')
        if str(inputVal).lower() == 'yes':
            self.flash.send('txt_status', 'setText', {
                'text': _('Stopping kiosk services ...') })
            os.system('echo howcute121|sudo -S /etc/init.d/cron stop')
            os.system('echo howcute121|sudo -S pkill -f init.py')
            for service in self.services:
                os.system('pkill -f %s' % service)
            
            os.system('sync')
            self.flash.send('txt_status', 'setText', {
                'text': _('You can power off the machine now.') })
            while True:
                time.sleep(1)
        


