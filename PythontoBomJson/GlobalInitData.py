#  -*- coding:utf-8 -*-
import os
#from useful_tools import *
import xml.etree.ElementTree as ET
import configparser
import pypyodbc
import json

base_dir = os.path.abspath(os.path.join(os.getcwd()))
ServerPath = os.path.abspath(os.path.join(os.getcwd(),'../..'))+'\\nginx-1.0.11\\nginx-1.0.11\html\\'
RootPath = ""
print('base_dir=',base_dir)
def defineRootPath(path):
    global RootPath
    RootPath = path

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

class BoardMat(object):
    def __init__(self):
        self.id = 0
        self.name = ''
        self.color = ''
        self.alias = ''
        self.alias2 = ''
        self.alias3 = ''
        self.bh = 0

class pluginob(object):
    def __init__(self):
        self.name = ''
        self.dll = ''
        self.handle = 0

class PriceTable(object):
    def __init__(self):
        self.name = ''
        self.mat = ''
        self.price1 = ''
        self.price2 = ''
        self.cost = ''
        self.price_exp1 = ''
        self.price_exp2 = ''
        self.bh = 0
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
#初始化BaseGraph目录
def get_file_ext(filename):
    '''

    :param filename: '123.txt'
    :return: txt
    '''
    return  filename[filename.index('.') + 1:]

def SearchBGDir(file_dir):
    gBGHash = {}
    #gBGHash 为收集 BaseGraph 目录下文件内容
    if os.path.exists(file_dir):
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if get_file_ext(file)!='x2d':
                    continue
                with open(file_dir+file,'r') as f:
                    bg = file[:(len(file)-4)]
                    xml = f.read()
                    try:
                        xml = xml.decode('gbk').encode('utf8').replace('gb2312', 'utf-8')
                    except:
                        xml = xml.replace('gb2312', 'utf-8')
                    n = xml.find('V="1"')
                    if n>0:
                        gBGHash[bg] = xml
                    else:
                        pass
    return gBGHash

def InitBGHash():
    X2dPath = RootPath + '\\BaseGraph\\'
    gBGHash = SearchBGDir(X2dPath)
    return gBGHash


#初始化Plugins目录
def InitPluginsList():
    gPluginsList = []
    pluginPath = RootPath + '\\Plugins\\'
    filename = pluginPath+'qdbom.xml'

    if os.path.exists(filename):
        with open(filename,'r') as f:
            xml = f.read()
        root = ET.fromstring(xml.decode('gb2312').encode('utf8').replace('gb2312','utf-8'))
        for i in range(len(root)):
            node = root[i]
            attri1 = node.get('Name','')
            attri2 = node.get('Dll','')
            if (attri1 ==None) or (attri1 == '') : continue
            if (attri2 == None) or (attri2 == '') : continue
            p = pluginob()
            p.name = attri1
            p.dll = attri2
            p.handle = 0
            # if p.name ==
            # FuncPluginGetValue_P = WINFUNCTYPE(c_int, c_char_p, c_char_p, c_char_p, c_char_p, POINTER(c_char * 256))
            # func = FuncPluginGetValue_P(FuncPluginGetValue)
            # p.SetCallbackFunc(c_char_p('GetValue'), func, 0)

            gPluginsList.append(p)
    return gPluginsList
