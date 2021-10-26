# -*- coding: UTF-8 -*-
import socket
import select
from json import *
pw='lyt'
sv='1'
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 6666))
sock.listen(5)
inputs = [sock]
boss=None
servant=None

while True:
    r_list, w_list, e_list = select.select(inputs, [], [])
    for event in r_list:
        if event is sock:
            s, addr = event.accept()
            print(addr,"新的客户端连接")
            inputs.append(s)
            inf="当前连接数："+str(len(inputs)-1)
            if boss!=None:
                boss.send(dumps({'msg':inf,'op':'cmd_rv'}).encode('utf-8'))
        else:
            try:
                data = event.recv(1024)
                if not data:
                   if boss!=None and boss==event:
                       boss=None
                       inputs.remove(event)
                       continue
                obj = loads(data.decode("utf-8"))
                id = obj['id']
                msg = obj['msg']
                op=obj['op']
                if id == pw and msg == pw:
                   inf = "当前连接数：" + str(len(inputs) - 1)
                   boss=event
                   if boss != None:
                       boss.send(dumps({'op':'cmd_rv','msg':inf}).encode('utf-8'))
                       continue
                elif id==sv and msg==sv:
                    servant=event
                elif op=='cmd':
                   if servant!=None:
                       servant.send(dumps({'op':op,'msg':msg}).encode('utf-8'))
                elif op=='cmd_size':
                   now=0
                   boss.send(dumps({'op':op,'msg':msg}).encode('utf-8'))
                   while now != msg:
                       if msg-now>1024:
                           size=1024
                       else:
                           size=msg-now
                       now+=size
                       data=event.recv(size)
                       print(data)
                       boss.send(data)
                elif op=='cmd_rv':
                    boss.send(data)
                elif op=='get':
                    servant.send(dumps({'op':op,'msg':msg}).encode('utf-8'))
                elif op=='get_rv':
                    boss.send(dumps({'op': op, 'msg': msg}).encode('utf-8'))
                    now=0
                    name,size=msg.split('|')
                    size=int(size)
                    while now!=size:
                        data=event.recv(1024)
                        now+=len(data)
                        boss.send(data)
                elif op=='put':
                    servant.send(data)
                    now=0
                    name,size=msg.split('|')
                    size=int(size)
                    while now!=size:
                        data=event.recv(1024)
                        now+=len(data)
                        servant.send(data)
                else:
                    print(op," ",msg)
            except(socket.error):
                if boss != None and boss == event:
                   boss=None
                inputs.remove(event)
                continue








