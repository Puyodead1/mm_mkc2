# Source Generated with Decompyle++
# File: init_mkcdb.pyc (Python 2.5)

'''
init mkc.db

Modules:
    config,
    shutil,
    ConnectionProxy

Change Log:
    2009-11-23  Modified by Kitch
        add config auto_receive_updates & auto_update_time
    2009-08-20  Modified by Kitch
        add table refunds
    2009-07-22  Modified by Kitch
        1. add ExternalIP to table info
        2. add table customer_behavior
    2009-06-03  Modified by Kitch
        add config load_code, enable_disc_out
    2009-05-04  Modified by Kitch
        add config grace_period
    2009-04-30  Modified by Kitch
        add config return_slot
    2009-04-07  Modified by Kitch
        change default T&C
    2009-04-03  Modified by Kitch
        add table commands
    2009-01-15  Modified by Kitch
        add config "run_test"
    2008-12-05  Modified by Kitch
        sync to dbnode
    2008-04-15  Created by Kitch

'''
__version__ = '0.5.0'
from .conn_proxy import ConnProxy
from . import config
import shutil
from . import tools
import os
BACKUP_DIR = os.path.join(config.USER_ROOT, 'backup/data/')
VERSION_FILE = os.path.join(config.USER_ROOT, 'kiosk/var/version.ini')

def escapeAlgorithm(algorithm):
    return algorithm.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;').replace("'", '&apos;')


