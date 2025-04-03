# Source Generated with Decompyle++
# File: guiDiscAvailableNoticeForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2009-09-02 Andrew
andrew.lu@cereson.com

Filename: guiDiscAvailableNoticeForm.py

Screen ID: R31

Change Log:

'''
from mcommon import *
from guiBaseForms import CustomerForm
log = initlog('guiAvailableNoticeForm')

class DiscAvailableNoticeForm(CustomerForm):
    
    def __init__(self):
        super(DiscAvailableNoticeForm, self).__init__()
        self.screenID = 'R31'
        self.preWindowID = 'DiscDetailForm'
        self.timeoutSec = 180
        self.lstResponseCtrl.extend([
            'btn_cancel',
            'btn_back',
            'btn_finish',
            'DiscAvailableNoticeForm_ctr_all_keyboard'])

    
    def _initComponents(self):
        super(DiscAvailableNoticeForm, self)._initComponents()
        self.disc = globalSession.disc
        release = self.movieProxy.allowRental(self.disc)
        if release == '1':
            self.comingsoon = True
        else:
            self.comingsoon = False
        if not (globalSession.notifyEmail):
            self._notifyStepOne()
        else:
            self._notifyStepTwo()

    
    def _notifyStepOne(self):
        if self.comingsoon == True:
            msg = _("The disc is coming soon, would you like to receive an email alert when it's available?\n")
        else:
            msg = _("The disc has currently been rented out, would you like to receive an email alert when it's returned?\n")
        msg += _('If you have already registered as our member, leave the same email address with your member account.')
        self.flash.send('txtbox_msg', 'setText', {
            'text': msg })
        self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', { })

    
    def _notifyStepTwo(self):
        msg = ''
        ret = self.umsProxy.getMemberInfoByMail(globalSession.notifyEmail)
        if ret:
            msg = _("Dear Member:\nThe disc has been added to your wish list, we will send you email alert when it's available.")
        else:
            msg = _("You will find the disc in your wish list after you complete the registration. we will send you email alert when it's available.")
        self.flash.send('txtbox_msg', 'setText', {
            'text': msg })
        self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'hide', { })
        self.umsProxy.addWannaSeeForKiosk(globalSession.notifyEmail, self.disc.upc)

    
    def on_DiscAvailableNoticeForm_ctr_all_keyboard_event(self):
        eventType = self._getEventParam('DiscAvailableNoticeForm_ctr_all_keyboard', 'type')
        if eventType == 'click':
            pass
        elif eventType == 'ok':
            emailAddr = self._getEventParam('DiscAvailableNoticeForm_ctr_all_keyboard', 'val')
            if isValidEmail(emailAddr) == False:
                self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', { })
            else:
                globalSession.notifyEmail = emailAddr
                self._notifyStepTwo()
        

    
    def on_btn_finish_event(self):
        self.nextWindowID = 'RentMainForm'
        self.windowJump = True

    
    def on_btn_back_event(self):
        self.on_back()

    
    def on_btn_cancel_event(self):
        self.on_cancel()


