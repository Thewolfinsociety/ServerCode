#  -*- coding:utf8 -*-
'''
目标:通过dll操作xml文件。
思路:
参加接口getorderinfor
20191120 增加接口 getxml, 生成需要的订单xml
20191122 修改接口 getxml, 生成需要的订单xml
'''
'''
vesion:2.51
time:20191122
author:litao
'''
from ctypes import *
import json,os,sys,re,zipfile,chardet
import xml_dom_operate as productxmlprocess
from xml.dom.minidom import parse
import xml.dom.minidom
import xml.etree.ElementTree as ET
import logging
log = logging.getLogger(__name__)
Dllbase_dir = os.getcwd()
DLLPATH = Dllbase_dir +'\\QdLibdb.dll'
Path=os.path.abspath(os.path.join(os.getcwd()))+'\\Python'
ordfilepath= Path+'\\comordfile\\'
xmlfilepath=Dllbase_dir+'\\Temp\\'
Mapfilepath=Path+'\\Mapfile\\'

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

mBufLen=c_int(1024000)
dlen = c_int(1024000)
DB_SET = 27

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
def ReAllocBuf(n):
    log.debug('n.value='+str(n.value))
    t = n.value // 1024000
    if t <= 0 : t = 1
    else: t = t + 1
    log.debug('t='+str(t))
    mBufLen = c_int(1024*1000 * t)
    return mBufLen
all = 0
def ReturnDict0(mDB, p, pKey):
    global all
    s = {}
    result = -1
    print('all=',all)
    for i in range(0,len(pKey)):
        result = readord.DB_GetData(mDB,c_char_p(pKey[i]),pointer(p),id(dlen),DB_SET)
        print('result1=',result)
        m = (p.value).decode('gbk')
        print(m)
        if dlen >= mBufLen:

            result = readord.DB_Get(mDB,c_char_p(pKey[i]),pointer(p), dlen, DB_SET)
            print('result2=', result)
        if result == 0:
            m=(p.value).decode('gbk')
            all = all + len(m)
            s[pKey[i]]=m
    print('all1=', all)
    return s

def ReturnDict1(mDB, pKey):
    global all
    s = {}
    result = -1
    p = create_string_buffer(dlen.value)
    for i in range(0,len(pKey)):
        result = readord.DB_GetData(mDB,c_char_p(pKey[i]),pointer(p),id(dlen),DB_SET)
        if dlen >= mBufLen:
            result = readord.DB_Get(mDB,c_char_p(pKey[i]),pointer(p), dlen, DB_SET)
        if result == 0:
            m = (p.value).decode('gbk')
            s[pKey[i]] = m
    return s

def ReturnDict(mDB, pKey):
    s = {}
    for i in range(0,len(pKey)):
        result = -1
        mBufLen = c_int(1024000)
        dlen = mBufLen
        p = create_string_buffer(dlen.value)
        result = readord.DB_GetData(mDB,c_char_p(pKey[i].encode('gbk')),pointer(p),pointer(dlen),DB_SET)
        if dlen.value >= mBufLen.value:
            dlen = ReAllocBuf(dlen)
            p = create_string_buffer(dlen.value)
            result = readord.DB_Get(mDB,c_char_p(pKey[i].encode('gbk')),pointer(p),dlen,DB_SET)
        if result == 0:
            m=(p.value).decode('gbk')
            s[pKey[i]]=m
        p = None
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

        products = collection.getElementsByTagName('产品')

        for product in products:
            product_list = []
            self.mType = '产品'
            self.mID = product.getAttribute('ID')
            self.mIDStr = product.getAttribute('IDSTR')
            self.mDBID = product.getAttribute('DBID')
            self.mName= product.getAttribute('名称')
            self.mDes = product.getAttribute('描述')
            self.mCB = product.getAttribute('CB')
            self.mX = product.getAttribute('X')
            self.mY = product.getAttribute('Y')
            self.mZ = product.getAttribute('Z')
            self.mL= product.getAttribute('宽')
            self.mD = product.getAttribute('深')
            self.mH = product.getAttribute('高')
            self.mOX = product.getAttribute('OX')
            self.mOY = product.getAttribute('OY')
            self.mOZ = product.getAttribute('OZ')
            self.mMinL= product.getAttribute('LMIN')
            self.mMinD = product.getAttribute('DMIN')
            self.mMinH= product.getAttribute('HMIN')
            self.mMaxL= product.getAttribute('LMAX')
            self.mMaxD = product.getAttribute('DMAX')
            self.mMaxH= product.getAttribute('HMAX')
            self.mIsRoomSpace = product.getAttribute('IsRoomSpace')
            self.mTextureClass = product.getAttribute('装饰类别')
            self.mMat = product.getAttribute('材料')
            self.mColor = product.getAttribute('颜色')
            self.XID= product.getAttribute('XID')

            product_list.append('<%s ID="%s" IDSTR="%s" DBID="%s" 名称="%s" 描述="%s" '
                                'CB="%s" X="%s" Y="%s" Z="%s" 宽="%s" 深="%s" 高="%s" '
                                'OX="%s" OY="%s" OZ="%s" LMIN="%s" DMIN="%s" HMIN="%s" '
                                'LMAX="%s" DMAX="%s" HMAX="%s" IsRoomSpace="%s" 装饰类别="%s" '
                                '材料="%s" 颜色="%s" XID="%s" >' % (
                                    self.mType,
                                    self.mID,
                                    self.mIDStr,
                                    self.mDBID,
                                    self.mName,
                                    self.mDes,
                                    self.mCB,
                                    self.mX,
                                    self.mY,
                                    self.mZ,
                                    self.mL,
                                    self.mD,
                                    self.mH,
                                    self.mOX,
                                    self.mOY,
                                    self.mOZ,
                                    self.mMinL,
                                    self.mMinD,
                                    self.mMinH,
                                    self.mMaxL,
                                    self.mMaxD,
                                    self.mMaxH,
                                    self.mIsRoomSpace,
                                    self.mTextureClass,
                                    self.mMat,
                                    self.mColor,
                                    self.XID
                                    ))
            order_product[self.mDBID] = product_list
            order_product[self.mDBID+'l'] = self.mL
            order_product[self.mDBID+'p'] = self.mD
            order_product[self.mDBID+'h'] = self.mH

        xml_product['product']=order_product
        return xml_product

