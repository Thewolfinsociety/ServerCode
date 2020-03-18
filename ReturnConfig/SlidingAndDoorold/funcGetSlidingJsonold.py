#  -*- coding:utf-8 -*-
'''
vesion 1.0.1
2019/7/10
author:litao
'''

import json
import os, sys
import xml.etree.ElementTree as ET
import ConfigParser
import copy
from ctypes import *
import copy
reload(sys)
sys.setdefaultencoding('utf-8')   #使用其他编码时，utf-8为默认解码方式
def copyini(IniPath):
    copyinifile = os.path.dirname(IniPath) + '\\copy.ini'
    with open(copyinifile, 'w+') as f:
        with open(IniPath, 'r') as f1:
            content = f1.read()
            content = content.replace('//', '#')
        f.write(content)
    cf = ConfigParser.ConfigParser()

    cf.read(copyinifile)
    return cf
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

def SlidingInitData():
    global mSlidingExpList,mSlidingTypeList,mSlidingParamList,mUDBoxParamList,mTrackParamList, \
        mHBoxParamList,mVBoxParamList,mPanelBomDetailList,mSSExpList, \
        UHBoxParam, HHBoxParam, SlidingParam, mSlidingAccessoryList, \
        mSlidingWjBomDetailList, mSlidingColorClassList, mSlidingColorList, \
        HBoxParamcfglist,cfglist,PanelTypeList,Cfgobj2,Cfgobj3,Cfgobj4,\
        SHBoxParam,HCfgobj2,HCfgobj3,HCfgobj4,HSHBoxParam
    # cf = ConfigParser.ConfigParser()
    #
    # cf.read(base_dir + '\\qd.conf')
    cf = copyini(base_dir + '\\qd.conf')
    try:
        mNoFZTPriceFlag = cf.get(u"QuickDraw".encode('gb2312'), u"NoFZTPriceFlag".encode('gb2312'))
    except:
        mNoFZTPriceFlag = 1
    try:
        mNoCDWPriceFlag = cf.get(u"QuickDraw".encode('gb2312'), u"NoCDWPriceFlag".encode('gb2312'))
    except:
        mNoCDWPriceFlag = 0
    try:
        mBomPriceFlag = cf.get(u"QuickDraw".encode('gb2312'), u"BomPriceFlag".encode('gb2312'))
    except:
        mBomPriceFlag = 0
    #print 'mNoFZTPriceFlag=',mNoFZTPriceFlag,'mNoCDWPriceFlag=',mNoCDWPriceFlag,'mBomPriceFlag=',mBomPriceFlag
    cf1 = copyini(base_dir + '\\QdCloud\\Sliding.ini')

    try:
        doorApart = cf1.get(u"isDoorApart", u"doorApart").encode('utf8')
    except:
        doorApart = 0
    try:
        isRoundWidth =cf1.get(u"isRoundWidth", u"isRound").encode('utf8')
    except:
        isRoundWidth = 0
    try:
        isSumDim = cf1.get(u"isSumDim", u"isSum").encode('utf8')
    except:
        isSumDim =0
    try:
        markIniStr=cf1.get(u"ShowMarks", u"name").encode('utf8')
    except:
        markIniStr = 0
    try:
        doorInfoConfigStr=cf1.get(u"doorInfoConfig", u"doorInfo").encode('utf8')
    except:
        doorInfoConfigStr = 0

    #print mNoFZTPriceFlag,mNoCDWPriceFlag,mBomPriceFlag,doorApart,isRoundWidth,markIniStr,doorInfoConfigStr
    #-------------------cfg
    try:
        print base_dir
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\单门数量类型.cfg'.encode('gb2312'),'r') as f:
            mSlidingExpListcontent=f.read()
        if mSlidingExpListcontent=='':
            mSlidingExpListcontent = json.dumps([])
    except:
        mSlidingExpListcontent = json.dumps([])
    #print 'mSlidingExpListcontent=',mSlidingExpListcontent
    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\门类型.cfg'.encode('gb2312'),'r') as f:
            mSlidingTypeListcontent=f.read()
        if mSlidingTypeListcontent == '':
            mSlidingTypeListcontent = json.dumps([])
    except:
        mSlidingTypeListcontent = json.dumps([])
    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\趟门参数.cfg'.encode('gb2312'),'r') as f:
            SlidingParamcontent=f.read()
        if SlidingParamcontent=='':
            SlidingParamcontent = json.dumps([])
    except:
        SlidingParamcontent = json.dumps([])
    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\上下横框参数.cfg'.encode('gb2312'),'r') as f:
            UDBoxParamcontent=f.read()
        if UDBoxParamcontent == '':
            UDBoxParamcontent = json.dumps([])
    except:
        UDBoxParamcontent = json.dumps([])
    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\上下轨参数.cfg'.encode('gb2312'),'r') as f:
            TrackParamcontent=f.read()
        if TrackParamcontent =='':
            TrackParamcontent = json.dumps([])
    except:
        TrackParamcontent = json.dumps([])

    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\中横框参数.cfg'.encode('gb2312'),'r') as f:
            HBoxParamcontent=f.read()
        if HBoxParamcontent=='':
            HBoxParamcontent = json.dumps([])
    except:
        HBoxParamcontent = json.dumps([])
    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\门板类型.cfg'.encode('gb2312'),'r') as f:
            PanelTypeListcontent=f.read()
        if PanelTypeListcontent=='':
            PanelTypeListcontent = json.dumps([])
    except:
        PanelTypeListcontent = json.dumps([])
    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\报价.cfg'.encode('gb2312'),'r') as f:
            mSlidingPriceListcontent=f.read()
        if mSlidingPriceListcontent == '':
            mSlidingPriceListcontent = json.dumps([])
    except:
        mSlidingPriceListcontent = json.dumps([])
    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\报价方案.cfg'.encode('gb2312'),'r') as f:
            mPriceTableListcontent=f.read()
        if mPriceTableListcontent =='':
            mPriceTableListcontent = json.dumps([])
    except:
        mPriceTableListcontent = json.dumps([])
    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\颜色分类2.cfg'.encode('gb2312'),'r') as f:
            mSlidingColorListcontent=f.read()
        if mSlidingColorListcontent =='':
            mSlidingColorListcontent =json.dumps([])
    except:
        mSlidingColorListcontent = json.dumps([])
    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\颜色分类.cfg'.encode('gb2312'),'r') as f:
            mSlidingColorClassListcontent=f.read()
        if mSlidingColorClassListcontent == '':
            mSlidingColorClassListcontent = json.dumps([])
    except:
        mSlidingColorClassListcontent = json.dumps([])
    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\五金配件分类数据.cfg'.encode('gb2312'),'r') as f:
            mSlidingWjBomDetailListcontent=f.read()
        if mSlidingWjBomDetailListcontent == '':
            mSlidingWjBomDetailListcontent = json.dumps([])
    except:
        mSlidingWjBomDetailListcontent = json.dumps([])
    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\百叶板计算公式.cfg'.encode('gb2312'),'r') as f:
            mSSExpListcontent=f.read()
        if mSSExpListcontent=='':
            mSSExpListcontent = json.dumps([])
    except:
        mSSExpListcontent = json.dumps([])
    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\五金配件.cfg'.encode('gb2312'),'r') as f:
            mSlidingAccessoryListcontent=f.read()
        if mSlidingAccessoryListcontent == '':
            mSlidingAccessoryListcontent = json.dumps([])
    except:
        mSlidingAccessoryListcontent = json.dumps([])

    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\竖框参数.cfg'.encode('gb2312'),'r') as f:
            mVBoxParamListcontent=f.read()
        if mVBoxParamListcontent=='':
            mVBoxParamListcontent = json.dumps([])
    except:
        mVBoxParamListcontent = json.dumps([])
    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\门板附加物料.cfg'.encode('gb2312'),'r') as f:
            mPanelBomDetailListcontent=f.read()
        if mPanelBomDetailListcontent == '':
            mPanelBomDetailListcontent = json.dumps([])
    except:
        mPanelBomDetailListcontent = json.dumps([])
    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\竖中横框参数.cfg'.encode('gb2312'),'r') as f:
            UHBoxParamcontent=f.read()
        if UHBoxParamcontent == '':
            UHBoxParamcontent = json.dumps([])
    except:
        UHBoxParamcontent = json.dumps([])
    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\横中横框参数.cfg'.encode('gb2312'),'r') as f:
            HHBoxParamcontent=f.read()
        if HHBoxParamcontent=='':
            HHBoxParamcontent = json.dumps([])
    except:
        HHBoxParamcontent = json.dumps([])

    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\趟门2竖分格.cfg'.encode('gb2312'),'r') as f:
            Cfgobj2content=f.read()
        if Cfgobj2content=='':
            Cfgobj2content = json.dumps([])


    except:
        Cfgobj2content = json.dumps([])

    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\趟门3竖分格.cfg'.encode('gb2312'),'r') as f:
            Cfgobj3content=f.read()
        if Cfgobj3content=='':
            Cfgobj3content = json.dumps([])
    except:
        Cfgobj3content = json.dumps([])

    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\趟门4竖分格.cfg'.encode('gb2312'),'r') as f:
            Cfgobj4content=f.read()
        if Cfgobj4content=='':
            Cfgobj4content = json.dumps([])
    except:
        Cfgobj4content = json.dumps([])

    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\竖中横框参数.cfg'.encode('gb2312'),'r') as f:
            SHBoxParamcontent=f.read()
        if SHBoxParamcontent=='':
            SHBoxParamcontent = json.dumps([])
    except:
        SHBoxParamcontent = json.dumps([])

    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\趟门2横分格.cfg'.encode('gb2312'),'r') as f:
            HCfgobj2content=f.read()
        if HCfgobj2content=='':
            HCfgobj2content = json.dumps([])
    except:
        HCfgobj2content = json.dumps([])

    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\趟门3横分格.cfg'.encode('gb2312'),'r') as f:
            HCfgobj3content=f.read()
        if HCfgobj3content=='':
            HCfgobj3content = json.dumps([])
    except:
        HCfgobj3content = json.dumps([])

    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\趟门4横分格.cfg'.encode('gb2312'),'r') as f:
            HCfgobj4content=f.read()
        if HCfgobj4content=='':
            HCfgobj4content = json.dumps([])
    except:
        HCfgobj4content = json.dumps([])

    try:
        with open(base_dir + u'\\QdCloud\\Sliding\\趟门配置表\\横中横框参数.cfg'.encode('gb2312'),'r') as f:
            HSHBoxParamcontent=f.read()
        if HSHBoxParamcontent=='':
            HSHBoxParamcontent = json.dumps([])
    except:
        HSHBoxParamcontent = json.dumps([])

    try:
        with open(base_dir + u'\\data\\QdData\\门转换表.cfg'.encode('gb2312'),'r') as f:
            cfglistcontent=f.read()
        if cfglistcontent=='':
            cfglistcontent = json.dumps([])
    except:
        cfglistcontent = json.dumps([])

    mSlidingExpList = json.loads(mSlidingExpListcontent,encoding='gbk')
    mSlidingTypeList = json.loads(mSlidingTypeListcontent,encoding='gbk')
    mSlidingParamList = json.loads(SlidingParamcontent,encoding='gbk')
    mUDBoxParamList = json.loads(UDBoxParamcontent,encoding='gbk')
    mTrackParamList = json.loads(TrackParamcontent,encoding='gbk')
    mHBoxParamList = json.loads(HBoxParamcontent,encoding='gbk')
    PanelTypeList = json.loads(PanelTypeListcontent,encoding='gbk')
    mSlidingPriceList = json.loads(mSlidingPriceListcontent,encoding='gbk')
    mPriceTableList = json.loads(mPriceTableListcontent,encoding='gbk')
    mSlidingColorList = json.loads(mSlidingColorListcontent,encoding='gbk')
    mSlidingColorClassList = json.loads(mSlidingColorClassListcontent,encoding='gbk')
    mSlidingWjBomDetailList = json.loads(mSlidingWjBomDetailListcontent,encoding='gbk')

    mSSExpList = json.loads(mSSExpListcontent,encoding='gbk')
    mSlidingAccessoryList = json.loads(mSlidingAccessoryListcontent,encoding='gbk')
    mVBoxParamList = json.loads(mVBoxParamListcontent,encoding='gbk')
    mPanelBomDetailList = json.loads(mPanelBomDetailListcontent,encoding='gbk')
    UHBoxParam = json.loads(UHBoxParamcontent,encoding='gbk')
    HHBoxParam = json.loads(HHBoxParamcontent,encoding='gbk')
    Cfgobj2 = json.loads(Cfgobj2content,encoding='gbk')
    Cfgobj3 = json.loads(Cfgobj3content, encoding='gbk')
    Cfgobj4 = json.loads(Cfgobj4content, encoding='gbk')
    SHBoxParam = json.loads(SHBoxParamcontent, encoding='gbk')
    HCfgobj2 = json.loads(HCfgobj2content, encoding='gbk')
    HCfgobj3 = json.loads(HCfgobj3content, encoding='gbk')
    HCfgobj4 = json.loads(HCfgobj4content, encoding='gbk')
    HSHBoxParam = json.loads(HSHBoxParamcontent, encoding='gbk')
    cfglist = json.loads(cfglistcontent, encoding='gbk')
    sSort(Cfgobj2)
    sSort(Cfgobj3)
    sSort(Cfgobj4)
    sSort(HCfgobj2)
    sSort(HCfgobj3)
    sSort(HCfgobj4)
    for i in range(0,len(mSlidingExpList)):

        mSlidingExpList[i]['doornum'] = Number(mSlidingExpList[i]['doornum'])
        mSlidingExpList[i]['overlapnum'] = Number(mSlidingExpList[i]['overlapnum'])
        mSlidingExpList[i]['lkvalue'] = Number(mSlidingExpList[i]['lkvalue'])
        # if 'overlap' not in mSlidingExpList[i]:
        #     mSlidingExpList[i]['overlap'] = 0
        # else:
        #     mSlidingExpList[i]['overlap'] = Number(mSlidingExpList[i]['overlap'] if mSlidingExpList[i]['overlap'] else 0)
        mSlidingExpList[i]['noexp'] = GetTrueFalse(mSlidingExpList[i]['noexp'])# // mSlidingExpList[i].noexp == 'TRUE'? true:false;
    for i in range(0, len(mSSExpList)):

        mSSExpList[i]['height'] = mSSExpList[i]['height']
        mSSExpList[i]['width'] = mSSExpList[i]['width']
        mSSExpList[i]['heightcap'] = mSSExpList[i]['heightcap']
        mSSExpList[i]['widthcap'] = mSSExpList[i]['widthcap']
        mSSExpList[i]['minheight'] = mSSExpList[i]['minheight']
        mSSExpList[i]['minwidth'] = mSSExpList[i]['minwidth']
        mSSExpList[i]['size'] = mSSExpList[i]['size']

    for i in range(0, len(mSlidingParamList)):
        mSlidingParamList[i]["ddlw"] = Number(mSlidingParamList[i]['ddlpos'])
        mSlidingParamList[i]["fztlen"] = Number(mSlidingParamList[i]['fztkd'])
        mSlidingParamList[i]["myclass"] = mSlidingParamList[i]['doortype']

        mSlidingParamList[i]['cpm_lmax'] = Number(mSlidingParamList[i]['cpm_lmax'])
        mSlidingParamList[i]['cpm_hmax'] = Number(mSlidingParamList[i]['cpm_hmax'])
        mSlidingParamList[i]['is_xq'] = GetTrueFalse(mSlidingParamList[i]['is_xq'])
        mSlidingParamList[i]['hboxvalue'] = Number(mSlidingParamList[i]['hboxvalue'])
        mSlidingParamList[i]['laminating'] = GetTrueFalse(mSlidingParamList[i]['laminating'])

    for i in range(0, len(mSlidingAccessoryList)):

        mSlidingAccessoryList[i]['isglass'] = GetTrueFalse(mSlidingAccessoryList[i]['isglass'])
        mSlidingAccessoryList[i]['isbaiye'] = GetTrueFalse(mSlidingAccessoryList[i]['isbaiye'])
        mSlidingAccessoryList[i]['isuserselect'] = GetTrueFalse(mSlidingAccessoryList[i]['isuserselect'])

    for i in range(0,len(mUDBoxParamList)):
        mUDBoxParamList[i]["ubheight"] = Number(mUDBoxParamList[i]['upboxheight'])
        mUDBoxParamList[i]["ubdepth"] = Number(mUDBoxParamList[i]['upboxdepth'])
        mUDBoxParamList[i]["ubthick"] = Number(mUDBoxParamList[i]['upboxthick'])
        mUDBoxParamList[i]["dbheight"] = Number(mUDBoxParamList[i]['downboxheight'])
        mUDBoxParamList[i]["dbdepth"] = Number(mUDBoxParamList[i]['downboxdepth'])
        mUDBoxParamList[i]["dbthick"] = Number(mUDBoxParamList[i]['downboxthick'])
        mUDBoxParamList[i]["uphole"] = Number(mUDBoxParamList[i]['upholepos'])
        mUDBoxParamList[i]["downhole"] = Number(mUDBoxParamList[i]['downholepos'])
        mUDBoxParamList[i]["upsize"] = Number(mUDBoxParamList[i]['upsize'])

    for i in range(0, len(mHBoxParamList)):
        mHBoxParamList[i]["hole"] = Number(mHBoxParamList[i]['holepos'])
        mHBoxParamList[i]["ishboxvalue"] = Number(mHBoxParamList[i]['ishboxvalue'])
    for i in range(0, len(UHBoxParam)):
        UHBoxParam[i]["ishboxvalue"] = Number(UHBoxParam[i]['ishboxvalue'])
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

    for i in range(0, len(PanelTypeList)):

        PanelTypeList[i]["name"] = PanelTypeList[i]['name']

        PanelTypeList[i]["jtvalue"] = Number( PanelTypeList[i]['jtValue'] if "jtvalue" not in PanelTypeList[i] else PanelTypeList[i]['jtvalue'])

        PanelTypeList[i]["jtValue"] = PanelTypeList[i]["jtvalue"]
        PanelTypeList[i]["wjname"] = PanelTypeList[i]['wjname']
        PanelTypeList[i]["isglass"] = GetTrueFalse(PanelTypeList[i]['isglass'])
        PanelTypeList[i]["isbaiye"] = GetTrueFalse(PanelTypeList[i]['isbaiye'])
        PanelTypeList[i]["iswhole"] = GetTrueFalse(PanelTypeList[i]['iswHole'] if "iswhole" not in PanelTypeList[i] else PanelTypeList[i]['iswhole'])
        PanelTypeList[i]["iswHole"] = PanelTypeList[i]["iswhole"]
        PanelTypeList[i]["bktype"] = PanelTypeList[i]['bktype']
        PanelTypeList[i]["direct"] = PanelTypeList[i]['direct']
        PanelTypeList[i]["lmax"] = Number(PanelTypeList[i]['lmax'])
        PanelTypeList[i]["lmin"] = Number(PanelTypeList[i]['lmin'])
        PanelTypeList[i]["wmax"] = Number(PanelTypeList[i]['wmax'])
        PanelTypeList[i]["wmin"] = Number(PanelTypeList[i]['wmin'])

        PanelTypeList[i]["pnl2d"] = PanelTypeList[i]['panel2d']
        PanelTypeList[i]["slave"] = PanelTypeList[i]['slaVe'] if 'slave' not in PanelTypeList[i] else PanelTypeList[i]['slave']
        PanelTypeList[i]["slaVe"] = PanelTypeList[i]["slave"]
        PanelTypeList[i]["slave2"] = PanelTypeList[i]['slaVe2'] if 'slave2' not in PanelTypeList[i] else PanelTypeList[i]['slave2']
        PanelTypeList[i]["slaVe2"] = PanelTypeList[i]["slave2"]
        PanelTypeList[i]["mk3d"] = PanelTypeList[i]['mk3d']
        PanelTypeList[i]["mkl"] = Number(PanelTypeList[i]['mkl'])
        PanelTypeList[i]["mkh"] = Number(PanelTypeList[i]['mkH'] if 'mkh' not in PanelTypeList[i] else PanelTypeList[i]['mkh'])
        PanelTypeList[i]["mkH"] = PanelTypeList[i]["mkh"]
        PanelTypeList[i]['thick'] = Number(PanelTypeList[i]['tHick'] if 'thick' not in PanelTypeList[i] else PanelTypeList[i]['thick'])

        PanelTypeList[i]["tHick"] = PanelTypeList[i]["thick"]
        PanelTypeList[i]["memo"] = PanelTypeList[i]["memo"]
        PanelTypeList[i]["memo2"] = PanelTypeList[i]["memo2"]
        PanelTypeList[i]["memo3"] = PanelTypeList[i]["memo3"]
        PanelTypeList[i]["bdfile"] = PanelTypeList[i]["bdfile"]

    return mSlidingWjBomDetailList,Cfgobj2, Cfgobj3, Cfgobj4, HCfgobj2, HCfgobj3, HCfgobj4, SHBoxParam, HSHBoxParam, cfglist
    # obj = {
    #     'cfg':{
    #         "mSlidingExpList" : mSlidingExpList,
    #         "mSlidingTypeList" :mSlidingTypeList,
    #         "SlidingParam" : SlidingParam,
    #         "UDBoxParam" : UDBoxParam,
    #         "TrackParam" : TrackParam,
    #         "HBoxParam" : HBoxParam,
    #         "PanelTypeList" : PanelTypeList,
    #         "mSlidingPriceList" : mSlidingPriceList,
    #         "mPriceTableList" : mPriceTableList,
    #         "mSlidingColorList" : mSlidingColorList,
    #         "mSlidingColorClassList" : mSlidingColorClassList,
    #         "mSlidingTypeListList" : mSlidingExpList,
    #         "mSlidingWjBomDetailList" : mSlidingWjBomDetailList,
    #         "mSSExpList" : mSSExpList,
    #         "mSlidingAccessoryList" : mSlidingAccessoryList,
    #         "mVBoxParamList" : mVBoxParamList ,
    #         "mPanelBomDetailList" : mPanelBomDetailList ,
    #         "UHBoxParam" : UHBoxParam,
    #         "HHBoxParam" : HHBoxParam,
    #         "Cfgobj2" : Cfgobj2,
    #         "Cfgobj3" : Cfgobj3,
    #         "Cfgobj4" : Cfgobj4,
    #         "SHBoxParam" : SHBoxParam,
    #         "HCfgobj2" : HCfgobj2,
    #         "HCfgobj3" : HCfgobj3,
    #         "HCfgobj4" : HCfgobj4,
    #         "HSHBoxParam" : HSHBoxParam,
    #         "cfglist": cfglist
    #     },
    #     'Cini':{
    #         'mNoFZTPriceFlag':mNoFZTPriceFlag,
    #         'mNoCDWPriceFlag':mNoCDWPriceFlag,
    #         'mBomPriceFlag':mBomPriceFlag,
    #     },
    #     'Sini':{
    #         'doorApart':doorApart,
    #         'isRoundWidth':isRoundWidth,
    #         'isSumDim':isSumDim,
    #         'markIniStr':markIniStr,
    #         'doorInfoConfigStr':doorInfoConfigStr,
    #     },
    #     # 'Db':{
    #     #     'TMlimit':TMlimit
    #     #}
    # }
    #return obj



