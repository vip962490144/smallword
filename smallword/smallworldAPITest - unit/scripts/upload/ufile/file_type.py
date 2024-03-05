# -*- coding:utf-8 -*-
# @Author   :Jaden.wang
import os
import re

import filetype

def main(url):
    kind = filetype.guess(url)
    if kind is None:
        print('Cannot guess file type!')
        return

    print('File extension: %s' % kind.extension)
    print('File MIME type: %s' % kind.mime)
    print(kind.mime)


def file_type(url):
    kind = filetype.guess(url)
    if kind is None:
        print('Cannot guess file type!')
        return

    return kind.mime


# 判断文件类型
def get_file_type(work_path):
    url = work_path
    work_path = os.path.basename(work_path)
    # 判断是不是..视频
    if work_path.endswith(('.mp4', '.mkv', '.avi', '.wmv', '.iso')):
        kind = filetype.guess(url)
        data = {"type": 2, "duration": "10047", "mime_type": kind.mime,
                "thumbnail_mime_type": kind.mime}
        return data
    elif work_path.endswith(('.jpg', '.png', '.jpeg', '.bmp')):
        kind = filetype.guess(url)
        data = {"type": 1, "mime_type": kind.mime}
        return data


if __name__ == '__main__':
    url = r'D:\1.jpg'
    localfile1 = r'D:\test.mp4'
    # main(url)
    data = get_file_type(url)
    print(data)
