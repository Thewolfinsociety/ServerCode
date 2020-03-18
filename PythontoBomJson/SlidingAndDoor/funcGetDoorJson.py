#  -*- coding:utf-8 -*-
'''
vesion 1.0.1
2019/10/30
author:litao
'''
import json
import os
import xml.etree.ElementTree as ET
import configparser
import copy
from ctypes import *
import uuid
import xml.dom.minidom as DOM
import logging
import sys
import imp
import execjs
base_dir = os.path.abspath(os.path.join(os.getcwd()))
log = logging.getLogger(base_dir+"\\Python\\Log\\all.log")


QdUpTemplatePath = base_dir+'\\QdUpTemplate.dll'
QdUpTemplate = windll.LoadLibrary(QdUpTemplatePath)
RootPath = ""
def copyini(IniPath):
    copyinifile = os.path.dirname(IniPath) + '\\copy.ini'
    with open(copyinifile, 'w+') as f:
        with open(IniPath, 'r') as f1:
            content = f1.read()
            content = content.replace('//', '#')
        f.write(content)
    cf = configparser.ConfigParser()
    cf.read(copyinifile)
    return cf
def Number(string):
    if string=='':
        return 0
    string = float(string)
    try:
        if int(string) == float(string):
            return int(string)
        return float(string)
    except:
        return 0
def GetTrueFalse(string):
    if(string == 'TRUE' or string == 'True'or string == True or string == 1 or string == "1"):
        return True
    else:
        return False
def InitData():
    global mAccessoryList,mColorList,mColorClassList,mColorClass2List,\
        mTypeList,mExpList,mHandleList,mHBoxParamList,mHingeList,mCurHingeList, \
        mPanelBomDetailListDoor,mPanelTypeList,mParamList,mPriceList, \
        mPriceTableList, mShutterExpList, mWJBomList, mWJBomDetailList, \
        mDoorXMLList, HoleConfig, CoverTypeType,GetHingeHoleBD,GetHandleHoleBD
    cf = configparser.ConfigParser()
    try:
        cf = copyini(RootPath + '\\QdCloud\\XDiyDoors.ini')
        log.debug(RootPath + '\\QdCloud\\XDiyDoors.ini')
        CoverTypeType = cf.get("CoverType".encode('gb2312'), "nType".encode('gb2312'))
    except:
        CoverTypeType = 0
    if os.path.exists(RootPath + '\\QdCloud\\Door\\doorHoleConfig.js'):
        with open(RootPath + '\\QdCloud\\Door\\doorHoleConfig.js', 'r') as f:
            jsdata = f.read().decode('utf8')
            HoleConfig = jsdata
    else:
        HoleConfig = ''
    try:
        with open(RootPath + '\\QdCloud\\Door\\掩门配置表\\五金配件.cfg'.encode('gb2312'),'r') as f:
            mAccessoryListcontent=f.read()
        if mAccessoryListcontent=='':
            mAccessoryListcontent = json.dumps([])
    except:
        mAccessoryListcontent = json.dumps([])
    try:
        with open(RootPath + '\\QdCloud\\Door\\掩门配置表\\颜色.cfg'.encode('gb2312'),'r') as f:
            mColorListcontent=f.read()
        if mColorListcontent=='':
            mColorListcontent = json.dumps([])
    except:
        mColorListcontent = json.dumps([])
    try:
        with open(RootPath + '\\QdCloud\\Door\\掩门配置表\\颜色分类.cfg'.encode('gb2312'), 'r') as f:
            mColorClassListcontent = f.read()
        if mColorClassListcontent == '':
            mColorClassListcontent = json.dumps([])
    except:
        mColorClassListcontent = json.dumps([])
    try:
        with open(RootPath + '\\QdCloud\\Door\\掩门配置表\\颜色分类2.cfg'.encode('gb2312'), 'r') as f:
            mColorClass2Listcontent = f.read()
        if mColorClass2Listcontent == '':
            mColorClass2Listcontent = json.dumps([])
    except:
        mColorClass2Listcontent = json.dumps([])
    try:
        with open(RootPath + '\\QdCloud\\Door\\掩门配置表\\门类型.cfg'.encode('gb2312'),'r') as f:
            mTypeListcontent=f.read()
        if mTypeListcontent=='':
            mTypeListcontent = json.dumps([])
    except:
        mTypeListcontent = json.dumps([])
    try:
        with open(RootPath + '\\QdCloud\\Door\\掩门配置表\\单门数量类型.cfg'.encode('gb2312'),'r') as f:
            mExpListcontent=f.read()
        if mExpListcontent=='':
            mExpListcontent = json.dumps([])
    except:
        mExpListcontent = json.dumps([])
    try:
        with open(RootPath + '\\QdCloud\\Door\\掩门配置表\\拉手.cfg'.encode('gb2312'),'r') as f:
            mHandleListcontent=f.read()
        if mHandleListcontent=='':
            mHandleListcontent = json.dumps([])
    except:
        mHandleListcontent = json.dumps([])
    try:
        with open(RootPath + '\\QdCloud\\Door\\掩门配置表\\中横框参数.cfg'.encode('gb2312'),'r') as f:
            mHBoxParamListcontent=f.read()
        if mHBoxParamListcontent=='':
            mHBoxParamListcontent = json.dumps([])
    except:
        mHBoxParamListcontent = json.dumps([])
    try:
        with open(RootPath + '\\QdCloud\\Door\\掩门配置表\\门铰分类.cfg'.encode('gb2312'),'r') as f:
            mHingeListcontent=f.read()
        if mHingeListcontent=='':
            mHingeListcontent = json.dumps([])
    except:
        mHingeListcontent = json.dumps([])
    try:
        with open(RootPath + '\\QdCloud\\Door\\掩门配置表\\门铰.cfg'.encode('gb2312'), 'r') as f:
            mCurHingeListcontent = f.read()
        if mCurHingeListcontent == '':
            mCurHingeListcontent = json.dumps([])
    except:
        mCurHingeListcontent = json.dumps([])
    try:
        with open(RootPath + '\\QdCloud\\Door\\掩门配置表\\门芯附加物料.cfg'.encode('gb2312'), 'r') as f:
            mPanelBomDetailListDoorcontent = f.read()
        if mPanelBomDetailListDoorcontent == '':
            mPanelBomDetailListDoorcontent = json.dumps([])
    except:
        mPanelBomDetailListDoorcontent = json.dumps([])
    try:
        with open(RootPath + '\\QdCloud\\Door\\掩门配置表\\门芯类型.cfg'.encode('gb2312'), 'r') as f:
            mPanelTypeListcontent = f.read()
        if mPanelTypeListcontent == '':
            mPanelTypeListcontent = json.dumps([])
    except:
        mPanelTypeListcontent = json.dumps([])
    try:
        with open(RootPath + '\\QdCloud\\Door\\掩门配置表\\掩门参数.cfg'.encode('gb2312'), 'r') as f:
            mParamListcontent = f.read()
        if mParamListcontent == '':
            mParamListcontent = json.dumps([])
    except:
        mParamListcontent = json.dumps([])
    try:
        with open(RootPath + '\\QdCloud\\Door\\掩门配置表\\报价.cfg'.encode('gb2312'), 'r') as f:
            mPriceListcontent = f.read()
        if mPriceListcontent == '':
            mPriceListcontent = json.dumps([])
    except:
        mPriceListcontent = json.dumps([])
    try:
        with open(RootPath + '\\QdCloud\\Door\\掩门配置表\\报价方案.cfg'.encode('gb2312'), 'r') as f:
            mPriceTableListcontent = f.read()
        if mPriceTableListcontent == '':
            mPriceTableListcontent = json.dumps([])
    except:
        mPriceTableListcontent = json.dumps([])
    try:
        with open(RootPath + '\\QdCloud\\Door\\掩门配置表\\百叶板配置.cfg'.encode('gb2312'), 'r') as f:
            mShutterExpListcontent = f.read()
        if mShutterExpListcontent == '':
            mShutterExpListcontent = json.dumps([])
    except:
        mShutterExpListcontent = json.dumps([])
    try:
        with open(RootPath + '\\QdCloud\\Door\\掩门配置表\\五金配件分类.cfg'.encode('gb2312'), 'r') as f:
            mWJBomListcontent = f.read()
        if mWJBomListcontent == '':
            mWJBomListcontent = json.dumps([])
    except:
        mWJBomListcontent = json.dumps([])
    try:
        with open(RootPath + '\\QdCloud\\Door\\掩门配置表\\五金配件分类数据.cfg'.encode('gb2312'), 'r') as f:
            mWJBomDetailListcontent = f.read()
        if mWJBomDetailListcontent == '':
            mWJBomDetailListcontent = json.dumps([])
    except:
        mWJBomDetailListcontent = json.dumps([])
    try:
        with open(RootPath + '\\QdCloud\\Door\\掩门配置表\\XML单门结构.cfg'.encode('gb2312'), 'r') as f:
            mDoorXMLListcontent = f.read()
        if mDoorXMLListcontent == '':
            mDoorXMLListcontent = json.dumps([])
    except:
        mDoorXMLListcontent = json.dumps([])
    mExpList = json.loads(mExpListcontent,encoding='gbk')
    mHandleList = json.loads(mHandleListcontent, encoding='gbk')
    mHBoxParamList = json.loads(mHBoxParamListcontent, encoding='gbk')
    mHingeList = json.loads(mHingeListcontent, encoding='gbk')
    mCurHingeList = json.loads(mCurHingeListcontent, encoding='gbk')
    mPanelBomDetailListDoor = json.loads(mPanelBomDetailListDoorcontent, encoding='gbk')
    mPanelTypeList = json.loads(mPanelTypeListcontent, encoding='gbk')
    mParamList = json.loads(mParamListcontent, encoding='gbk')
    mPriceList = json.loads(mPriceListcontent, encoding='gbk')
    mPriceTableList = json.loads(mPriceTableListcontent, encoding='gbk')
    mShutterExpList = json.loads(mShutterExpListcontent, encoding='gbk')
    mWJBomList = json.loads(mWJBomListcontent, encoding='gbk')
    mWJBomDetailList = json.loads(mWJBomDetailListcontent, encoding='gbk')
    mDoorXMLList = json.loads(mDoorXMLListcontent, encoding='gbk')
    mAccessoryList = json.loads(mAccessoryListcontent, encoding='gbk')
    mColorList = json.loads(mColorListcontent, encoding='gbk')
    mColorClassList = json.loads(mColorClassListcontent, encoding='gbk')
    mColorClass2List = json.loads(mColorClass2Listcontent, encoding='gbk')
    mTypeList = json.loads(mTypeListcontent, encoding='gbk')
    #以上是掩门的
    # sSort(Cfgobj2)
    # sSort(Cfgobj3)
    # sSort(Cfgobj4)
    # sSort(HCfgobj2)
    # sSort(HCfgobj3)
    # sSort(HCfgobj4)
    for i in range(0,len(mExpList)):
        mExpList[i]['doornum'] = Number(mExpList[i]['doornum'])
        mExpList[i]['capnum'] = Number(mExpList[i]['capnum'])
        mExpList[i]['lkvalue'] = Number(mExpList[i]['lkvalue'])
    for i in range(0,len(mHBoxParamList)):
        mHBoxParamList[i]['height'] = Number(mHBoxParamList[i]['height'])
        mHBoxParamList[i]['depth'] = Number(mHBoxParamList[i]['depth'])
        mHBoxParamList[i]['thick'] = Number(mHBoxParamList[i]['thick'])
    for i in range(0,len(mHingeList)):
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
    for i in range(0, len(mPanelBomDetailListDoor)):
        mPanelBomDetailListDoor[i]["lmin"] = Number(mPanelBomDetailListDoor[i]['lmin'])
        mPanelBomDetailListDoor[i]["lmax"] = Number(mPanelBomDetailListDoor[i]['lmax'])
        mPanelBomDetailListDoor[i]["hmin"] = Number(mPanelBomDetailListDoor[i]['hmin'])
        mPanelBomDetailListDoor[i]["hmax"] = Number(mPanelBomDetailListDoor[i]['hmax'])
        mPanelBomDetailListDoor[i]["num"] = Number(mPanelBomDetailListDoor[i]['num'])
    for i in range(0, len(mPanelTypeList)):
        mPanelTypeList[i]["thick"] = Number(mPanelTypeList[i]['thick'])
        mPanelTypeList[i]["lfb"] = Number(mPanelTypeList[i]['lfb'])
        mPanelTypeList[i]["hfb"] = Number(mPanelTypeList[i]['hfb'])
        mPanelTypeList[i]["bomtype"] = mPanelTypeList[i]['bomtype']
        mPanelTypeList[i]["bktype"] = mPanelTypeList[i]['bktype']
        mPanelTypeList[i]["lmax"] = Number(mPanelTypeList[i]['lmax'])
        mPanelTypeList[i]["lmin"] = Number(mPanelTypeList[i]['lmin'])
        mPanelTypeList[i]["wmax"] = Number(mPanelTypeList[i]['wmax'])
        mPanelTypeList[i]["wmin"] = Number(mPanelTypeList[i]['wmin'])
        mPanelTypeList[i]["is_buy"] = mPanelTypeList[i]['is_buy']
        mPanelTypeList[i]["direct"] = mPanelTypeList[i]['direct']
        mPanelTypeList[i]["fbstr"] = mPanelTypeList[i]['fbstr']
        mPanelTypeList[i]["pnl3d"] = mPanelTypeList[i]['pnl3d']
        mPanelTypeList[i]["memo"] = mPanelTypeList[i]['memo']
        mPanelTypeList[i]["panelbom"] = mPanelTypeList[i]['panelbom']
        mPanelTypeList[i]["ypos"] = Number(mPanelTypeList[i]['ypos'])
        mPanelTypeList[i]["iswhole"] = mPanelTypeList[i]['iswhole']
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
        mParamList[i]["udboxjtw"] = Number(mParamList[i]['udboxjtw'] if 'udboxjt' not in mParamList[i] else mParamList[i]['udboxjt'])
        mParamList[i]["hboxjtw"] = Number(mParamList[i]['hboxjtw'])
        mParamList[i]["iscalc_framebom"] = GetTrueFalse(mParamList[i]['iscalc_framebom'])
        mParamList[i]["frame_valuel"] = Number(mParamList[i]['frame_valuel'])
        mParamList[i]["frame_valueh"] = Number(mParamList[i]['frame_valueh'])
        mParamList[i]["udbox_hbox_value"] = Number(mParamList[i]['udbox_hbox_value'])
        mParamList[i]["is_xq"] = GetTrueFalse(mParamList[i]['is_xq'])
        mParamList[i]["cb_yyvalue"] = Number(mParamList[i]['cb_yyvalue'])
        mParamList[i]["is_buy"] = mParamList[i]['is_buy']
        mParamList[i]["noframe_bom"] = Number(mParamList[i]['noframe_bom'])
    for i in range(0, len(mPriceList)):
        mPriceList[i]["price"] =Number(mPriceList[i]["price"])
        mPriceList[i]["price2"] = Number(mPriceList[i]["price2"])
        mPriceList[i]["start_num"] =Number(mPriceList[i]["start_num"])
    for i in range(0, len(mPriceTableList)):
        mPriceTableList[i]["bh"] = 0 if "BH" not in mPriceTableList[i] else Number(mPriceTableList[i]["BH"])
    for i in range(0, len(mShutterExpList)):
        mShutterExpList[i]["height"] =Number(mShutterExpList[i]["height"])
        mShutterExpList[i]["width"] = Number(mShutterExpList[i]["width"])
        mShutterExpList[i]["heightcap"] = Number(mShutterExpList[i]["heightcap"])
        mShutterExpList[i]["widthcap"] = Number(mShutterExpList[i]["widthcap"])
        mShutterExpList[i]["minheight"] = Number(mShutterExpList[i]["minheight"])
        mShutterExpList[i]["minwidth"] = Number(mShutterExpList[i]["minwidth"])
    for i in range(0, len(mWJBomDetailList)):
        mWJBomDetailList[i]["door_bh"] =Number(mWJBomDetailList[i]["door_bh"])
        mWJBomDetailList[i]["bktypeAry"] = []
        if mWJBomDetailList[i]["bktype"] !='':
            mWJBomDetailList[i]["bktypeAry"]= mWJBomDetailList[i]['bktype'].split(',')
    for i in range(0, len(mAccessoryList)):
        mAccessoryList[i]["myunit"] = mAccessoryList[i]["unit"]
    for i in range(0, len(mTypeList)):
        mTypeList[i]["isframe"] = GetTrueFalse(mTypeList[i]["isframe"])
        mTypeList[i]["covertype"] = Number(mTypeList[i]["covertype"])
        mTypeList[i]["lkvalue"] = GetTrueFalse(mTypeList[i]["lkvalue"])
        mTypeList[i]["ud_lkvalue"] =mTypeList[i]['lkvalue'] if "ud_lkvalue" not in mTypeList[i] else Number(mTypeList[i]['ud_lkvalue'])
        mTypeList[i]["depth"] = Number(mTypeList[i]["depth"])
        mTypeList[i]["eb_lkvalue"] = Number(mTypeList[i]["eb_lkvalue"])
        mTypeList[i]["eb_ud_lkvalue"] = Number(mTypeList[i]["eb_ud_lkvalue"])
    #以上是掩门
