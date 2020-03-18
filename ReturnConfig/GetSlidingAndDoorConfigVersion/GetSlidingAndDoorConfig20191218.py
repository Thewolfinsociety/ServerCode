# -*- coding: utf-8 -*-
'''
服务器版
功能：返回趟门掩门配置
vesion 1.0.2
2019/12/12
author:litao
'''
from xml.dom import minidom
import logging
import os
import sys
import math
import pypyodbc
import traceback
from lupa import LuaRuntime
import threading
import time


if os.getcwd()+'\\Python3\\' not in sys.path:
    sys.path.append(os.getcwd()+'\\Python3\\')
if os.getcwd() + '\\Python3\\PythontoBomJson' not in sys.path:
    sys.path.append(os.getcwd() + '\\Python3\\PythontoBomJson')
if os.getcwd() + '\\Python3\\ReturnConfig' not in sys.path:
    sys.path.append(os.getcwd() + '\\Python3\\ReturnConfig')

from ReturnConfig.SlidingAndDoor.funcGetSlidingJson import *
from ReturnConfig.SlidingAndDoor.funcGetDoorJson import *
from ExpValue import GetExpValue
SADlog = logging.getLogger()
threadLock = threading.Lock()

log_dir = "log"  # 日志存放文件夹名称
log_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), log_dir)
if not os.path.isdir(log_path):
    os.makedirs(log_path)
# logger = logging.getLogger()
# logger.setLevel(logging.ERROR)
def outputlog():
    main_log_handler = logging.FileHandler(log_path +
                                           "/SAD_%s.log" % time.strftime("%Y-%m-%d_%H-%M-%S",
                                                                         time.localtime(time.time())), mode="w+",
                                           encoding="utf-8")
    main_log_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    main_log_handler.setFormatter(formatter)
    SADlog.addHandler(main_log_handler)

    # 控制台打印输出日志
    console = logging.StreamHandler()  # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象
    console.setLevel(logging.INFO)  # 设置要打印日志的等级，低于这一等级，不会打印
    formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
outputlog()
#举例查看log的形式
SADlog.setLevel(logging.ERROR)
Sliding = {
        'SfgParam': {
            'HTxml': '<产品 名称="横2格门" 类别="" 摆放方式="整块;左右延伸:-1;前后延伸:-1;上下延伸:-1;尺寸限制:1,1220,1,1220,1,2430;" 装饰类别="趟门" 材料="" 颜色="" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" LgwjFlag="0"><摆放规则列表/><变量列表></变量列表><我的模块><板件 名称="门芯1" X="0" Y="$门芯1前偏移" Z="0" 宽="$门芯1宽度" 深="$门芯1厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="1" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="1"/><板件 名称="竖中横1" X="$门芯1宽度-$竖中横进槽" Y="0" Z="0" 宽="L" 深="$竖中横厚度" 高="$竖中横宽度" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="2"/><板件 名称="门芯2" X="$门芯1宽度+$竖中横宽度-2*$竖中横进槽" Y="$门芯2前偏移" Z="0" 宽="L-$门芯1宽度-$竖中横宽度+2*$竖中横进槽" 深="$门芯2厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="1" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="3"/></我的模块><我的规格><规格 名称="竖2格门" 宽="800" 深="20" 高="1000"/></我的规格></产品>',
            'Txml': '<产品 名称="竖2格门" 类别="" 摆放方式="整块;左右延伸:-1;前后延伸:-1;上下延伸:-1;尺寸限制:1,1220,1,1220,1,2430;" 装饰类别="趟门" 材料="" 颜色="" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" LgwjFlag="0"><摆放规则列表/><变量列表></变量列表><我的模块><板件 名称="门芯1" X="0" Y="$门芯1前偏移" Z="0" 宽="$门芯1宽度" 深="$门芯1厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="1" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="1"/><板件 名称="竖中横1" X="$门芯1宽度-$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横宽度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="1" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="2"/><板件 名称="门芯2" X="$门芯1宽度+$竖中横宽度-2*$竖中横进槽" Y="$门芯2前偏移" Z="0" 宽="L-$门芯1宽度-$竖中横宽度+2*$竖中横进槽" 深="$门芯2厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="1" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="3"/></我的模块><我的规格><规格 名称="竖2格门" 宽="800" 深="20" 高="1000"/></我的规格></产品>',
            'Sxml': '<产品 名称="竖3格门_两边均分" 类别="" 摆放方式="整块;左右延伸:-1;前后延伸:-1;上下延伸:-1;尺寸限制:1,1220,1,1220,1,2430;" 装饰类别="趟门" 材料="" 颜色="" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" LgwjFlag="0"><摆放规则列表/><变量列表></变量列表><我的模块><板件 名称="门芯1" X="0" Y="$门芯1前偏移" Z="0" 宽="(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2" 深="$门芯1厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="1" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="1"/><板件 名称="竖中横1" X="(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2-$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="1" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="2"/><板件 名称="门芯2" X="(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2+$竖中横宽度-2*$竖中横进槽" Y="$门芯2前偏移" Z="0" 宽="$门芯2宽度" 深="$门芯2厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="3"/><板件 名称="竖中横2" X="L-(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2-$竖中横宽度+$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="1" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="4"/><板件 名称="门芯3" X="L-(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2" Y="$门芯3前偏移" Z="0" 宽="(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2" 深="$门芯3厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="1" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="5"/></我的模块><我的规格><规格 名称="竖3格门" 宽="800" 深="20" 高="1000"/></我的规格></产品>',
            'Fxml': '<产品 名称="竖4格门_改123" 类别="" 摆放方式="整块;左右延伸:-1;前后延伸:-1;上下延伸:-1;尺寸限制:1,1220,1,1220,1,2430;" 装饰类别="趟门" 材料="" 颜色="" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" LgwjFlag="0"><摆放规则列表/><变量列表></变量列表><我的模块><板件 名称="门芯1" X="0" Y="$门芯1前偏移" Z="0" 宽="$门芯1宽度" 深="$门芯1厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="1"/><板件 名称="竖中横1" X="$门芯1宽度-$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="4" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="2"/><板件 名称="门芯2" X="$门芯1宽度+$竖中横宽度-2*$竖中横进槽" Y="$门芯2前偏移" Z="0" 宽="$门芯2宽度" 深="$门芯2厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="3"/><板件 名称="竖中横2" X="$门芯1宽度+$门芯2宽度+$竖中横宽度-3*$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="4" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="4"/><板件 名称="门芯3" X="$门芯1宽度+$门芯2宽度+2*$竖中横宽度-4*$竖中横进槽" Y="$门芯3前偏移" Z="0" 宽="$门芯3宽度" 深="$门芯3厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="5"/><板件 名称="竖中横3" X="$门芯1宽度+$门芯2宽度+$门芯3宽度+2*$竖中横宽度-5*$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="4" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="6"/><板件 名称="门芯4" X="L-(L-$门芯1宽度-$门芯2宽度-$门芯3宽度-3*$竖中横宽度+6*$竖中横进槽)" Y="$门芯4前偏移" Z="0" 宽="L-$门芯1宽度-$门芯2宽度-$门芯3宽度-3*$竖中横宽度+6*$竖中横进槽" 深="$门芯4厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="7"/></我的模块><我的规格><规格 名称="竖3格门" 宽="900" 深="20" 高="1000"/></我的规格></产品>',
            'HSxml': '<产品 名称="横3格门_两边均分" 类别="" 摆放方式="整块;左右延伸:-1;前后延伸:-1;上下延伸:-1;尺寸限制:1,1220,1,1220,1,2430;" 装饰类别="趟门" 材料="" 颜色="" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" LgwjFlag="0"><摆放规则列表/><变量列表></变量列表><我的模块><板件 名称="门芯1" X="0" Y="$门芯1前偏移" Z="0" 宽="(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2" 深="$门芯1厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="1" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="1"/><板件 名称="竖中横1" X="(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2-$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="2"/><板件 名称="门芯2" X="(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2+$竖中横宽度-2*$竖中横进槽" Y="$门芯2前偏移" Z="0" 宽="$门芯2宽度" 深="$门芯2厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="3"/><板件 名称="竖中横2" X="L-(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2-$竖中横宽度+$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="4"/><板件 名称="门芯3" X="L-(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2" Y="$门芯3前偏移" Z="0" 宽="(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2" 深="$门芯3厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="1" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="5"/></我的模块><我的规格><规格 名称="竖3格门" 宽="800" 深="20" 高="1000"/></我的规格></产品>',
            'HFxml': '<产品 名称="横4格门_改123" 类别="" 摆放方式="整块;左右延伸:-1;前后延伸:-1;上下延伸:-1;尺寸限制:1,1220,1,1220,1,2430;" 装饰类别="趟门" 材料="" 颜色="" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" LgwjFlag="0"><摆放规则列表/><变量列表></变量列表><我的模块><板件 名称="门芯1" X="0" Y="$门芯1前偏移" Z="0" 宽="$门芯1宽度" 深="$门芯1厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="1"/><板件 名称="竖中横1" X="$门芯1宽度-$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="2"/><板件 名称="门芯2" X="$门芯1宽度+$竖中横宽度-2*$竖中横进槽" Y="$门芯2前偏移" Z="0" 宽="$门芯2宽度" 深="$门芯2厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="3"/><板件 名称="竖中横2" X="$门芯1宽度+$门芯2宽度+$竖中横宽度-3*$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="4"/><板件 名称="门芯3" X="$门芯1宽度+$门芯2宽度+2*$竖中横宽度-4*$竖中横进槽" Y="$门芯3前偏移" Z="0" 宽="$门芯3宽度" 深="$门芯3厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="5"/><板件 名称="竖中横3" X="$门芯1宽度+$门芯2宽度+$门芯3宽度+2*$竖中横宽度-5*$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="6"/><板件 名称="门芯4" X="L-(L-$门芯1宽度-$门芯2宽度-$门芯3宽度-3*$竖中横宽度+6*$竖中横进槽)" Y="$门芯4前偏移" Z="0" 宽="L-$门芯1宽度-$门芯2宽度-$门芯3宽度-3*$竖中横宽度+6*$竖中横进槽" 深="$门芯4厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="7"/></我的模块><我的规格><规格 名称="竖3格门" 宽="900" 深="20" 高="1000"/></我的规格></产品>'},
    }




class PDoorsParam(object):    #掩门参数
    def __init__(self):
        self.id = 0
        self.deleted = False
        self.name = ''
        self.DoorsType = ''
        self.handle = ''
        self.wjname = ''
        self.hboxname = ''
        self.paneltype = ''
        self.cap = 0
        self.eb_cap = 0
        self.vboxname = ''
        self.udboxname = ''
        self.vboxl = ''
        self.udboxl = ''
        self.vboxh = 0
        self.udboxh = 0
        self.vthick = 0
        self.udthick = 0
        self.vboxjtw = 0
        self.udboxjtw = 0
        self.hboxjtw = 0
        self.udbox_hbox_value = 0
        self.d3name = ''
        self.hbox3d = ''
        self.ubox3d = ''
        self.dbox3d = ''
        self.cpm_lmax = 0
        self.cpm_hmax = 0
        self.vdirect = ''
        self.vfbstr = ''
        self.uddirect = ''
        self.udfbstr = ''
        self.vmemo = ''
        self.udmemo = ''
        self.fbstr = ''
        self.iscalc_framebom = 0
        self.is_xq = 0
        self.cb_yyvalue = 0
        self.is_buy = 0
        self.frame_valuel = 0
        self.frame_valueh = 0
        self.bomtype = ''
        self.left_doorxml = ''
        self.right_doorxml = ''
        self.doorxml = ''
        self.bdfile = ''
        self.l_bdfile = ''
        self.r_bdfile = ''
        self.u_bdfile = ''
        self.d_bdfile = ''
        self.noframe_bom = 0

class TDoorDoorRect(object):
    def __init__(self):
        self.x0 = 0
        self.y0 = 0
        self.doorw = 0
        self.doorh = 0
        self.x1 = 0
        self.y1 = 0
        self.doorw1 = 0
        self.doorh1 = 0
        self.selected = False
        self.hhdraw = False
        self.mOpenDirect = '' #开门方向
        self.mMemo = ''
        self.mDoorW = 0
        self.mDoorH = 0
        self.mVBoxW = 0
        self.mUDBoxH = 0
        self.mVBoxW0 = 0
        self.mUDBoxH0 = 0
        self.mHandle = ''
        self.mHandlePos = ''
        self.mHandlePosX = ''
        self.mHandlePosY = ''
        self.mHandleX = 0
        self.mHandleY = 0
        self.mHandleW = 0
        self.mHandleH = 0
        self.mHinge = ''
        self.mHingeCt = ''
        self.mIsFrame = False
        self.mHHArr = []
        self.mPanelType = ''
        self.mPanelColor = ''
        self.boxlist = []
        self.panellist = []
        self.mYPos = 0
        self.mPParam = PDoorsParam()
        self.mHingeHoleDes = ''
        self.mHingeHoleParam = ''
        self.mHingeHoleExtra = ''

class TDoorRect(object):
    def __init__(self):
        self.doorw = 0
        self.doorh = 0
        self.x0 = 0
        self.y0 = 0
        self.doorw2 = 0
        self.doorh2 = 0
        self.selected = False
        self.mUDBoxParam = {}
        self.mVBoxParam = {}
        self.mPanelType = ''
        self.mPanelColor = ''
        self.mVBoxColor = ''
        self.boxlist = []
        self.panellist = []
        self.mYPos = 0

