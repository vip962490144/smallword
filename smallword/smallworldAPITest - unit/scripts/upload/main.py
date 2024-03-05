#!/usr/bin/python3

import requests
import json

from scripts.logins import login_base
from scripts.upload.ufile.postfile import postfile

obj = login_base.LoginBase()

A = '{"mobile": "17621620970", "password": "123456"}'
login_actual = obj.login(A)
token = login_actual.json()["token"]

# token = '03631177d39da21b0652044b429294e3156ce9f7'
endpoint = 'http://106.75.11.161:9082'
appVersion = '2.9.8'
width = 100
height = 100
# localfile = r'D:\files\items\automation\upload\upload\test.png'
# localfile = r'D:\test.mp4'
localfile = r'D:\1.png'

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+token,
    'App-Version': appVersion
}

# createUcloudUpload
createUcloudUploadUrl = endpoint+'/file'
createUcloudUploadPayload = {
    'type': 1,
    'width': width,
    'height': height,
    'mime_type': 'image/png'
}
# createUcloudUploadPayload = {
#     'type': 2,
#     'width': width,
#     'height': height,
#     'mime_type': 'video/mp4'
# }
createUcloudUploadResp = requests.post(
    createUcloudUploadUrl, headers=headers, data=json.dumps(createUcloudUploadPayload))
createUcloudUploadRespJson = createUcloudUploadResp.json()
print(createUcloudUploadRespJson)

# doUploadUcloud
ret, resp = postfile(createUcloudUploadRespJson['file_url'], createUcloudUploadRespJson['signature'],
                     createUcloudUploadRespJson['file_id'], localfile)
print(resp)
