# Source Generated with Decompyle++
# File: db.pyc (Python 2.5)

'''
MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2009-02-20 Vincent
vincent.chen@cereson.com

Filename: db.py
DB validation

Change Log:
    2010-03-10  Modified by Kitch
        add index to table transactions
    2009-11-24  Modified by Kitch
        add field ms_expi_time(monthly subscription expired time) to table transactions & reservations
    2009-11-23  Modified by Kitch
        add config auto_receive_updates & auto_update_time
    2009-11-18  Modified by Kitch
        add config offset2xx & offset6xx
    2009-10-27  Modified by Kitch
        add table category
    2009-10-09  Modified by Kitch
        add field pickup_code to table reservations
    2009-08-20  Modified by Kitch
        add table refunds
    2009-07-22  Modified by Kitch
        1. add ExternalIP to table info
        2. add table customer_behavior
    2009-06-08  Modified by Kitch
        1. add fields upc, title, genre, price_plan, price_plan_text,
           coupon_code, coupon_plan, coupon_text to table reservations
        2. add field coupon_text to table transactions
    2009-06-05  Modified by Kitch
        add field price_plan_dynamic in rfids and upc_load_config
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
'''
__version__ = '0.5.2'
import re
from pysqlite2 import dbapi2 as sqlite
from .conn_proxy import ConnProxy
from .config import *
from .tools import getKioskCapacity

def escapeAlgorithm(algorithm):
    return algorithm.replace('&', '&amp;').replace('<', '&lt;').replace('"', '&quot;').replace("'", '&apos;')

SQL_DIVIDER = '--------------------'

class SchemaTools:
    '''
    Tools that help to fortify a db with a new schema
    '''
    
    def __init__(self, con, needSync = False):
        self.con = con
        self.needSync = needSync
        self.proxy = ConnProxy.getInstance()

    
    def fortify(self, schema):
        schema = schema.strip(' \n')
        
        try:
            entityType = self.getEntityType(schema).upper()
        except:
            entityType = 'invalid'

        if entityType == 'TABLE':
            return self.fortifyTable(schema)
        elif entityType == 'TRIGGER':
            return self.fortifyTrigger(schema)
        elif entityType == 'INDEX':
            return self.fortifyIndex(schema)
        else:
            return 'invalid'

    
    def fortifyTable(self, schema):
        '''creates/updates a table with schema'''
        tableName = self.getEntityName(schema)
        row = self.con.execute("SELECT sql FROM sqlite_master WHERE type='table' and name='%s';" % (tableName,)).fetchone()
        if row:
            oldSchema = row[0].strip(';')
            newSchema = schema.strip(';')
            if oldSchema == newSchema:
                return 'original'
            else:
                sqlList = []
                oldFields = self.getTableFields(oldSchema)
                newFields = self.getTableFields(newSchema)
                commonFields = [field for field in newFields if field in oldFields]
                sql = 'ALTER TABLE %s RENAME TO temp;' % (tableName,)
                sqlList.append(sql)
                self.con.execute(sql)
                sqlList.append(schema)
                self.con.execute(schema)
                fieldsStr = ','.join(commonFields)
                sql = 'INSERT INTO %s(%s) SELECT %s FROM temp;' % (tableName, fieldsStr, fieldsStr)
                sqlList.append(sql)
                self.con.execute(sql)
                sql = 'DROP TABLE temp;'
                sqlList.append(sql)
                self.con.execute(sql)
                self.con.commit()
                if self.needSync:
                    funcName = 'dbSyncScript'
                    scripts = '\n'.join(sqlList)
                    dbFile = 'machines/%s.db' % self.proxy.kioskId
                    params = {
                        'scripts': scripts,
                        'db_file': dbFile }
                    self.proxy.syncData(funcName, params)
                
                return 'altered'
        else:
            self.con.execute(schema)
            self.con.commit()
            if self.needSync:
                sqlList = []
                sqlList.append(schema)
                funcName = 'dbSyncScript'
                scripts = '\n'.join(sqlList)
                dbFile = 'machines/%s.db' % self.proxy.kioskId
                params = {
                    'scripts': scripts,
                    'db_file': dbFile }
                self.proxy.syncData(funcName, params)
            
            return 'new'

    
    def fortifyTrigger(self, schema):
        triggerName = self.getEntityName(schema)
        row = self.con.execute("SELECT sql FROM sqlite_master WHERE type='trigger' and name='%s';" % (triggerName,)).fetchone()
        sqlList = []
        if row:
            oldSchema = row[0].strip(';')
            newSchema = schema.strip(';')
            if oldSchema == newSchema:
                return 'original'
            else:
                sqlList.append('DROP TRIGGER %s;' % (triggerName,))
                sqlList.append(schema)
                self.con.execute('DROP TRIGGER %s;' % (triggerName,))
                self.con.execute(schema)
                self.con.commit()
                if self.needSync:
                    funcName = 'dbSyncScript'
                    scripts = '\n'.join(sqlList)
                    dbFile = 'machines/%s.db' % self.proxy.kioskId
                    params = {
                        'scripts': scripts,
                        'db_file': dbFile }
                    self.proxy.syncData(funcName, params)
                
                return 'altered'
        else:
            self.con.execute(schema)
            self.con.commit()
            if self.needSync:
                sqlList.append(schema)
                funcName = 'dbSyncScript'
                scripts = '\n'.join(sqlList)
                dbFile = 'machines/%s.db' % self.proxy.kioskId
                params = {
                    'scripts': scripts,
                    'db_file': dbFile }
                self.proxy.syncData(funcName, params)
            
            return 'new'

    
    def fortifyIndex(self, schema):
        indexName = self.getEntityName(schema)
        row = self.con.execute("SELECT sql FROM sqlite_master WHERE type='index' and name='%s';" % (indexName,)).fetchone()
        sqlList = []
        if row:
            oldSchema = row[0].strip(';')
            newSchema = schema.strip(';')
            if oldSchema == newSchema:
                return 'original'
            else:
                sqlList.append('DROP INDEX %s;' % (indexName,))
                sqlList.append(schema)
                self.con.execute('DROP INDEX %s;' % (indexName,))
                self.con.execute(schema)
                self.con.commit()
                if self.needSync:
                    funcName = 'dbSyncScript'
                    scripts = '\n'.join(sqlList)
                    dbFile = 'machines/%s.db' % self.proxy.kioskId
                    params = {
                        'scripts': scripts,
                        'db_file': dbFile }
                    self.proxy.syncData(funcName, params)
                
                return 'altered'
        else:
            self.con.execute(schema)
            self.con.commit()
            if self.needSync:
                sqlList.append(schema)
                funcName = 'dbSyncScript'
                scripts = '\n'.join(sqlList)
                dbFile = 'machines/%s.db' % self.proxy.kioskId
                params = {
                    'scripts': scripts,
                    'db_file': dbFile }
                self.proxy.syncData(funcName, params)
            
            return 'new'

    
    def getEntityType(self, schema):
        regex = re.compile('^\\s*create\\s+((?:table)|(?:index)|(?:trigger))', re.I)
        result = regex.findall(schema)
        if len(result) > 0:
            return result[0].lower()
        else:
            return None

    
    def getEntityName(self, schema):
        regex = re.compile("^\\s*create\\s+(?:(?:table)|(?:index)|(?:trigger))\\s+[\\[\\']?(\\w+)[\\[\\']?", re.I)
        result = regex.findall(schema)
        if len(result) > 0:
            return result[0].lower()
        else:
            return None

    
    def getTableFields(self, schema):
        regex = re.compile('.*\\((.*)\\).*', re.I | re.S)
        result = regex.findall(schema)
        fields = []
        if len(result) > 0:
            for s in result[0].split('\n'):
                field = s.strip()
                if field:
                    fields.append(field.split()[0])
                
            
        
        return fields

    
    def fortifyMany(self, sql):
        '''fortify multiple schemas'''
        schemas = sql.split(SQL_DIVIDER)
        for schema in schemas:
            if schema.strip(' \n'):
                self.fortify(schema)
            
        



