# Source Generated with Decompyle++
# File: guiRegisterMainForm.pyc (Python 2.5)

'''
Created on 2010-11-25
@author: andrew.lu@cereson.com
'''
from mcommon import *
from guiBaseForms import UserForm

class RegisterMainForm(UserForm):
    (ST_EMAIL, ST_PASSWD, ST_CONFIRM, ST_INVALID) = list(range(4))
    
    def __init__(self):
        super(RegisterMainForm, self).__init__()
        self.screenID = 'M10'
        self.timeoutSec = 60
        self.preWindowID = 'MainForm'
        self.lstResponseCtrl.extend([
            'RegisterMainForm_ctr_message_box',
            'RegisterMainForm_ctr_all_keyboard',
            'btn_cancel'])

    
    def _initComponents(self):
        super(RegisterMainForm, self)._initComponents()
        self.customer = globalSession.customer
        self._state = self.ST_EMAIL
        msg = _('Please enter your email address.')
        self.flash.send('txtbox_msg', 'setText', {
            'text': msg })
        msg = _('Please register your new membership card for security reason. A membership account will be set up and binded automatically.')
        self.flash.send('info_msg', 'setText', {
            'text': msg })
        self.flash.send('%s_ctr_message_box' % self.windowID, 'close', { })
        self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', {
            'type': 'email' })

    
    def on_btn_cancel_event(self):
        self.nextWindowID = 'MainForm'
        self.windowJump = True

    
    def _isEmailValidate(self):
        self.umsProxy.checkEmailForCerePay(self.customer)

    
    def on_RegisterMainForm_ctr_message_box_event(self):
        if self._getEventParam('RegisterMainForm_ctr_message_box', 'val') == 'yes':
            if self._state == self.ST_EMAIL:
                msg = _('Please enter your email address.')
                self.flash.send('txtbox_msg', 'setText', {
                    'text': msg })
                self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', {
                    'type': 'email' })
            elif self._state == self.ST_PASSWD:
                self._state = self.ST_PASSWD
                self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', {
                    'type': 'password' })
            elif self._state == self.ST_CONFIRM:
                self._state = self.ST_PASSWD
                msg = _('Please enter your password. Use 6 to 20 characters.')
                self.flash.send('txtbox_msg', 'setText', {
                    'text': msg })
                self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', {
                    'type': 'password' })
            
        

    
    def on_RegisterMainForm_ctr_all_keyboard_event(self):
        eventType = self._getEventParam('RegisterMainForm_ctr_all_keyboard', 'type')
        if eventType == 'click':
            pass
        elif eventType == 'ok':
            inputVal = self._getEventParam('RegisterMainForm_ctr_all_keyboard', 'val')
            if self._state == self.ST_EMAIL:
                self.customer.email = inputVal
                status = self.umsProxy.checkEmailForCerePay(self.customer)
                log.info('checkEmailForCerePay return %d' % status)
                if status == 0:
                    self._state = self.ST_PASSWD
                    msg = _('Please enter your password. Use 6 to 20 characters.')
                    self.flash.send('txtbox_msg', 'setText', {
                        'text': msg })
                    self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', {
                        'type': 'password' })
                elif status == 2:
                    msg = _('Sorry, the kiosk has communication issue, Please retry.')
                elif status in (3, 4):
                    msg = _('Invalid membership card, please contact with the card offers.')
                elif status in (5, 6):
                    msg = _('The email address already exists.')
                elif status == 7:
                    msg = _('Invalid email address.')
                else:
                    msg = _('unknown error.')
                if status > 0:
                    self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                        'message': msg,
                        'type': 'alert' })
                
            elif self._state == self.ST_PASSWD:
                x = len(inputVal)
                if x < 6 or x > 20:
                    alert = _('Please use 6 to 20 characters.')
                    self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                        'message': alert,
                        'type': 'alert' })
                else:
                    self.password = inputVal
                    self._state = self.ST_CONFIRM
                    msg = _('Please re-enter your password.')
                    self.flash.send('txtbox_msg', 'setText', {
                        'text': msg })
                    self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', {
                        'type': 'password' })
            elif self._state == self.ST_CONFIRM:
                if self.password != inputVal:
                    msg = _('The password does not match.')
                    self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                        'message': msg,
                        'type': 'alert' })
                else:
                    status = self.umsProxy.registerCerePayCard(self.customer, self.password)
                    log.info('registerCerePayCard return %d' % status)
                    if status == 0:
                        self.customer.isLogin = True
                        globalSession.loginCustomer = self.customer
                        self.nextWindowID = 'RegisterResultForm'
                        self.windowJump = True
                    elif status == 2:
                        msg = _('Sorry, the kiosk has communication issue, Please retry.')
                    elif status in (3, 4):
                        msg = _('Invalid membership card, please contact with the card offers.')
                    elif status == 5:
                        msg = N_('This card is not a membership card.')
                    elif status == 6:
                        msg = N_('This card is reported missing.')
                    elif status == 7:
                        msg = N_('This card is registered.')
                    elif status == 8:
                        msg = _('invalid email address')
                    elif status == 9:
                        msg = _('invalid password')
                    else:
                        msg = _('unknown error.')
                    if status > 0:
                        self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                            'message': msg,
                            'type': 'alert' })
                    
            
        

    
    def on_hide(self):
        super(RegisterMainForm, self).on_hide()
        self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'hide', { })