def fungetdoorjson(xml,W,H, Path):
    global RootPath
    RootPath = Path
    # global GetHingeHoleBD, GetHandleHoleBD
    # GetHingeHoleBD, GetHandleHoleBD = mGetHingeHoleBD, mGetHandleHoleBD
    # obj = InitData()
    s = XmlTemplate2Json(xml, W, H)
    return s
#解析xml数据
def GetDoorsExp(name):
    Result = {}
    for i in range(0,len(mExpList)):
        if (mExpList[i]['name'] == name):
            Result = mExpList[i]
    return Result
def GetDoorsType(name):
    Result = {}
    for i in range(0,len(mTypeList)):
        if (mTypeList[i]['name'] == name):
            Result = mTypeList[i]
    return Result
def GetDoorsParam(name1, name2):
    Result = {}
    for i in range(0,len(mParamList)):
        if (mParamList[i]['name'] == name2 and mParamList[i]['DoorsType'] == name1):
            Result = mParamList[i]
    return Result
def GetHBoxParam(name):
    Result = {}
    for i in range(0,len(mHBoxParamList)):
        if (mHBoxParamList[i]['name'] == name):
            Result = mHBoxParamList[i]
    return Result
def GetDoorsHandle(name):
    Result = {}
    for i in range(0,len(mHandleList)):
        if (mHandleList[i]['name'] == name):
            Result = mHandleList[i]
    return Result
def LoadFromXMLTemplate(xml, l, h):
    global mGuid,mL,mH,mLMFValue,mHMFValue,mMMFValue, mDataMode,mExtra, \
        mPExp,mCoverType,mPType,mPParam,mPHBoxParam,mMyPanelType,\
        mMyDoorsColor,mMyVBoxColor,mMyHBoxColor,mMyPanelColor,mZNMJ,\
        mGridItem,mCopyDoor,mLCap,mRCap,mUCap,mDCap,mIsVertical,\
        mDoorMemo,mExtend,mHingeHole
    p = create_string_buffer(102400)
    p.value = xml.decode('utf8')
    state = QdUpTemplate.UpXDiyDoorsTemplate(p, c_int(l), c_int(h))
    if state==-1:
        return ''
    xmltemplate = p.value.decode('gbk').encode('utf8')
    if (xmltemplate == ''):
        return
    mDataMode = 0
    root = ET.fromstring(xmltemplate)
    mAddLength = int(float(root.get('延长导轨', 0)))
    InitData()
    attri = root.get('guid', str(uuid.uuid1()))
    mGuid = attri
    mL = float(root.get('门洞宽', l))
    mH = float(root.get('门洞高', h))
    mLMFValue = float(root.get('L门缝', 0).replace(' ',''))
    mHMFValue = float(root.get('H门缝', 0).replace(' ',''))
    mMMFValue = float(root.get('M门缝', 0).replace(' ',''))
    attri = root.get('单门数量类型', '')
    mPExp = GetDoorsExp(attri)
    mDataMode = int(float(root.get('DataMode', '0')))
    mExtra = root.get('Extra', '')
    mCoverType = float(root.get('CT', '0'))
    string = root.get('门类型', '')
    mPType = GetDoorsType(string)
    attri = root.get('门框类型', '')
    mPParam = GetDoorsParam(string, attri)
    attri = root.get('中横框类型', '')
    mPHBoxParam = GetHBoxParam(attri)   #中横框
    attri = root.get('门芯类型', '')
    mMyPanelType = attri
    mMyDoorsColor = root.get('门颜色', '')
    mMyVBoxColor = root.get('门框颜色', '')
    mMyHBoxColor = root.get('中横框颜色', '')
    mMyPanelColor = root.get('门芯颜色', '')
    attri = root.get('ZNMJ', '')
    if attri!='' and attri =='1':
        mZNMJ = 1
    else:
        mZNMJ = 0
    mGridItem = 0
    mGridItem = int(root.get('均分', 0))
    if ((not mPExp) or  (not mPType) or (not mPParam)):
        mCopyDoor = -1
        return ''
    mLCap = int(root.get('左盖', 0))
    mRCap = int(root.get('右盖', 0))
    mUCap = int(root.get('上盖', 0))
    mDCap = int(root.get('下盖', 0))
    mIsVertical = root.get('是否竖排', False)
    if mIsVertical !=False and (mIsVertical=='true' or mIsVertical=='True' or mIsVertical=='TRUE' or mIsVertical==True):
        mIsVertical = True
    mDoorMemo = root.get('DoorMemo', '')
    mExtend = root.get('Extend', '')
    if mExtend !='': mExtend = urllib.parse.quote(mExtend)
    mHingeHole = root.get('HingeHole', '')
    return xmltemplate
def XmlTemplate2Json(Templatexml, l, h):
    global mIsSetDoors,mDoorsList
    mLockControl = False
    if (not Templatexml):
        return {}
    Templatexml = LoadFromXMLTemplate(Templatexml, l, h)
    if Templatexml == '':
        return {}
    Result = 0
    t = 0
    mIsSetDoors = True
    doorw = mL
    doorh = mH
    mDoorsList = []
    def ReadXML(Templatexml):
        root = ET.fromstring(Templatexml)
        jsonobj = []
        Node = {}
        arr = root.attrib
        Node[root.tag] = arr
        Xml2Json(root, Node[root.tag])
        return Node
    MBData = ReadXML(Templatexml)
    mDoorsList = MBData['掩门']['单门']
    if (len(mDoorsList) > 0):
        if mPType['isframe']: t = 1
        door = mDoorsList[0]
        doorw = door['宽']
        doorh = door['高']
    jo = {}
    jo['Extend'] = mExtend
    jo['门款类型'] = mPParam['name']
    jo['是否带框'] = t
    jo['HingeHole'] = mHingeHole
    jo['DoorMemo'] = mDoorMemo
    jo['DoorExtra'] = mExtra
    jo['门洞宽'] = int(mL) if int(mL)==float(mL) else float(mL)
    jo['门洞高'] = int(mH) if int(mH)==float(mH) else float(mH)
    jo['成品门宽'] = doorw
    jo['成品门高'] = doorh
    jo['扇数'] = len(mDoorsList)
    jo['DoorType'] = 2
    jo['报价'] = []
    ja = None
    ja = GetXMLBom(Templatexml, mL, mH)
    for i in range(len(ja)-1, -1, -1):
        if (ja[i]['Name'] == "无中横" or ja[i]['Name'] == "无拉手" or ja[i]['Name'] == "无门铰"):
            del ja[i]
    print('ja=',len(ja))
    jo['物料'] = ja
    #print json.dumps(jo,ensure_ascii=False)
    return jo
def Xml2Json(node, jsonobj):
    for i in range(0,len(node)):
        cnode = node[i]
        NodeName = cnode.tag
        subarr={}
        subattrs = cnode.attrib
        if NodeName not in jsonobj:
            jsonobj[NodeName]=[]
        jsonobj[NodeName].append(subattrs)
        if (len(cnode)>=0):
            Xml2Json(cnode, jsonobj[NodeName][len(jsonobj[NodeName])-1])
def findName(name, vlist):
    Result = {}
    for ii in range(len(vlist)):
        if (vlist[ii]['name'] == name):
            Result = vlist[ii]
    return Result
def TDoorRect(mDoorsList,i):
    mDoorsobject = mDoorsList[i]
    doo= {"doorw":0,"doorh":0}
    doo['doorw'] = float(mDoorsobject['宽'])
    doo['doorh'] = float(mDoorsobject['高'])
    doo['mMemo'] = mDoorsobject['Memo']
    doo['mOpenDirect'] = mDoorsobject['打开方向']
    doo['x1'] = float(mDoorsobject['X1'])
    doo['y1'] = float(mDoorsobject['Y1'])
    doo['mHandle'] = mDoorsobject['拉手']
    doo['mHinge'] = mDoorsobject['门铰']
    doo['mHingeCt'] = mDoorsobject['门铰CT']
    doo['mHandleW'] = float(mDoorsobject['HandleW'])
    doo['mHandleH'] = float(mDoorsobject['HandleH'])
    doo['mHandleX'] = float(mDoorsobject['HandleX'])
    doo['mHandleY'] = float(mDoorsobject['HandleY'])
    doo['mHandlePos'] = mDoorsobject['HandlePos']
    doo['mHingeHoleExtra'] ='' if 'HingeHoleExtra' not in mDoorsobject else mDoorsobject['HingeHoleExtra']
    doo['mHingeHoleDes'] ='' if 'HingeHoleDes' not in mDoorsobject else mDoorsobject['HingeHoleDes']
    doo['mHingeHoleParam'] = '' if 'HingeHoleParam' not in mDoorsobject else mDoorsobject['HingeHoleParam']
    doo['mHingeSideXmlpos'] = '' if 'HingeSideXmlpos' not in mDoorsobject else mDoorsobject['HingeSideXmlpos']
    doo["boxlist"] ="" if '中横框' not in mDoorsobject else mDoorsobject['中横框']
    doo["panellist"] = mDoorsobject['门芯']
    return doo
def SortVar(Item1,Item2):
    p1 = Item1
    p2 = Item2
    Result = 0
    N1 = len(p1[0])
    n2 = len(p2[0])
    if N1 > n2 :
        Result= -1
    if N1 < n2 :
        Result= 1
    return Result
def SAndDoorSetSubject(string , mExp):
    if string==None:
        return string
    if isinstance(string, float) or isinstance(string, int) or string.isdigit():  #是数值就不需要替换的
        return string
    if string == '':
        return 0
    items = list(mExp.items())
    items.sort(SortVar)
    for key ,value in items:
        string = string.replace(key,str(value))
    try:
        if string.isdigit():
            return eval(string)
        return eval(string)
    except:
        return string
def SupplementPwl(attrib, pwl, defaultvalue=''):
    if attrib not in pwl:
        pwl[attrib] = defaultvalue
    return pwl[attrib]
def EscapeBracket(string):
    n = string.find('(')
    if n>-1:
        return string[0:n]
    else:
        return string
def findMzhBiao2(jo):
    Result = None
    cfglist = aTablevalue["门转换表.cfg"]
    n = len(cfglist)
    for i in range(0, n):
        cfg = cfglist[i]
        if( cfg['模式']!= str(mDataMode) ):
            continue
        if( cfg['名称']!=jo['name'] ):
            continue
        if( cfg['物料名称']=='' ):
            continue
        s = cfg['边框类型'] + ','
        ss = jo['doorname'] + ','
        t = s.find(ss)
        if( t<0 ):
            continue
        return cfg
