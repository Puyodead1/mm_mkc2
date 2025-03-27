# Source Generated with Decompyle++
# File: guiRegisterResultForm.pyc (Python 2.5)

'''
Created on 2010-11-25
@author: andrew.lu@cereson.com
'''
from mcommon import *
from guiBaseForms import CustomerForm

class RegisterResultForm(CustomerForm):
    
    def __init__(self):
        super(RegisterResultForm, self).__init__()
        self.screenID = 'M10'
        self.preWindowID = 'MembershipCenterForm'
        self.uiErrorWindowID = 'MainForm'
        self.timeoutSec = 180
        self.lstResponseCtrl.extend([
            'btn_finish'])

    
    def _initComponents(self):
        super(RegisterResultForm, self)._initComponents()
        msg = _('Thank you for your registration.\n\nThe system will send two activate links to your email.\nPlease click on them to activate both of your cerepay and membership account for more service.\n\nEnjoy!')
        self.flash.send('txtbox_msg', 'setText', {
            'text': msg })

    
    def on_btn_finish_event(self):
        self.nextWindowID = 'MainForm'
        self.windowJump = True


