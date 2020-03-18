#  -*- coding:utf-8 -*-
'''
vesion 1.0.0
2019/10/29
author:litao
'''
import json,os,shutil,zipfile
import  numpy as np
import chardet
import hashlib
from ctypes import *
import xml.etree.ElementTree as ET
import copy
import time
import sys
import configparser
import pypyodbc
from .GlobalInitData import *
import imp
imp.reload(sys)

class Returnorder(object):
    def __init__(self,collection):
        # from xml.dom.minidom import parse
        # import xml.dom.minidom
        # DOMTree = xml.dom.minidom.parse(xmlfile)
        # collection = DOMTree.documentElement
        self.gQDDataID = collection.getAttribute('DATAID'.decode('utf8'))
        self.gQDSoftVer = collection.getAttribute("QD版本".decode('utf8'))
        self.gQDDataVer = collection.getAttribute("版本".decode('utf8'))
        self.mOrderName = collection.getAttribute("订单名称".decode('utf8'))
        self.mDistributor = collection.getAttribute("经销商".decode('utf8'))
        self.mAddress = collection.getAttribute("地址".decode('utf8'))
        self.mPhone = collection.getAttribute("电话".decode('utf8'))
        self.mFax = collection.getAttribute("传真".decode('utf8'))
        self.mMemo = collection.getAttribute("备注".decode('utf8'))
        self.mDateTime = collection.getAttribute("订单日期".decode('utf8'))
        self.mCustomerName = collection.getAttribute("客户姓名".decode('utf8'))
        self.mCustomerCellPhone = collection.getAttribute("客户手机".decode('utf8'))
        self.mCustomerPhone = collection.getAttribute("客户电话".decode('utf8'))
        self.mCustomerAddress = collection.getAttribute("客户地址".decode('utf8'))
        self.mExtra = collection.getAttribute("DBCC".decode('utf8'))
        self.mDBCC = collection.getAttribute("Extra".decode('utf8'))
    def getorderinfo(self):
        OrdDict = {}
        OrdDict['DATAID'] = self.gQDDataID.encode('utf8')
        OrdDict['QD版本'] = self.gQDSoftVer.encode('utf8')
        OrdDict['版本'] = self.gQDDataVer.encode('utf8')
        OrdDict['订单名称'] = self.mOrderName.encode('utf8')
        OrdDict['经销商'] = self.mDistributor.encode('utf8')
        OrdDict['地址'] = self.mAddress.encode('utf8')
        OrdDict['电话'] = self.mPhone.encode('utf8')
        OrdDict['传真'] = self.mFax.encode('utf8')
        OrdDict['备注'] = self.mMemo.encode('utf8')
        OrdDict['订单日期'] = self.mDateTime.encode('utf8')
        OrdDict['客户姓名'] = self.mCustomerName.encode('utf8')
        OrdDict['客户手机'] = self.mCustomerCellPhone.encode('utf8')
        OrdDict['客户电话'] = self.mCustomerPhone.encode('utf8')
        OrdDict['客户地址'] = self.mCustomerAddress.encode('utf8')
        OrdDict['Extra'] = self.mExtra.encode('utf8')
        OrdDict['DBCC'] = self.mDBCC.encode('utf8')
        return OrdDict
class TMyCalcItem(object):
    def __init__(self):
        self.m = np.matrix([[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]])
        self.v = [0,0,0]
        self.space = ''
        self.space_x = 0
        self.space_y = 0
        self.space_z = 0
        self.space_id = 0
        self.sozflag = ''
        self.bl = 0
        self.bp = 0
        self.bh = 0
        self.llfb = 0
        self.rrfb = 0
        self.ddfb = 0
        self.uufb = 0
        self.fb = 0
        self.pl = 0
        self.pd = 0
        self.ph = 0
        self.lx = 0
        self.ly = 0
        self.lz = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.l = 0
        self.p = 0
        self.h = 0
        self.gl = 0
        self.gp = 0
        self.gh = 0
        self.o_direct = 0
        self.direct = 0
        self.holeid = 0
        self.kcid = 0
        self.var_args = [0]*16
        self.ahole_index = [0]*101
        self.bhole_index = [0]*101
        self.akc_index = [0]*101
        self.bkc_index = [0]*101
        self.is_calc_holeconfig = [0]*6
        self.is_holeface_touch = [0]*6
        #基础图形描述
        self.bg_l_minx = 0
        self.bg_l_maxx = 0
        self.bg_r_minx = 0
        self.bg_r_maxx = 0
        self.bg_l_miny = 0
        self.bg_l_maxy = 0
        self.bg_r_miny = 0
        self.bg_r_maxy = 0
        self.bg_d_minx = 0
        self.bg_d_maxx = 0
        self.bg_u_minx = 0
        self.bg_u_maxx = 0
        self.bg_d_miny = 0
        self.bg_d_maxy = 0
        self.bg_u_miny = 0
        self.bg_u_maxy = 0
        self.bg_b_minx = 0
        self.bg_b_maxx = 0
        self.bg_f_minx = 0
        self.bg_f_maxx = 0
        self.bg_b_miny = 0
        self.bg_b_maxy = 0
        self.bg_f_miny = 0
        self.bg_f_maxy = 0
        #//第一个孔靠背的距离，两孔间距
        self.hole_back_cap = 0
        self.hole_2_dist = 0
        #zero_y 封边靠档
        self.zero_y = 0
        self.xptlist_jx = 0
        self.xptlist_pl = 0
        self.isxx = 0 #是否斜
        self.holeface = 0
        self.holeinfo = 0
        self.holeinfo = ''
        self.holeinfo_flag = 0
        self.bg = ''
        self.bdxmlid = ''
        self.mat = ''
        self.name = ''
        self.color = ''
        self.bdinfo = ''
        self.holeconfig_flag = ''
        self.kcconig_flag = ''
        self.bdxml = ''
        self.devcode = ''
        self.bhpt = []
        # Pointer
        self.data = 0
        self.big_p = None
        self.self_p = None
        self.l_item0 = None
        self.r_item0 = None
        self.u_item0 = None
        self.d_item0 = None
        self.l_item = None
        self.r_item = None
        self.u_item = None
        self.d_item = None
        self.guid = ''
    def Copy(self,item):
        self.m = item.m
        self.v = item.v
        self.space = item.space
        self.space_x = item.space_x
        self.space_y = item.space_y
        self.space_z = item.space_z
        self.sozflag = item.sozflag
        self.bl = item.bl
        self.bp = item.bp
        self.bh = item.bh
        self.llfb = item.llfb
        self.rrfb = item.rrfb
        self.ddfb = item.ddfb
        self.uufb = item.uufb
        self.fb = item.fb
        self.pl = item.pl
        self.pd = item.pd
        self.ph = item.ph
        self.lx = item.lx
        self.ly = item.ly
        self.lz = item.lz
        self.x = item.x
        self.y = item.y
        self.z = item.z
        self.l = item.l
        self.p = item.p
        self.h = item.h
        self.gl = item.gl
        self.gp = item.gp
        self.gh = item.gh
        self.o_direct = item.o_direct
        self.direct = item.direct
        self.holeid = item.holeid
        self.kcid = item.kcid
        self.var_args[i] = [item.var_args[i] for i in range(0,16)]
        for i in range(0,101):
            self.ahole_index[i] = item.ahole_index[i]
            self.bhole_index[i] = item.bhole_index[i]
            self.akc_index[i] = item.akc_index[i]
            self.bkc_index[i] = item.bkc_index[i]
        for i in range(0, 6):
            self.is_calc_holeconfig[i] = item.is_calc_holeconfig[i]
            self.is_holeface_touch[i] = item.is_holeface_touch[i]
        self.bg_l_minx = item.bg_l_minx
        self.bg_l_maxx = item.bg_l_maxx
        self.bg_r_minx = item.bg_r_minx
        self.bg_r_maxx = item.bg_r_maxx
        self.bg_l_miny = item.bg_l_miny
        self.bg_l_maxy = item.bg_l_maxy
        self.bg_r_miny = item.bg_r_miny
        self.bg_r_maxy = item.bg_r_maxy
        self.bg_d_minx = item.bg_d_minx
        self.bg_d_maxx = item.bg_d_maxx
        self.bg_u_minx = item.bg_u_minx
        self.bg_u_maxx = item.bg_u_maxx
        self.bg_d_miny = item.bg_d_miny
        self.bg_d_maxy = item.bg_d_maxy
        self.bg_u_miny = item.bg_u_miny
        self.bg_u_maxy = item.bg_u_maxy
        self.bg_b_minx = item.bg_b_minx
        self.bg_b_maxx = item.bg_b_maxx
        self.bg_f_minx = item.bg_f_minx
        self.bg_f_maxx = item.bg_f_maxx
        self.bg_b_miny = item.bg_b_miny
        self.bg_b_maxy = item.bg_b_maxy
        self.bg_f_miny = item.bg_f_miny
        self.bg_f_maxy = item.bg_f_maxy
        self.hole_back_cap = item.hole_back_cap
        self.hole_2_dist = item.hole_2_dist
        self.zero_y = item.zero_y
        self.xptlist_jx = item.xptlist_jx
        self.xptlist_pl = item.xptlist_pl
        self.isxx = item.isxx
        self.holeface = item.holeface
        self.holeinfo = item.holeinfo
        self.holeinfo_flag = item.holeinfo_flag
        self.bg = item.bg
        self.name = item.name
        self.bdxmlid = item.bdxmlid
        self.mat = item.mat
        self.color = item.color
        self.bdinfo = item.bdinfo
        self.holeconfig_flag = item.holeconfig_flag
        self.kcconig_flag = item.kcconig_flag
        self.bdxml = item.bdxml
        self.devcode = item.devcode
        self.bhpt = [MyBigHolePoint for i in range(len(item.bhpt))]
        for i in range(len(item.bhpt)):
            self.bhpt[i] = item.bhpt[i]
        self.data = item.data
        self.big_p = item.big_p
        self.self_p = item.self_p
        self.l_item0 = item.l_item0
        self.r_item0 = item.r_item0
        self.u_item0 = item.u_item0
        self.d_item0 = item.d_item0
        self.l_item = item.l_item
        self.r_item = item.r_item
        self.u_item = item.u_item
        self.d_item = item.d_item
