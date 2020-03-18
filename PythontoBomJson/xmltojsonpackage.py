#  -*- coding:utf-8 -*-
'''
vesion 1.1.1
2019/11/21
author:litao
'''
import os,sys
from useful_tools import *
import numpy as np
import xml.etree.ElementTree as ET
import pypyodbc
import xml.dom.minidom
from xml.dom import minidom
from xmltojsontools import *
from ctypes import *
import configparser
import io
import copy
import urllib.request, urllib.parse, urllib.error
from VectorGeometry import *
import uuid
import hashlib
from ExpValue import GetExpValue
from SlidingAndDoor.funcGetSlidingJson import fun
from SlidingAndDoor.funcGetDoorJson import fungetdoorjson
from ReturnConfig.GetSlidingAndDoorConfig import CompileLuaProgram
import logging

log = logging.getLogger(base_dir+"\\Python\\Log\\all.log")
des2wuliaodict = {}
holeconfigHash = {}
childbomHash = {}
wjruleHash = {}
ruleHash = {}
kcconfigHash = {}
productdatadict = {}
bomstdList = []
childxml = {}
mTmpExp = {}
mProductList = []
bomlist = []
slidinglist = []
mXMLStringList = []
mDoorList = []
doorslist = []
desdoorlist = []
desslidinglist = []
mBDXMLList = {}
Ord2PObj = {
	'listStr':'',
	'qdutils':'',
	'BH':18,
	'nServer':1,
}
JsonPrice = {"柜体列表": []}
Jsondata = 	{
			"Space16mm": [],
	  	}
#报价
des2price = []
QuoruleHash = {}
classHash = {}
ptableList = []
CBIgnoreHoleInfoChecked = True
gFormatPrecision = 2
gFormatPrecision2 = 2
gQDBomFlag = 1
mPicWidth2 = 700
mPicHeight2 = 400

StanleyDict = {}
X2dToBdGraphj = 0
gBGHash = {}
gPluginsList = []
seqInfoHash = {}
classseqInfoHash = {}
workflowlist = []
gBoardMatList = []
gErpItemList = []
mIIHoleCalcRule = {}
mDoorPrecision = 0
gROC = None
mJoBarCode = {}
value_lsk = 0
value_rsk = 0
value_zk = 0
value_zs = 0
value_ls = 0
value_lg = 0
value_ltm = 0
value_rtm = 0
def GetWorkflowStr(workflow, bomstd, hole, workflowlist):
    Result = ''
    for i in range(0,len(workflowlist)):
        pwf = workflowlist[i]
        if (pwf.name == workflow) and ((pwf.bomstd == '*') or (pwf.bomstd == bomstd)) and (
            (pwf.hole == '*') or (pwf.hole == hole)) :
            Result = Result + '%d,%d,%d,%d'%(pwf.id, pwf.board_cut, pwf.edge_banding, pwf.punching)
    return Result
def GetXptlist(poi,xptlist_isxx, xptlist_jx, xptlist_pl,gBGHash):
    # gBGHash = InitBGHash()
    def_bgparam = '{^PL^:^0^,^Cut^:^0^,^DJ^:^0^,^JX^:^0^,^CutA^:^0.0000^,^CutB^:^0.0000^,^BarH^:^0.0000^,^Points^:^^}'
    xptlist_isxx= 0
    xptlist_jx= 0
    xptlist_pl= 1
    if 'bg' not in poi  or (poi['bg']) =='':
        return
    bgindex = poi['bg'].replace('::','_')
    ## bgindex.encode('gb2312'),type(bgindex)
    ## gBGHash.keys()
    # if bgindex in gBGHash.keys():#u'BG_RECT背板'
    #     # '9999999'
    #     # type(BGName(bgindex)),BGName(bgindex)
    ## gBGHash
    if bgindex.encode('gb2312') not in gBGHash:
        return
    xml = gBGHash[bgindex.encode('gb2312')]
    if xml=='' and (poi['bg']!='BG::RECT'):
        return
    if xml!='':
        root = ET.fromstring(xml)  # 解析那段xml
        paramstr=root.get('Param','')
        for i in range(0,len(root)):
            node=root[i]
            str_type = node.get('Type','')
            if (str_type=='Polygon') and (node.tag=='PlaneXY') :
                ## '888888'
                xptlist_pl=1
            if (str_type=='Polygon') and (node.tag=='PlaneXZ') :
                xptlist_pl=2
            if (str_type=='Polygon') and (node.tag=='PlaneYZ') :
                xptlist_pl=3
def GetWorldMatrix(p,m): #存在问题
    '''
    :param p:  bomlist的元素
    :param m:  TMyCalcItem对象的 TMatrix属性
    :return:
    '''
    global pm
    pm = np.matrix([[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]])
    def GetLocalMatrix():
        '''
        a=np.matrix('1 2 7;3 4 8;5 6 9')
        :return:  TMatrix
        '''
        rm=IdentityHmgMatrix
        ## 'p=',type(p)
        ## p['lx'],p['ly'],p['lz']
        tm=CreateTranslationMatrix([p['lx'],p['ly'],p['lz']])
        ## type(p['oz']),p['oz']
        if p['oz'] =='':
            oz = 0
        else:
            oz=float(p['oz'])
        if abs(oz) > 0.001:
            oz=-oz*pi/180
            rm = CreateRotationMatrixZ(oz)
        if p['vp']==1 :# // 俯视
            m= CreateRotationMatrixX(DegToRad(90))
            rm= MatrixMultiply(rm, m)
            m = CreateTranslationMatrix(VectorMake(0, p['gh'], 0))
            tm= MatrixMultiply(tm, m)
        if p['vp']==2 :# // 左侧(B面)
            m= CreateRotationMatrixZ(DegToRad(-90))
            rm= MatrixMultiply(rm, m)
            m= CreateTranslationMatrix(VectorMake(0, p['gl'], 0))
            tm= MatrixMultiply(tm, m)
        if p['vp']==3:#// 右侧(C面)
            m= CreateRotationMatrixZ(DegToRad(90))
            rm= MatrixMultiply(rm, m)
            m= CreateTranslationMatrix(VectorMake(p['gl'], 0, 0))
            tm= MatrixMultiply(tm, m)
        if p['vp']==4 :# // 仰视
            rm= CreateRotationMatrixX(DegToRad(-90))
            rm= MatrixMultiply(rm, m)
            m= CreateTranslationMatrix(VectorMake(0, 0, p['gh']))
            tm= MatrixMultiply(tm, m)
        if p['vp']==5 :# // 反向
            m= CreateRotationMatrixZ(DegToRad(180))
            rm= MatrixMultiply(rm, m)
            m= CreateTranslationMatrix(VectorMake(p['gl'], p['gp'], 0))
            tm= MatrixMultiply(tm, m)
            Result = MatrixMultiply(rm, tm)
        Result = MatrixMultiply(rm, tm)
        return Result
    #if p['lx'] == 373:
        ## '1m', m
    m=GetLocalMatrix()
    #if p['lx'] == 373:
        ## '2m', m
    if p['parent'] ==None:
        ## 'None'
        return m
    ## 'hahahhah'
    #if p['lx'] == 373:
        ## 'pm1=', pm
    pm = GetWorldMatrix(p['parent'],pm)
    #if p['lx'] == 373:
        ## 'pm2=',pm
    m=MatrixMultiply(m, pm)
    return m
def BomItem2CalcItem(p,Item2,workflowlist,mBDXMLList,gBGHash):
    item = p
    Result = Item2
    #if item['lx'] ==373:
        ## 'Item1=',Item2.m
    ## type(item)
    if type(item)=="<type 'str'>":
        ## 'hahhahaha'
        sys.exit(1)
    Item2.m =GetWorldMatrix(item, Item2.m)
    #if item['lx'] == 373:
        ## 'Item2=',Item2.m
    Item2.space = ''
    Item2.space_x = 0
    Item2.space_y = 0
    Item2.space_z = 0
    GetXptlist(item, Item2.isxx, Item2.xptlist_jx, Item2.xptlist_pl,gBGHash)
    if 'tmp_soz' not in item:
        item['tmp_soz'] = ''
    if item['tmp_soz']=='':
        Item2.sozflag=''
    else:
        Item2.sozflag=md5(item['tmp_soz'])
    #GetSpaceItem(item, )
    Item2.space = item['subspace']
    Item2.space_x = item['space_x']
    Item2.space_y = item['space_y']
    Item2.space_z = item['space_z']
    Item2.bl = item['bl']
    Item2.bp = item['bp']
    Item2.bh = item['bh']
    Item2.pl = item['pl']
    Item2.pd = item['pd']
    Item2.ph = item['ph']
    Item2.lx = item['lx']
    Item2.ly = item['ly']
    Item2.lz = item['lz']
    Item2.x = item['x']- Item2.space_x
    Item2.y = item['y']- Item2.space_y
    Item2.z = item['z'] - Item2.space_z
    Item2.space_id = item['space_id']
    Item2.l = item['l']
    Item2.p = item['p']
    Item2.h = item['h']
    Item2.gl = item['gl']
    Item2.gp = item['gp']
    Item2.gh = item['gh']
    Item2.direct = item['direct']
    Item2.o_direct = item['direct']
    Item2.holeid = item['holeid']
    Item2.kcid = item['kcid']
    for i in range(0,101):
        if i <= 15:
            Item2.var_args[i]=item['var_args'][i]
        Item2.ahole_index[i]= item['ahole_index'][i]
        Item2.bhole_index[i]= item['bhole_index'][i]
        Item2.akc_index[i] = item['akc_index'][i]
        Item2.bkc_index[i] = item['bkc_index'][i]
        if i <= 5 :
            Item2.is_calc_holeconfig[i] = item['is_calc_holeconfig'][i]
        if i <= 5 :
            Item2.is_holeface_touch[i] = 0
    #// 基础图形描述
    Item2.bg_l_minx = item['bg_l_minx']
    Item2.bg_l_maxx = item['bg_l_maxx']
    Item2.bg_r_minx = item['bg_r_minx']
    Item2.bg_r_maxx = item['bg_r_maxx']
    Item2.bg_l_miny = item['bg_l_miny']
    Item2.bg_l_maxy = item['bg_l_maxy']
    Item2.bg_r_miny = item['bg_r_miny']
    Item2.bg_r_maxy = item['bg_r_maxy']
    Item2.bg_d_minx = item['bg_d_minx']
    Item2.bg_d_maxx = item['bg_d_maxx']
    Item2.bg_u_minx = item['bg_u_minx']
    Item2.bg_u_maxx = item['bg_u_maxx']
    Item2.bg_d_miny = item['bg_d_miny']
    Item2.bg_d_maxy = item['bg_d_maxy']
    Item2.bg_u_miny = item['bg_u_miny']
    Item2.bg_u_maxy = item['bg_u_maxy']
    Item2.bg_b_minx = item['bg_b_minx']
    Item2.bg_b_maxx = item['bg_b_maxx']
    Item2.bg_f_minx = item['bg_f_minx']
    Item2.bg_f_maxx = item['bg_f_maxx']
    Item2.bg_b_miny = item['bg_b_miny']
    Item2.bg_b_maxy = item['bg_b_maxy']
    Item2.bg_f_miny = item['bg_f_miny']
    Item2.bg_f_maxy = item['bg_f_maxy']
    Item2.hole_back_cap = item['hole_back_cap']
    Item2.hole_2_dist = item['hole_2_dist']
    Item2.zero_y = item['zero_y']
    Item2.bg = item['bg']
    Item2.mat = item['mat']
    Item2.name = item['name']
    Item2.color = item['color']
    Item2.bdxmlid = item['bdxmlid']
    Item2.holeconfig_flag = item['holeconfig_flag']
    Item2.kcconig_flag = item['kcconig_flag']
    Item2.devcode = item['devcode']
    Item2.data = p
    # if item['bl'] =='':
    #     item['bl'] =0
    # if item['bl'] =='':
    #     item['bl'] =0
    # if item['bl'] =='':
    #     item['bl'] =0
    string = 'Workflow="%s" JXS="%s" TIME="%s" ORDER="%s" GNO="%s" DESNO="%s" CBNO="%s" USER="%s" TYPE="%s" NAME="%s" FBSTR="%s" SIZE="%s" UNIT="%s" PackNo="%s"'%(
        GetWorkflowStr(item['workflow'], item['bomstd'], '', workflowlist),
        'jinxiaoshan',#mDistributor,#经销商
        '2019-02-28',#'FormatDateTime('yyyy-mm-dd', mDateTime),
        '123',#'#mOrderName,
        item['gno'],
        item['gdes'],
        item['gcb'],
        'litao',#mUserName,
        item['myclass'],
        item['name'],
        item['fbstr'],
        '%d*%d*%d'%(round(float(item['bl'])), round(float(item['bp'])), round(float(item['bh']))),
        item['myunit'],
        item['packno'],)
    Item2.bdinfo='%s MEMO="%s" Mat="%s" Color="%s" HoleStr="%s" KcStr="%s" HoleFlag="%s" KcFlag="%s" BomStd="%s" JXSPHONE="%s" JXSADDR="%s" CLIENT="%s" CLIENTPHONE="%s" CLIENTMOBILEPHONE="%s" CLIENTADDR="%s"'%(
        string,
        item['memo'],
        item['mat'],
        item['color'],
        item['holestr'],
        item['kcstr'],
        item['holeconfig_flag'],
        item['kcconig_flag'],
        item['bomstd'],
        '123',#'#mPhone,
        'dfdf',#'#mAddress,
        'name',#'#mCustomerName,
        '1232',#'#mCustomerPhone,
        '3434',#'#m#CustomerCellPhone,
        'dfdf')#'#mCustomerAddress)
    Item2.llfb = item['llfb']
    Item2.rrfb = item['rrfb']
    Item2.ddfb = item['ddfb']
    Item2.uufb = item['uufb']
    Item2.fb = item['fb']
    flag = 0
    bdxml = ''
    if Item2.bdxmlid != '':
        bdxml = mBDXMLList[Item2.bdxmlid]
        flag = 1
    if item['bg_filename'] != '' and os.path.exists(item['bg_filename']):
        with open(item['bg_filename']) as f:
            bdxml = f.read(item['bg_filename'])
            bdxml = ClearXMLDocTag(bdxml)
            flag = 2
    if bdxml == '':
        return Result
    mExp = {}
    mExp['L'] = Item2.gl
    mExp['W'] = Item2.gp
    if flag ==1:
        if Item2.direct in [1,5]:
            mExp['L'] = Item2.gl
            mExp['W'] = Item2.gp
        if Item2.direct in [2,3]:
            mExp['L'] = Item2.gl
            mExp['W'] = Item2.gh
        if Item2.direct in [4, 6] :
            mExp['L'] = Item2.gp
            mExp['W'] = Item2.gh
        mExp['CA'] = Item2.var_args[0]
        mExp['CB'] = Item2.var_args[1]
        mExp['CC'] = Item2.var_args[2]
        mExp['CD'] = Item2.var_args[3]
        mExp['CE'] = Item2.var_args[4]
        mExp['CF'] = Item2.var_args[5]
        mExp['CG'] = Item2.var_args[6]
        mExp['CH'] = Item2.var_args[7]
        mExp['CI'] = Item2.var_args[8]
        mExp['CJ'] = Item2.var_args[9]
        mExp['CK'] = Item2.var_args[10]
        mExp['CL'] = Item2.var_args[11]
        mExp['CM'] = Item2.var_args[12]
        mExp['CN'] = Item2.var_args[13]
        mExp['CO'] = Item2.var_args[14]
        mExp['CP'] = Item2.var_args[15]
    root = ET.fromstring(bdxml)
    for i in range(0,len(root)):
        if root[i].tag == 'Graph':
            node = root[i]
            attri = node.get('XX','')
    n = 0
    for i in range(0, len(root)):
        node = root[i]
        if (node.tag != 'FaceA') and (node.tag != 'FaceB'):
            continue
        for j in range(0,len(node)):
            cnode = node[j]
            if cnode.tag != 'BHole' :
                continue
            n = n + 1
    Item2.bhpt =[MyBigHolePoint() for i in range(n)]
    n = 0
    for i in range(0,len(root)):
        node = root[i]
        if (node.tag != 'FaceA') and (node.tag != 'FaceB'):
            continue
        for j in range(0, len(node)):
            cnode = node[j]
            if cnode.tag != 'BHole' :
                continue
            attri = cnode.get('X','')
            if attri !='':
                Item2.bhpt[n].sx = cnode.get('X')
            attri = cnode.get('Y', '')
            if attri != '':
                Item2.bhpt[n].sy = cnode.get('Y')
            attri = cnode.get('R', '')
            if attri != '':
                Item2.bhpt[n].sr = cnode.get('R')
            attri = cnode.get('Rb', '')
            if attri != '':
                Item2.bhpt[n].srb = cnode.get('Rb')
            Item2.bhpt[n].sri = Item2.bhpt[n].srb
            attri = cnode.get('X1', '')
            if attri != '':
                Item2.bhpt[n].sri= cnode.get('X1')
            attri = cnode.get('HDirect', '')
            if attri != '':
                Item2.bhpt[n].hdirect= cnode.get('hdirect')
                Item2.bhpt[n].face = node.tag
            attri = cnode.get('Hole_Xcap', '')
            if attri != '':
                Item2.bhpt[n].hole_xcap = int(mExpSetSubject(mExp,cnode.get('Hole_Xcap')))
            attri = cnode.get('Hole_Ycap', '')
            if attri != '':
                Item2.bhpt[n].hole_ycap = int(mExpSetSubject(mExp,cnode.get('Hole_Ycap')))
            attri = cnode.get('Holenum_X', '')
            if attri != '':
                Item2.bhpt[n].holenum_x = cnode.get('Holenum_X')
            attri = cnode.get('Holenum_Y', '')
            if attri != '':
                Item2.bhpt[n].holenum_y = cnode.get('Holenum_Y')
            if cnode.get('Hole_Z'):
                Item2.bhpt[n].hole_z = cnode.get('Hole_Z')
            #print '2=',SetSubject(mExp,Item2.bhpt[n].sx)
            Item2.bhpt[n].x = float(mExpSetSubject(mExp,Item2.bhpt[n].sx))
            Item2.bhpt[n].y = float(mExpSetSubject(mExp,Item2.bhpt[n].sy))
            Item2.bhpt[n].r = float(mExpSetSubject(mExp,Item2.bhpt[n].sr))
            Item2.bhpt[n].rb = float(mExpSetSubject(mExp,Item2.bhpt[n].srb))
            Item2.bhpt[n].ri = float(mExpSetSubject(mExp,Item2.bhpt[n].sri))
            n = n + 1
    return Result
def productdict(u,key,value,exdict):
    Result = {}
    if u ==[]:
        ## 'kong u'
        return
    for i in u:
        try:
            exdict[i[key]] = i[value]
        except:
            pass
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
    items.sort(SortVar)
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
def InitPomOrderItem(PBomOrderItem):
    PBomOrderItem['cid'] = 0
    PBomOrderItem['id'] = 0
    PBomOrderItem['pid'] = -1
    PBomOrderItem['seq'] = 0
    PBomOrderItem['classseq'] = 0
    PBomOrderItem['code'] = ''
    PBomOrderItem['keyref'] = ''
    PBomOrderItem['name'] = ''
    PBomOrderItem['userdefine'] = ''
    PBomOrderItem['x'] = 0
    PBomOrderItem['y'] = 0
    PBomOrderItem['z'] = 0
    PBomOrderItem['l'] = 0
    PBomOrderItem['p'] = 0
    PBomOrderItem['h'] = 0
    PBomOrderItem['num'] = 0
    PBomOrderItem['mark'] = 0
    PBomOrderItem['linemax'] = 0
    PBomOrderItem['bh'] = 0
    PBomOrderItem['ox'] = 0
    PBomOrderItem['oy'] = 0
    PBomOrderItem['oz'] = 0
    PBomOrderItem['texture'] = ''
    PBomOrderItem['root'] = ''
    PBomOrderItem['rname'] = ''
    PBomOrderItem['childnum'] = 0
    PBomOrderItem['slino'] = 0
    PBomOrderItem['mat'] = ''
    PBomOrderItem['mat2'] = ''
    PBomOrderItem['mat3'] = ''
    PBomOrderItem['slidingmat'] = ''
    PBomOrderItem['desc'] = ''
    PBomOrderItem['price'] = 0
    PBomOrderItem['totalprice'] = 0
    PBomOrderItem['price2'] = 0
    PBomOrderItem['totalprice2'] = 0
    PBomOrderItem['cost'] = 0
    PBomOrderItem['square'] = 0
    PBomOrderItem['var_names'] = [''] * 16
    PBomOrderItem['var_args'] = [0] * 16
    PBomOrderItem['cl'] = 0
    PBomOrderItem['cp'] = 0
    PBomOrderItem['ch'] = 0
    PBomOrderItem['pricetype'] = ''
    PBomOrderItem['myunit'] = ''
    PBomOrderItem['myclass'] = ''
    PBomOrderItem['outputname'] = ''
    PBomOrderItem['outputno'] = ''
    PBomOrderItem['gno'] = ''
    PBomOrderItem['gdes'] = ''
    PBomOrderItem['soglaname'] = ''
    PBomOrderItem['subspace'] = ''
    PBomOrderItem['sale_type'] = ''
    PBomOrderItem['price_calctype'] = ''
    PBomOrderItem['group'] = ''
    PBomOrderItem['erpmatcode'] = ''
    PBomOrderItem['blockmemo'] = ''
    PBomOrderItem['number_text'] = ''
    PBomOrderItem['doorstyle'] = ''
    PBomOrderItem['doormat'] = ''
    PBomOrderItem['doorcolor'] = ''
    PBomOrderItem['isoutput'] = ''
    PBomOrderItem['isnotstd'] = ''
    PBomOrderItem['is_calc_cost'] = ''
    PBomOrderItem['msg'] = ''
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
def SetSysLPHValue(L,P,H):
    LPH = {}
    LPH['L'] = L
    LPH['P'] = P
    LPH['H'] = H
    return LPH
def SetSysVariantValueForOrderItem(varstr, newpoi):
    n = varstr.find('$左收口宽度')
    if n >= 0 : newpoi['value_lsk'] = value_lsk
    n = varstr.find('$右收口宽度')
    if n >= 0 : newpoi['value_rsk'] = value_rsk
    n = varstr.find('$柱切角宽度')
    if n >=0 : newpoi['value_zk'] = value_zk
    n = varstr.find('$柱切角深度')
    if n >= 0 : newpoi['value_zs'] = value_zs
    n = varstr.find('$梁切角深度')
    if n >= 0 : newpoi['value_ls'] = value_ls
    n = varstr.find('$梁切角高度')
    if n >= 0 : newpoi['value_lg'] = value_lg
    n = varstr.find('$左侧趟门位')
    if n >= 0 : newpoi['value_ltm'] = value_ltm
    n = varstr.find('$右侧趟门位')
    if n >= 0 : newpoi['value_rtm'] = value_rtm
def SetIsCalcHoleConfig(poi, HC):
    p = str(HC)
    for i in range(0,6):
        poi['is_calc_holeconfig'][i] = 0
    for i in range(0,len(p)):
        if (i == 0) and (p[i] == '1') : poi['is_calc_holeconfig'][i] = 1
        if (i == 0) and (p[i] == '2') : poi['is_calc_holeconfig'][i] = 2
        if (i == 1) and (p[i] == '1') : poi['is_calc_holeconfig'][i] = 1
        if (i == 1) and (p[i] == '2') : poi['is_calc_holeconfig'][i] = 2
        if (i == 2) and (p[i] == '1') : poi['is_calc_holeconfig'][i] = 1
        if (i == 2) and (p[i] == '2') : poi['is_calc_holeconfig'][i] = 2
        if (i == 3) and (p[i] == '1') : poi['is_calc_holeconfig'][i] = 1
        if (i == 3) and (p[i] == '2') : poi['is_calc_holeconfig'][i] = 2
        if (i == 4) and (p[i] == '1') : poi['is_calc_holeconfig'][i] = 1
        if (i == 4) and (p[i] == '2') : poi['is_calc_holeconfig'][i] = 2
        if (i == 5) and (p[i] == '1') : poi['is_calc_holeconfig'][i] = 1
        if (i == 5) and (p[i] == '2') : poi['is_calc_holeconfig'][i] = 2
def GraphSizeToBomSize(l, p, h, direct):
    bl1 = l
    bp1 = p
    bh1 = h
    # # 'in'
    if direct == 1:  # 宽深高
        bl1 = l
        bp1 = p
        bh1 = h
    if direct == 2:  # 宽高深
        bl1 = l
        bp1 = h
        bh1 = p
    if direct == 3:  # 高宽深
        bl1 = h
        bp1 = l
        bh1 = p
    if direct == 4:  # 高深宽
        bl1 = h
        bp1 = p
        bh1 = l
    if direct == 5:  # 深宽高
        bl1 = p
        bp1 = l
        bh1 = h
    if direct == 6:  # 深高宽
        bl1 = p
        bp1 = h
        bh1 = l
    return bl1, bp1, bh1
def GraphSizeToBomSize1(l, p, h, direct, bl, bp, bh):
    bl = l
    bp = p
    bh = h
    # # 'in'
    if direct == 1:  # 宽深高
        bl = l
        bp = p
        bh = h
    if direct == 2:  # 宽高深
        bl = l
        bp = h
        bh = p
    if direct == 3:  # 高宽深
        bl = h
        bp = l
        bh = p
    if direct == 4:  # 高深宽
        bl = h
        bp = p
        bh = l
    if direct == 5:  # 深宽高
        bl = p
        bp = l
        bh = h
    if direct == 6:  # 深高宽
        bl = p
        bp = h
        bh = l
    return bl,bp,bh
def connectdata(dataDBfile):
    conn = pypyodbc.win_connect_mdb(r'DRIVER={Microsoft Access Driver (*.mdb  *.accbd)};DBQ=' + dataDBfile)
    cur = conn.cursor()
    return conn, cur
def Nonetonumber(value, type = 'I'):
    result = 0
    if value=="":
        return result
    if type =='F':
        result = float(value)
        return result
    if type=='I':
        result = int(float(value))
        return result
    return result
def getfjo(i, typelist, ufetchall):
    fjo = {}
    for j in range(0, len(ufetchall[i])):
        if isinstance(ufetchall[i][j], int) or isinstance(ufetchall[i][j], float):
            fjo[typelist[j]] = str(ufetchall[i][j])
        else:
            if typelist[j]=='price':
                fjo[typelist[j]] = int(ufetchall[i][j])
                continue
            if isinstance(ufetchall[i][j], str):
                fjo[typelist[j]] = ufetchall[i][j]
            elif ufetchall[i][j] is None:
                fjo[typelist[j]] = ''
            else:
                fjo[typelist[j]] = ufetchall[i][j]
    return fjo