def InitptableList():
    dataDBfile = RootPath.decode('gbk') + '\\data\\data.mdb'
    ptableList = []
    if os.path.exists(dataDBfile):

        conn = pypyodbc.win_connect_mdb(r'DRIVER={Microsoft Access Driver (*.mdb  *.accbd)};DBQ=' + dataDBfile)
        cur = conn.cursor()
        sql = "select * from base_pricetable where deleted=False order by 材料".encode('gbk')
        cur.execute(sql)

        pricetableallu = cur.fetchall()
        if pricetableallu!=[]:
                typelist = []
                for tup in cur.description:
                    typelist.append(tup[0])  # 编码gbk
                for i in range(0, len(pricetableallu)):
                    fjo = getfjo(i, typelist, pricetableallu)
                    ptable = PriceTable()
                    ptable.name = fjo['报价方案'.encode('gbk')]
                    ptable.mat = fjo['材料'.encode('gbk')]
                    ptable.price1 = fjo['价格1'.encode('gbk')]
                    ptable.price2 = fjo['价格2'.encode('gbk')]
                    ptable.bh = Nonetonumber(fjo['bh'])
                    ptable.cost = fjo['加工费用'.encode('gbk')]
                    ptable.price_exp1 = fjo['price_exp1']
                    ptable.price_exp2 = fjo['price_exp2']
                    ptableList.append(ptable)
    return ptableList
def InitBomHash(): #data.mdb
    def productdict(u, key, value, exdict):
        Result = {}
        if u == []:
            return
        for i in u:
            try:
                exdict[i[key]] = i[value]
            except:
                pass
    #global gROC
    seqInfoHash = {}
    classseqInfoHash = {}
    workflowlist = []
    gQDBomFlag = 1
    gROC = ReportOutputConfig()
    gROC.bj_out_classname = True
    gROC.bj_out_myclass = False
    gROC.bj_out_name = False
    gROC.bj_out_mat = True
    gROC.bj_out_color = True
    gROC.bj_out_size = True
    gROC.bj_out_price = True
    gROC.wl_out_classname = True
    gROC.wl_out_myclass = False
    gROC.wl_out_name = True
    gROC.wl_out_mat = True
    gROC.wl_out_color = True
    gROC.wl_out_size = True
    gROC.wl_out_kc = True
    gROC.wl_out_fb = True
    gROC.wl_out_memo = True
    gROC.wl_out_hole = True
    dataDBfile = RootPath.decode('gbk') + '\\data\\data.mdb'
    if os.path.exists(dataDBfile):

        conn = pypyodbc.win_connect_mdb(r'DRIVER={Microsoft Access Driver (*.mdb  *.accbd)};DBQ=' + dataDBfile)


        cur = conn.cursor()
        seqInfoHashSql = 'select bomname,bomseq from base_seqinfo'
        cur.execute(seqInfoHashSql)
        u = cur.fetchall()

        productdict(u,0,1,seqInfoHash)
        # # id(seqInfoHash),seqInfoHash
        if gQDBomFlag == 0 :
            seqinfosql = 'select name, seq from base_classseqinfo where ID>1000 order by seq asc'
        else:
            seqinfosql = 'select name, seq from base_classseqinfo where ID>1000 order by seq asc'
        cur.execute(seqinfosql)
        u = cur.fetchall()
        productdict(u, 0, 1, classseqInfoHash)
        reposql = 'select * from reports_config'
        cur.execute(reposql)
        u = cur.fetchall()

        gROC.bj_out_classname= u[0][1]
        gROC.bj_out_myclass= u[0][2]
        gROC.bj_out_name= u[0][3]
        gROC.bj_out_mat= u[0][4]
        gROC.bj_out_color= u[0][5]
        gROC.bj_out_size= u[0][6]
        gROC.bj_out_price= u[0][7]

        gROC.wl_out_classname= u[0][8]
        gROC.wl_out_myclass= u[0][9]
        gROC.wl_out_name= u[0][10]
        gROC.wl_out_maz= u[0][11]
        gROC.wl_out_color= u[0][12]
        gROC.wl_out_size = u[0][13]
        gROC.wl_out_kc = u[0][14]
        gROC.wl_out_fb = u[0][15]
        gROC.wl_out_memo = u[0][16]
        gROC.wl_out_hole = u[0][17]

        basesql = 'select id,name,bomstd,hole,board_cut,edge_banding,punching from base_workflow'
        cur.execute(basesql)
        u = cur.fetchall()

        for i in u:
            pwf = TKCConfig()
            pwf.id = i[0]
            pwf.name = i[1]
            pwf.bomstd = i[2]
            pwf.hole = i[3]
            pwf.board_cut = i[4]
            pwf.edge_banding = i[5]
            pwf.punching = i[6]
            workflowlist.append(pwf)
    return seqInfoHash, classseqInfoHash, workflowlist, gROC

