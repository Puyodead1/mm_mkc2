# Source Generated with Decompyle++
# File: price_coupon_config.pyc (Python 2.5)

import xml.dom.minidom as xml

def getValue(dom, key):
    result = ''
    
    try:
        xmlNodes = dom.getElementsByTagName(key)
        if len(xmlNodes) > 0:
            xmlElm = xmlNodes.item(0)
            result = xmlElm.firstChild.data
    except AttributeError:
        pass

    return result


class CouponConfig:
    
    def __init__(self, couponPlanData):
        '''
        <COUPON>
            <FACTORS>[List]</FACTORS>
            <TYPE>[String]</TYPE>
            <PRE_CONDITIONS>[string(code)(optional)]</PRE_CONDITIONS>
            <CONDITIONS>[string(code)]</CONDITIONS>
            <ALGORITHM>[string(code)]</ALGORITHM>
            <EXCLUSIVENESS>[List]</EXCLUSIVENESS>
            <ACCUMULATIVE>[Boolean]</ACCUMULATIVE>
            <NOTES>[Dictionary]</NOTES>
        </COUPON>
        '''
        self.couponPlanData = couponPlanData
        self.domCouponPlanData = None
        self.couponType = ''
        self.factors = []
        self.perConditions = ''
        self.conditions = ''
        self.algorithm = ''
        self.exclusiveness = []
        self.accumulative = 0
        self.notes = { }
        self.init()

    
    def init(self):
        self.domCouponPlanData = self._getDom()
        self.couponType = getValue(self.domCouponPlanData, 'TYPE').upper()
        _couponFactorsStr = getValue(self.domCouponPlanData, 'FACTORS')
        if _couponFactorsStr:
            self.factors = _couponFactorsStr.split('|')
        
        self.perConditions = getValue(self.domCouponPlanData, 'PRE_CONDITIONS')
        self.conditions = getValue(self.domCouponPlanData, 'CONDITIONS')
        self.algorithm = getValue(self.domCouponPlanData, 'ALGORITHM')
        _couponExclusivenessStr = getValue(self.domCouponPlanData, 'EXCLUSIVENESS')
        if _couponExclusivenessStr:
            self.exclusiveness = _couponExclusivenessStr.split('|')
        
        _couponAccumulativeStr = getValue(self.domCouponPlanData, 'ACCUMULATIVE')
        if _couponAccumulativeStr:
            self.accumulative = int(_couponAccumulativeStr)
        
        _couponNotesStr = getValue(self.domCouponPlanData, 'NOTES')
        if _couponNotesStr:
            self.notes = eval(_couponNotesStr)
        

    
    def _getDom(self):
        couponPlanData = self.couponPlanData
        domCouponPlanData = xml.dom.minidom.parseString(couponPlanData)
        return domCouponPlanData



class PriceConfig:
    
    def __init__(self, pricePlanData):
        '''
        <PRICE>
            <FACTORS>[List]</FACTORS>
            <FACTORS_ALGORITHM>[Dictionary]</FACTORS_ALGORITHM>
            <ALGORITHM>[String(code)]</ALGORITHM>
            <NOTES>[Dictionary]</NOTES>
        </PRICE>
        '''
        self.pricePlanData = pricePlanData
        self.domPricePlanData = None
        self.factors = []
        self.factorsAlgorithm = { }
        self.algorithm = ''
        self.notes = { }
        self.init()

    
    def init(self):
        self.domPricePlanData = self._getDom()
        _priceFactorsStr = getValue(self.domPricePlanData, 'FACTORS')
        if _priceFactorsStr:
            self.factors = _priceFactorsStr.split('|')
        
        _factorsAlgorithmStr = getValue(self.domPricePlanData, 'FACTORS_ALGORITHM')
        if _factorsAlgorithmStr:
            self.factorsAlgorithm = eval(_factorsAlgorithmStr)
        
        self.algorithm = getValue(self.domPricePlanData, 'ALGORITHM')
        _notesStr = getValue(self.domPricePlanData, 'NOTES')
        if _notesStr:
            self.notes = eval(_notesStr)
        

    
    def _getDom(self):
        pricePlanData = self.pricePlanData
        domPricePlanData = xml.dom.minidom.parseString(pricePlanData)
        return domPricePlanData



def _testCouponConfig():
    print('start testing CouponConfig...')
    print('-' * 100)
    cpd = "\n        <COUPON>\n            <FACTORS>FACTORS1|FACTORS2</FACTORS>\n            <TYPE>type</TYPE>\n            <!--PRE_CONDITIONS>[string(code)(optional)]</PRE_CONDITIONS-->\n            <CONDITIONS>CONDITIONS(code)</CONDITIONS>\n            <ALGORITHM>ALGORITHM(code)</ALGORITHM>\n            <EXCLUSIVENESS>EXCLUSIVENESS1|EXCLUSIVENESS2</EXCLUSIVENESS>\n            <ACCUMULATIVE>0</ACCUMULATIVE>\n            <NOTES>{'NOTES':''}</NOTES>\n        </COUPON>"
    cf = CouponConfig(cpd)
    print('couponType: ', cf.couponType)
    print('factors: ', cf.factors)
    print('perConditions: ', cf.perConditions)
    print('conditions: ', cf.conditions)
    print('algorithm: ', cf.algorithm)
    print('exclusiveness: ', cf.exclusiveness)
    print('accumulative: ', cf.accumulative)
    print('notes: ', cf.notes)
    print('end\n')


def _testPriceConfig():
    print('start testing PriceConfig...')
    print('-' * 100)
    ppd = "\n        <PRICE>\n            <FACTORS>FACTORS1|FACTORS2</FACTORS>\n            <FACTORS_ALGORITHM>{'a':'', 'b':''}</FACTORS_ALGORITHM>\n            <ALGORITHM>ALGORITHM(code)</ALGORITHM>\n            <NOTES>{'NOTES':''}</NOTES>\n        </PRICE>"
    pf = PriceConfig(ppd)
    print('factors: ', pf.factors)
    print('factorsAlgorithm: ', pf.factorsAlgorithm)
    print('algorithm: ', pf.algorithm)
    print('notes: ', pf.notes)
    print('end\n')

if __name__ == '__main__':
    _testCouponConfig()
    _testPriceConfig()