class hole(object):
    def __init__(self):
        self.wx = 0
        self.wy = 0
        self.wz = 0
        self.i_offset=[0,0,0]
        self.mx_x = 0
        self.mx_y = 0
        self.mx_z = 0
        self.p1 = TMyCalcItem()
        self.p2 = TMyCalcItem()
class THolePointInfo(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.hd = 0
        self.holeid = 0
        self.row = 0
        self.offset = 0
        self.smallcap = 0
        self.holecap = 0
        self.isii = 0
        self.b_bh = 0
        self.xx = 0
        self.yy = 0
        self.face = ''
        self.r = ''
        self.sr = ''
        self.sri = ''
        self.htype = ''
        self.c = 0
class THoleConfig(object):
    def __init__(self):
        self.id = 0
        self.name = ''
        self.l_bigname = ''
        self.l_smallname=''
        self.i_name = ''
        self.mx_name = ''
        self.l_holedepth = 0
        self.l_bigcap = 0
        self.l_smallcap = 0
        self.calctype = 0
        self.l_isoutput = 0
        self.i_isoutput = 0
        self.mx_isoutput = 0
        self.mx_calctype = 0
        self.mx_cap = 0
        self.ismirror = 0
        self.holecap = ''
        self.flag = ''
        self.flag2 = ''
        self.center_holecap = ''
        self.iscalc = 0
        self.bigface = 0
        self.myface = 0
        self.min = 0
        self.max = 0
        self.pkcap = 0
        self.holenum = 0
        self.center_holenum = 0
        self.bh = 0
        self.isoffset = 0
        self.b_isoffset = 0
        self.xo = ''
        self.yo = ''
        self.b_xo = ''
        self.b_yo = ''
        self.i_offsetvalue = 0
        self.algorithm = 0
        self.deleted = True
class TKCConfig(object):
    def __init__(self):
        self.id = 0
        self.name = ''
        self.flag = ''
        self.cutter = ''
        self.myface = 0
        self.min = 0
        self.max = 0
        self.x = 0
        self.y = 0
        self.l = 0
        self.w = 0
        self.device = 0
        self.deleted = True
class TKCInfo(object):
    def __init__(self):
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.l = 0
        self.w = 0
        self.kcid = ''
        self.device = 0
        self.flag = ''
        self.cutter = ''
        self.face = ''
class pluginob(object):
    def __init__(self):
        self.name = ''
        self.dll = ''
        self.handle = 0
class ErpMat(object):
    def __init__(self):
        self.id = 0
        self.name = ''
        self.mat = ''
        self.color = ''
        self.h = 0
        self.myclass = ''
        self.flag = ''
        self.myunit = ''
        self.deleted = True
class ReportOutputConfig(object):
    def __init__(self):
        self.bj_out_classname = True
        self.bj_out_myclass = False
        self.bj_out_name = False
        self.bj_out_mat = True
        self.bj_out_color = True
        self.bj_out_size = True
        self.bj_out_price = True
        self.wl_out_classname = True
        self.wl_out_myclass = False
        self.wl_out_name = True
        self.wl_out_mat = True
        self.wl_out_color = True
        self.wl_out_size = True
        self.wl_out_kc = True
        self.wl_out_fb = True
        self.wl_out_memo = True
        self.wl_out_hole = True
class BoardMat(object):
    def __init__(self):
        self.id = 0
        self.name = ''
        self.color = ''
        self.alias = ''
        self.alias2 = ''
        self.alias3 = ''
        self.bh = 0
#生产线配置
class TKCConfig(object):
    def __init__(self):
        # self.name = ''
        # self.bomstd = ''
        # self.hole = ''
        # self.id = 0
        # self.board_cut = 0
        # self.edge_banding = 0
        # self.punching = 0
        self.id = 0
        self.name = ''
        self.flag = ''
        self.cutter = ''
        self.myface = 0
        self.min = 0
        self.max = 0
        self.x = 0
        self.y = 0
        self.l = 0
        self.w = 0
        self.device = 0
        self.deleted = True
class des2wuliao(object):
    def __init__(self):
        self.key = ''
        self.s1 = ''
        self.s2 =''
        self.s3 = ''
        self.direct = 0
        self.no = ''
        self.oname = ''
class wujinruleclass(object):
    def __init__(self):
        self.myclass1 = ''
        self.myclass2 = ''
        self.lmin = 0
        self.lmax = 0
        self.pmin = 0
        self.pmax = 0
        self.hmin = 0
        self.hmax = 0
        self.lgflag = 0
        self.wjname = ''
        self.wjno = ''
        self.myunit = ''
        self.myunit2 = ''
        self.mat = ''
        self.color = ''
        self.wjid = 0
        self.num = 0
        self.price = 0
class BomRuleRec(object):
    def __init__(self):
        self.id = 0
        self.bh = 0
        self.myclass1 = ''
        self.myclass2 = ''
        self.mat =''
        self.lfb = 0
        self.llk = 0
        self.wfb = 0
        self.wlk = 0
        self.holestr = '',
        self.kcstr = ''
        self.memo = ''
        self.fbstr = ''
        self.is_outline = 0
        self.llfb = 0
        self.rrfb = 0
        self.uufb = 0
        self.ddfb = 0
        self.fb = 0
        self.deleted = True
class Bom2RuleRec(object):
    def __init__(self):
        self.id = 0
        self.lmax = 0
        self.lmin = 0
        self.dmax = 0
        self.dmin = 0
        self.hmax = 0
        self.hmin = 0
        self.bclass = ''
        self.pname = ''
        self.name = ''
        self.l = ''
        self.p = ''
        self.h = ''
        self.mat = ''
        self.color = ''
        self.lfb = 0
        self.llk = 0
        self.wfb = 0
        self.wlk = 0
        self.q = 0
        self.holestr = ''
        self.kcstr = ''
        self.ono = ''
        self.bomstd = ''
        self.bomtype = ''
        self.a_face = ''
        self.b_face =''
        self.memo = ''
        self.fbstr =''
        self.bg_filename = ''
        self.mpr_filename = ''
        self.bpp_filename = ''
        self.devcode = ''
        self.workflow = ''
        self.direct_calctype = 0
        self.youge_holecalc = 0
        self.llfb =0
        self.rrfb = 0
        self.uufb = 0
        self.ddfb = 0
        self.fb = 0
        self.deleted = True
class PBomStd(object):
    def __init__(self):
        self.myclass1 = ''
        self.myclass2 = ''
        self.lmax = 0
        self.lmin = 0
        self.dmax = 0
        self.dmin = 0
        self.hmax = 0
        self.hmin = 0
        self.stdflag = ''
        self.level = 0
  #尺寸判断
class linecalc(object):
    def __init__(self):
        self.name = ''
        self.linemax= 0
        
class PMRItem(object):
    def __init__(self):
        self.template = ''
        self.mytype = ''
        self.prefix = ''
        self.suffix = ''
        self.path = ''
        self.srcdll = ''
        self.combine = 0
        self.visible = 0
        self.filter_kl = 0
        self.filter_fb = 0
        self.filter_hole = 0
class Section(object):
    def __init__(self):
        self.parname = ''
        self.partext = ''
        self.T = 0
        self.flag = 0
        self.mytype = 0
        self.dotnum = 0
class MyBigHolePoint(object):
    def __init__(self):
        self.sx = ''
        self.sy = ''
        self.sr = ''
        self.srb = ''
        self.src = ''
        self.hdirect = ''
        self.face = ''
        self.holenum_x = 0
        self.holenum_y = 0
        self.hole_z = 0
        self.x = 0
        self.y = 0
        self.r = 0
        self.rb = 0
        self.ri = 0
class TGPPoint(object):
    def __init__(self):
        self.x =0
        self.y =0
#20191105
class PriceClass(object):
    def __init__(self):
        self.bj1 = ''
        self.bj2 = ''
        self.pricetype = ''
        self.myunit = ''
        self.myclass = ''
        self.factor = 0
        self.is_calc_cost = False
class PriceRule(object):
    def __init__(self):
        self.id = 0
        self.bj1 = ''
        self.bj2 = ''
        self.l = 0
        self.lmax = 0
        self.lmin = 0
        self.p = 0
        self.pmax = 0
        self.pmin = 0
        self.h = 0
        self.hmax = 0
        self.hmin = 0
        self.PriceTable = ''
        self.price1 = 0
        self.price2 = ''
        self.slidingmat = ''
        self.isnonstandard = False
        self.myclass = ''
        self.outname = ''
        self.sale_type = ''
class StrMap(object):
    def __init__(self):
        self.s1 = ''
        self.s2 = ''
        self.no = ''
        self.name = ''
        self.myclass = ''
def get_file_ext(filename):
    '''
    :param filename: '123.txt'
    :return: txt
    '''
    return  filename[filename.index('.') + 1:]
def ExtractFileExt(filename):
    '''
        :param filename: '123.txt'
        :return: .txt
        '''
    return filename[filename.index('.'):]
def ChangeFileExt(filename,filename2):
    '''
    :param filename: '123.txt'
    :param filename2: '' or '.db'
    :return: '123' or '123.db'
    '''
    return filename[0:filename.index('.')]+filename2
def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)
def DeleteDirectory(path):
    '''
    delete path
    :param path:r'D:\haha'
    :return:
    '''
    try:
        if not os.path.isdir(path): return
        shutil.rmtree(path)
    except Exception as e:
        print(e)
