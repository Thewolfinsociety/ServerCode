# -*- coding: utf-8 -*-
'''
标题： 根据类别列表提取网络报价的配置数据
作者： 娄小军
时间： 2019-07-04
更新：  python3版本，新增加一个路径参数
更新时间： 2019-11-08
vesion 1.0.9
'''
import os
import sqlite3
import json
import redis
import NetPriceSlidingData  # 调取趟门配置数据
import NetPriceSwingData     # 掩门
pool = redis.ConnectionPool(host='127.0.0.1',port=6379)    #'129.204.134.85'
r = redis.Redis(connection_pool=pool)

def returnresdata(recemessage):
    # try:
    #     status = True
    #     content = r.get(recemessage)
    #     if not content:
    #         return False, ''
    #
    #     result = json.loads(content, encoding='gbk')
    #
    #
    # except Exception as e:
    #     status = False
    #     result = ''
    #     content = ''
    #     print(e)
    status = False
    result = ''
    return status, result

# 获取材料
def GetMaterialsData(cur):
    sql = "select board_mate, board_thick, color, output_name from materials_table"
    cur.execute(sql)
    u = cur.fetchall()
    array = []
    for a in u:
        dict = {"板材材料": a[0], "板厚": a[1], "颜色": a[2], "报表输出名称": a[3]}
        array += [dict]
    return array


# 获取板件折扣方案
def GetBoardDisScheme(cur):
    sql = "select name, dis_type, sell_dis, retail_dis, supply_dis,\
            dis_range, supplyRefeDis from board_dis_scheme"
    cur.execute(sql)
    u = cur.fetchall()
    disScheme = []
    for a in u:
        if a[0] not in disScheme:
            disScheme.append(a[0])
    array = []
    for name in disScheme:
        schemeList = []
        for a in u:
            if a[0] == name:
                scheme = {"折扣类型": a[1], "经销折扣": a[2], "零售折扣": a[3],
                          "供货折扣": a[4], "折扣范围": a[5]}
                schemeList += [scheme]
        dict = {"名称": name, "方案": schemeList}
        array += [dict]
    return array


# 获取报价方案--门报价
def GetQuoteSchemeDoorPrice(cur, name):
    if len(name) < 2:
        return []
    sql0 = "select ID from quote_scheme where quote_group=? and quote_scheme=?"
    data = (name[0], name[1])
    cur.execute(sql0, data)
    Gid = cur.fetchone()
    array = []
    if Gid:
        sql = ("select gate_materials, name, supply_price, sell_price, retail_price,\
                pull_hand, gate_color from gate_quote where quote_scheme_ID =?")
        data = (Gid[0], )
        cur.execute(sql, data)
        u = cur.fetchall()
        if not u:
            dict = {"门材料": '', "name": '', "供货价": '', "经销价": '',
                    "零售价": '', "标配拉手": '', "门颜色": ''}
            array += [dict]
        else:
            for a in u:
                hands = a[5].split(',')
                color = a[6].split(',')
                dict = {"门材料": a[0], "name": a[1], "供货价": a[2], "经销价": a[3],
                        "零售价": a[4], "标配拉手": hands, "门颜色": color}
                array += [dict]
    return array


# 获取报价方案
def GetQuoteScheme(data, cur):
    array = {}
    for i in data:
        name = i.split('--')
        if len(name) < 2:
            continue
        doorQuote = GetQuoteSchemeDoorPrice(cur, name)
        sql = ("select quote_group, quote_scheme, supply_price, supply_process_charges,\
                const_value, max, min,materials, criteria, sell_price, shellFormula,\
                sell_process_charges, retail_price, retailFormula,\
                retail_process_charges, color, AreaFormula from quote_scheme \
                where quote_group=? and quote_scheme=?")
        data = (name[0], name[1])
        cur.execute(sql, data)
        u = cur.fetchall()
        list = []
        if not u:
            dict = {"组别": name[0], "报价方案": name[1], "供货价格":'', "供货加工费": '',
                    "定值": '', "最大": '', "最小": '', "材料": '', "条件": '',
                    "经销价格": '', "经销计算公式": '', "经销加工费": '',
                    "零售价格": '', "零售计算公式": '', "零售加工费": '',
                    "颜色": '', "面积计算公式": '', "门报价": ''}
            list += [dict]
            array[i] = list
        else:
            for a in u:
                dict = {"组别": a[0], "报价方案": a[1], "供货价格": a[2], "供货加工费": a[3],
                        "定值": a[4], "最大": a[5], "最小": a[6], "材料":a[7], "条件": a[8],
                        "经销价格": a[9], "经销计算公式": a[10], "经销加工费": a[11],
                        "零售价格": a[12], "零售计算公式": a[13], "零售加工费": a[14],
                        "颜色": a[15], "面积计算公式": a[16], "门报价": doorQuote}
                list += [dict]
                array[i] = list
    return array


