# Source Generated with Decompyle++
# File: clisitef.pyc (Python 2.5)

import os
import sys
import time
import datetime
import configparser
import traceback
import socket
import re
import shutil
from . import credit_card
from ctypes import c_char_p, c_short, create_string_buffer, cdll, c_long, pointer, c_int, c_ushort, sizeof
sys.path.append(os.path.abspath(os.path.join(os.path.pardir)))
from .config import *
from . import tools
LPC_TAX_INVOICE_NUMBER = c_char_p('1234')
MDY = time.strftime('%Y%m%d')
LPC_TAX_INVOICE_DATE = c_char_p(MDY)
HMS = time.strftime('%H%M%S')
LPC_TAX_INVOICE_TIME = c_char_p(HMS)
CA_BUFFER = create_string_buffer(20 * 1024 + 1)
I_LOOP_COUNTER = 0
DISPLAY_CHARS = '|/-\\'
DISPLAY_INDEX = 0
CONFIG_PATH = os.path.join(MKC_PATH, 'CliSiTef.ini')
LIB_PATH = os.path.join(USER_ROOT, 'kiosk', 'lib', 'SiTef', 'libclisitef.so')
LOG_PATH = os.path.join(USER_ROOT, 'kiosk/var/log/')
PINPAD_NAME = ''
SITEF_ERR_CODE = {
    -1: 'module not initialized',
    -2: 'operation cancelled by the operator',
    -3: 'invalid modality',
    -4: 'low memory to run the function',
    -5: 'no communication with SiTef,check IP|terminal_id|store_id',
    -6: 'operation cancelled by the user' }

def modify_ini(para):
    global PINPAD_NAME
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_PATH):
        config.read(CONFIG_PATH)
        ipsitef = config.get('SrvCliSiTef', 'ipsitef')
        store_id = config.get('PinPad', 'store_id')
        terminal_id = config.get('PinPad', 'terminal_id')
        if para:
            PINPAD_NAME = para['kiosk_id']
            if ipsitef != para['ip']:
                config.set('SrvCliSiTef', 'ipsitef', para['ip'])
                ipsitef = para['ip']
            
            if store_id != para['store_id']:
                config.set('PinPad', 'store_id', para['store_id'])
                store_id = para['store_id']
            
            if terminal_id != para['terminal_id']:
                config.set('PinPad', 'terminal_id', para['terminal_id'])
                terminal_id = para['terminal_id']
            
        
        config.set('Geral', 'DataEmAmbienteDeDesenvolvimento', MDY)
        config.write(open(CONFIG_PATH, 'r+'))
        return (ipsitef, store_id, terminal_id)
    else:
        print('Need file ClisiTef.ini')


def fmtMoney(money):
    newMoney = '%.2f' % round(float(money), 2)
    return newMoney