def DeleteFile(filename):
    '''
    :param filename: needed deleted filename
    :return:
    '''
    if os.path.exists(filename):
        os.remove(filename)
def CopyFile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print('6666666')
        return False
        #print "%s not exist!"%(srcfile)
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        if os.path.isfile(dstfile):
            os.remove(dstfile)
        shutil.copyfile(srcfile,dstfile)      #复制文件
        return True
def SimpleExpressToValue(holecap,mode,Extemp):
    Result = 0
    if holecap==None: return 0
    if len(holecap)<1: return 0
    buf = holecap
    strlen = len(holecap)
    #print holecap
    j = 0
    s1 = 0
    s2 = 0
    find = False
    while(not find):
        for i in range(0,strlen):
            if buf[i] =='(':
                if j==0:
                    s1 = i
                    s2 = 0
                j = j+1
            s2 = s2+1
            if buf[i] ==')':
                j = j-1
                if j == 0:
                    s=holecap[s1+1:s2-1]
                    v = SimpleExpressToValue(s,mode,Extemp)
                    s='('+s+')'
                    if mode == 1 : holecap = holecap.replace(s, str(v))
                    if mode == 2 : holecap = holecap.replace(s, str(v))
                    if mode == 3 : holecap = holecap.replace(s, str(v))
                    buf = holecap
                    strlen= len(holecap)
                    find= True
                    break
        find = True
    v =eval(holecap,Extemp)
    Result= 0
    if mode == 1 :
        Result = float(v)
    if mode == 2 :
        Result = int(v)
    if mode == 3 :
        Result =round(v)
    #print 'v=',v,'Result=',Result
    return Result
def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()
def nowSetSubject(string,Extemp):
    if isinstance(string, float) or isinstance(string, int) or string.isdigit():  #是数值就不需要替换的
        return int(Delphi_Round(float(string)))
    if string =='':
        return 0
    value = int(Delphi_Round(eval(string, Extemp)))
    return value
def mExpSetSubject(mExp,str1):  #此方法有用
    for key ,value in list(mExp.items()):
       str1 = str1.replace(key,str(mExp[key]))
    ## str1,type(str1)
    if str1=='':
        return 0
    Result = eval(str1)
    return Result
#可以保留
def OppositeFace(face):
    Result = face
    if face == 'Left' :
        Result = 'Right'
    elif face == 'Right' :
        Result = 'Left'
    elif face == 'Back' :
        Result = 'Front'
    elif face == 'Front' :
        Result = 'Back'
    elif face == 'Down' :
        Result = 'Up'
    elif face == 'Up' :
        Result = 'Down'
    return  Result
# def X2dToBdGraph(poi):
#     if poi.bdxml!='' :
#         Result = poi['bdxml']
#         return  Result
#
#     Result = '' + '<Graph>'+'\n'
#     Result = Result + '</Graph>'
#
#     xml = mBGHash[poi['bg']]
#     if xml == '' :
#
#         xml = '<?xml version="1.0" encoding="gb2312"?>'+'\n'
#         xml = xml + '<Graph Name="BG::RECT">'+'\n'
#         xml = xml + '<PlaneXY X="0" Y="0" L="L" W="W" Type="Polygon" Repeat="0">'+'\n'
#         xml = xml + '<Point X="0" Y="0" Hotspot="1" />'+'\n'
#         xml = xml + '<Point X="0" Y="W" Hotspot="1" />'+'\n'
#         xml = xml + '<Point X="L" Y="W" Hotspot="1" />'+'\n'
#         xml = xml + '<Point X="L" Y="0" Hotspot="1" />'+'\n'
#         xml = xml + '</PlaneXY>'+'\n'
#         xml = xml + '<PlaneXZ X="0" Y="0" L="L" W="W" Type="Rect" Repeat="0"/>'+'\n'
#         xml = xml + '<PlaneYZ X="0" Y="0" L="L" W="W" Type="Rect" Repeat="0"/>'+'\n'
#         xml = xml + '</Graph>'+'\n'
#         Result= program.GetMyProcAddress(xml, poi['gl'], poi['gp'], poi['gh'], poi['direct'], poi['var_args'][0], 16)
#     return Result
def SaveBDA(p, ab, mHPInfoList,mKCInfoList):
    Result = ''
    str1 = ''
    tl,tw = 0,0
    x0, y0, x1, y1 = 0, 0, 0, 0
    di = p.direct
    if di == 0: di = 1
    #A面孔
    for i in range(0,101):
        if (p.ahole_index[i] >= 0) and (p.ahole_index[i] < len(mHPInfoList)):
            hpinfo = mHPInfoList[p.ahole_index[i]]
            if hpinfo.r=='-1' : continue #// 过滤掉直径为-1的孔
            face = hpinfo.face
            hdirect = ''
            if (di in [4, 6]) : # // 侧板
                tl = hpinfo.x + hpinfo.xx
                tw = hpinfo.y + hpinfo.yy
                if (face == 'Up') or (face == 'Down'):
                    if tw == hpinfo.hd :
                        hdirect = 'D'
                    else:
                        hdirect = 'U'
                if (face == 'Front') or (face == 'Back') :
                    if tl == hpinfo.hd :
                        hdirect= 'L'
                    else:
                        hdirect= 'R'
            if (di in [2, 3]):  # // 背板
                tl = hpinfo.x + hpinfo.xx
                tw = hpinfo.y + hpinfo.yy
                if (face == 'Up') or (face == 'Down'):
                    if tw == hpinfo.hd:
                        hdirect = 'D'
                    else:
                        hdirect = 'U'
                if (face == 'Left') or (face == 'Right'):
                    if tl == hpinfo.hd:
                        hdirect = 'L'
                    else:
                        hdirect = 'R'
            if (di in [1, 5]):  # // 层板
                tl = hpinfo.x + hpinfo.xx
                tw = hpinfo.y + hpinfo.yy
                face = OppositeFace(hpinfo.face)
                if (face == 'Left') or (face == 'Right'):
                    if tl == hpinfo.hd:
                        hdirect = 'L'
                    else:
                        hdirect = 'R'
                if (face == 'Front') or (face == 'Back'):
                    if tw == hpinfo.hd:
                        hdirect = 'D'
                    else:
                        hdirect = 'U'
            if hpinfo.htype == 'L' :
                if hpinfo.r != '' :
                    print(type(tl), type(tw), type(hpinfo.r), type(hpinfo.sr), type(hdirect), type(ab), type(hpinfo.smallcap), type(hpinfo.sri))
                    str1= str1 +'\n'+ '<BHole X="%.2f" Y="%.2f" R="%s" Rb="%s" HDirect="%s" Face="%s" Hole_Z="%d" X1="%s"/>'%(
                        tl, tw, hpinfo.r, hpinfo.sr, hdirect, ab, hpinfo.smallcap, hpinfo.sri)+'\n'
            if (hpinfo.htype == 'I') or (hpinfo.htype == 'I+I') :
                if hpinfo.r != '' :
                    str1= str1 +'\n'+ '<VHole X="%.2f" Y="%.2f" R="%s" Rb="%s" HDirect="%s" Face="%s" Hole_Z="%d"/>'%(
                        tl, tw, hpinfo.r, hpinfo.sr, hdirect, ab, hpinfo.smallcap)+'\n'
    # A面开槽
    for i in range(0,101):
        if (p.akc_index[i] >= 0) and (p.akc_index[i] < len(mKCInfoList)) :
            KCInfo = mKCInfoList[p.akc_index[i]]
            s = p.kcconig_flag
            if KCInfo.flag != '' :  s =KCInfo.flag
            if (di in [4, 6]) or (di in [2, 3]) : #// 侧板 or 背板
                x0 = KCInfo.y0
                y0 = KCInfo.x0
                x1 = KCInfo.y1
                y1 = KCInfo.x1
            if (di in [1, 5]) : #// 层板
                x0 = KCInfo.x0
                y0 = KCInfo.y0
                x1 = KCInfo.x1
                y1 = KCInfo.y1
            str1 = str1 +'\n'+'<Cut X="%d" Y="%d" X1="%d" Y1="%d" Face="%s" CutName="%s" Cutter="%s" Hole_Z="%d" device="%d"/>'%(
                x0, y0, x1, y1, ab, s, KCInfo.cutter, KCInfo.w, KCInfo.device)+'\n'
    Result= str1
    return Result
