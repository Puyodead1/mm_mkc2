# Source Generated with Decompyle++
# File: guiRemoteArrangementForm.pyc (Python 2.5)

'''
MovieMate Kiosk Core V0.4
CopyRight MovieMate, Inc.

Created 2009-08-13 Andrew
andrew.lu@cereson.com

Filename:guiRemoteArrangement.py

Change Log:

'''
from mcommon import *
from guiRobotForm import RobotForm
exchangeSlot = 1000
log = initlog('guiRemoteArrangementForm')

class RemoteArrangementForm(RobotForm):
    
    def __init__(self):
        RobotForm.__init__(self)
        self.timeoutSec = 300
        self.nextWindowID = 'MainForm'
        self.preWindowID = 'MainForm'
        self.screenID = 'RA'

    
    def _initComponents(self):
        RobotForm._initComponents(self)
        self.exchangeEmpty = True
        self.laseSlot = 0
        self.exceptions = None
        self.disc = Disc()
        self.flash.send('txt_msg', 'setText', {
            'text': _('Remote Arrange') })
        self.flash.send('swf_send_disc', 'show', { })

    
    def moves(self, steps):
        dest = steps.pop(0)
        while steps:
            orig = steps[0]
            self.oneStep(orig, dest)
            dest = steps.pop(0)

    
    def oneStep(self, fromSlot, toSlot):
        self.laseSlot = fromSlot
        log.info('RackArranger:oneStep move from %s to %s' % (fromSlot, toSlot))
        
        try:
            if fromSlot == exchangeSlot:
                self.disc.slotID = toSlot
                self._exchangeToRack()
                self.exchangeEmpty = True
            elif toSlot == exchangeSlot:
                self.disc.slotID = fromSlot
                self._rackToExchange()
                self.exchangeEmpty = False
            else:
                self._rackToRack(fromSlot, toSlot)
        except InsertException as ex:
            self.connProxy.setBadSlot(toSlot)
            if fromSlot == exchangeSlot:
                
                try:
                    self._carriageToExchange()
                except:
                    msg = N_("Failed to send disc back to %(fs)s, it's on the carriage now.")
                    self.arrangeRecord(fromSlot, toSlot, 'failed', msg)
                    msg = N_("Last Operation: Exchange box -> Slot %(slot)s. Failed to send disc back to exchange box, it's on the carriage now.")
                    pm = {
                        'slot': toSlot }
                    raise FatalError(msg, pm, ex.errCode)

                msg = N_('Disc has been put back to %(fs)s.')
                self.arrangeRecord(fromSlot, toSlot, 'failed', msg)
                msg = N_('Last Operation: Exchange box -> Slot %(slot)s. Disc has been put back to Exchange box.')
                pm = {
                    'slot': toSlot }
                raise InsertException(msg, pm, ex.errCode)
            else:
                
                try:
                    self._rackToRack('-1', fromSlot)
                except:
                    rfid = self.connProxy.getRfidBySlotId(fromSlot)
                    if rfid:
                        self.connProxy.setBadRfid(rfid)
                    
                    msg = N_("Failed to send disc back to %(fs)s, it's on the carriage now.")
                    self.arrangeRecord(fromSlot, toSlot, 'failed', msg)
                    msg = N_("Last Operation: Slot %(fs)s -> Slot %(ts)s. Failed to send disc back to Slot %(fs)s, it's on the carriage now.")
                    pm = {
                        'fs': fromSlot,
                        'ts': toSlot }
                    raise FatalError(msg, pm, ex.errCode)

            msg = N_('Disc has been put back to Slot %(fs)s.')
            self.arrangeRecord(fromSlot, toSlot, 'failed', msg)
            msg = N_('Last Operation: Slot %(fs)s -> Slot %(ts)s. Disc has been put back to Slot %(fs)s.')
            pm = {
                'fs': fromSlot,
                'ts': toSlot }
            raise InsertException(msg, pm, ex.errCode)
        except (RetreiveNoDiscError, RetreiveFailError):
            rfid = self.connProxy.getRfidBySlotId(fromSlot)
            if rfid:
                self.connProxy.setBadRfid(rfid)
            
            msg = N_('%(fs)s is empty.')
            self.arrangeRecord(fromSlot, toSlot, 'failed', msg)
            raise 

        self.connProxy.moveSlot(fromSlot, toSlot)
        self.arrangeRecord(fromSlot, toSlot)

    
    def arrangeRecord(self, fromSlot, toSlot, fin = 'done', errmsg = ''):
        msg = N_('Remote Arrange: move disc from %(fs)s to %(ts)s %(fin)s.')
        if fromSlot == exchangeSlot:
            pm = {
                'fs': 'exchange box',
                'ts': 'slot %s' % toSlot }
        elif toSlot == exchangeSlot:
            pm = {
                'fs': 'slot %s' % fromSlot,
                'ts': 'exchange box' }
        else:
            pm = {
                'fs': 'slot %s' % fromSlot,
                'ts': 'slot %s' % toSlot }
        pm['fin'] = fin
        if errmsg:
            msg = msg + '<br>' + errmsg
        
        alert = KioskMessage(msg, pm)
        self.addAlert(INFO, alert.message)

    
    def getArrangePlan(self):
        self.plan = self.connProxy.getArrangementPlan()
        if self.plan:
            log.info('============ START ARRANGE ===========')
            log.info('Get new move plan: %s' % str(self.plan))
        

    
    def arrangeRack(self):
        if not (self.plan):
            return None
        
        success = True
        for setp in self.plan:
            
            try:
                self.moves(setp)
            except RetreiveNoDiscError as ex:
                msg = 'Remote Arrange Failed, ' + ex.message
                log.error('%s ---->\n%s' % (msg, traceback.format_exc()))
                pm = {
                    'slot_id': self.laseSlot }
                self.noDiscAlert(pm)
                success = False
                break
            except RetreiveFailError as ex:
                msg = 'Remote Arrange Failed, ' + ex.message
                log.error('%s ---->\n%s' % (msg, traceback.format_exc()))
                self.connProxy.emailAlert('PRIVATE', msg, critical = self.connProxy.UNCRITICAL)
                success = False
                break
            except InsertException as ex:
                msg = 'Remote Arrange Failed, ' + ex.message
                log.error('%s ---->\n%s' % (msg, traceback.format_exc()))
                self.connProxy.emailAlert('PRIVATE', msg, critical = self.connProxy.UNCRITICAL)
                success = False
                break
            except FatalError as ex:
                msg = 'Remote Arrange Failed, ' + ex.message
                log.error('%s ---->\n%s' % (msg, traceback.format_exc()))
                success = False
                self.except ions = ex
                break
            except Exception as ex:
                msg = 'Remote Arrange Failed, ' + ex.message
                log.error('%s ---->\n%s' % (msg, traceback.format_exc()))
                self.connProxy.emailAlert('PRIVATE', msg, critical = self.connProxy.UNCRITICAL)
                success = False
                self.exceptions = ex
                break

        
        
        try:
            if success == True:
                if self.exchangeEmpty == False:
                    self.oneStep(exchangeSlot, self.laseSlot)
                
                self._goToExchange()
            
            self.connProxy.finishArrangement()
        except (RetreiveNoDiscError, RetreiveFailError) as ex:
            msg = 'Remote Arrange Failed, ' + ex.message
            log.error('%s ---->\n%s' % (msg, traceback.format_exc()))
            self.connProxy.emailAlert('PRIVATE', msg, critical = self.connProxy.UNCRITICAL)
            success = False
        except FatalError as ex:
            msg = 'Remote Arrange Failed, ' + ex.message
            log.error('%s ---->\n%s' % (msg, traceback.format_exc()))
            success = False
            self.except ions = ex
        except Exception as ex:
            msg = 'Remote Arrange Failed, ' + ex.message
            log.error('%s ---->\n%s' % (msg, traceback.format_exc()))
            self.connProxy.emailAlert('PRIVATE', msg, critical = self.connProxy.UNCRITICAL)
            success = False
            self.exceptions = ex

        if success == True:
            msg = N_('Remote Arrange finished successfully.')
            self.addAlert(INFO, msg)
            subject = 'Notification - %s - Remote Arrangement' % self.connProxy.kioskId
            self.connProxy.emailAlert('CLIENT', self.customerAlert, subject = subject, critical = self.connProxy.MINICRITICAL)
        else:
            self.addAlert(ERROR, msg)
            if self.exceptions:
                raise self.exceptions
            

    
    def _run(self):
        self.getArrangePlan()
        if self.plan:
            self.arrangeRack()
        


