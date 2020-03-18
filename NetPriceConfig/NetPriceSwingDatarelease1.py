# -*- coding: utf-8 -*-
'''
标题： 掩门配置--提取掩门报价的配置数据
作者： 娄小军
创建时间： 2019-07-10
更新： 新加路径参数
更新时间:2019-12-16
vesion 1.0.3
'''
import os
import sqlite3
import json


'''配件'''
def get_YM_parts(name, cur):
    '''
    配件数据提取
    :param name: 配件类型
    :return:     相关配件数据
    '''
    array = []
    for n in name:
        sql = ("select name2, price, price2, price3, jgprice, jgprice2, jgprice3,\
                color, discount, pricetype, myunit from YM_parts where name2=?")
        sData = (n, )
        cur.execute(sql, sData)
        u = cur.fetchall()
        if u:
            for a in u:
                dict = {"myType": "配件", "name2": a[0], "经销价格": a[1], "零售价格": a[2],
                        "供货价格": a[3], "经销加工费": a[4], "零售加工费": a[5], "供货加工费": a[6],
                        "颜色": a[7], "折扣类型": a[8], "报价类型": a[9], "单位": a[10]}
                if dict not in array:
                    array += [dict]
    return array

'''门芯'''
def get_YM_doorCore(name, cur):
    '''
    门芯数据提取
    :param name: 门板类型
    :return:     相关门芯数据
    '''
    array = []
    for n in name:
        sql = ("select name2, direct, price, price2, price3, jgprice, jgprice2,\
                jgprice3, color, Atj, Amax, Amin, Avalue, lmax, lmin, lvalue,\
                wmax, wmin, wvalue, hmax, hmin, hvalue, discount, pricetype, myunit\
                from YM_doorCore where name2=?")
        sData = (n,)
        cur.execute(sql, sData)
        u = cur.fetchall()
        if u:
            for a in u:
                dict = {"myType": "门芯", "name2": a[0], "纹路": a[1],
                        "经销价格": a[2], "零售价格": a[3], "供货价格": a[4],
                        "经销加工费": a[5], "零售加工费": a[6], "供货加工费": a[7],
                        "颜色": a[8], "附加条件": a[9],
                        "面积最大值": a[10], "面积最小值": a[11], "面积定值": a[12],
                        "长度最大值": a[13], "长度最小值": a[14], "长度定值": a[15],
                        "宽度最大值": a[16], "宽度最小值": a[17], "宽度定值": a[18],
                        "高度最大值": a[19], "高度最小值": a[20], "高度定值": a[21],
                        "折扣类型": a[22], "报价类型": a[23], "单位": a[24]}
                if dict not in array:
                    array += [dict]
    return array

'''门洞'''
def get_YM_doorOpening(name, cur):
    '''
    门洞数据提取
    :param name: 边框类型
    :return:     相关门洞数据
    '''
    array = []
    for n in name:
        sql = ("select name1, price, price2, price3, jgprice, jgprice2,\
                jgprice3, Atj, Amax, Amin, Avalue, lmax, lmin,\
                lvalue, wmax, wmin, wvalue, discount, pricetype, myunit\
                from YM_doorOpening where name1=?")
        sData = (n,)
        cur.execute(sql, sData)
        u = cur.fetchall()
        if u:
            for a in u:
                dict = {"myType": "门洞", "name2": a[0],
                        "经销价格": a[1], "零售价格": a[2], "供货价格": a[3],
                        "经销加工费": a[4], "零售加工费": a[5], "供货加工费": a[6],
                        "附加条件": a[7],
                        "面积最大值": a[8], "面积最小值": a[9], "面积定值": a[10],
                        "长度最大值": a[11], "长度最小值": a[12], "长度定值": a[13],
                        "宽度最大值": a[14], "宽度最小值": a[15], "宽度定值": a[16],
                        "折扣类型": a[17], "报价类型": a[18], "单位": a[19]}
                if dict not in array:
                    array += [dict]
    return array

