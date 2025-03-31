# Source Generated with Decompyle++
# File: control.pyc (Python 2.5)

'''
Main controler
2009-07-02 created by Mavis
'''
import os
import select
import time
import json
from PyQt4 import QtCore, QtGui
from squery import socketQuery

class MainControl(QtCore.QThread):
    
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self)
        self.sock = socketQuery()
        self.sock.setup()
        self.trace = self.sock.trace()

    
    def setLanguage(self, param):
        if not param or not param['lang']:
            self.trace.error('[setLanguage] [Error] Invalid param: %s' % param)
            return None
        
        import config
        if param['lang'] != 'en':
            lang = param['lang']
            if os.path.isdir(config.PICDIR + lang):
                '\n                if os.path.isfile(config.PICDIR+lang+"/btn_bg_rent_"+lang+".png"):\n                    config.pic_btn_rent_bg = config.PICDIR+lang+"/btn_bg_rent_"+lang+".png"\n                if os.path.isfile(config.PICDIR+lang+"/btn_bg_return_"+lang+".png"):\n                    config.pic_btn_return_bg = config.PICDIR+lang+"/btn_bg_return_"+lang+".png"\n                if os.path.isfile(config.PICDIR+lang+"/btn_bg_p_"+lang+".png"):\n                    config.pic_btn_pickup_bg = config.PICDIR+lang+"/btn_bg_p_"+lang+".png"\n                '
                if os.path.isfile(config.PICDIR + lang + '/bg_admin_' + lang + '.png'):
                    config.pic_bg_admin = config.PICDIR + lang + '/bg_admin_' + lang + '.png'
                
                if os.path.isfile(config.PICDIR + lang + '/icon_bigKeyboard_' + lang + '.png'):
                    config.pic_icon_bigKeyboard = config.PICDIR + lang + '/icon_bigKeyboard_' + lang + '.png'
                
                if os.path.isfile(config.PICDIR + lang + '/test_mode_flag_' + lang + '.png'):
                    config.pic_test_flag = config.PICDIR + lang + '/test_mode_flag_' + lang + '.png'
                
                if os.path.isfile(config.PICDIR + lang + '/mask_comingSoon_' + lang + '.png'):
                    config.pic_coming_soon = config.PICDIR + lang + '/mask_comingSoon_' + lang + '.jpg'
                
            
            config.transFile = 'trans_' + lang + '.qm'
            self.emit(QtCore.SIGNAL('execCommand(QString)'), 'self.setLanguage()')
        else:
            '\n            config.pic_btn_rent_bg = config.PICDIR+"btn_bg_rent.png"\n            config.pic_btn_return_bg = config.PICDIR+"btn_bg_return.png"\n            config.pic_btn_pickup_bg = config.PICDIR+"btn_bg_p.png"\n            '
            config.pic_bg_admin = config.PICDIR + 'bg_admin.png'
            config.pic_icon_bigKeyboard = config.PICDIR + 'icon_bigKeyboard.png'
            config.pic_test_flag = config.PICDIR + 'test_mode_flag.png'
            config.pic_coming_soon = config.PICDIR + 'mask_comingSoon.png'
            config.transFile = ''
        self.emit(QtCore.SIGNAL('execCommand(QString)'), 'self.setLanguage()')

    
    def initGUI(self, param = { }):
        transDir = transDir
        import config_mkc
        if param and 'model' in param and param['model'] == '1':
            os.system('echo "image_game/" > ' + transDir + '.config_model')
            self.emit(QtCore.SIGNAL('execCommand(QString)'), 'self.initGUI(1)')
        else:
            os.system('rm -rf ' + transDir + '.config_model')
            self.emit(QtCore.SIGNAL('execCommand(QString)'), 'self.initGUI()')

    
    def gotoWindow(self, param):
        wid = param['wid']
        if not wid:
            print('[gotoWindow] Error: wid can not be NULL!')
            return -1
        
        self.emit(QtCore.SIGNAL('execCommand(QString)'), 'objforms.hideCurrentForm()')
        if wid == 'LoadTakeInForm' or wid == 'LoadResultForm':
            cmd = "objforms.showForm('LoadDiscInfoForm')"
            self.emit(QtCore.SIGNAL('execCommand(QString)'), cmd)
        
        cmd = "objforms.showForm('" + str(wid) + "')"
        self.emit(QtCore.SIGNAL('execCommand(QString)'), cmd)

    
    def showWindow(self, param):
        wid = param['wid']
        if not wid:
            print('[gotoWindow] Error: wid can not be NULL!')
            return -1
        
        cmd = "objforms.showForm('" + str(wid) + "')"
        self.emit(QtCore.SIGNAL('execCommand(QString)'), cmd)

    
    def hideWindow(self, param):
        wid = param['wid']
        if not wid:
            print('[gotoWindow] Error: wid can not be NULL!')
            return -1
        
        cmd = "objforms.hideForm('" + str(wid) + "')"
        self.emit(QtCore.SIGNAL('execCommand(QString)'), cmd)

    
    def exitNormal(self):
        print('GUI Will exit normally...')
        self.emit(QtCore.SIGNAL('execCommand(QString)'), 'exitNormal')

    
    def setCurrencySymbol(self, param):
        if param:
            import config
            config.symbol = param['symbol']
        

    
    def revData(self):
        last_error_time = ''
        error_count = 0
        while True:
            
            try:
                (rlist, wlist, elist) = select.select([
                    self.sock.sd], [], [], 0.0001)
                if self.sock.sd in rlist:
                    fullData = ''
                    
                    try:
                        length = ''
                        while True:
                            data = self.sock.sd.recv(1)
                            if data == '\n':
                                break
                            
                            length = length + data
                        lenData = 0
                        while lenData != int(length):
                            data = self.sock.sd.recv(int(length) - lenData)
                            lenData += len(data)
                            fullData = fullData + data
                    except Exception as ex:
                        now = time.time()
                        error_count += 1
                        if not last_error_time or now - last_error_time > 10 * 60:
                            last_error_time = now
                            self.trace.error('error times:%s [revData] [Error] when sock.recv: %s' % (error_count, ex))
                            error_count = 0
                        
                    except:
                        now - last_error_time > 10 * 60

                    if fullData:
                        self.process(fullData)
                    
            except Exception as ex:
                self.trace.error('[revData] [Error] when select/recv/process data: %s' % ex)


    
    def process(self, jstring):
        
        try:
            
            try:
                data = json.loads(jstring)
            except Exception as ex:
                self.trace.error('[process] [Error] Data from mkc is NOT valid JSON data! %s' % ex)
                return -1

            if not data['wid'] and not data['cid']:
                param = data['param_info']
                cmd = data['cmd']
                if not cmd:
                    self.trace.error('[process] Error: cmd can not be NULL!')
                    return -1
                
                if param:
                    
                    try:
                        eval('self.' + str(cmd) + '(' + str(param) + ')')
                    except Exception as ex:
                        self.trace.error('[process] [Error] when do command: %s' % ex)

                else:
                    
                    try:
                        eval('self.' + cmd + '()')
                    except Exception as ex:
                        self.trace.error('[process] [Error] when do command: %s' % ex)

            elif data['wid'] and data['cid']:
                func = data['cmd']
                wid = data['wid']
                cid = data['cid']
                if not func:
                    self.trace.error('[process] Error: wid or cmd can not be NULL! %s' % data)
                    return None
                
                if data['param_info'] and cid:
                    if func == 'setText':
                        param = data['param_info']['text']
                        param = repr(param)
                        cmd = 'objforms.getForm("' + wid + '").ui.' + cid + '.' + func + '(' + param + ')'
                        self.emit(QtCore.SIGNAL('execCommand(QString)'), cmd)
                        return None
                    else:
                        param = data['param_info']
                    cmd = "objforms.getForm('" + wid + "').ui." + cid + '.' + func + '(' + str(param) + ')'
                else:
                    cmd = "objforms.getForm('" + wid + "').ui." + cid + '.' + func + '()'
                self.emit(QtCore.SIGNAL('execCommand(QString)'), cmd)
            else:
                self.trace.error('[process] [Error]: Received Invalid Data! %s' % data)
                return -1
        except Exception as ex:
            self.trace.error('[process] [Error] : %s' % ex)


    
    def run(self):
        self.revData()