# 报价配置
def GetNetPriceData(data, cur):
    QuoConf = {}
    QuoteScheme = []
    for name in data:
        if ',' in name:
            # status, result = returnresdata(rootname + attri)
            # if status:

            sql = ("select 报价类别, 分类,单位, 输出名称, 加工费, 报价方式, 打折类型, 报表类型,\
                    备注1, 备注2, 独立报价 from quote_conf where 报价类别 =?" )
            data = (name,)
            cur.execute(sql, data)
            u = cur.fetchone()
            if not u:
                continue
            array = {"报价类别": u[0], "分类": u[1], "单位": u[2], "输出名称": u[3],
                "加工费": u[4], "报价方式": u[5], "打折类型": u[6], "报表类型": u[7],
                "备注1": u[8], "备注2": u[9], "独立报价": u[10]}

            sql1 = "select 报价类别, 报价方案, 标准, type, 最大, 最小, 定值 from quote_conf_rule where 报价类别 =?"
            data = (name, )
            cur.execute(sql1, data)
            u = cur.fetchall()
            Len1 = []   # 标准长度
            Len2 = []   # 非标准长度
            Len3 = []   # 非标准2长度
            Weit1 = []
            Weit2 = []
            Weit3 = []
            Heigh1 = []
            Heigh2 = []
            Heigh3 = []
            quoteRule = {}
            for a in u:
                if a[1] and a[1] not in QuoteScheme:
                    # 获取相应的报价方案
                    QuoteScheme.append(a[1])
                if a[2] == "标准":
                    if a[3] == "长度":
                        dict = {"最大": a[4], "最小": a[5], "定值": a[6]}
                        Len1 += [dict]
                    if a[3] == "宽度":
                        dict = {"最大": a[4], "最小": a[5], "定值": a[6]}
                        Weit1 += [dict]
                    if a[3] == "高度":
                        dict = {"最大": a[4], "最小": a[5], "定值": a[6], "报价方案":a[1]}
                        Heigh1 += [dict]
                    type1 = {"长度": Len1, "宽度": Weit1, "高度": Heigh1}
                    quoteRule["标准"] = type1
                # 非标准
                if a[2] == "非标准":
                    if a[3] == "长度":
                        dict = {"最大": a[4], "最小": a[5], "定值": a[6]}
                        Len2 += [dict]
                    if a[3] == "宽度":
                        dict = {"最大": a[4], "最小": a[5], "定值": a[6]}
                        Weit2 += [dict]
                    if a[3] == "高度":
                        dict = {"最大": a[4], "最小": a[5], "定值": a[6], "报价方案":a[1]}
                        Heigh2 += [dict]
                    type2 = {"长度": Len2, "宽度": Weit2, "高度": Heigh2}
                    quoteRule["非标准"] = type2
                # 非标准2
                if a[2] == "非标准2":
                    if a[3] == "长度":
                        dict = {"最大": a[4], "最小": a[5], "定值": a[6]}
                        Len3 += [dict]
                    if a[3] == "宽度":
                        dict = {"最大": a[4], "最小": a[5], "定值": a[6]}
                        Weit3 += [dict]
                    if a[3] == "高度":
                        dict = {"最大": a[4], "最小": a[5], "定值": a[6], "报价方案":a[1]}
                        Heigh3 += [dict]
                    type3 = {"长度": Len3, "宽度": Weit3, "高度": Heigh3}
                    quoteRule["非标准2"] = type3
            array["报价规则"]= quoteRule

            # 五金规则
            sql = ("select 报价类别, 五金名称, 最大宽度, 最小宽度, 最大深度, 最小深度, 最大高度, \
                    最小高度, 数量, 配置规则, 材料, 颜色, 连柜功能 from wj_rule where 报价类别=?")
            data = (name, )
            cur.execute(sql, data)
            u = cur.fetchall()
            WJRule = []
            for a in u:
                dict = {"五金名称": a[1], "最大宽度": a[2], "最小宽度": a[3], "最大深度": a[4],
                        "最小深度": a[5], "最大高度": a[6], "最小高度": a[7], "数量": a[8],
                        "配置规则": a[9], "材料": a[10], "颜色": a[11], "是否连柜五金": a[12]}
                WJRule += [dict]
            array["五金规则"] = WJRule


            QuoConf[name] = array

    list = {"报价配置": QuoConf,
            "报价方案": QuoteScheme}
    return list


