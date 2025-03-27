# Source Generated with Decompyle++
# File: raTest.pyc (Python 2.5)

'''
Created on 2010-2-8
@author: andrew.lu@cereson.com
'''
import sys
import traceback
import random
from mcommon import isS250
from discRecovery import CheckBase, MkcLockException

class RATest(CheckBase):
    
    def __init__(self):
        super(RATest, self).__init__('raTest', 'RemoteArrange Test', 'RAT-')
        if isS250():
            self.slotList = list(range(101, 171)) + list(range(228, 271)) + list(range(501, 571)) + list(range(601, 671))
        else:
            self.slotList = list(range(101, 241)) + list(range(354, 441)) + list(range(501, 639)) + list(range(701, 839))
        self.emptyList = []

    
    def addEmptySlot(self, slot):
        if slot in self.slotList:
            self.emptyList.append(slot)
        else:
            raise Exception('Invalid slot id.')

    
    def _getRandomSlot(self):
        slen = len(self.slotList) - 1
        slot = random.randint(0, slen)
        while self.slotList[slot] in self.emptyList:
            slot = random.randint(0, slen)
        return self.slotList[slot]

    
    def _get2RandomSlot(self):
        slot1 = self._getRandomSlot()
        slot2 = self._getRandomSlot()
        while slot2 == slot1:
            slot2 = self._getRandomSlot()
        return (slot1, slot2)

    
    def _emptySwap(self):
        slot = self._getRandomSlot()
        empty = self.emptyList.pop()
        self.log.info('|====> move disc from slot %s to empty slot %s' % (slot, empty))
        self.controller.rackToRack(slot, empty)
        self.emptyList.append(slot)

    
    def _fullSwap(self):
        (slot1, slot2) = self._get2RandomSlot()
        empty = self.emptyList.pop()
        self.log.info('|====> move disc from slot %s to slot %s' % (slot1, slot2))
        self.controller.rackToRack(slot1, empty)
        self.controller.rackToRack(slot2, slot1)
        self.controller.rackToRack(empty, slot2)
        self.emptyList.append(empty)

    
    def run(self):
        
        try:
            while True:
                self._emptySwap()
                self._fullSwap()
        except:
            self.log.error('RA Test failed!\n%s' % traceback.format_exc())



if __name__ == '__main__':
    ra = RATest()
    if len(sys.argv) < 2:
        print('please input empty slot id')
        sys.exit(-1)
    
    
    try:
        for id in sys.argv[1:]:
            ra.addEmptySlot(int(id))
        
        ra.start()
        ra.run()
        ra.end()
    except MkcLockException:
        ex = None
        print(ex.message)
        sys.exit(-2)
    except:
        print(traceback.format_exc())
        sys.exit(-1)

    sys.exit(0)

