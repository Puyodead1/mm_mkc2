# Source Generated with Decompyle++
# File: flashScreen.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2009-05-18 Andrew
andrew.lu@cereson.com

Filename: flashScreen.py

Change Log:
    

'''
import ui_proxy
from mcommon import *
log = initlog('flashScreen')
screen = None

def startScreen():
    global screen
    screen = ui_proxy.IF(F_Q_SEND, F_Q_RECEIVE, config.flash_port)
    screen.start()
    screen.waitClient()


def restartScreen():
    screen.restartQtGui()
    log.info('GUI Restarted. ')

