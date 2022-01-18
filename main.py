import socket,time,threading
import os.path
import configparser
from json import *
from menu import show

#init
host=""
port=0
recv_path=""
try:
    ini="./configuation.ini"
    config = configparser.ConfigParser()
    config.read(ini,encoding='utf-8')
    host=config.get('server_IP','ip')
    port=int(config.get('server_IP','port'))
    recv_path=config.get('default','default_dir')
except:
    print("初始化配置出错，检查configuation.ini文件")
def RThread(s):
    while True:

        data = s.recv(1024)
        if not data:
            s.close()
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
            if not os.path.isdir(recv_path):
                os.mkdir(recv_path)
            os.chdir(recv_path)
            f=open(name,'ab')
            while now !=size:
                data=s.recv(1024)
                f.write(data)
                now+=len(data)
            print('接收完毕')
            f.close()
        elif op=='cmd_rv':
            print(msg)
        elif op=='put_rv1':
            if msg == 'ok':
                size=f_size
                s.send(dumps({'id':id,'op':'put_rv2','msg':f_size}).encode('utf-8'))
                f = open(addr, 'rb')
                has_send = 0
                while has_send != size:
                    file = f.read(1024)
                    s.sendall(file)
                    has_send += len(file)
                f.close()
            else:
                print(msg)

def put(msg):
    global f_size
    global addr
    addr=msg
    address=input("对方存放文件的路径")
    if os.path.isfile(msg):
        size=os.stat(msg).st_size
        f_size=size
        message=address+'|'+os.path.basename(msg)+'|'+str(size)
        print(message)
        s.send(dumps({'id': id, 'msg': message,'op':'put'}).encode('utf-8'))
    else:
        print('文件夹不存在')
def reconnect():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
      try:
         s.connect((host,port))
         sl = "admin"
         print("连接成功")
         s.send(dumps({'id': id, 'msg': sl,'op':'cmd'}).encode('utf-8'))
         wainct=0
         break
      except:
          print('\r','---重连中等待---',flush=True,end='')
          time.sleep(3)
    return s

id='admin'
addr=''
f_size=0
s=reconnect()
t1=threading.Thread(target=RThread,args=(s,))
t1.setDaemon(True)
t1.start()

while True:
    a=input("")
    b=a.split()
    if b[0]=='get' and len(b)==2:
        s.send(dumps({'id':id,'op':'get','msg':b[1]}).encode('utf-8'))
    elif b[0]=='put' and len(b)==2:
        put(b[1])
    else:
        s.send(dumps({'id':id,'op':'cmd','msg':a}).encode('utf-8'))