def OneBomData2Json(des):
    ResultJsonStr = ''
    dataDBfile = RootPath + '\\data\\data.mdb'
    if des=='' or (not os.path.exists(dataDBfile)):
        return ResultJsonStr
    else:
        conn, cur = connectdata(dataDBfile)
        n = des.find(',')
        s1 = des[:n].decode('utf8')
        s2 = des[n+1:].decode('utf8')
        sql = "select myclass2.*, myclass1.name as pname from myclass1, myclass2 where myclass2.myclass1=myclass1.id and myclass1.name='%s' and myclass2.name='%s'" % (
            s1, s2)
        cur.execute(sql)
        jo = {}
        ja = []
        fjo = {}
        des2wuliaoallu = cur.fetchall()
        if des2wuliaoallu==[]:
            return ResultJsonStr
        else:
            typelist = []
            for tup in cur.description:
                typelist.append(tup[0])  # 编码gbk
            for i in range(0, len(des2wuliaoallu)):
                fjo = getfjo(i, typelist, des2wuliaoallu)
                cjo = {}
                key = s1+','+s2
                cjo['key'] = key
                string = fjo['封边留空1']+','+fjo['封边留空2']
                cjo['s1'] = key
                cjo['s2'] = string
                cjo['s3'] = fjo['五金清单1']+','+fjo['五金清单2']
                cjo['direct'] = 0
                cjo['no'] = fjo['输出编号']  # 输出编号
                cjo['oname'] = fjo['输出名称']  # 输出名称
                cjo['childbom'] = fjo['物料分解']  # 物料分解
                cjo['priceclass'] = fjo['type']  # type
                if gQDBomFlag == 0:
                    cjo['bomclass'] = fjo['type']
                else:
                    cjo['bomclass'] = fjo['bomclass']  # bomclass
                cjo['linecalc'] = fjo['线性物体计算']  # 线性物体计算
                cjo['HoleConfig'] = fjo['孔位配置']  # 孔位配置
                cjo['bomstd'] = fjo['尺寸判定']  # 尺寸判定
                cjo['bomtype'] = fjo['物料分类']  # 物料分类
                cjo['KCConfig'] = fjo['开槽配置']  # 开槽配置
                cjo['bg_filename'] = fjo['bg_filename'] # bg_filename
                cjo['mpr_filename'] = fjo['mpr_filename']
                cjo['bpp_filename'] = fjo['bpp_filename']
                cjo['devcode'] = fjo['devcode']
                cjo['zero_y'] = fjo['zero_y']
                cjo['is_output_bgdata'] = fjo['is_output_bgdata']
                cjo['is_output_mpr'] = fjo['is_output_mpr']
                cjo['is_output_bpp'] = fjo['is_output_bpp']
                cjo['direct_calctype'] = fjo['direct_calctype']
                cjo['youge_holecalc'] = fjo['youge_holecalc']
                cjo['workflow'] = fjo['workflow']
                ja.append(cjo)
        jo['des2wuliao'] = ja
        #封边留空  bom_rule
        ja = []
        sql = ("select * from bom_rule where deleted=False and 物料类别1='%s' and 物料类别2='%s' order by 物料类别1 asc, 物料类别2 asc, 材料 asc " % (
            fjo['封边留空1'], fjo['封边留空2']))
        cur.execute(sql)
        ruleHashuf = cur.fetchall()
        if ruleHashuf != []:
            typelist = []
            ruleHash_dict = {}
            for tup in cur.description:
                typelist.append(tup[0])  # 编码gbk
            for i in range(0, len(ruleHashuf)):
                ruleHash_dict = getfjo(i, typelist, ruleHashuf)
                cjo = {}
                key = ruleHash_dict['物料类别1']+ ',' + ruleHash_dict['物料类别2']
                cjo['key'] = key
                cjo['myclass1'] = ruleHash_dict['物料类别1']
                cjo['myclass2'] = ruleHash_dict['物料类别1']
                cjo['mat'] = ruleHash_dict['材料']
                cjo['lfb'] = Nonetonumber(ruleHash_dict['l封边'])
                cjo['llk'] = Nonetonumber(ruleHash_dict['l留空'])
                cjo['wfb'] = Nonetonumber(ruleHash_dict['w封边'])
                cjo['wlk'] = Nonetonumber(ruleHash_dict['w留空'])
                cjo['holestr'] = ruleHash_dict['打孔']
                cjo['kcstr'] = ruleHash_dict['开槽']
                cjo['memo'] = ruleHash_dict['备注']
                cjo['fbstr'] = ruleHash_dict['封边']
                cjo['is_outline'] =0 if ruleHash_dict['is_outline'] =='' else int(ruleHash_dict['is_outline'])
                cjo['bh'] = Nonetonumber(ruleHash_dict['bh'])
                cjo['llfb'] = Nonetonumber(ruleHash_dict['lfb'])
                cjo['rrfb'] = Nonetonumber(ruleHash_dict['rfb'])
                cjo['ddfb'] = Nonetonumber(ruleHash_dict['dfb'])
                cjo['uufb'] = Nonetonumber(ruleHash_dict['ufb'])
                cjo['fb'] = Nonetonumber(ruleHash_dict['fb'])
                ja.append(cjo)
                prule = BomRuleRec()
        jo['ruleHash'] = ja
        #物料分解  base_bom2_class
        ja = []
        sql = "select base_bom2_class.name as bclass, bom2_rule.* from base_bom2_class,bom2_rule where bom2_rule.pid=base_bom2_class.id and bom2_rule.deleted = False and base_bom2_class.name='%s'" % (
            fjo['物料分解'])
        cur.execute(sql)
        wuliao_listuf = cur.fetchall()
        if wuliao_listuf != []:
            typelist = []
            wuliao_dict = {}
            for tup in cur.description:
                typelist.append(tup[0])  # 编码gbk
            for i in range(0, len(wuliao_listuf)):
                wuliao_dict = getfjo(i, typelist, wuliao_listuf)
                cjo = {}
                cjo['key'] =  wuliao_dict['bclass']
                cjo['id'] = Nonetonumber(wuliao_dict['id'])
                cjo['name'] = wuliao_dict['名称']
                cjo['mat'] = wuliao_dict['材料']
                cjo['color'] = wuliao_dict['颜色']
                cjo['lfb'] = Nonetonumber(wuliao_dict['l封边'])
                cjo['llk'] = Nonetonumber(wuliao_dict['l留空'])
                cjo['wfb'] = Nonetonumber(wuliao_dict['w封边'])
                cjo['wlk'] = Nonetonumber(wuliao_dict['w留空'])
                cjo['holestr'] = wuliao_dict['打孔']
                cjo['kcstr'] = wuliao_dict['开槽']
                cjo['memo'] = wuliao_dict['备注']
                cjo['ono'] = wuliao_dict['输出编号']
                cjo['bclass'] = wuliao_dict['bclass']
                cjo['fbstr'] = wuliao_dict['封边']
                cjo['bomstd'] = wuliao_dict['尺寸判定']
                cjo['bomtype'] = wuliao_dict['物料分类']
                cjo['a_face'] = wuliao_dict['a面孔']
                cjo['b_face'] = wuliao_dict['b面孔']
                cjo['bg_filename'] = wuliao_dict['bg_filename']
                cjo['mpr_filename'] = wuliao_dict['mpr_filename']
                cjo['bpp_filename'] = wuliao_dict['bpp_filename']
                cjo['devcode'] = wuliao_dict['devcode']
                cjo['direct_calctype'] = Nonetonumber(wuliao_dict['direct_calctype'])
                cjo['workflow'] = wuliao_dict['workflow']
                cjo['l'] = wuliao_dict['长度']
                cjo['p'] = wuliao_dict['宽度']
                cjo['h'] = wuliao_dict['厚度']
                cjo['q'] = wuliao_dict['数量']
                cjo['llfb'] = Nonetonumber(wuliao_dict['lfb'])
                cjo['rrfb'] = Nonetonumber(wuliao_dict['rfb'])
                cjo['ddfb'] = Nonetonumber(wuliao_dict['dfb'])
                cjo['uufb'] = Nonetonumber(wuliao_dict['ufb'])
                cjo['fb'] = Nonetonumber(wuliao_dict['fb'])
                cjo['lmax'] = Nonetonumber(wuliao_dict['lmax'])
                cjo['lmin'] = Nonetonumber(wuliao_dict['lmin'])
                cjo['dmax'] = Nonetonumber(wuliao_dict['dmax'])
                cjo['dmin'] = Nonetonumber(wuliao_dict['dmin'])
                cjo['hmax'] = Nonetonumber(wuliao_dict['hmax'])
                cjo['hmin'] = Nonetonumber(wuliao_dict['hmin'])
                cjo['deleted'] = False
                ja.append(cjo)
        jo['childbomHash'] = ja
        #五金
        sql = ("select base_wj_rule.*,[单位],xzw_basewj.[输出编号] as wjno,xzw_basewj.ID as wjid,xzw_basewj.[价格] " \
                       "as price from base_wj_rule,xzw_basewj where base_wj_rule.[五金名称]=xzw_basewj.[五金名称] and 五金规则类别1='%s' and 五金规则类别2='%s' " % (
            fjo['五金清单1'], fjo['五金清单2']))
        cur.execute(sql)
        ja = []
        wujin_listuf = cur.fetchall()
        if wujin_listuf:
            typelist = []
            wujin_dict = {}
            for tup in cur.description:
                typelist.append(tup[0])  # 编码gbk
            for i in range(0, len(wujin_listuf)):
                wujin_dict = getfjo(i, typelist, wujin_listuf)
                cjo = {}
                key = wujin_dict['五金规则类别1'] + ',' + wujin_dict['五金规则类别2']
                cjo['key'] = key
                cjo['myclass1'] = wujin_dict['五金规则类别1']
                cjo['myclass2'] = wujin_dict['五金规则类别2']
                cjo['lmax'] = Nonetonumber(wujin_dict['宽最大'])
                cjo['lmin'] = Nonetonumber(wujin_dict['宽最小'])
                cjo['pmax'] = Nonetonumber(wujin_dict['深最大'])
                cjo['pmin'] = Nonetonumber(wujin_dict['深最小'])
                cjo['hmax'] = Nonetonumber(wujin_dict['高最大'])
                cjo['hmin'] = wujin_dict['高最小']
                cjo['wjname'] = wujin_dict['五金名称']
                cjo['wjno'] = wujin_dict['wjno']
                cjo['num'] = Nonetonumber(wujin_dict['数量'])
                cjo['myunit'] = wujin_dict['配置规则']
                cjo['lgflag'] = Nonetonumber(wujin_dict['连柜功能'])
                cjo['myunit2'] = wujin_dict['单位']
                cjo['mat'] = wujin_dict['材料']
                cjo['color'] = wujin_dict['颜色']
                cjo['wjid'] = Nonetonumber(wujin_dict['wjid'])
                cjo['price'] = Nonetonumber(wujin_dict['price'])
                ja.append(cjo)
        jo['wjruleHash'] = ja
        sql = ("select * from base_linecalc where name='%s' " % (fjo['线性物体计算']))
        cur.execute(sql)
        ja = []
        linecal_listuf = cur.fetchall()
        if linecal_listuf:
            typelist = []
            linecal_dict = {}
            for tup in cur.description:
                typelist.append(tup[0])  # 编码gbk
            for i in range(0, len(linecal_listuf)):
                linecal_dict = getfjo(i, typelist, linecal_listuf)
                cjo = {}
                if linecal_dict['name']:
                    cjo['name'] = linecal_dict['name']
                    cjo['linemax'] = Nonetonumber(linecal_dict['linemax'])
                ja.append(cjo)
        jo['linecalcList'] = ja
        ja = []
        sql = ("select * from base_holeconfig where name='%s' order by id" % (fjo['孔位配置']))
        cur.execute(sql)
        holeconfig_listuf = cur.fetchall()
        if holeconfig_listuf:
            typelist = []
            holeconfig_dict = {}
            for tup in cur.description:
                typelist.append(tup[0])  # 编码gbk
            for i in range(0, len(holeconfig_listuf)):
                holeconfig_dict = getfjo(i, typelist, holeconfig_listuf)
                cjo = {}
                key = holeconfig_dict['name']
                cjo['key'] = key
                cjo['id'] = holeconfig_dict['id']
                cjo['name'] = holeconfig_dict['name']
                cjo['flag'] = holeconfig_dict['flag']
                cjo['flag2'] = holeconfig_dict['flag2']
                cjo['l_bigname'] = holeconfig_dict['l_bigname']
                cjo['l_smallname'] = holeconfig_dict['l_smallname']
                cjo['i_name'] = holeconfig_dict['i_name']
                cjo['mx_name'] = holeconfig_dict['mx_name']
                cjo['l_holedepth'] = Nonetonumber(holeconfig_dict['l_holedepth'])
                cjo['l_bigcap'] = Nonetonumber(holeconfig_dict['l_bigcap'])
                cjo['l_smallcap'] = Nonetonumber(holeconfig_dict['l_smallcap'])
                cjo['calctype'] = Nonetonumber(holeconfig_dict['calctype'])
                cjo['holecap'] = holeconfig_dict['holecap']
                cjo['mx_calctype'] = Nonetonumber(holeconfig_dict['mx_calctype'])
                cjo['mx_cap'] = Nonetonumber(holeconfig_dict['mx_cap'])
                cjo['l_isoutput'] = Nonetonumber(holeconfig_dict['l_isoutput'])
                cjo['i_isoutput'] = Nonetonumber(holeconfig_dict['i_isoutput'])
                cjo['mx_isoutput'] = Nonetonumber(holeconfig_dict['mx_isoutput'])
                cjo['ismirror'] = Nonetonumber(holeconfig_dict['ismirror'])
                cjo['iscalc'] = Nonetonumber(holeconfig_dict['iscalc'])
                cjo['bigface'] = Nonetonumber(holeconfig_dict['bigface'])
                cjo['myface'] = Nonetonumber(holeconfig_dict['myface'])
                cjo['min'] = Nonetonumber(holeconfig_dict['min'])
                cjo['max'] = Nonetonumber(holeconfig_dict['max'])
                cjo['bh'] = Nonetonumber(holeconfig_dict['bh'])
                cjo['isoffset'] = Nonetonumber(holeconfig_dict['isoffset'])
                cjo['xo'] = holeconfig_dict['xo']
                cjo['yo'] = holeconfig_dict['yo']
                cjo['b_isoffset'] = Nonetonumber(holeconfig_dict['b_isoffset'])
                cjo['b_xo'] = holeconfig_dict['b_xo']
                cjo['b_yo'] = holeconfig_dict['b_yo']
                cjo['pkcap'] = Nonetonumber(holeconfig_dict['pkcap'])
                cjo['holenum'] = Nonetonumber(holeconfig_dict['holenum'])
                cjo['center_holenum'] = Nonetonumber(holeconfig_dict['center_holenum'])
                cjo['center_holecap'] = holeconfig_dict['center_holecap']
                cjo['i_offsetvalue'] = Nonetonumber(holeconfig_dict['i_offsetvalue'])
                cjo['algorithm'] = Nonetonumber(holeconfig_dict['algorithm'])
                ja.append(cjo)
        jo['holeconfigHash'] = ja
        ja = []
        sql = ("select * from base_kcconfig where name='%s' order by id" % (fjo['开槽配置']))
        cur.execute(sql)
        kcconfig_listuf = cur.fetchall()
        if kcconfig_listuf:
            typelist = []
            kcconfig_dict = {}
            for tup in cur.description:
                typelist.append(tup[0])  # 编码gbk
            for i in range(0, len(kcconfig_listuf)):
                kcconfig_dict = getfjo(i, typelist, kcconfig_listuf)
                cjo = {}
                key = kcconfig_dict['name']
                cjo['key'] = key
                cjo['id'] = Nonetonumber(kcconfig_dict['id'])
                cjo['name'] = kcconfig_dict['name']
                cjo['flag'] = kcconfig_dict['flag']
                cjo['myface'] = Nonetonumber(kcconfig_dict['myface'])
                cjo['cutter'] = Nonetonumber(kcconfig_dict['cutter'])
                cjo['min'] = Nonetonumber(kcconfig_dict['min'])
                cjo['max'] = Nonetonumber(kcconfig_dict['max'])
                cjo['x'] = Nonetonumber(kcconfig_dict['x'])
                cjo['y'] = Nonetonumber(kcconfig_dict['y'])
                cjo['l'] = Nonetonumber(kcconfig_dict['l'])
                cjo['w'] = Nonetonumber(kcconfig_dict['w'])
                cjo['device'] = Nonetonumber(kcconfig_dict['device'])
                ja.append(cjo)
        jo['kcconfigHash'] = ja
        ja = []
        #尺寸判定
        sql = ("select * from base_bomstd_rule where myclass1='%s' and myclass2='%s' order by [level] asc, [ID] asc" % (fjo['pname'], fjo['name']))
        cur.execute(sql)
        bomstd_rule_listuf = cur.fetchall()
        if bomstd_rule_listuf:
            typelist = []
            bomstd_rule_dict = {}
            for tup in cur.description:
                typelist.append(tup[0])  # 编码gbk
            for i in range(0, len(bomstd_rule_listuf)):
                bomstd_rule_dict = getfjo(i, typelist, bomstd_rule_listuf)
                cjo = {}
                cjo['myclass1'] = bomstd_rule_dict['myclass1']
                cjo['myclass2'] = bomstd_rule_dict['myclass2']
                cjo['lmax'] = Nonetonumber(bomstd_rule_dict['lmax'])
                cjo['lmin'] = Nonetonumber(bomstd_rule_dict['lmin'])
                cjo['dmax'] = Nonetonumber(bomstd_rule_dict['PMAX'])
                cjo['dmin'] = Nonetonumber(bomstd_rule_dict['PMIN'])
                cjo['hmax'] = Nonetonumber(bomstd_rule_dict['hmax'])
                cjo['hmin'] = Nonetonumber(bomstd_rule_dict['hmin'])
                cjo['stdflag'] = bomstd_rule_dict['stdflag']
                cjo['level'] = Nonetonumber(bomstd_rule_dict['level'])
                ja.append(cjo)
        jo['bomstdList'] = ja
        jo['result'] = 1
        # finally:
        #     conn.close()
        return json.dumps(jo,encoding='gbk',ensure_ascii=False)
def strtomd5(string):
    m2 = hashlib.md5()
    m2.update(string)
    md5code = m2.hexdigest()
    return md5code
def LoadOneBomData(des):
    Result = 0
    if des =='' or des ==',': return
    string = RootPath+'\\BomData\\'+strtomd5(des)
    if os.path.exists(string):
        with open(string, 'r') as f:
            objstr = f.read()
    else:
        objstr = OneBomData2Json(des)
        if not os.path.exists(RootPath+'\\BomData\\'):
            os.makedirs(RootPath+'\\BomData\\')
        with open(string,'w+') as f:
            f.write(objstr)
    if objstr == '':
        return Result
    jo =json.loads(objstr,encoding='utf8')
    ja = jo['des2wuliao']
    for i in range(0,len(ja)):
        cjo = ja[i]
        M = {}
        M['s1'] = cjo['s1']
        M['s2']= cjo['s2']
        M['s3'] = cjo['s3']
        M['direct'] = Nonetonumber(cjo['direct'])
        M['no'] = cjo['no']
        M['oname'] = cjo['oname']
        M['childbom'] = cjo['childbom']
        M['priceclass'] = cjo['priceclass']
        M['bomclass'] = cjo['bomclass']
        M['linecalc'] = cjo['linecalc']
        M['HoleConfig'] = cjo['HoleConfig']
        M['bomstd'] = cjo['bomstd']
        M['bomtype'] = cjo['bomtype']
        M['KCConfig'] = cjo['KCConfig']
        M['bg_filename'] = cjo['bg_filename']
        M['mpr_filename'] = cjo['mpr_filename']
        M['bpp_filename'] = cjo['bpp_filename']
        M['devcode'] = cjo['devcode']
        M['zero_y'] = Nonetonumber(cjo['zero_y'])
        M['is_output_bgdata'] = Nonetonumber(cjo['is_output_bgdata'])
        M['is_output_mpr'] = Nonetonumber(cjo['is_output_mpr'])
        M['is_output_bpp'] = Nonetonumber(cjo['is_output_bpp'])
        M['direct_calctype'] = Nonetonumber(cjo['direct_calctype'])
        M['youge_holecalc']= Nonetonumber(cjo['youge_holecalc'])
        M['workflow'] = cjo['workflow']
        key = cjo['key']
        des2wuliaodict[key] = M
    ja = jo['ruleHash']
    for i in range(0, len(ja)):
        cjo = ja[i]
        prule = BomRuleRec()
        prule.myclass1= cjo['myclass1']
        prule.myclass2= cjo['myclass2']
        prule.mat= cjo['mat']
        prule.lfb= Nonetonumber(cjo['lfb'])
        prule.llk= Nonetonumber(cjo['llk'])
        prule.wfb= Nonetonumber(cjo['wfb'])
        prule.wlk= Nonetonumber(cjo['wlk'])
        prule.holestr= cjo['holestr']
        prule.kcstr= cjo['kcstr']
        prule.memo= cjo['memo']
        prule.fbstr= cjo['fbstr']
        prule.is_outline= Nonetonumber(cjo['is_outline'])
        prule.bh= Nonetonumber(cjo['bh'])
        prule.llfb= Nonetonumber(cjo['llfb'])
        prule.rrfb= Nonetonumber(cjo['rrfb'])
        prule.ddfb= Nonetonumber(cjo['ddfb'])
        prule.uufb= Nonetonumber(cjo['uufb'])
        prule.fb= Nonetonumber(cjo['fb'])
        key= cjo['key']
        if key not in ruleHash:
            prulelist = []
            ruleHash[key] = prulelist
        else:
            prulelist = ruleHash[key]
        prulelist.append(prule)
    ja = jo['childbomHash']
    for i in range(0,len(ja)):
        cjo= ja[i]
        pcbomrule = Bom2RuleRec()
        pcbomrule.id= Nonetonumber(cjo['id'])
        pcbomrule.name= cjo['name']
        pcbomrule.mat= cjo['mat']
        pcbomrule.color= cjo['color']
        pcbomrule.lfb= Nonetonumber(cjo['lfb'])
        pcbomrule.llk = Nonetonumber(cjo['llk'])
        pcbomrule.wfb = Nonetonumber(cjo['wfb'])
        pcbomrule.wlk = Nonetonumber(cjo['wlk'])
        pcbomrule.holestr = cjo['holestr']
        pcbomrule.kcstr = cjo['kcstr']
        pcbomrule.memo = cjo['memo']
        pcbomrule.ono = cjo['ono']
        pcbomrule.bclass = cjo['bclass']
        pcbomrule.fbstr = cjo['fbstr']
        pcbomrule.bomstd = cjo['bomstd']
        pcbomrule.bomtype = cjo['bomtype']
        pcbomrule.a_face = cjo['a_face']
        pcbomrule.b_face = cjo['b_face']
        pcbomrule.bg_filename = cjo['bg_filename']
        pcbomrule.mpr_filename = cjo['mpr_filename']
        pcbomrule.bpp_filename = cjo['bpp_filename']
        pcbomrule.devcode = cjo['devcode']
        pcbomrule.direct_calctype = Nonetonumber(cjo['direct_calctype'])
        pcbomrule.workflow = cjo['workflow']
        pcbomrule.l = cjo['l']
        pcbomrule.p = cjo['p']
        pcbomrule.h = cjo['h']
        pcbomrule.q = Nonetonumber(cjo['q'])
        pcbomrule.llfb = Nonetonumber(cjo['llfb'])
        pcbomrule.rrfb = Nonetonumber(cjo['rrfb'])
        pcbomrule.ddfb = Nonetonumber(cjo['ddfb'])
        pcbomrule.uufb = Nonetonumber(cjo['uufb'])
        pcbomrule.fb = Nonetonumber(cjo['fb'])
        pcbomrule.lmax = Nonetonumber(cjo['lmax'])
        pcbomrule.lmin = Nonetonumber(cjo['lmin'])
        pcbomrule.dmax = Nonetonumber(cjo['dmax'])
        pcbomrule.dmin = Nonetonumber(cjo['dmin'])
        pcbomrule.hmax = Nonetonumber(cjo['hmax'])
        pcbomrule.hmin = Nonetonumber(cjo['hmin'])
        pcbomrule.deleted = cjo['deleted']
        key= cjo['key']
        if key not in childbomHash:
            clist = []
            childbomHash[key] = clist
        else:
            clist = childbomHash[key]
        clist.append(pcbomrule)
    ja = jo['wjruleHash']
    for i in range(0,len(ja)):
        cjo = ja[i]
        pwjrule = wujinruleclass()
        pwjrule.myclass1 = cjo['myclass1']
        pwjrule.myclass2 = cjo['myclass2']
        pwjrule.lmax = Nonetonumber(cjo['lmax'])
        pwjrule.lmin = Nonetonumber(cjo['lmin'])
        pwjrule.pmax = Nonetonumber(cjo['pmax'])
        pwjrule.pmin = Nonetonumber(cjo['pmin'])
        pwjrule.hmax = Nonetonumber(cjo['hmax'])
        pwjrule.hmin = Nonetonumber(cjo['hmin'])
        pwjrule.wjname = cjo['wjname']
        pwjrule.wjno = cjo['wjno']
        pwjrule.num = Nonetonumber(cjo['num'])
        pwjrule.myunit = cjo['myunit']
        pwjrule.lgflag = Nonetonumber(cjo['lgflag'])
        pwjrule.myunit2 = cjo['myunit2']
        pwjrule.mat = cjo['mat']
        pwjrule.color = cjo['color']
        pwjrule.wjid = Nonetonumber(cjo['wjid'])
        pwjrule.price = Nonetonumber(cjo['price'])
        key = cjo['key']
        key = cjo['key']
        if key not in wjruleHash:
            wujinrulelist = []
            wjruleHash[key] = wujinrulelist
        else:
            wujinrulelist = wjruleHash[key]
        wujinrulelist.append(pwjrule)
    ja = jo['linecalcList']
    for i in range(0,len(ja)):
        cjo = ja[i]
        linecalcList[cjo['name']] = Nonetonumber(cjo['linemax'])
    ja = jo['holeconfigHash']
    for i in range(0, len(ja)):
        cjo = ja[i]
        phole = THoleConfig()
        phole.id = Nonetonumber(cjo['id'])
        phole.name = cjo['name']
        phole.flag = cjo['flag']
        phole.flag2 = cjo['flag2']
        phole.l_bigname = cjo['l_bigname']
        phole.l_smallname = cjo['l_smallname']
        phole.i_name = cjo['i_name']
        phole.mx_name = cjo['mx_name']
        phole.l_holedepth = Nonetonumber(cjo['l_holedepth'])
        phole.l_bigcap = Nonetonumber(cjo['l_bigcap'])
        phole.l_smallcap = Nonetonumber(cjo['l_smallcap'])
        phole.calctype = Nonetonumber(cjo['calctype'])
        phole.holecap = cjo['holecap']
        phole.mx_calctype = Nonetonumber(cjo['mx_calctype'])
        phole.mx_cap = Nonetonumber(cjo['mx_cap'])
        phole.l_isoutput = Nonetonumber(cjo['l_isoutput'])
        phole.i_isoutput = Nonetonumber(cjo['i_isoutput'])
        phole.mx_isoutput = Nonetonumber(cjo['mx_isoutput'])
        phole.ismirror = Nonetonumber(cjo['ismirror'])
        phole.iscalc = Nonetonumber(cjo['iscalc'])
        phole.bigface = Nonetonumber(cjo['bigface'])
        phole.myface = Nonetonumber(cjo['myface'])
        phole.min = Nonetonumber(cjo['min'])
        phole.max = Nonetonumber(cjo['max'])
        phole.bh = Nonetonumber(cjo['bh'])
        phole.isoffset = Nonetonumber(cjo['isoffset'])
        phole.xo = Nonetonumber(cjo['xo'])
        phole.yo = Nonetonumber(cjo['yo'])
        phole.b_isoffset = Nonetonumber(cjo['b_isoffset'])
        phole.b_xo = cjo['b_xo']
        phole.b_yo = cjo['b_yo']
        phole.pkcap = Nonetonumber(cjo['pkcap'])
        phole.holenum = Nonetonumber(cjo['holenum'])
        phole.center_holenum = Nonetonumber(cjo['center_holenum'])
        phole.center_holecap = cjo['center_holecap']
        phole.i_offsetvalue = Nonetonumber(cjo['i_offsetvalue'])
        phole.algorithm = Nonetonumber(cjo['algorithm'])
        key = cjo['key']
        if key not in holeconfigHash:
            pholelist = []
            holeconfigHash[key] = pholelist
        else:
            pholelist = holeconfigHash[key]
        pholelist.append(phole)
    ja = jo['kcconfigHash']
    for i in range(0, len(ja)):
        cjo = ja[i]
        pkc = TKCConfig()
        pkc.id = Nonetonumber(cjo['id'])
        pkc.name = cjo['name']
        pkc.flag = cjo['flag']
        pkc.myface = Nonetonumber(cjo['myface'])
        pkc.cutter = cjo['cutter']
        pkc.min = Nonetonumber(cjo['min'])
        pkc.max = Nonetonumber(cjo['max'])
        pkc.x = Nonetonumber(cjo['x'])
        pkc.y = Nonetonumber(cjo['y'])
        pkc.l = Nonetonumber(cjo['l'])
        pkc.w = Nonetonumber(cjo['w'])
        pkc.device = Nonetonumber(cjo['device'])
        key = cjo['key']
        if key not in kcconfigHash:
            kcinfolist = []
            kcconfigHash[key] = kcinfolist
        else:
            kcinfolist = kcconfigHash[key]
        kcinfolist.append(pkc)
    ja = jo['bomstdList']
    for i in range(0, len(ja)):
        cjo = ja[i]
        pbs = PBomStd()
        pbs.myclass1 = cjo['myclass1']
        pbs.myclass2 = cjo['myclass2']
        pbs.lmax = Nonetonumber(cjo['lmax'])
        pbs.lmin = Nonetonumber(cjo['lmin'])
        pbs.dmax = Nonetonumber(cjo['dmax'])
        pbs.dmin = Nonetonumber(cjo['dmin'])
        pbs.hmax = Nonetonumber(cjo['hmax'])
        pbs.hmin = Nonetonumber(cjo['hmin'])
        pbs.stdflag = cjo['stdflag']
        pbs.level = Nonetonumber(cjo['level'])
        bomstdList.append(pbs)
    jo = None
def Des2Des(poi):
    if poi['desc'] == '':
        l = poi['l']
        p = poi['p']
        h = poi['h']
        direct = int(poi['direct'])
        bl, bp, bh = GraphSizeToBomSize(l, p, h, direct)
        wuliaol = int(bl)
        wuliaop = int(bp)
        wuliaoh = int(bh)
        poi['bl'] = wuliaol
        poi['bp'] = wuliaop
        poi['bh'] = wuliaoh
        return
    else:
        des2 = None
        if poi['desc'] in des2wuliaodict:
            des2 = des2wuliaodict[poi['desc']]
        else:
            LoadOneBomData(poi['desc'])
            if poi['desc'] in des2wuliaodict:
                des2 = des2wuliaodict[poi['desc']]
        if des2 :
            poi['desc'] = des2['s1']
            poi['bomdes'] = des2['s2']
            poi['bomwjdes'] = des2['s3']
            poi['name'] = des2['oname']  # 输出名称
            poi['childbom'] = des2['childbom']  # 物料分解
            poi['myclass'] = des2['bomclass']
            poi['linecalc'] =des2['linecalc']
            poi['bomstddes'] = des2['bomstd']
            poi['bomtype'] = des2['bomtype']
            if des2['linecalc'] != '' :
                poi['linemax'] = linecalcList[poi['linecalc']] # 线性物体计算
                if poi['linemax'] == -1 : poi['linecalc'] = ''
            if des2['HoleConfig'] !='':
                poi['holeid'] = des2['HoleConfig']
            if des2['KCConfig'] !='':
                poi['kcid'] = des2['KCConfig']
            poi['bg_filename'] = des2['bg_filename']  # bg_filename
            poi['bpp_filename'] = des2['bpp_filename']
            poi['devcode'] = des2['devcode']
            poi['zero_y'] = des2['zero_y']
            poi['is_output_bgdata'] = des2['is_output_bgdata']
            poi['is_output_bgdata'] = des2['is_output_mpr']
            poi['is_output_bpp'] = des2['is_output_bpp']
            poi['direct_calctype'] = des2['direct_calctype']
            poi['youge_holecalc'] = des2['youge_holecalc']
            poi['workflow'] = des2['workflow']
#尺寸判定
def ToBomStd(des, l, p, h):
    Result = ''
    if des == '':
        return Result
    else:
        for i in range(0,len(bomstdList)):
            pbs = bomstdList[i]
            if (pbs.myclass1 + ',' + pbs.myclass2) == des :
                if (pbs.lmax >= l) and (pbs.lmin <= l) and (pbs.dmax >= p) \
                    and (pbs.dmin <= p) and (pbs.hmax >= h) and (pbs.hmin <= h) :
                    Result = pbs.stdflag
                    return Result
    return Result