def SaveBDB(p, ab, mHPInfoList,mKCInfoList):
    Result = ''
    x0, y0, x1, y1 = 0,0,0,0
    str1 = ''
    di = p.direct
    if di == 0: di = 1
    tl,tw = 0,0
    #B面孔
    for i in range(0,101):
        if (p.bhole_index[i] >= 0) and (p.bhole_index[i] < len(mHPInfoList)):
            hpinfo = mHPInfoList[p.bhole_index[i]]
            if hpinfo.r=='-1' : continue #// 过滤掉直径为-1的孔
            face = hpinfo.face
            hdirect = ''
            if (di in [4, 6]) : # // 侧板
                tl = hpinfo.x + hpinfo.xx
                tw = hpinfo.y + hpinfo.yy
                if (face == 'Up') or (face == 'Down'):
                    if tw == hpinfo.hd :
                        hdirect = 'D'
                    else:
                        hdirect = 'U'
                if (face == 'Front') or (face == 'Back') :
                    if tl == hpinfo.hd :
                        hdirect= 'L'
                    else:
                        hdirect= 'R'
            if (di in [2, 3]):  # // 背板
                tl = hpinfo.x + hpinfo.xx
                tw = hpinfo.y + hpinfo.yy
                if (face == 'Up') or (face == 'Down'):
                    if tw == hpinfo.hd:
                        hdirect = 'D'
                    else:
                        hdirect = 'U'
                if (face == 'Left') or (face == 'Right'):
                    if tl == hpinfo.hd:
                        hdirect = 'L'
                    else:
                        hdirect = 'R'
            if (di in [1, 5]):  # // 层板
                tl = hpinfo.x + hpinfo.xx
                tw = hpinfo.y + hpinfo.yy
                face = OppositeFace(hpinfo.face)
                if (face == 'Left') or (face == 'Right'):
                    if tl == hpinfo.hd:
                        hdirect = 'L'
                    else:
                        hdirect = 'R'
                if (face == 'Front') or (face == 'Back'):
                    if tw == hpinfo.hd:
                        hdirect = 'D'
                    else:
                        hdirect = 'U'
            if hpinfo.htype == 'L' :
                if hpinfo.r != '' :
                    str1= str1 +'\n'+ '<BHole X="%.2f" Y="%.2f" R="%s" Rb="%s" HDirect="%s" Face="%s" Hole_Z="%d" X1="%s"/>'%(tl, tw, hpinfo.r, hpinfo.sr, hdirect, ab, hpinfo.smallcap, hpinfo.sri)+'\n'
            if (hpinfo.htype == 'I') or (hpinfo.htype == 'I+I') :
                if hpinfo.r != '' :
                    str1= str1 +'\n'+ '<VHole X="%.2f" Y="%.2f" R="%s" Rb="%s" HDirect="%s" Face="%s" Hole_Z="%d"/>'%(tl, tw, hpinfo.r, hpinfo.sr, hdirect, ab, hpinfo.smallcap)+'\n'
    # B面开槽
    for i in range(0,101):
        if (p.bkc_index[i] >= 0) and (p.bkc_index[i] < len(mKCInfoList)) :
            KCInfo = mKCInfoList[p.bkc_index[i]]
            s = p.kcconig_flag
            if KCInfo.flag != '' :  s =KCInfo.flag
            if (di in [4, 6]) or (di in [2, 3]) : #// 侧板 or 背板
                x0 = KCInfo.y0
                y0 = KCInfo.x0
                x1 = KCInfo.y1
                y1 = KCInfo.x1
            if (di in [1, 5]) : #// 层板
                x0 = KCInfo.x0
                y0 = KCInfo.y0
                x1 = KCInfo.x1
                y1 = KCInfo.y1
            str1 = str1 +'\n'+'<Cut X="%d" Y="%d" X1="%d" Y1="%d" Face="%s" CutName="%s" Cutter="%s" Hole_Z="%d" device="%d"/>'%(x0, y0, x1, y1, ab, s, KCInfo.cutter, KCInfo.w, KCInfo.device)+'\n'
    Result= str1
    return Result
def X2dToBdGraph(poi, gBGHash):
    if poi.bdxml!='' :
        Result = poi.bdxml
        return  Result
    Result = '' + '<Graph>'+'\n'
    Result = Result + '</Graph>'
    if poi.bg =='BG::RECT':
        poi.bg = 'BG_RECT'
    # print poi.bg.encode('gbk')
    # if gBGHash not in dir():
    #
    #print json.dumps(gBGHash.keys(), ensure_ascii=False)
    if poi.bg.encode('gb2312') not in gBGHash:
        xml =''
    else:
        xml = gBGHash[poi.bg.encode('gb2312')]
    if xml == '' :
        xml = '<?xml version="1.0" encoding="gb2312"?>'+'\n'
        xml = xml + '<Graph Name="BG::RECT">'+'\n'
        xml = xml + '<PlaneXY X="0" Y="0" L="L" W="W" Type="Polygon" Repeat="0">'+'\n'
        xml = xml + '<Point X="0" Y="0" Hotspot="1" />'+'\n'
        xml = xml + '<Point X="0" Y="W" Hotspot="1" />'+'\n'
        xml = xml + '<Point X="L" Y="W" Hotspot="1" />'+'\n'
        xml = xml + '<Point X="L" Y="0" Hotspot="1" />'+'\n'
        xml = xml + '</PlaneXY>'+'\n'
        xml = xml + '<PlaneXZ X="0" Y="0" L="L" W="W" Type="Rect" Repeat="0"/>'+'\n'
        xml = xml + '<PlaneYZ X="0" Y="0" L="L" W="W" Type="Rect" Repeat="0"/>'+'\n'
        xml = xml + '</Graph>'+'\n'
    p = windll.LoadLibrary((base_dir.decode('gbk') + '\\' + 'QdCNC.dll.XYZ.20161220').encode('gbk'))
    p.InitDll(0, 0)
    xml = xml.replace('utf-8','gb2312').decode('utf8').encode('gbk')
    # if not os.path.exists(base_dir + '\\testdata\\X2dToBdGraph\\'):
    #     os.makedirs(base_dir + '\\testdata\\X2dToBdGraph\\')
    # with open(base_dir + '\\testdata\\X2dToBdGraph\\' + 'isoutput' + str(X2dToBdGraphj) + '.txt', 'w') as f:
    #     var_args = ''
    #     for i in range(16):
    #         var_args =var_args + str(poi.var_args[i])
    #     f.write('j='+str(X2dToBdGraphj)+'\n'+'xml='+xml+'\n'+'gl='+str(poi.gl)+'\n'+
    #             'gp='+str(poi.gp)+'\n'+'gh='+str(poi.gh)+'\n'+'direct='+
    #             str(poi.direct)+'\n'+'var_args='+var_args+'\n')
    xml= p.X2dToBdGraph(c_char_p(xml), c_int(poi.gl), c_int(poi.gp), c_int(poi.gh), c_int(poi.direct), id(poi.var_args[0]), 16)
    Result = c_char_p(xml).value.decode('gbk').encode('utf8')
    return Result
def SaveBD(poi,gBGHash,mHPInfoList, mKCInfoList, l, p, h, is_savehead):
    def SetLPH(ll, pp, hh, gl, gp, gh):
        ll = gl
        pp = gp
        hh = gh
        return ll, pp, hh
    Result = ''
    s = ''
    print('func=','SaveBD')
    for i in range(0,16):
        s = s + ' C%s="%d"'%(chr(65 + i), poi.var_args[i])
    print('s=',s)
    cncback = 0 #; // 比亚斯、豪迈打孔设备靠档
    cncback1 = 0 #; // 雕刻机设备靠档
    l, p, h = SetLPH(l, p, h, poi.l, poi.p, poi.h)
    if (poi.direct in [0, 1, 5]) :   #// 层板
        l, p, h = SetLPH(l, p, h, poi.gl, poi.gp, poi.gh)
        #// 前后封边，左右封边
        cncback = 0  #// 默认：后封边对应下靠档
        if poi.zero_y == 4 : cncback = 1  #// 前封边对应上靠档
        if poi.zero_y == 1 : cncback = 2 #// 左封边对应左靠档
        if poi.zero_y == 2 : cncback =3 # // 右封边对应右靠档
        if poi.direct in [0, 1] : cncback1 = 0# // 横纹层板，默认后封边靠档
        if poi.direct in [5] :  cncback1 = 2 # // 竖纹层板，默认左封边靠档
    if (poi.direct in [2, 3]) : #// 背板
        p, l, h = SetLPH(p, l, h, poi.gh, poi.gl, poi.gp)
        cncback = 2 #// 上下封边，左右封边
        cncback = 2 # // 默认：左封边对应左靠档
        if poi.zero_y == 5 : cncback = 0# // 下封边对应下靠档
        if poi.zero_y == 6 : cncback = 1# // 上封边对应上靠档
        if poi.zero_y == 2 : cncback = 3# // 右封边对应右靠档
        if poi.direct in [2] : cncback1 = 0# // 横纹背板，默认下封边靠档
        if poi.direct in [3] : cncback1 = 2# // 竖纹背板，默认左封边靠档
    if (poi.direct in [4, 6]) : #// 侧板
        p, l, h =SetLPH(p, l, h, poi.gh, poi.gp, poi.gl)
        #// 前后封边，左右封边
        cncback = 2  #// 默认：后封边对应左靠档
        if poi.zero_y == 4 : cncback = 3 #// 前封边对应右靠档
        if poi.zero_y == 5 : cncback = 0#// 下封边对应下靠档
        if poi.zero_y == 6 : cncback = 1#// 上封边对应上靠档
        if poi.direct in [4] : cncback1 = 2#// 竖纹侧板，默认后封边靠档
        if poi.direct in [6] : cncback1 = 0 # // 横纹侧板，默认下封边靠档
    xml = ''
    if is_savehead : xml ='<?xml version="1.0" encoding="gb2312"?>'+'\n'
    xml = xml + '\n'+'<Board L="%d" W="%d" BH="%d" CncBack="%d" CncBack1="%d"%s FB="%.2f" LFB="%.2f" RFB="%.2f" DFB="%.2f" UFB="%.2f" YHFB="%.2f" DevCode="%s" DI="%d" %s>'%(
        l, p, h, cncback, cncback1, s, poi.fb, poi.llfb, poi.rrfb, poi.ddfb, poi.uufb, 0.0, poi.devcode, poi.direct,
        poi.bdinfo)+'\n'
    xml = xml + X2dToBdGraph(poi,gBGHash)
    if (poi.direct in [2, 3]) : #// 背板
        xml= xml + '<FaceA>'  + '\n' + SaveBDB(poi, 'A', mHPInfoList,mKCInfoList) + '</FaceA>'+ '\n'
        xml= xml + '<FaceB>'  + '\n'+ SaveBDA(poi, 'B', mHPInfoList,mKCInfoList) + '</FaceB>'+ '\n'
    else:
        xml = xml + '<FaceA>'  + '\n'+ SaveBDA(poi, 'A', mHPInfoList,mKCInfoList) + '</FaceA>'+ '\n'
        xml = xml + '<FaceB>'  + '\n'+ SaveBDB(poi, 'B', mHPInfoList,mKCInfoList) + '</FaceB>'+ '\n'
    xml = xml + '</Board>'
    Result = xml
    return Result
