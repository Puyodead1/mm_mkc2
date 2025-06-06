# Source Generated with Decompyle++
# File: m0_3_6to0_4_0.pyc (Python 2.5)

'''
##  Migrate the kiosk from 0.3.7 to 0.4.0.
##
##  Change Log:
##      2009-01-21 Created by Tim
##
'''
import pexpect
import sys
import base64
import shutil
from . import upg_proxy
from . import config
from . import mda
from . import tools
import sys
sys.path.append(config.MKC_PATH)
import mobject
OLD_UPC_DB_PATH = '/home/puyodead1/kiosk/db/upc.db.036'

def bakDbs():
    '''
    Back up dbs.
    '''
    shutil.copy(config.MKC_DB_PATH, config.MKC_DB_PATH + '.3.6.0')
    shutil.copy(config.UPC_DB_PATH, config.UPC_DB_PATH + '.3.6.0')


def migrateCc():
    '''
    Migrate cc table to service side.
    '''
    print('migrate CC start ...')
    sql = 'SELECT id, number, name, expdate, track1, track2, display FROM cc;'
    db = mda.Db(config.MKC_DB_PATH)
    rows = db.query(sql)
    upgProxy = upg_proxy.UPGProxy.getInstance()
    customer = mobject.Customer()
    for row in rows:
        (cc_id, number, name, expdate, track1, track2, display) = row
        customer.ccName = name
        customer.ccNum = upgProxy._decodeStr(number)
        customer.ccExpDate = expdate
        customer.track1 = upgProxy._decodeStr(track1)
        customer.track2 = upgProxy._decodeStr(track2)
        s = upgProxy.getCCInfoByCustomer(customer)
        if s == 1:
            raise Exception('Internal error in migrateCc when getCCInfoByCustomer.')
        elif s == 2:
            raise Exception('Remote error in migrateCc when getCCInfoByCustomer.')
        
        new_cc_id = customer.ccid
        print(cc_id, new_cc_id)
        sql = 'UPDATE declinedq SET cc_id=? WHERE cc_id=?;'
        db.update(sql, (new_cc_id, cc_id))
        sql = 'UPDATE postauthq SET cc_id=? WHERE cc_id=?;'
        db.update(sql, (new_cc_id, cc_id))
        sql = 'UPDATE preauthq SET cc_id=? WHERE cc_id=?;'
        db.update(sql, (new_cc_id, cc_id))
        sql = 'UPDATE reservations SET cc_id=? WHERE cc_id=?;'
        db.update(sql, (new_cc_id, cc_id))
        sql = 'UPDATE shopping_carts SET cc_id=? WHERE cc_id=?;'
        db.update(sql, (new_cc_id, cc_id))
        sql = 'UPDATE transactions SET cc_id=? WHERE cc_id=?;'
        db.update(sql, (new_cc_id, cc_id))
        sql = 'UPDATE upg SET cc_id=? WHERE cc_id=?;'
        db.update(sql, (new_cc_id, cc_id))
        sql = 'DELETE FROM cc WHERE id=?;'
        db.update(sql, (cc_id,))
    
    del db
    print('migrate CC end ...')


def migrateMedia():
    '''
    Migrate media table from upc.db to media.db.
    '''
    print('migrateMedia start ...')
    db = mda.Db(config.MEDIA_DB_PATH)
    mediaSch = '\nCREATE TABLE media\n(\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\n    upc TEXT,\n    media_name TEXT,\n    media_md5 TEXT,\n    state TEXT DEFAULT "notconnect",\n    create_time TEXT,\n    download_url TEXT,\n    last_access_time TEXT\n);\n    '
    sql = "ATTACH DATABASE '%s' AS upcDb;" % OLD_UPC_DB_PATH
    db.update(sql)
    sql = 'INSERT INTO media(upc, media_name, media_md5, state, create_time,download_url) SELECT upc, media_name, media_md5, state, create_time, download_url FROM upcDb.media;'
    db.update(sql)
    del db
    print('migrateMedia end ...')


def migrateMkc():
    sqlList = []
    newConfig = {
        'preauth_method': "insert into config(variable, value) values('preauth_method', 'full');",
        'preauth_custom_amount': "insert into config(variable, value) values('preauth_custom_amount', '0');",
        'sale_convert_price': "insert into config(variable, value) values('sale_convert_price', '39.00');",
        'run_test': "insert into config(variable, value) values('run_test', 'yes');",
        'rating_lock': "insert into config(variable, value) values('rating_lock', 'no');",
        'tech_support_contact': "insert into config(variable, value) values('tech_support_contact', '');",
        'show_mode_passcode': "insert into config(variable, value) values('show_mode_passcode', '594110');",
        'upg_url': "insert into config(variable, value) values('upg_url', 'upg1.waven.com/upg/agent/upgAgent');",
        'kiosk_logo': "insert into config(variable, value) values('kiosk_logo', '');",
        'reservation_expiration': "insert into config(variable, value) values('reservation_expiration', '720');",
        'rental_lock': "insert into config(variable, value) values('rental_lock', 'yes');",
        'max_dvd_out': "insert into config(variable, value) values('max_dvd_out', '10');",
        'speaker_volume': "insert into config(variable, value) values('speaker_volume', '80');",
        'buy_limit': "insert into config(variable, value) values('buy_limit', '5');",
        'return_options': "insert into config(variable, value) values('return_options', 'disc');" }
    db = mda.Db(config.MKC_DB_PATH)
    for key in list(newConfig.keys()):
        sql = 'SELECT value FROM config WHERE variable=?;'
        row = db.query(sql, 'one', (key,))
        if not row:
            sql = newConfig[key]
            sqlList.append(sql)
        
    
    sql = 'alter table rfids add column sale_convert_price TEXT;'
    sqlList.append(sql)
    sql = "UPDATE rfids SET sale_convert_price='39.00';"
    sqlList.append(sql)
    sql = 'alter table upc_load_config add column sale_convert_price TEXT;'
    sqlList.append(sql)
    sql = "UPDATE upc_load_config SET sale_convert_price='39.00';"
    sqlList.append(sql)
    sql = "ATTACH DATABASE '%s' AS upcDb;" % config.UPC_DB_PATH
    sqlList.append(sql)
    sql = 'alter table rfids add column movie_id TEXT;'
    sqlList.append(sql)
    sql = 'UPDATE rfids SET movie_id=(SELECT movie_id FROM upcDb.upc AS U WHERE U.upc=rfids.upc);'
    sqlList.append(sql)
    sql = "ALTER TABLE shopping_carts RENAME TO 'shopping_carts_tmp';"
    sqlList.append(sql)
    sql = 'CREATE TABLE shopping_carts\n        (\n             id TEXT PRIMARY KEY,\n             cc_id INTEGER,\n             upg_id INTEGER,\n             time_open TEXT,\n             time_close TEXT,\n             coupon_code TEXT,\n             coupon_plan TEXT\n        );'
    sqlList.append(sql)
    sql = 'INSERT INTO shopping_carts SELECT * FROM shopping_carts_tmp;'
    sqlList.append(sql)
    sql = 'DROP TABLE shopping_carts_tmp;'
    sqlList.append(sql)
    db.updateTrs(sqlList)
    del db


def rsyncDb():
    db = mda.Db(config.SYNC_DB_PATH)
    sql = 'UPDATE db_sync SET state=1;'
    db.update(sql)
    sql = 'UPDATE db_sync_remote_kiosk SET state=1;'
    db.update(sql)
    del db


def main():
    bakDbs()
    migrateCc()
    migrateMedia()
    migrateMkc()
    rsyncDb()

if __name__ == '__main__':
    main()

