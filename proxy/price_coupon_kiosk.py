# Source Generated with Decompyle++
# File: price_coupon_kiosk.pyc (Python 2.5)

'''
Price Coupon Engine Kiosk Side
Filename: price_coupon_kiosk.py
'''
from .mda import Db
from .config import *
from .tools import *
from .price_coupon_config import CouponConfig, PriceConfig
log = getLog(fileName = 'price_coupon.log', loggerName = 'PRICE_COUPON')

class PriceCouponEngine:
    
    def __init__(self, shoppingCart):
        '''
        shoppingCart:
        {
            "transactions":(
                {"id":"", "rfid":"", "upc":"", "title":"", "genre":"", "amount":"",
                 "sales_tax":"", "out_time":"", "in_time":"", "gene":"", "slot_id":"",
                 "cc_id":"", "sale_price":"", "price_plan":"", "coupon_code":"",
                 "coupon_plan":"", "shopping_cart_id":"", "reserve_id":""},
                {"id":"", "rfid":"", "upc":"", "title":"", "genre":"", "amount":"",
                 "sales_tax":"", "out_time":"", "in_time":"", "gene":"", "slot_id":"",
                 "cc_id":"", "sale_price":"", "price_plan":"", "coupon_code":"",
                 "coupon_plan":"", "shopping_cart_id":"", "reserve_id":""},
            ),
            "coupon_plan":""
        }
        '''
        self.transactions = []
        if 'transactions' in shoppingCart:
            self.transactions = shoppingCart['transactions']
        
        self.multipleCouponPlan = shoppingCart['coupon_plan']
        self.mkcDb = Db(MKC_DB_PATH)

    
    def __del__(self):
        del self.mkcDb

    
    def _chkConditions(self, conditions):
        result = False
        
        try:
            transactions = self.transactions
            exec(conditions)
        except Exception:
            ex = None
            result = False
            log.error('An error occured when _chkConditions in price_coupon_kiosk: %s' % str(ex))

        return result

    
    def calculate(self):
        '''
        result:
        {
            "[rfid]":{"price":[price], "coupon_used":1},
            "[rfid]":{"price":[price], "coupon_used":0}
        }
        '''
        result = { }
        transactions = self.transactions
        for transaction in transactions:
            rfid = transaction['rfid']
            price = 0
            couponUsed = 0
            couponPlanData = transaction['coupon_plan']
            if couponPlanData:
                cf = CouponConfig(couponPlanData)
                conditions = cf.conditions
                if self._chkConditions(conditions):
                    algorithm = cf.algorithm
                    exec(algorithm)
                    couponUsed = 1
                
            else:
                outTime = transaction['out_time']
                inTime = transaction['in_time']
                pricePlanData = transaction['price_plan']
                params = {
                    'out_time': outTime,
                    'in_time': inTime }
                ppe = PricePlanEngine(pricePlanData, params)
                price = ppe.calculate()
            result[rfid] = {
                'price': price,
                'coupon_used': couponUsed }
        
        result['shopping_cart_coupon_used'] = 0
        if self.multipleCouponPlan:
            mcf = CouponConfig(self.multipleCouponPlan)
            mconditions = mcf.conditions
            malgorithm = mcf.algorithm
            maccumulative = mcf.accumulative
            if self._chkConditions(mconditions):
                exec(malgorithm)
                result['shopping_cart_coupon_used'] = 1
            
        
        return result



class PricePlanEngine:
    
    def __init__(self, pricePlanData, params):
        self.params = params
        self.priceConfig = PriceConfig(pricePlanData)

    
    def _calculateFactors(self, inputFactors):
        factors = self.priceConfig.factors
        factorsAlgorithm = self.priceConfig.factorsAlgorithm
        params = self.params
        resultFactors = { }
        for key in factors:
            if key in inputFactors:
                resultFactors[key] = inputFactors[key]
            else:
                factor = 0
                exec(factorsAlgorithm[key])
                resultFactors[key] = factor
        
        return resultFactors

    
    def calculate(self, factors = { }):
        result = 0
        
        try:
            factors = self._calculateFactors(factors)
            exec(self.priceConfig.algorithm)
        except Exception:
            ex = None
            result = 0
            log.error('An error occured when calculate(PricePlanEngine) in price_coupon_kiosk: %s' % str(ex))

        return result



def calculatePrice(params):
    '''
    API for calculating price when return
    '''
    result = { }
    
    try:
        shoppingCart = params['shopping_cart']
        cpe = PriceCouponEngine(shoppingCart)
        result = cpe.calculate()
    except Exception:
        ex = None
        result = { }
        log.error('An error occured when calculatePrice in price_coupon_kiosk: %s' % str(ex))

    return result


