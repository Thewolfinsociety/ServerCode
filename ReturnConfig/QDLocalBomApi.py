# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# @Time : 2019/11/01 9:38
#
# @Author : litao
#
# @File : Qdbom.py version1.0
import sys
import time
import os
from ctypes import *
import json
import logging
import datetime
import logging.config

from GetSlidingAndDoorConfig import *

def genLogDict(logDir, logFile):
    '''
    配置日志格式的字典
    '''
    logDict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
            },
            'standard': {
                'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
            },
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },

            "default": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": os.path.join(logDir, logFile),
                'mode': 'w+',
                "maxBytes": 1024*1024*5,  # 5 MB
                "backupCount": 20,
                "encoding": "utf8"
            },
        },

        # "loggers": {
        #     "app_name": {
        #         "level": "INFO",
        #         "handlers": ["console"],
        #         "propagate": "no"
        #     }
        # },

        "root": {
            'handlers': ['default'],
            'level': "DEBUG",
            'propagate': False
        }
    }
    return logDict

def initLogConf():
    """
    配置日志
    """
    baseDir = os.path.dirname(os.path.abspath(__file__))
    logDir = os.path.join(baseDir, "logs")
    if not os.path.exists(logDir):
        os.makedirs(logDir)  # 创建路径

    logFile = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
    logDict = genLogDict(logDir, logFile)
    logging.config.dictConfig(logDict)



initLogConf()
_logging = logging.getLogger(__file__)
# logging.basicConfig(level="DEBUG")
# _logging = logging.getLogger(__file__)
_logging.info('scenexmlname=')
QdUpTemplatePath = os.path.abspath(os.path.join(os.getcwd()))+'\\QDLocalBomApi.dll'
print (QdUpTemplatePath)
QdUp = windll.LoadLibrary(QdUpTemplatePath)
#QdUpTemplatePath = 'Project2.dll'.encode('gbk')
# print os.getcwd(),os.path.dirname(sys.executable)
# print os.path.abspath(os.path.join(os.getcwd()))


filename =os.path.abspath(os.path.join(os.getcwd()))+ '\\Python3\\ReturnConfig\\123xml.txt'


base_dir = os.path.abspath(os.path.join(os.getcwd(),'..'))
print ('2=',base_dir)
ServerPath = os.path.abspath(os.path.join(os.getcwd(),'../..'))+'\\nginx-1.0.11\\nginx-1.0.11\html\\data'
config = ''
# try:
#     config = LoadXML2Bom(filename, ServerPath)
# except Exception as e:
#     print (e)
#     config = ''
#print config.keys()
with open(filename ,'r', encoding='gbk') as f:
    mScendXML = f.read().encode('gbk')
_logging.info('scenexmlname='+filename)



def returnconfig(config = '', state = True):
    if state:
        configjson = json.dumps(config, ensure_ascii=False).encode('gbk')
    else:
        with open(os.path.abspath(os.path.join(os.getcwd())) + '\\Python\\ReturnConfig\\allconfig.txt', 'r') as f:
            configjson = f.read()
    return configjson


config = {
        'ymconfig': {
            'mExpList': [],
            'mTypeList': [],
            'mParamList': [],
            'mHandleList': [],
            'mHingeList': [],
            'mDoorHBoxParamList': [],
            'mDoorPanelTypeList': [],
            'mAccessoryList': [],
            'mColorClassList': [],
            'mColorClass2List': [],
            'mShutterExpList': [],
            'mWJBomList': [],
            'mWJBomDetailList': [],
            'mDoorPanelBomDetailList': [],
            'mDoorXMLList': []
        },
        'tmconfig': {
            'SlidingExp': [],  # 1.单门数量类型
            'SlidingType': [],  # 2.门类型
            'SlidingParam': [],  # 3.边框类型
            'UDBoxParam': [],  # 4.上下横框类型
            'TrackParam': [],  # 5.趟门上下轨参数
            'HBoxParam': [],  # 6.趟门中横框
            'VBoxParam': [],  # 7.竖框参数
            'SlidingColor': [],  # 8.颜色分类2
            'PanelType': [],  # 9.门板类型
            'SlidingAccessory': [],  # 10.五金配件
            'SlidingColorClass': [],  # 11.颜色分类
            'SSExp': [],  # 12.百叶板计算公式
            'SlidingWjBomDetail': [],  # 13.五金配件分类数据
            'PanelBomDetail': [],  # 14.门板附加物料
            'Cfglist': [],  # 15.门转换表
            'Hfg2': [],  # 16.趟门2横分格
            'Hfg3': [],  # 17.趟门3横分格
            'Hfg4': [],  # 18.趟门4横分格
            'Sfg2': [],  # 19.趟门2竖分格
            'Sfg3': [],  # 20.趟门3竖分格
            'Sfg4': [],  # 21.趟门4竖分格
            'HSHBoxParam': [],  # 22.横中横 HSHBoxParam
            'SHBoxParam': [],  # 23.竖中横 SHBoxParam
            'SfgParam': {},  # 24 xml
        },
        'gtconfig':{
            'qdsoft_id':'data',
            'UrlIp':'http://129.204.134.85:8002/Qdbom'
        }
}

# configjson = returnconfig(config)

if __name__ == '__main__':
    QdUp.InitData()
    try:
        with open(os.path.abspath(os.path.join(os.getcwd()))+ '\\Python3\\ReturnConfig\\123config.txt','r',encoding='utf8') as f:
            configjson = f.read().encode('utf8')
        print(configjson)
        result = QdUp.GetXmlDes(c_char_p(mScendXML), c_char_p(configjson))
        desjsonStr = c_char_p(result).value
        print (desjsonStr.decode('gbk'))
        _logging.info( 'desjson='+ desjsonStr.decode('gbk'))
        desjson = json.loads(desjsonStr.decode('gbk'))
        _logging.info('slidingdeslist='+str(len(desjson['slidingdeslist']))) #'趟门类别列表'
        _logging.info('doordeslist='+str(len(desjson['doordeslist'])))   #'掩门类别列表'
        _logging.info('bomdeslist='+str(len(desjson['bomdeslist'])))   #'板件类别列表'
        _logging.info('door=' + str(len(desjson['door'])))  # '板件类别列表'
        _logging.info('sliding=' + str(len(desjson['sliding'])))  # '板件类别列表'
        #_logging.debug( desjson['door'] )   #掩门数据

        #print len(desjson['slidingdeslist'])
        doorjson = desjson['door']    #'掩门数据'
        slidingjson = desjson['sliding']  # '掩门数据'
        # print slidingstr
        # print type(slidingstr)
        # slidingjson = json.loads(slidingstr, encoding='gbk')
        # for oneslide in doorjson:
        #     print u'物料',oneslide[u'物料']

        #for onedoor in doorjson
        name = input("name")
        os.system("pause")
    except Exception as e:
        print (e)
        name = input("name")
        os.system("pause")
    finally:
        name = input("name")
        os.system("pause")

name = input("name")
os.system("pause")
QdUp.UnInitData()

# print config.keys(),len(config.keys())
#     五金配件'pbomdetail',SlidingColor    颜色分类2, PanelType    门板类型 PanelType    五金配件 SlidingAccessory
#     颜色分类 SlidingColorClass    #SSExp    百叶板计算公式   五金配件分类数据 SlidingWjBomDetail
#     PanelBomDetail 门板附加物料
#
#     config = {
#         ''
#     }