def readMDXml(cnode,sMKobj,ntype): #读取趟门，掩门的数据
    if (ntype):
        mddt = {
            "成品门高": 0,
            "成品门宽": 0,
            "门款类型": "",
            "扇数": 0,
            "Extra": "Extra",
            "DoorType": 1,
            "门洞高": 0,
            "门洞宽": 0,
        }
    else : #// 掩门门洞
        mddt = {
            "成品门高": 0,
            "成品门宽": 0,
            "门款类型": "",
            "Extend": "",
            "扇数": 0,
            "DoorExtra": "",
            "HingeHole": "",
            "是否带框": 0,
            "DoorMemo": "",
            "门洞高": 0,
            "门洞宽": 0
        }
    for ip in range( 0,cnode.childNodes.length):
        scnode = cnode.childNodes[ip]
        if ("趟门" == scnode.nodeName or "掩门" == scnode.nodeName):
            mddt["门款类型"] = '0'
            if ntype:
                if scnode.hasAttribute("边框类型"):
                    mddt["门款类型"] = scnode.getAttribute("边框类型")
            else:
                if scnode.hasAttribute("门框类型"):
                    mddt["门款类型"] = scnode.getAttribute("门框类型")
            mddt["门洞高"] = int(float(sMKobj['h']))
            mddt["门洞宽"] = int(float(sMKobj['l']))
            if (not ntype):
                mddt["DoorExtra"] =  scnode.getAttribute("Extra")
                mddt["DoorMemo"] =  scnode.getAttribute("DoorMemo")
                mddt["HingeHole"] =  scnode.getAttribute("HingeHole")
                mddt["Extend"] =  scnode.getAttribute("Extend")
                mddt["是否带框"] =  int(float(scnode.getAttribute("是否带框")))
            else:
                pass
            nDMnum = 0
            for iip in range(0, scnode.childNodes.length):
                sscnode = scnode.childNodes[iip]
                if ("单门" == sscnode.nodeName):
                    if (nDMnum == 0):
                        try:
                            mddt["成品门宽"] =  int(float(scnode.getAttribute("宽")))
                            mddt["成品门高"] =  int(float(scnode.getAttribute("高")))
                        except:
                            pass
                    nDMnum  = nDMnum + 1
            mddt["扇数"] = nDMnum
    return mddt
def newDoorItem():
    DoorItem = {}
    DoorItem['xml'] = ''
    DoorItem['name'] = ''
    DoorItem['gno'] = ''
    DoorItem['des'] = ''
    DoorItem['gcb'] = ''
    DoorItem['extra'] = ''
    DoorItem['doortype'] = ''
    DoorItem['hingehole'] = ''
    DoorItem['doormemo'] = ''
    DoorItem['doorextra'] = ''
    DoorItem['l'] = 0
    DoorItem['d'] = 0
    DoorItem['h'] = 0
    DoorItem['one_l'] = 0
    DoorItem['one_h'] = 0
    DoorItem['num'] = 0
    DoorItem['xmlindex'] = 0
    DoorItem['slino'] = 0
    DoorItem['isframe'] = 0
    DoorItem['userdata'] = 0
    return DoorItem
def ImportSlidingXomItemForBom(pid, cid, subspace, gno, gdes, gcb, extra, mark, outputtype, xml,blockxml, obj):
    global id, slino
    mXMLStringList.append(xml)
    dtype = obj['门框类型']
    sliw = float(obj['门洞宽'])
    slih = float(obj['门洞高'])
    doorw = float(obj['成品门宽'])
    doorh = float(obj['成品门高'])
    doornum = int(obj['扇数'])
    doorextra = obj['DoorExtra']
    ja = obj['物料']
    for i in range(0, len(obj['物料'])):
        cjo = obj['物料'][i]
        pslibom = newpslibom()
        pslibom['xmlindex']= len(mXMLStringList) - 1
        pslibom['cid'] = cid
        pslibom['slino'] = slino
        pslibom['subspace']= subspace
        pslibom['id'] = id
        pslibom['pid'] = pid
        pslibom['space_id'] = -1
        pslibom['sliw'] = sliw
        pslibom['slih']= slih
        pslibom['doorw']= 0  if doorw=='' else float(doorw)
        pslibom['doorh']= 0  if doorh=='' else float(doorh)
        if int(pslibom['doorw']) == float(pslibom['doorw']):
            pslibom['doorw'] = int(pslibom['doorw'])
        if int(pslibom['doorh']) == float(pslibom['doorh']):
            pslibom['doorh'] = int(pslibom['doorh'])
        pslibom['doornum']= int(float(doornum))
        pslibom['gno'] = gno
        pslibom['gdes'] = gdes
        pslibom['dtype'] = dtype
        pslibom['gcb'] = gcb
        pslibom['extra'] = extra
        pslibom['mark'] = mark
        pslibom['code'] = cjo['Code']
        pslibom['name'] = cjo['Name']
        pslibom['mat'] = cjo['Name']
        pslibom['color'] = cjo['Color']
        pslibom['l'] =0  if cjo['L']=='' else float(cjo['L'])
        pslibom['p'] = 0  if cjo['W']=='' else float(cjo['W'])
        pslibom['h'] = 0  if cjo['H']=='' else float(cjo['H'])
        if int(pslibom['l']) == float(pslibom['l']):
            pslibom['l'] = int(pslibom['l'])
        if int(pslibom['p']) == float(pslibom['p']):
            pslibom['p'] = int(pslibom['p'])
        if int(pslibom['h']) == float(pslibom['h']):
            pslibom['h'] = int(pslibom['h'])
        pslibom['num'] = int(cjo['Num'])
        pslibom['group'] = str(cjo['Group'])
        pslibom['myunit'] = cjo['Unit']
        pslibom['doorname'] = cjo['DoorName']
        pslibom['bomtype'] = '' if 'Bomtype' not in cjo else cjo['Bomtype']
        pslibom['memo'] = cjo['Memo']
        pslibom['memo2'] = cjo['Memo2']
        pslibom['memo3'] = cjo['Memo3']
        pslibom['bdfile'] = cjo['BDFILE']
        pslibom['doormemo'] = '' if 'DoorMemo' not in cjo else cjo['DoorMemo']
        pslibom['door_index'] = 0 if 'DoorIndex' not in cjo else int(cjo['DoorIndex'])
        pslibom['isglass'] = 0 if 'Glass' not in cjo else int(cjo['Glass'])
        pslibom['is_buy'] = 0 if 'IsBuy' not in cjo else int(cjo['IsBuy'])
        pslibom['direct'] = cjo['Di']
        pslibom['fbstr'] = '' if 'FBStr' not in cjo else cjo['FBStr']
        pslibom['bdxmlid'] ='' if 'BDXMLID' not in cjo else cjo['BDXMLID']
        if pslibom['bdxmlid'] != '' :
            mBDXMLList[pslibom['bdxmlid']] = cjo['BDXML']
        slidinglist.append(pslibom)
        id = id + 1
    DoorItem = newDoorItem()
    DoorItem['name'] = ''
    DoorItem['gno'] = gno
    DoorItem['des'] = gdes
    DoorItem['gcb'] = gcb
    DoorItem['extra'] = extra
    DoorItem['slino'] = slino
    DoorItem['l'] = sliw
    DoorItem['h'] = slih
    DoorItem['d'] = 0
    DoorItem['one_l'] = doorw
    DoorItem['one_h'] = doorh
    DoorItem['num'] = doornum
    DoorItem['doorextra'] = doorextra
    DoorItem['isframe'] = 1
    DoorItem['doortype'] = '趟门'
    DoorItem['hingehole'] = ''
    DoorItem['xmlindex'] = len(mXMLStringList) - 1
    DoorItem['xml'] = blockxml
    mDoorList.append(DoorItem)
    slino = slino + 1
def ImportDoorsXomItemForBom(pid, cid, subspace,gno,gdes,gcb,extra, mark,outputtype,xml,blockxml,obj):
    global id, slino
    mXMLStringList.append(xml)
    dtype = obj['门款类型']
    isframe = obj['是否带框']
    hingehole = obj['HingeHole']
    doormemo = obj['DoorMemo']
    doorextra = obj['DoorExtra']
    sliw = float(obj['门洞宽'])
    slih = float(obj['门洞高'])
    doorw = float(obj['成品门宽'])
    doorh = float(obj['成品门高'])
    doornum = int(obj['扇数'])
    ja = obj['物料']
    for i in range(0, len(obj['物料'])):
        cjo = obj['物料'][i]
        pslibom = newpslibom()
        pslibom['xmlindex']= len(mXMLStringList) -1
        pslibom['cid'] = cid
        pslibom['slino'] = slino
        pslibom['subspace']= subspace
        pslibom['id'] = id
        pslibom['pid'] = pid
        pslibom['space_id'] = -1
        pslibom['sliw'] = sliw
        pslibom['slih']= slih
        pslibom['doorw'] = 0 if doorw == '' else float(doorw)
        pslibom['doorh'] = 0 if doorh == '' else float(doorh)
        if int(pslibom['doorw']) == float(pslibom['doorw']):
            pslibom['doorw'] = int(pslibom['doorw'])
        if int(pslibom['doorh']) == float(pslibom['doorh']):
            pslibom['doorh'] = int(pslibom['doorh'])
        pslibom['doornum']= doornum
        pslibom['gno'] = gno
        pslibom['gdes'] = gdes
        pslibom['dtype'] = dtype
        pslibom['gcb'] = gcb
        pslibom['extra'] = extra
        pslibom['mark'] = mark
        pslibom['code'] = cjo['Code']
        pslibom['name'] = cjo['Name']
        pslibom['mat'] = cjo['Name']
        pslibom['color'] = cjo['Color']
        pslibom['l'] = 0 if cjo['L'] == '' else float(cjo['L'])
        pslibom['p'] = 0 if cjo['W'] == '' else float(cjo['W'])
        pslibom['h'] = 0 if cjo['H'] == '' else float(cjo['H'])
        if int(pslibom['l']) == float(pslibom['l']):
            pslibom['l'] = int(pslibom['l'])
        if int(pslibom['p']) == float(pslibom['p']):
            pslibom['p'] = int(pslibom['p'])
        if int(pslibom['h']) == float(pslibom['h']):
            pslibom['h'] = int(pslibom['h'])
        pslibom['num'] = int(cjo['Num'])
        pslibom['group'] = str(cjo['Group'])
        pslibom['myunit'] = cjo['Unit']
        pslibom['doorname'] = cjo['DoorName']
        pslibom['bomtype'] = cjo['Bomtype']
        pslibom['memo'] = cjo['Memo']
        pslibom['memo2'] = cjo['Memo2']
        pslibom['memo3'] = cjo['Memo3']
        pslibom['bdfile'] = cjo['BDFILE']
        pslibom['doormemo'] = '' if 'DoorMemo' not in cjo else cjo['DoorMemo']
        pslibom['door_index'] = 0 if 'DoorIndex' not in cjo else int(cjo['DoorIndex'])
        pslibom['isglass'] = 0 if 'Glass' not in cjo else int(cjo['Glass'])
        pslibom['is_buy'] = 0 if 'IsBuy' not in cjo else int(cjo['IsBuy'])
        pslibom['direct'] = cjo['Di']
        pslibom['fbstr'] = '' if 'FBStr' not in cjo else cjo['FBStr']
        pslibom['bdxmlid'] = '' if 'BDXMLID' not in cjo else cjo['BDXMLID']
        if pslibom['bdxmlid'] != '' :
            mBDXMLList[pslibom['bdxmlid']] = cjo['BDXML']
        doorslist.append(pslibom)
        id = id + 1
    DoorItem = newDoorItem()
    DoorItem['name'] = ''
    DoorItem['gno'] = gno
    DoorItem['des'] = gdes
    DoorItem['gcb'] = gcb
    DoorItem['extra'] = extra
    DoorItem['slino'] = slino
    DoorItem['l'] = sliw
    DoorItem['h'] = slih
    DoorItem['d'] = 0
    DoorItem['one_l'] = doorw
    DoorItem['one_h'] = doorh
    DoorItem['num'] = doornum
    DoorItem['isframe'] = isframe
    DoorItem['doortype'] = '掩门'
    DoorItem['xmlindex'] = len(mXMLStringList) - 1
    DoorItem['doorextra'] = doorextra
    DoorItem['xml'] = blockxml
    DoorItem['hingehole'] = hingehole
    DoorItem['doormemo'] = doormemo
    DoorItem['doorextra'] = doorextra
    mDoorList.append(DoorItem)
    slino = slino + 1
def getfirstchild(node):
    Result = None
    for child in node.childNodes:
        if child.nodeType !=1: continue
        Result = child
        break
    return Result
def InitPriceJson(sMKobjb, newpoi):
    sMKobjb['显示方式'] = newpoi['显示方式']
    sMKobjb['number_text'] = newpoi['number_text']
    sMKobjb['group'] = newpoi['group']
    sMKobjb['isoutput'] = True
    sMKobjb['name'] = newpoi['name']
    sMKobjb['id'] = newpoi['id']
    sMKobjb['pid'] = newpoi['pid']
    sMKobjb['gno'] = newpoi['gno']
    sMKobjb['gdes'] = newpoi['gdes']
    sMKobjb['subspace'] = newpoi['subspace']
    sMKobjb['bh'] = newpoi['boardheight']
    sMKobjb['price_calctype'] = newpoi['pricecalctype']
    sMKobjb['is_calc_cost'] = False
    sMKobjb['cost'] = 0
    sMKobjb['slino'] = -1
    sMKobjb['linemax'] = newpoi['linemax']
    sMKobjb['Program'] = newpoi['Program']
    sMKobjb['guid'] = newpoi['guid']
    sMKobjb['var_args'] = newpoi['var_args']
    sMKobjb['var_names'] = newpoi['var_names']
    sMKobjb['x'] = newpoi['x']
    sMKobjb['y'] = newpoi['y']
    sMKobjb['z'] = newpoi['z']
    sMKobjb['l'] = newpoi['l']
    sMKobjb['p'] = newpoi['p']
    sMKobjb['h'] = newpoi['h']
    sMKobjb['lo'] = newpoi['l']
    sMKobjb['po'] = newpoi['p']
    sMKobjb['ho'] = newpoi['h']
    sMKobjb['oz'] = newpoi['oz']
    sMKobjb['DI'] = newpoi['DI']
    sMKobjb['direct'] = newpoi['DI']
    sMKobjb['mat'] = newpoi['mat']
    sMKobjb['color'] = newpoi['color']
    sMKobjb['desc'] = newpoi['desc']
    sMKobjb['num'] = newpoi['num']
    sMKobjb['mark'] = newpoi['mark']
    sMKobjb['userdefine'] = newpoi['userdefine']
def GraphSizeToBJSize(bjsize, pbom):
    ll = 0
    pp = 0
    s= bjsize
    n = bjsize.find(',')
    if n >= 0 :
        s1 = bjsize[:n]
        ll = int(s1)
        s = str(s[n+1:])
        n = s.find(',')
        if n >= 0:
            s1= s[0: n]
            pp = int(s1)
            s = s[n+1:]
        hh = int(s)
        pbom['l'] = pbom['l'] + ll
        pbom['p'] = pbom['p'] + pp
        pbom['h'] = pbom['h'] + hh
def ImportXomItemForBom(param,AllPrice):
    global id,slino
    Result = 0
    isdoor = False
    LPH = SetSysLPHValue(param['pl'],param['pd'],param['ph'])
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
        node = nodelist[0]    #模板节点
        if node.nodeName == '模板':
            childxml = ''
            cnode = getfirstchild(node)
            if cnode:
                childxml = cnode.toxml('Utf-8')
                AllPrice["模板"] = childxml
                if (string == '趟门,趟门'):
                    AllPrice["趟门门洞"] = readMDXml(cnode, AllPrice, 1)
                    obj = fun(childxml, AllPrice["趟门门洞"]["门洞宽"],
                              AllPrice["趟门门洞"]["门洞高"], RootPath)
                    if obj:
                        for key, value in list(obj.items()):
                            AllPrice[key] = obj[key]
                            if key=='物料':
                                for onesliding in obj['物料']:
                                    if onesliding["Name"] not in desslidinglist:
                                        desslidinglist.append(onesliding["Name"])
                        ImportSlidingXomItemForBom(id - 1, param['cid'],
                                                   param['subspace'],
                                                   param['gno'], param['gdes'],
                                                   param['gcb'],
                                                   param['extra'], param['mark'],
                                                   param['outputtype'],
                                                   childxml, cnode.toxml('Utf-8'),
                                                   obj)
                if (string == '掩门,掩门'):
                    AllPrice["掩门门洞"] = readMDXml(cnode, AllPrice, 0)
                    obj = fungetdoorjson(childxml, AllPrice["掩门门洞"]["门洞宽"],
                                         AllPrice["掩门门洞"]["门洞高"], RootPath)
                    if obj:
                        for key, value in list(obj.items()):
                            AllPrice[key] = obj[key]
                            if key=='物料':
                                for onesliding in obj['物料']:
                                    if onesliding["Name"] not in desdoorlist:
                                        desdoorlist.append(onesliding["Name"])
                        ImportDoorsXomItemForBom(id - 1, param['cid'],
                                                 param['subspace'],
                                                 param['gno'], param['gdes'],
                                                 param['gcb'],
                                                 param['extra'], param['mark'],
                                                 param['outputtype'],
                                                 childxml, cnode.toxml('Utf-8'), obj)
            return Result
    string = root.getAttribute('板材单价')
    if string and param['pricecalctype'] == '':
        param['pricecalctype'] = string
    Var = {}
    for i in range(0, root.childNodes.length):
        node = root.childNodes[i]
        if node.nodeType != 1: continue
        if node.nodeName == 'BDXML':
            for j in range(0, node.childNodes.length):
                cnode = node.childNodes[j]
                if cnode.nodeType == 1:
                    if cnode.childNodes.length <= 0:
                        mBDXMLList[cnode.nodeName] = cnode.data
                    else:
                        for k in range(0,cnode.childNodes.length):
                            ccnode = cnode.childNodes[k]
                            if ccnode.nodeType == 1:
                                mBDXMLList[cnode.nodeName] = ccnode.toxml('UTF-8')
    nodelist = root.getElementsByTagName('变量列表')
    for i in range(0, root.childNodes.length):
        node = root.childNodes[i]
        if node.nodeType != 1: continue
        if node.nodeName == '变量列表':
            for j in range(0, node.childNodes.length):
                cnode = node.childNodes[j]
                if cnode.nodeType!= 1: continue
                if cnode.nodeName == '变量':
                    vname = cnode.getAttribute('名称')
                    value = cnode.getAttribute('值')
                    IsDisplay = cnode.getAttribute('是否显示')
                    Var = SetSysVariantValue(vname, value, Var)
    for i in range(0,root.childNodes.length):
        node = root.childNodes[i]
        if node.nodeType != 1: continue
        if node.nodeName == '我的模块':
            mkJs = []
            for j in range(0,node.childNodes.length):
                cnode = node.childNodes[j]
                if (cnode.nodeName != '板件') and (cnode.nodeName != '五金') and (
                        cnode.nodeName != '型材五金')and (cnode.nodeName != '模块') and (
                        cnode.nodeName != '门板'):
                    continue
                bg = cnode.getAttribute('基础图形')
                if bg =='BG::SPACE':continue
                string = cnode.getAttribute('显示方式')
                if string == '3':continue
                newpoi = {}
                newpoi['显示方式'] = string
                InitBomOrderItem(newpoi)
                # ACDlg = '0'
                # if cnode.hasAttribute(u'ACDlg'):
                #     ACDlg = cnode.getAttribute(u'ACDlg')
                # newpoi['ACDlg'] = ACDlg
                # Flag32 = '0'
                # if cnode.hasAttribute(u'Flag32'):
                #     Flag32 = cnode.getAttribute(u'Flag32')
                # newpoi['Flag32'] = Flag32
                # Tag = ''
                # if cnode.hasAttribute(u'Tag'):
                #     Tag = cnode.getAttribute(u'Tag')
                # newpoi['Tag'] = Tag
                # PRJ = '0.0'
                # if cnode.hasAttribute(u'PRJ'):
                #     PRJ = cnode.getAttribute(u'PRJ')
                # newpoi['PRJ'] = PRJ
                # original_ldh = ''
                # if cnode.hasAttribute(u'original_ldh'):
                #     original_ldh = cnode.getAttribute(u'original_ldh')
                # newpoi['original_ldh'] = original_ldh
                # ActFlag = ''
                # if cnode.hasAttribute(u'ActFlag'):
                #     ActFlag = cnode.getAttribute(u'ActFlag')
                #
                # if cnode.hasAttribute(u'SpaceFlag'):
                #     SpaceFlag = cnode.getAttribute(u'SpaceFlag')
                #     newpoi['SpaceFlag'] = SpaceFlag
                # LockEdit = ''
                # if cnode.hasAttribute(u'LockEdit'):
                #     LockEdit = cnode.getAttribute(u'LockEdit')
                # newpoi['LockEdit'] = LockEdit
                # newpoi['Type'] = cnode.nodeName
                if cnode.nodeName == '板件': newpoi['myunit']= '块'
                newpoi['guid'] = cnode.getAttribute('GUID')
                if newpoi['guid'] == '' or len(newpoi['guid']) < 10:
                    guid = str(uuid.uuid1())  # 唯一标识符guid
                    guid = ''.join(guid.split('-'))
                    newpoi['guid'] = guid
                tmp_space_x = param['space_x']
                tmp_space_y = param['space_y']
                tmp_space_z = param ['space_z']
                ass = cnode.getAttribute('报价规则')
                newpoi["报价规则"] = ass
                textureclass = cnode.getAttribute('装饰类别')
                newpoi['number_text'] = cnode.getAttribute('NumberText')
                if newpoi['number_text'] == '':
                    newpoi['number_text'] = param ['number_text']
                newpoi['pl'] = param['pl']
                newpoi['pd'] = param['pd']
                newpoi['ph'] = param['ph']
                newpoi['bg'] = bg
                newpoi['holeid'] = -1
                newpoi['kcid'] = -1
                newpoi['cid'] = param['cid']
                newpoi['isoutput'] = True
                for k in range(16):
                    newpoi['var_args'][k] = 0
                    newpoi['var_names'][k] = ''
                newpoi['nodename'] = cnode.nodeName
                newpoi['id'] = id
                newpoi['pid'] = param['pid']
                newpoi['subspace'] = param['subspace']
                newpoi['space_x'] = param['space_x']
                newpoi['space_y'] = param['space_y']
                newpoi['space_z'] = param['space_z']
                newpoi['space_id'] = param['space_id']
                newpoi['parent'] = param['parent']
                tmp_subspace = ''
                tmp_subspace = cnode.getAttribute('子空间')
                if tmp_subspace == 'A': tmp_subspace = ''
                newpoi['subspace'] = param['subspace'] + tmp_subspace
                if tmp_subspace != '': newpoi['isoutput'] = False
                newpoi['name'] = cnode.getAttribute('名称')
                varstr = ''
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
                    xx0 =int(cnode.getAttribute('XX0'))
                if cnode.hasAttribute('XX1'):
                    xx1 =int( cnode.getAttribute('XX1'))
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
                if cnode.getAttribute('OX') !='':
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
                if tmp_subspace != '':
                    tmp_space_x = newpoi['x']
                    tmp_space_y = newpoi['y']
                    tmp_space_z = newpoi['z']
                if tmp_subspace == 'B' or tmp_subspace == 'C':
                    product_item = mProductList[param['cid']]
                    product_item['l'] = product_item['l'] + newpoi['l']
                varstr = '0'
                if cnode.hasAttribute('GCL'):
                    varstr = cnode.getAttribute('GCL')
                newpoi['gcl']= int(varstr)
                newpoi['gcl2']= newpoi['gcl']
                varstr = '0'
                if cnode.hasAttribute('GCD'):
                    varstr = cnode.getAttribute('GCD')
                newpoi['gcd']= int(varstr)
                newpoi['gcd2'] = newpoi['gcd']
                varstr = '0'
                if cnode.hasAttribute('GCH'):
                    varstr = cnode.getAttribute('GCH')
                newpoi['gch'] = int(varstr)
                newpoi['gch2'] = newpoi['gch']
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
                newpoi['holeflag'] = 0
                string = ''
                string = cnode.getAttribute('HoleFlag')
                if string != '':
                    ToValueInt=int(SetSubject(LPH, string, Var))
                    newpoi['holeflag'] = ToValueInt
                #所有16个参数
                args=[0]*16
                for k in range(0,16):
                    args[k] = 0
                    string = ''
                    if cnode.hasAttribute(('参数'+str(k))):
                        string = cnode.getAttribute(('参数'+str(k)))
                    if (string != '') :
                        vname = ''
                        value = ''
                        vname, value = MyVariant(string, vname, value)
                        ToValueInt = int(SetSubject(LPH, value, Var))
                        args[k] = ToValueInt
                        newpoi['var_args'][k] = args[k]
                        newpoi['var_names'][k] = vname
                        varstr = varstr + '+' + vname
                        newpoi['C'+str(k)] = ToValueInt
                #size高级编程
                program_str = ''
                if cnode.hasAttribute('Program'):
                    program_str = cnode.getAttribute('Program')
                if cnode.hasAttribute('SizeProgram'):
                    SpStr = cnode.getAttribute('SizeProgram')
                    LUAFILE = RootPath + '\\Program\\'
                    luafile1 = LUAFILE + SpStr
                    codefile = open(luafile1, 'r')
                    code = codefile.read()
                    obj = {'X': newpoi['x'],  # X
                           'Y': newpoi['y'],  # Y
                           'Z': newpoi['z'],  # Z
                           'L': newpoi['l'],  # 宽
                           'D': newpoi['p'],  # 深
                           'H': newpoi['h'],  # 高
                           'OZ':newpoi['oz'],  # OZ旋转
                           }
                    SizeProgramStr = CompileLuaProgram(obj, luafile1)
               
                    if SizeProgramStr != '':
                        SizeProgramStr = SizeProgramStr[1:len(SizeProgramStr) - 1]
                        Sizeprogramstrlist = SizeProgramStr.split(',')
                        Sizeattridict = {}
                        for Sizeprogramstrlistchild in Sizeprogramstrlist:
                            Sizeattrilist = Sizeprogramstrlistchild.split(':')
                            Sizeattridict[Sizeattrilist[0]] = Sizeattrilist[1]
                        if 'X' in Sizeattridict:
                            newpoi['x'] = Sizeattridict['X']
                        if 'Y' in Sizeattridict:
                            newpoi['y'] = Sizeattridict['Y']
                        if 'Z' in Sizeattridict:
                            newpoi['z'] = Sizeattridict['Z']
                        if 'L' in Sizeattridict:
                            newpoi['l'] = Sizeattridict['L']
                        if 'P' in Sizeattridict:
                            newpoi['p'] = Sizeattridict['P']
                        if 'H' in Sizeattridict:
                            newpoi['h'] = Sizeattridict['H']
                        if 'OZ' in Sizeattridict:
                            newpoi['oz'] = Sizeattridict['OZ']
                di = 0
                if cnode.hasAttribute('DI'):
                    di = int(float(cnode.getAttribute('DI')))
                newpoi['DI'] = di
                newpoi['direct'] = di
                newpoi['mat'] = ''
                if cnode.hasAttribute('材料'):
                    newpoi['mat'] = cnode.getAttribute('材料')
                if newpoi['mat'] == '':
                    if textureclass == param['textureclass']:
                        newpoi['mat'] = param['pmat']
                newpoi['color'] = ''
                if cnode.hasAttribute('颜色'):
                    newpoi['color'] = cnode.getAttribute('颜色')
                if newpoi['color'] == '':
                    if textureclass == param['textureclass']:
                        newpoi['color'] = param['pcolor']
                        newpoi['颜色'] = newpoi['color']
                newpoi['desc'] = ''
                if cnode.hasAttribute('类别'):
                    newpoi['desc'] = cnode.getAttribute('类别')
                newpoi['类别'] = newpoi['desc']
                if cnode.hasAttribute('编码'):
                    newpoi['code'] = cnode.getAttribute('编码')
                if cnode.hasAttribute('工艺'):
                    newpoi['process'] = cnode.getAttribute('工艺')
                ls = ''
                if cnode.hasAttribute('UI'):
                    if cnode.getAttribute('UI') == '拉手':
                        ls = ls +newpoi['name']+','
                    if cnode.getAttribute('UI') == '拉手集合':
                        newpoi['memo'] = newpoi['memo'] + ls
                        newpoi['ls'] = ls
                newpoi['lgflag'] = 0
                newpoi['LgwjFlag'] = '0'
                if cnode.hasAttribute('LgwjFlag'):
                    newpoi['LgwjFlag'] = cnode.getAttribute('LgwjFlag')
                    if cnode.getAttribute('LgwjFlag') == '1':
                        newpoi['lgflag'] = 1
                if cnode.hasAttribute('ClipSelect'):
                    newpoi['ClipSelect'] = cnode.getAttribute('ClipSelect')
                newpoi['holetype'] = 0
                newpoi['HoleType'] = '0'
                if cnode.hasAttribute('HoleType'):
                    newpoi['HoleType'] = cnode.getAttribute('HoleType')
                newpoi['HoleFlag'] = '0'
                if cnode.hasAttribute('HoleFlag'):
                    newpoi['HoleFlag'] = cnode.getAttribute('HoleFlag')
                newpoi['Mark'] = '0'
                if cnode.hasAttribute('Mark'):
                    newpoi['Mark'] = cnode.getAttribute('Mark')
                newpoi['LMIN'] = '0'
                if cnode.hasAttribute('LMIN'):
                    newpoi['LMIN'] = cnode.getAttribute('LMIN')
                newpoi['LMAX'] = '0'
                if cnode.hasAttribute('LMAX'):
                    newpoi['LMAX'] = cnode.getAttribute('LMAX')
                newpoi['HMIN'] = '0'
                if cnode.hasAttribute('HMIN'):
                    newpoi['HMIN'] = cnode.getAttribute('HMIN')
                newpoi['HMAX'] = '0'
                if cnode.hasAttribute('HMAX'):
                    newpoi['HMAX'] = cnode.getAttribute('HMAX')
                newpoi['GUID'] = ''
                if cnode.hasAttribute('GUID'):
                    newpoi['GUID'] = cnode.getAttribute('GUID')
                newpoi['Dlgt'] = '0'
                if cnode.hasAttribute('Dlgt'):
                    newpoi['Dlgt'] = cnode.getAttribute('Dlgt')
                newpoi['DMIN'] = '0'
                if cnode.hasAttribute('DMIN'):
                    newpoi['DMIN'] = cnode.getAttribute('DMIN')
                newpoi['DMAX'] = '0'
                if cnode.hasAttribute('DMAX'):
                    newpoi['DMAX'] = cnode.getAttribute('DMAX')
                if cnode.hasAttribute('BT_PID'):
                    newpoi['BT_PID'] = cnode.getAttribute('BT_PID')
                if cnode.hasAttribute('BT_ID'):
                    newpoi['BT_ID'] = cnode.getAttribute('BT_ID')
                if cnode.hasAttribute('链接'):
                    newpoi['链接'] = cnode.getAttribute('链接')
                if cnode.hasAttribute('holetype'):
                    if cnode.getAttribute('holetype') != '':
                        newpoi['holetype'] = int(cnode.getAttribute('holetype'))
                autodirect = 0
                if cnode.hasAttribute('autodirect'):
                    if cnode.getAttribute('autodirect') != '':
                        autodirect = cnode.getAttribute('autodirect')
                if cnode.hasAttribute('HC'): #// 动态判定HoleConfig是否要计算
                    if cnode.getAttribute('HC') !='':
                        SetIsCalcHoleConfig(newpoi, cnode.getAttribute('HC'))
                newpoi['bdxmlid'] = ''
                if cnode.hasAttribute('BDXMLID'):
                    if cnode.getAttribute('BDXMLID') != '':
                        newpoi['bdxmlid'] = cnode.getAttribute('BDXMLID')
                if cnode.hasAttribute('HI'):
                    if cnode.getAttribute('HI') != '':
                        HI = urllib.parse.unquote(cnode.getAttribute('HI'))
                        newpoi['holeinfo'] = HI
                newpoi['extend'] = ''
                if cnode.hasAttribute('Extend'):
                    if cnode.getAttribute('Extend') != '':
                        newpoi['extend'] = cnode.getAttribute('Extend')
                newpoi['group'] = ''
                if cnode.hasAttribute('Group'):
                    if cnode.getAttribute('Group') != '':
                        pbom['group'] = '%s-%s' % (cnode.getAttribute('Group'), strtomd5(uid.uuid1()))
                newpoi['分组'] = ''
                if cnode.hasAttribute('分组'):
                    newpoi['分组'] = cnode.getAttribute('分组')
                newpoi['VP'] = '0'
                if cnode.hasAttribute('VP'):
                    newpoi['VP'] = cnode.getAttribute('VP')
                newpoi['UI'] = ''
                if cnode.hasAttribute('UI'):
                    newpoi['UI'] = cnode.getAttribute('UI')
                if cnode.hasAttribute('图形参数'):
                    if cnode.getAttribute('图形参数') != '':
                        SetBGParam(newpoi, cnode.getAttribute('图形参数'))
                newpoi['lfb'] = 0
                newpoi['llk'] = 0
                newpoi['wfb']= 0
                newpoi['wlk'] = 0
                newpoi['gno']= param['gno']
                newpoi['gdes']= param['gdes']
                newpoi['gcb'] = param['gcb']
                newpoi['extra'] = param['extra']
                newpoi['user_fbstr'] = ''
                if cnode.hasAttribute('FBSTR'):
                    newpoi['user_fbstr'] =cnode.getAttribute('FBSTR')
                if (newpoi['user_fbstr'] != '') :
                    newpoi['llk'], newpoi['wlk'], newpoi['llfb'], newpoi['rrfb'], newpoi['ddfb'], newpoi['uufb'],newpoi['fb'], newpoi['fbstr'] = FBStr2Value(
                        newpoi['user_fbstr'], newpoi['llk'], newpoi['wlk'], newpoi['llfb'], newpoi['rrfb'], newpoi['ddfb'], newpoi['uufb'], newpoi['fb'], newpoi['fbstr'])
                newpoi['value_lsk'] = 0
                newpoi['value_rsk'] = 0
                newpoi['value_zk'] = 0
                newpoi['value_zs'] = 0
                newpoi['value_ls'] = 0
                newpoi['value_lg'] = 0
                newpoi['value_ltm'] = 0
                newpoi['value_rtm'] = 0
                SetSysVariantValueForOrderItem(varstr, newpoi)
                # if newpoi['guid']== '8DCAA76C873F4215DAD533E6A5BB1CEA':
                #     print 'poi=',newpoi['value_lg']
                #     exit(1)
                newpoi['num'] = 1
                if cnode.hasAttribute('Num'):
                    newpoi['num'] = int(cnode.getAttribute('Num'))*param['num']
                newpoi['mark'] = 0
                if cnode.hasAttribute('Mark'):
                    newpoi['mark'] = int(cnode.getAttribute('Mark'))
                if cnode.hasAttribute('Memo'):
                    newpoi['memo'] = cnode.getAttribute('Memo')
                newpoi['userdefine'] = ''
                if cnode.hasAttribute('UD'):
                    newpoi['userdefine'] = cnode.getAttribute('UD')
                if cnode.hasAttribute('VP'):
                    newpoi['vp'] =int(float(cnode.getAttribute('VP')))
                newpoi['blockmemo'] = ''
                Result = Result + 1
                Des2Des(newpoi)
                bomlist.append(newpoi)
                # sMKobjb = {}
                # sMKobjb[u'我的模块'] = newpoi[u'我的模块']
                # sMKobjb[u'变量列表'] = newpoi[u'变量列表']
                childxml = ''
                id = id + 1
                firstchild = getfirstchild(cnode)
                if firstchild:
                    childxml = firstchild.toxml('UTF-8')
                real_l = newpoi['l']
                real_d = newpoi['p']
                if newpoi['oz'] == '0':
                    newpoi['oz'] = 0
                if (tmp_subspace == 'L') : #// L面空间，进行旋转计算
                    if (newpoi['var_args'][0] == 1) :
                        newpoi['oz'] = arctan((real_d - newpoi['var_args'][2]) / (real_l - newpoi['var_args'][1])) / pi * 180  #// 旋转角度
                        newpoi['p'] = newpoi['var_args'][3] #// 深度
                        t = sqrt((real_l - newpoi['var_args'][1]) * (real_l - newpoi['var_args'][1]) + (real_d - newpoi['var_args'][2]) * (
                                    real_d - newpoi['var_args'][2]))
                        newpoi['l'] = Delphi_Round(t) #// 宽度
                        newpoi['x'] = Delphi_Round(newpoi['var_args'][1] - newpoi['var_args'][3] * (real_d - newpoi['var_args'][2]) / t) #// x
                        newpoi['y'] = Delphi_Round(real_d - newpoi['var_args'][3] * (real_l - newpoi['var_args'][1]) / t)  #; // y
                        if newpoi['var_args'][4] != 0 : newpoi['l'] = newpoi['var_args'][4]
                        newpoi['lx'] = newpoi['x']
                        newpoi['ly'] = newpoi['y']
                    else:
                        newpoi['oz'] = 0
                if (tmp_subspace == 'R') : #// R面空间，进行旋转计算
                    if (newpoi['var_args'][0] == 1):
                        newpoi['oz'] = -arctan(
                            (real_d - newpoi['var_args'][2]) / (real_l - newpoi['var_args'][1])) / pi * 180  # // 旋转角度
                        newpoi['p'] = newpoi['var_args'][3]  # // 深度
                        t = sqrt((real_l - newpoi['var_args'][1]) * (real_l - newpoi['var_args'][1]) + (
                                    real_d - newpoi['var_args'][2]) * (
                                         real_d - newpoi['var_args'][2]))
                        newpoi['l'] = Delphi_Round(t)  # // 宽度
                        newpoi['x'] = newpoi['x'] +round(newpoi['var_args'][3]  * (
                                    real_d - newpoi['var_args'][1]) / t)  # // x
                        newpoi['y'] = Delphi_Round(newpoi['var_args'][2]-newpoi['var_args'][3] * (real_l - newpoi['var_args'][1]) / t)  # ; // y
                        if newpoi['var_args'][4] != 0: newpoi['l'] = newpoi['var_args'][4]
                        newpoi['lx'] = newpoi['x']
                        newpoi['ly'] = newpoi['y']
                    else:
                        newpoi['oz'] = 0
                newpoi['tmp_soz'] = param['sozflag']
                tmp_soz = param['sozflag']
                if tmp_subspace !='': tmp_soz =''
                if (tmp_subspace == '') and (float(newpoi['oz']) != 0) : tmp_soz = str(param['sozflag']) + ('@%d_%d'%(funcid(newpoi),float(newpoi['oz'])))
                childnum = 0
                newpoi['boardheight'] = param['boardheight']
                newpoi['pricecalctype'] = param['pricecalctype']
                newpoi['Program'] = program_str
                sMKobjb = {}
                InitPriceJson(sMKobjb, newpoi)
                if cnode.hasAttribute('BJSize'):
                    BJSize = cnode.getAttribute('BJSize')
                    GraphSizeToBJSize(BJSize, sMKobjb)
                log.debug(json.dumps(sMKobjb, ensure_ascii=False))
                if bg == 'BG::DOORRECT':
                    sMKobjb['l'] = sMKobjb['l'] + args[0] + args[1]
                    sMKobjb['h'] = sMKobjb['h'] + args[2] + args[3]
                #sMKobjb = copy.deepcopy(newpoi)
                if childxml != '':
                    param2 = {}
                    for key, value in list(param.items()):
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
                    param2['sozflag'] = tmp_soz
                    param2['xml'] = childxml
                    param2['textureclass'] = textureclass
                    param2['pmat'] = newpoi['mat']
                    param2['pcolor'] = newpoi['color']
                    param2['pid'] = id - 1
                    param2['mark']= newpoi['mark']
                    param2['pl'] = newpoi['l']
                    param2['pd'] = newpoi['p']
                    param2['ph'] = newpoi['h']
                    param2['px'] = newpoi['x']
                    param2['py'] = newpoi['y']
                    param2['pz'] = newpoi['z']
                    param2['space_x'] = tmp_space_x
                    param2['space_y'] = tmp_space_y
                    param2['space_z'] = tmp_space_z
                    if spaceflag == '1':
                        param2['space_id'] = newpoi['id']
                    else:
                        param2['space_id'] = param['space_id']
                    param2['num'] = newpoi['num']
                    param2['parent'] = newpoi
                    if newpoi['number_text'] != '':
                        param2['number_text'] = newpoi['number_text']
                    if cnode.hasAttribute('输出类型'):
                        param2['outputtype'] = cnode.getAttribute('输出类型')
                        sMKobjb['outputtype'] = cnode.getAttribute('输出类型')
                    child = getfirstchild(cnode)
                    if child:
                        param2['rootnode'] = child
                        param2['xdoc'] = param['xdoc']
                        childnum = ImportXomItemForBom(param2, sMKobjb)
                if program_str:
                    ImportCloneItemForBom(Var, program_str, newpoi, cnode, param, id, slino, mkJs)
                    #FunctionAddProgram1(newpoi,param,cnode,mkJs)
                bl, bp, bh = GraphSizeToBomSize(newpoi['l'], newpoi['p'], newpoi['h'], newpoi['direct'])
                sMKobjb['l'] = bl
                sMKobjb['p'] = bp
                sMKobjb['h'] = bh
                newpoi['gcl2'], newpoi['gcd2'], newpoi['gch2'] = GraphSizeToBomSize1(newpoi['gcl'], newpoi['gcd'], newpoi['gch'], newpoi['direct'], newpoi['gcl2'], newpoi['gcd2'], newpoi['gch2'])
                if (autodirect == 1) and (bp > 1220) : #// 自动纹路转换
                    di = TextureDirectChange(di)
                    newpoi['direct'] = di
                    bl, bp, bh = GraphSizeToBomSize(newpoi['l'], newpoi['p'], newpoi['h'], newpoi['direct'])
                    newpoi['gcl2'], newpoi['gcd2'], newpoi['gch2'] = GraphSizeToBomSize1(newpoi['gcl'], newpoi['gcd'], newpoi['gch'], newpoi['direct'], newpoi['gcl2'], newpoi['gcd2'], newpoi['gch2'])
                newpoi['gl'] = newpoi['l']
                newpoi['gp'] = newpoi['p']
                newpoi['gh'] = newpoi['h']
                newpoi['l'] = bl
                newpoi['p'] = bp
                newpoi['h'] = bh
                if bh <= 36: sMKobjb['bh'] = bh
                newpoi['bl'] = int(bl) - int(newpoi['lfb']) - int(newpoi['llk'])
                newpoi['bp'] = int(bp) - int(newpoi['wfb']) - int(newpoi['wlk'])
                newpoi['bh'] = int(bh)
                if childnum==None:
                    childnum = 0
                newpoi['childnum'] = childnum
                sMKobjb['childnum'] = childnum
                if cnode.hasAttribute('装饰类别'):
                    attri = cnode.getAttribute('装饰类别')
                    if attri != '' and (attri == '趟门' or attri == '掩门' or (newpoi['myclass'] == '趟门,趟门') or \
                                        (newpoi['myclass'] == '掩门,掩门')):
                        newpoi['isoutput'] = False
                if (int(newpoi['bl']) < 1) or (int(newpoi['bp']) < 1) or (int(newpoi['bh']) < 1) : newpoi['isoutput'] = False #// 过滤掉尺寸小于等于零的物料，xml情况复杂
                if (int(newpoi['bl']) > 1) and (int(newpoi['bp']) > 1) and (int(newpoi['bh']) <= 1) : newpoi['isoutput'] = False #// 过滤掉一些尺寸为0的物料数据
                #尺寸判定
                sMKobjb['isoutput'] = newpoi['isoutput']
                newpoi['bomstd'] = ToBomStd(newpoi['bomstddes'], newpoi['l'], newpoi['p'], newpoi['h'])
                if childnum > 0 :
                    ## 'hhahahah'
                    newpoi['isoutput'] = False
                newpoi['outputtype'] = ''
                if cnode.hasAttribute('输出类型'):
                    newpoi['outputtype'] = cnode.getAttribute('输出类型')
                sMKobjb['outputtype'] = newpoi['outputtype']
                mkJs.append(sMKobjb)
            AllPrice["我的模块"] = mkJs
    return Result
