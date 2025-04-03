# Source Generated with Decompyle++
# File: dvr.pyc (Python 2.5)

import os
import sys
import signal
child = -1
pth = ''

def start_record(pth):
    global child
    if child > 0:
        return 2
    
    
    try:
        if os.access(pth, os.F_OK):
            os.remove(pth)
    except:
        return -1

    child = os.fork()
    if child == 0:
        for fd in range(3, 1024):
            
            try:
                os.close(fd)
            except:
                pass

        
        
        try:
            print('execl...')
            os.execl('/usr/bin/ffmpeg', 'ffmpeg', '-loglevel', 'quiet', '-f', 'video4linux2', '-i', '/dev/video0', '-s', 'cif', '-y', pth)
            print('$$$$')
        except:
            pass

        print('****')
        sys.exit(-1)
    
    return 0


def stop_record():
    global child
    if child > 0:
        
        try:
            os.kill(child, signal.SIGQUIT)
            os.waitpid(child, os.WNOHANG)
        except:
            pass

    
    child = -1
    pth = ''
    return 0

if __name__ == '__main__':
    r = start_record('/tmp/test.avi')
    print(r)
    import time
    time.sleep(5)
    stop_record()

