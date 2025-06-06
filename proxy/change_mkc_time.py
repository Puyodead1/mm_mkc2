# Source Generated with Decompyle++
# File: change_mkc_time.pyc (Python 2.5)

'''
##  Change all the time of the mkc.db, only used after change timezone.
##
##  Change Log:
##      2009-03-13 Modified by Tim
##          Alterable delay hours.
'''
import os
import sys
from optparse import OptionParser
from .mda import Db
from .config import MKC_DB_PATH
from .tools import getTimeChange, getKioskId
KIOSK_ID = getKioskId()
DELAY_HOURS = 0
db = Db(MKC_DB_PATH)

def changeDeclinedq():
    print('changeDeclinedq')
    sql = 'SELECT id, process_time, next_process_time FROM declinedq;'
    rows = db.query(sql)
    all = []
    for dqId, process_time, next_process_time in rows:
        process_time = getTimeChange(process_time, hour = DELAY_HOURS)
        next_process_time = getTimeChange(next_process_time, hour = DELAY_HOURS)
        all.append((process_time, next_process_time, dqId))
    
    sql = 'UPDATE declinedq SET process_time=?, next_process_time=? WHERE id=?;'
    db.updateMany(sql, all)


def changeEvents():
    print('changeEvents')
    sql = 'SELECT id, time_recorded, time_updated FROM events;'
    rows = db.query(sql)
    all = []
    for eventId, time_recorded, time_updated in rows:
        time_recorded = getTimeChange(time_recorded, hour = DELAY_HOURS)
        time_updated = getTimeChange(time_updated, hour = DELAY_HOURS)
        all.append((time_recorded, time_updated, eventId))
    
    sql = 'UPDATE events SET time_recorded=?, time_updated=? WHERE id=?;'
    db.updateMany(sql, all)


def changePostauthq():
    print('changePostauthq')
    sql = 'SELECT id, add_time FROM postauthq;'
    rows = db.query(sql)
    all = []
    for Id, add_time in rows:
        add_time = getTimeChange(add_time, hour = DELAY_HOURS)
        all.append((add_time, Id))
    
    sql = 'UPDATE postauthq SET add_time=? WHERE id=?;'
    db.updateMany(sql, all)


def changePreauthq():
    print('changePreauthq')
    sql = 'SELECT id, preauth_time, last_access_time FROM preauthq;'
    rows = db.query(sql)
    all = []
    for Id, preauth_time, last_access_time in rows:
        preauth_time = getTimeChange(preauth_time, hour = DELAY_HOURS)
        last_access_time = getTimeChange(last_access_time, hour = DELAY_HOURS)
        all.append((preauth_time, last_access_time, Id))
    
    sql = 'UPDATE preauthq SET preauth_time=?, last_access_time=? WHERE id=?;'
    db.updateMany(sql, all)


def changeReservations():
    print('changeReservations')
    sql = 'SELECT id, reserve_time FROM reservations;'
    rows = db.query(sql)
    all = []
    for Id, reserve_time in rows:
        reserve_time = getTimeChange(reserve_time, hour = DELAY_HOURS)
        all.append((reserve_time, Id))
    
    sql = 'UPDATE reservations SET reserve_time=? WHERE id=?;'
    db.updateMany(sql, all)


def changeShoppingCarts():
    print('changeShoppingCarts')
    sql = 'SELECT id, time_open, time_close FROM shopping_carts;'
    rows = db.query(sql)
    open = []
    close = []
    for Id, time_open, time_close in rows:
        if time_close:
            time_open = getTimeChange(time_open, hour = DELAY_HOURS)
            time_close = getTimeChange(time_close, hour = DELAY_HOURS)
            close.append((time_open, time_close, Id))
        else:
            time_open = getTimeChange(time_open, hour = DELAY_HOURS)
            open.append((time_open, Id))
    
    print('closed')
    sql = 'UPDATE shopping_carts SET time_open=?, time_close=? WHERE id=?;'
    db.updateMany(sql, close)
    print('open')
    sql = 'UPDATE shopping_carts SET time_open=? WHERE id=?;'
    db.updateMany(sql, open)


def changeTransactions():
    print('changeTransactions')
    sql = 'SELECT id, out_time, in_time FROM transactions;'
    rows = db.query(sql)
    ins = []
    outs = []
    for Id, out_time, in_time in rows:
        if in_time:
            out_time = getTimeChange(out_time, hour = DELAY_HOURS)
            in_time = getTimeChange(in_time, hour = DELAY_HOURS)
            ins.append((out_time, in_time, Id))
        else:
            out_time = getTimeChange(out_time, hour = DELAY_HOURS)
            outs.append((out_time, Id))
    
    print('ins')
    sql = 'UPDATE transactions SET out_time=?, in_time=? WHERE id=?;'
    db.updateMany(sql, ins)
    print('outs')
    sql = 'UPDATE transactions SET out_time=? WHERE id=?;'
    db.updateMany(sql, outs)


def changeUpg():
    print('changeUpg')
    sql = 'SELECT id, time FROM upg;'
    rows = db.query(sql)
    all = []
    for Id, upg_time in rows:
        upg_time = getTimeChange(upg_time, hour = DELAY_HOURS)
        all.append((upg_time, Id))
    
    sql = 'UPDATE upg SET time=? WHERE id=?;'
    db.updateMany(sql, all)

USEAGE = '\n    python %prog [options] -h\n'

def main():
    global DELAY_HOURS
    op = OptionParser(USEAGE)
    op.add_option('-d', '--delay_hours', action = 'store', dest = 'delayHours', type = 'string', help = 'The hours you want to delay.')
    (options, args) = op.parse_args(sys.argv[1:])
    
    try:
        if options.delayHours and options.delayHours.lstrip(' -').isdigit():
            c = input('Change all the time of the mkc.db, only used after change timezone, it is dangerous, continue (yes)|no?')
            if c.lower() not in ('y', '', 'yes'):
                os.abort()
            
            DELAY_HOURS = int(options.delayHours)
            changeDeclinedq()
            changeEvents()
            changePostauthq()
            changePreauthq()
            changeReservations()
            changeShoppingCarts()
            changeTransactions()
            changeUpg()
        else:
            print('=' * 10)
            print('We want a digital.')
            print('=' * 10)
            op.print_help()
    except Exception as ex:
        print('Error ..... ', ex)
        print(op.print_help())


if __name__ == '__main__':
    main()