def NewWLData():
    pwl = {}
    pwl["ono"] = ''
    pwl["gno"] = ''
    pwl["hno"] = ''
    pwl["name"] = ''
    pwl["direct"] = ''
    pwl["myunit"] = ''
    pwl["bomtype"] = ''
    pwl["num"] = 1
    pwl["l"] = 0
    pwl["w"] = 0
    pwl["h"] = 0
    pwl["code"] = ''
    pwl["color"] = ''
    pwl["group"] = 0
    pwl["isglass"] = 0
    pwl["fbstr"] = ''
    pwl["memo"] = ''
    pwl["memo2"] = ''
    pwl["memo3"] = ''
    pwl["doormemo"] = ''
    pwl["bdfile"] = ''
    pwl["doorname"] = mPParam['name']
    pwl["is_buy"] = 0
    pwl["door_index"] = 0
    pwl["pnl_num"] = 0
    pwl["pnl_index"] = 0
    return pwl
def ToValueInt(string):
    if isinstance(string, float) or isinstance(string, int) or string.isdigit():  #是数值就不需要替换的
        return int(string)
    try:
        if(string == ''):
            return 0
        num = eval(string)
        return int(num)
    except Exception as e:
        print(e)
def ToValueFloat(string):
    if isinstance(string, float) or isinstance(string, int) or string.isdigit():  #是数值就不需要替换的
        return float(string)
    try:
        if (string == ''):
            return 0
        num = eval(string)
        return Number(num)
    except Exception as e:
        print(e)
def GetWjBom(name):
    Result = {}
    for i in range(len(mWJBomList)):
        pwjbom = mWJBomList[i]
        if (pwjbom['name'] == name):
            Result = pwjbom
    return Result
def GetAccessory(name):
    Result = {}
    for i in range(len(mAccessoryList)):
        pa = mAccessoryList[i]
        if (pa['name'] == name):
            Result = pa
    return Result
def GetColorClass(myclass,color):
    Result = {}
    for i in range(len(mColorClassList)):
        p = mColorClassList[i]
        if (p['myclass'] == myclass and p['color'] == color):
            Result = p
    return Result
def GetColorClass2(bktype,color):
    Result = {}
    for i in range(len(mColorClass2List)):
        pa = mColorClass2List[i]
        if (pa['bktype'] == bktype and pa['color'] == color):
            Result = pa
    return Result
def GetPanelType(bktype,name):
    Result = {}
    for i in range(len(mPanelTypeList)):
        p = mPanelTypeList[i]
        if (p['name'] == name and p['bktype'] == '*'):
            Result = p
            return Result
        if (p['name'] == name and p['bktype'] == bktype):
            Result = p
            return Result
    return Result
def AddWjBom(ALLlist, name, door_bh, opendirect, bktype):
    def arryFindstr(arr, string):
        for k in range(len(arr)):
            if (arr[k] == string):
                return True
        return False
    pwjbom = GetWjBom(name)
    if (pwjbom):
        for i in range(len(mWJBomDetailList)):
            pwjbomdetail = mWJBomDetailList[i]
            if ((pwjbomdetail['bomname'] == pwjbom['name']) and ((pwjbomdetail['door_bh'] == 0)
                                                                 or (pwjbomdetail['door_bh'] == door_bh))
                    and ((pwjbomdetail['opendirect'] == '') or (pwjbomdetail['opendirect'] == opendirect))
                    and ((pwjbomdetail['bktype'] == '') or (arryFindstr(pwjbomdetail['bktypeAry'], bktype)))):
                pwl = NewWLData()
                pwl['name'] = pwjbomdetail['name']
                pwl['l'] = SAndDoorSetSubject(pwjbomdetail['l'], mExp)
                pwl['l'] = ToValueFloat(pwl['l'])
                pwl['h']= SAndDoorSetSubject(pwjbomdetail['d'], mExp)
                pwl['h']= ToValueFloat(pwl['h'])
                ##print pwjbomdetail['num'],json.dumps(mExp,ensure_ascii=False)
                pwl['num'] = SAndDoorSetSubject(pwjbomdetail['num'], mExp)
                pwl['num'] = ToValueInt(pwl['num'])
                #print pwl['num'],len(ALLlist)
                pwl['group'] = 3
                pa = GetAccessory(pwl['name'])
                if (pa):
                    pwl['color'] = pa['color']
                    pwl['memo'] = pa['memo']
                    pwl['bdfile'] = pa['bdfile']
                    pcolorclass2 = GetColorClass2(mPParam['name'], mMyVBoxColor)
                    if (pcolorclass2):
                        if ( pa['color'] == '$边框配件颜色1' ):pwl['color'] = pcolorclass2['bkcolor1']
                        if ( pa['color'] == '$边框配件颜色2' ):pwl['color'] = pcolorclass2['bkcolor2']
                        if ( pa['color'] == '$边框配件颜色3' ):pwl['color'] = pcolorclass2['bkcolor3']
                        if ( pa['color'] == '$边框配件颜色4' ):pwl['color'] = pcolorclass2['bkcolor4']
                    pwl['group'] = 2
                    pwl['bomtype'] = pa['bomtype']
                    if ( (pa['bomtype'] == '木板') or (pa['bomtype'] == '玻璃') or (pa['bomtype'] == '百叶') or (pa['bomtype'] == '板材') ):
                        pwl['bomtype'] = '板材'
                    if ( pa['bomtype'] == '型材五金' ): pwl['group'] = 1
                    if ( pa['bomtype']== '五金' ): pwl['group'] = 3
                    if ( pa['bomtype'] == '玻璃' ): pwl['isglass'] = 1
                ALLlist.append(pwl)
def GetParamXMLBom(ALLlist,string,doorindex,x,z,l,h):
    def GraphSizeToBomSize(l, p, h, direct, pwl):
        pwl['bl'] = l
        pwl['bp']= p
        pwl['bh'] = h
        if (direct == 1): #// 宽深高
            pwl['bl'] = l
            pwl['bp'] = p
            pwl['bh'] = h
        if (direct == 2): #// 宽高深
            pwl['bl'] = l
            pwl['bp'] = h
            pwl['bh'] = p
        if (direct == 3): #// 高宽深
            pwl['bl'] = h
            pwl['bp'] = l
            pwl['bh'] = p
        if (direct == 4): #// 高深宽
            pwl['bl'] = h
            pwl['bp'] = p
            pwl['bh'] = l
        if (direct == 5): #// 深宽高
            pwl['bl'] = p
            pwl['bp'] = l
            pwl['bh'] = h
        if (direct == 6): #// 深高宽
            pwl['bl'] = p
            pwl['bp'] = h
            pwl['bh'] = l
    xml = ''
    exp = {}
    for i in range(0, len(mDoorXMLList)):
        p = mDoorXMLList[i]
        if (string == p['name']):
            xml = p['xml']
            break
    root = ET.fromstring(xml)
    node = None
    if (len(root) > 0):
        for j in range(0 , len(root)):
             if (root[j].tag == "变量列表"):
                 node= root[j]
                 break
    if (node):
        for i in range(0, len(node)):
            cnode = node[i]
            if (cnode.attrib=={}):
                continue
            vname = ''
            vvar = ''
            vname = cnode.get('名称', '')
            vvar = cnode.get('值', '')
            exp[vname] = vvar
    exp['L'] = '%.4f'%l
    exp['H'] = '%.4f'%h
    node = None
    if (len(root) > 0):
        for j in range(0, len(root)):
            if (root[j].tag == "我的模块"):
                node= root[j]
                break
    if (node):
        for i in range(0, len(node)):
            cnode = node[i]
            if (cnode.attrib=={}):
                continue
            atxt = cnode.get('输出类型','')
            if ((atxt) and ((atxt == '报价') or (atxt == '无'))): continue
            di = 0
            attri = cnode.get('DI', 0)
            di = int(attri)
            ll = 0
            dd = 0
            hh = 0
            attri = cnode.get('宽', '0')
            if (attri):
                ll = SAndDoorSetSubjectattri(attri, exp)
                ll = ToValueFloat(ll)
                attri = cnode.GET('深', '0')
                if (attri):
                    dd = SAndDoorSetSubjectattri(attri, exp)
                    dd = ToValueFloat(dd)
                    attri = attri = cnode.GET('高', '0')
                    if (attri):
                        hh = SAndDoorSetSubjectattri(attri, exp)
                        hh = ToValueFloat(hh)
                        pwl = NewWLData()
                        attri = cnode.get('名称', '')
                        if (attri): pwl['name'] = attri
                        GraphSizeToBomSize(ll, dd, hh, di, pwl)
                        attri = cnode.get('Num', '0')
                        if (attri): pwl['num'] = int(attri)
                        attri =  cnode.get('颜色')
                        if (attri): pwl['color'] = attri
                        pwl['color'] = pwl['color'].replace('$边框颜色', mMyVBoxColor)
                        attri = cnode.get('备注')
                        if (attri): pwl['memo'] = attri
                        attri = cnode.get('BOMTYPE')
                        if (attri): pwl['bomtype'] = attri
                        pwl['group'] = 2
                        if (pwl['bomtype'] == '玻璃'): pwl['isglass'] = 1
                        if ((pwl['bomtype'] == '木板') or (pwl['bomtype'] == '玻璃') or (pwl['bomtype'] == '百叶') or (pwl['bomtype'] == '板材')):
                            pwl['bomtype'] = '板材'
                        if (pwl['bomtype'] == '型材五金'): pwl['group'] = 1
                        if (pwl['bomtype'] == '五金'): pwl['group'] = 3
                        pwl['door_index'] = doorindex
                        ALLlist.append(pwl)
def Delphi_Round(num):
    if num < 0:
        return -int((Delphi_Round(-num)))
    round10 = num * 10
    round1 = round(num)
    if (round10 - round1 * 10 == -5):
        pint = int(num)
        pvalue = pint % 10  #; // 个位的数值
        if (pvalue % 2): return (pint+1)   #// 奇进偶不进
        else: return pint
    else:
        return int(round1)
def GetHingeNum(phinge, l, d,opendirect):
    Result = 1
    if ((opendirect == '左') or (opendirect == '右')):
        if ((d > phinge['min1']) and (d < phinge['max1'])):
            Result = phinge['num1']
        if ((d > phinge['min2']) and (d < phinge['max2'])):
            Result = phinge['num2']
        if ((d > phinge['min3']) and (d < phinge['max3'])):
            Result = phinge['num3']
        if ((d > phinge['min4']) and (d < phinge['max4'])):
            Result = phinge['num4']
        if ((d > phinge['min5']) and (d < phinge['max5'])):
            Result = phinge['num5']
    else:
        if ((l > phinge['min1']) and (l < phinge['max1'])):
            Result = phinge['num1']
        if ((l > phinge['min2']) and (l < phinge['max2'])):
            Result = phinge['num2']
        if ((l > phinge['min3']) and (l < phinge['max3'])):
            Result = phinge['num3']
        if ((l > phinge['min4']) and (l < phinge['max4'])):
            Result = phinge['num4']
        if ((l > phinge['min5']) and (l < phinge['max5'])):
            Result = phinge['num5']
    return Result
def GetCurHinge(mj,  mHinge):
    Result = None
    if (mj == ''): return Result
    for i in range(len(mCurHingeList)):
        p = mCurHingeList[i]
        if (p['name'] == mj):
            if (p['hingetype'] == mHinge):
                Result = p
    return Result
def	GetHingeName(phinge, ct):
    Result = phinge['name']
    if( phinge['alias']=='' ): return Result
    jo = json.loads(phinge['alias'])
    for i in range(0, 99):
        if ('Na'+str(i+1)) not in jo: continue
        if( jo['Na'+str(i+1)]==''): continue
        na = jo['Na'+str(i+1)]
        t = jo['T'+str(i+1)]
        zn = jo['Zn'+str(i+1)]
        if( zn=='True' or zn =="TRUE" or zn ==True or zn ==1): znmj = 1
        else: znmj = 0
        if( (ct==t) and (mZNMJ==znmj) ):
            Result = na
            break
    return Result
def GetVboxKCInfo(door):
    Result = ''
    d0 = 0
    d1 = 0
    h0 = 0
    for i in range(0, len(door['panellist'])):
        pnl = door['panellist'][i]
        if( d0==0 ):
             d0 = pnl['thick']
             h0 = Delphi_Round(float(pnl['h0']))
        elif( (d1==0) and (pnl['thick']!=d0) ):
             d1 = pnl['thick']
    if((d0>0) and (d1>0) and (d0!=d1)):
        Result = '%s*%s_%s'%(h0, d0, d1)
    else:
        if( d0>0 ):
            Result = '%s*%s'%(h0, d0)
    return Result
def Swap(pwl):
    s3 = pwl['l']
    pwl['l'] = pwl['w']
    pwl['w'] = Number(s3)
def GetHboxKCInfo(door, n, p):
    def GetNearestDownPanel(p):
        Result = None
        t = door['doorh']
        for i in range(0, len(door['panellist'])):
            pnl = door['panellist'][i]
            if ( p == pnl ):continue
            if (((Number(p['y0']) + Number(p['h0'])- pnl['y0']) > 0) and ((Number(p['y0']) + Number(p['h0']) - pnl['y0']) < t)):
                t = (Number(p['y0']) + Number(p['h0']) - pnl['y0'])
                Result = pnl
        return Result
    def GetNearestUpPanel(p):
        Result = None
        t = door['doorh']
        for i in range(0, len(door['panellist'])):
            pnl = door['panellist'][i]
            if (p == pnl):continue
            if (((pnl['y0'] - p['y0']) > 0) and ((pnl['y0'] - p['y0']) < t)):
                t = (pnl['y0'] - p['y0'])
                Result = pnl
        return Result
    Result = ''
    if ((n == 0) and (len(door['panellist']) > 0)): #// 下横框
        pnl = door['panellist'][0]
        Result = '%s'%(pnl['thick'])
        if ((n == 1) and (p) and (len(door['panellist'])> 0)): #// 中横框
            pnl = GetNearestDownPanel(p)
            pnl1 = GetNearestUpPanel(p)
            if ((pnl) and (pnl1)):
                Result = '%s_%s'%( pnl['thick'], pnl1['thick'])
    if ((n == 2) and (len(door['panellist']))): #// 上横框
        pnl = door['panellist'][len(door['panellist'])- 1]
        Result = '%s'%(pnl['thick'])
    return Result