class DoorRectPanel(object):
    def __init__(self):
        self.selected = False
        self.w0 = 0                  #可视
        self.h0 = 0
        self.x0 = 0
        self.y0 = 0
        self.d0 = 0
        self.w1 = 0
        self.h1 = 0
        self.x1 = 0
        self.y1 = 0
        self.d1 = 0
        self.w2 = 0
        self.h2 = 0
        self.x2 = 0
        self.y2 = 0
        self.d2 = 0
        self.PanelType = ''
        self.color = ''
        self.direct =''
        self.pricetype = ''
        self.color2 = ''
        self.price = 0
        self.price2 = 0
        self.thick = 0

class RectPanel(object):
    def __init__(self):
        self.selected = False
        self.w0 = 0                  #可视
        self.h0 = 0
        self.x0 = 0
        self.y0 = 0
        self.d0 = 0
        self.w1 = 0
        self.h1 = 0
        self.x1 = 0
        self.y1 = 0
        self.d1 = 0
        self.w2 = 0
        self.h2 = 0
        self.x2 = 0
        self.y2 = 0
        self.d2 = 0
        self.PanelType = ''
        self.color = ''
        self.direct =''
        self.memo = ''
        self.pricetype = ''
        self.color2 = ''
        self.price = 0
        self.price2 = 0
        self.extradata = ''

class DoorRectBox(object):
    def __init__(self):
        self.vh = False
        self.selected = False
        self.w0 = 0                  #可视
        self.h0 = 0
        self.x0 = 0
        self.y0 = 0
        self.d0 = 0
        self.w1 = 0
        self.h1 = 0
        self.x1 = 0
        self.y1 = 0
        self.d1 = 0
        self.w2 = 0
        self.h2 = 0
        self.x2 = 0
        self.y2 = 0
        self.d2 = 0
        self.boxtype = ''
        self.color = ''

def InitBomOrderItem(PBomOrderItem):
    PBomOrderItem['cid'] = 0
    PBomOrderItem['id'] = 0
    PBomOrderItem['pid'] = -1
    PBomOrderItem['seq'] = 0
    PBomOrderItem['classseq'] = 0
    PBomOrderItem['mark'] = 0
    PBomOrderItem['vp'] = 0
    # 新加属性
    PBomOrderItem['code'] = ''
    PBomOrderItem['name'] = ''
    PBomOrderItem['mat'] = ''
    PBomOrderItem['mat2'] = ''
    PBomOrderItem['mat3'] = ''
    PBomOrderItem['color'] = ''
    PBomOrderItem['workflow'] = ''
    PBomOrderItem['pl'] = 0
    PBomOrderItem['pd'] = 0
    PBomOrderItem['ph'] = 0
    PBomOrderItem['space_x'] = 0
    PBomOrderItem['space_y'] = 0
    PBomOrderItem['space_z'] = 0
    PBomOrderItem['space_id'] = 0
    PBomOrderItem['gcl'] = 0
    PBomOrderItem['gcd'] = 0
    PBomOrderItem['gch'] = 0
    PBomOrderItem['gcl2'] = 0
    PBomOrderItem['gcd2'] = 0
    PBomOrderItem['gch2'] = 0
    PBomOrderItem['tmp_soz'] = ''

    PBomOrderItem['lx'] = 0
    PBomOrderItem['ly'] = 0
    PBomOrderItem['lz'] = 0
    PBomOrderItem['x'] = 0
    PBomOrderItem['y'] = 0
    PBomOrderItem['z'] = 0
    PBomOrderItem['l'] = 0
    PBomOrderItem['p'] = 0
    PBomOrderItem['h'] = 0
    PBomOrderItem['gl'] = 0
    PBomOrderItem['gp'] = 0
    PBomOrderItem['gh'] = 0
    PBomOrderItem['holeflag'] = 0
    PBomOrderItem['linemax'] = 0
    PBomOrderItem['holetype'] = 0

    PBomOrderItem['ox'] = 0
    PBomOrderItem['oy'] = 0
    PBomOrderItem['oz'] = 0
    PBomOrderItem['childnum'] = 0

    PBomOrderItem['desc'] = ''
    PBomOrderItem['bomdes'] = ''
    PBomOrderItem['bomwjdes'] = ''
    PBomOrderItem['bomstddes'] = ''
    PBomOrderItem['childbom'] = ''
    PBomOrderItem['myclass'] = ''
    PBomOrderItem['nodename'] = ''
    PBomOrderItem['linecalc'] = ''
    PBomOrderItem['bomstd'] = ''
    PBomOrderItem['bg'] = ''

    PBomOrderItem['direct'] = 0
    PBomOrderItem['lgflag'] = 0
    PBomOrderItem['holeid'] = 0
    PBomOrderItem['kcid'] = 0
    PBomOrderItem['num'] = 0

    PBomOrderItem['lfb'] = 0
    PBomOrderItem['llk'] = 0
    PBomOrderItem['wfb'] = 0
    PBomOrderItem['wlk'] = 0
    PBomOrderItem['llfb'] = 0
    PBomOrderItem['rrfb'] = 0
    PBomOrderItem['ddfb'] = 0
    PBomOrderItem['uufb'] = 0
    PBomOrderItem['fb'] = 0

    PBomOrderItem['holestr'] = ''
    PBomOrderItem['kcstr'] = ''

    PBomOrderItem['memo'] = ''
    PBomOrderItem['gno'] = ''
    PBomOrderItem['gdes'] = ''
    PBomOrderItem['gcb'] = ''
    PBomOrderItem['extra'] = ''
    PBomOrderItem['fbstr'] = ''
    PBomOrderItem['subspace'] = ''
    PBomOrderItem['process'] = ''

    PBomOrderItem['ls'] = ''
    PBomOrderItem['myunit'] = ''
    PBomOrderItem['bomtype'] = ''
    PBomOrderItem['bdxmlid'] = ''
    PBomOrderItem['user_fbstr'] = ''

    PBomOrderItem['bl'] = 0
    PBomOrderItem['bp'] = 0
    PBomOrderItem['bh'] = 0

    PBomOrderItem['var_names'] = [''] * 16
    PBomOrderItem['var_args'] = [0] * 16

    PBomOrderItem['value_lsk'] = 0
    PBomOrderItem['value_rsk'] = 0
    PBomOrderItem['value_zk'] = 0
    PBomOrderItem['value_zs'] = 0
    PBomOrderItem['value_ls'] = 0
    PBomOrderItem['value_lg'] = 0
    PBomOrderItem['value_ltm'] = 0
    PBomOrderItem['value_rtm'] = 0

    PBomOrderItem['a_hole_info'] = ''
    PBomOrderItem['b_hole_info'] = ''
    PBomOrderItem['holeinfo'] = ''

    PBomOrderItem['isoutput'] = True
    PBomOrderItem['is_outline'] = False
    PBomOrderItem['outputtype'] = ''
    PBomOrderItem['holeconfig_flag'] = ''
    PBomOrderItem['kcconig_flag'] = ''
    PBomOrderItem['bg_data'] = ''

    PBomOrderItem['mBGParam'] = ''

    PBomOrderItem['bg_filename'] = ''
    PBomOrderItem['mpr_filename'] = ''
    PBomOrderItem['bpp_filename'] = ''
    PBomOrderItem['devcode'] = ''


    PBomOrderItem['zero_y'] = 0
    PBomOrderItem['direct_calctype'] = 0
    PBomOrderItem['youge_holecalc'] = 0

    PBomOrderItem['is_output_bgdata'] = 0
    PBomOrderItem['is_output_mpr'] = 0
    PBomOrderItem['is_output_bpp'] = 0

    PBomOrderItem['bg_l_minx'] = 0
    PBomOrderItem['bg_l_maxx'] = 0
    PBomOrderItem['bg_r_minx'] = 0
    PBomOrderItem['bg_r_maxx'] = 0

    PBomOrderItem['bg_d_minx'] = 0
    PBomOrderItem['bg_d_maxx'] = 0
    PBomOrderItem['bg_u_minx'] = 0
    PBomOrderItem['bg_u_maxx'] = 0

    PBomOrderItem['bg_b_minx'] = 0
    PBomOrderItem['bg_b_maxx'] = 0
    PBomOrderItem['bg_f_minx'] = 0
    PBomOrderItem['bg_f_maxx'] = 0

    PBomOrderItem['bg_l_miny'] = 0
    PBomOrderItem['bg_l_maxy'] = 0
    PBomOrderItem['bg_r_miny'] = 0
    PBomOrderItem['bg_r_maxy'] = 0

    PBomOrderItem['bg_d_miny'] = 0
    PBomOrderItem['bg_d_maxy'] = 0
    PBomOrderItem['bg_u_miny'] = 0
    PBomOrderItem['bg_u_maxy'] = 0

    PBomOrderItem['bg_b_miny'] = 0
    PBomOrderItem['bg_b_maxy'] = 0
    PBomOrderItem['bg_f_miny'] = 0
    PBomOrderItem['bg_f_maxy'] = 0

    PBomOrderItem['hole_back_cap'] = 0
    PBomOrderItem['hole_2_dist'] = 0
    PBomOrderItem['trans_ab'] = False
    PBomOrderItem['ahole_index'] = [-1] * 101
    PBomOrderItem['bhole_index'] = [-1] * 101

    PBomOrderItem['akc_index'] = [-1] * 101
    PBomOrderItem['bkc_index'] = [-1] * 101

    PBomOrderItem['is_calc_holeconfig'] = [0] * 6
    PBomOrderItem['parent'] = None
    PBomOrderItem['basewj_price'] = ''
    PBomOrderItem['extend'] = ''
    PBomOrderItem['group'] = ''
    PBomOrderItem['packno'] = ''
    PBomOrderItem['userdata'] = ''
    PBomOrderItem['userdefine'] = ''
    PBomOrderItem['guid'] = ''

def SortVar(elem):
    return len(elem[0])

def SetSubject(LPH, childVarstr, Var):

    L = float(LPH['L'])
    P = float(LPH['P'])
    H = float(LPH['H'])

    if childVarstr == '' or childVarstr == None:
        return 0
    if childVarstr.isdigit():
        return eval(childVarstr)
    if Var == {}:
        childVarstr = check(childVarstr)
        return eval(childVarstr)
    items = list(Var.items())
    items.sort(key=SortVar,reverse=True)
    for vname, vvalue in items:
        if vname=='':
            continue
        childVarstr = childVarstr.replace(vname,vvalue)
    childVarstr=check(childVarstr)

    try:
        childVarint = eval(childVarstr)
    except:
        childVarint = GetExpValue(L, P, H, childVarstr)

    return childVarint

def SetSysLPHValue(L,P,H):
    LPH = {}
    LPH['L'] = L
    LPH['P'] = P
    LPH['H'] = H
    return LPH

def check(childVarstr):
    if childVarstr[len(childVarstr)-1] =='-' or childVarstr[len(childVarstr)-1] =='+' or childVarstr[len(childVarstr)-1] =='*' or childVarstr[len(childVarstr)-1] =='/':
        childVarstr = childVarstr[0:len(childVarstr)-1]
    return childVarstr

def ChangeFileExt(filename,filename2):
    '''

    :param filename: '123.txt'
    :param filename2: '' or '.db'
    :return: '123' or '123.db'
    '''
    return filename[0:filename.index('.')]+filename2

def SetSysVariantValue(vname, value ,Var):
    global value_lsk,value_rsk,value_zk,value_zs,value_ls,value_lg,value_ltm,value_rtm

    # Var['value_lsk'] = '0'
    # Var['value_rsk'] = '0'
    # Var['value_zk'] = '0'
    # Var['value_zs'] = '0'
    # Var['value_ls'] = '0'
    # Var['value_lg'] = '0'
    # Var['value_ltm'] = '0'
    # Var['value_rtm'] = '0'
    Var[vname] = value
    if vname == '$左收口宽度' :value_lsk = int(float(value))
    if vname == '$右收口宽度' :value_rsk = int(float(value))
    if vname == '$柱切角宽度' :value_zk = int(float(value))
    if vname == '$柱切角深度' :value_zs = int(float(value))
    if vname == '$梁切角深度' :value_ls = int(float(value))
    if vname == '$梁切角高度' :value_lg = int(float(value))
    if vname == '$左侧趟门位' :value_ltm = int(float(value))
    if vname == '$右侧趟门位' : value_rtm = int(float(value))
    return Var

def InitSysVariantValue():
    global value_lsk, value_rsk, value_zk, value_zs, value_ls, value_lg, value_ltm, value_rtm
    value_lsk = 0
    value_rsk = 0
    value_zk = 0
    value_zs = 0
    value_ls = 0
    value_lg = 0
    value_ltm = 0
    value_rtm = 0

def MyVariant(str1, s1, s2):
    s1 = ''
    s2 = ''
    ws = str1
    n = ws.find(':')
    s1 = ws[0: n]
    s2 = ws[n+1:]
    return s1,s2

