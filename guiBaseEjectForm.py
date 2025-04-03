# Source Generated with Decompyle++
# File: guiBaseEjectForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V0.4
CopyRight MovieMate, Inc.

Created 2008-11-19 Vincent
vincent.chen@cereson.com

Filename:guiBaseEjectInForm.py

Change Log:
    2011-02-10  Kitch
        add statusCode 13 to checkRfidAndSaveTrs

'''
import os
import config
from mcommon import *
from guiRobotForm import RobotForm
import proxy.tools as ptools
from proxy.config import VIDEO_PATH
log = initlog('guiBaseEjectInForm')
(INVALID, TORETURN, TOLOAD, TOERROR) = list(range(4))

class BaseEjectForm(RobotForm):
    
    def __init__(self):
        RobotForm.__init__(self)
        self.resultForm = ''

    
    def _initComponents(self):
        RobotForm._initComponents(self)

    
    def _guiExchangeToRack(self):
        self.flash.send('swf_take_dvd', 'hide', { })
        self.flash.send('swf_vomit_dvd', 'hide', { })
        self.flash.send('swf_send_disc', 'show', { })

    
    def _guiRackToExchange(self):
        msg = _('Fetching the Disc From Slot ......')
        self._setProcessText(msg)
        self.flash.send('swf_take_dvd', 'show', { })
        self.flash.send('swf_vomit_dvd', 'hide', { })
        self.flash.send('swf_send_disc', 'hide', { })

    
    def _guiVomitDisc(self):
        msg = _('Please Take Your Disc.')
        self._setProcessText(msg)
        self.flash.send('swf_take_dvd', 'hide', { })
        self.flash.send('swf_vomit_dvd', 'show', { })
        self.flash.send('swf_send_disc', 'hide', { })

    
    def on_wrongOutRfid(self, ex):
        self.addAlert(WARNING, ex.message)
        self._setProcessText(ex.i18nmsg)
        
        try:
            self._exchangeToRack()
        except InsertException:
            self._insertLoop()

        self.connProxy.setBadRfid(self.disc.rfid)
        globalSession.param['eject_result'] += ex.i18nmsg + '\n'
        self.connProxy.emailAlert('PRIVATE', ex.message, critical = self.connProxy.UNCRITICAL)

    
    def on_invalidDiscException(self, ex):
        pm = {
            'slot_id': self.disc.slotID }
        self.rfidFailAlert(pm)
        self.on_wrongOutRfid(ex)

    
    def _getConflictRfidMsg(self, slotID, shouldBeSlotID):
        pass

    
    def dbSync(self):
        pass

    
    def _setBadDisc(self, rfid = None):
        if rfid:
            self.disc.rfid = rfid
        else:
            self.disc.rfid = str(time.time())
        self.disc.title = 'Unknown Title'
        self.disc.movieID = '0000'
        self.disc.upc = '0' * 12
        self.disc.genre = 'Unknown Genre'

    
    def _checkRfid(self):
        
        try:
            cart = ShoppingCart()
            self.returnType = str(self.connProxy.checkRfidAndSaveTrs(self.disc, cart))
            self.connProxy.loadRecoverRfidInfo(self.returnType, self.disc)
        except Exception:
            log.error('[%s] Conn Proxy _verifyDisc Error:\n%s' % (self.windowID, traceback.format_exc()))
            msg = N_('Conn proxy get Disc information from DB failed.')
            raise SaveStatusError(msg)

        log.info('[Return Type]: %s' % self.returnType)
        '\n        statusCode: \n        0: can not return (invalid)\n        1: can return (from this kiosk)\n        2: can return (from another kiosk)\n        3: can not return (no empty slots)\n        4: already existing (with open transaction)\n        5: already existing (without open transaction)\n        6: purchased disc (Buy-it-Now / Converted to sale already)\n        7: convert to sale right now (local)\n        8: convert to sale right now (remote)\n        9. return and load\n        10. disc remembered as unloaded\n        11: manually cleared\n        12: can not return (from another client)\n        13: can not return (250 & 500)\n\n        return: 1, 2, 4, 5, 9\n        load: 0, 6, 7, 8, 10, 11\n        exception: 3, 12, 13\n        \n        Important Notice:\n        1. If a disc is returned remotely, but has been converted to "SALE" already\n           "0" will return: "Can not return this Disc."\n        2. checkRfidAndSaveTrs() will do:\n           "verify rfid"\n           "set transaction to pending"\n           "set slot state to in"\n        '
        ret = INVALID
        if self.returnType in ('1', '2', '4', '5', '9'):
            msg = N_('A disc is found in exchange box, it is put to slot %(slot)s.')
            pm = {
                'slot': self.disc.slotID }
            self.alertmsg = KioskMessage(msg, pm)
            ret = TORETURN
        elif self.returnType in ('6', '7', '8'):
            msg = N_('A disc which has been already sold is found in exchange box, it is put to slot %(slot)s.')
            pm = {
                'slot': self.disc.slotID }
            self.alertmsg = KioskMessage(msg, pm)
            ret = TOLOAD
        elif self.returnType == '10':
            msg = N_('An unloaded disc is found in exchange box, it is put to slot %(slot)s.')
            pm = {
                'slot': self.disc.slotID }
            self.alertmsg = KioskMessage(msg, pm)
            ret = TOLOAD
        elif self.returnType == '11':
            msg = N_('A manually cleared disc is found in exchange box, it is put to slot %(slot)s.')
            pm = {
                'slot': self.disc.slotID }
            self.alertmsg = KioskMessage(msg, pm)
            ret = TOLOAD
        elif self.returnType == '0':
            msg = N_('An unknown disc is found in exchange box, it is put to slot %(slot)s.')
            pm = {
                'slot': self.disc.slotID }
            self.alertmsg = KioskMessage(msg, pm)
            ret = TOLOAD
        elif self.returnType == '3':
            msg = N_('A disc is found in exchange box, but kiosk has no empty slot for it.')
            self.alertmsg = KioskMessage(msg)
            ret = TOERROR
        elif self.returnType == '12':
            msg = N_("A disc is found in exchange box, but this disc does not belong to this kiosk's owner.")
            self.alertmsg = KioskMessage(msg)
            ret = TOERROR
        elif self.returnType == '13':
            msg = N_('A disc is found in exchange box, but this disc is not recognized.')
            self.alertmsg = KioskMessage(msg)
            ret = TOERROR
        
        return ret

    
    def _returnDiscBack(self):
        
        try:
            tmpmsg = N_('[%(wid)s] insert disc into exchange box failed. Disc will be put back to slot %(slot)s.')
            pm = {
                'wid': self.windowID,
                'slot': self.disc.slotID }
            msg = KioskMessage(tmpmsg, pm)
            self.addAlert(WARNING, msg.message)
            self._carriageToRack()
        except InsertException:
            self._insertLoop()


    
    def _insertFailRecovery(self, exin):
        self.disc = Disc()
        
        try:
            self._readRfid()
        except WrongOutRfidError:
            log.info('[%s] - Read RFID failed when doing insert fail recovery.' % self.windowID)
            self.disc.rfid = str(time.time())
        except InvalidDiscRfidError:
            log.info('[%s] - Invalid RFID when doing insert fail recovery.' % self.windowID)

        
        try:
            self._rackToRack('223', '-1')
        except (RetreiveNoDiscError, RetreiveFailError) as ex:
            msg = N_('Retrieve disc from exchange box to carriage failed. Please contact our tech support.')
            raise FatalError(msg, { }, exin.errCode)

        ret = self._checkRfid()
        log.info('[%s] - %s' % (self.windowID, self.alertmsg))
        if ret == TORETURN:
            self.addAlert(INFO, self.alertmsg.message)
        elif ret == TOLOAD:
            self.addAlert(WARNING, self.alertmsg.message)
        elif ret == TOERROR:
            self.addAlert(ERROR, self.alertmsg.message)
            raise FatalError(self.alertmsg.rawmsg, self.alertmsg.param, ret)
        
        msg = _('A disc is found in exchange box, it will be put to slot %s') % self.disc.slotID
        self._setProcessText(msg)
        
        try:
            self._carriageToRack()
        except RetrieveExchangeException as ex:
            raise FatalError(ex.rawmsg, ex.param, ex.errCode)
        except InsertException:
            self._insertLoop()

        self._saveExchangeRecoveryStatus()

    
    def _saveExchangeRecoveryStatus(self):
        
        try:
            log.info('[%s] Save Status: disc: %s, rfid:%s' % (self.windowID, self.disc.title, self.disc.rfid))
            self.connProxy.saveRecoverStatus(self.returnType, self.disc)
        except Exception:
            log.error('[%s] Conn Proxy SAVE Status Error:\n%s' % (self.windowID, traceback.format_exc()))
            msg = N_('Save recover status to DB failed.')
            raise SaveStatusError(msg)


    
    def _rentSaleNoDiscAlert(self):
        pm = {
            'slot_id': self.disc.slotID }
        self.noDiscAlert(pm)

    
    def on_done(self):
        self.dbSync()
        if not (self.shoppingCart.getSize() == self.shoppingCart.getEjectedDiscsSize()):
            '\n            tmpShoppingCart = deepcopy(self.shoppingCart)\n            globalSession.shoppingCart.clear()\n            for disc in tmpShoppingCart.getUnejectedDiscs():\n                globalSession.shoppingCart.addDisc(disc)\n            '
            msg = _('Not all of the discs have been ejected.')
            globalSession.param['eject_result'] = '%s\n%s' % (msg, globalSession.param['eject_result'])
        
        self.nextWindowID = self.resultForm

    
    def getUserEmail(self):
        pass

    
    def _run(self):
        globalSession.param['eject_result'] = ''
        discs = self.shoppingCart.discs
        kiosk_id = config.getKioskId()
        today = ptools.getCurTime('%Y-%m-%d')
        today_path = os.path.join(VIDEO_PATH, today)
        for disc in discs:
            
            try:
                if not os.path.exists(today_path):
                    os.makedirs(today_path)
                
                db_action_time = ptools.getCurTime('%Y-%m-%d %H:%M:%S')
                action_time = ptools.getCurTime('%Y-%m-%d-%H-%M-%S')
                vname = '%s-%s.avi' % (kiosk_id, action_time)
                video_path = os.path.join(VIDEO_PATH, today_path, vname)
                err_msg = ''
                action_type = 'out'
                self._start_record(video_path)
                success = True
                self.disc = disc
                taken = str(self.shoppingCart.getEjectedDiscsSize())
                processing = str(self.shoppingCart.getSize() - self.shoppingCart.getEjectedDiscsSize())
                self.flash.send('txt_taked', 'setText', {
                    'text': taken })
                self.flash.send('txt_processing', 'setText', {
                    'text': processing })
                rfid = self.disc.rfid
                
                try:
                    self._rackToExchange()
                    self._vomitDisc()
                except InsertException as ex:
                    err_msg = str(ex)
                    self.save_failed_trs(self.disc, err_msg, db_action_time, action_type, today, vname, kiosk_id)
                    log.error('_rackToExchange: %s' % str(ex))
                    globalSession.param['eject_result'] += ex.i18nmsg + '\n'
                    self._returnDiscBack()
                    self._insertFailRecovery(ex)

                if success == True:
                    self.shoppingCart.ejectDisc(rfid)
                    self._saveStatus(disc)
            except RetreiveNoDiscError as ex:
                err_msg = str(ex)
                self.save_failed_trs(self.disc, err_msg, db_action_time, action_type, today, vname, kiosk_id)
                rfid = self.connProxy.getRfidBySlotId(self.disc.slotID)
                if rfid:
                    self.connProxy.setBadRfid(rfid)
                    msg = '%s - %s' % (ex.message, 'The disc is set to bad.')
                    self._rentSaleNoDiscAlert()
                
                log.error('[%s] - %s' % (self.windowID, ex))
                self._setProcessText(ex.i18nmsg)
                globalSession.param['eject_result'] += ex.i18nmsg + '\n'
            except RetreiveFailError as ex:
                err_msg = str(ex)
                self.save_failed_trs(self.disc, err_msg, db_action_time, action_type, today, vname, kiosk_id)
                rfid = self.connProxy.getRfidBySlotId(self.disc.slotID)
                if rfid:
                    self.connProxy.setBadRfid(rfid)
                    msg = '%s - %s' % (ex.message, 'The disc is set to bad.')
                    self.addAlert(WARNING, msg)
                
                log.error('[%s] - %s' % (self.windowID, ex))
                self._setProcessText(ex.i18nmsg)
                globalSession.param['eject_result'] += ex.i18nmsg + '\n'
                self.connProxy.emailAlert('PRIVATE', ex.message, critical = self.connProxy.UNCRITICAL)
            except WrongOutRfidError as ex:
                log.error('[%s] - %s' % (self.windowID, ex))
                err_msg = str(ex)
                self.save_failed_trs(self.disc, err_msg, db_action_time, action_type, today, vname, kiosk_id)
                self.on_wrongOutRfid(ex)
            except InvalidDiscException as ex:
                err_msg = str(ex)
                self.save_failed_trs(self.disc, err_msg, db_action_time, action_type, today, vname, kiosk_id)
                self.on_invalidDiscException(ex)
            except SaveStatusError as ex:
                globalSession.param['eject_result'] += ex.i18nmsg + '\n'
                self.connProxy.emailAlert('PRIVATE', ex.message, critical = self.connProxy.UNCRITICAL)
                err_msg = str(ex)
                self.save_failed_trs(self.disc, err_msg, db_action_time, action_type, today, vname, kiosk_id)
            except FatalError as ex:
                err_msg = str(ex)
                self.save_failed_trs(self.disc, err_msg, db_action_time, action_type, today, vname, kiosk_id)
                self.addAlert(ERROR, ex.message)
                self.dbSync()
                raise 
            except Exception as ex:
                err_msg = str(ex)
                self.save_failed_trs(self.disc, err_msg, db_action_time, action_type, today, vname, kiosk_id)
                self.dbSync()
                raise 
            finally:
                self._stop_record()

        
        self.on_done()
        self.getUserEmail()