#// /获取当前门的门铰孔，拉手孔信息
def GetHandleHoleBDEx(sign, mHandleW, mHandleH, mOpenDirect):
    if (HoleConfig):
        # log.info('sign=' + str(sign) + ',' + 'mHandleW=' + str(mHandleW) + ',' +
        #          'mHandleH=' + str(mHandleH) + ',' + 'mOpenDirect='+ str(mOpenDirect))
        Result = ''
        with open(RootPath + '\\data\\Door\\doorHoleConfig.js', 'r') as f:
            jsdata = f.read()
        jscontext = execjs.compile(jsdata)
        Result = jscontext.call('GetHandleHoleBD', sign, mHandleW, mHandleH, mOpenDirect)

        # log.info('Result=' + Result)
        return Result
def GetHandleHoleBDEx(sign, mHandleW, mHandleH, mOpenDirect):
    if (HoleConfig):
        # log.info('sign=' + str(sign) + ',' + 'mHandleW=' + str(mHandleW) + ',' +
        #          'mHandleH=' + str(mHandleH) + ',' + 'mOpenDirect='+ str(mOpenDirect))
        Result = ''
        with open(RootPath + '\\QdCloud\\Door\\doorHoleConfig.js', 'r') as f:
            jsdata = f.read().decode('utf8')
        with PyV8.JSLocker():
            ctxt = PyV8.JSContext()
            ctxt.__enter__()
            ctxt.eval(jsdata)
            GetHandleHoleBD = ctxt.locals.GetHandleHoleBD
            Result = GetHandleHoleBD(sign, mHandleW, mHandleH, mOpenDirect)
            ctxt.leave()
        # log.info('Result=' + Result)
        return Result
def	GetJsonFaceA(door, direct): #// -10190
    Result = '[]'
    sx = 0
    sy = 0
    if (door['mHingeHoleDes'] == ''):
        return Result
    if ((door['mOpenDirect'] == '右') or (door['mOpenDirect'] == '左')): door['l'] = door['doorh']
    if ((door['mOpenDirect'] == '上') or (door['mOpenDirect'] == '下')): door['l'] = door['doorw']
    objstr = GetHingeHoleBDEx(door['mHingeHoleDes'], door['l'], door['mOpenDirect'], door['mHingeHoleParam'])
    jo = json.loads(objstr)
    if(not jo):
        return Result
    n = jo['Num']
    ja = []
    for i in range(0, n):
        cjo = {}
        cjo['Type'] = 'VHole'
        iOffset = Delphi_Round(jo['Offset'])
        if(door['mOpenDirect']=='右' ):
            if( direct != '横纹' ):
                sy = 'W-%s'%(iOffset)
                sx = jo['V'+str(i)]
            else:
                sx = 'L-%s'%(iOffset)
                sy = jo['V'+str(i)]
        if (door['mOpenDirect'] == '左'):
            if (direct != '横纹'):
                sy = '%s' % (iOffset)
                sx = jo['V' + str(i)]
            else:
                sx = '%s' % (iOffset)
                sy = jo['V' + str(i)]
        if (door['mOpenDirect'] == '上'):
            if (direct != '横纹'):
                sy = jo['V' + str(i)]
                sx = 'L-%s' % (iOffset)
            else:
                sx = jo['V' + str(i)]
                sy = 'W-%s' % (iOffset)
        if (door['mOpenDirect'] == '下'):
            if (direct != '横纹'):
                sy = jo['V' + str(i)]
                sx = '%s' % (iOffset)
            else:
                sx = jo['V' + str(i)]
                sy = '%s' % (iOffset)
        cjo['Y'] = sy
        cjo['X'] = sx
        cjo['R'] = jo['R']
        if 'Face' not in jo: jo['Face']=''
        if(not jo['Face'] or jo['Face']=='' ): cjo['Face'] = 'A'
        else: cjo['Face'] = jo['Face']
        ja.append(cjo)
        cjo = None
    if('Offset2' in jo and jo['Offset2']>-1):
        for i in range(0,n):
            cjo = {}
            cjo['Type'] = 'VHole'
            iOffset = Delphi_Round(jo['Offset2'])
            if (door['mOpenDirect'] == '左'):
                if (direct != '横纹'):
                    sy = 'W-%s' % (iOffset)
                    sx = jo['V' + str(i)]
                else:
                    sx = 'L-%s' % (iOffset)
                    sy = jo['V' + str(i)]
            if (door['mOpenDirect'] == '右'):
                if (direct != '横纹'):
                    sy = '%s' % (iOffset)
                    sx = jo['V' + str(i)]
                else:
                    sx = '%s' % (iOffset)
                    sy = jo['V' + str(i)]
            if (door['mOpenDirect'] == '下'):
                if (direct != '横纹'):
                    sy = jo['V' + str(i)]
                    sx = 'L-%s' % (iOffset)
                else:
                    sx = jo['V' + str(i)]
                    sy = 'W-%s' % (iOffset)
            if (door['mOpenDirect'] == '上'):
                if (direct != '横纹'):
                    sy = jo['V' + str(i)]
                    sx = '%s' % (iOffset)
                else:
                    sx = jo['V' + str(i)]
                    sy = '%s' % (iOffset)
            cjo['Y'] = sy
            cjo['X'] = sx
            cjo['R'] = jo['R']
            if 'Face' not in jo: jo['Face'] = ''
            if (not jo['Face'] or jo['Face'] == ''):
                cjo['Face'] = 'A'
            else:
                cjo['Face'] = jo['Face']
            ja.append(cjo)
            cjo = None
    jo = None
    objstr = json.dumps(ja)
    ja = None
    Result = objstr.replace('"', '^')
    return Result
def GetHandleHoleScript(s):
    Result = ''
    for i in range(0, len(mHandleList)):
        p = mHandleList[i]
        if (p['name'] == s ):
            Result = p['holescript']
    return Result
def	GetJsonFaceB(door, direct): #// -10190
    Result = '[]'
    sign = ''
    objstr = ''
    sx = 0
    sy = 0
    if (door['mHandlePos'] != ''):
        objstr =door['mHandlePos'].replace('^', '"')
        sign = GetHandleHoleScript(door['mHandle'])
    if sign != '':
        try:
            ja = ctxt.eval('var s = GetHandleHoleBD("%s","%s","%s","%s");'%(sign, door['mHandleW'], door['mHandleH'], door['mOpenDirect']))
            ja = ctxt.eval('var sjson = JSON.stringify(s);')
            jajson = str(ctxt.eval('sjson')).decode('utf8')
            ja  = json.loads(jajson)
        except:
            ja = ''
        if (ja!=''):
            if not ja:
                return Result
            length = len(ja)
            for i in range(0, length):
                cjo = ja[i]
                cjo['Type'] = 'VHole'
                if (door['mOpenDirect'] == '右'):
                    if (direct != '横纹'):
                        sy = '%s' % (str(Delphi_Round(float(door['mHandleX'])+float(cjo['X']))))
                        sx = '%s' % (str(Delphi_Round(float(door['mHandleY'])+float(cjo['Y']))))
                    else:
                        sx = '%s' % (str(Delphi_Round(float(door['mHandleX'])+float(cjo['X']))))
                        sy = '%s' % (str(Delphi_Round(float(door['mHandleY'])+float(cjo['Y']))))
                if (door['mOpenDirect'] == '左'):
                    if (direct != '横纹'):
                        sy = '%s' % (str(Delphi_Round(float(door['mHandleX'])+float(cjo['X']))))
                        sx = '%s' % (str(Delphi_Round(float(door['mHandleY'])+float(cjo['Y']))))
                    else:
                        sx = '%s' % (str(Delphi_Round(float(door['mHandleX'])+float(cjo['X']))))
                        sy = '%s' % (str(Delphi_Round(float(door['mHandleY'])+float(cjo['Y']))))
                if (door['mOpenDirect'] == '上'):
                    if (direct != '横纹'):
                        sx = '%s' % (str(Delphi_Round(float(door['mHandleY'])+float(cjo['Y']))))
                        sy = '%s' % (str(Delphi_Round(float(door['mHandleX'])+float(cjo['X']))))
                    else:
                        sy = '%s' % (str(Delphi_Round(float(door['mHandleY'])+float(cjo['Y']))))
                        sx = '%s' % (str(Delphi_Round(float(door['mHandleX'])+float(cjo['X']))))
                if (door['mOpenDirect'] == '下'):
                    if (direct != '横纹'):
                        sx = '%s' % (str(Delphi_Round(float(door['mHandleY'])+float(cjo['Y']))))
                        sy = '%s' % (str(Delphi_Round(float(door['mHandleX'])+float(cjo['X']))))
                    else:
                        sy = '%s' % (str(Delphi_Round(float(door['mHandleY'])+float(cjo['Y']))))
                        sx = '%s' % (str(Delphi_Round(float(door['mHandleX'])+float(cjo['X']))))
                cjo['Y'] = sy
                cjo['X'] = sx
                if 'Face' not in cjo:  cjo['Face'] = ''
                if (cjo['Face'] == ''): cjo['Face'] = 'B'
                cjo = None
            objstr = json.dumps(ja)
            Result = objstr.replace('"','^')
            ja = None
    return Result
def GetDoorsHinge(mj, dt):
    Result = None
    if( not dt):  return Result
    if( mj == ''): return Result
    for i in range(0, len(mHingeList)):
        p = mHingeList[i]
        if (p['name'] == mj):
            Result = p
    return Result
