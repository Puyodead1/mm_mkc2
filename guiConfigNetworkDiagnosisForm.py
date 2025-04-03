# Source Generated with Decompyle++
# File: guiConfigNetworkDiagnosisForm.pyc (Python 2.5)

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
import subprocess
from mcommon import *
from guiBaseForms import ConfigForm
from config import KIOSK_HOME
log = initlog('ConfigNetworkDiagnosisForm')

class ConfigNetworkDiagnosisForm(ConfigForm):
    
    def __init__(self):
        ConfigForm.__init__(self)
        self.screenID = 'C7'
        self.preWindowID = 'AdminMainForm'
        self.uiErrorWindowID = 'AdminMainForm'
        self.timeoutSec = 60
        self.lstResponseCtrl += [
            'ConfigNetworkDiagnosisForm_ctr_message_box']

    
    def _initComponents(self):
        ConfigForm._initComponents(self)
        self.flash.send('txt_status', 'setText', {
            'text': '' })
        msg = _('Perform network diagnosis?')
        self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
            'message': msg,
            'type': 'confirm' })

    
    def on_ConfigNetworkDiagnosisForm_ctr_message_box_event(self):
        inputVal = self._getEventParam('ConfigNetworkDiagnosisForm_ctr_message_box', 'val')
        if str(inputVal).lower() == 'yes':
            self.flash.send('txt_status', 'setText', {
                'text': _('Network Diagnosing, please wait.') })
            cmd = os.path.join(KIOSK_HOME, 'kiosk/utilities/connectionChecker.py')
            p1 = subprocess.Popen([
                'echo',
                'howcute121'], stdout = subprocess.PIPE)
            p2 = subprocess.Popen('sudo -S %s' % cmd, stdin = p1.stdout, stdout = subprocess.PIPE, shell = True)
            output = p2.communicate()[0]
            self.flash.send('txt_status', 'setText', {
                'text': output })
        