def initDb():
    proxy = ConnProxy.getInstance()
    if not os.path.exists(BACKUP_DIR):
        os.mkdir(BACKUP_DIR)
    
    bakFileName = BACKUP_DIR + 'mkc.db.bak.' + tools.getCurTime('%Y-%m-%d')
    if not os.path.exists(bakFileName):
        shutil.copy(config.MKC_DB_PATH, bakFileName)
    
    kioskLogo = os.path.join(config.USER_ROOT, 'kiosk/var/gui/sys/kiosk_logo.png')
    defaultLogo = config.UI_PATH + 'default_logo.png'
    shutil.copy(defaultLogo, kioskLogo)
    sqlList = []
    sql = 'DELETE FROM cc;'
    sqlList.append(sql)
    sql = 'DELETE FROM commands;'
    sqlList.append(sql)
    sql = 'DELETE FROM declinedq;'
    sqlList.append(sql)
    sql = 'DELETE FROM events;'
    sqlList.append(sql)
    sql = 'DELETE FROM postauthq;'
    sqlList.append(sql)
    sql = 'DELETE FROM preauthq;'
    sqlList.append(sql)
    sql = 'DELETE FROM reservations;'
    sqlList.append(sql)
    sql = 'DELETE FROM rfid_cost;'
    sqlList.append(sql)
    sql = 'DELETE FROM rfids;'
    sqlList.append(sql)
    sql = 'DELETE FROM category;'
    sqlList.append(sql)
    sql = 'DELETE FROM shopping_carts;'
    sqlList.append(sql)
    sql = 'DELETE FROM transactions;'
    sqlList.append(sql)
    sql = 'DELETE FROM upc_load_config;'
    sqlList.append(sql)
    sql = 'DELETE FROM upg;'
    sqlList.append(sql)
    sql = 'DELETE FROM customer_behavior;'
    sqlList.append(sql)
    sql = 'DELETE FROM price_plans;'
    sqlList.append(sql)
    sql = 'DELETE FROM price_plans_week;'
    sqlList.append(sql)
    sql = "INSERT INTO price_plans_week(title, price_plan, price_plan_text, price_plan_br, price_plan_text_br, price_plan_game, price_plan_text_game) VALUES('%s', '', '', '', '', '', '');"
    sqlList.append(sql % 'Sunday')
    sqlList.append(sql % 'Monday')
    sqlList.append(sql % 'Tuesday')
    sqlList.append(sql % 'Wednesday')
    sqlList.append(sql % 'Thursday')
    sqlList.append(sql % 'Friday')
    sqlList.append(sql % 'Saturday')
    sql = 'DELETE FROM refunds;'
    sqlList.append(sql)
    sql = 'DELETE FROM card_read;'
    sqlList.append(sql)
    sql = 'DELETE FROM trs_process;'
    sqlList.append(sql)
    sql = 'DELETE FROM over_capacity_rfids;'
    sqlList.append(sql)
    sql = 'DELETE FROM failed_trs;'
    sqlList.append(sql)
    sql = "UPDATE config SET value='1' WHERE variable='default_price_plan';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='39.00' WHERE variable='default_sale_price';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='20.00' WHERE variable='default_cost';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='%s' WHERE variable='terms_and_conditions';"
    terms_and_conditions = 'Terms and Conditions\nTo rent a DVD, Video Game or other product from this Automated Kiosk you must swipe your credit card.\nBy swiping your credit card you certify that you are the legal owner of the card that you are at least 18 years of age, and that you agree to all of the Terms and Conditions listed herein. If you are under the age of 18 you may only use this Kiosk with the express permission of a Parent or Guardian.\n\n1. You agree to pay the rental rates as listed on the kiosk screen.\n2. If we are required to collect Sales Taxes in your area, either on rental, purchase or applicable Maximum Replacement Cost, they are additional to the rental price and you understand and agree that they are automatically applied to your credit card over and above the value of the rental.\n3. You understand and agree that your credit card will be charged an additional period fee, as displayed on the kiosk screen, for each additional period you keep the DVD, Video Game or other product beyond the return time.\n4. The Rental Day Limit allowed for a rental is  ___  after which the rental is converted into a sale.\n                a. DVD - $30.00\n                b. Blu-Ray - $35.00\n                c. Video Game - $45.00\n5. If the rental day limit has been reached, you have purchased the DVD, or Video Game or other product and do not need to return it.  If you return the DVD, Video Game, or other product after the replacement cost has been charged, you agree and understand that no refund will be issued, but that we will mail that product to you upon written request and payment of delivery charges.\n6. If the DVD, Video Game or other product is returned Damaged, without the original box or other product or information included in the box you understand and agree that your Payment Card will be assessed additional charges up to the Maximum Replacement Cost of that DVD, Video Game or other product.\n7. If you reserve a DVD online, the reservation period begins immediately.  You have 12 hours to pick up your reserved DVD(s).  Your reservation will expire after 12 hours and you will be charged a one night rental fee for each reserved DVD.\n8. If you have questions, comments or concerns, please contact: the owner / operator.'
    sql = sql % terms_and_conditions
    sqlList.append(sql)
    sql = "UPDATE config SET value='8.25' WHERE variable='sales_tax';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='6.825' WHERE variable='rentals_tax';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='10' WHERE variable='grace_period';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='14' WHERE variable='sale_convert_days';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='' WHERE variable='upg_acct_id';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='thismachineisgreat' WHERE variable='operator_code';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='$' WHERE variable='currency_symbol';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='kiosk' WHERE variable='arrangement';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='no' WHERE variable='show_mode';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='no' WHERE variable='upg_show_mode';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='594110' WHERE variable='show_mode_passcode';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='upg1.waven.com/upg/agent/upgAgent' WHERE variable='upg_url';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='' WHERE variable='kiosk_logo';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='' WHERE variable='kiosk_logo_md5';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='720' WHERE variable='reservation_expiration';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='yes' WHERE variable='rental_lock';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='39.00' WHERE variable='sale_convert_price';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='full' WHERE variable='preauth_method';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='0' WHERE variable='preauth_custom_amount';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='yes' WHERE variable='run_test';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='no' WHERE variable='rating_lock';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='' WHERE variable='tech_support_contact';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='3' WHERE variable='max_dvd_out';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='1' WHERE variable='buy_limit';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='80' WHERE variable='speaker_volume';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='disc' WHERE variable='return_options';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='auto' WHERE variable='return_slot';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='0' WHERE variable='grace_period';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='ineedfreshjuice' WHERE variable='load_code';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='yes' WHERE variable='enable_disc_out';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='en' WHERE variable='default_language';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='ihatefreshjuice' WHERE variable='unload_code';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='no' WHERE variable='enable_avs';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='' WHERE variable='payment_options';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='' WHERE variable='payment_params';"
    sqlList.append(sql)
    sql = "UPDATE config SET value=0 WHERE variable='robot_retry';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='default' WHERE variable='member_preauth';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='' WHERE variable='language_switch';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='no' WHERE variable='auto_receive_updates';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='02' WHERE variable='auto_update_time';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='no' WHERE variable='bluray_warning';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='' WHERE variable='shopping_cart_message';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='yes' WHERE variable='show_available_notice';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='no' WHERE variable='show_deposit_amount';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='no' WHERE variable='receive_adult_content';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='movie' WHERE variable='ui_theme';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='$2.99 Game Rentals' WHERE variable='kiosk_gr_slogan';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='0' WHERE variable='over_capacity_slots_limit';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='10' WHERE variable='over_capacity_alert_threshold';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='full' WHERE variable='preauth_method_br';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='0.00' WHERE variable='preauth_custom_amount_br';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='full' WHERE variable='preauth_method_game';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='0.00' WHERE variable='preauth_custom_amount_game';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='full' WHERE variable='preauth_method_cp';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='0.00' WHERE variable='preauth_custom_amount_cp';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='full' WHERE variable='preauth_method_cp_br';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='0.00' WHERE variable='preauth_custom_amount_cp_br';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='full' WHERE variable='preauth_method_cp_game';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='0.00' WHERE variable='preauth_custom_amount_cp_game';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='1' WHERE variable='reprocessing_interval';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='7' WHERE variable='reprocessing_count';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='default' WHERE variable='good_credibility_preauth';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='usa' WHERE variable='rating_system';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='100' WHERE variable='allow_rental_purchase';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='0' WHERE variable='bandwidth_limit';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='0' WHERE variable='sale_prevent_days';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='no' WHERE variable='mainform_sale_price';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='VGhlIEtpb3NrIHJlcXVpcmVzIE1haW50ZW5hbmNlLiAgV2UgYXBvbG9naXplIGZvciB0aGUgaW5jb252ZW5pZW5jZS4gUGxlYXNlIGNvbnRhY3Qgc3VwcG9ydCBhdCB0aGUgcGhvbmUgbnVtYmVyIGxpc3RlZCBiZWxvdw==' WHERE variable='error_message';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='' WHERE variable='return_time';"
    sqlList.append(sql)
    sql = "UPDATE config SET value='no' WHERE variable='enable_webcam';"
    sqlList.append(sql)
    sql = "UPDATE info SET value='%s' WHERE variable='KioskID';" % proxy.kioskId
    sqlList.append(sql)
    sql = "UPDATE info SET value='%s' WHERE variable='IP';" % str(tools.getEthIP()).strip()
    sqlList.append(sql)
    sql = "UPDATE info SET value='%s' WHERE variable='MAC';" % str(tools.getEthMac()).strip()
    sqlList.append(sql)
    
    try:
        kiosksoft = str(open(VERSION_FILE).readline()).strip()
        if kiosksoft:
            if not kiosksoft.startswith('V'):
                kiosksoft = 'V' + kiosksoft
            
        else:
            kiosksoft = str(config.KIOSKSOFT).strip()
    except:
        kiosksoft = str(config.KIOSKSOFT).strip()

    sql = "UPDATE info SET value='%s' WHERE variable='KioskSoft';" % kiosksoft
    sqlList.append(sql)
    sql = "UPDATE info SET value='%s' WHERE variable='Firmware';" % str(config.FIRMWARE).strip()
    sqlList.append(sql)
    sql = "UPDATE info SET value='%s' WHERE variable='KioskTimeZone';" % str(tools.getTimeZone()).strip()
    sqlList.append(sql)
    sql = "UPDATE info SET value='' WHERE variable='UMGChannel';"
    sqlList.append(sql)
    sql = "UPDATE info SET value='' WHERE variable='ExternalIP';"
    sqlList.append(sql)
    sql = "UPDATE info SET value='off' WHERE variable='HDMI';"
    sqlList.append(sql)
    sql = "UPDATE slots SET rfid='', state='empty';"
    sqlList.append(sql)
    proxy.mkcDb.updateTrs(sqlList)
    firstNight = 'factor = 1'
    nights = '\noutTime = params["out_time"]\ninTime = params["in_time"]\nfirstCutoffTime = str(outTime).split(" ")[0] + " 23:59:59"\nif firstCutoffTime < outTime:\n    firstCutoffTime = getTimeChange(firstCutoffTime, day=1)\nnights = 0\nnextCutoffTime = getTimeChange(firstCutoffTime, day=1)\nwhile nextCutoffTime < inTime:\n    nights += 1\n    oldTime = nextCutoffTime\n    nextCutoffTime = getTimeChange(nextCutoffTime, day=1)\n    if oldTime == nextCutoffTime:\n        break\nfactor = nights'
    factorsAlgorithm = '{"first_night":\'\'\'%s\'\'\', "nights":\'\'\'%s\'\'\'}'
    factorsAlgorithm = factorsAlgorithm % (firstNight, nights)
    factorsAlgorithm = escapeAlgorithm(factorsAlgorithm)
    algorithm = '\nfirstNight = float(factors["first_night"])\nnights= float(factors["nights"])\nresult = 1.99 * firstNight + 0.99 * nights'
    algorithm = escapeAlgorithm(algorithm)
    data1 = '\n<PRICE>\n    <FACTORS>first_night|nights</FACTORS>\n    <FACTORS_ALGORITHM>%s</FACTORS_ALGORITHM>\n    <ALGORITHM>%s</ALGORITHM>\n    <NOTES></NOTES>\n</PRICE>'
    data1 = data1 % (factorsAlgorithm, algorithm)
    sql1 = "INSERT INTO price_plans(data, data_text) VALUES(?, 'First Night Fee 1.99, \nAdditional Night Fee 0.99, \nCutoff Time 23:59:59');"
    firsthours24 = 'factor = 1'
    hours12 = '\noutTime = params["out_time"]\ninTime = params["in_time"]\naddiStartTime = getTimeChange(outTime, hour=24)\nif addiStartTime >= inTime:\n    addiHoursCount = 0\nelse:\n    addiHoursCount = 0\n    while addiStartTime < inTime:\n        addiHoursCount += 1\n        oldTime = addiStartTime\n        addiStartTime = getTimeChange(addiStartTime, hour=12)\n        if oldTime == addiStartTime:\n            break\nfactor = addiHoursCount'
    factorsAlgorithm = '{"first_24_hours":\'\'\'%s\'\'\', "12_hours":\'\'\'%s\'\'\'}'
    factorsAlgorithm = factorsAlgorithm % (firsthours24, hours12)
    factorsAlgorithm = escapeAlgorithm(factorsAlgorithm)
    algorithm = '\nfirsthours24 = float(factors["first_24_hours"])\nhours12 = float(factors["12_hours"])\nresult = 1.59 * firsthours24 + 0.99 * hours12'
    algorithm = escapeAlgorithm(algorithm)
    data2 = '\n<PRICE>\n    <FACTORS>first_24_hours|12_hours</FACTORS>\n    <FACTORS_ALGORITHM>%s</FACTORS_ALGORITHM>\n    <ALGORITHM>%s</ALGORITHM>\n    <NOTES></NOTES>\n</PRICE>'
    data2 = data2 % (factorsAlgorithm, algorithm)
    sql2 = "INSERT INTO price_plans(data, data_text) VALUES(?, 'First 24 hours Fee 1.59, \nNext per 12 hours Fee 0.99');"
    proxy.mkcDb.update(sql1, (data1,))
    proxy.mkcDb.update(sql2, (data2,))
    sqlList = []
    sql = 'DELETE FROM db_sync;'
    sqlList.append(sql)
    sql = 'DELETE FROM db_sync_remote_kiosk;'
    sqlList.append(sql)
    proxy.syncDb.updateTrs(sqlList)
    
    try:
        from . import server_kiosk_sync_thread
        ku = server_kiosk_sync_thread.KioskUtils()
        ku.downloadPricePlans()
        del ku
    except:
        pass

    sqlList = []
    rows = proxy.mkcDb.query('SELECT sql FROM sqlite_master;')
    if rows:
        for row in rows:
            if row[0]:
                sqlList.append(str(row[0]) + ';')
            
        
    
    rows = proxy.mkcDb.query('SELECT variable, value FROM config;')
    if rows:
        for row in rows:
            (variable, value) = row
            sql = "INSERT INTO config(variable, value) VALUES('%s', '%s');"
            sql = sql % (variable.replace("'", "''"), value.replace("'", "''"))
            sqlList.append(sql)
        
    
    rows = proxy.mkcDb.query('SELECT variable, value FROM info;')
    if rows:
        for row in rows:
            (variable, value) = row
            sql = "INSERT INTO info(variable, value) VALUES('%s', '%s');"
            sql = sql % (variable.replace("'", "''"), value.replace("'", "''"))
            sqlList.append(sql)
        
    
    rows = proxy.mkcDb.query('SELECT data, data_text FROM price_plans;')
    if rows:
        for row in rows:
            (data, data_text) = row
            sql = "INSERT INTO price_plans(data, data_text) VALUES('%s', '%s');"
            sql = sql % (data.replace("'", "''"), data_text.replace("'", "''"))
            sqlList.append(sql)
        
    
    rows = proxy.mkcDb.query('SELECT title, price_plan, price_plan_text FROM price_plans_week;')
    if rows:
        for row in rows:
            (title, price_plan, price_plan_text) = row
            sql = "INSERT INTO price_plans_week(title, price_plan, price_plan_text) VALUES('%s', '%s', '%s');"
            sql = sql % (str(title).replace("'", "''"), str(price_plan).replace("'", "''"), str(price_plan_text).replace("'", "''"))
            sqlList.append(sql)
        
    
    rows = proxy.mkcDb.query('SELECT id, rank FROM slots;')
    if rows:
        for row in rows:
            (id, rank) = row
            sql = "INSERT INTO slots(id, rank) VALUES('%s', '%s');"
            sql = sql % (str(id).replace("'", "''"), str(rank).replace("'", "''"))
            sqlList.append(sql)
        
    
    schema = '\n'.join(sqlList)
    funcName = 'dbSyncInitMKCDb'
    params = {
        'schema': schema }
    proxy.syncData(funcName, params)
    
    try:
        proxy.syncDb.update('DELETE FROM server_queue;')
    except:
        pass

    
    try:
        os.system('rm -f %s' % os.path.join(config.USER_ROOT, 'kiosk', 'var', 'mkd.sys', '.ownership'))
    except:
        pass

    print('\n*********Done!')


def main():
    print('start...')
    initDb()
    print('end')

if __name__ == '__main__':
    main()

