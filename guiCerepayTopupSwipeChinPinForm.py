# Source Generated with Decompyle++
# File: guiCerepayTopupSwipeChinPinForm.pyc (Python 2.5)

from guiCerepayTopupSwipeCardBaseForm import CerepayTopupSwipeCardBaseForm
from mcommon import *
from proxy.upg_proxy import UPGProxy
log = initlog('CerepayTopupSwipeChinPinForm')

class CerepayTopupSwipeChinPinForm(CerepayTopupSwipeCardBaseForm):
    
    def __init__(self):
        super(CerepayTopupSwipeChinPinForm, self).__init__()
        self.screenID = 'M8'

    
    def _initComponents(self):
        super(CerepayTopupSwipeChinPinForm, self)._initComponents()

    
    def on_CerepayTopupSwipeChinPinForm_ctr_message_box_event(self):
        if self._getEventParam(self._ctr_msg_box_string, 'val') == 'yes':
            self.on_back()
        