def CompileLuaProgram(obj, program_string):
    SADlog.debug('program_string='+program_string)
    
    parmes = "CA,CB,CC,CD,CE,CF,CG,CH,CJ,CK,CL,CM,CN,CO,CP,CQ,LX,LY,LZ,LL,LD,LH,LOZ = %d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d"%(
        obj['C0'],
        obj['C1'],
        obj['C2'],
        obj['C3'],
        obj['C4'],
        obj['C5'],
        obj['C6'],
        obj['C7'],
        obj['C8'],
        obj['C9'],
        obj['C10'],
        obj['C11'],
        obj['C12'],
        obj['C13'],
        obj['C14'],
        obj['C15'],
        obj['X'],
        obj['Y'],
        obj['Z'],
        obj['L'],
        obj['D'],
        obj['H'],
        obj['OZ'])
    SADlog.debug('parmes='+parmes)
    #抽盒内嵌-托底缓冲滑轨ZRG002.lua,826右斜切转角顶线.lua
    executor1 = Executor(program_string,parmes)
    xml = executor1.run()
    if not xml: xml = ''
    SADlog.debug('string='+xml)
    return xml

def GetXMLByLink(link):
    Result = ''
    if link=='': return ''
    XSDBfile = RootPath + '\\data\\XScriptDb.mdb'
    conn = pypyodbc.win_connect_mdb(r'DRIVER={Microsoft Access Driver (*.mdb  *.accbd)};DBQ=' + XSDBfile)
    cur = conn.cursor()
    sql = "select xml from  xml_template where path='%s'" % (link)
    cur.execute(sql)
    t = cur.fetchall()
    if t == []:
        filename = link.replace('模板目录\\', RootPath+'\\')
        filename = ChangeFileExt(filename, '.xmlitem')
        if os.path.exists(filename):
            with open(filename,'r') as f:
                xmlstring = f.read()
            return xmlstring
        return ''
    else:
        xmlstr = t[0][0].replace('"', "'")
        return xmlstr

def EnumXML(xml):
    def CreateNodeByXML(xmlfile):
        if xmlfile=='' : return
        DOMTree = minidom.parseString(xmlfile)
        node = DOMTree.documentElement
        return node
    def EnumNode(blocknode):
        for i in range(0, len(blocknode.childNodes)):
            node = blocknode.childNodes[i]
            if node.nodeName=='我的模块' :
                for j in range(0, len(node.childNodes)):
                    cnode = node.childNodes[j]
                    if cnode.nodeType !=1: continue
                    attri = cnode.getAttribute('链接')
                    if (attri == '') : continue
                    string = GetXMLByLink(attri)
                    if string=='' : continue
                    tmpnode = CreateNodeByXML(string)
                    cnode.appendChild(tmpnode)
                    if os.path.exists(string):
                        os.remove(string)
            EnumNode(node)
    if xml == '':
        return ''
    DOMTree = minidom.parseString(xml)
    root = DOMTree.documentElement
    EnumNode(root)
    Result = root.toxml('utf8')
    return Result

def Xml2ChildNodes(xml):
    if xml =='': return 
    DOMTree = minidom.parseString(xml)
    node = DOMTree.documentElement
    return node

def ImportCloneItemForBom(Var,program_str, clone_oi, clonenode, param, id):
    def trim(S):
        L = len(S)
        I = 0
        while (I < L) and (S[I] <= ' '): I = I+1
        if I >= L : Result =''
        else:
            while S[L-1] <= ' ':
                L = L - 1
        Result = S[I: L]
        return Result
    def S2S(string, s1, s2):
        s1 = ''
        s2 = ''
        ws = string
        n = ws.find('=')
        s1 = ws[:n]
        s2 = ws[n+1:]
        s1 = trim(s1)
        s2 = trim(s2)
        s2 = s2.replace('^', ',')
        return s1, s2
    def UpdateAttribute(node, name, value):
        attri = node.getAttribute(name)
        node.setAttribute(name, value)

    Result = 0
    LPH = SetSysLPHValue(param['pl'], param['pd'], param['ph'])
    ext = ExtractFileExt(program_str)
    LUAPath = base_dir + '\\Program\\'
    luafile = LUAPath + program_str
    SADlog.debug('luafile:' + luafile)
    if not os.path.exists(luafile):
        SADlog.warning(luafile + ' not exists!!!')
    else:
        #with open(luafile, 'r') as f:
            #program_string = f.read()

        obj = {'X': clone_oi['x'],  # X
               'Y': clone_oi['y'],  # Y
               'Z': clone_oi['z'],  # Z
               'L': clone_oi['l'],  # 宽
               'D': clone_oi['p'],  # 深
               'H': clone_oi['h'],  # 高
               'OZ': clone_oi['oz'],  # OZ旋转
               }
        for i in range(16):
            obj['C'+str(i)] = clone_oi['var_args'][i]
        if ext =='.lua':
            wstr = CompileLuaProgram(obj, luafile)
        else:
            SADlog.warning(program_str + ' not exists!!!')

        n = wstr.find(';')
        while n > 0:
            cnode = clonenode.cloneNode(True)
            nodeName = cnode.nodeName
            ln = wstr[:n]
            wstr = wstr[n+1:]
            n = ln.find(',')
            while n >0:
                vstr = ln[:n]
                s1 = ''
                s2 = ''
                s1, s2 = S2S(vstr, s1, s2)
                if s1=='NN' : nodeName = s2
                else: UpdateAttribute(cnode, s1, s2)
                ln = ln[n +1:]
                n = ln.find(',')
            if (n <= 0) and (ln !=''):
                s1 = ''
                s2 = ''
                s1, s2 = S2S(ln, s1, s2)
                if s1 == 'NN':
                    nodeName = s2
                else:
                    UpdateAttribute(cnode, s1, s2)
            n = wstr.find(';')

            if (cnode.nodeName != '板件') and (cnode.nodeName != '五金') and (
                            cnode.nodeName != '型材五金') and (cnode.nodeName != '模块') and (
                            cnode.nodeName != '门板'):
                continue
            bg = cnode.getAttribute('基础图形')
            if bg == 'BG::SPACE': continue
            string = cnode.getAttribute('显示方式')
            if string == '3': continue
            newpoi = {}
            newpoi['显示方式'] = string
            InitBomOrderItem(newpoi)

            newpoi['pl'] = param['pl']
            newpoi['pd'] = param['pd']
            newpoi['ph'] = param['ph']
            
            tmp_subspace = cnode.getAttribute('子空间')
            if tmp_subspace == 'A': tmp_subspace = ''
            newpoi['x'] = int(param['px']) + 0
            newpoi['y'] = int(param['py']) + 0
            newpoi['z'] = int(param['pz']) + 0
            xx0 = 0
            xx1 = 0
            yy0 = 0
            yy1 = 0
            zz0 = 0
            zz1 = 0
            if cnode.hasAttribute('XX0'):
                xx0 = int(cnode.getAttribute('XX0'))
            if cnode.hasAttribute('XX1'):
                xx1 = int(cnode.getAttribute('XX1'))
            if cnode.hasAttribute('YY0'):
                yy0 = int(cnode.getAttribute('YY0'))
            if cnode.hasAttribute('YY1'):
                yy1 = int(cnode.getAttribute('YY1'))
            if cnode.hasAttribute('ZZ0'):
                zz0 = int(cnode.getAttribute('ZZ0'))
            if cnode.hasAttribute('ZZ1'):
                zz1 = int(cnode.getAttribute('ZZ1'))
            varstr = ''
            if cnode.hasAttribute('X'):
                varstr = cnode.getAttribute('X')

            ToValueInt = int(Delphi_Round(SetSubject(LPH, varstr, Var)))

            newpoi['lx'] = ToValueInt + xx0
            newpoi['x'] = int(param['px']) + newpoi['lx']

            varstr = ''
            if cnode.hasAttribute('Y'):
                varstr = cnode.getAttribute('Y')
            ToValueInt = int(Delphi_Round(SetSubject(LPH, varstr, Var)))
            newpoi['ly'] = ToValueInt + yy0
            newpoi['y'] = int(param['py']) + newpoi['ly']

            varstr = ''
            if cnode.hasAttribute('Z'):
                varstr = cnode.getAttribute('Z')
            ToValueInt = int(Delphi_Round(SetSubject(LPH, varstr, Var)))

            newpoi['lz'] = ToValueInt + zz0
            newpoi['z'] = int(param['pz']) + newpoi['lz']

            newpoi['ox'] = 0
            if cnode.getAttribute('OX') != '':
                newpoi['ox'] = float(cnode.getAttribute('OX'))
            newpoi['oy'] = 0
            if cnode.getAttribute('OY') != '':
                newpoi['oy'] = float(cnode.getAttribute('OY'))
            newpoi['oz'] = 0
            if cnode.getAttribute('OZ') != '':
                newpoi['oz'] = float(cnode.getAttribute('OZ'))

            varstr = ''
            if cnode.hasAttribute('宽'):
                varstr = cnode.getAttribute('宽')
            ToValueInt = int(Delphi_Round(SetSubject(LPH, varstr, Var)))
            newpoi['l'] = int(ToValueInt) + int(xx1) + (0 - int(xx0))

            varstr = ''
            if cnode.hasAttribute('深'):
                varstr = cnode.getAttribute('深')
            ToValueInt = int(Delphi_Round(SetSubject(LPH, varstr, Var)))
            newpoi['p'] = ToValueInt + int(yy1) + (0 - int(yy0))

            varstr = ''
            if cnode.hasAttribute('高'):
                varstr = cnode.getAttribute('高')
            ToValueInt = int(Delphi_Round(SetSubject(LPH, varstr, Var)))
            newpoi['h'] = ToValueInt + int(zz1) + (0 - int(zz0))

            # 所有16个参数
            args = [0] * 16
            for k in range(0, 16):
                args[k] = 0
                string = ''
                if cnode.hasAttribute(('参数' + str(k))):
                    string = cnode.getAttribute(('参数' + str(k)))
                if (string != ''):
                    vname = ''
                    value = ''
                    vname, value = MyVariant(string, vname, value)
                    ToValueInt = int(SetSubject(LPH, value, Var))
                    args[k] = ToValueInt
                    newpoi['var_args'][k] = args[k]
                    newpoi['var_names'][k] = vname
                    varstr = varstr + '+' + vname
                    newpoi['C' + str(k)] = ToValueInt

            if bg == 'BG::DOORRECT':
                newpoi['l'] = newpoi['l'] + args[0] + args[1]
                newpoi['h'] = newpoi['h'] + args[2] + args[3]

            if bg == 'BG::BLOCK_X':
                if newpoi['var_args'][0] == 2 :

                    if newpoi['var_args'][1] == 1 :

                        newpoi['p'] = Delphi_Round(math.sqrt(newpoi['var_args'][3] * newpoi['var_args'][3] + newpoi['var_args'][4] * newpoi['var_args'][4]))

                    elif poi['var_args'][1] == 2 :

                        newpoi['l'] = Delphi_Round(math.sqrt(newpoi['var_args'][3] * newpoi['var_args'][3] + newpoi['var_args'][4] * newpoi['var_args'][4]))

            if cnode.hasAttribute('类别'):
                newpoi['desc'] = cnode.getAttribute('类别')
            newpoi['类别'] = newpoi['desc']
            linkpath = ''
            if cnode.hasAttribute('链接'):
                linkpath = cnode.getAttribute('链接')
            newpoi['类别'] = newpoi['desc']
            real_l = newpoi['l']
            real_d = newpoi['p']
            if newpoi['oz'] == '0':
                newpoi['oz'] = 0
            if (tmp_subspace == 'L'):  # // L面空间，进行旋转计算

                if (newpoi['var_args'][0] == 1):

                    newpoi['oz'] = arctan(
                        (real_d - newpoi['var_args'][2]) / (real_l - newpoi['var_args'][1])) / pi * 180  # // 旋转角度
                    newpoi['p'] = newpoi['var_args'][3]  # // 深度
                    t = sqrt((real_l - newpoi['var_args'][1]) * (real_l - newpoi['var_args'][1]) + (
                                real_d - newpoi['var_args'][2]) * (
                                     real_d - newpoi['var_args'][2]))
                    newpoi['l'] = Delphi_Round(t)  # // 宽度
                    newpoi['x'] = Delphi_Round(
                        newpoi['var_args'][1] - newpoi['var_args'][3] * (real_d - newpoi['var_args'][2]) / t)  # // x
                    newpoi['y'] = Delphi_Round(
                        real_d - newpoi['var_args'][3] * (real_l - newpoi['var_args'][1]) / t)  # ; // y
                    if newpoi['var_args'][4] != 0: newpoi['l'] = newpoi['var_args'][4]
                    newpoi['lx'] = newpoi['x']
                    newpoi['ly'] = newpoi['y']
                else:
                    newpoi['oz'] = 0

            if (tmp_subspace == 'R'):  # // R面空间，进行旋转计算

                if (newpoi['var_args'][0] == 1):

                    newpoi['oz'] = -arctan(
                        (real_d - newpoi['var_args'][2]) / (real_l - newpoi['var_args'][1])) / pi * 180  # // 旋转角度
                    newpoi['p'] = newpoi['var_args'][3]  # // 深度
                    t = sqrt((real_l - newpoi['var_args'][1]) * (real_l - newpoi['var_args'][1]) + (
                            real_d - newpoi['var_args'][2]) * (
                                     real_d - newpoi['var_args'][2]))
                    newpoi['l'] = Delphi_Round(t)  # // 宽度
                    newpoi['x'] = newpoi['x'] + round(newpoi['var_args'][3] * (
                            real_d - newpoi['var_args'][1]) / t)  # // x
                    newpoi['y'] = Delphi_Round(
                        newpoi['var_args'][2] - newpoi['var_args'][3] * (real_l - newpoi['var_args'][1]) / t)  # ; // y
                    if newpoi['var_args'][4] != 0: newpoi['l'] = newpoi['var_args'][4]
                    newpoi['lx'] = newpoi['x']
                    newpoi['ly'] = newpoi['y']
                else:
                    newpoi['oz'] = 0
            childnum = 0

            newpoi['Program'] = program_str
            sMKobjb = {}

            childxml = ''
            if linkpath !='':

                childxml = EnumXML(GetXMLByLink(linkpath))
                tmpnode = Xml2ChildNodes(childxml)
                if tmpnode != None:
                    for ccnode in cnode.childNodes:
                        cnode.removeChild(ccnode)
                    cnode.appendChild(tmpnode)
                else:
                    if cnode.childNodes.length> 0 :
                        childxml = cnode.toxml('utf8')

            if childxml != '':
                param2 = {}
                for key, value in param.items():
                    param2[key] = value
                # param2 = {}
                # for key, value in param.items():
                #     param2[key] = value
                spaceflag = ''
                if cnode.hasAttribute('SpaceFlag'):
                    spaceflag = cnode.getAttribute('SpaceFlag')
                param2['pname'] = newpoi['name']
                param2['guid'] = newpoi['guid']
                param2['subspace'] = newpoi['subspace']
          
                param2['xml'] = childxml
 
                param2['pmat'] = newpoi['mat']
                param2['pcolor'] = newpoi['color']
        
                param2['mark'] = newpoi['mark']
                param2['pl'] = newpoi['l']
                param2['pd'] = newpoi['p']
                param2['ph'] = newpoi['h']
                param2['px'] = newpoi['x']
                param2['py'] = newpoi['y']
                param2['pz'] = newpoi['z']
      
       
                param2['num'] = newpoi['num']
                param2['parent'] = newpoi

                if cnode.hasAttribute('输出类型'):
                    param2['outputtype'] = cnode.getAttribute('输出类型')
                    sMKobjb['outputtype'] = cnode.getAttribute('输出类型')
                child = getfirstchild(cnode)
                if child:
                    param2['rootnode'] = child
                    param2['xdoc'] = param['xdoc']
                    childnum = ImportXomItemForBom(param2)
  
