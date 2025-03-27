# Source Generated with Decompyle++
# File: topup_for_cerepay_thread.pyc (Python 2.5)

'''
This file is used to settle the failure of topup CerePay in the queue.
The failure maybe caused by the unstable network or something else.

Change Log:
    2011-01-11 Created by Tim

'''
import time
import threading
from . import upg_proxy
from . import tools

class TopupCerePayThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self, name = 'TOPUP_CERESON_THREAD')

    
    def run(self):
        '''
        '''
        log = tools.getLog('topup_cereson_thread.log', 'THREAD')
        while True:
            
            try:
                proxy = upg_proxy.UPGProxy.getInstance()
                topups = proxy._get_failed_cerepay_topup()
                if topups:
                    cpCfg = proxy.getCerePayCfg()
                    if not cpCfg:
                        raise Exception('UPG account DOESNOT support CerePay')
                    
                    for topup in topups:
                        
                        try:
                            res = proxy.topup_cerepay(cpCfg['MERCHANTID'], cpCfg['PASSWORD'], cpCfg['CURRENCY'], topup['cerepay_member_id'], proxy._getAmount(topup['amount']), topup['oid'])
                            if str(res['errCode']) != str(topup['state']):
                                proxy._update_cerepay_topup_queue(topup['id'], res['errCode'], res['errMsg'])
                        except Exception:
                            ex = None
                            log.error('process %s: %s' % (topup, ex))

                    
                
                del proxy
            except Exception:
                ex = None
                log.error('process: %s' % ex)

            time.sleep(600)



def main():
    topupThread = TopupCerePayThread()
    topupThread.start()

if __name__ == '__main__':
    main()

