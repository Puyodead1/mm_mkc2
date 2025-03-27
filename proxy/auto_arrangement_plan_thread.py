# Source Generated with Decompyle++
# File: auto_arrangement_plan_thread.pyc (Python 2.5)

''' make the data of auto-arrange plan which the kiosk owner has set

    Change Log:
        2011-02-09  Modified by Kitch
            change logic for S500 in methods: _separateSlotsState
        2010-11-18 Created by Kitch
'''
import os
import sys
import time
from .tools import getCurTime, getWeekday, getTimeChange
from .tools import getLog, isLocked, fmtNoneStr, getKioskCapacity
from .conn_proxy import ConnProxy
from .movie_proxy import MovieProxy
log = getLog('auto_arrangement_plan_thread.log', 'AUTO_ARRANGEMENT_PLAN_THREAD')
connProxy = ConnProxy().getInstance()
movieProxy = MovieProxy().getInstance()

def _getPlans():
    ''' get the auto-arramge plan list from mkc.db
    '''
    plans = []
    
    try:
        sql = 'SELECT id, arrange_params, arrange_date, arrange_time, generate_time, state FROM remote_arrangement_plans;'
        rows = connProxy.mkcDb.query(sql)
        if rows:
            for row in rows:
                plan = { }
                plan['id'] = row[0]
                plan['arrange_params'] = row[1]
                plan['arrange_date'] = row[2]
                plan['arrange_time'] = row[3]
                plan['generate_time'] = row[4]
                plan['state'] = row[5]
                plans.append(plan)
            
    except Exception:
        ex = None
        log.error('_getPlans: %s' % str(ex))

    return plans


def _saveArrangeData(planId, data, processTime):
    ''' save the arranement data into mkc.db

    and change the generate time of table remote_arrangement_plans
    '''
    
    try:
        data = str(data)
        sql = "SELECT id FROM commands WHERE state='active' AND command='arrange_slots';"
        row = connProxy.mkcDb.query(sql, 'one')
        cid = 0
        if row:
            (cid,) = row
        
        if cid:
            sql = 'UPDATE commands SET data=?, time_begin=? WHERE id=?;'
            connProxy.mkcDb.update(sql, (data, processTime, cid))
        else:
            sql = "INSERT INTO commands(command, data, time_begin) VALUES('arrange_slots', ?, ?);"
            connProxy.mkcDb.update(sql, (data, processTime))
        sql = 'UPDATE remote_arrangement_plans SET generate_time=? WHERE id=?;'
        connProxy.mkcDb.update(sql, (getCurTime(), planId))
    except Exception:
        ex = None
        log.error('_saveArrangeData: %s' % str(ex))



def _getSlots():
    ''' get the slots data
    '''
    slots = []
    
    try:
        sql = 'SELECT s.id, s.state AS slot_state, r.title, r.upc, r.rfid, r.state AS rfid_state FROM slots AS s LEFT JOIN rfids AS r ON s.rfid=r.rfid;'
        rows = connProxy.mkcDb.query(sql)
        if rows:
            for row in rows:
                data = { }
                (id, slotState, title, upc, rfid, rfidState) = row
                data['id'] = id
                data['rfid'] = fmtNoneStr(rfid)
                data['title'] = fmtNoneStr(title)
                data['upc'] = fmtNoneStr(upc)
                data['slot_state'] = fmtNoneStr(slotState)
                data['rfid_state'] = fmtNoneStr(rfidState)
                slots.append(data)
            
    except Exception:
        ex = None
        log.error('_getSlots: %s' % str(ex))

    return slots