def ExtractFileExt(filename):
    '''
        :param filename: '123.txt'
        :return: .txt
        '''
    return filename[filename.index('.'):]

def getfirstchild(node):
    Result = None
    for child in node.childNodes:
        if child.nodeType !=1: continue
        Result = child
        break
    return Result

def IsHasObj(oldlist, obj):
    Result = False
    if obj in oldlist:
        Result = True
    return Result

def Add2Config(name, obj):
    if obj == {}:return
    if name not in config['ymconfig']:
        config['ymconfig'][name] = []
    ishas = False
    ishas = IsHasObj(config['ymconfig'][name], obj)
    if ishas:return
    config['ymconfig'][name].append(obj)
    #SADlog.debug(name+json.dumps(obj,ensure_ascii=False))

def Add2SlidingConfig(name, obj):
    if name not in config['tmconfig']:
        config['tmconfig'][name] = []
    ishas = IsHasObj(config['tmconfig'][name], obj)
    if ishas: return
    config['tmconfig'][name].append(obj)
    #SADlog.debug(name+json.dumps(obj,ensure_ascii=False))

def arryFindstr(arr, string):
    for k in range(len(arr)):
        if (arr[k] == string):
            return True
    return False

def AddmWJBomDetailList(wjname, door_bh, opendirect, bktype):
    pwjbom = GetWjBom(wjname)
    if pwjbom:
        Add2Config('mWJBomList', pwjbom)  # 五金配件分类.cfg
        for i in range(len(mWJBomDetailList)):
            pwjbomdetail = mWJBomDetailList[i]
            if ((pwjbomdetail['bomname'] == pwjbom['name']) and ((pwjbomdetail['door_bh'] == 0)
                                                                 or (pwjbomdetail['door_bh'] == door_bh))
                    and ((pwjbomdetail['opendirect'] == '') or (pwjbomdetail['opendirect'] == opendirect))
                    and ((pwjbomdetail['bktype'] == '') or (arryFindstr(pwjbomdetail['bktypeAry'], bktype)))):
                Add2Config('mWJBomDetailList', pwjbomdetail)  # 五金配件分类数据.cfg
                if pwjbomdetail:
                    pa = GetDoorAccessory(pwjbomdetail['name'])
                    Add2Config('mAccessoryList', pa)

def AddDoorPanelBomDetailList(bomclass, mat, color, color2, color3, pnll, pnlh):
    for i in range(0, len(mDoorPanelBomDetailList)):
        ppbdetail = mDoorPanelBomDetailList[i]
        if ((ppbdetail['bomclass'] == bomclass) and (float(ppbdetail['lmin']) < float(pnll)) and (float(ppbdetail['lmax']) >= float(pnll)) and (
                float(ppbdetail['hmin']) < float(pnlh)) and (float(ppbdetail['hmax']) >= float(pnlh))):
            Add2Config('mDoorPanelBomDetailList', ppbdetail)

def DoorRecalcDoor(door, t1, t2, tt1, tt2, m, mGridItem):
    if (mGridItem==6) and (len(door.panellist)==2):  #// 两均分(下格固定)
        for j in range(0, len(door.boxlist)):
            rb = door.boxlist[j]
            rb.y0 = rb.y0 + (t2 / 1) * (0 + 0) + tt2 * m
            rb.y1 = rb.y1 + (t2 / 1) * (0 + 0) + tt2 * m
            rb.y2 = rb.y2 + (t2 / 1) * (0 + 0) + tt2 * m
            rb.x0 = rb.x0 + tt1 * m
            rb.x1 = rb.x1 + tt1 * m
            rb.x2 = rb.x2 + tt1 * m
            rb.w0 = rb.w0 + t1
            rb.w1 = rb.w1 + t1
            rb.w2 = rb.w2 + t1
        for j in range(0, len(door.panellist)):
            pnl = door.panellist[j]
            n = 0
            if j==1: pnl.h0 = pnl.h0 + (t2 / 1)
            pnl.y0 = pnl.y0 + (t2 / 1) * n + tt2 * m
            if j==1: pnl.h1 = pnl.h1 + (t2 / 1)
            pnl.y1 = pnl.y1 + (t2 / 1) * n + tt2 * m
            if j==1: pnl.h2 = pnl.h2 + (t2 / 1)
            pnl.y2 = pnl.y2 + (t2 / 1) * n + tt2 * m
            pnl.x0 = pnl.x0 + tt1 * m
            pnl.x1 = pnl.x1 + tt1 * m
            pnl.x2 = pnl.x2 + tt1 * m
            pnl.w0 = pnl.w0 + t1
            pnl.w1 = pnl.w1 + t1
            pnl.w2 = pnl.w2 + t1
    elif (mGridItem==8) and (len(door.panellist)==3) : #// 三格，中间格保持不变
        for j in range(0, len(door.boxlist)):
            rb = door.boxlist[j]
            rb.y0 = rb.y0 + (t2 / 2) * (0 + 1) + tt2 * m
            rb.y1 = rb.y1 + (t2 / 2) * (0 + 1) + tt2 * m
            rb.y2 = rb.y2 + (t2 / 2) * (0 + 1) + tt2 * m
            rb.x0 = rb.x0 + tt1 * m
            rb.x1 = rb.x1 + tt1 * m
            rb.x2 = rb.x2 + tt1 * m
            rb.w0 = rb.w0 + t1
            rb.w1 = rb.w1 + t1
            rb.w2 = rb.w2 + t1
        for j in range(0, len(door.panellist)):
            pnl = door.panellist[j]
            n = j
            if j == 2: n = 1
            if j != 1: pnl.h0 = pnl.h0 + (t2 / 2)
            pnl.y0 = pnl.y0 + (t2 / 2) * n + tt2 * m
            if j != 1: pnl.h1 = pnl.h1 + (t2 / 2)
            pnl.y1 = pnl.y1 + (t2 / 2) * n + tt2 * m
            if j != 1: pnl.h2 = pnl.h2 + (t2 / 2)
            pnl.y2 = pnl.y2 + (t2 / 2) * n + tt2 * m
            pnl.x0 = pnl.x0 + tt1 * m
            pnl.x1 = pnl.x1 + tt1 * m
            pnl.x2 = pnl.x2 + tt1 * m
            pnl.w0 = pnl.w0 + t1
            pnl.w1 = pnl.w1 + t1
            pnl.w2 = pnl.w2 + t1
    elif (mGridItem==7) and (len(door.panellist)==2): #// 两均分(上格固定)
        for j in range(0, len(door.boxlist)):
            rb = door.boxlist[j]
            rb.y0 = rb.y0 + (t2 / 1) * (0 + 1) + tt2 * m
            rb.y1 = rb.y1 + (t2 / 1) * (0 + 1) + tt2 * m
            rb.y2 = rb.y2 + (t2 / 1) * (0 + 1) + tt2 * m
            rb.x0 = rb.x0 + tt1 * m
            rb.x1 = rb.x1 + tt1 * m
            rb.x2 = rb.x2 + tt1 * m
            rb.w0 = rb.w0 + t1
            rb.w1 = rb.w1 + t1
            rb.w2 = rb.w2 + t1
        for j in range(0, len(door.panellist)):
            pnl = door.panellist[j]
            n = 0
            if j==1: n =1
            if j==0: pnl.h0 =pnl.h0 + (t2 / 1)
            pnl.y0 = pnl.y0 + (t2 / 1) * n + tt2 * m
            if j==0: pnl.h1 =pnl.h1 + (t2 / 1)
            pnl.y1 = pnl.y1 + (t2 / 1) * n + tt2 * m
            if j==0: pnl.h2 =pnl.h2 + (t2 / 1)
            pnl.y2 = pnl.y2 + (t2 / 1) * n + tt2 * m
            pnl.x0 = pnl.x0 + tt1 * m
            pnl.x1 = pnl.x1 + tt1 * m
            pnl.x2 = pnl.x2 + tt1 * m
            pnl.w0 = pnl.w0 + t1
            pnl.w1 = pnl.w1 + t1
            pnl.w2 = pnl.w2 + t1
    elif (mGridItem==9) and (len(door.panellist)==3) : #// 三均分(上两格固定)
        for j in range(0, len(door.boxlist)):
            rb = door.boxlist[j]
            rb.y0 = rb.y0 + (t2 / 1) * (0 + 1) + tt2 * m
            rb.y1 = rb.y1 + (t2 / 1) * (0 + 1) + tt2 * m
            rb.y2 = rb.y2 + (t2 / 1) * (0 + 1) + tt2 * m
            rb.x0 = rb.x0 + tt1 * m
            rb.x1 = rb.x1 + tt1 * m
            rb.x2 = rb.x2 + tt1 * m
            rb.w0 = rb.w0 + t1
            rb.w1 = rb.w1 + t1
            rb.w2 = rb.w2 + t1
        for j in range(0, len(door.panellist)):
            pnl = door.panellist[j]
            n = 0
            if j > 0: n = 1
            if j==0: pnl.h0 = pnl.h0 + (t2 / 1)
            pnl.y0 = pnl.y0 + (t2 / 1) * n + tt2 * m
            if j==0: pnl.h1 = pnl.h1 + (t2 / 1)
            pnl.y1 = pnl.y1 + (t2 / 1) * n + tt2 * m
            if j==0: pnl.h2 = pnl.h2 + (t2 / 1)
            pnl.y2 = pnl.y2 + (t2 / 1) * n + tt2 * m
            pnl.x0 = pnl.x0 + tt1 * m
            pnl.x1 = pnl.x1 + tt1 * m
            pnl.x2 = pnl.x2 + tt1 * m
            pnl.w0 = pnl.w0 + t1
            pnl.w1 = pnl.w1 + t1
            pnl.w2 = pnl.w2 + t1
    elif (mGridItem==10) and (len(door.panellist)==3) : #// 三均分(上两格固定)
        for j in range(0, len(door.boxlist)):
            rb = door.boxlist[j]
            rb.y0 = rb.y0 + (t2 / 1) * (0 + 0) + tt2 * m
            rb.y1 = rb.y1 + (t2 / 1) * (0 + 0) + tt2 * m
            rb.y2 = rb.y2 + (t2 / 1) * (0 + 0) + tt2 * m
            rb.x0 = rb.x0 + tt1 * m
            rb.x1 = rb.x1 + tt1 * m
            rb.x2 = rb.x2 + tt1 * m
            rb.w0 = rb.w0 + t1
            rb.w1 = rb.w1 + t1
            rb.w2 = rb.w2 + t1
        for j in range(0, len(door.panellist)):
            pnl = door.panellist[j]
            n = 0
            if j==2 : pnl.h0 = pnl.h0 + (t2 / 1)
            pnl.y0 = pnl.y0 + (t2 / 1) * n + tt2 * m
            if j==2 : pnl.h1 = pnl.h1 + (t2 / 1)
            pnl.y1 = pnl.y1 + (t2 / 1) * n + tt2 * m
            if j==2 : pnl.h2 = pnl.h2 + (t2 / 1)
            pnl.y2 = pnl.y2 + (t2 / 1) * n + tt2 * m
            pnl.x0 = pnl.x0 + tt1 * m
            pnl.x1 = pnl.x1 + tt1 * m
            pnl.x2 = pnl.x2 + tt1 * m
            pnl.w0 = pnl.w0 + t1
            pnl.w1 = pnl.w1 + t1
            pnl.w2 = pnl.w2 + t1
    else:
        for j in range(0, len(door.boxlist)):
            rb = door.boxlist[j]
            rb.y0 = rb.y0 + (t2 / len(door.panellist)) * (j + 1) + tt2 * m
            rb.y1 = rb.y1 + (t2 / len(door.panellist)) * (j + 1) + tt2 * m
            rb.y2 = rb.y2 + (t2 / len(door.panellist)) * (j + 1) + tt2 * m
            rb.x0 = rb.x0 + tt1 * m
            rb.x1 = rb.x1 + tt1 * m
            rb.x2 = rb.x2 + tt1 * m
            rb.w0 = rb.w0 + t1
            rb.w1 = rb.w1 + t1
            rb.w2 = rb.w2 + t1
        for j in range(0, len(door.panellist)):
            pnl = door.panellist[j]
            pnl.h0 = pnl.h0 + (t2 / len(door.panellist))
            pnl.y0 = pnl.y0 + (t2 / len(door.panellist)) * j + tt2 * m
            pnl.h1 = pnl.h1 + (t2 / len(door.panellist))
            pnl.y1 = pnl.y1 + (t2 / len(door.panellist)) * j + tt2 * m
            pnl.h2 = pnl.h2 + (t2 / len(door.panellist))
            pnl.y2 = pnl.y2 + (t2 / len(door.panellist)) * j + tt2 * m
            pnl.x0 = pnl.x0 + tt1 * m
            pnl.x1 = pnl.x1 + tt1 * m
            pnl.x2 = pnl.x2 + tt1 * m
            pnl.w0 = pnl.w0 + t1
            pnl.w1 = pnl.w1 + t1
            pnl.w2 = pnl.w2 + t1