def GetXMLBom(xml, mL, mH):
    global MBData,aTablevalue,ALLlist,mDataMode,mGridItem,mExp,skcolor1, skcolor2, skcolor3, skcolor4
    def ReadXML(xml):
        global mDataMode,mGridItem
        root = ET.fromstring(xml)
        mDataMode = root.get('mDataMode',0)
        mGridItem = float(root.get('均分', 0))
        # string = root.get(u'门类型', '')
        # attri = root.get(u'门框类型', '')
        # mPParam = GetDoorsParam(string, attri)
        jsonobj = []
        Node = {}
        arr = root.attrib
        Node[root.tag] = arr
        Xml2Json(root, Node[root.tag])
        return Node
    Result = ''
    MBData = ReadXML(xml)
    mDoorsList = MBData['掩门']['单门']
    wldata = {
                 "doorname": "", "ono": "", "gno": "", "hno": "", "code": "", "name": "", "color": "", "direct": "",
                 "myunit": "", "bomtype": "", "fbstr": "", "bdfile": "", "memo": "", "memo2": "", "memo3": "",
                 "doormemo": "", "num": 0, "group": 0, "door_index": 0, "pnl_num": 0, "pnl_index,	isglass": 0,
                 "is_buy": 0, "faceA": '', "faceB": '',"l":0, "w":0, "h":0
    }
    if MBData == {}:
        return Result
    if (not mIsSetDoors): return Result
    mExp = {}
    ALLlist = []
    mExp['$门洞高度'] = mH
    mExp['$门洞宽度'] = mL
    mExp['$重叠数'] = mPExp['capnum']
    mExp['$门扇数'] = mPExp['doornum']
    if (len(mDoorsList) > 0):
        door = mDoorsList[0]
        mExp['$成品门宽度'] = door['宽']
        mExp['$成品门高度'] = door['高']
    if (mDataMode == 0): AddWjBom(ALLlist, mPParam['wjname'], 0, '', mPParam['name'])
    log.debug('ALLlist1='+str(len(ALLlist)))
    for i in range(0, len(mDoorsList)):
        if (mDataMode == 1):break
        door0 = None
        door1 = None
        if (i > 0): door0 = TDoorRect(mDoorsList, i-1)
        if (i < len(mDoorsList)-1): door1 = TDoorRect(mDoorsList, i+1)
        door = TDoorRect(mDoorsList, i)
        for j in range(0, len(door['panellist'])):
            pnl = door['panellist'][j]
            pnltype = GetPanelType(mPParam['name'], pnl['类型'])
            if (pnltype): pnl['thick'] = pnltype['thick']
            else: pnl['thick'] = 0
        if ((door1 != None) and (mPParam['left_doorxml'] != '') and (door['mOpenDirect'] == '左') and (
                door1['mOpenDirect'] == '右')):
            GetParamXMLBom(ALLlist, mPParam['left_doorxml'], i + 1, door['x1'] - mLCap, door['y1'] - mDCap,
                                door['doorw'], door['doorh'])
        elif ((door0 != None) and (mPParam['right_doorxml'] != '') and (door0['mOpenDirect'] == '左') and (
                door['mOpenDirect'] == '右')):
            GetParamXMLBom(ALLlist, mPParam['right_doorxml'], i + 1, door['x1'] - mLCap,
                                door['y1'] - mDCap, door['doorw'], door['doorh'])
        elif (mPParam['doorxml'] != ''):
                GetParamXMLBom(ALLlist, mPParam['doorxml'], i + 1, door['x1'] - mLCap,
                               door['y1'] - mDCap, door['doorw'], door['doorh'])
        log.debug('ALLlist2=' + str(len(ALLlist)))
        bh = Delphi_Round(mPType['depth'])
        if (mPType['isframe']):
            pwl = NewWLData()
            pwl['name'] = mPParam['name']
            pwl['l'] = door['doorw']
            pwl['w'] = door['doorh']
            pwl['h'] = mPType['depth']
            pwl['color'] = mMyVBoxColor
            pwl['group'] = 4
            pwl['memo'] = ''
            pwl['doormemo'] = door['mMemo']
            pwl['bomtype'] = '门框'
            pwl['direct'] = mPParam['vdirect']
            pwl['fbstr'] = mPParam['vfbstr']
            pwl['door_index'] = i + 1
            if (mPParam['noframe_bom'] == 0):
                ALLlist.append(pwl)
                log.debug('ALLlist3=' + str(len(ALLlist)))
        else:
            if ( len(door['panellist']) > 0 ):
                pnl = door['panellist'][0]
                pnltype = GetPanelType(mPParam['name'], pnl['类型'])
                if ( pnltype ):  bh = pnltype['thick']
        mExp['$成品门宽度'] = str(door['doorw'])
        mExp['$成品门高度'] = str(door['doorh'])
        phandle = GetDoorsHandle(door['mHandle'])
        if (phandle):
            pwl = NewWLData()
            pwl['name'] = phandle['name']
            pwl['l'] = SAndDoorSetSubject(phandle['width'], mExp)
            pwl['l'] = ToValueFloat(pwl['l'])
            pwl['w'] = SAndDoorSetSubject(phandle['depth'], mExp)
            pwl['w'] = ToValueFloat(pwl['w'])
            pwl['h'] = SAndDoorSetSubject(phandle['height'], mExp)
            pwl['h'] = ToValueFloat(pwl['h'])
            pwl['color'] = ''
            pwl['group'] = 3
            pwl['memo'] = phandle['memo']
            pwl['bomtype'] = phandle['bomtype']
            pwl['door_index'] = i + 1
            ALLlist.append(pwl)
            log.debug('ALLlist4=' + str(len(ALLlist)))
            AddWjBom(ALLlist, phandle['wjname'], bh, door['mOpenDirect'], mPParam['name'])
            log.debug('ALLlist5=' + str(len(ALLlist)))
        # if (len(door['mHingeHoleExtra']) > 5): #// 非空 那么门铰的输出数据就得从这里输出门铰的数据，以及门铰五金数据。
        #
        #     hExrobj = json.loads(door['mHingeHoleExtra'].replace('^','"'))
        #
        #     if u'门铰' in hExrobj:
        #
        #         for ihige in range(0 ,len(hExrobj[u'门铰'])):
        #
        #             phinge = GetCurHinge(hExrobj[u'门铰'][ihige][u'门铰类型'], door['mHinge'])
        #             if (phinge):
        #                 pwl = NewWLData()
        #                 pwl['name'] = GetHingeName(phinge, door['mHingeCt'])
        #                 pwl['l'] = 1
        #                 pwl['w'] = 1
        #                 pwl['h'] = 1
        #                 pwl['color'] = ''
        #                 pwl['group'] = 3
        #                 pwl['memo'] = phinge['memo']
        #                 pwl['memo2'] = ''
        #                 pwl['num'] = 1
        #                 pwl['bomtype'] = phinge['bomtype']
        #                 pwl['door_index'] = i + 1
        #                 ALLlist.append(pwl)
        #                 log.debug('ALLlist6=' + str(len(ALLlist)))
        #                 for j in range(0, pwl['num']):
        #                     AddWjBom(ALLlist, phinge['wjname'], bh, door['mOpenDirect'], mPParam['name'])
        #                 log.debug('ALLlist7=' + str(len(ALLlist)))
        #         hExrobj = None
        # else:
        phinge = GetDoorsHinge(door['mHinge'], mPType)
        if (phinge):
            pwl = NewWLData()
            pwl['name'] = GetHingeName(phinge, door['mHingeCt'])
            pwl['l'] = 1
            pwl['w'] = 1
            pwl['h'] = 1
            pwl['color'] = ''
            pwl['group'] = 3
            pwl['memo'] = phinge['memo']
            pwl['memo2'] = door['mHingeHoleExtra']
            pwl['num'] = GetHingeNum(phinge, Delphi_Round(door['doorw']),
                                       Delphi_Round(door['doorh']), door['mOpenDirect'])
            pwl['bomtype'] = phinge['bomtype']
            pwl['door_index'] = i + 1
            ALLlist.append(pwl)
            log.debug('ALLlist8=' + str(len(ALLlist)))
            for j in range(pwl['num']):
                AddWjBom(ALLlist, phinge['wjname'], bh, door['mOpenDirect'], mPParam['name'])
            log.debug('ALLlist9=' + str(len(ALLlist)))
        if (mPType['isframe']):
            if (mPParam['iscalc_framebom'] == True): #// 计算横框竖框物料
                pwl = NewWLData()
                pwl['name'] = mPParam['vboxname']
                if (phandle):pwl['memo'] = phandle['name']
                pwl['l'] = SAndDoorSetSubject(mPParam['vboxl'],mExp)
                pwl['l'] = ToValueFloat(pwl['l'])
                pwl['w'] = mPParam['vboxh']
                pwl['color'] = mMyVBoxColor
                pwl['group'] = 1
                pwl['h'] = mPType['depth']
                pwl['memo'] = mPParam['vmemo']
                pwl['memo'] = (pwl['memo'].encode('utf8')).replace('$竖框槽位信息', GetVboxKCInfo(door)).decode('utf8')
                pwl['bomtype'] = mPParam['bomtype']
                pwl['direct'] = mPParam['vdirect']
                pwl['fbstr'] = mPParam['vfbstr']
                pwl['bdfile'] = mPParam['l_bdfile']
                pwl['is_buy'] = mPParam['is_buy']
                pwl['door_index'] = i+1
                if ( mPParam['vdirect'] == '横纹' ): Swap(pwl)
                pwl2 = NewWLData()
                pwl2 = copy.deepcopy(pwl)
                pwl2['bdfile'] = mPParam['r_bdfile']
                if ( mPParam['noframe_bom'] == 0 ): ALLlist.append(pwl)
                if ( mPParam['noframe_bom'] == 0 ): ALLlist.append(pwl2)
                pwl = NewWLData()
                pwl['name'] = mPParam['udboxname']
                pwl['l'] = SAndDoorSetSubject(mPParam['udboxl'], mExp)
                pwl['l'] = ToValueFloat(pwl['l'])
                pwl['w'] = mPParam['udboxh']
                pwl['color'] = mMyVBoxColor
                pwl['group'] = 1
                pwl['h'] = mPType['depth']
                pwl['memo'] = mPParam['udmemo']
                pwl['memo'] = pwl['memo'].replace('$横框槽位信息', GetHboxKCInfo(door, 0, None))
                pwl['bomtype'] = mPParam['bomtype']
                pwl['direct']  = mPParam['uddirect']
                pwl['fbstr']  = mPParam['udfbstr']
                if ( mPParam['uddirect'] == '横纹' ): Swap(pwl);
                pwl['bdfile'] = mPParam['u_bdfile']
                pwl['is_buy'] = mPParam['is_buy']
                pwl['door_index'] = i+1
                pwl2 = NewWLData()
                pwl2 = copy.deepcopy(pwl)
                pwl['memo'] = mPParam['udmemo']
                pwl['memo'] = (pwl['memo'].encode('utf8')).replace('$横框槽位信息', GetHboxKCInfo(door, 2, None)).decode('utf8')
                pwl['bdfile'] = mPParam['d_bdfile']
                if ( mPParam['noframe_bom'] == 0 ):
                    ALLlist.append(pwl)
                if ( mPParam['noframe_bom'] == 0 ):
                    ALLlist.append(pwl2)
                log.debug('ALLlist10=' + str(len(ALLlist)))
            else:
                pwl = NewWLData()
                pwl['name'] = mPParam['name']
                if ( phandle ):
                    pwl['memo'] = phandle['name']
                pwl['l'] = door['doorh'] - mPParam['frame_valueh']
                pwl['w'] = door['doorw'] - mPParam['frame_valuel']
                pwl['color'] = mMyVBoxColor
                pwl['group'] = 1
                pwl['h'] = mPType['depth']
                pwl['memo'] = mPParam['vmemo']
                pwl['bomtype'] = mPParam['bomtype']
                pwl['fbstr'] = mPParam['fbstr']
                pwl['bdfile'] = mPParam['bdfile']
                pwl['is_buy'] = mPParam['is_buy']
                pwl['door_index'] = i+1
                if (mPParam['noframe_bom'] == 0 ):
                    ALLlist.append(pwl)
                log.debug('ALLlist11=' + str(len(ALLlist)))
            for j in range(0, len(door['boxlist'])):
                rb = door['boxlist'][j]
                if (Number(rb['h0']) <= 0):continue
                pwl = NewWLData()
                pwl['name'] = rb['类型']
                pwl['color'] = rb['颜色']
                pwl['l'] = SAndDoorSetSubject(mPParam['udboxl'], mExp)
                pwl['l'] = ToValueFloat(pwl['l']) - mPParam['udbox_hbox_value']
                pwl['w'] = Number(rb['h0'])
                pwl['h'] = Number(rb['d0'])
                pwl['group'] = 1
                pwl['door_index'] = i + 1
                hbox = GetHBoxParam(rb['类型'])
                if (hbox):
                    pwl['direct'] = hbox['direct']
                    if (hbox['direct'] == '横纹'): Swap(pwl)
                    pwl['fbstr'] = hbox['fbstr']
                    pwl['memo'] = hbox['memo']
                    pwl['memo'] = pwl['memo'].replace('$横框槽位信息', GetHboxKCInfo(door, 1, rb))
                    pwl['bomtype'] = hbox['bomtype']
                    pwl['bdfile'] = hbox['bdfile']
                ALLlist.append(pwl)
                log.debug('ALLlist12=' + str(len(ALLlist)))
                if (hbox):
                    AddWjBom(ALLlist, hbox['wjname'], bh, door['mOpenDirect'], mPParam['name'])
                    log.debug('ALLlist13=' + str(len(ALLlist)))
            for j in range(0, len(door['panellist'])):
                pnl = door['panellist'][j]
                mExp['$门板高度0']= str(pnl['h0'])
                mExp['$门板宽度0'] = str(pnl['w0'])
                mExp['$门板高度'] = str(pnl['h1'])
                mExp['$门板宽度']= str(pnl['w1'])
                pnltype = GetPanelType(mPParam['name'], pnl['类型'])
                mytype = ''
                if (pnltype):
                    mytype = pnltype['mytype']
                    GetPanelBom(ALLlist, pnltype['panelbom'], pnl['类型'], pnl['颜色'], pnl['颜色2'], mMyVBoxColor, pnl['w1'], pnl['h1'])
                    log.debug('ALLlist14=' + str(len(ALLlist)))
                glvalue1 = 0
                glvalue2 = 0
                if ( mytype == '玻璃' ):
                    glvalue1 = mPParam['vboxjtw'] * 2
                    pos = GetPanelPosInDoor(door, pnl)
                    if ( (pos == 1) ): #// 最下格
                        glvalue2 = mPParam['hboxjtw'] + mPParam['udboxjtw']
                    if ( (pos == 2) ): #// 最上格
                        glvalue2 = mPParam['hboxjtw'] + mPParam['udboxjtw']
                    if ( (pos == 0) ): #// 中间格
                        glvalue2 = mPParam['hboxjtw'] * 2
                    if ( (pos == -1) ):
                        glvalue2 = mPParam['udboxjtw'] * 2
                if (mytype == '百叶'):
                    LouverList = []
                    pssexp = GetSSExp(pnl['类型'])
                    h = Number(pnl['h1'])
                    w = Number(pnl['w1'])
                    t = 0
                    if (pssexp['height'] != 0):
                        n = int((h - 0 - glvalue2) / pssexp['height'])
                        t = (h - 0 - glvalue2) - pssexp['height'] * n
                        if ( t > pssexp['minheight']):
                            n = n + 1
                        else:
                            t = 0
                        for k in range(0,n):
                            if ( (k == n - 1) and (t != 0) ):
                                pwl = NewWLData()
                                pwl['name'] = pnl['类型'] #// '门芯';
                                pwl['color'] = pnl['颜色']
                                pwl['code'] = ''
                                pwl['l'] = (w - 0 - glvalue1)
                                pwl['w'] = t
                                pcolorclass = GetColorClass('门芯', pnl['颜色'])
                                pwl['direct'] = pnl['纹路']
                                pwl['num'] = 1
                                pwl['group'] = 2
                                pwl['door_index'] = i+1
                                pwl['pnl_num'] = len(door['panellist'])
                                pwl['pnl_index'] = j
                                if ( pnltype ):
                                    pwl['memo'] = pnltype['memo']
                                    pwl['memo2'] = pnltype['memo2']
                                    pwl['memo3'] = pnltype['memo3']
                                    pwl['h'] = pnltype['thick']
                                    pwl['w'] = pwl['w'] - pnltype['lfb']
                                    pwl['l'] = pwl['l'] - pnltype['hfb']
                                    pwl['bomtype'] = pnltype['bomtype']
                                    pwl['fbstr'] = pnltype['fbstr']
                                    pwl['bdfile'] = pnltype['bdfile']
                                    pwl['is_buy'] = pnltype['is_buy']
                                if (pwl['l'] < 0):pwl['l'] = 0
                                if (pwl['w'] < 0):pwl['w'] = 0
                                ALLlist.append(pwl)
                                log.debug('ALLlist15=' + str(len(ALLlist)))
                            else:
                                pwl = NewWLData()
                                pwl['name'] = pnl['类型']  # // '门芯';
                                pwl['color'] = pnl['颜色']
                                pwl['code'] = ''
                                pwl['l'] = (w - 0 - glvalue1)
                                pwl['w'] = pssexp['height']
                                pcolorclass = GetColorClass('门芯', pnl['颜色'])
                                pwl['direct'] = pnl['纹路']
                                pwl['num'] = 1
                                pwl['group'] = 2
                                pwl['door_index'] = i + 1
                                pwl['pnl_num'] = len(door['panellist'])
                                pwl['pnl_index'] = j
                                if (pnltype):
                                    pwl['memo'] = pnltype['memo']
                                    pwl['memo2'] = pnltype['memo2']
                                    pwl['memo3'] = pnltype['memo3']
                                    pwl['h'] = pnltype['thick']
                                    pwl['w'] = pwl['w'] - pnltype['lfb']
                                    pwl['l'] = pwl['l'] - pnltype['hfb']
                                    pwl['bomtype'] = pnltype['bomtype']
                                    pwl['fbstr'] = pnltype['fbstr']
                                    pwl['bdfile'] = pnltype['bdfile']
                                    pwl['is_buy'] = pnltype['is_buy']
                                if (pwl['l'] < 0): pwl['l'] = 0
                                if (pwl['w'] < 0): pwl['w'] = 0
                                ALLlist.append(pwl)
                                log.debug('ALLlist16=' + str(len(ALLlist)))
                    elif (pssexp['width'] != 0):
                        n = int((w - 0 - glvalue1) / pssexp['width'])
                        t = (w - 0 - glvalue1) - pssexp['width'] * n
                        if (t > pssexp['minwidth']):
                            n = n + 1
                        else:
                            t = 0
                        for k in range(0,n):
                            if ( (k == n - 1) and (t != 0) ):
                                pwl = NewWLData()
                                pwl['name'] = pnl['类型'] #// '门芯';
                                pwl['color'] = pnl['颜色']
                                pwl['code'] = ''
                                pwl['l'] = (h - 0 - glvalue2)
                                pwl['w'] = t
                                pcolorclass = GetColorClass('门芯', pnl['颜色'])
                                pwl['direct'] = pnl['纹路']
                                pwl['num'] = 1
                                pwl['group'] = 2
                                pwl['door_index'] = i+1
                                pwl['pnl_num'] = len(door['panellist'])
                                pwl['pnl_index'] = j
                                if ( pnltype ):
                                    pwl['memo'] = pnltype['memo']
                                    pwl['memo2'] = pnltype['memo2']
                                    pwl['memo3'] = pnltype['memo3']
                                    pwl['h'] = pnltype['thick']
                                    pwl['w'] = pwl['w'] - pnltype['lfb']
                                    pwl['l'] = pwl['l'] - pnltype['hfb']
                                    pwl['bomtype'] = pnltype['bomtype']
                                    pwl['fbstr'] = pnltype['fbstr']
                                    pwl['bdfile'] = pnltype['bdfile']
                                    pwl['is_buy'] = pnltype['is_buy']
                                if (pwl['l'] < 0):pwl['l'] = 0
                                if (pwl['w'] < 0):pwl['w'] = 0
                                ALLlist.append(pwl)
                                log.debug('ALLlist17=' + str(len(ALLlist)))
                            else:
                                pwl = NewWLData()
                                pwl['name'] = pnl['类型']  # // '门芯';
                                pwl['color'] = pnl['颜色']
                                pwl['code'] = ''
                                pwl['l'] = (h - 0 - glvalue2)
                                pwl['w'] = pssexp['width']
                                pcolorclass = GetColorClass('门芯', pnl['颜色'])
                                pwl['direct'] = pnl['纹路']
                                pwl['num'] = 1
                                pwl['group'] = 2
                                pwl['door_index'] = i + 1
                                pwl['pnl_num'] = len(door['panellist'])
                                pwl['pnl_index'] = j
                                if (pnltype):
                                    pwl['memo'] = pnltype['memo']
                                    pwl['memo2'] = pnltype['memo2']
                                    pwl['memo3'] = pnltype['memo3']
                                    pwl['h'] = pnltype['thick']
                                    pwl['w'] = pwl['w'] - pnltype['lfb']
                                    pwl['l'] = pwl['l'] - pnltype['hfb']
                                    pwl['bomtype'] = pnltype['bomtype']
                                    pwl['fbstr'] = pnltype['fbstr']
                                    pwl['bdfile'] = pnltype['bdfile']
                                    pwl['is_buy'] = pnltype['is_buy']
                                if (pwl['l'] < 0): pwl['l'] = 0
                                if (pwl['w'] < 0): pwl['w'] = 0
                                ALLlist.append(pwl)
                                log.debug('ALLlist18=' + str(len(ALLlist)))
                else:
                    pwl = NewWLData()
                    pwl['group'] = 2
                    pwl['name'] = pnl['类型']  # // '门芯';
                    pwl['direct'] = pnl['纹路']
                    pwl['color'] = pnl['颜色']
                    pwl['code'] = ''
                    pwl['w'] = float(pnl['w1']) - glvalue1
                    pwl['l'] = float(pnl['h1']) - glvalue2
                    pwl['door_index'] = i + 1
                    pwl['pnl_num'] = len(door['panellist'])
                    pwl['pnl_index'] = j
                    if (mytype == '玻璃'): pwl['isglass'] = 1
                    if (pnltype):
                        pwl['memo'] = pnltype['memo']
                        pwl['memo2'] = pnltype['memo2']
                        pwl['memo3'] = pnltype['memo3']
                        pwl['h'] = pnltype['thick']
                        pwl['w'] = float(pwl['w']) - pnltype['lfb']
                        pwl['l'] = float(pwl['l']) - pnltype['hfb']
                        if (pnltype['direct'] == '横纹'): Swap(pwl)
                        pwl['bomtype'] = pnltype['bomtype']
                        pwl['fbstr'] = pnltype['fbstr']
                        pwl['bdfile'] = pnltype['bdfile']
                        pwl['is_buy'] = pnltype['is_buy']
                    ALLlist.append(pwl)
                    log.debug('ALLlist19=' + str(len(ALLlist)))
        else:
            for j in range(0, len(door['panellist'])):
                pnl = door['panellist'][j]
                pnltype = GetPanelType(mPParam['name'], pnl['类型'])
                mytype = ''
                if (pnltype):
                    mytype = pnltype['mytype']
                    GetPanelBom(ALLlist, pnltype['panelbom'], pnl['类型'], pnl['颜色'], pnl['颜色2'], mMyVBoxColor,
                                pnl['w1'], pnl['h1'])
                glvalue1 = 0
                glvalue2 = 0
                pwl = NewWLData()
                pwl['faceA'] = GetJsonFaceA(door, pnl['纹路'])
                pwl['faceB'] = GetJsonFaceB(door, pnl['纹路'])
                pwl['group'] = 2
                pwl['name'] = pnl['类型']
                pwl['direct'] = pnl['纹路']
                pwl['color'] = pnl['颜色']
                pwl['w'] = float(pnl['w1']) - glvalue1
                pwl['l'] = float(pnl['h1']) - glvalue2
                pwl['door_index'] = i + 1
                pwl['pnl_num'] = len(door['panellist'])
                pwl['pnl_index'] = j
                if (mytype == '玻璃'): pwl['isglass'] = 1
                if (pnltype):
                    pwl['memo'] = pnltype['memo']
                    pwl['memo2'] = pnltype['memo2']
                    pwl['memo3'] = pnltype['memo3']
                    pwl['h'] = pnltype['thick']
                    pwl['w'] = float(pwl['w']) - pnltype['lfb']
                    pwl['l'] = float(pwl['l']) - pnltype['hfb']
                    if (pnltype['direct'] == '横纹'): Swap(pwl)
                    pwl['bomtype'] = pnltype['bomtype']
                    pwl['fbstr'] = pnltype['fbstr']
                    pwl['bdfile'] = pnltype['bdfile']
                    pwl['is_buy'] = pnltype['is_buy']
                if (len(door['panellist']) == 1): pwl['doormemo'] = door['mMemo']
                if (phandle):
                    pwl['memo'] = phandle['name']
                ALLlist.append(pwl)
                log.debug('ALLlist20=' + str(len(ALLlist)))
    #// 定款门按照单门输出
    for i in range(0, len(mDoorsList)):
        if (mDataMode == 0):
            break
        door = TDoorRect(mDoorsList, i)
        pwl = NewWLData()
        pwl['name'] = mPParam['name']
        pwl['color'] = mMyVBoxColor
        pwl['num'] = 1
        pwl['memo'] = mPParam['vmemo']
        pwl['l'] = door['doorh']
        pwl['w'] = door['doorw']
        pwl['group'] = 2
        pwl['bomtype'] = '门框'
        ALLlist.append(pwl)
    log.debug('ALLlist20=' + str(len(ALLlist)))
    # 自选配件
    if '配件' in MBData:
        treelist2 = MBData['配件']
        if (treelist2):
            for i in range(0, len(treelist2)):
                pwl = NewWLData()
                pwl['name'] = treelist2[i]['名称']
                pwl['code'] = pwl['code']
                pwl['color'] = ''
                pwl['l'] = 0
                pwl['w'] = 0
                pwl['h'] = 0
                pwl['num'] = int(treelist2[i]['数量'])
                pwl['group'] = 3
                pwl['bomtype'] = '五金'
                ALLlist.append(pwl)
    list2 = []
    j = 1
    for i in range(0, len(ALLlist)):
        pwl = ALLlist[i]
        if (eval(str(pwl['num'])) <= 0):
            continue
        if 'w' not in pwl :
            pwl['w'] = 0
        if 'l' not in pwl :
            pwl['l'] = 0
        if 'h' not in pwl :
            pwl['h'] = 0
        if 'code' not in pwl or pwl['code']=='':
            pwl['code'] = j
        try:
            l = float(pwl['l'])
        except:
            l = pwl['l']
        newpw2 = {}
        newpw2 ["Num"] = int(float(eval(str(pwl['num']))))
        newpw2["W"] = ''
        newpw2["L"] = ''
        newpw2["H"] = ''
        if pwl['w'] !='':
            newpw2["W"] =str(int(Number(pwl['w']))) if int(Number(pwl['w']))==float(pwl['w']) else str(float(pwl['w']))
        if pwl['l'] != '':
            newpw2["L"] = str(int(Number(pwl['l']))) if int(Number(pwl['l']))==float(pwl['l']) else str(float(pwl['l']))
        if pwl['h'] != '':
            newpw2["H"] = str(int(Number(pwl['h']))) if int(Number(pwl['h']))==float(pwl['h']) else str(float(pwl['h']))
        newpw2["#"] = j
        newpw2["DoorIndex"] = SupplementPwl('door_index', pwl)
        newpw2["IsBuy"] = SupplementPwl('is_buy', pwl)
        newpw2["PanelIndex"] = SupplementPwl('pnl_index', pwl)
        newpw2["Group"] = SupplementPwl('group', pwl)
        newpw2["Glass"] = SupplementPwl('isglass', pwl)
        newpw2["Di"] = SupplementPwl('direct', pwl)
        newpw2["PanelNum"] = SupplementPwl('pnl_num', pwl, defaultvalue='0')
        newpw2["DoorName"] = SupplementPwl('doorname', pwl)
        newpw2["Unit"] = SupplementPwl('myunit', pwl)
        newpw2["Name"] = EscapeBracket(SupplementPwl('name', pwl))
        newpw2["Code"] = SupplementPwl('code', pwl)
        newpw2["Memo"] = SupplementPwl('memo', pwl)
        newpw2["Memo2"] = SupplementPwl('memo2', pwl)
        newpw2["Color"] = SupplementPwl('color', pwl)
        newpw2["Bomtype"] = SupplementPwl('bomtype', pwl)
        newpw2["Memo3"] = SupplementPwl('memo3', pwl)
        newpw2["Bomsize"] = SupplementPwl('bomsize', pwl)
        newpw2["FaceA"] = SupplementPwl('faceA', pwl)
        newpw2["FaceB"] = SupplementPwl('faceB', pwl)
        newpw2["FBStr"] = SupplementPwl('fbstr', pwl)
        newpw2["DoorMemo"] = SupplementPwl('doormemo', pwl)
        newpw2['BDXMLID'] = ''
        newpw2["BDFILE"] = SupplementPwl('bdfile', pwl)
        if newpw2["BDFILE"] !='' and os.path.exists(RootPath.decode('gbk') +'\\' +newpw2["BDFILE"]):
            with open(RootPath.decode('gbk') +'\\' +newpw2["BDFILE"], 'r') as f:
                xml = f.read()
            root = BD2XML1(xml, newpw2)
            text = root.toxml('utf-8')
            #log.info('text='+text.decode('utf8'))
            newpw2['BDXML'] = text.replace('"',"'")
            newpw2['BDXMLID'] = ''.join(str(uuid.uuid1()).split('-'))
            newpw2['BDFILE'] = ''
        j = j + 1
        list2.append(newpw2)
    return list2