def RemoveInvisibleNode(root):
    def EnumChild(node):
        for i in range(len(node.childNodes)-1,-1,-1):
            cnode = node.childNodes[i]
            if node.nodeName == '我的模块' :
                if cnode.nodeType == 1:
                    string =cnode.getAttribute('显示方式')
                    #string= cnode.getAttribute(u'显示方式')
                    if string == '3' :
                        node.childNodes.remove(cnode)
                        continue
            EnumChild(node.childNodes[i])
    EnumChild(root)
def CombineWallNode(root):
    find = False
    l = 5000
    d = 5000
    h = 3000
    for i in range(0,len(root.childNodes)):
        node = root.childNodes[i]
        if (node.nodeName == '房型') :
            l = l if node.getAttribute('宽')=='' else int(node.getAttribute('宽'))
            d = d if node.getAttribute('深')=='' else int(node.getAttribute('深'))
            h = h if node.getAttribute('高')=='' else int(node.getAttribute('高'))
        if (node.nodeName != '产品'): continue
        dbid = node.getAttribute('DBID')
        if dbid[:6]=='#Wall_' : find = True
        if find : break
    if not find : return
    xml = '<产品 名称="全屋空间" DBID="#Wall_All" X="0" Y="0" Z="0" 宽="%d" 深="%d" 高="%d" OX="0" OY="0" OZ="0" 装饰类别="板材" 空间类型="复合空间">'%(l, d, h)
    xml = xml + '<产品 名称="全屋空间" X="0" Y="0" Z="0" 宽="%d" 深="%d" 高="%d" OX="0" OY="0" OZ="0" 装饰类别="板材" 空间类型="复合空间">'%(l, d, h)
    xml = xml + '<我的模块></我的模块></产品></产品>'
    DOMTree = minidom.parseString(xml)
    newnode = DOMTree.getElementsByTagName('产品')[0] #产品节点
    newnode2 = newnode.childNodes[0]   #产品节点
    for child in newnode2.childNodes:
        if child.nodeName =='我的模块':
            newnode2 = child
            continue
    #root 场景结点
    for i in range(len(root.childNodes)-1, -1, -1):
        node = root.childNodes[i]
        if node.nodeType!=1:continue
        if (node.nodeName != '产品') : continue
        dbid = node.getAttribute('DBID')
        if dbid[0: 6]=='#Wall_':
            xml2 = '<模块'
            for name, value in list(node.attributes.items()):
                xml2 = xml2 + ' %s="%s"'%(name, value)
            for child in node.childNodes:    #找到第一个节点
                if child.nodeType!=1: continue
                node2 = child
                continue
            for name, value in list(node2.attributes.items()): #清空节点属性
                node2.removeAttribute(name)
            xml2 = xml2 + '>' + node2.toxml('UTF-8') + '</模块>'
            DOMTree = minidom.parseString(xml2)
            node2 = DOMTree.getElementsByTagName('模块')[0]  # 产品节点
            newnode2.appendChild(node2)
            root.childNodes.remove(node)
    root.appendChild(newnode)
def LoadXMLFile2Bom(xml):
    global cid,bomlist,id,slino,mProductList, doorslist, slidinglist, JsonPrice,\
    des2wuliaodict,holeconfigHash,childbomHash,wjruleHash,mBDXMLList,\
    ruleHash,kcconfigHash,childxml,mTmpExp,mXMLStringList,mDoorList,bomstdList
    mProductList, bomlist, doorlist, slidinglist, mXMLStringList, mDoorList = [], [], [], [], [], []
    mBDXMLList = {}
    productdatadict = {}
    JsonPrice = {"柜体列表": []}
    childxml = {}
    mTmpExp = {}
    DOMTree = xml.dom.minidom.parse(xmlfile)#xmlfilepath+xmlfile
    collection = DOMTree.documentElement
    root = DOMTree.getElementsByTagName('订单')[0]
    RemoveInvisibleNode(root)  #清除显示方式为3 的节点
    CombineWallNode(root)
    id = 1
    slino = 1
    cid = 0
    j = 0
    for i in range(0,root.childNodes.length):
        node = root.childNodes[i]
        if node.nodeType == 1:
            if node.nodeName != '产品':
                continue
            #判断是否存在该产品
            if not os.path.exists(base_dir+'\\Python\\Webcache\\'):
                os.makedirs(base_dir+'\\Python\\Webcache\\')
            m2 = hashlib.md5()
            m2.update(node.toxml('UTF-8'))
            productdata = m2.hexdigest()
            productdatadict[productdata] = j
            if os.path.exists(base_dir + '\\Python\\Webcache\\'+productdata):
                j = j+1
                continue
            name = ''
            l = 0
            d = 0
            h = 0
            textureclass = ''
            X = 0
            Y = 0
            Z = 0
            OX = 0
            OY = 0
            OZ = 0
            ID = ''
            IDSTR = ''
            bh = 18
            mat = ''
            color = ''
            des = ''
            gcb = ''
            extra = ''
            spaceflag = '' #默认
            guid = ''
            if node.childNodes[1].hasAttribute('板材厚度'):
                bh = node.childNodes[1].getAttribute('板材厚度')
            if node.hasAttribute('板材厚度'):
                bh = node.getAttribute('板材厚度')
            if node.childNodes[1].getAttribute('Extra') == '':
                pass
            else:
                extra= node.childNodes[1].getAttribute('Extra')
            if node.hasAttribute('名称') :
                name = node.getAttribute('名称')
            if node.hasAttribute('描述') :
                des = node.getAttribute('描述')
            if node.hasAttribute('CB') :
                gcb = node.getAttribute('CB')
            if node.hasAttribute('宽') :
                l = int(node.getAttribute('宽'))
            if node.hasAttribute('深') :
                d = int(node.getAttribute('深'))
            if node.hasAttribute('高') :
                h = int(node.getAttribute('高'))
            if node.hasAttribute('材料') :
                mat = node.getAttribute('材料')
            if node.hasAttribute('颜色') :
                color = node.getAttribute('颜色')
            if node.hasAttribute('基础图形') :
                mBG = node.getAttribute('基础图形')
            if node.hasAttribute('SpaceFlag') :
                spaceflag = node.getAttribute('SpaceFlag')
            if node.hasAttribute('guid') :
                guid = node.getAttribute('guid')
            if node.hasAttribute('装饰类别') :
                textureclass = node.getAttribute('装饰类别')
            if node.hasAttribute('X') :
                X = node.getAttribute('X')
            if node.hasAttribute('Y'):
                Y = node.getAttribute('Y')
            if node.hasAttribute('Z') :
                Z = node.getAttribute('Z')
            if node.hasAttribute('OX') :
                OX = node.getAttribute('OX')
            if node.hasAttribute('OY') :
                OY = node.getAttribute('OY')
            if node.hasAttribute('OZ') :
                OZ = node.getAttribute('OZ')
            if node.hasAttribute('ID') :
                ID = node.getAttribute('ID')
            if node.hasAttribute('IDSTR') :
                IDSTR = node.getAttribute('IDSTR')
            if bh != 18 and IDSTR!='':
                bh = 16
                OneSapce = {"板材厚度":16,  "IDSTR":IDSTR}
                Jsondata['Space16mm'].append(OneSapce)
            LMIN = '1'
            LMAX = '10000'
            HMIN = '1'
            HMAX = '10000'
            DMIN = '1'
            DMAX = '10000'
            DBID = ''
            IsRoomSpace = ''
            BomOnePrice = ''
            if node.hasAttribute('LMIN'):
                LMIN = node.getAttribute('LMIN')
            if node.hasAttribute('LMAX'):
                LMAX = node.getAttribute('LMAX')
            if node.hasAttribute('HMIN'):
                HMIN = node.getAttribute('HMIN')
            if node.hasAttribute('HMAX'):
                HMAX = node.getAttribute('HMAX')
            if node.hasAttribute('DMIN'):
                DMIN = node.getAttribute('DMIN')
            if node.hasAttribute('DMAX'):
                DMAX = node.getAttribute('DMAX')
            if node.hasAttribute('IDSTR'):
                IDSTR = node.getAttribute('IDSTR')
            if node.hasAttribute('DBID'):
                DBID = node.getAttribute('DBID')
            if node.hasAttribute('IsRoomSpace'):
                IsRoomSpace = node.getAttribute('IsRoomSpace')
            if node.hasAttribute('板材单价'):
                BomOnePrice = node.getAttribute('板材单价')
            #    'SpaceFlag 不清楚'
            p = {}
            p['id'] = cid
            p['name'] = name
            p['gno'] = name
            p['mat'] = mat
            p['color'] = color
            p['des'] = des
            p['gcb'] = gcb
            p['Extra'] = extra
            p['l'] = l
            p['d'] = d
            p['h'] = h
            p['bh'] = bh
            p['guid'] = guid
            cid = cid + 1
            mProductList.append(p)
            param={}
            #param 为产品
            param['productid'] = len(mProductList)
            param['cid'] = cid - 1
            param['boardheight'] = bh
            param['blist'] = bomlist
            param['gno'] = name
            param['guid'] = guid
            param['gdes'] = des
            param['gcb'] = gcb
            param['extra'] = extra
            param['pname'] = ''
            param['subspace'] = ''
            param['sozflag'] = ''
            param['xml'] = node.childNodes[1].toxml('UTF-8')
            param['textureclass'] = ''
            param['pmat'] = mat
            param['pcolor'] = color
            param['pid'] = -1
            param['pl'] = l
            param['pd'] = d
            param['ph'] = h
            param['px'] = 0
            param['py'] = 0
            param['pz'] = 0
            param['space_x'] = 0
            param['space_y'] = 0
            param['space_z'] = 0
            if spaceflag=='1':
                param['space_id'] = 0
            else:
                param['space_id'] = -1
            param['outputtype'] = ''
            param['num'] = 1
            param['parent'] = None
            param['blockmemo'] = ''
            param['number_text'] = ''
            param['rootnode'] = node.childNodes[1]
            param['xdoc'] = DOMTree
            AllPrice = {
                "装饰类别": textureclass,
                "高": h,
                "深": d,
                "宽": l,
                "Z": Z,
                "Y": Y,
                "X": X,
                "#": 1,
                "IDSTR": IDSTR,
                "颜色": color,
                "材料": mat,
                "描述": des,
                "名称": name,
                "OZ": OZ,
                "OY": OY,
                "OX": OX,
                "ID": ID,
                "Type": "柜体空间",
                "LMIN": LMIN,
                "LMAX": LMAX,
                "HMIN": HMIN,
                "HMAX": HMAX,
                "DMIN": DMIN,
                "DMAX": DMAX,
                "DBID": DBID,
                "IsRoomSpace": IsRoomSpace,
                "板材单价": BomOnePrice
            }
            ImportXomItemForBom(param, AllPrice)
            JsonPrice['柜体列表'].append(AllPrice)
            j = j+1
    #Jsondata["JsonPrice"] = JsonPrice
    ## len(blist),id,json.dumps(blist,ensure_ascii=False)
    #// 拆分数量
    for i in range(len(bomlist)-1,-1,-1):
        poi = bomlist[i]
        if poi['num'] > 1 :
            for j in range(1,poi['num']):
                poi2 = {}
                for key, value in list(poi.items()):
                    poi2[key] = value
                poi2['num'] = 1
                bomlist.append(poi2)
            poi['num'] = 1
    print('len of holeconfigHash',len(holeconfigHash))
    return mProductList,bomlist,doorslist,slidinglist,mBDXMLList,JsonPrice,productdatadict

def InitRootPathConfig(Path):
    global gFormatPrecision, gFormatPrecision2, gQDBomFlag, mPicWidth2, mPicHeight2, mExportDir,\
        StanleyDict, X2dToBdGraphj, gBGHash, gPluginsList, seqInfoHash, classseqInfoHash, \
    workflowlist, gBoardMatList, gErpItemList, mIIHoleCalcRule,mDoorPrecision, gROC, mJoBarCode
    cf = configparser.ConfigParser()
    confPath = RootPath + '\\qd.conf'
    copyconffile = RootPath + '\\copyqd.conf'
    #配置
    if os.path.exists(confPath):
        with open(copyconffile, 'w+') as f:
            with open(confPath, 'r') as f1:
                content = f1.read()
                content = content.replace('//', '#')
            f.write(content)
        cf.read(copyconffile)
        try:
            gFormatPrecision = cf.get("BarCode".encode('gb2312'), "B_BPP".encode('gb2312'))
        except:
            gFormatPrecision = 2
        try:
            gFormatPrecision2 = cf.get("BarCode".encode('gb2312'), "B_BPP".encode('gb2312'))
        except:
            gFormatPrecision2 = 2
        try:
            gQDBomFlag = cf.get("QuickDraw".encode('gb2312'), "QDBomFlag".encode('gb2312'))
        except:
            gQDBomFlag = 1
        try:
            mDoorPrecision = cf.get("QuickDraw".encode('gb2312'), "DoorPrecision".encode('gb2312'))
        except:
            mDoorPrecision = 0
        try:
            db_host = cf.get("孔位计算规则".encode('gb2312'), "通孔计算".encode('gb2312'))
        except:
            db_host = '{}'
        try:
            mJoBarcode = cf.get("BarCode".encode('gb2312'), "A_MPR".encode('gb2312'))
            mJoBarCode['A_MPR'] = ToBarCode({}, mJoBarcode)
        except:
            mJoBarCode['A_MPR'] = ''
        try:
            mJoBarcode = cf.get("BarCode".encode('gb2312'), "B_MPR".encode('gb2312'))
            mJoBarCode['B_MPR'] = ToBarCode({}, mJoBarcode)
        except:
            mJoBarCode['B_MPR'] = ''
        try:
            mJoBarcode = cf.get("BarCode".encode('gb2312'), "AB_BPP".encode('gb2312'))
            mJoBarCode['AB_BPP'] = ToBarCode({}, mJoBarcode)
        except:
            mJoBarCode['AB_BPP'] = ''
        try:
            mJoBarcode = cf.get("BarCode".encode('gb2312'), "A_BPP".encode('gb2312'))
            mJoBarCode['A_BPP'] = ToBarCode({}, mJoBarcode)
        except:
            mJoBarCode['A_BPP'] = ''
        try:
            mJoBarcode = cf.get("BarCode".encode('gb2312'), "B_BPP".encode('gb2312'))
            mJoBarCode['B_BPP'] = ToBarCode({}, mJoBarcode)
        except:
            mJoBarCode['B_BPP'] = ''
        try:
            mJoBarcode = cf.get("BarCode".encode('gb2312'), "DXF".encode('gb2312'))
            mJoBarCode['DXF'] = ToBarCode({}, mJoBarcode)
        except:
            mJoBarCode['DXF'] = ''
        try:
            mJoBarcode = cf.get("BarCode".encode('gb2312'), "BDFILE".encode('gb2312'))
            mJoBarCode['BDFILE'] = ToBarCode({}, mJoBarcode)
        except:
            mJoBarCode['BDFILE'] = ''
        mIIHoleCalcRule = json.loads(db_host)
        os.remove(copyconffile)
    confPath = RootPath + '\\qd.ini'
    copyconffile = RootPath + '\\copyqd.ini'
    if os.path.exists(confPath):
        with open(copyconffile, 'w+') as f:
            with open(confPath, 'r') as f1:
                content = f1.read()
                content = content.replace('//', '#')
            f.write(content)
        cf.read(copyconffile)
        try:
            mPicWidth2 = cf.get("SlidingDesign".encode('gb2312'), "PicWidth2".encode('gb2312'))
        except:
            mPicWidth2 = 700
        try:
            mPicHeight2 = cf.get("SlidingDesign".encode('gb2312'), "PicHeight2".encode('gb2312'))
        except:
            mPicHeight2 = 400
        try:
            mExportDir = cf.get('QdBom', 'ExportDir')
        except:
            mExportDir = RootPath + '\\' + 'Temp' + '\\'
        os.remove(copyconffile)
    #路径
    dataDBfile = RootPath + '\\Plugins\\data\\stanley.mdb'
    if os.path.exists(dataDBfile):
        #数据库
        conn = pypyodbc.win_connect_mdb(r'DRIVER={Microsoft Access Driver (*.mdb  *.accbd)};DBQ=' + dataDBfile)
        cur = conn.cursor()
        sql = 'select * from data order by id'
        cur.execute(sql)
        StanleyDict = {}
        StanleyU = cur.fetchall()
        for StanleyI in StanleyU:
            StanleyDict[StanleyI[1]] = StanleyI[2]
    #变量
    X2dToBdGraphj = 0
    #初始化文件数据
    gBGHash, gPluginsList, seqInfoHash, classseqInfoHash, \
    workflowlist, gBoardMatList, gErpItemList, gROC= InitData(Path)
    print('len of gBGHash=', len(gBGHash))
    print('len of gPluginsList=', len(gPluginsList))
    print('len of seqInfoHash=', len(seqInfoHash))
    print('len of classseqInfoHash=', len(classseqInfoHash))
    print('len of workflowlist=', len(workflowlist))
    print('len of gBoardMatList=', len(gBoardMatList))
    print('len of gErpItemList=', len(gErpItemList))
    print('len of mIIHoleCalcRule=', len(mIIHoleCalcRule))
    print('len of mDoorPrecision=', mDoorPrecision)
    print('len of gROC=', gROC.bj_out_classname)
    print('len of mJoBarCode=', len(mJoBarCode))