def RecalcDoor(door, t1, t2, hh, mGridItem):
    if (mGridItem == 6) and (len(door.panellist)==2):  # 两均分(下格固定)
        t2 = hh
        for j in range(0, len(door.boxlist)):
            rb = door.boxlist[j]
            rb.y0 = rb.y0 + t2 * (0 + 0)
            rb.y1 = rb.y1 + t2 * (0 + 0)
            rb.y2 = rb.y2 + t2 * (0 + 0)
        for j in range(0, len(door.panellist)):
            pnl = door.panellist[j]
            if j==1:
                pnl.h0 = pnl.h0 + t2
                pnl.y0 = pnl.y0
                pnl.h1 = pnl.h1 + t2
                pnl.y1 = pnl.y1
                pnl.h2 = pnl.h2 + t2
                pnl.y2 = pnl.y2
    elif (mGridItem == 7) and (len(door.panellist)==2):  # 两均分，上格固定
        t2 = hh
        for j in range(0, len(door.boxlist)):
            rb = door.boxlist[j]
            rb.y0 = rb.y0 + t2 * (0 + 1)
            rb.y1 = rb.y1 + t2 * (0 + 1)
            rb.y2 = rb.y2 + t2 * (0 + 1)
        for j in range(0, len(door.panellist)):
            pnl = door.panellist[j]
            if j==1:
                pnl.h0 = pnl.h0
                pnl.y0 = pnl.y0 + t2
                pnl.h1 = pnl.h1
                pnl.y1 = pnl.y1 + t2
                pnl.h2 = pnl.h2
                pnl.y2 = pnl.y2 + t2
            elif j==0:
                pnl.h0 = pnl.h0 + t2
                pnl.y0 = pnl.y0
                pnl.h1 = pnl.h1 + t2
                pnl.y1 = pnl.y1
                pnl.h2 = pnl.h2 + t2
                pnl.y2 = pnl.y2
    elif (mGridItem == 8) and (len(door.panellist)==3):  # 三格，中间格固定
        t2 = hh / 2
        for j in range(0, len(door.boxlist)):
            rb = door.boxlist[j]
            rb.y0 = rb.y0 + t2 * (0 + 1)
            rb.y1 = rb.y1 + t2 * (0 + 1)
            rb.y2 = rb.y2 + t2 * (0 + 1)
        for j in range(0, len(door.panellist)):
            pnl = door.panellist[j]
            if j==1:
                pnl.h0 = pnl.h0
                pnl.y0 = pnl.y0 + t2
                pnl.h1 = pnl.h1
                pnl.y1 = pnl.y1 + t2
                pnl.h2 = pnl.h2
                pnl.y2 = pnl.y2 + t2
            elif j==0:
                pnl.h0 = pnl.h0 + t2
                pnl.y0 = pnl.y0
                pnl.h1 = pnl.h1 + t2
                pnl.y1 = pnl.y1
                pnl.h2 = pnl.h2 + t2
                pnl.y2 = pnl.y2
            elif j==2:
                pnl.h0 = pnl.h0 + t2
                pnl.y0 = pnl.y0 + t2
                pnl.h1 = pnl.h1 + t2
                pnl.y1 = pnl.y1 + t2
                pnl.h2 = pnl.h2 + t2
                pnl.y2 = pnl.y2 + t2
    elif (mGridItem == 9) and (len(door.panellist)==3):  # 三均分(上两格固定)
        t2 = hh
        for j in range(0, len(door.boxlist)):
            rb = door.boxlist[j]
            rb.y0 = rb.y0 + t2 * (0 + 1)
            rb.y1 = rb.y1 + t2 * (0 + 1)
            rb.y2 = rb.y2 + t2 * (0 + 1)
        for j in range(0, len(door.panellist)):
            pnl = door.panellist[j]
            if j > 0:
                pnl.h0 = pnl.h0
                pnl.y0 = pnl.y0 + t2
                pnl.h1 = pnl.h1
                pnl.y1 = pnl.y1 + t2
                pnl.h2 = pnl.h2
                pnl.y2 = pnl.y2 + t2
            elif j==0:
                pnl.h0 = pnl.h0 + t2
                pnl.y0 = pnl.y0
                pnl.h1 = pnl.h1 + t2
                pnl.y1 = pnl.y1
                pnl.h2 = pnl.h2 + t2
                pnl.y2 = pnl.y2
    elif (mGridItem == 10) and (len(door.panellist)==3):  # 三均分(下两格固定)    }
        t2 = hh
        for j in range(0, len(door.boxlist)):
            rb = door.boxlist[j]
            rb.y0 = rb.y0 + t2 * (0 + 0)
            rb.y1 = rb.y1 + t2 * (0 + 0)
            rb.y2 = rb.y2 + t2 * (0 + 0)
        for j in range(0, len(door.panellist)):
            pnl = door.panellist[j]
            if j > 1:
                pnl.h0 = pnl.h0 + t2
                pnl.y0 = pnl.y0
                pnl.h1 = pnl.h1 + t2
                pnl.y1 = pnl.y1
                pnl.h2 = pnl.h2 + t2
                pnl.y2 = pnl.y2
            elif j==0:
                pnl.h0 = pnl.h0
                pnl.y0 = pnl.y0
                pnl.h1 = pnl.h1
                pnl.y1 = pnl.y1
                pnl.h2 = pnl.h2
                pnl.y2 = pnl.y2
    else:
        t2 = hh / (len(door.panellist))
        for j in range(0, len(door.boxlist)):
            rb = door.boxlist[j]
            rb.y0 = rb.y0 + t2 * (j + 1)
            rb.y1 = rb.y1 + t2 * (j + 1)
            rb.y2 = rb.y2 + t2 * (j + 1)
        for j in range(0, len(door.panellist)):
            pnl = door.panellist[j]
            pnl.h0 = pnl.h0 + t2
            pnl.y0 = pnl.y0 + t2 * j
            pnl.h1 = pnl.h1 + t2
            pnl.y1 = pnl.y1 + t2 * j
            pnl.h2 = pnl.h2 + t2
            pnl.y2 = pnl.y2 + t2 * j

def getymconfig(xmltemplate, l, h):
    root = ET.fromstring(xmltemplate)
    attri = root.get('门洞宽','0')
    mL = float(attri)
    attri = root.get('门洞高', '0')
    mH = float(attri)
    attri = root.get('单门数量类型', '')
    mPExp = GetDoorsExp(attri)
    Add2Config('mExpList', mPExp)
    string = root.get('门类型', '')
    mPType = GetDoorsType(string)
    Add2Config('mTypeList', mPType)
    attri = root.get('门框类型', '')
    mPParam = GetDoorsParam(string, attri)
    mMyVBoxColor = root.get('门框颜色', '')
    Add2Config('mParamList', mPParam)
    attri = root.get('中横框类型', '')
    mPHBoxParam = GetHBoxParam(attri)
    Add2Config('mDoorHBoxParamList', mPHBoxParam)
    mGridItem = 0
    attri = root.get('均分')
    if attri != None : mGridItem = int(attri)
    mDataMode = int(root.get('DataMode', '0'))
    m = -1
    ll = 0
    hh = 0
    if (mPExp == {}) or (mPType == {}) or (mPParam == {}):
        mCopyDoor = -1
        return
    mIsVertical = False
    attri = root.get('是否竖排',False)
    if (attri != None) and (attri == 'True') :
        mIsVertical = True
    if l != 0 : ll = l - (mL)
    if h != 0 : hh = h - (mH)
    mL = Delphi_Round(mL + ll)
    mH = Delphi_Round(mH + hh)
    m = 0
    t1 = ll / mPExp['doornum'] #; // 计算需要补回的门洞差值
    t2 = hh
    tt1 = t1
    tt2 = 0
    if mIsVertical :
        t1 = ll
        t2 = hh / mPExp['doornum']
        tt1 = 0
        tt2 = t2
    m = -1
    mDoorsList = []
    for i in range(0, len(root)):
        node = root[i]
        if (node.tag != '单门'): continue
        m = m + 1
        door = TDoorDoorRect()
        mDoorsList.append(door)
        door.mPParam = mPParam
        door.mHandle = node.get('拉手', '')
        door.mOpenDirect = node.get('打开方向', '')
        door.mHinge = node.get('门铰', '')
        for j in range(0, len(node)):
            cnode = node[j]
            if cnode.tag != '门芯' : continue
            pnl = DoorRectPanel()
            door.panellist.append(pnl)
            pnl.PanelType = cnode.get('类型', '')
            pnl.color = cnode.get('颜色', '')
            pnl.color2 = cnode.get('颜色2', '')
            attri = cnode.get('w0', '0')
            pnl.w0 = float(attri)
            attri = cnode.get('h0', '0')
            pnl.h0 = float(attri)
            attri = cnode.get('x0', '0')
            pnl.x0 = float(attri)
            attri = cnode.get('y0', '0')
            pnl.y0 = float(attri)
            attri = cnode.get('d0', '0')
            pnl.d0 = float(attri)
            attri = cnode.get('w1', '0')
            pnl.w1 = float(attri)
            attri = cnode.get('h1', '0')
            pnl.h1 = float(attri)
            attri = cnode.get('x1', '0')
            pnl.x1 = float(attri)
            attri = cnode.get('y1', '0')
            pnl.y1 = float(attri)
            attri = cnode.get('d1', '0')
            pnl.d1 = float(attri)
            attri = cnode.get('w2', '0')
            pnl.w2 = float(attri)
            attri = cnode.get('h2', '0')
            pnl.h2 = float(attri)
            attri = cnode.get('x2', '0')
            pnl.x2 = float(attri)
            attri = cnode.get('y2', '0')
            pnl.y2 = float(attri)
            attri = cnode.get('d2', '0')
            pnl.d2 = float(attri)
        #中横框
        for i in range(0, len(node)):
            cnode = node[i]
            if (cnode.tag != '中横框'): continue
            rb = DoorRectBox()
            rb.selected = False
            door.boxlist.append(rb)
            attri = cnode.get('类型', '0')
            rb.boxtype = attri
            attri = cnode.get('颜色', '0')
            rb.color = attri
            rb.vh = True
            attri = cnode.get('vh', '0')
            if attri == 'False':
                rb.vh = False
            attri = cnode.get('w0', '0')
            rb.w0 = float(attri)
            attri = cnode.get('h0', '0')
            rb.h0 = float(attri)
            attri = cnode.get('x0', '0')
            rb.x0 = float(attri)
            attri = cnode.get('y0', '0')
            rb.y0 = float(attri)
            attri = cnode.get('d0', '0')
            rb.d0 = float(attri)
            attri = cnode.get('w1', '0')
            rb.w1 = float(attri)
            attri = cnode.get('h1', '0')
            rb.h1 = float(attri)
            attri = cnode.get('x1', '0')
            rb.x1 = float(attri)
            attri = cnode.get('y1', '0')
            rb.y1 = float(attri)
            attri = cnode.get('d1', '0')
            rb.d1 = float(attri)
            attri = cnode.get('w2', '0')
            rb.w2 = float(attri)
            attri = cnode.get('h2', '0')
            rb.h2 = float(attri)
            attri = cnode.get('x2', '0')
            rb.x2 = float(attri)
            attri = cnode.get('y2', '0')
            rb.y2 = float(attri)
            attri = cnode.get('d2', '0')
            rb.d2 = float(attri)
        DoorRecalcDoor(door, t1, t2, tt1, tt2, m, mGridItem)
    for i in range(0, len(mDoorsList)):
        door = mDoorsList[i]
        bh = Delphi_Round(mPType['depth'])
        SADlog.debug('拉手=' + door.mHandle)
        phandle = GetDoorsHandle(door.mHandle)
        Add2Config('mHandleList', phandle)  # 拉手
        SADlog.debug('门铰=' + door.mHinge)
        phinge = GetDoorsHinge(door.mHinge, mPType)
        Add2Config('mHingeList', phinge)  # 门铰
        if phandle:
            AddmWJBomDetailList(phandle['wjname'], bh, door.mOpenDirect, mPParam['name'])
        #SADlog.debug(phinge, bh, door.mOpenDirect, mPParam)
        if phinge:
            AddmWJBomDetailList(phinge['wjname'], bh, door.mOpenDirect, mPParam['name'])
        if (mPType['isframe']):
            #门芯
            for j in range(0, len(door.panellist)):
                pnl = door.panellist[j]
                pnltype = GetDoorPanelType(mPParam['name'], pnl.PanelType) #GetDoorPanelType
                Add2Config('mDoorPanelTypeList', pnltype)  # 百叶板配置
                if pnltype:
                    mytype = pnltype['mytype']
                    AddDoorPanelBomDetailList(pnltype['panelbom'], pnl.PanelType, pnl.color, pnl.color2, mMyVBoxColor,
                                pnl.w1, pnl.h1)
                SADlog.debug('门芯类型=' + pnl.PanelType)
                pssexp = GetDoorSSExp(pnl.PanelType)
                Add2Config('mShutterExpList', pssexp)  #百叶板配置
                SADlog.debug('颜色=' + pnl.color)
                pcolorclass = GetColorClass('门芯',pnl.color)
                Add2Config('mColorClassList', pcolorclass)  # 颜色分类 门芯颜色
            #中横框
            for j in range(0, len(door.boxlist)):
                rb = door.boxlist[j]
                boxtype = rb.boxtype
                hbox = GetHBoxParam(boxtype)
                Add2Config('mDoorHBoxParamList', hbox)
                wjname = hbox['wjname']
                AddmWJBomDetailList(wjname, bh, door.mOpenDirect,  mPParam['name'])
        else:
            if ( len(door.panellist) > 0 ):
                pnl = door.panellist[0]
                pnltype = GetDoorPanelType(mPParam['name'], pnl.PanelType)
                if ( pnltype ):  bh = pnltype['thick']
            for j in range(0, len(door.panellist)):
                pnl = door.panellist[j]
                pnltype = GetDoorPanelType(mPParam['name'], pnl.PanelType)  # GetDoorPanelType
                Add2Config('mDoorPanelTypeList', pnltype)
                if pnltype:
                    AddDoorPanelBomDetailList(pnltype['panelbom'], pnl.PanelType, pnl.color, pnl.color2, mMyVBoxColor,
                                pnl.w1, pnl.h1)
                SADlog.debug('门芯类型=' + pnl.PanelType)
                pssexp = GetDoorSSExp(pnl.PanelType)
                Add2Config('mShutterExpList', pssexp)  # 百叶板配置
                SADlog.debug('颜色=' + pnl.color)
                pcolorclass = GetColorClass('门芯', pnl.color)
                Add2Config('mColorClassList', pcolorclass)  # 颜色分类 门芯颜色
    pcolorclass2 = GetColorClass2(mPParam['name'], mMyVBoxColor)
    Add2Config('mColorClass2List', pcolorclass2)  # 颜色分类2  门框颜色
    if (mDataMode == 0):
        wjname = mPParam['wjname']
        door_bh, opendirect, bktype = 0, '', mPParam['name']
        AddmWJBomDetailList(wjname, door_bh, opendirect, bktype)
    left_doorxml = mPParam['left_doorxml']
    pxml = returnxml(left_doorxml)
    Add2Config('mDoorXMLList', pxml)
    right_doorxml = mPParam['right_doorxml']
    pxml = returnxml(right_doorxml)
    Add2Config('mDoorXMLList', pxml)
    doorxml = mPParam['doorxml']
    pxml = returnxml(doorxml)
    Add2Config('mDoorXMLList', pxml)