def BDXML_BDXML(xml,xml2):
    isauto_acut = 0
    isauto_bcut = 0
    # 分析xml
    print('hahahGetDeviceOutputString1=',xml.decode('utf8'))
    root = ET.fromstring(xml)
    for i in range(0,len(root)):
        if root[i].tag == 'FaceA':
            nodeA = root[i]
            for j in range(len(nodeA)-1,-1,-1):
                cnode = nodeA[j]
                if cnode.tag == 'VHole' or cnode.tag == 'Cut':
                    attri = cnode.get('NotAuto')
                    if cnode.tag == 'Cut' and attri == '1':
                        isauto_acut = 1 #有自动开槽
                    if not (attri == '1') :
                        nodeA.remove(cnode)
        if root[i].tag == 'FaceB':
            nodeB = root[i]
            for j in range(len(nodeB)-1,-1,-1):
                cnode = nodeB[j]
                if cnode.tag == 'VHole' or cnode.tag == 'Cut':
                    attri = cnode.get('NotAuto')
                    if cnode.tag == 'Cut' and attri == '1':
                        isauto_bcut = 1  # 有自动开槽
                    if not (attri == '1'):
                        nodeB.remove(cnode)
    #print '123', xml2
    xml2 = xml2.encode('utf8').replace('gb2312','utf-8')
    root2 = ET.fromstring(xml2)
    #分析xml2
    for i in range(0,len(root2)):
        if root2[i].tag == 'FaceA':
            nodeA2 = root2[i]
            for j in range(0,len(nodeA2)):
                cnode2 = nodeA2[j]
                if cnode2.tag == 'VHole' or cnode2.tag == 'Cut':
                    attri = cnode2.get('NotAuto')
                    if isauto_acut == 1 and cnode2.tag == 'Cut' and attri == '1':
                        continue
                    nodeA.append(cnode2)
        if root2[i].tag == 'FaceB':
            nodeB2 = root2[i]
            for j in range(0, len(nodeB2)):
                cnode2 = nodeB2[j]
                if cnode2.tag == 'VHole' or cnode2.tag == 'Cut':
                    attri = cnode2.get('NotAuto')
                    if isauto_bcut == 1 and cnode2.tag == 'Cut' and attri == '1':
                        continue
                    nodeB.append(cnode2)
    xml = ET.tostring(root)
    print('hahahGetDeviceOutputString2=', '222222')
    return xml
def GetZeroY(p):
    #//默认，左封边，右封边，后封边，前封边，下封边，上封边
    Result = 0
    if ((p['direct'] == 1) or (p['direct'] == 5)) and (p['zero_y'] == 4) : Result = 1 #//横板-层板类
    if ((p['direct'] == 2) or (p['direct'] == 3)) and (p['zero_y'] == 2) : Result = 1 #//竖横板-背板类
    if ((p['direct'] == 4) or (p['direct'] == 6)) and (p['zero_y'] == 4) : Result = 1 #//侧板类
    return Result
def Swap(a, b):
    t = a
    a = b
    b = t
    return a, b
def SwapThree(a, b, c):
    t = a
    a = b
    b = c
    c = t
    return a ,b, c
def YougeHead(l, p, h, ischangexy):
    global gl,gd,gh
    is_changexy = ischangexy
    if is_changexy : l,p = Swap(l, p)
    gl = l
    gd = p
    gh = h
    Result = ''
    return Result
def YougeHoleVert(x, y, di, face, flag, offset):
    global gl, gd, gh
    if is_changexy : Swap(x, y)
    
    if face=='A' : Result = '(%d,%d,%s,%d),'%(y, round(gl-x), flag, offset)
    else:
        Result = '(%d,%d,%s,%d),'%(y, x, flag, offset)
    return Result
def YougeHoleVert2(x, y, di, face, flag, offset):
    global gl, gd, gh
    if is_changexy : x, y = Swap(x, y)
    
    if face=='A' : Result = '(%d,%d,%s,%d),'%(y, round(gl-x), flag, offset)
    else:
        Result = '(%d,%d,%s,%d),'%(y, x, flag, offset)
    return Result
def YougeHoleHoriz2(x, y, z, hd, di, ab, face, flag):
    Result = ''
    return Result
def YougeGCut(x0, y0, x1, y1, di, face, flag, cutter):
    Result = ''
    return Result
def YougeComment(s):
    Result = ''
    return Result
def YougeDevCode(devcode, c1, c2):
    Result = ''
    return Result
def FormatBarCode(jo, ordername, gno, gcb, index):
    Result = ''
    ja = jo['args']
    n = len(ja)
    print('n=',n,'ja=',json.dumps(ja),'jo=',json.dumps(jo))
    a=[0]*3
    for i in range(0,n):
        if ja[i]=='OrderName' :
            a[i]= ordername
        elif ja[i]=='Gno' :
            a[i] = gno
        elif ja[i] =='Gcb' :
            a[i]= gcb
        elif ja[i]=='Index' :
            a[i] = index
    s = jo['format']
    s1 = s.find('%')
    if s1>=0:
        stext = s[s1+1:]
        s2 = stext.find('%')
        if s2>=0:
            stext = stext[s2 + 1:]
            s3 = stext.find('%')
            if s3>=0:
                Result = s % (str(a[0]), str(a[1]), a[2])
            else:
                Result = s % (str(a[0]), a[1])
    # if s =="'%s-%s-%.3dA'" or s =="'%s-%s-%.3dB'" or s =="'%s-%s-%.3d'" or s =="'A%s-%s-%.3d'" or s =="'B%s-%s-%.3d'" \
    #         or s =="'%s-%s-%.3d'":
    #     #print '66666666666'
    #     Result = s%(str(a[0]),str(a[1]),a[2])
    # elif s == "'%s%.3d'":
    #     #print '77777777777'
    #     Result = s % (str(a[0]), a[1])
    # else:
    #     Result = s % (str(a[0]), str(a[1]), a[2])
    print('Result=',Result)
    return Result[1:len(Result)-1]
def ToBarCode(cjo,code):
    cjo['IsCode'] = 0
    if code=='' : return
    isformat = 0
    code = code.replace(' ', '', )
    ws = code.replace(';', '', )
    n1 = ws.find('Format(')
    n2= ws.find(',')
    if (n1 >= 0) and (n2 > n1) :
        isformat= 1
        cjo['format'] = ws[ n1 + 7: n2]
    if isformat==0 : return
    n1 = ws.find('[')
    n2 = ws.find(']')
    if (n1 >= 0) and (n2 > n1) :
        cjo['IsCode'] = isformat
        cjo['args'] = ws[n1+1: n2].split(",")
    return cjo
def GetHoleFaceInfo(p,mHPInfoList):
    Result = 0
    for i in range(0,101):                 #//A面有孔
        if (p['ahole_index'][i] >= 0) and (p['ahole_index'][i] < len(mHPInfoList)) :
            hpinfo = mHPInfoList[p['ahole_index'][i]]
            if hpinfo.r!='-1' :
                Result = 1
                break
    for i in range(0, 101):
        if (p['bhole_index'][i] >= 0) and (p['bhole_index'][i] < len(mHPInfoList)) :
            hpinfo = mHPInfoList[p['bhole_index'][i]]
            if hpinfo.r!='-1' :
                if Result == 0 : Result = 2
                if Result == 1 : Result = 3
                break
    return Result
def GetKCFaceInfo(p, mKCInfoList):
    Result = 0
    for i in range(0, 101):              #//A面有槽
        if (p['akc_index'][i] >= 0) and (p['akc_index'][i] < len(mKCInfoList)) :
            Result = 1
            break
    for i in range(0, 101):                  #//B面有槽
        if (p['bkc_index'][i] >= 0) and (p['bkc_index'][i] < len(mKCInfoList)) :
            if Result == 0 : Result = 2
            if Result == 1 : Result = 0   #//3
            break
    return Result
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
def SortBomItemBySeq(Item1,Item2):
    p1 = Item1
    p2 = Item2
    Result = 0
    N1 = int(p1['classseq'])
    n2 = int(p2['classseq'])
    if N1 <= 0 :
        N1 = 100000
    if n2 <= 0 :
        n2= 100000
    if N1 > n2 :
        Result= 1
    if N1 < n2 :
        Result= -1
    if Result != 0 : return Result
    N1= int(p1['seq'])
    n2= int(p2['seq'])
    if N1 <= 0 :
        N1= 100000
    if n2 <= 0 :
        n2= 100000
    if N1 > n2 :
        Result = 1
    if N1 < n2 :
        Result = -1
    if Result == 0 :
        if int(p1['l']) > int(p2['l']) :
            Result = -1
        if int(p1['l']) < int(p2['l']) :
            Result = 1
        if Result == 0 :
            if int(p1['p']) > int(p2['p']) :
                Result = -1
            if int(p1['p']) < int(p2['p']) :
                Result = 1
            if Result == 0:
                if int(p1['x']) > int(p2['x']):
                    Result = -1
                if int(p1['x']) < int(p2['x']):
                    Result = 1
                if Result == 0:
                    if int(p1['y']) > int(p2['y']):
                        Result = -1
                    if int(p1['y']) < int(p2['y']):
                        Result = 1
                    if Result == 0:
                        if int(p1['z']) > int(p2['z']):
                            Result = -1
                        if int(p1['z']) < int(p2['z']):
                            Result = 1
                        if Result == 0:
                            if int(p1['num']) > int(p2['num']):
                                Result = -1
                            if int(p1['num']) < int(p2['num']):
                                Result = 1
                            if Result == 0:
                                try:
                                    if p1['gno'] > p2['gno']:
                                        Result = -1
                                    if p1['gno'] < p2['gno']:
                                        Result = 1
                                    if Result == 0:
                                        if p1['name'] > p2['name']:
                                            Result = -1
                                        if p1['name'] < p2['name']:
                                            Result = 1
                                        if Result == 0:
                                            if p1['var_args'][0] > p2['var_args'][0]:
                                                Result = -1
                                            if p1['var_args'][0] < p2['var_args'][0]:
                                                Result = 1
                                            if Result == 0:
                                                if p1['color'] > p2['color']:
                                                    Result = -1
                                                if p1['color'] < p2['color']:
                                                    Result = 1
                                                if Result == 0:
                                                    if p1['mat'] > p2['mat']:
                                                        Result = -1
                                                    if p1['mat'] < p2['mat']:
                                                        Result = 1
                                except:
                                    pass
    return Result
