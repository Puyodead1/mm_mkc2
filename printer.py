# Source Generated with Decompyle++
# File: printer.pyc (Python 2.5)

'''
Created on 2010-5-28
@author: andrew.lu@cereson.com
'''
import time
import serial
import types
from PIL import Image
from mcommon import maskCard

class Printer(object):
    ESC = 27
    FS = 28
    VT = 11
    HT = 9
    GS = 29
    WIDTH = 32
    
    def __init__(self, port = '/dev/ttyUSB1', baudrate = 9600, timeout = 0.5):
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.timeout = timeout
        self.paperWidth = Printer.WIDTH

    
    def init(self):
        self.ser.open()
        self.ser.flushInput()
        self.ser.flushOutput()
        self.initPrinter()
        self.getPrinterStatus()
        self.reversePrint()

    
    def close(self):
        self.ser.close()

    
    def setPaperWidth(self, width):
        self.paperWidth = width

    
    def _xwrite(self, *args):
        for data in args:
            if type(data) == int:
                data = chr(data)
            elif type(data) == bytes:
                pass
            elif type(data) == str:
                data = str(data)
            else:
                print(type(data), str(data))
                raise ParameterException('invalid data type')
            self.ser.write(data)
        
        self.ser.flush()

    
    def initPrinter(self):
        self._xwrite(Printer.ESC, '@')

    
    def setCharset(self, n):
        if n < 0 or n > 3:
            raise ParameterException('invalid parameters')
        
        self._xwrite(Printer.ESC, '6', n)

    
    def paperSkip(self, n):
        if n < 0 or n > 255:
            raise ParameterException('invalid parameters')
        
        self._xwrite(Printer.ESC, 'J', n)

    
    def setLineSpace(self, n):
        if n < 0 or n > 255:
            raise ParameterException('invalid parameters')
        
        self._xwrite(Printer.ESC, '1', n)

    
    def setCharacterSpacing(self, n):
        if n < 0 or n > 255:
            raise ParameterException('invalid parameters')
        
        self._xwrite(Printer.ESC, 'p', n)

    
    def setVerticalTable(self, *args):
        self._xwrite(Printer.ESC, 'B')
        self._xwrite(*args)
        self._xwrite(0)

    
    def doVerticalTable(self):
        self._xwrite(Printer.VT)

    
    def setHorizontalTable(self, *args):
        self._xwrite(Printer.ESC, 'D')
        self._xwrite(*args)
        self._xwrite(0)

    
    def doHorizontalTable(self):
        self._xwrite(Printer.HT)

    
    def printSpace(self, count, type = 'LINE'):
        if type == 'LINE':
            self._xwrite(Printer.ESC, 'f', 1, count)
        elif type == 'SPACE':
            self._xwrite(Printer.ESC, 'f', 0, count)
        else:
            raise ParameterException('invalid parameters')

    
    def setRightLimit(self, n):
        self._xwrite(Printer.ESC, 'Q', n)

    
    def setLeftLimit(self, n):
        self._xwrite(Printer.ESC, 'l', n)

    
    def setGrayscale(self, n):
        if n < 0 or n > 13:
            raise ParameterException('invalid parameters')
        
        self._xwrite(Printer.ESC, 'm', n)

    
    def setCharacterWidth(self, n):
        if n < 0 or n > 4:
            raise ParameterException('invalid parameters')
        
        self._xwrite(Printer.ESC, '7', n)

    
    def setCharacterHeight(self, n):
        if n < 0 or n > 4:
            raise ParameterException('invalid parameters')
        
        self._xwrite(Printer.ESC, '8', n)

    
    def enableHalfMode(self, mode = True):
        self._xwrite(Printer.ESC, ':', int(mode))

    
    def enableUnderline(self, mode = True):
        self._xwrite(Printer.ESC, '-', int(mode))

    
    def enableOverline(self, mode = True):
        self._xwrite(Printer.ESC, '+', int(mode))

    
    def enableHighlight(self, mode = True):
        self._xwrite(Printer.ESC, 'i', int(mode))

    
    def reversePrint(self, mode = True):
        self._xwrite(Printer.ESC, 'c', int(not mode))

    
    def rotateCharacter(self, n):
        if n < 0 or n > 4:
            raise ParameterException('invalid parameters')
        
        self._xwrite(Printer.FS, 'I', n)

    
    def printImage(self, file):
        '''
        image max width is 380.
        '''
        MAX_WIDTH = 380
        image = Image.open(file)
        width = image.size[0]
        height = image.size[1]
        if width > MAX_WIDTH:
            h = height * MAX_WIDTH / width
            image = image.resize((MAX_WIDTH, h))
            width = image.size[0]
            height = image.size[1]
        
        mh = width * 3 / 256
        ml = width * 3 % 256
        turns = height / 24
        if height % 24:
            turns += 1
        
        self.setLineSpace(0)
        for t in range(turns):
            self._xwrite(Printer.ESC, 'K', ml, mh)
            for i in range(width):
                ret0 = 0
                for j in range(8):
                    
                    try:
                        pixel = image.getpixel((i, t * 24 + j))
                        if pixel[0] > 240:
                            ret0 = ret0 << 1
                        else:
                            ret0 = ret0 << 1 | 1
                    except IndexError:
                        ret0 = ret0 << 1

                
                ret1 = 0
                for j in range(8):
                    
                    try:
                        pixel = image.getpixel((i, t * 24 + j + 8))
                        if pixel[0] > 240:
                            ret1 = ret1 << 1
                        else:
                            ret1 = ret1 << 1 | 1
                    except IndexError:
                        ret1 = ret1 << 1

                
                ret2 = 0
                for j in range(8):
                    
                    try:
                        pixel = image.getpixel((i, t * 24 + j + 16))
                        if pixel[0] > 240:
                            ret2 = ret2 << 1
                        else:
                            ret2 = ret2 << 1 | 1
                    except IndexError:
                        ret2 = ret2 << 1

                
                self._xwrite(ret0, ret1, ret2)
            
            self.printLine('\n')
        
        self.printLine('(%s, %s)\n' % (width, height))
        self.setLineSpace(3)
        self.printSpace(2)

    
    def setBarCodeLineWidth(self, width1, width2):
        if width1 < 0 or width1 > 4:
            raise ParameterException('invalid parameters')
        
        if width2 not in list(range(3, 10, 2)):
            raise ParameterException('invalid parameters')
        
        self._xwrite(Printer.GS, 'W', width1, width2)

    
    def printBarCode(self, code, system = 'EAN_13', hri = True):
        self._xwrite(Printer.GS, 'H', int(hri))
        if system == 'EAN_13':
            self._xwrite(Printer.GS, 'k', 2)
        elif system == 'EAN_8':
            self._xwrite(Printer.GS, 'k', 3)
        else:
            raise ParameterException('invalid parameters')
        self._xwrite(code)
        self._xwrite(0)

    
    def setBarCodeHight(self, height):
        if height < 0 or height > 256:
            raise ParameterException('invalid parameters')
        
        self._xwrite(Printer.GS, 'h', height)

    
    def setBarCodeWidth(self, width):
        if width < 0 or width > 4:
            raise ParameterException('invalid parameters')
        
        self._xwrite(Printer.GS, 'w', width)

    
    def cutPaper(self, n):
        if n < 0 or n > 3:
            raise ParameterException('invalid parameters')
        
        self.printSpace(10)
        self._xwrite(Printer.ESC, 'k', n)

    
    def getPrinterStatus(self):
        self._xwrite(Printer.FS, 'v', 0)
        paper = self.ser.readlines()
        self._xwrite(Printer.FS, 'v', 1)
        door = self.ser.readlines()
        if not door:
            raise PrinterException('Communication error')
        
        return (ord(door[0]), ord(paper[0]))

    
    def printLine(self, line):
        self._xwrite(line)
        self._xwrite('\n')

    
    def printSplitLine(self, c):
        self.printLine(c * self.paperWidth)

    
    def printCenter(self, words, fillchar = ' '):
        self.printLine(words.center(self.paperWidth, fillchar))

    
    def printJustifyLine(self, key, value):
        self._xwrite(key)
        self._xwrite(':')
        self._xwrite(str(value).rjust(self.paperWidth - len(key) - 1))
        self._xwrite('\n')

    
    def printReceipt(self, kioskId, cart, customer, tc):
        self.printSplitLine('-')
        self.printCenter('Receipt')
        self.printSplitLine('-')
        transid = []
        for disc in cart.discs:
            transid.append(str(disc.trsID))
        
        self.printLine('ID: %s' % ' ,'.join(transid))
        self.printJustifyLine('Kiosk ID', kioskId)
        self.printLine('')
        self.printJustifyLine('Card Number', maskCard(customer.ccNum))
        self.printJustifyLine('Customer', customer.ccName)
        self.printCenter(' Details ', '=')
        totalAmount = 0
        finished = cart.getEjectedDiscs()
        discFail = False
        for disc in cart.discs:
            totalAmount += float(disc.preauthAmount)
            msg = ''
            if disc.gene == 'rent':
                msg = 'Rental Deposit'
            else:
                msg = 'Sales'
            if disc not in finished:
                msg = msg + ' *'
                discFail = True
            
            self.printJustifyLine(msg, disc.preauthAmount)
        
        self.printSplitLine('-')
        self.printJustifyLine('Total', '%.2f' % round(totalAmount, 2))
        self.printSplitLine('=')
        if tc:
            self.printLine('')
            self.printLine('Terms and Conditions:')
            self.printLine(tc)
        
        if discFail == True:
            self.printLine('The disc with * is charged but not ejected. You can get full refund in 10 mins if NO disc is out. If only partial is ejected, the refund will happen when ALL the out discs in Receipt are returned AND you are still over-charged.')
        
        self.printLine('')
        self.printLine(time.strftime('%Y-%m-%d %H:%M').rjust(self.paperWidth))
        self.printSplitLine('-')
        self.cutPaper(1)