def GetWjBomDetaildata(wjname, skcolor1, skcolor2, skcolor3, skcolor4):
    result = {}
    pa = {}
    for m in range(0 , len(mSlidingWjBomDetailList)):
        pbomdetail = mSlidingWjBomDetailList[m]
        if pbomdetail['bomname'] == wjname :
            pa = GetSlidingAccessory(pbomdetail['name'])
            if pa:
                color = ToColor(pa['color'], skcolor1, skcolor2, skcolor3, skcolor4)
                Add2SlidingConfig('SlidingAccessory', pa)
                pcolorclass = GetSlidingColorClass('配件', pa['name'], color)
                Add2SlidingConfig('SlidingColorClass', pcolorclass)
    return result

def gettmconfig(xmltemplate, l, h):
    root = ET.fromstring(xmltemplate)
    attri = root.get('门洞宽', '0')
    mL = int(attri)
    attri = root.get('门洞高', '0')
    mH = int(attri)
    attri = root.get('延长导轨','0')
    mAddLength = int(attri)
    attri = root.get('单门数量类型', '')
    pexp = GetSlidingExp(attri)           #单门数量类型
    Add2SlidingConfig('SlidingExp', pexp)
    attri = root.get('门类型','')
    pstype = GetSlidingType(attri)
    Add2SlidingConfig('SlidingType', pstype)
    attri = root.get('边框类型', '')
    psp = GetSlidingParam(attri)
    Add2SlidingConfig('SlidingParam', psp)
    attri = root.get('上下横框类型', '')
    pudbox = GetUDBoxParam(attri)
    Add2SlidingConfig('UDBoxParam', pudbox)
    attri = root.get('上下轨类型', '')
    ptrack = GetTrackParam(attri)
    Add2SlidingConfig('TrackParam', ptrack)
    attri = root.get('中横框类型', '')
    phbox = GetSlidingHBoxParam(attri)
    Add2SlidingConfig('HboxParam', phbox)
    pvbox = {}
    if psp: pvbox = GetVBoxParam(psp['vboxtype'])
    Add2SlidingConfig('VBoxParam', pvbox)
    attri = root.get('门板类型', '')
    if attri:
        mMyPanelType = attri
    else:
        mMyPanelType = ''
    attri = root.get('门颜色', '')
    if attri:
        mMySlidingColor = attri
    else:
        mMySlidingColor = ''
    attri = root.get('竖框颜色','')
    if attri  : mMyVBoxColor = attri
    else: mMyVBoxColor = ''
    attri = root.get('上横框颜色', '')
    if attri:
        mMyUpBoxColor = attri
    else:
        mMyUpBoxColor = ''
    attri = root.get('下横框颜色', '')
    if attri:
        mMyDownBoxColor = attri
    else:
        mMyDownBoxColor = ''
    attri = root.get('上轨颜色', '')
    if attri  : mMyUpTrackColor = attri
    else:  mMyUpTrackColor =''
    attri = root.get('下轨颜色', '')
    if attri:
        mMyDownTrackColor = attri
    else:
        mMyDownTrackColor = ''
    attri = root.get('中横框颜色', '')
    if attri:
        mMyHBoxColor = attri
    else:
        mMyHBoxColor = ''
    attri = root.get('门板颜色', '')
    if attri:
        mMyPanelColor = attri
    else:
        mMyPanelColor = ''
    mDataMode = int(root.get('DataMode', '0'))
    mGridItem = 0
    attri = root.get('均分')
    if attri != None: mGridItem = int(attri)
    if (pexp =={}) or (pstype == {}) or (psp == {}) or (pudbox =={}) \
        or (ptrack == {}) or (phbox =={}) or (pvbox == {}):
        return
    nHasMzhb = False #门转换表
    ll = 0
    hh = 0
    if l != 0 : ll = l - (mL)
    if h != 0 : hh = h - (mH)
    if pexp['noexp'] :
        ll = 0
        hh = 0
    mSlidingExp = pexp
    mSlidingParam = psp
    mSlidingType = pstype
    mTrackParam = ptrack
    UDBoxParam = pudbox
    HBoxParam = phbox
    VBoxParam = pvbox
    m = 0
    t1 = hh / (mGridItem + 1)
    if mGridItem==5: t1 = hh  # ======
    if mGridItem==6: t1 = hh  # 两均分，下格固定
    if mGridItem==7: t1 = hh  # 两均分，上格固定
    if mGridItem==8: t1 = hh / 2  # 三均分，中间格固定
    if mGridItem==9: t1 = hh  # 三均分(上两格固定)
    if mGridItem==10: t1 = hh  # 三均分(下两格固定)
    mDoorsList = []
    m = -1
    t1 = ll/mSlidingExp['doornum']
    t2 = 0
    for i in range(0, len(root)):
        node = root[i]
        if node.tag !='单门': continue
        m = m+1
        door = TDoorRect()
        mDoorsList.append(door)
        attri = node.get('宽')
        door.doorw = float(attri) + t1  # 补差值
        attri = node.get('高')
        door.doorh = float(attri) + hh
        attri = node.get('X0')
        door.x0 = float(attri) + t1 * m  # 补差值
        attri = node.get('Y0')
        door.y0 = float(attri)
        attri = node.get('竖框类型')
        pvbox = GetVBoxParam(attri)
        if pvbox: door.mVBoxParam = pvbox
        attri = node.get('竖框颜色')
        door.mVBoxColor = attri
        attri = node.get('上下横框类型')
        pudbox = GetUDBoxParam(attri)
        if pudbox: door.mUDBoxParam = pudbox
        for j in range(0, len(node)):
            cnode = node[j]
            if cnode.tag != '中横框' : continue
            rb = DoorRectBox()
            door.boxlist.append(rb)
            attri = cnode.get('类型')
            rb.boxtype = attri
            attri = cnode.get('颜色')
            rb.color = attri
            rb.vh = True
            attri = cnode.get('vh')
            if attri == 'False' : rb.vh = False
            attri = cnode.get('w0')
            rb.w0 = float(attri) + t1
            attri = cnode.get('h0')
            rb.h0 = float(attri)
            attri = cnode.get('x0')
            rb.x0 = float(attri) + t1 * m
            attri = cnode.get('y0')
            rb.y0 = float(attri)
            attri = cnode.get('d0')
            rb.d0 = float(attri)
            attri = cnode.get('w1')
            rb.w1 = float(attri) + t1
            attri = cnode.get('h1')
            rb.h1 = float(attri)
            attri = cnode.get('x1')
            rb.x1 = float(attri) + t1 * m
            attri = cnode.get('y1')
            rb.y1 = float(attri)
            attri = cnode.get('d1')
            rb.d1 = float(attri)
            attri = cnode.get('w2')
            rb.w2 = float(attri) + t1
            attri = cnode.get('h2')
            rb.h2 = float(attri)
            attri = cnode.get('x2')
            rb.x2 = float(attri) + t1 * m
            attri = cnode.get('y2')
            rb.y2 = float(attri)
            attri = cnode.get('d2')
            rb.d2 = float(attri)
        for j in range(0, len(node)):
            cnode = node[j]
            if cnode.tag != '门板' : continue
            pnl = RectPanel()
            pnl.selected = False
            door.panellist.append(pnl)
            attri = cnode.get('类型')
            pnl.PanelType = attri
            attri = cnode.get('颜色')
            pnl.color = attri
            attri = cnode.get('颜色2')
            if attri: pnl.color2 = attri
            attri = cnode.get('纹路')
            pnl.direct = attri
            attri = cnode.get('备注')
            if attri:
                pnl.memo = attri
            attri = cnode.get('ExtraData')
            if attri:
                pnl.extradata = attri
            attri = cnode.get('w0')
            pnl.w0 = float(attri) + t1
            attri = cnode.get('h0')
            pnl.h0 = float(attri)
            attri = cnode.get('x0')
            pnl.x0 = float(attri)
            attri = cnode.get('y0')
            pnl.y0 = float(attri)
            attri = cnode.get('d0')
            pnl.d0 = float(attri)
            attri = cnode.get('w1')
            pnl.w1 = float(attri) + t1
            attri = cnode.get('h1')
            pnl.h1 = float(attri)
            attri = cnode.get('x1')
            pnl.x1 = float(attri) + t1 * m
            attri = cnode.get('y1')
            pnl.y1 = float(attri)
            attri = cnode.get('d1')
            pnl.d1 = float(attri)
            attri = cnode.get('w2')
            pnl.w2 = float(attri) + t1
            attri = cnode.get('h2')
            pnl.h2 = float(attri)
            attri = cnode.get('x2')
            pnl.x2 = float(attri) + t1 * m
            attri = cnode.get('y2')
            pnl.y2 = float(attri)
            attri = cnode.get('d2')
            pnl.d2 = float(attri)
        RecalcDoor(door, t1, t2, hh, mGridItem)
    skcolor1, skcolor2, skcolor3, skcolor4 = '', '' ,'', ''
    if len(mDoorsList) > 0:
        door = mDoorsList[0]
        pcolorclass = GetSlidingColorClass('竖框', mSlidingParam['vboxtype'], door.mVBoxColor)
        if pcolorclass:
            Add2SlidingConfig('SlidingColorClass', pcolorclass)
            skcolor1 = pcolorclass['skcolor1']
            skcolor2 = pcolorclass['skcolor2']
            skcolor3 = pcolorclass['skcolor3']
            skcolor4 = pcolorclass['skcolor4']
    if (mDataMode==0) and (mTrackParam['wlupcode'] != ''):
        pcolorclass = GetSlidingColorClass('上轨', mTrackParam['upname'], mMyUpTrackColor)
        if pcolorclass: Add2SlidingConfig('SlidingColorClass', pcolorclass)
    if (mDataMode==0) and (mTrackParam['wldncode'] != ''):
        pcolorclass = GetSlidingColorClass('上轨', mTrackParam['dnname'], mMyDownTrackColor)
        if pcolorclass: Add2SlidingConfig('SlidingColorClass', pcolorclass)
    #趟门关联五金
    wjname = mSlidingParam['wjname']
    if (mDataMode==0) and (wjname != ''):
        pbomdetail = GetWjBomDetaildata(wjname, skcolor1, skcolor2, skcolor3, skcolor4)
        Add2SlidingConfig('SlidingWjBomDetail', pbomdetail)
    #上轨五金
    if (mDataMode==0) and (mTrackParam['wjname1'] != ''):
        pbomdetail = GetWjBomDetaildata(mTrackParam['wjname1'], skcolor1, skcolor2, skcolor3, skcolor4)
        Add2SlidingConfig('SlidingWjBomDetail', pbomdetail)
    #下轨五金
    if (mDataMode==0) and (mTrackParam['wjname2'] != ''):
        pbomdetail = GetWjBomDetaildata(mTrackParam['wjname2'], skcolor1, skcolor2, skcolor3, skcolor4)
        Add2SlidingConfig('SlidingWjBomDetail', pbomdetail)
    #竖框
    for i in range(0, len(mDoorsList)):
        if (mDataMode==1) : break
        door = mDoorsList[i]
        pvbox = GetVBoxParam(door.mVBoxParam['name'])
        if pvbox:
            Add2SlidingConfig('VBoxParam', pvbox)  #竖框参数
        pcolorclass = GetSlidingColorClass('竖框', door.mVBoxColor)
        Add2SlidingConfig('SlidingColorClass', pcolorclass)
        if door.mVBoxParam['wjname'] != '':
            pbomdetail = GetWjBomDetaildata(door.mVBoxParam['wjname'], skcolor1, skcolor2, skcolor3, skcolor4)
            Add2SlidingConfig('SlidingWjBomDetail', pbomdetail)
    # 上下横框
    for i in range(0, len(mDoorsList)):
        if (mDataMode == 1): break
        door = mDoorsList[i]
        pcolorclass = GetSlidingColorClass('上横框', mMyUpBoxColor)
        Add2SlidingConfig('SlidingColorClass', pcolorclass)
        pcolorclass = GetSlidingColorClass('下横框', mMyDownBoxColor)
        Add2SlidingConfig('SlidingColorClass', pcolorclass)
        #上横框五金
        if door.mUDBoxParam['wjname1'] != '':
            pbomdetail = GetWjBomDetaildata(door.mUDBoxParam['wjname1'], skcolor1, skcolor2, skcolor3, skcolor4)
            Add2SlidingConfig('SlidingWjBomDetail', pbomdetail)
        #下横框五金
        if door.mUDBoxParam['wjname2'] != '':
            pbomdetail = GetWjBomDetaildata(door.mUDBoxParam['wjname2'], skcolor1, skcolor2, skcolor3, skcolor4)
            Add2SlidingConfig('SlidingWjBomDetail', pbomdetail)
        for j in range(0, len(door.panellist)):
            pnl = door.panellist[j]
            pnltype = GetSlidingPanelType(mSlidingParam['name'], pnl.PanelType)
    for i in range(0, len(mDoorsList)):
        if (mDataMode == 1): break
        door = mDoorsList[i]
        for j in range(0, len(door.boxlist)):
            rb = door.boxlist[j]
            if rb.h0 <= 0 : continue
            phbox = GetSlidingHBoxParam(rb.boxtype)
            Add2SlidingConfig('HBoxParam', phbox)
            pcolorclass = GetSlidingColorClass('中横框', rb.color)
            Add2SlidingConfig('SlidingColorClass', pcolorclass)
            if phbox['wjname'] != '':
                pbomdetail = GetWjBomDetaildata(phbox['wjname'], skcolor1, skcolor2, skcolor3, skcolor4)
                Add2SlidingConfig('SlidingWjBomDetail', pbomdetail)
    for i in range(0, len(mDoorsList)):
        if (mDataMode == 1): break
        door = mDoorsList[i]
        for j in range(len(door.panellist)):
            pnl = door.panellist[j]
            if (pnl.extradata!='' and len(pnl.extradata) > 5): #有竖格门芯再此 从门板中ExtraData字段提取竖格门芯
                Sfg_Param = {}
                sfgFK = Sfg_Param
                sJson = pnl.extradata
                sJson = sJson.replace('^', '"')
                data = json.loads(sJson)
                data['L'] = pnl.w1
                data['H'] = pnl.h1
                if 'direc' not in data: data['direc'] = 0
                if (data['nType'] == 2):
                    if 'direc' in data and data['direc'] == 1:
                        xml = Sliding['SfgParam']['HTxml']
                        cfgobj = copy.deepcopy(HCfgobj2)
                        config['tmconfig']['SfgParam']['HTxml'] = xml
                        config['tmconfig']['Hfg2'] = HCfgobj2
                    else:
                        xml = Sliding['SfgParam']['Txml']
                        cfgobj = copy.deepcopy(Cfgobj2)
                        config['tmconfig']['SfgParam']['Txml'] = xml
                        config['tmconfig']['Sfg2'] = Cfgobj2
                if (data['nType'] == 3):
                    if 'direc' in data and data['direc'] == 1:
                        xml = Sliding['SfgParam']['HSxml']
                        cfgobj = copy.deepcopy(HCfgobj3)
                        config['tmconfig']['SfgParam']['HSxml'] = xml
                        config['tmconfig']['Hfg3'] = HCfgobj3
                    else:
                        xml = Sliding['SfgParam']['Sxml']
                        cfgobj = copy.deepcopy(HCfgobj2)
                        config['tmconfig']['SfgParam']['Sxml'] = xml
                        config['tmconfig']['Sfg3'] = Cfgobj3
                if (data['nType'] == 4):
                    if 'direc' in data and data['direc'] == 1:
                        xml = Sliding['SfgParam']['HFxml']
                        cfgobj = copy.deepcopy(HCfgobj4)
                        config['tmconfig']['SfgParam']['HFxml'] = xml
                        config['tmconfig']['Hfg4'] = HCfgobj4
                    else:
                        xml = Sliding['SfgParam']['Fxml']
                        cfgobj = copy.deepcopy(Cfgobj4)
                        config['tmconfig']['SfgParam']['Fxml'] = xml
                        config['tmconfig']['Sfg4'] = Cfgobj4
                config['tmconfig']['HSHBoxParam'] = [],  # 22.横中横 HSHBoxParam
                config['tmconfig']['SHBoxParam'] = [],  # 23.竖中横 SHBoxParam
            pnltype = GetSlidingPanelType(mSlidingParam['name'], pnl.PanelType)
            if (pnltype ):
                Add2SlidingConfig('PanelType', pnltype)
                pnlbomdetail = GetPanelBomdata(pnltype['slaVe'],pnl.PanelType, pnl.color, pnl.color2,door.mVBoxColor, pnl.w1, pnl.h1)
                Add2SlidingConfig('PanelBomDetail', pnlbomdetail) #门板附加物料
            pssexp = GetSlidingSSExp(pnl.PanelType)
            Add2SlidingConfig('SSExp', pssexp)
            pcolorclass = GetSlidingColorClass('门板', pnl.PanelType, pnl.color)
            if pcolorclass: Add2SlidingConfig('SlidingColorClass', pcolorclass)
            #添加门板的关联五金
            if (pnltype) and (pnltype['wjname'] !=''):
                pbomdetail = GetWjBomDetaildata(pnltype['wjname'], skcolor1, skcolor2, skcolor3, skcolor4)
                Add2SlidingConfig('SlidingWjBomDetail', pbomdetail)