def zip_files(files, zip_name):
    zip = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_STORED)
    for file in files:
        print(('compressing', file))
        print(os.path.basename(file))  # basename///dirname
        if not os.path.exists(file): continue
        filefullpath = os.path.join(file)
        zip.write(filefullpath, os.path.basename(file))
    zip.close()
    print ('compressing finished')
def zip_ya(startdir, file_new):
    file_news = startdir + '.zip'  # 压缩后文件夹的名字
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''  # 实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
    z.close()
def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)
#os.makedirs(u"D:\\Python+设计软件运行环境\\电子单\\mOrderNamedxPopupGNOText\\")
#
#print 'AB'.lower()# Filename : test.py
# author by : www.runoob.com
#print ChangeFileExt('123.ord','.zip')
def MyVariant(str1,s1,s2):
    s1 = ''
    s2 = ''
    ws = str1
    n = ws.find(':')
    s1 = ws[0: n]
    s2 = ws[n+1:]
    return s1,s2
def Delphi_Round(num):
    if isinstance(num, str):
        if num =='':
            num = 0
        num = float(num)
    if num < 0:
        return -(Delphi_Round(-num))
    round10 = num * 10
    round1 = round(num)
    if (round10 - round1 * 10 == -5):
        pint = int(num)
        pvalue = pint % 10  #; // 个位的数值
        if (pvalue % 2): return (pint+1)   #// 奇进偶不进
        else: return pint
    else:
        return round1
def Delphi_not(num):
    return -num-1
def dealpoint(num):
    if num ==int(num):
        return int(num)
    else:
        return num
def funcid(newpoi):
    return id(newpoi)
'''
ZFile 用于文件解压缩，压缩
'''
class ZFile(object):
    def __init__(self, filename, mode='r', basedir=''):
        self.filename = filename
        self.mode = mode
        if self.mode in ('w', 'a'):
            self.zfile = zipfile.ZipFile(filename, self.mode, compression=zipfile.ZIP_DEFLATED)
        else:
            self.zfile = zipfile.ZipFile(filename, self.mode)
        self.basedir = basedir
        if not self.basedir:
            self.basedir = os.path.dirname(filename)
    def addfile(self, path, arcname=None):
        path = path.replace('//', '/')
        if not arcname:
            if path.startswith(self.basedir):
                arcname = path[len(self.basedir):]
            else:
                arcname = ''
        self.zfile.write(path, arcname)
    def addfiles(self, paths):
        for path in paths:
            if isinstance(path, tuple):
                self.addfile(*path)
            else:
                self.addfile(path)
    def close(self):
        self.zfile.close()
    def extract_to(self, path):
        for p in self.zfile.namelist():
            self.extract(p, path)
    def extract(self, filename, path):
        if not filename.endswith('/'):
            f = os.path.join(path, filename)
            dir = os.path.dirname(f)
            if not os.path.exists(dir):
                os.makedirs(dir)
            file(f, 'wb').write(self.zfile.read(filename))
#zip解压缩到指定目录
def extractZip(zfile, path):
    z = ZFile(zfile)
    z.extract_to(path)
    z.close()
def FBStr2Value(string, l, w, llfb, rrfb, ddfb, uufb, ffb, fb):
    wstr = string
    n = wstr.find(',')
    if n >= 0 :
        s = wstr[0:n]
        l  = float(s)
        wstr = wstr[n+1:]
    n = wstr.find(',')
    if n >= 0:
        s = wstr[0:n]
        w = float(s)
        wstr = wstr[n + 1:]
    n = wstr.find(',')
    if n >= 0:
        s = wstr[0:n]
        llfb = float(s)
        wstr = wstr[n + 1:]
    n = wstr.find(',')
    if n >= 0:
        s = wstr[0:n]
        rrfb = float(s)
        wstr = wstr[n + 1:]
    n = wstr.find(',')
    if n >= 0 :
        s = wstr[0:n]
        ddfb = float(s)
        wstr = wstr[n + 1:]
    n = wstr.find(',')
    if n >= 0:
        s = wstr[0:n]
        uufb = float(s)
        wstr = wstr[n + 1:]
    n = wstr.find(',')
    if n >= 0:
        s = wstr[0:n]
        ffb = float(s)
        wstr = wstr[n + 1:]
    fb = wstr
    return l, w, llfb, rrfb, ddfb, uufb, ffb, fb
#20190716 AB面转换
def TransAB_NoChange(p):
    p['trans_ab'] = False
    str1 = p['a_hole_info']
    p['a_hole_info'] = p['b_hole_info']
    p['b_hole_info'] = str1
    for i in range(0,101):
        t = p['ahole_index'][i]
        p['ahole_index'][i] = p['bhole_index'][i]
        p['bhole_index'][i] = t
        t1 = p['akc_index'][i]
        p['akc_index'][i] = p['bkc_index'][i]
        p['bkc_index'][i] = t1
#20190717
def GetHingeHole(psb, mDoorList):
    Result = ''
    string = ''
    for i in range(0, len(mDoorList)):
        DoorItem = mDoorList[i]
        if DoorItem['slino']==psb['slino'] :
          string = DoorItem['hingehole']
          break
    if string=='' : return Result
    n  = string.find(':')
    s1 = string[0: n]
    i = 0
    s1 = string[n+1: len(string)]
    n = s1.find(';')
    while n > 0:
        s2 = s1[0: n]
        N1 = s2.find(';')
        s3 = s2[0: N1]
        j = int(s3)
        s2 = s2[N1+1: len(s2)]
        N1 = s2.find(',')
        s3 = s2[0: N1]
        k = int(s3)
        s2 = s2[N1+1: len(s2)]
        N1 = s2.find(',')
        s3 = s2[0: N1]
        v1 = int(s3)
        s2 = s2[N1 + 1: len(s2)]
        N1 = s2.find(',')
        s3 = s2[0: N1]
        v2 = int(s3)
        s2 = s2[N1 + 1: len(s2)]
        N1 = s2.find(',')
        s3 = s2[0: N1]
        v3 = int(s3)
        s3 = s2[N1 + 1: len(s2)]
        v4 = int(s3)
        if (j==psb['door_index']-1) :
            if v4 in [0, 1] :
                Result = str(v2) + ','
            if v4 in [2, 3] :
                Result = str(v1) + ','
        s1  = s1[n+1:len(s1)]
        n  = s1.find(';')
        i = i+1
    return Result
def GetDoorMemo(psb, mDoorList):
    Result = ''
    string = ''
    for i in range(0, len(mDoorList)):
        DoorItem = mDoorList[i]
        if DoorItem['slino']==psb['slino'] :
            string = DoorItem['doormemo']
            break
    if string=='' : return Result
    n = string.find(':')
    s1 = string[0:n]
    i = 0
    s1 = string[n+1:len(string)]
    n = s1.find(';')
    while n > 0 :
        s2 = s1[0:n]
        if (i==psb['door_index']-1) :
            Result = s2
        s1 = s1[n+1:len(s1)]
        n = s1.find(';')
        i = i+1
    return Result
def GetDoorExtra(psb, mDoorList):
    Result = ''
    for i in range(0, len(mDoorList)):
        DoorItem = mDoorList[i]
        if DoorItem['slino']==psb['slino'] :
            Result = DoorItem['doorextra']
            break
    return Result
def pnumber(num):
    if int(num)==float(num): return int(num)
    else: return float(num)
def IsSamePSBItem(psb, psb2, mDoorList):
    Result  = False
    if (psb['slino'] == psb2['slino']) and (psb['name'] == psb2['name']) and (psb['mat'] == psb2['mat']) and (psb['color'] == psb2['color']) \
    and (psb['l'] == psb2['l']) and (psb['p'] == psb2['p']) and (psb['h'] == psb2['h']) and (psb['direct'] == psb2['direct'])\
    and (psb['memo'] == psb2['memo']) and (psb['memo2'] == psb2['memo2']) and (psb['memo3'] == psb2['memo3'])\
    and (psb['subspace'] == psb2['subspace']) and (psb['fbstr'] == psb2['fbstr']) and (psb['doormemo'] == psb2['doormemo']) \
    and (psb['mark'] == psb2['mark']) :
        Result = True
    if (Result) and (psb['door_index'] > 0) :
        if GetHingeHole(psb, mDoorList)!=GetHingeHole(psb2, mDoorList) : Result = False
        if GetDoorMemo(psb, mDoorList)!=GetDoorMemo(psb2, mDoorList) : Result = False
    return Result
