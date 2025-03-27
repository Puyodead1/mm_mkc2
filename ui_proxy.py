# Source Generated with Decompyle++
# File: ui_proxy.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2009-08-03 Andrew
andrew.lu@cereson.com

Filename: ui_proxy.py

Change Log:
'''
import threading
import os
import time
import socket
import select
import simplejson as json
import traceback
from mcommon import QItem, initlog
from mcommon import startHdmi
from config import QTGUI
'\nvars for plugin_player\n'
DEFAULT_MEDIA = 'default.mpg'
MPLAYER_OPTS = 'nohup mplayer -loop 0 -ontop -geometry 271x201+676+185 -quiet %s -display :0.0 > /dev/null &'
trace = initlog('UIPROXY', 'ui_proxy')

def startGui():
    trace.info('[Start Qt GUI] ...')
    cmd = 'DISPLAY=:0.0 %s > /home/mm/kiosk/var/log/qt_gui.log 2>&1 &' % QTGUI
    os.system(cmd)


def stopGui():
    trace.info('[Stop Qt GUI] ...')
    os.system('pkill -f %s' % QTGUI)


def restartUI():
    trace.info('[Restart QT GUI] .......')
    stopGui()
    startGui()


def internal_error_qitem(reason, qtype = 'EVENT', identity = None, timestamp = None):
    qitem = QItem(_type = qtype, _identity = identity, _timestamp = timestamp, _param = {
        'errornum': '-100',
        'errorinfo': reason })
    return qitem


class JsonTrans(object):
    
    def to_queue(cls, json_data):
        item = None
        
        try:
            q_param = json.loads(json_data)
            q_type = q_param['type']
            item = QItem(q_type, None, None, q_param)
        except Exception:
            ex = None
            trace.info('[Json Trans to_queue] error: %s\ninput json data:%s' % (ex, json_data))

        return item

    to_queue = classmethod(to_queue)
    
    def to_json(cls, qitem):
        json_data = None
        
        try:
            qdata = qitem.param
            qdata['type'] = qitem.itemType
            qdata['id'] = qitem.identity
            json_data = json.dumps(qdata)
        except Exception:
            ex = None
            trace.info('[Json Trans to_json] error: %s\ninput qitem:%s' % (ex, qitem))

        return json_data

    to_json = classmethod(to_json)


class UIListener(threading.Thread):
    
    def __init__(self, port, to_mkc_Q):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.msgLen = 0
        self.msg = ''
        self.to_mkc_Q = to_mkc_Q
        self.port = port
        self.sock_ready = False
        self._clientReady = False
        trace.info('[UIListener __init__] init UIListener ~~~~~~~~~~~~~~~~~')
        self.sock_init()

    
    def sock_init(self):
        self.cli_sd = None
        
        try:
            self.sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            import fcntl
            o = fcntl.fcntl(self.sd, fcntl.F_GETFD)
            if not o:
                pass
            fcntl.fcntl(self.sd, fcntl.F_SETFD, fcntl.FD_CLOEXEC)
            self.sd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            self.sd.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
            self.sd.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 3)
            self.sd.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 2)
            self.sd.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 9)
            self.sd.bind(('0', self.port))
            self.sd.listen(1)
            self.sock_ready = True
        except Exception:
            ex = None
            trace.info('[UIListener __init__] init sock error: %s' % ex)
            self.sd = None
            self.cli_sd = None
            self.sock_ready = False
            return False


    
    def run(self):
        
        try:
            while True:
                trace.info('[UIListener run] ~~~~~~~~~~~~~~~~ only one! only one!')
                if self._stop.isSet():
                    return None
                
                if self.sock_ready is False:
                    if self.sock_init() is False:
                        
                        try:
                            self.to_mkc_Q.put(internal_error_qitem(qtype = 'EVENT', reason = 'init sock error'))
                        except Exception:
                            ex = None
                            trace.error('[UIListener run] cannot write to_mkc_Q: %s' % ex)

                        time.sleep(1)
                        continue
                    else:
                        trace.info('[UIListener run] reinit socket ok')
                else:
                    trace.info('[UIListener run] socket init ok')
                self.stdin_list = [
                    self.sd]
                while True:
                    if self._stop.isSet():
                        trace.info('[UIListener run] _stop event set')
                        return None
                    
                    
                    try:
                        (stdin, stdou, stderr) = select.select(self.stdin_list, (), (), 1)
                    except Exception:
                        ex = None
                        trace.error('[UIListener run] select failed. %s' % ex.message)
                        break

                    if self.cli_sd in stdin:
                        
                        try:
                            data = self.cli_sd.recv(8192)
                        except:
                            trace.info('[UIListener run] socket except, set data to null\n%s' % traceback.format_exc())
                            data = ''

                        if not data:
                            trace.info('[UIListener run] connection lost! restart QT gui')
                            self.cli_sd.close()
                            self._clientReady = False
                            self.stdin_list.remove(self.cli_sd)
                            stopGui()
                            os._exit(-1)
                        else:
                            ret = self.parseTcpStream(data)
                            while ret:
                                self.process(ret)
                                ret = self.parseTcpStream()
                    elif self.sd in stdin:
                        if self.cli_sd:
                            trace.info('[UIListener run] remove old client handler for new client')
                            self.stdin_list = [
                                self.sd]
                            self.cli_sd.close()
                        
                        (self.cli_sd, cli_addr) = self.sd.accept()
                        self._clientReady = True
                        trace.info('[UIListener run] new client coming: %s' % cli_addr[0])
                        self.stdin_list.append(self.cli_sd)
                        time.sleep(2)
                    
        except:
            trace.error('UI_PROXY EXIT THE MAINLOOP!!!\n%s' % traceback.format_exc())


    
    def parseTcpStream(self, data = ''):
        ret = ''
        self.msg += data
        if self.msgLen == 0 and self.msg:
            
            try:
                i = self.msg.index('\n')
                self.msgLen = int(self.msg[:i])
                self.msg = self.msg[i + 1:]
            except:
                self

        
        if self.msg and self.msgLen > 0 and len(self.msg) >= self.msgLen:
            ret = self.msg[:self.msgLen]
            self.msg = self.msg[self.msgLen:]
            self.msgLen = 0
        
        return ret

    
    def process(self, new_data):
        trace.info('[UIListener process] recv raw json_data: %s' % new_data)
        qitem = JsonTrans.to_queue(new_data)
        if not qitem:
            trace.error('[UIListener process] cannot convert json to queue')
            
            try:
                self.to_mkc_Q.put(internal_error_qitem('cannot convert json to queue'), timeout = 2)
            except Exception:
                ex = None
                trace.error('[UIListener process] cannot write to_mkc_Q: %s' % ex)

        else:
            
            try:
                self.to_mkc_Q.put(qitem, timeout = 2)
            except Exception:
                ex = None
                trace.error('[UIListener process] cannot write to_mkc_Q: %s' % ex)


    
    def join(self, timeout = 5):
        trace.info('[UIListener join] enter join')
        self._stop.set()
        threading.Thread.join(self, timeout)

    
    def send_msg(self, msg):
        
        try:
            if self.cli_sd:
                trace.info('WILL SEND MSG type:%s, context:%s' % (type(msg), msg))
                length = len(msg)
                self.cli_sd.send(str(length) + '\n')
                self.cli_sd.send(msg)
            else:
                trace.error('[UIListener send_msg] client socket not ready')
        except Exception:
            ex = None
            self._clientReady = False
            trace.info('[UIListener send_msg]ex=%s\ncannot send: %s' % (ex, repr(msg)))
            raise 


    
    def waitGuiRestart(self):
        self._clientReady = False
        stopGui()
        trace.info('[UIListener waitGuiRestart]Start waiting Qt gui restart ...')
        while self._clientReady == False:
            trace.info('[UIListener waitGuiRestart] wait qt gui to connect.')
            time.sleep(1)

    
    def waitGuiConnect(self):
        trace.info('[UIListener waitGuiConnect]Start waiting Qt gui init...')
        while self._clientReady == False:
            trace.info('[UIListener waitGuiConnect] wait qt gui to connect.')
            time.sleep(1)



class MKCListener(threading.Thread):
    
    def __init__(self, from_mkc_Q, to_mkc_Q, to_ui):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.from_mkc_Q = from_mkc_Q
        self.to_mkc_Q = to_mkc_Q
        self.to_ui = to_ui

    
    def join(self, timeout = 2):
        self._stop.set()
        threading.Thread.join(self, timeout)

    
    def run(self):
        while True:
            
            try:
                qitem = self.from_mkc_Q.get(timeout = 1)
                if qitem and qitem.param:
                    self.process(qitem)
            except Exception:
                if self._stop.isSet():
                    trace.debug('[MKCListener run]  _stop event set!')
                    return None
                
            except:
                self._stop.isSet()


    
    def process(self, qitem):
        
        try:
            if qitem.param['wid'] == 'sub_movie_detail' and qitem.param['cid'] == 'video_movie_player':
                if qitem.param['cmd'] in ('playByName', 'close'):
                    trace.info('!!!!XXXXXX process plugin_player qitem=%s' % qitem)
                    self.plugin_player(qitem)
                    return None
                
        except:
            pass

        json_data = JsonTrans.to_json(qitem)
        if not json_data:
            
            try:
                tmp = internal_error_qitem(qtype = 'RESULT', reason = 'cannot convert qitem to json', identity = qitem.identity)
                self.to_mkc_Q.put(tmp, timeout = 2)
                return None
            except Exception:
                ex = None
                trace.error('[MKCListener process] cannot write to_mkc_Q: %s' % ex)
                return None

        
        
        try:
            self.to_ui.send_msg(json_data)
        except Exception:
            ex = None
            
            try:
                tmp = internal_error_qitem(qtype = 'RESULT', reason = 'cannot send_msg to ui: %s' % ex, identity = qitem.identity)
                self.to_mkc_Q.put(tmp, timeout = 2)
            except Exception:
                ex = None
                trace.error('[MKCListener process] cannot write to_mkc_Q: %s' % ex)



    
    def plugin_player(self, qitem):
        ret_qitem = QItem('RESULT', qitem.identity, '', { })
        if qitem.param['cmd'] == 'playByName':
            media_file = qitem.param['param_info']['name']
            if not os.path.isfile(media_file):
                trace.info('[MKCListener plugin_player] given file no exists, using default')
                media_file = DEFAULT_MEDIA
            
            os.system(MPLAYER_OPTS % media_file)
            trace.info('[MKCListener plugin_player] playing media: %s' % media_file)
            time.sleep(1.5)
            
            try:
                (w, r) = os.popen2('pgrep mplayer; echo $?')
                rev = r.read()
                w.close()
                r.close()
                rev = rev.split()[-1]
                if rev != '0':
                    trace.error('[MKCListener plugin_player] mplayer not running!')
                    ret_qitem.param = {
                        'errornum': rev,
                        'errorinfo': 'mplayer not running?' }
                else:
                    ret_qitem.param = {
                        'errornum': rev,
                        'errorinfo': '' }
            except Exception:
                ex = None
                trace.error('[MKCListener plugin_player] cannot check mplayer process')
                ret_qitem.param = {
                    'errornum': '-99',
                    'errorinfo': 'cannot check mplayer process' }

        elif qitem.param['cmd'] == 'close':
            trace.info('[MKCListener plugin_player] close mplayer..')
            os.system('pkill mplayer')
            os.system('pkill -9 mplayer')
            ret_qitem.param = {
                'errornum': '0',
                'errorinfo': '' }
        
        
        try:
            self.to_mkc_Q.put(ret_qitem, timeout = 2)
        except Exception:
            ex = None
            trace.error('[MKCListener plugin_player] cannot write to_mkc_Q: %s' % ex)




class IF(threading.Thread):
    '''
    Interface for mkc core and ui,
    route msg between mkc core and ui.
    '''
    
    def __init__(self, from_mkc_Q, to_mkc_Q, port):
        threading.Thread.__init__(self, name = 'ui_proxy')
        self._stop = threading.Event()
        self.ui_listener = UIListener(port, to_mkc_Q)
        self.mkc_listener = MKCListener(from_mkc_Q, to_mkc_Q, self.ui_listener)

    
    def join(self, timeout = 5):
        trace.debug('[IF join] enter join')
        self.ui_listener.join()
        self.mkc_listener.join()
        self._stop.set()
        threading.Thread.join(self, timeout)

    
    def run(self):
        stopGui()
        self.mkc_listener.start()
        self.ui_listener.start()
        startGui()
        time.sleep(1)
        while True:
            self._stop.wait()
            trace.debug('[IF run] _stop event set!')
            stopGui()
            break

    
    def restartQtGui(self):
        self.ui_listener.waitGuiRestart()

    
    def waitClient(self):
        self.ui_listener.waitGuiConnect()