def fun(xml,W,H):


    # obj = InitData()
    s = XmlTemplate2Json(xml, W, H)

    return s
#解析xml数据
def GetParam(listtype,name):
    Result = {}
    for i in range(0,len(listtype)):
        if (listtype[i]['name'] == name):
            Result = listtype[i]
    return Result

def GetSlidingExp(name):
    Result = {}
    for i in range(0, len(mSlidingExpList)):
        if (mSlidingExpList[i]['name'] == name):
            Result = mSlidingExpList[i]
    return Result

def GetSlidingType(name):
    Result = {}
    for i in range(0, len(mSlidingTypeList)):
        if (mSlidingTypeList[i]['name'] == name):
            Result = mSlidingTypeList[i]
    return Result

def GetSlidingParam(name):
    Result = {}
    for i in range(0, len(mSlidingParamList)):
        if (mSlidingParamList[i]['name'] == name):
            Result = mSlidingParamList[i]
    return Result

def GetTrackParam(name):
    Result = {}
    for i in range(0, len(mTrackParamList)):
        if (mTrackParamList[i]['name'] == name):
            Result = mTrackParamList[i]
    return Result

def GetUDBoxParam(name):
    Result = {}
    for i in range(0, len(mUDBoxParamList)):
        if (mUDBoxParamList[i]['name'] == name):
            Result = mUDBoxParamList[i]
    return Result

def GetVBoxParam(name):
    Result = {}
    for i in range(0, len(mVBoxParamList)):
        if (mVBoxParamList[i]['name'] == name):
            Result = mVBoxParamList[i]
    return Result

def GetSlidingHBoxParam(name):
    Result = {}
    for i in range(0, len(mHBoxParamList)):
        if (mHBoxParamList[i]['name'] == name):
            Result = mHBoxParamList[i]
    return Result

def LoadXMLTemplate(xml, l, h):
    global mDataMode,mSlidingExp,mSlidingParam,mSlidingType,mTrackParam,mUDBoxParam,mHBoxParam,mVBoxParam

    PriceModulePath = base_dir+'\\QdUpTemplate.dll'.encode('gbk')
    PriceModule = windll.LoadLibrary(PriceModulePath)
    p = create_string_buffer(102400)
    p.value = xml.decode('utf8').encode('gbk')
    state = PriceModule.UpSlidingTemplate(p, c_int(l), c_int(h))

    if state==-1:
        return ''

    xmltemplate = p.value.decode('gbk').encode('utf8')
    if (xmltemplate == ''): return ''
    mDataMode = 0
    root = ET.fromstring(xmltemplate)
    mL = l
    mH = h
    mL = int(float(root.get(u'门洞宽',mL)))
    mH = int(float(root.get(u'门洞高', mH)))
    mAddLength = int(float(root.get(u'延长导轨', 0)))
    SlidingInitData()
    attri = root.get(u'单门数量类型', '')
    pexp = GetParam(mSlidingExpList,attri)
    attri = root.get(u'门类型', '')
    pstype = GetParam(mSlidingTypeList, attri)

    attri = root.get(u'边框类型', '')
    psp = GetSlidingParam(mSlidingParamList, attri)  #趟门参数.cfg'
    attri = root.get(u'上下横框类型', '')

    pudbox = GetParam(mUDBoxParamList, attri)

    attri = root.get(u'上下轨类型', '')
    ptrack = GetParam(mTrackParamList, attri)
    attri = root.get(u'中横框类型', '')
    phbox = GetParam(mHBoxParamList, attri)
    if psp != {}:
        pvbox = GetParam(mVBoxParamList, psp['vboxtype'])

    mMyPanelType = root.get(u'门板类型', '')
    mMySlidingColor = root.get(u'门颜色', '')
    mMyVBoxColor = root.get(u'竖框颜色', '')
    mMyUpBoxColor = root.get(u'上横框颜色', '')
    mMyDownBoxColor = root.get(u'下横框颜色', '')
    mMyUpTrackColor = root.get(u'上轨颜色', '')
    mMyDownTrackColor = root.get(u'下轨颜色', '')
    mMyHBoxColor = root.get(u'中横框颜色', '')
    mMyPanelColor = root.get(u'门板颜色', '')
    mDataMode = float(root.get(u'DataMode', '0'))
    Sliding = {'RGDataMode' : {"ItemIndex":0}}
    Sliding['RGDataMode']['ItemIndex'] = mDataMode
    mExtra = root.get(u'Extra', '')
    mGridItem = root.get(u'均分', 0)
    if((pexp == {}) or (pstype == {}) or (psp == {}) or (pudbox == {}) \
            or (ptrack == {}) or (phbox == {}) or (pvbox == None)):
        mCopyDoor = -1
        return ''
    if (pexp): mSlidingExp= pexp
    if (psp):mSlidingParam= psp
    if (pstype): mSlidingType= pstype
    if (ptrack): mTrackParam= ptrack
    if (pudbox): mUDBoxParam= pudbox
    if (phbox): mHBoxParam= phbox
    if (pvbox): mVBoxParam= pvbox
    return xmltemplate


def XmlTemplate2Json(Templatexml, l, h):
    global nHasMzhb,mSlidingParam
    def ReadXML(Templatexml):
        global mExtra,mDataMode,mGridItem
        root = ET.fromstring(Templatexml)
        mDataMode = root.get('mDataMode',0)
        mExtra = root.get('Extra','')
        mGridItem = float(root.get(u'均分', 0))
        jsonobj = []
        Node = {}

        arr = root.attrib
        Node[root.tag] = arr
        Xml2Json(root, Node[root.tag])
        return Node
    cfglist = []
    xml = ''
    mXMLTemplate = Templatexml
    nHasMzhb = False
    mSlidingParam = {'name': ''}
    if os.path.exists(base_dir.decode('gbk') + u'\\data\\QdData\\门转换表.cfg'):
        with open(base_dir.decode('gbk') + u'\\data\\QdData\\门转换表.cfg') as f:
             string = f.read()
        if (not string):string = '[]';
        cfglist = eval("(" + string + ")")
        nHasMzhb =True

    Templatexml = LoadXMLTemplate(Templatexml, l, h)
    if Templatexml == '': return {}
    Result = 0
    mIsSetDoors = True
    if (not mIsSetDoors): return {}

    doorw = l
    doorh = h

    MBData = ReadXML(Templatexml)

    mDoorsList = MBData[u'趟门'][u'单门']
    if (len(mDoorsList) > 0):
        door = mDoorsList[0]
        doorw = door[u'宽']
        doorh = door[u'高']


    jo = {}
    jo[u'门框类型'] = mSlidingParam['name']
    jo[u'门洞宽'] = l
    jo[u'门洞高'] = h
    jo[u'成品门宽'] = doorw
    jo[u'成品门高'] = doorh
    jo[u'扇数'] = len(mDoorsList)
    jo[u'DoorExtra'] = mExtra
    jo[u'DoorType'] = 1
    ja = []
    jo[u'报价'] = ja
    jo[u'物料'] = GetXMLBom(Templatexml)

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
    def GetPanelPosInDoor(mDoorsobject,i):
        pos = -1
        if len(MBData[u'分格']) == 1:
            return pos
        elif (len(MBData[u'分格'])== 2):

            if (i == 0):pos = 1
            if (i == 1): pos = 2
        else:
            if (i == 0): pos = 1
            elif (i != (len(MBData[u'分格']) - 1)) :pos = 0
            else:
                pos = 2
            return pos
        return pos
    mDoorsobject = mDoorsList[i]
    doo= {"doorw":0,"doorh":0}
    doo['doorw'] = float(mDoorsobject[u'宽'])
    doo['doorh'] = float(mDoorsobject[u'高'])
    doo["mVBoxColor"] = mDoorsobject[u'竖框颜色']
    doo["mVBoxParam"] =  findName(mDoorsobject[u'竖框类型'],aTablevalue[u'竖框参数.cfg'])
    doo["mUDBoxParam"] =  findName(mDoorsobject[u'上下横框类型'],aTablevalue[u'上下横框参数.cfg'])
    doo["boxlist"] =None if u'中横框' not in mDoorsobject else mDoorsobject[u'中横框']
    doo["panellist"] = mDoorsobject[u'门板']
    doo['GetPanelPosInDoor'] = GetPanelPosInDoor(mDoorsobject,i)

    return doo


def GetSlidingColorClass(*argv):
    if len(argv) == 3:

        styp = argv[0]
        stype2 = argv[1]
        color = argv[2]
        Result = {}
        for i in range(0,len(mSlidingColorClassList)):
            if ((mSlidingColorClassList[i]['myclass'] == styp) and (mSlidingColorClassList[i]['mat'] == stype2) and
            ((color == mSlidingColorClassList[i]['color']))):
                Result = mSlidingColorClassList[i]
                break

        return Result
    if len(argv) == 2:
        myclass = argv[0]
        color = argv[1]

        Result = {}
        for i in range(0, len(mSlidingColorClassList)):
            if ((mSlidingColorClassList[i]['myclass'] == myclass) and
                    ((color != '') or (color == mSlidingColorClassList[i]['color']))):
                Result = mSlidingColorClassList[i]
                break

        return Result

