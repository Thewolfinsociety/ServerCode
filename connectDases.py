# -*- coding: UTF-8 -*-
# @Time : 2019/11/26 13:10
# @Author : litao
# @File : connectDases.py.py 增加孔位五金
'''
更新至Python3

'''
import os
import json
import tornado.escape
import tornado.ioloop
from tornado.options import define, options, parse_command_line
from tornado.web import RequestHandler
import zipfile
import json
import pypyodbc
import sys
import os
import configparser
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
import redis
import json

#最新20191230
from tornado.concurrent import Future

pool = redis.ConnectionPool(host='127.0.0.1',port=6379)    #'129.204.134.85'
r = redis.Redis(connection_pool=pool)


define("port", default=8002, help="run on the given port", type=int)
base_dir = os.path.abspath(os.path.join(os.getcwd(),'..'))

dataDBPath = base_dir + '\\nginx-1.0.11\\nginx-1.0.11\\html\\ServerData\\'


def returntaskresdata(recemessage):
    task_id = ('celery-task-meta-' + recemessage)
    try:
        status = True
        content = r.get(task_id)
        result = json.loads(content).get("result")
    except Exception as e:
        status = False
        result = ''
        content = ''
        print(e)

    return status, result

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

def connectdata(dataDBfile):
    conn = pypyodbc.win_connect_mdb('DRIVER={Microsoft Access Driver (*.mdb)};DBQ=' + dataDBfile)
    cur = conn.cursor()
    return conn, cur

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
            # if typelist[j] ==u'封边留空1':
            #     print '66666666666666',ufetchall[i][j]
            #     if isinstance(fjo[typelist[j]], unicode):
            #         print '9999999'
    return fjo

def Nonetonumber(value, type = 'I'):
    result = 0
    if value=="":
        return result
    if type =='F':
        result = float(value)
        return result
    if float(result) == int(float(value)):
        result = int(float(value))
    else:
        result = float(value)
    return result

def OneBomData2Json(PathName ,des, gQDBomFlag):
    Result = {'result':0,'des2wuliao':[],'ruleHash':[],'childbomHash':[],'wjruleHash':[],'linecalcList':[],
              'holeconfigHash':[],'kcconfigHash':[],'bomstdList':[]}
    dataDBfile = dataDBPath + PathName + '\\data\\data.mdb'

    if (not os.path.exists(dataDBfile)):
        logger.error('数据库不存在!!!')
        return Result
    else:
        conn, cur = connectdata(dataDBfile)
        n = des.find(',')
        s1 = des[:n]
        s2 = des[n+1:]
        sql = "select myclass2.*, myclass1.name as pname from myclass1, myclass2 where myclass2.myclass1=myclass1.id and myclass1.name='%s' and myclass2.name='%s'" % (
            s1, s2)
        cur.execute(sql)
        jo = {}
        ja = []
        fjo = {}
        des2wuliaoallu = cur.fetchall()
        if des2wuliaoallu ==[]:
            return Result
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
                # cjo = {}
                # key = s1+','+s2
                # cjo['key'] = key
                # str = u[0][7]+','+u[0][8]
                # cjo['s1'] = key
                # cjo['s2'] = str
                # cjo['s3'] = u[0][9] +','+ u[0][10]
                # cjo['direct'] = 0
                # cjo['no'] = u[0][13]  # 输出编号
                # cjo['oname'] = u[0][12]  # 输出名称
                # cjo['childbom'] = u[0][11]  # 物料分解
                # cjo['priceclass'] = u[0][3]  # type
                #
                # if gQDBomFlag == 0:
                #     cjo['bomclass'] = u[0][3]
                # else:
                #     cjo['bomclass'] = u[0][4]  # bomclass
                # cjo['linecalc'] = u[0][16]  # 线性物体计算
                # cjo['HoleConfig'] = u[0][17]  # 孔位配置
                # cjo['bomstd'] = u[0][18]  # 尺寸判定
                # cjo['bomtype'] = u[0][19]  # 物料分类
                # cjo['KCConfig'] = u[0][20]  # 开槽配置
                # cjo['bg_filename'] = u[0][23] # bg_filename
                # cjo['bpp_filename'] = u[0][25]
                # cjo['devcode'] = u[0][35]
                # cjo['zero_y'] = u[0][36]
                # cjo['is_output_bgdata'] = u[0][26]
                # cjo['is_output_mpr'] = u[0][27]
                # cjo['is_output_bpp'] = u[0][28]
                # cjo['direct_calctype'] = u[0][37]
                # cjo['youge_holecalc'] = u[0][38]
                # cjo['workflow'] = u[0][39]
                #
                # fjo[u'封边留空1'] = u[0][7]
                # fjo[u'封边留空2'] = u[0][8]
                # fjo[u'物料分解'] = u[0][11]
                # fjo[u'五金清单1'] = u[0][9]
                # fjo[u'五金清单2'] = u[0][10]
                # fjo[u'线性物体计算'] = u[0][16]
                # fjo[u'孔位配置'] = u[0][17]
                # fjo[u'开槽配置'] = u[0][20]
                # fjo['pname'] = u[0][1]
                # fjo['name'] = u[0][2]
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
                #print json.dumps(holeconfig_dict,ensure_ascii=False)
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
                cjo['dmax'] = Nonetonumber(bomstd_rule_dict['pmax'])
                cjo['dmin'] = Nonetonumber(bomstd_rule_dict['pmin'])
                cjo['hmax'] = Nonetonumber(bomstd_rule_dict['hmax'])
                cjo['hmin'] = Nonetonumber(bomstd_rule_dict['hmin'])
                cjo['stdflag'] = bomstd_rule_dict['stdflag']
                cjo['level'] = Nonetonumber(bomstd_rule_dict['level'])
                ja.append(cjo)
        jo['bomstdList'] = ja
        jo['result'] = 1
        # finally:
        #     conn.close()
        # json.dumps(jo,ensure_ascii=False).encode('utf8')
        return jo