def BD2XML1(xml, newpw2):
    xml = xml.decode('gbk').encode('utf-8').replace('gb2312','utf-8')
    DOMTree = DOM.parseString(xml)
    root = DOMTree.documentElement
    root.setAttribute('L', newpw2["L"])
    root.setAttribute('W', newpw2["W"])
    root.setAttribute('BH', newpw2["H"])
    nodeA = None
    nodeB = None
    for i in range(0, len(root.childNodes)):
        node = root.childNodes[i]
        if node.nodeName.upper() =='FACEA':
            nodeA = node
        if (node.nodeName.upper() =='FACEB'):
            nodeB = node
        if (nodeB and nodeA):break
    if (not nodeA): #// 创建节点 FaceA
        # 设置根结点emps
        nodeA = DOMTree.createElement('FaceA')
        #nodeA = ET.Element('FaceA', {})
        root.appendChild(nodeA)
    if (not nodeB): #// 创建节点 FaceB
        nodeB = DOMTree.createElement('FaceB')
        root.appendChild(nodeB)
    if 'FaceA' in newpw2 and newpw2['FaceA']!='' :
        objstr = newpw2['FaceA']
        objstr = objstr.replace('^', '"')
        ja = json.loads(objstr)
        for i in range(0, len(ja)):
            cjo = ja[i]
            cnode = DOMTree.createElement(cjo['Type'])
            if ( cjo['Face'] == 'A' ): nodeA.appendChild(cnode)
            elif ( cjo['Face'] == 'B' ): nodeB.appendChild(cnode)
            else:
                cnode = None
                continue
            if 'X' not in cjo:
                cjo['X'] = ''
            cnode.setAttribute('X', str(cjo['X']))
            if 'Y' not in cjo:
                cjo['Y'] = ''
            cnode.setAttribute('Y', str(cjo['Y']))
            if 'R' not in cjo:
                cjo['R'] = ''
            cnode.setAttribute('R', str(cjo['R']))
            if 'Rb' not in cjo:
                cjo['Rb'] = ''
            cnode.setAttribute('Rb', str(cjo['Rb']))
            if 'HDirect' not in cjo:
                cjo['HDirect'] = ''
            cnode.setAttribute('HDirect', str(cjo['HDirect']))
            if 'Face' not in cjo:
                cjo['Face'] = ''
            cnode.setAttribute('Face', str(cjo['Face']))
            if 'Hole_Z' not in cjo:
                cjo['Hole_Z'] = ''
            cnode.setAttribute('Hole_Z', str(cjo['Hole_Z']))
            cjo = None
        ja = None
    if 'FaceB' in newpw2 and newpw2['FaceB']!='' :
        objstr = newpw2['FaceB']
        objstr = objstr.replace('^', '"')
        ja = json.loads(objstr)
        for i in range(0, len(ja)):
            cjo = ja[i]
            cnode = DOMTree.createElement(cjo['Type'])
            if ( cjo['Face'] == 'A' ): nodeA.appendChild(cnode)
            elif ( cjo['Face'] == 'B' ): nodeB.appendChild(cnode)
            else:
                cnode = None
                continue
            if 'X' not in cjo:
                cjo['X'] = ''
            cnode.setAttribute('X', str(cjo['X']))
            if 'Y' not in cjo:
                cjo['Y'] = ''
            cnode.setAttribute('Y', str(cjo['Y']))
            if 'R' not in cjo:
                cjo['R'] = ''
            cnode.setAttribute('R', str(cjo['R']))
            if 'Rb' not in cjo:
                cjo['Rb'] = ''
            cnode.setAttribute('Rb', str(cjo['Rb']))
            if 'HDirect' not in cjo:
                cjo['HDirect'] = ''
            cnode.setAttribute('HDirect', str(cjo['HDirect']))
            if 'Face' not in cjo:
                cjo['Face'] = ''
            cnode.setAttribute('Face', str(cjo['Face']))
            if 'Hole_Z' not in cjo:
                cjo['Hole_Z'] = ''
            cnode.setAttribute('Hole_Z', str(cjo['Hole_Z']))
            cjo = None
        ja = None
    return root
