# Source Generated with Decompyle++
# File: guiShowAllSlotForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiUnloadBySlotForm.py
Unload By Slot
Screen ID: U12

Change Log:

'''
import os
import traceback
import config
from mcommon import *
from guiBaseForms import UserForm
log = initlog('guiShowAllSlotForm')

class ShowAllSlotForm(UserForm):
    
    def __init__(self):
        UserForm.__init__(self)
        self.windowID = 'ShowAllSlotForm'
        self.nextWindowID = 'AdminMainForm'
        self.screenID = 'U12'
        self.timeoutSec = 60
        self.action = ''
        self.ac_slot_id = ''
        self.current_select = 'all'
        self.cur_code = ''
        self.preWindowID = 'AdminMainForm'
        self.uiErrorWindowID = 'AdminMainForm'
        self.action_list = [
            'load',
            'unload',
            'mark as bad',
            'clear']
        self.lstResponseCtrl = [
            'btn_logout',
            'btn_back',
            'btn_cancel',
            'btn_icon_keyboard',
            'ShowAllSlotForm_ctr_num_keyboard',
            'all_slot_qtn',
            'ctr_slot_list',
            'ShowAllSlotForm_ctr_message_box']

    
    def _initComponents(self):
        UserForm._initComponents(self)
        self.cur_code = globalSession.param.get('priv')
        log.info('show all slots %s ' % self.cur_code)
        globalSession.param['load_one_slot'] = ''
        self.action = ''
        self.ac_slot_id = ''
        if self.current_select:
            self.reset_detail(self.current_select)
        else:
            self.reset_detail('all')

    
    def reset_detail(self, _filter = 'all'):
        (s_qtn, lstSlots) = self.connProxy.get_all_slots_status(_filter, self.cur_code)
        log.info('reset_detail %s' % lstSlots)
        self.flash.send('ctr_slot_list', 'setSlotList', {
            'ctr_slot_list': lstSlots })
        self.flash.send('all_slot_qtn', 'set_label_text', {
            'text': s_qtn })
        self.flash.send('all_slot_qtn', 'set_current_select', {
            'name': _filter })

    
    def on_all_slot_qtn_event(self):
        self.current_select = self._getEventParam('all_slot_qtn', 'info')
        self.reset_detail(self.current_select)

    
    def on_btn_logout_event(self):
        self.on_exit()

    
    def on_btn_back_event(self):
        self.on_back()

    
    def on_btn_cancel_event(self):
        self.on_cancel()

    
    def on_btn_icon_keyboard_event(self):
        self.flash.send('%s_ctr_num_keyboard' % self.windowID, 'show', { })

    
    def on_ShowAllSlotForm_ctr_num_keyboard_event(self):
        eventType = self._getEventParam('ShowAllSlotForm_ctr_num_keyboard', 'type')
        if eventType == 'click':
            pass
        elif eventType == 'ok':
            slotID = self._getEventParam('ShowAllSlotForm_ctr_num_keyboard', 'val')
            self.reset_detail(slotID)
        

    
    def on_ctr_slot_list_event(self):
        '''
        action  [ "Clear", "Mark as Bad", "Unload", "Load" ]
        '''
        action_dic = {
            'clear': 'clear bad',
            'mark as bad': 'mark as bad',
            'load': 'Load',
            'unload': 'Unload' }
        globalSession.disc = Disc()
        self.action = ''
        info_msg = self._getEventParam('ctr_slot_list', 'info')
        (slot_id, action, rfid) = info_msg.split('|')
        globalSession.disc.rfid = rfid
        globalSession.disc.slotID = slot_id
        if action:
            msg = _('Are you sure to %s for %s?' % (action_dic.get(action, ''), slot_id))
            self.flash.send('%s_ctr_message_box' % self.windowID, 'show', {
                'message': msg,
                'type': 'confirm' })
            self.action = action
            self.ac_slot_id = slot_id
        

    
    def on_ShowAllSlotForm_ctr_message_box_event(self):
        if self._getEventParam('ShowAllSlotForm_ctr_message_box', 'val') == 'yes':
            if self.action == 'unload':
                globalSession.shoppingCart.addDisc(globalSession.disc)
                self.nextWindowID = 'UnloadEjectForm'
                self.windowJump = True
            elif self.action == 'load':
                globalSession.param['load_one_slot'] = self.ac_slot_id
                self.nextWindowID = 'AdminMainForm'
                self.windowJump = True
            elif self.action in [
                'clear',
                'mark as bad']:
                self.connProxy.change_slots_state(self.action, self.ac_slot_id)
            
            self.reset_detail(self.current_select)
        


