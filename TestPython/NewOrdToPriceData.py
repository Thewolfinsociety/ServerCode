#  -*- coding:utf-8 -*-
#  -*- coding:utf-8 -*-
'''
自动化测试报价需要的数据服务
功能：
vesion 0.0.1
2020/02/12
author:litao
'''
import os
import xml.etree.ElementTree as ET
import logging
from ctypes import *
import time
import shutil
import sys
import json
import win32api
import requests
from datetime import datetime
logging.basicConfig(level="INFO")
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
base_dir = os.getcwd()
flag = int(sys.argv[1])
print ('flag',flag)

def ReAllocBuf(n):
    log.debug('n.value='+str(n.value))
    t = n.value // 1024000
    if t <= 0 : t = 1
    else: t = t + 1
    log.debug('t='+str(t))
    mBufLen = c_int(1024*1000 * t)
    return mBufLen

def ReturnDict(mDB, pKey):
    s = {}
    for i in range(0,len(pKey)):
        result = -1
        mBufLen = c_int(1024000)
        dlen = mBufLen
        p = create_string_buffer(dlen.value)
        result = readord.DB_GetData(mDB,c_char_p(pKey[i].encode('gbk')),pointer(p),pointer(dlen),DB_SET)
        if dlen.value >= mBufLen.value:
            dlen = ReAllocBuf(dlen)
            p = create_string_buffer(dlen.value)
            result = readord.DB_Get(mDB,c_char_p(pKey[i].encode('gbk')),pointer(p),dlen,DB_SET)
        if result == 0:
            m=(p.value).decode('gbk')
            s[pKey[i]]=m
        p = None
    return s

def CallGetXmlDes(config, mScendXML, outDespath):

    configjson = json.dumps(config, ensure_ascii=False).encode('gbk')
    mScendXML = mScendXML.encode('gbk')
    result = QdUp.GetXmlDes(c_char_p(mScendXML), c_char_p(configjson))
    desjsonStr = c_char_p(result).value
    #_logging.debug( 'desjson='+ desjsonStr)
    with open(outDespath, 'w+',encoding='utf8') as f:
        f.write(desjsonStr.decode('gbk'))
    desjson = json.loads(desjsonStr.decode('gbk'))
    log.info('slidingdeslist='+str(len(desjson['slidingdeslist']))) #'趟门类别列表'
    log.info('doordeslist='+str(len(desjson['doordeslist'])))   #'掩门类别列表'
    log.info('bomdeslist='+str(len(desjson['bomdeslist'])))   #'板件类别列表'
    # except Exception as e:
    #     print (e)

def CallXml2JsonBom(mScendXML, outBompath):
    mScendXML = mScendXML.encode('gbk')
    config = {
        'gtconfig':{
                'username': '学习',
                'ordername': '123',
                'distributor': '',
                'address': '',
                'phone': '',
                'fax': '',
                'memo': '',
                'customername': '',
                'cutomercellphone': '',
                'customerphone': '',
                'customeraddress': '',
                'dt': '',
                'qdsoft_id': 'data',
                'UrlIp': 'http://129.204.134.85:8002/Qdbom'
        }
    }
    configjson = json.dumps(config, ensure_ascii=False).encode('gbk')
    print(configjson)
    result = QdUp.Xml2JsonBom(c_char_p(mScendXML), c_char_p(configjson))
    bomjson = c_char_p(result).value
    #print (bomjson)
    with open(outBompath, 'w+',encoding='utf8') as f:
        f.write(bomjson.decode('gbk'))
    bomobj = json.loads(bomjson.decode('gbk'))
    log.info('bomlist=' + str(len(bomobj['bomlist'])))
    log.info('mProductlist=' + str(len(bomobj['mProductList'])))
    log.info('basewjlist=' + str(len(bomobj['basewjlist'])))