def _separateSlotsState(kioskSlots, fr):
    ''' separate the slots to can be moved slots 

    and can not be moved slots
    '''
    canSlots = []
    notSlots = []
    if fr == '0':
        for itm in kioskSlots:
            if itm['slot_state'].lower() == 'empty':
                pass
            elif itm['rfid_state'] in ('in', 'unload', 'out'):
                canSlots.append({
                    'slot_id': itm['id'],
                    'rfid': itm['rfid'],
                    'title': itm['title'],
                    'upc': itm['upc'],
                    'state': itm['rfid_state'] })
            elif itm['slot_state'].lower() == 'occupied':
                state = itm['rfid_state'].lower()
            else:
                state = itm['slot_state'].lower()
            notSlots.append({
                'slot_id': itm['id'],
                'rfid': itm['rfid'],
                'title': itm['title'],
                'upc': itm['upc'],
                'state': state })
        
    elif fr == '1':
        for itm in kioskSlots:
            if itm['slot_state'].lower() == 'empty':
                pass
            elif itm['rfid_state'] in ('in', 'unload', 'out') and str(itm['id']) < '500':
                canSlots.append({
                    'slot_id': itm['id'],
                    'rfid': itm['rfid'],
                    'title': itm['title'],
                    'upc': itm['upc'],
                    'state': itm['rfid_state'] })
            elif itm['slot_state'].lower() == 'occupied':
                state = itm['rfid_state'].lower()
            else:
                state = itm['slot_state'].lower()
            notSlots.append({
                'slot_id': itm['id'],
                'rfid': itm['rfid'],
                'title': itm['title'],
                'upc': itm['upc'],
                'state': state })
        
    elif fr == '2':
        for itm in kioskSlots:
            if itm['slot_state'].lower() != 'empty':
                kioskCapacity = getKioskCapacity()
                if kioskCapacity == '250' and str(itm['id']).startswith('1'):
                    leftFront = True
                elif kioskCapacity == '500' and str(itm['id']) < '300':
                    leftFront = True
                else:
                    leftFront = False
                if itm['rfid_state'] in ('in', 'unload', 'out') and leftFront:
                    canSlots.append({
                        'slot_id': itm['id'],
                        'rfid': itm['rfid'],
                        'title': itm['title'],
                        'upc': itm['upc'],
                        'state': itm['rfid_state'] })
                elif itm['slot_state'].lower() == 'occupied':
                    state = itm['rfid_state'].lower()
                else:
                    state = itm['slot_state'].lower()
                notSlots.append({
                    'slot_id': itm['id'],
                    'rfid': itm['rfid'],
                    'title': itm['title'],
                    'upc': itm['upc'],
                    'state': state })
            
        
    elif fr == '3':
        for itm in kioskSlots:
            if itm['slot_state'].lower() != 'empty':
                kioskCapacity = getKioskCapacity()
                if kioskCapacity == '250' and str(itm['id']).startswith('2'):
                    rightFront = True
                elif kioskCapacity == '500' and str(itm['id']) > '300' and str(itm['id']) < '500':
                    rightFront = True
                else:
                    rightFront = False
                if itm['rfid_state'] in ('in', 'unload', 'out') and rightFront:
                    canSlots.append({
                        'slot_id': itm['id'],
                        'rfid': itm['rfid'],
                        'title': itm['title'],
                        'upc': itm['upc'],
                        'state': itm['rfid_state'] })
                elif itm['slot_state'].lower() == 'occupied':
                    state = itm['rfid_state'].lower()
                else:
                    state = itm['slot_state'].lower()
                notSlots.append({
                    'slot_id': itm['id'],
                    'rfid': itm['rfid'],
                    'title': itm['title'],
                    'upc': itm['upc'],
                    'state': state })
            
        
    
    return (canSlots, notSlots)


