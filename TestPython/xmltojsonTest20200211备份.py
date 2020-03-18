#  -*- coding:utf-8 -*-
import os
import xml.etree.ElementTree as ET
import logging
from ctypes import *
import time
import shutil
import sys
import json
sys.path.append(os.getcwd()+'\\Python3')
sys.path.append(os.getcwd()+'\\Python3\\ReturnConfig')
from ReturnConfig.GetSlidingAndDoorConfig import LoadXML2Bom
import win32api
import redis
pool = redis.ConnectionPool(host='127.0.0.1',port=6379)    #'129.204.134.85'
r = redis.Redis(connection_pool=pool)

logging.basicConfig(level="INFO")
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


base_dir = os.getcwd()
DLLPATH = base_dir +'\\QdLibdb.dll'

#配置dll函数
readord = cdll.LoadLibrary(DLLPATH)
DB_Open =readord.DB_Open
DB_Close = readord.DB_Close
DB_Get =readord.DB_Get
DB_Put = readord.DB_Put
DB_GetFile =readord.DB_GetFile
DB_PutFile = readord.DB_PutFile
DB_Move =readord.DB_Move
DB_Del = readord.DB_Del
DB_DelKey = readord.DB_DelKey
DB_GetData =readord.DB_GetData
DB_PutData =readord.DB_PutData

mBufLen=c_int(1024000)
dlen = c_int(1024000)
DB_SET = 27

QdUpTemplatePath = base_dir+'\\QDLocalBomApi.dll'
print (QdUpTemplatePath)
QdUp = windll.LoadLibrary(QdUpTemplatePath)
s = QdUp.InitData(c_char_p('data'.encode('gbk')),c_char_p('http://129.204.134.85/Qdbom'.encode('gbk')))
if s==0:
    log.error('初始化失败')
    exit(1)
else:
    log.info('初始化成功')
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

def CallGetXmlDes(configjson, mScendXML, outDespath):

    configjson = configjson.decode('utf8').encode('gbk')
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
        string = ET.tostring(scenedict[DBID], encoding='utf-8', short_empty_elements=False)
        ourpath = os.path.join(outdir, DBID)

        #ET.ElementTree(node).write(ourpath, encoding='utf-8')'<?xml version="1.0" encoding="utf-8"?>'+'\n'+
        with open(ourpath,'w+', encoding='utf8') as f:
            f.write(string.decode('utf8'))
        # log.debug('pKey='+ string.decode('utf8'))
        log.info('DBID=' + DBID)

        version = r.get('data' + 'Verison')
        if not version:
            r.set('data' + 'Verison', '0.01')
            version = '0.01'
        myversion = 'data' + version.decode('utf8')
        if flag == 1:
            configdata = LoadXML2Bom(ourpath, myversion, "D:\\nginx-1.0.11\\nginx-1.0.11\html\data")
            outconfigpath = os.path.join(outdir, 'configdata_' + DBID)
            with open(outconfigpath, 'w+', encoding='utf8') as f:
                f.write(configdata.decode('utf8'))
            outDespath = os.path.join(outdir, 'outDesdata_' + DBID)
            CallGetXmlDes(configdata, string.decode('utf8'), outDespath)
        elif flag ==2:
            outbomdatapath = os.path.join(outdir, 'outBomdata_' + DBID)
            CallXml2JsonBom(string.decode('utf8'), outbomdatapath)
        else:
            configdata = LoadXML2Bom(ourpath, "D:\\nginx-1.0.11\\nginx-1.0.11\html\data")
            outconfigpath = os.path.join(outdir, 'configdata_' + DBID)
            with open(outconfigpath, 'w+', encoding='utf8') as f:
                f.write(json.dumps(configdata, ensure_ascii=False))

            outDespath = os.path.join(outdir, 'outDesdata_' + DBID)
            CallGetXmlDes(configdata, string.decode('utf8'), outDespath)
            outbomdatapath = os.path.join(outdir, 'outBomdata_' + DBID)
            CallXml2JsonBom(string.decode('utf8'), outbomdatapath)
    configdata = ''
    ProDBIDList.clear()
    scenedict.clear()
    pKey.clear()
    AllOrdInfo.clear()
    SceneInfo.clear()
    ProInfo.clear()
def mycopyfile(srcfile,dstfile):
    #print srcfile
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

    filenum = 0
    path = 'D:\\HGSoftware\\009_华广定制一体化设计软件_在线版本\Python\\xmls\\123\\A051255D8BBB3758EB19376711116483'
    # path = 'extradata.xml'
    OrdFileDir =  base_dir+'\\Python3\\TestPython\\ord\\'



    log.debug('OrdFileDir=' + OrdFileDir)
    log_dir = "log"  # 日志存放文件夹名称
    log_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), log_dir)
    if not os.path.isdir(log_path):
        os.makedirs(log_path)
    # logger = logging.getLogger()
    # logger.setLevel(logging.ERROR)
    outputlog()
    import psutil
    for dirpath, dirnames, filenames in os.walk(OrdFileDir):
        for filename in filenames:
            if GetFileExt(filename) != '.ord': continue
            log.info('OrdFilePath=' + dirpath + '\\' + filename)
            OrdFilePath = dirpath + '\\' + filename
            now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
            log.info('Cal 开始时间='+now)
            try:
                info = psutil.virtual_memory()

                log.info('内存使用前:'+str(psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024)+'M')

                TestOrdToXmlString(dirpath + '\\' + filename)
                dstfile = os.path.join(os.path.dirname(os.path.dirname(dirpath)),'finish', filename)
                log.debug(dstfile)
                mycopyfile(OrdFilePath, dstfile)
                os.remove(OrdFilePath)
                log.debug('success'+filename)
                filenum = filenum + 1
                log.info('Has Cal File: ' + str(filenum))
                log.info('内存使用后:' + str(psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024)+'M')
                over = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
                log.info('Cal 结束时间=' + over)
                log.info('耗时=' + over)
            except Exception as e:
                log.error(e.value)
                dstfile = os.path.join(os.path.dirname(os.path.dirname(dirpath)),'error', filename)
                mycopyfile(OrdFilePath, dstfile)
                os.system("pause")

    os.system("pause")
    QdUp.UnInitData()
    #win32api.FreeLibrary(readord._handle)
    #win32api.FreeLibrary(QdUp._handle)