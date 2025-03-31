# Source Generated with Decompyle++
# File: guiCerepayTopupErrorForm.pyc (Python 2.5)

import time
from guiBaseForms import CustomerForm
from mcommon import *
from proxy.upg_proxy import UPGProxy
log = initlog('CerepayTopupErrorForm')

class CerepayTopupErrorForm(CustomerForm):
    
    def __init__(self):
        super(CerepayTopupErrorForm, self).__init__()
        self.nextWindowID = 'CerepayCenterForm'
        self.preWindowID = 'CerepayTopupSwipeChinPinForm'
        self.uiErrorWindowID = 'CerepayCenterForm'
        self.timeoutSec = 180
        self.screenID = 'M10'
        self.lstResponseCtrl.extend([
            'btn_back'])
        self._CerepayTopupErrorForm__upg_proxy = UPGProxy()

    
    def _initComponents(self):
        super(CerepayTopupErrorForm, self)._initComponents()

    
    def _run(self):
        
        try:
            need_wait_time = 15 * 60
            start_time = time.time()
            while True:
                (status, trs_uuid) = self._CerepayTopupErrorForm__upg_proxy.get_topup_status_by_queue_id(globalSession.cerepayTopupQueueID)
                if not status and time.time() - start_time < need_wait_time:
                    time.sleep(10)
                    continue
                else:
                    break
            if not status:
                self.nextWindowID = 'CerepayTopupReceiptForm'
                self.windowJump = True
                globalSession.isCerepayCardInfoDirty = True
                globalSession.cerepayTopupTransactionUUID = trs_uuid
                return None
        except Exception as ex:
            pass
        
        self.on_btn_back_event()
        return None