def _arrangeSlots(canSlots, notSlots, fr):
    ''' rearrange the slots
    '''
    slots = []
    slotIdsAll = _getSlots()
    for item in slotIdsAll:
        slots.append({
            'slot_id': item['id'],
            'rfid': None,
            'state': 'empty' })
    
    for item in notSlots:
        for i in range(len(slots)):
            if slots[i]['slot_id'] == item['slot_id']:
                slots.pop(i)
                slots.insert(i, item)
                break
            
        
    
    if fr == '3':
        for item in canSlots:
            for i in range(len(slots)):
                slot_id = slots[i]['slot_id']
                if slots[i]['state'] == 'empty':
                    if kioskCapacity == '250' and str(slot_id).startswith('2'):
                        slots.pop(i)
                        slots.insert(i, {
                            'slot_id': slot_id,
                            'rfid': item['rfid'],
                            'state': item['state'] })
                        break
                    elif kioskCapacity == '500' and str(slot_id) > '300' and str(slot_id) < '500':
                        slots.pop(i)
                        slots.insert(i, {
                            'slot_id': slot_id,
                            'rfid': item['rfid'],
                            'state': item['state'] })
                        break
                    
                
            
        
    else:
        for item in canSlots:
            for i in range(len(slots)):
                if slots[i]['state'] == 'empty':
                    slot_id = slots[i]['slot_id']
                    slots.pop(i)
                    slots.insert(i, {
                        'slot_id': slot_id,
                        'rfid': item['rfid'],
                        'state': item['state'] })
                    break
                
            
        
    return [(item['slot_id'], item['rfid']) for item in slots]