'''中横框'''
def get_YM_centerTransom(name, cur):
    '''
    中横框提取数据
    :param name: 中横框类型
    :return:中横框数据
    '''
    array = []
    for n in name:
        sql = ("select name2, price, price2, price3, jgprice, jgprice2,\
                jgprice3, color, discount, pricetype, myunit, start_num\
                from YM_centerTransom where name2 =?")
        sData = (n,)
        cur.execute(sql, sData)
        u = cur.fetchall()
        if u:
            for a in u:
                dict = {"myType": "中横框", "name2": a[0],
                        "经销价格": a[1], "零售价格": a[2], "供货价格": a[3],
                        "经销加工费": a[4], "零售加工费": a[5], "供货加工费": a[6],
                        "颜色": a[7], "折扣类型": a[8], "报价类型": a[9],
                        "单位": a[10], "开始报价数量": a[11]}
                if dict not in array:
                    array += [dict]
    return array

'''包装箱'''
def get_YM_packagingBox(name, cur):
    '''
    包装箱提取数据
    :param name:边框类型
    :return:包装箱数据
    '''
    array = []
    for n in name:
        sql = ("select name1, name2, price, price2, price3, jgprice,\
                jgprice2, jgprice3, discount, pricetype, myunit, num\
                from YM_packagingBox where name2 =? or name1= ?")
        sData = (n, n)
        cur.execute(sql, sData)
        u = cur.fetchall()
        if u:
            for a in u:
                dict = {"myType": "包装箱", "name1": a[0], "name2": a[1],
                        "经销价格": a[2], "零售价格": a[3], "供货价格": a[4],
                        "经销加工费": a[5], "零售加工费": a[6], "供货加工费": a[7],
                        "折扣类型": a[8], "报价类型": a[9], "单位": a[10], "数量": a[11]}
                if dict not in array:
                    array += [dict]
    return array

'''成品单门'''
def get_YM_finishedProductSimpleGate(name, cur):
    '''
    成品单门提取数据
    :param name:边框类型
    :return:成品单门数据
    '''
    array = []
    for n in name:
        sql = ("select name1, price, price2, price3, jgprice, jgprice2,\
                jgprice3, Atj, color, Amax, Amin, Avalue, lmax, lmin,\
                lvalue, wmax, wmin, wvalue, discount, pricetype, myunit\
                from YM_finishedProductSimpleGate where name1 =?")
        sData = (n,)
        cur.execute(sql, sData)
        u = cur.fetchall()
        if u:
            for a in u:
                dict = {"myType": "成品单门", "name2": a[0],
                        "经销价格": a[1], "零售价格": a[2], "供货价格": a[3],
                        "经销加工费": a[4], "零售加工费": a[5], "供货加工费": a[6],
                        "附加条件": a[7], "颜色": a[8],
                        "面积最大值": a[9], "面积最小值": a[10], "面积定值": a[11],
                        "长度最大值": a[12], "长度最小值": a[13], "长度定值": a[14],
                        "宽度最大值": a[15], "宽度最小值": a[16], "宽度定值": a[17],
                        "折扣类型": a[18], "报价类型": a[19], "单位": a[20]}
                if dict not in array:
                    array += [dict]
    return array

'''定款门'''
def get_YM_setDoor(name, cur):
    '''
    定款门提取数据
    :param name:定款门名称
    :return:定款门数据
    '''
    array = []
    for n in name:
        sql = ("select name1, price, price2, price3, jgprice,  jgprice2,\
                jgprice3, Atj, Amax, Amin, Avalue, lmax, lmin, lvalue,\
                wmax, wmin, wvalue, discount, pricetype, myunit\
                from YM_setDoor where name1 =?")
        sData = (n,)
        cur.execute(sql, sData)
        u = cur.fetchall()
        if u:
            for a in u:
                dict = {"myType": "定款门", "name2": a[0],
                        "经销价格": a[1], "零售价格": a[2], "供货价格": a[3],
                        "经销加工费": a[4], "零售加工费": a[5], "供货加工费": a[6],
                        "附加条件": a[7],
                        "面积最大值": a[8],  "面积最小值": a[9],  "面积定值": a[10],
                        "长度最大值": a[11], "长度最小值": a[12], "长度定值": a[13],
                        "宽度最大值": a[14], "宽度最小值": a[15], "宽度定值": a[16],
                        "折扣类型":   a[17], "报价类型": a[18], "单位": a[19]}
                if dict not in array:
                    array += [dict]
    return array