def GetAccessory(name):
    Result = {}
    for k in range(0,len(aTablevalue[u"五金配件.cfg"])):

        if(aTablevalue[u"五金配件.cfg"][k]['name'] == name):
            Result = aTablevalue[u"五金配件.cfg"][k]
            break

    return Result

def NewWLData():

    pwl={}
    pwl["num"] = 1
    pwl["l"] = 0
    pwl["w"] = 0
    pwl["h"] = 0
    pwl["code"] = ''
    pwl["color"] = ''
    pwl["group"] = 0
    pwl["isglass"] = 0
    pwl["bomsize"] = 0
    pwl["door_index"] = 0
    pwl["pnl_num"] = 0
    pwl["pnl_index"] = 0
    pwl["doorname"] = MBData[u'边框类型']
    return pwl

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

def SAndDoorSetSubject(string, mExp):

    if string==None:
        return string
    if isinstance(string, float) or isinstance(string, int) or string.isdigit():  #是数值就不需要替换的
        return string
    if string == '':
        return string

    items = mExp.items()
    items.sort(SortVar)
    for key ,value in items:

        string = string.replace(key,str(value))

    try:
        if string.isdigit():
            return eval(string)
        return eval(string)

    except:

        return string

def ToColor(c, c1, c2, c3, c4):  #//:string;

    Result = c
    if( c==u'$竖框配件颜色1' ): Result = c1
    if( c==u'$竖框配件颜色2' ): Result = c2
    if( c==u'$竖框配件颜色3' ): Result = c3
    if( c==u'$竖框配件颜色4' ): Result = c4
    return Result

def GetDataValue(data,SubMXList):
    xml = ''
    CurcfgObj = None
    cfgobj = []

    if (data['nType'] == 2):

        if 'direc' in data and data['direc'] == 1:

            xml = Sliding['Sfg_Param']['HTxml']

            cfgobj = copy.deepcopy(HCfgobj2)
        else :

            xml = Sliding['Sfg_Param']['Txml']
            cfgobj = copy.deepcopy(Cfgobj2)

    if (data['nType'] == 3):
        if 'direc' in data and data['direc'] == 1:

            xml = Sliding['Sfg_Param']['HSxml']

            cfgobj = copy.deepcopy(HCfgobj3)
        else:
            xml = Sliding['Sfg_Param']['Sxml']
            cfgobj = copy.deepcopy(HCfgobj2)
    if (data['nType'] == 4):
        if 'direc' in data and data['direc'] == 1:

            xml = Sliding['Sfg_Param']['HFxml']
            cfgobj = copy.deepcopy(HCfgobj4)
        else:
            xml = Sliding['Sfg_Param']['Fxml']
            cfgobj = copy.deepcopy(Cfgobj4)
    bfind = False

    for i in range(0, len(cfgobj)):

        if (data['name'] == cfgobj[i][u'适配竖中横']):

            CurcfgObj = cfgobj[i]
            bfind = True
            break

    if (not bfind): #// 没有对应的模板公式。

        outobj = {
        "xml": xml,
        "CurcfgObj": None,
        "cSBoxp": None
        }
        return outobj
    #u'根据竖中横名称 - - 查询对应竖中横的3个变量的值'
    JSBoxp = SHBoxParam   #竖中横框参数表
    if ('direc' in data and data['direc'] == 1): JSBoxp = HSHBoxParam #// 横中横框参数
    cSBoxp = ''
    for i in range(0, len(JSBoxp)):

        if (data['name'] == JSBoxp[i]['name']): #// 找到竖中横表中对应的中横参数

            cSBoxp = JSBoxp[i]

            pdata = {
                u"名称"	    :   u"$竖中横宽度",
                u"值" 		:JSBoxp[i]['height'],
                u"是否显示" 	:"0",
                u"可选值" 	:""
            }

            pdata2 = {
                u"名称"	 	:u"$竖中横厚度",
                u"值" 		:JSBoxp[i]['depth'],
                u"是否显示" 	:"0",
                u"可选值" 	:""
            }

            pdata3 = {
            u"名称"	 	:u"$槽芯厚度",
            u"值" 		:JSBoxp[i]['thick'],
            u"是否显示" 	:"0",
            u"可选值" 	:""
            }
            if('direc' in data and data['direc'] == 1):

                pdata = {
                    u"名称"	 	:u"$横度",
                    u"值" 		:JSBoxp[i]['height'],
                    u"是否显示" 	:"0",
                    u"可选值" 	:""
                }
                pdata2 = {
                    u"名称"	 	:u"$横中横厚度",
                    u"值" 		: JSBoxp[i]['depth'],
                    u"是否显示" :"0",
                    u"可选值" :""
                }

                pdata3 = {
                    u"名称"	 :  u"$槽芯厚度",
                    u"值" 		:JSBoxp[i]['thick'],
                    u"是否显示" 	:"0",
                    u"可选值" 	:""
                }
                data[u'变量列表'].append(pdata)
                data[u'变量列表'].append(pdata2)
                data[u'变量列表'].append(pdata3)
                break

            data[u'变量列表'].append(pdata)
            data[u'变量列表'].append(pdata2)
            data[u'变量列表'].append(pdata3)
            break

    def ReSetParamValue(CurcfgObj):
        for i in range(0, len(data[u'变量列表'])):

            name = data[u'变量列表'][i][u'名称']

            bfind = False
            for j in range(0, len(CurcfgObj[u'变量列表'])):

                if (CurcfgObj[u'变量列表'][j][u'名称'] == name):
                    CurcfgObj[u'变量列表'][j][u'值'] = data[u'变量列表'][i][u'值']
                    bfind = True
                    break

            if (not bfind):
                data[u'变量列表'][i][u'是否显示'] = "0"
                data[u'变量列表'][i][u'可选值'] = ""
                CurcfgObj[u'变量列表'].append(data[u'变量列表'][i])

    def ResetMxData():
        if u'门芯列表' not in data or data[u'门芯列表'] == {}:
            for j in range(0, len(CurcfgObj[u'门芯列表'])):

                if ((CurcfgObj[u'门芯列表'][j][u'材料'] == '')):
                    CurcfgObj[u'门芯列表'][j][u'材料'] = data[u'材料']
                if ((CurcfgObj[u'门芯列表'][j][u'颜色'] == '')):
                    CurcfgObj[u'门芯列表'][j][u"颜色"] = data[u'颜色']

                if (CurcfgObj[u'门芯列表'][j][u"名称"].find(u"中横") >= 0):  # // 竖中横

                    CurcfgObj[u'门芯列表'][j][u'材料'] = data['name']
        elif (data[u'门芯列表']):

            HBoxcolor = ''  # ; // 中横颜色
            for j in range(0, len(CurcfgObj[u'门芯列表'])):

                b1find = False
                b1find2 = False
                for i in range(0, len(data[u'门芯列表'])):
                    if (CurcfgObj[u'门芯列表'][j][u'名称'] == data[u'门芯列表'][i][u'名称']):

                        CurcfgObj[u'门芯列表'][j][u"材料"] = data[u'门芯列表'][i][u'材料'] if data[u'门芯列表'][i][u'材料']!='' else data[u'材料']

                        CurcfgObj[u'门芯列表'][j][u"颜色"] = data[u'门芯列表'][i][u'颜色'] if data[u'门芯列表'][i][u'颜色'] else data[u'颜色']
                        if (u'子门芯' in data and data[u'门芯列表'][i][u'子门芯'] and len(json.dumps(data[u'门芯列表'][i][u'子门芯'])) > 5):
                            sub = {
                                u'名称': data[u'门芯列表'][i][u'名称'],
                                'index': i,
                                u'子门芯': data[u'门芯列表'][i][u'子门芯']
                            }
                            SubMXList.append(sub)

                        b1find = True

                    if (data[u'门芯列表'][i][u'名称'].find(u"中横") >= 0 and (not b1find2)):
                        HBoxcolor = data[u'门芯列表'][i][u'颜色']
                        b1find2 = True

                    if (b1find and b1find2):
                        break

                if (CurcfgObj[u'门芯列表'][j][u'名称'].find(u"中横")) >= 0:  # // 竖中横

                    CurcfgObj[u'门芯列表'][j][u"材料"] = data['name']
                    CurcfgObj[u'门芯列表'][j][u"颜色"] = HBoxcolor if HBoxcolor else data[u'颜色']

    def GetCurValue(L, H):
        L = float(L)
        H = float(H)
        CurcfgObj[u'门芯列表2'] = []
        CurcfgObj[u'门芯列表3'] = []

        texp = {}
        for i in range(0, len(CurcfgObj[u'变量列表'])):
            Varname = CurcfgObj[u'变量列表'][i][u'名称']

            Varvalue = CurcfgObj[u'变量列表'][i][u'值']
            texp[Varname] = Varvalue

        valuelist = [u"颜色", u"材料", u"名称"]
        for k in range(0, len(CurcfgObj[u'门芯列表'])):
            mxNewOjc = copy.deepcopy(CurcfgObj[u'门芯列表'][k])
            mxNewOjc2 = CurcfgObj[u'门芯列表'][k]
            # mxNewOjc = json.dumps()
            # mxNewOjc2 = json.dumps(CurcfgObj[u'门芯列表'][k])

            for key, value in mxNewOjc.items():
                if key in valuelist:
                    continue
                value = SAndDoorSetSubject(value, texp)
                if isinstance(value, float) or isinstance(value, int) or value.isdigit():
                    mxNewOjc[key] = value
                    continue
                try:
                    mxNewOjc[key] = eval(value)
                except:
                    mxNewOjc[key] = value
            for key, value in mxNewOjc2.items():
                if key in valuelist:
                    continue
                value= SAndDoorSetSubject(value, texp)
                if isinstance(value, float) or isinstance(value, int) or value.isdigit():
                    mxNewOjc2[key] = value
                    continue
                try:
                    mxNewOjc2[key] = eval(value)
                except:
                    mxNewOjc2[key] = value

            CurcfgObj[u'门芯列表2'].append(mxNewOjc)
            CurcfgObj[u'门芯列表3'].append(mxNewOjc2)


    if (data[u'变量列表']!=[]): #// 传入的变量替换掉模板中变量

        ReSetParamValue(CurcfgObj)
    #// 更新对应的材料颜色数据。

    ResetMxData()
    GetCurValue(data['L'], data['H'])
    outobj = {
        "xml": xml,
        "CurcfgObj": CurcfgObj,
        "cSBoxp": cSBoxp
    }
    return outobj

def GetBomObj(data):
    def GetSheetOject(name ,bktype,listtype):

        for i in range(0, len(listtype)):

            if(name == listtype[i]['name'] and bktype == listtype[i]['bktype']):

                return listtype[i]
        return {}

    SubMXList = []
    tobj = GetDataValue(data, SubMXList)
    #// 补充上纹路
    for j in range(0, len(tobj['CurcfgObj'][u'门芯列表'])):

        if u'材料'not in tobj['CurcfgObj'][u'门芯列表'][j]:
            tobj['CurcfgObj'][u'门芯列表'][j][u'材料'] = ''
        pnltype = GetSheetOject(tobj['CurcfgObj'][u'门芯列表'][j][u'材料'], data[u'边框类型'], PanelTypeList)
        if (pnltype !={}):
            tobj['CurcfgObj'][u'门芯列表'][j]['direct2'] = pnltype['direct']
            tobj['CurcfgObj'][u'门芯列表2'][j]['direct2'] = pnltype['direct']
            tobj['CurcfgObj'][u'门芯列表3'][j]['direct2'] = pnltype['direct']

        tobj['CurcfgObj']['direc'] = data['direc']

    if (SubMXList):
        for i in range(0, len(SubMXList)):

            da = SubMXList[i]
            subSubMXList =[]
    # 重新赋值宽高。
            SubMXList[i]['subtobj'] = GetDataValue(da[u'子门芯'], subSubMXList)
            for j in range(0, len(SubMXList[i]['subtobj']['CurcfgObj'][u'门芯列表'])):

                pnltype = GetSheetOject(SubMXList[i]['subtobj'].CurcfgObj[u'门芯列表'][j][u'材料'], data[u'边框类型'], PanelTypeList)
                if (pnltype):
                    SubMXList[i]['subtobj']['CurcfgObj'][u'门芯列表'][j]['direct2'] = pnltype['direct']
                    SubMXList[i]['subtobj']['CurcfgObj'][u'门芯列表2'][j]['direct2'] = pnltype['direct']
                    SubMXList[i]['subtobj']['CurcfgObj']['门芯列表3'][j]['direct2'] = pnltype['direct']

                SubMXList[i]['subtobj'].CurcfgObj['direc'] = da[u'子门芯']['direc']


        for j in range(0, len(tobj['CurcfgObj'][u'门芯列表'])):

            v = tobj['CurcfgObj'][u'门芯列表'][j][u'名称']
            for k in range(0,len(SubMXList)):

                if (SubMXList[k][u'名称'] == v):

                    tobj['CurcfgObj'][u'门芯列表'][j]['subtobj'] = SubMXList[k]['subtobj']
                    tobj['CurcfgObj'][u'门芯列表2'][j]['subtobj'] = SubMXList[k]['subtobj']
                    tobj['CurcfgObj'][u'门芯列表3'][j]['subtobj'] = SubMXList[k]['subtobj']
                    break

    nOutobj = tobj
    return nOutobj

def SupplementPwl(attrib, pwl):
    if attrib not in pwl:
        pwl[attrib] = ''

    return pwl[attrib]

def EscapeBracket(string):
    string = str(string).replace('[','').replace(']','').replace('(','').replace(')','')
    return string

def findMzhBiao2(jo):
    Result = None
    cfglist = aTablevalue[u"门转换表.cfg"]
    n = len(cfglist)

    for i in range(0, n):
        cfg = cfglist[i]
        if( cfg[u'模式']!= str(mDataMode) ):
            continue
        if( cfg[u'名称']!=jo['name'] ):
            continue
        if( cfg[u'物料名称']=='' ):
            continue
        s = cfg[u'边框类型'] + ','
        ss = jo['doorname'] + ','

        t = s.find(ss)
        if( t<0 ):
            continue
        return cfg


