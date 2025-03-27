# Source Generated with Decompyle++
# File: chip_n_pin.pyc (Python 2.5)

'''
##  Used by S250 kiosk for the gateway CHIP PIN(EVT) in Europe.
##
##  Response Status:
##      1 Approved Online
##      2 Approved Offline
##      3 Approved Manual (Referral)
##      4 Declined Online
##      5 Declined Offline
##      9 Cancelled
##      16 Capture Card, declined online
##      19 Transaction Aborted
##      20 Pre sales completed
##      21 Pre sales rejected
##      22 Card number not matched
##      23 Expiry date not matched
##      24 Invalid transaction state
##      25 Transaction not valid for requested operation
##      26 Invalid PGTR
##      27 Invalid Merchant
##      28 Invalid Terminal
##      29 Merchant status is not valid
##      30 Invalid card number
##      31 Expired Card
##      32 Pre valid card
##      33 Invalid issue number
##      34 Invalid card expiry date
##      35 Invalid start date
##      36 Card not accepted
##      37 Transaction not allowed
##      38 Cash back not allowed
##      42 Status Busy
##      43 Status Not Busy
##      50 AVS details required
##      60 Card activated (Gift card activation)
##      61 Card already activated (Gift card activation)
##      62 Card not activated (For Gift Card)
##      63 Hot Listed Card (for Gift Card)
##      64 Insufficient Balance ( for Gift Card)
##      65 Invalid Security Code ( for Gift Card)
##  Change Log:
##      2010-06-22 Modified by Tim
##          Change the status 2(Approved Offline) for SALE or CANCEL to DECLINED.
##      2010-05-14 Created by Tim
##
'''
import socket
from . import tools
from . import credit_card
RESPONSE_MSG = {
    '1': 'Approved Online',
    '2': 'Approved Offline',
    '3': 'Approved Manual (Referral)',
    '4': 'Declined Online',
    '5': 'Declined Offline',
    '9': 'Cancelled',
    '16': 'Capture Card, declined online',
    '19': 'Transaction Aborted',
    '20': 'Pre sales completed',
    '21': 'Pre sales rejected',
    '22': 'Card number not matched',
    '23': 'Expiry date not matched',
    '24': 'Invalid transaction state',
    '25': 'Transaction not valid for requested operation',
    '26': 'Invalid PGTR',
    '27': 'Invalid Merchant',
    '28': 'Invalid Terminal',
    '29': 'Merchant status is not valid',
    '30': 'Invalid card number',
    '31': 'Expired Card',
    '32': 'Pre valid card',
    '33': 'Invalid issue number',
    '34': 'Invalid card expiry date',
    '35': 'Invalid start date',
    '36': 'Card not accepted',
    '37': 'Transaction not allowed',
    '38': 'Cash back not allowed',
    '42': 'Status Busy',
    '43': 'Status Not Busy',
    '50': 'AVS details required',
    '60': 'Card activated (Gift card activation)',
    '61': 'Card already activated (Gift card activation)',
    '62': 'Card not activated (For Gift Card)',
    '63': 'Hot Listed Card (for Gift Card)',
    '64': 'Insufficient Balance ( for Gift Card)',
    '65': 'Invalid Security Code ( for Gift Card)' }