'''单门尺寸限制'''
def get_YM_doorSizeLimit(name, cur):
    '''
    单门尺寸限制提取数据
    :param name:单门
    :return:单门尺寸限制数据
    '''
    array = []
    for n in name:
        sql = ("select name, mjlimit from YM_doorSizeLimit where name =?")
        sData = (n,)
        cur.execute(sql, sData)
        u = cur.fetchall()
        if u:
            for a in u:
                dict = {"myType": "单门尺寸限制", "name2":a[0], "最小单门面积":a[1]}
                if dict not in array:
                    array += [dict]
    return array

'''门铰'''
def get_YM_doorHinge(name, cur):
    '''
    门铰提取数据
    :param name:门铰类型
    :return:门铰数据
    '''
    array = []
    for n in name:
        sql = ("select name2, price, price2, price3,\
                jgprice, jgprice2, jgprice3, discount, pricetype, myunit\
                from YM_doorHinge where name2 =?")
        sData = (n,)
        cur.execute(sql, sData)
        u = cur.fetchall()
        if u:
            for a in u:
                dict = {"myType": "门铰", "name2": a[0],
                        "经销价格": a[1], "零售价格": a[2], "供货价格": a[3],
                        "经销加工费": a[4], "零售加工费": a[5], "供货加工费": a[6],
                        "折扣类型": a[7], "报价类型": a[8], "单位": a[9]}
                if dict not in array:
                    array += [dict]
    return array

'''拉手'''
def get_YM_shakeHands(name, cur):
    '''
    拉手提取数据
    :param name:拉手类型
    :return:拉手数据
    '''
    array = []
    for n in name:
        sql = ("select name2, price, price2, price3,\
                jgprice, jgprice2, jgprice3, discount, pricetype, myunit\
                from YM_shakeHands where name2=?")
        sData = (n,)
        cur.execute(sql, sData)
        u = cur.fetchall()
        if u:
            for a in u:
                dict = {"myType": "拉手", "name2": a[0],
                        "经销价格": a[1], "零售价格": a[2], "供货价格": a[3],
                        "经销加工费": a[4], "零售加工费": a[5], "供货加工费": a[6],
                        "折扣类型": a[7], "报价类型": a[8], "单位": a[9]}
                if dict not in array:
                    array += [dict]
    return array

'''上下横'''
def get_YM_upAndDownTransom(name, cur):
    '''
    上下横提取数据
    :param name:上下横类型
    :return:上下横数据
    '''
    array = []
    for n in name:
        sql = ("select name2, price, price2, price3, jgprice, jgprice2,\
                jgprice3, color, discount, pricetype, myunit, start_num\
                from YM_upAndDownTransom where name2 =?")
        sData = (n,)
        cur.execute(sql, sData)
        u = cur.fetchall()
        if u:
            for a in u:
                dict = {"myType": "上下横", "name2": a[0],
                        "经销价格": a[1], "零售价格": a[2], "供货价格": a[3],
                        "经销加工费": a[4], "零售加工费": a[5], "供货加工费": a[6],
                        "颜色": a[7], "折扣类型": a[8], "报价类型": a[9],
                        "单位": a[10], "开始报价数量": a[11]}
                if dict not in array:
                    array += [dict]
    return array

