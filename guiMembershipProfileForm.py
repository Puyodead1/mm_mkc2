# Source Generated with Decompyle++
# File: guiMembershipProfileForm.pyc (Python 2.5)

'''
Created on 2010-7-9
@author: andrew.lu@cereson.com
'''
from mcommon import *
from guiBaseForms import CustomerForm
log = initlog('MembershipProfileForm')

class MembershipProfileForm(CustomerForm):
    
    def __init__(self):
        super(MembershipProfileForm, self).__init__()
        self.screenID = 'M7'
        self.preWindowID = 'MembershipCenterForm'
        self.uiErrorWindowID = 'MainForm'
        self.timeoutSec = 180
        self.lstResponseCtrl.extend([
            'btn_back',
            'btn_password',
            'MembershipProfileForm_ctr_all_keyboard'])

    
    def _initComponents(self):
        super(MembershipProfileForm, self)._initComponents()
        if globalSession.loginCustomer.ccNum:
            num = globalSession.loginCustomer.ccNum
        else:
            num = globalSession.loginCustomer.primaryCcNumber
        self.flash.send('card_number', 'setText', {
            'text': maskCard(num) })
        self.flash.send('email', 'setText', {
            'text': globalSession.loginCustomer.email })
        self.flash.send('txt_msg', 'setText', {
            'text': '' })
        self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'hide', { })

    
    def on_btn_back_event(self):
        self.on_back()

    
    def on_btn_password_event(self):
        self.flash.send('txt_msg', 'setText', {
            'text': _('Please enter your current password.') })
        self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', {
            'type': 'password' })
        self.state = 'old'
        self.old = ''
        self.new = ''
        self.confirm = ''

    
    def on_MembershipProfileForm_ctr_all_keyboard_event(self):
        eventType = self._getEventParam('MembershipProfileForm_ctr_all_keyboard', 'type')
        if eventType == 'click':
            pass
        elif eventType == 'ok':
            password = self._getEventParam('MembershipProfileForm_ctr_all_keyboard', 'val')
            if self.state == 'old':
                self.old = password
                self.flash.send('txt_msg', 'setText', {
                    'text': _('Please enter your new password.') })
                self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', {
                    'type': 'password' })
                self.state = 'new'
            elif self.state == 'new':
                if len(password) < 6:
                    self.flash.send('txt_msg', 'setText', {
                        'text': _('New password must have at least 6 characters.') })
                    self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', {
                        'type': 'password' })
                else:
                    self.new = password
                    self.flash.send('txt_msg', 'setText', {
                        'text': _('Please confirm your new password.') })
                    self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', {
                        'type': 'password' })
                    self.state = 'confirm'
            elif self.state == 'confirm':
                if password == self.new:
                    self.confirm = password
                    ret = self.umsProxy.changeMemberPasswdForKiosk(globalSession.loginCustomer, self.old, self.new)
                    if ret == '0':
                        self.flash.send('txt_msg', 'setText', {
                            'text': _('Your password is changed successfully.') })
                    elif ret == '1':
                        self.flash.send('txt_msg', 'setText', {
                            'text': _('The password you gave is incorrect.') })
                    elif ret == '2':
                        self.flash.send('txt_msg', 'setText', {
                            'text': _('New password must have at least 6 characters.') })
                    elif ret == '3':
                        self.flash.send('txt_msg', 'setText', {
                            'text': _('Communication error, please retry.') })
                    
                else:
                    self.flash.send('txt_msg', 'setText', {
                        'text': _('Passwords do not match.') })
                self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'hide', { })
            
        


