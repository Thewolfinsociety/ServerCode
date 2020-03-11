# -*- coding: UTF-8 -*-
'''
用获取的#order 内容得到订单、场景、产品
'''

from xml.dom.minidom import parse
import xml.dom.minidom
import json
# 使用minidom解析器打开 XML 文档
#订单类
class Returnorder(object):
    def __init__(self,xmlfile):
        # from xml.dom.minidom import parse
        # import xml.dom.minidom
        DOMTree = xml.dom.minidom.parse(xmlfile)
        collection = DOMTree.documentElement
        self.gQDDataID = collection.getAttribute('DATAID')
        self.gQDSoftVer = collection.getAttribute("QD版本")
        self.gQDDataVer = collection.getAttribute("版本")
        self.mOrderName = collection.getAttribute("订单名称")
        self.mDistributor = collection.getAttribute("经销商")
        self.mAddress = collection.getAttribute("地址")
        self.mPhone = collection.getAttribute("电话")
        self.mFax = collection.getAttribute("传真")
        self.mMemo = collection.getAttribute("备注")
        self.mDateTime = str(int(float(collection.getAttribute("订单日期"))))
        self.mCustomerName = collection.getAttribute("客户姓名")
        self.mCustomerCellPhone = collection.getAttribute("客户手机")
        self.mCustomerPhone = collection.getAttribute("客户电话")
        self.mCustomerAddress = collection.getAttribute("客户地址")
        self.mExtra = collection.getAttribute("DBCC")
        self.mDBCC = collection.getAttribute("Extra")

    def getorderinfo(self):
        xml_order = {}
        xml_order['order'] = ('<订单 DATAID="{v1}" QD版本="{v2}" 版本="{v3}" 订单名称="{v4}" 经销商="{v5}" 地址="{v6}" '
                            '电话="{v7}" 传真="{v8}" 备注="{v9}" 订单日期="{v10}" 客户姓名="{v11}" 客户手机="{v12}" '
                            '客户电话="{v13}" 客户地址="{v14}" Extra="{v15}" DBCC="{v16}">'
            .format(
            v1=self.gQDDataID ,
            v2=self.gQDSoftVer,
            v3=self.gQDDataVer,
            v4 =self.mOrderName,
            v5 =self.mDistributor,
            v6 =self.mAddress,
            v7 =self.mPhone,
            v8 =self.mFax,
            v9 =self.mMemo,
            v10 =self.mDateTime,
            v11 = self.mCustomerName,
            v12 =self.mCustomerCellPhone,
            v13 =self.mCustomerPhone,
            v14 =self.mCustomerAddress,
            v15 = self.mExtra,
            v16=self.mDBCC
        ))
        return xml_order
#场景类
class Returnscene(object):
    def __init__(self,xmlfile):
        DOMTree = xml.dom.minidom.parse(xmlfile)
        collection = DOMTree.documentElement
        scenes = collection.getElementsByTagName("场景")
        for scene in scenes:
            self.sname = scene.getAttribute("名称")
            self.sdes = scene.getAttribute("描述")
            # order_scene["DBCC"] = scene.getAttribute("DBCC")
            self.sdbid = scene.getAttribute("DBID")

    def getsceneinfo(self):
        xml_scene = {}
        xml_scene['scene']=('<场景 名称="%s" 描述="%s" DBID="%s">' % (
            self.sname,
            self.sdes,
            self.sdbid
        ))
        return xml_scene
#产品类
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
        scenes = collection.getElementsByTagName("场景")
        xml_product = {}
        for scene in scenes:
            products = scene.getElementsByTagName('产品')
            order_product = {}
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
#初始化函数返回JSON 字符串
def callxml(xmlfile):
    xml={}
    order_class=Returnorder(xmlfile)
    scene_class=Returnscene(xmlfile)
    product_class=Returnproduct()
    order=order_class.getorderinfo()
    scene=scene_class.getsceneinfo()
    product=product_class.getproductdict(xmlfile)
    xml['order']=order['order']
    xml['scene']=scene['scene']
    xml['product']=product['product']
    return json.dumps(xml,ensure_ascii=False), order_class

# t=callxml('processhelp.xml')
# print len(json.loads(t))