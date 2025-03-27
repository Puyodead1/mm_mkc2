# Source Generated with Decompyle++
# File: linuxCmd.pyc (Python 2.5)

'''

MovieMate Kiosk Core V2.0
CopyRight MovieMate, Inc.

Created 2009-03-03 Andy
andy.zhang@cereson.com

Filename:linuxCmd.py
All linux cmd

Change Log:
'''
import os
import time
from queue import *
from random import choice
from time import strftime, strptime
import fcntl
import subprocess
from config import MVMOUSE, KIOSK_HOME, VGA_PORT
from proxy.conn_proxy import ConnProxy
lockfile = open('/tmp/hdmi.lock', 'w')

def lock():
    for i in range(10):
        
        try:
            fcntl.lockf(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except:
            time.sleep(0.5)

    


def unlock():
    fcntl.lockf(lockfile, fcntl.LOCK_UN)


def get_hdmi_port():
    cmd = 'echo \'howcute121\' | sudo -S sh -c "dmidecode | grep -A8 \'Base Board Information$\' | grep \'Product Name\'"'
    output = subprocess.getoutput(cmd)
    base_board = output.split(':')
    if base_board[-1].strip() == 'DG45FC':
        hdmi_port = 'HDMI-1'
    else:
        hdmi_port = 'HDMI-2'
    return hdmi_port


def startHdmi():
    '''
    This api can only run in main thread, because it uses ConnProxy singleton.
    '''
    hdmi_port = get_hdmi_port()
    lock()
    if os.path.exists(os.path.join(KIOSK_HOME, 'kiosk/tmp/hdmimonitor.start')):
        (w, r) = os.popen2('DISPLAY=:0.0 /usr/bin/xrandr -q | /bin/grep -i %s | /bin/grep -w -i connected' % hdmi_port)
        data = r.read()
        w.close()
        r.close()
        if data != '':
            if os.system('DISPLAY=:0.0 /usr/bin/xrandr --output %s --auto' % hdmi_port):
                os.system('DISPLAY=:0.0 /usr/bin/xrandr --output %s --auto' % hdmi_port)
            
            time.sleep(3)
            if os.system('DISPLAY=:0.0 /usr/bin/xrandr --output %s --left-of %s' % (VGA_PORT, hdmi_port)):
                os.system('DISPLAY=:0.0 /usr/bin/xrandr --output %s --left-of %s' % (VGA_PORT, hdmi_port))
            
            time.sleep(3)
            os.system('touch %s' % os.path.join(KIOSK_HOME, 'kiosk/tmp/hdmi.connected'))
            ConnProxy().setHDMI('on')
        
    
    unlock()
    os.system('DISPLAY=:0.0 %s 800 -800' % MVMOUSE)


def stopHdmi():
    '''
    This api can only run in main thread, because it uses ConnProxy singleton.
    '''
    lock()
    if os.path.exists(os.path.join(KIOSK_HOME, 'kiosk/tmp/hdmimonitor.start')):
        os.system('pkill mplayer')
        if os.path.exists(os.path.join(KIOSK_HOME, 'kiosk/tmp/hdmi.connected')):
            os.remove(os.path.join(KIOSK_HOME, 'kiosk/tmp/hdmi.connected'))
        
        os.system('DISPLAY=:0.0 xrandr --output %s --off' % get_hdmi_port())
        ConnProxy().setHDMI('off')
    
    unlock()


def changeHostName(name):
    if not name:
        return 0
    else:
        cmd = 'echo ' + name + ' > /tmp/hostname.tmp;echo howcute121 | sudo -S  mv /tmp/hostname.tmp /etc/hostname'
        os.system(cmd)
        cmd = 'echo howcute121 | sudo -S hostname ' + name
        os.system(cmd)
        cmd = 'cat /etc/hosts | grep -v S250 > /tmp/hosts.tmp;echo howcute121 | sudo -S mv /tmp/hosts.tmp /etc/hosts;echo howcute121 | sudo -S echo 127.0.0.1 ' + name + ' >> /etc/hosts'
        os.system(cmd)
        (wfd, rfd) = os.popen2('hostname')
        hostname = rfd.read().split('\n')
        if hostname[0] == name:
            return 1
        else:
            return 0


def setSystemVolume(volume):
    os.system('amixer set Master %s%%' % volume)


def storeSystemVolume(volume):
    os.system('amixer set Master %s%%' % volume)
    os.system("echo 'howcute121' | sudo -S alsactl store")

