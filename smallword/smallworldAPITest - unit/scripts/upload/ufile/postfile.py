# -*- coding: utf-8 -*-


import os
import time
import hashlib
import json
from .baseufile import BaseUFile
from .httprequest import _put_stream, _put_file, _post_file, ResponseInfo, _uploadhit_file, _download_file, _delete_file, _getfilelist, _head_file, _restore_file, _classswitch_file, _copy_file, _rename_file
from .util import _check_dict, ufile_put_url, ufile_post_url, file_etag, ufile_uploadhit_url, ufile_getfilelist_url, mimetype_from_file, ufile_restore_url, ufile_classswitch_url, ufile_copy_url, ufile_rename_url
from .logger import logger
from .compact import b, s, u, url_parse
from . import config
from .config import BLOCKSIZE
import string


def postfile(url,authorization, key, localfile, header=None):
    """
    表单上传文件到UFile空间

    :param key:  string 类型，上传文件在空间中的名称
    :param localfile: string类型，本地文件名称
    :param header: dict类型，http 请求header，键值对类型分别为string，比如{'User-Agent': 'Google Chrome'}
    :return: ret: 如果http状态码为[200, 204, 206]之一则返回None，否则如果服务器返回json信息则返回dict类型，键值对类型分别为string, unicode string类型，否则返回空的dict
    :return:  ResponseInfo: 响应的具体信息，UCloud UFile 服务器返回信息或者网络链接异常
    """
    if header is None:
        header = dict()
    _check_dict(header)
    if 'User-Agent' not in header:
        header['User-Agent'] = config.get_default('user_agent')
    mime_type = s(mimetype_from_file(localfile))

    # update the request header content-type
    boundary = __make_boundary()
    header['Content-Type'] = 'multipart/form-data; boundary={0}'.format(
        boundary)

    # form fields
    fields = dict()
    fields['FileName'] = key
    fields['Authorization'] = authorization
    with open(localfile, 'rb') as stream:
        postdata = __make_postbody(
            boundary, fields, stream, mime_type, localfile)

    # update the request header content-length
    header['Content-Length'] = str(len(postdata))

    # post url

    # start post file
    logger.info('start post file {0} as {1}'.format(
        localfile, key))
    logger.info('post url is {0}'.format(url))

    return _post_file(url, header, postdata)


def __make_boundary():
    """
    生成post内容主体的限定字符串

    :return:: string类型
    """
    t = time.time()
    m = hashlib.md5()
    m.update(b(str(t)))
    return m.hexdigest()


def __make_postbody(boundary, fields, stream, mime_type, localfile):
    """
    生成post请求内容主体

    :param boundary: string类型，post内容主体的限定字符串
    :param fields: ditc类型，键值对类型分别为string类型
    :param stream: 可读的file-like object(file object 或者BytesIO)
    :param mime_type: string类型，上传文件或数据的MIME类型
    :param localfile: string类型，上传文件或数据的本地名称
    :return: 二进制数据流
    """

    binarystream = b''
    for (key, value) in fields.items():
        binarystream += b('--{0}\r\n'.format(boundary))
        binarystream += b(
            'Content-Disposition: form-data; name="{0}"\r\n'.format(key))
        binarystream += b('\r\n')
        binarystream += b('{0}\r\n'.format(value))

    binarystream += b('--{0}\r\n'.format(boundary))
    binarystream += b(
        'Content-Disposition: form-data; name="file"; filename="{0}"\r\n'.format(localfile))
    binarystream += b('Content-Type: {0}\r\n'.format(mime_type))
    binarystream += b('\r\n')

    binarystream += stream.read()
    binarystream += b('\r\n')
    binarystream += b('--{0}\r\n'.format(boundary))

    return binarystream