class MkcDb:
    
    def __init__(self):
        self.con = sqlite.connect(MKC_DB_PATH, timeout = 5)
        self.cur = self.con.cursor()
        self.proxy = ConnProxy.getInstance()

    
    def verifyDb(self):
        self._validateDb()
        self._loadConfig()
        self._loadInfo()
        self._loadSlots()

    
    def _validateDb(self):
        '''Initializes and creates a database'''
        schemaTools = SchemaTools(self.con, True)
        sql = 'CREATE TABLE cc\n        (\n            id INTEGER PRIMARY KEY,\n            number TEXT,\n            name TEXT,\n            expdate TEXT,\n            track1 TEXT,\n            track2 TEXT,\n            display TEXT,\n            member_id TEXT\n        );'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' cc')
        sql = "CREATE TABLE commands\n        (\n            id INTEGER PRIMARY KEY,\n            command TEXT,\n            data TEXT,\n            result TEXT,\n            time_begin TEXT,\n            time_end TEXT,\n            log TEXT,\n            state TEXT DEFAULT 'active'\n        );"
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' commands')
        sql = 'CREATE TABLE config\n        (\n            id INTEGER PRIMARY KEY,\n            variable TEXT,\n            value TEXT\n        );'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' config')
        sql = "CREATE TABLE events\n        (\n            id INTEGER PRIMARY KEY,\n            category TEXT,\n            action TEXT,\n            data1 TEXT,\n            data2 TEXT,\n            data3 TEXT,\n            data4 TEXT,\n            data5 TEXT,\n            result TEXT,\n            time_recorded TEXT,\n            time_updated TEXT,\n            state TEXT DEFAULT 'open'\n        );"
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' events')
        sql = 'CREATE TABLE info\n        (\n            id INTEGER PRIMARY KEY,\n            variable TEXT,\n            value TEXT\n        );'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' info')
        sql = "CREATE TABLE postauthq\n        (\n            id INTEGER PRIMARY KEY,\n            upg_id INTEGER,\n            cc_id INTEGER,\n            acct_id TEXT,\n            transaction_id INTEGER,\n            shopping_cart_id INTEGER,\n            add_time TEXT,\n            state TEXT DEFAULT 'open',\n            amount INTEGER,\n            card_type INTEGER DEFAULT 0\n        );"
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' postauthq')
        sql = "CREATE TABLE declinedq\n        (\n            id INTEGER PRIMARY KEY,\n            upg_id INTEGER,\n            cc_id INTEGER,\n            acct_id TEXT,\n            transaction_id INTEGER,\n            process_count INTEGER,\n            process_time TEXT,\n            next_process_time TEXT,\n            state TEXT DEFAULT 'open',\n            amount INTEGER,\n            card_type INTEGER DEFAULT 0\n        );"
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' declinedq')
        sql = "CREATE TABLE preauthq\n        (\n            id INTEGER PRIMARY KEY,\n            upg_acct_id TEXT,\n            cc_id INTEGER,\n            amount INTEGER,\n            upg_id INTEGER,\n            oid TEXT,\n            preauth_time TEXT,\n            preauth_method TEXT,\n            last_access_time TEXT,\n            state TEXT DEFAULT 'open'\n        );"
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' preauthq')
        sql = 'CREATE TABLE price_plans\n        (\n            id INTEGER PRIMARY KEY,\n            data TEXT,\n            data_text TEXT\n        );'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' price_plans')
        if rev == 'new':
            
            try:
                firstNight = 'factor = 1'
                nights = '\noutTime = params["out_time"]\ninTime = params["in_time"]\nfirstCutoffTime = str(outTime).split(" ")[0] + " 23:59:59"\nif firstCutoffTime < outTime:\n    firstCutoffTime = getTimeChange(firstCutoffTime, day=1)\nnights = 0\nnextCutoffTime = getTimeChange(firstCutoffTime, day=1)\nwhile nextCutoffTime < inTime:\n    nights += 1\n    oldTime = nextCutoffTime\n    nextCutoffTime = getTimeChange(nextCutoffTime, day=1)\n    if oldTime == nextCutoffTime:\n        break\nfactor = nights'
                factorsAlgorithm = '{"first_night":\'\'\'%s\'\'\', "nights":\'\'\'%s\'\'\'}'
                factorsAlgorithm = factorsAlgorithm % (firstNight, nights)
                factorsAlgorithm = escapeAlgorithm(factorsAlgorithm)
                algorithm = '\nfirstNight = float(factors["first_night"])\nnights= float(factors["nights"])\nresult = 1.99 * firstNight + 0.99 * nights'
                algorithm = escapeAlgorithm(algorithm)
                data1 = '\n<PRICE>\n    <FACTORS>first_night|nights</FACTORS>\n    <FACTORS_ALGORITHM>%s</FACTORS_ALGORITHM>\n    <ALGORITHM>%s</ALGORITHM>\n    <NOTES></NOTES>\n</PRICE>'
                data1 = data1 % (factorsAlgorithm, algorithm)
                sql1 = "INSERT INTO price_plans(data, data_text) VALUES('%s', 'First Night Fee 1.99, \nAdditional Night Fee 0.99, \nCutoff Time 23:59:59');"
                sql1 = sql1 % data1.replace("'", "''")
                firsthours24 = 'factor = 1'
                hours12 = '\noutTime = params["out_time"]\ninTime = params["in_time"]\naddiStartTime = getTimeChange(outTime, hour=24)\nif addiStartTime >= inTime:\n    addiHoursCount = 0\nelse:\n    addiHoursCount = 0\n    while addiStartTime < inTime:\n        addiHoursCount += 1\n        oldTime = addiStartTime\n        addiStartTime = getTimeChange(addiStartTime, hour=12)\n        if oldTime == addiStartTime:\n            break\nfactor = addiHoursCount'
                factorsAlgorithm = '{"first_24_hours":\'\'\'%s\'\'\', "12_hours":\'\'\'%s\'\'\'}'
                factorsAlgorithm = factorsAlgorithm % (firsthours24, hours12)
                factorsAlgorithm = escapeAlgorithm(factorsAlgorithm)
                algorithm = '\nfirsthours24 = float(factors["first_24_hours"])\nhours12 = float(factors["12_hours"])\nresult = 1.59 * firsthours24 + 0.99 * hours12'
                algorithm = escapeAlgorithm(algorithm)
                data2 = '\n<PRICE>\n    <FACTORS>first_24_hours|12_hours</FACTORS>\n    <FACTORS_ALGORITHM>%s</FACTORS_ALGORITHM>\n    <ALGORITHM>%s</ALGORITHM>\n    <NOTES></NOTES>\n</PRICE>'
                data2 = data2 % (factorsAlgorithm, algorithm)
                sql2 = "INSERT INTO price_plans(data, data_text) VALUES('%s', 'First 24 hours Fee 1.59, \nNext per 12 hours Fee 0.99');"
                sql2 = sql2 % data2.replace("'", "''")
                sqlList = []
                self.cur.execute(sql1)
                self.cur.execute(sql2)
                self.con.commit()
                sqlList.append('DELETE FROM price_plans;')
                sqlList.append(sql1)
                sqlList.append(sql2)
                funcName = 'dbSyncScript'
                scripts = '\n'.join(sqlList)
                dbFile = 'machines/%s.db' % self.proxy.kioskId
                params = {
                    'scripts': scripts,
                    'db_file': dbFile }
                self.proxy.syncData(funcName, params)
            except Exception:
                ex = None
                msg = 'init table price_plans error: ' + str(ex)
                print(msg)
                self.proxy.log.error(msg)

        
        sql = 'CREATE TABLE rfid_cost\n        (\n            id INTEGER PRIMARY KEY,\n            rfid TEXT,\n            cost TEXT\n        );'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' rfid_cost')
        sql = "CREATE TABLE rfids\n        (\n            rfid TEXT PRIMARY KEY,\n            upc TEXT,\n            movie_id TEXT,\n            title TEXT,\n            genre TEXT,\n            sales_price TEXT,\n            sale_convert_price TEXT,\n            price_plan_id INTEGER,\n            price_plan_dynamic INTEGER DEFAULT 0,\n            enable_reduce TEXT DEFAULT 0,\n            reduce_formula TEXT DEFAULT '0,0,0',\n            last_reduce_date TEXT DEFAULT '',\n            enable_reduce_convert_price TEXT DEFAULT 0,\n            reduce_formula_convert_price TEXT DEFAULT '0,0,0',\n            last_reduce_date_convert_price TEXT DEFAULT '',\n            category_id TEXT DEFAULT '',\n            state TEXT,\n            lock_by TEXT,\n            lock_time TEXT\n        );"
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' rfids')
        sql = 'CREATE TABLE category\n        (\n            id INTEGER PRIMARY KEY,\n            category_name TEXT,\n            sale_price TEXT,\n            sale_convert_price TEXT,\n            price_plan_id TEXT,\n            notes TEXT\n        );'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' category')
        sql = 'CREATE TABLE shopping_carts\n        (\n            id TEXT PRIMARY KEY,\n            cc_id INTEGER,\n            upg_id INTEGER,\n            time_open TEXT,\n            time_close TEXT,\n            coupon_code TEXT,\n            coupon_plan TEXT,\n            coupon_text TEXT\n        );'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' shopping_carts')
        sql = "CREATE TABLE slots\n        (\n            id INTEGER PRIMARY KEY,\n            kiosk_id TEXT,\n            rank TEXT,\n            rfid TEXT,\n            state TEXT DEFAULT 'empty'\n        );"
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' slots')
        sql = "CREATE TABLE transactions\n        (\n            id INTEGER PRIMARY KEY,\n            rfid TEXT,\n            upc TEXT,\n            title TEXT,\n            genre TEXT,\n            amount INTEGER,\n            sales_tax TEXT,\n            out_time TEXT,\n            in_time TEXT,\n            notes TEXT,\n            state TEXT,\n            gene TEXT,\n            slot_id TEXT,\n            cc_id INTEGER,\n            sale_price TEXT,\n            price_plan TEXT,\n            price_plan_text TEXT,\n            coupon_code TEXT,\n            coupon_plan TEXT,\n            coupon_text TEXT,\n            coupon_usage_state TEXT,\n            upg_id INTEGER,\n            upg_account_id TEXT,\n            shopping_cart_id TEXT,\n            reserve_id INTEGER,\n            in_kiosk TEXT,\n            card_type INTEGER DEFAULT 0,\n            ms_expi_time TEXT DEFAULT '',\n            cc_display TEXT DEFAULT '',\n            sc_coupon_text TEXT DEFAULT '',\n            upg_oid TEXT DEFAULT ''\n        );"
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' transactions')
        sql = 'CREATE INDEX idx_transactions_out_time ON transactions(out_time);'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' idx_transactions_out_time')
        sql = 'CREATE INDEX idx_transactions_in_time ON transactions(in_time);'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' idx_transactions_in_time')
        sql = 'CREATE INDEX idx_transactions_state ON transactions(state);'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' idx_transactions_state')
        sql = 'CREATE INDEX idx_transactions_upg_id ON transactions(upg_id);'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' idx_transactions_upg_id')
        sql = 'CREATE TABLE upc_load_config\n        (\n            id INTEGER PRIMARY KEY,\n            upc TEXT,\n            price_plan_id INTEGER,\n            price_plan_dynamic INTEGER DEFAULT 0,\n            sale_price TEXT,\n            sale_convert_price TEXT,\n            cost TEXT\n        );'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' upc_load_config')
        sql = "CREATE TABLE upg\n        (\n            id INTEGER PRIMARY KEY,\n            acct_id TEXT,\n            pq_id INTEGER,\n            type TEXT,\n            oid TEXT,\n            amount INTEGER,\n            cc_id INTEGER,\n            result_code INTEGER,\n            result_msg INTEGER,\n            time TEXT,\n            preauth_method TEXT,\n            notes TEXT,\n            additional TEXT DEFAULT ''\n        );"
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' upg')
        sql = "CREATE TABLE reservations\n        (\n            id INTEGER PRIMARY KEY,\n            rfid TEXT,\n            slot_id TEXT,\n            upc TEXT,\n            title TEXT,\n            genre TEXT,\n            cc_id INTEGER,\n            upg_id INTEGER,\n            pickup_code TEXT,\n            price_plan TEXT DEFAULT '',\n            price_plan_text TEXT DEFAULT '',\n            coupon_code TEXT DEFAULT '',\n            coupon_plan TEXT DEFAULT '',\n            coupon_text TEXT DEFAULT '',\n            reserve_time TEXT,\n            reserve_method TEXT,\n            gene TEXT,\n            state TEXT DEFAULT 'reserved',\n            ms_keep_days TEXT DEFAULT '',\n            ms_id INTEGER DEFAULT ''\n        );"
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' reservations')
        sql = 'CREATE TABLE price_plans_week\n        (\n            id INTEGER PRIMARY KEY,\n            title TEXT,\n            price_plan TEXT,\n            price_plan_text TEXT,\n            price_plan_br TEXT,\n            price_plan_text_br TEXT,\n            price_plan_game TEXT,\n            price_plan_text_game TEXT\n        );'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' price_plans_week')
        if rev == 'new':
            sqlList = []
            sqlList.append('DELETE FROM price_plans_week;')
            sql = "INSERT INTO price_plans_week(title, price_plan, price_plan_text, price_plan_br, price_plan_text_br, price_plan_game, price_plan_text_game) VALUES('%s', '', '', '', '', '', '');"
            self.cur.execute(sql % 'Sunday')
            sqlList.append(sql % 'Sunday')
            self.cur.execute(sql % 'Monday')
            sqlList.append(sql % 'Monday')
            self.cur.execute(sql % 'Tuesday')
            sqlList.append(sql % 'Tuesday')
            self.cur.execute(sql % 'Wednesday')
            sqlList.append(sql % 'Wednesday')
            self.cur.execute(sql % 'Thursday')
            sqlList.append(sql % 'Thursday')
            self.cur.execute(sql % 'Friday')
            sqlList.append(sql % 'Friday')
            self.cur.execute(sql % 'Saturday')
            sqlList.append(sql % 'Saturday')
            self.con.commit()
            funcName = 'dbSyncScript'
            scripts = '\n'.join(sqlList)
            dbFile = 'machines/%s.db' % self.proxy.kioskId
            params = {
                'scripts': scripts,
                'db_file': dbFile }
            self.proxy.syncData(funcName, params)
        
        sql = 'CREATE TABLE customer_behavior\n        (\n            id INTEGER PRIMARY KEY,\n            cc_id TEXT,\n            operate_type TEXT,\n            gender TEXT,\n            age TEXT,\n            start_time TEXT,\n            end_time TEXT\n        );'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' customer_behavior')
        sql = 'CREATE TABLE refunds\n        (\n            id INTEGER PRIMARY KEY,\n            trs_id TEXT,\n            cc_id TEXT,\n            display TEXT,\n            refund_amount INTEGER,\n            refund_time TEXT,\n            notes TEXT\n        );'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' refunds')
        sql = 'CREATE TABLE card_read\n        (\n            id INTEGER PRIMARY KEY,\n            read_time TEXT,\n            state TEXT\n        );'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' card_read')
        sql = 'CREATE TABLE trs_process\n        (\n            id INTEGER PRIMARY KEY,\n            transaction_id INTERGER,\n            process_time TEXT\n        );'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' trs_process')
        sql = 'CREATE TABLE over_capacity_rfids\n        (\n            id INTEGER PRIMARY KEY,\n            rfid TEXT,\n            add_time TEXT\n        );'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' over_capacity_rfids')
        sql = "CREATE TABLE remote_arrangement_plans\n        (\n            id INTEGER PRIMARY KEY,\n            arrange_name TEXT,\n            arrange_params TEXT,\n            arrange_date TEXT,\n            arrange_time TEXT,\n            generate_time TEXT,\n            create_time TEXT,\n            update_time TEXT,\n            state TEXT DEFAULT 'active'\n        );"
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' remote_arrangement_plans')
        sql = 'CREATE TABLE cerepay_topup\n        (\n            id INTEGER PRIMARY KEY,\n            acct_id TEXT,\n            cerepay_member_id TEXT,\n            card_type INTEGER,\n            upg_id INTEGER,\n            oid TEXT,\n            amount INTEGER,\n            state TEXT,\n            cerepay_uuid TEXT,\n            last_msg TEXT,\n            add_time TEXT,\n            last_time TEXT\n        );'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' cerepay_topup')
        sql = 'CREATE TABLE failed_trs\n        (\n            id INTEGER PRIMARY KEY,\n            rfid TEXT,\n            upc TEXT,\n            title TEXT,\n            action_time TEXT,\n            action_type TEXT,\n            slot_id TEXT,\n            cc_display TEXT,\n            state TEXT,\n            video_name TEXT,\n            video_url TEXT,\n            error_msg TEXT\n        );'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' failed_trs')

    
    def _loadInfo(self):
        info = { }
        self.cur.execute('SELECT variable, value FROM info ORDER BY variable;')
        rows = self.cur.fetchall()
        for row in rows:
            (variable, value) = row
            info[variable] = value
        
        sqlList = []
        if 'KioskID' not in info:
            sql = "INSERT INTO info(variable, value) VALUES('KioskID', '');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'IP' not in info:
            sql = "INSERT INTO info(variable, value) VALUES('IP', '');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'MAC' not in info:
            sql = "INSERT INTO info(variable, value) VALUES('MAC', '');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'KioskSoft' not in info:
            sql = "INSERT INTO info(variable, value) VALUES('KioskSoft', '');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'Firmware' not in info:
            sql = "INSERT INTO info(variable, value) VALUES('Firmware', '');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'KioskTimeZone' not in info:
            sql = "INSERT INTO info(variable, value) VALUES('KioskTimeZone', '');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'StartTime' not in info:
            sql = "INSERT INTO info(variable, value) VALUES('StartTime', '');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'UMGChannel' not in info:
            sql = "INSERT INTO info(variable, value) VALUES('UMGChannel', '');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'ExternalIP' not in info:
            sql = "INSERT INTO info(variable, value) VALUES('ExternalIP', '');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'HDMI' not in info:
            sql = "INSERT INTO info(variable, value) VALUES('HDMI', 'off');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'CapacityType' not in info:
            sql = "INSERT INTO info(variable, value) VALUES('CapacityType', '');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if sqlList:
            funcName = 'dbSyncScript'
            scripts = '\n'.join(sqlList)
            dbFile = 'machines/%s.db' % self.proxy.kioskId
            params = {
                'scripts': scripts,
                'db_file': dbFile }
            self.proxy.syncData(funcName, params)
        

    
    def _loadConfig(self):
        config = { }
        self.cur.execute('SELECT variable, value FROM config ORDER BY variable;')
        rows = self.cur.fetchall()
        for row in rows:
            (variable, value) = row
            config[variable] = value
        
        sqlList = []
        if 'default_price_plan' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('default_price_plan', '1');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'default_sale_price' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('default_sale_price', '39.00');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'default_cost' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('default_cost', '20.00');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'terms_and_conditions' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('terms_and_conditions', '%s');"
            terms_and_conditions = 'Terms and Conditions\nTo rent a DVD, Video Game or other product from this Automated Kiosk you must swipe your credit card.\nBy swiping your credit card you certify that you are the legal owner of the card that you are at least 18 years of age, and that you agree to all of the Terms and Conditions listed herein. If you are under the age of 18 you may only use this Kiosk with the express permission of a Parent or Guardian.\n\n1. You agree to pay the rental rates as listed on the kiosk screen.\n2. If we are required to collect Sales Taxes in your area, either on rental, purchase or applicable Maximum Replacement Cost, they are additional to the rental price and you understand and agree that they are automatically applied to your credit card over and above the value of the rental.\n3. You understand and agree that your credit card will be charged an additional period fee, as displayed on the kiosk screen, for each additional period you keep the DVD, Video Game or other product beyond the return time.\n4. The Rental Day Limit allowed for a rental is  ___  after which the rental is converted into a sale.\n                a. DVD - $30.00\n                b. Blu-Ray - $35.00\n                c. Video Game - $45.00\n5. If the rental day limit has been reached, you have purchased the DVD, or Video Game or other product and do not need to return it.  If you return the DVD, Video Game, or other product after the replacement cost has been charged, you agree and understand that no refund will be issued, but that we will mail that product to you upon written request and payment of delivery charges.\n6. If the DVD, Video Game or other product is returned Damaged, without the original box or other product or information included in the box you understand and agree that your Payment Card will be assessed additional charges up to the Maximum Replacement Cost of that DVD, Video Game or other product.\n7. If you reserve a DVD online, the reservation period begins immediately.  You have 12 hours to pick up your reserved DVD(s).  Your reservation will expire after 12 hours and you will be charged a one night rental fee for each reserved DVD.\n8. If you have questions, comments or concerns, please contact: the owner / operator.'
            sql = sql % terms_and_conditions
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'sales_tax' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('sales_tax', '8.25');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'rentals_tax' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('rentals_tax', '6.825');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'sale_convert_days' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('sale_convert_days', '14');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'upg_acct_id' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('upg_acct_id', '');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'operator_code' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('operator_code', 'thismachineisgreat');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'currency_symbol' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('currency_symbol', '$');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'arrangement' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('arrangement', 'kiosk');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'show_mode' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('show_mode', 'yes');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'upg_show_mode' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('upg_show_mode', 'yes');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'show_mode_passcode' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('show_mode_passcode', '594110');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'upg_url' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('upg_url', 'upg1.waven.com/upg/agent/upgAgent');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'kiosk_logo' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('kiosk_logo', '');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'kiosk_logo_md5' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('kiosk_logo_md5', '');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'reservation_expiration' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('reservation_expiration', '720');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'rental_lock' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('rental_lock', 'yes');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'sale_convert_price' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('sale_convert_price', '39.00');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'preauth_method' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('preauth_method', 'full');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'preauth_custom_amount' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('preauth_custom_amount', '0.00');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'run_test' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('run_test', 'yes');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'rating_lock' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('rating_lock', 'no');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'tech_support_contact' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('tech_support_contact', '');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'max_dvd_out' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('max_dvd_out', '3');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'buy_limit' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('buy_limit', '1');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'speaker_volume' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('speaker_volume', '80');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'return_options' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('return_options', 'disc');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'pulses_per_slot' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('pulses_per_slot', '390.095');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'top_offset' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('top_offset', '34.914');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'bottom_offset' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('bottom_offset', '200');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'exchange_offset' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('exchange_offset', '70');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'back_offset' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('back_offset', '0');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'sensor_distance' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('sensor_distance', '0');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'sensor_distance_fl' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('sensor_distance_fl', '0');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'distance1' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('distance1', '0');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'distance2' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('distance2', '0');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'return_slot' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('return_slot', 'auto');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'grace_period' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('grace_period', '0');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'load_code' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('load_code', 'ineedfreshjuice');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'enable_disc_out' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('enable_disc_out', 'yes');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'default_language' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('default_language', 'en');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'unload_code' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('unload_code', 'ihatefreshjuice');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'enable_avs' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('enable_avs', 'no');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'payment_options' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('payment_options', '');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'payment_params' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('payment_params', '');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'robot_retry' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('robot_retry', 0);"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'member_preauth' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('member_preauth', 'default');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'language_switch' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('language_switch', '');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'offset2xx' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('offset2xx', '0');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'offset6xx' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('offset6xx', '0');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'auto_receive_updates' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('auto_receive_updates', 'no');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'auto_update_time' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('auto_update_time', '02');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'bluray_warning' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('bluray_warning', 'no');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'shopping_cart_message' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('shopping_cart_message', '');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'show_available_notice' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('show_available_notice', 'yes');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'show_deposit_amount' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('show_deposit_amount', 'no');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'receive_adult_content' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('receive_adult_content', 'no');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'ui_theme' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('ui_theme', 'movie');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'kiosk_gr_slogan' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('kiosk_gr_slogan', '$2.99 Game Rentals');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'over_capacity_slots_limit' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('over_capacity_slots_limit', '0');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'over_capacity_alert_threshold' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('over_capacity_alert_threshold', '10');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'preauth_method_br' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('preauth_method_br', 'full');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'preauth_custom_amount_br' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('preauth_custom_amount_br', '0.00');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'preauth_method_game' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('preauth_method_game', 'full');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'preauth_custom_amount_game' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('preauth_custom_amount_game', '0.00');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'preauth_method_cp' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('preauth_method_cp', 'full');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'preauth_custom_amount_cp' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('preauth_custom_amount_cp', '0.00');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'preauth_method_cp_br' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('preauth_method_cp_br', 'full');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'preauth_custom_amount_cp_br' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('preauth_custom_amount_cp_br', '0.00');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'preauth_method_cp_game' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('preauth_method_cp_game', 'full');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'preauth_custom_amount_cp_game' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('preauth_custom_amount_cp_game', '0.00');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'reprocessing_interval' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('reprocessing_interval', '1');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'reprocessing_count' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('reprocessing_count', '7');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'good_credibility_preauth' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('good_credibility_preauth', 'default');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'rating_system' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('rating_system', 'usa');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'allow_rental_purchase' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('allow_rental_purchase', '100');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'bandwidth_limit' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('bandwidth_limit', 0);"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'sale_prevent_days' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('sale_prevent_days', 0);"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'backup_db_interval_hour' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('backup_db_interval_hour', 6);"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'mainform_sale_price' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('mainform_sale_price', 'no');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'error_message' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('error_message', 'VGhlIEtpb3NrIHJlcXVpcmVzIE1haW50ZW5hbmNlLiAgV2UgYXBvbG9naXplIGZvciB0aGUgaW5jb252ZW5pZW5jZS4gUGxlYXNlIGNvbnRhY3Qgc3VwcG9ydCBhdCB0aGUgcGhvbmUgbnVtYmVyIGxpc3RlZCBiZWxvdw==');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'return_time' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('return_time', '');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if 'enable_webcam' not in config:
            sql = "INSERT INTO config(variable, value) VALUES('enable_webcam', 'no');"
            self.cur.execute(sql)
            self.con.commit()
            sqlList.append(sql)
        
        if sqlList:
            funcName = 'dbSyncScript'
            scripts = '\n'.join(sqlList)
            dbFile = 'machines/%s.db' % self.proxy.kioskId
            params = {
                'scripts': scripts,
                'db_file': dbFile }
            self.proxy.syncData(funcName, params)
        

    
    def _loadSlots(self):
        sqlList = []
        slots = []
        self.cur.execute('SELECT id FROM slots ORDER BY id;')
        rows = self.cur.fetchall()
        capacity = getKioskCapacity()
        if capacity == '250':
            for i in range(101, 111):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'A');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(111, 121):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'B');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(121, 131):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'C');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(131, 141):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'D');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(141, 151):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'E');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(151, 161):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'F');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(161, 171):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'G');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(228, 231):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'H');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(231, 241):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'I');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(241, 251):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'J');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(251, 261):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'K');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(261, 271):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'L');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(501, 511):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'M');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(511, 521):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'N');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(521, 531):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'O');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(531, 541):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'P');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(541, 551):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'Q');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(551, 561):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'R');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(561, 571):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'S');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(601, 611):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'T');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(611, 621):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'U');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(621, 631):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'V');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(631, 641):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'W');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(641, 651):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'X');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(651, 661):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'Y');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(661, 671):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'Z');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
        else:
            for i in range(101, 121):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'A');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(121, 141):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'B');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(141, 161):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'C');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(161, 181):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'D');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(181, 201):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'E');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(201, 221):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'F');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(221, 241):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'G');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(354, 361):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'H');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(361, 381):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'I');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(381, 401):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'J');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(401, 421):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'K');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(421, 441):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'L');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(501, 521):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'M');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(521, 541):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'N');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(541, 561):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'O');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(561, 581):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'P');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(581, 601):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'Q');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(601, 621):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'R');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(621, 639):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'S');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(701, 721):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'T');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(721, 741):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'U');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(741, 761):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'V');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(761, 781):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'W');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(781, 801):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'X');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(801, 821):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'Y');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
            for i in range(821, 839):
                if i not in slots:
                    sql = "INSERT INTO slots(id, rank) VALUES('%s', 'Z');" % str(i)
                    self.cur.execute(sql)
                    sqlList.append(sql)
                
            
        self.con.commit()
        if sqlList:
            funcName = 'dbSyncScript'
            scripts = '\n'.join(sqlList)
            dbFile = 'machines/%s.db' % self.proxy.kioskId
            params = {
                'scripts': scripts,
                'db_file': dbFile }
            self.proxy.syncData(funcName, params)
        



