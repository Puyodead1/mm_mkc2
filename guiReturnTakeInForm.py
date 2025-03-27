# Source Generated with Decompyle++
# File: guiReturnTakeInForm.pyc (Python 2.5)

"""

MovieMate Kiosk Core V0.4
CopyRight MovieMate, Inc.

Created 2008-11-19 Vincent
vincent.chen@cereson.com

Filename:guiReturnTakeInForm.py

Change Log:
    Vincent 2009-05-04 Add grace period message
    Vincent 2009-03-30 Change this form's timeout from 10 sec to 20
    2011-02-10  Kitch
        add statusCode 13 to checkRfidAndSaveTrs

"""
from guiBaseTakeInForm import BaseTakeInForm
from mobject import *
from mcommon import *
log = initlog('guiReturnTakeInForm')

class ReturnTakeInForm(BaseTakeInForm):
    
    def __init__(self):
        BaseTakeInForm.__init__(self)
        self.nextWindowID = 'ReturnResultForm'
        self.preWindowID = 'MainForm'
        self.resultForm = 'ReturnResultForm'
        self.ejectDiscBackForm = 'ReturnResultForm'
        self.screenID = 'T1'
        self.timeoutSec = 20
        self.lstResponseCtrl.extend([
            'ReturnTakeInForm_ctr_message_box'])

    
    def _saveStatus(self):
        self.connProxy.saveReturnStatus(self.returnType, self.disc)
        if globalSession.param.get('return_option') == 'code' or globalSession.param.get('return_option') == 'card':
            self.connProxy.setBadRfid(self.disc.rfid)
            globalSession.param['return_option'] = ''
        

    
    def on_dberror(self):
        self._exchangeEject()

    
    def _guiVomitDisc(self):
        msg = N_('Your disc is returned and total charge: %(cur)s %(total).2f\nBut, we are unable to take in this disc, please close the disc case tight and try again.')
        pm = {
            'cur': globalSession.param['currency_symbol'],
            'total': float(self.disc.rentalPrice) }
        alert = KioskMessage(msg, pm)
        globalSession.param['return_msg'] = alert.i18nmsg
        self._setProcessText(msg)
        m = N_('A disc in slot %(slot)s is returned and total charge %(cur)s %(total).2f, but S250 is unable to take in it.')
        pm = {
            'slot': self.disc.slotID,
            'cur': globalSession.param['currency_symbol'],
            'total': float(self.disc.rentalPrice) }
        km = KioskMessage(m, pm)
        self.addAlert(WARNING, km.message)

    
    def on_invalidDisc(self, ex):
        if self.connProxy._getConfigByKey('return_options') == 'disc':
            msg = N_('Invalid Label\nPlease take the disc back.')
            self._setProcessText(msg)
            self._exchangeEject()
            globalSession.param['return_msg'] = msg
            self.nextWindowID = self.ejectDiscBackForm
        else:
            self.nextWindowID = 'ReturnOptionForm'
            self.windowJump = True

    
    def _retrieveFailRecovery(self, exin):
        self._vomitDisc()

    
    def _insertFailRecovery(self, exin):
        self._insertLoop()

    
    def _verifyDisc(self):
        
        try:
            cart = ShoppingCart()
            self.returnType = str(self.connProxy.checkRfidAndSaveTrs(self.disc, cart))
            log.info('Disc title:%s' % self.disc.title)
        except Exception:
            ex = None
            log.error('[%s] Conn Proxy _verifyDisc Error:\n%s' % (self.windowID, traceback.format_exc()))
            msg = N_('Operation failed, please retry in 5 minutes.')
            raise SaveStatusError(msg)

        log.info('[Return Type]: %s' % self.returnType)
        '\n        statusCode: \n        0: can not return (invalid)\n        1: can return (from this kiosk)\n        2: can return (from another kiosk)\n        3: can not return (no empty slots)\n        4: already existing (with open transaction)\n        5: already existing (without open transaction)\n        6: purchased disc (Buy-it-Now / Converted to sale already)\n        7: convert to sale right now (local)\n        8: convert to sale right now (remote)\n        9. return and load\n        10: disc remembered as unloaded\n        11: manually cleared\n        12: can not return (from another client)\n        13: can not return (250 & 500)\n\n        acceptable: 1, 2, 4, 5, 9\n        unacceptable: 0, 3, 6, 7, 8, 10, 11, 12\n        \n        Important Notice:\n        1. If a disc is returned remotely, but has been converted to "SALE" already\n           "0" will return: "Can not return this Disc."\n        2. checkRfidAndSaveTrs() will do:\n           "verify rfid"\n           "set transaction to pending"\n           "set slot state to in"\n        '
        couponMsg = ''
        if cart.coupon.couponCode and cart.couponUsed:
            couponMsg = _('. Coupon activated, other discs in the same shopping cart will be charged with discount accordingly')
        elif cart.coupon.couponCode and not (cart.couponUsed):
            couponMsg = _('. Coupon detected, please return other discs in the same shopping cart within 1 hour to activate the discount')
        
        if self.returnType == '1':
            msg = _('Total Charge: %(cur)s %(money).2f') % {
                'cur': globalSession.param['currency_symbol'],
                'money': float(self.disc.rentalPrice) }
            globalSession.param['return_msg'] = msg + couponMsg
        elif self.returnType == '2':
            msg = _('Total Charge: %(cur)s %(money).2f') % {
                'cur': globalSession.param['currency_symbol'],
                'money': float(self.disc.rentalPrice) }
            globalSession.param['return_msg'] = msg + couponMsg
        elif self.returnType == '3':
            msg = N_('Sorry, no empty slots found in this kiosk, please contact the operator, or return the disc to another kiosk belongs to the same owner.')
            raise WrongInRfidError(msg)
        elif self.returnType == '4':
            log.warning('RFID status invalid %s, with open trs' % self.disc.rfid)
            msg = _('Total Charge: %(cur)s %(money).2f') % {
                'cur': globalSession.param['currency_symbol'],
                'money': float(self.disc.rentalPrice) }
            globalSession.param['return_msg'] = msg + couponMsg
        elif self.returnType == '5':
            log.warning('RFID status invalid %s, without open trs' % self.disc.rfid)
            msg = _('The disc has been put back to slot %(slot)s') % {
                'slot': self.disc.slotID }
            globalSession.param['return_msg'] = msg + couponMsg
        elif self.returnType == '6':
            msg = N_('The Disc has been sold to you.\nPlease take it back.')
            raise WrongInRfidError(msg)
        elif self.returnType in ('7', '8'):
            msg = N_('The Disc has been sold to you.\nPlease take it back.')
            self._saveStatus()
            raise WrongInRfidError(msg)
        elif self.returnType == '9':
            log.warning('Open trs found, RFID not found for %s' % self.disc.rfid)
            msg = _('Total Charge: %(cur)s %(money).2f') % {
                'cur': globalSession.param['currency_symbol'],
                'money': float(self.disc.rentalPrice) }
            globalSession.param['return_msg'] = msg + couponMsg
        elif self.returnType == '10':
            log.warning('disc remembered as unloaded')
            msg = N_('Return failed.\nThe disc is not registered in this inventory. Please contact the owner/operator of this kiosk if you have any questions.')
            raise WrongInRfidError(msg)
        elif self.returnType == '11':
            log.warning('manually cleared')
            msg = N_('Return failed.\nThe disc is not registered in this inventory. Please contact the owner/operator of this kiosk if you have any questions.')
            raise WrongInRfidError(msg)
        elif self.returnType == '12':
            if self.disc.outAddress:
                msg = N_("This disc does not belong to this kiosk's owner.\nPlease Return this disc at %(addr)s.")
                raise WrongInRfidError(msg, {
                    'addr': self.disc.outAddress })
            else:
                msg = N_("This disc does not belong to this kiosk's owner.\n")
                raise WrongInRfidError(msg)
        elif self.returnType == '13':
            msg = N_('Return failed.\nThis disc is not recognized.')
            raise WrongInRfidError(msg)
        elif self.returnType == '0':
            msg = N_('Return failed.\nDisc Unrecognizable.')
            raise WrongInRfidError(msg)
        
        if self.disc.isGracePeriod:
            msg = _('Grace period activated, there is no charge.')
            globalSession.param['return_msg'] = msg
        
        if self.disc.msExpiTime:
            msg = _('Monthly subscription activated, there is no charge.')
            globalSession.param['return_msg'] = msg
        

    
    def _needRentalPurchase(self):
        (status, self.amount, trsId, ccId, accountId) = self.connProxy.checkRentalPurchaseConfirm(self.disc, int(self.returnType))
        if status == 0:
            return False
        
        if not (self.disc.releaseDate):
            self.movieProxy.getMovieDetailByUpc(self.disc)
        
        if str(self.movieProxy.allowRental(self.disc)) == '2':
            return False
        
        msg = _('Your rental fee of this disc is %(cur)s%(rental)s, would you like to pay %(cur)s%(money).2f more to buy it?') % {
            'rental': self.disc.rentalPrice,
            'cur': globalSession.param['currency_symbol'],
            'money': self.amount - float(self.disc.rentalPrice) }
        self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
            'message': msg,
            'type': 'confirm' })
        log.info("Wait customer's purchase choice.")
        while True:
            self.event = self.flash.get(timeout = self.timeoutSec)
            if self.event == None:
                continue
            
            if self.event:
                log.info('[UI Event]: %s.' % self.event)
            
            ctrlID = self.event.get('cid')
            if ctrlID == 'ReturnTakeInForm_ctr_message_box':
                if self._getEventParam('ReturnTakeInForm_ctr_message_box', 'val') == 'yes':
                    break
                else:
                    self.flash.send('%s_ctr_message_box' % self.windowID, 'hide', { })
                    return False
            elif ctrlID is None:
                self.flash.send('%s_ctr_message_box' % self.windowID, 'hide', { })
                return False
            
        self.flash.send('%s_ctr_message_box' % self.windowID, 'hide', { })
        (ret, msg) = self.upgProxy.saleForRentNBuyDisc(self.disc, accountId, ccId, self.amount)
        if ret == 0:
            msg = _('Total Charge: %(cur)s %(money).2f') % {
                'cur': globalSession.param['currency_symbol'],
                'money': self.amount }
            globalSession.param['return_msg'] = msg
            msg2 = _('You have bought the disc, please take your disc back.')
            self._setProcessText(msg2)
            return True
        elif ret == 1:
            msg = _('Transaction is declined by getway, the disc will return to kiosk.')
            self._setProcessText(msg)
            return False
        else:
            msg = _('Communication error, the disc will return to kiosk.')
            self._setProcessText(msg)
            return False

    
    def _doRentalPurchase(self):
        self.connProxy.saveRentalPurchaseStatus(self.disc, int(self.returnType), self.amount)
        self._exchangeEject()

    
    def _initComponents(self):
        self.cancelFrom = ''
        self.upgProxy = UPGProxy()
        if globalSession.param.get('need_eject'):
            msg = _('Please take your disc back and try again.')
            self._setProcessText(msg)
            self._exchangeEject()
            globalSession.param['need_eject'] = False
        
        BaseTakeInForm._initComponents(self)
        self.disc = globalSession.disc
        msg = _('To ensure a completed transaction: \nPlease close the dvd case completely before inserting.')
        self._setProcessText(msg)

    
    def _run(self):
        BaseTakeInForm._run(self)