def testOneBomData2Json(PathName, des):
    Result = {'result':0}
    ResultJsonStr = json.dumps(Result, ensure_ascii=False).encode('utf8')
    dataDBfile = dataDBPath + PathName + '\\data\\data.mdb'
    if des == '' or (not os.path.exists(dataDBfile)):
        return ResultJsonStr
    else:
        conn, cur = connectdata(dataDBfile)
        n = des.find(',')
        print('n=',n)
        s1 = des[:n]
        s2 = des[n+1:]
        print('s1= ',s1,'s2=',s2)
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
            print(json.dumps(typelist, ensure_ascii=False))
            print('len of typelist=',len(typelist),'len of des2wuliaoallu[0]=',len(des2wuliaoallu[0]))
            print('pname=',des2wuliaoallu[0][40])
            for i in range(0, len(des2wuliaoallu)):
                fjo = getfjo(i, typelist, des2wuliaoallu)
                print(json.dumps(fjo,ensure_ascii=False))
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
                # cjo = {}
                # key = s1+','+s2
                # cjo['key'] = key
                # str = u[0][7]+','+u[0][8]
                # cjo['s1'] = key
                # cjo['s2'] = str
                # cjo['s3'] = u[0][9] +','+ u[0][10]
                # cjo['direct'] = 0
                # cjo['no'] = u[0][13]  # 输出编号
                # cjo['oname'] = u[0][12]  # 输出名称
                # cjo['childbom'] = u[0][11]  # 物料分解
                # cjo['priceclass'] = u[0][3]  # type
                #
                # if gQDBomFlag == 0:
                #     cjo['bomclass'] = u[0][3]
                # else:
                #     cjo['bomclass'] = u[0][4]  # bomclass
                # cjo['linecalc'] = u[0][16]  # 线性物体计算
                # cjo['HoleConfig'] = u[0][17]  # 孔位配置
                # cjo['bomstd'] = u[0][18]  # 尺寸判定
                # cjo['bomtype'] = u[0][19]  # 物料分类
                # cjo['KCConfig'] = u[0][20]  # 开槽配置
                # cjo['bg_filename'] = u[0][23] # bg_filename
                # cjo['bpp_filename'] = u[0][25]
                # cjo['devcode'] = u[0][35]
                # cjo['zero_y'] = u[0][36]
                # cjo['is_output_bgdata'] = u[0][26]
                # cjo['is_output_mpr'] = u[0][27]
                # cjo['is_output_bpp'] = u[0][28]
                # cjo['direct_calctype'] = u[0][37]
                # cjo['youge_holecalc'] = u[0][38]
                # cjo['workflow'] = u[0][39]
                #
                # fjo[u'封边留空1'] = u[0][7]
                # fjo[u'封边留空2'] = u[0][8]
                # fjo[u'物料分解'] = u[0][11]
                # fjo[u'五金清单1'] = u[0][9]
                # fjo[u'五金清单2'] = u[0][10]
                # fjo[u'线性物体计算'] = u[0][16]
                # fjo[u'孔位配置'] = u[0][17]
                # fjo[u'开槽配置'] = u[0][20]
                # fjo['pname'] = u[0][1]
                # fjo['name'] = u[0][2]
                ja.append(cjo)
        jo['des2wuliao'] = ja
        print(json.dumps(jo,ensure_ascii=False))
        #封边留空  bom_rule
        ja = []
        print(fjo['封边留空1'],fjo['封边留空2'])
        import chardet
        print(chardet.detect(fjo['封边留空1']),chardet.detect(fjo['封边留空2']))
        sql = ("select * from bom_rule where deleted=False and 物料类别1='%s' and 物料类别2='%s' order by 物料类别1 asc, 物料类别2 asc, 材料 asc " % (
            fjo['封边留空1'], fjo['封边留空2']))
        cur.execute(sql)
        ruleHashuf = cur.fetchall()
        if ruleHashuf != []:
            typelist = []
            ruleHash_dict = {}
            for tup in cur.description:
                typelist.append(tup[0])  # 编码gbk
            print('len of typelist=', len(typelist))
            for i in range(0, len(ruleHashuf)):
                ruleHash_dict = getfjo(i, typelist, ruleHashuf)
                print('len of ruleHash_dict=', len(ruleHash_dict), json.dumps(ruleHash_dict,ensure_ascii=False))
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
        jo['ruleHash'] = ja
        print(json.dumps(jo, ensure_ascii=False))
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
            print('len of typelist=',len(typelist))
            for i in range(0, len(wuliao_listuf)):
                wuliao_dict = getfjo(i, typelist, wuliao_listuf)
                print('len of wuliao_dict=',len(wuliao_dict),json.dumps(wuliao_dict,ensure_ascii=False))
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
            print('len of typelist=', len(typelist))
            for i in range(0, len(wujin_listuf)):
                wujin_dict = getfjo(i, typelist, wujin_listuf)
                print('len of wujin_dict=', len(wujin_dict), json.dumps(wujin_dict, ensure_ascii=False))
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
            print('len of typelist=', len(typelist))
            for i in range(0, len(linecal_listuf)):
                linecal_dict = getfjo(i, typelist, linecal_listuf)
                print('len of linecal_dict=', len(linecal_dict), json.dumps(linecal_dict, ensure_ascii=False))
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
            print('len of typelist=', len(typelist))
            for i in range(0, len(holeconfig_listuf)):
                holeconfig_dict = getfjo(i, typelist, holeconfig_listuf)
                print('len of holeconfig_dict=', len(holeconfig_dict))
                #print json.dumps(holeconfig_dict,ensure_ascii=False)
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
            print('len of typelist=', len(typelist))
            for i in range(0, len(kcconfig_listuf)):
                kcconfig_dict = getfjo(i, typelist, kcconfig_listuf)
                print('len of kcconfig_dict=', len(kcconfig_dict), json.dumps(kcconfig_dict,
                                                                               ensure_ascii=False))
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
            print('len of typelist=', len(typelist))
            for i in range(0, len(bomstd_rule_listuf)):
                bomstd_rule_dict = getfjo(i, typelist, bomstd_rule_listuf)
                print('len of bomstd_rule_dict=', len(bomstd_rule_dict), json.dumps(bomstd_rule_dict,
                                                                              ensure_ascii=False))
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
        return jo

def getseqinfo(PathName):
    Result = {'result': 0}
    jo = {}
    ja = []
    ResultJsonStr = json.dumps(Result, ensure_ascii=False).encode('utf8')
    dataDBfile = dataDBPath + PathName + '\\data\\data.mdb'
    if (not os.path.exists(dataDBfile)):
        return ja
    conn, cur = connectdata(dataDBfile)
    sql = "select bomname,bomseq from base_seqinfo"
    cur.execute(sql)

    seqinfoallu = cur.fetchall()
    try:
        if seqinfoallu == []:
            return ja
        else:
            typelist = []
            for tup in cur.description:
                typelist.append(tup[0])  # 编码gbk
            for i in range(0, len(seqinfoallu)):
                fjo = getfjo(i, typelist, seqinfoallu)
                cjo = {}
                if fjo['bomname'] == '': continue
                cjo['bomname'] = fjo['bomname']
                cjo['bomseq'] = Nonetonumber(fjo['bomseq'])
                ja.append(cjo)
        jo = {'seqinfo':ja}
        jo['result'] = 1
    finally:
        conn.close()
    return ja
