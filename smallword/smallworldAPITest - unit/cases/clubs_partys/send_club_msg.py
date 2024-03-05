import socketio
import random
import uuid
import time

# 发言人token
token_arr = [
    'a27add7987f9d72128b124eea8d5f018bbb8ad7f'
]

# 说话库
speak_arr = [
    '这是第一句话，在很久很久以前....',
    '这是第二句话，在山上有座庙....',
    '大家好，我是渣渣辉。系兄弟就来kan我'
]
speak_arr_len = len(speak_arr)

# 图片库
img_arr = [
    "https://cdn-image.onemicroworld.com/B488B79E-8141-258C-BD8D-FA2344B8E5A7?UCloudPublicKey=qgchM9CFzaKL9XWizIjY4EXmtmtDqPoFCr69qE5P&Signature=pkP5X7Qva3jkJrxM1YfkXclBKdQ%3D",
    "https://cdn-image.onemicroworld.com/B704D1A7-CD74-4677-0507-6D867535F58A?UCloudPublicKey=qgchM9CFzaKL9XWizIjY4EXmtmtDqPoFCr69qE5P&Signature=krP%2FAFmYR3oxGfFhnPphaLVy9H4%3D",
    "https://cdn-image.onemicroworld.com/10756-42939-4748-kyut-lr24-avatar?UCloudPublicKey=qgchM9CFzaKL9XWizIjY4EXmtmtDqPoFCr69qE5P&Signature=NCJL0oBJ87iOGaT%2BjfoRagBYDdE%3D",
    "https://cdn-image.onemicroworld.com/12868-51303-y586-jnrb-5nqw-photo?UCloudPublicKey=qgchM9CFzaKL9XWizIjY4EXmtmtDqPoFCr69qE5P&Signature=dyxNJwzg0UneLN/aRMa316eAXAw="
]


def connect():
    print("I'm connected!")
    # pass
    return


# 监听链接失败 无实际作用
def connect_error(err):
    print("The connection failed!")
    print(err)
    return
    # pass


# 监听链接断开 无实际作用
def disconnect():
    print("I'm disconnected!")
    return
    # pass


# 监听俱乐部说话
# def club_msg(msg):
#     print("!!!!receive: ", msg)
#     return
    # pass


# 发送socket消息次数
range_num = 10

# socketio对象数组 下标对应token的下标
sio_arr = []

# 创建socketio对象 保存在数组
for i in range(range_num):
    sio_arr.append(socketio.Client(logger=True, engineio_logger=True))
    # 链接socket
    # ws://test-socket.onemicroworld.com/socket.io/?EIO=3&transport=websocket&token=f0eef6ceef38db84028ec3e4f771f2cfcafc27ff&d_v=2.0
    sio_arr[i].on('connect', connect)
    sio_arr[i].on('connect_error', connect)
    sio_arr[i].on('disconnect', disconnect)
    # sio_arr[i].on('club msg', club_msg)
    # sio_arr[i].connect('ws://106.75.29.100:3000/socket.io?token=' + token_arr[i], transports=['websocket'])
    # token随机抽取
    token_num = random.randint(0, 1)
    # print(token_num)
    sio_arr[i].connect('ws://test-socket.onemicroworld.com/socket.io?token=' + token_arr[0], transports=['websocket'])

time.sleep(1)

for i in range(range_num):
    print("send!!!!!!")
    send_time = int(time.time() * 1000)
    # 随机取一句话
    # rand_num = random.randrange(0, speak_arr_len)
    # rand_msg = speak_arr[rand_num]
    # 图片随机抽取
    # img_num = random.randint(0, len(img_arr))
    try:
        # 发一句话
        sio_arr[i].emit('club msg', {
            "from": "10756",
            "to": "12749",
            "msg": {
                "id": str(uuid.uuid1()),
                "send_user": {
                    "id": "10756",
                    "avatar": "https://cdn-image.onemicroworld.com/10756-42939-4748-kyut-lr24-avatar?UCloudPublicKey=qgchM9CFzaKL9XWizIjY4EXmtmtDqPoFCr69qE5P&Signature=NCJL0oBJ87iOGaT%2BjfoRagBYDdE%3D",
                    "nickname": "Max零零二灬🐯",
                    "vip": 104,
                    "star": 87,
                    "star_total": 220,
                    "avatar_frame": 3
                },
                "other_id": "12749",
                "chat_type": 2,
                "msg": {"text": speak_arr[2], "realText": speak_arr[2], "atUserIdArr": []},
                "msg_type": 1,
                "send_time": send_time,
                "send_status": 1,
                "chat_bubble_flag": False,
                "create_time": send_time,
                "bubble_read_status": 1
            }
        })
        sio_arr[i].callbacks()
        # 等待3s
        time.sleep(1.5)
        # 发一张图
        sio_arr[i].emit('club msg', {
            "from": "12868",
            "to": "12749",
            "msg": {
                "id": str(uuid.uuid1()),
                "send_user": {
                    "id": "12868",
                    "avatar": "https://cdn-image.onemicroworld.com/12868-51303-y586-jnrb-5nqw-photo?UCloudPublicKey=qgchM9CFzaKL9XWizIjY4EXmtmtDqPoFCr69qE5P&Signature=dyxNJwzg0UneLN/aRMa316eAXAw=",
                    "nickname": "Nv七二零",
                    "vip": 1, "star": 0,
                    "star_total": 0,
                    "avatar_frame": 0
                },
                "other_id": "12749",
                "chat_type": 2,
                "msg": {"thumbnail": img_arr[3] + "&iopcmd=thumbnail&type=6&gifmode=6&width=207&height=240",
                        "origin": img_arr[3],
                        "origin_w": 828,
                        "origin_h": 1472,
                        "show_w": 135,
                        "show_h": 240,
                        "clubTaskSubmit": None,
                        "fileType": 1
                        },
                "msg_type": 2,
                "send_time": send_time,
                "send_status": 1,
                "chat_bubble_flag": False,
                "create_time": send_time,
                "bubble_read_status": 1
            }
        })
    except Exception as e:
        pass
    # 等待1.5s
    time.sleep(1.5)
