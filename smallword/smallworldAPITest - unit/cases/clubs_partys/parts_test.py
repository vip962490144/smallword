# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import json
import socketserver
import websocket
import socket

from scripts.handle_config import do_config
from scripts.logins.login_base import LoginBase

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = socket.gethostbyname("test-socket.onemicroworld.com")
# HOST = "test-socket.onemicroworld.com"
PORT = 443
# PORT = 80
BUFSIZ = 1024
ADDR = (HOST, PORT)

ws = websocket.WebSocket()
ws.connect("ws://example.com/websocket", http_proxy_host="proxy_host_name", http_proxy_port=3128)

# actual = LoginBase().login(do_config("username", "A"))
# token = actual.json()["token"]
# print(token)
# sock.bind(ADDR)

sock.connect(ADDR)

i = 0
while i < 10:
    # cmd = input("Please input msg:")
    dict_a = ""
    data1 = '{{"query": {"token": "e0ab81f1771b6f1725ef13855ad0a0a0650ebed1", "d_v": "1"}},' \
            '{' \
            '"from": 12703,' \
            '"to": 12707,' \
            '"msg": {"id": "0b346bb5-8d0f-4b74-bf84-629944c6b8ec", "type": 1,' \
            '"content": {' \
            '"text": "hello",' \
            '"realText": "hello"' \
            '}}}}'
    # data1 = json.loads(data1)
    # print(type(data1))
    str_1 = data1.encode()
    sock.send(str_1)
    data = sock.recv(1024)
    print(data)
    i += 1

sock.close()

    # s.close()