def GetXMLBom(xml):
    global MBData,aTablevalue,ALLlist,mDataMode,mGridItem,mExp,skcolor1, skcolor2, skcolor3, skcolor4
    def ReadXML(xml):
        global mDataMode,mGridItem
        root = ET.fromstring(xml)
        mDataMode = root.get('mDataMode',0)
        mGridItem = float(root.get(u'均分', 0))
        jsonobj = []
        Node = {}
        arr = root.attrib
        Node[root.tag] = arr
        Xml2Json(root, Node[root.tag])
        return Node

    MBData = ReadXML(xml)

    if MBData == {}:
        return ''
    #颜色
    skcolor1, skcolor2, skcolor3, skcolor4 = '','','',''
    #初始化所有的配置数据
    SlidingInitData()
    #将趟门的所有物料数据添加进来
    ALLlist = []

    MBData = MBData[u'趟门']

    wldata = {
    "code": "",
    "name": "",
    "color": "",
    "direct": "",
    "myunit": "",
    "memo": "",
    "doorname": "",
    "memo2": "",
    "memo3": "",
    "bdfile": "",
    "num":"",
    "group":"",
    "door_index":"",
    "pnl_num":"",
    "pnl_index":"",
    "isglass":"",
    "l":"",
    "w":"",
    "h":"",
    "bomsize":""
    }
    aTablevalue = {} #// 读取基本表的配置
    aTablevalue[u"百叶板计算公式.cfg"] = mSSExpList
    aTablevalue[u"单门数量类型.cfg"] = mSlidingExpList
    aTablevalue[u"门板附加物料.cfg"] = mPanelBomDetailList
    aTablevalue[u"门板类型.cfg"] = PanelTypeList
    aTablevalue[u"门类型.cfg"] = mSlidingTypeList
    aTablevalue[u"上下轨参数.cfg"] = TrackParam
    aTablevalue[u"上下横框参数.cfg"] = UDBoxParam
    aTablevalue[u"竖框参数.cfg"] = mVBoxParamList
    aTablevalue[u"竖中横框参数.cfg"] = UHBoxParam
    aTablevalue[u"横中横框参数.cfg"] = HHBoxParam
    aTablevalue[u"趟门参数.cfg"] = SlidingParam
    aTablevalue[u"五金配件.cfg"] = mSlidingAccessoryList
    aTablevalue[u"五金配件分类数据.cfg"] = mSlidingWjBomDetailList
    aTablevalue[u"颜色分类.cfg"] = mSlidingColorClassList
    aTablevalue[u"颜色分类2.cfg"] = mSlidingColorList
    aTablevalue[u"中横框参数.cfg"] = HBoxParam
    aTablevalue[u"门转换表.cfg"] = cfglist


    mSlidingExpList = findName(MBData[u'单门数量类型'], aTablevalue[u'单门数量类型.cfg'])
    mL = float(MBData[u'门洞宽'])
    mH = float(MBData[u'门洞高'])
    mAddLength = MBData[u'延长导轨']
    mDoorsList = MBData[u'单门']
    mExp = {}
    mExp[u'$门洞高度'] = MBData[u'门洞高']
    mExp[u'$门洞宽度'] = MBData[u'门洞宽']
    mExp[u'$重叠数'] = mSlidingExpList['overlapnum']
    mExp[u'$门扇数'] = mSlidingExpList['doornum']

    mSlidingParam = findName(MBData[u'边框类型'], aTablevalue[u'趟门参数.cfg'])
    if( len(mDoorsList) > 0 ):

        door = TDoorRect(mDoorsList, 0)
        mExp[u'$成品门宽度'] = door['doorw']
        mExp[u'$成品门高度'] = door['doorh']
        #'竖框' 为颜色分类的cfg中myclass,    mSlidingParam['vboxtype']为颜色分类的cfg中mat door['mVBoxColor']为颜色分类的cfg中color
        pcolorclass = GetSlidingColorClass(u'竖框', mSlidingParam['vboxtype'],door['mVBoxColor'])#//door.mVBoxColor 竖框颜色
        if( pcolorclass !={}):

            skcolor1 = pcolorclass['skcolor1']
            skcolor2 = pcolorclass['skcolor2']
            skcolor3 = pcolorclass['skcolor3']
            skcolor4 = pcolorclass['skcolor4']

    #// 获取上下轨数据
    mTrackParam = findName(MBData[u'上下轨类型'], aTablevalue[u'上下轨参数.cfg']) #上下轨类型 和 上下轨参数.cfg得到上下轨数据
    mMyUpTrackColor = MBData[u'上轨颜色']
    #// 上轨
    if ((mDataMode == 0) and (mTrackParam['wlupcode'] != '')):

        pwl = NewWLData()
        pwl['name'] = mTrackParam['upname']
        pwl['code'] = mTrackParam['wlupcode']
        pwl['color'] = mMyUpTrackColor
        pwl['l'] = mL - float(mTrackParam['lkvalue1'])
        if (mAddLength > 0) : pwl['l'] = float(pwl['l']) + float(mAddLength)
        pwl['w'] = 0
        pwl['h'] = 0
        pwl['bomsize'] = mTrackParam['upsize']
        pcolorclass = GetSlidingColorClass(u'上轨', pwl['name'], pwl['color'])  #竖框配件颜色
        if pcolorclass !={}:
            pwl['code'] = pwl['code'] + '' + pcolorclass['wlcode']
        pwl['num'] = 1
        pwl['group'] = 1
        pwl['memo'] = mTrackParam['upmemo']
        pwl['myunit'] = u'条'
        pwl['bdfile'] = mTrackParam['upbdfile']
        ALLlist.append(pwl)
        mExp[u'$上轨长度'] = pwl['l']

    mMyDownTrackColor = MBData[U'下轨颜色']
    # // 下轨
    if ((mDataMode == 0) and (mTrackParam['wldncode'])):

        pwl = NewWLData()
        pwl['name'] = mTrackParam['dnname']
        pwl['code'] = mTrackParam['wldncode']
        pwl['color'] = mMyDownTrackColor
        pwl['l'] = mL - float(mTrackParam['lkvalue2'])
        if (mAddLength > 0): pwl['l'] = float(pwl['l']) + float(mAddLength)
        pwl['w'] = 0
        pwl['h'] = 0
        pwl['bomsize'] = mTrackParam['downsize']
        pcolorclass = GetSlidingColorClass(u'下轨', pwl['name'], pwl['color'])
        if pcolorclass != {}:
            pwl['code'] = pwl['code'] + '' + pcolorclass['wlcode']
        pwl['num'] = 1
        pwl['group'] = 1
        pwl['memo'] = mTrackParam['dnmemo']
        pwl['myunit'] = u'条'
        pwl['bdfile'] = mTrackParam['dnbdfile']
        ALLlist.append(pwl)
        mExp[u'$下轨长度'] = pwl['l']

    #// 趟门关联的五金
    wjname = mSlidingParam['wjname']
    if ((mDataMode == 0) and (wjname != '')):

        for m in range(0,len(mSlidingWjBomDetailList)):

            pbomdetail = mSlidingWjBomDetailList[m]
            if ( pbomdetail['bomname'] == wjname ):

                pwl = NewWLData()
                pwl['name'] = pbomdetail['name']
                pwl['l'] = SAndDoorSetSubject(pbomdetail['l'], mExp)

                pwl['w'] = SAndDoorSetSubject(pbomdetail['d'], mExp)
                pwl['num'] = SAndDoorSetSubject(pbomdetail['num'], mExp)
                pa = GetAccessory(pwl['name'])
                pwl['group'] = 3
                if (pa != {}):

                    pwl['memo'] = pa['memo']
                    pwl['memo2'] = pa['memo2']
                    pwl['memo3'] = pa['memo3']
                    pwl['bdfile'] = pa['bdfile']
                    pwl['color'] = ToColor(pa['color'], skcolor1, skcolor2, skcolor3, skcolor4)
                    pwl['code'] = pa['wlcode']
                    pcolorclass = GetSlidingColorClass(u'配件', pa['name'], pwl['color'])
                    if (pcolorclass !={}):
                        pwl['code'] = pwl['code'] + '' + pcolorclass['wlcode']
                    pwl['myunit'] = pa['unit']
                    if ( pa['isglass'] ): pwl['isglass'] = 1
                    else: pwl['isglass'] = 0
                    if ( pa['myclass'] == u'型材' ): pwl['group'] = 1
                    if ( pa['myclass'] == u'门板' ): pwl['group'] = 2

                ALLlist.append(pwl)
    # // 上轨五金
    if ((mDataMode == 0) and (mTrackParam['wjname1'] != '')): #// 上轨五金

        for m in range(0, len(mSlidingWjBomDetailList)):

            pbomdetail = mSlidingWjBomDetailList[m]
            if ( pbomdetail['bomname'] == mTrackParam['wjname1']):

                pwl = NewWLData()
                pwl['name'] = pbomdetail['name']
                pwl['l'] = SAndDoorSetSubject(pbomdetail['l'], mExp)

                pwl['w'] = SAndDoorSetSubject(pbomdetail['d'], mExp)
                pwl['num'] = SAndDoorSetSubject(pbomdetail['num'], mExp)
                pa = GetAccessory(pwl['name'])
                pwl['group'] = 3
                if (pa != {}):

                    pwl['memo'] = pa['memo']
                    pwl['memo2'] = pa['memo2']
                    pwl['memo3'] = pa['memo3']
                    pwl['bdfile'] = pa['bdfile']
                    pwl['color'] = ToColor(pa['color'], skcolor1, skcolor2, skcolor3, skcolor4)
                    pwl['code'] = pa['wlcode']
                    pwl['myunit'] = pa['unit']
                    if (pa['isglass']):
                        pwl['isglass'] = 1
                    else:
                        pwl['isglass'] = 0
                    pcolorclass = GetSlidingColorClass(u'配件', pa['name'], pwl['color'])
                    if (pcolorclass != {}):
                        pwl['code'] = pwl['code'] + '' + pcolorclass['wlcode']
                    if (pa['myclass'] == u'型材'): pwl['group'] = 1
                    if (pa['myclass'] == u'门板'): pwl['group'] = 2

                ALLlist.append(pwl)

    # // 下轨五金
    if ((mDataMode == 0) and (mTrackParam['wjname2'] != '')): #// 下轨五金

        for m in range(0, len(mSlidingWjBomDetailList)):

            pbomdetail = mSlidingWjBomDetailList[m]
            if ( pbomdetail['bomname'] == mTrackParam['wjname2']):

                pwl = NewWLData()
                pwl['name'] = pbomdetail['name']
                pwl['l'] = SAndDoorSetSubject(pbomdetail['l'], mExp)
                pwl['w'] = SAndDoorSetSubject(pbomdetail['d'], mExp)
                pwl['num'] = SAndDoorSetSubject(pbomdetail['num'], mExp)
                pa = GetAccessory(pwl['name'])
                pwl['group'] = 3
                if (pa != {}):

                    pwl['memo'] = pa['memo']
                    pwl['memo2'] = pa['memo2']
                    pwl['memo3'] = pa['memo3']
                    pwl['bdfile'] = pa['bdfile']
                    pwl['color'] = ToColor(pa['color'], skcolor1, skcolor2, skcolor3, skcolor4)
                    pwl['code'] = pa['wlcode']
                    pwl['myunit'] = pa['unit']
                    if (pa['isglass']):
                        pwl['isglass'] = 1
                    else:
                        pwl['isglass'] = 0
                    pcolorclass = GetSlidingColorClass(u'配件', pa['name'], pwl['color'])
                    if (pcolorclass != {}):
                        pwl['code'] = pwl['code'] + '' + pcolorclass['wlcode']
                    if (pa['myclass'] == u'型材'): pwl['group'] = 1
                    if (pa['myclass'] == u'门板'): pwl['group'] = 2

                ALLlist.append(pwl)

    #// 竖框 + 竖框五金
    for i in range(0,len(mDoorsList)):
        if ((mDataMode == 1)):
            break
        door = TDoorRect(mDoorsList, i)

        pwl = NewWLData()
        pwl['name'] = door['mVBoxParam']['name']
        pwl['color'] = door['mVBoxColor']

        pvbox = findName(pwl['name'], aTablevalue[u'竖框参数.cfg'])
        if (pvbox !={}):

            pwl['memo'] = pvbox['memo']
            pwl['bdfile'] = pvbox['bdfile']
            pwl['code'] = pvbox['wlcode']
            pwl['w'] = 0
            pwl['h'] = 0

        pcolorclass = GetSlidingColorClass(u'竖框', pwl['name'], pwl['color'])
        if (pcolorclass !={}):
            pwl['code'] = pwl['code'] + '' + pcolorclass['wlcode']
        pwl['num'] = 2
        pwl['l'] = door['doorh'] - float(pvbox['vboxvalue'])
        pwl['group'] = 1
        pwl['myunit'] = u'根'
        pwl['bomsize'] = pvbox['size']
        pwl['door_index'] = i + 1
        ALLlist.append(pwl)
        mExp[u'$竖框长度'] = pwl['l']

        if (door['mVBoxParam']['wjname'] != ''): #// 竖框五金

            for m in range(0, len(mSlidingWjBomDetailList)):

                pbomdetail = mSlidingWjBomDetailList[m]
                if ( pbomdetail['bomname'] == door['mVBoxParam']['wjname']):

                    pwl = NewWLData()
                    pwl['name'] = pbomdetail['name']
                    pwl['l'] = SAndDoorSetSubject(pbomdetail['l'], mExp)

                    pwl['w'] = SAndDoorSetSubject(pbomdetail['d'], mExp)
                    pwl['num'] = SAndDoorSetSubject(pbomdetail['num'], mExp)
                    pa = GetAccessory(pwl['name'])
                    pwl['group'] = 3
                    pwl['door_index'] = i + 1
                    if (pa != {}):

                        pwl['memo'] = pa['memo']
                        pwl['memo2'] = pa['memo2']
                        pwl['memo3'] = pa['memo3']
                        pwl['bdfile'] = pa['bdfile']

                        pwl['color'] = ToColor(pa['color'], skcolor1, skcolor2, skcolor3, skcolor4)

                        pwl['code'] = pa['wlcode']
                        pwl['myunit'] = pa['unit']
                        if (pa['isglass']):
                            pwl['isglass'] = 1
                        else:
                            pwl['isglass'] = 0
                        pcolorclass = GetSlidingColorClass(u'配件', pa['name'], pwl['color'])
                        if (pcolorclass != {}):
                            pwl['code'] = pwl['code'] + '' + pcolorclass['wlcode']
                        if (pa['myclass'] == u'型材'): pwl['group'] = 1
                        if (pa['myclass'] == u'门板'): pwl['group'] = 2

                    ALLlist.append(pwl)


    mMyUpBoxColor = MBData[u'上横框颜色']
    mMyDownBoxColor = MBData[u'下横框颜色']
    mUDBoxParam = findName(MBData[u'上下横框类型'],aTablevalue[u'上下横框参数.cfg'])

    for i in range(0,len(mDoorsList)):
        if ((mDataMode == 1)):
            break
        door = TDoorRect(mDoorsList, i)

        pwl = NewWLData()
        pwl['name'] = mUDBoxParam['upname']
        pwl['color'] = mMyUpBoxColor
        pwl['code'] = mUDBoxParam['wlupcode']
        pwl['bdfile'] = mUDBoxParam['upbdfile']
        pcolorclass = GetSlidingColorClass(u'上横框', pwl['name'], pwl['color'])
        if (pcolorclass != {}):
            pwl['code'] = pwl['code'] + '' + pcolorclass['wlcode']
        pwl['w'] = 0
        pwl['h'] = 0

        pwl['num'] = 1
        pwl['group'] = 1
        pwl['l'] = door['doorw'] - float(door['mVBoxParam']['udboxvalue'])*2
        pwl['bomsize'] = mUDBoxParam['upsize']
        pwl['memo'] = mUDBoxParam['upmemo']
        pwl['door_index'] = i + 1
        pwl['myunit'] = u'根'
        ALLlist.append(pwl)

        mExp[u'$上横框长度'] = pwl['l']

        pwl = NewWLData()
        pwl['name'] = mUDBoxParam['dnname']
        pwl['color'] = mMyDownBoxColor
        pwl['code'] = mUDBoxParam['wldncode']
        pwl['bdfile'] = mUDBoxParam['dnbdfile']
        pcolorclass = GetSlidingColorClass(u'下横框', pwl['name'], pwl['color'])
        if (pcolorclass != {}):
            pwl['code'] = pwl['code'] + '' + pcolorclass['wlcode']
        pwl['w'] = 0
        pwl['h'] = 0
        pwl['num'] = 1
        pwl['group'] = 1
        pwl['l'] = door['doorw'] - float(door['mVBoxParam']['udboxvalue']) * 2

        pwl['bomsize'] = mUDBoxParam['downsize']
        pwl['memo'] = mUDBoxParam['dnmemo']
        pwl['door_index'] = i + 1
        pwl['myunit'] = u'根'
        ALLlist.append(pwl)
        mExp[u'$下横框长度'] = pwl['l']

        if (door['mUDBoxParam']['wjname1'] != ''): #// 上横框五金

            for m in range(0, len(mSlidingWjBomDetailList)):

                pbomdetail = mSlidingWjBomDetailList[m]
                if ( pbomdetail['bomname'] == door['mUDBoxParam']['wjname1']):

                    pwl = NewWLData()
                    pwl['name'] = pbomdetail['name']
                    pwl['l'] = SAndDoorSetSubject(pbomdetail['l'], mExp)
                    pwl['w'] = SAndDoorSetSubject(pbomdetail['d'], mExp)
                    pwl['num'] = SAndDoorSetSubject(pbomdetail['num'], mExp)
                    pa = GetAccessory(pwl['name'])
                    pwl['group'] = 3
                    pwl['door_index'] = i + 1
                    if (pa != {}):

                        pwl['memo'] = pa['memo']
                        pwl['memo2'] = pa['memo2']
                        pwl['memo3'] = pa['memo3']
                        pwl['bdfile'] = pa['bdfile']
                        pwl['color'] = ToColor(pa['color'], skcolor1, skcolor2, skcolor3, skcolor4)
                        pwl['code'] = pa['wlcode']
                        pwl['myunit'] = pa['unit']
                        if (pa['isglass']):
                            pwl['isglass'] = 1
                        else:
                            pwl['isglass'] = 0
                        pcolorclass = GetSlidingColorClass(u'配件', pa['name'], pwl['color'])
                        if (pcolorclass != {}):
                            pwl['code'] = pwl['code'] + '' + pcolorclass['wlcode']
                        if (pa['myclass'] == u'型材'): pwl['group'] = 1
                        if (pa['myclass'] == u'门板'): pwl['group'] = 2
                    ALLlist.append(pwl)

        if (door['mUDBoxParam']['wjname2'] != ''): #// 下横框五金

            for m in range(0, len(mSlidingWjBomDetailList)):

                pbomdetail = mSlidingWjBomDetailList[m]
                if ( pbomdetail['bomname'] == door['mUDBoxParam']['wjname2']):

                    pwl = NewWLData()
                    pwl['name'] = pbomdetail['name']
                    pwl['l'] = SAndDoorSetSubject(pbomdetail['l'], mExp)
                    pwl['w'] = SAndDoorSetSubject(pbomdetail['d'], mExp)
                    pwl['num'] = SAndDoorSetSubject(pbomdetail['num'], mExp)
                    pa = GetAccessory(pwl['name'])
                    pwl['group'] = 3
                    pwl['door_index'] = i + 1
                    if (pa != {}):

                        pwl['memo'] = pa['memo']
                        pwl['memo2'] = pa['memo2']
                        pwl['memo3'] = pa['memo3']
                        pwl['bdfile'] = pa['bdfile']
                        pwl['color'] = ToColor(pa['color'], skcolor1, skcolor2, skcolor3, skcolor4)
                        pwl['code'] = pa['wlcode']
                        pwl['myunit'] = pa['unit']
                        if (pa['isglass']):
                            pwl['isglass'] = 1
                        else:
                            pwl['isglass'] = 0
                        pcolorclass = GetSlidingColorClass(u'配件', pa['name'], pwl['color'])
                        if (pcolorclass != {}):
                            pwl['code'] = pwl['code'] + '' + pcolorclass['wlcode']
                        if (pa['myclass'] == u'型材'): pwl['group'] = 1
                        if (pa['myclass'] == u'门板'): pwl['group'] = 2

                    ALLlist.append(pwl)

    #中横框属性计算    +    下横框五金
    for i in range(0, len(mDoorsList)):
        if ((mDataMode == 1)): break
        door = TDoorRect(mDoorsList, i)
        if ('boxlist' not in door): continue
        if (door['boxlist'] ==None): continue
        for j in range(0, len(door['boxlist'])):

            rb = door['boxlist'][j]
            if (rb['h0'] <= 0):continue
            addBox(rb,door,i)


    #添加门芯
    for i in range(0, len(mDoorsList)):
        if ((mDataMode == 1)): break
        door = TDoorRect(mDoorsList, i)
        if ('panellist' not in door): continue
        if (door['panellist'] ==None): continue
        for j in range(0, len(door['panellist'])):

            pnl = door['panellist'][j]
            if ('ExtraData' in pnl and len(pnl['ExtraData']) > 5): #有竖格门芯再此 从门板中ExtraData字段提取竖格门芯
                Sfg_Param = {}
                sfgFK = Sfg_Param

                sJson = pnl['ExtraData']
                sJson = sJson.replace('^', '"')

                Jsonvar = json.loads(sJson)
                Jsonvar['L'] = pnl['w1']
                Jsonvar['H'] = pnl['h1']

                if 'direc' not in Jsonvar: Jsonvar['direc'] = 0
                FGObj = GetBomObj(Jsonvar)

                for fg in range(0, len(FGObj['CurcfgObj'][u'门芯列表2'])):
                    oneMxs = FGObj['CurcfgObj'][u'门芯列表2'][fg]

                    if ('subtobj' in oneMxs and len(json.dumps(oneMxs['subtobj'])) > 5):

                        for subfg in range(0, len(oneMxs['subtobj']['CurcfgObj'][u'门芯列表2'])):

                            subMxs = oneMxs['subtobj']['CurcfgObj'][u'门芯列表2'][subfg]
                            newMx = {
                                'd0': eval(subMxs[u'深'])
                                , 'd1': eval(subMxs[u'深'])
                                , 'd2': eval(subMxs[u'深'])
                                , 'h0': eval(subMxs[u'高'])
                                , 'h1': eval(subMxs[u'高'])
                                , 'h2': eval(subMxs[u'高'])
                                , 'w0': eval(subMxs[u'宽'])
                                , 'w1': eval(subMxs[u'宽'])
                                , 'w2': eval(subMxs[u'宽'])
                                , 'x0': eval(subMxs['x'])
                                , 'x1': eval(subMxs['x'])
                                , 'x2': eval(subMxs['x'])
                                , 'y0': eval(subMxs['y'])
                                , 'y1': eval(subMxs['y'])
                                , 'y2': eval(subMxs['y'])
                                , u'备注': ""
                                , u'类型': subMxs[u'材料']
                                , u'纹路': subMxs['direct2']
                                , u'颜色': subMxs[u'颜色']
                                , u'颜色2': ""
                            }
                            if (subMxs[u'名称'].find(u'门芯') == 0):

                                newMx['PanelNum'] = pnl['PanelNum']
                                # 根据门芯的物料尺寸 - 门芯的进槽值  = 门芯的见光尺寸
                                lObj = ResetSubMxSize(mGridItem, j, fg, subfg, FGObj, Jsonvar, door['mUDBoxParam'],
                                                      door['mVBoxParam'])
                                newMx['h0'] = newMx['h0'] - lObj['ch0']
                                newMx['w0'] = newMx['w0'] - lObj['cw0']
                                AddOneMx(i, door, j, newMx, nHasMzhb)

                            else:
                                # // 竖中横的 高 ：物料尺寸不根据 模板公式来计算，直接为其图像尺寸
                                # // 门芯尺寸- 竖时为其  门芯尺寸 - 上下横框进槽值，
                                # // 门均分数，最外层是第几门芯，第二次是第几个门芯，最后的是第几个门芯
                                relength = ResetMBoxSize(mGridItem, j, fg, subfg, FGObj, Jsonvar, door['mUDBoxParam'],
                                                         door['mVBoxParam'])

                                newMx['h0'] = eval(oneMxs[u'高']) - relength
                                newMx['h1'] = eval(oneMxs[u'高'])
                                newMx['h2'] = eval(oneMxs[u'高'])
                                nType = 1
                                if (oneMxs['subtobj']['CurcfgObj']['direc'] == 1):
                                    nType = 2  # // 横切
                                    newMx['h0'] = eval(oneMxs[u'宽']) - relength
                                    newMx['h1'] = eval(oneMxs[u'宽'])
                                    newMx['h2'] = eval(oneMxs[u'宽'])

                                addBox(newMx,door,i, nType)

                    else:
                        if u'材料' not in oneMxs: oneMxs[u'材料'] = ''
                        if 'direct2' not in oneMxs: oneMxs[u'direct2'] = ""
                        if u'颜色' not in oneMxs: oneMxs[u'颜色'] = ""
                        #print 'oneMxs=',json.dumps(oneMxs,ensure_ascii=False)
                        newMx = {
                            'd0': eval(str(oneMxs[u'深']))
                            , 'd1': eval(str(oneMxs[u'深']))
                            , 'd2': eval(str(oneMxs[u'深']))
                            , 'h0': eval(str(oneMxs[u'高']))
                            , 'h1': eval(str(oneMxs[u'高']))
                            , 'h2': eval(str(oneMxs[u'高']))
                            , 'w0': eval(str(oneMxs[u'宽']))
                            , 'w1': eval(str(oneMxs[u'宽']))
                            , 'w2': eval(str(oneMxs[u'宽']))
                            , 'x0': eval(str(oneMxs[u'x']))
                            , 'x1': eval(str(oneMxs[u'x']))
                            , 'x2': eval(str(oneMxs[u'x']))
                            , 'y0': eval(str(oneMxs[u'y']))
                            , 'y1': eval(str(oneMxs[u'y']))
                            , 'y2': eval(str(oneMxs[u'y']))
                            , u'备注': ""
                            , u'类型': oneMxs[u'材料']
                            , u'纹路': oneMxs['direct2']
                            , u'颜色': oneMxs[u'颜色']
                            , u'颜色2': ""
                        }
                        if (oneMxs[u'名称'].find(u'门芯') == 0):
                            if 'PanelNum' not in pnl:
                                pnl['PanelNum'] = 0

                            newMx['PanelNum'] = pnl['PanelNum']
                            # 根据门芯的物料尺寸 - 门芯的进槽值  = 门芯的见光尺寸
                            lObj = ResetMxSize(mGridItem, j, fg, FGObj, Jsonvar, door['mUDBoxParam'],
                                               door['mVBoxParam'])
                            newMx['h0'] = newMx['h0'] - lObj['ch0']
                            newMx['w0'] = newMx['w0'] - lObj['cw0']
                            # print 'newMx=',json.dumps(newMx,ensure_ascii=False)
                            # print 'AddOneMx', len(ALLlist)
                            AddOneMx(i, door, j, newMx, nHasMzhb)

                        else:
                            # // 竖中横的 高 ：物料尺寸不根据 模板公式来计算，直接为其图像尺寸
                            # // 门芯尺寸- 竖时为其  门芯尺寸 - 上下横框进槽值，
                            # // 门均分数，最外层是第几门芯，第二次是第几个门芯，最后的是第几个门芯
                            if 'h0' not in pnl: pnl['h0'] = ''
                            if 'w0' not in pnl: pnl['w0'] = ''
                            newMx['h0'] = pnl['h0']
                            newMx['h1'] = pnl['h0']
                            newMx['h2'] = pnl['h0']
                            nType = 1
                            if (FGObj['CurcfgObj']['direc'] == 1):
                                nType = 2  # // 横切
                                newMx['h0'] = pnl['w0']
                                newMx['h1'] = pnl['w0']
                                newMx['h2'] = pnl['w0']
                            addBox(newMx, door,i, nType)
                            # print 'addBox3', len(ALLlist)
            else:
                AddOneMx(i, door, j, pnl, nHasMzhb)
                # print 'AddOneMx2', len(ALLlist)

    #// 定款门按照单门输出
    for i in range(0, len(mDoorsList)):

        if (mDataMode == 0):
            break
        door = TDoorRect(mDoorsList, i)

        pwl = NewWLData()
        pwl['name'] = mSlidingParam['name']
        pwl['color'] = door['mVBoxColor']
        pwl['num'] = 1
        pwl['memo'] = mSlidingParam['memo']
        pwl['l'] = door['doorh']
        pwl['w'] = door['doorw']
        pwl['group'] = 2
        ALLlist.append(pwl)
        # print u'定款门12', len(ALLlist)

    # 自选配件
    if u'配件' in MBData:
        treelist2 = MBData[u'配件']
        if (treelist2):

            for i in range(0, len(treelist2)):

                pwl = NewWLData()
                pwl['name'] = treelist2[i][u'名称']
                pwl['code'] = pwl['code']
                pwl['color'] = ''
                pcolorclass = GetSlidingColorClass(u'配件', pwl['color'])
                if (pcolorclass):
                    pwl['code'] = pwl['code'] + '' + pcolorclass['wlcode']
                pwl['l'] = 0
                pwl['w'] = 0
                pwl['h'] = 0
                pwl['num'] = treelist2[i][u'数量']
                pwl['group'] = 3
                pa = GetAccessory(pwl['name'])
                if ( pa  ):

                    pwl['memo'] = pa['memo']
                    pwl['memo2'] = pa['memo2']
                    pwl['memo3'] = pa['memo3']
                    pwl['bdfile'] = pa['bdfile']
                    pwl['color'] = ToColor(pa.color, skcolor1, skcolor2, skcolor3, skcolor4)
                    pwl['code'] = pa['wlcode']
                    pwl['myunit'] = pa['unit']
                    if ( pa['isglass'] ): pwl['isglass'] = 1
                    else: pwl['isglass'] = 0
                    pcolorclass = GetSlidingColorClass(u'配件', pwl['color'])
                    if ( pcolorclass  ): pwl['code'] = pwl['code'] + '' + pcolorclass['wlcode']
                    if ( pa['myclass'] == u'型材' ): pwl['group'] = 1
                    if ( pa['myclass'] == u'门板' ): pwl['group'] = 2

                ALLlist.append(pwl)
                # print u'配件13', len(ALLlist)
                mExp[u'$上轨长度']= pwl['l']
    # print u'len of ALLlist', len(ALLlist)
    list2 = []
    j = 0
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
        newpw2 = {
                "Num": int(float(eval(str(pwl['num'])))),
                "W": float(pwl['w']),
                "L": l,
                "H": float(pwl['h']),
                "#": j,
                "DoorIndex": SupplementPwl('door_index',pwl),
                "PanelIndex": SupplementPwl('pnl_index',pwl),
                "Group": SupplementPwl('group',pwl),
                "Glass": SupplementPwl('isglass',pwl),
                "Di":SupplementPwl('direct',pwl),
                "PanelNum": SupplementPwl('pnl_num',pwl),
                "DoorName": SupplementPwl('doorname',pwl),
                "Unit":SupplementPwl('myunit',pwl),
                "Name": EscapeBracket(SupplementPwl('door_index',pwl)),
                "Code": pwl['code'],
                "Color":SupplementPwl('color',pwl),
                "Memo": SupplementPwl('memo',pwl),
                "Memo2": SupplementPwl('memo2',pwl),
                "Memo3": SupplementPwl('memo3',pwl),
                "Bomsize":SupplementPwl('bomsize',pwl),
                "BDFILE":SupplementPwl('bdfile',pwl),
        }
        j = j+1
        if (nHasMzhb):

            myUi = findMzhBiao2(pwl)

            if (not myUi):

                continue

            newpw2['Name'] = myUi[u'物料名称']
            newpw2['Unit'] = myUi[u'单位']

        list2.append(newpw2)
    # print 'len of list2', len(list2)
    return list2



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

    for i in range(0, len(mPanelBomDetailList)):

        p = mPanelBomDetailList[i]

        if ((p['bomclass'] == bomclass) and (float(p['lmin']) < float(pnll)) and (float(p['lmax']) >= float(pnll)) and (
                float(p['hmin']) < float(pnlh)) and (float(p['hmax']) >= float(pnlh))):

            pwl = NewWLData()
            pwl['name'] = p['bomname']
            pwl['code'] = ''
            pwl['color'] = p['color'].replace(u'$门板颜色', color)
            if (pwl['color'].find(u"门芯颜色") != -1): #// 如果不加上这个那么会出现门板颜色替换时，替换失败。
                pwl['color']= p['color'].replace( u'$门芯颜色', color)
            pwl['color'] = pwl['color'].replace(u'$附加物料颜色', color2)
            pwl['color'] = pwl['color'].replace(u'$边框颜色', color3)
            pwl['memo ']= p['memo']
            pwl['memo2'] = p['memo2']
            pwl['memo3'] = p['memo3']

            pwl['l'] = SAndDoorSetSubject(p['l'], mExp)
            pwl['w'] = SAndDoorSetSubject(p['w'], mExp)
            pwl['h'] = SAndDoorSetSubject(p['h'], mExp)
            pwl['group'] = 2
            if ( p['bomtype'] == u'型材五金'):pwl['group'] = 1
            if ( p['bomtype'] == u'五金' ):pwl['group'] = 3
            if ( p['bomtype'] == u'玻璃' ):pwl['isglass'] = 1

            pwl['num'] = p['num']
            pwl['bdfile'] = p['bdfile']
            # print 'l=',pwl['l']
            # print 'w=', pwl['w']
            ALLlist.append(pwl)
            # print '44444444444414=',len(ALLlist)
