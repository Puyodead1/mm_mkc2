# Source Generated with Decompyle++
# File: guiMembershipTransactionForm.pyc (Python 2.5)

'''
Created on 2010-7-9
@author: andrew.lu@cereson.com
'''
from mcommon import *
from guiBaseForms import CustomerForm
log = initlog('MembershipTransactionForm')

class MembershipTransactionForm(CustomerForm):
    
    def __init__(self):
        super(MembershipTransactionForm, self).__init__()
        self.screenID = 'M4'
        self.preWindowID = 'MembershipCenterForm'
        self.uiErrorWindowID = 'MainForm'
        self.timeoutSec = 180
        self.lstResponseCtrl.extend([
            'btn_back'])

    
    def _initComponents(self):
        super(MembershipTransactionForm, self)._initComponents()
        if globalSession.loginCustomer.ccNum:
            text = globalSession.loginCustomer.ccNum[-4:]
        else:
            i = globalSession.loginCustomer.email.index('@')
            text = globalSession.loginCustomer.email[:i]
        self.flash.send('txt_msg', 'setText', {
            'text': text })
        trans = []
        if globalSession.loginCustomer.isLogin == True:
            alltrans = self.connProxy.getTransactionListForMember(globalSession.loginCustomer.allCcIds)
            for tran in alltrans:
                data = { }
                data['movie_pic'] = getPicFullPath(tran['movie_pic'])
                data['movie_title'] = tran['movie_title']
                data['price'] = '%.2f' % round(tran['price'], 2)
                data['state'] = tran['state']
                trans.append(data)
            
        
        self.flash.send('ctr_disc_list', 'setList', {
            'ctr_disc_list': trans })

    
    def on_btn_back_event(self):
        self.on_back()


