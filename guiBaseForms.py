# Source Generated with Decompyle++
# File: guiBaseForms.pyc (Python 2.5)

"""

MovieMate Kiosk Core V0.4
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename:guiBaseForms.py
Contains all GUI base(abstract) forms

-- MMForm
 |-- UserForm  (Abstract)
   |-- AdminMainForm
   |-- LoadDiscSettingForm
   |-- DiscBrowseForm
   |-- ShoppingCartForm
   |-- ...
 |-- RobotForm  (Abstract)
   |-- BaseTakeInForm  (Abstract)
     |-- LoadTakeInForm
     |-- ReturnTakeInForm
     |-- QuickLoadForm
   |-- BaseEjectForm  (Abstract)
     |-- CheckOutEjectForm
     |-- PickUpEjectForm
     |-- UnloadEjectForm
 |-- MainForm
 |-- MessageBox

Change Log:
    2009-05-08 Vincent Add fatal error form error code in log
    2009-02-09 Vincent Line 163, only save UI event when it's not None

"""
import traceback
from mcommon import *
from flashScreen import *
from config import *
from proxy.conn_proxy import ConnProxy
from proxy.movie_proxy import MovieProxy
from proxy.ums_proxy import UmsProxy
log = initlog('guiBaseForms')

class MMForm(object):
    
    def __init__(self):
        self.windowID = self.__class__.__name__
        self.nextWindowID = ''
        self.preWindowID = ''
        self.uiErrorWindowID = 'MainForm'
        self.fatalErrorWindowID = 'FatalErrorForm'
        self.connProxy = ConnProxy.getInstance()
        self.movieProxy = MovieProxy.getInstance()
        self.umsProxy = UmsProxy.getInstance()
        self.flash = FlashChannel(self.windowID)
        self.windowJump = False
        self.lstResponseCtrl = []

    
    def _getEventParam(self, ctrID, key):
        return self.event.get('param_info').get(ctrID).get(key)

    
    def _show(self, _wid = None):
        if _wid is None:
            _wid = self.windowID
        
        self.flash.send('', 'showWindow', {
            'wid': _wid })

    
    def _goto(self, _wid = None):
        if _wid is None:
            _wid = self.windowID
        
        self.flash.wid = ''
        self.flash.send('', 'gotoWindow', {
            'wid': _wid })
        self.flash.wid = self.windowID
        log.info('-------------------- %s --------------------' % self.windowID)

    
    def _hide(self, _wid = None):
        if _wid is None:
            _wid = self.windowID
        
        self.flash.send('', 'hideWindow', {
            'wid': _wid })

    
    def on_cancel(self):
        self.nextWindowID = self.uiErrorWindowID
        self.windowJump = True

    
    def on_back(self):
        self.nextWindowID = self.preWindowID
        self.windowJump = True

    
    def on_error(self):
        self.nextWindowID = self.uiErrorWindowID
        self.windowJump = True

    
    def on_hide(self):
        self._sendEmail()

    
    def on_exit(self):
        self.nextWindowID = 'MainForm'
        self.windowJump = True

    
    def on_timeout(self):
        self.nextWindowID = self.preWindowID
        self.windowJump = True

    
    def on_event(self, ctrlID):
        if ctrlID in self.lstResponseCtrl:
            statement = 'self.on_%s_event()' % ctrlID
            exec(statement)
        elif ctrlID is None:
            self.on_timeout()
        

    
    def addAlert(self, alertType, msg):
        if alertType == INFO:
            self._addInfoAlert(msg)
        elif alertType == WARNING:
            self._addWarningAlert(msg)
        elif alertType == ERROR:
            self._addErrorAlert(msg)
        

    
    def _addInfoAlert(self, msg):
        if self.customerAlert:
            self.customerAlert = self.customerAlert + '<br>Info: ' + msg
        else:
            self.customerAlert = 'Info: ' + msg

    
    def _addWarningAlert(self, msg):
        if self.customerAlert:
            self.customerAlert = self.customerAlert + '<br>Warning: ' + msg
        else:
            self.customerAlert = 'Warning: ' + msg

    
    def _addErrorAlert(self, msg):
        if self.customerAlert:
            self.customerAlert = self.customerAlert + '<br>Error: ' + msg
        else:
            self.customerAlert = 'Error: ' + msg

    
    def _sendEmail(self):
        pass

    
    def noDiscAlert(self, pm):
        if HOST_ID >= 46:
            self._specialAlert(NO_DISC_SBJ, NO_DISC_ALERT, pm, self.connProxy.MINICRITICAL)
        

    
    def rfidFailAlert(self, pm):
        self._specialAlert(RFID_FAIL_SBJ, RFID_FAIL_ALERT, pm, self.connProxy.MINICRITICAL)

    
    def fatalErrorAlert(self, pm):
        self._specialAlert(FATAL_ERROR_SBJ, FATAL_ERROR_ALERT, pm, self.connProxy.CRITICAL)

    
    def _specialAlert(self, subject, message, param, critical):
        param['host_id'] = self.connProxy.kioskId
        param['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        sbj = subject % param
        msg = message % param
        self.connProxy.emailAlert('PUBLIC', msg, subject = sbj, critical = critical)

    
    def _initComponents(self):
        self.windowJump = False
        self.customerAlert = ''
        self._goto()

    
    def _run(self):
        pass

    
    def sync_inactive_information(self, description):
        log.debug('sync_inactive_information %s' % get_active_information())
        if get_active_information() != 'inactive':
            self.connProxy.saveAIStatus('inactive', description)
            set_active_information('inactive')
        

    
    def render(self):
        
        try:
            self._initComponents()
            self._run()
        except FatalError:
            ex = None
            log.error('%s:%s\n%s' % (self.windowID, traceback.format_exc(), ex.errCode))
            globalSession.error = ex
            self.nextWindowID = self.fatalErrorWindowID
        except Exception:
            ex = None
            log.error('%s:%s' % (self.windowID, traceback.format_exc()))
            self.nextWindowID = self.uiErrorWindowID

        self.on_hide()
        return self.nextWindowID



class UserForm(MMForm):
    
    def __init__(self):
        MMForm.__init__(self)

    
    def _run(self):
        while True:
            self.event = self.flash.get(timeout = self.timeoutSec)
            if self.event == None:
                continue
            
            if self.event:
                log.info('[UI Event]: %s.' % self.event)
            
            ctrlID = self.event.get('cid')
            self.on_event(ctrlID)
            if self.windowJump:
                break
            



class CustomerForm(UserForm):
    
    def __init__(self):
        super(CustomerForm, self).__init__()
        self.lstResponseCtrl.extend([
            'ctr_btn_center'])

    
    def on_cancel(self):
        if globalSession.loginCustomer.isLogin:
            globalSession.param['preWindowID'] = self.windowID
            self.nextWindowID = 'MembershipLogoutForm'
        else:
            self.nextWindowID = self.uiErrorWindowID
        self.windowJump = True

    
    def on_back(self):
        if globalSession.loginCustomer.isLogin and self.preWindowID == 'MainForm':
            globalSession.param['preWindowID'] = self.windowID
            self.nextWindowID = 'MembershipLogoutForm'
        else:
            self.nextWindowID = self.preWindowID
        self.windowJump = True

    
    def _initComponents(self):
        super(CustomerForm, self)._initComponents()
        if globalSession.loginCustomer.isLogin:
            self.flash.send('ctr_btn_center', 'show', { })
            if globalSession.loginCustomer.gender == 'male':
                msg = _('Hello Mr. ')
            else:
                msg = _('Hello Ms. ')
            self.flash.send('ctr_btn_center', 'setText', {
                'text': msg + globalSession.loginCustomer.lastName })
        else:
            self.flash.send('ctr_btn_center', 'hide', { })

    
    def on_ctr_btn_center_event(self):
        cmd = self.event.get('param_info').get('cmd')
        if cmd == 'logout':
            if globalSession.loginCustomer.isLogin:
                globalSession.param['preWindowID'] = self.windowID
                self.nextWindowID = 'MembershipLogoutForm'
                self.windowJump = True
            
        elif cmd == 'center':
            if globalSession.loginCustomer.isLogin:
                self.nextWindowID = 'MembershipCenterForm'
                self.windowJump = True
            
        

    
    def on_timeout(self):
        self.on_exit()



class ConfigForm(UserForm):
    
    def __init__(self):
        UserForm.__init__(self)
        self.lstResponseCtrl = [
            'btn_cancel',
            'btn_test_mode_off',
            'btn_test_mode_on',
            'btn_speaker_volume',
            'btn_smart_load',
            'btn_operator_code',
            'btn_quick_load',
            'btn_hdmi_off',
            'btn_hdmi_on',
            'btn_network_diagnosis',
            'btn_poweroff']

    
    def _initComponents(self):
        UserForm._initComponents(self)
        self._setTestModeButton()
        self._setSmartLoadButton()
        self._setHDMIButton()

    
    def _setTestModeButton(self, hide = False):
        if globalSession.param['test_mode']:
            if hide == True:
                self.flash.send('btn_test_mode_off', 'hide', { })
                self.flash.send('btn_test_mode_on', 'hide', { })
                self.flash.send('btn_test_mode_off_disabled', 'hide', { })
                self.flash.send('btn_test_mode_on_disabled', 'show', { })
            else:
                self.flash.send('btn_test_mode_off', 'hide', { })
                self.flash.send('btn_test_mode_on', 'show', { })
                self.flash.send('btn_test_mode_off_disabled', 'hide', { })
                self.flash.send('btn_test_mode_on_disabled', 'hide', { })
        elif hide == True:
            self.flash.send('btn_test_mode_off', 'hide', { })
            self.flash.send('btn_test_mode_on', 'hide', { })
            self.flash.send('btn_test_mode_off_disabled', 'show', { })
            self.flash.send('btn_test_mode_on_disabled', 'hide', { })
        else:
            self.flash.send('btn_test_mode_off', 'show', { })
            self.flash.send('btn_test_mode_on', 'hide', { })
            self.flash.send('btn_test_mode_off_disabled', 'hide', { })
            self.flash.send('btn_test_mode_on_disabled', 'hide', { })

    
    def _setSmartLoadButton(self):
        if self.movieProxy.canQuickLoad() == '0':
            self.flash.send('btn_smart_load', 'hide', { })
        else:
            self.flash.send('btn_smart_load', 'show', { })

    
    def _setHDMIButton(self, hide = False):
        connected = os.path.isfile(HDMI_CONNECT)
        if connected == True:
            if hide == True:
                self.flash.send('btn_hdmi_off', 'hide', { })
                self.flash.send('btn_hdmi_on', 'hide', { })
                self.flash.send('btn_hdmi_off_disabled', 'hide', { })
                self.flash.send('btn_hdmi_on_disabled', 'show', { })
            else:
                self.flash.send('btn_hdmi_off', 'hide', { })
                self.flash.send('btn_hdmi_on', 'show', { })
                self.flash.send('btn_hdmi_off_disabled', 'hide', { })
                self.flash.send('btn_hdmi_on_disabled', 'hide', { })
        elif hide == True:
            self.flash.send('btn_hdmi_off', 'hide', { })
            self.flash.send('btn_hdmi_on', 'hide', { })
            self.flash.send('btn_hdmi_off_disabled', 'show', { })
            self.flash.send('btn_hdmi_on_disabled', 'hide', { })
        else:
            self.flash.send('btn_hdmi_off', 'show', { })
            self.flash.send('btn_hdmi_on', 'hide', { })
            self.flash.send('btn_hdmi_off_disabled', 'hide', { })
            self.flash.send('btn_hdmi_on_disabled', 'hide', { })

    
    def on_btn_cancel_event(self):
        self.on_cancel()

    
    def on_btn_test_mode_off_event(self):
        self.nextWindowID = 'ConfigTestModeForm'
        self.windowJump = True

    
    def on_btn_test_mode_on_event(self):
        self.nextWindowID = 'ConfigTestModeForm'
        self.windowJump = True

    
    def on_btn_speaker_volume_event(self):
        self.nextWindowID = 'ConfigSpeakerVolumeForm'
        self.windowJump = True

    
    def on_btn_smart_load_event(self):
        self.nextWindowID = 'ConfigSmartLoadForm'
        self.windowJump = True

    
    def on_btn_operator_code_event(self):
        self.nextWindowID = 'ConfigOperatorCodeForm'
        self.windowJump = True

    
    def on_btn_hdmi_off_event(self):
        self.nextWindowID = 'ConfigHDMIStateForm'
        self.windowJump = True

    
    def on_btn_hdmi_on_event(self):
        self.nextWindowID = 'ConfigHDMIStateForm'
        self.windowJump = True

    
    def on_btn_network_diagnosis_event(self):
        self.nextWindowID = 'ConfigNetworkDiagnosisForm'
        self.windowJump = True

    
    def on_btn_poweroff_event(self):
        self.nextWindowID = 'ConfigPowerOffForm'
        self.windowJump = True


'\nclass Root:\n    def __init__(self):\n        self.wid = self.__class__.__name__\n\nclass Son(Root):\n    def __init__(self):\n        Root.__init__(self)\n\nclass GrandSon(Son):\n    def __init__(self):\n        Son.__init__(self)\n        print self.wid        \n\n>>> g = GrandSon()\nGrandSon\n'
