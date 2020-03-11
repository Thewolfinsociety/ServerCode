#  -*- coding:utf-8 -*-
'''
服务器版
功能：
vesion 0.0.1
2020/03/11
author:litao
'''
import pypyodbc
from bsddb3 import db
import os
import json
def connectdata(datDBfile):
    conn = pypyodbc.win_connect_mdb('DRIVER={Microsoft Access Driver (*.mdb)};DBQ=' + datDBfile)
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

def OneBomData2Json(des, gQDBomFlag):
    Result = {'result':0,'des2wuliao':[],'ruleHash':[],'childbomHash':[],'wjruleHash':[],'linecalcList':[],
              'holeconfigHash':[],'kcconfigHash':[],'bomstdList':[]}
    datDBfile = 'data.mdb'

    if (not os.path.exists(datDBfile)):
        logger.error('数据库不存在!!!')
        return Result
    else:
        conn, cur = connectdata(datDBfile)
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

def irecords(curs):
    record = curs.first()
    while record:
        yield record
        record = curs.next()
if __name__ =='__main__':
    datDBfile = 'data.mdb'
    if (not os.path.exists(datDBfile)):
        logger.error('数据库不存在!!!')
    else:
        conn, cur = connectdata(datDBfile)
        # sql = "select myclass2.*, myclass1.name as pname from myclass1, myclass2 where myclass2.myclass1=myclass1.id"
        # #sql = "select * from myclass2"
        # cur.execute(sql)
        # u = cur.fetchall()
        # print(len(u))
        #
        # sql = "select myclass2.name, myclass1.name as pname from myclass1, myclass2 where myclass2.myclass1=myclass1.id and myclass1.name<>'' and myclass2.name<>''"
        # # sql = "select * from myclass2"
        # cur.execute(sql)
        # u = cur.fetchall()
        # print(len(u))
        # print(u[0])
        sql = "select myclass1.name, myclass2.name from myclass2,  myclass1 where myclass2.myclass1=myclass1.id and myclass1.name<>'' and myclass2.name<>''"

        cur.execute(sql)
        u = cur.fetchall()
        DB = db.DB()
        DB.open('Data', dbtype=db.DB_HASH, flags=db.DB_CREATE)
        for i in range(0, len(u)):
            data = u[i]
            if (data[0]== '') or (data[1] == ''):
                print('ERROR!!!')
                exit(1)
            des = data[0]+','+data[1]
            Text = DB.get(des.encode('utf8'))
            if Text:
                print(Text.decode('utf8'))
                exit(1)
                continue
            result = OneBomData2Json(des, 1)
            DB.put(des.encode('utf8'), json.dumps(result, ensure_ascii=False).encode('utf8'))

        Sum = 0
        for key, data in irecords(DB.cursor()):
            Sum = Sum + 1
        DB.close()
        if Sum == len(u): print('Success!!!!!!!!!!!!!!')
        else: print('ERROR!!!!!!!!!!!!!!!!')

        # for i in range(0, len(u)):
        #     data = u[i]
        #     print ('i=',i,',desc=', data[17],'des1=',data[5]+','+data[2])
        #     if data[17] == '' :
        #         OneBomData2Json(data[5]+','+data[2], 1)
        #     else:
        #
        #         if data[17] != data[5]+','+data[2]:
        #             des = data[17]
        #             n = des.find(',')
        #             s1 = des[:n]
        #             s2 = des[n + 1:]
        #             sql = "select myclass2.*, myclass1.name as pname from myclass1, myclass2 where myclass2.myclass1=myclass1.id and myclass1.name='%s' and myclass2.name='%s'" % (
        #                 s1, s2)
        #             cur.execute(sql)
        #             des2wuliaoallu = cur.fetchall()
        #             print(des2wuliaoallu)
        #             print('ERROR!!!!',data)
        #             exit(1)
        #         continue
# "select myclass2.*, myclass1.name as pname from myclass1, myclass2 where myclass2.myclass1=myclass1.id and myclass1.name='%s' and myclass2.name='%s'" % (
#                     s1, s2)
                #OneBomData2Json(data[17], 1)
