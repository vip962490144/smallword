import socketio
import random
import uuid
import time

#发言人token
token_arr = [
    '68760882b4e1ae23f4c0fe4ab8ccfc0901bf6bcb',
    'd84239b2448d814665f390d7b14c6fe2312b2ec8'
]

#说话库
speak_arr = [
    '这是第一句话，在很久很久以前....',
    '这是第二句话，在山上有座庙....',
    '大家好，我是渣渣辉。系兄弟就来kan我'
]
speak_arr_len = len(speak_arr)

#图片库
img_arr = [
    "https://cdn-image.onemicroworld.com/B488B79E-8141-258C-BD8D-FA2344B8E5A7?UCloudPublicKey=qgchM9CFzaKL9XWizIjY4EXmtmtDqPoFCr69qE5P&Signature=pkP5X7Qva3jkJrxM1YfkXclBKdQ%3D",
    "https://cdn-image.onemicroworld.com/B704D1A7-CD74-4677-0507-6D867535F58A?UCloudPublicKey=qgchM9CFzaKL9XWizIjY4EXmtmtDqPoFCr69qE5P&Signature=krP%2FAFmYR3oxGfFhnPphaLVy9H4%3D"
]

def connect():
    print("I'm connected!")
    return

#监听链接失败 无实际作用
def connect_error(err):
    print("The connection failed!")
    print(err)
    return

#监听链接断开 无实际作用
def disconnect():
    print("I'm disconnected!")
    return

#监听俱乐部说话
def club_msg(msg):
    print("!!!!receive: ", msg)
    return

#socketio对象数组 下标对应token的下标
sio_arr = []

#创建socketio对象 保存在数组
for i in range(len(token_arr)):
    sio_arr.append(socketio.Client(logger=True, engineio_logger=True))
    #链接socket
    #ws://test-socket.onemicroworld.com/socket.io/?EIO=3&transport=websocket&token=f0eef6ceef38db84028ec3e4f771f2cfcafc27ff&d_v=2.0
    sio_arr[i].on('connect', connect)
    sio_arr[i].on('connect_error', connect)
    sio_arr[i].on('disconnect', disconnect)
    sio_arr[i].on('club msg', club_msg)
    sio_arr[i].connect('ws://106.75.29.100:3000/socket.io?token=' + token_arr[i], transports=['websocket'])

for i in range(len(token_arr)):
    print("send!!!!!!")
    send_time = int(time.time() * 1000)
    #随机取一句话
    rand_num = random.randrange(0, speak_arr_len)
    rand_msg = speak_arr[rand_num]
    #发一句话
    sio_arr[i].emit('club msg', {
        "from":"8677",
        "to":"4178",
        "msg":{
            "id": str(uuid.uuid1()),
            "send_user":{
                "id":"8677",
                "avatar":"https://cdn-image.onemicroworld.com/10860-40308-yvu1-oskb-t4qd-photo?UCloudPublicKey=qgchM9CFzaKL9XWizIjY4EXmtmtDqPoFCr69qE5P&Signature=Ke6g0Asvs+pkxBB5V6Wz0n9+GLY=",
                "nickname":"哈哈",
                "vip":189,
                "star":57,
                "star_total":1807,
                "avatar_frame":0
            },
            "other_id":"4178",
            "chat_type":2,
            "msg": {"text": rand_msg,"realText":rand_msg,"atUserIdArr":[]},
            "msg_type":1,
            "send_time":send_time,
            "send_status":1,
            "chat_bubble_flag":False,
            "create_time":send_time,
            "bubble_read_status":1
        }
    })
    #发一张图
    sio_arr[i].emit('club msg', {
        "from":"10859",
        "to":"4178",
        "msg":{
            "id": str(uuid.uuid1()),
            "send_user":{
                "id":"10859",
                "avatar":"https://cdn-image.onemicroworld.com/10859-39970-gz2x-98a4-jv78-photo?UCloudPublicKey=qgchM9CFzaKL9XWizIjY4EXmtmtDqPoFCr69qE5P&Signature=6Y2T8K8dBzHupK9FBQRhzZ4AEBM=",
                "nickname":"专业测试人员qew",
                "vip":1,"star":123278,
                "star_total":123400,
                "avatar_frame":3
            },
            "other_id":"4178",
            "chat_type":2,
            "msg":{"thumbnail": img_arr[i] + "&iopcmd=thumbnail&type=6&gifmode=6&width=207&height=240",
                "origin": img_arr[i],
                "origin_w":828,
                "origin_h":1472,
                "show_w":135,
                "show_h":240,
                "clubTaskSubmit": None,
                "fileType":1
            },
            "msg_type":2,
            "send_time":send_time,
            "send_status":1,
            "chat_bubble_flag":False,
            "create_time":send_time,
            "bubble_read_status":1
        }
    })
    #等待1s
    time.sleep(1)