def clearlist(name):
    '''
    :param name: list 对象
    :return:
    :目的：清空全局变量列表
    '''
    del name[:]

def InitGlobalData():
    clearlist(bomlist)  # 板材列表
    clearlist(mProductList)  # 柜体列表
    clearlist(doorslist)  # 掩门列表
    clearlist(slidinglist)  # 趟门门列表
    clearlist(desdoorlist)  # 掩门des字段列表
    clearlist(desslidinglist)  # 掩门des字段列表
    clearlist(des2price)  # 报价
    clearlist(bomstdList)  # 尺寸判断
    clearlist(mDoorList)  # 门数据
    clearlist(mXMLStringList)  # 门xml 列表
    JsonPrice.clear()  # 所有数据汇总
    QuoruleHash.clear()  # 报价数据
    classHash.clear()  # base_quotation_class 数据库数据
    productdatadict.clear()
    des2wuliaodict.clear()
    holeconfigHash.clear()
    childbomHash.clear()
    wjruleHash.clear()
    ruleHash.clear()
    kcconfigHash.clear()
    childxml.clear()
    mTmpExp.clear()
    mBDXMLList.clear()

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

def LoadXML2Bom(xmlfile, Path):
    global cid, id, slino, RootPath
    InitGlobalData()
    RootPath = Path
    InitRootPathConfig(RootPath)
    JsonPrice["柜体列表"] = []
    DOMTree = minidom.parse(xmlfile)
    node = DOMTree.documentElement
    RemoveInvisibleNode(node)
    InitSysVariantValue()
    id = 1
    slino = 1
    cid = 0
    j = 0
    # if not os.path.exists(base_dir+'\\Python\\Webcache\\'):
    #     os.makedirs(base_dir+'\\Python\\Webcache\\')
    # m2 = hashlib.md5()
    # m2.update(node.toxml('UTF-8'))
    # productdata = m2.hexdigest()
    # productdatadict[productdata] = j
    # if os.path.exists(base_dir + '\\Python\\Webcache\\'+productdata):
    #     j = j+1
    name = ''
    l = 0
    d = 0
    h = 0
    textureclass = ''
    X = 0
    Y = 0
    Z = 0
    OX = 0
    OY = 0
    OZ = 0
    ID = ''
    IDSTR = ''
    bh = 18
    mat = ''
    color = ''
    des = ''
    gcb = ''
    extra = ''
    spaceflag = ''  # 默认
    guid = ''
    firstchild = getfirstchild(node)
    if firstchild.nodeName == '产品':
        if firstchild.hasAttribute('板材厚度'):
            bh = firstchild.getAttribute('板材厚度')
        if firstchild.hasAttribute('Extra'):
            extra = firstchild.getAttribute('Extra')
    if node.hasAttribute('Extra'):
        if node.getAttribute('Extra'):
            extra = node.getAttribute('Extra')
    if node.hasAttribute('名称'):
        name = node.getAttribute('名称')
    if node.hasAttribute('描述'):
        des = node.getAttribute('描述')
    if node.hasAttribute('CB'):
        gcb = node.getAttribute('CB')
    if node.hasAttribute('宽'):
        l = int(node.getAttribute('宽'))
    if node.hasAttribute('深'):
        d = int(node.getAttribute('深'))
    if node.hasAttribute('高'):
        h = int(node.getAttribute('高'))
    if node.hasAttribute('材料'):
        mat = node.getAttribute('材料')
    if node.hasAttribute('颜色'):
        color = node.getAttribute('颜色')
    if node.hasAttribute('基础图形'):
        mBG = node.getAttribute('基础图形')
    if node.hasAttribute('SpaceFlag'):
        spaceflag = node.getAttribute('SpaceFlag')
    if node.hasAttribute('guid'):
        guid = node.getAttribute('guid')
    if node.hasAttribute('装饰类别'):
        textureclass = node.getAttribute('装饰类别')
    if node.hasAttribute('X'):
        X = node.getAttribute('X')
    if node.hasAttribute('Y'):
        Y = node.getAttribute('Y')
    if node.hasAttribute('Z'):
        Z = node.getAttribute('Z')
    if node.hasAttribute('OX'):
        OX = node.getAttribute('OX')
    if node.hasAttribute('OY'):
        OY = node.getAttribute('OY')
    if node.hasAttribute('OZ'):
        OZ = node.getAttribute('OZ')
    if node.hasAttribute('ID'):
        ID = node.getAttribute('ID')
    if node.hasAttribute('IDSTR'):
        IDSTR = node.getAttribute('IDSTR')
    if bh != 18 and IDSTR != '':
        bh = 16
        OneSapce = {"板材厚度": 16, "IDSTR": IDSTR}
        Jsondata['Space16mm'].append(OneSapce)
    LMIN = '1'
    LMAX = '10000'
    HMIN = '1'
    HMAX = '10000'
    DMIN = '1'
    DMAX = '10000'
    DBID = ''
    IsRoomSpace = ''
    BomOnePrice = ''
    if node.hasAttribute('LMIN'):
        LMIN = node.getAttribute('LMIN')
    if node.hasAttribute('LMAX'):
        LMAX = node.getAttribute('LMAX')
    if node.hasAttribute('HMIN'):
        HMIN = node.getAttribute('HMIN')
    if node.hasAttribute('HMAX'):
        HMAX = node.getAttribute('HMAX')
    if node.hasAttribute('DMIN'):
        DMIN = node.getAttribute('DMIN')
    if node.hasAttribute('DMAX'):
        DMAX = node.getAttribute('DMAX')
    if node.hasAttribute('IDSTR'):
        IDSTR = node.getAttribute('IDSTR')
    if node.hasAttribute('DBID'):
        DBID = node.getAttribute('DBID')
    if node.hasAttribute('IsRoomSpace'):
        IsRoomSpace = node.getAttribute('IsRoomSpace')
    if node.hasAttribute('板材单价'):
        BomOnePrice = node.getAttribute('板材单价')
    p = {}
    p['id'] = cid
    p['name'] = name
    p['gno'] = name
    p['mat'] = mat
    p['color'] = color
    p['des'] = des
    p['gcb'] = gcb
    p['Extra'] = extra
    p['l'] = l
    p['d'] = d
    p['h'] = h
    p['bh'] = bh
    p['guid'] = guid
    cid = cid + 1
    mProductList.append(p)
    param = {}
    # param 为产品
    param['productid'] = len(mProductList)
    param['cid'] = cid - 1
    param['boardheight'] = bh
    param['blist'] = bomlist
    param['gno'] = name
    param['guid'] = guid
    param['gdes'] = des
    param['gcb'] = gcb
    param['extra'] = extra
    param['pname'] = ''
    param['subspace'] = ''
    param['sozflag'] = ''
    param['xml'] = firstchild.toxml('UTF-8')
    param['textureclass'] = ''
    param['pmat'] = mat
    param['pcolor'] = color
    param['pid'] = -1
    param['pl'] = l
    param['pd'] = d
    param['ph'] = h
    param['px'] = 0
    param['py'] = 0
    param['pz'] = 0
    param['space_x'] = 0
    param['space_y'] = 0
    param['space_z'] = 0
    if spaceflag == '1':
        param['space_id'] = 0
    else:
        param['space_id'] = -1
    param['outputtype'] = ''
    param['pricecalctype'] = ''
    param['num'] = 1
    param['parent'] = None
    param['blockmemo'] = ''
    param['number_text'] = ''
    param['rootnode'] = firstchild
    param['xdoc'] = DOMTree
    AllPrice = {
        "装饰类别": textureclass,
        "高": h,
        "深": d,
        "宽": l,
        "Z": Z,
        "Y": Y,
        "X": X,
        "#": 1,
        "颜色": color,
        "材料": mat,
        "描述": des,
        "名称": name,
        "OZ": OZ,
        "OY": OY,
        "OX": OX,
        "ID": ID,
        "Type": "柜体空间",
        "DBID": DBID,
        "IsRoomSpace": IsRoomSpace,
        "板材单价": BomOnePrice
    }
    ImportXomItemForBom(param, AllPrice)
    JsonPrice['柜体列表'].append(AllPrice)
    # // 拆分数量
    for i in range(len(bomlist) - 1, -1, -1):
        poi = bomlist[i]
        if poi['num'] > 1:
            for j in range(1, poi['num']):
                poi2 = {}
                for key, value in list(poi.items()):
                    poi2[key] = value
                poi2['num'] = 1
                bomlist.append(poi2)
            poi['num'] = 1
    # for i in range(0, len(bomQuolist)):
    #     pbom = bomQuolist[i]
    #     QuoDes2Des(pbom)
    return mProductList, bomlist, desdoorlist, desslidinglist, mBDXMLList, JsonPrice, productdatadict, \
           workflowlist, mIIHoleCalcRule, mBDXMLList, gBGHash
# def OneQuoData2Json(des):
#     ResultJsonStr = ''
#     dataDBfile = RootPath + u'\\data\\data.mdb'
#     if des == '' or (not os.path.exists(dataDBfile)):
#         return ResultJsonStr
#     else:
#         conn, cur = connectdata(dataDBfile)
#         n = des.find(',')
#         s1 = des[:n].decode('utf8')
#         s2 = des[n + 1:].decode('utf8')
#         sql = (u"select * from base_quotation_class where [报价类别1]='%s' and [报价类别2]='%s' and deleted=False" % (
#             s1, s2))
#         cur.execute(sql)
#         jo = {}
#         ja = []
#         fjo = {}
#         quotationclassallu = cur.fetchall()
#
#         if quotationclassallu:
#             typelist = []
#             for tup in cur.description:
#                 typelist.append(tup[0])  # 编码gbk
#             for i in range(0, len(quotationclassallu)):
#                 fjo = getfjo(i, typelist, quotationclassallu)
#
#                 cjo = {}
#                 key = s1 + ',' + s2
#                 cjo['key'] = key
#
#                 cjo['bj1'] = fjo[u'报价类别1']  # 报价类别1
#                 cjo['bj2'] = fjo[u'报价类别2']  # 报价类别2
#                 cjo['pricetype'] = fjo[u'报价方式']  # type
#
#                 cjo['factor'] = Nonetonumber(fjo[u'价格系数'], 'F')
#                 cjo['myunit'] = fjo[u'单位']  # 单位
#                 cjo['myclass'] = fjo[u'分类']  # 分类
#                 cjo['is_calc_cost'] = fjo[u'is_calc_cost']  # 物料分类
#                 ja.append(cjo)
#         jo['classHash'] = ja
#         ja = []
#         sql = (
#                     u"select * from base_quotation_rule where [报价类别1]='%s' and [报价类别2]='%s' and deleted=False order by 报价类别1 asc, 报价类别2 asc, 是否非标 desc, [level] asc, 门板材料" % (
#                 s1, s2))
#         cur.execute(sql)
#         quotationruleallu = cur.fetchall()
#         if quotationruleallu != []:
#             typelist = []
#             quotationrule = {}
#             for tup in cur.description:
#                 typelist.append(tup[0])  # 编码gbk
#
#             for i in range(0, len(quotationruleallu)):
#                 quotationrule = getfjo(i, typelist, quotationruleallu)
#                 key = quotationrule[u'报价类别1'] + ',' + quotationrule[u'报价类别2']
#                 cjo = {}
#                 cjo['key'] = key
#
#                 cjo['bj1'] = quotationrule[u'报价类别1']  # 报价类别1
#                 cjo['bj2'] = quotationrule[u'报价类别2']  # 报价类别2
#                 cjo['l'] = Nonetonumber(quotationrule[u'l'])
#                 cjo['lmax'] = Nonetonumber(quotationrule[u'lmax'])
#                 cjo['lmin'] = Nonetonumber(quotationrule[u'lmin'])
#                 cjo['p'] = Nonetonumber(quotationrule[u'p'])
#                 cjo['pmax'] = Nonetonumber(quotationrule[u'pmax'])
#                 cjo['pmin'] = Nonetonumber(quotationrule[u'pmin'])
#                 cjo['h'] = Nonetonumber(quotationrule[u'h'])
#                 cjo['hmax'] = Nonetonumber(quotationrule[u'hmax'])
#                 cjo['hmin'] = Nonetonumber(quotationrule[u'hmin'])
#
#                 cjo['slidingmat'] = quotationrule[u'门板材料']
#                 cjo['isnonstandard'] = quotationrule[u'是否非标']
#
#                 cjo['id'] = Nonetonumber(quotationrule[u'id'])
#                 cjo['myclass'] = quotationrule[u'分类']
#                 cjo['PriceTable'] = quotationrule[u'报价方案']
#                 cjo['price1'] = quotationrule[u'价格1']
#                 cjo['price2'] = quotationrule[u'价格2']
#                 cjo['outname'] = quotationrule[u'outname']
#                 cjo['sale_type'] = quotationrule[u'sale_type']
#
#                 ja.append(cjo)
#         jo['ruleHash'] = ja
#
#         ja = []
#         sql = (u"select myclass2.*, myclass1.name as pname from myclass1, myclass2 where myclass2.myclass1=myclass1.id and [报价类别1]='%s' and [报价类别2]='%s'" % (
#                 s1, s2))
#         cur.execute(sql)
#         des2priceuf = cur.fetchall()
#         if des2priceuf != []:
#             typelist = []
#             des2price_dict = {}
#             for tup in cur.description:
#                 typelist.append(tup[0])  # 编码gbk
#
#             for i in range(0, len(des2priceuf)):
#                 des2price_dict = getfjo(i, typelist, des2priceuf)
#                 cjo = {}
#                 key = des2price_dict[u'pname'] + ',' + des2price_dict[u'name']
#
#                 string = des2price_dict[u'报价类别1'] + ',' + des2price_dict[u'报价类别2']
#                 cjo['key'] = key
#                 cjo['no'] = des2price_dict[u'输出编号']
#                 cjo['name'] = des2price_dict[u'输出名称']
#                 cjo['myclass'] = des2price_dict[u'type']
#
#                 cjo['s1'] = key
#                 cjo['s2'] = string
#
#                 ja.append(cjo)
#         jo['des2price'] = ja
#         jo['result'] = 1
#
#     return json.dumps(jo, encoding='gbk', ensure_ascii=False)
#
# def LoadOneQuoData(des):
#     if (des =='') or (des ==','): return
#     Result = 0
#
#     string = RootPath + '\\BomPrice\\' + strtomd5(des)
#     if os.path.exists(string):
#         with open(string, 'r') as f:
#             objstr = f.read()
#     else:
#         objstr = OneQuoData2Json(des)
#         if not os.path.exists(RootPath + '\\BomPrice\\'):
#             os.makedirs(RootPath + '\\BomPrice\\')
#         with open(string, 'w+') as f:
#             f.write(objstr)
#     if objstr == '':
#         return Result
#     jo = json.loads(objstr, encoding='utf8')
#     ja = jo['classHash']
#     for i in range(0, len(ja)):
#         cjo = ja[i]
#         pclass = PriceClass()
#         pclass.bj1 = cjo['bj1']
#         pclass.bj2 = cjo['bj2']
#         pclass.pricetype = cjo['pricetype']
#         pclass.factor = cjo['factor']
#         pclass.myunit = cjo['myunit']
#         pclass.myclass = cjo['myclass']
#         pclass.is_calc_cost = cjo['is_calc_cost']
#         key = cjo['key']
#         if key not in classHash:
#             pclasslist = []
#             classHash[key] = pclasslist
#         else:
#             pclasslist = classHash[key]
#             pclasslist.append(pclass)
#     ja = jo['ruleHash']
#     for i in range(0, len(ja)):
#         cjo = ja[i]
#         prule = PriceRule()
#         prule.bj1 = cjo['bj1']
#         prule.bj2 = cjo['bj2']
#         prule.l = cjo['l']
#         prule.lmax = cjo['lmax']
#         prule.lmin = cjo['lmin']
#         prule.p = cjo['p']
#         prule.pmax = cjo['pmax']
#         prule.pmin = cjo['pmin']
#         prule.h = cjo['h']
#         prule.hmax = cjo['hmax']
#         prule.hmin = cjo['hmin']
#         prule.slidingmat = cjo['slidingmat']
#         prule.isnonstandard = cjo['isnonstandard']
#         prule.id = cjo['id']
#         prule.myclass = cjo['myclass']
#
#         prule.PriceTable = cjo['PriceTable']
#         prule.price1 = cjo['price1']
#         prule.price2 = cjo['price2']
#         prule.outname = cjo['outname']
#         prule.sale_type = cjo['sale_type']
#
#         key = cjo['key']
#         if key not in QuoruleHash:
#             prulelist = []
#             QuoruleHash[key] = prulelist
#         else:
#             prulelist = QuoruleHash[key]
#         prulelist.append(prule)
#
#     ja = jo['des2price']
#
#     for i in range(0, len(ja)):
#         cjo = ja[i]
#         m = StrMap()
#         key = cjo['key']
#         m.s1 = cjo['s1']
#         m.s2 = cjo['s2']
#         m.no = cjo['no']
#         m.name = cjo['name']
#         m.myclass = cjo['myclass']
#         des2price.append(m)
#
#
# def QuoDes2Des(pbom):
#     if pbom['desc'] == '':
#         pbom['isoutput'] = False
#         return
#     find = False
#     for i in range(0, len(des2price)):
#         m = des2price[i]
#         if m.s1 == pbom['desc']:
#             find = True
#             break
#     if not find:
#         LoadOneQuoData(pbom['desc'])
#         for i in range(0, len(des2price)):
#
#             m = des2price[i]
#             if m.s1 == pbom['desc']:
#                 find = True
#                 break
#     if not find : return
#     for i in range(0, len(des2price)):
#         m = des2price[i]
#         if m.s1 == pbom['desc']:
#
#             pbom['desc'] = m.s2
#             pbom['outputno'] = m.no
#             pbom['outputname'] = m.name
#             pbom['name'] = m.name
#             pbom['myclass'] = m.myclass
#             pbom['seq'] =seqInfoHash[pbom['outputname']] if pbom['outputname'] in seqInfoHash else -1
#             pbom['classseq'] = classseqInfoHash[pbom['myclass']] if pbom['myclass'] in classseqInfoHash else -1
#             break
#
def FunctionAddProgram1(productPart,param,cnode,mkJs):  # 第七步骤 添加ProgramStr属性 递归中添加
    global id
    program_copy_list = []
    # SizeProgram不产生新节点，只是计算之后更新自身的节点值
    '''
    1）ord提取xml，xml转换成json列表
    2）json列表里有高级编程的属性'Program'，编译成ProgramStr，产生复制的节点
    3）高级编程复制出来的节点里有链接的，需要重新嵌套计算出xml来
    4）对高级编程节点里计算出来的xml，转换成json加入到json列表
    '''
    attridict = {}
    if 'Program' in productPart:
        if productPart['Program'].find('.') == -1:
            productPart['Program'] = productPart['Program'] + '.lua'
        LUAPath = base_dir + '\\Program\\'
        log.info('LUAPath='+LUAPath)
        luafile = LUAPath + productPart['Program']
        log.info('luafile:'+luafile)
        if not os.path.exists(luafile):
            log.warning(luafile+' not exists!!!')
        else:
            with open(luafile, 'r') as f:
                code = f.read()
            obj = {'X': productPart['x'],  # X
                   'Y': productPart['y'],  # Y
                   'Z': productPart['z'],  # Z
                   'L': productPart['l'],  # 宽
                   'D': productPart['p'],  # 深
                   'H': productPart['h'],  # 高
                   'OZ': productPart['oz'],  # OZ旋转
                   }
            obj = json.dumps(obj)
            handle = QdUtils.CreateCompiler()
            programstr = QdUtils.CompileLuaProgram(handle, obj, code, '')
            ProgramStr = c_char_p(programstr).value
            print('ProgramStr:',ProgramStr.decode('utf8'))
            # ProgramStr=u"链接=模板目录\\@模块\\中脚条模块\\0;"
            productPart['ProgramStr'] = ProgramStr
            QdUtils.DestroyCompiler(handle)
            index = ProgramStr.find(',')
            # # 'index:',index
            if index < 0:
                program_list = ProgramStr.split(';')
                program_copy_list = []
                for i in range(0, len(program_list) - 1):
                    program_copy_list.append(program_list[i].decode('utf8'))
                s1 = productPart
            else:
                programstrlist = ProgramStr.split(',')
                for programstrlistchild in programstrlist:
                    attrilist = programstrlistchild.split('=')
                    attridict[attrilist[0]] = attrilist[1]
                # print 'attridict:', json.dumps(attridict, encoding='utf8', ensure_ascii=False)
                program_copy_list = []
                if '链接' in attridict:
                    linkstr = attridict['链接']
                    program_list = linkstr.split(';')
                    for i in range(0, len(program_list) - 1):
                        program_copy_list.append(program_list[i].decode('utf8'))
                    s1 = productPart
                elif '链接' in attridict:
                    print('链接1')
    else:
        pass
    if program_copy_list == []:
        product_copy = {}
        for key, value in list(productPart.items()):
            product_copy[key] = value
        if 'OZ' in attridict:
            OZ = attridict['OZ']
            if OZ == None:
                product_copy['OZ'] = 0
            else:
                product_copy['OZ'] = float(OZ)
        if '宽' in attridict:
            product_copy['l'] = int(attridict['宽'])
        if '深' in attridict:
            product_copy['p'] = int(attridict['深'])
        if '高' in attridict:
            product_copy['h'] = int(attridict['高'])
        if 'Y' in attridict:
            product_copy['ly'] = int(attridict['Y'])
            product_copy['y'] = param['py'] + product_copy['ly']
        if '类别' in attridict:
            print(attridict['类别'].replace('^',',').decode('utf8'))
            product_copy['desc'] = attridict['类别'].replace('^',',').decode('utf8')
        if '基础图形' in attridict:
            product_copy['bg'] = attridict['基础图形']
        product_copy['ProgramStr'] = ''
        product_copy['Program'] = ''
        product_copy['链接'] = ''
        product_copy['id'] = (id)
        product_copy['pid'] = productPart['pid']
        product_copy['space_id'] = param['space_id']
        product_copy['extra'] = ''
        Des2Des(product_copy)
        bomlist.append(product_copy)
        sMKobjb = {}
        InitPriceJson(sMKobjb, product_copy)
        mkJs.append(sMKobjb)
        bl, bp, bh = GraphSizeToBomSize(product_copy['l'], product_copy['p'], product_copy['h'], product_copy['direct'])
        sMKobjb['l'] = bl
        sMKobjb['p'] = bp
        sMKobjb['h'] = bh
        product_copy['gcl2'], product_copy['gcd2'], product_copy['gch2'] = GraphSizeToBomSize1(
            product_copy['gcl'], product_copy['gcd'],
            product_copy['gch'], product_copy['direct'],
            product_copy['gcl2'], product_copy['gcd2'],
            product_copy['gch2'])
        product_copy['gl'] = product_copy['l']
        product_copy['gp'] = product_copy['p']
        product_copy['gh'] = product_copy['h']
        product_copy['l'] = bl
        product_copy['p'] = bp
        product_copy['h'] = bh
        product_copy['bl'] = int(bl) - int(product_copy['lfb']) - int(product_copy['llk'])
        product_copy['bp'] = int(bp) - int(product_copy['wfb']) - int(product_copy['wlk'])
        product_copy['bh'] = int(bh)
        if (int(product_copy['bl']) < 1) or (int(product_copy['bp']) < 1) or (int(product_copy['bh']) < 1):
            product_copy['isoutput'] = False  # // 过滤掉尺寸小于等于零的物料，xml情况复杂
        if (int(product_copy['bl']) > 1) and (int(product_copy['bp']) > 1) and (int(product_copy['bh']) <= 1):
            product_copy['isoutput'] = False  # // 过滤掉一些尺寸为0的物料数据
        product_copy['bomstd'] = ToBomStd(product_copy['bomstddes'], product_copy['l'], product_copy['p'],
                                          product_copy['h'])
        if cnode.hasAttribute('装饰类别'):
            attri = cnode.getAttribute('装饰类别')
            if attri != '' and (attri == '趟门' or attri == '掩门' or (product_copy['myclass'] == '趟门,趟门') or \
                                (product_copy['myclass'] == '掩门,掩门')):
                product_copy['isoutput'] = False
        product_copy['bomstd'] = ToBomStd(product_copy['bomstddes'], product_copy['l'], product_copy['p'],
                                          product_copy['h'])
        if cnode.hasAttribute('输出类型'):
            product_copy['outputtype'] = cnode.getAttribute('输出类型')
        return
    else:
        if index < 0:
            for j in range(0, len(program_copy_list)):
                ## program_copy_list
                product_copy = {}
                for key, value in list(s1.items()):
                    product_copy[key] = value
                product_copy['ProgramStr'] = ''
                product_copy['Program'] = ''
                product_copy['链接'] = program_copy_list[j][3:]
                product_copy['id'] = (id)
                product_copy['pid'] = productPart['pid']
                product_copy['space_id'] = param['space_id']
                product_copy['extra'] = ''
                product_copy['我的模块'] = []
                Des2Des(product_copy)
                bomlist.append(product_copy)
                #mkJs.append(product_copy)
                sMKobjb = {}
                InitPriceJson(sMKobjb, product_copy)
                xmlstr = creatxml(program_copy_list[j][3:], RootPath+'\\Python\\'+str(j) + 't.xml')
                childL = productPart['l']
                childP = productPart['p']
                childH = productPart['h']
                childY = productPart['y']
                bl, bp, bh = GraphSizeToBomSize(product_copy['l'], product_copy['p'], product_copy['h'], product_copy['direct'])
                sMKobjb['l'] = bl
                sMKobjb['p'] = bp
                sMKobjb['h'] = bh
                product_copy['gcl2'], product_copy['gcd2'], product_copy['gch2'] = GraphSizeToBomSize1(
                product_copy['gcl'], product_copy['gcd'],
                product_copy['gch'], product_copy['direct'],
                product_copy['gcl2'], product_copy['gcd2'],
                product_copy['gch2'])
                product_copy['gl'] = product_copy['l']
                product_copy['gp'] = product_copy['p']
                product_copy['gh'] = product_copy['h']
                product_copy['l'] = bl
                product_copy['p'] = bp
                product_copy['h'] = bh
                product_copy['bl'] = int(bl) - int(product_copy['lfb']) - int(product_copy['llk'])
                product_copy['bp'] = int(bp) - int(product_copy['wfb']) - int(product_copy['wlk'])
                product_copy['bh'] = int(bh)
                # print newpoi['name'],newpoi['guid'],newpoi['bl'],newpoi['bp'],newpoi['bh'],newpoi['isoutput']
                if (int(product_copy['bl']) < 1) or (int(product_copy['bp']) < 1) or (int(product_copy['bh']) < 1):
                    product_copy['isoutput'] = False  # // 过滤掉尺寸小于等于零的物料，xml情况复杂
                if (int(product_copy['bl']) > 1) and (int(product_copy['bp']) > 1) and (int(product_copy['bh']) <= 1):
                    product_copy['isoutput'] = False  # // 过滤掉一些尺寸为0的物料数据
                product_copy['bomstd'] = ToBomStd(product_copy['bomstddes'], product_copy['l'], product_copy['p'],
                                                  product_copy['h'])
                childxml['材料'] = productPart['mat']
                childxml['颜色'] = productPart['color']
                childxml['textureclass'] = productPart['textureclass']
                if cnode.hasAttribute('装饰类别'):
                    attri = cnode.getAttribute('装饰类别')
                    if attri != '' and (attri == '趟门' or attri == '掩门' or (product_copy['myclass'] == '趟门,趟门') or \
                                        (product_copy['myclass'] == '掩门,掩门')):
                        product_copy['isoutput'] = False
                product_copy['bomstd'] = ToBomStd(product_copy['bomstddes'], product_copy['l'], product_copy['p'], product_copy['h'])
                if cnode.hasAttribute('输出类型'):
                    product_copy['outputtype'] = cnode.getAttribute('输出类型')
                programstrtojson(xmlstr,childxml,childL, childP, childH, childY,productPart,product_copy)
                product_copy_copy = copy.deepcopy(product_copy)
                product_copy_copy['parent'] = None
                sMKobjb['我的模块'] = product_copy_copy['我的模块']
                mkJs.append(sMKobjb)
        else:
            for j in range(0, len(program_copy_list)):
                product_copy = {}
                for key, value in list(s1.items()):
                    product_copy[key] = value
                product_copy['ProgramStr'] = ''
                product_copy['Program'] = ''
                product_copy['链接'] = program_copy_list[j]
                product_copy['id'] = id
                product_copy['pid'] = productPart['pid']
                product_copy['space_id'] = param['space_id']
                product_copy['我的模块'] = []
                if '宽' in attridict:
                    childL = attridict['宽']
                    product_copy['l'] = int(attridict['宽'])
                else:
                    childL = product_copy['l']
                if '深' in attridict:
                    childP = attridict['深']
                    product_copy['p'] = int(attridict['深'])
                else:
                    childP = product_copy['p']
                if '高' in attridict:
                    childH = attridict['高']
                    product_copy['h'] = int(attridict['高'])
                else:
                    childH = product_copy['高']
                if 'Y' in attridict:
                    product_copy['ly'] = int(attridict['Y'])
                    product_copy['y'] =param['py'] + product_copy['ly']
                    childY = product_copy['y']
                else:
                    childY = product_copy['y']
                sMKobjb = {}
                InitPriceJson(sMKobjb, product_copy)
                bl, bp, bh = GraphSizeToBomSize(product_copy['l'], product_copy['p'], product_copy['h'], product_copy['direct'])
                sMKobjb['l'] = bl
                sMKobjb['p'] = bp
                sMKobjb['h'] = bh
                product_copy['gcl2'], product_copy['gcd2'], product_copy['gch2'] = GraphSizeToBomSize1(product_copy['gcl'], product_copy['gcd'],
                                                                                                       product_copy['gch'], product_copy['direct'],
                                                                                                       product_copy['gcl2'], product_copy['gcd2'],
                                                                                                       product_copy['gch2'])
                product_copy['gl'] = product_copy['l']
                product_copy['gp'] = product_copy['p']
                product_copy['gh'] = product_copy['h']
                product_copy['l'] = bl
                product_copy['p'] = bp
                product_copy['h'] = bh
                product_copy['bl'] = int(bl) - int(product_copy['lfb']) - int(product_copy['llk'])
                product_copy['bp'] = int(bp) - int(product_copy['wfb']) - int(product_copy['wlk'])
                product_copy['bh'] = int(bh)
                if (int(product_copy['bl']) < 1) or (int(product_copy['bp']) < 1) or (int(product_copy['bh']) < 1):
                    product_copy['isoutput'] = False  # // 过滤掉尺寸小于等于零的物料，xml情况复杂
                if (int(product_copy['bl']) > 1) and (int(product_copy['bp']) > 1) and (int(product_copy['bh']) <= 1):
                    product_copy['isoutput'] = False  # // 过滤掉一些尺寸为0的物料数据
                product_copy['bomstd'] = ToBomStd(product_copy['bomstddes'], product_copy['l'], product_copy['p'], product_copy['h'])
                product_copy['extra'] = ''
                Des2Des(product_copy)
                bomlist.append(product_copy)
                xmlstr = creatxml(program_copy_list[j], str(j) + 't.xml')
                childxml['材料']=productPart['mat']
                childxml['颜色'] = productPart['color']
                childxml['textureclass'] =productPart['textureclass']
                if cnode.hasAttribute('装饰类别'):
                    attri = cnode.getAttribute('装饰类别')
                    if attri != '' and (attri == '趟门' or attri == '掩门' or (product_copy['myclass'] == '趟门,趟门') or \
                                        (product_copy['myclass'] == '掩门,掩门')):
                        product_copy['isoutput'] = False
                product_copy['bomstd'] = ToBomStd(product_copy['bomstddes'], product_copy['l'], product_copy['p'], product_copy['h'])
                if cnode.hasAttribute('输出类型'):
                    product_copy['outputtype'] = cnode.getAttribute('输出类型')
                programstrtojson(xmlstr,childxml,childL, childP, childH, childY,productPart,product_copy)
                product_copy_copy = copy.deepcopy(product_copy)
                product_copy_copy['parent'] = None
                sMKobjb['我的模块'] = product_copy_copy['我的模块']
                mkJs.append(sMKobjb)

