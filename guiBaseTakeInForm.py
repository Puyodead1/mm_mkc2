# Source Generated with Decompyle++
# File: guiBaseTakeInForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V0.4
CopyRight MovieMate, Inc.

Created 2008-11-19 Vincent
vincent.chen@cereson.com

Filename:guiBaseTakeInForm.py

Change Log:
    2009-04-17 Vincent For return options
    2011-03-15 Kitch
        add exception OperationalError

'''
import time
from mcommon import *
from guiRobotForm import RobotForm
from control import *
from proxy.tools import getKioskCapacity, unlock

from sqlite3 import OperationalError

from proxy.config import VIDEO_PATH
log = initlog('guiBaseTakenInForm')

class BaseTakeInForm(RobotForm):
    
    def __init__(self):
        RobotForm.__init__(self)
        self.timeoutSec = 20

    
    def _guiExchangeEject(self):
        self.flash.send('txtbox_msg2', 'hide', { })
        self.flash.send('swf_insert', 'hide', { })
        self.flash.send('swf_insert_h', 'hide', { })
        self.flash.send('swf_send_disc', 'hide', { })
        self.flash.send('swf_vomit_dvd', 'show', { })
        self.flash.send('btn_cancel', 'hide', { })
        self.flash.send('btn_continue', 'hide', { })
        time.sleep(0.2)
        self.flash.send('btn_continue', '_update_parent_ui', { })

    
    def _guiExchangeToRack(self):
        self.flash.send('txtbox_msg2', 'hide', { })
        self.flash.send('swf_insert', 'hide', { })
        self.flash.send('swf_insert_h', 'hide', { })
        self.flash.send('swf_send_disc', 'show', { })
        self.flash.send('swf_vomit_dvd', 'hide', { })
        self.flash.send('btn_cancel', 'hide', { })
        self.flash.send('btn_continue', 'hide', { })
        time.sleep(0.2)
        self.flash.send('btn_continue', '_update_parent_ui', { })

    
    def _guiContinue(self):
        self.flash.send('btn_continue', 'hide', { })
        time.sleep(0.2)
        self.flash.send('btn_continue', '_update_parent_ui', { })
        self.robot._exchange_open()

    
    def _guiCancel(self):
        self.flash.send('btn_cancel', 'hide', { })
        self.flash.send('btn_continue', 'hide', { })
        msg = _('Operation Canceled.')
        if not (self.cancelFrom):
            msg = _('Timeout. Operation Canceled.')
        
        self._setProcessText(msg)
        time.sleep(0.2)
        self.flash.send('btn_continue', '_update_parent_ui', { })

    
    def _initComponents(self):
        RobotForm._initComponents(self)
        self.disc = Disc()
        self.recoverSlot = 0
        msg = _('Please close the dvd case completely before inserting.')
        self._setProcessText(msg)
        self.flash.send('txtbox_msg2', 'show', { })
        self.flash.send('btn_cancel', 'show', { })
        self.flash.send('swf_send_disc', 'hide', { })
        self.flash.send('swf_vomit_dvd', 'hide', { })
        self.flash.send('swf_insert', 'hide', { })
        self.flash.send('swf_insert_h', 'hide', { })
        if getKioskCapacity() == '250':
            self.continue_click = True
            self.flash.send('btn_continue', 'hide', { })
            self.flash.send('swf_insert', 'show', { })
        else:
            self.flash.send('btn_continue', 'show', { })
            self.flash.send('swf_insert_h', 'show', { })
            self.continue_click = False
        time.sleep(0.2)
        self.flash.send('btn_continue', '_update_parent_ui', { })

    
    def on_dberror(self):
        self._exchangeEject()

    
    def on_wrongInRfid(self, ex):
        self._setProcessText(ex.i18nmsg)
        self._exchangeEject()
        self.nextWindowID = self.ejectDiscBackForm
        globalSession.param['return_msg'] = ex.i18nmsg

    
    def on_invalidDisc(self, ex):
        self.on_wrongInRfid(ex)

    
    def _cancel(self, r):
        self.robot.cancel()
        log.info('[Robot Cancel Called]')
        self._guiCancel()
        cancelTimeout = False
        start_time = time.time()
        sent = False
        while True:
            retFromRobot = self.robot.getResult(r, timeout = 600)
            if retFromRobot:
                log.info('[%s] canceled, return %s' % (self.windowID, retFromRobot))
                if retFromRobot['errno'] != ROBOT_CANCELED:
                    
                    try:
                        self._exchangeEject()
                    except Exception as ex:
                        log.error('exchangeEject failed: %s' % str(ex))

                
                break
            
            if cancelTimeout == False:
                cancelTimeout = True
                m = N_('Cancel Time Out, Please take out everything in the exchange box and retry')
                pm = { }
                msg = KioskMessage(m, pm)
                log.warning(msg.message)
                self._setProcessText(msg.i18nmsg)
            
            if time.time() - start_time > 10 * 60 and sent == False:
                unlock()
                self.connProxy.emailAlert('PUBLIC', msg.message, critical = self.connProxy.UNCRITICAL)
                self.sync_inactive_information('exchangeEject failed')
                sent = True
            
        sync_active_information(self.connProxy, 'kiosk recoverme')
        self.nextWindowID = self.preWindowID
        log.info('Goto %s ========================' % self.nextWindowID)

    
    def _run(self):
        
        try:
            tick = time.time()
            while True:
                if self.windowID not in [
                    'ReturnTakeInForm']:
                    break
                
                if self.continue_click:
                    break
                
                if time.time() - tick > self.timeoutSec:
                    log.info('[%s] - Timeout for continue.' % self.windowID)
                    self._guiCancel()
                    break
                
                eventFromFlash = self.flash.get(self.windowID, 0.1)
                if eventFromFlash:
                    if eventFromFlash.get('cid') == 'btn_continue':
                        log.info('[%s] - Continue Button Clicked.' % self.windowID)
                        self._guiContinue()
                        self.continue_click = True
                    elif eventFromFlash.get('cid') == 'btn_cancel':
                        log.info('[%s] - Cancel Button Clicked.' % self.windowID)
                        self._guiCancel()
                        break
                    
                
            retFromRobot = None
            returnOption = globalSession.param.get('return_option')
            kiosk_id = config.getKioskId()
            today = ptools.getCurTime('%Y-%m-%d')
            today_path = os.path.join(VIDEO_PATH, today)
            if not os.path.exists(today_path):
                os.makedirs(today_path)
            
            db_action_time = ptools.getCurTime('%Y-%m-%d %H:%M:%S')
            action_time = ptools.getCurTime('%Y-%m-%d-%H-%M-%S')
            vname = '%s-%s.avi' % (kiosk_id, action_time)
            video_path = os.path.join(VIDEO_PATH, today_path, vname)
            err_msg = ''
            action_type = 'in'
            self._start_record(video_path)
            if globalSession.disc.rfid and returnOption:
                retFromRobot = {
                    'errno': ROBOT_OK,
                    'rfid': globalSession.disc.rfid }
            else:
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
                self.flash.send('btn_continue', 'hide', { })
                self.flash.send('btn_cancel', 'hide', { })
                time.sleep(0.2)
                self.flash.send('btn_continue', '_update_parent_ui', { })
                self._compareRfid(retFromRobot)
                ret = self._needRentalPurchase()
                if ret == True:
                    self._doRentalPurchase()
                else:
                    
                    try:
                        self._exchangeToRack()
                    except InsertException as ex:
                        err_msg = str(ex)
                        self.save_failed_trs(self.disc, err_msg, db_action_time, action_type, today, vname, kiosk_id)
                        log.error('_exchangeToRack: %s' % str(ex))
                        self._insertFailRecovery(ex)
                    except RetrieveExchangeException as ex:
                        err_msg = str(ex)
                        self.save_failed_trs(self.disc, err_msg, db_action_time, action_type, today, vname, kiosk_id)
                        log.error('_exchangeToRack: %s' % str(ex))
                        self._retrieveFailRecovery(ex)

                    self._saveStatus()
                self.nextWindowID = self.resultForm
        except WrongInRfidError as ex:
            err_msg = str(ex)
            self.save_failed_trs(self.disc, err_msg, db_action_time, action_type, today, vname, kiosk_id)
            log.error('[%s] - %s' % (self.windowID, ex))
            self.on_wrongInRfid(ex)
        except SaveStatusError as ex:
            err_msg = str(ex)
            self.save_failed_trs(self.disc, err_msg, db_action_time, action_type, today, vname, kiosk_id)
            msg = _('Operation failed, the disc is ejecting back ...\nPlease retry in 5 minutes.')
            self._setProcessText(msg)
            self.on_dberror()
            self.nextWindowID = self.ejectDiscBackForm
            globalSession.param['return_msg'] = ex.i18nmsg
            self.connProxy.emailAlert('PRIVATE', ex.message, critical = self.connProxy.UNCRITICAL)
        except OperationalError as ex:
            err_msg = str(ex)
            self.save_failed_trs(self.disc, err_msg, db_action_time, action_type, today, vname, kiosk_id)
            msg = _('Operation failed, the disc is ejecting back ...\nPlease retry in 5 minutes.')
            self._setProcessText(msg)
            self.on_dberror()
            self.nextWindowID = self.ejectDiscBackForm
            globalSession.param['return_msg'] = ex.i18nmsg
            self.connProxy.emailAlert('PRIVATE', ex.message, critical = self.connProxy.UNCRITICAL)
        except InvalidDiscException as ex:
            err_msg = str(ex)
            self.save_failed_trs(self.disc, err_msg, db_action_time, action_type, today, vname, kiosk_id)
            self.on_invalidDisc(ex)
        except FatalError as ex:
            err_msg = str(ex)
            self.save_failed_trs(self.disc, err_msg, db_action_time, action_type, today, vname, kiosk_id)
            self.addAlert(ERROR, ex.message)
            raise 
        except Exception as ex:
            err_msg = str(ex)
            self.save_failed_trs(self.disc, err_msg, db_action_time, action_type, today, vname, kiosk_id)
            raise 
        finally:
            self._stop_record()

        globalSession.param['return_option'] = ''
        return self.nextWindowID

    
    def _needRentalPurchase(self):
        return False

    
    def _doRentalPurchase(self):
        pass