def getclassseqinfo(PathName):
    Result = {'result': 0}
    jo = {}
    ja = []
    ResultJsonStr = json.dumps(Result, ensure_ascii=False).encode('utf8')
    dataDBfile = dataDBPath + PathName + '\\data\\data.mdb'

    if (not os.path.exists(dataDBfile)):
        return ja
    conn, cur = connectdata(dataDBfile)
    sql = "select * from base_classseqinfo where ID>1000 order by seq asc"
    cur.execute(sql)

    classseqinfoallu = cur.fetchall()
    try:
        if classseqinfoallu == []:
            return ja
        else:
            typelist = []
            for tup in cur.description:
                typelist.append(tup[0])  # 编码gbk
            for i in range(0, len(classseqinfoallu)):
                fjo = getfjo(i, typelist, classseqinfoallu)
                cjo = {}
                cjo['name'] = fjo['name']
                cjo['seq'] = Nonetonumber(fjo['seq'])
                ja.append(cjo)
        jo = {'classseqinfo': ja}
        jo['result'] = 1
    finally:
        conn.close()
    return ja
def getreportsconfig(PathName):
    Result = {'result': 0}
    ResultJsonStr = json.dumps(Result, ensure_ascii=False).encode('utf8')
    dataDBfile = dataDBPath + PathName + '\\data\\data.mdb'
    if (not os.path.exists(dataDBfile)):
        return ResultJsonStr
    conn, cur = connectdata(dataDBfile)
    sql = "select * from reports_config"
    cur.execute(sql)
    jo = {}
    ja = []
    reportsconfigallu = cur.fetchall()
    try:
        if reportsconfigallu == []:
            return ResultJsonStr
        else:
            typelist = []
            for tup in cur.description:
                typelist.append(tup[0])  # 编码gbk
            for i in range(0, len(reportsconfigallu)):
                fjo = getfjo(i, typelist, reportsconfigallu)
                cjo = {}
                cjo['bj_out_classname'] = fjo['bj_out_classname']
                cjo['bj_out_myclass'] = fjo['bj_out_myclass']
                cjo['bj_out_name'] = fjo['bj_out_name']
                cjo['bj_out_mat'] = fjo['bj_out_mat']
                cjo['bj_out_color'] = fjo['bj_out_color']
                cjo['bj_out_size'] = fjo['bj_out_size']
                cjo['bj_out_price'] = fjo['bj_out_price']
                cjo['wl_out_classname'] = fjo['wl_out_classname']
                cjo['wl_out_myclass'] = fjo['wl_out_myclass']
                cjo['wl_out_name'] = fjo['wl_out_name']
                cjo['wl_out_mat'] = fjo['wl_out_mat']
                cjo['wl_out_color'] = fjo['wl_out_color']
                cjo['wl_out_size'] = fjo['wl_out_size']
                cjo['wl_out_kc'] = fjo['wl_out_kc']
                cjo['wl_out_fb'] = fjo['wl_out_fb']
                cjo['wl_out_memo'] = fjo['wl_out_memo']
                cjo['wl_out_hole'] = fjo['wl_out_hole']
                ja.append(cjo)
        jo = {'reportsconfig': ja}
        jo['result'] = 1
    finally:
        conn.close()
    return ja
def getworkflow(PathName):
    Result = {'result': 0}
    jo = {}
    ja = []
    ResultJsonStr = json.dumps(Result, ensure_ascii=False).encode('utf8')
    dataDBfile = dataDBPath + PathName + '\\data\\data.mdb'
    if (not os.path.exists(dataDBfile)):
        return ja
    conn, cur = connectdata(dataDBfile)
    sql = "select * from base_workflow"
    cur.execute(sql)

    reportsconfigallu = cur.fetchall()
    try:
        if reportsconfigallu == []:
            return ja
        else:
            typelist = []
            for tup in cur.description:
                typelist.append(tup[0])  # 编码gbk
            for i in range(0, len(reportsconfigallu)):
                fjo = getfjo(i, typelist, reportsconfigallu)
                cjo = {}
                cjo['id'] = Nonetonumber(fjo['id'])
                cjo['name'] = fjo['name']
                cjo['bomstd'] = fjo['bomstd']
                cjo['hole'] = fjo['hole']
                cjo['board_cut'] = Nonetonumber(fjo['board_cut'])
                cjo['edge_banding'] = Nonetonumber(fjo['edge_banding'])
                cjo['punching'] = Nonetonumber(fjo['punching'])
                ja.append(cjo)
        jo = {'workflow': ja}
        jo['result'] = 1
    finally:
        conn.close()
    return ja
def getErpItem(PathName):
    Result = {'result': 0}
    jo = {}
    ja = []
    ResultJsonStr = json.dumps(Result, ensure_ascii=False).encode('utf8')
    ErpDBfile = dataDBPath + PathName + '\\Plugins\\erp.mdb'
    if (not os.path.exists(ErpDBfile)):
        return ja
    dbname = ErpDBfile
    if not os.path.exists(ErpDBfile):
        if not os.path.exists(dataDBPath + PathName + '\\snimay.mdb'):
            return ResultJsonStr
        dbname = dataDBPath + PathName + '\\snimay.mdb'
    conn, cur = connectdata(dbname)
    sql = "select * from mat order by id"
    cur.execute(sql)

    ErpItemallu = cur.fetchall()
    try:
        if ErpItemallu == []:
            return ja
        else:
            typelist = []
            for tup in cur.description:
                typelist.append(tup[0])  # 编码gbk
            for i in range(0, len(ErpItemallu)):
                fjo = getfjo(i, typelist, ErpItemallu)
                cjo = {}
                cjo['id'] = Nonetonumber(fjo['id'])
                cjo['name'] = fjo['name']
                cjo['mat'] = fjo['mat']
                cjo['color'] = fjo['color']
                cjo['h'] = Nonetonumber(fjo['h'])
                cjo['flag'] = fjo['flag']
                cjo['myclass'] = fjo['myclass']
                cjo['unit'] = fjo['unit']
                ja.append(cjo)
        jo = {'ErpItem': ja}
        jo['result'] = 1
    finally:
        conn.close()
    return ja