def _testAdditionalHours():
    a = '\noutTime = "2008-11-20 16:09:23"\ninTime = "2008-11-25 16:19:04"\naddiStartTime = getTimeChange(outTime, hour=[FIRSTSOMEHOURS])\nif addiStartTime >= inTime:\n    addiHoursCount = 0\nelse:\n    addiHoursCount = 0\n    while addiStartTime < inTime:\n        addiHoursCount += 1\n        oldTime = addiStartTime\n        addiStartTime = getTimeChange(addiStartTime, hour=[ADDITIONALSOMEHOURS])\n        if oldTime == addiStartTime:\n            break\n\nprint "Additional [ADDITIONALSOMEHOURS] hours count: ", addiHoursCount\n'
    exec(a.replace('[FIRSTSOMEHOURS]', '24').replace('[ADDITIONALSOMEHOURS]', '6'))


def _testAdditionalNights():
    a = '\noutTime = "2008-11-23 15:37:04"\ninTime = "2008-11-25 15:46:35"\nfirstCutoffTime = str(outTime).split(" ")[0] + " [CUTOFFTIME]"\nif firstCutoffTime < outTime:\n    firstCutoffTime = getTimeChange(firstCutoffTime, day=1)\nnights = 0\nnextCutoffTime = getTimeChange(firstCutoffTime, day=1)\nwhile nextCutoffTime < inTime:\n    nights += 1\n    oldTime = nextCutoffTime\n    nextCutoffTime = getTimeChange(nextCutoffTime, day=1)\n    if oldTime == nextCutoffTime:\n        break\nprint "Additional nights: ", nights\n'
    exec(a.replace('[CUTOFFTIME]', '23:59:59'))


def _testCalculatePrice():
    sc = {
        'coupon_plan': '',
        'transactions': [
            {
                'in_time': '2008-05-14 15:41:27',
                'price_plan': '\n        <PRICE>\n            <FACTORS>first_24_hours|hours6_hours</FACTORS>\n            <FACTORS_ALGORITHM>{&quot;first_24_hours&quot;:&apos;&apos;&apos;factor = 1&apos;&apos;&apos;, &quot;6_hours&quot;:&apos;&apos;&apos;\noutTime = params[&quot;out_time&quot;]\ninTime = params[&quot;in_time&quot;]\naddiStartTime = getTimeChange(outTime, hour=24)\nif addiStartTime >= inTime:\n    addiHoursCount = 0\nelse:\n    addiHoursCount = 0\n    while addiStartTime &lt; inTime:\n        addiHoursCount += 1\n        oldTime = addiStartTime\n        addiStartTime = getTimeChange(addiStartTime, hour=6)\n        if oldTime == addiStartTime:\n            break\nfactor = addiHoursCount&apos;&apos;&apos;}</FACTORS_ALGORITHM>\n            <ALGORITHM>\nfirstHours24 = int(factors[&quot;first_24_hours&quot;])\nhours6= int(factors[&quot;6_hours&quot;])\nresult = 1.59 * firstHours24 + 0.99 * hours6</ALGORITHM>\n            <NOTES></NOTES>\n        </PRICE>',
                'id': 88,
                'coupon_usage_state': None,
                'out_time': '2008-05-11 12:12:12',
                'title': 'Scoop (2006)',
                'state': 'open',
                'shopping_cart_id': 82,
                'sale_price': '42.22',
                'reserve_id': None,
                'rfid': '01063ED0DC',
                'genre': 'Comedy',
                'cc_id': 2,
                'coupon_plan': '',
                'notes': None,
                'upc': '025193121325',
                'coupon_code': '',
                'amount': 42.22,
                'slot_id': '102',
                'sales_tax': '8.25',
                'gene': 'rent',
                'upg_id': 1 }] }
    params = {
        'shopping_cart': sc }
    print(calculatePrice(params))


def _testGetRentalPrice():
    pricePlanData = '\n    <PRICE>\n        <FACTORS>first_night|nights</FACTORS>\n        <FACTORS_ALGORITHM>{&quot;first_night&quot;:&apos;&apos;&apos;factor = 1&apos;&apos;&apos;, \n&quot;nights&quot;:&apos;&apos;&apos;\noutTime = params[&quot;out_time&quot;]\ninTime = params[&quot;in_time&quot;]\nfirstCutoffTime = str(outTime).split(&quot; &quot;)[0] + &quot; 23:59:59&quot;\nif firstCutoffTime &lt; outTime:\n    firstCutoffTime = getTimeChange(firstCutoffTime, day=1)\nnights = 0\nnextCutoffTime = getTimeChange(firstCutoffTime, day=1)\nwhile nextCutoffTime &lt; inTime:\n    nights += 1\n    oldTime = nextCutoffTime\n    nextCutoffTime = getTimeChange(nextCutoffTime, day=1)\n    if oldTime == nextCutoffTime:\n        break\nfactor = nights&apos;&apos;&apos;}</FACTORS_ALGORITHM>\n        <ALGORITHM>\nfirstNight = int(factors[&quot;first_night&quot;])\nnights = int(factors[&quot;nights&quot;] )\nresult = 1.69 * firstNight + 1.69 * nights</ALGORITHM>\n        <NOTES></NOTES>\n    </PRICE>\n    '
    params = {
        'out_time': '2008-01-01 12:12:12',
        'in_time': '2008-01-01 12:12:13' }
    ppe = PricePlanEngine(pricePlanData, params)
    print(ppe.calculate())

if __name__ == '__main__':
    _testGetRentalPrice()

