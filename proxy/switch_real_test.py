# Source Generated with Decompyle++
# File: switch_real_test.pyc (Python 2.5)

'''
    Change Log:
        2009-02-25 Created by Kitch
            Switch Real Server 2 Test Server and Reverse

'''
__VERSION_ = '0.02'
import os
import sys
import shutil
from .conn_proxy import ConnProxy
from .config import USER_ROOT

def switch(toEnvironment = ''):
    TESTENV = os.path.join(USER_ROOT, 'kiosk', 'var', 'TEST.ENV')
    REALENV = os.path.join(USER_ROOT, 'kiosk', 'var', 'REAL.ENV')
    if not toEnvironment:
        print('Check the current environment...')
        environment = 'real'
        if os.path.exists(TESTENV):
            environment = 'test'
        elif os.path.exists(REALENV):
            environment = 'real'
        
        print('Current Mode: %s environment' % environment)
        if environment == 'real':
            toEnvironment = 'test'
        else:
            toEnvironment = 'real'
    
    print('Switching to %s environment...' % toEnvironment)
    fromMKA = os.path.join(USER_ROOT, 'kiosk', 'bin', 'mka.py.%s' % toEnvironment)
    toMKA = os.path.join(USER_ROOT, 'kiosk', 'bin', 'mka.py')
    shutil.copy(fromMKA, toMKA)
    print('cp %s to %s done' % (fromMKA, toMKA))
    fromDCE = os.path.join(USER_ROOT, 'kiosk', 'lib', 'pyDCE', 'DCEConfig.py.%s' % toEnvironment)
    toDCE = os.path.join(USER_ROOT, 'kiosk', 'lib', 'pyDCE', 'DCEConfig.py')
    shutil.copy(fromDCE, toDCE)
    print('cp %s to %s done' % (fromDCE, toDCE))
    if os.path.exists(TESTENV):
        os.remove(TESTENV)
    
    if os.path.exists(REALENV):
        os.remove(REALENV)
    
    os.system('touch %s' % os.path.join(USER_ROOT, 'kiosk', 'var', '%s.ENV' % toEnvironment.upper()))
    proxy = ConnProxy.getInstance()
    params = { }
    if toEnvironment == 'real':
        params['upg_acct_id'] = ''
        params['upg_url'] = 'upg1.waven.com/upg/agent/upgAgent'
    else:
        params['upg_acct_id'] = '2000'
        params['upg_url'] = 'cereson.gicp.net/upgtest/agent/upgAgent'
    proxy.setConfig(params)
    print('Change config table in mkc.db done')
    print('Switch to %s environment done' % toEnvironment)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        switch()
    elif sys.argv[1].lower() in ('-t', '-test'):
        switch('test')
    elif sys.argv[1].lower() in ('-r', '-real'):
        switch('real')
    elif sys.argv[1].lower() in ('-h', '-help'):
        print('./switch_real_test.py [-t|-test]|[-r|-real]')
    else:
        print('./switch_real_test.py [-t|-test]|[-r|-real]')