def getpricetable(PathName):
    Result = {'result': 0}
    ResultJsonStr = json.dumps(Result, ensure_ascii=False).encode('utf8')
    dataDBfile = dataDBPath + PathName + '\\data\\data.mdb'
    if (not os.path.exists(dataDBfile)):
        return ResultJsonStr
    conn, cur = connectdata(dataDBfile)
    sql = "select * from base_pricetable where deleted=False order by 材料"
    cur.execute(sql)
    jo = {}
    ja = []
    pricetableallu = cur.fetchall()
    try:
        if pricetableallu == []:
            return ResultJsonStr
        else:
            typelist = []
            for tup in cur.description:
                typelist.append(tup[0])  # 编码gbk
            for i in range(0, len(pricetableallu)):
                fjo = getfjo(i, typelist, pricetableallu)
                cjo = {}
                cjo['name'] = fjo['报价方案']
                cjo['mat'] = fjo['材料']
                cjo['price1'] = fjo['价格1']
                cjo['price2'] = fjo['价格2']
                cjo['bh'] = Nonetonumber(fjo['bh'])
                cjo['cost'] = fjo['加工费用']
                cjo['price_exp1'] = fjo['price_exp1']
                cjo['price_exp2'] = fjo['price_exp2']
                ja.append(cjo)
            jo = {'ptable': ja}
            jo['result'] = 1
    finally:
        conn.close()
    return jo
def OneQuoData2Json(PathName, des):
    Result = {'result': 0}
    ResultJsonStr = json.dumps(Result, ensure_ascii=False).encode('utf8')
    dataDBfile = dataDBPath + PathName + '\\data\\data.mdb'
    if (not os.path.exists(dataDBfile)):
        return ResultJsonStr
    if des == '':
        return ResultJsonStr
    else:
        conn, cur = connectdata(dataDBfile)
        try:
            n = des.find(',')
            s1 = des[:n]
            s2 = des[n + 1:]
            sql = ("select * from base_quotation_class where [报价类别1]='%s' and [报价类别2]='%s' and deleted=False" % (
                s1, s2))
            cur.execute(sql)
            jo = {}
            ja = []
            fjo = {}
            quotationclassallu = cur.fetchall()
            if quotationclassallu:
                typelist = []
                for tup in cur.description:
                    typelist.append(tup[0])  # 编码gbk
                for i in range(0, len(quotationclassallu)):
                    fjo = getfjo(i, typelist, quotationclassallu)
                    cjo = {}
                    key = s1 + ',' + s2
                    cjo['key'] = key
                    cjo['bj1'] = fjo['报价类别1']  # 报价类别1
                    cjo['bj2'] = fjo['报价类别2']  # 报价类别2
                    cjo['pricetype'] = fjo['报价方式']  # type
                    cjo['factor'] = Nonetonumber(fjo['价格系数'], 'F')
                    cjo['myunit'] = fjo['单位']  # 单位
                    cjo['myclass'] = fjo['分类']  # 分类
                    cjo['is_calc_cost'] = fjo['is_calc_cost']  # 物料分类
                    ja.append(cjo)
            jo['classHash'] = ja
            #
            ja = []
            sql = (
                        "select * from base_quotation_rule where [报价类别1]='%s' and [报价类别2]='%s' and deleted=False order by 报价类别1 asc, 报价类别2 asc, 是否非标 desc, [level] asc, 门板材料" % (
                    s1, s2))
            cur.execute(sql)
            quotationruleallu = cur.fetchall()
            if quotationruleallu != []:
                typelist = []
                quotationrule = {}
                for tup in cur.description:
                    typelist.append(tup[0])  # 编码gbk
                for i in range(0, len(quotationruleallu)):
                    quotationrule = getfjo(i, typelist, quotationruleallu)
                    key = quotationrule['报价类别1'] + ',' + quotationrule['报价类别2']
                    cjo = {}
                    cjo['key'] = key
                    cjo['bj1'] = quotationrule['报价类别1']  # 报价类别1
                    cjo['bj2'] = quotationrule['报价类别2']  # 报价类别2
                    cjo['l'] = Nonetonumber(quotationrule['l'])
                    cjo['lmax'] = Nonetonumber(quotationrule['lmax'])
                    cjo['lmin'] = Nonetonumber(quotationrule['lmin'])
                    cjo['p'] = Nonetonumber(quotationrule['p'])
                    cjo['pmax'] = Nonetonumber(quotationrule['pmax'])
                    cjo['pmin'] = Nonetonumber(quotationrule['pmin'])
                    cjo['h'] = Nonetonumber(quotationrule['h'])
                    cjo['hmax'] = Nonetonumber(quotationrule['hmax'])
                    cjo['hmin'] = Nonetonumber(quotationrule['hmin'])
                    cjo['slidingmat'] = quotationrule['门板材料']
                    cjo['isnonstandard'] = quotationrule['是否非标']
                    cjo['id'] = Nonetonumber(quotationrule['id'])
                    cjo['myclass'] = quotationrule['分类']
                    cjo['PriceTable'] = quotationrule['报价方案']
                    cjo['price1'] = quotationrule['价格1']
                    cjo['price2'] = quotationrule['价格2']
                    cjo['outname'] = quotationrule['outname']
                    cjo['sale_type'] = quotationrule['sale_type']
                    ja.append(cjo)
            jo['ruleHash'] = ja
            ja = []
            sql = (
                        "select myclass2.*, myclass1.name as pname from myclass1, myclass2 where myclass2.myclass1=myclass1.id and [报价类别1]='%s' and [报价类别2]='%s'" % (
                    s1, s2))
            cur.execute(sql)
            des2priceuf = cur.fetchall()
            if des2priceuf != []:
                typelist = []
                des2price_dict = {}
                for tup in cur.description:
                    typelist.append(tup[0])  # 编码gbk
                for i in range(0, len(des2priceuf)):
                    des2price_dict = getfjo(i, typelist, des2priceuf)
                    cjo = {}
                    key = des2price_dict['pname'] + ',' + des2price_dict['name']
                    string = des2price_dict['报价类别1'] + ',' + des2price_dict['报价类别2']
                    cjo['key'] = key
                    cjo['no'] = des2price_dict['输出编号']
                    cjo['name'] = des2price_dict['输出名称']
                    cjo['myclass'] = des2price_dict['type']
                    cjo['s1'] = key
                    cjo['s2'] = string
                    ja.append(cjo)
            jo['des2price'] = ja
            jo['result'] = 1
        finally:
            conn.close()
        return json.dumps(jo, ensure_ascii=False).encode('utf8')
