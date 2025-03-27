# Source Generated with Decompyle++
# File: config_mkc.pyc (Python 2.5)

import logging.handlers as logging
HOST = '127.0.0.1'
PORT = 50007
MAXDATA = 2 * 4096
KIOSK_CONF = '/etc/kioskhome'
file = open(KIOSK_CONF, 'r')
HOMEDIR = file.readline().rstrip()
file.close()
transDir = HOMEDIR + 'kiosk/mkc2/gui/'

def initLog(name):
    logger = logging.getLogger()
    rotateHandle = logging.handlers.TimedRotatingFileHandler(HOMEDIR + 'kiosk/var/log/' + name, 'midnight')
    formatter = logging.Formatter('%(asctime)s : %(levelname)-8s %(message)s')
    rotateHandle.setFormatter(formatter)
    logger.addHandler(rotateHandle)
    logger.setLevel(logging.DEBUG)
    return logger