def AddOneMx(i, door, j, pnl, nHasMzhb):
    #print 'AddOneMxw1=',pnl['w1']
    mExp[u'$门板高度0'] = pnl['h0']
    mExp[u'$门板宽度0'] = pnl['w0']
    mExp[u'$门板高度'] = pnl['h1']
    mExp[u'$门板宽度'] = pnl['w1']
    jtvalue = 0
    isglass = False
    isbaiye = False
    w1 = 0
    h1 = 0
    #print '44444444444401=' + str(len(ALLlist))
    pnltype = GetPanelType(mSlidingParam['name'], pnl[u'类型'])

    if (pnltype):
        GetPanelBom(ALLlist, pnltype['slaVe'], pnl[u'类型'], pnl[u'颜色'], pnl[u'颜色2'], door['mVBoxColor'], pnl['w1'], pnl['h1'])
        jtvalue = float(pnltype['jtValue']) * 2

        isglass = pnltype['isglass'] #// (pnltype.isglass == "TRUE")?true:false;
        isbaiye = pnltype['isbaiye'] #// (pnltype.isbaiye == "TRUE")?true:false;
        w1 = float(pnltype['mkl'])
        h1 = float(pnltype['mkH'])
    #print '4444444444441=' + str(len(ALLlist))
    glvalue1 = 0
    glvalue2 = 0
    #// 当板材为玻璃的时候，需要减掉趟门的玻璃位
    #print 'isglass=',isglass,'isbaiye=',isbaiye
    if (isglass):

        glvalue1 = float(mSlidingParam['vboxjtw']) * 2
        pos = GetPanelPosInDoor(door, pnl)
        if ((pos == 1)): #// 最下格
            glvalue2 = float(mSlidingParam['hboxjtw']) + float(mSlidingParam['dboxjtw'])
        elif ( (pos == 2) ): #// 最上格
            glvalue2 = float(mSlidingParam['hboxjtw']) + float(mSlidingParam['uboxjtw'])
        elif ( (pos == 0) ): #// 中间格
            glvalue2 = float(mSlidingParam['hboxjtw']) * 2
        else: glvalue2 = float(mSlidingParam['dboxjtw']) + float(mSlidingParam['uboxjtw'])

    pssexp = GetSSExp(pnl[u'类型'])
    #print 'pssexp=',json.dumps(pssexp, ensure_ascii=False)

    if ((not isglass) and (isbaiye) and (pssexp)):
        #print pssexp['paneltype']

        h = float(pnl['h1']) - h1
        w = float(pnl['w1']) - w1
        if (Number(pssexp['height']) != 0):

            n = (h - jtvalue - glvalue2) / float(pssexp['height'])
            n = int(n) #// GetFixed(n, 0) #// 直接舍弃取整
            t = (h - jtvalue - glvalue2) - float(pssexp['height']) * n
            if ( t > float(pssexp['minheight']) ):

                n = n + 1
            else:
                t = 0
            for k in range(0, n):

                if ((k == n - 1) and (t != 0)):

                    pwl = NewWLData()
                    pwl['name'] = pnl[u'类型'] #// '门板';
                    pwl['color'] = pnl[u'颜色']
                    pwl['memo'] = pnl[u'备注']
                    pwl['code'] = ''
                    pwl['l'] = (w - jtvalue - glvalue1)
                    pwl['w']= t
                    pcolorclass = GetSlidingColorClass(u'门板', pnl[u'类型'], pnl[u'颜色'])
                    if (pcolorclass):
                        pwl['code'] = pwl['code']+pcolorclass['wlcode']
                    pwl['direct'] = pnl[u'纹路']
                    pwl['num'] = 1
                    pwl['group'] = 2
                    pwl['bomsize'] = pssexp['size']
                    pwl['door_index'] = i+1
                    pwl['pnl_num'] = len(door['panellist'])
                    pwl['pnl_index'] = j
                    if ( pnltype ):

                        pwl['h'] = pnltype['tHick']
                        pwl['memo'] = pnltype['memo']
                        pwl['memo2'] = pnltype['memo2']
                        pwl['memo3'] = pnltype['memo3']
                        pwl['bdfile'] = pnltype['bdfile']


                    pwl['myunit'] = u'块'
                    ALLlist.append(pwl)
                    #print '15=',len(ALLlist)
                    if ( (pnltype ) and (pnltype['slaVe'] != '' and (not nHasMzhb))):
                        pwl2 = NewWLData()
                        pwl2 = copy.deepcopy(pwl)
                        pwl['name'] = pwl['name'].replace(pnltype['slaVe'], '')
                        pwl2['code'] = pwl['code'] + '+'
                        pwl2['name'] = pnltype['slaVe']
                        pwl2['color'] = pnltype['slaVe']
                        pwl2['memo'] = pnltype['memo']
                        ALLlist.append(pwl2)
                        #print '16=', len(ALLlist)
                    if ( pnltype['slaVe2'] != '' ):

                        pwl2 = NewWLData()
                        pwl2 = copy.deepcopy(pwl)
                        pwl2['code'] = pwl['code'] + '+'
                        pwl2['name'] = pnltype['slaVe2']
                        pwl2['color'] = pnltype['slaVe2']
                        pwl2['memo'] = pnltype['memo']
                        ALLlist.append(pwl2)
                        #print '17=', len(ALLlist)
                else:
                    pwl = NewWLData()
                    pwl['name'] = pnl[u'类型'] #// '门板';
                    pwl['color'] = pnl[u'颜色']
                    pwl['memo'] = pnl[u'备注']
                    pwl['code'] = ''
                    pwl['l'] = (w - jtvalue - glvalue1)
                    pwl['w'] = float(pssexp['height'])
                    pcolorclass = GetSlidingColorClass(u'门板', pnl[u'类型'], pnl[u'颜色'])
                    if (pcolorclass):
                        pwl['code'] = pwl['code'] + pcolorclass['wlcode']
                    pwl['direct'] = pnl[u'纹路']
                    pwl['bomsize'] = pssexp['size']
                    pwl['num'] = 1
                    pwl['group'] = 2
                    pwl['door_index'] = i + 1
                    pwl['pnl_num'] = len(door['panellist'])
                    pwl['pnl_index'] = j
                    if (pnltype):

                        pwl['h'] = pnltype['tHick']
                        pwl['memo'] = pnltype['memo']
                        pwl['memo2'] = pnltype['memo2']
                        pwl['memo3'] = pnltype['memo3']
                        pwl['bdfile'] = pnltype['bdfile']

                    pwl['myunit'] = u'块'
                    ALLlist.append(pwl)
                    #print '18=', len(ALLlist)
                    if ((pnltype) and (pnltype['slaVe'] != '' and (not nHasMzhb))):

                        pwl2 = NewWLData()
                        pwl2 = copy.deepcopy(pwl)
                        pwl['name'] = pwl['name'].replace(pnltype['slaVe'], '')
                        pwl2['code'] = pwl['code'] + '+'
                        pwl2['name'] = pnltype['slaVe']
                        pwl2['color'] = pnltype['slaVe']
                        pwl2['memo'] = pnltype['memo']
                        ALLlist.append(pwl2)
                        #print '19=', len(ALLlist)
                        if (pnltype['slaVe2'] != ''):

                            pwl2 = NewWLData()
                            pwl2 = copy.deepcopy(pwl)
                            pwl2['code'] = pwl['code'] + '+'
                            pwl2['name'] = pnltype['slaVe2']
                            pwl2['color'] = pnltype['slaVe2']
                            pwl2['memo'] = pnltype['memo']
                            ALLlist.append(pwl2)
                            #print '20=', len(ALLlist)
        elif (pssexp['width'] != 0):
            n = (w - jtvalue - glvalue1) / float(pssexp['width'])
            n = int(n)  # // GetFixed(n, 0) #// 直接舍弃取整
            t = (w - jtvalue - glvalue1) - float(pssexp['width']) * n
            if (t > float(pssexp['minwidth'])):

                n = n + 1
            else:
                t = 0
            for k in range(0, n):

                if ((k == n - 1) and (t != 0)):

                    pwl = NewWLData()
                    pwl['name'] = pnl[u'类型']  # // '门板';
                    pwl['color'] = pnl[u'颜色']
                    pwl['memo'] = pnl[u'备注']
                    pwl['code'] = ''
                    pwl['l'] = (h - jtvalue - glvalue2)
                    pwl['w'] = t
                    pcolorclass = GetSlidingColorClass(u'门板', pnl[u'类型'], pnl[u'颜色'])
                    if (pcolorclass):
                        pwl['code'] = pwl['code'] + pcolorclass['wlcode']
                    pwl['direct'] = pnl[u'纹路']
                    pwl['num'] = 1
                    pwl['group'] = 2
                    pwl['bomsize'] = pssexp['size']
                    pwl['door_index'] = i + 1
                    pwl['pnl_num'] = len(door['panellist'])
                    pwl['pnl_index'] = j
                    if (pnltype):
                        pwl['h'] = pnltype['tHick']
                        pwl['memo'] = pnltype['memo']
                        pwl['memo2'] = pnltype['memo2']
                        pwl['memo3'] = pnltype['memo3']
                        pwl['bdfile'] = pnltype['bdfile']

                    pwl['myunit'] = u'块'
                    ALLlist.append(pwl)
                    #print '21=', len(ALLlist)
                    if ((pnltype) and (pnltype['slaVe'] != '' and (not nHasMzhb))):
                        pwl2 = NewWLData()
                        pwl2 = copy.deepcopy(pwl)
                        pwl['name'] = pwl['name'].replace(pnltype['slaVe'], '')
                        pwl2['code'] = pwl['code'] + '+'
                        pwl2['name'] = pnltype['slaVe']
                        pwl2['color'] = pnltype['slaVe']
                        pwl2['memo'] = pnltype['memo']
                        ALLlist.append(pwl2)
                        #print '22=', len(ALLlist)
                        if (pnltype['slaVe2'] != ''):
                            pwl2 = NewWLData()
                            pwl2 = copy.deepcopy(pwl)
                            pwl2['code'] = pwl['code'] + '+'
                            pwl2['name'] = pnltype['slaVe2']
                            pwl2['color'] = pnltype['slaVe2']
                            pwl2['memo'] = pnltype['memo']
                            ALLlist.append(pwl2)
                            #print '23=', len(ALLlist)
                else:
                    pwl = NewWLData()
                    pwl['name'] = pnl[u'类型']  # // '门板';
                    pwl['color'] = pnl[u'颜色']
                    pwl['memo'] = pnl[u'备注']
                    pwl['code'] = ''
                    pwl['l'] = (w - jtvalue - glvalue1)
                    pwl['w'] = float(pssexp['width'])
                    pcolorclass = GetSlidingColorClass(u'门板', pnl[u'类型'], pnl[u'颜色'])
                    if (pcolorclass):
                        pwl['code'] = pwl['code'] + pcolorclass['wlcode']
                    pwl['direct'] = pnl[u'纹路']
                    pwl['bomsize'] = pssexp['size']
                    pwl['num'] = 1
                    pwl['group'] = 2
                    pwl['door_index'] = i + 1
                    pwl['pnl_num'] = len(door['panellist'])
                    pwl['pnl_index'] = j
                    if (pnltype):

                        pwl['h'] = pnltype['tHick']
                        pwl['memo'] = pnltype['memo']
                        pwl['memo2'] = pnltype['memo2']
                        pwl['memo3'] = pnltype['memo3']
                        pwl['bdfile'] = pnltype['bdfile']

                    pwl['myunit'] = u'块'
                    ALLlist.append(pwl)
                    #print '24=', len(ALLlist)
                    if ((pnltype) and (pnltype['slaVe'] != '' and (not nHasMzhb))):

                        pwl2 = NewWLData()
                        pwl2 = copy.deepcopy(pwl)
                        pwl['name'] = pwl['name'].replace(pnltype['slaVe'], '')
                        pwl2['code'] = pwl['code'] + '+'
                        pwl2['name'] = pnltype['slaVe']
                        pwl2['color'] = pnltype['slaVe']
                        pwl2['memo'] = pnltype['memo']
                        ALLlist.append(pwl2)
                        #print '25=', len(ALLlist)
                        if (pnltype.slaVe2 != ''):
                            pwl2 = NewWLData()
                            pwl2 = copy.deepcopy(pwl)
                            pwl2['code'] = pwl['code'] + '+'
                            pwl2['name'] = pnltype['slaVe2']
                            pwl2['color'] = pnltype['slaVe2']
                            pwl2['memo'] = pnltype['memo']
                            ALLlist.append(pwl2)
                            #print '26=', len(ALLlist)

    if (not ((not isglass) and (isbaiye))) : #// 玻璃 or 木板     非百叶

        pwl = NewWLData()
        pwl['name'] = pnl[u'类型'] #// '门板';
        pwl['color'] = pnl[u'颜色']
        pwl['memo'] = pnl[u'备注']
        pwl['code'] = ''
        #print u'纹路=',pnl[u'纹路']
        #print 'w1=',pnl['w1'],'h1=',pnl['h1'],'jtvalue=',jtvalue,'glvalue1=',glvalue1,'w1=',w1
        if (pnl[u'纹路'] == u'横纹'):
            #print type(w1)
            pwl['l'] = (float(pnl['w1']) - jtvalue - glvalue1) - w1
            pwl['w'] = (float(pnl['h1']) - jtvalue - glvalue2) - h1
        else:
            #print type(jtvalue)
            pwl['w'] = (float(pnl['w1']) - jtvalue - glvalue1) - w1
            pwl['l'] = (float(pnl['h1']) - jtvalue - glvalue2) - h1

        pcolorclass = GetSlidingColorClass(u'门板', pnl[u'类型'], pnl[u'颜色'])
        if ( pcolorclass ):
            pwl['code'] = pwl['code']+pcolorclass['wlcode']
        pwl['direct'] = pnl[u'纹路']
        pwl['num'] = 1
        pwl['group'] = 2
        pwl['door_index'] = i+1
        pwl['pnl_num'] = len(door['panellist'])
        pwl['pnl_index'] = j

        if ( pnltype ):

            pwl['h'] = pnltype['thick']
            pwl['memo'] = pnltype['memo']
            pwl['memo2'] = pnltype['memo2']
            pwl['memo3'] = pnltype['memo3']
            pwl['bdfile'] = pnltype['bdfile']

        if ( isglass ) :
            pwl['isglass'] = 1
        pwl['myunit'] = u'块'
        #print 'l=',pwl['l']
        #print 'w=', pwl['w']
        ALLlist.append(pwl)
        #print '5.5555555513=', len(ALLlist)
        if ( (pnltype ) and (pnltype['slaVe'] != '' and (not nHasMzhb)) ):


            pwl2 = NewWLData()
            pwl2 = copy.deepcopy(pwl)
            pwl['name'] = pwl['name'].replace(pnltype['slaVe'], '')
            pwl2['code'] = pwl['code'] + '+'
            pwl2['name'] = pnltype['slaVe']
            pwl2['color'] = pnltype['slaVe']
            pwl2['memo'] = pnltype['memo']
            ALLlist.append(pwl2)
            #print '28=', len(ALLlist)
            if ( pnltype['slaVe2'] != '' ):

                pwl2 = NewWLData()
                pwl2 = copy.deepcopy(pwl)
                pwl2['code'] = pwl['code'] + '+'
                pwl2['name'] = pnltype['slaVe2']
                pwl2['color'] = pnltype['slaVe2']
                pwl2['memo'] = pnltype['memo']
                ALLlist.append(pwl2)
                #print '29=', len(ALLlist)

        #// 添加门板的关联五金
        if ((pnltype ) and (pnltype['wjname'] != '') and (not (nHasMzhb)) ):# // 没门转换表时的逻辑

            for m in range(0, len(mSlidingWjBomDetailList)):
                pbomdetail = mSlidingWjBomDetailList[m]
                if ( pbomdetail['bomname'] == pnltype['wjname']):

                    pwl = NewWLData()
                    pwl['name'] = pbomdetail['name']
                    pwl['l'] = SAndDoorSetSubject(pbomdetail['l'], mExp)
                    pwl['w'] = SAndDoorSetSubject(pbomdetail['d'], mExp)
                    pwl['num'] = SAndDoorSetSubject(pbomdetail['num'], mExp)
                    pa = GetAccessory(pwl['name'])
                    pwl['group'] = 3
                    pwl['door_index'] = i + 1
                    pwl['pnl_num'] = len(door['panellist'])
                    pwl['pnl_index'] = j
                    if (pa != {}):

                        pwl['memo'] = pa['memo']
                        pwl['memo2'] = pa['memo2']
                        pwl['memo3'] = pa['memo3']
                        pwl['bdfile'] = pa['bdfile']
                        pwl['color'] = ToColor(pa['color'], skcolor1, skcolor2, skcolor3, skcolor4)
                        pwl['code'] = pa['wlcode']
                        pwl['myunit'] = pa['unit']
                        if (pa['isglass']):
                            pwl['isglass'] = 1
                        else:
                            pwl['isglass'] = 0
                        pcolorclass = GetSlidingColorClass(u'配件', pwl['color'])
                        if (pcolorclass != {}):
                            pwl['code'] = pwl['code'] + '' + pcolorclass['wlcode']
                        if (pa['myclass'] == u'型材'): pwl['group'] = 1
                        if (pa['myclass'] == u'门板'):
                            pwl['group'] = 2
                            pwl['color'] = pnl[u'颜色']
                    ALLlist.append(pwl)
                    #print '30=', len(ALLlist)
    # // 添加门板的关联五金
    if ((pnltype) and (pnltype['wjname'] != '') and (not nHasMzhb)):  # // 有门转换表时的逻辑

        for m in range(0, len(mSlidingWjBomDetailList)):

            pbomdetail = mSlidingWjBomDetailList[m]
            if (pbomdetail['bomname'] == pnltype['wjname']):

                pwl = NewWLData()
                pwl['name'] = pbomdetail['name']
                pwl['l'] = SAndDoorSetSubject(pbomdetail['l'], mExp)
                pwl['w'] = SAndDoorSetSubject(pbomdetail['d'], mExp)
                pwl['num'] = SAndDoorSetSubject(pbomdetail['num'], mExp)
                pa = GetAccessory(pwl['name'])
                pwl['group'] = 3
                pwl['door_index'] = i + 1
                pwl['pnl_num'] = len(door['panellist'])
                pwl['pnl_index'] = j
                if (pa != {}):

                    pwl['memo'] = pa['memo']
                    pwl['memo2'] = pa['memo2']
                    pwl['memo3'] = pa['memo3']
                    pwl['bdfile'] = pa['bdfile']
                    pwl['color'] = ToColor(pa['color'], skcolor1, skcolor2, skcolor3, skcolor4)
                    pwl['code'] = pa['wlcode']
                    pwl['myunit'] = pa['unit']
                    if (pa['isglass']):
                        pwl['isglass'] = 1
                    else:
                        pwl['isglass'] = 0
                    pcolorclass = GetSlidingColorClass(u'配件', pwl['color'])
                    if (pcolorclass != {}):
                        pwl['code'] = pwl['code'] + '' + pcolorclass['wlcode']
                    if (pa['myclass'] == u'型材'): pwl['group'] = 1
                    if (pa['myclass'] == u'门板'):
                        pwl['group'] = 2
                        pwl['color'] = pnl[u'颜色']
                ALLlist.append(pwl)
                #print '31=', len(ALLlist)

