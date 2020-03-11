#  -*- coding:utf-8 -*-
'''
服务器版
功能：
vesion 1.0.1
2019/11/19
author:litao
'''
#version information XmlToJson Add Netconfig
import sys
import os
import re
from ctypes import *
import json
import tornado.ioloop, _thread,threading,queue,time
from tornado.options import define,options, parse_command_line
import tornado.httpserver
from tornado.web import RequestHandler
import uuid
from tornado import gen
from tornado.concurrent import Future
import zipfile
import hashlib
import base64
import socket,sys ,json,time,os             # 导入 socket 模块
import shutil
import ctypes
import inspect,pypyodbc,urllib.request,urllib.parse,urllib.error
import configparser
import sqlite3
import demjson
import logging
from logging import handlers
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from bsddb3 import db
from celery.result import AsyncResult
import redis
import tasks
from tornado import httpclient

from PythontoBomJson.Websimplify_xml_utf8 import functionordtoxml
from PythontoBomJson.Websimplify_xml_utf8 import getorderinfor

from ReturnConfig.GetSlidingAndDoorConfig import LoadXML2Bom
sys.path.append(os.getcwd()+'\\Python3\\NetPriceConfig')
from NetPriceConfig import NetworkQuoteConfigData

pool = redis.ConnectionPool(host='127.0.0.1',port=6379)    #'129.204.134.85'
r = redis.Redis(connection_pool=pool)

port = int(sys.argv[1])	#端口号
webpath = sys.argv[2]	#设计软件绝对路径D:\Python设计软件环境
webpath = webpath
DataPath = webpath + '\\data\\'
CFGPath=webpath+'\\data\\'+'qddata\\'
DBfile = webpath + '\\data\\XScriptDb.db'
'''
路径
'''
TempPath = os.path.abspath(os.path.join(os.getcwd()))+'\\Temp'
PythonPath = os.path.abspath(os.path.join(os.getcwd()))+'\\Python'
define("port", default=port, help="run on the given port", type=int)
path_file = os.path.join(webpath, 'index.html')  	# 取文件路径'
if os.path.isfile(path_file):					# 查看文件是否存在
    rootCata= Path+'index.html'
else:
    rootCata = False
string = {} #xml标识符
queuePath=webpath+'\\python\\'+'queue\\'  #utf8,unicode
base_dir = os.path.abspath(os.path.join(os.getcwd()))
ServerPath = os.path.abspath(os.path.join(os.getcwd(),'..'))+'\\nginx-1.0.11\\nginx-1.0.11\html\\'
LocalPath = 'C:\\Users\\Administrator\\Downloads\\nginx-1.0.11\\nginx-1.0.11\\html\\'
class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射
    def __init__(self,filename,level='info',when='H',backCount=3,fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):

        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount)#往文件里写入#指定间隔时间自动生成文件的处理器
        #fh = logging.FileHandler(filename=filename, encoding="utf-8")
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.suffix = "%Y%m%d%H.log"  # 设置 切分后日志文件名的时间格式 默认 filename+"." + suffix 如果需要更改需要改logging 源码
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)

if not os.path.exists(base_dir+"\\Python3\\Log"):
    os.makedirs(base_dir+"\\Python3\\Log")
log = Logger(base_dir+"\\Python3\\Log\\all"+"_%s.log" % time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime(time.time())), level='info')
sys.path.append(webpath+'\\Python3\\PythontoBomJson')

def returnresdata(recemessage):
    try:
        status = True
        content = r.get(recemessage)
        if not content:
            return False, ''
        result = json.loads(content)
    except Exception as e:
        status = False
        result = ''
        content = ''
        print(e)

    return status, result

def nowtime():
    return time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime(time.time()))
#改变文件名后缀
def ChangeFileExt(filename,filename2):
    '''
    :param filename: '123.txt'
    :param filename2: '' or '.db'
    :return: '123' or '123.db'
    '''
    return filename[0:filename.index('.')]+filename2
#压缩路径接口
def zip_ya(startdir, file_new):
    file_news = startdir + '.zip'  # 压缩后文件夹的名字
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''  # 实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
    z.close()
#压缩文件接口
def zip_files(files, zip_name):
    zip = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_STORED)
    for file in files:
        print(('compressing', file))
        print(file)  # basename///dirname
        if not os.path.exists(file):
            print('file not exist')
            return 0
        filefullpath = os.path.join(file)
        print(('filefullpath=',filefullpath))
        zip.write(filefullpath, os.path.basename(file))
        os.remove(file)   #打包完就删除生成的单个柜子zip
    zip.close()
    print ('compressing finished')
    return 1

class BaseHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers",
                        "x-requested-with,access_token")  # 这里要填写上请求带过来的Access-Control-Allow-Headers参数，如access_token就是我请求带过来的参数
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE")  # 请求允许的方法
        self.set_header("Access-Control-Max-Age", "3600")  # 用来指定本次预检请求的有效期，单位为秒，，在此期间不用发出另一条预检请求。

    # 定义一个响应OPTIONS 请求，不用作任务处理
    def options(self):
        pass
# 获取静态文件
class IndexHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, webpath):
        self.set_header("Cache-control", "no-cache")