def CompileLuaProgram(obj, program_str):
    handle = QdUtils.CreateCompiler()
    programstr = QdUtils.CompileLuaProgram(handle, obj, program_str, '')
    ProgramStr = c_char_p(programstr).value
    print('ProgramStr:', ProgramStr.decode('utf8'))
    QdUtils.DestroyCompiler(handle)
    return ProgramStr
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
    DOMTree = minidom.parseString(xml)
    node = DOMTree.documentElement
    return node
def ImportCloneItemForBom(Var,program_str, clone_oi, clonenode, param, id, slino, mkJs):
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
        node.setAttribute(name.decode('utf8'), value.decode('utf8'))
    Result = 0
    LPH = SetSysLPHValue(param['pl'], param['pd'], param['ph'])
    ext = ExtractFileExt(program_str)
    LUAPath = base_dir + '\\Program\\'
    log.info('LUAPath=' + LUAPath)
    luafile = LUAPath + program_str
    log.info('luafile:' + luafile)
    if not os.path.exists(luafile):
        log.warning(luafile + ' not exists!!!')
    else:
        with open(luafile, 'r') as f:
            program_string = f.read()
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
            obj = json.dumps(obj)
            wstr = CompileLuaProgram(obj, program_string)
        else:
            log.warning(program_str + ' not exists!!!')
        #try:
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
            if (nodeName != '板件') and (nodeName != '五金') and (
                    nodeName != '型材五金') and (nodeName != '模块') and (
                    nodeName != '门板'):
                continue
            linkpath = ''
            attri = cnode.getAttribute('链接')
            if attri: linkpath = attri
            bg = ''
            if cnode.hasAttribute('基础图形'):
                bg = cnode.getAttribute('基础图形')
                if bg == 'BG::SPACE':
                    continue
            string = ''
            if cnode.hasAttribute('显示方式'):
                string = cnode.getAttribute('显示方式')
                if string == '3':
                    continue
            newpoi = {}
            newpoi['显示方式'] = string
            InitBomOrderItem(newpoi)
            if nodeName == '板件' : newpoi['myunit'] = '块'
            textureclass = ''
            if cnode.hasAttribute('装饰类别'):
                textureclass = cnode.getAttribute('装饰类别')
            tmp_space_x = param['space_x']
            tmp_space_y = param['space_y']
            tmp_space_z = param['space_z']
            newpoi['pl'] = param['pl']
            newpoi['pd'] = param['pd']
            newpoi['ph'] = param['ph']
            # ACDlg = '0'
            # if cnode.hasAttribute(u'ACDlg'):
            #     ACDlg = cnode.getAttribute(u'ACDlg')
            # newpoi['ACDlg'] = ACDlg
            # Flag32 = '0'
            # if cnode.hasAttribute(u'Flag32'):
            #     Flag32 = cnode.getAttribute(u'Flag32')
            # newpoi['Flag32'] = Flag32
            # Tag = ''
            # if cnode.hasAttribute(u'Tag'):
            #     Tag = cnode.getAttribute(u'Tag')
            # newpoi['Tag'] = Tag
            # PRJ = '0.0'
            # if cnode.hasAttribute(u'PRJ'):
            #     PRJ = cnode.getAttribute(u'PRJ')
            # newpoi['PRJ'] = PRJ
            # original_ldh = ''
            # if cnode.hasAttribute(u'original_ldh'):
            #     original_ldh = cnode.getAttribute(u'original_ldh')
            # newpoi['original_ldh'] = original_ldh
            # ActFlag = ''
            # if cnode.hasAttribute(u'ActFlag'):
            #     ActFlag = cnode.getAttribute(u'ActFlag')
            #
            # if cnode.hasAttribute(u'SpaceFlag'):
            #     SpaceFlag = cnode.getAttribute(u'SpaceFlag')
            #     newpoi['SpaceFlag'] = SpaceFlag
            # LockEdit = ''
            # if cnode.hasAttribute(u'LockEdit'):
            #     LockEdit = cnode.getAttribute(u'LockEdit')
            # newpoi['LockEdit'] = LockEdit
            # newpoi['Type'] = cnode.nodeName
            newpoi['guid'] = cnode.getAttribute('GUID')
            if newpoi['guid'] == '' or len(newpoi['guid']) < 10:
                guid = str(uuid.uuid1())  # 唯一标识符guid
                guid = ''.join(guid.split('-'))
                newpoi['guid'] = guid
            if cnode.hasAttribute('报价规则'):
                ass = cnode.getAttribute('报价规则')
                newpoi["报价规则"] = ass
            newpoi['number_text'] = ''
            if cnode.hasAttribute('NumberText'):
                newpoi['number_text'] = cnode.getAttribute('NumberText')
            if newpoi['number_text'] == '':
                newpoi['number_text'] = param['number_text']
            newpoi['bg'] = bg
            newpoi['holeid'] = -1
            newpoi['kcid'] = -1
            newpoi['cid'] = param['cid']
            newpoi['isoutput'] = True
            for k in range(16):
                newpoi['var_args'][k] = 0
                newpoi['var_names'][k] = ''
            newpoi['nodename'] = cnode.nodeName
            newpoi['id'] = id
            newpoi['pid'] = param['pid']
            newpoi['subspace'] = param['subspace']
            newpoi['space_x'] = param['space_x']
            newpoi['space_y'] = param['space_y']
            newpoi['space_z'] = param['space_z']
            newpoi['space_id'] = param['space_id']
            newpoi['parent'] = param['parent']
            tmp_subspace = ''
            if cnode.hasAttribute('子空间'):
                tmp_subspace = cnode.getAttribute('子空间')
            newpoi['子空间'] = tmp_subspace
            if tmp_subspace == 'A':
                tmp_subspace = ''
            newpoi['subspace'] = param['subspace'] + tmp_subspace
            if tmp_subspace != '':
                newpoi['isoutput'] = False
            newpoi['name'] = cnode.getAttribute('名称')
            varstr = ''
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
            # print type(ToValueInt)
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
                newpoi['ox'] = cnode.getAttribute('OX')
            newpoi['oy'] = 0
            if cnode.getAttribute('OY') != '':
                newpoi['oy'] = cnode.getAttribute('OY')
            newpoi['oz'] = 0
            if cnode.getAttribute('OZ') != '':
                newpoi['oz'] = cnode.getAttribute('OZ')
            varstr = ''
            if cnode.hasAttribute('宽'):
                varstr = cnode.getAttribute('宽')
            ToValueInt = int(Delphi_Round(SetSubject(LPH, varstr, Var)))
            newpoi['l'] = int(ToValueInt) + int(xx1) + (0 - int(xx0))
            if tmp_subspace != '':
                tmp_space_x = newpoi['x']
                tmp_space_y = newpoi['y']
                tmp_space_z = newpoi['z']
            if tmp_subspace == 'B' or tmp_subspace == 'C':
                product_item = mProductList[param['cid']]
                product_item['l'] = product_item['l'] + newpoi['l']
            varstr = '0'
            if cnode.hasAttribute('GCL'):
                varstr = cnode.getAttribute('GCL')
            newpoi['gcl'] = int(varstr)
            newpoi['gcl2'] = newpoi['gcl']
            varstr = '0'
            if cnode.hasAttribute('GCD'):
                varstr = cnode.getAttribute('GCD')
            newpoi['gcd'] = int(varstr)
            newpoi['gcd2'] = newpoi['gcd']
            varstr = '0'
            if cnode.hasAttribute('GCH'):
                varstr = cnode.getAttribute('GCH')
            newpoi['gch'] = int(varstr)
            newpoi['gch2'] = newpoi['gch']
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
            newpoi['holeflag'] = 0
            string = ''
            string = cnode.getAttribute('HoleFlag')
            if string != '':
                ToValueInt = int(SetSubject(LPH, string, Var))
                newpoi['holeflag'] = ToValueInt
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
            di = 0
            if cnode.hasAttribute('DI'):
                di = int(float(cnode.getAttribute('DI')))
            newpoi['DI'] = di
            newpoi['direct'] = di
            newpoi['mat'] = ''
            if cnode.hasAttribute('材料'):
                newpoi['mat'] = cnode.getAttribute('材料')
            if newpoi['mat'] == '':
                if textureclass == param['textureclass']:
                    newpoi['mat'] = param['pmat']
            newpoi['color'] = ''
            if cnode.hasAttribute('颜色'):
                newpoi['color'] = cnode.getAttribute('颜色')
            if newpoi['color'] == '':
                if textureclass == param['textureclass']:
                    newpoi['color'] = param['pcolor']
                    newpoi['颜色'] = newpoi['color']
            newpoi['desc'] = ''
            if cnode.hasAttribute('类别'):
                newpoi['desc'] = cnode.getAttribute('类别')
            newpoi['类别'] = newpoi['desc']
            if cnode.hasAttribute('编码'):
                newpoi['code'] = cnode.getAttribute('编码')
            if cnode.hasAttribute('工艺'):
                newpoi['process'] = cnode.getAttribute('工艺')
            ls = ''
            if cnode.hasAttribute('UI'):
                if cnode.getAttribute('UI') == '拉手':
                    ls = ls + newpoi['name'] + ','
                if cnode.getAttribute('UI') == '拉手集合':
                    newpoi['memo'] = newpoi['memo'] + ls
                    newpoi['ls'] = ls
            newpoi['lgflag'] = 0
            newpoi['LgwjFlag'] = '0'
            if cnode.hasAttribute('LgwjFlag'):
                newpoi['LgwjFlag'] = cnode.getAttribute('LgwjFlag')
                if cnode.getAttribute('LgwjFlag') == '1':
                    newpoi['lgflag'] = 1
            if cnode.hasAttribute('ClipSelect'):
                newpoi['ClipSelect'] = cnode.getAttribute('ClipSelect')
            newpoi['holetype'] = 0
            newpoi['HoleType'] = '0'
            if cnode.hasAttribute('HoleType'):
                newpoi['HoleType'] = cnode.getAttribute('HoleType')
            newpoi['HoleFlag'] = '0'
            if cnode.hasAttribute('HoleFlag'):
                newpoi['HoleFlag'] = cnode.getAttribute('HoleFlag')
            newpoi['Mark'] = '0'
            if cnode.hasAttribute('Mark'):
                newpoi['Mark'] = cnode.getAttribute('Mark')
            newpoi['LMIN'] = '0'
            if cnode.hasAttribute('LMIN'):
                newpoi['LMIN'] = cnode.getAttribute('LMIN')
            newpoi['LMAX'] = '0'
            if cnode.hasAttribute('LMAX'):
                newpoi['LMAX'] = cnode.getAttribute('LMAX')
            newpoi['HMIN'] = '0'
            if cnode.hasAttribute('HMIN'):
                newpoi['HMIN'] = cnode.getAttribute('HMIN')
            newpoi['HMAX'] = '0'
            if cnode.hasAttribute('HMAX'):
                newpoi['HMAX'] = cnode.getAttribute('HMAX')
            newpoi['GUID'] = ''
            if cnode.hasAttribute('GUID'):
                newpoi['GUID'] = cnode.getAttribute('GUID')
            newpoi['Dlgt'] = '0'
            if cnode.hasAttribute('Dlgt'):
                newpoi['Dlgt'] = cnode.getAttribute('Dlgt')
            newpoi['DMIN'] = '0'
            if cnode.hasAttribute('DMIN'):
                newpoi['DMIN'] = cnode.getAttribute('DMIN')
            newpoi['DMAX'] = '0'
            if cnode.hasAttribute('DMAX'):
                newpoi['DMAX'] = cnode.getAttribute('DMAX')
            if cnode.hasAttribute('BT_PID'):
                newpoi['BT_PID'] = cnode.getAttribute('BT_PID')
            if cnode.hasAttribute('BT_ID'):
                newpoi['BT_ID'] = cnode.getAttribute('BT_ID')
            if cnode.hasAttribute('链接'):
                newpoi['链接'] = cnode.getAttribute('链接')
            if cnode.hasAttribute('holetype'):
                if cnode.getAttribute('holetype') != '':
                    newpoi['holetype'] = int(cnode.getAttribute('holetype'))
            autodirect = 0
            if cnode.hasAttribute('autodirect'):
                if cnode.getAttribute('autodirect') != '':
                    autodirect = cnode.getAttribute('autodirect')
            if cnode.hasAttribute('HC'):  # // 动态判定HoleConfig是否要计算
                if cnode.getAttribute('HC') != '':
                    SetIsCalcHoleConfig(newpoi, cnode.getAttribute('HC'))
            newpoi['bdxmlid'] = ''
            if cnode.hasAttribute('BDXMLID'):
                if cnode.getAttribute('BDXMLID') != '':
                    newpoi['bdxmlid'] = cnode.getAttribute('BDXMLID')
            if cnode.hasAttribute('HI'):
                if cnode.getAttribute('HI') != '':
                    HI = urllib.parse.unquote(cnode.getAttribute('HI'))
                    newpoi['holeinfo'] = HI
            newpoi['extend'] = ''
            if cnode.hasAttribute('Extend'):
                if cnode.getAttribute('Extend') != '':
                    newpoi['extend'] = cnode.getAttribute('Extend')
            newpoi['group'] = ''
            if cnode.hasAttribute('Group'):
                if cnode.getAttribute('Group') != '':
                    pbom['group'] = '%s-%s' % (cnode.getAttribute('Group'), strtomd5(uid.uuid1()))
            newpoi['分组'] = ''
            if cnode.hasAttribute('分组'):
                newpoi['分组'] = cnode.getAttribute('分组')
            newpoi['VP'] = '0'
            if cnode.hasAttribute('VP'):
                newpoi['VP'] = cnode.getAttribute('VP')
            if cnode.hasAttribute('图形参数'):
                if cnode.getAttribute('图形参数') != '':
                    SetBGParam(newpoi, cnode.getAttribute('图形参数'))
            newpoi['lfb'] = 0
            newpoi['llk'] = 0
            newpoi['wfb'] = 0
            newpoi['wlk'] = 0
            newpoi['gno'] = param['gno']
            newpoi['gdes'] = param['gdes']
            newpoi['gcb'] = param['gcb']
            newpoi['extra'] = param['extra']
            newpoi['user_fbstr'] = ''
            if cnode.hasAttribute('FBSTR'):
                newpoi['user_fbstr'] = cnode.getAttribute('FBSTR')
            if (newpoi['user_fbstr'] != ''):
                newpoi['llk'], newpoi['wlk'], newpoi['llfb'], newpoi['rrfb'], newpoi['ddfb'], newpoi['uufb'], newpoi[
                    'fb'], newpoi['fbstr'] = FBStr2Value(
                    newpoi['user_fbstr'], newpoi['llk'], newpoi['wlk'], newpoi['llfb'], newpoi['rrfb'], newpoi['ddfb'],
                    newpoi['uufb'], newpoi['fb'], newpoi['fbstr'])
            newpoi['value_lsk'] = 0
            newpoi['value_rsk'] = 0
            newpoi['value_zk'] = 0
            newpoi['value_zs'] = 0
            newpoi['value_ls'] = 0
            newpoi['value_lg'] = 0
            newpoi['value_ltm'] = 0
            newpoi['value_rtm'] = 0
            SetSysVariantValueForOrderItem(varstr, newpoi)
            newpoi['num'] = 1
            if cnode.hasAttribute('Num'):
                newpoi['num'] = int(cnode.getAttribute('Num')) * param['num']
            newpoi['mark'] = 0
            if cnode.hasAttribute('Mark'):
                newpoi['mark'] = int(cnode.getAttribute('Mark'))
            if cnode.hasAttribute('Memo'):
                newpoi['memo'] = cnode.getAttribute('Memo')
            newpoi['userdefine'] = ''
            if cnode.hasAttribute('UD'):
                newpoi['userdefine'] = cnode.getAttribute('UD')
            if cnode.hasAttribute('VP'):
                newpoi['vp'] = int(float(cnode.getAttribute('VP')))
            newpoi['blockmemo'] = ''
            Result = Result + 1
            Des2Des(newpoi)
            bomlist.append(newpoi)
            id = id + 1
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
            newpoi['tmp_soz'] = param['sozflag']
            tmp_soz = param['sozflag']
            if tmp_subspace != '': tmp_soz = ''
            if (tmp_subspace == '') and (float(newpoi['oz']) != 0): tmp_soz = str(param['sozflag']) + (
                        '@%d_%d' % (funcid(newpoi), float(newpoi['oz'])))
            childnum = 0
            newpoi['boardheight'] = param['boardheight']
            newpoi['pricecalctype'] = param['pricecalctype']
            newpoi['Program'] = program_str
            sMKobjb = {}
            InitPriceJson(sMKobjb, newpoi)
            if cnode.hasAttribute('BJSize'):
                BJSize = cnode.getAttribute('BJSize')
                GraphSizeToBJSize(BJSize, sMKobjb)
            log.debug(json.dumps(sMKobjb, ensure_ascii=False))
            childxml = ''
            if linkpath !='':
                childxml = EnumXML(GetXMLByLink(linkpath))
                tmpnode = Xml2ChildNodes(childxml)
                if tmpnode != None:
                    for ccnode in cnode.childNodes:
                        cnode.removeChild(ccnode)
                    cnode.appendChild(tmpnode)
                else:
                    if cnode.childNodes> 0 :
                        childxml = cnode.toxml('utf8')
            if childxml != '':
                param2 = {}
                for key, value in list(param.items()):
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
                param2['sozflag'] = tmp_soz
                param2['xml'] = childxml
                param2['textureclass'] = textureclass
                param2['pmat'] = newpoi['mat']
                param2['pcolor'] = newpoi['color']
                param2['pid'] = id - 1
                param2['mark'] = newpoi['mark']
                param2['pl'] = newpoi['l']
                param2['pd'] = newpoi['p']
                param2['ph'] = newpoi['h']
                param2['px'] = newpoi['x']
                param2['py'] = newpoi['y']
                param2['pz'] = newpoi['z']
                param2['space_x'] = tmp_space_x
                param2['space_y'] = tmp_space_y
                param2['space_z'] = tmp_space_z
                if spaceflag == '1':
                    param2['space_id'] = newpoi['id']
                else:
                    param2['space_id'] = param['space_id']
                param2['num'] = newpoi['num']
                param2['parent'] = newpoi
                if newpoi['number_text'] != '':
                    param2['number_text'] = newpoi['number_text']
                if cnode.hasAttribute('输出类型'):
                    param2['outputtype'] = cnode.getAttribute('输出类型')
                    sMKobjb['outputtype'] = cnode.getAttribute('输出类型')
                child = getfirstchild(cnode)
                if child:
                    param2['rootnode'] = child
                    param2['xdoc'] = param['xdoc']
                    childnum = ImportXomItemForBom(param2, sMKobjb)
            bl, bp, bh = GraphSizeToBomSize(newpoi['l'], newpoi['p'], newpoi['h'], newpoi['direct'])
            sMKobjb['l'] = bl
            sMKobjb['p'] = bp
            sMKobjb['h'] = bh
            newpoi['gcl2'], newpoi['gcd2'], newpoi['gch2'] = GraphSizeToBomSize1(newpoi['gcl'], newpoi['gcd'],
                                                                                 newpoi['gch'], newpoi['direct'],
                                                                                 newpoi['gcl2'], newpoi['gcd2'],
                                                                                 newpoi['gch2'])
            if (autodirect == 1) and (bp > 1220):  # // 自动纹路转换
                di = TextureDirectChange(di)
                newpoi['direct'] = di
                bl, bp, bh = GraphSizeToBomSize(newpoi['l'], newpoi['p'], newpoi['h'], newpoi['direct'])
                newpoi['gcl2'], newpoi['gcd2'], newpoi['gch2'] = GraphSizeToBomSize1(newpoi['gcl'], newpoi['gcd'],
                                                                                     newpoi['gch'], newpoi['direct'],
                                                                                     newpoi['gcl2'], newpoi['gcd2'],
                                                                                     newpoi['gch2'])
            newpoi['gl'] = newpoi['l']
            newpoi['gp'] = newpoi['p']
            newpoi['gh'] = newpoi['h']
            newpoi['l'] = bl
            newpoi['p'] = bp
            newpoi['h'] = bh
            if bh <= 36: sMKobjb['bh'] = bh
            newpoi['bl'] = int(bl) - int(newpoi['lfb']) - int(newpoi['llk'])
            newpoi['bp'] = int(bp) - int(newpoi['wfb']) - int(newpoi['wlk'])
            newpoi['bh'] = int(bh)
            if childnum == None:
                childnum = 0
            newpoi['childnum'] = childnum
            sMKobjb['childnum'] = childnum
            if cnode.hasAttribute('装饰类别'):
                attri = cnode.getAttribute('装饰类别')
                if attri != '' and (attri == '趟门' or attri == '掩门' or (newpoi['myclass'] == '趟门,趟门') or \
                                    (newpoi['myclass'] == '掩门,掩门')):
                    newpoi['isoutput'] = False
            if (int(newpoi['bl']) < 1) or (int(newpoi['bp']) < 1) or (int(newpoi['bh']) < 1): newpoi[
                'isoutput'] = False  # // 过滤掉尺寸小于等于零的物料，xml情况复杂
            if (int(newpoi['bl']) > 1) and (int(newpoi['bp']) > 1) and (int(newpoi['bh']) <= 1): newpoi[
                'isoutput'] = False  # // 过滤掉一些尺寸为0的物料数据
            # 尺寸判定
            sMKobjb['isoutput'] = newpoi['isoutput']
            newpoi['bomstd'] = ToBomStd(newpoi['bomstddes'], newpoi['l'], newpoi['p'], newpoi['h'])
            if childnum > 0:
                newpoi['isoutput'] = False
            newpoi['outputtype'] = ''
            if cnode.hasAttribute('输出类型'):
                newpoi['outputtype'] = cnode.getAttribute('输出类型')
            sMKobjb['outputtype'] = newpoi['outputtype']
            mkJs.append(sMKobjb)
        # except Exception as e:
        #     log.warning(e.message)
        #     pass
        # ProgramStr=u"链接=模板目录\\@模块\\中脚条模块\\0;"
# 高级编程链接的xml转json，node='我的模块'，高级编程链接的xml转json功能函数EnumNode1入口
def programstrtojson(xmlstr,childxml,childL, childP, childH, childY,productPart,product_copy):
    global id,cid
    id = id+1
    if xmlstr == '':
        return
    DOMTree = xml.dom.minidom.parse(xmlstr)
    root = DOMTree.documentElement
    slino = 1
    Var = {}
    for i in range(0, root.childNodes.length):
        node = root.childNodes[i]
        if node.nodeType == 1:
            ## node.nodeName
            if node.nodeName != '产品':
                continue
            name = ''
            l = 0
            d = 0
            h = 0
            bh = 18
            mat = ''
            color = ''
            des = ''
            gcb = ''
            extra = ''
            spaceflag = ''  # 默认
            if node.childNodes[1].getAttribute('板材厚度') == '':
                pass
            else:
                bh = node.childNodes[1].getAttribute('板材厚度')
            if node.childNodes[1].getAttribute('Extra') == '':
                pass
            else:
                extra = node.childNodes[1].getAttribute('Extra')
            if node.hasAttribute('名称'):
                name = node.getAttribute('名称')
            if node.hasAttribute('描述'):
                des = node.getAttribute('描述')
            if node.hasAttribute('CB'):
                gcb = node.getAttribute('CB')
            if node.hasAttribute('宽'):
                l = int(node.getAttribute('宽'))
            if node.hasAttribute('深'):
                d = int(node.getAttribute('深'))
            if node.hasAttribute('高'):
                h = int(node.getAttribute('高'))
            if node.hasAttribute('材料'):
                mat = node.getAttribute('材料')
            if node.hasAttribute('颜色'):
                color = node.getAttribute('颜色')
            if node.hasAttribute('基础图形'):
                mBG = node.getAttribute('基础图形')
            if node.hasAttribute('SpaceFlag'):
                spaceflag = node.getAttribute('SpaceFlag')
            #    'SpaceFlag 不清楚'
            #bomlist = []
            p = {}
            p['id'] = cid
            p['name'] = name
            p['gno'] = productPart['gno']
            if color == '' and childxml['颜色'] != '':
                color = childxml['颜色']
            if mat == '' and childxml['材料'] != '':
                mat = childxml['材料']
            p['mat'] = mat
            p['color'] = color
            p['des'] = productPart['gdes']
            p['gcb'] = gcb
            p['Extra'] = extra
            #print l,d,h,childL,childP,childH
            if l == 0:
                l = childL
            p['l'] = l
            if d == 0:
                d = childP
            p['d'] = d
            if h == 0:
                h =childH
            p['h'] = h
            p['bh'] = bh
            param1 = {}
            param1['productid'] = len(mProductList)
            param1['cid'] = productPart['cid']
            param1['boardheight'] = bh
            #param1['blist'] = bomlist
            param1['gno'] = productPart['gno']
            param1['gdes'] = productPart['gdes']
            if gcb == '':
                gcb = product_copy['gcb']
            param1['gcb'] = gcb
            if extra == '':
                extra = productPart['extra']
            param1['extra'] = extra
            param1['pname'] = ''
            param1['subspace'] = product_copy['subspace']
            param1['sozflag'] = ''
            param1['xml'] = node.childNodes[1].toxml('UTF-8')
            param1['textureclass'] = childxml['textureclass']
            param1['pmat'] = mat
            param1['pcolor'] = color
            param1['pid'] = product_copy['id']
            param1['pl'] = l
            param1['pd'] = d
            param1['ph'] = h
            param1['px'] = product_copy['x']
            param1['py'] = product_copy['y']
            param1['pz'] = product_copy['z']
            param1['space_x'] = product_copy['space_x']
            param1['space_y'] = product_copy['space_y']
            param1['space_z'] = product_copy['space_z']
            if spaceflag == '1':
                param1['space_id'] = product_copy['id']
            else:
                param1['space_id'] = product_copy['space_id']
            param1['outputtype'] = product_copy['outputtype']
            param1['num'] = 1
            param1['parent'] = None
            param1['blockmemo'] = ''
            param1['number_text'] = ''
            param1['pricecalctype'] = product_copy['pricecalctype']
            # param1['rootnode'] = node
            # param1['xdoc'] = DOMTree
            param1['rootnode'] = node
            param1['xdoc'] = None
            childnum = 0
            products = {'我的模块':[],'变量列表':[]}
            childnum = ImportXomItemForBom(param1,products)
            if childnum > 0: product_copy['isoutput'] = False
            if childnum == None:
                childnum = 0
            product_copy['childnum'] = childnum
            #print u'我的模块',products[u'我的模块']
            for product in products['我的模块']:
                product_copy['我的模块'].append(product)
            products = {'我的模块':[],'变量列表':[]}
    # product_copy[u'柜体列表'] = JsonPrice1
def InitBgMinAndMax(bomlist):
    for i in range(0,len(bomlist)):
        p = bomlist[i]
        if 'bg' not in p:
            continue
        ## '123', p['bg']
        bg = p['bg']
        if p['bg'] == 'BG::RECT' :
            p['bg'] = p['bg'].replace('::','_')
            ## 'bbbb',p['bg']
        p['bg_l_minx'] = 0
        p['bg_l_maxx'] = p['gp']
        p['bg_l_miny'] = 0
        p['bg_l_maxy'] = p['gh']
        p['bg_d_minx'] = 0
        p['bg_d_maxx'] = p['gl']
        p['bg_d_miny'] = 0
        p['bg_d_maxy'] = p['gp']
        p['bg_b_minx'] = 0
        p['bg_b_maxx'] = p['gl']
        p['bg_b_miny'] = 0
        p['bg_b_maxy'] = p['gh']
        p['bg_r_minx'] = p['bg_l_minx']
        p['bg_r_maxx'] = p['bg_l_maxx']
        p['bg_r_miny'] = p['bg_l_miny']
        p['bg_r_maxy'] = p['bg_l_maxy']
        p['bg_u_minx'] = p['bg_d_minx']
        p['bg_u_maxx'] = p['bg_d_maxx']
        p['bg_u_miny'] = p['bg_d_miny']
        p['bg_u_maxy'] = p['bg_d_maxy']
        p['bg_f_minx'] = p['bg_b_minx']
        p['bg_f_maxx'] = p['bg_b_maxx']
        p['bg_f_miny'] = p['bg_b_miny']
        p['bg_f_maxy'] = p['bg_b_maxy']
        ## 'p[bg]1:',p['bg']
        InitBgMinAndMaxItem(p)
        #if p['name'] == u'底板':
            ## '2:',p['guid'], p['bg_l_maxx']
            #sys.exit(1)
        p['bg'] = bg
