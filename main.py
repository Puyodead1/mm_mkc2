# Source Generated with Decompyle++
# File: main.pyc (Python 2.5)

'''
MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-10-07 Vincent
vincent.chen@cereson.com

Filename: main.py
The Main Entry of MKC

Change Log:
    Andrew 2009-05-15 check whether initRobot failed. #1691
    Andrew 2009-05-12 Read fatalerror.log to find is there any error
    Andrew 2009-05-06 Change first start form to RecoverTakeInForm
    Vincent 2009-04-09 Add 3 Return Option Form
    Vincent 2009-03-10 Add Super Admin 3 Forms
    Vincent 2009-03-04 Add verifyDb in __init__ for verify DB schema
    Vincent 2009-02-28 For #1583
'''
import time
from proxy.conn_proxy import ConnProxy
import proxy.db as proxy
import control
from mcommon import *
from flashScreen import startScreen
loadForms = set([
    'MainForm',
    'CheckOutEjectForm',
    'CheckOutSwipeCardForm',
    'ShoppingCartForm',
    'PickUpEjectForm',
    'PickUpSwipeCardForm',
    'PickUpDiscListForm',
    'PickUpResultForm',
    'QuickLoadForm',
    'ReturnTakeInForm',
    'RentMainForm',
    'DiscDetailForm',
    'DiscPriceForm',
    'AdminMainForm',
    'LoadDiscListForm',
    'LoadDiscInfoForm',
    'LoadUpcEnterForm',
    'LoadTitleEnterForm',
    'LoadTakeInForm',
    'TestMainForm',
    'TestingForm',
    'TestResultForm',
    'TestTakeInForm',
    'ReportForm',
    'KioskInfoForm',
    'UnloadBySlotForm',
    'UnloadByTitleForm',
    'UnloadEjectForm',
    'UnloadResultForm',
    'CouponForm',
    'CheckOutResultForm',
    'ReturnResultForm',
    'LoadResultForm',
    'FatalErrorForm',
    'ConfigTestModeForm',
    'ConfigSpeakerVolumeForm',
    'ConfigOperatorCodeForm',
    'ConfigSmartLoadForm',
    'ConfigHDMIStateForm',
    'ConfigNetworkDiagnosisForm',
    'ConfigPowerOffForm',
    'SuperAdminMainForm',
    'SuperAdminVerticalAdjForm',
    'SuperAdminOffsetAdjForm',
    'ReturnOptionForm',
    'ReturnDiscListForm',
    'ReturnSwipeCardForm',
    'UnloadMarkedForm',
    'RecoverTakeInForm',
    'SuperAdminDistanceForm',
    'InitFailForm',
    'RemoteArrangementForm',
    'DiscAvailableNoticeForm',
    'PickUpCodeForm',
    'CheckOutSwipeDebitCardForm',
    'CheckOutChooseCardForm',
    'CheckOutSwipeChipPinForm',
    'MembershipLoginSwipeCardForm',
    'MembershipLoginPasswordForm',
    'MembershipCenterForm',
    'MembershipCouponForm',
    'MembershipProfileForm',
    'MembershipTransactionForm',
    'MembershipLogoutForm',
    'RegisterSwipeCardForm',
    'RegisterMainForm',
    'RegisterResultForm',
    'CerepayCenterForm',
    'CheckOutWithoutCerepayCardForm',
    'CerepayTopupMainForm',
    'CerepayTopupSwipeChinPinForm',
    'CerepayTopupSwipeCreditCardForm',
    'CerepayTopupErrorForm',
    'CerepayTopupReceiptForm',
    'ReturnManuallyTakeInForm',
    'CheckOutSwipeProsaForm',
    'CheckOutSwipeSiTefForm',
    'ShowAllSlotForm'])
log = initlog('main')

class Main(object):
    connProxy: ConnProxy

    def __init__(self):
        ''' The self.forms set structure is import.
        Each of its component should related to a form Class which has the same name
        "MainForm" is the first page which must be implemented.
        '''
        self.forms = loadForms
        self.connProxy = ConnProxy.getInstance()
        self.connProxy.verifyDb()
        self._initForms()

        print('init form finished')
        
        try:
            self.connProxy.logMkcEvent(category = 'system', action = 'startup', data1 = 'MKC Start')
        except:
            pass

        print("init robot")
        # self.connProxy.setKioskInfo()
        (self.rerr, self.rmsg) = initRobot()
        log.info('[Main run] ROBOT INIT: %s, %s' % (self.rerr, self.rmsg))
        (self.serr, self.smsg) = sensorDetect()
        log.info('[Main run] SENSOR DECECT: %s, %s' % (self.serr, self.smsg))

    
    def _profileStart(self):
        self._st = time.time()

    
    def _profileEnd(self, msg):
        log.info('%s spend time %s' % (msg, time.time() - self._st))

    
    def _installGlobalTheme(self):
        import builtins
        theme = self.connProxy._getConfigByKey('ui_theme')
        log.info('set MKC to %s theme' % theme)
        builtins.__dict__['MKC_THEME'] = theme

    
    def _initForms(self):
        self._installGlobalTheme()
        
        try:
            for form in loadForms:
                cmd = 'from gui%(form)s import %(form)s' % {
                    'form': form }
                exec(cmd)
            
            for form in self.forms:
                statement = 'self.%s = %s()' % (form, form)
                exec(statement)
        except Exception:
            msg = '[Main _init_forms] register form: %s error:%s' % (form, traceback.format_exc())
            log.error(msg)
            self.connProxy.emailAlert('PRIVATE', msg, 'andrew.lu@cereson.com', critical = self.connProxy.UNCRITICAL)


    
    def _initFatal(self):
        if self.rerr != control.ROBOT_OK:
            m = N_('Kiosk init failed.<br>POWER OFF THE KIOSK. Make sure you unscrew the SIX locking-screws inside the kiosk before power on.')
            alert = KioskMessage(m, { })
            self.connProxy.emailAlert('PRIVATE', alert.message, critical = self.connProxy.UNCRITICAL)
            msg = 'Init Machine Fatal Error.\n%s' % self.rmsg
            log.error('[Main run] INFO:%s' % msg)
            return True
        
        if self.serr != 0:
            self.connProxy.emailAlert('PRIVATE', self.smsg, critical = self.connProxy.UNCRITICAL)
        
        return False

    
    def run(self):
        
        try:
            self.nextForm = 'RecoverTakeInForm'
            if self._initFatal():
                self.nextForm = 'InitFailForm'
            
            self.startTime = time.time()
            while True:
                '\n                # If the sreen will show MainForm, check to restart\n                if self.nextForm == "MainForm":\n                    restartLeft = RESTART_INTERVAL - (time.time() - self.startTime)\n                    log.info("Next Screen Restart Time Left: %s seconds." % restartLeft)\n                    if restartLeft <= 0:\n                        restartScreen()\n                        self.startTime = time.time()\n                '
                self._showFormByName(self.nextForm)
        except Exception:
            log.error('[Main run] error:%s\n%s' % (traceback.format_exc(), self.__dict__))


    
    def _showFormByName(self, formName):
        if formName not in self.forms:
            log.info('[Main _showFormByName] no such form registered: %s, use MainForm' % formName)
            formName = 'MainForm'
        
        statement = 'self.nextForm = self.%s.render()' % formName
        exec(statement)
        self.lastForm = formName



def start():
    startFlag()
    globalSession.clear()
    startScreen()
    time.sleep(2)
    setLanguage('en')
    main = Main()
    sync_active_information(main.connProxy)
    main.run()