class SyncDb:
    
    def __init__(self):
        self.con = sqlite.connect(SYNC_DB_PATH, timeout = 5)
        self.cur = self.con.cursor()
        self.proxy = ConnProxy.getInstance()

    
    def verifyDb(self):
        self._validateDb()

    
    def _validateDb(self):
        '''Initializes and creates a database'''
        schemaTools = SchemaTools(self.con)
        sql = 'CREATE TABLE db_sync\n        (\n            id INTEGER PRIMARY KEY AUTOINCREMENT,\n            function_name TEXT,\n            port_num INTEGER,\n            params TEXT,\n            add_time TEXT,\n            sync_time TEXT,\n            state INTEGER DEFAULT 0\n        );'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' db_sync')
        sql = "CREATE TABLE db_sync_remote_kiosk\n        (\n            id INTEGER PRIMARY KEY AUTOINCREMENT,\n            remote_kiosk_id TEXT DEFAULT '',\n            function_name TEXT,\n            port_num INTEGER,\n            params TEXT,\n            add_time TEXT,\n            sync_time TEXT,\n            state INTEGER DEFAULT 0\n        );"
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' db_sync_remote_kiosk')
        sql = 'CREATE TABLE db_sync_no_sequence\n        (\n            id INTEGER PRIMARY KEY AUTOINCREMENT,\n            function_name TEXT,\n            port_num INTEGER,\n            params TEXT,\n            add_time TEXT,\n            sync_time TEXT,\n            state INTEGER DEFAULT 0\n        );'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' db_sync_no_sequence')



class MediaDb:
    
    def __init__(self):
        self.con = sqlite.connect(MEDIA_DB_PATH, timeout = 5)
        self.cur = self.con.cursor()
        self.proxy = ConnProxy.getInstance()

    
    def verifyDb(self):
        self._validateDb()

    
    def _validateDb(self):
        '''Initializes and creates a database'''
        schemaTools = SchemaTools(self.con)
        sql = 'CREATE TABLE media\n(\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\n    upc TEXT,\n    media_name TEXT,\n    media_md5 TEXT,\n    state TEXT DEFAULT "notconnect",\n    create_time TEXT,\n    download_url TEXT,\n    last_access_time TEXT\n);'
        rev = schemaTools.fortify(sql)
        self.proxy.log.info(rev + ' media')



def verifyDb():
    syncDb = SyncDb()
    syncDb.verifyDb()
    mediaDb = MediaDb()
    mediaDb.verifyDb()
    mkcDb = MkcDb()
    mkcDb.verifyDb()

if __name__ == '__main__':
    verifyDb()

