# Source Generated with Decompyle++
# File: guiMainForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: MainForm.py
The very first touch screen form
Screen ID: R1

Change Log:
    2009-03-09 Vincent: For Vertical Adj
    2009-02-16 Vincent: Line 140 For #1580
'''
from proxy.config import MOVIE_DEFAULT_PIC_NAME
from proxy.tools import unlock
from proxy.tools import lock
from mcommon import *
from guiBaseForms import MMForm
from config import KIOSK_HOME
log = initlog('guiMainForm')
ERROR_BG = os.path.join(KIOSK_HOME, 'kiosk/var/gui/sys/bg_outofservice.png')
LANGUANG_BG = os.path.join(KIOSK_HOME, 'kiosk/var/gui/sys/bg_switch_language.png')

def changeBackground(fullname):
    cmd = 'gconftool-2 -t string -s /desktop/gnome/background/picture_filename %s'
    os.system(cmd % fullname)
    cmd2 = 'gconftool-2 -t string -s /desktop/gnome/background/picture_options wallpaper'
    os.system(cmd2)


class MainForm(MMForm):
    
    def __init__(self):
        MMForm.__init__(self)
        self.screenID = 'R1'
        self.preWindowID = 'MainForm'
        self.timeoutSec = 300
        self.lstResponseCtrl = [
            'btn_rent',
            'btn_return',
            'btn_pickup',
            'btn_buy',
            'btn_login',
            'btn_active',
            'ctr_movie_list']
        self.buttons = []
        self.languageList = []
        self.langSwitch = False
        self._initGui()
        self._setThemeButtons()
        self._getDefaultLanguage()
        self._setLanguageButtons()
        self.connProxy.getKioskLogo()

    
    def _setThemeButtons(self):
        if MKC_THEME == 'game':
            self.lstResponseCtrl.append('btn_wii')
            self.lstResponseCtrl.append('btn_ps3')
            self.lstResponseCtrl.append('btn_xbox')
        

    
    def _getDefaultLanguage(self):
        language = ''
        
        try:
            language = self.connProxy._getConfigByKey('default_language')
            if language:
                log.info('default language is %s' % language)
        except:
            log.error('get default language failed, set to English.')
            language = 'en'

        self.defaultLanguage = language

    
    def _initGui(self):
        self.flash.wid = ''
        params = { }
        if MKC_THEME == 'game':
            params['model'] = '1'
        
        self.flash.send('', 'initGUI', params)
        self.flash.wid = self.windowID

    
    def _setLanguage(self):
        if self.langSwitch:
            language = self.language
        else:
            language = self.defaultLanguage
        self.langSwitch = False
        log.info('set language to %s' % language)
        self.language = setLanguage(language)
        self.flash.wid = ''
        self.flash.send('', 'setLanguage', {
            'lang': self.language })
        self.flash.wid = self.windowID

    
    def _resetLanguage(self, lan):
        if self.language != lan:
            self.language = lan
            self.langSwitch = True
            self.nextWindowID = 'MainForm'
            self.windowJump = True
        

    
    def _setLanguageButtons(self):
        
        try:
            lanlist = self.connProxy._getConfigByKey('language_switch')
            log.info('language list is %s' % lanlist)
            i = 1
            ltemp = lanlist.split(',')
            for lan in ltemp:
                if i > 3:
                    break
                
                x = lan.strip()
                if x:
                    self.languageList.append(x)
                    bt = 'btn_%s' % x
                    btKey = 'on_%s_event' % bt
                    on_btn_language_event = None
                    func = "def on_btn_language_event(self):\n                        self._resetLanguage('%(language)s')" % {
                        'language': x }
                    exec(func)
                    setattr(MainForm, btKey, on_btn_language_event)
                    self.lstResponseCtrl.append(bt)
                    self.buttons.append(bt)
                    i += 1
                
        except:
            log.error('get language list failed, hide all language buttons.\n%s' % traceback.format_exc())


    
    def _showLanguageButtons(self):
        if self.languageList:
            self.flash.send('ctr_btn_lang', 'initLanguage', {
                'ctr_btn_lang': self.languageList })
            self.languageList = []
        

    
    def _getNewReleaseWithBigCover(self):
        tmpMvlist = self.connProxy.getAvailableMovieList('genre', 'NEW RELEASE')
        mvlist = []
        for mv in tmpMvlist:
            smv = { }
            smv['upc'] = mv.get('upc')
            picName = mv.get('movie_pic')
            picFullPath = getPicFullPath(picName)
            if picFullPath.find(MOVIE_DEFAULT_PIC_NAME) < 0:
                smv['movie_pic'] = picFullPath
                if str(mv.get('is_bluray')) == '1':
                    smv['is_bluray'] = '1'
                else:
                    disc = Disc()
                    disc.upc = mv.get('upc')
                    self.movieProxy.getMovieDetailByUpc(disc)
                    if disc.discType == 'WII':
                        smv['is_bluray'] = '2'
                    elif disc.discType == 'XBOX360':
                        smv['is_bluray'] = '3'
                    elif disc.discType == 'PS3':
                        smv['is_bluray'] = '4'
                    else:
                        smv['is_bluray'] = '0'
                mvlist.append(smv)
            
        
        return mvlist

    
    def _initComponents(self):
        log.info('=======================================')
        log.info('=   Main Form Initializing ......     =')
        self._setLanguage()
        MMForm._initComponents(self)
        if globalSession.loginTime:
            self.connProxy.saveCustomterBehavior(globalSession.loginType, globalSession.loginTime, time.strftime('%Y-%m-%d %H:%M:%S'))
        
        globalSession.clear()
        self.connProxy.resetAll()
        if MKC_THEME == 'game':
            slogan = self.connProxy._getConfigByKey('kiosk_gr_slogan')
            self.flash.send('txt_msg', 'setText', {
                'text': slogan })
        else:
            mvlist = self._getNewReleaseWithBigCover()
            self.flash.send('ctr_movie_list', 'setMovieList', {
                'ctr_movie_list': mvlist })
        currencySymbol = self.connProxy.getDefaultCurrencySymbol()
        self.flash.wid = ''
        self.flash.send('', 'setCurrencySymbol', {
            'symbol': currencySymbol })
        self.flash.wid = self.windowID
        globalSession.param['currency_symbol'] = currencySymbol
        globalSession.param['test_mode'] = True
        if self.connProxy._getConfigByKey('upg_show_mode') == 'no':
            globalSession.param['test_mode'] = False
        
        if globalSession.param.get('test_mode'):
            self.flash.send('test_mode_flag', 'show', { })
        else:
            self.flash.send('test_mode_flag', 'hide', { })
        self._showLanguageButtons()
        unlock()
        log.info('=   Main Form Initialized             =')
        log.info('=======================================')

    
    def _gameRent(self, id):
        globalSession.firstKey = 'genre'
        globalSession.firstGenreID = id
        self.nextWindowID = 'RentMainForm'
        self.windowJump = True

    
    def on_btn_wii_event(self):
        self._gameRent('WII')

    
    def on_btn_ps3_event(self):
        self._gameRent('PS3')

    
    def on_btn_xbox_event(self):
        self._gameRent('XBOX360')

    
    def on_btn_rent_event(self):
        globalSession.loginTime = time.strftime('%Y-%m-%d %H:%M:%S')
        globalSession.loginType = 'RENT'
        self.nextWindowID = 'RentMainForm'
        self.windowJump = True

    
    def on_btn_return_event(self):
        globalSession.loginTime = time.strftime('%Y-%m-%d %H:%M:%S')
        globalSession.loginType = 'RETURN'
        self.nextWindowID = 'ReturnTakeInForm'
        self.windowJump = True

    
    def on_btn_pickup_event(self):
        globalSession.loginTime = time.strftime('%Y-%m-%d %H:%M:%S')
        globalSession.loginType = 'PICKUP'
        self.nextWindowID = 'PickUpCodeForm'
        self.windowJump = True

    
    def on_btn_buy_event(self):
        globalSession.loginTime = time.strftime('%Y-%m-%d %H:%M:%S')
        globalSession.loginType = 'BUY'
        globalSession.firstGenreID = 'ON SALE'
        self.nextWindowID = 'RentMainForm'
        self.windowJump = True

    
    def on_btn_login_event(self):
        globalSession.loginTime = time.strftime('%Y-%m-%d %H:%M:%S')
        globalSession.loginType = 'LOGIN'
        option = self.connProxy._getConfigByKey('payment_options')
        if option == 'intecon':
            self.nextWindowID = 'MembershipLoginPasswordForm'
        elif option == 'chipnpin':
            self.nextWindowID = 'MembershipLoginSwipeCardForm'
        else:
            self.nextWindowID = 'MembershipLoginSwipeCardForm'
        self.windowJump = True

    
    def on_btn_active_event(self):
        globalSession.loginTime = time.strftime('%Y-%m-%d %H:%M:%S')
        globalSession.loginType = 'ACTIVE'
        self.nextWindowID = 'RegisterSwipeCardForm'
        self.windowJump = True

    
    def on_ctr_movie_list_event(self):
        globalSession.loginTime = time.strftime('%Y-%m-%d %H:%M:%S')
        globalSession.loginType = 'RENT'
        upc = self._getEventParam('ctr_movie_list', 'upc')
        if upc:
            disc = Disc()
            disc.upc = upc
            self.connProxy.loadDiscInfo(disc)
            globalSession.disc = disc
            self.nextWindowID = 'DiscDetailForm'
            self.windowJump = True
        

    
    def on_hide(self):
        MMForm.on_hide(self)
        lock()

    
    def on_timeout(self):
        if self.connProxy.getArrangementPlan():
            self.nextWindowID = 'RemoteArrangementForm'
            self.windowJump = True
        

    
    def _run(self):
        while True:
            self.event = self.flash.get(timeout = self.timeoutSec)
            if self.event != None:
                ctrlID = self.event.get('cid')
                if ctrlID:
                    log.info('[UI Event]: %s.' % self.event)
                
                self.on_event(ctrlID)
                if self.windowJump:
                    break
                
            

    
    def render(self):
        
        try:
            self._initComponents()
            self._run()
        except Exception:
            msg = '[MainForm render] failed:%s' % traceback.format_exc()
            log.error(msg)
            self.connProxy.emailAlert('PRIVATE', msg, 'andrew.lu@cereson.com', critical = self.connProxy.UNCRITICAL)
            time.sleep(5)
            self.nextWindowID = 'MainForm'

        self.on_hide()
        return self.nextWindowID