def InitBoardMatList(): #XScriptDb.mdb
    XSDBfile = RootPath.decode('gbk') + '\\data\\XScriptDb.mdb'
    gBoardMatList = []
    if os.path.exists(XSDBfile):
        connX = pypyodbc.win_connect_mdb(r'DRIVER={Microsoft Access Driver (*.mdb  *.accbd)};DBQ=' + XSDBfile)
        base_boardsql = "select * from base_boardmaterial_classify"
        gBoardMatList = []
        cur = connX.cursor()
        cur.execute(base_boardsql)
        u = cur.fetchall()
        for i in u:
            p = BoardMat()
            p.name = i[1]
            p.bh = i[3]
            p.alias = i[4]
            p.alias2 = i[5]
            p.alias3 = i[6]
            p.color = i[2]
            gBoardMatList.append(p)
    return gBoardMatList

def InitErpList():    #erp.mdb and snimay.mdb
    erpDBfile = RootPath.decode('gbk') + '\\Plugins\\erp.mdb'
    gErpItemList = []
    if not os.path.exists(erpDBfile):

        if not os.path.exists(RootPath.decode('gbk')+'snimay.mdb'):
            return gErpItemList
        erpDBfile =RootPath.decode('gbk') + '\\Plugins\\snimay.mdb'
    if os.path.exists(erpDBfile):
        conn = pypyodbc.win_connect_mdb(r'DRIVER={Microsoft Access Driver (*.mdb  *.accbd)};DBQ=' + erpDBfile)
        cur = conn.cursor()

        sql = "select * from mat order by id"
        cur.execute(sql)
        u1 = cur.fetchall()
        for u in u1:
            p = {}
            p['deleted'] = False
            p['id'] = u[0]
            p['name'] = u[1]
            p['mat'] = u[2]
            p['color'] = u[3]
            p['h'] = u[4]
            p['flag'] = u[5]
            p['myclass'] = u[6]
            p['myunit'] = u[7]
            gErpItemList.append(p)
    return gErpItemList

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

