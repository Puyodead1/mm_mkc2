# Source Generated with Decompyle++
# File: guiCerepayTopupMainForm.pyc (Python 2.5)

from mcommon import *
from guiBaseForms import CustomerForm
from proxy.upg_proxy import UPGProxy
log = initlog('CerepayTopupMainForm')

class CerepayTopupMainForm(CustomerForm):
    
    def __init__(self):
        super(CerepayTopupMainForm, self).__init__()
        self.screenID = 'M7'
        self.preWindowID = 'CerepayCenterForm'
        self.uiErrorWindowID = 'CerepayCenterForm'
        self.timeoutSec = 180
        self.lstResponseCtrl.extend([
            self.number_keyboard_string,
            'btn_cancel',
            'btn_back'])

    
    def _initComponents(self):
        super(CerepayTopupMainForm, self)._initComponents()
        self._CerepayTopupMainForm__show_num_keyboard()

    
    def number_keyboard_string(self):
        return '%s_ctr_num_keyboard' % self.windowID

    number_keyboard_string = property(number_keyboard_string)
    
    def __show_num_keyboard(self):
        self.flash.send(self.number_keyboard_string, 'show', { })

    
    def __close_num_keyboard(self):
        self.flash.send(self.number_keyboard_string, 'close', { })

    
    def on_CerepayTopupMainForm_ctr_num_keyboard_event(self):
        event_type = self._getEventParam(self.number_keyboard_string, 'type')
        if event_type == 'ok':
            globalSession.cerepayTopupAmount = float(self._getEventParam(self.number_keyboard_string, 'val'))
            if globalSession.isUsingChipnPin:
                self.nextWindowID = 'CerepayTopupSwipeChinPinForm'
                self.windowJump = True
            else:
                self.nextWindowID = 'CerepayTopupSwipeCreditCardForm'
                self.windowJump = True
        elif event_type == 'close':
            self.on_btn_cancel_event()
        

    
    def on_btn_cancel_event(self):
        self.nextWindowID = 'CerepayCenterForm'
        self.windowJump = True

    
    def on_btn_back_event(self):
        self.on_btn_cancel_event()