class CliSiTef(credit_card.Trade):
    
    def __init__(self, para, kiosk_id, upgServer, upgPort, upgBaseurl, upgTrsMode = 'LIVE'):
        super(CliSiTef, self).__init__(kiosk_id, upgServer, upgPort, upgBaseurl, upgTrsMode)
        self.sock = None
        self.log = None
        self.lpc_si_tef_ip = ''
        self.lpc_store_id = ''
        self.lpc_terminal_id = ''
        self.log = tools.getLog('CliSiTef.log')
        (self.lpc_si_tef_ip, self.lpc_store_id, self.lpc_terminal_id) = modify_ini(para)
        self.zdata = { }
        self.is_test = False

    
    def __del__(self):
        ''' '''
        del self.log

    
    def regular_trace_file(self):
        
        try:
            pattern = re.compile('CliSiTef.*.dmp|Erro.*.dmp|CliSiTef.*.txt')
            mkc_files = os.listdir(MKC_PATH)
            for f in mkc_files:
                if pattern.match(f):
                    shutil.move(os.path.join(MKC_PATH, f), LOG_PATH)
                
            
            for f in os.listdir(LOG_PATH):
                if pattern.match(f):
                    ct = os.stat(os.path.join(LOG_PATH, f)).st_ctime
                    today = datetime.date.today().strftime('%Y-%m-%d')
                    (year, month, day) = today.split('-')
                    t1 = datetime.datetime(int(year), int(month), int(day))
                    ct = time.strftime('%Y-%m-%d')
                    (year, month, day) = ct.split('-')
                    t2 = datetime.datetime(int(year), int(month), int(day))
                    if (t1 - t2).days > 30:
                        os.remove(os.path.join(LOG_PATH, f))
                        self.log.info('removed %s' % f)
                    
                
        except Exception as ex:
            self.log.error('Regular Sitef log error %s' % ex)


    
    def _extracharge(self, acctId, cardNum, expDate, nameOnCard, amount, track2 = '', track1 = ''):
        if amount and float(amount) == 0:
            self.log.info("recharge amount is zero,needn't extracharge")
            return ('0', '', '')
        
        trsCode = ''
        trsMsg = ''
        oid = ''
        
        try:
            self.log.info('extra charge:acctId %s,cardNum %s,nameOnCard %s, amount %s' % (acctId, cardNum, nameOnCard, amount))
            trsType = 'SALE'
            (trsCode, trsMsg, oid) = credit_card.Trade.trade(self, acctId, trsType, cardNum, expDate, nameOnCard, amount, '', '')
            self.log.info('extra charge result: trsCode %s trsMsg %s oid %s' % (trsCode, trsMsg, oid))
        except credit_card.UpgInternalError as ex:
            trsCode = '-1'
            m = 'Internal Error when extracharge from UPG: %s' % ex
            trsMsg = m
            self.log.error(m)
        except Exception as ex:
            trsCode = '-2'
            m = 'Local Error when extracharge from UPG: %s' % ex
            trsMsg = m
            self.log.error(m)

        return (trsCode, trsMsg, oid)

    
    def _cancel(self, acctId, cardNum, expDate, nameOnCard, amount, track2 = '', track1 = '', oid = ''):
        '''
        cancel amount must equal to sale amount
        '''
        trsCode = ''
        trsMsg = ''
        
        try:
            self.log.info('cancel: acctId %s, cardNum %s, nameOnCard %s, amount %s, oid %s' % (acctId, cardNum, nameOnCard, amount, oid))
            trsType = 'CREDIT'
            (trsCode, trsMsg, oid) = credit_card.Trade.trade(self, acctId, trsType, cardNum, expDate, nameOnCard, amount, track2, track1, oid)
            self.log.info('cancel result: trsCode %s trsMsg %s oid %s' % (trsCode, trsMsg, oid))
        except credit_card.UpgInternalError as ex:
            trsCode = '-1'
            m = 'Internal Error when cancel from UPG: %s' % ex
            trsMsg = m
            self.log.error(m)
        except Exception as ex:
            trsCode = '-2'
            m = 'Local Error when cancel from UPG: %s' % ex
            trsMsg = m
            self.log.error(m)

        return (trsCode, trsMsg, oid)

    
    def refund(self, acctId, cardNum, expDate, nameOnCard, charge_amount, refund_amount, resultCode = 0, oid = '', track2 = '', track1 = ''):
        '''
        return trsCode_refund,trsMsg_refund

        trsCode_refund  0  success
                        -1 cancel failed
                        -2 charge failed
        '''
        trsCode_cancel = ''
        trsMsg_cancel = ''
        trsCode_sale = ''
        trsMsg_sale = ''
        trsCode_refund = -2
        trsMsg_refund = ''
        excharge_amount = fmtMoney(float(charge_amount) - float(refund_amount))
        self.log.info('refund: acctId %s, cardNum %s, nameOnCard %s, charge_amount %s,refund_amount %s, oid %s' % (acctId, cardNum, nameOnCard, charge_amount, refund_amount, oid))
        
        try:
            if resultCode in (-1, 0):
                '\n                need cancel and extracharge to finish refund\n                '
                r1 = self._cancel(acctId, cardNum, expDate, nameOnCard, charge_amount, track2, track1, oid)
                (trsCode_cancel, trsMsg_cancel, oid) = r1
                if trsCode_cancel == '0':
                    (trsCode_sale, trsMsg_sale, oid) = self._extracharge(acctId, cardNum, expDate, nameOnCard, excharge_amount)
                    if trsCode_sale == '0':
                        trsCode_refund = 0
                        trsMsg_refund = 'refund success'
                    else:
                        trsMsg_refund = 'recharge failed in refund'
                        trsCode_refund = -2
                else:
                    trsCode_refund = -1
                    trsMsg_refund = 'cancel failed in refund'
                    self.log.info('refund result trsCode %s trsMsg %s' % (trsCode_refund, trsMsg_refund))
                    return (trsCode_refund, trsMsg_refund)
            elif resultCode == -2:
                '\n                last time successfully cancel,but failed  to extracharge\n                '
                (trsCode_sale, trsMsg_sale, oid) = self._extracharge(acctId, cardNum, expDate, nameOnCard, charge_amount)
                if trsCode_sale != '0':
                    trsCode_refund = -2
                    trsMsg_refund = 'recharge failed in refund'
                else:
                    trsMsg_refund = 'refund success'
                    trsCode_refund = 0
        except Exception as ex:
            self.log.error(ex)
            self.log.info('refund result trsCode %s trsMsg %s' % (trsCode_refund, trsMsg_refund))

        return (trsCode_refund, trsMsg_refund)

    
    def sync_info_upg(self, acctId, amount):
        trsType = 'SALE'
        oid = '%s--%s' % (self.zdata.get('trans_time', '')[4:], self.zdata.get('trans_doc', ''))
        for i in range(3):
            
            try:
                r = credit_card.Trade.trade(self, acctId, trsType, self.zdata.get('card_sha1', ''), self.zdata.get('card_expdate', ''), self.zdata.get('card_name', ''), amount, oid = oid)
            except credit_card.UpgInternalError as ex:
                trsCode = '-1'
                m = 'Internal Error when sale from UPG: %s' % ex
                trsMsg = m
                self.log.error(m)
            except Exception as ex:
                trsCode = '-2'
                m = 'Local Error when sale from UPG: %s' % ex
                trsMsg = m
                self.log.error(m)

        

    
    def sale(self, acctId, amount, test = False):
        '''
        return dict {" "}
        '''
        
        try:
            self.is_test = test
            self.amount = fmtMoney(amount)
            self.zdata['amount'] = amount
            self.log.info(' Transaction Start Now '.center(90, '='))
            libclisitef = cdll.LoadLibrary(LIB_PATH)
            sts = libclisitef.ConfiguraIntSiTefInterativo(self.lpc_si_tef_ip, self.lpc_store_id, self.lpc_terminal_id, c_short(0))
            pin = libclisitef.VerificaPresencaPinPad()
            self.log.info('pinpad connect kiosk status %s' % pin)
            if pin != 1:
                msg = "Can't find any pinpad,check serial port"
                self.log.error('err %d connect pinpad %s' % (pin, msg))
                self.zdata['msg'] = msg
                return self.zdata
            
            if not PINPAD_NAME:
                pass
            libclisitef.EscreveMensagemPermanentePinPad('Welcome')
            if sts != 0:
                msg = 'Err %d initializing the DLL.' % sts
                self.log.error(msg)
                self.zdata['msg'] = msg
                return self.zdata
            
            result = self.do_transaction(libclisitef, self.amount)
            msg = ('result:', result)
            self.log.info(msg)
            self.zdata['status'] = result
            if result == 0:
                confirm = c_short(1)
                final = libclisitef.FinalizaTransacaoSiTefInterativo(confirm, LPC_TAX_INVOICE_NUMBER, LPC_TAX_INVOICE_DATE, LPC_TAX_INVOICE_TIME)
                if final == 0:
                    msg = 'success'
                    self.zdata['status'] = result
                    self.sync_info_upg(acctId, amount)
                    self.regular_trace_file()
                else:
                    self.zdata['status'] = final
                    msg = 'FinalizaTransacaoSiTefInterativo failed'
            elif result > 0:
                msg = 'Transaction denied with return code = %d' % result
                self.log.error(msg)
            elif result in range(-6, 0):
                msg = 'Pinpad init error code:%s %s' % (result, SITEF_ERR_CODE[result])
                self.log.error(msg)
            else:
                msg = 'Transaction denied by dll or by the cash operator with return code = %d' % result
                self.log.error(msg)
            self.zdata['msg'] = msg
        except Exception:
            self.log.error(traceback.format_exc())
        finally:
            if not PINPAD_NAME:
                pass
            libclisitef.EscreveMensagemPermanentePinPad('Welcome')
            msg = 'ZDATA:%s' % self.zdata
            self.log.info(msg)

        return self.zdata

    
    def do_transaction(self, libclisitef, amount):
        trs_type = c_long(0)
        amount = c_char_p(amount)
        operador = c_char_p('Operator')
        param_adic = c_char_p('SementeHash=8234567893144456')
        product = c_char_p('Product')
        result = libclisitef.IniciaFuncaoSiTefInterativo(trs_type, amount, LPC_TAX_INVOICE_NUMBER, LPC_TAX_INVOICE_DATE, LPC_TAX_INVOICE_TIME, operador, param_adic, product)
        if result != 10000:
            return result
        
        i_next_cmd = pointer(c_int(0))
        ul_tipo_campo = pointer(c_long(0))
        us_min_size = pointer(c_ushort(0))
        us_max_size = pointer(c_ushort(0))
        i_result = c_int(0)
        while True:
            result = libclisitef.ContinuaFuncaoSiTefInterativo(i_next_cmd, ul_tipo_campo, us_min_size, us_max_size, CA_BUFFER, sizeof(CA_BUFFER), i_result)
            if result != 10000:
                break
            
            if i_next_cmd.contents.value == 0:
                i_result = self.receive_data(ul_tipo_campo.contents, CA_BUFFER)
            else:
                i_result = self.collect_data(i_next_cmd.contents, ul_tipo_campo.contents, us_min_size.contents, us_max_size.contents, CA_BUFFER, CA_BUFFER)
        return result

    
    def collect_data(self, i_command, ul_tipo_campo, us_min_size, us_max_size, lpc_input_data, lpc_output_data):
        global I_LOOP_COUNTER, I_LOOP_COUNTER, DISPLAY_INDEX, DISPLAY_INDEX
        i_command = i_command.value
        if i_command != 23:
            I_LOOP_COUNTER = 0
        
        if i_command in (1, 2, 3, 4):
            msg = 'Display Message:[%s]' % lpc_input_data.value
            if lpc_input_data.value.find('Insira ou passe o cartao na leitora') != -1 and self.is_test:
                sys.exit(0)
            
            self.log.info(msg)
            self.choice_question = repr(lpc_input_data.value)
            return 0
        elif i_command in (11, 12, 13, 14):
            msg = 'Clear Display: [%d]\n' % i_command
            self.log.info(msg)
            return 0
        elif i_command == 37:
            msg = 'Get confirmation on PinPad:'
            self.log.info(msg)
        elif i_command == 20:
            self.log.info(lpc_input_data.value)
            a = '1'
            lpc_output_data.value = chr(ord(a) - 1)
            return 0
        elif i_command == 21:
            a = '0'
            msg = '%s:%s' % (i_command, self.choice_question)
            self.log.info(msg)
            if self.choice_question.find('Selecione a forma de pagamento') != -1 and lpc_input_data.value.find('Cartao de Credito') != -1:
                a = '3'
            elif self.choice_question.find('Selecione a forma de pagamento') != -1 and lpc_input_data.value.find('A Vista') != -1:
                a = '1'
            elif self.choice_question.find('Selecione o tipo do Cartao de Credito') != -1:
                a = '1'
            
            lpc_output_data.value = chr(ord(a))
            return 0
        elif i_command == 22:
            '\n            if lpc_input_data.value.find("Homologacao CliSiTef") == -1:\n                print "success"\n                return 0\n            elif lpc_input_data.value.find("Sem conexao SiTef") == -1:\n                print "connect sitef failed"\n                return 0\n            '
            msg = '%s:%s' % (i_command, lpc_input_data.value)
            self.log.info(msg)
            if lpc_input_data.value.find('Cartao com chip. Insira o cartao') != -1:
                msg = 'card error,plz swipe'
                self.log.info(msg)
                return -2
            
            if lpc_input_data.value.find('Cartao Removido') != -1:
                msg = 'Cartao Removido'
                self.log.info(msg)
                return 2
            elif lpc_input_data.value.find('Sem conexao SiTef') != -1:
                return -1
            else:
                return 0
        elif i_command == 23:
            time.sleep(0.1)
            I_LOOP_COUNTER += 1
            msg = '%s [%d]' % (DISPLAY_CHARS[DISPLAY_INDEX], I_LOOP_COUNTER)
            self.log.info(msg)
            DISPLAY_INDEX += 1
            if DISPLAY_INDEX == len(DISPLAY_CHARS):
                DISPLAY_INDEX = 0
            
            if I_LOOP_COUNTER > 30:
                return -1
            
            return 0
        elif i_command == 30:
            a = input('%s:\n' % lpc_input_data.value)
            if a == 'b':
                return 1
            elif a == 'c':
                return 2
            else:
                lpc_output_data.value = a
                return 0
        elif i_command in (31, 32, 33, 34, 35, 38):
            msg = 'Command: %s, TipoCampo: %s' % (i_command, ul_tipo_campo.value)
            self.log.info(msg)
            return 0
        else:
            msg = 'Command: %s, TipoCampo: %s' % (i_command, ul_tipo_campo.value)
            self.log.info(msg)

    
    def receive_data(self, ul_tipo_campo, lpc_input_data):
        msg = ''
        if ul_tipo_campo.value == 1:
            msg = 'Finalization data: [%s]' % lpc_input_data.value
        elif ul_tipo_campo.value == 121:
            msg = 'Client Receipt:\n%s' % lpc_input_data.value
        elif ul_tipo_campo.value == 122:
            msg = 'Cashier Receipt:\n%s' % lpc_input_data.value
        elif ul_tipo_campo.value == 131:
            msg = 'Institution ID:%s' % lpc_input_data.value
        elif ul_tipo_campo.value == 132:
            msg = 'Card typeo:%s' % lpc_input_data.value
        elif ul_tipo_campo.value == 136:
            msg = '6 first positions:%s' % lpc_input_data.value
            self.zdata['six_first_num'] = lpc_input_data.value
        elif ul_tipo_campo.value == 123:
            msg = '#Receipt#%s' % lpc_input_data.value
        elif ul_tipo_campo.value == 2041:
            self.zdata['card_sha1'] = lpc_input_data.value
        elif ul_tipo_campo.value == 2022:
            self.zdata['card_expdate'] = lpc_input_data.value
        elif ul_tipo_campo.value == 2021:
            self.zdata['last_four_num'] = lpc_input_data.value[-4:]
        elif ul_tipo_campo.value == 105:
            self.zdata['trans_time'] = lpc_input_data.value
            msg = 'trans_time:%s' % lpc_input_data.value
        elif ul_tipo_campo.value == 134:
            self.zdata['trans_doc'] = lpc_input_data.value
            msg = 'trans_doc:%s' % lpc_input_data.value
        elif ul_tipo_campo.value == 2023:
            self.zdata['cc_name'] = lpc_input_data.value
        else:
            msg = 'TipoCampo= %s, Contents= %s' % (ul_tipo_campo.value, lpc_input_data.value)
        self.log.info(msg)
        return 0


if __name__ == '__main__':
    para = { }
    clisitef = CliSiTef(para, 'S250-911', '127.0.0.1', 10000, '')
    clisitef.sale('', 3, test = True)

