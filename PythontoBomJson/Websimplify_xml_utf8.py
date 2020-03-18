#  -*- coding:utf-8 -*-

'''

目标:通过dll操作xml文件。

思路:

参加接口getorderinfor

'''

'''

vesion:2.5

time:20190524

author:litao

'''

from ctypes import *

import json,os,sys,re,zipfile,chardet

from . import xml_dom_operate as productxmlprocess

from xml.dom.minidom import parse

import xml.dom.minidom

import xml.etree.ElementTree as ET

import shutil

#Dllbase_dir = os.path.abspath(os.path.j



# oin(os.getcwd(), ".."))

Dllbase_dir =  os.getcwd()
DLLPATH = Dllbase_dir +'\\QdLibdb.dll'
Path=os.path.abspath(os.path.join(os.getcwd()))+'\\Python'
ordfilepath=Path+'\\comordfile\\'

xmlfilepath=Dllbase_dir+'\\Temp\\'

Mapfilepath=Path+'\\Mapfile\\'

def del_file(path):

	ls = os.listdir(path)

	for i in ls:

		c_path = os.path.join(path, i)

		#print 'test:',c_path

		if os.path.isdir(c_path):

			del_file(c_path)

		else:

			os.remove(c_path)



def zip_files(files, zip_name):

    zip = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_STORED)

    for file in files:

        print(('compressing', file))

        filefullpath = os.path.join(BomBoardDataPath, file)

        zip.write(filefullpath, file)

    zip.close()

    print ('compressing finished')



def zip_ya(startdir,file_news):



    z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名

    for dirpath, dirnames, filenames in os.walk(startdir):

        fpath = dirpath.replace(startdir,'') #这一句很重要，不replace的话，就从根目录开始复制

        fpath = fpath and fpath + os.sep or ''#这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩

        for filename in filenames:

            z.write(os.path.join(dirpath, filename),fpath+filename)

            print ('压缩成功')

    z.close()



def ReturnDict(readord,mDB,len1,pKey):

    s = {}

    DB_SET = 27



    for i in range(0,len(pKey)):

        p = create_string_buffer(10240000)

        readord.DB_GetData(mDB,c_char_p(pKey[i]),pointer(p),id(len1),DB_SET)

        ret = readord.DB_GetData(mDB,c_char_p(pKey[i]),pointer(p),id(len1),DB_SET)

        m=(p.value).decode('gbk').encode('utf8')

        s[pKey[i]]=m

        p = None

    # print 's=',s['#order'].decode('utf8')

    # exit(1)

    return s



