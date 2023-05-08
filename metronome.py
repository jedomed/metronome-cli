#!/usr/bin/env python3
import subprocess
import sys
import os
import time
from threading import Thread
import termios
from termios import *

def calc_bpm(bpm):
    bpm_time = 60/bpm
    print("BPM:", bpm)
    return bpm_time

bpm = float(sys.argv[1])
bpm_time = calc_bpm(bpm)

def repeat_play_sound():
    starttime = time.time()
    while True:
        subprocess.Popen(["ogg123", "/home/borot/dun.ogg"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)
        time.sleep(bpm_time - ((time.time() - starttime) % bpm_time))


class _Getch:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:       
            mode = old_settings
            mode[3] = mode[3] & ~(ECHO | ICANON | IEXTEN)
            tcsetattr(sys.stdin.fileno(), TCSAFLUSH, mode)
            ch = sys.stdin.read(3)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def key_read():
    def add_bpm(add):
        global bpm
        bpm = bpm + add
        if bpm <= 0:
            bpm = 1
        bpm_time = 60/bpm
        print("\033[A                             \033[A")
        print("BPM:", bpm)
        return bpm_time
    while True:
        global bpm_time
        inkey = _Getch()
        k=inkey()
        if k=='\x03[C':
            os._exit(1)
        elif k=='\x1b[A':
            bpm_time = add_bpm(1)
        elif k=='\x1b[B':
            bpm_time = add_bpm(-1)

if __name__ == '__main__':
    Thread(target = key_read).start()
    Thread(target = repeat_play_sound).start()