def IsSameOrderItem(poi,poi2,gROC,mHPInfoList, CBIgnoreHoleInfoChecked=True):
    gQDBomFlag = 1
    Result = False
    # if poi['name'] == u'垫块' and poi2['name'] == u'垫块':
    #     print 'mark1=',poi['mark'],'mark2=',poi2['mark']
    #     print poi['bl'],poi['bp'],poi['bh']
    #     print poi2['bl'],poi2['bp'],poi2['bh']
    if poi['mark'] != poi2['mark'] :
        # if poi['name'] == u'垫块' and poi2['name'] == u'垫块':
        #     print type(poi['mark'])
        #     print type(poi2['mark'])
        #     exit(1)
        return Result
    samepluginitem = True
    flag = gQDBomFlag
    if poi['nodename'] == '五金' : flag = 0
    if poi['nodename'] == '型材五金' : flag = 0
    # if poi['name'] == u'垫块' and poi2['name'] == u'垫块' and poi['bl'] == 58 and poi['bp'] == 58 and poi['bh'] == 18:
    #     print 'flag=',flag
    if flag == 0 :
        # print u'验证俩者是否相同第一步'
        # print '2l=', poi2['l'], '1l=', poi['l']
        # if poi2['l'] == poi['l']:
        #
        #     print u'l 相同'
        # if poi2['name'] == poi['name']:
        #     print u'name 相同'
        # print '2p=', poi2['p'], '1p=', poi['p']
        # if poi2['p'] == poi['p']:
        #     print u'p 相同'
        #
        # if poi2['h'] == poi['h']:
        #     print u'h 相同'
        # if poi2['mat'] == poi['mat']:
        #     print u'mat 相同'
        # if poi2['color'] == poi['color']:
        #     print u'color 相同'
        # if poi2['desc'] == poi['desc']:
        #     print u'desc 相同'
        # if poi2['direct'] == poi['direct']:
        #     print u'direct 相同'
        # if poi2['process'] == poi['process']:
        #     print u'process 相同'
        # if poi2['subspace'] == poi['subspace']:
        #     print u'subspace 相同'
        # print 'IsSameHoleInfo=', IsSameHoleInfo(poi, poi2, mHPInfoList)
        # if IsSameHoleInfo(poi, poi2, mHPInfoList):
        #     print u'HoleInfo 相同'
        if (poi2['l'] == poi['l']) and (poi2['name'] == poi['name']) \
            and (poi2['p'] == poi['p']) and (poi2['h'] == poi['h'])  \
            and (poi2['mat'] == poi['mat']) and (poi2['color'] == poi['color'])    \
            and (poi2['desc'] == poi['desc']) and (poi2['direct'] == poi['direct']) \
            and (poi2['process'] == poi['process']) and IsSameHoleInfo(poi, poi2, mHPInfoList, CBIgnoreHoleInfoChecked)\
            and (poi2['subspace'] == poi['subspace']):
            Result = True
        for i in range(0,16):
            if poi['var_args'][i] != poi2['var_args'][i] :
                Result = False
    else:
        if ((not gROC.wl_out_classname) or (poi2['desc'] == poi['desc'])) and (poi2['name'] == poi['name'])  \
            and ((not gROC.wl_out_myclass) or (poi2['myclass'] == poi['myclass']))    \
            and ((not gROC.wl_out_classname) or (poi2['desc'] == poi['desc']))    \
            and ((not gROC.wl_out_mat) or (poi2['mat'] == poi['mat']))    \
            and ((not gROC.wl_out_color) or (poi2['color'] == poi['color']))    \
            and ((not gROC.wl_out_size) or ((poi2['l'] == poi['l']) and (poi2['p'] == poi['p']) and (poi2['h'] == poi['h'])    \
            and (Delphi_Round(poi2['bl']) == Delphi_Round(poi['bl'])) and (Delphi_Round(poi2['bp']) == Delphi_Round(poi['bp']))     \
            and (Delphi_Round(poi2['bh']) == Delphi_Round(poi['bh']))))    \
            and ((not gROC.wl_out_kc) or ((poi2['kcstr'] == poi['kcstr']) and (IsSameKcInfo(poi, poi2))))    \
            and ((not gROC.wl_out_fb) or (poi2['fbstr'] == poi['fbstr']))    \
            and ((not gROC.wl_out_memo) or (poi2['memo'] == poi['memo']))    \
            and ((not gROC.wl_out_hole) or (IsSameHoleInfo(poi, poi2, mHPInfoList)))    \
            and (poi2['bdxmlid'] == poi['bdxmlid'])    \
            and (poi2['group'] == poi['group'])    \
            and (poi2['subspace'] == poi['subspace']) and (samepluginitem):
            Result = True
        # if poi['name']==u'垫块' and poi2['name']==u'垫块' and poi['bl'] ==58 and poi['bp'] ==58 and poi['bh'] ==18:
        #     print 'Result=',Result
        #     print 'Result=', Result
        #     print poi['var_args']
        #     print poi2['var_args']
        for i in range(0, 16):
            if poi['var_args'][i] != poi2['var_args'][i]: Result = False
    return Result
def IsSameHoleInfo(poi1, poi2, mHPInfoList, CBIgnoreHoleInfoChecked):
    def IsSameHolePointInfo(phinfo1, phinfo2):
        Result = False
        if (phinfo1.x == phinfo2.x) and (phinfo1.y == phinfo2.y) and (phinfo1.r == phinfo2.r) and (phinfo1.sr== phinfo2.sr):
            Result = True
            return Result
        return Result
    Result = True
    #默认忽略打孔信息
    if CBIgnoreHoleInfoChecked:
        return Result
    if (poi2['a_hole_info'] != poi1['a_hole_info']) or (poi2['b_hole_info'] != poi1['b_hole_info']) :
        # print '1a_hole_info ' + 'and '+'b_hole_info '+' is not equal'
        # print 'poi2=',poi2['a_hole_info'],poi2['b_hole_info']
        # print 'poi1=',poi1['a_hole_info'],poi1['b_hole_info']
        Result = False
    for i in range(0,101):
        if poi1['ahole_index'][i] >= 0 :
            phinfo1 = mHPInfoList[poi1['ahole_index'][i]]
            find = False
            for j in range(0, 101):
                if poi2['ahole_index'][j] >= 0 :
                    phinfo2 = mHPInfoList[poi2['ahole_index'][j]]
                    if IsSameHolePointInfo(phinfo1, phinfo2):
                        find= True
                        break
            if not find:
                # print '2ahole_index ' + 'and ' + 'ahole_index ' + ' is not equal'
                Result = False
                return Result
        if poi1['bhole_index'][i] >= 0 :
            phinfo1 = mHPInfoList[poi1['bhole_index'][i]]
            find = False
            for j in range(0,101):
                if poi2['bhole_index'][j] >= 0 :
                    phinfo2 = mHPInfoList[poi2['bhole_index'][j]]
                    if IsSameHolePointInfo(phinfo1, phinfo2) :
                        find = True
                        break
            if not find :
                Result = False
                # print '3ahole_index ' + 'and ' + 'ahole_index ' + ' is not equal'
                return Result
    return Result
def IsSameKcInfo(poi1, poi2):
    Result = True
    if poi2['kcconig_flag'] != poi1['kcconig_flag']:
        Result = False
    return Result
