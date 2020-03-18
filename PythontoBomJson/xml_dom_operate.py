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
        self.gQDDataID = collection.getAttribute('DATAID'.decode('utf8'))
        self.gQDSoftVer = collection.getAttribute("QD版本".decode('utf8'))
        self.gQDDataVer = collection.getAttribute("版本".decode('utf8'))
        self.mOrderName = collection.getAttribute("订单名称".decode('utf8'))
        self.mDistributor = collection.getAttribute("经销商".decode('utf8'))
        self.mAddress = collection.getAttribute("地址".decode('utf8'))
        self.mPhone = collection.getAttribute("电话".decode('utf8'))
        self.mFax = collection.getAttribute("传真".decode('utf8'))
        self.mMemo = collection.getAttribute("备注".decode('utf8'))
        self.mDateTime = str(int(float(collection.getAttribute("订单日期".decode('utf8')))))
        self.mCustomerName = collection.getAttribute("客户姓名".decode('utf8'))
        self.mCustomerCellPhone = collection.getAttribute("客户手机".decode('utf8'))
        self.mCustomerPhone = collection.getAttribute("客户电话".decode('utf8'))
        self.mCustomerAddress = collection.getAttribute("客户地址".decode('utf8'))
        self.mExtra = collection.getAttribute("DBCC".decode('utf8'))
        self.mDBCC = collection.getAttribute("Extra".decode('utf8'))

    def getorderinfo(self):
        xml_order = {}
        xml_order['order'] = ('<订单 DATAID="{v1}" QD版本="{v2}" 版本="{v3}" 订单名称="{v4}" 经销商="{v5}" 地址="{v6}" '
                            '电话="{v7}" 传真="{v8}" 备注="{v9}" 订单日期="{v10}" 客户姓名="{v11}" 客户手机="{v12}" '
                            '客户电话="{v13}" 客户地址="{v14}" Extra="{v15}" DBCC="{v16}">'
            .format(
            v1=self.gQDDataID.encode('utf8') ,
            v2=self.gQDSoftVer.encode('utf8'),
            v3=self.gQDDataVer.encode('utf8'),
            v4 =self.mOrderName.encode('utf8'),
            v5 =self.mDistributor.encode('utf8'),
            v6 =self.mAddress.encode('utf8'),
            v7 =self.mPhone.encode('utf8'),
            v8 =self.mFax.encode('utf8'),
            v9 =self.mMemo.encode('utf8'),
            v10 =self.mDateTime.encode('utf8'),
            v11 = self.mCustomerName.encode('utf8'),
            v12 =self.mCustomerCellPhone.encode('utf8'),
            v13 =self.mCustomerPhone.encode('utf8'),
            v14 =self.mCustomerAddress.encode('utf8'),
            v15 = self.mExtra.encode('utf8'),
            v16=self.mDBCC.encode('utf8')
        ))
        return xml_order
#场景类
class Returnscene(object):
    def __init__(self,xmlfile):
        DOMTree = xml.dom.minidom.parse(xmlfile)
        collection = DOMTree.documentElement
        scenes = collection.getElementsByTagName("场景".decode('utf8'))
        for scene in scenes:
            self.sname = scene.getAttribute("名称".decode('utf8'))
            self.sdes = scene.getAttribute("描述".decode('utf8'))
            # order_scene["DBCC".decode('utf8')] = scene.getAttribute("DBCC".decode('utf8'))
            self.sdbid = scene.getAttribute("DBID".decode('utf8'))

    def getsceneinfo(self):
        xml_scene = {}
        xml_scene['scene']=('<场景 名称="%s" 描述="%s" DBID="%s">' % (
            self.sname.encode('utf8'),
            self.sdes.encode('utf8'),
            self.sdbid.encode('utf8')
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
        scenes = collection.getElementsByTagName("场景".decode('utf8'))
        xml_product = {}
        for scene in scenes:
            products = scene.getElementsByTagName('产品'.decode('utf8'))
            order_product = {}
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
    return json.dumps(xml,encoding='utf-8',ensure_ascii=False),order_class

# t=callxml('processhelp.xml')
# print len(json.loads(t))