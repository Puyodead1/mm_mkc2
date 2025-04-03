# Source Generated with Decompyle++
# File: guiPickUpResultForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiPickUpResultForm.py
Pick Up Result
Screen ID: P4

Change Log:

'''
import datetime
import time
import config
from mcommon import *
from guiBaseForms import CustomerForm
log = initlog('guiPickUpResultForm')

class PickUpResultForm(CustomerForm):
    
    def __init__(self):
        super(PickUpResultForm, self).__init__()
        self.screenID = 'P4'
        self.timeoutSec = 60
        self.preWindowID = 'MainForm'
        self.lstResponseCtrl.extend([
            'btn_finish'])

    
    def _initComponents(self):
        super(PickUpResultForm, self)._initComponents()
        self.pickupCart = globalSession.pickupCart
        globalSession.pickupCart = ShoppingCart()
        ms_msg = ''
        
        try:
            for disc in self.pickupCart._ejectedDiscs:
                if disc.msExpiTime:
                    xmsg = _('Monthly subscription activated, please return these discs before %(time)s.')
                    tt = datetime.datetime(*time.strptime(disc.msExpiTime, '%Y-%m-%d %H:%M:%S')[:6]).strftime('%H:00 on %b %d, %Y')
                    pm = {
                        'time': tt }
                    ms_msg = xmsg % pm
                    break
                
        except:
            msg = traceback.format_exc()
            log.error(msg)
            self.connProxy.emailAlert('PRIVATE', msg, 'andrew.lu@cereson.com', critical = self.connProxy.UNCRITICAL)

        total = self.pickupCart.getEjectedDiscsSize()
        msg = _('Your transaction is done.')
        if ms_msg and total > 0:
            msg += '\n%s\n' % ms_msg
        
        if globalSession.param.get('eject_result'):
            msg += globalSession.param.get('eject_result')
        
        self.flash.send('txtbox_msg', 'setText', {
            'text': msg })
        self.flash.send('txt_taken', 'setText', {
            'text': str(self.pickupCart.getEjectedDiscsSize()) })

    
    def on_btn_finish_event(self):
        self.on_cancel()


