import cv2
import argparse
import os
import time
import csv
import codecs
import pandas as pd

from scripts.constants import BASE_DIR, CONFIGS_DIR


def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Process pic')
    parser.add_argument('--input', help='video to process', dest='input', default=None, type=str)
    parser.add_argument('--output', help='pic to store', dest='output', default=None, type=str)
    # default为间隔多少帧截取一张图片
    parser.add_argument('--skip_frame', dest='skip_frame', help='skip number of video', default=100,
                        type=int)  # 此处可更改提取帧的间隔
    args = parser.parse_args(
        ['--input', r'D:\viddd.mp4', '--output', r'D:\video-photo'])  # 此处添加路径，input为输入视频的路径 ，output为输出存放图片的路径
    return args


def process_video(i_video, o_video, num):
    cap = cv2.VideoCapture(i_video)
    num_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    expand_name = '.jpg'
    if not cap.isOpened():
        print("Please check the path.")
    cnt = 0
    count = 0
    while 1:
        ret, frame = cap.read()
        cnt += 1
        #  how
        # many
        # frame
        # to
        # cut
        if cnt % num == 0:
            count += 1
            cv2.imwrite(os.path.join(o_video, str(count) + expand_name), frame)

        if not ret:
            break

def write_config(mobile):
    """
    将数据写入配置文件
    :return:
    """
    boy_text = os.path.join(CONFIGS_DIR, "test_user_7.txt")
    with open(boy_text, 'a') as boy:
        boy.write(str(mobile)+',\n')


if __name__ == '__main__':

    # args = parse_args()
    # if not os.path.exists(args.output):
    #     os.makedirs(args.output)
    # print('Called with args:')
    # print(args)
    # process_video(args.input, args.output, args.skip_frame)
    # print(BASE_DIR)
    # mobile = 13520000000
    # for var in range(20000):
    #     write_config(mobile)
    #     mobile += 1

    # with open("Ex_info.csv","a+") as csvfile: ##“ ab+ ”去除空白行，又叫换行！
    #     csvfile.write(codecs.BOM_UTF8)  ##存入表内的文字格式
    #     writer = csv.writer(csvfile)  #存入表时所使用的格式
    #     writer.writerow(['表头','表头','表头','表头'])
    # mobile = 13520000000

    # with open("my.csv", "a", newline='') as f:
    #     for var in range(2):
            # write_config(mobile)
            #
            # writer = csv.writer(f)
            # writer.writerow(["mobile"])
            # row = [mobile]
            # for r in row:
            #     writer.writerow(r)
            # mobile += 1

    mobile = 13520010000
    columns = ["mobile"]
    result_list = []
    for var in range(10000):
        # write_config(mobile)
        list_a = [mobile]
        result_list.append(list_a)
        mobile += 1

    # for var in result_list:
    dt = pd.DataFrame(result_list, columns=columns)
    dt.to_excel("result1.xlsx", index=0)
    dt.to_csv("result1.csv", index=0)