def producemJoBarCode():
    mJoBarCode = {}  # 'qd.conf'/[BarCode]
    mDoorPrecision = 0
    mIIHoleCalcRule = {}
    cf = configparser.ConfigParser()
    confPath = RootPath + '\\qd.conf'
    copyconffile = RootPath + '\\copyqd.conf'
    if os.path.exists(confPath):
        print(copyconffile)
        with open(copyconffile, 'w+') as f:
            with open(confPath, 'r') as f1:
                content = f1.read()
                content = content.replace('//', '#')
            f.write(content)

        cf.read(copyconffile)


        try:
            db_host = cf.get("孔位计算规则".encode('gb2312'), "通孔计算".encode('gb2312'))
        except:
            db_host = '{}'
        try:
            mJoBarcode =cf.get("BarCode".encode('gb2312'), "A_MPR".encode('gb2312'))
            mJoBarCode['A_MPR'] = ToBarCode({},mJoBarcode)
        except:
            mJoBarCode['A_MPR'] =''
        try:
            mJoBarcode = cf.get("BarCode".encode('gb2312'), "B_MPR".encode('gb2312'))
            mJoBarCode['B_MPR'] = ToBarCode({}, mJoBarcode)
        except:
            mJoBarCode['B_MPR'] =''
        try:
            mJoBarcode = cf.get("BarCode".encode('gb2312'), "AB_BPP".encode('gb2312'))
            mJoBarCode['AB_BPP'] = ToBarCode({}, mJoBarcode)
        except:
            mJoBarCode['AB_BPP'] =''
        try:
            mJoBarcode = cf.get("BarCode".encode('gb2312'), "A_BPP".encode('gb2312'))
            mJoBarCode['A_BPP'] = ToBarCode({}, mJoBarcode)
        except:
            mJoBarCode['A_BPP'] =''
        try:
            mJoBarcode = cf.get("BarCode".encode('gb2312'), "B_BPP".encode('gb2312'))
            mJoBarCode['B_BPP'] = ToBarCode({}, mJoBarcode)
        except:
            mJoBarCode['B_BPP'] =''
        try:
            mJoBarcode = cf.get("BarCode".encode('gb2312'), "DXF".encode('gb2312'))
            mJoBarCode['DXF'] = ToBarCode({}, mJoBarcode)
        except:
            mJoBarCode['DXF'] =''
        try:
            mJoBarcode = cf.get("BarCode".encode('gb2312'), "BDFILE".encode('gb2312'))
            mJoBarCode['BDFILE'] = ToBarCode({}, mJoBarcode)
        except:
            mJoBarCode['BDFILE'] = ''
        os.remove(copyconffile)

    # kvs = cf.items(u"孔位计算规则".encode('gb2312'))
        mIIHoleCalcRule = json.loads(db_host)
        try:
            mDoorPrecision = cf.get("QuickDraw".encode('gb2312'), "DoorPrecision".encode('gb2312'))
        except:
            mDoorPrecision = 0
    #print 'mDoorPrecision=',mDoorPrecision

    return mIIHoleCalcRule,mDoorPrecision, mJoBarCode


def getfjo(i, typelist, ufetchall):
    fjo = {}
    for j in range(0, len(ufetchall[i])):
        if isinstance(ufetchall[i][j], int) or isinstance(ufetchall[i][j], float):
            fjo[typelist[j]] = str(ufetchall[i][j])
        else:
            if typelist[j]=='price':
                fjo[typelist[j]] = int(ufetchall[i][j])
                continue
            # if typelist[j] ==u'封边留空1'.encode('gbk'):
            #     print '66666666666666',ufetchall[i][j]
            #     if isinstance(ufetchall[i][j], unicode):
            #         print '9999999'
            if isinstance(ufetchall[i][j], str):
                fjo[typelist[j]] = ufetchall[i][j].encode('gbk')

            elif ufetchall[i][j] is None:
                fjo[typelist[j]] = ''
            else:
                fjo[typelist[j]] = ufetchall[i][j]
            # if typelist[j] ==u'封边留空1'.encode('gbk'):
            #     print '66666666666666',ufetchall[i][j]
            #     if isinstance(fjo[typelist[j]], unicode):
            #         print '9999999'
    return fjo

def InitData(Path):
    global RootPath
    RootPath = Path
    gBGHash = InitBGHash()   #根目录 BaseGraph 文件夹
    gPluginsList = InitPluginsList() #Plugins 文件夹
    seqInfoHash, classseqInfoHash, workflowlist,gROC = InitBomHash() #data.mdb
    gBoardMatList = InitBoardMatList()  #XScriptDb.mdb
    gErpItemList = InitErpList()  #erp.mdb and snimay.mdb
    #ptableList = InitptableList()

    #mIIHoleCalcRule, mDoorPrecision, mJoBarCode= producemJoBarCode() #qd.conf
    return gBGHash,gPluginsList,seqInfoHash, classseqInfoHash, workflowlist, gBoardMatList, gErpItemList, gROC

if __name__ == '__main__':
    #base_dir = os.path.abspath(os.path.join(os.getcwd(),'../..'))
    print('base_dir=',base_dir)
    gBGHash, gPluginsList, seqInfoHash, classseqInfoHash, \
    workflowlist, gBoardMatList, gErpItemList, mIIHoleCalcRule,mDoorPrecision, gROC,mJoBarCode = InitData()
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
    import time
    time.sleep(10)