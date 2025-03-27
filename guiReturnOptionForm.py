# Source Generated with Decompyle++
# File: guiReturnOptionForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2009-04-17 Vincent
vincent.chen@cereson.com

Filename: guiReturnOptionForm.py
Screen ID: T3

Change Log:
'''
import os
import traceback
from mcommon import *
from guiBaseForms import UserForm
log = initlog('guiReturnOptionForm')

class ReturnOptionForm(UserForm):
    
    def __init__(self):
        super(ReturnOptionForm, self).__init__()
        self.screenID = 'T3'
        self.preWindowID = 'ReturnTakeInForm'
        self.timeoutSec = 60
        self.lstResponseCtrl.extend([
            'btn_try_again',
            'btn_by_card',
            'btn_by_code',
            'btn_cancel',
            'ReturnOptionForm_ctr_num_keyboard',
            'ReturnOptionForm_ctr_message_box'])

    
    def _initComponents(self):
        super(ReturnOptionForm, self)._initComponents()
        self._setReturnOptions()
        self.flash.send('btn_try_again', 'show', { })
        msg = _('Invalid disc.')
        self.flash.send('txt_msg', 'setText', {
            'text': msg })
        self.flash.send('txt_msg', 'show', { })
        self.flash.send('ReturnOptionForm_ctr_num_keyboard', 'hide', { })

    
    def _setReturnOptions(self):
        self.returnOptions = self.connProxy._getConfigByKey('return_options')
        log.info('Value of return_options %s' % self.returnOptions)
        self.flash.send('txt_return_option', 'hide', { })
        self.flash.send('btn_by_card', 'hide', { })
        self.flash.send('btn_by_code', 'hide', { })
        "\n        'Disc Only' ( value 'disc')\n        'Disc & Card' (value 'card')\n        'Disc & Code' (value 'code')\n        'Disc & Card & Code' (value 'cardcode')\n        "
        if self.returnOptions == 'disc':
            self.flash.send('txt_return_option', 'hide', { })
            self.flash.send('btn_by_card', 'hide', { })
            self.flash.send('btn_by_code', 'hide', { })
        else:
            self.flash.send('txt_return_option', 'show', { })
            if self.returnOptions.find('card') > -1:
                self.flash.send('btn_by_card', 'show', { })
            
            if self.returnOptions.find('code') > -1:
                self.flash.send('btn_by_code', 'show', { })
            

    
    def on_btn_by_code_event(self):
        self.flash.send('ReturnOptionForm_ctr_num_keyboard', 'show', { })
        msg = _('Please input the last 4 digits of the credit card you used to rent the disc.')
        self.flash.send('txt_msg', 'setText', {
            'text': msg })
        self.flash.send('txt_return_option', 'hide', { })
        self.flash.send('btn_by_card', 'hide', { })
        self.flash.send('btn_by_code', 'hide', { })
        self.flash.send('btn_try_again', 'hide', { })

    
    def on_btn_by_card_event(self):
        self.nextWindowID = 'ReturnSwipeCardForm'
        self.windowJump = True

    
    def on_btn_cancel_event(self):
        self.nextWindowID = 'ReturnTakeInForm'
        self.windowJump = True

    
    def on_btn_try_again_event(self):
        globalSession.param['need_eject'] = True
        self.nextWindowID = 'ReturnTakeInForm'
        self.windowJump = True

    
    def on_ReturnOptionForm_ctr_num_keyboard_event(self):
        eventType = self._getEventParam('ReturnOptionForm_ctr_num_keyboard', 'type')
        if eventType == 'click':
            pass
        elif eventType == 'ok':
            code = self._getEventParam('ReturnOptionForm_ctr_num_keyboard', 'val')
            lstDiscs = self.connProxy.getOutDiscsByCode(code)
            if len(lstDiscs) == 0:
                msg = _('No discs found rented by this card.')
                self.flash.send('ReturnOptionForm_ctr_message_box', 'show', {
                    'message': msg,
                    'type': 'alert' })
            elif len(lstDiscs) == 1:
                globalSession.disc = lstDiscs[0]
                globalSession.param['return_option'] = 'code'
                self.nextWindowID = 'ReturnTakeInForm'
                self.windowJump = True
            else:
                globalSession.param['disc_list'] = lstDiscs
                self.nextWindowID = 'ReturnDiscListForm'
                self.windowJump = True
        

    
    def on_ReturnOptionForm_ctr_message_box_event(self):
        self.nextWindowID = 'ReturnOptionForm'
        self.windowJump = True