def UpdateBomList(bomlist, basewjlist,slidinglist,doorslist, gROC, mHPInfoList, mDoorList, CBIgnoreHoleInfoChecked, dxPopupGNOText):
    #global allBomList,bjBomList,wjBomList,xcwjBomList,allBomList2,bjBomList2,wjBomList2,xcwjBomList2
    allBomList = []
    bjBomList = []  # 装饰类别-板材列表
    wjBomList = []  # 装饰类别-五金
    xcwjBomList = []
    allBomList2 = []
    bjBomList2 = []
    wjBomList2 = []
    xcwjBomList2 = []
    slBomList = []    #趟门
    slBomList2 = []
    dlBomList = []    #掩门
    dlBomList2 = []
    Data = {}
    for i in range(0,len(bomlist)):
        p = bomlist[i]
        if not p['isoutput'] : continue
        if dxPopupGNOText !='所有' :
            if dxPopupGNOText != p['gno'] : continue
        if p['nodename'] == '五金' :
            wjBomList.append(p)
        elif p['nodename'] == '型材五金' :
            xcwjBomList.append(p)
        else:
            bjBomList.append(p)
        allBomList.append(p)
    for i in range(0,len(basewjlist)):
        p = basewjlist[i]
        if dxPopupGNOText !='所有' :
            if dxPopupGNOText != p['gno'] : continue
        #print 'color=', p['color'], 'mat=', p['mat']
        wjBomList.append(p)
        allBomList.append(p)
    for i in range(0,len(allBomList)):
        poi = allBomList[i]
        find = False
        for j in range(0,len(allBomList2)):
            poi2 = allBomList2[j]
            # if poi['name'] == u'垫块': #and poi2['name'] == poi['name'] and poi['bl']==poi2['bl'] and poi['bp']== poi2['bp'] and poi['bh'] == poi2['bh']:
            #     print '6666666'
            #     print 'i=',i,'j=',j,
            #     print poi['gno']
                #exit(1)
            if IsSameOrderItem(poi, poi2, gROC, mHPInfoList, CBIgnoreHoleInfoChecked):
                find = True
                poi2['num'] = int(poi2['num']) + int(poi['num'])
                poi2['id'] = poi['id']
                break
        if find : continue
        poi2 = {}
        for key ,value in list(poi.items()):
            poi2[key] = value
        if poi['nodename'] == '五金':
            wjBomList2.append(poi2)
        elif poi['nodename'] == '型材五金' :
            xcwjBomList2.append(poi2)
        else:
            bjBomList2.append(poi2)
        allBomList2.append(poi2)
    #趟门物料
    for i in range(0, len(slidinglist)):
        psb = slidinglist[i]
        if dxPopupGNOText !='所有' :
            if dxPopupGNOText != psb['gno'] : continue
        slBomList.append(psb)
    for i in range(0, len(slBomList)):
        psb = slBomList[i]
        find = False
        for j in range(0, len(slBomList2)):
            psb2 = slBomList2[j]
            if IsSamePSBItem(psb, psb2, mDoorList) :
                find = True
                psb2['num'] = int(psb2['num']) + int(psb['num'])
                break
        if find : continue
        psb2 = {}
        psb2['blockmemo'] = ''
        psb2['number_text'] = ''
        psb2 = copy.deepcopy(psb)
        slBomList2.append(psb2)
    #掩门物料
    for i in range(0, len(doorslist)):
        psb = doorslist[i]
        if dxPopupGNOText !='所有' :
            if dxPopupGNOText != psb['gno'] : continue
        dlBomList.append(psb)
    for i in range(0, len(dlBomList)):
        psb = dlBomList[i]
        find = False
        for j in range(0, len(dlBomList2)):
            psb2 = dlBomList2[j]
            if IsSamePSBItem(psb, psb2, mDoorList) :
                find = True
                psb2['num'] = int(psb2['num']) + int(psb['num'])
                break
        if find : continue
        psb2 = {}
        psb2['blockmemo'] = ''
        psb2['number_text'] = ''
        psb2 = copy.deepcopy(psb)
        dlBomList2.append(psb2)
    #Data['Order'] =orderdict
    Data['bjBomList'] = bjBomList
    Data['basewjlist'] = wjBomList
    Data['xcwjBomList'] = xcwjBomList
    bjBomList.sort(SortBomItemBySeq)
    bjBomList2.sort(SortBomItemBySeq)
    wjBomList.sort(SortBomItemBySeq)
    wjBomList2.sort(SortBomItemBySeq)
    xcwjBomList.sort(SortBomItemBySeq)
    xcwjBomList2.sort(SortBomItemBySeq)
    allBomList.sort(SortBomItemBySeq)
    allBomList2.sort(SortBomItemBySeq)
    return allBomList,bjBomList,wjBomList,xcwjBomList,slBomList,dlBomList, allBomList2,bjBomList2,wjBomList2,xcwjBomList2,slBomList2,dlBomList2,Data
#20190730
def newpslibom():
    pslibom = {}
    pslibom['cid'] = 0
    pslibom['id'] = 0
    pslibom['pid'] = 0
    pslibom['seq'] = 0
    pslibom['num'] = 0
    pslibom['mark'] = 0
    pslibom['doornum'] = 0
    pslibom['slino'] = 0
    pslibom['xmlindex'] = 0
    pslibom['isglass'] = 0
    pslibom['is_buy'] = 0
    pslibom['door_index'] = 0
    pslibom['space_id'] = 0
    pslibom['name'] = ''
    pslibom['l'] = 0
    pslibom['p'] = 0
    pslibom['h'] = 0
    pslibom['sliw'] = 0
    pslibom['slih'] = 0
    pslibom['doorw'] = 0
    pslibom['doorh'] = 0
    pslibom['code'] = ''
    pslibom['mat'] = ''
    pslibom['mat2'] = ''
    pslibom['mat3'] = ''
    pslibom['color'] = ''
    pslibom['direct'] = ''
    pslibom['gno'] = ''
    pslibom['gdes'] = ''
    pslibom['gcb'] = ''
    pslibom['extra'] = ''
    pslibom['group'] = ''
    pslibom['bomtype'] = ''
    pslibom['memo'] = ''
    pslibom['memo2'] = ''
    pslibom['memo3'] = ''
    pslibom['subspace'] = ''
    pslibom['fbstr'] = ''
    pslibom['doorname'] = ''
    pslibom['myunit'] = ''
    pslibom['dtype'] = ''
    pslibom['bdfile'] = ''
    pslibom['bdxmlid'] = ''
    pslibom['doormemo'] = ''
    pslibom['extend'] = ''
    pslibom['erpunit'] = ''
    pslibom['erpmatcode'] = ''
    pslibom['blockmemo'] = ''
    pslibom['number_text'] = ''
    return pslibom
def writeexcell(ParValue,jsoncontent):
    if not isinstance(jsoncontent, str):
        jsoncontent = str(jsoncontent)
    if isinstance(jsoncontent, str):
        ParValue[0].value = jsoncontent.encode('gbk')
    else:
        try:
            ParValue[0].value = jsoncontent.decode('utf8').encode('gbk')
        except:
            ParValue[0].value = jsoncontent
    #     j = 0
    #     for i in (jsoncontent.encode('cp936')):  # 'cp936'
    #         ParValue[0][j] = i
    #         j = j + 1
    # else:
    #     try:
    #         j = 0
    #         for i in (jsoncontent.decode('utf8').encode('cp936')):#'cp936'
    #             ParValue[0][j] = i
    #             j = j + 1
    #     except:
    #         j = 0
    #         import chardet
    #         print chardet.detect(jsoncontent)
    #         try:
    #             print 'jsoncontent=',jsoncontent.decode('utf8')
    #         except:
    #             pass
    #         try:
    #             for i in (jsoncontent.decode('gbk').encode('cp936')):  # 'cp936'
    #                 ParValue[0][j] = i
    #                 j= j + 1
    #         except:
    #             j = 0
    #             ParValue[0] = jsoncontent.decode('utf8').encode('gbk')
                # for i in (jsoncontent.decode('utf8').encode('cp936')):  # 'cp936'
                #     ParValue[0][j] = i
                #     j = j + 1
def ParName2NameAndText(parname,partext,flag, mytype, dotnum):
    partext = ''
    flag = 0  #;// 0前置，1后置
    mytype = 0 #// 0字符串，1四舍五入数值，2阶段数值
    dotnum = 0 #; // 小数位数
    wstr = parname
    m = wstr.find('$')
    n = wstr.find('"')
    if n > 0 :
        flag= 2
        if m >= n :
            flag=1
            wstr= wstr[n:]
            n = wstr.find('"')
            if n > 0 :
                partext = wstr[0: n]
                str1 = '"%s"'% partext
                parname = parname.replace( str1, '')
    wstr = parname
    n = wstr.find(':')
    if n > 0 :
        parname = wstr[0:n] + ']'
        str1 = wstr[n+1:]
        if len(str1)==3 :
            p = str1
            if p[0]=='N' : mytype = 1
            if p[0]=='T' : mytype =2
            dotnum = int(p[1])
    return parname, partext, flag, mytype, dotnum
def getLocalTime(DephiTime):
    ts = (DephiTime-25569) * 86400.0
    #print ts
    timeArray = time.localtime(ts)  # 秒数
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)#%H:%M:%S
    #print(otherStyleTime)
    return otherStyleTime
def Noround(anum, x):
    xx = int("1" + "0" * x)
    bnum = int(float(str(anum * xx))) / xx
    return (bnum)
def delphi_format(num, x):
    x = x + 1
    xx = int("1" + "0" * x)
    count = int(float(str(num * xx)))
    while (count > 10):
        count = count % 10
    if count >= 5:
        result = Noround(num, 4) + 0.0001
    else:
        result = Noround(num, 4)
    return result
# 20190801
def AutoBomFormatSingle(t):
    if int(t) == float(t):
        return str(int(t))
    else:
        if gFormatPrecision == 1:
            Result = '%.4f'%(delphi_format(t,4))
        if gFormatPrecision == 1:
            Result = '%.3f' % (delphi_format(t, 3))
        if gFormatPrecision == 1:
            Result = '%.2f'%(delphi_format(t,2))
        if gFormatPrecision == 1:
            Result = '%.1f'%(delphi_format(t,1))
        else:
            Result = str(Delphi_Round(t))
        if int(float(Result)) == float(Result):
            return str(int(float(Result)))
        return Result
# 20190802
def code(content):
	if isinstance(content, str):
		#s=u"中文"
		cotent=content.encode('gb2312')
		return content
	else:
		#s="中文"
		try:
			content=content.decode('utf-8').encode('gb2312')
			return content
		except:
			return content
def FormatSingle(*argv):
    if len(argv) ==3:
        t, dotnum, isround = argv[0], argv[1], argv[2]
        result = ''
        if dotnum==0 :
            if isround : result = '%d'%( Delphi_Round(t))
            else: result = '%d'%(int(t))
        elif dotnum>0 :
            if isround :
                string = '%%.%df'%(dotnum)
                result = string%(t)
            else:
                string = '%%.%df'%(dotnum+1)
                result =  string%(t)
                result = result[:len(result)-1]
        return result
    if len(argv) ==2:
        fmt, t = argv[0], argv[1]
        Result = 0
        s = Delphi_Round(t) - t
        if abs(s) < 0.001:
            Result = ('%d'%(Delphi_Round(t)))
        else:
            #print 'round=',delphi_format(t,4)
            Result = (fmt)%(delphi_format(t,4))
        return Result
#20191014
def WriteStringToFile(filename, xml):
    with open(filename, 'w+') as f:
        f.write(xml)
if __name__ == '__main__':
    pass