# 退出程序操作
class ExitSystem(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        try:
            pass
        except:
            pass
        finally:
            print("***服务器退出***")
            os._exit(0)  # 退出程序

class XmlToJson(BaseHandler):
    def post(self):
        global RootPath
        guid = str(uuid.uuid1())  # 唯一标识符guid
        guid = ''.join(guid.split('-'))
        log.logger.debug('guid=' + guid)
        Result = {'result': 0}
        xml = self.get_argument('xml').encode('utf-8')
        RootName = self.get_argument('rootname', None)
        if RootName:
            RootPath = ServerPath + RootName.encode('gbk')
            print('RootPath=' + RootPath)
            if not os.path.exists(RootPath):
                Result['result'] = -1
                self.write(json.dumps(Result, ensure_ascii=False).encode('utf8'))
                return
        else:
            RootPath = base_dir
        #defineRootPath(RootPath)
            log.logger.debug('RootPath=' + RootPath)
        if not os.path.exists(RootPath + '\\Python\\Webcache\\'):
            os.makedirs(RootPath + '\\Python\\Webcache\\')
        m2 = hashlib.md5()
        m2.update(xml)
        pricedatamd5 = m2.hexdigest()
        log.logger.debug('pricedatamd5=' + pricedatamd5)
        # if os.path.exists(RootPath + '\\Python\\Webcache\\'+pricedatamd5):
        #     with open(RootPath + '\\Python\\Webcache\\'+pricedatamd5,'r') as f:
        #         Bomjson = f.read()
        #         self.write(Bomjson)
        # else:
        UpLoadXmlPath = RootPath + '\\Python\\UpLoadXml\\'
        if(not os.path.exists(UpLoadXmlPath)):
            os.makedirs(UpLoadXmlPath)
        with open(UpLoadXmlPath + guid, 'w+') as f:
            f.write(xml)
            #本地测试版
        #     Bomjson = XmltoJson(UpLoadXmlPath + guid, NetworkQuoteConfigData.GetNetworkQuoteConfigHandl, RootPath)
        # #PriceJsonPath = base_dir + u'\\Python\\PythontoBomJson\\PriceJson\\'
        #     if not os.path.exists(RootPath + '\\Python\\Webcache\\'):
        #         os.makedirs(RootPath + '\\Python\\Webcache\\')
        #     with open(RootPath + '\\Python\\Webcache\\' + pricedatamd5, 'w+') as f:
        #         f.write(Bomjson)
        #     self.write(Bomjson)
        #     os.remove(UpLoadXmlPath + guid)
            #-------------服务版本
        try:
            Bomjson = XmltoJson(UpLoadXmlPath + guid, NetworkQuoteConfigData.GetNetworkQuoteConfigHandl, RootPath)
            #PriceJsonPath = base_dir + u'\\Python\\PythontoBomJson\\PriceJson\\'
            if not os.path.exists(RootPath + '\\Python\\Webcache\\'):
                os.makedirs(RootPath + '\\Python\\Webcache\\')
            with open(RootPath + '\\Python\\Webcache\\' + pricedatamd5, 'w+') as f:
                f.write(Bomjson)
            self.write(Bomjson)
            os.remove(UpLoadXmlPath + guid)
        except Exception as e:
             log.logger.error(('guid='+str(guid)+',  CalFail!')+str(e))

             self.write(json.dumps(Result,ensure_ascii=False).encode('utf8'))
        # UpLoadXmlPath = base_dir + '\\Python\\UpLoadXml\\'
        # file_metas = self.request.files.get('file', None)  # 提取表单中‘name’为‘file’的文件元数据
        # if not file_metas:
        #     ret['result'] = 'Invalid Args'
        #     log.logger.debug((u'参数错误').encode('gbk'))
        #     self.write('参数错误')
        # else:
        #     print len(file_metas)
        #     for meta in file_metas:
        #         guid = str(uuid.uuid1())  # 唯一标识符guid
        #         guid = ''.join(guid.split('-'))
        #         print 'guid=',guid
        #         log.logger.debug(('filename=' + meta['filename']).encode('gbk'))
        #         file_path = os.path.join(UpLoadXmlPath, guid)
        #         with open(file_path, 'wb') as up:
        #             up.write(meta['body'])
        #         try:
        #             PriceJsonPath = base_dir + u'\\Python\\PythontoBomJson\\PriceJson\\'
        #             if not os.path.exists(PriceJsonPath):
        #                 os.makedirs(PriceJsonPath)
        #             Bomjson = XmltoJson(UpLoadXmlPath + guid)
        #             with open(PriceJsonPath + guid + '.txt', 'w+') as f:
        #                 f.write(Bomjson)
        #             self.write(Bomjson)
        #         except:
        #             log.logger.debug(('filename=' + meta['filename']+',guid='+str(guid)+',  CalFail!').encode('gbk'))
        #             self.write(json.dumps(Result,ensure_ascii=False).encode('utf8'))


class Executor(ThreadPoolExecutor):
    """ 创建多线程的线程池，线程池的大小为10
    创建多线程时使用了单例模式，如果Executor的_instance实例已经被创建，
    则不再创建，单例模式的好处在此不做讲解
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not getattr(cls, '_instance', None):
            cls._instance = ThreadPoolExecutor(max_workers=10)
        return cls._instance

def irecords(curs):
    record = curs.first()
    while record:
        yield record
        record = curs.next()
def Number(string):
    try:
        return float(string)
    except:
        return 0

def GetTrueFalse(string):
    if(string == 'TRUE' or string == 'True'or string == True or string == 1):
        return True
    else:
        return False

def adb_DoorInitData(adb, rootname, Path):
    RootPath = Path
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\五金配件.cfg', 'r') as f:
            mAccessoryListcontent = f.read()
        if mAccessoryListcontent == '':
            mAccessoryListcontent = json.dumps([])
    except:
        mAccessoryListcontent = json.dumps([])
        log.error('ini=' + RootPath + '\\data\\XDiyDoors.ini')
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\颜色.cfg', 'r') as f:
            mColorListcontent = f.read()
        if mColorListcontent == '':
            mColorListcontent = json.dumps([])
    except:
        mColorListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\颜色分类.cfg', 'r') as f:
            mColorClassListcontent = f.read()
        if mColorClassListcontent == '':
            mColorClassListcontent = json.dumps([])
    except:
        mColorClassListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\颜色分类2.cfg', 'r') as f:
            mColorClass2Listcontent = f.read()
        if mColorClass2Listcontent == '':
            mColorClass2Listcontent = json.dumps([])
    except:
        mColorClass2Listcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\门类型.cfg', 'r') as f:
            mTypeListcontent = f.read()
        if mTypeListcontent == '':
            mTypeListcontent = json.dumps([])
    except:
        mTypeListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\单门数量类型.cfg', 'r') as f:
            mExpListcontent = f.read()
        if mExpListcontent == '':
            mExpListcontent = json.dumps([])
    except:
        mExpListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\拉手.cfg', 'r') as f:
            mHandleListcontent = f.read()
        if mHandleListcontent == '':
            mHandleListcontent = json.dumps([])
    except:
        mHandleListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\中横框参数.cfg', 'r') as f:
            mDoorHBoxParamListcontent = f.read()
        if mDoorHBoxParamListcontent == '':
            mDoorHBoxParamListcontent = json.dumps([])
    except:
        mDoorHBoxParamListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\门铰分类.cfg', 'r') as f:
            mHingeListcontent = f.read()
        if mHingeListcontent == '':
            mHingeListcontent = json.dumps([])
    except:
        mHingeListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\门铰.cfg', 'r') as f:
            mCurHingeListcontent = f.read()
        if mCurHingeListcontent == '':
            mCurHingeListcontent = json.dumps([])
    except:
        mCurHingeListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\门芯附加物料.cfg', 'r') as f:
            mDoorPanelBomDetailListcontent = f.read()
        if mDoorPanelBomDetailListcontent == '':
            mDoorPanelBomDetailListcontent = json.dumps([])
    except:
        mDoorPanelBomDetailListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\门芯类型.cfg', 'r') as f:
            mDoorPanelTypeListcontent = f.read()
        if mDoorPanelTypeListcontent == '':
            mDoorPanelTypeListcontent = json.dumps([])
    except:
        mDoorPanelTypeListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\掩门参数.cfg', 'r') as f:
            mParamListcontent = f.read()
        if mParamListcontent == '':
            mParamListcontent = json.dumps([])
    except:
        mParamListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\报价.cfg', 'r') as f:
            mPriceListcontent = f.read()
        if mPriceListcontent == '':
            mPriceListcontent = json.dumps([])
    except:
        mPriceListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\报价方案.cfg', 'r') as f:
            mPriceTableListcontent = f.read()
        if mPriceTableListcontent == '':
            mPriceTableListcontent = json.dumps([])
    except:
        mPriceTableListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\百叶板配置.cfg', 'r') as f:
            mShutterExpListcontent = f.read()
        if mShutterExpListcontent == '':
            mShutterExpListcontent = json.dumps([])
    except:
        mShutterExpListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\五金配件分类.cfg', 'r') as f:
            mWJBomListcontent = f.read()
        if mWJBomListcontent == '':
            mWJBomListcontent = json.dumps([])
    except:
        mWJBomListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\五金配件分类数据.cfg', 'r') as f:
            mWJBomDetailListcontent = f.read()
        if mWJBomDetailListcontent == '':
            mWJBomDetailListcontent = json.dumps([])
    except:
        mWJBomDetailListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\XML单门结构.cfg', 'r') as f:
            mDoorXMLListcontent = f.read()
        if mDoorXMLListcontent == '':
            mDoorXMLListcontent = json.dumps([])
    except:
        mDoorXMLListcontent = json.dumps([])

    mExpList = json.loads(mExpListcontent, encoding='gbk')
    for i in range(0, len(mExpList)):
        mExpList[i]['doornum'] = Number(mExpList[i]['doornum'])
        mExpList[i]['capnum'] = Number(mExpList[i]['capnum'])
        mExpList[i]['lkvalue'] = Number(mExpList[i]['lkvalue'])
    mExpListcontent = json.dumps(mExpList).encode('gbk')

    mDoorHBoxParamList = json.loads(mDoorHBoxParamListcontent, encoding='gbk')
    for i in range(0, len(mDoorHBoxParamList)):
        mDoorHBoxParamList[i]['height'] = Number(mDoorHBoxParamList[i]['height'])
        mDoorHBoxParamList[i]['depth'] = Number(mDoorHBoxParamList[i]['depth'])
        mDoorHBoxParamList[i]['thick'] = Number(mDoorHBoxParamList[i]['thick'])
    mDoorHBoxParamListcontent = json.dumps(mDoorHBoxParamList).encode('gbk')

    mHingeList = json.loads(mHingeListcontent, encoding='gbk')
    for i in range(0, len(mHingeList)):
        mHingeList[i]['min1'] = Number(mHingeList[i]['min1'])
        mHingeList[i]['max1'] = Number(mHingeList[i]['max1'])
        mHingeList[i]['num1'] = Number(mHingeList[i]['num1'])
        mHingeList[i]['min2'] = Number(mHingeList[i]['min2'])
        mHingeList[i]['max2'] = Number(mHingeList[i]['max2'])
        mHingeList[i]['num2'] = Number(mHingeList[i]['num2'])
        mHingeList[i]['min3'] = Number(mHingeList[i]['min3'])
        mHingeList[i]['max3'] = Number(mHingeList[i]['max3'])
        mHingeList[i]['num3'] = Number(mHingeList[i]['num3'])
        mHingeList[i]['min4'] = Number(mHingeList[i]['min4'])
        mHingeList[i]['max4'] = Number(mHingeList[i]['max4'])
        mHingeList[i]['num4'] = Number(mHingeList[i]['num4'])
        mHingeList[i]['min5'] = Number(mHingeList[i]['min5'])
        mHingeList[i]['max5'] = Number(mHingeList[i]['max5'])
        mHingeList[i]['num5'] = Number(mHingeList[i]['num5'])
        mHingeList[i]['iszn'] = "0" if 'iszn' not in mHingeList[i] else mHingeList[i]['iszn']
        mHingeList[i]['bh'] = Number(mHingeList[i]['bh'])
    mHingeListcontent = json.dumps(mHingeList).encode('gbk')

    mDoorPanelBomDetailList = json.loads(mDoorPanelBomDetailListcontent, encoding='gbk')
    for i in range(0, len(mDoorPanelBomDetailList)):
        mDoorPanelBomDetailList[i]["lmin"] = Number(mDoorPanelBomDetailList[i]['lmin'])
        mDoorPanelBomDetailList[i]["lmax"] = Number(mDoorPanelBomDetailList[i]['lmax'])
        mDoorPanelBomDetailList[i]["hmin"] = Number(mDoorPanelBomDetailList[i]['hmin'])
        mDoorPanelBomDetailList[i]["hmax"] = Number(mDoorPanelBomDetailList[i]['hmax'])
        mDoorPanelBomDetailList[i]["num"] = Number(mDoorPanelBomDetailList[i]['num'])
    mDoorPanelBomDetailListcontent = json.dumps(mDoorPanelBomDetailList).encode('gbk')

    mDoorPanelTypeList = json.loads(mDoorPanelTypeListcontent, encoding='gbk')
    for i in range(0, len(mDoorPanelTypeList)):
        mDoorPanelTypeList[i]["thick"] = Number(mDoorPanelTypeList[i]['thick'])
        mDoorPanelTypeList[i]["lfb"] = Number(mDoorPanelTypeList[i]['lfb'])
        mDoorPanelTypeList[i]["hfb"] = Number(mDoorPanelTypeList[i]['hfb'])
        mDoorPanelTypeList[i]["bomtype"] = mDoorPanelTypeList[i]['bomtype']
        mDoorPanelTypeList[i]["bktype"] = mDoorPanelTypeList[i]['bktype']
        mDoorPanelTypeList[i]["lmax"] = Number(mDoorPanelTypeList[i]['lmax'])
        mDoorPanelTypeList[i]["lmin"] = Number(mDoorPanelTypeList[i]['lmin'])
        mDoorPanelTypeList[i]["wmax"] = Number(mDoorPanelTypeList[i]['wmax'])
        mDoorPanelTypeList[i]["wmin"] = Number(mDoorPanelTypeList[i]['wmin'])
        mDoorPanelTypeList[i]["is_buy"] = mDoorPanelTypeList[i]['is_buy']
        mDoorPanelTypeList[i]["direct"] = mDoorPanelTypeList[i]['direct']
        mDoorPanelTypeList[i]["fbstr"] = mDoorPanelTypeList[i]['fbstr']
        mDoorPanelTypeList[i]["pnl3d"] = mDoorPanelTypeList[i]['pnl3d']
        mDoorPanelTypeList[i]["memo"] = mDoorPanelTypeList[i]['memo']
        mDoorPanelTypeList[i]["panelbom"] = mDoorPanelTypeList[i]['panelbom']
        mDoorPanelTypeList[i]["ypos"] = Number(mDoorPanelTypeList[i]['ypos'])
        mDoorPanelTypeList[i]["iswhole"] = mDoorPanelTypeList[i]['iswhole']
    mDoorPanelTypeListcontent = json.dumps(mDoorPanelTypeList).encode('gbk')

    mParamList = json.loads(mParamListcontent, encoding='gbk')
    for i in range(0, len(mParamList)):
        mParamList[i]["DoorsType"] = mParamList[i]['doorstype']
        mParamList[i]["Handle"] = mParamList[i]['handle']
        mParamList[i]["PanelType"] = mParamList[i]['paneltype']
        mParamList[i]["cap"] = mParamList[i]['cap']
        mParamList[i]["eb_cap"] = Number(mParamList[i]['eb_cap'])
        mParamList[i]["vboxh"] = Number(mParamList[i]['vboxh'])
        mParamList[i]["udboxh"] = Number(mParamList[i]['udboxh'])
        mParamList[i]["vthick"] = mParamList[i]['vthick']
        mParamList[i]["udthick"] = Number(mParamList[i]['udthick'])
        mParamList[i]["vboxjtw"] = Number(mParamList[i]['vboxjtw'])
        mParamList[i]["udboxjtw"] = Number(
            mParamList[i]['udboxjtw'] if 'udboxjt' not in mParamList[i] else mParamList[i]['udboxjt'])
        mParamList[i]["hboxjtw"] = Number(mParamList[i]['hboxjtw'])
        mParamList[i]["iscalc_framebom"] = GetTrueFalse(mParamList[i]['iscalc_framebom'])
        mParamList[i]["frame_valuel"] = Number(mParamList[i]['frame_valuel'])
        mParamList[i]["frame_valueh"] = Number(mParamList[i]['frame_valueh'])
        mParamList[i]["udbox_hbox_value"] = Number(mParamList[i]['udbox_hbox_value'])
        mParamList[i]["is_xq"] = GetTrueFalse(mParamList[i]['is_xq'])
        mParamList[i]["cb_yyvalue"] = Number(mParamList[i]['cb_yyvalue'])
        mParamList[i]["is_buy"] = mParamList[i]['is_buy']
        mParamList[i]["noframe_bom"] = Number(mParamList[i]['noframe_bom'])
    mParamListcontent = json.dumps(mParamList).encode('gbk')

    mShutterExpList = json.loads(mShutterExpListcontent, encoding='gbk')
    for i in range(0, len(mShutterExpList)):
        mShutterExpList[i]["height"] = Number(mShutterExpList[i]["height"])
        mShutterExpList[i]["width"] = Number(mShutterExpList[i]["width"])
        mShutterExpList[i]["heightcap"] = Number(mShutterExpList[i]["heightcap"])
        mShutterExpList[i]["widthcap"] = Number(mShutterExpList[i]["widthcap"])
        mShutterExpList[i]["minheight"] = Number(mShutterExpList[i]["minheight"])
        mShutterExpList[i]["minwidth"] = Number(mShutterExpList[i]["minwidth"])
    mShutterExpListcontent = json.dumps(mShutterExpList).encode('gbk')

    mWJBomDetailList = json.loads(mWJBomDetailListcontent, encoding='gbk')
    for i in range(0, len(mWJBomDetailList)):
        mWJBomDetailList[i]["door_bh"] = Number(mWJBomDetailList[i]["door_bh"])
        mWJBomDetailList[i]["bktypeAry"] = []
        if mWJBomDetailList[i]["bktype"] != '':
            mWJBomDetailList[i]["bktypeAry"] = mWJBomDetailList[i]['bktype'].split(',')
    mWJBomDetailListcontent = json.dumps(mWJBomDetailList).encode('gbk')

    mAccessoryList = json.loads(mAccessoryListcontent, encoding='gbk')
    for i in range(0, len(mAccessoryList)):
        mAccessoryList[i]["myunit"] = mAccessoryList[i]["unit"]
    mAccessoryListcontent = json.dumps(mAccessoryList).encode('gbk')

    mTypeList = json.loads(mTypeListcontent, encoding='gbk')
    for i in range(0, len(mTypeList)):
        mTypeList[i]["isframe"] = GetTrueFalse(mTypeList[i]["isframe"])
        mTypeList[i]["covertype"] = Number(mTypeList[i]["covertype"])
        mTypeList[i]["lkvalue"] = Number(mTypeList[i]["lkvalue"])
        mTypeList[i]["ud_lkvalue"] = mTypeList[i]['lkvalue'] if "ud_lkvalue" not in mTypeList[i] else Number(
            mTypeList[i]['ud_lkvalue'])
        mTypeList[i]["depth"] = Number(mTypeList[i]["depth"])
        mTypeList[i]["eb_lkvalue"] = Number(mTypeList[i]["eb_lkvalue"])
        mTypeList[i]["eb_ud_lkvalue"] = Number(mTypeList[i]["eb_ud_lkvalue"])
    mTypeListcontent = json.dumps(mTypeList).encode('gbk')

    adb.put((rootname + 'mExpList').encode('utf8'), mExpListcontent)
    adb.put((rootname + 'mHandleList').encode('utf8'), mHandleListcontent)
    adb.put((rootname + 'mDoorHBoxParamList').encode('utf8'), mDoorHBoxParamListcontent)
    adb.put((rootname + 'mHingeList').encode('utf8'), mHingeListcontent)
    adb.put((rootname + 'mCurHingeList').encode('utf8'), mCurHingeListcontent)
    adb.put((rootname + 'mDoorPanelBomDetailList').encode('utf8'), mDoorPanelBomDetailListcontent)
    adb.put((rootname + 'mDoorPanelTypeList').encode('utf8'), mDoorPanelTypeListcontent)

    adb.put((rootname + 'mParamList').encode('utf8'), mParamListcontent)

    adb.put((rootname + 'mShutterExpList').encode('utf8'), mShutterExpListcontent)
    adb.put((rootname + 'mWJBomList').encode('utf8'), mWJBomListcontent)
    adb.put((rootname + 'mWJBomDetailList').encode('utf8'), mWJBomDetailListcontent)
    adb.put((rootname + 'mDoorXMLList').encode('utf8'), mDoorXMLListcontent)
    adb.put((rootname + 'mAccessoryList').encode('utf8'), mAccessoryListcontent)
    adb.put((rootname + 'mColorList').encode('utf8'), mColorListcontent)

    adb.put((rootname + 'mColorClassList').encode('utf8'), mColorClassListcontent)
    adb.put((rootname + 'mColorClass2List').encode('utf8'), mColorClass2Listcontent)
    adb.put((rootname + 'mTypeList').encode('utf8'), mTypeListcontent)

def adb_SlidingInitData(adb, rootname, Path):
    RootPath = Path

    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\单门数量类型.cfg', 'r') as f:
            mSlidingExpListcontent = f.read()
        if mSlidingExpListcontent == '':
            mSlidingExpListcontent = json.dumps([])
    except:
        mSlidingExpListcontent = json.dumps([])

    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\门类型.cfg', 'r') as f:
            mSlidingTypeListcontent = f.read()
        if mSlidingTypeListcontent == '':
            mSlidingTypeListcontent = json.dumps([])
    except:
        mSlidingTypeListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\趟门参数.cfg', 'r') as f:
            SlidingParamcontent = f.read()
        if SlidingParamcontent == '':
            SlidingParamcontent = json.dumps([])
    except:
        SlidingParamcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\上下横框参数.cfg', 'r') as f:
            UDBoxParamcontent = f.read()
        if UDBoxParamcontent == '':
            UDBoxParamcontent = json.dumps([])
    except:
        UDBoxParamcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\上下轨参数.cfg', 'r') as f:
            TrackParamcontent = f.read()
        if TrackParamcontent == '':
            TrackParamcontent = json.dumps([])
    except:
        TrackParamcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\中横框参数.cfg', 'r') as f:
            HBoxParamcontent = f.read()
        if HBoxParamcontent == '':
            HBoxParamcontent = json.dumps([])
    except:
        HBoxParamcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\门板类型.cfg', 'r') as f:
            PanelTypeListcontent = f.read()
        if PanelTypeListcontent == '':
            PanelTypeListcontent = json.dumps([])
    except:
        PanelTypeListcontent = json.dumps([])

    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\颜色分类2.cfg', 'r') as f:
            mSlidingColorListcontent = f.read()
        if mSlidingColorListcontent == '':
            mSlidingColorListcontent = json.dumps([])
    except:
        mSlidingColorListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\颜色分类.cfg', 'r') as f:
            mSlidingColorClassListcontent = f.read()
        if mSlidingColorClassListcontent == '':
            mSlidingColorClassListcontent = json.dumps([])
    except:
        mSlidingColorClassListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\五金配件分类数据.cfg', 'r') as f:
            mSlidingWjBomDetailListcontent = f.read()
        if mSlidingWjBomDetailListcontent == '':
            mSlidingWjBomDetailListcontent = json.dumps([])
    except:
        mSlidingWjBomDetailListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\百叶板计算公式.cfg', 'r') as f:
            mSSExpListcontent = f.read()
        if mSSExpListcontent == '':
            mSSExpListcontent = json.dumps([])
    except:
        mSSExpListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\五金配件.cfg', 'r') as f:
            mSlidingAccessoryListcontent = f.read()
        if mSlidingAccessoryListcontent == '':
            mSlidingAccessoryListcontent = json.dumps([])
    except:
        mSlidingAccessoryListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\竖框参数.cfg', 'r') as f:
            mVBoxParamListcontent = f.read()
        if mVBoxParamListcontent == '':
            mVBoxParamListcontent = json.dumps([])
    except:
        mVBoxParamListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\门板附加物料.cfg', 'r') as f:
            mPanelBomDetailListcontent = f.read()
        if mPanelBomDetailListcontent == '':
            mPanelBomDetailListcontent = json.dumps([])
    except:
        mPanelBomDetailListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\竖中横框参数.cfg', 'r') as f:
            UHBoxParamcontent = f.read()
        if UHBoxParamcontent == '':
            UHBoxParamcontent = json.dumps([])
    except:
        UHBoxParamcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\横中横框参数.cfg', 'r') as f:
            HHBoxParamcontent = f.read()
        if HHBoxParamcontent == '':
            HHBoxParamcontent = json.dumps([])
    except:
        HHBoxParamcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\趟门2竖分格.cfg', 'r') as f:
            Cfgobj2content = f.read()
        if Cfgobj2content == '':
            Cfgobj2content = json.dumps([])
    except:
        Cfgobj2content = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\趟门3竖分格.cfg', 'r') as f:
            Cfgobj3content = f.read()
        if Cfgobj3content == '':
            Cfgobj3content = json.dumps([])
    except:
        Cfgobj3content = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\趟门4竖分格.cfg', 'r') as f:
            Cfgobj4content = f.read()
        if Cfgobj4content == '':
            Cfgobj4content = json.dumps([])
    except:
        Cfgobj4content = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\竖中横框参数.cfg', 'r') as f:
            SHBoxParamcontent = f.read()
        if SHBoxParamcontent == '':
            SHBoxParamcontent = json.dumps([])
    except:
        SHBoxParamcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\趟门2横分格.cfg', 'r') as f:
            HCfgobj2content = f.read()
        if HCfgobj2content == '':
            HCfgobj2content = json.dumps([])
    except:
        HCfgobj2content = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\趟门3横分格.cfg', 'r') as f:
            HCfgobj3content = f.read()
        if HCfgobj3content == '':
            HCfgobj3content = json.dumps([])
    except:
        HCfgobj3content = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\趟门4横分格.cfg', 'r') as f:
            HCfgobj4content = f.read()
        if HCfgobj4content == '':
            HCfgobj4content = json.dumps([])
    except:
        HCfgobj4content = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\横中横框参数.cfg', 'r') as f:
            HSHBoxParamcontent = f.read()
        if HSHBoxParamcontent == '':
            HSHBoxParamcontent = json.dumps([])
    except:
        HSHBoxParamcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\QdData\\门转换表.cfg', 'r') as f:
            cfglistcontent = f.read()
        if cfglistcontent == '':
            cfglistcontent = json.dumps([])
    except:
        cfglistcontent = json.dumps([])

    mSlidingExpList = json.loads(mSlidingExpListcontent, encoding='gbk')
    for i in range(0, len(mSlidingExpList)):
        mSlidingExpList[i]['doornum'] = Number(mSlidingExpList[i]['doornum'])
        mSlidingExpList[i]['overlapnum'] = Number(mSlidingExpList[i]['overlapnum'])
        mSlidingExpList[i]['lkvalue'] = Number(mSlidingExpList[i]['lkvalue'])
        mSlidingExpList[i]['noexp'] = GetTrueFalse(mSlidingExpList[i]['noexp'])
    mSlidingExpListcontent = json.dumps(mSlidingExpList).encode('gbk')

    mSSExpList = json.loads(mSSExpListcontent, encoding='gbk')
    for i in range(0, len(mSSExpList)):
        mSSExpList[i]['height'] = mSSExpList[i]['height']
        mSSExpList[i]['width'] = mSSExpList[i]['width']
        mSSExpList[i]['heightcap'] = mSSExpList[i]['heightcap']
        mSSExpList[i]['widthcap'] = mSSExpList[i]['widthcap']
        mSSExpList[i]['minheight'] = mSSExpList[i]['minheight']
        mSSExpList[i]['minwidth'] = mSSExpList[i]['minwidth']
        mSSExpList[i]['size'] = mSSExpList[i]['size']
    mSSExpListcontent = json.dumps(mSSExpList).encode('gbk')

    mSlidingParamList = json.loads(SlidingParamcontent, encoding='gbk')
    for i in range(0, len(mSlidingParamList)):
        mSlidingParamList[i]["ddlw"] = Number(mSlidingParamList[i]['ddlpos'])
        mSlidingParamList[i]["fztlen"] = Number(mSlidingParamList[i]['fztkd'])
        mSlidingParamList[i]["myclass"] = mSlidingParamList[i]['doortype']
        mSlidingParamList[i]['cpm_lmax'] = Number(mSlidingParamList[i]['cpm_lmax'])
        mSlidingParamList[i]['cpm_hmax'] = Number(mSlidingParamList[i]['cpm_hmax'])
        mSlidingParamList[i]['is_xq'] = GetTrueFalse(mSlidingParamList[i]['is_xq'])
        mSlidingParamList[i]['hboxvalue'] = Number(mSlidingParamList[i]['hboxvalue'])
        mSlidingParamList[i]['laminating'] = GetTrueFalse(mSlidingParamList[i]['laminating'])
    SlidingParamcontent = json.dumps(mSlidingParamList).encode('gbk')

    mSlidingAccessoryList = json.loads(mSlidingAccessoryListcontent, encoding='gbk')
    for i in range(0, len(mSlidingAccessoryList)):
        mSlidingAccessoryList[i]['isglass'] = GetTrueFalse(mSlidingAccessoryList[i]['isglass'])
        mSlidingAccessoryList[i]['isbaiye'] = GetTrueFalse(mSlidingAccessoryList[i]['isbaiye'])
        mSlidingAccessoryList[i]['isuserselect'] = GetTrueFalse(mSlidingAccessoryList[i]['isuserselect'])
    mSlidingAccessoryListcontent = json.dumps(mSlidingAccessoryList).encode('gbk')

    mUDBoxParamList = json.loads(UDBoxParamcontent, encoding='gbk')
    for i in range(0, len(mUDBoxParamList)):
        mUDBoxParamList[i]["ubheight"] = Number(mUDBoxParamList[i]['upboxheight'])
        mUDBoxParamList[i]["ubdepth"] = Number(mUDBoxParamList[i]['upboxdepth'])
        mUDBoxParamList[i]["ubthick"] = Number(mUDBoxParamList[i]['upboxthick'])
        mUDBoxParamList[i]["dbheight"] = Number(mUDBoxParamList[i]['downboxheight'])
        mUDBoxParamList[i]["dbdepth"] = Number(mUDBoxParamList[i]['downboxdepth'])
        mUDBoxParamList[i]["dbthick"] = Number(mUDBoxParamList[i]['downboxthick'])
        mUDBoxParamList[i]["uphole"] = Number(mUDBoxParamList[i]['upholepos'])
        mUDBoxParamList[i]["downhole"] = Number(mUDBoxParamList[i]['downholepos'])
        mUDBoxParamList[i]["upsize"] = Number(mUDBoxParamList[i]['upsize'])
    UDBoxParamcontent = json.dumps(mUDBoxParamList).encode('gbk')

    mHBoxParamList = json.loads(HBoxParamcontent, encoding='gbk')
    for i in range(0, len(mHBoxParamList)):
        mHBoxParamList[i]["hole"] = Number(mHBoxParamList[i]['holepos'])
        mHBoxParamList[i]["ishboxvalue"] = Number(mHBoxParamList[i]['ishboxvalue'])
    HBoxParamcontent = json.dumps(mHBoxParamList).encode('gbk')

    UHBoxParam = json.loads(UHBoxParamcontent, encoding='gbk')
    for i in range(0, len(UHBoxParam)):
        UHBoxParam[i]["ishboxvalue"] = Number(UHBoxParam[i]['ishboxvalue'])
    UHBoxParamcontent = json.dumps(UHBoxParam).encode('gbk')

    mVBoxParamList = json.loads(mVBoxParamListcontent, encoding='gbk')
    for i in range(0, len(mVBoxParamList)):
        mVBoxParamList[i]["name"] = mVBoxParamList[i]["name"]
        mVBoxParamList[i]["height"] = Number(mVBoxParamList[i]["height"])
        mVBoxParamList[i]["depth"] = Number(mVBoxParamList[i]["depth"])
        mVBoxParamList[i]["thick"] = Number(mVBoxParamList[i]["thick"])
        mVBoxParamList[i]["panelvalue"] = Number(mVBoxParamList[i]["panelvalue"])
        mVBoxParamList[i]["wlcode"] = mVBoxParamList[i]["wlcode"]
        mVBoxParamList[i]["wjname"] = mVBoxParamList[i]["wjname"]
        mVBoxParamList[i]["udboxvalue"] = Number(mVBoxParamList[i]["udboxvalue"])
        mVBoxParamList[i]["vboxvalue"] = Number(mVBoxParamList[i]["vboxvalue"])
        mVBoxParamList[i]["size"] = Number(mVBoxParamList[i]["size"])
        mVBoxParamList[i]["model"] = mVBoxParamList[i]["model"]
        mVBoxParamList[i]["memo"] = mVBoxParamList[i]["memo"]
        mVBoxParamList[i]["bdfile"] = mVBoxParamList[i]["bdfile"]
    mVBoxParamListcontent = json.dumps(mVBoxParamList).encode('gbk')

    PanelTypeList = json.loads(PanelTypeListcontent, encoding='gbk')
    for i in range(0, len(PanelTypeList)):
        PanelTypeList[i]["name"] = PanelTypeList[i]['name']
        PanelTypeList[i]["jtvalue"] = Number(
            PanelTypeList[i]['jtValue'] if "jtvalue" not in PanelTypeList[i] else PanelTypeList[i]['jtvalue'])
        PanelTypeList[i]["jtValue"] = PanelTypeList[i]["jtvalue"]
        PanelTypeList[i]["wjname"] = PanelTypeList[i]['wjname']
        PanelTypeList[i]["isglass"] = GetTrueFalse(PanelTypeList[i]['isglass'])
        PanelTypeList[i]["isbaiye"] = GetTrueFalse(PanelTypeList[i]['isbaiye'])
        PanelTypeList[i]["iswhole"] = GetTrueFalse(
            PanelTypeList[i]['iswHole'] if "iswhole" not in PanelTypeList[i] else PanelTypeList[i]['iswhole'])
        PanelTypeList[i]["iswHole"] = PanelTypeList[i]["iswhole"]
        PanelTypeList[i]["bktype"] = PanelTypeList[i]['bktype']
        PanelTypeList[i]["direct"] = PanelTypeList[i]['direct']
        PanelTypeList[i]["lmax"] = Number(PanelTypeList[i]['lmax'])
        PanelTypeList[i]["lmin"] = Number(PanelTypeList[i]['lmin'])
        PanelTypeList[i]["wmax"] = Number(PanelTypeList[i]['wmax'])
        PanelTypeList[i]["wmin"] = Number(PanelTypeList[i]['wmin'])
        PanelTypeList[i]["pnl2d"] = PanelTypeList[i]['panel2d']
        PanelTypeList[i]["slave"] = PanelTypeList[i]['slaVe'] if 'slave' not in PanelTypeList[i] else PanelTypeList[i][
            'slave']
        PanelTypeList[i]["slaVe"] = PanelTypeList[i]["slave"]
        PanelTypeList[i]["slave2"] = PanelTypeList[i]['slaVe2'] if 'slave2' not in PanelTypeList[i] else \
        PanelTypeList[i]['slave2']
        PanelTypeList[i]["slaVe2"] = PanelTypeList[i]["slave2"]
        PanelTypeList[i]["mk3d"] = PanelTypeList[i]['mk3d']
        PanelTypeList[i]["mkl"] = Number(PanelTypeList[i]['mkl'])
        PanelTypeList[i]["mkh"] = Number(
            PanelTypeList[i]['mkH'] if 'mkh' not in PanelTypeList[i] else PanelTypeList[i]['mkh'])
        PanelTypeList[i]["mkH"] = PanelTypeList[i]["mkh"]
        PanelTypeList[i]['thick'] = Number(
            PanelTypeList[i]['tHick'] if 'thick' not in PanelTypeList[i] else PanelTypeList[i]['thick'])
        PanelTypeList[i]["tHick"] = PanelTypeList[i]["thick"]
        PanelTypeList[i]["memo"] = PanelTypeList[i]["memo"]
        PanelTypeList[i]["memo2"] = PanelTypeList[i]["memo2"]
        PanelTypeList[i]["memo3"] = PanelTypeList[i]["memo3"]
        PanelTypeList[i]["bdfile"] = PanelTypeList[i]["bdfile"]
    PanelTypeListcontent = json.dumps(PanelTypeList).encode('gbk')

    adb.put((rootname + 'mSlidingExpList').encode('utf8'), mSlidingExpListcontent)
    adb.put((rootname + 'mSlidingTypeList').encode('utf8'), mSlidingTypeListcontent)
    adb.put((rootname + 'mSlidingParamList').encode('utf8'), SlidingParamcontent)
    adb.put((rootname + 'mUDBoxParamList').encode('utf8'), UDBoxParamcontent)
    adb.put((rootname + 'mTrackParamList').encode('utf8'), TrackParamcontent)
    adb.put((rootname + 'mHBoxParamList').encode('utf8'), HBoxParamcontent)
    adb.put((rootname + 'PanelTypeList').encode('utf8'), PanelTypeListcontent)
    adb.put((rootname + 'mSlidingColorList').encode('utf8'), mSlidingColorListcontent)
    adb.put((rootname + 'mSlidingColorClassList').encode('utf8'), mSlidingColorClassListcontent)
    adb.put((rootname + 'mSlidingWjBomDetailList').encode('utf8'), mSlidingWjBomDetailListcontent)
    adb.put((rootname + 'mSSExpList').encode('utf8'), mSSExpListcontent)
    adb.put((rootname + 'mSlidingAccessoryList').encode('utf8'), mSlidingAccessoryListcontent)
    adb.put((rootname + 'mVBoxParamList').encode('utf8'), mVBoxParamListcontent)
    adb.put((rootname + 'mPanelBomDetailList').encode('utf8'), mPanelBomDetailListcontent)
    adb.put((rootname + 'UHBoxParam').encode('utf8'), UHBoxParamcontent)
    adb.put((rootname + 'UHBoxParam').encode('utf8'), UHBoxParamcontent)
    adb.put((rootname + 'HHBoxParam').encode('utf8'), HHBoxParamcontent)
    adb.put((rootname + 'Cfgobj2').encode('utf8'), Cfgobj2content)
    adb.put((rootname + 'Cfgobj3').encode('utf8'), Cfgobj3content)
    adb.put((rootname + 'Cfgobj4').encode('utf8'), Cfgobj4content)
    adb.put((rootname + 'SHBoxParam').encode('utf8'), SHBoxParamcontent)
    adb.put((rootname + 'HCfgobj2').encode('utf8'), HCfgobj2content)
    adb.put((rootname + 'HCfgobj3').encode('utf8'), HCfgobj3content)
    adb.put((rootname + 'HCfgobj4').encode('utf8'), HCfgobj4content)
    adb.put((rootname + 'HSHBoxParam').encode('utf8'), HSHBoxParamcontent)
    adb.put((rootname + 'cfglist').encode('utf8'), cfglistcontent)

def DoorInitData(myversion, Path):
    RootPath = Path
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\五金配件.cfg', 'r') as f:
            mAccessoryListcontent = f.read()
        if mAccessoryListcontent == '':
            mAccessoryListcontent = json.dumps([])
    except:
        mAccessoryListcontent = json.dumps([])
        log.error('ini=' + RootPath + '\\data\\XDiyDoors.ini')
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\颜色.cfg', 'r') as f:
            mColorListcontent = f.read()
        if mColorListcontent == '':
            mColorListcontent = json.dumps([])
    except:
        mColorListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\颜色分类.cfg', 'r') as f:
            mColorClassListcontent = f.read()
        if mColorClassListcontent == '':
            mColorClassListcontent = json.dumps([])
    except:
        mColorClassListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\颜色分类2.cfg', 'r') as f:
            mColorClass2Listcontent = f.read()
        if mColorClass2Listcontent == '':
            mColorClass2Listcontent = json.dumps([])
    except:
        mColorClass2Listcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\门类型.cfg', 'r') as f:
            mTypeListcontent = f.read()
        if mTypeListcontent == '':
            mTypeListcontent = json.dumps([])
    except:
        mTypeListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\单门数量类型.cfg', 'r') as f:
            mExpListcontent = f.read()
        if mExpListcontent == '':
            mExpListcontent = json.dumps([])
    except:
        mExpListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\拉手.cfg', 'r') as f:
            mHandleListcontent = f.read()
        if mHandleListcontent == '':
            mHandleListcontent = json.dumps([])
    except:
        mHandleListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\中横框参数.cfg', 'r') as f:
            mDoorHBoxParamListcontent = f.read()
        if mDoorHBoxParamListcontent == '':
            mDoorHBoxParamListcontent = json.dumps([])
    except:
        mDoorHBoxParamListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\门铰分类.cfg', 'r') as f:
            mHingeListcontent = f.read()
        if mHingeListcontent == '':
            mHingeListcontent = json.dumps([])
    except:
        mHingeListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\门铰.cfg', 'r') as f:
            mCurHingeListcontent = f.read()
        if mCurHingeListcontent == '':
            mCurHingeListcontent = json.dumps([])
    except:
        mCurHingeListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\门芯附加物料.cfg', 'r') as f:
            mDoorPanelBomDetailListcontent = f.read()
        if mDoorPanelBomDetailListcontent == '':
            mDoorPanelBomDetailListcontent = json.dumps([])
    except:
        mDoorPanelBomDetailListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\门芯类型.cfg', 'r') as f:
            mDoorPanelTypeListcontent = f.read()
        if mDoorPanelTypeListcontent == '':
            mDoorPanelTypeListcontent = json.dumps([])
    except:
        mDoorPanelTypeListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\掩门参数.cfg', 'r') as f:
            mParamListcontent = f.read()
        if mParamListcontent == '':
            mParamListcontent = json.dumps([])
    except:
        mParamListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\报价.cfg', 'r') as f:
            mPriceListcontent = f.read()
        if mPriceListcontent == '':
            mPriceListcontent = json.dumps([])
    except:
        mPriceListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\报价方案.cfg', 'r') as f:
            mPriceTableListcontent = f.read()
        if mPriceTableListcontent == '':
            mPriceTableListcontent = json.dumps([])
    except:
        mPriceTableListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\百叶板配置.cfg', 'r') as f:
            mShutterExpListcontent = f.read()
        if mShutterExpListcontent == '':
            mShutterExpListcontent = json.dumps([])
    except:
        mShutterExpListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\五金配件分类.cfg', 'r') as f:
            mWJBomListcontent = f.read()
        if mWJBomListcontent == '':
            mWJBomListcontent = json.dumps([])
    except:
        mWJBomListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\五金配件分类数据.cfg', 'r') as f:
            mWJBomDetailListcontent = f.read()
        if mWJBomDetailListcontent == '':
            mWJBomDetailListcontent = json.dumps([])
    except:
        mWJBomDetailListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Door\\掩门配置表\\XML单门结构.cfg', 'r') as f:
            mDoorXMLListcontent = f.read()
        if mDoorXMLListcontent == '':
            mDoorXMLListcontent = json.dumps([])
    except:
        mDoorXMLListcontent = json.dumps([])

    mExpList = json.loads(mExpListcontent, encoding='gbk')
    for i in range(0, len(mExpList)):
        mExpList[i]['doornum'] = Number(mExpList[i]['doornum'])
        mExpList[i]['capnum'] = Number(mExpList[i]['capnum'])
        mExpList[i]['lkvalue'] = Number(mExpList[i]['lkvalue'])
    mExpListcontent = json.dumps(mExpList).encode('gbk')

    mDoorHBoxParamList = json.loads(mDoorHBoxParamListcontent, encoding='gbk')
    for i in range(0, len(mDoorHBoxParamList)):
        mDoorHBoxParamList[i]['height'] = Number(mDoorHBoxParamList[i]['height'])
        mDoorHBoxParamList[i]['depth'] = Number(mDoorHBoxParamList[i]['depth'])
        mDoorHBoxParamList[i]['thick'] = Number(mDoorHBoxParamList[i]['thick'])
    mDoorHBoxParamListcontent = json.dumps(mDoorHBoxParamList).encode('gbk')

    mHingeList = json.loads(mHingeListcontent, encoding='gbk')
    for i in range(0, len(mHingeList)):
        mHingeList[i]['min1'] = Number(mHingeList[i]['min1'])
        mHingeList[i]['max1'] = Number(mHingeList[i]['max1'])
        mHingeList[i]['num1'] = Number(mHingeList[i]['num1'])
        mHingeList[i]['min2'] = Number(mHingeList[i]['min2'])
        mHingeList[i]['max2'] = Number(mHingeList[i]['max2'])
        mHingeList[i]['num2'] = Number(mHingeList[i]['num2'])
        mHingeList[i]['min3'] = Number(mHingeList[i]['min3'])
        mHingeList[i]['max3'] = Number(mHingeList[i]['max3'])
        mHingeList[i]['num3'] = Number(mHingeList[i]['num3'])
        mHingeList[i]['min4'] = Number(mHingeList[i]['min4'])
        mHingeList[i]['max4'] = Number(mHingeList[i]['max4'])
        mHingeList[i]['num4'] = Number(mHingeList[i]['num4'])
        mHingeList[i]['min5'] = Number(mHingeList[i]['min5'])
        mHingeList[i]['max5'] = Number(mHingeList[i]['max5'])
        mHingeList[i]['num5'] = Number(mHingeList[i]['num5'])
        mHingeList[i]['iszn'] = "0" if 'iszn' not in mHingeList[i] else mHingeList[i]['iszn']
        mHingeList[i]['bh'] = Number(mHingeList[i]['bh'])
    mHingeListcontent = json.dumps(mHingeList).encode('gbk')

    mDoorPanelBomDetailList = json.loads(mDoorPanelBomDetailListcontent, encoding='gbk')
    for i in range(0, len(mDoorPanelBomDetailList)):
        mDoorPanelBomDetailList[i]["lmin"] = Number(mDoorPanelBomDetailList[i]['lmin'])
        mDoorPanelBomDetailList[i]["lmax"] = Number(mDoorPanelBomDetailList[i]['lmax'])
        mDoorPanelBomDetailList[i]["hmin"] = Number(mDoorPanelBomDetailList[i]['hmin'])
        mDoorPanelBomDetailList[i]["hmax"] = Number(mDoorPanelBomDetailList[i]['hmax'])
        mDoorPanelBomDetailList[i]["num"] = Number(mDoorPanelBomDetailList[i]['num'])
    mDoorPanelBomDetailListcontent = json.dumps(mDoorPanelBomDetailList).encode('gbk')

    mDoorPanelTypeList = json.loads(mDoorPanelTypeListcontent, encoding='gbk')
    for i in range(0, len(mDoorPanelTypeList)):
        mDoorPanelTypeList[i]["thick"] = Number(mDoorPanelTypeList[i]['thick'])
        mDoorPanelTypeList[i]["lfb"] = Number(mDoorPanelTypeList[i]['lfb'])
        mDoorPanelTypeList[i]["hfb"] = Number(mDoorPanelTypeList[i]['hfb'])
        mDoorPanelTypeList[i]["bomtype"] = mDoorPanelTypeList[i]['bomtype']
        mDoorPanelTypeList[i]["bktype"] = mDoorPanelTypeList[i]['bktype']
        mDoorPanelTypeList[i]["lmax"] = Number(mDoorPanelTypeList[i]['lmax'])
        mDoorPanelTypeList[i]["lmin"] = Number(mDoorPanelTypeList[i]['lmin'])
        mDoorPanelTypeList[i]["wmax"] = Number(mDoorPanelTypeList[i]['wmax'])
        mDoorPanelTypeList[i]["wmin"] = Number(mDoorPanelTypeList[i]['wmin'])
        mDoorPanelTypeList[i]["is_buy"] = mDoorPanelTypeList[i]['is_buy']
        mDoorPanelTypeList[i]["direct"] = mDoorPanelTypeList[i]['direct']
        mDoorPanelTypeList[i]["fbstr"] = mDoorPanelTypeList[i]['fbstr']
        mDoorPanelTypeList[i]["pnl3d"] = mDoorPanelTypeList[i]['pnl3d']
        mDoorPanelTypeList[i]["memo"] = mDoorPanelTypeList[i]['memo']
        mDoorPanelTypeList[i]["panelbom"] = mDoorPanelTypeList[i]['panelbom']
        mDoorPanelTypeList[i]["ypos"] = Number(mDoorPanelTypeList[i]['ypos'])
        mDoorPanelTypeList[i]["iswhole"] = mDoorPanelTypeList[i]['iswhole']
    mDoorPanelTypeListcontent = json.dumps(mDoorPanelTypeList).encode('gbk')

    mParamList = json.loads(mParamListcontent, encoding='gbk')
    for i in range(0, len(mParamList)):
        mParamList[i]["DoorsType"] = mParamList[i]['doorstype']
        mParamList[i]["Handle"] = mParamList[i]['handle']
        mParamList[i]["PanelType"] = mParamList[i]['paneltype']
        mParamList[i]["cap"] = mParamList[i]['cap']
        mParamList[i]["eb_cap"] = Number(mParamList[i]['eb_cap'])
        mParamList[i]["vboxh"] = Number(mParamList[i]['vboxh'])
        mParamList[i]["udboxh"] = Number(mParamList[i]['udboxh'])
        mParamList[i]["vthick"] = mParamList[i]['vthick']
        mParamList[i]["udthick"] = Number(mParamList[i]['udthick'])
        mParamList[i]["vboxjtw"] = Number(mParamList[i]['vboxjtw'])
        mParamList[i]["udboxjtw"] = Number(
            mParamList[i]['udboxjtw'] if 'udboxjt' not in mParamList[i] else mParamList[i]['udboxjt'])
        mParamList[i]["hboxjtw"] = Number(mParamList[i]['hboxjtw'])
        mParamList[i]["iscalc_framebom"] = GetTrueFalse(mParamList[i]['iscalc_framebom'])
        mParamList[i]["frame_valuel"] = Number(mParamList[i]['frame_valuel'])
        mParamList[i]["frame_valueh"] = Number(mParamList[i]['frame_valueh'])
        mParamList[i]["udbox_hbox_value"] = Number(mParamList[i]['udbox_hbox_value'])
        mParamList[i]["is_xq"] = GetTrueFalse(mParamList[i]['is_xq'])
        mParamList[i]["cb_yyvalue"] = Number(mParamList[i]['cb_yyvalue'])
        mParamList[i]["is_buy"] = mParamList[i]['is_buy']
        mParamList[i]["noframe_bom"] = Number(mParamList[i]['noframe_bom'])
    mParamListcontent = json.dumps(mParamList).encode('gbk')

    mShutterExpList = json.loads(mShutterExpListcontent, encoding='gbk')
    for i in range(0, len(mShutterExpList)):
        mShutterExpList[i]["height"] = Number(mShutterExpList[i]["height"])
        mShutterExpList[i]["width"] = Number(mShutterExpList[i]["width"])
        mShutterExpList[i]["heightcap"] = Number(mShutterExpList[i]["heightcap"])
        mShutterExpList[i]["widthcap"] = Number(mShutterExpList[i]["widthcap"])
        mShutterExpList[i]["minheight"] = Number(mShutterExpList[i]["minheight"])
        mShutterExpList[i]["minwidth"] = Number(mShutterExpList[i]["minwidth"])
    mShutterExpListcontent = json.dumps(mShutterExpList).encode('gbk')

    mWJBomDetailList = json.loads(mWJBomDetailListcontent, encoding='gbk')
    for i in range(0, len(mWJBomDetailList)):
        mWJBomDetailList[i]["door_bh"] = Number(mWJBomDetailList[i]["door_bh"])
        mWJBomDetailList[i]["bktypeAry"] = []
        if mWJBomDetailList[i]["bktype"] != '':
            mWJBomDetailList[i]["bktypeAry"] = mWJBomDetailList[i]['bktype'].split(',')
    mWJBomDetailListcontent = json.dumps(mWJBomDetailList).encode('gbk')

    mAccessoryList = json.loads(mAccessoryListcontent, encoding='gbk')
    for i in range(0, len(mAccessoryList)):
        mAccessoryList[i]["myunit"] = mAccessoryList[i]["unit"]
    mAccessoryListcontent = json.dumps(mAccessoryList).encode('gbk')

    mTypeList = json.loads(mTypeListcontent, encoding='gbk')
    for i in range(0, len(mTypeList)):
        mTypeList[i]["isframe"] = GetTrueFalse(mTypeList[i]["isframe"])
        mTypeList[i]["covertype"] = Number(mTypeList[i]["covertype"])
        mTypeList[i]["lkvalue"] = Number(mTypeList[i]["lkvalue"])
        mTypeList[i]["ud_lkvalue"] = mTypeList[i]['lkvalue'] if "ud_lkvalue" not in mTypeList[i] else Number(
            mTypeList[i]['ud_lkvalue'])
        mTypeList[i]["depth"] = Number(mTypeList[i]["depth"])
        mTypeList[i]["eb_lkvalue"] = Number(mTypeList[i]["eb_lkvalue"])
        mTypeList[i]["eb_ud_lkvalue"] = Number(mTypeList[i]["eb_ud_lkvalue"])
    mTypeListcontent = json.dumps(mTypeList).encode('gbk')

    r.set((myversion + 'mExpList').encode('utf8'), mExpListcontent)
    r.set((myversion + 'mHandleList').encode('utf8'), mHandleListcontent)
    r.set((myversion + 'mDoorHBoxParamList').encode('utf8'), mDoorHBoxParamListcontent)
    r.set((myversion + 'mHingeList').encode('utf8'), mHingeListcontent)
    r.set((myversion + 'mCurHingeList').encode('utf8'), mCurHingeListcontent)
    r.set((myversion + 'mDoorPanelBomDetailList').encode('utf8'), mDoorPanelBomDetailListcontent)
    r.set((myversion + 'mDoorPanelTypeList').encode('utf8'), mDoorPanelTypeListcontent)

    r.set((myversion + 'mParamList').encode('utf8'), mParamListcontent)

    r.set((myversion + 'mShutterExpList').encode('utf8'), mShutterExpListcontent)
    r.set((myversion + 'mWJBomList').encode('utf8'), mWJBomListcontent)
    r.set((myversion + 'mWJBomDetailList').encode('utf8'), mWJBomDetailListcontent)
    r.set((myversion + 'mDoorXMLList').encode('utf8'), mDoorXMLListcontent)
    r.set((myversion + 'mAccessoryList').encode('utf8'), mAccessoryListcontent)
    r.set((myversion + 'mColorList').encode('utf8'), mColorListcontent)

    r.set((myversion + 'mColorClassList').encode('utf8'), mColorClassListcontent)
    r.set((myversion + 'mColorClass2List').encode('utf8'), mColorClass2Listcontent)
    r.set((myversion + 'mTypeList').encode('utf8'), mTypeListcontent)

def SlidingInitData(myversion, Path):
    RootPath = Path

    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\单门数量类型.cfg', 'r') as f:
            mSlidingExpListcontent = f.read()
        if mSlidingExpListcontent == '':
            mSlidingExpListcontent = json.dumps([])
    except:
        mSlidingExpListcontent = json.dumps([])

    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\门类型.cfg', 'r') as f:
            mSlidingTypeListcontent = f.read()
        if mSlidingTypeListcontent == '':
            mSlidingTypeListcontent = json.dumps([])
    except:
        mSlidingTypeListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\趟门参数.cfg', 'r') as f:
            SlidingParamcontent = f.read()
        if SlidingParamcontent == '':
            SlidingParamcontent = json.dumps([])
    except:
        SlidingParamcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\上下横框参数.cfg', 'r') as f:
            UDBoxParamcontent = f.read()
        if UDBoxParamcontent == '':
            UDBoxParamcontent = json.dumps([])
    except:
        UDBoxParamcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\上下轨参数.cfg', 'r') as f:
            TrackParamcontent = f.read()
        if TrackParamcontent == '':
            TrackParamcontent = json.dumps([])
    except:
        TrackParamcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\中横框参数.cfg', 'r') as f:
            HBoxParamcontent = f.read()
        if HBoxParamcontent == '':
            HBoxParamcontent = json.dumps([])
    except:
        HBoxParamcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\门板类型.cfg', 'r') as f:
            PanelTypeListcontent = f.read()
        if PanelTypeListcontent == '':
            PanelTypeListcontent = json.dumps([])
    except:
        PanelTypeListcontent = json.dumps([])

    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\颜色分类2.cfg', 'r') as f:
            mSlidingColorListcontent = f.read()
        if mSlidingColorListcontent == '':
            mSlidingColorListcontent = json.dumps([])
    except:
        mSlidingColorListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\颜色分类.cfg', 'r') as f:
            mSlidingColorClassListcontent = f.read()
        if mSlidingColorClassListcontent == '':
            mSlidingColorClassListcontent = json.dumps([])
    except:
        mSlidingColorClassListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\五金配件分类数据.cfg', 'r') as f:
            mSlidingWjBomDetailListcontent = f.read()
        if mSlidingWjBomDetailListcontent == '':
            mSlidingWjBomDetailListcontent = json.dumps([])
    except:
        mSlidingWjBomDetailListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\百叶板计算公式.cfg', 'r') as f:
            mSSExpListcontent = f.read()
        if mSSExpListcontent == '':
            mSSExpListcontent = json.dumps([])
    except:
        mSSExpListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\五金配件.cfg', 'r') as f:
            mSlidingAccessoryListcontent = f.read()
        if mSlidingAccessoryListcontent == '':
            mSlidingAccessoryListcontent = json.dumps([])
    except:
        mSlidingAccessoryListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\竖框参数.cfg', 'r') as f:
            mVBoxParamListcontent = f.read()
        if mVBoxParamListcontent == '':
            mVBoxParamListcontent = json.dumps([])
    except:
        mVBoxParamListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\门板附加物料.cfg', 'r') as f:
            mPanelBomDetailListcontent = f.read()
        if mPanelBomDetailListcontent == '':
            mPanelBomDetailListcontent = json.dumps([])
    except:
        mPanelBomDetailListcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\竖中横框参数.cfg', 'r') as f:
            UHBoxParamcontent = f.read()
        if UHBoxParamcontent == '':
            UHBoxParamcontent = json.dumps([])
    except:
        UHBoxParamcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\横中横框参数.cfg', 'r') as f:
            HHBoxParamcontent = f.read()
        if HHBoxParamcontent == '':
            HHBoxParamcontent = json.dumps([])
    except:
        HHBoxParamcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\趟门2竖分格.cfg', 'r') as f:
            Cfgobj2content = f.read()
        if Cfgobj2content == '':
            Cfgobj2content = json.dumps([])
    except:
        Cfgobj2content = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\趟门3竖分格.cfg', 'r') as f:
            Cfgobj3content = f.read()
        if Cfgobj3content == '':
            Cfgobj3content = json.dumps([])
    except:
        Cfgobj3content = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\趟门4竖分格.cfg', 'r') as f:
            Cfgobj4content = f.read()
        if Cfgobj4content == '':
            Cfgobj4content = json.dumps([])
    except:
        Cfgobj4content = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\竖中横框参数.cfg', 'r') as f:
            SHBoxParamcontent = f.read()
        if SHBoxParamcontent == '':
            SHBoxParamcontent = json.dumps([])
    except:
        SHBoxParamcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\趟门2横分格.cfg', 'r') as f:
            HCfgobj2content = f.read()
        if HCfgobj2content == '':
            HCfgobj2content = json.dumps([])
    except:
        HCfgobj2content = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\趟门3横分格.cfg', 'r') as f:
            HCfgobj3content = f.read()
        if HCfgobj3content == '':
            HCfgobj3content = json.dumps([])
    except:
        HCfgobj3content = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\趟门4横分格.cfg', 'r') as f:
            HCfgobj4content = f.read()
        if HCfgobj4content == '':
            HCfgobj4content = json.dumps([])
    except:
        HCfgobj4content = json.dumps([])
    try:
        with open(RootPath + '\\data\\Sliding\\趟门配置表\\横中横框参数.cfg', 'r') as f:
            HSHBoxParamcontent = f.read()
        if HSHBoxParamcontent == '':
            HSHBoxParamcontent = json.dumps([])
    except:
        HSHBoxParamcontent = json.dumps([])
    try:
        with open(RootPath + '\\data\\QdData\\门转换表.cfg', 'r') as f:
            cfglistcontent = f.read()
        if cfglistcontent == '':
            cfglistcontent = json.dumps([])
    except:
        cfglistcontent = json.dumps([])

    mSlidingExpList = json.loads(mSlidingExpListcontent, encoding='gbk')
    for i in range(0, len(mSlidingExpList)):
        mSlidingExpList[i]['doornum'] = Number(mSlidingExpList[i]['doornum'])
        mSlidingExpList[i]['overlapnum'] = Number(mSlidingExpList[i]['overlapnum'])
        mSlidingExpList[i]['lkvalue'] = Number(mSlidingExpList[i]['lkvalue'])
        mSlidingExpList[i]['noexp'] = GetTrueFalse(mSlidingExpList[i]['noexp'])
    mSlidingExpListcontent = json.dumps(mSlidingExpList).encode('gbk')

    mSSExpList = json.loads(mSSExpListcontent, encoding='gbk')
    for i in range(0, len(mSSExpList)):
        mSSExpList[i]['height'] = mSSExpList[i]['height']
        mSSExpList[i]['width'] = mSSExpList[i]['width']
        mSSExpList[i]['heightcap'] = mSSExpList[i]['heightcap']
        mSSExpList[i]['widthcap'] = mSSExpList[i]['widthcap']
        mSSExpList[i]['minheight'] = mSSExpList[i]['minheight']
        mSSExpList[i]['minwidth'] = mSSExpList[i]['minwidth']
        mSSExpList[i]['size'] = mSSExpList[i]['size']
    mSSExpListcontent = json.dumps(mSSExpList).encode('gbk')

    mSlidingParamList = json.loads(SlidingParamcontent, encoding='gbk')
    for i in range(0, len(mSlidingParamList)):
        mSlidingParamList[i]["ddlw"] = Number(mSlidingParamList[i]['ddlpos'])
        mSlidingParamList[i]["fztlen"] = Number(mSlidingParamList[i]['fztkd'])
        mSlidingParamList[i]["myclass"] = mSlidingParamList[i]['doortype']
        mSlidingParamList[i]['cpm_lmax'] = Number(mSlidingParamList[i]['cpm_lmax'])
        mSlidingParamList[i]['cpm_hmax'] = Number(mSlidingParamList[i]['cpm_hmax'])
        mSlidingParamList[i]['is_xq'] = GetTrueFalse(mSlidingParamList[i]['is_xq'])
        mSlidingParamList[i]['hboxvalue'] = Number(mSlidingParamList[i]['hboxvalue'])
        mSlidingParamList[i]['laminating'] = GetTrueFalse(mSlidingParamList[i]['laminating'])
    SlidingParamcontent = json.dumps(mSlidingParamList).encode('gbk')

    mSlidingAccessoryList = json.loads(mSlidingAccessoryListcontent, encoding='gbk')
    for i in range(0, len(mSlidingAccessoryList)):
        mSlidingAccessoryList[i]['isglass'] = GetTrueFalse(mSlidingAccessoryList[i]['isglass'])
        mSlidingAccessoryList[i]['isbaiye'] = GetTrueFalse(mSlidingAccessoryList[i]['isbaiye'])
        mSlidingAccessoryList[i]['isuserselect'] = GetTrueFalse(mSlidingAccessoryList[i]['isuserselect'])
    mSlidingAccessoryListcontent = json.dumps(mSlidingAccessoryList).encode('gbk')

    mUDBoxParamList = json.loads(UDBoxParamcontent, encoding='gbk')
    for i in range(0, len(mUDBoxParamList)):
        mUDBoxParamList[i]["ubheight"] = Number(mUDBoxParamList[i]['upboxheight'])
        mUDBoxParamList[i]["ubdepth"] = Number(mUDBoxParamList[i]['upboxdepth'])
        mUDBoxParamList[i]["ubthick"] = Number(mUDBoxParamList[i]['upboxthick'])
        mUDBoxParamList[i]["dbheight"] = Number(mUDBoxParamList[i]['downboxheight'])
        mUDBoxParamList[i]["dbdepth"] = Number(mUDBoxParamList[i]['downboxdepth'])
        mUDBoxParamList[i]["dbthick"] = Number(mUDBoxParamList[i]['downboxthick'])
        mUDBoxParamList[i]["uphole"] = Number(mUDBoxParamList[i]['upholepos'])
        mUDBoxParamList[i]["downhole"] = Number(mUDBoxParamList[i]['downholepos'])
        mUDBoxParamList[i]["upsize"] = Number(mUDBoxParamList[i]['upsize'])
    UDBoxParamcontent = json.dumps(mUDBoxParamList).encode('gbk')

    mHBoxParamList = json.loads(HBoxParamcontent, encoding='gbk')
    for i in range(0, len(mHBoxParamList)):
        mHBoxParamList[i]["hole"] = Number(mHBoxParamList[i]['holepos'])
        mHBoxParamList[i]["ishboxvalue"] = Number(mHBoxParamList[i]['ishboxvalue'])
    HBoxParamcontent = json.dumps(mHBoxParamList).encode('gbk')

    UHBoxParam = json.loads(UHBoxParamcontent, encoding='gbk')
    for i in range(0, len(UHBoxParam)):
        UHBoxParam[i]["ishboxvalue"] = Number(UHBoxParam[i]['ishboxvalue'])
    UHBoxParamcontent = json.dumps(UHBoxParam).encode('gbk')

    mVBoxParamList = json.loads(mVBoxParamListcontent, encoding='gbk')
    for i in range(0, len(mVBoxParamList)):
        mVBoxParamList[i]["name"] = mVBoxParamList[i]["name"]
        mVBoxParamList[i]["height"] = Number(mVBoxParamList[i]["height"])
        mVBoxParamList[i]["depth"] = Number(mVBoxParamList[i]["depth"])
        mVBoxParamList[i]["thick"] = Number(mVBoxParamList[i]["thick"])
        mVBoxParamList[i]["panelvalue"] = Number(mVBoxParamList[i]["panelvalue"])
        mVBoxParamList[i]["wlcode"] = mVBoxParamList[i]["wlcode"]
        mVBoxParamList[i]["wjname"] = mVBoxParamList[i]["wjname"]
        mVBoxParamList[i]["udboxvalue"] = Number(mVBoxParamList[i]["udboxvalue"])
        mVBoxParamList[i]["vboxvalue"] = Number(mVBoxParamList[i]["vboxvalue"])
        mVBoxParamList[i]["size"] = Number(mVBoxParamList[i]["size"])
        mVBoxParamList[i]["model"] = mVBoxParamList[i]["model"]
        mVBoxParamList[i]["memo"] = mVBoxParamList[i]["memo"]
        mVBoxParamList[i]["bdfile"] = mVBoxParamList[i]["bdfile"]
    mVBoxParamListcontent = json.dumps(mVBoxParamList).encode('gbk')

    PanelTypeList = json.loads(PanelTypeListcontent, encoding='gbk')
    for i in range(0, len(PanelTypeList)):
        PanelTypeList[i]["name"] = PanelTypeList[i]['name']
        PanelTypeList[i]["jtvalue"] = Number(
            PanelTypeList[i]['jtValue'] if "jtvalue" not in PanelTypeList[i] else PanelTypeList[i]['jtvalue'])
        PanelTypeList[i]["jtValue"] = PanelTypeList[i]["jtvalue"]
        PanelTypeList[i]["wjname"] = PanelTypeList[i]['wjname']
        PanelTypeList[i]["isglass"] = GetTrueFalse(PanelTypeList[i]['isglass'])
        PanelTypeList[i]["isbaiye"] = GetTrueFalse(PanelTypeList[i]['isbaiye'])
        PanelTypeList[i]["iswhole"] = GetTrueFalse(
            PanelTypeList[i]['iswHole'] if "iswhole" not in PanelTypeList[i] else PanelTypeList[i]['iswhole'])
        PanelTypeList[i]["iswHole"] = PanelTypeList[i]["iswhole"]
        PanelTypeList[i]["bktype"] = PanelTypeList[i]['bktype']
        PanelTypeList[i]["direct"] = PanelTypeList[i]['direct']
        PanelTypeList[i]["lmax"] = Number(PanelTypeList[i]['lmax'])
        PanelTypeList[i]["lmin"] = Number(PanelTypeList[i]['lmin'])
        PanelTypeList[i]["wmax"] = Number(PanelTypeList[i]['wmax'])
        PanelTypeList[i]["wmin"] = Number(PanelTypeList[i]['wmin'])
        PanelTypeList[i]["pnl2d"] = PanelTypeList[i]['panel2d']
        PanelTypeList[i]["slave"] = PanelTypeList[i]['slaVe'] if 'slave' not in PanelTypeList[i] else PanelTypeList[i][
            'slave']
        PanelTypeList[i]["slaVe"] = PanelTypeList[i]["slave"]
        PanelTypeList[i]["slave2"] = PanelTypeList[i]['slaVe2'] if 'slave2' not in PanelTypeList[i] else \
        PanelTypeList[i]['slave2']
        PanelTypeList[i]["slaVe2"] = PanelTypeList[i]["slave2"]
        PanelTypeList[i]["mk3d"] = PanelTypeList[i]['mk3d']
        PanelTypeList[i]["mkl"] = Number(PanelTypeList[i]['mkl'])
        PanelTypeList[i]["mkh"] = Number(
            PanelTypeList[i]['mkH'] if 'mkh' not in PanelTypeList[i] else PanelTypeList[i]['mkh'])
        PanelTypeList[i]["mkH"] = PanelTypeList[i]["mkh"]
        PanelTypeList[i]['thick'] = Number(
            PanelTypeList[i]['tHick'] if 'thick' not in PanelTypeList[i] else PanelTypeList[i]['thick'])
        PanelTypeList[i]["tHick"] = PanelTypeList[i]["thick"]
        PanelTypeList[i]["memo"] = PanelTypeList[i]["memo"]
        PanelTypeList[i]["memo2"] = PanelTypeList[i]["memo2"]
        PanelTypeList[i]["memo3"] = PanelTypeList[i]["memo3"]
        PanelTypeList[i]["bdfile"] = PanelTypeList[i]["bdfile"]
    PanelTypeListcontent = json.dumps(PanelTypeList).encode('gbk')

    r.set((myversion + 'mSlidingExpList').encode('utf8'), mSlidingExpListcontent)
    r.set((myversion + 'mSlidingTypeList').encode('utf8'), mSlidingTypeListcontent)
    r.set((myversion + 'mSlidingParamList').encode('utf8'), SlidingParamcontent)
    r.set((myversion + 'mUDBoxParamList').encode('utf8'), UDBoxParamcontent)
    r.set((myversion + 'mTrackParamList').encode('utf8'), TrackParamcontent)
    r.set((myversion + 'mHBoxParamList').encode('utf8'), HBoxParamcontent)
    r.set((myversion + 'PanelTypeList').encode('utf8'), PanelTypeListcontent)
    r.set((myversion + 'mSlidingColorList').encode('utf8'), mSlidingColorListcontent)
    r.set((myversion + 'mSlidingColorClassList').encode('utf8'), mSlidingColorClassListcontent)
    r.set((myversion + 'mSlidingWjBomDetailList').encode('utf8'), mSlidingWjBomDetailListcontent)
    r.set((myversion + 'mSSExpList').encode('utf8'), mSSExpListcontent)
    r.set((myversion + 'mSlidingAccessoryList').encode('utf8'), mSlidingAccessoryListcontent)
    r.set((myversion + 'mVBoxParamList').encode('utf8'), mVBoxParamListcontent)
    r.set((myversion + 'mPanelBomDetailList').encode('utf8'), mPanelBomDetailListcontent)
    r.set((myversion + 'UHBoxParam').encode('utf8'), UHBoxParamcontent)
    r.set((myversion + 'UHBoxParam').encode('utf8'), UHBoxParamcontent)
    r.set((myversion + 'HHBoxParam').encode('utf8'), HHBoxParamcontent)
    r.set((myversion + 'Cfgobj2').encode('utf8'), Cfgobj2content)
    r.set((myversion + 'Cfgobj3').encode('utf8'), Cfgobj3content)
    r.set((myversion + 'Cfgobj4').encode('utf8'), Cfgobj4content)
    r.set((myversion + 'SHBoxParam').encode('utf8'), SHBoxParamcontent)
    r.set((myversion + 'HCfgobj2').encode('utf8'), HCfgobj2content)
    r.set((myversion + 'HCfgobj3').encode('utf8'), HCfgobj3content)
    r.set((myversion + 'HCfgobj4').encode('utf8'), HCfgobj4content)
    r.set((myversion + 'HSHBoxParam').encode('utf8'), HSHBoxParamcontent)
    r.set((myversion + 'cfglist').encode('utf8'), cfglistcontent)

def AddDataToDBD(myversion):
    # RootPath = ServerPath + RootName
    # adb = db.DB()
    # adb.open(RootPath+'\\SlidADoorDBD', dbtype=db.DB_HASH, flags=db.DB_CREATE)
    # #adb.put('data'.encode('utf8'), '1')
    # for key, data in irecords(adb.cursor()):
    #     if key == RootName.encode('utf8'):
    #         return 1
    # adb.put(RootName.encode('utf8'), '1')
    # #将趟门掩门数据加入到dbd数据库
    # RootPath = ServerPath + RootName
    # SlidingInitData(adb, RootName, RootPath)
    # DoorInitData(adb, RootName, RootPath)
    # adb.close()
    # return 0

    mExpListdata = r.get(myversion + 'mExpList')
    if not mExpListdata:
        DoorInitData(myversion, RootPath)
        SlidingInitData(myversion, RootPath)
    return 1

def irecords(curs):
    record = curs.first()
    while record:
        yield record
        record = curs.next()

class ReturnConfig(BaseHandler):
    # 获取趟门，掩门配置数据
    async def post(self):
        global RootPath
        Result = {'result': 0}
        xml = self.get_argument('xml', '').encode('utf8')
        RootName = self.get_argument('rootname', None)
        if RootName:
            RootPath = ServerPath + RootName
        else:
            RootPath = base_dir
        if (not os.path.exists(RootPath)) or (not xml):
            Result['result'] = -1
            self.write(json.dumps(Result, ensure_ascii=False).encode('utf8'))
            return
        version = r.get(RootName + 'Verison')
        if not version:
            r.set(RootName + 'Verison', '0.01')
            version = '0.01'
        myversion = RootName + version.decode('utf8')
        AddDataToDBD(myversion)
        if not os.path.exists(RootPath + '\\Python\\ConfigWebcache\\'):
            os.makedirs(RootPath + '\\Python\\ConfigWebcache\\')
        m2 = hashlib.md5()
        m2.update(xml)
        pricedatamd5 = m2.hexdigest()


        # if os.path.exists(RootPath + '\\Python\\ConfigWebcache\\'+pricedatamd5):
        #     with open(RootPath + '\\Python\\ConfigWebcache\\'+pricedatamd5, 'r', encoding='utf8') as f:
        #         Bomjson =f.read()
        #         self.write(Bomjson)
        # else:
        UpLoadXmlPath = RootPath + '\\Python\\UpLoadXml\\'
        if (not os.path.exists(UpLoadXmlPath)):
            os.makedirs(UpLoadXmlPath)
        guid = str(uuid.uuid1())  # 唯一标识符guid
        guid = ''.join(guid.split('-'))
        with open(UpLoadXmlPath + guid, 'w+', encoding='utf8') as f:
            f.write(xml.decode('utf8'))
        # 本地测试版
        result =await self.calresult(RootPath,myversion,pricedatamd5,UpLoadXmlPath,guid)
        print('result=',1)
        self.finish(result)

    async def calresult(self, RootPath,myversion,pricedatamd5,UpLoadXmlPath,guid):
        res = await LoadXML2Bom(UpLoadXmlPath + guid, myversion, RootPath)

        print("after yielded")
        if not os.path.exists(RootPath + '\\Python\\ConfigWebcache\\'):
            os.makedirs(RootPath + '\\Python\\ConfigWebcache\\')
        with open(RootPath + '\\Python\\ConfigWebcache\\' + pricedatamd5, 'w+', encoding='utf8') as f:
            f.write(res.decode('utf8'))
        os.remove(UpLoadXmlPath + guid)
        return res



class ReturnPriceConfig(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(8)
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,access_token")
        # 这里要填写上请求带过来的Access-Control-Allow-Headers参数，如access_token就是我请求带过来的参数
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE")  # 请求允许的方法
        self.set_header("Access-Control-Max-Age", "3600")  # 用来指定本次预检请求的有效期，单位为秒，，在此期间不用发出另一条预检请求。

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        http_client = httpclient.AsyncHTTPClient()
        http_client.fetch(self.request, callback=self.process)

    #def get(self, *args, **kwargs):
    @tornado.web.asynchronous
    def process(self, response):
        print("---网络报价配置数据---")
        Result = {'result': 0}
        name = self.get_argument('name').encode('utf8')
        slidingDoor = self.get_argument("slidingDoor").encode('utf8')
        swingDoor = self.get_argument("swingDoor").encode('utf8')
        RootName = self.get_argument('rootname', None)

        name = json.loads(name, encoding='utf8')
        slidingDoor = json.loads(slidingDoor, encoding='utf8')
        swingDoor = json.loads(swingDoor, encoding='utf8')

        if RootName:
            RootPath = ServerPath + RootName
            if not os.path.exists(RootPath):
                Result['result'] = -1
                self.write(json.dumps(Result, ensure_ascii=False).encode('utf8'))
                return
        else:
            RootPath = base_dir
        version = r.get(RootName + 'Verison')
        if not version:
            r.set(RootName + 'Verison', '0.01')
            version = '0.01'
        myversion = RootName + version.decode('utf8')
        print('RootPath='+RootPath)
        data = NetworkQuoteConfigData.GetNetworkQuoteConfigHandl(name, slidingDoor, swingDoor, RootPath,myversion)
        result = json.dumps(data, ensure_ascii=False).encode('utf8')
        self.write(result)
        self.finish()

    @run_on_executor
    def post(self, *args, **kwargs):
        print("---网络报价配置数据---")
        Result = {'result': 0}
        name = self.get_argument('name').encode('utf8')
        slidingDoor = self.get_argument("slidingDoor").encode('utf8')
        swingDoor = self.get_argument("swingDoor").encode('utf8')
        RootName = self.get_argument('rootname', None)

        name = json.loads(name, encoding='utf8')
        slidingDoor = json.loads(slidingDoor, encoding='utf8')
        swingDoor = json.loads(swingDoor, encoding='utf8')

        if RootName:
            RootPath = ServerPath + RootName
            if not os.path.exists(RootPath):
                Result['result'] = -1
                self.write(json.dumps(Result, ensure_ascii=False).encode('utf8'))
                return
        else:
            RootPath = base_dir
        version = r.get(RootName + 'Verison')
        if not version:
            r.set(RootName + 'Verison', '0.01')
            version = '0.01'
        myversion = RootName + version.decode('utf8')
        print('RootPath=' + RootPath)
        data = NetworkQuoteConfigData.GetNetworkQuoteConfigHandl(name, slidingDoor, swingDoor, RootPath, myversion)
        result = json.dumps(data, ensure_ascii=False).encode('utf8')
        self.write(result)
        #self.finish()

application = tornado.web.Application([
    (r"/exit_localserver", ExitSystem),  # 退出程序
    (r"/XmlToJson/", XmlToJson),
    (r"/Price/ReturnBomConfig/", ReturnConfig),
    (r"/Price/ReturnPriceConfig/", ReturnPriceConfig),
    (r"/(.*)", IndexHandler, {"path": webpath}),  # 查找文件
],autoreload=True,
template_path = ServerPath)
template_path='templates'
static_path='static'
if __name__ == '__main__':
    print("***服务器启动***")
    print(("端口号：", options.port))
    threadLock = threading.Lock()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except:
        pass