class Returnproduct(object):

    def __init__(self):

        self.mType=''

        self.mID=''

        self.mIDStr=''

        self.mDBID=''

        self.mName=''

        self.mDes=''

        self.mCB=''

        self.mX=''

        self.mY=''

        self.mZ=''

        self.mL=''

        self.mD=''

        self.mH=''

        self.mOX=''

        self.mOY=''

        self.mOZ=''

        self.mMinL=''

        self.mMinD=''

        self.mMinH=''

        self.mMaxL=''

        self.mMaxD=''

        self.mMaxH=''

        self.mIsRoomSpace=''

        self.mTextureClass=''

        self.mMat=''

        self.mColor=''

        self.XID=''

    def getproductdict(self,xmlfile):

        DOMTree = xml.dom.minidom.parse(xmlfile)

        collection = DOMTree.documentElement



        xml_product = {}

        order_product = {}



        products = collection.getElementsByTagName('产品'.decode('utf8'))



        for product in products:

            product_list = []

            self.mType = '产品'

            self.mID = product.getAttribute('ID'.decode('utf8'))

            self.mIDStr = product.getAttribute('IDSTR'.decode('utf8'))

            self.mDBID = product.getAttribute('DBID'.decode('utf8'))

            self.mName= product.getAttribute('名称'.decode('utf8'))

            self.mDes = product.getAttribute('描述'.decode('utf8'))

            self.mCB = product.getAttribute('CB'.decode('utf8'))

            self.mX = product.getAttribute('X'.decode('utf8'))

            self.mY = product.getAttribute('Y'.decode('utf8'))

            self.mZ = product.getAttribute('Z'.decode('utf8'))

            self.mL= product.getAttribute('宽'.decode('utf8'))

            self.mD = product.getAttribute('深'.decode('utf8'))

            self.mH = product.getAttribute('高'.decode('utf8'))

            self.mOX = product.getAttribute('OX'.decode('utf8'))

            self.mOY = product.getAttribute('OY'.decode('utf8'))

            self.mOZ = product.getAttribute('OZ'.decode('utf8'))

            self.mMinL= product.getAttribute('LMIN'.decode('utf8'))

            self.mMinD = product.getAttribute('DMIN'.decode('utf8'))

            self.mMinH= product.getAttribute('HMIN'.decode('utf8'))

            self.mMaxL= product.getAttribute('LMAX'.decode('utf8'))

            self.mMaxD = product.getAttribute('DMAX'.decode('utf8'))

            self.mMaxH= product.getAttribute('HMAX'.decode('utf8'))

            self.mIsRoomSpace = product.getAttribute('IsRoomSpace'.decode('utf8'))

            self.mTextureClass = product.getAttribute('装饰类别'.decode('utf8'))

            self.mMat = product.getAttribute('材料'.decode('utf8'))

            self.mColor = product.getAttribute('颜色'.decode('utf8'))

            self.XID= product.getAttribute('XID'.decode('utf8'))



            product_list.append('<%s ID="%s" IDSTR="%s" DBID="%s" 名称="%s" 描述="%s" '

                                'CB="%s" X="%s" Y="%s" Z="%s" 宽="%s" 深="%s" 高="%s" '

                                'OX="%s" OY="%s" OZ="%s" LMIN="%s" DMIN="%s" HMIN="%s" '

                                'LMAX="%s" DMAX="%s" HMAX="%s" IsRoomSpace="%s" 装饰类别="%s" '

                                '材料="%s" 颜色="%s" XID="%s" >' % (

                                    self.mType,

                                    self.mID.encode('utf8'),

                                    self.mIDStr.encode('utf8'),

                                    self.mDBID.encode('utf8'),

                                    self.mName.encode('utf8'),

                                    self.mDes.encode('utf8'),

                                    self.mCB.encode('utf8'),

                                    self.mX.encode('utf8'),

                                    self.mY.encode('utf8'),

                                    self.mZ.encode('utf8'),

                                    self.mL.encode('utf8'),

                                    self.mD.encode('utf8'),

                                    self.mH.encode('utf8'),

                                    self.mOX.encode('utf8'),

                                    self.mOY.encode('utf8'),

                                    self.mOZ.encode('utf8'),

                                    self.mMinL.encode('utf8'),

                                    self.mMinD.encode('utf8'),

                                    self.mMinH.encode('utf8'),

                                    self.mMaxL.encode('utf8'),

                                    self.mMaxD.encode('utf8'),

                                    self.mMaxH.encode('utf8'),

                                    self.mIsRoomSpace.encode('utf8'),

                                    self.mTextureClass.encode('utf8'),

                                    self.mMat.encode('utf8'),

                                    self.mColor.encode('utf8'),

                                    self.XID.encode('utf8')

                                    ))

            order_product[self.mDBID.encode('utf8')] = product_list

            order_product[self.mDBID.encode('utf8')+'l'] = self.mL.encode('utf8')

            order_product[self.mDBID.encode('utf8')+'p'] = self.mD.encode('utf8')

            order_product[self.mDBID.encode('utf8')+'h'] = self.mH.encode('utf8')



        xml_product['product']=order_product

        return xml_product