def InitBgMinAndMaxItem(p):   #xml来源    /BaseGraph/x2d文件
    mTempList = []
    minx = 0
    maxx = 0
    miny = 0
    maxy = 0
    sminmax = {}
    sminmax['minx'] = 0
    sminmax['maxx'] = 0
    sminmax['miny'] = 0
    sminmax['maxy'] = 0
    #global mTempList
    def AddList():
        mTempList = []
        for i in range(0,len(node)):  #node  怎么来的 mTempList
            cnode = node[i]
            if cnode.tag != 'Point':
                continue
            pt = TGPPoint()
            pt.x= nowSetSubject(cnode.get('X',0), mTmpExp)
            pt.y = nowSetSubject(cnode.get('Y',0), mTmpExp)
            mTempList.append(pt)
        return mTempList
    def GetMinAndMax():
        ## '9999:',mTempListCopy
        pt = mTempListCopy[0]
        sminmax['minx'] = pt.x
        sminmax['miny'] = pt.y
        sminmax['maxx'] = pt.x
        sminmax['maxy'] = pt.y
        ## 'hahha',sminmax
        for i in range(0,len(mTempListCopy)):
            pt = mTempListCopy[i]
            if sminmax['minx'] > pt.x: sminmax['minx'] = pt.x
            if sminmax['maxx'] < pt.x: sminmax['maxx'] = pt.x
            if sminmax['miny'] > pt.y: sminmax['miny'] = pt.y
            if sminmax['maxy'] < pt.y: sminmax['maxy'] = pt.y
        ## 'hahha', pt['x'], pt['y'], pt['x'], pt['y'], sminmax
    def GetMinAndMax_FromX(MO):
        for i in range(0, len(mTempListCopy)):
            pt = mTempListCopy[i]
            if sminmax['miny'] == pt.y:
                MO['min0'] = pt.x
                MO['max0'] = pt.x
            if sminmax['maxy'] == pt.y:
                MO['min1'] = pt.x
                MO['max1'] = pt.x
        for i in range(0,len(mTempListCopy)):
            pt = mTempListCopy[i]
            if sminmax['miny'] == pt.y:
                if MO['min0'] > pt.x: MO['min0'] = pt.x
                if MO['max0'] < pt.x: MO['max0'] = pt.x
            if sminmax['maxy'] == pt.y:
                if MO['min1'] > pt.x: MO['min1'] = pt.x
                if MO['max1'] < pt.x: MO['max1'] = pt.x
    def GetMinAndMax_FromY(MO):
        ## '123mTempListCopy:',mTempListCopy
        for i in range(0, len(mTempListCopy)):
            pt = mTempListCopy[i]
            if sminmax['minx'] == pt.x:
                MO['min0'] = pt.y
                MO['max0'] = pt.y
            if sminmax['maxx'] == pt.x:
                MO['min1'] = pt.y
                MO['max1'] = pt.y
        for i in range(0, len(mTempListCopy)):
            pt = mTempListCopy[i]
            if sminmax['minx'] == pt.x:
                if MO['min0'] > pt.y: MO['min0'] = pt.y
                if MO['max0'] < pt.y: MO['max0'] = pt.y
            if sminmax['maxx'] == pt.x:
                if MO['min1'] > pt.y: MO['min1'] = pt.y
                if MO['max1'] < pt.y: MO['max1'] = pt.y
    ## 'p[bg]:',p['bg']
    # if p['name'] ==u'底板':
    #     # p['guid'],p['bg_l_maxx']
    if p['bg'] == '':
        return
    # X2dName = Currentpath + '\\BaseGraph\\' + p['bg'] + '.x2d'#'BG_RECT'
    # X2dPath1 = os.path.dirname(X2dName) + '\\'
    # if not os.path.exists(X2dPath1):
    #     os.makedirs(X2dPath1)
    # X2dNamePath = X2dPath + p['bg'] + '.x2d'
    #
    # if not os.path.exists(X2dName):
    #     ## X2dName
    #     replaceXmlEncoding(X2dNamePath, X2dName)
    #
    # DOMTree = xml.dom.minidom.parse(X2dName)
    # collection = DOMTree.documentElement
    # ## collection.nodeName
    #
    #with open(X2dName, 'r+') as f:
    if p['bg'].encode('gb2312') not in gBGHash:
        return
    xmlContent = gBGHash[p['bg'].encode('gb2312')].replace('gb2312','utf_8')
    if xmlContent == '':
        return
    root = ET.fromstring(xmlContent) # 解析那段xml
    ## 1
    ## root.tag
    mTmpExp['CA'] = p['var_args'][0]
    mTmpExp['CB'] = p['var_args'][1]
    mTmpExp['CC'] = p['var_args'][2]
    mTmpExp['CD'] = p['var_args'][3]
    mTmpExp['CE'] = p['var_args'][4]
    mTmpExp['CF'] = p['var_args'][5]
    mTmpExp['CG'] = p['var_args'][6]
    mTmpExp['CH'] = p['var_args'][7]
    mTmpExp['CI'] = p['var_args'][8]
    mTmpExp['CJ'] = p['var_args'][9]
    mTmpExp['CK'] = p['var_args'][10]
    mTmpExp['CL'] = p['var_args'][11]
    mTmpExp['CM'] = p['var_args'][12]
    mTmpExp['CN'] = p['var_args'][13]
    mTmpExp['CO'] = p['var_args'][14]
    mTmpExp['CP'] = p['var_args'][15]
    for i in range(0,len(root)):
        if root[i].tag =='PlaneXY':   # PlaneXY
            node = root[i]
            tystr = node.get('Type')
            ## tystr
            if tystr == 'Polygon':
                L = p['gl']
                W = p['gp']
                mTmpExp['L'] = L
                mTmpExp['W'] = W
                ## '66666', L, W
                mTempListCopy = AddList()
                ## 'len(mTempList)',len(mTempList),'mTempList=',mTempList,
                #mTempListCopy = []
                # for chlidmTempList in mTempList:
                #
                #     for key ,value in chlidmTempList.items():
                #         chlidmTempList[key] = int(nowSetSubject(value, mTmpExp))
                #     mTempListCopy.append(chlidmTempList)
                ## mTempListCopy
                if len(mTempListCopy) >= 4 :
                    GetMinAndMax()
                    MO = {}
                    MO['min0'] = p['bg_l_minx']
                    MO['max0'] = p['bg_l_maxx']
                    MO['min1'] = p['bg_r_minx']
                    MO['max1'] = p['bg_r_maxx']
                    GetMinAndMax_FromY(MO)
                    p['bg_l_minx'] = MO['min0']
                    p['bg_l_maxx'] = MO['max0']
                    p['bg_r_minx'] = MO['min1']
                    p['bg_r_maxx'] = MO['max1']
                    MO['min0'] = p['bg_b_minx']
                    MO['max0'] = p['bg_b_maxx']
                    MO['min1'] = p['bg_f_minx']
                    MO['max1'] = p['bg_f_maxx']
                    GetMinAndMax_FromX(MO)
                    p['bg_b_minx'] = MO['min0']
                    p['bg_b_maxx'] = MO['max0']
                    p['bg_f_minx'] = MO['min1']
                    p['bg_f_maxx'] = MO['max1']
                    #if p['name'] == u'底板':
                        ## '3=',p['guid'], p['bg_l_maxx']
                # if p['name'] == u'半圆弧顶板':
                #     #print len(mTempListCopy)
                #     exit(1)
        if root[i].tag =='PlaneXZ':   # PlaneXY
            node = root[i]
            tystr = node.get('Type')
            if tystr == 'Polygon':
                L = p['gl']
                W = p['gh']
                mTmpExp['L'] = L
                mTmpExp['W'] = W
                ## '66666', L, W
                mTempListCopy = AddList()
                ## mTempList
                # mTempListCopy = []
                # for chlidmTempList in mTempList:
                #
                #     for key, value in chlidmTempList.items():
                #         chlidmTempList[key] = int(nowSetSubject(value, mTmpExp))
                #     mTempListCopy.append(chlidmTempList)
                ## mTempListCopy
                if len(mTempListCopy) >= 4 :
                    GetMinAndMax()
                    MO = {}
                    MO['min0'] = p['bg_l_miny']
                    MO['max0'] = p['bg_l_maxy']
                    MO['min1'] = p['bg_r_miny']
                    MO['max1'] = p['bg_r_maxy']
                    GetMinAndMax_FromY(MO)
                    p['bg_l_miny'] = MO['min0']
                    p['bg_l_maxy'] = MO['max0']
                    p['bg_r_miny'] = MO['min1']
                    p['bg_r_maxy'] = MO['max1']
                    MO['min0'] = p['bg_d_minx']
                    MO['max0'] = p['bg_d_maxx']
                    MO['min1'] = p['bg_u_minx']
                    MO['max1'] = p['bg_u_maxx']
                    GetMinAndMax_FromX(MO)
                    p['bg_d_minx'] = MO['min0']
                    p['bg_d_maxx'] = MO['max0']
                    p['bg_u_minx'] = MO['min1']
                    p['bg_u_maxx'] = MO['max1']
        if root[i].tag =='PlaneYZ':   # PlaneXY
            node = root[i]
            tystr = node.get('Type')
            if tystr == 'Polygon':
                # mTempList   给里面添加对象
                L = p['gp']
                W = p['gh']
                mTmpExp['L'] = L
                mTmpExp['W'] = W
                ## '66666', L, W
                mTempListCopy = AddList()
                #     exit(1)
                ## mTempList
                # mTempListCopy = []
                # print json.dumps(mTempList,ensure_ascii=False)
                # for chlidmTempList in mTempList:
                #
                #     for key, value in chlidmTempList.items():
                #         chlidmTempList[key] = int(nowSetSubject(value, mTmpExp))
                #     mTempListCopy.append(chlidmTempList)
                ## mTempListCopy
                if len(mTempListCopy) >= 4 :
                    # 获取最小最大值
                    GetMinAndMax()
                    MO = {}
                    MO['min0'] = p['bg_d_miny']
                    MO['max0'] = p['bg_d_maxy']
                    MO['min1'] = p['bg_u_miny']
                    MO['max1'] = p['bg_u_maxy']
                    GetMinAndMax_FromX(MO)
                    p['bg_d_miny'] = MO['min0']  #0
                    p['bg_d_maxy'] = MO['max0']  #p['gh'] 1000
                    p['bg_u_miny'] = MO['min1']  #0
                    p['bg_u_maxy'] = MO['max1']  #p['gp']  519
                    MO['min0'] = p['bg_b_miny']
                    MO['max0'] = p['bg_b_maxy']
                    MO['min1'] = p['bg_f_miny']
                    MO['max1'] = p['bg_f_maxy']
                    GetMinAndMax_FromY(MO)
                    p['bg_b_miny'] = MO['min0']
                    p['bg_b_maxy'] = MO['max0']
                    p['bg_f_miny'] = MO['min1']
                    p['bg_f_maxy'] = MO['max1']