def ImportXomItemForBom(param):
        Result = 0
        LPH = SetSysLPHValue(param['pl'], param['pd'], param['ph'])
        root = param['rootnode']
        string = root.getAttribute('模块备注')
        if string:
            param['blockmemo'] = string
            param['blockmemo'] = param['blockmemo'].replace('[宽]', str(param['pl']))
            param['blockmemo'] = param['blockmemo'].replace('[深]', str(param['pd']))
            param['blockmemo'] = param['blockmemo'].replace('[高]', str(param['ph']))

        string = root.getAttribute('类别')
        if (string == '趟门,趟门') or (string == '掩门,掩门'):
            nodelist = root.getElementsByTagName('模板')

            if len(nodelist) < 0: return
            node = nodelist[0]  # 模板节点

            cnode = getfirstchild(node)
            childxml = ''
            if cnode:
                childxml = cnode.toxml('utf8')
                #SADlog.debug(childxml)
            if (childxml!='') and (string == '趟门,趟门'):
                tmobj = {}
                tmobj['pl'] = param['pl']
                tmobj['ph'] = param['ph']
                tmobj['childxml'] = childxml
                tmlist.append(tmobj)
                #gettmconfig(childxml, param['pl'], param['ph'])
            if (childxml!='') and (string == '掩门,掩门'):
                ymobj = {}
                ymobj['pl'] = param['pl']
                ymobj['ph'] = param['ph']
                ymobj['childxml'] = childxml
                ymlist.append(ymobj)
                #getymconfig(childxml, param['pl'], param['ph'])

        Var = {}
        for i in range(0, root.childNodes.length):
            node = root.childNodes[i]
            if node.nodeType != 1: continue
            if node.nodeName == '变量列表':
                for j in range(0, node.childNodes.length):
                    cnode = node.childNodes[j]
                    if cnode.nodeType != 1: continue
                    if cnode.nodeName == '变量':
                        vname = cnode.getAttribute('名称')

                        value = cnode.getAttribute('值')

                        Var = SetSysVariantValue(vname, value, Var)

        for i in range(0, root.childNodes.length):
            node = root.childNodes[i]
            if node.nodeType != 1: continue
            if node.nodeName == '我的模块':
                for j in range(0, node.childNodes.length):
                    cnode = node.childNodes[j]
                    if cnode.nodeType != 1: continue
                    if (cnode.nodeName != '板件') and (cnode.nodeName != '五金') and (
                            cnode.nodeName != '型材五金') and (cnode.nodeName != '模块') and (
                            cnode.nodeName != '门板'):
                        continue
                    bg = cnode.getAttribute('基础图形')
                    if bg == 'BG::SPACE': continue
                    string = cnode.getAttribute('显示方式')
                    if string == '3': continue
                    newpoi = {}
                    newpoi['显示方式'] = string
                    InitBomOrderItem(newpoi)

                    newpoi['pl'] = param['pl']
                    newpoi['pd'] = param['pd']
                    newpoi['ph'] = param['ph']
                    newpoi['parent'] = param['parent']
                    tmp_subspace = cnode.getAttribute('子空间')
                    if tmp_subspace == 'A': tmp_subspace = ''
                    newpoi['x'] = int(param['px']) + 0
                    newpoi['y'] = int(param['py']) + 0
                    newpoi['z'] = int(param['pz']) + 0
                    xx0 = 0
                    xx1 = 0
                    yy0 = 0
                    yy1 = 0
                    zz0 = 0
                    zz1 = 0
                    if cnode.hasAttribute('XX0'):
                        xx0 = int(cnode.getAttribute('XX0'))
                    if cnode.hasAttribute('XX1'):
                        xx1 = int(cnode.getAttribute('XX1'))
                    if cnode.hasAttribute('YY0'):
                        yy0 = int(cnode.getAttribute('YY0'))
                    if cnode.hasAttribute('YY1'):
                        yy1 = int(cnode.getAttribute('YY1'))
                    if cnode.hasAttribute('ZZ0'):
                        zz0 = int(cnode.getAttribute('ZZ0'))
                    if cnode.hasAttribute('ZZ1'):
                        zz1 = int(cnode.getAttribute('ZZ1'))
                    varstr = ''
                    if cnode.hasAttribute('X'):
                        varstr = cnode.getAttribute('X')

                    ToValueInt = int(Delphi_Round(SetSubject(LPH, varstr, Var)))

                    newpoi['lx'] = ToValueInt + xx0
                    newpoi['x'] = int(param['px']) + newpoi['lx']

                    varstr = ''
                    if cnode.hasAttribute('Y'):
                        varstr = cnode.getAttribute('Y')
                    ToValueInt = int(Delphi_Round(SetSubject(LPH, varstr, Var)))
                    newpoi['ly'] = ToValueInt + yy0
                    newpoi['y'] = int(param['py']) + newpoi['ly']

                    varstr = ''
                    if cnode.hasAttribute('Z'):
                        varstr = cnode.getAttribute('Z')
                    ToValueInt = int(Delphi_Round(SetSubject(LPH, varstr, Var)))

                    newpoi['lz'] = ToValueInt + zz0
                    newpoi['z'] = int(param['pz']) + newpoi['lz']

                    newpoi['ox'] = 0
                    if cnode.getAttribute('OX') != '':
                        newpoi['ox'] = float(cnode.getAttribute('OX'))
                    newpoi['oy'] = 0
                    if cnode.getAttribute('OY') != '':
                        newpoi['oy'] = float(cnode.getAttribute('OY'))
                    newpoi['oz'] = 0
                    if cnode.getAttribute('OZ') != '':
                        newpoi['oz'] = float(cnode.getAttribute('OZ'))

                    varstr = ''
                    if cnode.hasAttribute('宽'):
                        varstr = cnode.getAttribute('宽')
                    ToValueInt = int(Delphi_Round(SetSubject(LPH, varstr, Var)))
                    newpoi['l'] = int(ToValueInt) + int(xx1) + (0 - int(xx0))

                    varstr = ''
                    if cnode.hasAttribute('深'):
                        varstr = cnode.getAttribute('深')
                    ToValueInt = int(Delphi_Round(SetSubject(LPH, varstr, Var)))
                    newpoi['p'] = ToValueInt + int(yy1) + (0 - int(yy0))

                    varstr = ''
                    if cnode.hasAttribute('高'):
                        varstr = cnode.getAttribute('高')
                    ToValueInt = int(Delphi_Round(SetSubject(LPH, varstr, Var)))
                    newpoi['h'] = ToValueInt + int(zz1) + (0 - int(zz0))

                    # 所有16个参数
                    args = [0] * 16
                    for k in range(0, 16):
                        args[k] = 0
                        string = ''
                        if cnode.hasAttribute(('参数' + str(k))):
                            string = cnode.getAttribute(('参数' + str(k)))
                        if (string != ''):
                            vname = ''
                            value = ''
                            vname, value = MyVariant(string, vname, value)
                            ToValueInt = int(SetSubject(LPH, value, Var))
                            args[k] = ToValueInt
                            newpoi['var_args'][k] = args[k]
                            newpoi['var_names'][k] = vname
                            varstr = varstr + '+' + vname
                            newpoi['C' + str(k)] = ToValueInt
                    # size高级编程
                    program_str = ''
                    if cnode.hasAttribute('Program'):
                        program_str = cnode.getAttribute('Program')
                    if cnode.hasAttribute('GUID'):
                        newpoi['GUID'] = cnode.getAttribute('GUID')
                    if cnode.hasAttribute('SizeProgram'):
                        SpStr = cnode.getAttribute('SizeProgram')
                        LUAFILE = base_dir + '\\Program\\'
                        luafile1 = LUAFILE + SpStr
                        if os.path.exists(luafile1):

                            obj = {'X': newpoi['x'],  # X
                                   'Y': newpoi['y'],  # Y
                                   'Z': newpoi['z'],  # Z
                                   'L': newpoi['l'],  # 宽
                                   'D': newpoi['p'],  # 深
                                   'H': newpoi['h'],  # 高
                                   'OZ': newpoi['oz'],  # OZ旋转
                                   }
                            for i in range(16):
                                obj['C'+str(i)] = newpoi['var_args'][i]
                            SizeProgramStr = CompileLuaProgram(obj, luafile1)
                
                            if SizeProgramStr != '':
                                SizeProgramStr = SizeProgramStr[1:len(SizeProgramStr) - 1]
                                Sizeprogramstrlist = SizeProgramStr.split(',')
                                Sizeattridict = {}
                                for Sizeprogramstrlistchild in Sizeprogramstrlist:
                                    Sizeattrilist = Sizeprogramstrlistchild.split(':')
                                    Sizeattridict[Sizeattrilist[0]] = Sizeattrilist[1]
                                if 'X' in Sizeattridict:
                                    newpoi['x'] = int(Sizeattridict['X'])

                                if 'Y' in Sizeattridict:
                                    newpoi['y'] = int(Sizeattridict['Y'])

                                if 'Z' in Sizeattridict:
                                    newpoi['z'] = int(Sizeattridict['Z'])

                                if 'L' in Sizeattridict:
                                    newpoi['l'] = int(Sizeattridict['L'])

                                if 'D' in Sizeattridict:
                                    newpoi['p'] = int(Sizeattridict['D'])

                                if 'H' in Sizeattridict:
                                    newpoi['h'] = int(Sizeattridict['H'])

                                if 'OZ' in Sizeattridict:
                                    newpoi['oz'] = float(Sizeattridict['OZ'])
                    if cnode.hasAttribute('类别'):
                        newpoi['desc'] = cnode.getAttribute('类别')

                    real_l = newpoi['l']
                    real_d = newpoi['p']
                    if newpoi['oz'] == '0':
                        newpoi['oz'] = 0
                    if (tmp_subspace == 'L'):  # // L面空间，进行旋转计算

                        if (newpoi['var_args'][0] == 1):
                            newpoi['oz'] = arctan((real_d - newpoi['var_args'][2]) / (
                                        real_l - newpoi['var_args'][1])) / pi * 180  # // 旋转角度
                            newpoi['p'] = newpoi['var_args'][3]  # // 深度
                            t = sqrt((real_l - newpoi['var_args'][1]) * (real_l - newpoi['var_args'][1]) + (
                                        real_d - newpoi['var_args'][2]) * (
                                             real_d - newpoi['var_args'][2]))
                            newpoi['l'] = Delphi_Round(t)  # // 宽度
                            newpoi['x'] = Delphi_Round(newpoi['var_args'][1] - newpoi['var_args'][3] * (
                                        real_d - newpoi['var_args'][2]) / t)  # // x
                            newpoi['y'] = Delphi_Round(
                                real_d - newpoi['var_args'][3] * (real_l - newpoi['var_args'][1]) / t)  # ; // y
                            if newpoi['var_args'][4] != 0: newpoi['l'] = newpoi['var_args'][4]
                            newpoi['lx'] = newpoi['x']
                            newpoi['ly'] = newpoi['y']
                        else:
                            newpoi['oz'] = 0

                    if (tmp_subspace == 'R'):  # // R面空间，进行旋转计算

                        if (newpoi['var_args'][0] == 1):
                            newpoi['oz'] = -arctan(
                                (real_d - newpoi['var_args'][2]) / (
                                            real_l - newpoi['var_args'][1])) / pi * 180  # // 旋转角度
                            newpoi['p'] = newpoi['var_args'][3]  # // 深度
                            t = sqrt((real_l - newpoi['var_args'][1]) * (real_l - newpoi['var_args'][1]) + (
                                    real_d - newpoi['var_args'][2]) * (
                                             real_d - newpoi['var_args'][2]))
                            newpoi['l'] = Delphi_Round(t)  # // 宽度
                            newpoi['x'] = newpoi['x'] + round(newpoi['var_args'][3] * (
                                    real_d - newpoi['var_args'][1]) / t)  # // x
                            newpoi['y'] = Delphi_Round(newpoi['var_args'][2] - newpoi['var_args'][3] * (
                                        real_l - newpoi['var_args'][1]) / t)  # ; // y
                            if newpoi['var_args'][4] != 0: newpoi['l'] = newpoi['var_args'][4]
                            newpoi['lx'] = newpoi['x']
                            newpoi['ly'] = newpoi['y']
                        else:
                            newpoi['oz'] = 0
                    childxml = ''
                    firstchild = getfirstchild(cnode)
                    if firstchild:
                        childxml = firstchild.toxml('UTF-8')
                    if childxml != '':
                        param2 = {}
                        for key, value in param.items():
                            param2[key] = value
                        param2['pl'] = newpoi['l']
                        param2['pd'] = newpoi['p']
                        param2['ph'] = newpoi['h']
                        param2['px'] = newpoi['x']
                        param2['py'] = newpoi['y']
                        param2['pz'] = newpoi['z']
                        param2['num'] = newpoi['num']
                        param2['parent'] = newpoi
                        if cnode.hasAttribute('输出类型'):
                            param2['outputtype'] = cnode.getAttribute('输出类型')
                        child = getfirstchild(cnode)
                        if child:
                            param2['rootnode'] = child
                            param2['xdoc'] = param['xdoc']
                            childnum = ImportXomItemForBom(param2)
                    if program_str:
                        ImportCloneItemForBom(Var, program_str, newpoi, cnode, param, id)

