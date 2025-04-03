# Source Generated with Decompyle++
# File: guiRentMainForm.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2008-11-04 Vincent
vincent.chen@cereson.com

Filename: guiRentMainForm.py
Movie List Form with Gerne tab list
Screen ID: R2

Change Log:
    2011-01-11 Kitch Add French translation for Genres
    2009-03-10 Vincent Add Super Admin Form Entry
    2009-03-06 Vincent Add informative text
    2009-02-16 Vincent 1. Add on_hide, hide 2 keyboard
                       2. Test Mode can only input the first char of OP code

'''
from mcommon import *
from guiBaseForms import CustomerForm
import time
log = initlog('guiRentMainForm')

class RentMainForm(CustomerForm):
    
    def __init__(self):
        super(RentMainForm, self).__init__()
        self.screenID = 'R2'
        self.preWindowID = 'MainForm'
        self.timeoutSec = 60
        self.lstResponseCtrl.extend([
            'ctr_movie_list',
            'ctr_shopping_cart',
            'ctr_tab_list',
            'btn_icon_keyboard',
            'RentMainForm_ctr_all_keyboard',
            'btn_slot_id',
            'RentMainForm_ctr_num_keyboard',
            'btn_cancel',
            'movie_scroll_bar'])

    
    def _initComponents(self):
        super(RentMainForm, self)._initComponents()
        self.iskeyboardShown = 0
        self.genreList = self._getGenreList()
        self._displayMovies(globalSession.firstKey, globalSession.firstGenreID)
        self.flash.send('ctr_tab_list', 'setTabList', {
            'ctr_tab_list': self.genreList,
            'focus': globalSession.firstGenreID })
        lstTitle = []
        for disc in globalSession.shoppingCart.discs:
            dict = { }
            dict['movie_title'] = disc.title
            lstTitle.append(dict)
        
        self.flash.send('ctr_shopping_cart', 'setTabList', {
            'ctr_shopping_cart': lstTitle })

    
    def _changeItem(self, item):
        item['color'] = ''
        if item['id'] == 'NEW RELEASE':
            if MKC_THEME == 'game':
                item['text'] = _('All Games')
            else:
                item['text'] = _('New Release')
        elif item['id'] == 'ALL DISCS':
            item['text'] = _('All Discs')
        elif item['id'] == 'ON SALE':
            if MKC_THEME == 'game':
                item['text'] = _('Clearance Games')
            elif self.connProxy._getConfigByKey('mainform_sale_price') == 'no':
                item['text'] = _('Clearance Discs')
            else:
                item['text'] = _('On Sale')
                item['color'] = 'red'
        else:
            item['text'] = _(item['text'])
        return item

    
    def get_processed_genre_list(self):
        gl = self.connProxy.getAllGenreList(MKC_THEME)
        return [self._changeItem(item) for item in gl]

    
    def _displayMovies(self, key, val):
        mvlist = self.connProxy.getAvailableMovieList(key, val)
        show_sale_price = False
        if self.connProxy._getConfigByKey('mainform_sale_price') == 'yes':
            show_sale_price = True
        
        for mv in mvlist:
            mv['movie_pic'] = getPicFullPath(mv.get('movie_pic'))
            mv['available_count'] = str(mv.get('available_count'))
            disc = Disc()
            disc.upc = mv.get('upc')
            self.movieProxy.getMovieDetailByUpc(disc)
            if 'rfid' in mv:
                disc.rfid = mv['rfid']
            else:
                disc.rfid = ''
            release = self.movieProxy.allowRental(disc)
            if release == '1':
                mv['available_count'] = '-1'
            
            if show_sale_price:
                self.connProxy.loadDiscInfo(disc, disc.rfid)
                mv['rental_price'] = disc.rentalPrice
                mv['sales_price'] = disc.salePrice
                mv['form'] = globalSession.loginType
            else:
                mv['form'] = ''
                mv['sales_price'] = '0.00'
                mv['rental_price'] = '0.00'
            if str(mv.get('is_bluray')) == '1':
                mv['is_bluray'] = '1'
            elif disc.discType == 'WII':
                mv['is_bluray'] = '2'
            elif disc.discType == 'XBOX360':
                mv['is_bluray'] = '3'
            elif disc.discType == 'PS3':
                mv['is_bluray'] = '4'
            else:
                mv['is_bluray'] = '0'
        
        self.flash.send('ctr_movie_list', 'setMovieList', {
            'ctr_movie_list': mvlist })
        text = _('Disc List')
        self.category = ''
        if key == 'genre':
            for itm in self.genreList:
                if itm.get('id') == val:
                    if val == 'NEW RELEASE':
                        text = _('%s By Date') % itm.get('text')
                    elif val == 'CATEGORY':
                        text = itm.get('text')
                        self.category = 'category'
                    elif val == 'ON SALE':
                        text = _('%s By Sale Price') % itm.get('text')
                    else:
                        text = _('%s By Title') % itm.get('text')
                    break
                
            
        elif key == 'keyword':
            text = _('Title contains "%s" ') % val
        
        self.flash.send('txt_rent_label', 'setText', {
            'text': text })
        if not mvlist and key == 'keyword':
            self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', { })
        

    
    def on_hide(self):
        super(RentMainForm, self).on_hide()
        self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'close', { })
        self.flash.send('%s_ctr_num_keyboard' % self.windowID, 'close', { })

    
    def on_ctr_movie_list_event(self):
        upc = self._getEventParam('ctr_movie_list', 'upc')
        rfid = self._getEventParam('ctr_movie_list', 'rfid')
        log.info('rfid---------%s:' % rfid)
        if upc:
            disc = Disc()
            disc.upc = upc
            disc.rfid = rfid
            disc.entrance = self.category
            globalSession.disc = disc
            self.connProxy.loadDiscInfo(globalSession.disc, rfid)
            self.nextWindowID = 'DiscDetailForm'
            self.windowJump = True
        

    
    def on_ctr_shopping_cart_event(self):
        if globalSession.shoppingCart.getSize() > 0:
            self.nextWindowID = 'ShoppingCartForm'
            self.windowJump = True
        

    
    def on_ctr_tab_list_event(self):
        genre = self._getEventParam('ctr_tab_list', 'genre')
        globalSession.firstKey = 'genre'
        globalSession.firstGenreID = genre
        self._displayMovies(globalSession.firstKey, globalSession.firstGenreID)

    
    def on_btn_icon_keyboard_event(self):
        if self.iskeyboardShown == 2:
            self.flash.send('%s_ctr_num_keyboard' % self.windowID, 'hide', { })
        
        self.iskeyboardShown = 1
        self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', { })
        self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'setType', {
            'type': 'text' })

    
    def on_RentMainForm_ctr_all_keyboard_event(self):
        eventType = self._getEventParam('RentMainForm_ctr_all_keyboard', 'type')
        if eventType == 'click':
            pass
        elif eventType == 'ok':
            inputVal = self._getEventParam('RentMainForm_ctr_all_keyboard', 'val')
            if str(inputVal).upper() == 'ADMIN':
                self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'show', {
                    'type': 'password' })
            elif str(inputVal).upper() == 'WELOVEBARRY':
                self.nextWindowID = 'FatalErrorForm'
                self.windowJump = True
            elif str(inputVal).upper() == 'WOSHIGONGREN':
                self.nextWindowID = 'SuperAdminMainForm'
                self.windowJump = True
            elif str(inputVal).upper() == str(self.connProxy._getConfigByKey('load_code')).upper():
                globalSession.param['priv'] = 'load'
                self.nextWindowID = 'AdminMainForm'
                self.windowJump = True
            elif str(inputVal).upper() == str(self.connProxy._getConfigByKey('unload_code')).upper():
                globalSession.param['priv'] = 'unload'
                self.nextWindowID = 'AdminMainForm'
                self.windowJump = True
            else:
                operatorCode = self.connProxy._getConfigByKey('operator_code')
                if str(inputVal).upper() == str(operatorCode).upper() and str(inputVal).upper() == str(operatorCode).upper()[0] and globalSession.param.get('test_mode'):
                    globalSession.param['priv'] = 'admin'
                    self.nextWindowID = 'AdminMainForm'
                    self.windowJump = True
                else:
                    globalSession.firstKey = 'keyword'
                    globalSession.firstGenreID = inputVal
                    self._displayMovies(globalSession.firstKey, globalSession.firstGenreID)
        

    
    def on_btn_slot_id_event(self):
        if self.iskeyboardShown == 1:
            self.flash.send('%s_ctr_all_keyboard' % self.windowID, 'hide', { })
        
        self.iskeyboardShown = 2
        self.flash.send('%s_ctr_num_keyboard' % self.windowID, 'show', { })

    
    def on_RentMainForm_ctr_num_keyboard_event(self):
        eventType = self._getEventParam('RentMainForm_ctr_num_keyboard', 'type')
        if eventType == 'click':
            pass
        elif eventType == 'ok':
            expressID = self._getEventParam('RentMainForm_ctr_num_keyboard', 'val')
            globalSession.disc = Disc()
            globalSession.disc.expressID = expressID
            self.connProxy.loadDiscInfo(globalSession.disc)
            if globalSession.disc.upc:
                self.nextWindowID = 'DiscDetailForm'
                self.windowJump = True
            else:
                self.flash.send('ctr_movie_list', 'setMovieList', {
                    'ctr_movie_list': [] })
                self.flash.send('%s_ctr_num_keyboard' % self.windowID, 'show', { })
        

    
    def on_btn_cancel_event(self):
        log.info('prewindowID:%s' % self.preWindowID)
        self.on_cancel()

    
    def on_movie_scroll_bar_event(self):
        pass


a = _('Action')
a = _('Action/Adventure')
a = _('Action/Comedy')
a = _('Afterlife')
a = _('Animation')
a = _('Anime')
a = _('Art/Foreign')
a = _('Ballet')
a = _('Childrens')
a = _('Comedies')
a = _('Comedy')
a = _('Comedy/Drama')
a = _('Dance/Ballet')
a = _('Documentary')
a = _('Drama')
a = _('Drama/Silent')
a = _('Dramas')
a = _('Exercise')
a = _('Family')
a = _('Fantasy')
a = _('Foreign')
a = _('Foreign Films')
a = _('Games')
a = _('Genres')
a = _('Gospel')
a = _('Horror')
a = _('Karaoke')
a = _('Kids/Family')
a = _('Late Night')
a = _('Music')
a = _('Musical')
a = _('Mystery')
a = _('Mystery/Suspense')
a = _('Oldies')
a = _('Opera')
a = _('Others')
a = _('Pop/Rock')
a = _('Rap')
a = _('Satire')
a = _('SciFI')
a = _('SciFi')
a = _('Science Fiction/Fantasy')
a = _('Silent')
a = _('Software')
a = _('Spanish')
a = _('Special Interest')
a = _('Spoken')
a = _('Sports')
a = _('Suspense')
a = _('Suspense/Horror')
a = _('Suspense/Thriller')
a = _('TV Classics')
a = _('TV Series')
a = _('Thriller')
a = _('VAR')
a = _('War')
a = _('Western')
a = _('Westerns')
