#!/usr/bin/python
#coding:utf-8
import os
import threading
import time
import sys
def exit():
    time.sleep(3)
    #os.abort()
    #return 0
    os._exit(0)

def main():
    t=threading.Thread(target=exit)
    t.setDaemon(True)
    t.start()
    a=raw_input('input:')
    print a
    print sys.stdin[1]
    print sys.stdin[2]

if __name__=='__main__':
    main()