'''附加物料'''
def get_YM_additionalMaterials(name, cur):
    '''
    附加物料提取数据
    :param name:边框类型，，物料名称
    :return:附加物料数据
    '''
    array = []
    for n in name:
        sql = ("select name1, name2, price, price2, price3, jgprice, jgprice2,\
                jgprice3, color, Atj, Amax, Amin, Avalue, lmax, lmin, lvalue,\
                wmax, wmin, wvalue, hmax, hmin, hvalue, discount, pricetype, myunit\
                from YM_additionalMaterials where name1 =? or name2 = ?")
        sData = (n, n)
        cur.execute(sql, sData)
        u = cur.fetchall()
        if u:
            for a in u:
                dict = {"myType": "附加物料", "name1": a[0], "name2": a[1],
                        "经销价格": a[2], "零售价格": a[3], "供货价格": a[4],
                        "经销加工费": a[5], "零售加工费": a[6], "供货加工费": a[7],
                        "颜色": a[8], "附加条件": a[9],
                        "面积最大值": a[10], "面积最小值": a[11], "面积定值": a[12],
                        "长度最大值": a[13], "长度最小值": a[14], "长度定值": a[15],
                        "宽度最大值": a[16], "宽度最小值": a[17], "宽度定值": a[18],
                        "高度最大值": a[19], "高度最小值": a[20], "高度定值": a[21],
                        "折扣类型": a[22], "报价类型": a[23], "单位": a[24]}
                if dict not in array:
                    array += [dict]
    return array

'''竖框'''
def get_YM_mullion(name, cur):
    '''
    竖框提取数据
    :param name:竖框类型
    :return:竖框数据
    '''
    array = []
    for n in name:
        sql = ("select name2, price, price2, price3, jgprice, jgprice2,\
                jgprice3, color, discount, pricetype, myunit, start_num\
                from YM_mullion where name2 = ?")
        sData = (n, )
        cur.execute(sql, sData)
        u = cur.fetchall()
        if u:
            for a in u:
                dict = {"myType": "竖框", "name2": a[0],
                        "经销价格": a[1], "零售价格": a[2], "供货价格": a[3],
                        "经销加工费": a[4], "零售加工费": a[5], "供货加工费": a[6],
                        "颜色": a[7], "折扣类型": a[8], "报价类型": a[9],
                        "单位": a[10], "开始报价数量": a[11]}
                if dict not in array:
                    array += [dict]
    return array


'''获取掩门配置报价数据'''
def GetSwingNetConfig(name, rootPath):
    DBfilename = rootPath + "\\data\\" + "NetPriceDB.db"
    conn = sqlite3.connect(DBfilename)
    cur = conn.cursor()
    array = []
    '''配件'''
    data = get_YM_parts(name, cur)
    if data:
        array += data
    '''门芯'''
    data = get_YM_doorCore(name, cur)
    if data:
        array += data
    '''门洞'''
    data = get_YM_doorOpening(name, cur)
    if data:
        array += data
    '''中横框'''
    data = get_YM_centerTransom(name, cur)
    if data:
        array += data
    '''包装箱'''
    data = get_YM_packagingBox(name, cur)
    if data:
        array += data
    '''成品单门'''
    data = get_YM_finishedProductSimpleGate(name, cur)
    if data:
        array += data
    '''定款门'''
    data = get_YM_setDoor(name, cur)
    if data:
        array += data
    '''单门尺寸限制'''
    data = get_YM_doorSizeLimit(name, cur)
    if data:
        array += data
    '''门铰'''
    data = get_YM_doorHinge(name, cur)
    if data:
        array += data
    '''拉手'''
    data = get_YM_shakeHands(name, cur)
    if data:
        array += data
    '''上下横'''
    data = get_YM_upAndDownTransom(name, cur)
    if data:
        array += data
    '''附加物料'''
    data = get_YM_additionalMaterials(name, cur)
    if data:
        array += data
    '''竖框'''
    data = get_YM_mullion(name, cur)
    if data:
        array += data
    cur.close()
    conn.close()
    return array