def GetSSExp(name):
    Result = {}
    for i in range(0, len(mSSExpList)):

        if(mSSExpList[i]['paneltype'] == name):
            Result = mSSExpList[i]
    return Result


def GetPanelType(bktype,name):

    vlist = aTablevalue[u"门板类型.cfg"]
    for ii in range(len(vlist)):

        if(vlist[ii]['name'] == name and vlist[ii]['bktype'] == bktype ):
            return vlist[ii]



#// 计算门芯的 插件进值， 用来计算 见光参数。
def ResetSubMxSize(mGrid,PanelIndex,fg,subfg,FGObj,Jsonvar,mUDBoxParam,mVBoxParam):
    outData= {'cw0':0,'ch0':0}
    if(mUDBoxParam=='' or mVBoxParam==''):
        return outData
    def GetSheetOject2(name ,bktype,listtype):

        for i in range(0, len(listtype)):

            if(name == listtype[i]['name'] and listtype[i][u'边框类型'] ):

                sarrs = listtype[i][u'边框类型'].split(',')
                for k in sarrs:

                    if(sarrs[k] == bktype):return listtype[i]

        return None

    # 子分格一定是竖分格
    nIndex = 0
    nSubIndex = 0
    ss1 = ''
    subss1 = ''
    ss1 = FGObj['CurcfgObj'][u'门芯列表2'][fg][u'名称']
    subss1 = FGObj['CurcfgObj'][u'门芯列表2'][fg]['subtobj']['CurcfgObj'][u'门芯列表2'][subfg][u'名称']
    nIndex = ss1[len(ss1)-1:] * 1
    nSubIndex = subss1[len(subss1)-1:] * 1

    hbox = FGObj['cSBoxp']
    hsubbox = FGObj['CurcfgObj'][u'门芯列表2'][fg]['subtobj']['cSBoxp']
    #// 上横插槽值

    U1 = mUDBoxParam['upboxheight'] - mUDBoxParam['upboxthick']

    D1 = mUDBoxParam['downboxheight'] - mUDBoxParam['downboxthick']

    M1 = (hbox['height'] - hbox['thick']) / 2

    SM1 = (hsubbox['height'] - hsubbox['thick']) / 2

    S1 = mVBoxParam['height'] - mVBoxParam['thick']

    ch0 = 0

    cw0 = 0
    if (FGObj['CurcfgObj']['direc'] == 1):#// 外层是横分格
        tmp =  SM1
        SM1 = M1
        M1 =  tmp


    if (mGrid == 0):   # // 0 单分格

    #// 最上格的时候减量为上横插槽值和横中横插槽值
        if (Jsonvar['nType'] == 2):

            if (nIndex == 1):
                ch0 = D1 + SM1
            else: ch0 = U1 + SM1

        elif (Jsonvar.nType == 3):

            if (nIndex == 1):    ch0= D1+ SM1
            elif (nIndex == 2):    ch0= SM1 + SM1
            else: ch0=  U1+ SM1

        elif (Jsonvar['nType'] == 4):

            if (nIndex == 1):    ch0= D1+ SM1
            elif (nIndex == 2 or nIndex == 3):    ch0= SM1 + SM1;
            else: ch0= U1+ SM1


    else:  # // 两均分 // 三均分 // 四均分 // 五均分

        if (PanelIndex == 0 and nIndex == 1):
            ch0 = D1 + SM1
        elif (PanelIndex == mGrid and nIndex == Jsonvar['nType']): ch0= U1+ SM1
        else: ch0= SM1 + SM1

    if (nSubIndex == 1 or nSubIndex == Jsonvar['nType']): cw0 = S1 + M1 #// 第一个竖列，或者最后一竖列都是 竖框 +一个中横框减量
    else: cw0 = M1 + M1

    outData['cw0'] = cw0
    outData['ch0'] = ch0
    return outData

