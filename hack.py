import os.path
import socket
import time
import threading
from json import *

host='127.0.0.1'
port=6666
p='cmd'
def RThread(s):
    while True:
      try:
        data = s.recv(1024)
        if not data:
            break
        data=data.decode('utf-8')
        obj = loads(data)
        op=obj['op']
        msg=obj['msg']
        if op=='cmd_size':
            now =0
            while now != msg:
                if msg - now > 1024:
                    size = 1024
                else:
                    size = msg - now
                now += size
                data=s.recv(size).decode('utf-8')
                print(data)
        elif op=='get_rv':
            print('开始接收')
            now=0
            name,size=msg.split('|')
            size=int(size)
            if not os.path.isdir("d:/接收"):
                os.mkdir("d:/接收")
            os.chdir("d:/接收")
            f=open(name,'ab')
            while now !=size:
                data=s.recv(1024)
                f.write(data)
                now+=len(data)
            print('接收完毕')
            f.close()
        elif op=='cmd_rv':
            print(msg)
        else:
            print(data)

      except(socket.error):
          s=reconnect()
      except:
          pass
def put(msg):
    if os.path.isfile(msg):
        size=os.stat(msg).st_size
        message=msg+'|'+str(size)
        s.send(dumps({'id':id,'op':'put','msg':message}).encode('utf-8'))
        f=open(msg,'rb')
        has_send = 0
        while has_send != size:
            file = f.read(1024)
            s.sendall(file)
            has_send += len(file)
        f.close()
    else:
        print("文件夹不存在")


def reconnect():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
      try:
         s.connect((host,port))
         sl = "lyt"
         s.sendall(dumps({'id': id, 'msg': sl,'op':p}).encode('utf-8'))
         print("连接成功")
         break
      except:
          print("---重连中")
          time.sleep(3)
    return s
id='lyt'
s=reconnect()
t1=threading.Thread(target=RThread,args=(s,))
t1.setDaemon(True)
t1.start()
while True:
    a=input("")
    b=a.split()
    if b[0]=='cmd' or b[0]=='get' or b[0]=='put':
        p=b[0]
        if p=='put':
            put(b[1])
        else:
            s.sendall(dumps({'id':id,'op':p,'msg':b[1]}).encode('utf-8'))
    else :
        s.sendall(dumps({'id': id, 'op':p,'msg':a}).encode("utf-8"))













