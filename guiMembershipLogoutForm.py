# Source Generated with Decompyle++
# File: guiMembershipLogoutForm.pyc (Python 2.5)

'''
Created on 2010-8-17
@author: andrew.lu@cereson.com
'''
from mcommon import *
from guiBaseForms import UserForm
log = initlog('MembershipLogoutForm')

class MembershipLogoutForm(UserForm):
    
    def __init__(self):
        super(MembershipLogoutForm, self).__init__()
        self.screenID = 'x0'
        self.timeoutSec = 60
        self.lstResponseCtrl.extend([
            'btn_yes',
            'btn_no'])

    
    def _initComponents(self):
        super(MembershipLogoutForm, self)._initComponents()
        self.preWindowID = globalSession.param['preWindowID']
        msg = _('Are you sure you want to logout?')
        self.flash.send('txt_msg', 'setText', {
            'text': msg })

    
    def on_btn_yes_event(self):
        self.nextWindowID = 'MainForm'
        self.windowJump = True

    
    def on_btn_no_event(self):
        self.nextWindowID = globalSession.param['preWindowID']
        self.windowJump = True