def _makeData(arrangeParams, arrangeDate, arrangeTime, generateTime, state):
    ''' make the arranement data according to arrangeParams, 

    arrangeDate, arrangeTime, generateTime and state
    create the data under the following situations only:
    1. \'active\' state
    2. today\'s weekday is in the arrangeDate
    3. <=10 minutes ahead of the arrangeTime or later
    4. generateTime is not today

    @params arrangeParams: the auto-arrange params with 
                           sort_key, sort_order and fr(front rack): XX, XX, XX
    @params arrangeDate: the arrange weekday "list": 0,1,2,...
    @params arrangeTime: the arrange time: "XX:XX:XX"
    @params state: \'active\' or \'inactive\'
    @return data: the arranement data: [(101, \'00E9C42730000104E0\'), (102, None), ...]
    '''
    slots = None
    
    try:
        params = eval(arrangeParams)
        sortKey = params['sort_key']
        sortOrder = params['sort_order']
        fr = params['fr']
        now = getCurTime()
        today = getCurTime('%Y-%m-%d')
        planTime = '%s %s' % (today, arrangeTime)
        planTime10MinsAgo = getTimeChange(planTime, minute = -10)
        print(now, today, planTime, planTime10MinsAgo)
        if state != 'active':
            print('state')
            return None
        
        if str(getWeekday(now)) not in arrangeDate.split(','):
            print('weekday')
            return None
        
        if planTime10MinsAgo > now:
            print('process time')
            return None
        
        if str(generateTime).find(today) >= 0:
            print('generate time')
            return None
        
        if sortOrder == 'asc':
            reverse = False
        else:
            reverse = True
        if sortKey.lower() == 'title':
            
            try:
                kioskSlots = _getSlots()
                (canSlots, notSlots) = _separateSlotsState(kioskSlots, fr.lower())
                canSlots.sort(cmp = (lambda x, y: cmp(str(x['title']).lower(), str(y['title']).lower())), reverse = reverse)
                slots = _arrangeSlots(canSlots, notSlots, fr)
            except Exception:
                ex = None
                log.error("when sort_key is 'title' in _makeData: %s" % str(ex))

        elif sortKey == 'release_date':
            
            try:
                kioskSlots = _getSlots()
                (canSlots, notSlots) = _separateSlotsState(kioskSlots, fr.lower())
                upcList = []
                for itm in canSlots:
                    upcList.append(itm['upc'])
                
                movieList = movieProxy.getMovieListByUpcListEspSyn(upcList)
                for itm in canSlots:
                    itm['release_date'] = ''
                    for movie in movieList:
                        if movie['upc'] == itm['upc']:
                            itm['release_date'] = movie['dvd_release_date']
                            break
                        
                    
                
                canSlots.sort(cmp = (lambda x, y: cmp(str(x['release_date']).lower() + str(x['title']).lower(), str(y['release_date']).lower() + str(y['title']).lower())), reverse = reverse)
                slots = _arrangeSlots(canSlots, notSlots, fr)
            except Exception:
                ex = None
                log.error("when sort_key is 'release_date' in _makeData: %s" % str(ex))

        elif sortKey == 'disc_type':
            
            try:
                kioskSlots = _getSlots()
                (canSlots, notSlots) = _separateSlotsState(kioskSlots, fr.lower())
                upcList = []
                for itm in canSlots:
                    upcList.append(itm['upc'])
                
                movieList = movieProxy.getMovieListByUpcListEspSyn(upcList)
                for itm in canSlots:
                    itm['sort'] = ''
                    for movie in movieList:
                        if movie['upc'] == itm['upc']:
                            movie['dvd_version'] = str(movie['dvd_version']).lower()
                            if movie['dvd_version'].find('blu') >= 0 and movie['dvd_version'].find('ray') >= 0:
                                itm['sort'] = '1'
                            elif sortOrder == 'asc':
                                if movie['genre'] == 'Games':
                                    itm['sort'] = '0'
                                else:
                                    itm['sort'] = '2'
                            elif movie['genre'] == 'Games':
                                itm['sort'] = '2'
                            else:
                                itm['sort'] = '0'
                            break
                        
                    
                
                canSlots.sort(cmp = (lambda x, y: cmp(x['sort'] + str(x['title']).lower(), y['sort'] + str(y['title']).lower())))
                slots = _arrangeSlots(canSlots, notSlots, fr)
            except Exception:
                ex = None
                log.error("when sort_key is 'disc_type' in _makeData: %s" % str(ex))

        elif sortKey == 'upc':
            
            try:
                kioskSlots = _getSlots()
                (canSlots, notSlots) = _separateSlotsState(kioskSlots, fr.lower())
                allSlotIds = [ str(itm['id']) for itm in kioskSlots ]
                notSlotIds = [ str(itm['slot_id']) for itm in notSlots ]
                allCanSlotIds = [] if itm not in notSlotIds else []
                allCanSlotIds.sort()
                frontSlots = []
                backSlots = []
                canSlots.sort(cmp = (lambda x, y: cmp(str(x['title']).lower(), str(y['title']).lower())))
                for itm in canSlots:
                    found = 0
                    for fs in frontSlots:
                        pass
                    
                    if found:
                        allCanSlotIds.remove(max(allCanSlotIds))
                        backSlots.insert(0, itm)
                    else:
                        allCanSlotIds.remove(min(allCanSlotIds))
                        frontSlots.append(itm)
                
                for itm in allCanSlotIds:
                    if int(itm) < 300:
                        frontSlots.append({
                            'slot_id': '',
                            'title': '',
                            'upc': '',
                            'rfid': None,
                            'state': '' })
                    else:
                        backSlots.insert(0, {
                            'slot_id': '',
                            'title': '',
                            'upc': '',
                            'rfid': None,
                            'state': '' })
                
                canSlots = frontSlots + backSlots
                slots = _arrangeSlots(canSlots, notSlots, fr)
            except Exception:
                ex = None
                log.error("when sort_key is 'upc' in _makeData: %s" % str(ex))

    except Exception:
        ex = None
        log.error('_makeData: %s' % str(ex))

    return slots


def run():
    ''' main routine
    '''
    while True:
        lock = isLocked()
        print('lock: ', lock)
        if str(lock) == '0':
            plans = _getPlans()
            print(plans)
            if plans:
                for plan in plans:
                    planId = plan['id']
                    arrangeParams = plan['arrange_params']
                    arrangeDate = plan['arrange_date']
                    arrangeTime = plan['arrange_time']
                    generateTime = plan['generate_time']
                    state = plan['state']
                    data = _makeData(arrangeParams, arrangeDate, arrangeTime, generateTime, state)
                    print('data: ', data)
                    if data:
                        _saveArrangeData(planId, data, getCurTime())
                    
                
            
        
        time.sleep(600)

if __name__ == '__main__':
    run()

