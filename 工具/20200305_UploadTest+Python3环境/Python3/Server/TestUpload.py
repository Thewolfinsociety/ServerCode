import requests
import json
import os
#url = 'http://127.0.0.1:8001/Ftp/UploadFile/'
url = 'http://saming.iok.la:23655/hgerp_base/url/cloudOrder_uploadCloudOrder.action'
name = "9000.txt"
path = os.getcwd() + '\\Python3\\Server\\'+name
files = {'upload':open(path, "rb")}
data = {
    'idCode':"HTTPURLOPERATE2015",
    'distributorCode':"001",
    'uploadFileName':name,
    'logName':'xzy01',

}
content = requests.post(url, data, files=files)
print (content.text)
jsonobj = json.loads(content.text)
print(jsonobj['result'])
if jsonobj['result'] == '0':
    print(66666666)