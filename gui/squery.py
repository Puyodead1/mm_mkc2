# Source Generated with Decompyle++
# File: squery.pyc (Python 2.5)

import socket
import config_mkc
import json

class socketQuery:
    
    def __init__(self):
        pass

    
    def setup(self):
        global trace, socketq
        trace = config_mkc.initLog('qt_trace.log')
        socketq = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketq.setblocking(1)
        
        try:
            socketq.connect((config_mkc.HOST, config_mkc.PORT))
        except Exception as ex:
            self.trace().error('[socketQuery] [Error] Can not connect: %s' % ex)

        self.sd = socketq

    
    def send(self, data):
        
        try:
            data = json.dumps(data)
            socketq.send(str(len(data)) + '\n')
            socketq.send(data)
            self.trace().info('Sending data: %s' % data)
        except Exception as ex:
            self.trace().error('[socketQuery] Can not send: %s\nSend data: %s' % (ex, data))


    
    def trace(self):
        return trace

    
    def deinit(self):
        socketq.close()


