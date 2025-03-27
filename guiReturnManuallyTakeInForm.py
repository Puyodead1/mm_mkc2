# Source Generated with Decompyle++
# File: guiReturnManuallyTakeInForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V1.0.012
CopyRight MovieMate, Inc.

Created 2012-02-17 Tim
tim.guo@cereson.com

Filename:guiReturnManuallyTakeInForm.py

Change Log:
'''
import time
import copy
import traceback

try:
    from sqlite3 import OperationalError
except:
    from pysqlite2.dbapi2 import OperationalError

from guiRobotForm import RobotForm
from mcommon import initlog, globalSession, N_, SaveStatusError, WrongInRfidError, ERROR, getPicFullPath
from mobject import Disc, ShoppingCart, InsertException, RetrieveExchangeException, InvalidDiscException, FatalError, KioskMessage
from control import ROBOT_CANCELED, ROBOT_OK, ROBOT_TIMEOUT, ROBOT_RFID_READ_ERROR, ROBOT_INVALID_RFID, ROBOT_INVALID_LABEL
from proxy.tools import getTimeChange, fmtMoney
log = initlog('guiReturnManuallyTakeInForm')
(NO_DISC_OUT, CONFIRM_RETURN, SUBMIT_CLICK) = list(range(3))

class ReturnManuallyTakeInForm(RobotForm):
    
    def __init__(self):
        RobotForm.__init__(self)
        self.screenID = 'T5'
        self.preWindowID = 'AdminMainForm'
        self.nextWindowID = 'AdminMainForm'
        self.timeoutSec = 60
        self.lstResponseCtrl = [
            'btn_submit',
            'btn_cancel',
            'radio_by_amount',
            'radio_by_day',
            'ReturnManuallyTakeInForm_ctr_num_keyboard',
            'ReturnManuallyTakeInForm_ctr_message_box',
            'disc_out_list']

    
    def _initComponents(self):
        RobotForm._initComponents(self)
        msg = _('Please close the dvd case completely before inserting.')
        self._setProcessText(msg)
        self.disc = Disc()
        self._show_charge_options = True
        self._submit_click = True
        self.flash.send('txtbox_msg', 'show', { })
        self.flash.send('btn_cancel', 'show', { })
        self.flash.send('btn_submit', 'hide', { })
        self.flash.send('swf_insert', 'show', { })
        self.flash.send('swf_send_disc', 'hide', { })
        self.flash.send('swf_vomit_dvd', 'hide', { })
        self.flash.send('disc_out_list', 'hide', { })
        self.flash.send('ctr_movie_detail', 'clearDetail', { })
        self._cache_event_data = {
            'day': 0,
            'day_amount': fmtMoney(0),
            'day_in_time': self.disc.outTime,
            'amount': fmtMoney(0),
            'amount_in_time': self.disc.outTime }
        self._return_type = ''
        self.flag = NO_DISC_OUT
        self._show_select_list = 0

    
    def _on_timeout(self):
        while True:
            self.event = self.flash.get(timeout = None)
            if self.event == None:
                continue
            
            if self.event:
                log.info('[UI Event]: %s.' % self.event)
            
            ctrlID = self.event.get('cid')
            self.on_event(ctrlID)
            if self.windowJump:
                break
            

    
    def _run(self):
        '''
        '''
        
        try:
            retFromRobot = None
            tick = time.time()
            r = self.robot.doCmdAsync('suck_disc', { }, self.timeoutSec)
            self.cancelFrom = ''
            while time.time() - tick < self.timeoutSec:
                retFromRobot = self.robot.getResult(r)
                if retFromRobot:
                    log.info('[Robot Event]: %s' % retFromRobot)
                    break
                
                eventFromFlash = self.flash.get(self.windowID, 0.1)
                if eventFromFlash:
                    if eventFromFlash.get('cid') == 'btn_cancel':
                        log.info('[%s] - Cancel Button Clicked.' % self.windowID)
                        retFromRobot = None
                        self.cancelFrom = 'user'
                        break
                    
                
            if not retFromRobot:
                self._cancel(r)
            else:
                self.flash.send('btn_cancel', 'hide', { })
                self.flash.send('btn_submit', 'hide', { })
                self._compareRfid(retFromRobot)
                if self._show_select_list:
                    self.flash.send('btn_cancel', 'show', { })
                    self._display_out_discs()
                    self._on_timeout()
                else:
                    self._verifyDisc()
                    if self._show_charge_options:
                        self.on_radio_by_amount_event()
                        self.on_radio_by_day_event()
                        self._submit_click = False
                        self._gui_show_charge_options()
                        self._on_timeout()
                    else:
                        self._ex_to_slot()
        except WrongInRfidError:
            ex = None
            log.error('[%s] - %s' % (self.windowID, ex))
            self.on_wrongInRfid(ex)
        except SaveStatusError:
            ex = None
            msg = _('Operation failed, the disc is ejecting back ...\nPlease retry in 5 minutes.')
            self._setProcessText(msg)
            self.on_dberror()
            self.connProxy.emailAlert('PRIVATE', ex.message, critical = self.connProxy.UNCRITICAL)
        except OperationalError:
            ex = None
            msg = _('Operation failed, the disc is ejecting back ...\nPlease retry in 5 minutes.')
            self._setProcessText(msg)
            self.on_dberror()
            self.connProxy.emailAlert('PRIVATE', ex.message, critical = self.connProxy.UNCRITICAL)
        except InvalidDiscException:
            ex = None
            self.on_invalidDisc(ex)
        except FatalError:
            ex = None
            self.addAlert(ERROR, ex.message)
            raise 
        except Exception:
            ex = None
            raise 
        


    
    def _display_out_discs(self):
        '''
        data = [{"feature":[{"name":"sk"},{"time":"2012"},{"aa":"a"}],"movie_pic":"/home/mm/var/images/goodsrec/images/735.jpg","is_bluray":"2", "rfid":"001FBE2730000104E0"},
                {"feature":[{"name":"sj"},{"time":"2015"},{"aa":"f"},{"sk":"twj"}],"movie_pic":"/home/mm/var/images/goodsrec/images/740.jpg","is_bluray":"2", "rfid":"001FBE2730000104E0"}]
        '''
        out_discs = self.connProxy.getOutDiscsByCode('')
        data = []
        if out_discs:
            for d in out_discs:
                disc = { }
                disc['rfid'] = d.rfid
                disc['movie_pic'] = getPicFullPath(d.picture)
                disc['upc'] = d.upc
                disc['feature'] = []
                disc['feature'].append({
                    _('Title'): d.title })
                disc['feature'].append({
                    _('Rental Time'): d.outTime })
                disc['feature'].append({
                    _('CC Name'): d.cc_display })
                data.append(disc)
            
            self.flash.send('disc_out_list', 'setDiscList', {
                'discs': data })
            self.flash.send('disc_out_list', 'show', { })
            self.flash.send('txtbox_msg', 'show', { })
            self.flash.send('swf_insert', 'hide', { })
            msg = _('The RFID is damaged. Please select the disc from the list.')
            self._setProcessText(msg)
        else:
            self.return_no_disc_out = 1
            msg = _('No disc out.')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'alert' })

    
    def on_disc_out_list_event(self):
        self.disc.rfid = self._getEventParam('disc_out_list', 'rfid')
        self.disc.upc = self._getEventParam('disc_out_list', 'upc')
        if self.disc.upc:
            self.flag = CONFIRM_RETURN
            msg = _('Would you like to return this disc?')
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'confirm' })
        

    
    def on_ReturnManuallyTakeInForm_ctr_message_box_event(self):
        if self._getEventParam('ReturnManuallyTakeInForm_ctr_message_box', 'val') == 'yes':
            if self.flag == NO_DISC_OUT:
                self.flash.send('swf_insert', 'hide', { })
                self.flash.send('swf_vomit_dvd', 'show', { })
                msg = _('The disc is ejecting back ...\nPlease take the disc.')
                self._setProcessText(msg)
                self.robot.exchange_eject2()
                self.nextWindowID = self.preWindowID
                self.windowJump = True
                log.info('Goto %s ========================' % self.nextWindowID)
            elif self.flag == CONFIRM_RETURN:
                self.flash.send('disc_out_list', 'hide', { })
                
                try:
                    self._verifyDisc()
                except WrongInRfidError:
                    ex = None
                    log.error('[%s] - %s' % (self.windowID, ex))
                    self.on_wrongInRfid(ex)
                except SaveStatusError:
                    ex = None
                    msg = _('Operation failed, the disc is ejecting back ...\nPlease retry in 5 minutes.')
                    self._setProcessText(msg)
                    self.on_dberror()
                    self.connProxy.emailAlert('PRIVATE', ex.message, critical = self.connProxy.UNCRITICAL)

                self.on_radio_by_amount_event()
                self.on_radio_by_day_event()
                self._submit_click = False
                self._gui_show_charge_options()
                self._on_timeout()
            elif self.flag == SUBMIT_CLICK and not (self._submit_click):
                self.flash.send('txtbox_msg', 'show', { })
                self.flash.send('ctr_movie_detail', 'clearDetail', { })
                self.flash.send('swf_insert', 'hide', { })
                self.flash.send('swf_vomit_dvd', 'show', { })
                self.connProxy.save_rental_movie_out_status(self.disc, self.returnType)
                if self._show_select_list:
                    self.flash.send('btn_sumit', 'hide', { })
                    msg = N_('The transaction is completed.\n \n Please take back the disc and re-load the disc once paste a new RFID.')
                    km = KioskMessage(msg, { })
                    self._setProcessText(km.i18nmsg)
                    self.robot.exchange_eject2()
                    self.connProxy.saveUnloadStatus(self.disc)
                else:
                    self._ex_to_slot()
                    if self.returnType in ('2', '7', '8', '9'):
                        self.connProxy.getDefaultSettings(self.disc)
                        if not (self.disc.movieID):
                            self.movieProxy.getMovieDetailByUpc(self.disc)
                        
                        self.connProxy.saveReturnStatus('2', self.disc)
                    
                    self._submit_click = True
                self.windowJump = True
                log.info('Goto %s ========================' % self.nextWindowID)
            
        

    
    def _submit(self):
        if not (self._submit_click):
            self.flag = SUBMIT_CLICK
            msg = _('The customer will be charged %(cur)s %(money)s, please confirm.' % {
                'cur': globalSession.param['currency_symbol'],
                'money': self.disc.rentalPrice })
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'confirm' })
        

    
    def on_btn_submit_event(self):
        self._submit()

    
    def _gui_day(self):
        self.flash.send('day', 'setText', {
            'text': str(self._cache_event_data['day']) })
        msg = _('(Amount: %(cur)s %(money)s)') % {
            'cur': globalSession.param['currency_symbol'],
            'money': self._cache_event_data['day_amount'] }
        self.flash.send('day_msg', 'setText', {
            'text': msg })

    
    def _gui_amount(self):
        log.info('amount: %s' % self._cache_event_data['amount'])
        self.flash.send('amount', 'setText', {
            'text': str(self._cache_event_data['amount']) })

    
    def on_radio_by_day_event(self):
        ''' set the day and amount
        '''
        self._return_type = 'day'
        self.disc.rentalPrice = self._cache_event_data['day_amount']
        self.disc.inTime = self._cache_event_data['day_in_time']
        self._gui_day()

    
    def on_ReturnManuallyTakeInForm_ctr_num_keyboard_event(self):
        '''
        '''
        if self._getEventParam('ReturnManuallyTakeInForm_ctr_num_keyboard', 'type') == 'ok':
            val = self._getEventParam('ReturnManuallyTakeInForm_ctr_num_keyboard', 'val')
            log.info('return type: %s' % self._return_type)
            if self._return_type == 'day':
                
                try:
                    day = int(val)
                except:
                    day = self._cache_event_data['day']

                self.disc.inTime = getTimeChange(self.disc.outTime, day = day)
                self.connProxy.calculate_price_without_coupon(self.disc)
                if float(self.disc.salePrice) < float(self.disc.rentalPrice):
                    self.disc.rentalPrice = self.disc.salePrice
                
                self.disc.rentalPrice = fmtMoney(self.disc.rentalPrice)
                self._cache_event_data['day'] = day
                self._cache_event_data['day_amount'] = self.disc.rentalPrice
                self._cache_event_data['day_in_time'] = self.disc.inTime
                self._gui_day()
            elif self._return_type == 'amount':
                
                try:
                    amount = float(val)
                except:
                    amount = self._cache_event_data['amount']

                self.disc.inTime = getTimeChange(self.disc.outTime, second = 2)
                self.disc.rentalPrice = fmtMoney(amount)
                if float(self.disc.salePrice) < float(amount):
                    self.disc.rentalPrice = self.disc.salePrice
                
                self.disc.rentalPrice = fmtMoney(self.disc.rentalPrice)
                self._cache_event_data['amount'] = self.disc.rentalPrice
                self._cache_event_data['amount_in_time'] = self.disc.inTime
                self._gui_amount()
            else:
                log.info('invalid return type: %s' % self._return_type)
        

    
    def on_radio_by_amount_event(self):
        ''' set amount
        '''
        self._return_type = 'amount'
        self.disc.rentalPrice = self._cache_event_data['amount']
        self.disc.inTime = self._cache_event_data['amount_in_time']
        self._gui_amount()

    
    def _guiExchangeEject(self):
        self.flash.send('txtbox_msg', 'show', { })
        self.flash.send('swf_insert', 'hide', { })
        self.flash.send('swf_send_disc', 'hide', { })
        self.flash.send('swf_vomit_dvd', 'show', { })
        self.flash.send('btn_cancel', 'hide', { })
        self.flash.send('btn_submit', 'hide', { })
        self.flash.send('ctr_movie_detail', 'clearDetail', { })

    
    def _guiExchangeToRack(self):
        self.flash.send('txtbox_msg', 'show', { })
        self.flash.send('swf_insert', 'hide', { })
        self.flash.send('swf_send_disc', 'show', { })
        self.flash.send('swf_vomit_dvd', 'hide', { })
        self.flash.send('ctr_movie_detail', 'clearDetail', { })
        self.flash.send('btn_cancel', 'hide', { })
        self.flash.send('btn_submit', 'hide', { })

    
    def _compareRfid(self, retFromRobot):
        self._verifyRet(retFromRobot)
        errno = retFromRobot['errno']
        self.disc.rfid = retFromRobot.get('rfid')
        log.info('_compareRfid %s - %s %s' % (errno, self.disc.rfid, ROBOT_RFID_READ_ERROR))
        if errno == ROBOT_OK:
            pass
        elif errno == ROBOT_TIMEOUT:
            msg = N_('Security Tag Read Failed\nPlease take the disc back.')
            km = KioskMessage(msg, { })
            self.logEvent('warning', '', km.message, self.disc)
            raise WrongInRfidError(msg)
        elif errno == ROBOT_INVALID_RFID:
            msg = N_('Invalid Security Tag\nPlease take the disc back.')
            km = KioskMessage(msg, { })
            self.logEvent('warning', '', km.message, self.disc)
            raise InvalidDiscException(msg)
        elif errno == ROBOT_RFID_READ_ERROR:
            self._show_select_list = 1
        elif errno == ROBOT_INVALID_LABEL:
            msg = N_('Invalid Label\nPlease take the disc back.')
            km = KioskMessage(msg, { })
            self.logEvent('warning', '', km.message, self.disc)
            raise WrongInRfidError(msg)
        else:
            msg = N_('Invalid Disc: Unknown Error\nPlease take the disc back.')
            km = KioskMessage(msg, { })
            self.logEvent('warning', '', km.message, self.disc)
            raise WrongInRfidError(msg)

    
    def _verifyDisc(self):
        
        try:
            cart = ShoppingCart()
            self.returnType = str(self.connProxy.checkRfidAndSaveTrs(self.disc, cart))
        except Exception:
            ex = None
            log.error('[%s] Conn Proxy _verifyDisc Error:\n%s' % (self.windowID, traceback.format_exc()))
            msg = N_('Operation failed, please retry in 5 minutes.')
            raise SaveStatusError(msg)

        self._cache_event_data['day_in_time'] = self.disc.outTime
        self._cache_event_data['amount_in_time'] = self.disc.outTime
        log.info('[Return Type]: %s' % self.returnType)
        '\n        statusCode: \n        0: can not return (invalid)\n        1: can return (from this kiosk)\n        2: can return (from another kiosk)\n        3: can not return (no empty slots)\n        4: already existing (with open transaction)\n        5: already existing (without open transaction)\n        6: purchased disc (Buy-it-Now / Converted to sale already)\n        7: convert to sale right now (local)\n        8: convert to sale right now (remote)\n        9: return and load\n        10: disc remembered as unloaded\n        11: manually cleared\n        12: can not return (from another client)\n        13: can not return (250 & 500)\n\n        acceptable: 1, 2, 4, 5, 7, 8, 9\n        unacceptable: 0, 3, 6, 10, 11, 12\n        \n        Important Notice:\n        1. If a disc is returned remotely, but has been converted to "SALE" already\n           "0" will return: "Can not return this Disc."\n        2. checkRfidAndSaveTrs() will do:\n           "verify rfid"\n           "set transaction to pending"\n           "set slot state to in"\n        '
        couponMsg = ''
        if self.returnType == '1':
            pass
        elif self.returnType == '2':
            pass
        elif self.returnType == '3':
            msg = N_('Sorry, no empty slots found in this kiosk, please contact the operator, or return the disc to another kiosk belongs to the same owner.')
            raise WrongInRfidError(msg)
        elif self.returnType == '4':
            pass
        elif self.returnType == '5':
            log.warning('RFID status invalid %s, without open trs' % self.disc.rfid)
            self._show_charge_options = False
        elif self.returnType == '6':
            msg = N_('The Disc has been sold to you.\nPlease take it back.')
            raise WrongInRfidError(msg)
        elif self.returnType in ('7', '8'):
            pass
        elif self.returnType == '9':
            log.warning('Open trs found, RFID not found for %s' % self.disc.rfid)
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
        

    
    def _gui_show_charge_options(self):
        '''
        '''
        self._guiCancel()
        self.flash.send('txtbox_msg', 'hide', { })
        self.flash.send('btn_cancel', 'hide', { })
        self.flash.send('btn_submit', 'show', { })
        self.flash.send('swf_insert', 'hide', { })
        self.flash.send('swf_send_disc', 'hide', { })
        self.flash.send('swf_vomit_dvd', 'hide', { })
        feature = [
            {
                'Title': self.disc.title },
            {
                'Rental Time': self.disc.outTime },
            {
                'Price Plan': self.disc.pricePlan },
            {
                'Rental Tax': self.disc.rentalTax },
            {
                'Sale Price': self.disc.salePrice }]
        self.movieProxy.getMovieDetailByUpc(self.disc)
        data = {
            'feature': feature,
            'is_bluray': self.disc.isBluray,
            'movie_pic': getPicFullPath(self.disc.picture) }
        self.flash.send('ctr_movie_detail', 'setMovieDetail', data)

    
    def on_btn_cancel_event(self):
        if self._show_select_list:
            self.cancelFrom = 'user'
            self.flash.send('disc_out_list', 'hide', { })
            self.flash.send('swf_vomit_dvd', 'show', { })
            self.robot.exchange_eject2()
            self.nextWindowID = self.preWindowID
            self.windowJump = True
            log.info('Goto %s ========================' % self.nextWindowID)
        

    
    def _cancel(self, r):
        self.robot.cancel()
        log.info('[Robot Cancel Called]')
        self._guiCancel()
        cancelTimeout = False
        while True:
            retFromRobot = self.robot.getResult(r, timeout = 600)
            if retFromRobot:
                log.info('[%s] canceled, return %s' % (self.windowID, retFromRobot))
                if retFromRobot['errno'] != ROBOT_CANCELED:
                    
                    try:
                        self._exchangeEject()
                    except Exception:
                        ex = None
                        log.error('exchangeEject failed: %s' % str(ex))

                
                break
            
            if cancelTimeout == False:
                cancelTimeout = True
                m = N_('Cancel Time Out, \nPlease take out everything in the exchange box and retry')
                pm = { }
                msg = KioskMessage(m, pm)
                log.warning(msg.message)
                self._setProcessText(msg.i18nmsg)
            
        self.nextWindowID = self.preWindowID
        self.windowJump = True
        log.info('Goto %s ========================' % self.nextWindowID)

    
    def _guiCancel(self):
        self.flash.send('btn_cancel', 'hide', { })
        self.flash.send('btn_submit', 'hide', { })
        self.flash.send('ctr_movie_detail', 'clearDetail', { })
        msg = _('Operation Canceled.')
        if not (self.cancelFrom):
            msg = _('Timeout. Operation Canceled.')
        
        self._setProcessText(msg)

    
    def on_hide(self):
        self._submit()

    
    def on_wrongInRfid(self, ex):
        self._setProcessText(ex.i18nmsg)
        self._exchangeEject()

    
    def on_dberror(self):
        self._exchangeEject()

    
    def on_invalidDisc(self, ex):
        self.on_wrongInRfid(ex)

    
    def _insertFailRecovery(self, exin):
        self._insertLoop()

    
    def _retrieveFailRecovery(self, exin):
        self._vomitDisc()

    
    def _ex_to_slot(self):
        
        try:
            msg = _('Please Wait while the disk is checked and reloaded back into the inventory.')
            km = KioskMessage(msg, { })
            self._setProcessText(km.i18nmsg)
            self._exchangeToRack()
        except InsertException:
            ex = None
            log.error('_exchangeToRack: %s' % str(ex))
            self._insertFailRecovery(ex)
        except RetrieveExchangeException:
            ex = None
            log.error('_exchangeToRack: %s' % str(ex))
            self._retrieveFailRecovery(ex)