def getboardmat(PathName):
    Result = {'result': 0}
    jo = {}
    ja = []
    ResultJsonStr = json.dumps(Result, ensure_ascii=False).encode('utf8')
    XScriptDBfile = dataDBPath + PathName + '\\data\\XScriptDb.mdb'
    if not os.path.exists(XScriptDBfile):
        return ja
    conn, cur = connectdata(XScriptDBfile)
    sql = "select * from base_boardmaterial_classify"
    cur.execute(sql)

    boardmatallu = cur.fetchall()
    try:
        if boardmatallu == []:
            return ja
        else:
            typelist = []
            for tup in cur.description:
                typelist.append(tup[0])  # 编码gbk
            for i in range(0, len(boardmatallu)):
                fjo = getfjo(i, typelist, boardmatallu)
                cjo = {}
                cjo['name'] = fjo['name']
                cjo['bh'] = Nonetonumber(fjo['bh'])
                cjo['alias'] = fjo['alias']
                cjo['alias2'] = fjo['alias2']
                cjo['alias3'] = fjo['alias3']
                cjo['color'] = fjo['color']
                ja.append(cjo)
            jo = {'boardmat': ja}
            jo['result'] = 1
    finally:
        conn.close()
    return ja
def getxmlbylink(PathName, link):
    Result = {'result': 0}
    ResultJsonStr = json.dumps(Result, ensure_ascii=False).encode('utf8')
    XScriptDBfile = dataDBPath + PathName + '\\data\\XScriptDb.mdb'
    if not os.path.exists(XScriptDBfile):
        return ResultJsonStr
    conn, cur = connectdata(XScriptDBfile)
    sql = ("select * from xml_template where [path]='%s' and deleted=0 order by id asc" % (link)).encode(
        'gbk')
    cur.execute(sql)
    jo = {}
    ja = []
    xmlbylinkallu = cur.fetchall()
    try:
        if xmlbylinkallu == []:
            return ResultJsonStr
        else:
            typelist = []
            for tup in cur.description:
                typelist.append(tup[0])  # 编码gbk
            for i in range(0, len(xmlbylinkallu)):
                fjo = getfjo(i, typelist, xmlbylinkallu)
                cjo = {}
                cjo['path'] = fjo['path']
                cjo['XML'] = fjo['xml']
                ja.append(cjo)
            jo = {'XMLByLink': ja}
            jo['result'] = 1
    finally:
        conn.close()
    return json.dumps(jo, ensure_ascii=False).encode('utf8')