def BD2XML(xml, newpw2):
    xml = xml.decode('gbk').encode('utf-8').replace('gb2312','utf-8')
    root = ET.fromstring(xml)
    root.set('L', newpw2["L"])
    root.set('W', newpw2["W"])
    root.set('BH', newpw2["H"])
    nodeA = None
    nodeB = None
    for i in range(0, len(root)):
        node = root[i]
        if node.tag.upper() =='FACEA':
            nodeA = node
        if (node.tag.upper() =='FACEB'):
            nodeB = node
        if (nodeB and nodeA):break
    if (not nodeA): #// 创建节点 FaceA
        nodeA = ET.Element('FaceA', {})
        root.append(nodeA)
    if (not nodeB): #// 创建节点 FaceB
        nodeB = ET.Element('FaceB', {})
        root.append(nodeB)
    if 'FaceA' in newpw2 and newpw2['FaceA']!='' :
        objstr = newpw2['FaceA']
        objstr = objstr.replace('^', '"')
        ja = json.loads(objstr)
        for i in range(0, len(ja)):
            cjo = ja[i]
            cnode = ET.Element(cjo['Type'], {})
            if ( cjo['Face'] == 'A' ): nodeA.append(cnode)
            elif ( cjo['Face'] == 'B' ): nodeB.append(cnode)
            else:
                cnode = None
                continue
            if 'X' not in cjo:
                cjo['X'] = ''
            cnode.set('X', str(cjo['X']))
            if 'Y' not in cjo:
                cjo['Y'] = ''
            cnode.set('Y', str(cjo['Y']))
            if 'R' not in cjo:
                cjo['R'] = ''
            cnode.set('R', str(cjo['R']))
            if 'Rb' not in cjo:
                cjo['Rb'] = ''
            cnode.set('Rb', str(cjo['Rb']))
            if 'HDirect' not in cjo:
                cjo['HDirect'] = ''
            cnode.set('HDirect', str(cjo['HDirect']))
            if 'Face' not in cjo:
                cjo['Face'] = ''
            cnode.set('Face', str(cjo['Face']))
            if 'Hole_Z' not in cjo:
                cjo['Hole_Z'] = ''
            cnode.set('Hole_Z', str(cjo['Hole_Z']))
            cjo = None
        ja = None
    if 'FaceB' in newpw2 and newpw2['FaceB']!='' :
        objstr = newpw2['FaceB']
        objstr = objstr.replace('^', '"')
        ja = json.loads(objstr)
        for i in range(0, len(ja)):
            cjo = ja[i]
            cnode = ET.Element(cjo['Type'], {})
            if ( cjo['Face'] == 'A' ): nodeA.append(cnode)
            elif ( cjo['Face'] == 'B' ): nodeB.append(cnode)
            else:
                cnode = None
                continue
            if 'X' not in cjo:
                cjo['X'] = ''
            cnode.set('X', str(cjo['X']))
            if 'Y' not in cjo:
                cjo['Y'] = ''
            cnode.set('Y', str(cjo['Y']))
            if 'R' not in cjo:
                cjo['R'] = ''
            cnode.set('R', str(cjo['R']))
            if 'Rb' not in cjo:
                cjo['Rb'] = ''
            cnode.set('Rb', str(cjo['Rb']))
            if 'HDirect' not in cjo:
                cjo['HDirect'] = ''
            cnode.set('HDirect', str(cjo['HDirect']))
            if 'Face' not in cjo:
                cjo['Face'] = ''
            cnode.set('Face', str(cjo['Face']))
            if 'Hole_Z' not in cjo:
                cjo['Hole_Z'] = ''
            cnode.set('Hole_Z', str(cjo['Hole_Z']))
            cjo = None
        ja = None
    return root
def GetPanelPosInDoor(door, p):
    Result = -1
    b1 = False
    b2 = False
    for i in range(0, len(door['panellist'])):
        pnl = door['panellist'][i]
        if (pnl == p):
            continue
        if (pnl['y1'] > p['y1']):
            b1 = True
        if (pnl['y1'] < p['y1']):
            b2 = True
    if (b1): Result = 1  #// 上格有面板
    if ( b2 ): Result = 2 #// 下格有面板
    if ( (b1) and (b2) ): Result = 0
    return Result
def GetPanelBom(ALLlist, bomclass, mat, color, color2, color3, pnll, pnlh):
    for i in range(0, len(mPanelBomDetailListDoor)):
        p = mPanelBomDetailListDoor[i]
        if ((p['bomclass'] == bomclass) and (float(p['lmin']) < float(pnll)) and (float(p['lmax']) >= float(pnll)) and (
                float(p['hmin']) < float(pnlh)) and (float(p['hmax']) >= float(pnlh))):
            pwl = NewWLData()
            pwl['name'] = p['bomname']
            pwl['bdfile'] = p['bdfile']
            pwl['code'] = ''
            pwl['color'] = p['color'].replace('$门板颜色', color)
            if (pwl['color'].find("门芯颜色") != -1): #// 如果不加上这个那么会出现门板颜色替换时，替换失败。
                pwl['color']= p['color'].replace( '$门芯颜色', color)
            pwl['color'] = pwl['color'].replace('$附加物料颜色', color2)
            pwl['color'] = pwl['color'].replace('$边框颜色', color3)
            pwl['memo']= p['memo']
            pwl['l'] = SAndDoorSetSubject(p['l'], mExp)
            pwl['w'] = SAndDoorSetSubject(p['w'], mExp)
            pwl['h'] = SAndDoorSetSubject(p['h'], mExp)
            pwl['group'] = 2
            pwl['bomtype'] = '型材五金'
            if ((p['bomtype'] == '木板') or (p['bomtype'] == '玻璃') or (p['bomtype'] == '百叶') or (p['bomtype'] == '板材')):
                pwl['bomtype'] = '板材'
            elif (p['bomtype'] != ''):  #{// 非空的时候 就置成配置的数据的
                pwl['bomtype'] = p['bomtype']
            if ( p['bomtype'] == '型材五金'):pwl['group'] = 1
            if ( p['bomtype'] == '五金' ):pwl['group'] = 3
            if ( p['bomtype'] == '玻璃' ):pwl['isglass'] = 1
            pwl['num'] = p['num']
            ALLlist.append(pwl)
def GetSSExp(name):
    Result = {}
    for i in range(0, len(mShutterExpList)):
        if(mShutterExpList[i]['paneltype'] == name):
            Result = mShutterExpList[i]
    return Result