# 计算门芯的 插件进值， 用来计算 见光参数。
def ResetMxSize(mGrid,PanelIndex,fg,FGObj,Jsonvar,mUDBoxParam,mVBoxParam):
    outData = {'cw0': 0, 'ch0': 0}
    if (mUDBoxParam == '' or mVBoxParam == ''):
        return outData

    def GetSheetOject2(name, bktype, listtype):

        for i in range(0, len(listtype)):

            if (name == listtype[i]['name'] and listtype[i][u'边框类型']):

                sarrs = listtype[i][u'边框类型'].split(',')
                for k in sarrs:

                    if (sarrs[k] == bktype): return listtype[i]

        return None

    # 子分格一定是竖分格
    nIndex = 0
    nSubIndex = 0
    ss1 = ''
    subss1 = ''
    ss1 = FGObj['CurcfgObj'][u'门芯列表2'][fg][u'名称']

    nIndex = ss1[len(ss1) - 1:] * 1

    hbox = FGObj['cSBoxp']

    # // 上横插槽值

    U1 = float(mUDBoxParam['upboxheight']) - float(mUDBoxParam['upboxthick'])

    D1 = float(mUDBoxParam['downboxheight']) - float(mUDBoxParam['downboxthick'])

    M1 = (float(hbox['height']) - float(hbox['thick'])) / 2

    S1 = float(mVBoxParam['height']) - float(mVBoxParam['thick'])

    ch0 = 0
    cw0 = 0

    if (FGObj['CurcfgObj']['direc'] == 1):  # // 当前横分格
        if (PanelIndex == 0 and nIndex == 1):
            ch0 = D1 + M1
        elif (PanelIndex == mGrid and nIndex == Jsonvar['nType']): ch0= U1+ M1
        else: ch0= M1 + M1
        cw0 = S1 * 2
    else:
        if (mGrid == 0):  # // 0 单分格

            ch0 = D1 + U1


        else:  # // 两均分 // 三均分 // 四均分 // 五均分

            if (PanelIndex == 0 and nIndex == 1):
                ch0 = D1 + M1
            elif (PanelIndex == mGrid and nIndex == Jsonvar['nType']):
                ch0 = U1 + M1
            else:
                ch0 = M1 + M1

        if (nIndex == 1 or nIndex == Jsonvar['nType']):
            cw0 = S1 + M1  # // 第一个竖列，或者最后一竖列都是 竖框 +一个中横框减量
        else:
            cw0 = M1 + M1
    outData['cw0'] = cw0
    outData['ch0'] = ch0
    return outData


#获取中横减量 横中横，竖中横，和斜中横等
def ResetMBoxSize(mGrid,PanelIndex,fg,subfg,FGObj,Jsonvar,mUDBoxParam,mVBoxParam):

    outData = {'cw0': 0, 'ch0': 0}
    if (mUDBoxParam == '' or mVBoxParam == ''):
        return 0

    def GetSheetOject2(name, bktype, listtype):

        for i in range(0, len(listtype)):

            if (name == listtype[i]['name'] and listtype[i][u'边框类型']):

                sarrs = listtype[i][u'边框类型'].split(',')
                for k in sarrs:

                    if (sarrs[k] == bktype): return listtype[i]

        return None

    # 子分格一定是竖分格
    nIndex = 0
    nSubIndex = 0
    ss1 = ''
    subss1 = ''
    ss1 = FGObj['CurcfgObj'][u'门芯列表2'][fg][u'名称']

    nIndex = ss1[len(ss1) - 1:] * 1


    hbox = FGObj['cSBoxp']

    # // 上横插槽值

    U1 = mUDBoxParam['upboxheight'] - mUDBoxParam['upboxthick']

    D1 = mUDBoxParam['downboxheight'] - mUDBoxParam['downboxthick']

    M1 = (hbox['height'] - hbox['thick']) / 2


    S1 = mVBoxParam['height'] - mVBoxParam['thick']

    if (FGObj['CurcfgObj']['direc'] == 1):  # // 外层是横分格


        if (mGrid == 0):  # // 0 单分格

            # // 最上格的时候减量为上横插槽值和横中横插槽值
            if (Jsonvar['nType'] == 2):

                if (nIndex == 1):
                    return D1 + M1
                else:
                    return U1 + M1

            elif (Jsonvar.nType == 3):

                if (nIndex == 1):
                    return D1 + M1
                elif (nIndex == 2):
                    return M1 + M1
                else:
                    return U1 + M1

            elif (Jsonvar['nType'] == 4):

                if (nIndex == 1):
                    return D1 + M1
                elif (nIndex == 2 or nIndex == 3):
                    return M1 + M1
                else:
                    return U1 + M1


        else:  # // 两均分 // 三均分 // 四均分 // 五均分

            if (PanelIndex == 0 and nIndex == 1):
                return D1 + M1
            elif (PanelIndex == mGrid and nIndex == Jsonvar['nType']):
                return U1 + M1
            else:
                return M1 + M1
    else:
        if (nIndex == 1 ):
            return S1 + M1 # // 第一个竖列，或者最后一竖列都是 竖框 +一个中横框减量
        elif(nIndex == Jsonvar['nType']) : return S1 + M1
        else:
            return M1 + M1

    return 0



def addBox(rb,door,i,nType=False):

    pwl = NewWLData()
    pwl['name'] = rb[u'类型']
    pwl['color'] = rb[u'颜色']
    phbox = {}

    if (not nType):phbox = findName(rb[u'类型'],aTablevalue[u'中横框参数.cfg'])

    elif (nType == 1): phbox = findName(rb[u'类型'], aTablevalue[u'竖中横框参数.cfg'])
    elif (nType == 2): phbox = findName(rb[u'类型'], aTablevalue[u'横中横框参数.cfg'])
    else:
        pass

    if ( phbox ):

        pwl['memo'] = phbox['memo']
        pwl['bdfile'] = phbox['bdfile']
        pwl['code'] = phbox['wlcode']
        pwl['w'] = 0
        pwl['h'] = 0
        pwl['bomsize'] = phbox['size']

        pcolorclass = GetSlidingColorClass(u'中横框', phbox['name'], pwl['color'])
        if ( pcolorclass!={}): pwl['code'] = pwl['code']+pcolorclass['wlcode']



        pwl['num'] = 1
        pwl['l'] = (door['doorw'] - float(door['mVBoxParam']['height']) * 2)

        # print json.dumps(mSlidingParam,ensure_ascii=False),pwl['l'],nType
        # print json.dumps(phbox,ensure_ascii=False),phbox['ishboxvalue'],pwl['l'],nType

        if ( (phbox) and (phbox['ishboxvalue'] == 1) ):

            pwl['l'] = float(pwl['l']) + float(mSlidingParam['hboxvalue'])

        if (nType):

            pwl['l'] = rb['h0']
            #print json.dumps(rb,ensure_ascii=False)

            if ( (phbox != {}) and (phbox['ishboxvalue'] == 1) ):

                pwl['l'] = float(pwl['l']) + float(mSlidingParam['hboxvalue'])


        pwl['group'] = 1
        pwl['door_index'] = i+1
        pwl['myunit'] = u'根'

        ALLlist.append(pwl)
        #print '32',len(ALLlist),pwl['l']
        mExp[u'$中横框长度'] = pwl['l']
        if (phbox and phbox['wjname'] != '' ): #// 下横框五金
            for m in range(0, len(mSlidingWjBomDetailList)):

                pbomdetail = mSlidingWjBomDetailList[m]
                if ( pbomdetail['bomname'] == phbox['wjname']):

                    pwl = NewWLData()
                    pwl['name'] = pbomdetail['name']
                    pwl['l'] = SAndDoorSetSubject(pbomdetail['l'], mExp)
                    pwl['w'] = SAndDoorSetSubject(pbomdetail['d'], mExp)
                    pwl['num'] = SAndDoorSetSubject(pbomdetail['num'], mExp)
                    pa = GetAccessory(pwl['name'])
                    pwl['group'] = 3
                    pwl['door_index'] = i + 1
                    if (pa != {}):

                        pwl['memo'] = pa['memo']
                        pwl['memo2'] = pa['memo2']
                        pwl['memo3'] = pa['memo3']
                        pwl['bdfile'] = pa['bdfile']
                        pwl['color'] = ToColor(pa['color'], skcolor1, skcolor2, skcolor3, skcolor4)
                        pwl['code'] = pa['wlcode']
                        pwl['myunit'] = pa['unit']
                        if (pa['isglass']):
                            pwl['isglass'] = 1
                        else:
                            pwl['isglass'] = 0
                        pcolorclass = GetSlidingColorClass(u'配件', pa['name'], pwl['color'])
                        if (pcolorclass != {}):
                            pwl['code'] = pwl['code'] + '' + pcolorclass['wlcode']
                        if (pa['myclass'] == u'型材'): pwl['group'] = 1
                        if (pa['myclass'] == u'门板'): pwl['group'] = 2

                    ALLlist.append(pwl)
                    #print '33=', len(ALLlist)