# 用户权限
def GetUserPermission(cur):
    sql = ("select username, password, Gid, price_type, dis_scheme, "
           "gate_quote, default_price from user_permission")
    cur.execute(sql)
    u =cur.fetchall()
    array = []
    for a in u:
        priceType = a[3].split(',')
        disType = a[4].split(',')
        doorPricr = a[5].split(',')
        defaultPrice = a[6].split(',')
        dict = {"用户名": a[0], "密码": a[1], "价格类型": priceType,
                "折扣类型": disType, "门报价": doorPricr, "默认报价": defaultPrice}
        array += [dict]
    return array


# 合并规则
def GetMergingRules(cur):
    sql = ("select univalence, size, report_output, materials, sort_name,\
            output_name, color, memo1, memo2 from merging_rules")
    cur.execute(sql)
    u = cur.fetchone()
    if not u:
        array = {"单价": '', "尺寸": '', "报表输出分类": '', "材料": '',
                 "类别名称": '', "输出名称": '', "颜色": '', "备注1": '', "备注2": ''}
    else:
        array = {"单价": u[0], "尺寸": u[1], "报表输出分类": u[2], "材料": u[3],
                 "类别名称": u[4], "输出名称": u[5], "颜色": u[6], "备注1": u[7], "备注2": u[8]}
    return array


# 报价输出排序
def GetQuoteOutputSort(cur):
    sql0 = "select name from quote_output_myclass1 order by ID"
    cur.execute(sql0)
    u = cur.fetchall()
    array = []
    for a in u:
        sql = "select output_name from quote_output_sort where name=? order by ID"
        data = (a[0],)
        cur.execute(sql, data)
        Lest = cur.fetchall()
        temp = []
        for i in Lest:
            dict = {"名称排序": i[0]}
            temp += [dict]
        dict2 = {"name": a[0], "subName": temp}
        array += [dict2]
    return array


# 基础五金
def getBase_Wj(cur):
    sql = "select name, units, price1, price2, price3, Numb from base_wj"
    cur.execute(sql)
    u = cur.fetchall()
    array = []
    for a in u:
        dict = {"名称": a[0], "单位": a[1], "价格": a[2],
                "零售价": a[3], "经销价": a[4], "编号": a[5]}
        array += [dict]
    return array

def getdata(rootname, attri, func, cur):

    status, result = returnresdata(rootname + attri)
    if status:
        #(rootname + attri, result)
        #print('status', True)
        mPExp = result
    else:
        #('status', False)
        mPExp = func(cur)  # 单门数量类型
        r.set(rootname + attri, json.dumps(mPExp, ensure_ascii=False).encode('gbk'))
    return mPExp

# 根据类别列表获取网络报价配置
def GetNetworkQuoteConfigHandl(name, slidingDoor, swingDoor, rootPath, myversion):
    print("-----网络报价配置数据获取---")
    try:
    # base_dir = os.path.abspath(os.path.join(os.getcwd()))
        DBfilename = rootPath + "\\data\\" + "NetPriceDB.db"
        conn = sqlite3.connect(DBfilename)
        cur = conn.cursor()
        materials = getdata(myversion, 'materials',GetMaterialsData, cur)          # 材料表
        boardDisScheme = getdata(myversion, 'boardDisScheme', GetBoardDisScheme, cur)  # 板件折扣
        userPermission = getdata(myversion, 'userPermission', GetUserPermission, cur) # 用户权限
        mergingRule = getdata(myversion, 'mergingRule', GetMergingRules, cur)# 合并规则
        quoteSort = getdata(myversion, 'quoteSort', GetQuoteOutputSort, cur)    # 报价输出排序
        baseWj = getdata(myversion, 'baseWj', getBase_Wj, cur)                   # 基础五金

        list = GetNetPriceData(name, cur)  # 报价配置
        array = list["报价配置"]
        QuoteSchemeData = list["报价方案"]

        QuoteScheme = GetQuoteScheme(QuoteSchemeData, cur)  # 报价方案
        slidingDoorData = NetPriceSlidingData.GetDoorDataHandler(slidingDoor, rootPath, myversion, r)   # 趟门配置数据
        swingDoorData = NetPriceSwingData.GetSwingNetConfig(swingDoor, rootPath)          # 掩门配置数据
        dict = {"材料": materials,
                "板件折扣方案": boardDisScheme,
                "报价排序": quoteSort,
                "基础五金": baseWj,
                "用户权限": userPermission,
                "合并规则": mergingRule,
                "报价方案": QuoteScheme,
                "报价配置": array,
                "趟门配置": slidingDoorData,
                "掩门配置": swingDoorData,
                "result":1
            }
        return dict
    except Exception as e:
        print("网络报价配置数据 ERROR： ", e)
        result = {"state": -1, "info": "获取网络报价配置数据系统错误", "result":0}
        return result