def TestOrdToXmlString(ordfile):
    log.debug('ordfile=' + ordfile)
    ordfilepath = os.path.dirname(ordfile)
    log.debug('ordfilepath=' + ordfilepath)
    ordfilename = os.path.basename(ordfile)
    ordname = ordfilename[:ordfilename.find('.')]
    log.debug('ordname=' + ordname)
    outdir = os.path.join(ordfilepath, ordname)
    log.debug('outdir=' + outdir)
    mDB = DB_Open(c_char_p(ordfile.encode('gbk')), 1)
    pKey = ['#order']  # ['#order']
    AllOrdInfo = ReturnDict(mDB, pKey)
    if ('#order' not in AllOrdInfo): #or ('#order_scene0' not in AllOrdInfo):
        log.error('Cal error')
        DB_Close(mDB)
        return ''
    log.debug(AllOrdInfo['#order'])
    root = ET.fromstring(AllOrdInfo['#order'])

    for i in range(0, len(root)):
        scenenode = root[i]
        if scenenode.tag == '场景':
            scenedbid = root.get('DBID', '#order_scene0')
    pKey = [scenedbid]
    log.debug('pKey=' + scenedbid)
    SceneInfo = ReturnDict(mDB, pKey)

    if (scenedbid not in SceneInfo):  # or ('#order_scene0' not in AllOrdInfo):
        DB_Close(mDB)
        log.error('Cal error')
        return ''
    sceneroot = ET.fromstring(SceneInfo[scenedbid])
    ProDBIDList = []
    scenedict = {}
    for j in range(0, len(sceneroot)):
        node = sceneroot[j]
        if node.tag != '产品': continue
        DBID = node.get('DBID', '')
        ProDBIDList.append(DBID)
        scenedict[DBID] = node

    ProInfo = ReturnDict(mDB, ProDBIDList)
    DB_Close(mDB)

    if not os.path.exists(outdir):
        os.makedirs(outdir)
    for DBID in ProDBIDList:
        pronode = ET.fromstring(ProInfo[DBID])
        scenedict[DBID].append(pronode)
        string = ET.tostring(scenedict[DBID], encoding='utf-8', short_empty_elements=False) #ord 拆分的xml
        ourpath = os.path.join(outdir, DBID)
        #ET.ElementTree(node).write(ourpath, encoding='utf-8')'<?xml version="1.0" encoding="utf-8"?>'+'\n'+
        with open(ourpath,'w+', encoding='utf8') as f:
            f.write(string.decode('utf8'))
        # log.debug('pKey='+ string.decode('utf8'))
        log.info('DBID=' + DBID)

        d = {'xml':string, 'rootname':factoryid}      #string: xml, rootname 为工厂id
        response = requests.post(tyconfigurl, data=d)  #获取趟门、掩门配置数据
        dataobj = json.loads(response.content)
        configjson = response.content.decode('utf8').encode('gbk')
        if dataobj['result'] == 1:
            #print (dataobj)
            outTYAndDesdatapath = os.path.join(outdir, 'outTYAndDesdata_' + DBID)
            mSceneXML = string.decode('utf8').encode('gbk')
            result = QdUp.GetXmlDes(c_char_p(mSceneXML), c_char_p(configjson))
            #xml - mScenexml, 趟门掩门配置数据，计算出趟门掩门数据，类别字段列表
            TYAndDesdatajson = c_char_p(result).value
            with open(outTYAndDesdatapath, 'w+', encoding='utf8') as f:
                f.write(TYAndDesdatajson.decode('gbk'))
            TYAndDesdata = json.loads(TYAndDesdatajson.decode('gbk'))
            d = {'deslist': json.dumps(TYAndDesdata['bomdeslist'],ensure_ascii=False), 'factorypath': 'data'}
            response = requests.post(desurl, data=d)
            desconfig = response.content.decode('utf8').encode('gbk')
            #根据 类别字段列表获取 物料配置数据
            outDesConfigpath = os.path.join(outdir, 'outDesConfigdata_' + DBID)
            with open(outDesConfigpath, 'w+', encoding='utf8') as f:
                f.write(desconfig.decode('gbk'))
            #根据类别字段, 获取物料配置数据
            bomobj = json.loads(desconfig.decode('gbk'))
            d = {'factorypath': factoryid}
            response = requests.post(globalurl, data = d)
            gData = json.loads(response.content)
            #获取全局数据
            bomconfig = {
                'gtconfig': {
                    'username': '学习',
                    'ordername': '123',
                    'distributor': '',
                    'address': '',
                    'phone': '',
                    'fax': '',
                    'memo': '',
                    'customername': '',
                    'cutomercellphone': '',
                    'customerphone': '',
                    'customeraddress': '',
                    'dt': '',
                    'seqinfo': gData['seqinfo'],
                    'classseqinfo': gData['classseqinfo'],
                    'workflow': gData['workflow'],
                    'ErpItem': gData['ErpItem'],
                    'boardmat': gData['boardmat'],
                    'HoleWjFContent': gData['HoleWjFContent'],
                    'desdata': bomobj,
                }
            }
            #配置好计算物料数据
            bomConfigString = json.dumps(bomconfig, ensure_ascii=False).encode('gbk')
            outBompath = os.path.join(outdir, 'outbomConfig_' + DBID)
            with open(outBompath, 'w+', encoding='utf8') as f:
                f.write(bomConfigString.decode('gbk'))
            result = QdUp.Xml2JsonBom(c_char_p(mSceneXML), c_char_p(bomConfigString))
            bomjson = c_char_p(result).value    #得到计算好的物料数据
            outBompath = os.path.join(outdir, 'outBomdata_' + DBID)
            with open(outBompath, 'w+', encoding='utf8') as f:
                f.write(bomjson.decode('gbk'))

            d = {'name': json.dumps(TYAndDesdata['bomdeslist'],ensure_ascii=False),
                 'slidingDoor': json.dumps(TYAndDesdata['slidingdeslist'],ensure_ascii=False),
                 'swingDoor': json.dumps(TYAndDesdata['doordeslist'],ensure_ascii=False),
                 'rootname': factoryid}
            response = requests.post(priceconfigurl, data=d)
            ouPriceConfigpath = os.path.join(outdir, 'outPriceConfigdata_' + DBID)
            with open(ouPriceConfigpath, 'w+', encoding='utf8') as f:
                f.write(response.content.decode('utf8'))
            # bomobj = json.loads(bomjson.decode('gbk'))
            # print('bomlist=' + str(len(bomobj['bomlist'])))
            # print('mProductlist=' + str(len(bomobj['mProductList'])))
            # print('basewjlist=' + str(len(bomobj['basewjlist'])))
            # log.info('bomlist=' + str(len(bomobj['bomlist'])))
            # log.info('mProductlist=' + str(len(bomobj['mProductList'])))
            # log.info('basewjlist=' + str(len(bomobj['basewjlist'])))

    ProDBIDList.clear()
    scenedict.clear()
    pKey.clear()
    AllOrdInfo.clear()
    SceneInfo.clear()
    ProInfo.clear()

def mycopyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
        return 0
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        return 1

def GetFileExt(filename):
    '''

    :param filename: '123.txt'
    :param filename2: '' or '.db'
    :return: '123' or '123.db'
    '''

    return filename[filename.find('.'):]

def GetPath(filename):
    return filename[filename.find('.'):]

def outputlog():
    main_log_handler = logging.FileHandler(log_path +
                                           "/DealZip_%s.log" % time.strftime("%Y-%m-%d_%H-%M-%S",
                                                                        time.localtime(time.time())), mode="w+",
                                           encoding="utf-8")
    main_log_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    main_log_handler.setFormatter(formatter)
    log.addHandler(main_log_handler)

    # # 控制台打印输出日志
    # console = logging.StreamHandler()  # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象
    # console.setLevel(logging.INFO)  # 设置要打印日志的等级，低于这一等级，不会打印
    # formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
    # console.setFormatter(formatter)
    # logging.getLogger('').addHandler(console)

if __name__ == '__main__':
    flag = int(sys.argv[1])
    factoryid = sys.argv[2]
    print('flag=',flag,'factory=',factoryid)
    if flag ==1 :
        # OrdFilesUrl = 'http://127.0.0.1:8004/TestPrice/ReadOrdPath/'
        # XmlToJsonUrl = 'http://127.0.0.1:8004/TestPrice/XmlToJson/'
        # OrdToXmlUrl = 'http://127.0.0.1:8004/TestPrice/OrdToXml/'
        OrdFilesUrl = 'http://127.0.0.1/TestPrice/ReadOrdPath/'
        XmlToJsonUrl = 'http://127.0.0.1/TestPrice/XmlToJson/'
        OrdToXmlUrl = 'http://127.0.0.1/TestPrice/OrdToXml/'
    else:
        OrdFilesUrl = 'http://qdsoft.huaguangsoft.com/TestPrice/ReadOrdPath/'
        XmlToJsonUrl = 'http://qdsoft.huaguangsoft.com/TestPrice/XmlToJson/'
        OrdToXmlUrl = 'http://qdsoft.huaguangsoft.com/TestPrice/OrdToXml/'
    filenum = 0
    log_dir = "log"  # 日志存放文件夹名称
    log_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), log_dir)
    if not os.path.isdir(log_path):
        os.makedirs(log_path)
    outputlog()
    response = requests.get(OrdFilesUrl)  # 获取趟门、掩门配置数据
    ordDict = json.loads(response.content)
    ordlist = ordDict['files']
    print('len of ordlist=',len(ordlist))
    ordnum = 0
    for ordfile in ordlist:
        start = datetime.now()
        d = {'filename':ordfile, 'factoryid':factoryid}
        log.info(ordfile)
        response = requests.post(OrdToXmlUrl, data =d)  # ord to xml
        ReturnDict = json.loads(response.content)
        endtoxml = datetime.now()
        log.info('Toxml耗时=' + str((endtoxml-start).seconds)+'s')
        if ReturnDict['result'] ==1:
            response = requests.post(XmlToJsonUrl, data=d)  # xml to data
            ReturnDict = json.loads(response.content)
            if ReturnDict['result'] == 1:
                log.info('To JSON Success!!!')
                endtojson = datetime.now()
                log.info('xmlTojson耗时=' + str((endtojson - endtoxml).seconds) + 's')
                ordnum = ordnum + 1
    log.info('总共ordfiles=%d'%len(ordlist))
    log.info('计算成功ordfiles=%d'%ordnum)
