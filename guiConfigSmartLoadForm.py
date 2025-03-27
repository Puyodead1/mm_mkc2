# Source Generated with Decompyle++
# File: guiConfigSmartLoadForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2009-06-10 Andrew
andrew.lu@cereson.com

Filename: guiConfigSmartLoadForm.py
smart load
Screen ID: C4

Change Log:
    
'''
from mcommon import *
from control import *
from guiBaseForms import ConfigForm
log = initlog('ConfigSmartLoadForm')
(OK, CANCEL, FATAL_ERROR, DB_ERROR, UNKNOWN) = list(range(5))

class ConfigSmartLoadForm(ConfigForm):
    
    def __init__(self):
        ConfigForm.__init__(self)
        self.screenID = 'C4'
        self.preWindowID = 'AdminMainForm'
        self.uiErrorWindowID = 'MainForm'
        self.lstResponseCtrl += [
            'btn_all_smart_load',
            'btn_step2_cancel',
            'btn_finish']
        robot = Robot()
        self.robot = robot.getInstance()
        self.slottime = 52

    
    def _initComponents(self):
        ConfigForm._initComponents(self)
        self.SLCancel = False
        self.disc = Disc()
        self.finish = OK
        self.finalmsg = ''
        self.baddisc = False
        self.loaded = 0
        self.failed = 0
        self.newDisc = True
        self.slotleft = 0
        self.flash.send('txt_title', 'setText', {
            'text': _('Smart Load') })
        self._gotoStep(1)

    
    def _gotoStep(self, st):
        self.step = st
        if self.step == 1:
            self.timeoutSec = 60
            self.flash.send('ctr_group_step1', 'show', { })
            self.flash.send('ctr_group_step2', 'hide', { })
            self.flash.send('ctr_group_step3', 'hide', { })
            self._setTestModeButton()
            self._setHDMIButton()
            msg = _('1. Open the back door.\n\n2. Insert the Discs you want to load.\n\n3. Close the back door.')
            self.flash.send('txt_step1_msg', 'setText', {
                'text': msg })
        elif self.step == 2:
            self.timeoutSec = 300
            self.flash.send('ctr_group_step1', 'hide', { })
            self.flash.send('ctr_group_step2', 'show', { })
            self.flash.send('ctr_group_step3', 'hide', { })
            self._setTestModeButton(True)
            self._setHDMIButton(True)
            self._showSpendingTime(0)
        elif self.step == 3:
            self.timeoutSec = 60
            self.flash.send('ctr_group_step1', 'hide', { })
            self.flash.send('ctr_group_step2', 'hide', { })
            self.flash.send('ctr_group_step3', 'show', { })
            self._setTestModeButton(True)
            self._setHDMIButton(True)
            self.flash.send('txt_load_disc', 'setText', {
                'text': str(self.loaded) })
            self.flash.send('txt_unrecognizable_disc', 'setText', {
                'text': str(self.failed) })
            self.flash.send('txt_step3_msg', 'setText', {
                'text': _(self.finalmsg) })
            msg = N_('%(msg)s<br>Loaded Discs %(load)d<br>Unrecognizable Disc %(ur)d')
            pm = {
                'msg': self.finalmsg,
                'load': self.loaded,
                'ur': self.failed }
            alert = KioskMessage(msg, pm)
            self.addAlert(INFO, alert.message)
        

    
    def on_btn_all_smart_load_event(self):
        self._gotoStep(2)

    
    def on_btn_step2_cancel_event(self):
        self.SLCancel = not (self.SLCancel)
        if self.SLCancel:
            self.flash.send('btn_step2_cancel', 'setText', {
                'label': _('Stopping...') })
        else:
            self.flash.send('btn_step2_cancel', 'setText', {
                'label': _('Cancel') })

    
    def on_btn_finish_event(self):
        self.on_exit()

    
    def logEvent(self, logtype, errcode, errmsg, disc = None):
        if not disc:
            disc = Disc()
        
        self.connProxy.logMkcEvent(category = 'system', action = logtype, data1 = disc.slotID, data2 = disc.rfid, data3 = disc.upc, data4 = disc.title, data5 = errcode, data6 = errmsg)

    
    def _verifyRet(self, ret):
        if type(ret) != type({ }):
            log.error('Invalid type of ret, type: %s, ret: %s.' % (type(ret), ret))
            msg = KioskMessage(N_('Invalid Response of Robot, Please Restart the Kiosk and Retry.'), { })
            errCode = self.screenID + '-00R9000'
            self.logEvent('error', errCode, msg.message)
            raise FatalError(msg.rawmsg, msg.param, errCode)
        
        if 'errno' not in ret:
            log.error("Invalid value of ret, no 'errno' key found, ret: %s." % ret)
            msg = KioskMessage(N_('Invalid Response of Robot, Please Restart the Kiosk and Retry.'), { })
            errCode = self.screenID + '-00R9000'
            self.logEvent('error', errCode, msg.message)
            raise FatalError(msg.rawmsg, msg.param, errCode)
        

    
    def _setBadDisc(self, rfid):
        self.baddisc = True
        if rfid:
            self.disc.rfid = rfid
        else:
            self.disc.rfid = str(time.time())
        self.disc.title = 'Unknown Title'
        self.disc.movieID = '0000'
        self.disc.upc = '0' * 12
        self.disc.genre = 'Unknown Genre'

    
    def _saveStatus(self):
        
        try:
            log.info('[%s] Save Status: disc: %s, rfid:%s, isBad:%s' % (self.windowID, self.disc.title, self.disc.rfid, self.baddisc))
            self.connProxy.saveLoadStatus(self.disc)
            if self.baddisc:
                self.connProxy.setBadRfid(self.disc.rfid)
        except Exception:
            log.error('[%s] Conn Proxy SAVE Status Error:\n%s' % (self.windowID, traceback.format_exc()))
            msg = N_('DB operation failed.')
            raise SaveStatusError(msg)


    
    def _verifyDisc(self):
        
        try:
            self.newDisc = True
            returnType = str(self.connProxy.isRfidLoadable(self.disc))
            if returnType != '1':
                self.newDisc = False
        except Exception:
            log.error('[%s] check isRfidLoadable Error:\n%s' % self.windowID)
            msg = N_('DB operation failed.')
            raise SaveStatusError(msg)


    
    def _showSpendingTime(self, finish):
        sec = self.slotleft * self.slottime - finish
        t = time.gmtime(sec)
        timestr = _('%(hour)sh%(min)sm%(sec)ss') % {
            'hour': str(t[3]).rjust(2, '0'),
            'min': str(t[4]).rjust(2, '0'),
            'sec': str(t[5]).rjust(2, '0') }
        self.flash.send('txt_time_left', 'setText', {
            'text': timestr })

    
    def _showDiscDetail(self):
        dictDisc = { }
        if not (self.disc.title):
            dictDisc['movie_title'] = 'Loading...'
        else:
            dictDisc['movie_title'] = self.disc.title
        dictDisc['movie_pic'] = getPicFullPath(self.disc.picture)
        dictDisc['dvd_version'] = self.disc.version
        dictDisc['genre'] = self.disc.genre
        dictDisc['dvd_release_date'] = self.disc.releaseDate
        dictDisc['starring'] = self.disc.starring
        dictDisc['directors'] = self.disc.directors
        dictDisc['rating'] = self.disc.rating
        dictDisc['rent_price'] = self.disc.rentalPrice
        dictDisc['buy_price'] = self.disc.salePrice
        dictDisc['synopsis'] = self.disc.synopsis
        dictDisc['trailer_name'] = self.disc.trailerName
        dictDisc['is_available'] = '1'
        self.flash.send('ctr_movie_detail2', 'setMovieDetail', {
            'ctr_movie_detail': dictDisc })

    
    def _parseRobotResult(self, ret):
        self._verifyRet(ret)
        errno = ret['errno']
        if self.robotStep == 1:
            if errno == ROBOT_OK:
                log.info('[%s] - Retrieve from slot %s OK.' % (self.windowID, self.backslot))
            elif errno == ROBOT_NO_DISC:
                displayErrCode = self.screenID + '-05R' + str(errno)
                msg = N_('Warning(%(errcode)s): Retrieve from slot %(slot)s failed: No Disc.')
                param = {
                    'errcode': displayErrCode,
                    'slot': self.backslot }
                raise RetreiveNoDiscError(msg, param, displayErrCode)
            elif errno == ROBOT_TIMEOUT:
                displayErrCode = self.screenID + '-05R' + str(errno)
                msg = N_('Error: Retrieve from slot %(slot)s failed: Time out. Please try again later.')
                pm = {
                    'slot': self.backslot }
                km = KioskMessage(msg, pm)
                self.logEvent('error', displayErrCode, km.message, None)
                raise FatalError(msg, pm, displayErrCode)
            elif errno == ROBOT_CARRIAGE_JAM:
                displayErrCode = self.screenID + '-05R' + str(errno)
                msg = N_('Error: Retrieve from slot %(slot)s failed: Carriage jam. Please check if there is anything stuck in the route')
                pm = {
                    'slot': self.backslot }
                km = KioskMessage(msg, pm)
                self.logEvent('error', displayErrCode, km.message, None)
                raise FatalError(msg, pm, displayErrCode)
            elif errno == ROBOT_RETRIEVE_FAIL:
                displayErrCode = self.screenID + '-05R' + str(errno)
                msg = N_('Error: Retrieve from slot %(slot)s failed. Insert or Retrieve failure.')
                pm = {
                    'slot': self.backslot }
                km = KioskMessage(msg, pm)
                self.logEvent('error', displayErrCode, km.message, None)
                raise RetreiveNoDiscError(msg, pm, displayErrCode)
            elif errno == ROBOT_INSERT_FAIL:
                displayErrCode = self.screenID + '-05R' + str(errno)
                msg = N_('Error: Retrieve from slot %(slot)s failed: Insert Failed. Insert or Retrieve failure.')
                pm = {
                    'slot': self.backslot }
                km = KioskMessage(msg, pm)
                self.logEvent('error', displayErrCode, km.message, None)
                raise FatalError(msg, pm, displayErrCode)
            elif errno == ROBOT_RETRIEVE_FATAL:
                displayErrCode = self.screenID + '-05R' + str(errno)
                msg = N_('Error: Retrieve from slot %(slot)s failed: Retrieve fatal. The disc was unable to be retrieved, please check the slot for any physical issues.')
                pm = {
                    'slot': self.backslot }
                km = KioskMessage(msg, pm)
                self.logEvent('error', displayErrCode, km.message, None)
                raise FatalError(msg, pm, displayErrCode)
            elif errno == ROBOT_INSERT_FATAL:
                displayErrCode = self.screenID + '-05R' + str(errno)
                msg = N_('Error: Retrieve from slot %(slot)s failed: Insert Fatal. Please restart the kiosk and try again later.')
                pm = {
                    'slot': self.backslot }
                km = KioskMessage(msg, pm)
                self.logEvent('error', displayErrCode, km.message, None)
                raise FatalError(msg, pm, displayErrCode)
            else:
                displayErrCode = self.screenID + '-05R' + str(errno)
                msg = N_('Error: Retrieve from slot %(slot)s failed: Unknown error: %(err)s.?Please restart the kiosk and try again later.')
                pm = {
                    'slot': self.backslot,
                    'err': errno }
                km = KioskMessage(msg, pm)
                self.logEvent('error', displayErrCode, km.message, None)
                raise FatalError(msg, pm, displayErrCode)
        elif self.robotStep == 2:
            self.baddisc = False
            if errno == ROBOT_OK:
                self.disc.rfid = ret['rfid']
            elif errno == ROBOT_TIMEOUT:
                displayErrCode = self.screenID + '-08R' + str(errno)
                msg = _('Error: RFID Read Time Out.')
                self._setBadDisc(None)
            else:
                displayErrCode = self.screenID + '-08R' + str(errno)
                msg = N_('Error: Read rfid unknown Error %(err)s, please check the RFID tag, change the tag if necessary and reload the disc.')
                pm = {
                    'err': errno }
                raise FatalError(msg, pm, displayErrCode)
            if self.baddisc == False:
                self.disc.upc = self.movieProxy.getUpcByRfidQuickLoad(self.disc.rfid)
                if not (self.disc.upc):
                    log.info('[%s] - Cannot get upc.slot:%d, RFID:%s' % (self.windowID, self.backslot, self.disc.rfid))
                    self._setBadDisc(self.disc.rfid)
                else:
                    self.movieProxy.getMovieDetailByUpc(self.disc)
                    self._verifyDisc()
            
            self.connProxy.getDefaultSettings(self.disc)
            self._showDiscDetail()
        elif errno == ROBOT_OK:
            msg = N_('Disc is inserted into slot %(slot)s. Title: %(title)s, Rfid: %(rfid)s')
            pm = {
                'slot': self.disc.slotID,
                'title': self.disc.title,
                'rfid': self.disc.rfid }
            alert = KioskMessage(msg, pm)
            self.addAlert(INFO, alert.message)
        elif errno == ROBOT_NO_DISC:
            displayErrCode = self.screenID + '-03R' + str(errno)
            msg = N_('No Disc Found in Exchange Box, the disc might be dropped.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)
        elif errno == ROBOT_TIMEOUT:
            displayErrCode = self.screenID + '-03R' + str(errno)
            msg = N_('Robot Time Out. Please restart the kiosk.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)
        elif errno == ROBOT_CARRIAGE_JAM:
            displayErrCode = self.screenID + '-03R' + str(errno)
            msg = N_('Carriage Jam, Please check if there is anything stuck in the route. Then please contact our Tech Support.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)
        elif errno == ROBOT_INSERT_FAIL:
            displayErrCode = self.screenID + '-03R' + str(errno)
            msg = N_('Insert into Slot %(slot)s failed, Insert or Retrieve failure.')
            pm = {
                'slot': self.insertslot }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        elif errno == ROBOT_RETRIEVE_FAIL:
            displayErrCode = self.screenID + '-03R' + str(errno)
            msg = N_('Retrieve disc from exchange failed. Please try again and observe the mechanical action for the possible cause.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)
        elif errno == ROBOT_RETRIEVE_FATAL:
            displayErrCode = self.screenID + '-03R' + str(errno)
            msg = N_('Retrieve disc from exchange failed.Please try again and observe the mechanical action for the possible cause.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)
        elif errno == ROBOT_INSERT_FATAL:
            displayErrCode = self.screenID + '-03R' + str(errno)
            msg = N_('Insert into Slot %(slot)s failed, Insert or Retrieve failure.')
            pm = {
                'slot': self.insertslot }
            km = KioskMessage(msg, pm)
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, pm, displayErrCode)
        else:
            displayErrCode = self.screenID + '-03R' + str(errno)
            msg = N_('Retrieve from exchange box unknown error. Please restart the kiosk try again later. If still not work, please contact our Tech Support.')
            km = KioskMessage(msg, { })
            self.logEvent('error', displayErrCode, km.message, self.disc)
            raise FatalError(msg, { }, displayErrCode)

    
    def _eventPolling(self, step):
        log.info('[%s] is polling event, robot step %d ....................' % (self.windowID, step))
        self.robotStep = step
        if self.robotStep == 1:
            self.robotstarttime = time.time()
            self._showDiscDetail()
            param = {
                'slot': self.backslot }
            r = self.robot.doCmdAsync('rack_to_exchange', param, self.timeoutSec)
        elif self.robotStep == 2:
            r = self.robot.doCmdAsync('read_rfid', { }, self.timeoutSec)
        elif self.baddisc or self.newDisc == False:
            self.insertslot = self.backslot
        else:
            self.insertslot = self.connProxy.getSmartLoadSlotId(self.backslot)
        self.disc.slotID = self.insertslot
        param = {
            'slot': self.insertslot }
        r = self.robot.doCmdAsync('exchange_to_rack', param, self.timeoutSec)
        while True:
            spent = time.time() - self.robotstarttime
            if spent > 1:
                self._showSpendingTime(spent)
            
            ef = self.flash.get(self.windowID, 0.1)
            if ef:
                ctrlID = ef.get('cid')
                log.info('[%s] get UI EVENT: %s' % (self.windowID, ctrlID))
                if ctrlID == 'btn_step2_cancel':
                    self.on_btn_step2_cancel_event()
                
            
            rf = self.robot.getResult(r)
            if rf:
                log.info('[%s] get ROBOT EVENT: %s' % (self.windowID, rf))
                self._parseRobotResult(rf)
                break
            

    
    def _run(self):
        while True:
            log.info('[%s] is running. step:%d ....................................' % (self.windowID, self.step))
            if self.step != 2:
                self.event = self.flash.get(timeout = self.timeoutSec)
                if self.event:
                    log.info('[UI Event]: %s.' % self.event)
                
                if self.event != None:
                    ctrlID = self.event.get('cid')
                    self.on_event(ctrlID)
                    if self.windowJump:
                        break
                    
                
            else:
                backslots = self.connProxy.getSlotIds('back', [
                    'empty'])
                self.slotleft = len(backslots)
                for slot in backslots:
                    self._showSpendingTime(0)
                    self.disc = Disc()
                    log.info('[%s] START LOAD SLOT %s =================================' % (self.windowID, slot))
                    self.backslot = slot
                    
                    try:
                        self._eventPolling(1)
                        self._eventPolling(2)
                        self._eventPolling(3)
                        if self.newDisc:
                            self._saveStatus()
                        
                        self.slotleft -= 1
                    except FatalError:
                        ex = None
                        self.finish = FATAL_ERROR
                        self.finalmsg = N_('Smart Load finished unsuccessfully.') + ex.message
                        log.error('[%s] %s:%s' % (self.windowID, ex.errCode, ex.message))
                        break
                    except RetreiveNoDiscError:
                        ex = None
                        log.info('[%s] %s' % (self.windowID, ex))
                    except SaveStatusError:
                        ex = None
                        self.finish = DB_ERROR
                        self.finalmsg = N_('Smart Load finished unsuccessfully.') + ex.message
                        log.error('[%s] %s' % (self.windowID, ex.message))
                        break
                    except Exception:
                        ex = None
                        self.finish = UNKNOWN
                        self.finalmsg = N_('Smart Load finished unsuccessfully.') + ex.message
                        log.error('[%s] %s' % (self.windowID, ex.message))
                        log.error(traceback.format_exc())
                        break

                    if self.SLCancel:
                        self.finalmsg = N_('Smart Load canceled.')
                        self.finish = CANCEL
                        break
                    
                    self.finalmsg = N_('Smart Load Done.')
                
                self._gotoStep(3)