def CalcLgFlag(bomlist):
    for i in range(0, len(bomlist)):
        p = bomlist[i]
        if 'lgflag' not in p:
            continue
        if p['lgflag'] != 1:
            continue
        for j in range(0, len(bomlist)):
            if i == j:
                continue
            p2 = bomlist[j]
            if 'lgflag' not in p2:
                continue
            if p2['lgflag'] != 1:
                continue
            if p['subspace'] != p2['subspace']:
                continue
            t = p['z'] + (p['gh'] // 2)
            if not ((t > p2['z']) and (t < p2['z'] + p2['gh'])):
                continue
            if ((p['x'] + p['gl'] + 9) > p2['x']) and ((p['x'] + p['gl'] + 9) < (p2['x'] + p2['gl'])):
                p['lgflag'] = 2
                p2['lgflag'] = 0
    for i in range(0, len(bomlist)):
        p = bomlist[i]
        if 'lgflag' not in p:
            continue
        if p['lgflag'] == 1:
            p['lgflag'] = 0
        if p['lgflag'] == 2:
            p['lgflag'] = 1
def CalcBomWj():
    def MyRound(f):
        i = Delphi_Round(f)
        if (f-i) < 0.0001:
            Result = i
        else:
            Result = i+1
        return Result
    basewjlist = []
    for i in range(0,len(bomlist)):
        p = bomlist[i]
        if 'bomwjdes' not in p: continue
        if (p['bomwjdes'] != ',') and (p['bomwjdes'] != ''):
            if p['bomwjdes'] in wjruleHash:
                wujinlist = wjruleHash[p['bomwjdes']]
                for j in range(0,len(wujinlist)):
                    pwjrule = wujinlist[j]
                    p2 = {}
                    if ((pwjrule.lgflag == 0) or (p['lgflag'] == pwjrule.lgflag)) \
                        and ((p['bl'] >= pwjrule.lmin) and ((p['bl'] <= pwjrule.lmax) or (pwjrule.lmax == 0))) \
                        and ((p['bp'] >= pwjrule.pmin) and ((p['bp'] <= pwjrule.pmax) or (pwjrule.pmax == 0))) \
                        and ((p['bh'] >= pwjrule.hmin) and ((p['bh'] <= pwjrule.hmax) or (pwjrule.hmax == 0))):
                        InitBomOrderItem(p2)
                        p2['classseq'] = 10000
                        p2['seq'] = pwjrule.wjid
                        p2['cid'] = p['cid']
                        p2['nodename'] = '五金'
                        p2['name'] = pwjrule.wjname
                        p2['code'] = pwjrule.wjno
                        p2['gno'] = p['gno']
                        p2['gcb'] = p['gcb']
                        p2['extra'] = p['extra']
                        p2['subspace'] = p['subspace']
                        p2['guid'] = p['guid']
                        p2['modlename'] = p['name']
                        p2['l'] = 1
                        p2['p'] = 1
                        p2['h'] = 1
                        p2['bl'] = 1
                        p2['bp'] = 1
                        p2['bh'] = 1
                        p2['direct'] = 0
                        p2['desc'] = pwjrule.wjname
                        p2['myunit'] = pwjrule.myunit2
                        p2['mat'] = pwjrule.mat
                        p2['mat'] = p2['mat'].replace('[P]', p['mat'])
                        p2['color'] = pwjrule.color
                        p2['color'] = p2['color'].replace('[P]', p['color'])
                        if pwjrule.myunit == '单件' :
                            p2['num'] = pwjrule.num
                        elif pwjrule.myunit == '宽度(每米)' :
                            f = p['bl'] / 1000
                            t = MyRound(f)
                            p2['num'] = pwjrule.num * t
                        elif pwjrule.myunit == '深度(每米)' :
                            f= p['bp'] / 1000
                            t = MyRound(f)
                            p2['num'] = pwjrule.num * t
                        elif pwjrule.myunit == '高度(每米)':
                            f = p['bh'] / 1000
                            t = MyRound(f)
                            p2['num'] = pwjrule.num * t
                        elif pwjrule.myunit == '面积(每平米)' :
                            f= p['bl'] * p['bp'] / 1000 / 1000
                            t= MyRound(f)
                            p2['num']= pwjrule.num * t
                        else:
                            pass
                        p2['basewj_price'] = pwjrule.price
                        basewjlist.append(p2)
        if (p['bomdes'] != ',') and (p['bomdes'] != '') :
            # // 工艺减量
            if p['bomdes'] == '' or 'bomdes' not in p: continue
            prulelist = ruleHash[p['bomdes']]
            for j in range(0,len(prulelist)):
                prule = prulelist[j]
                if ((prule.mat == '*') or (prule.mat == p['mat'])) and ((prule.bh == 0) or (prule.bh == Delphi_Round(p['bh']))):
                    if p['lfb'] == 0 : p['lfb'] = prule.lfb
                    if p['llk'] == 0 : #// 非手动设置计算
                        p['llk']= prule.llk
                        p['bl']= int(p['bl'] - p['lfb'] - p['llk'])
                    if p['wfb'] == 0 : p['wfb'] =prule.wfb
                    if p['wlk'] == 0 :  #// 非手动设置计算
                        p['wlk'] = prule.wlk
                        p['bp'] = int(p['bp'] - p['wfb'] - p['wlk'])
                    p['holestr'] = prule.holestr
                    p['kcstr'] = prule.kcstr
                    p['memo'] = prule.memo + p['memo']
                    for k in range(0,16):
                        p['memo'] =p['memo'].replace('[$C%s]'%chr(65 + k), str(p['var_args'][k]))
                        p['kcstr'] =p['kcstr'].replace('[$C%s]'%chr(65 + k), str(p['var_args'][k]))
                    if p['user_fbstr'] == '' :
                        p['llfb'] = prule.llfb
                        p['rrfb'] = prule.rrfb
                        p['ddfb'] = prule.ddfb
                        p['uufb'] = prule.uufb
                        p['fb'] = prule.fb
                    if p['fbstr'] == '' : p['fbstr'] = prule.fbstr
                    break
    return basewjlist
def CalcHoleWj(bomlist, basewjlist, mHPInfoList,workflowlist,gBGHash,mKCInfoList):
    def AddWj(p, r, b_bh = 0, isii = 0):
        #  list.Add LoadChildBom  '物料分解'，封边开槽，基础五金，孔位配置，开槽配置
        #  basewjlist.Add  CalcBomWj,CalcHoleWj
        j = 0
        # if len(basewjlist)==1637:
        #     print 'r=',r,'b_bh=', b_bh,'isii=', isii,p['color']
        #     print p['bhole_index']
        for i in range(0, len(CfgList)):#len(CfgList)
            cfg = CfgList[i]
            if (isii != 0) and (cfg['holetype'] == 1):
                continue
            if (isii != 1) and (cfg['holetype'] == 2):
                continue
            #print 'hahha' + 'b_bh=' ,(b_bh) , 'cfgbh=' ,(str(cfg['bh'])) \
            #+'cfg.hole=' + cfg['hole'] + 'r=' + r + 'cfg.color=' + cfg['color'] + 'p.color=' + p['color'] \
            #+'cfg[holenum]=',cfg['holenum'],'cfg[c]',cfg['c']
            if ((b_bh == 0) or (cfg['bh'] == 0) or (cfg['bh'] == int(b_bh))) and (cfg['hole'] == r) and (cfg['color'] == '') or (cfg['color'] == p['color']):
                j = j+1
            if ((b_bh == 0) or (cfg['bh'] == 0) or (cfg['bh'] == int(b_bh))) and (cfg['hole'] == r) and ((cfg['color'] == '') or (cfg['color'] == p['color'])):
                #print '2222222222' + 'b_bh=', (b_bh), 'cfgbh=', (str(cfg['bh'])) \
                                                          # + 'cfg.hole=' + cfg['hole'] + 'r=' + r + 'cfg.color=' + cfg[
                                                            #'color'] + 'p.color=' + p['color']
                cfg['c'] = cfg['c'] + 1
                if (cfg['holenum'] > 0):
                    if cfg['holenum'] > cfg['c']:
                        continue
                p2 = {}
                cfg['c'] = 0
                InitBomOrderItem(p2)
                p2['classseq'] = 10000
                p2['seq'] = i
                p2['cid'] = p['cid']
                p2['nodename'] = '五金'
                p2['name'] = cfg['wjname']
                p2['gno'] = p['gno']
                p2['gcb'] = p['gcb']
                p2['guid'] = p['guid']
                p2['modlename'] = p['name']
                p2['extra'] = p['extra']
                p2['subspace'] = p['subspace']
                p2['l'] = 1
                p2['p'] = 1
                p2['h'] = 1
                p2['bl'] = 1
                p2['bp'] = 1
                p2['bh'] = 1
                p2['direct'] = 0
                p2['desc'] = cfg['wjname']
                p2['mat'] = cfg['wjmat']
                p2['mat'] = p2['mat'].replace('[P]', p['mat'])
                #print 'mat=',p2['mat']
                p2['color'] = cfg['wjcolor']
                p2['color'] = p2['color'].replace('[P]', p['color'])
                #print 'color=', p2['color']
                p2['num'] = cfg['wjnum']
                p2['basewj_price'] = 0
                p2['code'] = cfg['wjcode']
                basewjlist.append(p2)
    CFGPath = RootPath + '\\data\\qddata\\'
    if not os.path.exists(CFGPath):
        os.makedirs(CFGPath)
    HoleWjFile= CFGPath + '孔位五金.cfg'.encode('GB2312')
    if not os.path.exists(HoleWjFile):
        ## u'缺少孔位五金配置表'
        sys.exit(1)
    HoleWjF = io.open(HoleWjFile,encoding='GB2312')
    HoleWjFContent = HoleWjF.read()
    HoleWjFContent=json.loads(HoleWjFContent)
    CfgList = []
    for childContent in HoleWjFContent:
        cfg = {}
        cfg['c'] = 0
        cfg['holetype'] = 0
        if '孔位类型' not in childContent:
            childContent['孔位类型'] = ''
        if 'B板厚' not in childContent:
            childContent['B板厚'] = 0
        if '孔位标识' not in childContent:
            childContent['孔位标识'] = ''
        if '板材颜色' not in childContent:
            childContent['板材颜色'] = ''
        if '五金名称' not in childContent:
            childContent['五金名称'] = ''
        if '五金材料' not in childContent:
            childContent['五金材料'] = ''
        if '五金颜色' not in childContent:
            childContent['五金颜色'] = ''
        if '五金编号' not in childContent:
            childContent['五金编号'] = ''
        if '五金数量' not in childContent:
            childContent['五金数量'] = 0
        if (childContent['孔位类型']=='B') :
            cfg['holetype'] = 1
        if (childContent['孔位类型']=='I+I') :
            cfg['holetype'] = 2
        cfg['bh'] = childContent['B板厚']
        if '孔数量' not in childContent:
            cfg['holenum'] = 0
        else:
            cfg['holenum'] = childContent['孔数量']
        cfg['hole'] = str(childContent['孔位标识'])
        cfg['color'] = childContent['板材颜色']
        cfg['wjname'] = childContent['五金名称']
        cfg['wjmat'] = childContent['五金材料']
        cfg['wjcolor'] = childContent['五金颜色']
        if '五金编号' not in childContent:
            cfg['wjcode'] = ''
        else:
            cfg['wjcode'] = str(childContent['五金编号'])
        cfg['wjnum'] = childContent['五金数量']
        CfgList.append(cfg)   #list.Add(cfg);    #wujin配置信息初始化
    for i in range(0,len(bomlist)):
        p = bomlist[i]
        if not p['isoutput']: continue
        #with open (RootPath + '\\testdata\\'+'WJ.txt','a') as f:
        log.debug(str(i)+'='+str(len(basewjlist))+'\n')
        if 'isoutput' not in p:
            continue
        if not p['isoutput'] :
            continue
        for j in range(0, 101):
            if p['ahole_index'][j] >= 0:
                #print "p['ahole_index'][j]:",p['ahole_index'][j]
                phinfo = mHPInfoList[p['ahole_index'][j]]  #mHPInfoList 孔位信息列表
                AddWj(p, phinfo.r, phinfo.b_bh, phinfo.isii) #根据孔位信息添加孔位wujin
                #with open(RootPath + '\\testdata\\' + 'WJ.txt', 'a') as f:
                log.debug(str(i) + '=' + 'akong='+str(j)+','+str(p['ahole_index'][j])+',' + str(len(basewjlist)) + '\n')
            else:
                break
        for j in range(0, 101):
            if p['bhole_index'][j] >= 0:
                #print "p['bhole_index'][j]:", p['bhole_index'][j]
                # "p['bhole_index'][j]:",p['bhole_index'][j]
                phinfo = mHPInfoList[p['bhole_index'][j]]  #mHPInfoList 孔位信息列表
                # if p['bhole_index'][j] == 1251:
                #     print 'r1=',phinfo.r,'b_bh1=',phinfo.b_bh,'isii1=',phinfo.isii,'face1=',phinfo.face,'j1=',p['bhole_index'][j]
                if phinfo.isii==0:
                    #print 'r=',phinfo.r,'b_bh=',phinfo.b_bh,'isii=',phinfo.isii,'face=',phinfo.face,'j=',p['bhole_index'][j]
                    AddWj(p, phinfo.r, phinfo.b_bh, phinfo.isii) #根据孔位信息添加孔位wujin
                    #with open(RootPath + '\\testdata\\' + 'WJ.txt', 'a') as f:
                    log.debug(str(i) + '=' + 'bkong='+str(j) +','+str(p['bhole_index'][j])+','+ str(len(basewjlist)) + '\n')
            else:
                break
        #with open(RootPath + '\\testdata\\' + 'WJ.txt', 'a') as f:
        log.debug(str(i) + '=' +'kong'+ str(len(basewjlist)) + '\n')
        ###自定义孔位
        # if i==640:
        #     print p['bdxmlid'],p['bg_filename']
        flag = 0
        if 'bdxmlid' not in p: p['bdxmlid'] = ''
        if p['bdxmlid'] !='' and mBDXMLList[p['bdxmlid']] != '':    #node := root.ChildNodes.FindNode('BDXML');
            flag = 1
        if 'bg_filename' not in p: p['bg_filename'] = ''
        if p['bg_filename'] != '' and os.path.exists(p['bg_filename']) :
            flag = 2
        # if i==640:
        #     print 'flag=', flag
        xml = ''
        if flag in [1,2]:
            if flag == 1:
                xml = mBDXMLList[p['bdxmlid']]   #xml 来源问题
                calcitem = TMyCalcItem()
                ll = 0
                pp = 0
                hh = 0
                xml2 = SaveBD(BomItem2CalcItem(p, calcitem,workflowlist,mBDXMLList,gBGHash),gBGHash,mHPInfoList,mKCInfoList, ll, pp, hh, False)   #难点
                xml = BDXML_BDXML(xml, xml2)    #难点
                xml = '<?xml version="1.0" encoding="utf8"?>' + xml
            if flag == 2:
                #f = open(p['bg_filename'],'r')    #xml来源问题
                with open (p['bg_filename'],'r') as f:
                    xml = f.read().replace('gb2312', 'utf-8')
            # if i == 640:
            #     print 'xml=', xml
            root = ET.fromstring(xml)
            for k in range(0,len(root)):
                if root[k].tag == 'FaceA':
                    nodeA = root[k]
                    for j in range(0,len(nodeA)):
                        cnode = nodeA[j]
                        if (cnode.tag == 'BHole'):
                            if cnode.get('R'):
                                attri = cnode.get('R','')
                                if attri != '' :
                                    AddWj(p, attri, Delphi_Round(p['bh']), 0)
                                    n = 0
                                    if cnode.get('Holenum_X'):
                                        n = cnode.get('Holenum_X')
                                    for k in range(1,n-1):
                                        AddWj(p, attri, Delphi_Round(p['bh']), 0)
                                    n = 0
                                    if cnode.get('Holenum_Y'):
                                        n = cnode.get('Holenum_Y')
                                    for k in range(1, n - 1):
                                        AddWj(p, attri, Delphi_Round(p['bh']), 0)
                if root[k].tag == 'FaceB':
                    nodeB = root[k]
                    for j in range(0,len(nodeB)):
                        cnode = nodeB[j]
                        if (cnode.tag == 'BHole'):
                            if cnode.get('R'):
                                attri = cnode.get('R')
                                if attri != '' :
                                    AddWj(p, attri, Delphi_Round(p['bh']), 0)
                                    n = 0
                                    if cnode.get('Holenum_X'):
                                        n = cnode.get('Holenum_X')
                                    for k in range(1,n-1):
                                        AddWj(p, attri, Delphi_Round(p['bh']), 0)
                                    n = 0
                                    if cnode.get('Holenum_Y'):
                                        n = cnode.get('Holenum_Y')
                                    for k in range(1, n - 1):
                                        AddWj(p, attri, Delphi_Round(p['bh']), 0)
        #with open(RootPath + '\\testdata\\' + 'WJ.txt', 'a') as f:
        log.debug(str(i) + '=' +'zidingyikong'+ str(len(basewjlist)) + '\n')
    for i in range(0,len(CfgList)):
        CfgList[i] = {}
def ToBGInfo(p,gBGHash, mHPInfoList):
    Result = ''
    string = ''
    if 'bg' not in p:
        p['bg'] = ''
        return ''
    bg = p['bg']
    if p['bg'] != 'BG::RECT':
        p['bg'] = p['bg'].replace('::', '_')
    if p['bg'] != 'BG::RECT':
        string = ToBGInfoX2D(p,gBGHash, mHPInfoList)
    p['bg'] = bg
    Result = string
    return Result
def TranAB(bomlist,mHPInfoList, gBGHash):
    # 左右翻板，需要进行AB面反转
    for i in range(0,len(bomlist)):
        p = bomlist[i]
        p['bg_data'] = ToBGInfo(p, gBGHash, mHPInfoList)
        # if i == 208:
        #     print p['a_hole_info']
        #     print p['b_hole_info']
            #exit(1)
        if p['bg'] != 'BG::RECT' :
            continue
        if p['trans_ab']:
            TransAB(p)
    # if (p.direct=1) or (p.direct=5) then TransAB_NoChange(p); // 横板-层板类
    # if (p.direct=2) or (p.direct=3) then TransAB_NoChange(p); // 竖横板-背板类
    # AB面数据输出
        for j in range(0,101):
            if p['ahole_index'][j] >= 0:
                phinfo= mHPInfoList[p['ahole_index'][j]]  # phinfo 未确定
                if (p['direct'] == 5) or (p['direct'] == 3) or (p['direct'] == 4):# then // 侧板-竖纹，背板-竖纹
                    p['a_hole_info'] = p['a_hole_info'] + '(%d,%d,%s,%d),'%(phinfo.x, phinfo.y, phinfo.r, phinfo.offset)
                if (p['direct'] == 2) or (p['direct'] == 1) or (p['direct'] == 6): #then // 层板-横纹
                    #print 'phinfo.offset=',phinfo.offset
                    p['a_hole_info'] = p['a_hole_info'] + '(%d,%d,%s,%d),'%(phinfo.y, phinfo.x, phinfo.r, phinfo.offset)
            if p['bhole_index'][j] >= 0:
                phinfo = mHPInfoList[p['bhole_index'][j]]
                if (p['direct'] == 5) or (p['direct'] == 3) or (p['direct'] == 4):  # then // 侧板-竖纹，背板-竖纹
                    p['b_hole_info'] = p['b_hole_info'] + '(%d,%d,%s,%d),'%(phinfo.x, phinfo.y, phinfo.r, phinfo.offset)
                if (p['direct'] == 2) or (p['direct'] == 1) or (p['direct'] == 6): # then // 层板-横纹
                    p['b_hole_info'] = p['b_hole_info'] + '(%d,%d,%s,%d),'%(phinfo.y, phinfo.x,  phinfo.r, phinfo.offset)
        s1 = ''
        s2 = ''
        if p['hole_back_cap'] > 0 :
            s1 =str(p['hole_back_cap'])
        if p['hole_2_dist'] > 0 :
            s2 = str(p['hole_2_dist'])
        p['holeconfig_flag'] = p['holeconfig_flag'].replace('$X',s1)
        p['holeconfig_flag'] = p['holeconfig_flag'].replace('$D',s2)
def ToBGInfoX2DGraphSizeToBomSize(l, p, h, direct):
    bl = l
    bp = p
    bh = h
    # # 'in'
    if direct == 1:  # 宽深高
        bl = l
        bp = p
        bh = h
    if direct == 2:  # 宽高深
        bl = l
        bp = h
        bh = p
    if direct == 3:  # 高宽深
        bl = h
        bp = l
        bh = p
    if direct == 4:  # 高深宽
        bl = h
        bp = p
        bh = l
    if direct == 5:  # 深宽高
        bl = p
        bp = l
        bh = h
    if direct == 6:  # 深高宽
        bl = p
        bp = h
        bh = l
    return bl,bp,bh
def ToBGInfoX2D(p, gBGHash, mHPInfoList):
    Result = ''
    Plist = []
    l = p['l']
    w = p['p']
    di = 0
    if p['bg'] == '':
        return ''
    # X2dName = Currentpath + '\\BaseGraph\\' + p['bg'] + '.x2d'
    # X2dPath1 = os.path.dirname(X2dName) + '\\'
    # if not os.path.exists(X2dPath1):
    #     os.makedirs(X2dPath1)
    # X2dNamePath = X2dPath + p['bg'] + '.x2d'
    # #BaseGraph 文件夹中不存在 x2d文件，则返回
    # if not os.path.exists(X2dNamePath):
    #     return
    # if not os.path.exists(X2dName):
    #     replaceXmlEncoding(X2dNamePath, X2dName)
    #
    # DOMTree = xml.dom.minidom.parse(X2dName)
    # collection = DOMTree.documentElement
    # root = collection  # 解析那段xml
    if p['bg'].encode('gb2312') not in gBGHash:
        return ''
    xmlContent = gBGHash[p['bg'].encode('gb2312')]
    if xmlContent == '':
        return ''
    root = ET.fromstring(xmlContent)  # 解析那段xml
    for i in range(0, len(root)):
        node = ''
        if root[i].tag == 'PlaneXY':  # PlaneXY
            node = root[i]
            tystr = node.get('Type', '')
            if tystr != 'Polygon':
                node = ''
        if node == '' and root[i].tag == 'PlaneXZ':
            node = root[i]
            tystr = ''
            tystr = node.get('Type', '')
            if tystr != 'Polygon':
                node = ''
        if node == '' and root[i].tag == 'PlaneYZ':
            node = root[i]
            tystr = ''
            tystr = node.get('Type', '')
            if tystr != 'Polygon':
                node = ''
        if node != '':
            attri = ''
            attri = node.get('X', '')
            if attri != '':
                sx = attri
            attri = node.get('Y', '')
            if attri != '':
                sy = attri
            x0 = 0
            y0 = 0
            di = 1
            if p['direct'] == 3 or p['direct'] == 4 or p['direct'] == 5:
                di = 0
            ll, pp, hh = ToBGInfoX2DGraphSizeToBomSize(Delphi_Round(p['l']), Delphi_Round(p['p']), Delphi_Round(p['h']), p['direct'])
            if node.tag == 'PlaneXY':
                l = ll
                w = pp
            if di == 1:
                l = p['gl']
                w = p['gp']
            if node.tag == 'PlaneXZ':
                l = ll
                w = hh
            if di == 1:
                l = p['gl']
                w = p['gh']
            if node.tag == 'PlaneYZ':
                l = pp
                w = hh
                if di == 1:
                    l = p['gp']
                    w = p['gh']
            mExp = {}
            mExp['L'] = l
            mExp['W'] = w
            mExp['CA'] = p['var_args'][0]
            mExp['CB'] = p['var_args'][1]
            mExp['CC'] = p['var_args'][2]
            mExp['CD'] = p['var_args'][3]
            mExp['CE'] = p['var_args'][4]
            mExp['CF'] = p['var_args'][5]
            mExp['CG'] = p['var_args'][6]
            mExp['CH'] = p['var_args'][7]
            mExp['CI'] = p['var_args'][8]
            mExp['CJ'] = p['var_args'][9]
            mExp['CK'] = p['var_args'][10]
            mExp['CL'] = p['var_args'][11]
            mExp['CM'] = p['var_args'][12]
            mExp['CN'] = p['var_args'][13]
            mExp['CO'] = p['var_args'][14]
            mExp['CP'] = p['var_args'][15]
            for i in range(1, len(node) + 1):
                cnode0 = node[i - 1]
                x0 = float(nowSetSubject(cnode0.get('X'), mExp))
                y0 = float(nowSetSubject(cnode0.get('Y'), mExp))
                if i == len(node):
                    cnode = node[0]
                else:
                    cnode = node[i]
                x1 = float(nowSetSubject(cnode.get('X'), mExp))
                y1 = float(nowSetSubject(cnode.get('Y'), mExp))
                xx0 = 0
                yy0 = 0
                xx1 = 0
                yy1 = 0
                if cnode0.get('XA','') != '':
                    try: xx0 = float(cnode0.get('XA', 0))
                    except: xx0 = float(nowSetSubject(cnode0.get('XA', 0), mExp))
                if cnode0.get('YA','') !='':
                    try: yy0 = float(cnode0.get('YA', 0))
                    except: yy0 = float(nowSetSubject(cnode0.get('YA', 0), mExp))
                if cnode.get('XA','') != '':
                    try: xx1 = float(cnode.get('XA', 0))
                    except: xx1 = float(nowSetSubject(cnode.get('XA', 0), mExp))
                if cnode.get('YA','') != '' and cnode.get('YA','')!='0.00' :
                    try:
                        yy1 = float(cnode.get('YA', 0))
                    except:
                        #print 'u1=',float(cnode0.get('YA', 0))
                        string = cnode.get('YA', 0)
                        yy1 = float(nowSetSubject(string, mExp))
                if di == 1:
                    t1 = x0
                    t2 = y0
                    x0 = p['p'] - t2
                    y0 = t1
                    t1 = x1
                    t2 = y1
                    x1 = p['p'] - t2
                    y1 = t1
                    xx0, yy0 = Swap(xx0, yy0)
                    xx1, yy1 = Swap(xx1, yy1)
                if (cnode0.tag == 'Point'):
                    if not ((x0 == x1) and (y0 == y1)):
                        pline = {}
                        pline['x0'] = x0 + xx0
                        pline['y0'] = y0 + yy0
                        if len(Plist) > 0:
                            pline0 = Plist[len(Plist) - 1]
                            pline['x0'] = pline0['x1']
                            pline['y0'] = pline0['y1']
                        pline['x1'] = x1 + xx1
                        pline['y1'] = y1 + yy1
                        pline['r'] = 0
                        Plist.append(pline)
                if cnode0.tag == 'Arc':
                    angle = 0
                    attri = cnode0.get('Angle', '')
                    if (attri != ''):
                        angle = int(attri)
                        if angle >= 0:
                            angle = -1
                        else:
                            angle = 1
                    attri = cnode0.get('R')
                    attrivalue = nowSetSubject(attri, mExp)
                    r = angle * attrivalue
                    if not ((x0 == x1) and (y0 == y1)):
                        pline = {}
                        pline['x0'] = x0 + xx0
                        pline['y0'] = y0 + yy0
                        if len(Plist) > 0:
                            pline0 = Plist[len(Plist) - 1]
                            pline['x0'] = pline0['x1']
                            pline['y0'] = pline0['y1']
                        pline['x1'] = x1 + xx1
                        pline['y1'] = y1 + yy1
                        pline['r'] = 0
                        Plist.append(pline)
    # print 'Plist=',len(Plist)
    p['a_hole_info'] = ''
    p['b_hole_info'] = ''
    # AB面数据输出
    for i in range(0, 101):
        if p['ahole_index'][i] >= 0:
            phinfo = mHPInfoList[p['ahole_index'][i]]
            if di == 1:  # then // 侧板-竖纹，背板-竖纹
                p['a_hole_info'] = p['a_hole_info'] + '(%d,%d,%s,%d),'%(p['p'] - phinfo.y, phinfo.x, phinfo.r,phinfo.offset)
            else:  # then // 层板-横纹
                p['a_hole_info'] = p['a_hole_info'] + '(%d,%d,%s,%d),'%(phinfo.x, phinfo.y, phinfo.r,phinfo.offset)
        if p['bhole_index'][i] >= 0:
            phinfo = mHPInfoList[p['bhole_index'][i]]
            if di == 1:  # then // 侧板-竖纹，背板-竖纹
                p['b_hole_info'] = p['b_hole_info'] + '(%d,%d,%s,%d),'%(p['p'] - phinfo.y, phinfo.x, phinfo.r,phinfo.offset)
            else:  # then // 层板-横纹
                #print 'phinfo.offset=', phinfo.offset,type(phinfo.offset),type(phinfo.x),type(phinfo.y),type(phinfo.r),phinfo.r
                p['b_hole_info'] = p['b_hole_info'] + '(%d,%d,%s,%d),'%(phinfo.x, phinfo.y, phinfo.r,phinfo.offset)
        if (p['is_outline']) or (p['is_output_bgdata'] == 1):
            for i in range(0, len(Plist)):
                pline = Plist[i]
                Result = Result + '(%.1f,%.1f,%.1f,%.1f,%.1f),'%(pline['x0'], pline['y0'], pline['x1'],
                                                                       pline['y1'], pline['r'])
    return Result
#计算
def LoadChildBom(ppoi, cid, boardheight, string,bomlist, pid, l, p, h, mat, color, memo, gno, gdes, gcb, myclass, bomstd, num):
    Result = 0
    if string == '' : return
    bomname = string
    if bomname not in childbomHash:
        return
    clist = childbomHash[bomname]
    id = pid * 100
    exp ={}
    exp['L'] = l
    exp['P'] = p
    exp['H'] = h
    exp['BH'] = boardheight
    exp['mBHValue'] = boardheight
    for i in range(0,len(clist)):
        pcbomrule = clist[i]
        Result = Result + 1
        if not ((pcbomrule.lmin <= l) and (pcbomrule.lmax >= l) and (pcbomrule.dmin <= p) and (pcbomrule.dmax >= p)
                and (pcbomrule.hmin <= h) and (pcbomrule.hmax >= h)) : continue
        sl = pcbomrule.l
        sp = pcbomrule.p
        sh = pcbomrule.h
        il = nowSetSubject(sl,exp)
        ip = nowSetSubject(sp,exp)
        ih = nowSetSubject(sh,exp)
        for j in range(0,pcbomrule.q):
            p2 = {}
            InitBomOrderItem(p2)
            for k in range(0,16):
                p2['var_names'][k] = ppoi['var_names'][k]
                p2['var_args'][k]= ppoi['var_args'][k]
            p2['cid'] = cid
            p2['nodename'] = pcbomrule.bomtype
            p2['direct'] = 0
            p2['code'] = pcbomrule.ono
            p2['holestr'] = pcbomrule.holestr
            p2['kcstr'] = pcbomrule.kcstr
            p2['memo'] = ''
            p2['num'] = 1 * num
            p2['isoutput'] = True
            p2['myclass'] = myclass
            p2['bomtype'] = pcbomrule.bomtype
            p2['id'] = id
            p2['pid'] = pid
            p2['name'] = pcbomrule.name
            p2['x'] = 0
            p2['y'] = 0
            p2['z'] = 0
            p2['gl'] = il
            p2['gp'] = ip
            p2['gh'] = ih
            p2['l'] = il
            p2['p'] = ip
            p2['h'] = ih
            p2['ox'] = 0
            p2['oy'] = 0
            p2['oz'] = 0
            p2['parent'] = None
            if pcbomrule.color != '' :
                p2['color'] = pcbomrule.color
            else:
                p2['color'] = color
            p2['childnum'] = 0
            p2['mat'] = mat
            if pcbomrule.mat != '*' :
                p2['mat'] = pcbomrule.mat
            p2['lfb'] = int(pcbomrule.lfb)
            p2['llk'] = int(pcbomrule.llk)
            p2['wfb'] = int(pcbomrule.wfb)
            p2['wlk'] = int(pcbomrule.wlk)
            p2['bl'] = int(il - p2['lfb'] - p2['llk'])
            p2['bp'] = int(ip - p2['wfb'] - p2['wlk'])
            p2['bh'] = int(ih)
            p2['direct'] = 0
            p2['memo'] = pcbomrule.memo
            p2['memo'] = p2['memo'].replace('[P]', memo)
            for k in range(0,16):
                p2['memo'] = p2['memo'].replace('[$C%s]'% (chr(65 + k)), str(p2['var_args'][k]))
                p2['kcstr'] = p2['kcstr'].replace('[$C%s]'% (chr(65 + k)), str(p2['var_args'][k]))
            p2['fbstr'] = pcbomrule.fbstr
            p2['desc'] = pcbomrule.name
            p2['gdes'] = gdes
            p2['gno'] = gno
            p2['gcb'] = gcb
            p2['extra'] = ppoi['extra']
            p2['a_hole_info'] = pcbomrule.a_face
            p2['b_hole_info'] = pcbomrule.b_face
            p2['holeid'] = -1
            p2['kcid'] = -1
            p2['bomstd'] = pcbomrule.bomstd
            if bomstd != '' and bomstd != None: p2['bomstd'] = bomstd  # // 继承父模块的判定规则
            p2['holetyp'] = 1
            p2['bg_filename'] = pcbomrule.bg_filename
            p2['mpr_filename'] = pcbomrule.mpr_filename
            p2['bpp_filename'] = pcbomrule.bpp_filename
            if p2['bg_filename'] != '' :
                p2['is_output_bgdata'] = 1
            else:
                p2['is_output_bgdata'] = 0
            if p2['mpr_filename'] != '' :
                p2['is_output_mpr']= 1
            else:
                p2['is_output_mpr']= 0
            if p2['bpp_filename'] != '' :
                p2['is_output_bpp']= 1
            else:
                p2['is_output_bpp']= 0
                p2['direct_calctype']= 1
            if pcbomrule.direct_calctype == 1 : p2['direct_calctype'] = 2
            p2['youge_holecalc'] = 0
            p2['workflow']= pcbomrule.workflow
            p2['llfb'] = pcbomrule.llfb
            p2['rrfb'] = pcbomrule.rrfb
            p2['ddfb']= pcbomrule.ddfb
            p2['uufb']= pcbomrule.uufb
            p2['fb'] = pcbomrule.fb
            p2['extend'] = ppoi['extend']
            p2['group'] = ppoi['group']
            p2['blockmemo'] = ppoi['blockmemo']
            p2['devcode'] = pcbomrule.devcode
            p2['number_text'] = ppoi['number_text']
            #// result:= result + 1; #// 2019 - 03 - 13
            bomlist.append(p2)
            id = id+1
    return Result
def CalcLineCombine(bomlist, mProductList):
    for k in range(0,len(mProductList)):
  # 统计线性物体
        for i in range(0,len(bomlist)):
            p = bomlist[i]
            # if 'cid' not in p:  #问题二：cid 不是p 的属性
            #     p['cid'] = 0
            if p['cid'] != k :
                continue
            ## json.dumps(p,ensure_ascii=False)
            if not p['isoutput']:
                continue
            if 'linecalc' not in p:    #问题一：linecalc 不是p 的属性
                p['linecalc'] = ''
            if (p['linecalc'] != ''):
                for j in range(i+1,len(bomlist)):
                    p2 = bomlist[j]
                    if p2['cid'] != k :
                        continue
                    if not p2['isoutput']:
                        continue
                    if (p['linecalc'] == p2['linecalc']):
                        p2['bl']= p2['bl'] + p['bl']
                        p['isoutput'] = False
                        break
    for i in range(0,len(bomlist)):
        p = bomlist[i]
        if not p['isoutput'] :
            continue
        if (p['linecalc'] != ''):
            if p['linemax'] == 99999:
                p['num'] = 1
                p['l']= round(p['bl'])
            else:
                p['num'] = round(p['bl'] / p['linemax'])
                if p['bl'] > (p['linemax'] * p['num']):
                    p['num'] =p['num'] + 1
                    p['l'] = p['linemax']
                    p['bl'] = p['linemax']
def CalcSeq(bomlist):
    seqInfoHash = {}
    classseqInfoHash = {}
    dataDBfile = RootPath + '\\data\\data.mdb'
    conn = pypyodbc.win_connect_mdb(r'DRIVER={Microsoft Access Driver (*.mdb  *.accbd)};DBQ=' + dataDBfile)
    cur = conn.cursor()
    sql = "select bomname,bomseq from base_seqinfo"
    cur.execute(sql)
    u = cur.fetchall()
    for i in u:
        if i[0] == '':
            continue
        seqInfoHash[i[0]] = i[1]
    sql1 = "select * from base_classseqinfo where ID>1000 order by seq asc"
    cur.execute(sql1)
    u1 = cur.fetchall()
    for i in u1:
        if i[0] == '':
            continue
        classseqInfoHash[i[1]] = i[2]
    for i in range(0,len(bomlist)):
        p = bomlist[i]
        if p['name']=='':
            p['seq'] = 0
        else:
            if p['name'] in seqInfoHash:
                if seqInfoHash[p['name']] =='': p['seq'] = -1
                else: p['seq'] = seqInfoHash[p['name']]
            else:
                p['seq'] = -1
        if p['myclass'] in classseqInfoHash:
            if classseqInfoHash[p['myclass']] =='': p['classseq'] = -1
            else: p['classseq'] = classseqInfoHash[p['myclass']]
        else:
            p['classseq'] = -1
def GetBomUserDefine(p):
    if 'userdefine' not in p:
        return
    if p['userdefine'] == '':
        return
    wstr = p['userdefine']
    N1 = wstr.find(';')
    while N1 > 0 :
        s1 = wstr[0:N1]
        n2 = s1.find(':')
        if n2 > 0 :
            s2 = s1[n2+1: len(s1)]
            s1 = s1[0, n2]
            if s1 == 'Na':
                p['name'] = s2
            if s1 == 'Cl':
                p['color'] = s2
            if s1 == 'Mt':
                p['mat'] =s2
        wstr = wstr[N1+1:len(wstr) ]
        N1 = wstr.find(';')
def GetMatAlias(p, mat, color, bh, alias, alias2, alias3, gBoardMatList):
    p['mat'] = mat
    p['mat2'] = ''
    p['mat3'] = ''
    for i in range(0, len(gBoardMatList)):
        Mp = gBoardMatList[i]
        if Mp.color == '':
            continue
        if (Mp.name == mat) and (Mp.color == p['color']) and ((Mp.bh == 0) or (Mp.bh == int(bh))):
            if Mp.alias:
                p['mat'] = Mp.alias
            if Mp.alias2:
                p['mat2'] = Mp.alias2
            if Mp.alias:
                p['mat3'] = Mp.alias3
            return
    for i in range(0, len(gBoardMatList)):
        Gp = gBoardMatList[i]
        if Gp.color != '':
            continue
        if (Gp.name == mat) and ((Gp.bh == 0) or (Gp.bh == int(bh))):
            if Gp.alias:
                p['mat'] = Gp.alias
            if Gp.alias2:
                p['mat2'] = Gp.alias2
            if Gp.alias:
                p['mat3'] = Gp.alias3
            return
def CalcIsTHole(bomlist,slidinglist, doorslist, mIIHoleCalcRule, mHPInfoList, gBoardMatList):   #mHPInfoList未知
    for i in range(0,len(bomlist)):
        p = bomlist[i]
        if str(round(p['bh'])) in mIIHoleCalcRule and (mIIHoleCalcRule != {} ) and (mIIHoleCalcRule[str(round(p['bh']))]== 2) :
            continue
        for j in range(0,101):
            if p['ahole_index'][j] >= 0:
                phinfo = mHPInfoList[p['ahole_index'][j]]
                if phinfo.htype == 'I' : # 垂直孔
                    for k in range(0,101):
                        if p['bhole_index'][k] >= 0 :
                            phinfo2 = mHPInfoList[p['bhole_index'][k]]
                            if (phinfo2.htype == 'I') and (phinfo.x == phinfo2.x) and (
                                    phinfo.y == phinfo2.y) and (phinfo.r == phinfo2.r): #// 垂直孔
                                phinfo.htype = 'I+I'
                                phinfo2.htype = 'I+I'
                                break
    for i in range(0,len(bomlist)):
        p = bomlist[i]
        GetBomUserDefine(p)
    # 物料报表的材料别名转换
    for i in range(0,len(bomlist)):
        p = bomlist[i]
        GetMatAlias(p,p['mat'], p['color'], p['h'],p['mat'], p['mat2'], p['mat3'],gBoardMatList)
    for i in range(0, len(slidinglist)):
        pslibom = slidinglist[i]
        GetMatAlias(pslibom,pslibom['mat'], pslibom['color'], Delphi_Round(pslibom['h']), pslibom['mat'], pslibom['mat2'], pslibom['mat3'],gBoardMatList)
    for i in range(0, len(doorslist)):
        pslibom = doorslist[i]
        GetMatAlias(pslibom,pslibom['mat'], pslibom['color'], Delphi_Round(pslibom['h']), pslibom['mat'], pslibom['mat2'], pslibom['mat3'], gBoardMatList)
def FindProperPriceRecord(bomQuolist):
    def FindPriceTable(tablename, mat, bh):
        Result = None
        for i in range(0, len(ptableList)):
            p = ptableList[i]
            if (tablename == p.name) and ((mat == p.mat) or (p.mat =='*')) and ((p.bh==0) or (p.bh==bh)):
                Result = p
                break
        return Result
    def MyStrToFloat(str):
        Result = 0
        if str:
            Result = float(str)
        return Result
    if bomQuolist == []:
        return
    for i in range(0, len(bomQuolist)):
        pbom = bomQuolist[i]
        if not pbom['isoutput']: continue
        pbom['cl'] = pbom['l']
        pbom['cp'] = pbom['p']
        pbom['ch'] = pbom['h']
        pbom['isoutput'] = False
        pbom['cost'] = 0
        if pbom['desc'] in QuoruleHash:
            rulelist = QuoruleHash[pbom['desc']]
            pbom['price'] = -1
            pbom['price2'] = -1
            pbom['totalprice'] = 0
            pbom['totalprice2'] = 0
            pbom['num'] = 0
            pbom['isoutput'] = True
            pbom['pricetype'] = '报价错误'
            for j in range(0, len(rulelist)):
                prule = rulelist[j]
                msg = ''
                condition = 0
                condition = condition + 1
                if prule.l > 0:
                    msg = msg + '当前判定条件有宽度定值， 计算时候取其宽度值： '+str(prule.l)
                else:
                    msg = msg + '当前判断条件无宽度定值；' +  '\n'
                if (prule.lmin > 0) or (prule.lmax > 0):
                    if pbom['l'] >= prule.lmin and (pbom['l'] <= prule.lmax):
                        condition = condition + 1
                    else:
                        continue
                    msg = msg + '当前判断条件宽度值处于；' + str(prule.lmin) + '和' + str(prule.lmax) + '之间' + '\n'
                else:
                    condition = condition +1
                    msg = msg + '当前判断条件宽度值任意；' +  '\n'
                condition = condition + 1
                if prule.p > 0 :
                    msg = msg + '当前判断条件有深度定值，计算时候取该深度值：' + str(prule.p) +  '\n'
                else:
                    msg = msg + '当前判断条件无深度定值；' + '\n'
                if (prule.pmin > 0) or (prule.pmax > 0) :
                    if (pbom['p'] >= prule.pmin) and (pbom['p'] <= prule.pmax) :
                        condition = condition +1
                    else:
                        continue
                    msg = msg + '当前判断条件深度值处于；' + str(prule.pmin) + '和' + str(prule.pmax) + '之间' + '\n'
                else:
                    condition = condition +1
                    msg = msg + '当前判断条件深度值任意；' + '\n'
                condition = condition +1
                if prule.h > 0:
                    msg = msg + '当前判断条件有高度定值，计算时候取该高度值：' + str(prule.h) + '\n'
                else:
                    msg = msg + '当前判断条件无高度定值；' + '\n'
                if (prule.hmin > 0) or (prule.hmax > 0):
                    if (pbom['h'] >= prule.hmin) and (pbom['h'] <= prule.hmax):
                        condition = condition +1
                    else:
                        continue
                    msg = msg + '当前判断条件高度值处于；' + str(prule.hmin) + '和' + str(prule.hmax) + '之间' + '\n'
                else:
                    condition = condition +1
                    msg = msg + '当前判断条件高度值任意；' + '\n'
                if condition == 6:
                    if pbom['desc'] in classHash:
                        list2 = classHash[pbom['desc']]
                        if len(list2) <= 0 : continue
                        pclass = list2[0]
                        # 获得报价分类
                        pbom['pricetype'] = pclass.pricetype
                        pbom['myunit'] = pclass.myunit
                        pbom['soglaname'] = prule.outname
                        pbom['linemax'] = prule.l
                        pbom['num'] = 1
                        pbom['sale_type'] = prule.sale_type
                        pbom['is_calc_cost'] = pclass.is_calc_cost
                        pbom['cost']= 0
                        # pbom.myclass:= pclass.myclass;
                        # 门板材料不为空, 则表示需要计算门板材料, 这里似乎有问题
                        if (prule.slidingmat):
                            if (pbom['mat'] != prule.slidingmat) and (prule.slidingmat != '*') :
                                continue
                        if prule['PriceTable'] != '':
                            ptable = FindPriceTable(prule.PriceTable, pbom['mat'], pbom['bh'])
                            pbom['isoutput'] = True
                            pbom['price'] = -1
                            pbom['price2'] = -1
                            if ptable ==None : break
                            pbom['price'] = MyStrToFloat(ptable.price1)
                            pbom['price2'] = MyStrToFloat(ptable.price2)
                            pbom['cost'] = MyStrToFloat(ptable.cost)
                            if ptable.price_exp1 : # 需要按照公式计算板材单价
                                exp = {}
                                if pbom.price_calctype : # 先根据全局的板材单价公式计算
                                    exp['$板材单价'] = str(pbom['price'])
                                    pbom['price'] = float(nowSetSubject(pbom['price_calctype'],exp))
                                exp['$板材单价'] = str(pbom['price'])
                                pbom['price'] = float(nowSetSubject(ptable.price_exp1, exp))
                            if ptable.price_exp2 : # 需要按照公式计算板材单价
                                exp = {}
                                if pbom.price_calctype : # 先根据全局的板材单价公式计算
                                    exp['$板材单价'] = str(pbom['price'])
                                    pbom['price'] = float(nowSetSubject(pbom['price_calctype'],exp))
                                exp['$板材单价'] = str(pbom['price'])
                                pbom['price'] = float(nowSetSubject(ptable.price_exp2, exp))
                        else:
                            pbom['price'] = MyStrToFloat(prule.price1)
                            pbom['price2'] = MyStrToFloat(prule.price2)
                        # 输出报价
                        pbom['isoutput'] = True
                        pbom['isnotstd'] = prule.isnonstandard
                        if prule.l != 0 : pbom['cl'] = prule.l
                        if prule.p != 0 : pbom['cp'] = prule.p
                        if prule.h != 0 : pbom['ch'] = prule.h
                        break
if __name__ == '__main__':
    import logging
    logging.basicConfig(level="DEBUG")
    log = logging.getLogger(__name__)
    log.setLevel('DEBUG')
    xmlguid = '55faeb80e99211e9ad1db0fc36268ae0'
    xmlfile = 'D:\\nginx-1.0.11\\nginx-1.0.11\\html\\data\\Python\\UpLoadXml\\1a045e8f0c3711ea87c5b0fc36268ae0'#base_dir+'\\Python\\postxml\\3.xml'
    if (not os.path.exists(base_dir+'\\Python\\postxml\\')):
        os.makedirs(base_dir+'\\Python\\postxml\\')
    # with open(base_dir+'\\Python\\postxml\\1.xml','w+') as f:
    #     f.write(xml)
    LoadXML2Bom(xmlfile, base_dir)
    '''
        LoadXMLFile2Quo 不需要 mBDXMLList
    '''
    log.info('len of mProductList=' + str(len(mProductList)))
    log.info('len of bomlist=' + str(len(bomlist)))
    log.info('len of mXMLStringList=' + str(len(mXMLStringList)))
    log.info('len of mDoorList=' + str(len(mDoorList)))
    log.info('len of doorslist=' + str(len(doorslist)))
    log.info('len of slidinglist=' + str(len(slidinglist)))
    log.info('len of desslidinglist=' + str(len(desslidinglist)))
    log.info('len of desdoorlist=' + str(len(desdoorlist)))
    log.info('len of bomstdList=' + str(len(bomstdList)))
    with open(base_dir+'\\Python\\PythontoBomJson\\PriceJson\\'+xmlguid + '.txt', 'w+') as f:
        f.write(json.dumps(JsonPrice, ensure_ascii=False))