def sSort(HCfgobj):
    for i in range(0, len(HCfgobj)):

        slist = HCfgobj[i][u'门芯列表']

        nList = []
        if (len(slist) == 3): nList =[u'门芯1', u'竖中横1', u'门芯2']
        if (len(slist) == 5): nList =[u'门芯1', u'竖中横1', u'门芯2', u'竖中横2', u'门芯3'];
        if (len(slist) == 7): nList =[u'门芯1', u'竖中横1', u'门芯2', u'竖中横2', u'门芯3', u'竖中横3', u'门芯4']
        for j in range(0, len(nList)):

            for k in range(0, len(slist)):

                if (nList[j] == slist[k][u'名称']):

                    nList[j] = slist[k]
                    break
        HCfgobj[i][u'门芯列表'] = nList

Sliding = {
    'Sfg_Param':{'HTxml':u'<产品 名称="横2格门" 类别="" 摆放方式="整块;左右延伸:-1;'
                         u'前后延伸:-1;上下延伸:-1;尺寸限制:1,1220,1,1220,1,2430;'
                         u'" 装饰类别="趟门" 材料="" 颜色="" HoleFlag="0" Flag32="0" '
                         u'ErrorFlag="0" ActFlag="0" LgwjFlag="0"><摆放规则列表/><变量列表>'
                         u'</变量列表><我的模块><板件 名称="门芯1" X="0" Y="$门芯1前偏移" '
                         u'Z="0" 宽="$门芯1宽度" 深="$门芯1厚度" 高="H" 类别="" '
                         u'基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="1" '
                         u'HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" '
                         u'OZ="" 图形参数="" guid="1"/><板件 名称="竖中横1" X="$门芯1宽度-$竖中横进槽" '
                         u'Y="0" Z="0" 宽="L" 深="$竖中横厚度" 高="$竖中横宽度" 类别="" '
                         u'基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" '
                         u'Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="2"/>'
                         u'<板件 名称="门芯2" X="$门芯1宽度+$竖中横宽度-2*$竖中横进槽" Y="$门芯2前偏移" '
                         u'Z="0" 宽="L-$门芯1宽度-$竖中横宽度+2*$竖中横进槽" 深="$门芯2厚度" 高="H" '
                         u'类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="1" HoleFlag="0" '
                         u'Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="3"/></我的模块>'
                         u'<我的规格><规格 名称="竖2格门" 宽="800" 深="20" 高="1000"/></我的规格></产品>',
                 'Txml':u'<产品 名称="竖2格门" 类别="" 摆放方式="整块;左右延伸:-1;前后延伸:-1;'
                        u'上下延伸:-1;尺寸限制:1,1220,1,1220,1,2430;" 装饰类别="趟门" 材料="" '
                        u'颜色="" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" '
                        u'LgwjFlag="0"><摆放规则列表/><变量列表></变量列表><我的模块>'
                        u'<板件 名称="门芯1" X="0" Y="$门芯1前偏移" Z="0" 宽="$门芯1宽度" '
                        u'深="$门芯1厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" '
                        u'MATID="" DI="1" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" '
                        u'OZ="" 图形参数="" guid="1"/><板件 名称="竖中横1" X="$门芯1宽度-$竖中横进槽" Y="0" Z="0" '
                        u'宽="$竖中横宽度" 深="$竖中横宽度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" '
                        u'MATID="" DI="1" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" '
                        u'guid="2"/><板件 名称="门芯2" X="$门芯1宽度+$竖中横宽度-2*$竖中横进槽" Y="$门芯2前偏移" '
                        u'Z="0" 宽="L-$门芯1宽度-$竖中横宽度+2*$竖中横进槽" 深="$门芯2厚度" 高="H" 类别="" '
                        u'基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="1" HoleFlag="0" Flag32="0" '
                        u'ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="3"/></我的模块><我的规格><规格 '
                        u'名称="竖2格门" 宽="800" 深="20" 高="1000"/></我的规格></产品>',
                 'Sxml':u'<产品 名称="竖3格门_两边均分" 类别="" 摆放方式="整块;左右延伸:-1;前后延伸:-1;上下延伸:-1;尺寸限制:1,1220,1,1220,1,2430;" 装饰类别="趟门" 材料="" 颜色="" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" LgwjFlag="0"><摆放规则列表/><变量列表></变量列表><我的模块><板件 名称="门芯1" X="0" Y="$门芯1前偏移" Z="0" 宽="(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2" 深="$门芯1厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="1" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="1"/><板件 名称="竖中横1" X="(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2-$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="1" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="2"/><板件 名称="门芯2" X="(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2+$竖中横宽度-2*$竖中横进槽" Y="$门芯2前偏移" Z="0" 宽="$门芯2宽度" 深="$门芯2厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="3"/><板件 名称="竖中横2" X="L-(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2-$竖中横宽度+$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="1" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="4"/><板件 名称="门芯3" X="L-(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2" Y="$门芯3前偏移" Z="0" 宽="(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2" 深="$门芯3厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="1" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="5"/></我的模块><我的规格><规格 名称="竖3格门" 宽="800" 深="20" 高="1000"/></我的规格></产品>',
                 'Fxml':u'<产品 名称="竖4格门_改123" 类别="" 摆放方式="整块;左右延伸:-1;前后延伸:-1;上下延伸:-1;尺寸限制:1,1220,1,1220,1,2430;" 装饰类别="趟门" 材料="" 颜色="" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" LgwjFlag="0"><摆放规则列表/><变量列表></变量列表><我的模块><板件 名称="门芯1" X="0" Y="$门芯1前偏移" Z="0" 宽="$门芯1宽度" 深="$门芯1厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="1"/><板件 名称="竖中横1" X="$门芯1宽度-$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="4" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="2"/><板件 名称="门芯2" X="$门芯1宽度+$竖中横宽度-2*$竖中横进槽" Y="$门芯2前偏移" Z="0" 宽="$门芯2宽度" 深="$门芯2厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="3"/><板件 名称="竖中横2" X="$门芯1宽度+$门芯2宽度+$竖中横宽度-3*$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="4" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="4"/><板件 名称="门芯3" X="$门芯1宽度+$门芯2宽度+2*$竖中横宽度-4*$竖中横进槽" Y="$门芯3前偏移" Z="0" 宽="$门芯3宽度" 深="$门芯3厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="5"/><板件 名称="竖中横3" X="$门芯1宽度+$门芯2宽度+$门芯3宽度+2*$竖中横宽度-5*$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="4" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="6"/><板件 名称="门芯4" X="L-(L-$门芯1宽度-$门芯2宽度-$门芯3宽度-3*$竖中横宽度+6*$竖中横进槽)" Y="$门芯4前偏移" Z="0" 宽="L-$门芯1宽度-$门芯2宽度-$门芯3宽度-3*$竖中横宽度+6*$竖中横进槽" 深="$门芯4厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="7"/></我的模块><我的规格><规格 名称="竖3格门" 宽="900" 深="20" 高="1000"/></我的规格></产品>',
                 'HSxml':u'<产品 名称="横3格门_两边均分" 类别="" 摆放方式="整块;左右延伸:-1;前后延伸:-1;上下延伸:-1;尺寸限制:1,1220,1,1220,1,2430;" 装饰类别="趟门" 材料="" 颜色="" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" LgwjFlag="0"><摆放规则列表/><变量列表></变量列表><我的模块><板件 名称="门芯1" X="0" Y="$门芯1前偏移" Z="0" 宽="(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2" 深="$门芯1厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="1" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="1"/><板件 名称="竖中横1" X="(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2-$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="2"/><板件 名称="门芯2" X="(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2+$竖中横宽度-2*$竖中横进槽" Y="$门芯2前偏移" Z="0" 宽="$门芯2宽度" 深="$门芯2厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="3"/><板件 名称="竖中横2" X="L-(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2-$竖中横宽度+$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="4"/><板件 名称="门芯3" X="L-(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2" Y="$门芯3前偏移" Z="0" 宽="(L-$门芯2宽度-2*$竖中横宽度+4*$竖中横进槽)/2" 深="$门芯3厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="1" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="5"/></我的模块><我的规格><规格 名称="竖3格门" 宽="800" 深="20" 高="1000"/></我的规格></产品>',
                 'HFxml':u'<产品 名称="横4格门_改123" 类别="" 摆放方式="整块;左右延伸:-1;前后延伸:-1;上下延伸:-1;尺寸限制:1,1220,1,1220,1,2430;" 装饰类别="趟门" 材料="" 颜色="" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" LgwjFlag="0"><摆放规则列表/><变量列表></变量列表><我的模块><板件 名称="门芯1" X="0" Y="$门芯1前偏移" Z="0" 宽="$门芯1宽度" 深="$门芯1厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="1"/><板件 名称="竖中横1" X="$门芯1宽度-$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="2"/><板件 名称="门芯2" X="$门芯1宽度+$竖中横宽度-2*$竖中横进槽" Y="$门芯2前偏移" Z="0" 宽="$门芯2宽度" 深="$门芯2厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="3"/><板件 名称="竖中横2" X="$门芯1宽度+$门芯2宽度+$竖中横宽度-3*$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="4"/><板件 名称="门芯3" X="$门芯1宽度+$门芯2宽度+2*$竖中横宽度-4*$竖中横进槽" Y="$门芯3前偏移" Z="0" 宽="$门芯3宽度" 深="$门芯3厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="5"/><板件 名称="竖中横3" X="$门芯1宽度+$门芯2宽度+$门芯3宽度+2*$竖中横宽度-5*$竖中横进槽" Y="0" Z="0" 宽="$竖中横宽度" 深="$竖中横厚度" 高="H" 类别="" 基础图形="BG_竖中横" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="6"/><板件 名称="门芯4" X="L-(L-$门芯1宽度-$门芯2宽度-$门芯3宽度-3*$竖中横宽度+6*$竖中横进槽)" Y="$门芯4前偏移" Z="0" 宽="L-$门芯1宽度-$门芯2宽度-$门芯3宽度-3*$竖中横宽度+6*$竖中横进槽" 深="$门芯4厚度" 高="H" 类别="" 基础图形="BG::RECT" 装饰类别="趟门" MATID="" DI="3" HoleFlag="0" Flag32="0" ErrorFlag="0" ActFlag="0" OZ="" 图形参数="" guid="7"/></我的模块><我的规格><规格 名称="竖3格门" 宽="900" 深="20" 高="1000"/></我的规格></产品>'
                 },
}

#'''该趟门有问题'''

xml1 = '''<趟门 门洞宽="1366" 门洞高="2062" 延长导轨="0" 单门数量类型="两门" 门类型="移门" 门颜色="" 均分="2" 边框类型="Q1N框门" 竖框颜色="286BH#米白樱桃" 上下横框类型="Q1上下横" 上横框颜色="286BH#米白樱桃" 下横框颜色="286BH#米白樱桃" 上下轨类型="常规无阻尼滑轮" 上轨颜色="286BH#米白樱桃" 下轨颜色="286BH#米白樱桃" 中横框类型="Q1-3AN中横" 中横框颜色="286BH#米白樱桃" 门板类型="XP-001中纤板(竖纹)" 门板颜色="286BH#米白樱桃" DataMode="0" Extra="">
                  <分格 面板高度="868" 材料="XP-001中纤板(竖纹)" 颜色="286BH#米白樱桃" 纹路="竖纹" 胶条位="" 备注="" 定格=""/>
                  <分格 面板高度="200" 材料="经典百叶(竖放)" 颜色="286BH#米白樱桃" 纹路="竖纹" 胶条位="" 备注="" 定格="1"/>
                  <分格 面板高度="868" 材料="XP-001中纤板(竖纹)" 颜色="286BH#米白樱桃" 纹路="竖纹" 胶条位="" 备注="" 定格=""/>
                  <单门 宽="701" 高="2017" X0="0.00" Y0="0" 竖框类型="Q1N" 竖框颜色="286BH#米白樱桃" 上下横框类型="Q1上下横" 上横框颜色="286BH#米白樱桃" 下横框颜色="286BH#米白樱桃">
                    <中横框 类型="Q1-3AN中横" 颜色="286BH#米白樱桃" vh="True" w0="617" h0="26" x0="42" y0="907.5" d0="14" w1="643" h1="10" x1="29" y1="915.5" d1="14" w2="683" h2="0" x2="0" y2="920.5" d2="14"/>
                    <中横框 类型="Q1-3AN中横" 颜色="286BH#米白樱桃" vh="True" w0="617" h0="26" x0="42" y0="1117.5" d0="14" w1="643" h1="10" x1="29" y1="1125.5" d1="14" w2="683" h2="0" x2="0" y2="1130.5" d2="14"/>
                    <门板 类型="XP-001中纤板(竖纹)" 颜色="286BH#米白樱桃" 颜色2="" 纹路="竖纹" 备注="" ExtraData="" w0="617" h0="851.5" x0="42" y0="56" d0="14" w1="643" h1="868" x1="29" y1="47.5" d1="14" w2="683" h2="935.5" x2="0" y2="0" d2="14"/>
                    <门板 类型="经典百叶(竖放)" 颜色="286BH#米白樱桃" 颜色2="" 纹路="竖纹" 备注="" ExtraData="" w0="617" h0="184" x0="42" y0="933.5" d0="14" w1="643" h1="200" x1="29" y1="925.5" d1="14" w2="683" h2="225" x2="0" y2="920.5" d2="14"/>
                    <门板 类型="XP-001中纤板(竖纹)" 颜色="286BH#米白樱桃" 颜色2="" 纹路="竖纹" 备注="" ExtraData="" w0="617" h0="851.5" x0="42" y0="1143.5" d0="14" w1="643" h1="868" x1="29" y1="1135.5" d1="14" w2="683" h2="901.5" x2="0" y2="1130.5" d2="14"/>
                  </单门>
                  <单门 宽="701" 高="2017" X0="665.00" Y0="0" 竖框类型="Q1N" 竖框颜色="286BH#米白樱桃" 上下横框类型="Q1上下横" 上横框颜色="286BH#米白樱桃" 下横框颜色="286BH#米白樱桃">
                    <中横框 类型="Q1-3AN中横" 颜色="286BH#米白樱桃" vh="True" w0="617" h0="26" x0="707" y0="907.5" d0="14" w1="643" h1="10" x1="694" y1="915.5" d1="14" w2="683" h2="0" x2="665" y2="920.5" d2="14"/>
                    <中横框 类型="Q1-3AN中横" 颜色="286BH#米白樱桃" vh="True" w0="617" h0="26" x0="707" y0="1117.5" d0="14" w1="643" h1="10" x1="694" y1="1125.5" d1="14" w2="683" h2="0" x2="665" y2="1130.5" d2="14"/>
                    <门板 类型="XP-001中纤板(竖纹)" 颜色="286BH#米白樱桃" 颜色2="" 纹路="竖纹" 备注="" ExtraData="" w0="617" h0="851.5" x0="707" y0="56" d0="14" w1="643" h1="868" x1="694" y1="47.5" d1="14" w2="683" h2="935.5" x2="665" y2="0" d2="14"/>
                    <门板 类型="经典百叶(竖放)" 颜色="286BH#米白樱桃" 颜色2="" 纹路="竖纹" 备注="" ExtraData="" w0="617" h0="184" x0="707" y0="933.5" d0="14" w1="643" h1="200" x1="694" y1="925.5" d1="14" w2="683" h2="225" x2="665" y2="920.5" d2="14"/>
                    <门板 类型="XP-001中纤板(竖纹)" 颜色="286BH#米白樱桃" 颜色2="" 纹路="竖纹" 备注="" ExtraData="" w0="617" h0="851.5" x0="707" y0="1143.5" d0="14" w1="643" h1="868" x1="694" y1="1135.5" d1="14" w2="683" h2="901.5" x2="665" y2="1130.5" d2="14"/>
                  </单门>
                </趟门>'''
l = 1366
h = 2062
base_dir = os.path.abspath(os.path.join(os.getcwd(),'..'))

#XmlTemplate2Json(xml1,l,h)