if __name__ == '__main__':
    xml1 = '''<掩门 guid="54CDEED850E7B0AE34E4040BBEAF2731" 门洞宽="2000" 门洞高="2800" L门缝="0" H门缝="0" M门缝="-1.0000" 单门数量类型="四扇门" 门类型="吸塑门" 门颜色="请选择颜色" 均分="0" 左盖="18" 右盖="18" 上盖="18" 下盖="18" ZNMJ="0" CT="0" 门框类型="KXS137" 门框颜色="米白浮雕" 中横框类型="吸逆通用中横" 中横框颜色="米白浮雕" 门芯类型="KXS137" 门芯颜色="米白浮雕" 是否竖排="False" 是否带框="1" DoorMemo="" Extend="" HingeHole="" DataMode="0" Extra="{^path^:^data/Door/product/吸塑/对开^,^productName^:^KXS137^}">
												<分格 面板高度="2728" 高度="2728" 材料="KXS137" 颜色="米白浮雕" 纹路="" 胶条位="" 备注="" 定格="0"/>
												<单门 宽="505.75" 高="2836" DW1="509" DH1="2836" X0="0" Y0="0" X1="0" Y1="0" 门框类型="KXS137" 打开方向="左" 拉手="1-3黑简梯形-竖" 门铰="MD标配铰链@#全盖" 门铰CT="全盖" HandleX="475.75" HandleY="1358" HandleW="10" HandleH="120" HandlePos="{^X^:20,^AL^:1,^Sign^:^^,^AL_Y^:0,^isCenter^:0}" HandlePosX="20" HandlePosY="0" VBOXH="54" UDBOXH="54" T_W="3.25" LKVALUE="0" Memo="" HingeHoleDes="标准铰链孔" HingeHoleParam="{^一^:0,^二^:0,^三^:0,^四^:0,^五^:0}" HingeHoleExtra="" HingeSideXmlpos="">
													<门芯 类型="KXS137" 颜色="米白浮雕" 颜色2="" 纹路="" w0="397.75" h0="2728" x0="54" y0="54" d0="18" w1="397.75" h1="2728" x1="54" y1="54" d1="18" w2="505.75" h2="2836" x2="0" y2="0" d2="18"/>
												</单门>
												<单门 宽="505.75" 高="2836" DW1="509" DH1="2836" X0="508.75" Y0="0" X1="509.00" Y1="0" 门框类型="KXS137" 打开方向="右" 拉手="1-3黑简梯形-竖" 门铰="MD标配铰链@#全盖" 门铰CT="全盖" HandleX="20" HandleY="1358" HandleW="10" HandleH="120" HandlePos="{^X^:20,^AL^:1,^Sign^:^^,^AL_Y^:0,^isCenter^:0}" HandlePosX="20" HandlePosY="0" VBOXH="54" UDBOXH="54" T_W="3.25" LKVALUE="0" Memo="" HingeHoleDes="标准铰链孔" HingeHoleParam="{^一^:0,^二^:0,^三^:0,^四^:0,^五^:0}" HingeHoleExtra="" HingeSideXmlpos="">
													<门芯 类型="KXS137" 颜色="米白浮雕" 颜色2="" 纹路="" w0="397.75" h0="2728" x0="562.75" y0="54" d0="18" w1="397.75" h1="2728" x1="562.75" y1="54" d1="18" w2="505.75" h2="2836" x2="508.75" y2="0" d2="18"/>
												</单门>
												<单门 宽="505.75" 高="2836" DW1="509" DH1="2836" X0="1017.50" Y0="0" X1="1018.00" Y1="0" 门框类型="KXS137" 打开方向="左" 拉手="1-3黑简梯形-竖" 门铰="MD标配铰链@#全盖" 门铰CT="全盖" HandleX="475.75" HandleY="1358" HandleW="10" HandleH="120" HandlePos="{^X^:20,^AL^:1,^Sign^:^^,^AL_Y^:0,^isCenter^:0}" HandlePosX="20" HandlePosY="0" VBOXH="54" UDBOXH="54" T_W="3.25" LKVALUE="0" Memo="" HingeHoleDes="标准铰链孔" HingeHoleParam="{^一^:0,^二^:0,^三^:0,^四^:0,^五^:0}" HingeHoleExtra="" HingeSideXmlpos="">
													<门芯 类型="KXS137" 颜色="米白浮雕" 颜色2="" 纹路="" w0="397.75" h0="2728" x0="1071.5" y0="54" d0="18" w1="397.75" h1="2728" x1="1071.5" y1="54" d1="18" w2="505.75" h2="2836" x2="1017.5" y2="0" d2="18"/>
												</单门>
												<单门 宽="505.75" 高="2836" DW1="509" DH1="2836" X0="1526.25" Y0="0" X1="1527.00" Y1="0" 门框类型="KXS137" 打开方向="右" 拉手="1-3黑简梯形-竖" 门铰="MD标配铰链@#全盖" 门铰CT="全盖" HandleX="20" HandleY="1358" HandleW="10" HandleH="120" HandlePos="{^X^:20,^AL^:1,^Sign^:^^,^AL_Y^:0,^isCenter^:0}" HandlePosX="20" HandlePosY="0" VBOXH="54" UDBOXH="54" T_W="3.25" LKVALUE="0" Memo="" HingeHoleDes="标准铰链孔" HingeHoleParam="{^一^:0,^二^:0,^三^:0,^四^:0,^五^:0}" HingeHoleExtra="" HingeSideXmlpos="">
													<门芯 类型="KXS137" 颜色="米白浮雕" 颜色2="" 纹路="" w0="397.75" h0="2728" x0="1580.25" y0="54" d0="18" w1="397.75" h1="2728" x1="1580.25" y1="54" d1="18" w2="505.75" h2="2836" x2="1526.25" y2="0" d2="18"/>
												</单门>
											</掩门>'''
    xml2 = '''<掩门 guid="C409C31662DBD6346030F1007028CA35" 门洞宽="304" 门洞高="700" L门缝="0.0000" H门缝="0.0000" M门缝="-1.0000" 单门数量类型="单掩门" 门类型="平板门" 门颜色="859B#时尚灰" 均分="0" 左盖="0" 右盖="0" 上盖="0" 下盖="0" ZNMJ="0" CT="0" 门框类型="中纤板(QS-01)" 门框颜色="859B#时尚灰" 中横框类型="无中横" 中横框颜色="70#象牙白" 门芯类型="中纤板(竖纹)" 门芯颜色="70#象牙白" 是否竖排="False" 是否带框="0" DoorMemo="" Extend="" HingeHole="" DataMode="0" Extra="">
    
                                  <分格 面板高度="696" 高度="696" 材料="中纤板(竖纹)" 颜色="70#象牙白" 纹路="竖纹" 胶条位="" 备注="" 定格="0"/>
    
                                  <单门 宽="300" 高="696" DW1="304" DH1="700" X0="0.00" Y0="0" X1="0.00" Y1="0" 门框类型="中纤板(QS-01)" 打开方向="右" 拉手="DZ1602-C160-192" 门铰="东泰铰链@#MJ-D06内置阻尼铰链110大弯" 门铰CT="入柱" HandleX="27" HandleY="440" HandleW="6" HandleH="200" HandlePos="{^X^:27,^AL^:2,^Sign^:^^,^AL_Y^:56,^isCenter^:0}" HandlePosX="30" HandlePosY="0" VBOXH="0.00" UDBOXH="0.00" T_W="4.00" LKVALUE="4.00" Memo="" HingeHoleDes="01-18侧板门铰孔" HingeHoleParam="{^一^:0,^二^:0,^三^:0,^四^:0,^五^:0}" HingeHoleExtra="{^门铰^:[{^门铰类型^:^MJ-D06内置阻尼铰链110大弯^,^偏移值^:^0^},{^门铰类型^:^MJ-D06内置阻尼铰链110大弯^,^偏移值^:^0^}],^门铰孔标注^:^120-456-120^,^开门方向^:^右^}">
    
                                    <门芯 类型="中纤板(竖纹)" 颜色="70#象牙白" 颜色2="" 纹路="竖纹" w0="300" h0="696" x0="0" y0="0" d0="0" w1="300" h1="696" x1="0" y1="0" d1="0" w2="300" h2="696" x2="0" y2="0" d2="0"/>
    
                                  </单门>
    
                                </掩门>'''
    xml3 = '''<掩门 guid="2FFA62B16627AB4B254073BE568A250B" 门洞宽="739" 门洞高="2156" L门缝="0.0000" H门缝="0.0000" M门缝="-1.0000" 单门数量类型="双掩门" 门类型="平板门" 门颜色="859B#时尚灰" 均分="0" 左盖="18" 右盖="18" 上盖="18" 下盖="18" ZNMJ="0" CT="0" 门框类型="中纤板(QS-01)" 门框颜色="859B#时尚灰" 中横框类型="无中横" 中横框颜色="无" 门芯类型="中纤板(竖纹)" 门芯颜色="70#象牙白" 是否竖排="False" 是否带框="0" DoorMemo="" Extend="" HingeHole="" DataMode="0" Extra="{^path^:^QdCloud/Door/product/平开门/QS-01^,^productName^:^QS-01^}">
    
                      <分格 面板高度="2189" 高度="2189" 材料="中纤板(竖纹)" 颜色="70#象牙白" 纹路="竖纹" 胶条位="" 备注="" 定格="0"/>
    
                      <单门 宽="385" 高="2189" DW1="387.5" DH1="2192" X0="0.00" Y0="0" X1="0.00" Y1="0" 门框类型="中纤板(QS-01)" 打开方向="左" 拉手="无拉手" 门铰="东泰铰链@#MJ-D01内置阻尼铰链110直臂" 门铰CT="全盖" HandleX="385" HandleY="0" HandleW="0" HandleH="0" HandlePos="{^X^:0,^AL^:0,^Sign^:^^,^AL_Y^:0,^isCenter^:0}" HandlePosX="0" HandlePosY="0" VBOXH="0.00" UDBOXH="0.00" T_W="2.50" LKVALUE="3.00" Memo="" HingeHoleDes="01-18侧板门铰孔" HingeHoleParam="{^一^:0,^二^:0,^三^:0,^四^:0,^五^:0}" HingeHoleExtra="{^门铰^:[{^门铰类型^:^MJ-D01内置阻尼铰链110直臂^,^偏移值^:^0^},{^门铰类型^:^MJ-D01内置阻尼铰链110直臂^,^偏移值^:^0^},{^门铰类型^:^MJ-D01内置阻尼铰链110直臂^,^偏移值^:^0^},{^门铰类型^:^MJ-D01内置阻尼铰链110直臂^,^偏移值^:^0^},{^门铰类型^:^MJ-D01内置阻尼铰链110直臂^,^偏移值^:^0^}],^门铰孔标注^:^120-487-487-488-487-120^,^开门方向^:^左^}">
    
                        <门芯 类型="中纤板(竖纹)" 颜色="70#象牙白" 颜色2="" 纹路="竖纹" w0="385" h0="2189" x0="0" y0="0" d0="0" w1="385" h1="2189" x1="0" y1="0" d1="0" w2="385" h2="2189" x2="0" y2="0" d2="0"/>
    
                      </单门>
    
                      <单门 宽="385" 高="2189" DW1="387.5" DH1="2192" X0="387.00" Y0="0" X1="387.50" Y1="0" 门框类型="中纤板(QS-01)" 打开方向="右" 拉手="DZ1605T_900(左)" 门铰="东泰铰链@#MJ-D01内置阻尼铰链110直臂" 门铰CT="全盖" HandleX="0" HandleY="0" HandleW="35" HandleH="900" HandlePos="{^X^:0,^AL^:0,^Sign^:^^,^AL_Y^:0,^isCenter^:0}" HandlePosX="0" HandlePosY="0" VBOXH="0.00" UDBOXH="0.00" T_W="2.50" LKVALUE="3.00" Memo="" HingeHoleDes="01-18侧板门铰孔" HingeHoleParam="{^一^:0,^二^:0,^三^:0,^四^:0,^五^:0}" HingeHoleExtra="{^门铰^:[{^门铰类型^:^MJ-D01内置阻尼铰链110直臂^,^偏移值^:^0^},{^门铰类型^:^MJ-D01内置阻尼铰链110直臂^,^偏移值^:^0^},{^门铰类型^:^MJ-D01内置阻尼铰链110直臂^,^偏移值^:^0^},{^门铰类型^:^MJ-D01内置阻尼铰链110直臂^,^偏移值^:^0^},{^门铰类型^:^MJ-D01内置阻尼铰链110直臂^,^偏移值^:^0^}],^门铰孔标注^:^120-487-487-488-487-120^,^开门方向^:^右^}">
    
                        <门芯 类型="中纤板(竖纹)" 颜色="70#象牙白" 颜色2="" 纹路="竖纹" w0="385" h0="2189" x0="387" y0="0" d0="0" w1="385" h1="2189" x1="387" y1="0" d1="0" w2="385" h2="2189" x2="387" y2="0" d2="0"/>
    
                      </单门>
    
                    </掩门>'''
    xml4 = '''<掩门 guid="B673EB83387C825448D88247E1FD4769" 门洞宽="267" 门洞高="367" L门缝="0.0000" H门缝="0.0000" M门缝="-1.0000" 单门数量类型="单掩门" 门类型="平板门" 门颜色="请选择颜色" 均分="0" 左盖="18" 右盖="18" 上盖="18" 下盖="18" ZNMJ="0" CT="0" 门框类型="UV板(QU-01)" 门框颜色="838#闪银亮光" 中横框类型="无中横" 中横框颜色="838#闪银亮光" 门芯类型="UV板(竖纹)" 门芯颜色="838#闪银亮光" 是否竖排="False" 是否带框="0" DoorMemo="" Extend="" HingeHole="" DataMode="0" Extra="{^path^:^QdCloud/Door/product/平开门/QU-01^,^productName^:^QU-01^}">
                  <分格 面板高度="400" 高度="400" 材料="UV板(竖纹)" 颜色="838#闪银亮光" 纹路="竖纹" 胶条位="" 备注="" 定格="0"/>
                  <单门 宽="300" 高="400" DW1="303" DH1="403" X0="0.00" Y0="0" X1="0.00" Y1="0" 门框类型="UV板(QU-01)" 打开方向="左" 拉手="无拉手" 门铰="无门铰@#无" 门铰CT="其他" HandleX="300" HandleY="200" HandleW="0" HandleH="0" HandlePos="{^X^:0,^AL^:1,^Sign^:^^,^AL_Y^:0,^isCenter^:0}" HandlePosX="30" HandlePosY="0" VBOXH="0.00" UDBOXH="0.00" T_W="3.00" LKVALUE="3.00" Memo="" HingeHoleDes="" HingeHoleParam="{}" HingeHoleExtra="{^门铰^:[],^门铰孔标注^:^65-270-65^,^开门方向^:^左^}">
                    <门芯 类型="UV板(竖纹)" 颜色="838#闪银亮光" 颜色2="" 纹路="竖纹" w0="300" h0="400" x0="0" y0="0" d0="0" w1="300" h1="400" x1="0" y1="0" d1="0" w2="300" h2="400" x2="0" y2="0" d2="0"/>
                  </单门>
                </掩门>'''
    xml5 = '''<掩门 guid="1273035782525655962CCC11A58FA57A" 门洞宽="867" 门洞高="590" L门缝="0.0000" H门缝="0.0000" M门缝="-1.0000" 单门数量类型="双掩门" 门类型="包覆门" 门颜色="请选择颜色" 均分="0" 左盖="18" 右盖="0" 上盖="18" 下盖="18" ZNMJ="0" CT="0" 门框类型="QB-05" 门框颜色="952B#黄橡做旧" 中横框类型="无中横" 中横框颜色="952B#黄橡做旧" 门芯类型="QB-05A凹凸芯板" 门芯颜色="952B#黄橡做旧" 是否竖排="False" 是否带框="1" DoorMemo="1+QB-05+QB-05A凹凸芯板+952B#黄橡做旧+无中横+左+LS-035(横)+海蒂诗铰链@#MJ-H01内置阻尼铰链95直臂+120+383+120;2+QB-05+QB-05A凹凸芯板+952B#黄橡做旧+无中横+右+LS-035(横)+海蒂诗铰链@#MJ-H06内置阻尼铰链95大弯+120+383+120;" Extend="" HingeHole="" DataMode="0" Extra="{^path^:^QdCloud/Door/product/平开门/QB-05^,^productName^:^QB-05单格^}">
                  <分格 面板高度="623" 高度="623" 材料="QB-05A凹凸芯板" 颜色="952B#黄橡做旧" 纹路="竖纹" 胶条位="" 备注="" 定格="0"/>
                  <单门 宽="440" 高="623" DW1="442.5" DH1="626" X0="0.00" Y0="0" X1="0.00" Y1="0" 门框类型="QB-05" 打开方向="左" 拉手="LS-035(横)" 门铰="海蒂诗铰链@#MJ-H01内置阻尼铰链95直臂" 门铰CT="全盖" HandleX="149" HandleY="15" HandleW="142" HandleH="20" HandlePos="{^X^:149,^AL^:0,^Sign^:^^,^AL_Y^:15,^isCenter^:1}" HandlePosX="25" HandlePosY="0" VBOXH="0.00" UDBOXH="0.00" T_W="2.50" LKVALUE="3.00" Memo="" HingeHoleDes="01-18侧板门铰孔" HingeHoleParam="{^一^:0,^二^:0,^三^:0,^四^:0,^五^:0}" HingeHoleExtra="{^门铰^:[{^门铰类型^:^MJ-H01内置阻尼铰链95直臂^,^偏移值^:0},{^门铰类型^:^MJ-H01内置阻尼铰链95直臂^,^偏移值^:0}],^开门方向^:^左^,^门铰孔标注^:^120-383-120^}">
                    <门芯 类型="QB-05A凹凸芯板" 颜色="952B#黄橡做旧" 颜色2="" 纹路="竖纹" w0="440" h0="623" x0="0" y0="0" d0="0" w1="440" h1="623" x1="0" y1="0" d1="0" w2="440" h2="623" x2="0" y2="0" d2="0"/>
                  </单门>
                  <单门 宽="440" 高="623" DW1="442.5" DH1="626" X0="442.00" Y0="0" X1="442.50" Y1="0" 门框类型="QB-05" 打开方向="右" 拉手="LS-035(横)" 门铰="海蒂诗铰链@#MJ-H06内置阻尼铰链95大弯" 门铰CT="入柱" HandleX="149" HandleY="15" HandleW="142" HandleH="20" HandlePos="{^X^:149,^AL^:0,^Sign^:^^,^AL_Y^:15,^isCenter^:1}" HandlePosX="25" HandlePosY="0" VBOXH="0.00" UDBOXH="0.00" T_W="2.50" LKVALUE="3.00" Memo="" HingeHoleDes="01-18侧板门铰孔" HingeHoleParam="{^一^:0,^二^:0,^三^:0,^四^:0,^五^:0}" HingeHoleExtra="{^门铰^:[{^门铰类型^:^MJ-H06内置阻尼铰链95大弯^,^偏移值^:0},{^门铰类型^:^MJ-H06内置阻尼铰链95大弯^,^偏移值^:0}],^开门方向^:^右^,^门铰孔标注^:^120-383-120^}">
                    <门芯 类型="QB-05A凹凸芯板" 颜色="952B#黄橡做旧" 颜色2="" 纹路="竖纹" w0="440" h0="623" x0="442" y0="0" d0="0" w1="440" h1="623" x1="442" y1="0" d1="0" w2="440" h2="623" x2="442" y2="0" d2="0"/>
                  </单门>
                </掩门>'''
    l = 867
    h = 590
    RootPath = base_dir
    logging.basicConfig(level="DEBUG")
    log = logging.getLogger(__name__)
    log.setLevel('DEBUG')
    jo = XmlTemplate2Json(xml5,l,h)
    deslist = []
    for obj in jo['物料']:
        if obj['Name'] not in deslist:
            deslist.append(obj['Name'])
    log.debug('len of deslist='+str(len(deslist)))