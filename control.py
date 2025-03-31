# Source Generated with Decompyle++
# File: control.pyc (Python 2.5)

'''
robot interface for new S250 
note:
Do not blame me for the poor code style. 
many codes are copied from the former one.
Change Log:
2009-02-26 Vincent Fix a bug of status[2]
2011-02-24 Tim Fix the bug for the card number contains space of American Express
'''

try:
    import psyco
    psyco.full()
except:
    pass

__VERSION__ = '1.0'
import random
import sys
import time

from mcommon import Robot


def parseTrack(track1, track2):
    """
    T1:%B379014336027929^RECIPIENT/GIFT CARD       ^08121010510535320000000000000000?.65
    T2:%379014336027929^081210105105353200000?.2A
'T1:%B4988820004558168^LU/PIN*LU ^0908101100000000085000000?.F2\r
'
    """
    (ccNumber, ccName, ccExpDate) = ('', '', '')
    if track1:
        lines = track1.split('^')
        if not (len(lines) != 3):
            ccNumber = str(lines[0][1:]).strip().replace(' ', '')
            ccName = lines[1].strip().replace("'", '')
            ccExpDate = lines[2][:4]
        
    
    return (ccNumber, ccName, ccExpDate)


class CCValidator:
    
    def doubler(self, digit):
        '''Double digit, add its digits together if they are >= 10'''
        digit = int(digit)
        digit = digit * 2
        if digit < 0:
            print('Error!  digit < 0 sent: ' + str(digit))
            sys.exit(1)
        
        if digit > 18:
            print('Error!  digit > 18 sent: ' + str(digit))
            sys.exit(1)
        
        if digit < 10:
            return digit
        
        return digit - 9

    
    def reverse(self, str):
        '''Reverse the string str'''
        buf = ''
        a = 0
        while a < len(str):
            a += 1
            buf += str[-a]
        return buf

    
    def check(self, cc):
        '''Given a cc number (string), will return True if it passes mod10 check, False otherwise'''
        cc = self.reverse(cc)
        a = 0
        total = 0
        
        try:
            while a < len(cc):
                if a % 2 == 1:
                    total = total + self.doubler(cc[a])
                else:
                    total = total + int(cc[a])
                a += 1
        except:
            return False

        if total % 10 == 0:
            return True
        else:
            return False

    
    def make_number(self, prefix, length):
        '''Generate a random number that starts with prefix and is length long that passes mod10'''
        valid = False
        while not valid:
            cc = prefix
            while len(cc) < length:
                cc = cc + str(random.choice((0, 1, 2, 3, 4, 5, 6, 7, 8, 9)))
            if self.check(cc):
                valid = True
            
        return cc

    
    def make_invalid_number(self, prefix, length):
        '''generate a random number that starts with prefix and is length long that fails the mod10 test'''
        invalid = False
        while not invalid:
            cc = prefix
            while len(cc) < length:
                cc = cc + str(random.choice((0, 1, 2, 3, 4, 5, 6, 7, 8, 9)))
            if not self.check(cc):
                invalid = True
            
        return cc

    
    def print_numbers(self, count):
        '''Print count numbers that pass mod10 - example function'''
        passed = 0
        while passed < count:
            cc = self.make_number('4', 16)
            passed = passed + 1


'\ndef initlog(name):\n    log = logging.getLogger(name)\n    log.setLevel(logging.DEBUG)\n\n    hConsole = logging.StreamHandler()\n    hConsole.setLevel(logging.DEBUG)\n    hConsole.setFormatter(logging.Formatter(\'%(asctime)s %(name)s  %(levelname)s \t %(message)s\'))\n    log.addHandler(hConsole)\n\n    hFile = handlers.TimedRotatingFileHandler("./robot.log", \'D\', 1, 3)\n    hFile.setLevel(logging.INFO)\n    hFile.setFormatter(logging.Formatter(\'%(asctime)s %(name)s %(levelname)s \t %(message)s\'))\n    log.addHandler(hFile)\n\n    return log\n'


if __name__ == '__main__':
    robot = Robot.getInstance()
    while True:
        r = robot.doCmdSync('read_card', { }, 100)
        print(r)
    # while True:
    #     id = robot.doCmdAsync('suck_disc', { }, 5)
    #     mlog.debug('canceling...')
    #     time.sleep(5)
    #     robot.cancel()
    #     r = robot.getResult(id)
    #     print('*********************')
    #     print(r)
    #     print('*********************')
    #     continue
    #     continue
    #     '\n        s=raw_input("-->")\n        if s:\n            s=s.split()\n            robot.doCmdSync(s[0],)\n        '