class ExitSystem(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        print("***服务器退出***")
        os._exit(0)  # 退出程序

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
class Returnseqinfo(BaseHandler):
    def get(self, *args, **kwargs):
        PathName = self.get_argument('factorypath', None)
        PathName = PathName[0:3]
        try:
            ja = getseqinfo(PathName)
            result = {'seqinfo': ja,'result':1}
            ResultJson = json.dumps(result, ensure_ascii=False).encode('utf8')
        except:
            ResultJson = json.dumps({'result': 0}, ensure_ascii=False).encode('utf8')
        self.write(ResultJson)
class Returnclassseqinfo(BaseHandler):
    def get(self, *args, **kwargs):
        PathName = self.get_argument('factorypath', None)
        PathName = PathName[0:3]
        try:
            ja = getclassseqinfo(PathName)
            result = {'classseqinfo': ja, 'result': 1}
            ResultJson = json.dumps(result, ensure_ascii=False).encode('utf8')
        except:
            ResultJson = json.dumps({'result': 0}, ensure_ascii=False).encode('utf8')
        self.write(ResultJson)
class Returnreportsconfig(BaseHandler):
    def get(self, *args, **kwargs):
        PathName = self.get_argument('factorypath', None)
        PathName = PathName[0:3]
        try:
            ja = getreportsconfig(PathName)
            result = {'reportsconfig': ja, 'result': 1}
            ResultJson = json.dumps(result, ensure_ascii=False).encode('utf8')
        except:
            ResultJson = json.dumps({'result': 0}, ensure_ascii=False).encode('utf8')
        self.write(ResultJson)
class Returnworkflow(BaseHandler):
    def get(self, *args, **kwargs):
        PathName = self.get_argument('factorypath', None)
        PathName = PathName[0:3]
        try:
            ja = getworkflow(PathName)
            result = {'workflow': ja, 'result': 1}
            ResultJson = json.dumps(result, ensure_ascii=False).encode('utf8')
        except:
            ResultJson = json.dumps({'result': 0}, ensure_ascii=False).encode('utf8')
        self.write(ResultJson)
class ReturngErpItem(BaseHandler):
    def get(self, *args, **kwargs):
        PathName = self.get_argument('factorypath', None)
        PathName = PathName[0:3]
        try:
            ja = getErpItem(PathName)
            result = {'ErpItem': ja, 'result': 1}
            ResultJson = json.dumps(result, ensure_ascii=False).encode('utf8')
        except:
            ResultJson = json.dumps({'result': 0}, ensure_ascii=False).encode('utf8')
        self.write(ResultJson)
class ReturnBoardMat(BaseHandler):
    def get(self, *args, **kwargs):
        PathName = self.get_argument('factorypath', None)
        PathName = PathName[0:3]
        try:
            ja = getboardmat(PathName)
            result = {'boardmat': ja, 'result': 1}
            ResultJson = json.dumps(result, ensure_ascii=False).encode('utf8')
        except:
            ResultJson = json.dumps({'result': 0}, ensure_ascii=False).encode('utf8')
        self.write(ResultJson)
class Returngpricetable(BaseHandler):
    def get(self, *args, **kwargs):
        PathName = self.get_argument('factorypath', None)
        PathName = PathName[0:3]
        try:
            result = getpricetable(PathName)
            result['result'] = 1
            ResultJson = json.dumps(result, ensure_ascii=False).encode('utf8')
        except:
            ResultJson = json.dumps({'result': 0}, ensure_ascii=False).encode('utf8')
        self.write(ResultJson)

class Returndata(BaseHandler):
    def get(self, *args, **kwargs):
        print(self.get_argument('des', None))
        des = self.get_argument('des', None)
        PathName = self.get_argument('factorypath', None)
        PathName = PathName[0:3]
        gQDBomFlag = int(self.get_argument('gQDBomFlag', 1))
        print('des=',des,'PathName=',PathName,'gQDBomFlag=',gQDBomFlag)
        #try:
        result = OneBomData2Json(PathName ,des, gQDBomFlag)
        # except:
        resultJson = json.dumps(result, ensure_ascii=False).encode('utf8')
        self.write(resultJson)

class Returnquodata(BaseHandler):
    def get(self, *args, **kwargs):
        print(self.get_argument('des', None))
        des = self.get_argument('des', None)
        PathName = self.get_argument('factorypath', None)
        PathName = PathName[0:3]
        try:
            result = OneQuoData2Json(PathName, des)

        except:
            result = json.dumps({'result': 0}, ensure_ascii=False).encode('utf8')
        self.write(result)

class Returnxmlbylink(BaseHandler):
    def get(self, *args, **kwargs):
        link = self.get_argument('link', None)
        PathName = self.get_argument('factorypath', None)
        PathName = PathName[0:3]
        try:
            result = getxmlbylink(PathName, link)

        except:
            result = json.dumps({'result': 0}, ensure_ascii=False).encode('utf8')
        self.write(result)

class ReturnHoleWj(BaseHandler):
    def get(self, *args, **kwargs):
        PathName = self.get_argument('factorypath', 'mytest')
        PathName = PathName[0:3]
        HoleWjFile = dataDBPath + PathName + '\\data\\QDData\孔位五金.cfg'
        if (not os.path.exists(HoleWjFile)):
            result = json.dumps({'result': 0}, ensure_ascii=False).encode('utf8')
            self.write(result)
            return
        else:
            with open(HoleWjFile, 'r') as f:
                HoleWjFContent = f.read()
            result = json.dumps({'result': 1, 'HoleWjFContent': HoleWjFContent}, ensure_ascii=False).encode('utf8')
        self.write(result)

class ReturnNetQuo(BaseHandler):
    def get(self, *args, **kwargs):
        PathName = self.get_argument('factorypath', 'mytest')
        PathName = PathName[0:3]
        NetQuoFile = dataDBPath + PathName + '\\data\\QDData\\NetQuotation.cfg'
        if (not os.path.exists(NetQuoFile)):
            result = json.dumps({'result': 0}, ensure_ascii=False).encode('utf8')
            self.write(result)
            return
        else:
            with open(NetQuoFile, 'r') as f:
                NetQuoFContent = f.read()
            result = json.dumps({'result': 1, 'NetQuoFContent': NetQuoFContent}, ensure_ascii=False).encode('utf8')
        self.write(result)

class PostData(BaseHandler):
    def post(self, *args, **kwargs):
        factoryid = self.get_argument('factoryid', None)
        result = json.dumps({'result': 1})
        self.write(result)

# ========增加代码--开始========
def produce_stop_bat(pid, tmpfile="stop_xxx.bat"):
    # 待写入内容
    stop_cmd = 'taskkill /pid ' + str(pid) + ' /f'  # 关闭指定进程
    del_self_cmd = "del %0"  # 删除自身文件
    # 文件路径和名称
    tmp_all = os.path.join(os.path.dirname(os.path.realpath(__file__)), "stop_" + tmpfile + ".bat")
    # 写入文件
    with open(file=tmp_all, mode="w") as f:
        f.write(stop_cmd + "\n" + del_self_cmd)

def outputlog():
    main_log_handler = logging.FileHandler(log_path +
                                           "/ConnectDases_%s.log" % time.strftime("%Y-%m-%d_%H-%M-%S",
                                                                        time.localtime(time.time())), mode="w+",
                                           encoding="utf-8")
    main_log_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    main_log_handler.setFormatter(formatter)
    logger.addHandler(main_log_handler)

    # 控制台打印输出日志
    console = logging.StreamHandler()  # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象
    console.setLevel(logging.DEBUG)  # 设置要打印日志的等级，低于这一等级，不会打印
    formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    # 进程号
    pid = os.getpid()
    # 本文件名（不含后缀.py）
    myfilename = os.path.split(__file__)[-1].split(".")[0]
    # 生成关闭进程的脚本文件
    produce_stop_bat(pid, myfilename)

    # ========增加代码--结束========
class ReturnGlobalData(BaseHandler):
    def post(self, *args, **kwargs):
        PathName = self.get_argument('factorypath', None)
        PathName = PathName[0:3]
        version = r.get(PathName + 'Verison')
        if version:
            version = r.get(PathName + 'Verison')
            myversion = version.decode('utf8')
        else:
            r.set(PathName + 'Verison','0.01')
            myversion = '0.01'

        Result = {'result':1,'seqinfo':[],'classseqinfo':[],'workflow':[],'ErpItem':[],'boardmat':[],'HoleWjFContent':''}
        state, result = returnresdata(PathName +myversion+ 'allglobaldata')
        if state:
            resultjson = json.dumps(result, ensure_ascii=False).encode('utf8')
            self.write(resultjson)
            return
        try:
            # 1.seqinfo 数据表
            Result['seqinfo'] = getseqinfo(PathName)
            # 2.classseqinfo 数据表
            Result['classseqinfo'] = getclassseqinfo(PathName)
            #3.base_workflow 数据表
            Result['workflow'] = getworkflow(PathName)
            # 4.erp 数据表
            Result['ErpItem'] = getErpItem(PathName)
            # 5.boardmat 数据表
            Result['boardmat'] = getboardmat(PathName)
            # 6.孔位五金数据表

            HoleWjFile = dataDBPath + PathName + '\\data\\QDData\孔位五金.cfg'
            if (not os.path.exists(HoleWjFile)):
                HoleWjFContent = ''
            else:
                with open(HoleWjFile, 'r') as f:
                    HoleWjFContent = f.read()

            Result['HoleWjFContent'] = HoleWjFContent
        except:
            Result['result'] = 0
        resultjson = json.dumps(Result, ensure_ascii=False).encode('utf8')
        r.set(PathName +myversion+ 'allglobaldata', resultjson)
        self.write(resultjson)

class AllDesData(BaseHandler):
    # executor = ThreadPoolExecutor(10)
    #
    # @run_on_executor
    def post(self, *args, **kwargs):

        deslistjson = self.get_argument('deslist', None)
        PathName = self.get_argument('factorypath', None)
        gQDBomFlag = int(self.get_argument('gQDBomFlag', 1))
        IswriteCache = int(self.get_argument('IswriteCache', 0))
        PathName = PathName[0:3]
        print('PathName=',PathName)
        version = r.get(PathName + 'Verison')
        if version:
            version = r.get(PathName + 'Verison')
            myversion = version.decode('utf8')
        else:
            r.set(PathName + 'Verison', '0.01')
            myversion = '0.01'
        logger.info(deslistjson)
        deslist = json.loads(deslistjson)
        AllDesResult = {}
        for des in deslist:
            if IswriteCache == 0:
                state, result = returnresdata(PathName +myversion+ des)
                if state:
                    logger.info(des + 'redis exist data')
                    AllDesResult[des] = result
                    continue
            result = OneBomData2Json(PathName, des, gQDBomFlag)
            AllDesResult[des] = result
            r.set(PathName +myversion+ des, json.dumps(result, ensure_ascii=False).encode('utf8'))
            #print(PathName + des,r.get(PathName + des))
        # except:
        #print(AllDesResult)
        AllDesResult['result'] =1
        AllDesJson = json.dumps(AllDesResult, ensure_ascii=False).encode('utf8')
        self.write(AllDesJson)

class GetVersion(BaseHandler):
    def post(self, *args, **kwargs):
        PathName = self.get_argument('factorypath', None)
        PathName = PathName[0:3]
        version = r.get(PathName + 'Verison')
        result = {}
        if version:
            version = r.get(PathName + 'Verison')
            result['version'] = version.decode('utf8')
            result['result'] = 1
        else:
            r.set(PathName + 'Verison','0.01')
            result['version'] = '0.01'
            result['result'] = 1
        resultjson = json.dumps(result, ensure_ascii=False).encode('utf8')
        self.write(resultjson)
        self.finish()

class NonBlockSleep(tornado.web.RequestHandler):
    #@tornado.gen.coroutine
    # def get(self):
    #     time.sleep(2)
    #     print(2222222222)
    #     self.write("i sleep 2s")
    @tornado.gen.coroutine
    def get(self):
        # i = 0
        # print(00000000000)
        # while i < 40:
        #     yield tornado.gen.sleep(0.05)
        #     if i>=40:
        #         print(2222222222)
        #         break
        #     else:
        #         print(1111111111)
        #         i = i + 1
        # self.awake()
        result =yield self.asyn_sum(2, 3)
        print('result=',result)
        self.finish()
    # def get(self):
    #     tornado.ioloop.IOLoop.instance().add_timeout(time.time() + 2, callback=self.awake)
    #
    def awake(self):
        print(33333333333333)
        self.write("i sleep 2s")

    @tornado.gen.coroutine
    def asyn_sum(self, a, b):
        print("begin calculate:sum %d+%d" % (a, b))
        future = Future()

        def callback(a, b):
            print("calculating the sum of %d+%d:" % (a, b))
            future.set_result(a + b)
        tornado.ioloop.IOLoop.instance().add_callback(callback, a, b)

        #tornado.ioloop.IOLoop.instance().
        result = yield future

        print("after yielded")
        print("the %d+%d=%d" % (a, b, result))
        self.write(str(result))
        return result

class ClearCacheHandle(BaseHandler):
    def post(self, *args, **kwargs):
        PathName = self.get_argument('factorypath', None)
        PathName = PathName[0:3]
        version = r.get(PathName + 'Verison')
        result = {}
        if version:
            version = str(float(version.decode('utf8'))+0.01)
            r.set(PathName + 'Verison', version)
            result['version'] = version
            result['state'] = 1
        else:
            r.set(PathName + 'Verison','0.01')
            result['version'] = '0.01'
            result['state'] = 1
        resultjson = json.dumps(result, ensure_ascii=False).encode('utf8')
        self.write(resultjson)
        self.finish()

class ChangeCacheHandle(BaseHandler):  #增加和修改
    def post(self, *args, **kwargs):
        PathName = self.get_argument('factorypath', None)
        Item = self.get_argument('item', None)
        content = self.get_argument('content', None)
        PathName = PathName[0:3]
        version = r.get(PathName + 'Verison')
        if not version:
            r.set(PathName + 'Verison','0.01')
            version = r.get(PathName + 'Verison')

        myversion = PathName + version.decode('utf8')
        if Item=='allglobaldata' and content=='globaldata':
            data = {'result': 1, 'seqinfo': [], 'classseqinfo': [], 'workflow': [], 'ErpItem': [], 'boardmat': [],
                      'HoleWjFContent': ''}
            try:
                # 1.seqinfo 数据表
                data['seqinfo'] = getseqinfo(PathName)
                # 2.classseqinfo 数据表
                data['classseqinfo'] = getclassseqinfo(PathName)
                # 3.base_workflow 数据表
                data['workflow'] = getworkflow(PathName)
                # 4.erp 数据表
                data['ErpItem'] = getErpItem(PathName)
                # 5.boardmat 数据表
                data['boardmat'] = getboardmat(PathName)
                # 6.孔位五金数据表

                HoleWjFile = dataDBPath + PathName + '\\data\\QDData\孔位五金.cfg'
                if (not os.path.exists(HoleWjFile)):
                    HoleWjFContent = ''
                else:
                    with open(HoleWjFile, 'r') as f:
                        HoleWjFContent = f.read()

                data['HoleWjFContent'] = HoleWjFContent
            except:
                data['result'] = 0
            resultjson = json.dumps(data, ensure_ascii=False).encode('utf8')
            r.set(myversion + 'allglobaldata', resultjson)
            self.write(json.dumps({'state':1}, ensure_ascii=False).encode('utf8'))
            return

        if content == 'Des':
            result = OneBomData2Json(PathName, Item, 1)
            r.set(myversion + Item, json.dumps(result, ensure_ascii=False).encode('gbk'))
            self.write(json.dumps({'state': 1}, ensure_ascii=False).encode('utf8'))
            return
        content = content.encode('gbk')
        result = {}
        if version:

            r.set((myversion + Item).encode('utf8'), content)
            result['state'] = 1
        else:
            myversion = RootName + version.decode('utf8')
            r.set((myversion + Item).encode('utf8'), content)
            result['state'] = 1
        resultjson = json.dumps(result, ensure_ascii=False).encode('utf8')
        self.write(resultjson)
        self.finish()

class DeleteCacheHandle(BaseHandler):
    def post(self, *args, **kwargs):
        PathName = self.get_argument('factorypath', None)
        Item = self.get_argument('item', None)
        PathName = PathName[0:3]
        version = r.get(PathName + 'Verison')
        myversion = PathName + version.decode('utf8')
        key = (myversion + Item).encode('utf8')
        r.delete(key)
        result = {}
        result['state'] = 1
        resultjson = json.dumps(result, ensure_ascii=False).encode('utf8')
        self.write(resultjson)
        self.finish()

class GetCacheHandle(BaseHandler):
    def post(self, *args, **kwargs):
        PathName = self.get_argument('factorypath', None)
        Item = self.get_argument('item', None)
        PathName = PathName[0:3]
        version = r.get(PathName + 'Verison')
        myversion = PathName + version.decode('utf8')
        key = (myversion + Item).encode('utf8')
        content = r.get(key)
        result = {'state':0}
        if content:
            result['state'] = 1
            try:
                result['result'] = json.loads(content.decode('gbk'))
            except:
                result['result'] = json.loads(content.decode('utf8'))
        resultjson = json.dumps(result, ensure_ascii=False).encode('utf8')
        self.write(resultjson)
        self.finish()

def main():
    application = tornado.web.Application([
        (r"/exit_localserver", ExitSystem),
         (r'/Qdbom/bomdata/', Returndata), #http://127.0.0.1:8002/Qdbom/bomdata/?factorypath=data&des=YG%E4%B8%8A%E6%9F%9C,%E5%B7%A6%E4%BE%A7%E6%9D%BF
        (r'/Qdbom/seqinfo/', Returnseqinfo), #http://127.0.0.1:8002/Qdbom/seqinfo/?factorypath=data    返回seqinfo全局数据
        (r'/Qdbom/classseqinfo/', Returnclassseqinfo), #http://127.0.0.1:8002/Qdbom/classseqinfo/?factorypath=data    返回classseqinfo全局数据
        (r'/Qdbom/reportsconfig/', Returnreportsconfig), #http://127.0.0.1:8002/Qdbom/reportsconfig/?factorypath=data    返回gRoc全局数据
        (r'/Qdbom/workflow/', Returnworkflow),    #http://127.0.0.1:8002/Qdbom/workflow/?factorypath=data     返回workflow全局数据
        (r'/Qdbom/erpitem/', ReturngErpItem),     #http://127.0.0.1:8002/Qdbom/erpitem/?factorypath=data   返回Erp全局数据
        (r'/Qdbom/pricetable/', Returngpricetable), #http://127.0.0.1:8002/Qdbom/pricetable/?factorypath=data #返回报价table全局数据
        (r'/Qdbom/quodata/', Returnquodata),    #http://127.0.0.1:8002/Qdbom/quodata/?factorypath=data&des=SG%E4%B8%8A%E6%9F%9C,%E5%B7%A6%E4%BE%A7%E6%9D%BF_%E4%B8%8A%E6%8E%A5
        (r'/Qdbom/boardmat/', ReturnBoardMat), #http://127.0.0.1:8002/Qdbom/boardmat/?factorypath=data   #材料表全局数据
        (r'/Qdbom/xmlbylink/', Returnxmlbylink), #http://127.0.0.1:8002/Qdbom/xmlbylink/?factorypath=data&link=%E6%A8%A1%E6%9D%BF%E7%9B%AE%E5%BD%95\%E6%A0%87%E5%87%86%E6%9F%9C%E4%BD%93\%E7%A7%BB%E9%97%A8%E6%9F%9C\%E7%A7%BB%E9%97%A8%E4%B8%8B%E6%9F%9C\%E4%B8%80%E6%A0%BC%E6%9F%9C
        (r'/Qdbom/HoleWj/', ReturnHoleWj), #http://127.0.0.1:8002/Qdbom/HoleWj/?factorypath=data #孔位五金的全局数据
        (r'/Qdbom/NetQuo/',ReturnNetQuo),    #http://127.0.0.1:8002/Qdbom/NetQuo/?factorypath=data
        (r'/Qdbom/GlobalData/', ReturnGlobalData),
        (r'/Qdbom/AllDesData/', AllDesData),  #用于返回所有类别字段的数据库数据
        (r'/Qdbom/ClearCache/', ClearCacheHandle),
        (r'/Qdbom/GetCache/', GetCacheHandle),
        (r'/Qdbom/DeleteCache/', DeleteCacheHandle),
        (r'/Qdbom/ChangeCache/', ChangeCacheHandle),
        (r'/Qdbom/GetVersion/', GetVersion),  # 用于返回所有类别字段的数据库数据
        #(r'/Qdbom/Write/')
        (r'/Qdbom/NonBlockSleep/',NonBlockSleep),
    ], autoreload=True, xheaders=True,
        template_path=dataDBPath)  # 增加代码有改动，服务器自动重启
    template_path = 'templates'
    static_path = 'static'
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == '__main__':
    # Result = OneBomData2Json(u'格调空间系列,竖拉条_右'.encode('utf8'))
    log_dir = "log"  # 日志存放文件夹名称
    log_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), log_dir)
    if not os.path.isdir(log_path):
        os.makedirs(log_path)
    print(log_path)
    # 设置logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    outputlog()
    main()

'''
http://129.204.134.85:8002/Qdbom/seqinfo/?factorypath=data
http://129.204.134.85:8002/Qdbom/bomdata/?factorypath=data&des=YG%E4%B8%8A%E6%9F%9C,%E5%B7%A6%E4%BE%A7%E6%9D%BF
http://129.204.134.85:8002/Qdbom/xmlbylink/?factorypath=data&link=%E6%A8%A1%E6%9D%BF%E7%9B%AE%E5%BD%95\%E6%A0%87%E5%87%86%E6%9F%9C%E4%BD%93\%E7%A7%BB%E9%97%A8%E6%9F%9C\%E7%A7%BB%E9%97%A8%E4%B8%8B%E6%9F%9C\%E4%B8%80%E6%A0%BC%E6%9F%9C

http://129.204.134.85:8002/Qdbom/quodata/?factorypath=data&des=SG%E4%B8%8A%E6%9F%9C,%E5%B7%A6%E4%BE%A7%E6%9D%BF_%E4%B8%8A%E6%8E%A5

http://129.204.134.85:8002/Qdbom/pricetable/?factorypath=data
http://129.204.134.85:8002/Qdbom/HoleWj/?factorypath=data
'''