def functionordtoxml(ordfile):



    Dllbase_dir =  os.getcwd()

    DLLPATH = Dllbase_dir + '\\QdLibdb.dll'



    #配置dll函数

    readord = cdll.LoadLibrary(DLLPATH)

    DB_Open =readord.DB_Open

    DB_Close = readord.DB_Close

    DB_Get =readord.DB_Get

    DB_Put = readord.DB_Put

    DB_GetFile =readord.DB_GetFile

    DB_PutFile = readord.DB_PutFile

    DB_Move =readord.DB_Move

    DB_Del = readord.DB_Del

    DB_DelKey = readord.DB_DelKey

    DB_GetData =readord.DB_GetData

    DB_PutData =readord.DB_PutData

    #ord文件路径

    print('ordfilepath=',ordfilepath)

    filepath=ordfilepath+ordfile#K1000034010102180318000.ord

    mDB = DB_Open(c_char_p(filepath), 1)

    mbuflen=10240000



    len1=c_int(mbuflen)

    DB_SET = 27

    # mKeyBuf= create_string_buffer(1000)

    DB_FIRST = 7

    DB_NEXT = 16



    s={}  #装载ord文件内容

    #del_file(Mapfilepath) #删除Mapfile文件夹下文件

    pKey = ['#order','#order_scene0','#order_scene0_room0']

    s = ReturnDict(readord,mDB,len1,pKey)

    #print s['#order_scene0'].decode('utf8').encode('gb2312')

    orderxmlFile = Path+'\\order.xml'

    print('orderxmlFile=', orderxmlFile)

    with open(orderxmlFile, 'w+') as f:

        f.write(s['#order'])

    #print s['#order'].decode('utf8')

    root = ET.fromstring(s['#order'])

    arr = root.attrib

    scenexmlfile = Path+'\\scene.xml'

    with open(scenexmlfile, 'w+') as f:

        f.write(s['#order_scene0'])

    #print 'order_scene0',s['#order_scene0']

    #解析场景xml

    DOMTree = xml.dom.minidom.parse(scenexmlfile)

    collection = DOMTree.documentElement

    products = collection.getElementsByTagName("产品")

    productList = []

    productgno = []

    #柜子信息

    listInfos = []

    for product in products:

        DBIDContent = product.getAttribute("DBID")

        name = product.getAttribute("名称")

        productgno.append(name)

        if DBIDContent != '':

            productList.append(DBIDContent)

        dictAttr = {}

        for key in list(product.attributes.keys()):  # child.attrbutes.keys()查看所有属性，返回一个列表

            attr = product.attributes[key]  # 返回属性地址

            dictAttr[attr.name] = attr.value  # attr.name为属性名  attr.value为属性值

        listInfos.append(dictAttr)

    # print json.dumps(listInfos,ensure_ascii=False)



    prodcutXml = ReturnDict(readord, mDB, len1, productList) #dict key: key ,value:xml



    product_class = Returnproduct()

    product = product_class.getproductdict(scenexmlfile) #dict key:key ,value :产品前面的xml

    finalxmlfile = re.findall(r'(.+?)\.', ordfile).pop()

    #'xml3.xml'用于合成最终的xml文件

    print('xmlfile=',xmlfilepath+finalxmlfile)

    DBIDlist = []

    with open(xmlfilepath+finalxmlfile, 'wb') as f:

        #第一步

        f.write('<?xml version="1.0" encoding="utf-8"?>'+'\n')

        #第二步

        xmltext, orderdict = productxmlprocess.callxml(orderxmlFile)

        xml1=json.loads(xmltext)

        f.write(xml1['order'].encode('utf8')+'\n')    #加载订单

        f.write(xml1['scene'].encode('utf8')+'\n')    #加载场景

        f.write(s["#order_scene0_room0"]+'\n') #加载房型

        for i in productList:

            f.write(product['product'][i][0] + '\n')

            # print 'i=',len(productList)

            f.write(prodcutXml[i])

            #print prodcutXml[i].decode('utf8')

            root = ET.fromstring(prodcutXml[i])

            DBIDdict = {}

            DBIDdict['DBID'] = i

            DBIDdict['材料'] = root.get('材料')

            DBIDdict['颜色'] = root.get('颜色')

            DBIDlist.append(DBIDdict)

            f.write('</产品>' + '\n')

        f.write('</场景></订单>')



    DB_Close(mDB)

    for info in listInfos:

        for DBID in DBIDlist:

            if info['DBID']==DBID['DBID']:

                info['材料'] =  DBID['材料']

                info['颜色'] = DBID['颜色']



    os.remove(orderxmlFile)

    os.remove(scenexmlfile)

    #orddictAttr:订单属性，productgno产品名称，listInfos产品信息，orderdict订单字典

    return orderdict,productgno,listInfos,arr





def getorderinfor(ordfile):

    #def otherord():

    Dllbase_dir =  os.getcwd()

    #print 'Dllbase_dir=',Dllbase_dir

    DLLPATH = Dllbase_dir + '\\QdLibdb.dll'

    #配置dll函数

    readord = cdll.LoadLibrary(DLLPATH)

    DB_Open =readord.DB_Open

    DB_Close = readord.DB_Close



    filepath = ordfile

    #print 'filepath=', filepath

    mDB = DB_Open(c_char_p(filepath), 1)

    mbuflen=1024000

    p= create_string_buffer(10240000)

    len1=c_int(mbuflen)

    DB_SET = 27

    mKeyBuf= create_string_buffer(1000)

    DB_FIRST = 7

    DB_NEXT = 16

    s={}  #装载ord文件内容

    pKey = ['#order','#order_scene0','#order_scene0_room0']

    s = ReturnDict(mDB,p,len1,pKey)

    p = None

    mKeyBuf = None

    #print s['#order_scene0'].decode('utf8').encode('gb2312')

    # orderxmlFile = Path+'\\order.xml'

    # with open(orderxmlFile, 'w+') as f:

    #     f.write(s['#order'])

    # xmltext, orderdict = productxmlprocess.callxml(orderxmlFile)

    # xml1 = json.loads(xmltext)

    #print xml1['order']

    DB_Close(mDB)

    #print s['#order'].decode('utf8').encode('gbk')

    return s['#order'].decode('utf8').encode('gbk')

#functionordtoxml('4a7c9161a22811e9a92fb0fc36268ae0.ord')



#getorderinfor(u'D:\Python设计软件环境\Orders\\11.ord')