class ChipNPin(credit_card.Trade):
    
    def __init__(self, kioskId, upgServer, upgPort, upgBaseUrl, upgTrsMode = 'LIVE', host = '127.0.0.1', EVTPort = 10000, timeout = 120):
        ''' '''
        super(ChipNPin, self).__init__(kioskId, upgServer, upgPort, upgBaseUrl, upgTrsMode)
        self.host = host
        self.EVTPort = EVTPort
        self.timeout = timeout
        self.sock = None
        self.log = None
        self.log = tools.getLog('chip_n_pin.log')

    
    def __del__(self):
        ''' '''
        del self.log

    
    def sendReq(self, req):
        ''' Send request and get response.
        @param req(list):
        @return resp(dict):
        '''
        resp = { }
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            
            try:
                self.log.info('new req: %s' % req)
                self.sock.connect((self.host, self.EVTPort))
                self.sock.settimeout(self.timeout)
                self.sock.send(self.formReq(req))
                res = self.recvall()
                self.log.info('new res: %s' % res)
                resp = self.parseResp(res)
            finally:
                self.sock.close()

        except Exception:
            ex = None
            self.log.error('error when process req(%s): %s' % (req, ex))

        return resp

    
    def recvall(self):
        ''' Receive all response from the EVT.
        @return resp(str)
        '''
        resp = self.sock.recv(1024)
        while not resp.strip().endswith('99=0') or not resp:
            resp += self.sock.recv(1024)
        return resp

    
    def formReq(self, req):
        ''' Form request.
        @param req(list):
        @return result(str):
        '''
        return '\r\n'.join(req)

    
    def parseResp(self, resp):
        ''' Parse response.
        @param resp(str):
        @return res(dict):
        '''
        res = { }
        for r in resp.split('\n'):
            if r.strip():
                t = r.split('=')
                res[str(t[0])] = '='.join(t[1:])
            
        
        return res

    
    def isBusy(self):
        ''' Check if the EVT is busy.
        @return busy(bool)
        '''
        req = []
        req.append('2=34')
        req.append('99=0')
        resp = self.sendReq(req)
        busy = True
        if str(resp.get('3', '42')) == '43':
            busy = False
        
        return busy

    
    def sale(self, upgAcctId, trsRef, amount):
        ''' Sale with EVT.
        @param amount(float)
        @return
        '''
        result = { }
        result['busy'] = self.isBusy()
        if not result['busy']:
            req = []
            req.append('1=%s' % trsRef)
            req.append('2=0')
            req.append('3=%s' % self.fmtAmount(amount))
            req.append('99=0')
            resp = self.sendReq(req)
            result['status'] = '-3'
            result['message'] = 'Process failed, please retry.'
            if str(resp.get('2', '')) == '0':
                status = resp.get('3', '-1')
                if str(status) in ('1',):
                    result['status'] = '0'
                    result['message'] = self.getRespMsgByCode(status)
                else:
                    result['status'] = status
                    result['message'] = self.getRespMsgByCode(status)
                result['card_sha1'] = resp.get('59', '')
                result['card_number'] = resp.get('5', '')
                result['card_name'] = resp.get('10', '')
                result['card_expdate'] = resp.get('37', '')
                result['pgtr'] = resp.get('28', '')
                result['oid'] = resp.get('61', '')
                (code, msg, oid) = self._sale(upgAcctId, result['card_sha1'], result['card_expdate'], result['card_name'], self.fmtAmount(amount), track2 = '', track1 = '', oid = '%s|||%s' % (result['oid'], str(status)))
                if str(status) == str(code):
                    result['message'] = msg
                
            elif str(resp.get('2', '')) != '':
                result['status'] = '-1'
                result['message'] = 'Invalid response type.'
            
        else:
            result['status'] = '-2'
            result['message'] = 'EVT is busy.'
        return result

    
    def cancel(self, trsRef, pgtr, amount, cardnum, cardexp):
        ''' Sale with EVT.
        @param amount(float)
        @return
        '''
        result = { }
        result['busy'] = self.isBusy()
        if not result['busy']:
            req = []
            req.append('1=%s' % trsRef)
            req.append('2=3')
            req.append('3=%s' % self.fmtAmount(amount))
            req.append('5=%s' % cardnum)
            req.append('6=%s' % cardexp)
            req.append('13=%s' % pgtr)
            req.append('99=0')
            resp = self.sendReq(req)
            if str(resp['2']) == '0':
                status = resp['3']
                if str(status) in ('1',):
                    result['status'] = '0'
                    result['message'] = self.getRespMsgByCode(status)
                    result['card_sha1'] = resp['59']
                    result['card_number'] = resp['30']
                    result['card_name'] = resp['10']
                    result['card_expdate'] = resp['37']
                    result['pgtr'] = resp['28']
                
            else:
                result['status'] = '-1'
                result['msg'] = 'Invalid response type.'
        else:
            result['status'] = '-2'
            result['message'] = 'EVT is busy.'
        return result

    
    def fmtAmount(self, amount):
        ''' Format the amount for the EVT.
        @param amount(float)
        @return: amount(str)
        '''
        return '%.2f' % round(float(amount), 2)

    
    def getRespMsgByCode(self, respCode):
        ''' Get the response message by response code.
        @param respCode(str)
        @return: respMsg(str)
        '''
        respMsg = 'Unkown response: %s' % respCode
        if str(respCode) in RESPONSE_MSG:
            respMsg = RESPONSE_MSG[str(respCode)]
        
        return respMsg

    
    def postauth(self, acctId, cardNum, expDate, nameOnCard, amount, track2 = '', track1 = '', oid = '', ignore_bl = 1):
        """ POSTAUTH with the subscript.
        @param acctId(str): UPG account ID
        @param cardNum(str): PAN(Primary Account Number), like 123456XXXXXX1234
        @param expDate(str): Card Expired Date
        @param nameOnCard(str):
        @param amount(str):
        @param track2(str):
        @param track1(str):
        @param oid(str): the merchant's subscription wallet reference
        @param ignore_bl(int): 0/1
        @return: trsCode, trsMsg, oid(PGTR)
        """
        trsCode = ''
        trsMsg = ''
        
        try:
            self.log.info('postauth: acctId %s, cardNum %s, nameOnCard %s, amount %s, oid %s' % (acctId, cardNum, nameOnCard, amount, oid))
            trsType = 'POSTAUTH'
            r = credit_card.Trade.trade(self, acctId, trsType, cardNum, expDate, nameOnCard, amount, track2, track1, oid, ignore_bl)
            (trsCode, trsMsg, oid) = r
        except credit_card.UpgInternalError:
            ex = None
            trsCode = '-1'
            m = 'Internal Error when postauth from UPG: %s' % ex
            trsMsg = m
            self.log.error(m)
        except Exception:
            ex = None
            trsCode = '-2'
            m = 'Local Error when postauth from UPG: %s' % ex
            trsMsg = m
            self.log.error(m)

        return (trsCode, trsMsg, oid)

    
    def preauth(self, acctId, cardNum, expDate, nameOnCard, amount, track2 = '', track1 = '', oid = '', ignore_bl = 1):
        trsCode = ''
        trsMsg = ''
        
        try:
            trsType = 'PREAUTH'
            r = credit_card.Trade.trade(self, acctId, trsType, cardNum, expDate, nameOnCard, amount, track2, track1, oid, ignore_bl)
            (trsCode, trsMsg, oid) = r
        except credit_card.UpgInternalError:
            ex = None
            trsCode = '-1'
            m = 'Internal Error when preauth from UPG: %s' % ex
            trsMsg = m
            self.log.error(m)
        except Exception:
            ex = None
            trsCode = '-2'
            m = 'Local Error when preauth from UPG: %s' % ex
            trsMsg = m
            self.log.error(m)

        return (trsCode, trsMsg, oid)

    
    def _sale(self, acctId, cardNum, expDate, nameOnCard, amount, track2 = '', track1 = '', oid = '', ignore_bl = 1):
        trsCode = ''
        trsMsg = ''
        for i in range(5):
            
            try:
                trsType = 'SALE'
                r = credit_card.Trade.trade(self, acctId, trsType, cardNum, expDate, nameOnCard, amount, track2, track1, oid, ignore_bl)
                (trsCode, trsMsg, oid) = r
            except credit_card.UpgInternalError:
                ex = None
                trsCode = '-1'
                m = 'Internal Error when sale from UPG: %s' % ex
                trsMsg = m
                self.log.error(m)
            except Exception:
                ex = None
                trsCode = '-2'
                m = 'Local Error when sale from UPG: %s' % ex
                trsMsg = m
                self.log.error(m)

        
        return (trsCode, trsMsg, oid)

    
    def refund(self, acctId, cardNum, expDate, nameOnCard, amount, track2 = '', track1 = '', oid = '', ignore_bl = 1):
        trsCode = ''
        trsMsg = ''
        
        try:
            self.log.info('refund: acctId %s, cardNum %s, nameOnCard %s, amount %s, oid %s' % (acctId, cardNum, nameOnCard, amount, oid))
            trsType = 'CREDIT'
            r = credit_card.Trade.trade(self, acctId, trsType, cardNum, expDate, nameOnCard, amount, track2, track1, oid, ignore_bl)
            (trsCode, trsMsg, oid) = r
        except credit_card.UpgInternalError:
            ex = None
            trsCode = '-1'
            m = 'Internal Error when sale from UPG: %s' % ex
            trsMsg = m
            self.log.error(m)
        except Exception:
            ex = None
            trsCode = '-2'
            m = 'Local Error when sale from UPG: %s' % ex
            trsMsg = m
            self.log.error(m)

        return (trsCode, trsMsg, oid)



def main():
    chipNPin = ChipNPin('S250-A911', 'cereson.gicp.net', '', '/upgtest/agent/upgAgent', upgTrsMode = 'LIVE', host = '127.0.0.1', EVTPort = 10000, timeout = 120)
    print(chipNPin.sale('2000', 'test111', 1))

if __name__ == '__main__':
    main()

