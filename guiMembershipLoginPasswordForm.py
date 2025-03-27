# Source Generated with Decompyle++
# File: guiMembershipLoginPasswordForm.pyc (Python 2.5)

'''
Created on 2010-7-8
@author: andrew.lu@cereson.com
'''
from mcommon import *
from guiBaseForms import UserForm
log = initlog('MembershipLoginPasswordForm')

class MembershipLoginPasswordForm(UserForm):
    
    def __init__(self):
        super(MembershipLoginPasswordForm, self).__init__()
        self.screenID = 'M2'
        self.preWindowID = 'MainForm'
        self.uiErrorWindowID = 'MainForm'
        self.nextWindowID = 'MembershipCenterForm'
        self.timeoutSec = 180
        self.lstResponseCtrl.extend([
            'btn_back',
            'btn_cancel',
            'btn_card',
            'MembershipLoginPasswordForm_ctr_all_keyboard',
            'MembershipLoginPasswordForm_ctr_message_box'])

    
    def _initComponents(self):
        super(MembershipLoginPasswordForm, self)._initComponents()
        msg = _('Please enter your email address.')
        self.flash.send('txtbox_msg', 'setText', {
            'text': msg })
        self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', { })
        self.state = 'email'
        option = self.connProxy._getConfigByKey('payment_options')
        if option in [
            'intecon',
            'chipnpin']:
            self.flash.send('btn_card', 'hide', { })
        else:
            self.flash.send('btn_card', 'show', { })

    
    def on_btn_back_event(self):
        self.on_back()

    
    def on_btn_cancel_event(self):
        self.on_cancel()

    
    def on_btn_card_event(self):
        self.nextWindowID = 'MembershipLoginSwipeCardForm'
        self.windowJump = True

    
    def on_MembershipLoginPasswordForm_ctr_message_box_event(self):
        if self._getEventParam('MembershipLoginPasswordForm_ctr_message_box', 'val') == 'yes':
            msg = _('Please enter your email address.')
            self.flash.send('txtbox_msg', 'setText', {
                'text': msg })
            self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', { })
            self.state = 'email'
        

    
    def on_MembershipLoginPasswordForm_ctr_all_keyboard_event(self):
        eventType = self._getEventParam('MembershipLoginPasswordForm_ctr_all_keyboard', 'type')
        if eventType == 'click':
            pass
        elif eventType == 'ok':
            if self.state == 'email':
                emailAddr = self._getEventParam('MembershipLoginPasswordForm_ctr_all_keyboard', 'val')
                if isValidEmail(emailAddr) == False:
                    self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', { })
                else:
                    globalSession.loginCustomer.email = emailAddr
                    msg = _('Please enter your password.')
                    self.flash.send('txtbox_msg', 'setText', {
                        'text': msg })
                    self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', {
                        'type': 'password' })
                    self.state = 'password'
            elif self.state == 'password':
                password = self._getEventParam('MembershipLoginPasswordForm_ctr_all_keyboard', 'val')
                ret = self.umsProxy.setMemberDetailByEmail(globalSession.loginCustomer, password)
                if ret == '0':
                    globalSession.loginCustomer.isLogin = True
                    self.nextWindowID = 'MembershipCenterForm'
                    self.windowJump = True
                    return None
                elif ret in [
                    '1',
                    '3',
                    '4',
                    '5']:
                    msg = _('The username or password you entered is incorrect.')
                elif ret == '2':
                    msg = _('Account not activated.')
                elif ret == '6':
                    msg = _('Communication error, please retry.')
                elif ret == '7':
                    msg = _('Internal error.')
                else:
                    msg = _('Unknown error.')
                self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                    'message': msg,
                    'type': 'alert' })
            else:
                log.error('Error MembershipLoginPasswordForm state')
        