class PrinterException(Exception):
    pass


class ParameterException(Exception):
    pass


def printTest():
    ShoppingCart = ShoppingCart
    Customer = Customer
    import mobject
    UmsProxy = UmsProxy
    import proxy.ums_proxy
    printer = Printer()
    printer.init()
    cart = ShoppingCart()
    customer = Customer()
    customer.ccNum = '6222310348520562'
    customer.ccName = 'Mr. Test'
    umsProxy = UmsProxy.getInstance()
    tc = umsProxy.getAbbrTermsAndConditions()
    printer.printReceipt('A911', cart, customer, tc)


def main():
    printer = Printer()
    printer.init()
    print(printer.getPrinterStatus())
    for i in range(3):
        printer.printLine('Test line %s ......' % i)
    
    printer.printBarCode('1234567890abc')
    printer.printImage('ceresonLogo.jpg')
    printer.enableHighlight()
    printer.printLine('Test line Test more ......')
    printer.enableHighlight(False)
    printer.enableOverline()
    printer.printLine('Test line Test more ......')
    printer.enableOverline(False)
    printer.enableUnderline()
    printer.printLine('Test line Test more ......')
    printer.enableUnderline(False)
    printer.reversePrint()
    printer.printLine('More ......')
    printer.reversePrint(False)
    printer.cutPaper(1)

if __name__ == '__main__':
    printTest()

