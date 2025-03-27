# Source Generated with Decompyle++
# File: allps.pyc (Python 2.5)

'''
##  Used by S250 kiosk for ALLPS of the gateway INTECON in
##  South Africa.
##
##  Change Log:
##      2010-02-22 Modified by Tim
##          Change the reqType from "001", "111" to "109"
##      2009-11-09 Modified by Tim
##          The interface of ALLPS has changed.
##      2009-10-16 Created by Tim
##
'''
import os
import time
import ftplib
import socket
from . import tools
from .config import *

class Allps(object):
    
    def __init__(self, host = '127.0.0.1', port = 21, user = '', passwd = ''):
        ''' init '''
        self.ftp = ftplib.FTP()
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.log = tools.getLog('allps.log')
        self.date = tools.getCurTime('%Y%m%d')
        self.allpsFold = os.path.join(USER_ROOT, 'kiosk', 'var', 'allps', self.date)
        if not os.path.exists(self.allpsFold):
            os.makedirs(self.allpsFold)
        

    
    def __del__(self):
        del self.log
        self.ftp.close()

    
    def setImpFile(self, reqType, trsIdty, acctType, cents = 0, timeout = 10):
        ''' Setup the request file to the remote system.
        @Params: reqType(str): "109" #"001" or "111"
                            #"001": Balance Enquiry Request
                            #"111": Payment on Demand Request
                 trsIdty(str): unique transaction record identity per deployed
                            installation.
                 acctType(str): "01" or "02"
                            "01": Savings
                            "02": Current/Cheque
                 timeout(int): the second of timeout
        @Return: status(int): 0: success
                              1: unknown error
                              2: time out when connect to ftp server
                              3: connection refused when connect
                              4: Login or password incorrect
                              5: Permission denied when create new file
                              6: IOError
                 seq(int): sequence number
        '''
        status = 1
        seq = 0
        defaultto = socket.getdefaulttimeout()
        
        try:
            seq = self.getSeq()
            impFileName = '%s%s.imp' % (self.date, str(seq).zfill(3))
            impFile = os.path.join(self.allpsFold, impFileName)
            if reqType == '001':
                content = ','.join([
                    str(reqType),
                    str(trsIdty),
                    str(acctType)])
            else:
                content = ','.join([
                    str(reqType),
                    str(trsIdty),
                    str(acctType),
                    str(cents)])
            fdw = open(impFile, 'wb')
            
            try:
                fdw.write(content)
            finally:
                fdw.close()

            socket.setdefaulttimeout(timeout)
            self.connect()
            self.login()
            fdr = open(impFile)
            
            try:
                print('clear all files')
                self.clearFiles()
                print('store begin')
                self.ftp.storbinary('STOR %s' % impFileName, fdr)
                print('store end')
            finally:
                fdr.close()
                self.logout()

            status = 0
        except socket.timeout:
            ex = None
            status = 2
            self.log.error('Timeout when connect to the ftp server.')
        except socket.error:
            ex = None
            status = 3
            self.log.error('Connection refused when connect to the ftp server: %s' % ex)
        except ftplib.error_perm:
            ex = None
            lastresp = str(getattr(self.ftp, 'lastresp', None))
            self.log.info('lastresp: %s' % lastresp)
            if lastresp == '530':
                status = 4
            elif lastresp == '550':
                status = 5
            else:
                status = 1
            self.log.error('Permission deny from ftp server: %s' % ex)
        except IOError:
            ex = None
            status = 6
            self.log.error('IOError: %s' % ex)
        except Exception:
            ex = None
            status = 1
            self.log.error('Unknown error in setImpFile: %s' % ex)

        socket.setdefaulttimeout(defaultto)
        return (status, seq)

    
    def getExpFile(self, seq, trsIdty, timeout = 120):
        ''' Retrieve the response file from the remote system.
        @Params: seq(int): sequence file
                 trsIdty(str): unique transaction record identity per deployed
                            installation.
                 timeout(int): the second of timeout
        @Return: status(int): 0: success
                              1: unknown error
                              2: time out when connect to ftp server
                              3: connection refused when connect
                              4: Login or password incorrect
                              5: Permission denied when create new file
                              6: IOError
                              7: timeout when get export file
                              8: invalid response
                              9: canceled
        '''
        status = 1
        cardNum = ''
        errocode = ''
        erromsg = ''
        oid = ''
        defaultto = socket.getdefaulttimeout()
        
        try:
            escapeFiles = []
            begin = time.time()
            self.connect()
            self.login()
            while True:
                socket.setdefaulttimeout(10)
                if status == 0 or status == 9:
                    break
                
                time.sleep(0.5)
                if time.time() - begin > timeout:
                    status = 7
                    break
                
                expFiles = self.getFiles('exp')
                if not expFiles:
                    continue
                
                for expFileName in expFiles:
                    if expFileName in escapeFiles:
                        continue
                    
                    expFile = os.path.join(self.allpsFold, expFileName + '.%s' % seq)
                    status = 1
                    result = ''
                    fdw = open(expFile, 'wb')
                    fdr = open(expFile)
                    
                    try:
                        print('retrive begin')
                        for i in range(2):
                            print('retrive time', i)
                            self.ftp.retrbinary('RETR %s' % expFileName, fdw.write)
                            fdw.flush()
                            time.sleep(0.5)
                            fdr.seek(0)
                            result = fdr.read()
                            print('result', result)
                            if result:
                                break
                            
                        
                        print('retrive end')
                        print('result', result)
                    finally:
                        fdw.close()
                        fdr.close()

                    if result:
                        rs = result.split(',')
                        if len(rs) in (15, 10):
                            if str(rs[4]) == str(trsIdty):
                                reqType = rs[0].strip()
                                errocode = rs[5].strip()
                                erromsg = rs[6].strip()
                                oid = rs[3].strip()
                                if erromsg.upper() == 'CARD SWIPE CANCELLED.' or str(errocode) == '2007':
                                    status = 9
                                elif reqType == '001' and len(rs) == 10:
                                    cardNum = rs[9].strip()
                                    status = 0
                                elif reqType == '111' and len(rs) == 15:
                                    cardNum = rs[14].strip()
                                    status = 0
                                elif reqType == '109' and len(rs) == 15:
                                    cardNum = rs[14].strip()
                                    status = 0
                                else:
                                    self.log.error('Unknown erro in getExpFile: %s' % result)
                                break
                            else:
                                escapeFiles.append(expFileName)
                        else:
                            status = 8
                            self.log.error('Error in getExpFile: %s' % result)
                            time.sleep(0.5)
                    
                
            self.logout()
        except socket.timeout:
            ex = None
            status = 2
            self.log.error('Timeout when connect to the ftp server.')
        except socket.error:
            ex = None
            status = 3
            self.log.error('Connection refused when connect to the ftp server: %s' % ex)
        except ftplib.error_perm:
            ex = None
            lastresp = str(getattr(self.ftp, 'lastresp', None))
            self.log.info('lastresp: %s' % lastresp)
            if lastresp == '530':
                status = 4
            elif lastresp == '550':
                status = 5
            else:
                status = 1
            self.log.error('Permission deny from ftp server: %s' % ex)
        except IOError:
            ex = None
            status = 6
            self.log.error('IOError: %s' % ex)
        except Exception:
            ex = None
            status = 1
            self.log.error('Unknown error in setImpFile: %s' % ex)

        socket.setdefaulttimeout(defaultto)
        return (status, cardNum, errocode, erromsg, oid)

    
    def connect(self):
        ''' Connect ftp server.
        @Params: None
        @Return: None
        '''
        
        try:
            self.ftp.quit()
        except:
            pass

        self.ftp.connect(self.host, self.port)

    
    def login(self):
        ''' Login the ftp.
        @Params: None
        @Return: None
        '''
        print('login begin')
        self.ftp.login(self.user, self.passwd)
        print('login end')

    
    def logout(self):
        ''' Login the ftp.
        @Params: None
        @Return: None
        '''
        print('quit')
        self.ftp.quit()
        print('close')
        self.ftp.close()
        print('close end')

    
    def getSeq(self):
        ''' Get the sequence of today.
        @Params: None
        @Return: seq(int)
        '''
        seqFile = os.path.join(self.allpsFold, 'allps_seq_file.seq')
        seq = 0
        if os.path.exists(seqFile):
            fr = open(seqFile)
            
            try:
                seq = fr.read().strip()
                seq = int(seq) + 1
            except Exception:
                ex = None
                self.log.error('error in getSeq for (%s): %s' % (seq, ex))
                seq = 1
            finally:
                fr.close()

        else:
            seq = 1
        fw = open(seqFile, 'wb')
        
        try:
            fw.write(str(seq))
        finally:
            fw.close()

        return seq

    
    def clearFiles(self, ext = 'all'):
        ''' Clear all files of the ftp server.
        @Params: ext(str): all, exp or imp
        @Return: None
        '''
        fileNames = self.getFiles(ext)
        for fn in fileNames:
            
            try:
                self.log.info('delete file: %s' % fn)
                self.ftp.delete(fn)
            except Exception:
                ex = None
                self.log.error('Delete file %s failed: %s' % (fn, ex))

        

    
    def getFiles(self, ext = 'all'):
        ''' Get files from ftp server.
        @Params: exp(str): all, imp, exp
        @Return: fileList(list)
        '''
        fileList = []
        tmp = []
        '\n        tmp = ""\n        if ext == "exp":\n            tmp = self.ftp.dir("*.exp")\n            self.log.info("getFiles: exp: %s"%tmp)\n        elif ext == "imp":\n            tmp = self.ftp.dir("*.imp")\n            self.log.info("getFiles: imp: %s"%tmp)\n        else:\n            tmpexp = self.ftp.dir("*.exp")\n            self.log.info("getFiles: exp: %s"%tmpexp)\n            tmpimp = self.ftp.dir("*.imp")\n            self.log.info("getFiles: imp: %s"%tmpimp)\n        #tmp = tmp.replace("\n", " ").replace("\r", " ").replace("\t", " ")\n        if tmp:\n            tmpList = tmp.split()\n            for fn in tmpList:\n                if fn.endswith(".exp") or fn.endswith(".imp"):\n                    fileList.append(fn)\n        '
        self.ftp.retrlines('nlst', tmp.append)
        explist = []
        implist = []
        for fn in tmp:
            if fn.endswith('.exp'):
                explist.append(fn)
            elif fn.endswith('.imp'):
                implist.append(fn)
            
        
        if ext == 'exp':
            fileList = explist
        elif ext == 'imp':
            fileList = implist
        else:
            fileList = implist + explist
        return fileList



def test():
    '''
    allps = Allps("iserv.intecon.co.za", 21, "dvdnow", "andre@dvdnowsa")
    seq = allps.setImpFile("001", "test0010101", "01")
    print seq
    print allps.getExpFile(seq)
    '''
    allps = Allps('192.168.1.67', 21, 'Administrator', 'mimahenchang')
    seq = 14
    trsIdty = 'S250A91220091028142607'
    print(seq)
    print(allps.getExpFile(seq, trsIdty, 10))

if __name__ == '__main__':
    test()