def functionordtoxml(ordfile):
    print('ordfilepath=',ordfilepath)
    filepath=ordfilepath + ordfile #K1000034010102180318000.ord
    mDB = DB_Open(c_char_p(filepath), 1)
    s={}  #装载ord文件内容
    #del_file(Mapfilepath) #删除Mapfile文件夹下文件
    pKey = ['#order','#order_scene0','#order_scene0_room0']
    s = ReturnDict(mDB, pKey)
    #print s['#order_scene0'].encode('gb2312')
    orderxmlFile = Path+'\\order.xml'
    with open(orderxmlFile, 'w+') as f:
        f.write(s['#order'])
    DOMTree = xml.dom.minidom.parse(orderxmlFile)
    collection = DOMTree.documentElement
    orddictAttr = {}  #订单信息
    for key in list(collection.attributes.keys()):  # child.attrbutes.keys()查看所有属性，返回一个列表
        attr = collection.attributes[key]  # 返回属性地址
        orddictAttr[attr.name] = attr.value  # attr.name为属性名  attr.value为属性值

    #print 'orddictAttr',json.dumps(orddictAttr, ensure_ascii=False)
    scenexmlfile = Path+'\\scene.xml'
    with open(scenexmlfile, 'w+') as f:
        f.write(s['#order_scene0'])
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
        if DBIDContent != '': productList.append(DBIDContent)
        dictAttr = {}
        for key in list(product.attributes.keys()):  # child.attrbutes.keys()查看所有属性，返回一个列表
            attr = product.attributes[key]  # 返回属性地址
            dictAttr[attr.name] = attr.value  # attr.name为属性名  attr.value为属性值
        listInfos.append(dictAttr)
    # print json.dumps(listInfos,ensure_ascii=False)
    log.debug(json.dumps(productList,ensure_ascii=False))
    prodcutXml = ReturnDict(mDB, productList) #dict key: 产品DBID字段 ,value:产品 xml
    DB_Close(mDB)
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
        f.write(xml1['order']+'\n')    #加载订单
        f.write(xml1['scene']+'\n')    #加载场景
        f.write(s["#order_scene0_room0"]+'\n') #加载房型
        for i in productList:
            f.write(product['product'][i][0] + '\n')
            f.write(prodcutXml[i])
            root = ET.fromstring(prodcutXml[i])
            DBIDdict = {}
            DBIDdict['DBID'] = i
            DBIDdict['材料'] = root.get('材料')
            DBIDdict['颜色'] = root.get('颜色')
            DBIDlist.append(DBIDdict)
            f.write('</产品>' + '\n')
        f.write('</场景></订单>')


    for info in listInfos:
        for DBID in DBIDlist:
            if info['DBID']==DBID['DBID']:
                info['材料'] =  DBID['材料']
                info['颜色'] = DBID['颜色']
    os.remove(orderxmlFile)
    os.remove(scenexmlfile)
    #orddictAttr:订单属性，productgno产品名称，listInfos产品信息，orderdict订单字典
    return orderdict,productgno,listInfos,orddictAttr

def getorderinfor(ordfile):
    filepath = ordfile
    mDB = DB_Open(c_char_p(filepath), 1)
    pKey = ['#order','#order_scene0','#order_scene0_room0']
    s = ReturnDict(mDB, pKey)
    DB_Close(mDB)

    return s['#order'].encode('gbk')

def indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def getxml(ordfile):
    log.info('ordfile='+ordfile)
    mDB = DB_Open(c_char_p(ordfile.encode('gbk')), 1)
    print (mDB)
    pKey = ['#order']#['#order']
    AllOrdInfo = ReturnDict(mDB, pKey)

    if ('#order' not in AllOrdInfo): #or ('#order_scene0' not in AllOrdInfo):
        log.error('Cal error')
        DB_Close(mDB)
        return ''

    log.debug(AllOrdInfo['#order'])
    root = ET.fromstring(AllOrdInfo['#order'])
    log.debug(root.tag)
    ordername = root.get('订单名称','')
    log.debug('订单名:'+ordername)
    if (ordername !='') and (len(ordername) >= 4):
        ordernamefront4 = ordername[:4]
    else:
        ordernamefront4 = ''
    customphone = root.get('客户手机','')
    customname = root.get('客户姓名', '')
    customtel = root.get('客户电话', '')
    customaddress = root.get('客户地址', '')
    scenedbid = '#order_scene0'
    for i in range(0, len(root)):
        scenenode = root[i]
        if scenenode.tag == '场景':
            scenedbid = root.get('DBID','#order_scene0')

    log.debug(root.tag)
    rootnode = ET.Element('root')
    node_name = ET.SubElement(rootnode, 'rm_0')
    nodeid = ET.SubElement(node_name, 'id')
    nodeid.text = ordername   #
    nodecustomid = ET.SubElement(node_name, 'customid')
    nodecustomid.text = ordernamefront4   #
    nodeid = ET.SubElement(node_name, 'convey_date')   #默认空
    nodeid.text = ''
    nodeid = ET.SubElement(node_name, 'statu_s')    #默认1
    nodeid.text = '1'
    nodeid = ET.SubElement(node_name, 'custom_phone')
    nodeid.text = customphone
    nodeid = ET.SubElement(node_name, 'custom_name')
    nodeid.text = customname
    nodeid = ET.SubElement(node_name, 'custom_tel')
    nodeid.text = customtel
    nodeid = ET.SubElement(node_name, 'Installation_address')
    nodeid.text = customaddress
    log.debug(scenedbid)
    itemlistnode = ET.SubElement(node_name, 'itemlist')
    itemid = 0
    pKey = [scenedbid]

    AllOrdInfo = ReturnDict(mDB, pKey)

    DB_Close(mDB)
    if (scenedbid not in AllOrdInfo):  # or ('#order_scene0' not in AllOrdInfo):
        log.error('Cal error')
        return ''
    sceneroot = ET.fromstring(AllOrdInfo[scenedbid])
    for j in range(0, len(sceneroot)):
        node = sceneroot[j]
        if node.tag != '产品': continue
        log.debug(node.tag)
        name = node.get('描述', '')
        color = node.get('颜色', '')
        productid = node.get('名称', '')
        item = ET.SubElement(itemlistnode, 'item_' + str(itemid))
        itemid = itemid + 1
        item_namenode = ET.SubElement(item, 'name')
        item_namenode.text = name
        item_colornode = ET.SubElement(item, 'color')
        item_colornode.text = color
        item_pnumbernode = ET.SubElement(item, 'pnumber')
        item_pnumbernode.text = productid
        item_area_5mm_node = ET.SubElement(item, 'area_5mm')
        item_area_5mm_node.text = '0'
        item_area_18mm_node = ET.SubElement(item, 'area_18mm')
        item_area_18mm_node.text = '0'
        item_area_25mm_node = ET.SubElement(item, 'area_25mm')
        item_area_25mm_node.text = '0'
        item_area_move_node = ET.SubElement(item, 'area_move')
        item_area_move_node.text = '0'

    indent(rootnode)
    rough_string = ET.tostring(rootnode, 'utf-8', "html")  # 输出xml到out_files
    Result = '<?xml version="1.0" encoding="utf-8"?>'+'\n'+rough_string

    return Result

def OrdToXmlString(ordfile):
    pass
if __name__ == '__main__':
    import logging
    Dllbase_dir = os.getcwd()
    logging.basicConfig(level="DEBUG")
    log = logging.getLogger(__name__)
    log.setLevel('DEBUG')
    log.debug('Dllbase_dir='+Dllbase_dir)
    templatefile = Dllbase_dir+'\\Orders\\1122.ord'
    ORDFILE = 'K10006510266190520003.ord'
    print(getxml(templatefile))
    #functionordtoxml(ORDFILE)
    # for i in range(100):
    #     functionordtoxml(ORDFILE)
    #     print getxml(templatefile)
        #print getorderinfor(templatefile).decode('gbk')