def LoadXML2Bom(xmlfile, Path):
    '''
    xmlfile : xml文件
    path : 数据库目录
    '''

    global tmlist, ymlist,config, mWJBomDetailList, mAccessoryList, mDoorPanelBomDetailList,\
        mSlidingWjBomDetailList, Cfgobj2, Cfgobj3, Cfgobj4, HCfgobj2, HCfgobj3, HCfgobj4, SHBoxParam, \
        HSHBoxParam, cfglist, RootPath
    
    RootPath = Path
    tmlist = []
    ymlist = []
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
    mWJBomDetailList, mAccessoryList, mDoorPanelBomDetailList = DoorInitData(RootPath)
    mSlidingWjBomDetailList, Cfgobj2, Cfgobj3, Cfgobj4, HCfgobj2, HCfgobj3, HCfgobj4, SHBoxParam, HSHBoxParam, cfglist = SlidingInitData(RootPath)
    
    DOMTree = minidom.parse(xmlfile)
    root = DOMTree.documentElement
    node = getfirstchild(root)
    bh = 18
    InitSysVariantValue()
    if node.nodeName == '产品':
        string = (node.getAttribute('板材厚度'))
        if string: bh = int(string)
    l = 0
    d = 0
    h = 0
    if root.hasAttribute('宽') :
        l = int(root.getAttribute('宽'))
    if root.hasAttribute('深') :
        d = int(root.getAttribute('深'))
    if root.hasAttribute('高') :
        h = int(root.getAttribute('高'))
    param = {}
    param['pl'] = l
    param['pd'] = d
    param['ph'] = h
    param['px'] = 0
    param['py'] = 0
    param['pz'] = 0
    param['boardheight'] = bh
    param['rootnode'] = node
    param['xdoc'] = DOMTree
    param['parent'] = None

    ImportXomItemForBom(param)

    try:
        # 创建新线程
        thread1 = myThread(1, "tm", tmlist)
        thread2 = myThread(2, "ym", ymlist)
    except:
        print("Error: 无法启动线程")
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
    config['tmconfig']['Cfglist'] = cfglist
    # import json
    # with open('t.txt','w',encoding='utf8') as f:
    #     f.write(json.dumps(config,ensure_ascii=False))
    return config

class Executor(object):
    """
        执行lua的类
    """

    luaRuntime = None
    def __init__(self,filepath,params):
        threading.Thread.__init__(self)
        self.filepath = filepath
        self.params = params
        self.xml = ''
    def run(self):
        try:
            # 执行具体的函数,返回结果打印在屏幕上
            self.xml = self.getLuaRuntime()
            return self.xml
        except Exception as e:
            SADlog.error(self.filepath+', Cal error'+str(e))
            traceback.extract_stack()
 
    def getLuaRuntime(self):
        """
            从文件中加载要执行的lua脚本,初始化lua执行环境
        """

        fileHandler = open(self.filepath)
        content = ''
        try:
            with open(self.filepath,'r',encoding='utf8') as f:
                content = f.read()
        except Exception as e:
            SADlog.debug(self.filepath + ',FILE_UTF8 Decode Error')

        if content == '':
            try:
                with open(self.filepath,'r',encoding='gbk') as f:
                    content = f.read()
            except Exception as e:
                SADlog.debug(self.filepath + ',FILE_GBK Decode Error')

        # 创建lua执行环境
        Executor.luaScriptContent = content
        luaRuntime = LuaRuntime()
        luaRuntime.execute(self.params)
        # 从lua执行环境中取出全局函数functionCall作为入口函数调用,实现lua的反射调用
        g = luaRuntime.globals()
        pycall = luaRuntime.eval('function(pyfunc) math.pow=pyfunc end')
        pycall(math.pow)
        luaRuntime.execute(content)
        self.xml = g.XML
        Executor.luaRuntime = None
        return self.xml
    def getxml(self):
        return self.xml

class myThread (threading.Thread):
    def __init__(self, threadID, name, mylist):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.mylist = mylist
    def run(self):
        if self.name == 'tm':
            for sliding in self.mylist:
                threadLock.acquire()
                gettmconfig(sliding['childxml'], sliding['pl'], sliding['ph'])
                threadLock.release()
        elif self.name == 'ym':
            for door in self.mylist:
                threadLock.acquire()
                getymconfig(door['childxml'], door['pl'], door['ph'])
                threadLock.release()
        else:
            pass

# 创建两个线程

if __name__ == '__main__':
    print(time.time())
    mGridItem = 0 #均分
    RootPath = "D:\\nginx-1.0.11\\nginx-1.0.11\html\data"
    base_dir = os.path.abspath(os.path.join(os.getcwd()))
    print('2=',base_dir)
    path = 'D:\\HGSoftware\\001_美蝶设计软件工厂版190807\\Python3\\TestPython\\ord\\K10008220466190523001\\#order_scene0_space3420F65812518FAE670B179D73A6CBD8'
    LoadXML2Bom(path, "D:\\nginx-1.0.11\\nginx-1.0.11\html\data")
    # print ('len of tmlist='+str(len(tmlist)))
    # print('len of ymlist=' + str(len(ymlist)))
    print (time.time())
    for key, value in config['ymconfig'].items():
        SADlog.debug(key + ',' +str(len(value)))
