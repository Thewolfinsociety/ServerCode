#  -*- coding:utf-8 -*-
'''
vesion 0.0.1
2019/10/29
author:litao
'''
from useful_tools import *
from VectorGeometry import *
from xmltojsonpackage import *
from numpy import *
import logging
log = logging.getLogger(base_dir+"\\Python\\Log\\all.log")
def GetWorkflowStr(workflow, bomstd, hole, workflowlist):
    Result = ''
    for i in range(0,len(workflowlist)):
        pwf = workflowlist[i]
        if (pwf.name == workflow) and ((pwf.bomstd == '*') or (pwf.bomstd == bomstd)) and (
            (pwf.hole == '*') or (pwf.hole == hole)) :
            Result = Result + '%d,%d,%d,%d'%(pwf.id, pwf.board_cut, pwf.edge_banding, pwf.punching)
    return Result
def GetXptlist(poi,xptlist_isxx, xptlist_jx, xptlist_pl,gBGHash):
    # gBGHash = InitBGHash()
    def_bgparam = '{^PL^:^0^,^Cut^:^0^,^DJ^:^0^,^JX^:^0^,^CutA^:^0.0000^,^CutB^:^0.0000^,^BarH^:^0.0000^,^Points^:^^}'
    xptlist_isxx= 0
    xptlist_jx= 0
    xptlist_pl= 1
    if 'bg' not in poi  or (poi['bg']) =='':
        return
    bgindex = poi['bg'].replace('::','_')
    ## bgindex.encode('gb2312'),type(bgindex)
    ## gBGHash.keys()
    # if bgindex in gBGHash.keys():#u'BG_RECT背板'
    #     # '9999999'
    #     # type(BGName(bgindex)),BGName(bgindex)
    ## gBGHash
    if bgindex.encode('gb2312') not in gBGHash:
        return
    xml = gBGHash[bgindex.encode('gb2312')]
    if xml=='' and (poi['bg']!='BG::RECT'):
        return
    if xml!='':
        root = ET.fromstring(xml)  # 解析那段xml
        paramstr=root.get('Param','')
        for i in range(0,len(root)):
            node=root[i]
            str_type = node.get('Type','')
            if (str_type=='Polygon') and (node.tag=='PlaneXY') :
                ## '888888'
                xptlist_pl=1
            if (str_type=='Polygon') and (node.tag=='PlaneXZ') :
                xptlist_pl=2
            if (str_type=='Polygon') and (node.tag=='PlaneYZ') :
                xptlist_pl=3
def GetWorldMatrix(p,m): #存在问题
    '''
    :param p:  bomlist的元素
    :param m:  TMyCalcItem对象的 TMatrix属性
    :return:
    '''
    global pm
    pm = np.matrix([[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]])
    def GetLocalMatrix():
        '''
        a=np.matrix('1 2 7;3 4 8;5 6 9')
        :return:  TMatrix
        '''
        rm=IdentityHmgMatrix
        ## 'p=',type(p)
        ## p['lx'],p['ly'],p['lz']
        tm=CreateTranslationMatrix([p['lx'],p['ly'],p['lz']])
        ## type(p['oz']),p['oz']
        if p['oz'] =='':
            oz = 0
        else:
            oz=float(p['oz'])
        if abs(oz) > 0.001:
            # print 'oz=',oz
            oz=-oz*pi/180
            if oz ==pi/2:
                oz = 1.5707963705
            # print 'oz=', oz
            rm = CreateRotationMatrixZ(oz)
            # print '6666rm=',rm
          
        if p['vp']==1 :# // 俯视
            m= CreateRotationMatrixX(DegToRad(90))
            rm= MatrixMultiply(rm, m)
            m = CreateTranslationMatrix(VectorMake(0, p['gh'], 0))
            tm= MatrixMultiply(tm, m)
        if p['vp']==2 :# // 左侧(B面)
            m= CreateRotationMatrixZ(DegToRad(-90))
            rm= MatrixMultiply(rm, m)
            m= CreateTranslationMatrix(VectorMake(0, p['gl'], 0))
            tm= MatrixMultiply(tm, m)
        if p['vp']==3:#// 右侧(C面)
            m= CreateRotationMatrixZ(DegToRad(90))
            rm= MatrixMultiply(rm, m)
            m= CreateTranslationMatrix(VectorMake(p['gl'], 0, 0))
            #print 'm3333=', m,'tm33333=',tm,'guid=',p['guid'],'name=',p['name']
            tm= MatrixMultiply(tm, m)
            # print '333333tm=',tm
        if p['vp']==4 :# // 仰视
            rm= CreateRotationMatrixX(DegToRad(-90))
            rm= MatrixMultiply(rm, m)
            m= CreateTranslationMatrix(VectorMake(0, 0, p['gh']))
            tm= MatrixMultiply(tm, m)
        if p['vp']==5 :# // 反向
            m= CreateRotationMatrixZ(DegToRad(180))
            rm= MatrixMultiply(rm, m)
            m= CreateTranslationMatrix(VectorMake(p['gl'], p['gp'], 0))
            tm= MatrixMultiply(tm, m)
        # print 'rm=',rm
        # print 'vp=',p['vp']
        # print 'tm=',tm
        Result = MatrixMultiply(rm, tm)
        return Result
    m=GetLocalMatrix()
    #print 'm=',m
    if p['parent'] ==None:
        return m
    pm = GetWorldMatrix(p['parent'],pm)
    #print 'pm=',pm
    m=MatrixMultiply(m, pm)
    #print 'm2=',m
    return m
def BomItem2CalcItem(p,Item2,workflowlist,mBDXMLList,gBGHash):
    item = p
    Result = Item2
    #if item['lx'] ==373:
        ## 'Item1=',Item2.m
    ## type(item)
    if type(item)=="<type 'str'>":
        ## 'hahhahaha'
        sys.exit(1)
    Item2.guid = item['guid']
    Item2.m =GetWorldMatrix(item, Item2.m)
    # if Item2.guid =='e6ab89deaa0911e9a8dcb0fc36268ae0':
    #     exit(1)
    #if item['lx'] == 373:
        ## 'Item2=',Item2.m
    Item2.space = ''
    Item2.space_x = 0
    Item2.space_y = 0
    Item2.space_z = 0
    GetXptlist(item, Item2.isxx, Item2.xptlist_jx, Item2.xptlist_pl,gBGHash)
    if 'tmp_soz' not in item:
        item['tmp_soz'] = ''
    if item['tmp_soz']=='':
        Item2.sozflag=''
    else:
        Item2.sozflag=md5(item['tmp_soz'])
    #GetSpaceItem(item, )
    Item2.space = item['subspace']
    Item2.space_x = item['space_x']
    Item2.space_y = item['space_y']
    Item2.space_z = item['space_z']
    Item2.bl = item['bl']
    Item2.bp = item['bp']
    Item2.bh = item['bh']
    Item2.pl = item['pl']
    Item2.pd = item['pd']
    Item2.ph = item['ph']
    Item2.lx = item['lx']
    Item2.ly = item['ly']
    Item2.lz = item['lz']
    Item2.x = item['x']- Item2.space_x
    Item2.y = item['y']- Item2.space_y
    Item2.z = item['z'] - Item2.space_z
    Item2.space_id = item['space_id']
    Item2.l = item['l']
    Item2.p = item['p']
    Item2.h = item['h']
    Item2.gl = item['gl']
    Item2.gp = item['gp']
    Item2.gh = item['gh']
    Item2.direct = item['direct']
    Item2.o_direct = item['direct']
    Item2.holeid = item['holeid']
    Item2.kcid = item['kcid']
    for i in range(0,101):
        if i <= 15:
            Item2.var_args[i]=item['var_args'][i]
        Item2.ahole_index[i]= item['ahole_index'][i]
        Item2.bhole_index[i]= item['bhole_index'][i]
        Item2.akc_index[i] = item['akc_index'][i]
        Item2.bkc_index[i] = item['bkc_index'][i]
        if i <= 5 :
            Item2.is_calc_holeconfig[i] = item['is_calc_holeconfig'][i]
        if i <= 5 :
            Item2.is_holeface_touch[i] = 0
    #// 基础图形描述
    Item2.bg_l_minx = item['bg_l_minx']
    Item2.bg_l_maxx = item['bg_l_maxx']
    Item2.bg_r_minx = item['bg_r_minx']
    Item2.bg_r_maxx = item['bg_r_maxx']
    Item2.bg_l_miny = item['bg_l_miny']
    Item2.bg_l_maxy = item['bg_l_maxy']
    Item2.bg_r_miny = item['bg_r_miny']
    Item2.bg_r_maxy = item['bg_r_maxy']
    Item2.bg_d_minx = item['bg_d_minx']
    Item2.bg_d_maxx = item['bg_d_maxx']
    Item2.bg_u_minx = item['bg_u_minx']
    Item2.bg_u_maxx = item['bg_u_maxx']
    Item2.bg_d_miny = item['bg_d_miny']
    Item2.bg_d_maxy = item['bg_d_maxy']
    Item2.bg_u_miny = item['bg_u_miny']
    Item2.bg_u_maxy = item['bg_u_maxy']
    Item2.bg_b_minx = item['bg_b_minx']
    Item2.bg_b_maxx = item['bg_b_maxx']
    Item2.bg_f_minx = item['bg_f_minx']
    Item2.bg_f_maxx = item['bg_f_maxx']
    Item2.bg_b_miny = item['bg_b_miny']
    Item2.bg_b_maxy = item['bg_b_maxy']
    Item2.bg_f_miny = item['bg_f_miny']
    Item2.bg_f_maxy = item['bg_f_maxy']
    Item2.hole_back_cap = item['hole_back_cap']
    Item2.hole_2_dist = item['hole_2_dist']
    Item2.zero_y = item['zero_y']
    Item2.bg = item['bg']
    Item2.mat = item['mat']
    Item2.name = item['name']
    Item2.color = item['color']
    Item2.bdxmlid = item['bdxmlid']
    Item2.holeconfig_flag = item['holeconfig_flag']
    Item2.kcconig_flag = item['kcconig_flag']
    Item2.devcode = item['devcode']
    Item2.data = p
    str1 = 'Workflow="%s" JXS="%s" TIME="%s" ORDER="%s" GNO="%s" DESNO="%s" CBNO="%s" USER="%s" TYPE="%s" NAME="%s" FBSTR="%s" SIZE="%s" UNIT="%s" PackNo="%s"'%(
        GetWorkflowStr(item['workflow'], item['bomstd'], '', workflowlist),
        'jinxiaoshan',#mDistributor,#经销商
        '2019-02-28',#'FormatDateTime('yyyy-mm-dd', mDateTime),
        '123',#'#mOrderName,
        item['gno'],
        item['gdes'],
        item['gcb'],
        'litao',#mUserName,
        item['myclass'],
        item['name'],
        item['fbstr'],
        '%d*%d*%d'%(round(float(item['bl'])), round(float(item['bp'])), round(float(item['bh']))),
        item['myunit'],
        item['packno'],)
    Item2.bdinfo='%s MEMO="%s" Mat="%s" Color="%s" HoleStr="%s" KcStr="%s" HoleFlag="%s" KcFlag="%s" BomStd="%s" JXSPHONE="%s" JXSADDR="%s" CLIENT="%s" CLIENTPHONE="%s" CLIENTMOBILEPHONE="%s" CLIENTADDR="%s"'%(
        str1,
        item['memo'],
        item['mat'],
        item['color'],
        item['holestr'],
        item['kcstr'],
        item['holeconfig_flag'],
        item['kcconig_flag'],
        item['bomstd'],
        '123',#'#mPhone,
        'dfdf',#'#mAddress,
        'name',#'#mCustomerName,
        '1232',#'#mCustomerPhone,
        '3434',#'#m#CustomerCellPhone,
        'dfdf')#'#mCustomerAddress)
    Item2.llfb = item['llfb']
    Item2.rrfb = item['rrfb']
    Item2.ddfb = item['ddfb']
    Item2.uufb = item['uufb']
    Item2.fb = item['fb']
    Item2.holeinfo = item['holeinfo']
    flag = 0
    bdxml = ''
    if Item2.bdxmlid != '':
        #print 'len of mBDXMLList',len(mBDXMLList),Item2.bdxmlid
        bdxml = mBDXMLList[Item2.bdxmlid]
        flag = 1
    if item['bg_filename'] != '' and os.path.exists(item['bg_filename']):
        with open(item['bg_filename']) as f:
            bdxml = f.read(item['bg_filename'])
            bdxml = ClearXMLDocTag(bdxml)
            flag = 2
    if bdxml == '':
        return Result
    mExp = {}
    mExp['L'] = Item2.gl
    mExp['W'] = Item2.gp
    if flag ==1:
        if Item2.direct in [1,5]:
            mExp['L'] = Item2.gl
            mExp['W'] = Item2.gp
        if Item2.direct in [2,3]:
            mExp['L'] = Item2.gl
            mExp['W'] = Item2.gh
        if Item2.direct in [4, 6] :
            mExp['L'] = Item2.gp
            mExp['W'] = Item2.gh
        mExp['CA'] = Item2.var_args[0]
        mExp['CB'] = Item2.var_args[1]
        mExp['CC'] = Item2.var_args[2]
        mExp['CD'] = Item2.var_args[3]
        mExp['CE'] = Item2.var_args[4]
        mExp['CF'] = Item2.var_args[5]
        mExp['CG'] = Item2.var_args[6]
        mExp['CH'] = Item2.var_args[7]
        mExp['CI'] = Item2.var_args[8]
        mExp['CJ'] = Item2.var_args[9]
        mExp['CK'] = Item2.var_args[10]
        mExp['CL'] = Item2.var_args[11]
        mExp['CM'] = Item2.var_args[12]
        mExp['CN'] = Item2.var_args[13]
        mExp['CO'] = Item2.var_args[14]
        mExp['CP'] = Item2.var_args[15]
    root = ET.fromstring(bdxml)
    for i in range(0,len(root)):
        if root[i].tag == 'Graph':
            node = root[i]
            attri = node.get('XX','')
    n = 0
    for i in range(0, len(root)):
        node = root[i]
        if (node.tag != 'FaceA') and (node.tag != 'FaceB'):
            continue
        for j in range(0,len(node)):
            cnode = node[j]
            if cnode.tag != 'BHole' :
                continue
            n = n + 1
    Item2.bhpt =[MyBigHolePoint() for i in range(n)]
    n = 0
    for i in range(0,len(root)):
        node = root[i]
        if (node.tag != 'FaceA') and (node.tag != 'FaceB'):
            continue
        for j in range(0, len(node)):
            cnode = node[j]
            if cnode.tag != 'BHole' :
                continue
            attri = cnode.get('X','')
            if attri !='':
                Item2.bhpt[n].sx = cnode.get('X')
            attri = cnode.get('Y', '')
            if attri != '':
                Item2.bhpt[n].sy = cnode.get('Y')
            attri = cnode.get('R', '')
            if attri != '':
                Item2.bhpt[n].sr = cnode.get('R')
            attri = cnode.get('Rb', '')
            if attri != '':
                Item2.bhpt[n].srb = cnode.get('Rb')
            Item2.bhpt[n].sri = Item2.bhpt[n].srb
            attri = cnode.get('X1', '')
            if attri != '':
                Item2.bhpt[n].sri= cnode.get('X1')
            attri = cnode.get('HDirect', '')
            if attri != '':
                Item2.bhpt[n].hdirect= cnode.get('HDirect')
                Item2.bhpt[n].face = node.tag
            attri = cnode.get('Hole_Xcap', '')
            if attri != '':
                Item2.bhpt[n].hole_xcap = int(mExpSetSubject(mExp,cnode.get('Hole_Xcap')))
            attri = cnode.get('Hole_Ycap', '')
            if attri != '':
                Item2.bhpt[n].hole_ycap = int(mExpSetSubject(mExp,cnode.get('Hole_Ycap')))
            attri = cnode.get('Holenum_X', '')
            if attri != '':
                Item2.bhpt[n].holenum_x = int(cnode.get('Holenum_X'))
            attri = cnode.get('Holenum_Y', '')
            if attri != '':
                Item2.bhpt[n].holenum_y = int(cnode.get('Holenum_Y'))
            if cnode.get('Hole_Z'):
                Item2.bhpt[n].hole_z = int(cnode.get('Hole_Z'))
            #print '2=',SetSubject(mExp,Item2.bhpt[n].sx)
            Item2.bhpt[n].x = float(mExpSetSubject(mExp,Item2.bhpt[n].sx))
            Item2.bhpt[n].y = float(mExpSetSubject(mExp,Item2.bhpt[n].sy))
            Item2.bhpt[n].r = float(mExpSetSubject(mExp,Item2.bhpt[n].sr))
            Item2.bhpt[n].rb = float(mExpSetSubject(mExp,Item2.bhpt[n].srb))
            Item2.bhpt[n].ri = float(mExpSetSubject(mExp,Item2.bhpt[n].sri))
            n = n + 1
    return Result
def BomList2CalcList(bomlist, calclist,workflowlist,mBDXMLList,gBGHash, is_new_calcitem=True):
    # if is_new_calcitem:
    #     for i in range(0,len(calclist)-1):
    #calclist =[]
    # print 'len of bomlist',len(bomlist)
    # print 'len of calclist', len(calclist)
    for i in range(0,len(bomlist)):
        if is_new_calcitem:
            item = {}
            item = TMyCalcItem()
            calclist.append(item)
        # if i == 69:
        #     print 'name=',bomlist[i]['name'],'guid=',bomlist[i]['guid'],json.dumps(bomlist[i],ensure_ascii=False).encode('gbk')
        #     print GetWorldMatrix(bomlist[i], calclist[i].m)
            #exit(1)
                      #TMyCalcItem  #是个类不清楚是什么东西
        BomItem2CalcItem(bomlist[i], calclist[i],workflowlist,mBDXMLList,gBGHash)
        m3 = calclist[i].m.tolist()
        log.debug('i='+str(i)+'item.m='+str()+','+'p.m=' + str(pnumber(m3[0][0])) + ',' + str(pnumber(m3[0][1])) + ',' + str(pnumber(m3[0][2])) + ',' + str(
                pnumber(m3[0][3])) + ',' \
            + str(pnumber(m3[1][0])) + ',' + str(pnumber(m3[1][1])) + ',' + str(pnumber(m3[1][2])) + ',' + str(
                pnumber(m3[1][3])) + ',' \
            + str(pnumber(m3[2][0])) + ',' + str(pnumber(m3[2][1])) + ',' + str(pnumber(m3[2][2])) + ',' + str(
                pnumber(m3[2][3])) + ',' \
            + str(pnumber(m3[3][0])) + ',' + str(pnumber(m3[3][1])) + ',' + str(pnumber(m3[3][2])) + ',' + str(
                pnumber(m3[3][3])) + '\n')
def SubSpaceAItem_2(p1,p2,item1,item2):
    item1.Copy(p1)
    item2.Copy(p2)
    item1.self_p = p1
    item2.self_p = p2
    #print '5555555555',item1.m
    item1.v = VectorTransform(AffineVectorMake(0,0,0), item1.m)
    item1.x = 0
    item1.y = 0
    item1.z = 0
    #一个四元数（Quaternion）描述了一个旋转轴和一个旋转角度
    #print item2.m , MatrixInvert(item1.m)
    tm = MatrixMultiply(item2.m, MatrixInvert(item1.m))
    #print tm
    q = QuaternionFromMatrix(tm)
    roll =0
    pitch = 0
    yaw = 0
    roll, pitch, yaw = QuaternionToRollPitchYaw(q, roll, pitch, yaw) #// oz = roll, ox = pitch, oy = yaw
    ox = Delphi_Round(RadToDeg(pitch))
    oy = Delphi_Round(RadToDeg(yaw))
    oz = Delphi_Round(RadToDeg(roll))
    #// 通过枚举的方式考虑问题
    if oz==90 :  #// B空间
        item2.v = VectorTransform(AffineVectorMake(0, item2.gp, 0), tm)
        if (oy==90) : item2.v =VectorTransform(AffineVectorMake(0, 0, 0), tm)
    elif oz ==-90:    #C空间
        item2.v = VectorTransform(AffineVectorMake(item2.gl,0,0), tm)
    else:
        if ox == 90:
            item2.v = VectorTransform(AffineVectorMake(0, 0, item2.gh), tm)
        else:
            item2.v = VectorTransform(AffineVectorMake(0, 0, 0), tm)
    #计算相对位置
    item2.x = Delphi_Round(item2.v[0])
    item2.y = Delphi_Round(item2.v[1])
    item2.z = Delphi_Round(item2.v[2])
    if (oz==90) or (oz==-90):
        if (oy==90):
            item2.gl, item2.gp = Swap(item2.gl, item2.gp)
            item2.gl, item2.gh = Swap(item2.gl, item2.gh)
            item2.bg_b_miny, item2.bg_l_minx, item2.bg_d_minx = SwapThree(item2.bg_b_miny, item2.bg_l_minx, item2.bg_d_minx)
            item2.bg_b_minx, item2.bg_l_miny, item2.bg_d_miny = SwapThree(item2.bg_b_minx, item2.bg_l_miny, item2.bg_d_miny)
            item2.bg_b_maxy, item2.bg_l_maxx, item2.bg_d_maxx = SwapThree(item2.bg_b_maxy, item2.bg_l_maxx, item2.bg_d_maxx)
            item2.bg_b_maxx, item2.bg_l_maxy, item2.bg_d_maxy = SwapThree(item2.bg_b_maxx, item2.bg_l_maxy, item2.bg_d_maxy)
            item2.bg_f_miny, item2.bg_r_minx, item2.bg_u_minx = SwapThree(item2.bg_f_miny, item2.bg_r_minx, item2.bg_u_minx)
            item2.bg_f_minx, item2.bg_r_miny, item2.bg_u_miny = SwapThree(item2.bg_f_minx, item2.bg_r_miny, item2.bg_u_miny)
            item2.bg_f_maxy, item2.bg_r_maxx, item2.bg_u_maxx = SwapThree(item2.bg_f_maxy, item2.bg_r_maxx, item2.bg_u_maxx)
            item2.bg_f_maxx, item2.bg_r_maxy, item2.bg_u_maxy = SwapThree(item2.bg_f_maxx, item2.bg_r_maxy, item2.bg_u_maxy)
            di = item2.direct
            if item2.direct==4 : di = 2 # // 竖纹侧板->横纹背板
            if item2.direct==6 : di = 3 #// 横纹侧板->竖纹背板
            if item2.direct==3 : di = 1 #// 竖纹背板->横纹层板
            if item2.direct==2 : di = 5 #// 横纹背板->竖纹层板
            if item2.direct==1 : di = 6 #// 横纹层板->横纹侧板
            if item2.direct==5 : di = 4 #// 竖纹层板->竖纹侧板
            item2.direct = di
        else:
            item2.gl, item2.gp = Swap(item2.gl, item2.gp)
            item2.bg_l_minx, item2.bg_b_minx = Swap(item2.bg_l_minx, item2.bg_b_minx)
            item2.bg_l_maxx, item2.bg_b_maxx = Swap(item2.bg_l_maxx, item2.bg_b_maxx)
            item2.bg_l_miny, item2.bg_b_miny = Swap(item2.bg_l_miny, item2.bg_b_miny)
            item2.bg_l_maxy, item2.bg_b_maxy = Swap(item2.bg_l_maxy, item2.bg_b_maxy)
            item2.bg_r_minx, item2.bg_f_minx = Swap(item2.bg_r_minx, item2.bg_f_minx)
            item2.bg_r_maxx, item2.bg_f_maxx = Swap(item2.bg_r_maxx, item2.bg_f_maxx)
            item2.bg_r_miny, item2.bg_f_miny = Swap(item2.bg_r_miny, item2.bg_f_miny)
            Swap(item2.bg_r_maxy, item2.bg_f_maxy)
            item2.bg_d_minx, item2.bg_d_miny = Swap(item2.bg_d_minx, item2.bg_d_miny)
            item2.bg_d_maxx, item2.bg_d_maxy = Swap(item2.bg_d_maxx, item2.bg_d_maxy)
            item2.bg_u_minx, item2.bg_u_miny = Swap(item2.bg_u_minx, item2.bg_u_miny)
            item2.bg_u_maxx, item2.bg_u_maxy = Swap(item2.bg_u_maxx, item2.bg_u_maxy)
            di = item2.direct
            if item2.direct==4 : di = 3 #// 竖纹侧板->竖纹背板
            if item2.direct==6 : di = 2 #// 横纹侧板->横纹背板
            if item2.direct==3 : di = 4 #// 竖纹背板->竖纹侧板
            if item2.direct==2 : di = 6 #// 横纹背板->横纹侧板
            if item2.direct==1 : di = 5 #// 横纹层板->竖纹层板
            if item2.direct==5 : di = 1 #// 竖纹层板->横纹层板
            item2.direct = di
    if ox==90 :
        item2.gh, item2.gp = Swap(item2.gh, item2.gp)
        item2.bg_d_minx, item2.bg_b_minx = Swap(item2.bg_d_minx, item2.bg_b_minx)
        item2.bg_d_maxx, item2.bg_b_maxx = Swap(item2.bg_d_maxx, item2.bg_b_maxx)
        item2.bg_d_miny, item2.bg_b_miny = Swap(item2.bg_d_miny, item2.bg_b_miny)
        item2.bg_d_maxy, item2.bg_b_maxy = Swap(item2.bg_d_maxy, item2.bg_b_maxy)
        item2.bg_u_minx, item2.bg_f_minx = Swap(item2.bg_u_minx, item2.bg_f_minx)
        item2.bg_u_maxx, item2.bg_f_maxx = Swap(item2.bg_u_maxx, item2.bg_f_maxx)
        item2.bg_u_miny, item2.bg_f_miny = Swap(item2.bg_u_miny, item2.bg_f_miny)
        item2.bg_u_maxy, item2.bg_f_maxy = Swap(item2.bg_u_maxy, item2.bg_f_maxy)
        item2.bg_l_minx, item2.bg_l_miny = Swap(item2.bg_l_minx, item2.bg_l_miny)
        item2.bg_l_maxx, item2.bg_l_maxy = Swap(item2.bg_l_maxx, item2.bg_l_maxy)
        item2.bg_r_minx, item2.bg_r_miny = Swap(item2.bg_r_minx, item2.bg_r_miny)
        item2.bg_r_maxx, item2.bg_r_maxy = Swap(item2.bg_r_maxx, item2.bg_r_maxy)
        di = item2.direct
        if item2.direct==4 : di = 6# // 竖纹侧板->横纹侧板
        if item2.direct==6 : di = 4# // 横纹侧板->竖纹侧板
        if item2.direct==3 : di = 1# // 竖纹背板->竖纹层板
        if item2.direct==2 : di = 5# // 横纹背板->横纹层板
        if item2.direct==1 : di = 3# // 横纹层板->横纹背板
        if item2.direct==5 : di = 2# // 竖纹层板->竖纹背板
        item2.direct= di
    p1 = item1
    p2 = item2
    p1.space = ''
    p1.space_x = 0
    p1.space_y = 0
    p1.space_z = 0
    p2.space = ''
    p2.space_x = 0
    p2.space_y = 0
    p2.space_z = 0
    return p1,p2
def SubSpaceAItem(p1,p2,item1,item2):
    if p1.space != p2.space or p1.space == 'Y' or p1.space=='X' or p2.space=='X':
        p1,p2 = SubSpaceAItem_2(p1,p2,item1,item2)
        return p1,p2
    item1.Copy(p1)
    item2.Copy(p2)
    item1.self_p = p1
    item2.self_p = p2
    p1 = item1
    p2 = item2
    p1.space = ''
    p1.space_x = 0
    p1.space_y = 0
    p1.space_z = 0
    p2.space = ''
    p2.space_x = 0
    p2.space_y = 0
    p2.space_z = 0
    return p1,p2
def IsLSIntersection(a1, b1, a2, b2):
    min = 50
    Result = 1
    if b1 < a1 : a1, b1 = Swap(a1, b1)
    if b2 < a2 : a2, b2 = Swap(a2, b2)
    if (a2 <= a1) and (b2 >= b1) : return Result
    if ((a2 + min) >= a1) and ((a2 + min) >= b1) :
        if (b2 > a1) and (b2 > b1) : Result = 0
    if ((b2 - min) <= a1) and ((b2 - min) <= b1) :
        if (a2 < a1) and (b2 < b1) : Result = 0
    return Result
def CI_HoleFace(face, p):
    Result = face
    if p.space=='B' :
    #// 左右下上后前
        if face==0 : Result = 5 #; // 左封边->前封边
        if face==1 : Result = 4#; // 右封边->后封边
        if face==4 : Result = 1#; // 后封边->右封边
        if face==5 : Result = 0#; // 前封边->左封边
    if p.space=='C':
        #// 左右下上后前
        if face==0 : Result = 4#; // 左封边->后封边
        if face==1 : Result = 5#; // 右封边->前封边
        if face==4 : Result = 0#; // 后封边->左封边
        if face==5 : Result = 1    #; // 前封边->右封边
    return Result
def GetHoleConfig(hashid, faceid, poi, poi2):
    global holeconfigHash
    def CalcMinL(a1, b1, a2, b2):
        if a1 > a2 : a1, a2 = Swap(a1, a2)
        if b1 > b2 : b1, b2 = Swap(b1, b2)
        t = -1
        if (a1 <= b1) and (a1 < b2) : t = min(a2, b2) - b1
        elif (a1 > b1) and (a1 < b2) : t =min(a2, b2) - a1
        else: pass
        Result = round(t)
        return Result
    def CalcOne():
        ## 'CalcOne','p.myface=',p.myface,'CI_HoleFace(p.myface, poi)=',CI_HoleFace(p.myface, poi),'faceid=',faceid
        if (CI_HoleFace(p.myface, poi) == faceid) and ((p.bh == 0) or (p.bh == bh)):
            ## type(poi)
            ## 'hahahha','poi.bg_l_maxx=',poi.bg_l_maxx,'bg_l_minx=',poi.bg_l_minx
            t0 = poi.bg_l_maxx - poi.bg_l_minx
            t1 = poi.bg_l_maxy - poi.bg_l_miny
            if p.algorithm==1 : #// 接触面算法
                t0 = CalcMinL(poi.bg_l_minx + poi.y, poi2.bg_r_minx + poi2.y, poi.bg_l_maxx + poi.y,
                              poi2.bg_r_maxx + poi2.y)
                t1 = CalcMinL(poi.bg_l_miny + poi.z, poi2.bg_r_miny + poi2.z, poi.bg_l_maxy + poi.z,
                              poi2.bg_r_maxy + poi2.z)
            # 't0=' , t0 , ',t1=' , t1,  ',bh=' , bh,'poi.bg_l_maxx=',poi.bg_l_maxx,'bg_l_minx=',poi.bg_l_minx
            if (CI_HoleFace(p.myface, poi) == 0) and (((di in [1, 5]) and (t0 > p.min) and (t0 <= p.max)) or (
                    (di in [2, 3]) and (t1 > p.min) and (t1 <= p.max))) : #// 左面
                # 'a'
                ret = p
                ## 'ret.iscalc=',ret.iscalc
                return ret
            t0 = poi.bg_r_maxx - poi.bg_r_minx
            t1 = poi.bg_r_maxy - poi.bg_r_miny
            if p.algorithm==1 : #// 接触面算法
                t0 = CalcMinL(poi.bg_r_minx + poi.y, poi2.bg_l_minx + poi2.y, poi.bg_r_maxx + poi.y,
                              poi2.bg_l_maxx + poi2.y)
                t1 = CalcMinL(poi.bg_r_miny + poi.z, poi2.bg_l_miny + poi2.z, poi.bg_r_maxy + poi.z,
                              poi2.bg_l_maxy + poi2.z)
            if (CI_HoleFace(p.myface, poi) == 1) and (((di in [1, 5]) and (t0 > p.min) and (t0 <= p.max)) or (
                    (di in [2, 3]) and (t1 > p.min) and (t1 <= p.max))): #then // 右面
                # 'b'
                ret = p
                return ret
            t0 = poi.bg_d_maxx - poi.bg_d_minx
            t1 = poi.bg_d_maxy - poi.bg_d_miny
            if p.algorithm==1 : #// 接触面算法
                t0 = CalcMinL(poi.bg_d_minx + poi.x, poi2.bg_u_minx + poi2.x, poi.bg_d_maxx + poi.x,
                              poi2.bg_u_maxx + poi2.x)
                t1 = CalcMinL(poi.bg_d_miny + poi.y, poi2.bg_u_miny + poi2.y, poi.bg_d_maxy + poi.y,
                              poi2.bg_u_maxy + poi2.y)
            if (CI_HoleFace(p.myface, poi) == 2) and (((di in [4, 6]) and (t1 > p.min) and (t1 <= p.max)) or (
                    (di in [2, 3]) and (t0 > p.min) and (t0 <= p.max))) : #// 下面
                # 'c'
                ret = p
                return ret
            t0 = poi.bg_u_maxx - poi.bg_u_minx
            t1 = poi.bg_u_maxy - poi.bg_u_miny
            if p.algorithm==1 : #// 接触面算法
                t0 = CalcMinL(poi.bg_u_minx + poi.x, poi2.bg_d_minx + poi2.x, poi.bg_u_maxx + poi.x,
                              poi2.bg_d_maxx + poi2.x)
                t1 = CalcMinL(poi.bg_u_miny + poi.y, poi2.bg_d_miny + poi2.y, poi.bg_u_maxy + poi.y,
                              poi2.bg_d_maxy + poi2.y)
            if (CI_HoleFace(p.myface, poi) == 3) and (((di in [4, 6]) and (t1 > p.min) and (t1 <= p.max)) or (
                    (di in [2, 3]) and (t0 > p.min) and (t0 <= p.max))) :  # // 上面
                # 'd'
                ret = p
                return ret
            t0 = poi.bg_b_maxx - poi.bg_b_minx
            t1 = poi.bg_b_maxy - poi.bg_b_miny
            if p.algorithm==1 : #// 接触面算法
                t0 = CalcMinL(poi.bg_b_minx + poi.x, poi2.bg_f_minx + poi2.x, poi.bg_b_maxx + poi.x,
                              poi2.bg_f_maxx + poi2.x)
                t1 = CalcMinL(poi.bg_b_miny + poi.z, poi2.bg_f_miny + poi2.z, poi.bg_b_maxy + poi.z,
                              poi2.bg_f_maxy + poi2.z)
            if (CI_HoleFace(p.myface, poi) == 4) and (((di in [4, 6]) and (t1 > p.min) and (t1 <= p.max)) or (
                    (di in [1, 5]) and (t0 > p.min) and (t0 <= p.max))) :# // 后面
                # 'e'
                ret = p
                return ret
            t0 = poi.bg_f_maxx - poi.bg_f_minx
            t1 = poi.bg_f_maxy - poi.bg_f_miny
            if p.algorithm==1 : #// 接触面算法
                t0 = CalcMinL(poi.bg_f_minx + poi.x, poi2.bg_b_minx + poi2.x, poi.bg_f_maxx + poi.x,
                              poi2.bg_b_maxx + poi2.x)
                t1 = CalcMinL(poi.bg_f_miny + poi.z, poi.bg_b_miny + poi2.z, poi.bg_f_maxy + poi.z,
                              poi2.bg_b_maxy + poi2.z)
            if (CI_HoleFace(p.myface, poi) == 5) and (((di in [4, 6]) and (t1 > p.min) and (t1 <= p.max)) or (
                    (di in [1, 5]) and (t0 > p.min) and (t0 <= p.max))) : #// 前面
                # 'f'
                ret = p
                return ret
    p = THoleConfig()
    ret = THoleConfig()
    if hashid <= 0 : return
    bh = Delphi_Round(poi.bh)
    holelist = holeconfigHash[hashid]  #???
    ## 'holelist',len(holelist)
    ## holelist
    di = poi.direct
    ret = None
    if (len(holelist) > 0) and (di == 0) : di = 1# // 没有设定纹路，但是又需要计算孔位的模块，di值等价1
    di2 = poi2.direct
    if (len(holelist) > 0) and (di2 == 0) : di2 = 1 # // 没有设定纹路，但是又需要计算孔位的模块，di2值等价1
    for i in range(0,len(holelist)):
        p = holelist[i]
        if p.bh == 0: continue
        if ((di in [4, 6]) and (di2 in [4, 6]))  \
            or ((di in [1, 5]) and (di2 in [1, 5]))\
            or ((di in [2, 3]) and (di2 in [2, 3])):
            if p.algorithm != 2 :
                continue
        elif p.algorithm==2 :
            continue
        CalcOne()
        if ret != None :
            Result = ret
            return Result
    for i in range(0,len(holelist)):
        p = holelist[i]
        if p.bh != 0 : continue
        if ((di in [4, 6]) and (di2 in [4, 6]))\
            or ((di in [1, 5]) and (di2 in [1, 5]))\
            or ((di in [2, 3]) and (di2 in [2, 3])):
            if p.algorithm!= 2 : continue
        elif p.algorithm==2 : continue
        ret = CalcOne()
        ## ret
        if ret != None :
            Result = ret
            return Result
    return THoleConfig()
def AddHoleSelf_A(p, node):
    global mHPInfoList
    def AddOneHole(x, y, hd, holetype, face, rb, rv, rh, hc):
        for i in range(0, 101):
            # 'AddOneHole'
            if p.ahole_index[i] == -1:
                p.ahole_index[i] = len(mHPInfoList)
                hpinfo = THolePointInfo()
                mHPInfoList.append(hpinfo)
                log.debug('AddHoleSelf_A=' + str(len(mHPInfoList))+'\n')
                hpinfo.x = x
                hpinfo.y = y
                hpinfo.xx = 0
                hpinfo.yy = 0
                hpinfo.hd = hd
                hpinfo.htype = holetype
                if holetype=='L' : hpinfo.r = rb
                if holetype=='I' : hpinfo.r = rv
                hpinfo.holeid = 0
                hpinfo.row = 0
                hpinfo.offset = 0
                hpinfo.face = face
                hpinfo.sr = rh
                hpinfo.smallcap = hc
                hpinfo.holecap = 0
                hpinfo.c = None
                hpinfo.isii = 0
                hpinfo.b_bh = Delphi_Round(p.bh)
                log.debug(
                        'AddHoleSelf_A=' + 'x=' + str(pnumber(hpinfo.x)) + ',y=' + str(pnumber(hpinfo.y)) + ',xx=' + str(
                            hpinfo.xx)
                        + ',yy=' + str(hpinfo.yy) + ',hd=' + str(hpinfo.hd) + ',hpinfo.r=' + str(
                            hpinfo.r) + ',sri=' + str(hpinfo.sri)
                        + ',htype=' + hpinfo.htype + ',holeid=' + str(hpinfo.holeid) + ',row=' + str(hpinfo.row)
                        + ',offset=' + str(hpinfo.offset) + ',face=' + str(hpinfo.face) + ',sr=' + str(
                            hpinfo.sr) + ',smallcap=' + str(hpinfo.smallcap)
                        + ',holecap=' + str(hpinfo.holecap) + ',isii=' + str(hpinfo.isii) +
                        '\n')
                return
    mTmpExp = {}
    sx = node.get('X', '0')
    sy = node.get('Y', '0')
    if sx =='':sx = '0'
    if sy =='':sy = '0'
    if str(p.gl) is None:    mTmpExp['L'] = 0
    else:    mTmpExp['L'] = p.gl
    if str(p.gp) is None:    mTmpExp['P'] = 0
    else:    mTmpExp['P'] = p.gp
    if str(p.gh) is None:    mTmpExp['H'] = 0
    else:    mTmpExp['H'] = p.gh
    x = nowSetSubject(sx, mTmpExp)
    y = nowSetSubject(sy, mTmpExp)
    t = node.get('Fb', 0)
    if t =='': t = 0
    else: t = int(t)
    hd = x
    if p.direct in [1,5]: #c层板
        if t==0 : hd = x
        if t==1 : hd = p.l - x
        if t==4 : hd = y
        if t==5 : hd = p.p - y
    if p.direct in [4, 6] : #// 侧板
        if t==2 : hd=y
        if t==3 : hd=p.h - y
        if t==4 : hd=x
        if t==5 : hd=p.p - x
    if p.direct in [2, 3] : #// 背板
        if t==2 : hd=y
        if t==3 : hd=p.h - y
        if t==0 : hd=x
        if t==1 : hd=p.l - x
    holetype = 'L'
    holevalue = node.get('T', 0)
    if holevalue == '':
        holevalue = 0
    else:
        holevalue = int(holevalue)
    if holevalue ==1 : holetype= 'I'
    #// 左封边, 右封边, 下封边, 上封边, 后封边, 前封边
    face= ''
    if t==0 : face='Left'
    if t==1 : face='Right'
    if t==2 : face='Down'
    if t==3 : face='Up'
    if t==4 : face='Back'
    if t==5 : face='Front'
    rb= node.get('RB', '0')
    rv= node.get( 'RV', '0')
    rh= node.get( 'RH', '0')
    hcvalue= node.get('HC', 0)
    sxc= node.get('XC', '0')
    sxn= node.get('XN', '0')
    syc= node.get('YC', '0')
    syn= node.get('YN', '0')
    if rb == '': rb='0'
    if rv == '': rv = '0'
    if rh == '': rh = '0'
    if hcvalue == '': hc = 0
    else:hc = int(hcvalue)
    if sxc == '': sxc='0'
    if sxn == '': sxn = '0'
    if syc == '': syc = '0'
    if syn == '': syn = '0'
    xc = nowSetSubject(sxc, mTmpExp)
    xn = nowSetSubject(sxn, mTmpExp)
    yc = nowSetSubject(syc, mTmpExp)
    yn = nowSetSubject(syn, mTmpExp)
    AddOneHole(x, y, hd, holetype, face, rb, rv,rh ,hc)
    for i in range(1,xn):
        AddOneHole(x + xc * i, y, hd, holetype, face, rb, rv, rh, hc)
    for i in range(1,yn):
        AddOneHole(x, y + yc * i, hd, holetype, face, rb, rv, rh, hc)
def AddHoleSelf_B(p, node):
    global mHPInfoList
    def AddOneHole(x, y, hd, holetype, face, rb, rv, rh, hc):
        for i in range(0,101):
            if p.bhole_index[i] == -1:
                p.bhole_index[i] = len(mHPInfoList)
                hpinfo = THolePointInfo()
                mHPInfoList.append(hpinfo)
                #(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug('AddHoleSelf_B=' + str(len(mHPInfoList))+'\n')
                hpinfo.x = x
                hpinfo.y = y
                hpinfo.xx = 0
                hpinfo.yy = 0
                hpinfo.hd = hd
                hpinfo.htype = holetype
                if holetype=='L' : hpinfo.r = rb
                if holetype=='I' : hpinfo.r = rv
                hpinfo.holeid = 0
                hpinfo.row = 0
                hpinfo.offset = 0
                hpinfo.face = face
                hpinfo.sr = rh
                hpinfo.smallcap = hc
                hpinfo.holecap = 0
                hpinfo.c = None
                hpinfo.isii = 0
                hpinfo.b_bh = Delphi_Round(p.bh)
                #(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug(
                        'AddHoleSelf_B=' + 'x=' + str(pnumber(hpinfo.x)) + ',y=' + str(pnumber(hpinfo.y)) + ',xx=' + str(
                            hpinfo.xx)
                        + ',yy=' + str(hpinfo.yy) + ',hd=' + str(hpinfo.hd) + ',hpinfo.r=' + str(
                            hpinfo.r) + ',sri=' + str(hpinfo.sri)
                        + ',htype=' + hpinfo.htype + ',holeid=' + str(hpinfo.holeid) + ',row=' + str(hpinfo.row)
                        + ',offset=' + str(hpinfo.offset) + ',face=' + str(hpinfo.face) + ',sr=' + str(
                            hpinfo.sr) + ',smallcap=' + str(hpinfo.smallcap)
                        + ',holecap=' + str(hpinfo.holecap) + ',isii=' + str(hpinfo.isii) +
                        '\n')
                return
    mTmpExp = {}
    sx = node.get('X', '0')
    sy = node.get('Y', '0')
    if sx =='':sx = '0'
    if sy =='':sy = '0'
    if str(p.gl) is None:
        mTmpExp['L'] = 0
    else:
        mTmpExp['L'] = p.gl
    if str(p.gp) is None:
        mTmpExp['P'] = 0
    else:
        mTmpExp['P'] = p.gp
    if str(p.gh) is None:
        mTmpExp['H'] = 0
    else:
        mTmpExp['H'] = p.gh
    x = nowSetSubject(sx, mTmpExp)
    y = nowSetSubject(sy, mTmpExp)
    t = node.get('Fb', 0)
    if t == '':t = 0
    else:t = int(t)
    hd = x
    if p.direct in [1, 5]:  # c层板
        if t == 0: hd = x
        if t == 1: hd = p.l - x
        if t == 4: hd = y
        if t == 5: hd = p.p - y
    if p.direct in [4, 6]:  # // 侧板
        if t == 2: hd = y
        if t == 3: hd = p.h - y
        if t == 4: hd = x
        if t == 5: hd = p.p - x
    if p.direct in [2, 3]:  # // 背板
        if t == 2: hd = y
        if t == 3: hd = p.h - y
        if t == 0: hd = x
        if t == 1: hd = p.l - x
    holetype = 'L'
    holevalue = node.get('T', 0)
    if holevalue == '':
        holevalue = 0
    else:
        holevalue = int(holevalue)
    if holevalue == 1: holetype = 'I'
    # // 左封边, 右封边, 下封边, 上封边, 后封边, 前封边
    face = ''
    if t == 0: face = 'Left'
    if t == 1: face = 'Right'
    if t == 2: face = 'Down'
    if t == 3: face = 'Up'
    if t == 4: face = 'Back'
    if t == 5: face = 'Front'
    rb = node.get('RB', '0')
    rv = node.get('RV', '0')
    rh = node.get('RH', '0')
    hcvalue = node.get('HC', 0)
    sxc = node.get('XC', '0')
    sxn = node.get('XN', '0')
    syc = node.get('YC', '0')
    syn = node.get('YN', '0')
    if rb == '': rb = '0'
    if rv == '': rv = '0'
    if rh == '': rh = '0'
    if hcvalue == '': hc = 0
    else: hc = int(hcvalue)
    if sxc == '': sxc='0'
    if sxn == '': sxn = '0'
    if syc == '': syc = '0'
    if syn == '': syn = '0'
    xc = nowSetSubject(sxc, mTmpExp)
    xn = nowSetSubject(sxn, mTmpExp)
    yc = nowSetSubject(syc, mTmpExp)
    yn = nowSetSubject(syn, mTmpExp)
    AddOneHole(x, y, hd, holetype, face, rb, rv, rh, hc)
    for i in range(1, xn):
        AddOneHole(x + xc * i, y, hd, holetype, face, rb, rv, rh, hc)
    for i in range(1, yn):
        AddOneHole(x, y + yc * i, hd, holetype, face, rb, rv, rh, hc)
def CalcHoleFace_BackFace(p1, p2, c):  # 20192/22 结束在此
    global mHoleFaceTwice
    nocalc = False
    if (c == None) or ((c.iscalc == 0) and (p1.is_calc_holeconfig[4] != 1)) or \
            ((c.iscalc == 1) and (p1.is_calc_holeconfig[4] == 2)):
        nocalc = True
    di1 = p1.direct
    di2 = p2.direct
    if Delphi_not(di1) in [1, 2, 3, 4, 5, 6]: di1 = 1
    if Delphi_not(di2) in [1, 2, 3, 4, 5, 6]: di2 = 1
    if (di1 in [4, 6]) and (di2 in [2, 3]) and \
            (p1.x >= p2.x) and (p1.x + p1.gl <= p2.x + p2.gl) and \
            (IsLSIntersection(p1.z + p1.bg_b_miny, p1.z + p1.bg_b_maxy, p2.z + p2.bg_f_miny, p2.z + p2.bg_f_maxy) == 1):
        # // 层板与侧板接触，层板是横纹，侧板是竖纹
        if nocalc: return
        if (mHoleFaceTwice == 0) and (c.i_isoutput == 1):
            if p2.holeface == 0: p2.holeface = 2
            if p2.holeface == 1: p2.holeface = 3
            if (p1.x < (p2.x + p2.gl // 2)):
                if (p2.l_item0 == None): p2.l_item0 = p1.self_p
                if (p2.l_item0 != None) and (p2.l_item0.x < p1.x): p2.l_item0 = p1.self_p
            elif (p1.x + p1.gl > p2.x + p2.gl // 2):
                if (p2.r_item0 == None): p2.r_item0 = p1.self_p
                if (p2.r_item0 != None) and (p2.r_item0.x + p2.r_item0.gl > p1.x + p1.gl):p2.r_item0 = p1.self_p
        if (c.l_isoutput == 1) and (mHoleFaceTwice == 1) and (p1.holeface == 0):  # // AB面都没有孔位的时候进行第二次计算
            if p1.self_p == p2.l_item0: p1.holeface = 2
            if p1.self_p == p2.r_item0: p1.holeface = 1
    if (di1 in [1, 5]) and (di2 in [2, 3]) and \
            (p1.z >= p2.z) and (p1.z + p1.gh <= p2.z + p2.gh) and \
            (IsLSIntersection(p1.x + p1.bg_b_minx, p1.x + p1.bg_b_maxx, p2.x + p2.bg_f_minx, p2.x + p2.bg_f_maxx) == 1):
        # // 背板与侧板接触，背板竖纹，侧板竖纹
        if nocalc: return
        if (mHoleFaceTwice == 0) and (c.i_isoutput == 1):
            if p2.holeface == 0: p2.holeface = 2
            if p2.holeface == 1: p2.holeface = 3
            if (p1.z < p2.z + p2.gh // 2):
                if (p2.d_item0 == None): p2.d_item0 = p1.self_p
                if (p2.d_item0 != None) and (p2.d_item0.z < p1.z):p2.d_item0 = p1.self_p
            elif (p1.z + p1.gh > p2.z + p2.gh // 2):
                if (p2.u_item0 == None): p2.u_item0 = p1.self_p
                if (p2.u_item0 != None) and (p2.u_item0.z + p2.u_item0.gh > p1.z + p1.gh):p2.u_item0 = p1.self_p
        if (c.l_isoutput == 1) and (mHoleFaceTwice == 1) and (p1.holeface == 0):  # // AB面都没有孔位的时候进行第二次计算
            if p1.self_p == p2.d_item0: p1.holeface = 2
            if p1.self_p == p2.u_item0: p1.holeface = 1
def CalcHoleFace_DownFace(p1, p2, c):
    global mHoleFaceTwice
    nocalc = False
    if (c == None) or ((c.iscalc == 0) and (p1.is_calc_holeconfig[2] != 1)) \
            or ((c.iscalc == 1) and (p1.is_calc_holeconfig[2] == 2)):
        nocalc = True
    di1 = p1.direct
    di2 = p2.direct
    if Delphi_not(di1) in [1, 2, 3, 4, 5, 6]: di1 = 1
    if Delphi_not(di2) in [1, 2, 3, 4, 5, 6]: di2 = 1
    if (di1 in [4, 6]) and (di2 in [1, 5]) and \
            (p1.x >= p2.x) and (p1.x + p1.gl <= p2.x + p2.gl) and \
            (IsLSIntersection(p1.y + p1.bg_d_miny, p1.y + p1.bg_d_maxy, p2.y + p2.bg_u_miny, p2.y + p2.bg_u_maxy) == 1):
        # 中立板与底板接触，中立板是竖纹，底板横纹
        if nocalc: return
        if (mHoleFaceTwice == 0) and (c.i_isoutput == 1):  # // 纹理面
            if p2.holeface == 0: p2.holeface = 2
            if p2.holeface == 1: p2.holeface = 3
            # // // // /
            if (p1.x < p2.x + p2.gl // 2):
                if (p2.l_item0 == None): p2.l_item0 = p1.self_p
                if (p2.l_item0 != None) and (p2.l_item0.x < p1.x): p2.l_item0 = p1.self_p
            elif (p1.x + p1.gl > p2.x + p2.gl // 2):
                if (p2.r_item0 == None): p2.r_item0 = p1.self_p
                if (p2.r_item0 != None) and (p2.r_item0.x + p2.r_item0.gl > p1.x + p1.gl):p2.r_item0 = p1.self_p
        if (c.l_isoutput == 1) and (mHoleFaceTwice == 1) and (p1.holeface == 0):  # // AB面都没有孔位的时候进行第二次计算
            if p1.self_p == p2.l_item0: p1.holeface = 2
            if p1.self_p == p2.r_item0: p1.holeface = 1
    if (di1 in [2, 3]) and (di2 in [1, 5]) and \
            (p1.y >= p2.y) and (p1.y + p1.gp <= p2.y + p2.gp) and \
            (IsLSIntersection(p1.x + p1.bg_d_minx, p1.x + p1.bg_d_maxx, p2.x + p2.bg_u_minx, p2.x + p2.bg_u_maxx) == 1):
        # // 背板与底板接触，背板竖纹，底板横纹
        if nocalc: return
        if (mHoleFaceTwice == 0) and (c.i_isoutput == 1):  # // 纹理面
            if p2.holeface == 0: p2.holeface = 2
            if p2.holeface == 1: p2.holeface = 3
        # // // // /
            if (p1.y < p2.y + p2.gp // 2):
                if (p2.d_item0 == None): p2.d_item0 = p1.self_p
                if (p2.d_item0 != None) and (p2.d_item0.y < p1.y): p2.d_item0 = p1.self_p
            elif (p1.y + p1.gp > p2.y + p2.gp // 2):
                if (p2.u_item0 == None): p2.u_item0 = p1.self_p
                if (p2.u_item0 != None) and (p2.u_item0.y + p2.u_item0.gp > p1.y + p1.gp):p2.u_item0 = p1.self_p
        if (c.l_isoutput == 1) and (mHoleFaceTwice == 1) and (p1.holeface == 0):  # // AB面都没有孔位的时候进行第二次计算
            if p1.self_p == p2.d_item0: p1.holeface = 2
            if p1.self_p == p2.u_item0: p1.holeface = 1
def CalcHoleFace_FrontFace(p1, p2, c):
    global mHoleFaceTwice
    nocalc = False
    if (c == None) or ((c.iscalc == 0) and (p1.is_calc_holeconfig[5] != 1)) or \
            ((c.iscalc == 1) and (p1.is_calc_holeconfig[5] == 2)):
        nocalc = True
    di1 = p1.direct
    di2 = p2.direct
    if Delphi_not(di1) in [1, 2, 3, 4, 5, 6]: di1 = 1
    if Delphi_not(di2) in [1, 2, 3, 4, 5, 6]: di2 = 1
    if (di1 in [4, 6]) and (di2 in [2, 3]) and \
            (p1.x >= p2.x) and (p1.x + p1.gl <= p2.x + p2.gl) and \
            (IsLSIntersection(p1.z + p1.bg_f_miny, p1.z + p1.bg_f_maxy, p2.z + p2.bg_b_miny, p2.z + p2.bg_b_maxy) == 1):
        # // 层板与侧板接触，层板是横纹，侧板是竖纹
        if nocalc: return
        if (mHoleFaceTwice == 0) and (c.i_isoutput == 1):
            if p2.holeface == 0: p2.holeface = 1
            if p2.holeface == 2: p2.holeface = 3
            if (p1.x < (p2.x + p2.gl // 2)):
                if (p2.l_item == None): p2.l_item = p1.self_p
                if (p2.l_item != None) and (p2.l_item.x < p1.x): p2.l_item = p1.self_p
            elif (p1.x + p1.gl > p2.x + p2.gl // 2):
                if (p2.r_item == None): p2.r_item = p1.self_p
                if (p2.r_item != None) and (p2.r_item.x + p2.r_item.gl > p1.x + p1.gl): p2.r_item = p1.self_p
        if (c.l_isoutput == 1) and (mHoleFaceTwice == 1) and (p1.holeface == 0):  # // AB面都没有孔位的时候进行第二次计算
            if p1.self_p == p2.l_item: p1.holeface = 2
            if p1.self_p == p2.r_item: p1.holeface = 1
    if (di1 in [1, 5]) and (di2 in [2, 3]) and \
            (p1.z >= p2.z) and (p1.z + p1.gh <= p2.z + p2.gh) and \
            (IsLSIntersection(p1.x + p1.bg_f_minx, p1.x + p1.bg_f_maxx, p2.x + p2.bg_b_minx, p2.x + p2.bg_b_maxx) == 1):
        # // 背板与侧板接触，背板竖纹，侧板竖纹
        if nocalc: return
        if (mHoleFaceTwice == 0) and (c.i_isoutput == 1):
            if p2.holeface == 0: p2.holeface = 1
            if p2.holeface == 2: p2.holeface = 3
            if (p1.z < p2.z + p2.gh // 2):
                if (p2.d_item == None): p2.d_item = p1.self_p
                if (p2.d_item != None) and (p2.d_item.z < p1.z):p2.d_item = p1.self_p
            elif (p1.z + p1.gh > p2.z + p2.gh // 2):
                if (p2.u_item == None): p2.u_item = p1.self_p
                if (p2.u_item != None) and (p2.u_item.z + p2.u_item.gh > p1.z + p1.gh):p2.u_item = p1.self_p
        if (c.l_isoutput == 1) and (mHoleFaceTwice == 1) and (p1.holeface == 0):  # // AB面都没有孔位的时候进行第二次计算
            if p1.self_p == p2.d_item: p1.holeface = 2
            if p1.self_p == p2.u_item: p1.holeface = 1
def CalcHoleFace_LeftFace(p1, p2, c):
    global mHoleFaceTwice
    def IsLSIntersection(a1, b1, a2, b2):
        min = 50
        Result = 1
        if b1 < a1 :
            a1,b1 = b1,a1
        if b2 < a2:
            a2, b2 =b2, a2
        if (a2 <= a1) and (b2 >= b1):
            return
        if ((a2 + min) >= a1) and ((a2 + min) >= b1) :
            if (b2 > a1) and (b2 > b1):
                Result=0
        if ((b2 - min) <= a1) and ((b2 - min) <= b1) :
            if (a2 < a1) and (b2 < b1) :
                Result = 0
        return Result
    nocalc = False
    if (c == None) or ((c.iscalc == 0) and (p1.is_calc_holeconfig[0] != 1)) or \
            ((c.iscalc == 1) and (p1.is_calc_holeconfig[0] == 2)):
        nocalc = True
    di1 = p1.direct
    di2 = p2.direct
    if Delphi_not(di1) in [1,2,3,4,5,6] : di1 = 1
    if Delphi_not(di2) in [1,2,3,4,5,6] : di2 = 1
    ## 'CalcHoleFace_LeftFace',"di1=",di1,'di2=',di2
    if (di1 in [1, 5]) and (di2 in [4, 6]) and \
        (p1.z >= p2.z) and (p1.z + p1.gh <= p2.z + p2.gh) and \
        (IsLSIntersection(p1.y + p1.bg_l_minx, p1.y + p1.bg_l_maxx, p2.y + p2.bg_r_minx, p2.y + p2.bg_r_maxx)==1):
        #// 层板与侧板接触，层板是横纹，侧板是竖纹
        if nocalc : return
        if (mHoleFaceTwice==0) and (c.i_isoutput == 1):
            if p2.holeface==0 : p2.holeface = 2
            if p2.holeface==1 : p2.holeface = 3
            if (p1.z < (p2.z + p2.gh // 2)):
                if (p2.d_item0 ==None) : p2.d_item0 = p1.self_p
                if (p2.d_item0 != None) and (p2.d_item0.z < p1.z) : p2.d_item0 = p1.self_p
            elif (p1.z+p1.gh > p2.z+p2.gh // 2):
                if (p2.u_item0==None) : p2.u_item0 = p1.self_p
                if (p2.u_item0 != None) and (p2.u_item0.z + p2.u_item0.gh > p1.z + p1.gh) :p2.u_item0 = p1.self_p
        if (c.l_isoutput==1) and (mHoleFaceTwice==1) and (p1.holeface==0) : #// AB面都没有孔位的时候进行第二次计算
            if p1.self_p==p2.d_item0 : p1.holeface = 2
            if p1.self_p==p2.u_item0 : p1.holeface = 1
    if (di1 in [2, 3]) and (di2 in [4, 6]) and  \
        (p1.y >= p2.y) and (p1.y + p1.gp <= p2.y + p2.gp) and  \
        (IsLSIntersection(p1.z + p1.bg_l_miny, p1.z + p1.bg_l_maxy, p2.z + p2.bg_r_miny, p2.z + p2.bg_r_maxy)==1):
        #// 背板与侧板接触，背板竖纹，侧板竖纹
        if nocalc : return
        if (mHoleFaceTwice==0) and (c.i_isoutput == 1)  :
            if p2.holeface==0 : p2.holeface = 2
            if p2.holeface==1 : p2.holeface = 3
            if (p1.y < p2.y + p2.gp // 2) :
                if (p2.l_item0==None) : p2.l_item0 = p1.self_p
                if (p2.l_item0 != None) and (p2.l_item0.y < p1.y) : p2.l_item0 = p1.self_p
            elif (p1.x + p1.gl > p2.x + p2.gl // 2) :
                if (p2.r_item0 == None) : p2.r_item0 = p1.self_p
                if (p2.r_item0 != None) and (p2.r_item0.y + p2.r_item0.gh > p1.y + p1.gh) :
                    p2.r_item0 = p1.self_p
        if (c.l_isoutput==1) and (mHoleFaceTwice==1) and (p1.holeface==0) : #// AB面都没有孔位的时候进行第二次计算
            if p1.self_p==p2.l_item0 : p1.holeface = 2
            if p1.self_p==p2.r_item0 : p1.holeface = 1
            #     offset = 0
        # if algorithm==1 : #// 按接触面计算
        #
        #     if p2.gp + p2.y > p2.y : t=p2.y
        #     else : t = p2.gp + p2.y
        #     if t > p1.y : offset = t - p1.y
        # UpdateTempExpVariable(p1)
        # l = Length_HoleFace(p1, p2, c, 1, 0)# // 左面1, // 右面2, // 下面3, // 上面4, // 后面5, // 前面6
        # if c.algorithm==0 : #// 兼容算法
        #     t = (p1.bg_l_maxx + p1.y) - (p2.gp + p2.y)
        #     if (t > 0) and (c.calctype in [0, 1]) : l = l - t #// 接触面较小
        #     if p1.zero_y==4 : #// 前封边
        #         t = (p1.bg_l_minx + p1.y) - p2.y
        #         if (t < 0) and (c.calctype in [0, 1]) : l = l + t # // 接触面较小
        #mTmpExp['L'] = str(l)
def CalcHoleFace_RightFace(p1, p2, c):
    global mHoleFaceTwice
    nocalc = False
    if (c == None) or ((c.iscalc == 0) and (p1.is_calc_holeconfig[1] != 1)) or \
            ((c.iscalc == 1) and (p1.is_calc_holeconfig[1] == 2)):
        nocalc = True
    di1 = p1.direct
    di2 = p2.direct
    if Delphi_not(di1) in [1, 2, 3, 4, 5, 6]: di1 = 1
    if Delphi_not(di2) in [1, 2, 3, 4, 5, 6]: di2 = 1
    if (di1 in [1, 5]) and (di2 in [4, 6]) and \
            (p1.z >= p2.z) and (p1.z + p1.gh <= p2.z + p2.gh) and \
            (IsLSIntersection(p1.y + p1.bg_r_minx, p1.y + p1.bg_r_maxx, p2.y + p2.bg_l_minx, p2.y + p2.bg_l_maxx) == 1):
        # // 层板与侧板接触，层板是横纹，侧板是竖纹
        if nocalc: return
        if (mHoleFaceTwice == 0) and (c.i_isoutput == 1):
            if p2.holeface == 0: p2.holeface = 1
            if p2.holeface == 2: p2.holeface = 3
            if (p1.z < (p2.z + p2.gh // 2)):
                if (p2.d_item == None): p2.d_item = p1.self_p
                if (p2.d_item != None) and (p2.d_item.z < p1.z): p2.d_item = p1.self_p
            elif (p1.z + p1.gh > p2.z + p2.gh // 2):
                if (p2.u_item == None): p2.u_item = p1.self_p
                if (p2.u_item != None) and (p2.u_item.z + p2.u_item.gh > p1.z + p1.gh):
                    p2.u_item = p1.self_p
        if (c.l_isoutput == 1) and (mHoleFaceTwice == 1) and (p1.holeface == 0):  # // AB面都没有孔位的时候进行第二次计算
            if p1.self_p == p2.d_item: p1.holeface = 2
            if p1.self_p == p2.u_item: p1.holeface = 1
    if (di1 in [2, 3]) and (di2 in [4, 6]) and \
            (p1.y >= p2.y) and (p1.y + p1.gp <= p2.y + p2.gp) and \
            (IsLSIntersection(p1.z + p1.bg_r_miny, p1.z + p1.bg_r_maxy, p2.z + p2.bg_l_miny, p2.z + p2.bg_l_maxy) == 1):
        # // 背板与侧板接触，背板竖纹，侧板竖纹
        if nocalc: return
        if (mHoleFaceTwice == 0) and (c.i_isoutput == 1):
            if p2.holeface == 0: p2.holeface = 1
            if p2.holeface == 2: p2.holeface = 3
            if (p1.y < p2.y + p2.gp // 2):
                if (p2.l_item == None): p2.l_item = p1.self_p
                if (p2.l_item != None) and (p2.l_item.y < p1.y):p2.l_item = p1.self_p
            elif (p1.x + p1.gl > p2.x + p2.gl // 2):
                if (p2.r_item == None): p2.r_item = p1.self_p
                if (p2.r_item != None) and (p2.r_item.y + p2.r_item.gh > p1.y + p1.gh):
                    p2.r_item = p1.self_p
        if (c.l_isoutput == 1) and (mHoleFaceTwice == 1) and (p1.holeface == 0):  # // AB面都没有孔位的时候进行第二次计算
            if p1.self_p == p2.l_item: p1.holeface = 2
            if p1.self_p == p2.r_item: p1.holeface = 1
def CalcHoleFace_UpFace(p1, p2, c):
    global mHoleFaceTwice
    nocalc = False
    if (c == None) or ((c.iscalc == 0) and (p1.is_calc_holeconfig[3] != 1)) or \
            ((c.iscalc == 1) and (p1.is_calc_holeconfig[3] == 2)):
        nocalc = True
    di1 = p1.direct
    di2 = p2.direct
    if Delphi_not(di1) in [1, 2, 3, 4, 5, 6]: di1 = 1
    if Delphi_not(di2) in [1, 2, 3, 4, 5, 6]: di2 = 1
    if (di1 in [4, 6]) and (di2 in [1, 5]) and \
            (p1.x >= p2.x) and (p1.x + p1.gl <= p2.x + p2.gl) and \
            (IsLSIntersection(p1.y + p1.bg_u_miny, p1.y + p1.bg_u_maxy, p2.y + p2.bg_d_miny, p2.y + p2.bg_d_maxy) == 1):
        # // 层板与侧板接触，层板是横纹，侧板是竖纹
        if nocalc: return
        if (mHoleFaceTwice == 0) and (c.i_isoutput == 1):
            if p2.holeface == 0: p2.holeface = 1
            if p2.holeface == 2: p2.holeface = 3
            if (p1.x < p2.x + p2.gl // 2):
                if (p2.l_item == None): p2.l_item = p1.self_p
                if (p2.l_item != None) and (p2.l_item.x < p1.x): p2.l_item = p1.self_p
            elif (p1.x + p1.gl > p2.x + p2.gl // 2):
                if (p2.r_item == None): p2.r_item = p1.self_p
                if (p2.r_item != None) and (p2.r_item.x + p2.r_item.gl > p1.x + p1.gl):
                    p2.r_item = p1.self_p
        if (c.l_isoutput == 1) and (mHoleFaceTwice == 1) and (p1.holeface == 0):  # // AB面都没有孔位的时候进行第二次计算
            if p1.self_p == p2.l_item: p1.holeface = 2
            if p1.self_p == p2.r_item: p1.holeface = 1
    if (di1 in [2, 3]) and (di2 in [1, 5]) and \
            (p1.y >= p2.y) and (p1.y + p1.gp <= p2.y + p2.gp) and \
            (IsLSIntersection(p1.x + p1.bg_u_minx, p1.x + p1.bg_u_maxx, p2.x + p2.bg_d_minx, p2.x + p2.bg_d_maxx) == 1):
        # // 背板与侧板接触，背板竖纹，侧板竖纹
        if nocalc: return
        if (mHoleFaceTwice == 0) and (c.i_isoutput == 1):
            if p2.holeface == 0: p2.holeface = 1
            if p2.holeface == 2: p2.holeface = 3
            if (p1.y < p2.y + p2.gp // 2):
                if (p2.d_item == None): p2.d_item = p1.self_p
                if (p2.d_item != None) and (p2.d_item.y < p1.y): p2.d_item = p1.self_p
            elif (p1.y + p1.gp > p2.y + p2.gp // 2):
                if (p2.u_item == None): p2.u_item = p1.self_p
                if (p2.u_item != None) and (p2.u_item.y + p2.u_item.gp > p1.y + p1.gp):
                    p2.u_item = p1.self_p
        if (c.l_isoutput == 1) and (mHoleFaceTwice == 1) and (p1.holeface == 0):  # // AB面都没有孔位的时候进行第二次计算
            if p1.self_p == p2.d_item: p1.holeface = 2
            if p1.self_p == p2.u_item: p1.holeface = 1
def CalcBdxmlHole_FrontFace(p1, p2):
    ho = hole()
    di1 = p1.direct
    di2 = p2.direct
    if Delphi_not(di1) in [1, 2, 3, 4, 5, 6]: di1 = 1
    if Delphi_not(di2) in [1, 2, 3, 4, 5, 6]: di2 = 1
    ho.p1 = p1
    ho.p2 = p2
    if di1 in [4, 6] and di2 in [2, 3] and (p1.x >= p2.x) \
            and (p1.x + p1.gl <= p2.x + p2.gl) and \
            (IsLSIntersection(p1.z + p1.bg_f_miny, p1.z + p1.bg_f_maxy, p2.z + p2.bg_b_miny, p2.z + p2.bg_b_maxy) == 1):
        # 中立板与顶板接触，中立板是竖纹，底板横纹
        for i in range(0, len(p1.bhpt)):
            bhp = p1.bhpt[i]
            if bhp.hdirect == 'R':
                if bhp.face == 'FaceA':
                    smallcap = bhp.hole_z
                else:
                    smallcap = p1.gl - bhp.hole_z
                x = p1.x - p2.x + smallcap
                y = p1.z - p2.z + Delphi_Round(bhp.y) + p1.bg_f_miny
                p2.big_p = p1
                MakeVector(ho.i_offset, 0, 0, bhp.y - int(bhp.y))
                ho.wx = smallcap
                ho.wy = p1.gp
                ho.wz = int(bhp.y)
                if (bhp.sri != '') and (bhp.sri != '0'):
                    AddHole_A(None, p2, p1, ho, IdentityHmgMatrix, x, y, 0, -1, 0,
                              bhp.hole_z, 0, 'Front', 'I', bhp.sri, '', '')
                for j in range(1, bhp.holenum_y):
                    ty = y + bhp.hole_ycap * j
                    p2.big_p = p1
                    ho.wx = smallcap
                    ho.wy = p1.gp
                    ho.wz = int(bhp.y) + bhp.hole_ycap * j
                    if (bhp.sri != '') and bhp.sri != '0':
                        AddHole_A(None, p2, p1, ho, IdentityHmgMatrix, x, ty ,
                                  0, -1, 0, bhp.hole_z, 0, 'Front', 'I', bhp.sri, '', '')
    if (di1 in [1, 5]) and (di2 in [2, 3]) and (p1.z >= p2.z) and (p1.z + p1.gh <= p2.z + p2.gh) and \
            (IsLSIntersection(p1.x + p1.bg_f_minx, p1.x + p1.bg_f_maxx, p2.x + p2.bg_b_minx, p2.x + p2.bg_b_maxx) == 1):
        # 背板与顶板接触，背板竖纹，顶板横纹
        for i in range(0, len(p1.bhpt)):
            bhp = p1.bhpt[i]
            if bhp.hdirect == 'U':
                if bhp.face == 'FaceA':
                    smallcap = bhp.hole_z
                else:
                    smallcap = p1.gh - bhp.hole_z
                x = p1.z - p2.z + smallcap
                y = p1.x - p2.x + round(bhp.x) + p1.bg_f_minx
                p2.big_p = p1
                MakeVector(ho.i_offset, bhp.x - int(bhp.x), 0, 0)
                ho.wx = int(bhp.x)
                ho.wy = p1.gp
                ho.wz = smallcap
                if (bhp.sri != '') and (bhp.sri != '0'):
                    AddHole_A(None, p2, p1, ho, IdentityHmgMatrix, y, x, 0, -1, 0,
                              bhp.hole_z, 0, 'Front', 'I', bhp.sri, '', '')
                for j in range(1, bhp.holenum_x):
                    ty = y + bhp.hole_xcap * j
                    p2.big_p = p1
                    ho.wx = int(bhp.x) + bhp.hole_xcap * j
                    if (bhp.sri != '') and (bhp.sri != '0'):
                        AddHole_A(None, p2, p1, ho, IdentityHmgMatrix, y+bhp.hole_xcap*j, x, 0, -1,
                                  0, bhp.hole_z, 0, 'Front', 'I', bhp.sri, '', '')
def CalcBdxmlHole_LeftFace(p1, p2):
    ho = hole()
    di1 = p1.direct
    di2 = p2.direct
    if Delphi_not(di1) in [1,2,3,4,5,6] : di1 = 1
    if Delphi_not(di2)in [1,2,3,4,5,6] : di2 = 1
    ho.p1 = p1
    ho.p2 = p2
    if di1 in [1,5] and di2 in [4,6] and (p1.z>=p2.z) \
        and (p1.z + p1.gh<=p2.z+p2.gh) and \
    (IsLSIntersection(p1.y + p1.bg_l_minx, p1.y + p1.bg_l_maxx, p2.y + p2.bg_r_minx, p2.y + p2.bg_r_maxx)==1):
        #层板与侧板接触，层板是横纹，侧板是竖纹
        for i in range(0,len(p1.bhpt)):
            bhp = p1.bhpt[i]
            if bhp.hdirect == 'L':
                if bhp.face =='FaceA': smallcap = bhp.hole_z
                else: smallcap = p1.gh - bhp.hole_z
                x = p1.z - p2.z +smallcap
                y = p1.y - p2.y +Delphi_Round(bhp.y) + p1.bg_l_minx
                if p1.isxx==2:    #前后斜
                    pass
                if p1.isxx == 1: #左右斜
                    pass
                p2.big_p = p1
                MakeVector(ho.i_offset, 0, bhp.y - int(bhp.y), 0)
                ho.wx = 0
                ho.wy = int(bhp.y)
                ho.wz = smallcap
                if (bhp.sri != '') and (bhp.sri!='0') :
                    #(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcBdxmlHole_LeftFaceAddHole_B'+'Left1')
                    AddHole_B(None, p2, p1, ho, IdentityHmgMatrix, y, x, 0, -1, 0,
                              bhp.hole_z, 0, 'Left', 'I', bhp.sri, '', '')
                for j in range(1,bhp.holenum_y):
                    p2.big_p = p1
                    ho.wy = int(bhp.y) + bhp.hole_ycap * j
                    if (bhp.sri != '') and bhp.sri !='0':
                        #(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcBdxmlHole_LeftFaceAddHole_B' + 'Left2')
                        AddHole_B(None, p2,p1, ho, IdentityHmgMatrix, y + bhp.hole_ycap * j,
                                  x, 0, -1, 0, bhp.hole_z, 0, 'Left', 'I', bhp.sri, '', '')
    if (di1 in [2,3]) and (di2 in [4,6]) and (p1.y >= p2.y) and (p1.y + p1.gp<=p2.y + p2.gp) and \
            (IsLSIntersection(p1.z + p1.bg_l_miny, p1.z + p1.bg_l_maxy, p2.z + p2.bg_r_miny, p2.z + p2.bg_r_maxy)==1):
        # 背板与侧板接触， 背板竖纹， 侧板竖纹
        for i in range(0,len(p1.bhpt)):
            bhp = p1.bhpt[i]
            if bhp.hdirect =='L':
                if bhp.face =='FaceA':
                    smallcap = bhp.hole_z
                else:
                    smallcap = p1.gp - bhp.hole_z
                x = p1.z - p2.z + round(bhp.y) + p1.bg_l_miny
                y = p1.y - p2.y + smallcap
                p2.big_p = p1
                MakeVector(ho.i_offset, 0, 0, bhp.y - int(bhp.y))
                ho.wx = 0
                ho.wy = smallcap
                ho.wz = int(bhp.y)
                if (bhp.sri != '') and (bhp.sri != '0') :
                    AddHole_B(None, p2, p1, ho, IdentityHmgMatrix, y, x, 0, -1, 0,
                              bhp.hole_z, 0, 'Left', 'I', bhp.sri, '', '')
                    #(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcBdxmlHole_LeftFaceAddHole_B' + 'Left3')
                for j in range(1,bhp.holenum_y):
                    p2.big_p = p1
                    ho.wz = int(bhp.y) + bhp.hole_ycap * j
                    if (bhp.sri != '') and (bhp.sri != '0') :
                        #(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcBdxmlHole_LeftFaceAddHole_B' + 'Left4')
                        AddHole_B(None, p2, p1, ho, IdentityHmgMatrix, y, x+bhp.hole_ycap * j, 0, -1,
                                  0, bhp.hole_z, 0, 'Left', 'I', bhp.sri, '', '')
def CalcBdxmlHole_RightFace(p1, p2):
    ho = hole()
    di1 = p1.direct
    di2 = p2.direct
    if Delphi_not(di1) in [1, 2, 3, 4, 5, 6]: di1 = 1
    if Delphi_not(di2) in [1, 2, 3, 4, 5, 6]: di2 = 1
    ho.p1 = p1
    ho.p2 = p2
    if di1 in [1, 5] and di2 in [4, 6] and (p1.z >= p2.z) \
            and (p1.z + p1.gh <= p2.z + p2.gh) and \
            (IsLSIntersection(p1.y + p1.bg_r_minx, p1.y + p1.bg_r_maxx, p2.y + p2.bg_l_minx, p2.y + p2.bg_l_maxx) == 1):
        # 层板与侧板接触，层板是横纹，侧板是竖纹
        for i in range(0, len(p1.bhpt)):
            bhp = p1.bhpt[i]
            if bhp.hdirect == 'R':
                if bhp.face == 'FaceA':
                    smallcap = bhp.hole_z
                else:
                    smallcap = p1.gh - bhp.hole_z
                x = p1.z - p2.z + smallcap
                y = p1.y - p2.y + Delphi_Round(bhp.y) + p1.bg_r_minx
                if p1.isxx == 2:  # 前后斜
                    angle = -p1.var_args[0] * math.pi / 180
                    ll = bhp.y
                    x = p1.z - p2.z + smallcap + Delphi_Round(ll * math.sin(angle))
                    y = p1.y - p2.y + p1.bg_r_minx + Delphi_Round(ll * math.cos(angle))
                if p1.isxx == 1:  # 左右斜
                    angle = p1.var_args[0] * math.pi / 180
                    ll = p1.gl
                    x = p1.z - p2.z + smallcap + Delphi_Round(ll * math.sin(angle))
                p2.big_p = p1
                MakeVector(ho.i_offset, 0, bhp.y - int(bhp.y), 0)
                ho.wx = p1.gl
                ho.wy = int(bhp.y)
                ho.wz = smallcap
                if (bhp.sri != '') and (bhp.sri != '0'):
                    AddHole_A(None, p2, p1, ho, IdentityHmgMatrix, y, x, 0, -1, 0,
                              bhp.hole_z, 0, 'Right', 'I', bhp.sri, '', '')
                for j in range(1, bhp.holenum_y):
                    p2.big_p = p1
                    ho.wy = int(bhp.y) + bhp.hole_ycap * j
                    if (bhp.sri != '') and bhp.sri != '0':
                        AddHole_A(None, p2, p1, ho, IdentityHmgMatrix, y + bhp.hole_ycap * j,
                                  x, 0, -1, 0, bhp.hole_z, 0, 'Right', 'I', bhp.sri, '', '')
    if (di1 in [2, 3]) and (di2 in [4, 6]) and (p1.y >= p2.y) and (p1.y + p1.gp <= p2.y + p2.gp) and \
            (IsLSIntersection(p1.z + p1.bg_r_miny, p1.z + p1.bg_r_maxy, p2.z + p2.bg_l_miny, p2.z + p2.bg_l_maxy) == 1):
        # 背板与侧板接触， 背板竖纹， 侧板竖纹
        for i in range(0, len(p1.bhpt)):
            bhp = p1.bhpt[i]
            if bhp.hdirect == 'R':
                if bhp.face == 'FaceA':
                    smallcap = bhp.hole_z
                else:
                    smallcap = p1.gp - bhp.hole_z
                x = p1.z - p2.z + Delphi_Round(bhp.y) + p1.bg_r_miny
                y = p1.y - p2.y + smallcap
                p2.big_p = p1
                MakeVector(ho.i_offset, 0, 0, bhp.y - int(bhp.y))
                ho.wx = p1.gl
                ho.wy = smallcap
                ho.wz = int(bhp.y)
                if (bhp.sri != '') and (bhp.sri != '0'):
                    AddHole_A(None, p2, p1, ho, IdentityHmgMatrix, y, x, 0, -1, 0,
                              bhp.hole_z, 0, 'Right', 'I', bhp.sri, '', '')
                for j in range(1, bhp.holenum_y):
                    p2.big_p = p1
                    ho.wz = int(bhp.y) + bhp.hole_ycap * j
                    if (bhp.sri != '') and (bhp.sri != '0'):
                        AddHole_A(None, p2, p1, ho, IdentityHmgMatrix, y, x + bhp.hole_ycap * j, 0, -1,
                                  0, bhp.hole_z, 0, 'Right', 'I', bhp.sri, '', '')
def CalcBdxmlHole_UpFace(p1, p2):
    ho = hole()
    di1 = p1.direct
    di2 = p2.direct
    if Delphi_not(di1) in [1, 2, 3, 4, 5, 6]: di1 = 1
    if Delphi_not(di2) in [1, 2, 3, 4, 5, 6]: di2 = 1
    ho.p1 = p1
    ho.p2 = p2
    # if len(mHPInfoList) ==2932:
    #     print di1,di2,p1.x,p2.x,p1.x + p1.gl,p2.x + p2.gl,IsLSIntersection(p1.y + p1.bg_u_miny, p1.y + p1.bg_u_maxy, p2.y + p2.bg_d_miny, p2.y + p2.bg_d_maxy)
    if di1 in [4, 6] and di2 in [1, 5] and (p1.x >= p2.x) \
            and (p1.x + p1.gl <= p2.x + p2.gl) and \
            (IsLSIntersection(p1.y + p1.bg_u_miny, p1.y + p1.bg_u_maxy, p2.y + p2.bg_d_miny, p2.y + p2.bg_d_maxy) == 1):
        # 中立板与顶板接触，中立板是竖纹，底板横纹
        for i in range(0, len(p1.bhpt)):
            bhp = p1.bhpt[i]
            if bhp.hdirect == 'U':
                if bhp.face == 'FaceA':
                    smallcap = bhp.hole_z
                else:
                    smallcap = p1.gl - bhp.hole_z
                x = p1.x - p2.x + smallcap
                y = p1.y - p2.y + Delphi_Round(bhp.x) + p1.bg_u_miny
                p2.big_p = p1
                MakeVector(ho.i_offset, 0, bhp.x - int(bhp.x), 0)
                ho.wx = smallcap
                ho.wy = int(bhp.x)
                ho.wz = p1.gh
                if (bhp.sri != '') and (bhp.sri != '0'):
                    AddHole_A(None, p2, p1, ho, IdentityHmgMatrix, x, y, 0, -1, 0,
                              bhp.hole_z, 0, 'Up', 'I', bhp.sri, '', '')
                for j in range(1, bhp.holenum_x):
                    p2.big_p = p1
                    ho.wy = int(bhp.x) + bhp.hole_xcap * j
                    if (bhp.sri != '') and bhp.sri != '0':
                        AddHole_A(None, p2, p1, ho, IdentityHmgMatrix, x, y + bhp.hole_xcap * j,
                                   0, -1, 0, bhp.hole_z, 0, 'Up', 'I', bhp.sri, '', '')
    if (di1 in [2, 3]) and (di2 in [1, 5]) and (p1.y >= p2.y) and (p1.y + p1.gp <= p2.y + p2.gp) and \
            (IsLSIntersection(p1.x + p1.bg_u_minx, p1.x + p1.bg_u_maxx, p2.x + p2.bg_d_minx, p2.x + p2.bg_d_maxx) == 1):
        # 背板与顶板接触，背板竖纹，顶板横纹
        #print '6666666666',len(p1.bhpt)
        for i in range(0, len(p1.bhpt)):
            bhp = p1.bhpt[i]
            if bhp.hdirect == 'U':
                if bhp.face == 'FaceA':
                    smallcap = bhp.hole_z
                else:
                    smallcap = p1.gp - bhp.hole_z
                x = p1.x - p2.x + Delphi_Round(bhp.x) + p1.bg_u_minx
                y = p1.y - p2.y + smallcap
                p2.big_p = p1
                MakeVector(ho.i_offset, bhp.x - int(bhp.x), 0,0 )
                ho.wx = int(bhp.x)
                ho.wy = smallcap
                ho.wz = p1.gh
                #print 'bhp.sri=',bhp.sri
                if (bhp.sri != '') and (bhp.sri != '0'):
                    AddHole_A(None, p2, p1, ho, IdentityHmgMatrix, x, y,  0, -1, 0,
                              bhp.hole_z, 0, 'Up', 'I', bhp.sri, '', '')
                for j in range(1, bhp.holenum_x):
                    p2.big_p = p1
                    t = x + bhp.hole_xcap * j
                    ho.wx = int(bhp.x) + bhp.hole_xcap * j
                    if (bhp.sri != '') and (bhp.sri != '0'):
                        AddHole_A(None, p2, p1, ho, IdentityHmgMatrix, t, y, 0, -1,
                                  0, bhp.hole_z, 0, 'Up', 'I', bhp.sri, '', '')
def CalcBdxmlHole_BackFace(p1, p2):
    ho = hole()
    di1 = p1.direct
    di2 = p2.direct
    if Delphi_not(di1) in [1, 2, 3, 4, 5, 6]: di1 = 1
    if Delphi_not(di2) in [1, 2, 3, 4, 5, 6]: di2 = 1
    ho.p1 = p1
    ho.p2 = p2
    if di1 in [4, 6] and di2 in [2, 3] and (p1.x >= p2.x) \
            and (p1.x + p1.gl <= p2.x + p2.gl) and \
            (IsLSIntersection(p1.z + p1.bg_b_miny, p1.z + p1.bg_b_maxy, p2.z + p2.bg_f_miny, p2.z + p2.bg_f_maxy) == 1):
        # 侧板与背板接触，侧板竖纹，背板竖纹
        for i in range(0, len(p1.bhpt)):
            bhp = p1.bhpt[i]
            if bhp.hdirect == 'L':
                if bhp.face == 'FaceA':
                    smallcap = bhp.hole_z
                else:
                    smallcap = p1.gl - bhp.hole_z
                x = p1.x - p2.x + smallcap
                y = p1.z - p2.z + Delphi_Round(bhp.y) + p1.bg_b_miny
                p2.big_p = p1
                MakeVector(ho.i_offset, 0,  0,bhp.y - int(bhp.y))
                ho.wx = smallcap
                ho.wy = 0
                ho.wz = int(bhp.y)
                if (bhp.sri != '') and (bhp.sri != '0'):
                    AddHole_B(None, p2, p1, ho, IdentityHmgMatrix, x, y, 0, -1, 0,
                              bhp.hole_z, 0, 'Back', 'I', bhp.sri, '', '')
                for j in range(1, bhp.holenum_y):
                    ty = y + bhp.hole_ycap * j
                    p2.big_p = p1
                    ho.wz = int(bhp.y) + bhp.hole_ycap * j
                    if (bhp.sri != '') and bhp.sri != '0':
                        AddHole_B(None, p2, p1, ho, IdentityHmgMatrix, x, ty,
                                  0, -1, 0, bhp.hole_z, 0, 'Back', 'I', bhp.sri, '', '')
    if (di1 in [1, 5]) and (di2 in [2, 3]) and (p1.z >= p2.z) and (p1.z + p1.gh <= p2.z + p2.gh) and \
            (IsLSIntersection(p1.x + p1.bg_b_minx, p1.x + p1.bg_b_maxx, p2.x + p2.bg_f_minx, p2.x + p2.bg_f_maxx) == 1):
        # 背板与底板接触，背板竖纹，底板横纹
        for i in range(0, len(p1.bhpt)):
            bhp = p1.bhpt[i]
            if bhp.hdirect == 'D':
                if bhp.face == 'FaceA':
                    smallcap = bhp.hole_z
                else:
                    smallcap = p1.gh - bhp.hole_z
                x = p1.z - p2.z + smallcap
                y = p1.x - p2.x + Delphi_Round(bhp.x) + p1.bg_b_minx
                p2.big_p = p1
                MakeVector(ho.i_offset, bhp.x - int(bhp.x), 0, 0)
                ho.wx = int(bhp.x)
                ho.wy = 0
                ho.wz = smallcap
                if (bhp.sri != '') and (bhp.sri != '0'):
                    AddHole_B(None, p2, p1, ho, IdentityHmgMatrix, y, x, 0, -1, 0,
                              bhp.hole_z, 0, 'Back', 'I', bhp.sri, '', '')
                for j in range(1, p1.bhpt[i].holenum_x):
                    ty = y + bhp.hole_xcap * j
                    p2.big_p = p1
                    ho.wx = int(bhp.x) + bhp.hole_xcap * j
                    if (bhp.sri != '') and (bhp.sri != '0'):
                        AddHole_B(None, p2, p1, ho, IdentityHmgMatrix, ty, x, 0, -1,
                                  0, bhp.hole_z, 0, 'Back', 'I', bhp.sri, '', '')
def CalcBdxmlHole_DownFace(p1, p2):
    ho = hole()
    di1 = p1.direct
    di2 = p2.direct
    if Delphi_not(di1) in [1, 2, 3, 4, 5, 6]: di1 = 1
    if Delphi_not(di2) in [1, 2, 3, 4, 5, 6]: di2 = 1
    ho.p1 = p1
    ho.p2 = p2
    if di1 in [4, 6] and di2 in [1, 5] and (p1.x >= p2.x) \
            and (p1.x + p1.gl <= p2.x + p2.gl) and \
            (IsLSIntersection(p1.y + p1.bg_d_miny, p1.y + p1.bg_d_maxy, p2.y + p2.bg_u_miny, p2.y + p2.bg_u_maxy) == 1):
        # 中立板与底板接触，中立板是竖纹，底板横纹
        for i in range(0, len(p1.bhpt)):
            bhp = p1.bhpt[i]
            if bhp.hdirect == 'D':
                if bhp.face == 'FaceA':
                    smallcap = bhp.hole_z
                else:
                    smallcap = p1.gl - bhp.hole_z
                x = p1.x - p2.x + smallcap
                y = p1.y - p2.y + Delphi_Round(bhp.x) + p1.bg_u_miny
                p2.big_p = p1
                MakeVector(ho.i_offset, 0, bhp.x - int(bhp.x), 0)
                ho.wx = smallcap
                ho.wy = int(bhp.x)
                ho.wz = 0
                if (bhp.sri != '') and (bhp.sri != '0'):
                    AddHole_B(None, p2, p1, ho, IdentityHmgMatrix, x, y, 0, -1, 0,
                              bhp.hole_z, 0, 'Down', 'I', bhp.sri, '', '')
                for j in range(1, bhp.holenum_x):
                    p2.big_p = p1
                    ho.wy = int(bhp.x) + bhp.hole_xcap * j
                    if (bhp.sri != '') and bhp.sri != '0':
                        AddHole_B(None, p2, p1, ho, IdentityHmgMatrix, x, y + bhp.hole_xcap * j,
                                   0, -1, 0, bhp.hole_z, 0, 'Down', 'I', bhp.sri, '', '')
    if (di1 in [2, 3]) and (di2 in [1, 5]) and (p1.y >= p2.y) and (p1.y + p1.gp <= p2.y + p2.gp) and \
            (IsLSIntersection(p1.x + p1.bg_d_minx, p1.x + p1.bg_d_maxx, p2.x + p2.bg_u_minx, p2.x + p2.bg_u_maxx) == 1):
        # 背板与底板接触，背板竖纹，底板横纹
        for i in range(0, len(p1.bhpt)):
            bhp = p1.bhpt[i]
            if bhp.hdirect == 'D':
                if bhp.face == 'FaceA':
                    smallcap = bhp.hole_z
                else:
                    smallcap = p1.gp - bhp.hole_z
                x = p1.x - p2.x + Delphi_Round(bhp.x) + p1.bg_d_minx
                y = p1.y - p2.y + smallcap
                p2.big_p = p1
                MakeVector(ho.i_offset, bhp.x - int(bhp.x), 0,0 )
                ho.wx = int(bhp.x)
                ho.wy = smallcap
                ho.wz = 0
                if (bhp.sri != '') and (bhp.sri != '0'):
                    AddHole_B(None, p2, p1, ho, IdentityHmgMatrix, x, y,  0, -1, 0,
                              bhp.hole_z, 0, 'Down', 'I', bhp.sri, '', '')
                for j in range(1, bhp.holenum_x):
                    p2.big_p = p1
                    t = x + bhp.hole_xcap * j
                    ho.wx = int(bhp.x) + bhp.hole_xcap * j
                    if (bhp.sri != '') and (bhp.sri != '0'):
                        AddHole_A(None, p2, p1, ho, IdentityHmgMatrix, t, y, 0, -1,
                                  0, bhp.hole_z, 0, 'Down', 'I', bhp.sri, '', '')
def UpdateCalcItemResult(p, p2):
    for i in range(0,101):
        p.ahole_index[i] = p2.ahole_index[i]
        p.bhole_index[i] = p2.bhole_index[i]
    for i in range(0,101):
        p.akc_index[i] = p2.akc_index[i]
        p.bkc_index[i] = p2.bkc_index[i]
    p.kcconig_flag = p2.kcconig_flag
def UpdateTempExpVariable(p):
    mTmpExp['CA'] = p.var_args[0]
    mTmpExp['CB'] = p.var_args[1]
    mTmpExp['CC'] = p.var_args[2]
    mTmpExp['CD'] = p.var_args[3]
    mTmpExp['CE'] = p.var_args[4]
    mTmpExp['CF'] = p.var_args[5]
    mTmpExp['CG'] = p.var_args[6]
    mTmpExp['CH'] = p.var_args[7]
    mTmpExp['CI'] = p.var_args[8]
    mTmpExp['CJ'] = p.var_args[9]
    mTmpExp['CK'] = p.var_args[10]
    mTmpExp['CL'] = p.var_args[11]
    mTmpExp['CM'] = p.var_args[12]
    mTmpExp['CN'] = p.var_args[13]
    mTmpExp['CO'] = p.var_args[14]
    mTmpExp['CP'] = p.var_args[15]
def CalcHole_LeftFace(p1, p2 ,c):
    global mHoleRow
    """
    :rtype: object
    """
    ho = hole()
    nocalc = False
    if (c == None) or ((c.iscalc == 0) and (p1.is_calc_holeconfig[0] != 1)) or \
            ((c.iscalc == 1) and (p1.is_calc_holeconfig[0] == 2)):
        # 'nocalc'
        ## 'c.iscalc=',c.iscalc,'p1.is_calc_holeconfig[0]=',p1.is_calc_holeconfig[0],'c.iscalc=',c.iscalc,'p1.is_calc_holeconfig[0]',p1.is_calc_holeconfig[0]
        nocalc = True
    di1 = p1.direct
    di2 = p2.direct
    if not di1 in [1, 2, 3, 4, 5, 6]: di1 = 1
    if not di2 in [1, 2, 3, 4, 5, 6]: di2 = 1
    algorithm = 0
    if (c != None): algorithm = c.algorithm
    ho.p1 = p1
    ho.p2 = p2
    hc = 0
    face = 0
    l = 0
    if (((di1 in [1,5]) and (di2 in [4,6])) or ((algorithm == 2) and (di1 in [1,5]) and \
        (di2 in [1,5]))) and (p1.z >= p2.z) and (p1.z +p1.gh <= p2.z+p2.gh) and \
            (IsLSIntersection(p1.y +p1.bg_l_minx, p1.y+p1.bg_l_maxx, p2.y+p2.bg_r_minx, p2.y+p2.bg_r_maxx) ==1):
        # if len(mHPInfoList) == 978:
        #     print '66666'
        #
        #     print di1, di2, algorithm, p1.z, p2.z, p1.gh, p2.gh, p1.y + p1.bg_l_minx, p1.y + p1.bg_l_maxx, p2.y + p2.bg_r_minx, p2.y + p2.bg_r_maxx
        #     print IsLSIntersection(p1.y + p1.bg_l_minx, p1.y + p1.bg_l_maxx, p2.y + p2.bg_r_minx, p2.y + p2.bg_r_maxx),nocalc
        #     exit(1)
        if nocalc :
            return
        offset = 0
        if algorithm == 1: #按接触面计算
            if p2.gp + p2.y>p2.y : t = p2.y
            else: t = p2.gp+p2.y
            if t > p1.y: offset = t-p1.y
        UpdateTempExpVariable(p1)
        l = Length_HoleFace(p1, p2, c, 1, 0) #// 左面1, // 右面2, // 下面3, // 上面4, // 后面5, // 前面6
        if c.algorithm == 0:
            t = (p1.bg_l_maxx + p1.y) - (p2.gp + p2.y)
            if (t > 0) and c.calctype in [0,1] : l = l - t    #接触面积较小
            if p1.zero_y == 4:
                t = (p1.bg_l_minx + p1.y) - p2.y
                if t < 0 and (c.calctype in [0,1]): l =l+t  #接触面较小
        mTmpExp['L'] = l
        hc = int(SimpleExpressToValue(c.holecap,2,mTmpExp))
        # 'l='+str(l)+'c.holecap=',c.holecap,'hc=',hc,'c.id=',c.id
        chc = int(SimpleExpressToValue(c.center_holecap,2,mTmpExp))
        # 'c.l_isoutput=',c.l_isoutput
        if c.l_isoutput == 1:
            mHoleRow = mHoleRow + 1
            if c.calctype == 0 or c.calctype == 1:
                p1.holeconfig_flag = c.flag
                for i in range(0,c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    x = c.l_holedepth
                    y = c.l_bigcap + hc * i +p1.bg_l_minx
                    if c.ismirror ==1 : y = p1.bg_l_maxx - (c.l_bigcap + hc*i)
                    if i == 0: t =1
                    else: t= hc
                    if (c.bigface == 0) or ((c.bigface ==2) and (p1.holeface in [0,1,3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0,2,3])):
                        face = 0
                        p1.big_p = None
                        #(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_LeftFace1')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, x, y+offset, c.l_holedepth, c.id, t, c.l_smallcap, \
                                  hc, 'Left', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])): #//B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        #(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_LeftFace2')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc, 'Left', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
            if c.calctype == 2 : #// // 前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round(p1.gp - hc*(c.holenum -1)) /2
                for i in range(0,int(c.holenum//2)):  #前后端等距
                    mx_flag = -1
                    if i==0: mx_flag = 0
                    x = c.l_holedepth
                    y = l_bigcap + hc*i +p1.bg_l_minx
                    if (c.bigface == 0) or ((c.bigface ==2) and (p1.holeface in [0,1,3])) or \
                            ((c.bigface==3) and (p1.holeface in [0,2,3])): #A面内测外侧
                        face = 0
                        p1.big_p = None
                        #///(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_LeftFace3')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, x, y+offset, c.l_holedepth, c.id,
                                    t, c.l_smallcap, hc, 'Left', 'L', c.l_bigname, c.l_smallname,
                                    c.i_name, mx_flag, 0, c.mx_cap)
                    if (c.bigface ==1 ) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface ==3) and (p1.holeface in [1])):  #B面， 内测， 外侧
                        face = 1
                        p1.big_p = None
                        #///(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_LeftFace4')
                        AddHole_B(c, p1, p2,ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth,
                                  c.id, t, c.l_smallcap, hc, 'Left', 'L', c.l_bigname, c.l_smallname,
                                  c.i_name, mx_flag, 0, c.mx_cap)
                for i in range(0,int(c.holenum//2)):
                    mx_flag = -1
                    if i == 0: mx_flag =1
                    x = c.l_holedepth
                    y = p1.bg_l_maxx - (l_bigcap + hc*i)
                    if (c.bigface == 0) or ((c.bigface==2) and (p1.holeface in [0,1,3]))    \
                        or ((c.bigface == 3 ) and (p1.holeface in [0,2,3])): #B面，内测， 外侧
                        face = 0
                        p1.big_p = None
                        #///(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_LeftFace5')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, x, y+offset, c.l_holedepth, c.id, t, c.l_smallcap,
                        hc, 'Left', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
                    if (c.bigface ==1 ) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface ==3) and (p1.holeface in [1])):  #B面， 内测， 外侧
                        face = 1
                        p1.big_p = None
                        #///(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_LeftFace6')
                        AddHole_B(c, p1, p2,ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth,
                                  c.id, t, c.l_smallcap, hc, 'Left', 'L', c.l_bigname, c.l_smallname,
                                  c.i_name, mx_flag, 0, c.mx_cap)
                #中心孔
                cstart = p1.bg_l_minx +(p1.bg_l_maxx - p1.bg_l_minx) // 2 +((c.center_holenum - 1) %2)*(chc//2)
                if ((c.center_holenum) // 2) > 0 :
                    cstart = cstart - ((c.center_holenum) // 2)*chc
                for i in range(0,c.center_holenum):
                    x = c.l_holedepth
                    y = cstart + chc * i
                    if (c.bigface == 0) or ((c.bigface==2) and (p1.holeface in [0,1,3])) or    \
                            ((c.bigface ==3 ) and (p1.holeface in [0,2,3])):    #A面，内测， 外侧
                        face = 0
                        p1.big_p = None
                        #///(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_LeftFace7')
                        AddHole_A(c, p1,
                                  p2,  ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc, 'Left', 'L', c.l_bigname, c.l_smallname, c.i_name)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])): #// B面，内侧，外侧
                        face=1
                        p1.big_p = None
                        #///(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_LeftFace8')
                        AddHole_B(c, p1,p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t,
                                  c.l_smallcap, hc, 'Left', 'L', c.l_bigname, c.l_smallname, c.i_name)
        if (c.i_isoutput == 1) and (algorithm in [0, 1]) : #// 纹理面
            mHoleRow = mHoleRow + 1
            if face == 0:
                smallcap = c.l_smallcap
            else:
                smallcap = p1.gh - c.l_smallcap
            if (c.calctype == 0) or (c.calctype == 1): #靠背对齐； 靠背对齐- 三排孔
                p2.holeconfig_flag = c.flag2
                p2.hole_back_cap = p1.y - p2.y +c.l_bigcap + p1.bg_l_minx
                p2.hole_2_dist = hc
                for i in range(0,c.holenum):
                    mx_flag = -1
                    if i==0 : mx_flag = 0
                    if i==c.holenum - 1 : mx_flag = 1
                    ho.mx_x = 0
                    if mx_flag == 0: ho.mx_y = c.mx_cap
                    else: ho.mx_y = -c.mx_cap
                    ho.mx_z = 0
                    x = p1.z - p2.z + smallcap
                    y = p1.y - p2.y +c.l_bigcap + hc*i+p1.bg_l_minx
                    if p1.isxx == 2: #前后斜
                        angle = -p1.var_args[0]*math.pi/180
                        ll = c.l_bigcap + hc * i
                        x = p1.z - p2.z +smallcap + Delphi_Round(ll*sin(angle))
                        y = p1.y - p2.y +p1.bg_l_minx + Delphi_Round(ll*math.cos(angle))
                    if p1.isxx == 1: #左右斜
                        pass
                    if c.ismirror == 1: y = p1.bg_l_maxx - (c.l_bigcap + hc*i) + p1.y - p2.y #镜像
                    if i ==0:
                        t = 1
                    else:
                        t = hc
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, c.i_offsetvalue, 0)
                    ho.wx = 0
                    ho.wy = c.l_bigcap + hc * i + p1.bg_l_minx + offset
                    if c.ismirror ==1: ho.wy = p1.bg_l_maxx - c.l_bigcap - hc * i+offset
                    ho.wz = smallcap
                    #///(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_LeftFace9')
                    AddHole_B(c, p2,p1, ho, IdentityHmgMatrix, y + offset, x, 0, c.id, t, c.l_smallcap, hc,
                              'Left', 'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
                    if c.calctype == 1 :
                        #///(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_LeftFace10')
                        AddHole_B(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(0, 0,c.pkcap)), y + offset,
                                  x + c.pkcap, 0, c.id, t, c.l_smallcap, hc, 'Left', 'I', c.i_name, '', c.i_name,
                                  mx_flag, c.mx_cap, 0)
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_LeftFace11')
                        #// ho.wz:= smallcap - c.pkcap;
                        AddHole_B(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(0, 0,-c.pkcap)), y + offset,
                                  x - c.pkcap, 0, c.id, t, c.l_smallcap, hc, 'Left', 'I', c.i_name, '', c.i_name,
                                  mx_flag, c.mx_cap, 0)
            if c.calctype==2:
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round((p1.gp - hc*(c.holenum -1))/2)
                for i in range(0, int(c.holenum//2)):
                    mx_flag = -1
                    if i==0:    mx_flag = 0
                    ho.mx_x = 0
                    if mx_flag == 0:    ho.mx_y = c.mx_cap
                    else: ho.mx_y = -c.mx_cap
                    ho.mx_z = 0
                    x = p1.z - p2.z + smallcap
                    y = p1.y - p2.y +l_bigcap +hc*i +p1.bg_l_minx
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, c.i_offsetvalue, 0)
                    ho.wx = 0
                    ho.wy = l_bigcap + hc * i + p1.bg_l_minx + offset
                    ho.wz = smallcap
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_LeftFace12')
                    AddHole_B(c, p2,
                              p1, ho, IdentityHmgMatrix, y + offset, x, 0, c.id, t, c.l_smallcap, hc,
                              'Left', 'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
                for i in range(0,int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    ho.mx_x = 0
                    if mx_flag == 0: ho.mx_y = c.mx_cap
                    else: ho.mx_y = -c.mx_cap
                    ho.mx_z = 0
                    x = p1.z - p2.z + smallcap
                    y = p1.y - p2.y + (p1.bg_l_maxx - (l_bigcap + hc*i))
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, c.i_offsetvalue, 0)   #???
                    ho.wx = 0
                    ho.wy = (p1.bg_l_maxx - (l_bigcap + hc * i)) + offset
                    ho.wz = smallcap
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_LeftFace13')
                    AddHole_B(c, p2, p1, ho, IdentityHmgMatrix, y + offset, x, 0, c.id, t, c.l_smallcap,
                              hc, 'Left', 'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
                #中心孔
                cstart = p1.bg_l_minx + (p1.bg_l_maxx - p1.bg_l_minx)//2 + ((c.center_holenum -1) %2)*(chc//2)
                if ((c.center_holenum) //2) >0: cstart = cstart - ((c.center_holenum)//2)*chc
                for i in range(0,c.center_holenum):
                    x = p1.z - p2.z + smallcap
                    y = p1.y - p2.y + cstart + chc * i
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, c.i_offsetvalue, 0)
                    ho.wx = 0
                    ho.wy = cstart + chc * i + offset
                    ho.wz = smallcap
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_LeftFace14')
                    AddHole_B(c, p2,p1, ho, IdentityHmgMatrix, y + offset, x, 0, c.id, t, c.l_smallcap,
                              hc, 'Left', 'I', c.i_name, '', c.i_name)
    if (((di1 in [2, 3]) and (di2 in [4, 6])) or ((algorithm==2) and (di1 in [2, 3]) and (di2 in [2, 3]))) and \
        (p1.y >= p2.y) and (p1.y + p1.gp <= p2.y + p2.gp) and \
        (IsLSIntersection(p1.z + p1.bg_l_miny, p1.z + p1.bg_l_maxy, p2.z + p2.bg_r_miny, p2.z + p2.bg_r_maxy)==1):
        #背板与侧板接触，背板竖纹，侧板竖纹
        if nocalc : return
        # '123456'
        offset = 0
        if algorithm == 1:
            #按接触面计算
            if p2.gh + p2.z > p2.z: t = p2.z
            else: t = p2.gh+p2.z
            if t > p1.z : offset=t - p1.z
        UpdateTempExpVariable(p1)
        l = Length_HoleFace(p1, p2, c, 1, 1) #// 左面1, // 右面2, // 下面3, // 上面4, // 后面5, // 前面6
        if c.algorithm==0:  #// 兼容算法
            t = (p1.bg_l_maxy + p1.z) - (p2.gh + p2.z)
            if (t>0) and (c.calctype in [0,1]): l = l - t    #接触面较小
            if p1.zero_y == 6:    #上封边
                t = (p1.bg_l_miny+p1.z) - p2.z
                if (t < 0) and (c.calctype in [0,1]): l = l+t    #接触面较小
        mTmpExp['L'] = l
        hc = int(SimpleExpressToValue(c.holecap, 2, mTmpExp))
        chc = int(SimpleExpressToValue(c.center_holecap, 2, mTmpExp))
        if c.l_isoutput == 1:
            mHoleRow = mHoleRow + 1
            if (c.calctype == 0) or (c.calctype == 1):
                p1.holeconfig_flag = c.flag
                for i in range(0,c.holenum):
                    mx_flag = -1
                    if i==0: mx_flag = 0
                    if i==c.holenum-1: mx_flag = 1
                    x = c.l_holedepth
                    y = c.l_bigcap + hc * i +p1.bg_l_miny
                    if c.ismirror == 1: y = p1.bg_l_maxy - (c.l_bigcap + hc * i) #镜像
                    if i==0: t = 1
                    else: t = hc
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0,1,3])) or \
                        ((c.bigface==3) and (p1.holeface in [0,2,3])): #A面， 内测， 外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_LeftFace15')
                        AddHole_A(c, p1,
                              p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t, c.l_smallcap, hc,
                                'Left', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])): #B面， 内测， 外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_LeftFace16')
                        AddHole_B(c, p1,
                                  p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc, 'Left', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
            if c.calctype == 2:
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0 : l_bigcap = Delphi_Round((p1.gh - hc * (c.holenum - 1)) / 2)
                for i in range(0,int(c.holenum//2)):
                    mx_flag= -1
                    if i==0 : mx_flag=0
                    x= c.l_holedepth
                    y= l_bigcap + hc * i + p1.bg_l_miny
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3]))    \
                        or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])): #// A面，内侧，外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_LeftFace17')
                        AddHole_A(c, p1,
                                  p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t, c.l_smallcap, hc,
                                    'Left', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2]))\
                                or ((c.bigface == 3) and (p1.holeface in [1])):# //B面，内侧，外侧
                        face= 1
                        p1.big_p= None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_LeftFace18')
                        AddHole_B(c, p1,p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t, c.l_smallcap, hc,
                                    'Left', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i==0 : mx_flag =1
                    x= c.l_holedepth
                    y= p1.bg_l_maxy - (l_bigcap + hc * i)
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                        or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])): #// A面，内侧，外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_LeftFace19')
                        AddHole_A(c, p1,
                                  p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t, c.l_smallcap, hc, 'Left',
                                    'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2]))    \
                        or ((c.bigface == 3) and (p1.holeface in [1])): #// B面，内侧，外侧
                        face= 1
                        p1.big_p= None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_LeftFace20')
                        AddHole_B(c, p1,
                                  p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t, c.l_smallcap, hc,
                        'Left', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
                #中心孔
                cstart = p1.bg_l_miny + (p1.bg_l_maxy - p1.bg_l_miny) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0 : cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0,c.center_holenum):
                    x = c.l_holedepth
                    y = cstart + chc * i
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3]))\
                        or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])): #// A面，内侧，外侧
                        face= 0
                        p1.big_p= None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_LeftFace21')
                        AddHole_A(c, p1,
                                  p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t, c.l_smallcap, hc, 'Left',
                                  'L', c.l_bigname, c.l_smallname, c.i_name)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2]))    \
                        or ((c.bigface == 3) and (p1.holeface in [1])): #// B面，内侧，外侧
                        face= 1
                        p1.big_p= None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_LeftFace22')
                        AddHole_B(c, p1,
                                  p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t, c.l_smallcap, hc, 'Left',
                                    'L', c.l_bigname, c.l_smallname, c.i_name)
        if (c.i_isoutput == 1) and (algorithm in [0,1]):
            mHoleRow = mHoleRow +1
            if face == 0: smallcap = c.l_smallcap
            else: smallcap = p1.gp - c.l_smallcap
            if (c.calctype == 0) or (c.calctype == 1): #靠背对齐
                p2.holeconfig_flag = c.flag2
                p2.hole_back_cap = p1.z - p2.z + c.l_bigcap
                p2.hole_2_dist = hc
                for i in range(0,c.holenum):
                    mx_flag = -1
                    if i==0 : mx_flag = 0
                    if i==c.holenum - 1 : mx_flag=1
                    ho.mx_x = 0
                    ho.mx_y = 0
                    if mx_flag==0 : ho.mx_z=c.mx_cap
                    else: ho.mx_z= -c.mx_cap
                    x= p1.z - p2.z + c.l_bigcap + hc * i + p1.bg_l_miny
                    y= p1.y - p2.y + smallcap
                    if c.ismirror == 1 : x=p1.bg_l_maxy - (c.l_bigcap + hc * i) + p1.z - p2.z #// 镜像
                    if i == 0 : t= 1
                    else: t= hc
                    p2.big_p= p1
                    MakeVector(ho.i_offset, 0, 0, c.i_offsetvalue)
                    ho.wx= 0
                    ho.wy= smallcap
                    ho.wz= c.l_bigcap + hc * i + p1.bg_l_miny + offset
                    if c.ismirror == 1 : ho.wz=p1.bg_l_maxy - c.l_bigcap + hc * i + offset
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_LeftFace23')
                    AddHole_B(c, p2,p1, ho, IdentityHmgMatrix, y, x + offset, 0, c.id, t,
                              c.l_smallcap, hc, 'Left', 'I', c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap)
                    if c.calctype == 1:
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_LeftFace24')
                        AddHole_B(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(0, c.pkcap,
                            0)), y + c.pkcap, x + offset, 0, c.id, t, c.l_smallcap, hc, 'Left', 'I', c.i_name, '',
                                  c.i_name, mx_flag, 0, c.mx_cap)
                        #// ho.wy:= smallcap - c.pkcap;
                        AddHole_B(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(0, -c.pkcap,
                                0)), y - c.pkcap, x + offset, 0, c.id, t, c.l_smallcap, hc, 'Left',
                                  'I', c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap)
            if c.calctype == 2 :
                t= 0
                l_bigcap= c.l_bigcap
                if l_bigcap <= 0 : l_bigcap=Delphi_Round((p1.gh - hc * (c.holenum - 1)) / 2)
                for i in range(0,int(c.holenum//2)):
                    mx_flag= -1
                    if i==0 : mx_flag=0
                    ho.mx_x= 0
                    ho.mx_y= 0
                    if mx_flag==0 : ho.mx_z=c.mx_cap
                    else: ho.mx_z= -c.mx_cap
                    x= p1.z - p2.z + l_bigcap + hc * i + p1.bg_l_miny
                    y= p1.y - p2.y + smallcap
                    p2.big_p= p1
                    MakeVector(ho.i_offset, 0, 0, c.i_offsetvalue)#  ???
                    ho.wx= 0
                    ho.wy= smallcap
                    ho.wz= l_bigcap + hc * i + p1.bg_l_miny + offset
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_LeftFace25')
                    AddHole_B(c, p2,p1, ho, IdentityHmgMatrix, y, x + offset, 0, c.id, t,
                              c.l_smallcap, hc, 'Left', 'I', c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    ho.mx_x = 0
                    ho.mx_y = 0
                    if mx_flag == 0:
                        ho.mx_z = c.mx_cap
                    else:
                        ho.mx_z = -c.mx_cap
                    x= p1.z - p2.z + (p1.bg_l_maxy - (l_bigcap + hc * i))
                    y= p1.y - p2.y + smallcap
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, 0, c.i_offsetvalue)  # ???
                    ho.wx = 0
                    ho.wy = smallcap
                    ho.wz= (p1.bg_l_maxy - (l_bigcap + hc * i)) + offset
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_LeftFace26')
                    AddHole_B(c, p2, p1, ho, IdentityHmgMatrix, y, x + offset, 0, c.id, t,
                              c.l_smallcap, hc, 'Left', 'I', c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap)
                #// 中心孔
                cstart= p1.bg_l_miny + (p1.bg_l_maxy - p1.bg_l_miny)//2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0 : cstart=cstart - ((c.center_holenum) // 2) * chc
                for i in range(0,c.center_holenum):
                    x = p1.z - p2.z + cstart + chc * i
                    y = p1.y - p2.y + smallcap
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, 0, c.i_offsetvalue)
                    ho.wx= 0
                    ho.wy= smallcap
                    ho.wz= cstart + chc * i + offset
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_LeftFace27')
                    AddHole_B(c, p2,p1, ho, IdentityHmgMatrix, y, x + offset, 0, c.id, t, c.l_smallcap,
                              hc, 'Left', 'I', c.i_name, '', c.i_name)
def CalcHole_RightFace(p1, p2 ,c):
    global mHoleRow
    ho =hole()
    ## '12333333'
    nocalc = False
    if (c == None) or ((c.iscalc == 0) and (p1.is_calc_holeconfig[1] != 1)) or \
            ((c.iscalc == 1) and (p1.is_calc_holeconfig[1] == 2)):
        nocalc = True
    di1 = p1.direct
    di2 = p2.direct
    if not di1 in [1, 2, 3, 4, 5, 6]: di1 = 1
    if not di2 in [1, 2, 3, 4, 5, 6]: di2 = 1
    algorithm = 0
    if (c != None): algorithm = c.algorithm
    ho.p1 = p1
    ho.p2 = p2
    hc = 0
    face = 0
    l = 0
    if (((di1 in [1, 5]) and (di2 in [4, 6])) or ((algorithm == 2) and (di1 in [1, 5]) and \
                                                  (di2 in [1, 5]))) and (p1.z >= p2.z) and (
            p1.z + p1.gh <= p2.z + p2.gh) and \
            (IsLSIntersection(p1.y + p1.bg_r_minx, p1.y + p1.bg_r_maxx, p2.y + p2.bg_l_minx, p2.y + p2.bg_l_maxx) == 1):
        if nocalc: return
        offset = 0
        if algorithm == 1:  # 按接触面计算
            if p2.gp + p2.y > p2.y:    t = p2.y
            else:    t = p2.gp + p2.y
            if t > p1.y: offset = t - p1.y
        UpdateTempExpVariable(p1)
        l = Length_HoleFace(p1, p2, c, 2, 0)  # // 左面1, // 右面2, // 下面3, // 上面4, // 后面5, // 前面6
        if c.algorithm == 0:
            t = (p1.bg_r_maxx + p1.y) - (p2.gp + p2.y)
            if (t > 0) and c.calctype in [0, 1]: l = l - t  # 接触面积较小
            if p1.zero_y == 4:
                t = (p1.bg_r_minx + p1.y) - p2.y
                if t < 0 and (c.calctype in [0, 1]): l = l + t  # 接触面较小
        ## 'l=',l
        mTmpExp['L'] = l
        ## mTmpExp
        ## c.holecap
        hc = int(SimpleExpressToValue(c.holecap, 2, mTmpExp))
        chc = int(SimpleExpressToValue(c.center_holecap, 2, mTmpExp))
        if c.l_isoutput == 1:
            mHoleRow = mHoleRow + 1
            if c.calctype == 0 or c.calctype == 1:
                p1.holeconfig_flag = c.flag
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    x = p1.gl - c.l_holedepth
                    y = c.l_bigcap + hc * i + p1.bg_r_minx
                    if c.ismirror == 1: y = p1.bg_r_maxx - (c.l_bigcap + hc * i) #镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_RightFace1')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t, c.l_smallcap, \
                                  hc, 'Right', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])):  # //B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_RightFace2')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc, 'Right', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
            if c.calctype == 2:  # // // 前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round(p1.gp - hc * (c.holenum - 1)) / 2
                for i in range(0, int(c.holenum // 2)):  # 前后端等距
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    x = p1.gl - c.l_holedepth
                    y = l_bigcap + hc * i + p1.bg_r_minx
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # A面内测外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_RightFace3')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id,
                                  t, c.l_smallcap, hc, 'Right', 'L', c.l_bigname, c.l_smallname,
                                  c.i_name, mx_flag, 0, c.mx_cap)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])):  # B面， 内测， 外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_RightFace4')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth,
                                  c.id, t, c.l_smallcap, hc, 'Right', 'L', c.l_bigname, c.l_smallname,
                                  c.i_name, mx_flag, 0, c.mx_cap)
                for i in range(0, int(c.holenum //2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    x = p1.gl - c.l_holedepth
                    y = p1.bg_r_maxx - (l_bigcap + hc * i)
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0,2,3])):  # B面，内测， 外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_RightFace5')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc, 'Right', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])):  # B面， 内测， 外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_RightFace6')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth,
                                  c.id, t, c.l_smallcap, hc, 'Right', 'L', c.l_bigname, c.l_smallname,
                                  c.i_name, mx_flag, 0, c.mx_cap)
                # 中心孔
                cstart = p1.bg_r_minx + (p1.bg_r_maxx - p1.bg_r_minx) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0:
                    cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = p1.gl - c.l_holedepth
                    y = cstart + chc * i
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # A面，内测， 外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1,
                                  p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc, 'Right', 'L', c.l_bigname, c.l_smallname, c.i_name)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # // B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t,
                                  c.l_smallcap, hc, 'Right', 'L', c.l_bigname, c.l_smallname, c.i_name)
        if (c.i_isoutput == 1) and (algorithm in [0, 1]):  # // 纹理面
            mHoleRow = mHoleRow + 1
            if face == 0:
                smallcap = c.l_smallcap
            else:
                smallcap = p1.gh - c.l_smallcap
            if (c.calctype == 0) or (c.calctype == 1):  # 靠背对齐； 靠背对齐- 三排孔
                p2.holeconfig_flag = c.flag2
                p2.hole_back_cap = p1.y - p2.y + c.l_bigcap
                p2.hole_2_dist = hc
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    ho.mx_x = 0
                    if mx_flag == 0:
                        ho.mx_y = c.mx_cap
                    else:
                        ho.mx_y = -c.mx_cap
                    ho.mx_z = 0
                    x = p1.z - p2.z + smallcap
                    y = p1.y - p2.y + c.l_bigcap + hc * i + p1.bg_r_minx
                    if p1.isxx == 2:  # 前后斜
                        angle = -p1.var_args[0] * math.pi / 180
                        ll = c.l_bigcap + hc * i
                        x = p1.z - p2.z + smallcap + Delphi_Round(ll * sin(angle))
                        y = p1.y - p2.y + p1.bg_r_minx + Delphi_Round(ll * math.cos(angle))
                    if p1.isxx == 1:  # 左右斜
                        angle= p1.var_args[0] * math.pi / 180
                        ll= p1.gl
                        x= p1.z - p2.z + smallcap + Delphi_Round(ll * math.sin(angle))
                    if c.ismirror == 1: y = p1.bg_r_maxx - (c.l_bigcap + hc * i) + p1.y - p2.y  # 镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, c.i_offsetvalue, 0)
                    ho.wx = p1.gl
                    ho.wy = c.l_bigcap + hc * i + p1.bg_r_minx + offset
                    if c.ismirror == 1: ho.wy = p1.bg_r_maxx - c.l_bigcap - hc * i+offset
                    ho.wz = smallcap
                    # 'c.id=',c.id,'x=',y + offset,'y=',x,'c.i_name=',c.i_name
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, y + offset, x, 0, c.id, t, c.l_smallcap, hc,
                              'Right', 'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
                    #sys.exit(1)
                    # '9999AddHole_A'
                    if c.calctype == 1:   #靠背对齐-三排孔
                        AddHole_A(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(0, 0, c.pkcap)), y + offset,
                                  x + c.pkcap, 0, c.id, t, c.l_smallcap, hc, 'Right', 'I', c.i_name, '', c.i_name,
                                  mx_flag, c.mx_cap, 0)
                        # // ho.wz:= smallcap - c.pkcap;
                        AddHole_A(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(0, 0, -c.pkcap)), y + offset,
                                  x - c.pkcap, 0, c.id, t, c.l_smallcap, hc, 'Right', 'I', c.i_name, '', c.i_name,
                                  mx_flag, c.mx_cap, 0)
            if c.calctype == 2:    #前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round((p1.gp - hc * (c.holenum - 1)) / 2)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0:    mx_flag = 0
                    ho.mx_x = 0
                    if mx_flag == 0:
                        ho.mx_y = c.mx_cap
                    else:
                        ho.mx_y = -c.mx_cap
                    ho.mx_z = 0
                    x = p1.z - p2.z + smallcap
                    y = p1.y - p2.y + l_bigcap + hc * i + p1.bg_r_minx
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, c.i_offsetvalue, 0)
                    ho.wx = p1.gl
                    ho.wy = l_bigcap + hc * i + p1.bg_r_minx + offset
                    ho.wz = smallcap
                    AddHole_A(c, p2,
                              p1, ho, IdentityHmgMatrix, y + offset, x, 0, c.id, t, c.l_smallcap, hc,
                              'Right', 'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    ho.mx_x = 0
                    if mx_flag == 0:
                        ho.mx_y = c.mx_cap
                    else:
                        ho.mx_y = -c.mx_cap
                    ho.mx_z = 0
                    x = p1.z - p2.z + smallcap
                    y = p1.y - p2.y + (p1.bg_r_maxx - (l_bigcap + hc * i))
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, c.i_offsetvalue, 0)  # ???
                    ho.wx = p1.gl
                    ho.wy = (p1.bg_r_maxx - (l_bigcap + hc * i)) + offset
                    ho.wz = smallcap
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, y + offset, x, 0, c.id, t, c.l_smallcap,
                              hc, 'Right', 'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
                # 中心孔
                cstart = p1.bg_r_minx + (p1.bg_r_maxx - p1.bg_r_minx) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0: cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = p1.z - p2.z + smallcap
                    y = p1.y - p2.y + cstart + chc * i
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, c.i_offsetvalue, 0)
                    ho.wx = p1.gl
                    ho.wy = cstart + chc * i + offset
                    ho.wz = smallcap
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, y + offset, x, 0, c.id, t, c.l_smallcap,
                              hc, 'Right', 'I', c.i_name, '', c.i_name)
    if (((di1 in [2, 3]) and (di2 in [4, 6])) or ((algorithm == 2) and (di1 in [2, 3]) and (di2 in [2, 3]))) and \
            (p1.y >= p2.y) and (p1.y + p1.gp <= p2.y + p2.gp) and \
            (IsLSIntersection(p1.z + p1.bg_r_miny, p1.z + p1.bg_r_maxy, p2.z + p2.bg_l_miny, p2.z + p2.bg_l_maxy) == 1):
        # 背板与侧板接触，背板竖纹，侧板竖纹
        if nocalc: return
        offset = 0
        if algorithm == 1:
            # 按接触面计算
            if p2.gh + p2.z > p2.z: t = p2.z
            else: t=p2.gh+p2.z
            if t > p1.z: offset = t - p1.z
        UpdateTempExpVariable(p1)
        l = Length_HoleFace(p1, p2, c, 2, 1)  # // 左面1, // 右面2, // 下面3, // 上面4, // 后面5, // 前面6
        if c.algorithm == 0:  # // 兼容算法
            t = (p1.bg_r_maxy + p1.z) - (p2.gh + p2.z)
            if (t > 0) and (c.calctype in [0, 1]): l = l - t  # 接触面较小
            if p1.zero_y == 6:  # 上封边
                t = (p1.bg_r_miny + p1.z) - p2.z
                if (t < 0) and (c.calctype in [0, 1]): l = l + t  # 接触面较小
        mTmpExp['L'] = l
        hc = int(SimpleExpressToValue(c.holecap, 2, mTmpExp))
        chc = int(SimpleExpressToValue(c.center_holecap, 2, mTmpExp))
        if c.l_isoutput == 1:
            mHoleRow = mHoleRow + 1
            if (c.calctype == 0) or (c.calctype == 1):
                p1.holeconfig_flag = c.flag
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    x = c.l_bigcap + hc * i + p1.bg_r_miny
                    y = p1.gl - c.l_holedepth
                    if c.ismirror == 1: y = p1.bg_r_maxy - (c.l_bigcap + hc * i)  # 镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # A面， 内测， 外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1,
                                  p2, ho, IdentityHmgMatrix, y, x + offset, c.l_holedepth, c.id, t, c.l_smallcap, hc,
                                  'Right', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])):  # B面， 内测， 外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1,
                                  p2, ho, IdentityHmgMatrix, y, x + offset, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc, 'Right', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
            if c.calctype == 2:    #前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round((p1.gh - hc * (c.holenum - 1)) / 2)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    x = l_bigcap + hc * i + p1.bg_r_miny
                    y = p1.gl - c.l_holedepth
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # // A面，内侧，外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1,
                                  p2, ho, IdentityHmgMatrix, y, x + offset, c.l_holedepth, c.id, t, c.l_smallcap, hc,
                                  'Right', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # //B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y, x + offset, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc,'Right', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    x = p1.bg_r_maxy - (l_bigcap + hc * i)
                    y = p1.gl - c.l_holedepth
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # // A面，内侧，外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1,p2, ho, IdentityHmgMatrix,  y, x+offset, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc,'Right','L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # // B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1,p2, ho, IdentityHmgMatrix,  y, x+offset, c.l_holedepth, c.id, t,
                                  c.l_smallcap,hc,'Right', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag,
                                  0, c.mx_cap)
                # 中心孔
                cstart = p1.bg_r_miny + (p1.bg_r_maxy - p1.bg_r_miny) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0: cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = cstart + chc * i
                    y = p1.gl - c.l_holedepth
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # // A面，内侧，外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1,p2, ho, IdentityHmgMatrix, y, x + offset, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc,'Right','L', c.l_bigname, c.l_smallname, c.i_name)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # // B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1,p2, ho, IdentityHmgMatrix, y, x + offset, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc,'Right','L', c.l_bigname, c.l_smallname, c.i_name)
        if (c.i_isoutput == 1) and (algorithm in [0, 1]):
            mHoleRow = mHoleRow + 1
            if face == 0:
                smallcap = c.l_smallcap
            else:
                smallcap = p1.gp - c.l_smallcap
            if (c.calctype == 0) or (c.calctype == 1):  # 靠背对齐
                p2.holeconfig_flag = c.flag2
                p2.hole_back_cap = p1.z - p2.z + c.l_bigcap
                p2.hole_2_dist = hc
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    ho.mx_x = 0
                    ho.mx_y = 0
                    if mx_flag == 0:
                        ho.mx_z = c.mx_cap
                    else:
                        ho.mx_z = -c.mx_cap
                    x = p1.z - p2.z + c.l_bigcap + hc * i + p1.bg_r_miny
                    y = p1.y - p2.y + smallcap
                    if c.ismirror == 1: x = p1.bg_r_maxy - (c.l_bigcap + hc * i) + p1.z - p2.z  # // 镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, 0, c.i_offsetvalue)
                    ho.wx = p1.gl
                    ho.wy = smallcap
                    ho.wz = c.l_bigcap + hc * i + p1.bg_r_miny + offset
                    if c.ismirror == 1: ho.wz = p1.bg_r_maxy - c.l_bigcap - hc * i + offset
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, y, x, 0, c.id, t,
                              c.l_smallcap, hc, 'Right', 'I', c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap)
                    if c.calctype == 1:
                        AddHole_A(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(0, c.pkcap,0)), y + c.pkcap, x + offset, 0,
                                  c.id, t, c.l_smallcap, hc, 'Right', 'I', c.i_name, '',
                                  c.i_name, mx_flag, 0, c.mx_cap)
                        # // ho.wy:= smallcap - c.pkcap;
                        AddHole_A(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(0, -c.pkcap,0)), y - c.pkcap, x + offset, 0,
                                  c.id, t, c.l_smallcap, hc, 'Right',
                                  'I', c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap)
            if c.calctype == 2:
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round((p1.gh - hc * (c.holenum - 1)) / 2)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    ho.mx_x = 0
                    ho.mx_y = 0
                    if mx_flag == 0:
                        ho.mx_z = c.mx_cap
                    else:
                        ho.mx_z = -c.mx_cap
                    x = p1.z - p2.z + l_bigcap + hc * i + p1.bg_r_miny
                    y = p1.y - p2.y + smallcap
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, 0, c.i_offsetvalue)  # ???
                    ho.wx = p1.gl
                    ho.wy = smallcap
                    ho.wz = l_bigcap + hc * i + p1.bg_r_miny + offset
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, y, x + offset, 0, c.id, t,
                              c.l_smallcap, hc, 'Right', 'I', c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    ho.mx_x = 0
                    ho.mx_y = 0
                    if mx_flag == 0:
                        ho.mx_z = c.mx_cap
                    else:
                        ho.mx_z = -c.mx_cap
                    x = p1.z - p2.z + (p1.bg_r_maxy - (l_bigcap + hc * i))
                    y = p1.y - p2.y + smallcap
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, 0, c.i_offsetvalue)  # ???
                    ho.wx = p1.gl
                    ho.wy = smallcap
                    ho.wz = (p1.bg_r_maxy - (l_bigcap + hc * i)) + offset
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, y, x + offset, 0, c.id, t,
                              c.l_smallcap, hc, 'Right', 'I', c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap)
                # // 中心孔
                cstart = p1.bg_r_miny + (p1.bg_r_maxy - p1.bg_r_miny) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0: cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = p1.z - p2.z + cstart + chc * i
                    y = p1.y - p2.y + smallcap
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, 0, c.i_offsetvalue)
                    ho.wx = p1.gl
                    ho.wy = smallcap
                    ho.wz = cstart + chc * i + offset
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, y, x + offset, 0, c.id, t, c.l_smallcap,
                              hc, 'Right', 'I', c.i_name, '', c.i_name)
def CalcHole_BackFace(p1, p2 ,c):
    global mHoleRow
    ho = hole()
    nocalc = False
    if (c == None) or ((c.iscalc == 0) and (p1.is_calc_holeconfig[4] != 1)) or \
            ((c.iscalc == 1) and (p1.is_calc_holeconfig[4] == 2)):
        nocalc = True
    di1 = p1.direct
    di2 = p2.direct
    if not di1 in [1, 2, 3, 4, 5, 6]: di1 = 1
    if not di2 in [1, 2, 3, 4, 5, 6]: di2 = 1
    algorithm = 0
    if (c != None): algorithm = c.algorithm
    ho.p1 = p1
    ho.p2 = p2
    hc = 0
    face = 0
    l = 0
    if (((di1 in [4, 6]) and (di2 in [2, 3])) or ((algorithm == 2) and (di1 in [4, 6]) and \
                                                  (di2 in [4, 6]))) and (p1.x >= p2.x) and (
            p1.x + p1.gl <= p2.x + p2.gl) and \
            (IsLSIntersection(p1.z + p1.bg_b_miny, p1.z + p1.bg_b_maxy, p2.z + p2.bg_f_miny, p2.z + p2.bg_f_maxy) == 1):
        #/侧板与背板接触，侧板竖纹，背板竖纹
        if nocalc: return
        offset = 0
        if algorithm == 1:  # 按接触面计算
            if p2.gh + p2.z > p2.z:    t = p2.z
            else:    t = p2.gh + p2.z
            if t > p1.z: offset = t - p1.z
        UpdateTempExpVariable(p1)
        l = Length_HoleFace(p1, p2, c, 5, 1)  # // 左面1, // 右面2, // 下面3, // 上面4, // 后面5, // 前面6
        if c.algorithm == 0:    #兼容算法
            t = (p1.bg_b_maxy + p1.z) - (p2.gh + p2.z)
            if (t > 0) and c.calctype in [0, 1]: l = l - t  # 接触面积较小
            if p1.zero_y == 6:
                t = (p1.bg_b_miny + p1.z) - p2.z
                if t < 0 and (c.calctype in [0, 1]): l = l + t  # 接触面较小
        mTmpExp['L'] = l
        hc = int(SimpleExpressToValue(c.holecap, 2, mTmpExp))
        chc = int(SimpleExpressToValue(c.center_holecap, 2, mTmpExp))
        if c.l_isoutput == 1:
            mHoleRow = mHoleRow + 1
            if c.calctype == 0 or c.calctype == 1:
                p1.holeconfig_flag = c.flag
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    x = c.l_holedepth
                    y = c.l_bigcap + hc * i + p1.bg_b_miny
                    if c.ismirror == 1: y = p1.bg_b_maxy - (c.l_bigcap + hc * i) #镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):   #A面，内测，外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t, c.l_smallcap, \
                                  hc, 'Back', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])):  # //B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc, 'Back', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
            if c.calctype == 2:  # // // 前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round(p1.gh - hc * (c.holenum - 1)) / 2
                for i in range(0, int(c.holenum // 2)):  # 前后端等距
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    x = c.l_holedepth
                    y = l_bigcap + hc * i + p1.bg_b_miny
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # A面内测外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id,
                                  t, c.l_smallcap, hc, 'Back', 'L', c.l_bigname, c.l_smallname,
                                  c.i_name, mx_flag, 0, c.mx_cap)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])):  # B面， 内测， 外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth,
                                  c.id, t, c.l_smallcap, hc, 'Back', 'L', c.l_bigname, c.l_smallname,
                                  c.i_name, mx_flag, 0, c.mx_cap)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    x = c.l_holedepth
                    y = p1.bg_b_maxy - (l_bigcap + hc * i)
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0,2,3])):  # B面，内测， 外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc, 'Back', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])):  # B面， 内测， 外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth,
                                  c.id, t, c.l_smallcap, hc, 'Back', 'L', c.l_bigname, c.l_smallname,
                                  c.i_name, mx_flag, 0, c.mx_cap)
                # 中心孔
                cstart = p1.bg_b_miny + (p1.bg_b_maxy - p1.bg_b_miny) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0:
                    cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = c.l_holedepth
                    y = cstart + chc * i
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # A面，内测， 外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1,p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t,
                                  c.l_smallcap,hc, 'Back', 'L', c.l_bigname, c.l_smallname, c.i_name)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # // B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t,
                                  c.l_smallcap, hc, 'Back', 'L', c.l_bigname, c.l_smallname, c.i_name)
        if (c.i_isoutput == 1) and (algorithm in [0, 1]):  # // 纹理面
            mHoleRow = mHoleRow + 1    #排孔数
            if face == 0:
                smallcap = c.l_smallcap
            else:
                smallcap = p1.gl - c.l_smallcap
            if (c.calctype == 0) or (c.calctype == 1):  # 靠背对齐； 靠背对齐- 三排孔
                p2.holeconfig_flag = c.flag2
                p2.hole_back_cap = p1.z - p2.z + c.l_bigcap
                p2.hole_2_dist = hc
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    ho.mx_x = 0
                    ho.mx_y = 0
                    if mx_flag == 0:
                        ho.mx_z = c.mx_cap
                    else:
                        ho.mx_z = -c.mx_cap
                    x = p1.x - p2.x + smallcap
                    y = p1.z - p2.z + c.l_bigcap + hc * i + p1.bg_b_miny
                    if c.ismirror == 1: y = p1.bg_b_maxy - (c.l_bigcap + hc * i) + p1.z - p2.z  # 镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, 0, c.i_offsetvalue)
                    ho.wx = smallcap
                    ho.wy = 0
                    ho.wz = c.l_bigcap + hc * i + p1.bg_b_miny+offset
                    if c.ismirror == 1: ho.wz = p1.bg_b_maxy - c.l_bigcap - hc * i+offset
                    AddHole_B(c, p2, p1, ho, IdentityHmgMatrix, x, y + offset,  0, c.id, t, c.l_smallcap, hc,
                              'Back', 'I', c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap )
                    if c.calctype == 1:
                        AddHole_B(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(c.pkcap, 0, 0)), x + c.pkcap,
                                  y + offset,0, c.id, t, c.l_smallcap, hc, 'Back', 'I', c.i_name, '', c.i_name,
                                  mx_flag, 0, c.mx_cap)
                        # // ho.wz:= smallcap - c.pkcap;
                        AddHole_B(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(-c.pkcap, 0, 0)), x - c.pkcap,
                                  y + offset, 0, c.id, t, c.l_smallcap, hc, 'Back', 'I', c.i_name, '', c.i_name,
                                  mx_flag, 0, c.mx_cap)
            if c.calctype == 2:    #前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round((p1.gh - hc * (c.holenum - 1)) / 2)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0:    mx_flag = 0
                    ho.mx_x = 0
                    ho.mx_y = 0
                    if mx_flag == 0:
                        ho.mx_z = c.mx_cap
                    else:
                        ho.mx_z = -c.mx_cap
                    x = p1.x - p2.x + smallcap
                    y = p1.z - p2.z + l_bigcap + hc * i + p1.bg_b_miny
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, 0, c.i_offsetvalue)
                    ho.wx = smallcap
                    ho.wy = 0
                    ho.wz = l_bigcap + hc * i + p1.bg_b_miny+offset
                    AddHole_B(c, p2,
                              p1, ho, IdentityHmgMatrix, x, y + offset, 0, c.id, t, c.l_smallcap, hc,
                              'Back', 'I', c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    ho.mx_x = 0
                    ho.mx_y = 0
                    if mx_flag == 0:
                        ho.mx_z = c.mx_cap
                    else:
                        ho.mx_z = -c.mx_cap
                    x = p1.x - p2.x + smallcap
                    y = p1.z - p2.z + (p1.bg_b_maxy - (l_bigcap + hc * i))
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, 0,c.i_offsetvalue)  # ???
                    ho.wx = smallcap
                    ho.wy = 0
                    ho.wz = (p1.bg_b_maxy - (l_bigcap + hc * i))+offset
                    AddHole_B(c, p2, p1, ho, IdentityHmgMatrix, x, y+offset, 0, c.id, t, c.l_smallcap, hc, 'Back', 'I',
                                        c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap)
                # 中心孔
                cstart = p1.bg_b_miny + (p1.bg_b_maxy - p1.bg_b_miny) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0: cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = p1.x - p2.x + smallcap
                    y = p1.z - p2.z + cstart + chc * i
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, 0,c.i_offsetvalue)
                    ho.wx = smallcap
                    ho.wy = 0
                    ho.wz = cstart + chc * i+offset
                    AddHole_B(c, p2, p1, ho, IdentityHmgMatrix, x, y + offset, 0, c.id, t, c.l_smallcap,
                              hc, 'Back', 'I', c.i_name, '', c.i_name)
    if (((di1 in [1, 5]) and (di2 in [2, 3])) or ((algorithm == 2) and (di1 in [1, 5]) and (di2 in [1, 5]))) and \
            (p1.z >= p2.z) and (p1.z + p1.gh <= p2.z + p2.gh) and \
            (IsLSIntersection(p1.x + p1.bg_b_minx, p1.x + p1.bg_b_maxx, p2.x + p2.bg_f_minx, p2.x + p2.bg_f_maxx) == 1):
        # 层板与背板接触，层板横纹，背板竖纹
        if nocalc: return
        offset = 0
        if algorithm == 1:
            # 按接触面计算
            if p2.gl + p2.x > p2.x: t = p2.x
            else: t=p2.gl+p2.x
            if t > p1.x: offset = t - p1.x
        UpdateTempExpVariable(p1)
        l = Length_HoleFace(p1, p2, c, 5, 0)  # // 左面1, // 右面2, // 下面3, // 上面4, // 后面5, // 前面6
        if c.algorithm == 0:  # // 兼容算法
            t = (p1.bg_b_maxx + p1.x) - (p2.gl + p2.x)
            if (t > 0) and (c.calctype in [0, 1]): l = l - t  # 接触面较小
            if p1.zero_y == 2:  # 右封边
                t = (p1.bg_b_minx + p1.x) - p2.x
                if (t < 0) and (c.calctype in [0, 1]): l = l + t  # 接触面较小
        mTmpExp['L'] = l
        hc = int(SimpleExpressToValue(c.holecap, 2, mTmpExp))
        chc = int(SimpleExpressToValue(c.center_holecap, 2, mTmpExp))
        if c.l_isoutput == 1:
            mHoleRow = mHoleRow + 1
            if (c.calctype == 0) or (c.calctype == 1):
                p1.holeconfig_flag = c.flag
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    x = c.l_holedepth
                    y = c.l_bigcap + hc * i + p1.bg_b_minx
                    if c.ismirror == 1: y = p1.bg_b_maxx - (c.l_bigcap + hc * i)  # 镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # A面， 内测， 外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1,
                                  p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t, c.l_smallcap, hc,
                                  'Back', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap,0 )
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])):  # B面， 内测， 外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1,
                                  p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc, 'Back', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap,0)
            if c.calctype == 2:    #前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round((p1.gl - hc * (c.holenum - 1)) / 2)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    x = c.l_holedepth
                    y = l_bigcap + hc * i + p1.bg_b_minx
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # // A面，内侧，外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1,
                                  p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t, c.l_smallcap, hc,
                                  'Back', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # //B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc,'Back', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
                for i in range(0,int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    x = c.l_holedepth
                    y = p1.bg_b_maxx - (l_bigcap + hc * i)
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # // A面，内侧，外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1,p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc,'Back','L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0 )
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # // B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1,p2, ho, IdentityHmgMatrix,  y + offset, x, c.l_holedepth, c.id, t,
                                  c.l_smallcap,hc,'Back', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag,
                                  c.mx_cap, 0)
                # 中心孔
                cstart = p1.bg_b_minx + (p1.bg_b_maxx - p1.bg_b_minx) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0: cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = c.l_holedepth
                    y = cstart + chc * i
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # // A面，内侧，外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1,p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc,'Back','L', c.l_bigname, c.l_smallname, c.i_name)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # // B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1,p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc,'Back','L', c.l_bigname, c.l_smallname, c.i_name)
        if (c.i_isoutput == 1) and (algorithm in [0, 1]):
            mHoleRow = mHoleRow + 1
            if face == 0:
                smallcap = c.l_smallcap
            else:
                smallcap = p1.gh - c.l_smallcap
            if (c.calctype == 0) or (c.calctype == 1):  # 靠背对齐
                p2.holeconfig_flag = c.flag2
                p2.hole_back_cap = p1.z - p2.z + c.l_bigcap
                p2.hole_2_dist = hc
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    if mx_flag == 0:
                        ho.mx_x = c.mx_cap
                    else:
                        ho.mx_x = -c.mx_cap
                    ho.mx_y = 0
                    ho.mx_z = 0
                    x = p1.z - p2.z + smallcap
                    y = p1.x - p2.x + c.l_bigcap + hc * i + p1.bg_b_minx
                    if c.ismirror == 1: y = p2.gl - ((p2.x + p2.bg_b_maxx - p1.x - p1.bg_b_maxx) + (c.l_bigcap + hc * i))  # // 镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    p2.big_p = p1
                    MakeVector(ho.i_offset, c.i_offsetvalue, 0, 0)
                    ho.wx = c.l_bigcap + hc * i + p1.bg_b_minx+offset
                    if c.ismirror == 1: ho.wx = p1.bg_b_maxx - c.l_bigcap - hc * i + offset
                    ho.wy = 0
                    ho.wz = smallcap
                    AddHole_B(c, p2, p1, ho, IdentityHmgMatrix, y + offset, x, 0, c.id, t,
                              c.l_smallcap, hc, 'Back', 'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
                    if c.calctype == 1:
                        AddHole_B(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(0, 0, c.pkcap)), y + offset,
                                  x + c.pkcap, 0,c.id, t, c.l_smallcap, hc, 'Back', 'I', c.i_name, '',
                                  c.i_name, mx_flag, c.mx_cap, 0)
                        # // ho.wy:= smallcap - c.pkcap;
                        AddHole_B(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(0, 0, -c.pkcap)), y + offset,
                                  x-c.pkcap, 0,c.id, t, c.l_smallcap, hc, 'Back',
                                  'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0 )
            if c.calctype == 2:    #前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round((p1.gl - hc * (c.holenum - 1)) / 2)
                for i in range(0,int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if mx_flag == 0:
                        ho.mx_x = c.mx_cap
                    else:
                        ho.mx_x = -c.mx_cap
                    ho.mx_y = 0
                    ho.mx_z = 0
                    x = p1.z - p2.z + smallcap
                    y = p1.x - p2.x + l_bigcap + hc * i + p1.bg_b_minx
                    p2.big_p = p1
                    MakeVector(ho.i_offset, c.i_offsetvalue, 0, 0)
                    ho.wx = l_bigcap + hc * i + p1.bg_b_minx+offset
                    ho.wy = 0
                    ho.wz = smallcap
                    AddHole_B(c, p2, p1, ho, IdentityHmgMatrix, y + offset, x, 0, c.id, t,
                              c.l_smallcap, hc, 'Back', 'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
                for i in range(0,int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    if mx_flag == 0:
                        ho.mx_x = c.mx_cap
                    else:
                        ho.mx_x = -c.mx_cap
                    ho.mx_y = 0
                    ho.mx_z = 0
                    x = p1.z - p2.z + smallcap
                    y = p1.x - p2.x + (p1.bg_b_maxx - (l_bigcap + hc * i))
                    p2.big_p = p1
                    MakeVector(ho.i_offset, c.i_offsetvalue, 0, 0)  # ???
                    ho.wx = (p1.bg_b_maxx - (l_bigcap + hc * i))+offset
                    ho.wy = 0
                    ho.wz = smallcap
                    AddHole_B(c, p2, p1, ho, IdentityHmgMatrix, y+ offset, x , 0, c.id, t,
                              c.l_smallcap, hc, 'Back', 'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0 )
                # // 中心孔
                cstart = p1.bg_b_minx + (p1.bg_b_maxx - p1.bg_b_minx) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0: cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = p1.z - p2.z + smallcap
                    y = p1.x - p2.x + cstart + chc * i
                    p2.big_p = p1
                    MakeVector(ho.i_offset, c.i_offsetvalue, 0, 0 )
                    ho.wx = cstart + chc * i+offset
                    ho.wy = 0
                    ho.wz = smallcap
                    AddHole_B(c, p2, p1, ho, IdentityHmgMatrix, y + offset, x, 0, c.id, t, c.l_smallcap,
                              hc, 'Back', 'I', c.i_name, '', c.i_name)
def CalcHole_FrontFace(p1, p2, c):
    global mHoleRow
    ho = hole()
    nocalc = False
    if (c == None) or ((c.iscalc == 0) and (p1.is_calc_holeconfig[5] != 1)) or \
            ((c.iscalc == 1) and (p1.is_calc_holeconfig[5] == 2)):
        nocalc = True
    di1 = p1.direct
    di2 = p2.direct
    if not di1 in [1, 2, 3, 4, 5, 6]: di1 = 1
    if not di2 in [1, 2, 3, 4, 5, 6]: di2 = 1
    algorithm = 0
    if (c != None): algorithm = c.algorithm
    ho.p1 = p1
    ho.p2 = p2
    hc = 0
    face = 0
    l = 0
    if (((di1 in [4, 6]) and (di2 in [2, 3])) or ((algorithm == 2) and (di1 in [4, 6]) and \
                                                  (di2 in [4, 6]))) and (p1.x >= p2.x) and (
            p1.x + p1.gl <= p2.x + p2.gl) and \
            (IsLSIntersection(p1.z + p1.bg_f_miny, p1.z + p1.bg_f_maxy, p2.z + p2.bg_b_miny,
                              p2.z + p2.bg_b_maxy) == 1):
        # /侧板与背板接触，侧板竖纹，背板竖纹
        if nocalc: return
        offset = 0
        if algorithm == 1:  # 按接触面计算
            if p2.gh+p2.z>p2.z:
                t = p2.z
            else:
                t = p2.gh + p2.z
            if t > p1.z: offset = t - p1.z
        UpdateTempExpVariable(p1)
        l = Length_HoleFace(p1, p2, c, 6, 1)  # // 左面1, // 右面2, // 下面3, // 上面4, // 后面5, // 前面6
        if c.algorithm == 0:  # 兼容算法
            t = (p1.bg_f_maxy + p1.z) - (p2.gh + p2.z)
            if (t > 0) and c.calctype in [0, 1]: l = l - t  # 接触面积较小
            if p1.zero_y == 6:
                t = (p1.bg_f_miny + p1.z) - p2.z
                if t < 0 and (c.calctype in [0, 1]): l = l + t  # 接触面较小
        mTmpExp['L'] = l
        hc = int(SimpleExpressToValue(c.holecap, 2, mTmpExp))
        chc = int(SimpleExpressToValue(c.center_holecap, 2, mTmpExp))
        if c.l_isoutput == 1:
            mHoleRow = mHoleRow + 1
            if c.calctype == 0 or c.calctype == 1:
                p1.holeconfig_flag = c.flag
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    x = p1.gp - c.l_holedepth
                    y = c.l_bigcap + hc * i + p1.bg_f_miny
                    if c.ismirror == 1: y = p1.bg_f_maxy - (c.l_bigcap + hc * i)  # 镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # A面，内测，外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t,
                                  c.l_smallcap, \
                                  hc, 'Front', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])):  # //B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t,
                                  c.l_smallcap,
                                  hc, 'Front', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
            if c.calctype == 2:  # // // 前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round(p1.gh - hc * (c.holenum - 1)) / 2
                for i in range(0,int(c.holenum // 2)):  # 前后端等距
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    x = p1.gp - c.l_holedepth
                    y = l_bigcap + hc * i + p1.bg_f_miny
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # A面内测外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id,
                                  t, c.l_smallcap, hc, 'Front', 'L', c.l_bigname, c.l_smallname,
                                  c.i_name, mx_flag, 0, c.mx_cap)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])):  # B面， 内测， 外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth,
                                  c.id, t, c.l_smallcap, hc, 'Front', 'L', c.l_bigname, c.l_smallname,
                                  c.i_name, mx_flag, 0, c.mx_cap)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    x = p1.gp - c.l_holedepth
                    y = p1.bg_f_maxy - (l_bigcap + hc * i)
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # B面，内测， 外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t,
                                  c.l_smallcap,
                                  hc, 'Front', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, 0, c.mx_cap)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])):  # B面， 内测， 外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth,
                                  c.id, t, c.l_smallcap, hc, 'Front', 'L', c.l_bigname, c.l_smallname,
                                  c.i_name, mx_flag, 0, c.mx_cap)
                # 中心孔
                cstart = p1.bg_f_miny + (p1.bg_f_maxy - p1.bg_f_miny) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0:
                    cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = p1.gp - c.l_holedepth
                    y = cstart + chc * i
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # A面，内测， 外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t,
                                  c.l_smallcap, hc, 'Front', 'L', c.l_bigname, c.l_smallname, c.i_name)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # // B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, x, y + offset, c.l_holedepth, c.id, t,
                                  c.l_smallcap, hc, 'Front', 'L', c.l_bigname, c.l_smallname, c.i_name)
        if (c.i_isoutput == 1) and (algorithm in [0, 1]):  # // 纹理面
            mHoleRow = mHoleRow + 1  # 排孔数
            if face == 0:
                smallcap = c.l_smallcap
            else:
                smallcap = p1.gl - c.l_smallcap
            if (c.calctype == 0) or (c.calctype == 1):  # 靠背对齐； 靠背对齐- 三排孔
                p2.holeconfig_flag = c.flag2
                p2.hole_back_cap = p1.z - p2.z + c.l_bigcap
                p2.hole_2_dist = hc
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    ho.mx_x = 0
                    ho.mx_y = 0
                    if mx_flag == 0:
                        ho.mx_z = c.mx_cap
                    else:
                        ho.mx_z = -c.mx_cap
                    x = p1.x - p2.x + smallcap
                    y = p1.z - p2.z + c.l_bigcap + hc * i + p1.bg_f_miny
                    if c.ismirror == 1: y = p1.bg_f_maxy - (c.l_bigcap + hc * i) + p1.x - p2.x  # 镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, 0, c.i_offsetvalue)
                    ho.wx = smallcap
                    ho.wy = p1.gp
                    ho.wz = c.l_bigcap + hc * i + p1.bg_f_miny + offset
                    if c.ismirror == 1: ho.wz = p1.bg_f_maxy - c.l_bigcap - hc * i + offset
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, x, y, 0, c.id, t, c.l_smallcap, hc,
                              'Front', 'I', c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap)
                    if c.calctype == 1:
                        AddHole_A(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(c.pkcap, 0, 0)), x + c.pkcap,
                                  y + offset, 0, c.id, t, c.l_smallcap, hc, 'Front', 'I', c.i_name, '', c.i_name,
                                  mx_flag, 0, c.mx_cap)
                        # // ho.wz:= smallcap - c.pkcap;
                        AddHole_A(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(-c.pkcap,0, 0)), x - c.pkcap,
                                  y + offset, 0, c.id, t, c.l_smallcap, hc, 'Front', 'I', c.i_name, '', c.i_name,
                                  mx_flag, 0, c.mx_cap)
            if c.calctype == 2:  # 前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round((p1.gh - hc * (c.holenum - 1)) / 2)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0:    mx_flag = 0
                    ho.mx_x = 0
                    ho.mx_y = 0
                    if mx_flag == 0:
                        ho.mx_z = c.mx_cap
                    else:
                        ho.mx_z = -c.mx_cap
                    x = p1.x - p2.x + smallcap
                    y = p1.z - p2.z + l_bigcap + hc * i + p1.bg_f_miny
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, 0, c.i_offsetvalue)
                    ho.wx = smallcap
                    ho.wy = p1.gp
                    ho.wz = l_bigcap + hc * i + p1.bg_f_miny + offset
                    AddHole_A(c, p2,
                              p1, ho, IdentityHmgMatrix, x, y + offset, 0, c.id, t, c.l_smallcap, hc,
                              'Front', 'I', c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap)
                for i in range(0,int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    ho.mx_x = 0
                    ho.mx_y = 0
                    if mx_flag == 0:
                        ho.mx_z = c.mx_cap
                    else:
                        ho.mx_z = -c.mx_cap
                    ho.mx_z = 0
                    x = p1.x - p2.x + smallcap
                    y = p1.z - p2.z + (p1.bg_f_maxy - (l_bigcap + hc * i))
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, 0, c.i_offsetvalue)  # ???
                    ho.wx = smallcap
                    ho.wy = p1.gp
                    ho.wz = (p1.bg_f_maxy - (l_bigcap + hc * i)) + offset
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, x, y + offset, 0, c.id, t, c.l_smallcap, hc, 'Front',
                              'I',c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap)
                # 中心孔
                cstart = p1.bg_f_miny + (p1.bg_f_maxy - p1.bg_f_miny) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0: cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = p1.x - p2.x + smallcap
                    y = p1.z - p2.z + cstart + chc * i
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, 0, c.i_offsetvalue)
                    ho.wx = smallcap
                    ho.wy = p1.gp
                    ho.wz = cstart + chc * i + offset
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, x, y + offset, 0, c.id, t, c.l_smallcap,
                              hc, 'Front', 'I', c.i_name, '', c.i_name)
    if (((di1 in [1, 5]) and (di2 in [2, 3])) or ((algorithm == 2) and (di1 in [1, 5]) and (di2 in [1, 5]))) and \
            (p1.z >= p2.z) and (p1.z + p1.gh <= p2.z + p2.gh) and \
            (IsLSIntersection(p1.x + p1.bg_f_minx, p1.x + p1.bg_f_maxx, p2.x + p2.bg_b_minx, p2.x + p2.bg_b_maxx) == 1):
        # 层板与背板接触，层板横纹，背板竖纹
        if nocalc: return
        offset = 0
        if algorithm == 1:
            # 按接触面计算
            if p2.gl + p2.x > p2.x:
                t = p2.x
            else:
                t = p2.gl + p2.x
            if t > p1.x: offset = t - p1.x
        UpdateTempExpVariable(p1)
        l = Length_HoleFace(p1, p2, c, 6, 0)  # // 左面1, // 右面2, // 下面3, // 上面4, // 后面5, // 前面6
        if c.algorithm == 0:  # // 兼容算法
            t = (p1.bg_f_maxx + p1.x) - (p2.gl + p2.x)
            if (t > 0) and (c.calctype in [0, 1]): l = l - t  # 接触面较小
            if p1.zero_y == 2:  # 右封边
                t = (p1.bg_f_minx + p1.x) - p2.x
                if (t < 0) and (c.calctype in [0, 1]): l = l + t  # 接触面较小
        mTmpExp['L'] = l
        hc = int(SimpleExpressToValue(c.holecap, 2, mTmpExp))
        chc = int(SimpleExpressToValue(c.center_holecap, 2, mTmpExp))
        if c.l_isoutput == 1:
            mHoleRow = mHoleRow + 1
            if (c.calctype == 0) or (c.calctype == 1):
                p1.holeconfig_flag = c.flag
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    x = p1.gp - c.l_holedepth
                    y = c.l_bigcap + hc * i + p1.bg_f_minx
                    if c.ismirror == 1: y = p1.bg_f_maxx - (c.l_bigcap + hc * i)  # 镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # A面， 内测， 外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc,'Front', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])):  # B面， 内测， 外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc, 'Front', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
            if c.calctype == 2:  # 前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round((p1.gl - hc * (c.holenum - 1)) / 2)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    x = p1.gp - c.l_holedepth
                    y = l_bigcap + hc * i + p1.bg_f_minx
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # // A面，内侧，外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1,p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc,'Front', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # //B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,c.l_smallcap,
                                  hc, 'Front', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
                for i in range(0,int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    x = p1.gp - c.l_holedepth
                    y = p1.bg_f_maxx - (l_bigcap + hc * i)
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # // A面，内侧，外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,c.l_smallcap,
                                  hc, 'Front', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # // B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,
                                  c.l_smallcap, hc, 'Front', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag,
                                  c.mx_cap, 0)
                # 中心孔
                cstart = p1.bg_f_minx + (p1.bg_f_maxx - p1.bg_f_minx) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0: cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = p1.gp - c.l_holedepth
                    y = cstart + chc * i
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # // A面，内侧，外侧
                        face = 0
                        p1.big_p = None
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,
                                  c.l_smallcap,hc, 'Front', 'L', c.l_bigname, c.l_smallname, c.i_name)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # // B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,
                                  c.l_smallcap,hc, 'Front', 'L', c.l_bigname, c.l_smallname, c.i_name)
        if (c.i_isoutput == 1) and (algorithm in [0, 1]):
            mHoleRow = mHoleRow + 1
            if face == 0:
                smallcap = c.l_smallcap
            else:
                smallcap = p1.gh - c.l_smallcap
            if (c.calctype == 0) or (c.calctype == 1):  # 靠背对齐
                p2.holeconfig_flag = c.flag2
                p2.hole_back_cap = p1.x - p2.x + c.l_bigcap
                p2.hole_2_dist = hc
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    if mx_flag == 0:
                        ho.mx_x = c.mx_cap
                    else:
                        ho.mx_x = -c.mx_cap
                    ho.mx_y = 0
                    ho.mx_z = 0
                    x = p1.z - p2.z + smallcap
                    y = p1.x - p2.x + c.l_bigcap + hc * i + p1.bg_f_minx
                    if c.ismirror == 1: y = p2.gl - (
                                (p2.x + p2.bg_f_maxx - p1.x - p1.bg_f_maxx) + (c.l_bigcap + hc * i))  # // 镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    p2.big_p = p1
                    MakeVector(ho.i_offset, c.i_offsetvalue, 0, 0 )
                    ho.wx = c.l_bigcap + hc * i + p1.bg_f_minx + offset
                    if c.ismirror == 1: ho.wx = p1.bg_f_maxx - c.l_bigcap - hc * i + offset
                    ho.wy = p1.gp
                    ho.wz = smallcap
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, y + offset, x, 0, c.id, t,
                              c.l_smallcap, hc, 'Front', 'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
                    if c.calctype == 1:
                        AddHole_A(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(0, 0, c.pkcap)), y + offset,
                                  x + c.pkcap, 0, c.id, t, c.l_smallcap, hc, 'Front', 'I', c.i_name, '',
                                  c.i_name, mx_flag, c.mx_cap, 0)
                        # // ho.wy:= smallcap - c.pkcap;
                        AddHole_A(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(0, 0, -c.pkcap )), y + offset,
                                  x - c.pkcap, 0, c.id, t, c.l_smallcap, hc, 'Front',
                                  'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
            if c.calctype == 2:  # 前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round((p1.gl - hc * (c.holenum - 1)) / 2)
                for i in range(0,int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if mx_flag == 0:
                        ho.mx_x = c.mx_cap
                    else:
                        ho.mx_x = -c.mx_cap
                    ho.mx_y = 0
                    ho.mx_z = 0
                    x = p1.z - p2.z + smallcap
                    y = p1.x - p2.x + l_bigcap + hc * i + p1.bg_f_minx
                    p2.big_p = p1
                    MakeVector(ho.i_offset, c.i_offsetvalue, 0, 0)  # ???
                    ho.wx = l_bigcap + hc * i + p1.bg_f_minx + offset
                    ho.wy = p1.gp
                    ho.wz = smallcap
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, y + offset, x, 0, c.id, t,
                              c.l_smallcap, hc, 'Front', 'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
                for i in range(0,int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    x = p1.z - p2.z + smallcap
                    y = p1.x - p2.x + (p1.bg_f_maxx - (l_bigcap + hc * i))
                    p2.big_p = p1
                    MakeVector(ho.i_offset, c.i_offsetvalue, 0, 0)  # ???
                    ho.wx = (p1.bg_f_maxx - (l_bigcap + hc * i)) + offset
                    ho.wy = p1.gp
                    ho.wz = smallcap
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, y + offset, x, 0, c.id, t,
                              c.l_smallcap, hc, 'Front', 'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
                # // 中心孔
                cstart = p1.bg_f_minx + (p1.bg_f_maxx - p1.bg_f_minx) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0: cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = p1.z - p2.z + smallcap
                    y = p1.x - p2.x + cstart + chc * i
                    p2.big_p = p1
                    MakeVector(ho.i_offset, c.i_offsetvalue, 0, 0)
                    ho.wx = cstart + chc * i + offset
                    ho.wy = p1.gp
                    ho.wz = smallcap
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, y + offset, x, 0, c.id, t, c.l_smallcap,
                              hc, 'Front', 'I', c.i_name, '', c.i_name)
def CalcHole_DownFace(p1, p2, c):
    global mHoleRow
    ho = hole()
    nocalc = False
    if (c == None) or ((c.iscalc == 0) and (p1.is_calc_holeconfig[2] != 1)) or \
            ((c.iscalc == 1) and (p1.is_calc_holeconfig[2] == 2)):
        nocalc = True
    di1 = p1.direct
    di2 = p2.direct
    if not di1 in [1, 2, 3, 4, 5, 6]: di1 = 1
    if not di2 in [1, 2, 3, 4, 5, 6]: di2 = 1
    algorithm = 0
    if (c != None): algorithm = c.algorithm
    ho.p1 = p1
    ho.p2 = p2
    hc = 0
    face = 0
    l = 0
    if (((di1 in [4, 6]) and (di2 in [1, 5])) or ((algorithm == 2) and (di1 in [4, 6]) and \
                                                  (di2 in [4, 6]))) and (p1.x >= p2.x) and (
            p1.x + p1.gl <= p2.x + p2.gl) and \
            (IsLSIntersection(p1.y + p1.bg_d_miny, p1.y + p1.bg_d_maxy, p2.y + p2.bg_u_miny,
                              p2.y + p2.bg_u_maxy) == 1):
        # /侧板与背板接触，侧板竖纹，背板竖纹
        if nocalc: return
        offset = 0
        if algorithm == 1:  # 按接触面计算
            if p2.gp+p2.y>p2.y:
                t = p2.y
            else:
                t = p2.gp + p2.y
            if t > p1.y: offset = t - p1.y
        UpdateTempExpVariable(p1)
        l = Length_HoleFace(p1, p2, c, 3, 1)  # // 左面1, // 右面2, // 下面3, // 上面4, // 后面5, // 前面6
        # print 'l1=', l
        # print 'p2=',p2.guid,p2.name,p2.gp,p2.gl,p2.gh
        if c.algorithm == 0:  # 兼容算法
            t = (p1.bg_d_maxy + p1.y) - (p2.gp + p2.y)
            # print p1.bg_d_maxy,p1.y,p2.gp,p2.y
            if (t > 0) and c.calctype in [0, 1]: l = l - t  # 接触面积较小
            if p1.zero_y == 4:
                t = (p1.bg_d_miny + p1.y) - p2.y
                if t < 0 and (c.calctype in [0, 1]): l = l + t  # 接触面较小
        mTmpExp['L'] = l
        # print 'l2=',l,'t=',t
        # print 'c.holecap=',c.holecap
        hc = int(SimpleExpressToValue(c.holecap, 2, mTmpExp))
        chc = int(SimpleExpressToValue(c.center_holecap, 2, mTmpExp))
        if c.l_isoutput == 1:
            mHoleRow = mHoleRow + 1
            if c.calctype == 0 or c.calctype == 1:
                p1.holeconfig_flag = c.flag
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    x = c.l_holedepth
                    y = c.l_bigcap + hc * i + p1.bg_d_miny
                    if c.ismirror == 1: y = p1.bg_d_maxy - (c.l_bigcap + hc * i)  # 镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # A面，内测，外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_DownFace1' + '\n')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,
                                  c.l_smallcap, \
                                  hc, 'Down', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])):  # //B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_DownFace2' + '\n')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,c.l_smallcap,
                                  hc, 'Down', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
            if c.calctype == 2:  # // // 前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round(p1.gp - hc * (c.holenum - 1)) / 2
                for i in range(0,int(c.holenum // 2)):  # 前后端等距
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    x = c.l_holedepth
                    y = l_bigcap + hc * i + p1.bg_d_miny
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # A面内测外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_DownFace3' + '\n')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id,
                                  t, c.l_smallcap, hc, 'Down', 'L', c.l_bigname, c.l_smallname,
                                  c.i_name, mx_flag, c.mx_cap, 0)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])):  # B面， 内测， 外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_DownFace4' + '\n')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth,
                                  c.id, t, c.l_smallcap, hc, 'Down', 'L', c.l_bigname, c.l_smallname,
                                  c.i_name, mx_flag, c.mx_cap, 0)
                for i in range(0,int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    x = c.l_holedepth
                    y = p1.bg_d_maxy - (l_bigcap + hc * i)
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # B面，内测， 外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_DownFace5' + '\n')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,
                                  c.l_smallcap,
                                  hc, 'Down', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])):  # B面， 内测， 外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_DownFace6' + '\n')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth,
                                  c.id, t, c.l_smallcap, hc, 'Down', 'L', c.l_bigname, c.l_smallname,
                                  c.i_name, mx_flag, c.mx_cap,0)
                # 中心孔
                cstart = p1.bg_d_miny + (p1.bg_d_maxy - p1.bg_d_miny) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0:
                    cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = c.l_holedepth
                    y = cstart + chc * i
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # A面，内测， 外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_DownFace7' + '\n')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,
                                  c.l_smallcap, hc, 'Down', 'L', c.l_bigname, c.l_smallname, c.i_name)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # // B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_DownFace8' + '\n')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,
                                  c.l_smallcap, hc, 'Down', 'L', c.l_bigname, c.l_smallname, c.i_name)
        if (c.i_isoutput == 1) and (algorithm in [0, 1]):  # // 纹理面
            mHoleRow = mHoleRow + 1  # 排孔数
            if face == 0:
                smallcap = c.l_smallcap
            else:
                smallcap = p1.gl - c.l_smallcap
            if (c.calctype == 0) or (c.calctype == 1):  # 靠背对齐； 靠背对齐- 三排孔
                p2.holeconfig_flag = c.flag2
                p2.hole_back_cap = p1.y - p2.y + c.l_bigcap
                p2.hole_2_dist = hc
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    ho.mx_x = 0
                    ho.mx_y = 0
                    if mx_flag == 0:
                        ho.mx_y = c.mx_cap
                    else:
                        ho.mx_y = -c.mx_cap
                    ho.mx_z = 0
                    x = p1.x - p2.x + smallcap
                    y = p1.y - p2.y + c.l_bigcap + hc * i + p1.bg_d_miny
                    if c.ismirror == 1: y = p1.bg_d_maxy - (c.l_bigcap + hc * i) + p1.y - p2.y  # 镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, c.i_offsetvalue, 0)
                    ho.wx = smallcap
                    ho.wy = c.l_bigcap + hc * i + p1.bg_d_miny+offset
                    if c.ismirror == 1: ho.wy = p1.bg_d_maxy - c.l_bigcap - hc * i + offset
                    ho.wz = 0
                    #print 'B=',len(mHPInfoList),ho.wx,'wy=',ho.wy,'l_bigcap=',c.l_bigcap,'hc=',hc
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_DownFace9' + '\n')
                    AddHole_B(c, p2, p1, ho, IdentityHmgMatrix, x, y+offset, 0, c.id, t, c.l_smallcap, hc,
                              'Down', 'I', c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap)
                    #print 'B1=', len(mHPInfoList)
                    if c.calctype == 1:
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_DownFace10' + '\n')
                        AddHole_B(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(c.pkcap, 0, 0)), x + c.pkcap,
                                  y + offset, 0, c.id, t, c.l_smallcap, hc, 'Down', 'I', c.i_name, '', c.i_name,
                                  mx_flag, 0, c.mx_cap)
                        #print 'B2=', len(mHPInfoList)
                        # // ho.wz:= smallcap - c.pkcap;
                        AddHole_B(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(-c.pkcap,0, 0)), x - c.pkcap,
                                  y + offset, 0, c.id, t, c.l_smallcap, hc, 'Down', 'I', c.i_name, '', c.i_name,
                                  mx_flag, 0, c.mx_cap)
                        #print 'B3=', len(mHPInfoList)
            if c.calctype == 2:  # 前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round((p1.gp - hc * (c.holenum - 1)) / 2)
                for i in range(0,int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0:    mx_flag = 0
                    ho.mx_x = 0
                    if mx_flag == 0:
                        ho.mx_y = c.mx_cap
                    else:
                        ho.mx_y = -c.mx_cap
                    ho.mx_z = 0
                    x = p1.x - p2.x + smallcap
                    y = p1.y - p2.y + l_bigcap + hc * i + p1.bg_d_miny
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, c.i_offsetvalue, 0)
                    ho.wx = smallcap
                    ho.wy = l_bigcap + hc * i + p1.bg_d_miny+offset
                    ho.wz = 0
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_DownFace11' + '\n')
                    AddHole_B(c, p2,p1, ho, IdentityHmgMatrix, x, y + offset, 0, c.id, t, c.l_smallcap, hc,
                              'Down', 'I', c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap)
                    #print 'B4=', len(mHPInfoList)
                for i in range(0,int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    ho.mx_x = 0
                    if mx_flag == 0:
                        ho.mx_y = c.mx_cap
                    else:
                        ho.mx_y = -c.mx_cap
                    ho.mx_z = 0
                    x = p1.x - p2.x + smallcap
                    y = p1.y - p2.y + (p1.bg_d_maxy - (l_bigcap + hc * i))
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, c.i_offsetvalue,0 )  # ???
                    ho.wx = smallcap
                    ho.wy = (p1.bg_d_maxy - (l_bigcap + hc * i))+offset
                    ho.wz = 0
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_DownFace12' + '\n')
                    AddHole_B(c, p2, p1, ho, IdentityHmgMatrix, x, y + offset, 0, c.id, t, c.l_smallcap, hc, 'Down',
                              'I',c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap)
                    #print 'B5=', len(mHPInfoList)
                # 中心孔
                cstart = p1.bg_d_miny + (p1.bg_d_maxy - p1.bg_d_miny) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0: cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = p1.x - p2.x + smallcap
                    y = p1.y - p2.y + cstart + chc * i
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, c.i_offsetvalue, 0)
                    ho.wx = smallcap
                    ho.wy = cstart + chc * i+offset
                    ho.wz = 0
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_DownFace13' + '\n')
                    AddHole_B(c, p2, p1, ho, IdentityHmgMatrix, x, y + offset, 0, c.id, t, c.l_smallcap,
                              hc, 'Down', 'I', c.i_name, '', c.i_name)
                    #print 'B6=', len(mHPInfoList)
    if (((di1 in [2, 3]) and (di2 in [1, 5])) or ((algorithm == 2) and (di1 in [2, 3]) and (di2 in [2, 3]))) and \
            (p1.y >= p2.y) and (p1.y + p1.gp <= p2.y + p2.gp) and \
            (IsLSIntersection(p1.x + p1.bg_d_minx, p1.x + p1.bg_d_maxx, p2.x + p2.bg_u_minx, p2.x + p2.bg_u_maxx) == 1):
        # 层板与背板接触，层板横纹，背板竖纹
        if nocalc: return
        offset = 0
        if algorithm == 1:
            # 按接触面计算
            if p2.gl + p2.x > p2.x:
                t = p2.x
            else:
                t = p2.gl + p2.x
            if t > p1.x: offset = t - p1.x
        UpdateTempExpVariable(p1)
        l = Length_HoleFace(p1, p2, c, 3, 0)  # // 左面1, // 右面2, // 下面3, // 上面4, // 后面5, // 前面6
        if c.algorithm == 0:  # // 兼容算法
            t = (p1.bg_d_maxx + p1.x) - (p2.gl + p2.x)
            if (t > 0) and (c.calctype in [0, 1]): l = l - t  # 接触面较小
            if p1.zero_y == 2:  # 右封边
                t = (p1.bg_d_minx + p1.x) - p2.x
                if (t < 0) and (c.calctype in [0, 1]): l = l + t  # 接触面较小
        mTmpExp['L'] = l
        hc = int(SimpleExpressToValue(c.holecap, 2, mTmpExp))
        chc = int(SimpleExpressToValue(c.center_holecap, 2, mTmpExp))
        if c.l_isoutput == 1:
            mHoleRow = mHoleRow + 1
            if (c.calctype == 0) or (c.calctype == 1):
                p1.holeconfig_flag = c.flag
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    x = c.l_holedepth
                    y = c.l_bigcap + hc * i + p1.bg_d_minx
                    if c.ismirror == 1: y = p1.bg_d_maxx - (c.l_bigcap + hc * i)  # 镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # A面， 内测， 外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_DownFace14' + '\n')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc,'Down', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])):  # B面， 内测， 外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_DownFace15' + '\n')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc, 'Down', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
            if c.calctype == 2:  # 前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round((p1.gl - hc * (c.holenum - 1)) / 2)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    x = c.l_holedepth
                    y = l_bigcap + hc * i + p1.bg_d_minx
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # // A面，内侧，外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_DownFace16' + '\n')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc,'Down', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # //B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_DownFace17' + '\n')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,c.l_smallcap,
                                  hc, 'Down', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    x = c.l_holedepth
                    y = p1.bg_d_maxx - (l_bigcap + hc * i)
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # // A面，内侧，外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_DownFace18' + '\n')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,c.l_smallcap,
                                  hc, 'Down', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # // B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_DownFace19' + '\n')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,
                                  c.l_smallcap, hc, 'Down', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag,
                                  c.mx_cap, 0)
                # 中心孔
                cstart = p1.bg_d_minx + (p1.bg_d_maxx - p1.bg_d_minx) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0: cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = c.l_holedepth
                    y = cstart + chc * i
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # // A面，内侧，外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_DownFace20' + '\n')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,
                                  c.l_smallcap,hc, 'Down', 'L', c.l_bigname, c.l_smallname, c.i_name)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # // B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_DownFace21' + '\n')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,
                                  c.l_smallcap,hc, 'Down', 'L', c.l_bigname, c.l_smallname, c.i_name)
        if (c.i_isoutput == 1) and (algorithm in [0, 1]):
            mHoleRow = mHoleRow + 1
            if face == 0:
                smallcap = c.l_smallcap
            else:
                smallcap = p1.gp - c.l_smallcap
            if (c.calctype == 0) or (c.calctype == 1):  # 靠背对齐
                p2.holeconfig_flag = c.flag2
                p2.hole_back_cap = p1.x - p2.x + c.l_bigcap + p1.bg_d_minx
                p2.hole_2_dist = hc
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    if mx_flag == 0:
                        ho.mx_x = c.mx_cap
                    else:
                        ho.mx_x = -c.mx_cap
                    ho.mx_y = 0
                    ho.mx_z = 0
                    x = p1.x - p2.x + c.l_bigcap + hc * i + p1.bg_d_minx
                    y = p1.y - p2.y + smallcap
                    if c.ismirror == 1: x = p1.bg_d_maxx - (c.l_bigcap + hc * i) + p1.y - p2.y  # // 镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    p2.big_p = p1
                    MakeVector(ho.i_offset, c.i_offsetvalue, 0, 0 )
                    ho.wx = c.l_bigcap + hc * i + p1.bg_d_minx + offset
                    if c.ismirror == 1: ho.wx = p1.bg_d_maxx - c.l_bigcap - hc * i + offset
                    ho.wy = smallcap
                    ho.wz = 0
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_DownFace22' + '\n')
                    AddHole_B(c, p2, p1, ho, IdentityHmgMatrix, y + offset, x, 0, c.id, t,
                              c.l_smallcap, hc, 'Down', 'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
                    #print 'B7=', len(mHPInfoList)
                    if c.calctype == 1:
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_DownFace23' + '\n')
                        AddHole_B(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(0, c.pkcap,0 )), x+offset,
                                  y + c.pkcap, 0, c.id, t, c.l_smallcap, hc, 'Down', 'I', c.i_name, '',
                                  c.i_name, mx_flag, c.mx_cap, 0)
                        # // ho.wy:= smallcap - c.pkcap;
                        AddHole_B(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(0, -c.pkcap,0  )), x+offset,
                                  y - c.pkcap, 0, c.id, t, c.l_smallcap, hc, 'Down',
                                  'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
            if c.calctype == 2:  # 前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round((p1.gl - hc * (c.holenum - 1)) / 2)
                for i in range(0,int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if mx_flag == 0:
                        ho.mx_x = c.mx_cap
                    else:
                        ho.mx_x = -c.mx_cap
                    ho.mx_y = 0
                    ho.mx_z = 0
                    x = p1.x - p2.x + l_bigcap + hc * i + p1.bg_d_minx
                    y = p1.y - p2.y + smallcap
                    p2.big_p = p1
                    MakeVector(ho.i_offset, c.i_offsetvalue, 0, 0)  # ???
                    ho.wx = l_bigcap + hc * i + p1.bg_d_minx+offset
                    ho.wy = smallcap
                    ho.wz = 0
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_DownFace24' + '\n')
                    AddHole_B(c, p2, p1, ho, IdentityHmgMatrix, x + offset, y, 0, c.id, t,
                              c.l_smallcap, hc, 'Down', 'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
                    #print 'B8=', len(mHPInfoList)
                for i in range(0,int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    x = p1.x - p2.x + (p1.bg_d_maxx - (l_bigcap + hc * i))
                    y = p1.y - p2.y + smallcap
                    p2.big_p = p1
                    MakeVector(ho.i_offset, c.i_offsetvalue, 0, 0)  # ???
                    ho.wx = (p1.bg_d_maxx - (l_bigcap + hc * i)) + offset
                    ho.wy = smallcap
                    ho.wz = 0
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_DownFace25' + '\n')
                    AddHole_B(c, p2, p1, ho, IdentityHmgMatrix, x + offset, y, 0, c.id, t,
                              c.l_smallcap, hc, 'Down', 'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
                    #print 'B9=', len(mHPInfoList)
                # // 中心孔
                cstart = p1.bg_d_minx + (p1.bg_d_maxx - p1.bg_d_minx) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0: cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = p1.x - p2.x + cstart + chc * i
                    y = p1.y - p2.y + smallcap
                    p2.big_p = p1
                    MakeVector(ho.i_offset, c.i_offsetvalue, 0, 0)
                    ho.wx = cstart + chc * i+offset
                    ho.wy = smallcap
                    ho.wz = 0
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_DownFace26' + '\n')
                    AddHole_B(c, p2, p1, ho, IdentityHmgMatrix, x + offset, y, 0, c.id, t, c.l_smallcap,
                              hc, 'Down', 'I', c.i_name, '', c.i_name)
                    #print 'B10=', len(mHPInfoList)
def CalcHole_UpFace(p1, p2, c):
    global mHoleRow
    ho = hole()
    nocalc = False
    if (c == None) or ((c.iscalc == 0) and (p1.is_calc_holeconfig[3] != 1)) or \
            ((c.iscalc == 1) and (p1.is_calc_holeconfig[3] == 2)):
        nocalc = True
    di1 = p1.direct
    di2 = p2.direct
    if not di1 in [1, 2, 3, 4, 5, 6]: di1 = 1
    if not di2 in [1, 2, 3, 4, 5, 6]: di2 = 1
    algorithm = 0
    if (c != None): algorithm = c.algorithm
    ho.p1 = p1
    ho.p2 = p2
    hc = 0
    face = 0
    l = 0
    if (((di1 in [4, 6]) and (di2 in [1, 5])) or ((algorithm == 2) and (di1 in [4, 6]) and \
                                                  (di2 in [4, 6]))) and (p1.x >= p2.x) and (
            p1.x + p1.gl <= p2.x + p2.gl) and \
            (IsLSIntersection(p1.y + p1.bg_u_miny, p1.y + p1.bg_u_maxy, p2.y + p2.bg_d_miny,
                              p2.y + p2.bg_d_maxy) == 1):
        # /侧板与背板接触，侧板竖纹，背板竖纹
        if nocalc: return
        offset = 0
        if algorithm == 1:  # 按接触面计算
            if p2.gp+p2.y>p2.y:
                t = p2.y
            else:
                t = p2.gp + p2.y
            if t > p1.y: offset = t - p1.y
        UpdateTempExpVariable(p1)
        l = Length_HoleFace(p1, p2, c, 4, 1)  # // 左面1, // 右面2, // 下面3, // 上面4, // 后面5, // 前面6
        if c.algorithm == 0:  # 兼容算法
            t = (p1.bg_u_maxy + p1.y) - (p2.gp + p2.y)
            if (t > 0) and c.calctype in [0, 1]: l = l - t  # 接触面积较小
            if p1.zero_y == 4: #前封边
                t = (p1.bg_u_miny + p1.y) - p2.y
                if t < 0 and (c.calctype in [0, 1]): l = l + t  # 接触面较小
        mTmpExp['L'] = l
        hc = int(SimpleExpressToValue(c.holecap, 2, mTmpExp))
        chc = int(SimpleExpressToValue(c.center_holecap, 2, mTmpExp))
        if c.l_isoutput == 1:
            mHoleRow = mHoleRow + 1
            if c.calctype == 0 or c.calctype == 1:
                p1.holeconfig_flag = c.flag
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    x = p1.gh - c.l_holedepth
                    y = c.l_bigcap + hc * i + p1.bg_u_miny
                    if c.ismirror == 1: y = p1.bg_u_maxy - (c.l_bigcap + hc * i)  # 镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # A面，内测，外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_UpFace1' + '\n')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, y+offset,x, c.l_holedepth, c.id, t,
                                  c.l_smallcap, \
                                  hc, 'Up', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap,0 )
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])):  # //B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_UpFace2' + '\n')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,
                                  c.l_smallcap,
                                  hc, 'Up', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap,0 )
            if c.calctype == 2:  # // // 前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round(p1.gp - hc * (c.holenum - 1)) / 2
                for i in range(0,int(c.holenum // 2)):  # 前后端等距
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    x = p1.gh - c.l_holedepth
                    y = l_bigcap + hc * i + p1.bg_u_miny
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # A面内测外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_UpFace3' + '\n')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id,
                                  t, c.l_smallcap, hc, 'Up', 'L', c.l_bigname, c.l_smallname,
                                  c.i_name, mx_flag, c.mx_cap,0 )
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])):  # B面， 内测， 外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_UpFace4' + '\n')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth,
                                  c.id, t, c.l_smallcap, hc, 'Up', 'L', c.l_bigname, c.l_smallname,
                                  c.i_name, mx_flag, c.mx_cap,0 )
                for i in range(0,int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    x = p1.gh - c.l_holedepth
                    y = p1.bg_u_maxy - (l_bigcap + hc * i)
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # B面，内测， 外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_UpFace5' + '\n')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix,  y + offset, x, c.l_holedepth, c.id, t,
                                  c.l_smallcap,
                                  hc, 'Up', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0 )
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [1])):  # B面， 内测， 外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_UpFace6' + '\n')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix,  y + offset, x,c.l_holedepth,
                                  c.id, t, c.l_smallcap, hc, 'Up', 'L', c.l_bigname, c.l_smallname,
                                  c.i_name, mx_flag, c.mx_cap,0 )
                # 中心孔
                cstart = p1.bg_u_miny + (p1.bg_u_maxy - p1.bg_u_miny) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0:
                    cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = p1.gh - c.l_holedepth
                    y = cstart + chc * i
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # A面，内测， 外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_UpFace7' + '\n')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,
                                  c.l_smallcap, hc, 'Up', 'L', c.l_bigname, c.l_smallname, c.i_name)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # // B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_UpFace8' + '\n')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,
                                  c.l_smallcap, hc, 'Up', 'L', c.l_bigname, c.l_smallname, c.i_name)
        if (c.i_isoutput == 1) and (algorithm in [0, 1]):  # // 纹理面
            mHoleRow = mHoleRow + 1  # 排孔数
            if face == 0:
                smallcap = c.l_smallcap
            else:
                smallcap = p1.gl - c.l_smallcap
            if (c.calctype == 0) or (c.calctype == 1):  # 靠背对齐； 靠背对齐- 三排孔
                p2.holeconfig_flag = c.flag2
                p2.hole_back_cap = p1.y - p2.y + c.l_bigcap
                p2.hole_2_dist = hc
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    ho.mx_x = 0
                    if mx_flag == 0:
                        ho.mx_y = c.mx_cap
                    else:
                        ho.mx_y = -c.mx_cap
                    ho.mx_z = 0
                    x = p1.x - p2.x + smallcap
                    y = p1.y - p2.y + c.l_bigcap + hc * i + p1.bg_u_miny
                    if c.ismirror == 1: y = p1.bg_u_maxy - (c.l_bigcap + hc * i) + p1.y - p2.y  # 镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, c.i_offsetvalue, 0)
                    ho.wx = smallcap
                    ho.wy = c.l_bigcap + hc * i + p1.bg_u_miny+offset
                    if c.ismirror == 1: ho.wy = p1.bg_u_maxy - c.l_bigcap - hc * i + offset
                    ho.wz = p1.gh
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_UpFace9' + '\n')
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, x, y+offset, 0, c.id, t, c.l_smallcap, hc,
                              'Up', 'I', c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap)
                    if c.calctype == 1:
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_UpFace10' + '\n')
                        AddHole_A(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(c.pkcap, 0, 0)), x + c.pkcap,
                                  0, y + offset, c.id, t, c.l_smallcap, hc, 'Up', 'I', c.i_name, '', c.i_name,
                                  mx_flag, 0, c.mx_cap)
                        # // ho.wz:= smallcap - c.pkcap;
                        AddHole_A(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(-c.pkcap,0, 0)), x - c.pkcap,
                                  0, y + offset, c.id, t, c.l_smallcap, hc, 'Up', 'I', c.i_name, '', c.i_name,
                                  mx_flag, 0, c.mx_cap)
            if c.calctype == 2:  # 前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round((p1.gp - hc * (c.holenum - 1)) / 2)
                for i in range(0,int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0:  mx_flag = 0
                    ho.mx_x = 0
                    if mx_flag == 0:
                        ho.mx_y = c.mx_cap
                    else:
                        ho.mx_y = -c.mx_cap
                    ho.mx_z = 0
                    x = p1.x - p2.x + smallcap
                    y = p1.y - p2.y + l_bigcap + hc * i + p1.bg_u_miny
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0,  c.i_offsetvalue, 0)
                    ho.wx = smallcap
                    ho.wy = l_bigcap + hc * i + p1.bg_u_miny+offset
                    ho.wz = p1.gh
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_UpFace11' + '\n')
                    AddHole_A(c, p2,
                              p1, ho, IdentityHmgMatrix, x, y + offset, 0, c.id, t, c.l_smallcap, hc,
                              'Up', 'I', c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    ho.mx_x = 0
                    if mx_flag == 0:
                        ho.mx_y = c.mx_cap
                    else:
                        ho.mx_y = -c.mx_cap
                    ho.mx_z = 0
                    x = p1.x - p2.x + smallcap
                    y = p1.y - p2.y + (p1.bg_u_maxy - (l_bigcap + hc * i))
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, c.i_offsetvalue, 0)  # ???
                    ho.wx = smallcap
                    ho.wy = (p1.bg_u_maxy - (l_bigcap + hc * i))+offset
                    ho.wz = p1.gh
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_UpFace12' + '\n')
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, x, y + offset, 0, c.id, t, c.l_smallcap, hc, 'Up',
                              'I',c.i_name, '', c.i_name, mx_flag, 0, c.mx_cap)
                # 中心孔
                cstart = p1.bg_u_miny + (p1.bg_u_maxy - p1.bg_u_miny) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0: cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = p1.x - p2.x + smallcap
                    y = p1.y - p2.y + cstart + chc * i
                    p2.big_p = p1
                    MakeVector(ho.i_offset, 0, c.i_offsetvalue, 0)
                    ho.wx = smallcap
                    ho.wy = cstart + chc * i + offset
                    ho.wz = p1.gh
                    #print '1=',len(mHPInfoList)
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_UpFace13' + '\n')
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, x, y + offset, 0, c.id, t, c.l_smallcap,
                              hc, 'Up', 'I', c.i_name, '', c.i_name)
    if (((di1 in [2, 3]) and (di2 in [1, 5])) or ((algorithm == 2) and (di1 in [2, 3]) and (di2 in [2, 3]))) and \
            (p1.y >= p2.y) and (p1.y + p1.gp <= p2.y + p2.gp) and \
            (IsLSIntersection(p1.x + p1.bg_u_minx, p1.x + p1.bg_u_maxx, p2.x + p2.bg_d_minx, p2.x + p2.bg_d_maxx) == 1):
        # 层板与背板接触，层板横纹，背板竖纹
        if nocalc: return
        offset = 0
        if algorithm == 1:
            # 按接触面计算
            if p2.gl + p2.x > p2.x:
                t = p2.x
            else:
                t = p2.gl + p2.x
            if t > p1.x: offset = t - p1.x
        UpdateTempExpVariable(p1)
        l = Length_HoleFace(p1, p2, c, 4, 0)  # // 左面1, // 右面2, // 下面3, // 上面4, // 后面5, // 前面6
        if c.algorithm == 0:  # // 兼容算法
            t = (p1.bg_u_maxx + p1.x) - (p2.gl + p2.x)
            if (t > 0) and (c.calctype in [0, 1]): l = l - t  # 接触面较小
            if p1.zero_y == 2:  # 右封边
                t = (p1.bg_u_minx + p1.x) - p2.x
                if (t < 0) and (c.calctype in [0, 1]): l = l + t  # 接触面较小
        mTmpExp['L'] = l
        # mTmpExp
        # c.holecap,c.center_holecap
        hc = int(SimpleExpressToValue(c.holecap, 2, mTmpExp))
        chc = int(SimpleExpressToValue(c.center_holecap, 2, mTmpExp))
        if c.l_isoutput == 1:
            mHoleRow = mHoleRow + 1
            if (c.calctype == 0) or (c.calctype == 1):
                p1.holeconfig_flag = c.flag
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    x = p1.gh - c.l_holedepth
                    y = c.l_bigcap + hc * i + p1.bg_u_minx
                    if c.ismirror == 1: y = p1.bg_u_maxx - (c.l_bigcap + hc * i)  # 镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) or \
                            ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # A面， 内测， 外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_UpFace14' + '\n')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc,'Up', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) or \
                            ((c.bigface == 3) and (p1.holeface in [2])):  # B面， 内测， 外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_UpFace15' + '\n')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc, 'Up', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
            if c.calctype == 2:  # 前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round((p1.gl - hc * (c.holenum - 1)) / 2)
                # 'c.holenum',c.holenum
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    x = p1.gh - c.l_holedepth
                    y = l_bigcap + hc * i + p1.bg_u_minx
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # // A面，内侧，外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_UpFace16' + '\n')
                        AddHole_A(c, p1,p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t, c.l_smallcap,
                                  hc,'Up', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # //B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_UpFace17' + '\n')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,c.l_smallcap,
                                  hc, 'Up', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    x = p1.gh - c.l_holedepth
                    y = p1.bg_u_maxx - (l_bigcap + hc * i)
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # // A面，内侧，外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_UpFace18' + '\n')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,c.l_smallcap,
                                  hc, 'Up', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag, c.mx_cap, 0)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # // B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_UpFace19' + '\n')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,
                                  c.l_smallcap, hc, 'Up', 'L', c.l_bigname, c.l_smallname, c.i_name, mx_flag,
                                  c.mx_cap, 0)
                # 中心孔
                cstart = p1.bg_u_minx + (p1.bg_u_maxx - p1.bg_u_minx) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0: cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = p1.gh - c.l_holedepth
                    y = cstart + chc * i
                    # if len(mHPInfoList) == 40:
                    #     print 'x=',x,'y=',y,'gh=',p1.gh,'l_holedepth=',c.l_holedepth
                    #     print 'cstart=',cstart,'chc=',chc,'i=',i
                    if (c.bigface == 0) or ((c.bigface == 2) and (p1.holeface in [0, 1, 3])) \
                            or ((c.bigface == 3) and (p1.holeface in [0, 2, 3])):  # // A面，内侧，外侧
                        face = 0
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_UpFace20' + '\n')
                        AddHole_A(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,
                                  c.l_smallcap,hc, 'Up', 'L', c.l_bigname, c.l_smallname, c.i_name)
                    if (c.bigface == 1) or ((c.bigface == 2) and (p1.holeface in [2])) \
                            or ((c.bigface == 3) and (p1.holeface in [1])):  # // B面，内侧，外侧
                        face = 1
                        p1.big_p = None
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_UpFace21' + '\n')
                        AddHole_B(c, p1, p2, ho, IdentityHmgMatrix, y + offset, x, c.l_holedepth, c.id, t,
                                  c.l_smallcap,hc, 'Up', 'L', c.l_bigname, c.l_smallname, c.i_name)
        if (c.i_isoutput == 1) and (algorithm in [0, 1]):
            mHoleRow = mHoleRow + 1
            if face == 0:
                smallcap = c.l_smallcap
            else:
                smallcap = p1.gp - c.l_smallcap
            if (c.calctype == 0) or (c.calctype == 1):  # 靠背对齐
                p2.holeconfig_flag = c.flag2
                p2.hole_back_cap = p1.x - p2.x + c.l_bigcap
                p2.hole_2_dist = hc
                for i in range(0, c.holenum):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if i == c.holenum - 1: mx_flag = 1
                    if mx_flag == 0:
                        ho.mx_x = c.mx_cap
                    else:
                        ho.mx_x = -c.mx_cap
                    ho.mx_y = 0
                    ho.mx_z = 0
                    x = p1.x - p2.x + c.l_bigcap + hc * i + p1.bg_u_minx
                    y = p1.y - p2.y + smallcap
                    if c.ismirror == 1: x = p1.bg_u_maxx - (c.l_bigcap + hc * i) + p1.y - p2.y  # // 镜像
                    if i == 0:
                        t = 1
                    else:
                        t = hc
                    p2.big_p = p1
                    MakeVector(ho.i_offset, c.i_offsetvalue, 0, 0 )
                    ho.wx = c.l_bigcap + hc * i + p1.bg_u_minx + offset
                    if c.ismirror == 1: ho.wx = p1.bg_u_maxx - c.l_bigcap - hc * i + offset
                    ho.wy = smallcap
                    ho.wz = p1.gh
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_UpFace22' + '\n')
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, x + offset, y, 0, c.id, t,
                              c.l_smallcap, hc, 'Up', 'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
                    if c.calctype == 1:
                        #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                        log.debug('CalcHole_UpFace23' + '\n')
                        AddHole_A(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(0, c.pkcap, 0)), x + offset,
                                  y + c.pkcap, 0, c.id, t, c.l_smallcap, hc, 'Up', 'I', c.i_name, '',
                                  c.i_name, mx_flag, c.mx_cap, 0)
                        # // ho.wy:= smallcap - c.pkcap;
                        AddHole_A(c, p2, p1, ho, CreateTranslationMatrix(VectorMake(0, -c.pkcap, 0)), x + offset,
                                  y - c.pkcap, 0, c.id, t, c.l_smallcap, hc, 'Up',
                                  'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
            if c.calctype == 2:  # 前后端等距
                t = 0
                l_bigcap = c.l_bigcap
                if l_bigcap <= 0: l_bigcap = Delphi_Round((p1.gl - hc * (c.holenum - 1)) / 2)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 0
                    if mx_flag == 0:
                        ho.mx_x = c.mx_cap
                    else:
                        ho.mx_x = -c.mx_cap
                    ho.mx_y = 0
                    ho.mx_z = 0
                    x = p1.x - p2.x + l_bigcap + hc * i + p1.bg_u_minx
                    y = p1.y - p2.y + smallcap
                    p2.big_p = p1
                    MakeVector(ho.i_offset, c.i_offsetvalue, 0, 0)  # ???
                    ho.wx = l_bigcap + hc * i + p1.bg_u_minx+offset
                    ho.wy = smallcap
                    ho.wz = p1.gh
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_UpFace24' + '\n')
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, x + offset, y, 0, c.id, t,
                              c.l_smallcap, hc, 'Up', 'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
                for i in range(0, int(c.holenum // 2)):
                    mx_flag = -1
                    if i == 0: mx_flag = 1
                    if mx_flag==0 : ho.mx_x = c.mx_cap
                    else: ho.mx_x = -c.mx_cap
                    ho.mx_y = 0
                    ho.mx_z = 0
                    x = p1.x - p2.x + (p1.bg_u_maxx - (l_bigcap + hc * i))
                    y = p1.y - p2.y + smallcap
                    p2.big_p = p1
                    MakeVector(ho.i_offset, c.i_offsetvalue, 0, 0)  # ???
                    ho.wx = (p1.bg_u_maxx - (l_bigcap + hc * i))+offset
                    ho.wy = smallcap
                    ho.wz = p1.gh
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_UpFace25' + '\n')
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, x + offset, y, 0, c.id, t,
                              c.l_smallcap, hc, 'Up', 'I', c.i_name, '', c.i_name, mx_flag, c.mx_cap, 0)
                # // 中心孔
                cstart = p1.bg_u_minx + (p1.bg_u_maxx - p1.bg_u_minx) // 2 + ((c.center_holenum - 1) % 2) * (chc // 2)
                if ((c.center_holenum) // 2) > 0: cstart = cstart - ((c.center_holenum) // 2) * chc
                for i in range(0, c.center_holenum):
                    x = p1.x - p2.x + cstart + chc * i
                    y = p1.y - p2.y + smallcap
                    p2.big_p = p1
                    MakeVector(ho.i_offset, c.i_offsetvalue, 0, 0)
                    ho.wx = cstart + chc * i + offset
                    ho.wy = smallcap
                    ho.wz = p1.gh
                    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                    log.debug('CalcHole_UpFace26' + '\n')
                    AddHole_A(c, p2, p1, ho, IdentityHmgMatrix, x + offset, y, 0, c.id, t, c.l_smallcap,
                              hc, 'Up', 'I', c.i_name, '', c.i_name)
def AddOffsetIHole_A(c, p, p2, ho, x, y, hd, holeid, offset, smallcap, holecap, face, holetype, hole, sr, sri, \
                         mx_flag=-1, mx_x=0, mx_y=0):
    global mHPInfoList
    def ResetValue():
        x = t_x
        y = t_y
        face = t_face
        holetype = t_holetype
    t_x = x
    t_y = y
    t_face = face
    t_holetype = holetype
    for i in range(0,101):
        if p2.ahole_index[i] == -1:
            ResetValue()
            p2.ahole_index[i] = len(mHPInfoList)
            hpinfo = THolePointInfo()
            mHPInfoList.append(hpinfo)
            #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
            log.debug('AddOffsetIHole_AmHPInfoList1=' + str(len(mHPInfoList))+'\n')
            #print 'AddOffsetIHole_AmHPInfoList1=', len(mHPInfoList)
            mTmpExp['$SX'] =  str(p.x)
            mTmpExp['$SY'] =  str(p.y)
            mTmpExp['$SZ'] = str(p.z)
            mTmpExp['$DX'] = str(p2.x)
            mTmpExp['$DY'] = str(p2.y)
            mTmpExp['$DZ'] = str(p2.z)
            mTmpExp['$SL'] = str(p.gl)
            mTmpExp['$SD'] = str(p.gp)
            mTmpExp['$SH'] = str(p.gh)
            mTmpExp['$DL'] = str(p2.gl)
            mTmpExp['$DD'] = str(p2.gp)
            mTmpExp['$DH'] = str(p2.gh)
            mTmpExp['$X'] = str(x)
            mTmpExp['$Y'] = str(y)
            x = int(exp(mTmpExp,c.xo))
            y = int(exp(mTmpExp,c.yo))
            hpinfo.x = x
            hpinfo.y = y
            hpinfo.xx = 0
            hpinfo.yy = 0
            hpinfo.hd = hd
            hpinfo.r = c.i_name
            hpinfo.sri = sri
            hpinfo.htype = 'I'
            hpinfo.holeid = holeid
            hpinfo.row = mHoleRow
            hpinfo.offset = offset
            hpinfo.face = face
            hpinfo.sr = sr
            hpinfo.smallcap = smallcap
            hpinfo.holecap = holecap
            hpinfo.c = c
            hpinfo.isii = 0
            hpinfo.b_bh = Delphi_Round(p.bh)
            #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
            log.debug('AddOffsetIHole_AmHPInfoList1=' + 'x=' + str(pnumber(hpinfo.x)) + ',y=' + str(pnumber(hpinfo.y)) + ',xx=' + str(hpinfo.xx)
                        + ',yy=' + str(hpinfo.yy) + ',hd=' + str(hpinfo.hd) + ',hpinfo.r=' + str(
                    hpinfo.r) + ',sri=' + str(hpinfo.sri)
                        + ',htype=' + hpinfo.htype + ',holeid=' + str(hpinfo.holeid) + ',row=' + str(hpinfo.row)
                        + ',offset=' + str(hpinfo.offset) + ',face=' + str(hpinfo.face) + ',sr=' + str(
                    sr) + ',smallcap=' + str(smallcap)
                        + ',holecap=' + str(hpinfo.holecap) + ',isii=' + str(hpinfo.isii) +
                        '\n')
            break
    if (c != None) and (mx_flag>=0) and c.mx_isoutput ==1:
        ResetValue()
        if mx_flag == 0:
            x = x + mx_x
            y = y + mx_y
        else:
            x = x - mx_x
            y = y - mx_y
        for i in range(0,101):
            if p2.ahole_index[i] == -1:
                ResetValue()
                p2.ahole_index[i] = len(mHPInfoList)
                hpinfo = THolePointInfo()
                mHPInfoList.append(hpinfo)
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug('AddOffsetIHole_AmHPInfoList2=' + str(len(mHPInfoList))+'\n')
                #print 'AddOffsetIHole_AmHPInfoList2=', len(mHPInfoList)
                mTmpExp['$SX'] = str(p.x)
                mTmpExp['$SY'] = str(p.y)
                mTmpExp['$SZ'] = str(p.z)
                mTmpExp['$DX'] = str(p2.x)
                mTmpExp['$DY'] = str(p2.y)
                mTmpExp['$DZ'] = str(p2.z)
                mTmpExp['$SL'] = str(p.gl)
                mTmpExp['$SD'] = str(p.gp)
                mTmpExp['$SH'] = str(p.gh)
                mTmpExp['$DL'] = str(p2.gl)
                mTmpExp['$DD'] = str(p2.gp)
                mTmpExp['$DH'] = str(p2.gh)
                mTmpExp['$X'] = str(x)
                mTmpExp['$Y'] = str(y)
                x = int(exp(mTmpExp, c.xo))
                y = int(exp(mTmpExp, c.yo))
                hpinfo.x = x
                hpinfo.y = y
                hpinfo.xx = 0
                hpinfo.yy = 0
                hpinfo.hd = hd
                hpinfo.r = '0'
                hpinfo.sri = sri
                hpinfo.htype = 'I'
                hpinfo.r = c.mx_name
                hpinfo.sri = c.mx_name
                hpinfo.row = mHoleRow
                hpinfo.offset = offset
                hpinfo.face = face
                hpinfo.smallcap = smallcap
                hpinfo.holecap = holecap
                hpinfo.c = c
                hpinfo.isii = 0
                hpinfo.b_bh = Delphi_Round(p.bh)
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug(
                        'AddOffsetIHole_AmHPInfoList2=' + 'x=' + str(pnumber(hpinfo.x)) + ',y=' + str(pnumber(hpinfo.y)) + ',xx=' + str(
                            hpinfo.xx)
                        + ',yy=' + str(hpinfo.yy) + ',hd=' + str(hpinfo.hd) + ',hpinfo.r=' + str(
                            hpinfo.r) + ',sri=' + str(hpinfo.sri)
                        + ',htype=' + hpinfo.htype + ',holeid=' + str(hpinfo.holeid) + ',row=' + str(hpinfo.row)
                        + ',offset=' + str(hpinfo.offset) + ',face=' + str(hpinfo.face) + ',sr=' + str(
                            sr) + ',smallcap=' + str(smallcap)
                        + ',holecap=' + str(hpinfo.holecap) + ',isii=' + str(hpinfo.isii) +
                        '\n')
                break
def AddOffsetIHole_B(c, p, p2, ho, x, y, hd, holeid, offset, smallcap, holecap, face, holetype, hole, sr, sri, \
                         mx_flag=-1, mx_x=0, mx_y=0):
    global mHPInfoList
    def ResetValue():
        x = t_x
        y = t_y
        face = t_face
        holetype = t_holetype
    t_x = x
    t_y = y
    t_face = face
    t_holetype = holetype
    for i in range(0,101):
        if p2.bhole_index[i] == -1:
            ResetValue()
            p.bhole_index[i] = len(mHPInfoList)
            hpinfo = THolePointInfo()
            mHPInfoList.append(hpinfo)
            #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
            log.debug('AddOffsetIHole_B1=' + str(len(mHPInfoList))+'\n')
            #print 'AddOffsetIHole_B1=',len(mHPInfoList)
            mTmpExp['$SX'] =  str(p.x)
            mTmpExp['$SY'] =  str(p.y)
            mTmpExp['$SZ'] = str(p.z)
            mTmpExp['$DX'] = str(p2.x)
            mTmpExp['$DY'] = str(p2.y)
            mTmpExp['$DZ'] = str(p2.z)
            mTmpExp['$SL'] = str(p.gl)
            mTmpExp['$SD'] = str(p.gp)
            mTmpExp['$SH'] = str(p.gh)
            mTmpExp['$DL'] = str(p2.gl)
            mTmpExp['$DD'] = str(p2.gp)
            mTmpExp['$DH'] = str(p2.gh)
            mTmpExp['$X'] = str(x)
            mTmpExp['$Y'] = str(y)
            x = int(exp(mTmpExp,c.xo))
            y = int(exp(mTmpExp,c.yo))
            hpinfo.x = x
            hpinfo.y = y
            hpinfo.xx = 0
            hpinfo.yy = 0
            hpinfo.hd = hd
            hpinfo.r = c.i_name
            hpinfo.sri = sri
            hpinfo.htype = 'I'
            hpinfo.holeid = holeid
            hpinfo.row = mHoleRow
            hpinfo.offset = offset
            hpinfo.face = face
            hpinfo.sr = sr
            hpinfo.smallcap = smallcap
            hpinfo.holecap = holecap
            hpinfo.c = c
            hpinfo.isii = 0
            hpinfo.b_bh = Delphi_Round(p.bh)
            #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
            log.debug(
                    'AddOffsetIHole_B1=' + 'x=' + str(pnumber(hpinfo.x)) + ',y=' + str(pnumber(hpinfo.y)) + ',xx=' + str(
                        hpinfo.xx)
                    + ',yy=' + str(hpinfo.yy) + ',hd=' + str(hpinfo.hd) + ',hpinfo.r=' + str(
                        hpinfo.r) + ',sri=' + str(hpinfo.sri)
                    + ',htype=' + hpinfo.htype + ',holeid=' + str(hpinfo.holeid) + ',row=' + str(hpinfo.row)
                    + ',offset=' + str(hpinfo.offset) + ',face=' + str(hpinfo.face) + ',sr=' + str(
                        sr) + ',smallcap=' + str(smallcap)
                    + ',holecap=' + str(hpinfo.holecap) + ',isii=' + str(hpinfo.isii) +
                    '\n')
            break
    if (c != None) and (mx_flag>=0) and c.mx_isoutput ==1:
        ResetValue()
        if mx_flag == 0:
            x = x + mx_x
            y = y + mx_y
        else:
            x = x - mx_x
            y = y - mx_y
        for i in range(0,101):
            if p2.bhole_index[i] == -1:
                ResetValue()
                p.bhole_index[i] = len(mHPInfoList)
                hpinfo = THolePointInfo()
                mHPInfoList.append(hpinfo)
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug('AddOffsetIHole_B2=' + str(len(mHPInfoList))+'\n')
                #print 'AddOffsetIHole_B2=',len(mHPInfoList)
                mTmpExp['$SX'] = str(p.x)
                mTmpExp['$SY'] = str(p.y)
                mTmpExp['$SZ'] = str(p.z)
                mTmpExp['$DX'] = str(p2.x)
                mTmpExp['$DY'] = str(p2.y)
                mTmpExp['$DZ'] = str(p2.z)
                mTmpExp['$SL'] = str(p.gl)
                mTmpExp['$SD'] = str(p.gp)
                mTmpExp['$SH'] = str(p.gh)
                mTmpExp['$DL'] = str(p2.gl)
                mTmpExp['$DD'] = str(p2.gp)
                mTmpExp['$DH'] = str(p2.gh)
                mTmpExp['$X'] = str(x)
                mTmpExp['$Y'] = str(y)
                x = int(exp(mTmpExp, c.xo))
                y = int(exp(mTmpExp, c.yo))
                hpinfo.x = x
                hpinfo.y = y
                hpinfo.xx = 0
                hpinfo.yy = 0
                hpinfo.hd = hd
                hpinfo.r = '0'
                hpinfo.sri = sri
                hpinfo.htype = 'I'
                hpinfo.r = c.mx_name
                hpinfo.sri = c.mx_name
                hpinfo.holeid = holeid
                hpinfo.row = mHoleRow
                hpinfo.offset = offset
                hpinfo.face = face
                hpinfo.smallcap = smallcap
                hpinfo.holecap = holecap
                hpinfo.c = c
                hpinfo.isii = 0
                hpinfo.b_bh = Delphi_Round(p.bh)
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug(
                        'AddOffsetIHole_B2=' + 'x=' + str(pnumber(hpinfo.x)) + ',y=' + str(pnumber(hpinfo.y)) + ',xx=' + str(
                            hpinfo.xx)
                        + ',yy=' + str(hpinfo.yy) + ',hd=' + str(hpinfo.hd) + ',hpinfo.r=' + str(
                            hpinfo.r) + ',sri=' + str(hpinfo.sri)
                        + ',htype=' + hpinfo.htype + ',holeid=' + str(hpinfo.holeid) + ',row=' + str(hpinfo.row)
                        + ',offset=' + str(hpinfo.offset) + ',face=' + str(hpinfo.face) + ',sr=' + str(
                            sr) + ',smallcap=' + str(smallcap)
                        + ',holecap=' + str(hpinfo.holecap) + ',isii=' + str(hpinfo.isii) +
                        '\n')
                break
def AddIHole2_A(c, p, p2, ho, tm, x, y, hd, holeid, offset, smallcap, holecap,
    face, holetype, hole, sr, sri, mx_flag=-1, mx_x=0, mx_y=0):
    global mHPInfoList
    t = 2 # 存在计算误差， 或者设计误差， 板件接触面小于2 的时候也有孔产生
    v = [0,0,0]
    SetVector(v, ho.wx + ho.i_offset[0], ho.wy + ho.i_offset[1], ho.wz + ho.i_offset[2])    #？？？？
    #计算旋转的板件
    ## 'x=',x,'y=',y,'sri=',sri
        #sys.exit(1)
    #
    if p2.xptlist_jx in [3,4]:
        angle = p2.var_args[0]
        m = IdentityHmgMatrix # ???
        if (p2.xptlist_pl==1) and (p2.xptlist_jx==3) :
            m = CreateRotationMatrix((1, 0, 0), DegToRad(angle))
        if (p2.xptlist_pl==1) and (p2.xptlist_jx==4) :
            m = CreateRotationMatrix(AffineVectorMake(0, 1, 0), DegToRad(angle))
        if (p2.xptlist_pl==2) and (p2.xptlist_jx==3) :
            m = CreateRotationMatrix(AffineVectorMake(1, 0, 0), DegToRad(angle))
        if (p2.xptlist_pl==2) and (p2.xptlist_jx==4) :
            m = CreateRotationMatrix(AffineVectorMake(0, 0, 1), DegToRad(angle))
        if (p2.xptlist_pl==3) and (p2.xptlist_jx==3) :
            m = CreateRotationMatrix(AffineVectorMake(0, 1, 0), DegToRad(angle))
        if (p2.xptlist_pl==3) and (p2.xptlist_jx==4) :
            m=CreateRotationMatrix(AffineVectorMake(0, 0, 1), DegToRad(angle))
        m2 = MatrixMultiply(m, MatrixMultiply(p2.m, tm))
    else:
        ## 'p2.m=',p2.m,'tm=',tm
        m2 = MatrixMultiply(p2.m, tm)
    m3 = p2.m.tolist()
    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
    log.debug(
            'p2.m=' + str(pnumber(m3[0][0])) + ',' + str(pnumber(m3[0][1])) + ',' + str(pnumber(m3[0][2])) + ',' + str(
                pnumber(m3[0][3])) + ',' \
            + str(pnumber(m3[1][0])) + ',' + str(pnumber(m3[1][1])) + ',' + str(pnumber(m3[1][2])) + ',' + str(
                pnumber(m3[1][3])) + ',' \
            + str(pnumber(m3[2][0])) + ',' + str(pnumber(m3[2][1])) + ',' + str(pnumber(m3[2][2])) + ',' + str(
                pnumber(m3[2][3])) + ',' \
            + str(pnumber(m3[3][0])) + ',' + str(pnumber(m3[3][1])) + ',' + str(pnumber(m3[3][2])) + ',' + str(
                pnumber(m3[3][3])) + '\n')
    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
    log.debug(
            'tm=' + str(pnumber(tm[0][0])) + ',' + str(pnumber(tm[0][1])) + ',' + str(pnumber(tm[0][2])) + ',' + str(
                pnumber(tm[0][3])) + ',' \
            + str(pnumber(tm[1][0])) + ',' + str(pnumber(tm[1][1])) + ',' + str(pnumber(tm[1][2])) + ',' + str(
                pnumber(tm[1][3])) + ',' \
            + str(pnumber(tm[2][0])) + ',' + str(pnumber(tm[2][1])) + ',' + str(pnumber(tm[2][2])) + ',' + str(
                pnumber(tm[2][3])) + ',' \
            + str(pnumber(tm[3][0])) + ',' + str(pnumber(tm[3][1])) + ',' + str(pnumber(tm[3][2])) + ',' + str(
                pnumber(tm[3][3])) + '\n')
    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
    log.debug('v1=' + str(pnumber(v[0])) + ',' + str(pnumber(v[1])) + ',' + str(pnumber(v[2])) + '\n')
    m3 = m2.tolist()
    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
    log.debug(
            'm2=' + str(pnumber(m3[0][0])) + ',' + str(pnumber(m3[0][1])) + ',' + str(pnumber(m3[0][2])) + ',' + str(
                pnumber(m3[0][3])) + ',' \
            + str(pnumber(m3[1][0])) + ',' + str(pnumber(m3[1][1])) + ',' + str(pnumber(m3[1][2])) + ',' + str(
                pnumber(m3[1][3])) + ',' \
            + str(pnumber(m3[2][0])) + ',' + str(pnumber(m3[2][1])) + ',' + str(pnumber(m3[2][2])) + ',' + str(
                pnumber(m3[2][3])) + ',' \
            + str(pnumber(m3[3][0])) + ',' + str(pnumber(m3[3][1])) + ',' + str(pnumber(m3[3][2])) + ',' + str(
                pnumber(m3[3][3])) + '\n')
    v = VectorTransform(v, m2)
    ## 'v2=',v,p.m,MatrixInvert(p.m)
    m3 = p.m.tolist()
    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
    log.debug('v2=' + str(pnumber(v[0])) + ',' + str(pnumber(v[1])) + ',' + str(pnumber(v[2])) + '\n')
    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
    log.debug(
            'p.m=' + str(pnumber(m3[0][0])) + ',' + str(pnumber(m3[0][1])) + ',' + str(pnumber(m3[0][2])) + ',' + str(
                pnumber(m3[0][3])) + ',' \
            + str(pnumber(m3[1][0])) + ',' + str(pnumber(m3[1][1])) + ',' + str(pnumber(m3[1][2])) + ',' + str(
                pnumber(m3[1][3])) + ',' \
            + str(pnumber(m3[2][0])) + ',' + str(pnumber(m3[2][1])) + ',' + str(pnumber(m3[2][2])) + ',' + str(
                pnumber(m3[2][3])) + ',' \
            + str(pnumber(m3[3][0])) + ',' + str(pnumber(m3[3][1])) + ',' + str(pnumber(m3[3][2])) + ',' + str(
                pnumber(m3[3][3])) + '\n')
    v = VectorTransform(v, MatrixInvert(p.m))
    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
    log.debug('v3=' + str(pnumber(v[0])) + ',' + str(pnumber(v[1])) + ',' + str(pnumber(v[2])) + '\n')
    op = p.self_p
    xx = 0
    yy = 0
    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
    log.debug('op.direct=' + str(op.direct) +'v0='+str(v[0])+'v1='+str(v[1])+'v2='+str(v[2])+'\n')
    if op.direct in [1, 5] : # // 层板
        x = int(float(str(v[0])))
        xx = v[0] - x
        y = int(float(str(v[1])))
        yy = v[1] - y
        t = Delphi_Round(v[2])
    if op.direct in [4,6]: #侧板
        x = int(float(str(v[1])))
        xx = v[1] - x
        y = int(float(str(v[2])))
        yy = v[2] - y
        t = Delphi_Round(v[0])
    if op.direct in [2, 3]: #背板
        x= int(float(str(v[0])))
        xx = v[0] - x
        y = int(float(str(v[2])))
        yy = v[2] - y
        t = Delphi_Round(v[1])
    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
    log.debug('x=' + str(x)+'xx=' + str(xx)+'y=' + str(y)+'yy=' + str(yy)+'t='+str(t) +'\n')
    for i in range(0,101):
        if t > 2 : hole_index = p.bhole_index[i]
        else: hole_index = p.ahole_index[i]
        if hole_index == -1 :
            if t > 2 : p.bhole_index[i]=len(mHPInfoList)
            else: p.ahole_index[i] = len(mHPInfoList)
            hpinfo = THolePointInfo()
            mHPInfoList.append(hpinfo)
            #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
            log.debug('AddIHole2_A1=' + str(len(mHPInfoList))+',t1='+str(int(t))+'\n')
            #print  'AddIHole2_A1:', len(mHPInfoList),'t1=',t
            hpinfo.x = x
            hpinfo.y = y
            hpinfo.xx = pnumber(xx)
            hpinfo.yy = pnumber(yy)
            hpinfo.hd = hd
            if c != None : hpinfo.r = c.i_name
            else: hpinfo.r = hole
            hpinfo.sri = sri
            hpinfo.htype = 'I'
            hpinfo.holeid = holeid
            hpinfo.row = mHoleRow
            hpinfo.offset = offset
            hpinfo.face = face
            hpinfo.sr = sr
            hpinfo.smallcap = smallcap
            hpinfo.holecap = holecap
            hpinfo.c = c
            hpinfo.isii = 0
            hpinfo.b_bh = Delphi_Round(p2.bh)
            #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
            log.debug('AddIHole2_A1=' + 'x=' + str(pnumber(hpinfo.x)) + ',y=' + str(pnumber(hpinfo.y))+',xx='+str(hpinfo.xx)
                        +',yy='+str(hpinfo.yy)+',hd='+str(hpinfo.hd)+',hpinfo.r='+str(hpinfo.r)+',sri='+str(hpinfo.sri)
                        +',htype='+hpinfo.htype+',holeid='+str(hpinfo.holeid)+',row='+str(hpinfo.row)
                        +',offset='+str(hpinfo.offset)+',face='+str(hpinfo.face)+',sr='+str(sr)+',smallcap='+str(smallcap)
                        +',holecap='+str(hpinfo.holecap)+',isii='+str(hpinfo.isii)+
                        '\n')
            break
    if (c != None) and (mx_flag>=0) and c.mx_isoutput ==1:
        SetVector(v, ho.wx + ho.mx_x, ho.wy + ho.mx_y, ho.wz + ho.mx_z)  # ？？？？
        ## '6666666'
        v = VectorTransform(v, m2)
        v = VectorTransform(v, MatrixInvert(p.m))
        op = p.self_p
        xx = 0
        yy = 0
        if op.direct in [1, 5]:  # // 层板
            x = int(float(str(v[0])))
            xx = v[0] - x
            y = int(float(str(v[1])))
            yy = v[1] - y
            t = Delphi_Round(v[2])
        if op.direct in [4, 6]:  # 侧板
            x = int(float(str(v[1])))
            xx = v[1] - x
            y = int(float(str(v[2])))
            yy = v[2] - y
            t = Delphi_Round(v[0])
        if op.direct in [2, 3]:  # 背板
            x = int(float(str(v[0])))
            xx = v[0] - x
            y = int(float(str(v[2])))
            yy = v[2] - y
            t = Delphi_Round(v[1])
        for i in range(0, 101):
            if t > 2 : hole_index = p.bhole_index[i]
            else: hole_index = p.ahole_index[i]
            if hole_index == -1:
                if t > 2:
                    p.bhole_index[i] = len(mHPInfoList)    #???一样
                else:
                    p.ahole_index[i] = len(mHPInfoList)    #???一样
                hpinfo = THolePointInfo()
                mHPInfoList.append(hpinfo)
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug('AddIHole2_A2=' + str(len(mHPInfoList))+',t2='+str(int(t))+'\n')
                #print  'AddIHole2_A2:', len(mHPInfoList),'t2=',t
                hpinfo.x = x
                hpinfo.y = y
                hpinfo.xx = pnumber(xx)
                hpinfo.yy = pnumber(yy)
                hpinfo.hd = hd
                hpinfo.r = '0'
                hpinfo.sri = sri
                hpinfo.htype = 'I'
                if c!=None: hpinfo.r = c.mx_name
                hpinfo.sri = c.mx_name
                hpinfo.row = mHoleRow
                hpinfo.offset = offset
                hpinfo.face = face
                hpinfo.smallcap = smallcap
                hpinfo.holecap = holecap
                hpinfo.c = c
                hpinfo.isii = 0
                hpinfo.b_bh = Delphi_Round(p2.bh)
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug('AddIHole2_A2=' + 'x=' + str(pnumber(hpinfo.x)) + ',y=' + str(pnumber(hpinfo.y)) + ',xx=' + str(hpinfo.xx)
                            + ',yy=' + str(hpinfo.yy) + ',hd=' + str(hpinfo.hd) + ',hpinfo.r=' + str(
                        hpinfo.r) + ',sri=' + str(hpinfo.sri)
                            + ',htype=' + hpinfo.htype + ',holeid=' + str(hpinfo.holeid) + ',row=' + str(hpinfo.row)
                            + ',offset=' + str(hpinfo.offset) + ',face=' + str(hpinfo.face) + ',sr=' + str(
                        sr) + ',smallcap=' + str(smallcap)
                            + ',holecap=' + str(hpinfo.holecap) + ',isii=' + str(hpinfo.isii) +
                            '\n')
                break
def AddIHole2_B(c, p, p2, ho, tm, x, y, hd, holeid, offset, smallcap, holecap,
    face, holetype, hole, sr, sri, mx_flag=-1, mx_x=0, mx_y=0):
    global mHPInfoList
    # if len(mHPInfoList) == 602:
    #     print ('x=' + str(x) + 'y=' + str(y))
    t = 2 # 存在计算误差， 或者设计误差， 板件接触面小于2 的时候也有孔产生
    v = [0,0,0]
    #print 'ho=',v, ho.wx + ho.i_offset[0], ho.wy + ho.i_offset[1], ho.wz + ho.i_offset[2]
    SetVector(v, ho.wx + ho.i_offset[0], ho.wy + ho.i_offset[1], ho.wz + ho.i_offset[2])
    #计算旋转的板件
    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
    log.debug('p2.xptlist_jx'+str(p2.xptlist_jx) +'\n')
    if p2.xptlist_jx in [3,4]:
        angle = p2.var_args[0]
        m = IdentityHmgMatrix
        if (p2.xptlist_pl==1) and (p2.xptlist_jx==3) :
            m = CreateRotationMatrix((1, 0, 0), DegToRad(angle))
        if (p2.xptlist_pl==1) and (p2.xptlist_jx==4) :
            m = CreateRotationMatrix(AffineVectorMake(0, 1, 0), DegToRad(angle))
        if (p2.xptlist_pl==2) and (p2.xptlist_jx==3) :
            m = CreateRotationMatrix(AffineVectorMake(1, 0, 0), DegToRad(angle))
        if (p2.xptlist_pl==2) and (p2.xptlist_jx==4) :
            m = CreateRotationMatrix(AffineVectorMake(0, 0, 1), DegToRad(angle))
        if (p2.xptlist_pl==3) and (p2.xptlist_jx==3) :
            m = CreateRotationMatrix(AffineVectorMake(0, 1, 0), DegToRad(angle))
        if (p2.xptlist_pl==3) and (p2.xptlist_jx==4) :
            m=CreateRotationMatrix(AffineVectorMake(0, 0, 1), DegToRad(angle))
        m2 = MatrixMultiply(m, MatrixMultiply(p2.m, tm))
    else:
        m2 = MatrixMultiply(p2.m, tm)
    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
    log.debug('v1='+str(int(v[0]))+','+str(int(v[1]))+','+str(int(v[2]))+ '\n')
    #print 'v1=',v,type(m2)
    m3 = m2.tolist()
    # #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
    #     log.debug('m2='+str(int(m3[0][0]))+','+str(int(m3[0][1]))+','+str(int(m3[0][2]))+','+str(int(m3[0][3]))+','\
    #     +str(int(m3[1][0]))+','+str(int(m3[1][1]))+','+str(int(m3[1][2]))+','+str(int(m3[1][3]))+','\
    #     +str(int(m3[2][0]))+','+str(int(m3[2][1]))+','+str(int(m3[2][2]))+','+str(int(m3[2][3]))+',' \
    #     +str(int(m3[3][0]))+','+str(int(m3[3][1]))+','+str(int(m3[3][2]))+','+str(int(m3[3][3]))+'\n')
    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
    log.debug('m2='+str((m3[0][0]))+','+str((m3[0][1]))+','+str((m3[0][2]))+','+str((m3[0][3]))+','\
        +str((m3[1][0]))+','+str((m3[1][1]))+','+str((m3[1][2]))+','+str((m3[1][3]))+','\
        +str((m3[2][0]))+','+str((m3[2][1]))+','+str((m3[2][2]))+','+str((m3[2][3]))+',' \
        +str((m3[3][0]))+','+str((m3[3][1]))+','+str((m3[3][2]))+','+str((m3[3][3]))+'\n')
    v = VectorTransform(v, m2)
    #print 'v2=',v,p.m
    m3 = p.m.tolist()
    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
    log.debug('v2=' + str(pnumber(v[0])) + ',' + str(pnumber(v[1])) + ',' + str(pnumber(v[2])) + '\n')
    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
    log.debug('p.m='+str(pnumber(m3[0][0]))+','+str(pnumber(m3[0][1]))+','+str(pnumber(m3[0][2]))+','+str(pnumber(m3[0][3]))+','\
        +str(pnumber(m3[1][0]))+','+str(pnumber(m3[1][1]))+','+str(pnumber(m3[1][2]))+','+str(pnumber(m3[1][3]))+','\
        +str(pnumber(m3[2][0]))+','+str(pnumber(m3[2][1]))+','+str(pnumber(m3[2][2]))+','+str(pnumber(m3[2][3]))+',' \
        +str(pnumber(m3[3][0]))+','+str(pnumber(m3[3][1]))+','+str(pnumber(m3[3][2]))+','+str(pnumber(m3[3][3]))+'\n')
    v = VectorTransform(v, MatrixInvert(p.m))
    #print 'v3=',v
    #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
    log.debug('v3=' + str(pnumber(v[0])) + ',' + str(pnumber(v[1])) + ',' + str(pnumber(v[2])) + '\n')
    op = p.self_p
    xx = 0
    yy = 0
    if op.direct in [1, 5] : # // 层板
        x = int(float(str(v[0])))
        xx = v[0] - x
        y = int(float(str(v[1])))
        yy = v[1] - y
        t = Delphi_Round(v[2])
    if op.direct in [4,6]: #侧板
        x = int(float(str(v[1])))
        xx = v[1] - x
        y = int(float(str(v[2])))
        yy = v[2] - y
        t = Delphi_Round(v[0])
    if op.direct in [2, 3]: #背板
        x= int(float(str(v[0])))
        xx = v[0] - x
        y = int(float(str(v[2])))
        yy = v[2] - y
        t = Delphi_Round(v[1])
    for i in range(0,101):
        if t > 2 : hole_index = p.bhole_index[i]
        else: hole_index = p.ahole_index[i]
        if hole_index == -1:
            if t > 2 : p.bhole_index[i] = len(mHPInfoList)
            else: p.ahole_index[i] = len(mHPInfoList)
            hpinfo = THolePointInfo()
            mHPInfoList.append(hpinfo)
            #print  'AddIHole2_B1:',len(mHPInfoList),'t1=',t
            #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
            log.debug('AddIHole2_B1='+str(len(mHPInfoList))+',t1='+str(int(t))+'\n')
            hpinfo.x = x
            hpinfo.y = y
            hpinfo.xx = pnumber(xx)
            hpinfo.yy = pnumber(yy)
            hpinfo.hd = hd
            if c != None : hpinfo.r = c.i_name
            else: hpinfo.r = hole
            hpinfo.sri = sri
            hpinfo.htype = 'I'
            hpinfo.holeid = holeid
            hpinfo.row = mHoleRow
            hpinfo.offset = offset
            # print 'r=',hpinfo.r,'offset=',hpinfo.offset
            hpinfo.face = face
            hpinfo.sr = sr
            hpinfo.smallcap = smallcap
            hpinfo.holecap = holecap
            hpinfo.c = c
            hpinfo.isii = 0
            hpinfo.b_bh = Delphi_Round(p2.bh)
            #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
            log.debug('AddIHole2_B1=' + 'x=' + str(pnumber(hpinfo.x)) + ',y=' + str(pnumber(hpinfo.y))+',xx='+str(hpinfo.xx)
                        +',yy='+str(hpinfo.yy)+',hd='+str(hpinfo.hd)+',hpinfo.r='+str(hpinfo.r)+',sri='+str(hpinfo.sri)
                        +',htype='+hpinfo.htype+',holeid='+str(hpinfo.holeid)+',row='+str(hpinfo.row)
                        +',offset='+str(hpinfo.offset)+',face='+str(hpinfo.face)+',sr='+str(sr)+',smallcap='+str(smallcap)
                        +',holecap='+str(hpinfo.holecap)+',isii='+str(hpinfo.isii)+
                        '\n')
            # if len(mHPInfoList) == 687:
            #     print 'y=', y, 'direct=', op.direct, 'x=', x
            #     exit(1)
            break
    if (c != None) and (mx_flag>=0) and c.mx_isoutput ==1:
        SetVector(v, ho.wx + ho.mx_x, ho.wy + ho.mx_y, ho.wz + ho.mx_z)
        v = VectorTransform(v, m2)
        v = VectorTransform(v, MatrixInvert(p.m))
        op = p.self_p
        xx = 0
        yy = 0
        if op.direct in [1, 5]:  # // 层板
            x = int(float(str(v[0])))
            xx = v[0] - x
            y = int(float(str(v[1])))
            yy = v[1] - y
            t = Delphi_Round(v[2])
        if op.direct in [4, 6]:  # 侧板
            x = int(float(str(v[1])))
            xx = v[1] - x
            y = int(float(str(v[2])))
            yy = v[2] - y
            t = Delphi_Round(v[0])
        if op.direct in [2, 3]:  # 背板
            x = int(float(str(v[0])))
            xx = v[0] - x
            y = int(float(str(v[2])))
            yy = v[2] - y
            t = Delphi_Round(v[1])
        for i in range(0, 101):
            if t > 2:
                hole_index = p.bhole_index[i]  # ???一样
            else:
                hole_index = p.bhole_index[i]  # ???一样
            # if x == 76 and y == 9 and hd == 0 and holeid == 292389:
            #     sys.exit(1)
            if hole_index == -1:
                if t > 2 : p.bhole_index[i] = len(mHPInfoList)
                else: p.ahole_index[i]= len(mHPInfoList)
                hpinfo = THolePointInfo()
                mHPInfoList.append(hpinfo)
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug('AddIHole2_B2=' + str(len(mHPInfoList))+',t2='+str(int(t))+'\n')
                # print 'AddIHole2_B2:', len(mHPInfoList),'t2=',t
                hpinfo.x = x
                hpinfo.y = y
                hpinfo.xx = pnumber(xx)
                hpinfo.yy = pnumber(yy)
                hpinfo.hd = hd
                hpinfo.r = '0'
                hpinfo.sri = sri
                hpinfo.htype = 'I'
                if c!=None: hpinfo.r = c.mx_name
                hpinfo.sri = c.mx_name
                hpinfo.holeid = holeid
                hpinfo.row = mHoleRow
                hpinfo.offset = offset
                hpinfo.face = face
                hpinfo.smallcap = smallcap
                hpinfo.holecap = holecap
                hpinfo.c = c
                hpinfo.isii = 0
                hpinfo.b_bh = Delphi_Round(p2.bh)
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug('AddIHole2_B2=' + 'x=' + str(pnumber(hpinfo.x)) + ',y=' + str(pnumber(hpinfo.y)) + ',xx=' + str(hpinfo.xx)
                            + ',yy=' + str(hpinfo.yy) + ',hd=' + str(hpinfo.hd) + ',hpinfo.r=' + str(
                        hpinfo.r) + ',sri=' + str(hpinfo.sri)
                            + ',htype=' + hpinfo.htype + ',holeid=' + str(hpinfo.holeid) + ',row=' + str(hpinfo.row)
                            + ',offset=' + str(hpinfo.offset) + ',face=' + str(hpinfo.face) + ',sr=' + str(
                        sr) + ',smallcap=' + str(smallcap)
                            + ',holecap=' + str(hpinfo.holecap) + ',isii=' + str(hpinfo.isii) +
                            '\n')
                break
def AddLHole_A(c, p, p2, x, y, hd, holeid, offset, smallcap, holecap,
        face, holetype, hole, sr, sri, mx_flag=-1, mx_x=0, mx_y=0):
    global mHPInfoList
    def ResetValue():
        x = t_x
        y = t_y
        face = t_face
        holetype = t_holetype
    t_x = x
    t_y = y
    t_face = face
    t_holetype = holetype
    ## 'hahhahahahah','x=',x,'y=',y
    for i in range(0,101):
        if p.ahole_index[i] == -1:
            ResetValue()
            p.ahole_index[i] = len(mHPInfoList)
            hpinfo = THolePointInfo()
            mHPInfoList.append(hpinfo)
            #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
            log.debug('AddLHole_A1='+str(len(mHPInfoList))+'\n')
            # print 'AddLHole_A1:',len(mHPInfoList)
            if (c!=None) and c.b_isoffset ==1 and holetype=='L':
                mTmpExp['$SL'] =  str(p.gl)
                mTmpExp['$SD'] =  str(p.gp)
                mTmpExp['$SH'] = str(p.gh)
                mTmpExp['$DL'] = str(p2.gl)
                mTmpExp['$DD'] = str(p2.gp)
                mTmpExp['$DH'] = str(p2.gh)
                mTmpExp['$X'] = str(x)
                mTmpExp['$Y'] = str(y)
                x = int(Delphi_Round(exp(mTmpExp,c.b_xo)))
                y = int(Delphi_Round(exp(mTmpExp,c.b_yo)))
            hpinfo.x = x
            hpinfo.y = y
            hpinfo.xx = 0
            hpinfo.yy = 0
            hpinfo.hd = hd
            hpinfo.r = hole
            hpinfo.sri = sri
            hpinfo.htype = holetype
            hpinfo.holeid = holeid
            hpinfo.row = mHoleRow
            hpinfo.offset = offset
            hpinfo.face = face
            hpinfo.sr = sr
            hpinfo.smallcap = smallcap
            hpinfo.holecap = holecap
            hpinfo.c = c
            hpinfo.isii = 0
            hpinfo.b_bh = Delphi_Round(p2.bh)
            #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
            log.debug('AddLHole_A1=' + 'x=' + str(pnumber(hpinfo.x)) + ',y=' + str(pnumber(hpinfo.y)) + ',xx=' + str(hpinfo.xx)
                        + ',yy=' + str(hpinfo.yy) + ',hd=' + str(hpinfo.hd) + ',hpinfo.r=' + str(
                    hpinfo.r) + ',sri=' + str(hpinfo.sri)
                        + ',htype=' + hpinfo.htype + ',holeid=' + str(hpinfo.holeid) + ',row=' + str(hpinfo.row)
                        + ',offset=' + str(hpinfo.offset) + ',face=' + str(hpinfo.face) + ',sr=' + str(
                    sr) + ',smallcap=' + str(smallcap)
                        + ',holecap=' + str(hpinfo.holecap) + ',isii=' + str(hpinfo.isii) +
                        '\n')
            break
    if (c != None) and (mx_flag>=0) and c.mx_isoutput ==1:
        ResetValue()
        if mx_flag == 0:
            x = x + mx_x
            y = y + mx_y
        else:
            x = x - mx_x
            y = y - mx_y
        for i in range(0,101):
            if p.ahole_index[i] == -1:
                p.ahole_index[i] = len(mHPInfoList)
                hpinfo = THolePointInfo()
                mHPInfoList.append(hpinfo)
                # print 'AddLHole_A2:', len(mHPInfoList)
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug('AddLHole_A2=' + str(len(mHPInfoList))+'\n')
                if c!= None and c.b_isoffset == 1 and holetype == 'L':
                    mTmpExp['$SL'] = str(p.gl)
                    mTmpExp['$SD'] = str(p.gp)
                    mTmpExp['$SH'] = str(p.gh)
                    mTmpExp['$DL'] = str(p2.gl)
                    mTmpExp['$DD'] = str(p2.gp)
                    mTmpExp['$DH'] = str(p2.gh)
                    mTmpExp['$X'] = str(x)
                    mTmpExp['$Y'] = str(y)
                    x = int(exp(mTmpExp, c.b_xo))
                    y = int(exp(mTmpExp, c.b_yo))
                hpinfo.x = x
                hpinfo.y = y
                hpinfo.xx = 0
                hpinfo.yy = 0
                hpinfo.hd = hd
                hpinfo.r = '0'
                hpinfo.sri = sri
                hpinfo.htype = holetype
                if holetype=='L' :
                    hpinfo.sr = c.mx_name
                    hpinfo.sri = c.mx_name
                else:
                    hpinfo.r = c.mx_name
                    hpinfo.sri = c.mx_name
                hpinfo.holeid = holeid
                hpinfo.row = mHoleRow
                hpinfo.offset = offset
                hpinfo.face = face
                hpinfo.smallcap = smallcap
                hpinfo.holecap = holecap
                hpinfo.c = c
                hpinfo.isii = 0
                hpinfo.b_bh = Delphi_Round(p2.bh)
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug('AddLHole_A2=' + 'x=' + str(pnumber(hpinfo.x)) + ',y=' + str(pnumber(hpinfo.y)) + ',xx=' + str(hpinfo.xx)
                            + ',yy=' + str(hpinfo.yy) + ',hd=' + str(hpinfo.hd) + ',hpinfo.r=' + str(
                        hpinfo.r) + ',sri=' + str(hpinfo.sri)
                            + ',htype=' + hpinfo.htype + ',holeid=' + str(hpinfo.holeid) + ',row=' + str(hpinfo.row)
                            + ',offset=' + str(hpinfo.offset) + ',face=' + str(hpinfo.face) + ',sr=' + str(
                        sr) + ',smallcap=' + str(smallcap)
                            + ',holecap=' + str(hpinfo.holecap) + ',isii=' + str(hpinfo.isii) +
                            '\n')
                break
    # if holeid==264438 and x==29:
    #     # '77777'
    #     # sys.exit(1)
def AddLHole_B(c, p, p2, x, y, hd, holeid, offset, smallcap, holecap,
        face, holetype, hole, sr, sri, mx_flag=-1, mx_x=0, mx_y=0):
    global mHPInfoList
    def ResetValue():
        x = t_x
        y = t_y
        face = t_face
        holetype = t_holetype
    t_x = x
    t_y = y
    t_face = face
    t_holetype = holetype
    for i in range(0,101):
        if p.bhole_index[i] == -1:
            ResetValue()
            p.bhole_index[i] = len(mHPInfoList)
            hpinfo = THolePointInfo()
            mHPInfoList.append(hpinfo)
            #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
            log.debug('AddLHole_B1=' + str(len(mHPInfoList))+'\n')
            # 'AddLHole_B1:', len(mHPInfoList)
            if (c!=None) and c.b_isoffset ==1 and holetype=='L':
                mTmpExp['$SL'] =  str(p.gl)
                mTmpExp['$SD'] =  str(p.gp)
                mTmpExp['$SH'] = str(p.gh)
                mTmpExp['$DL'] = str(p2.gl)
                mTmpExp['$DD'] = str(p2.gp)
                mTmpExp['$DH'] = str(p2.gh)
                mTmpExp['$X'] = str(x)
                mTmpExp['$Y'] = str(y)
                x = int(exp(mTmpExp,c.b_xo))
                y = int(exp(mTmpExp,c.b_yo))
            hpinfo.x = x
            hpinfo.y = y
            hpinfo.xx = 0
            hpinfo.yy = 0
            hpinfo.hd = hd
            hpinfo.r = hole
            hpinfo.sri = sri
            hpinfo.htype = holetype
            hpinfo.holeid = holeid
            hpinfo.row = mHoleRow
            hpinfo.offset = offset
            hpinfo.face = face
            hpinfo.sr = sr
            hpinfo.smallcap = smallcap
            hpinfo.holecap = holecap
            hpinfo.c = c
            hpinfo.isii = 0
            hpinfo.b_bh = Delphi_Round(p2.bh)
            #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
            log.debug('AddLHole_B1=' + 'x=' + str(pnumber(hpinfo.x)) + ',y=' + str(pnumber(hpinfo.y)) + ',xx=' + str(hpinfo.xx)
                        + ',yy=' + str(hpinfo.yy) + ',hd=' + str(hpinfo.hd) + ',hpinfo.r=' + str(
                    hpinfo.r) + ',sri=' + str(hpinfo.sri)
                        + ',htype=' + hpinfo.htype + ',holeid=' + str(hpinfo.holeid) + ',row=' + str(hpinfo.row)
                        + ',offset=' + str(hpinfo.offset) + ',face=' + str(hpinfo.face) + ',sr=' + str(
                    sr) + ',smallcap=' + str(smallcap)
                        + ',holecap=' + str(hpinfo.holecap) + ',isii=' + str(hpinfo.isii) +
                        '\n')
            break
    if (c != None) and (mx_flag>=0) and c.mx_isoutput ==1:
        ResetValue()
        if mx_flag == 0:
            x = x + mx_x
            y = y + mx_y
        else:
            x = x - mx_x
            y = y - mx_y
        for i in range(0,101):
            if p.bhole_index[i] == -1:
                p.bhole_index[i] = len(mHPInfoList)
                hpinfo = THolePointInfo()
                mHPInfoList.append(hpinfo)
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug('AddLHole_B2=' + str(len(mHPInfoList))+'\n')
                # 'mHPInfoListAddLHole_B2:',len(mHPInfoList)
                if c!= None and c.b_isoffset == 1 and holetype == 'L':
                    mTmpExp['$SL'] = str(p.gl)
                    mTmpExp['$SD'] = str(p.gp)
                    mTmpExp['$SH'] = str(p.gh)
                    mTmpExp['$DL'] = str(p2.gl)
                    mTmpExp['$DD'] = str(p2.gp)
                    mTmpExp['$DH'] = str(p2.gh)
                    mTmpExp['$X'] = str(x)
                    mTmpExp['$Y'] = str(y)
                    x = int(exp(mTmpExp, c.b_xo))
                    y = int(exp(mTmpExp, c.b_yo))
                hpinfo.x = x
                hpinfo.y = y
                hpinfo.xx = 0
                hpinfo.yy = 0
                hpinfo.hd = hd
                hpinfo.r = '0'
                hpinfo.sri = sri
                hpinfo.htype = holetype
                if holetype=='L' :
                    hpinfo.sr = c.mx_name
                    hpinfo.sri = c.mx_name
                else:
                    hpinfo.r = c.mx_name
                    hpinfo.sri = c.mx_name
                hpinfo.holeid = holeid
                hpinfo.row = mHoleRow
                hpinfo.offset = offset
                hpinfo.face = face
                hpinfo.smallcap = smallcap
                hpinfo.holecap = holecap
                hpinfo.c = c
                hpinfo.isii = 0
                hpinfo.b_bh = Delphi_Round(p2.bh)
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug('AddLHole_B2=' + 'x=' + str(pnumber(hpinfo.x)) + ',y=' + str(pnumber(hpinfo.y)) + ',xx=' + str(hpinfo.xx)
                            + ',yy=' + str(hpinfo.yy) + ',hd=' + str(hpinfo.hd) + ',hpinfo.r=' + str(
                        hpinfo.r) + ',sri=' + str(hpinfo.sri)
                            + ',htype=' + hpinfo.htype + ',holeid=' + str(hpinfo.holeid) + ',row=' + str(hpinfo.row)
                            + ',offset=' + str(hpinfo.offset) + ',face=' + str(hpinfo.face) + ',sr=' + str(
                        sr) + ',smallcap=' + str(smallcap)
                            + ',holecap=' + str(hpinfo.holecap) + ',isii=' + str(hpinfo.isii) +
                            '\n')
                break
def AddHole_A(c,p, p2, ho, tm, x, y, hd, holeid, offset, smallcap, holecap,
              face, holetype, hole, sr, sri, mx_flag=-1, mx_x=0, mx_y=0, ischangeface=1):
    if (c!=None) and c.isoffset == 1 and (holetype == 'I'):
        return
    if (holetype == 'I'):
        ## 'AddHole_A'
        AddIHole2_A(c, p, p2, ho, tm, x, y, hd, holeid, offset, smallcap, holecap, face, holetype, hole, sr, sri,
                    mx_flag, mx_x, mx_y)
        return
    ## '9999999999999999999999'
    AddLHole_A(c, p, p2, x, y, hd, holeid, offset, smallcap, holecap, face, holetype, hole, sr, sri, mx_flag, mx_x,
               mx_y)
    if c == None or c.isoffset != 1:
        return
    if face == 'Down' or face =='Back' or face == 'Left':
        AddOffsetIHole_B(c, p, p2, ho, x, y, hd, holeid, offset, smallcap, holecap, face, holetype, hole, sr, sri, \
                         mx_flag, mx_x, mx_y)
    if face == 'Up' or face == 'Front' or face == 'Right':
        AddOffsetIHole_A(c, p, p2, ho, x, y, hd, holeid, offset, smallcap, holecap, face, holetype, hole, sr, sri,
                         mx_flag, mx_x, mx_y)
def AddHole_B(c, p, p2, ho, tm, x, y, hd, holeid, offset, smallcap, holecap,
              face, holetype, hole, sr, sri, mx_flag=-1, mx_x=0, mx_y=0, ischangeface=1):
    if (c!=None) and c.isoffset == 1 and (holetype == 'I'):
        return
    if (holetype == 'I'):
        AddIHole2_B(c, p, p2, ho, tm, x, y, hd, holeid, offset, smallcap, holecap, face, holetype, hole, sr, sri,
                    mx_flag, mx_x, mx_y)
        return
    ## 'AddHole_B'
    AddLHole_B(c, p, p2, x, y, hd, holeid, offset, smallcap, holecap, face, holetype, hole, sr, sri, mx_flag, mx_x,
               mx_y)
    if c == None or c.isoffset != 1:
        return
    if face == 'Down' or face =='Back' or face == 'Left':
        AddOffsetIHole_B(c, p, p2, ho, x, y, hd, holeid, offset, smallcap, holecap, face, holetype, hole, sr, sri, \
                         mx_flag, mx_x, mx_y)
    if face == 'Up' or face == 'Front' or face == 'Right':
        AddOffsetIHole_A(c, p, p2, ho, x, y, hd, holeid, offset, smallcap, holecap, face, holetype, hole, sr, sri,
                         mx_flag, mx_x, mx_y)
def Length_HoleFace(p1, p2, c, face, xy):
    def CalcMinL(a1, b1, a2, b2):# // a, b两直线的最小接触面
        if a1 > a2 : a1, a2 = Swap(a1, a2)
        if b1 > b2 : b1, b2 = Swap(b1, b2)
        t = -1
        if (a1 <= b1) and (a1 < b2) : t = min(a2, b2) - b1
        elif (a1 > b1) and (a1 < b2) : t = min(a2, b2) - a1
        Result = round(t)
        return Result
    l = 0
    if c.algorithm==1 : # // 按接触面计算
        if xy==0 :
            if face==1 : l = CalcMinL(p1.bg_l_minx + p1.y, p2.bg_r_minx + p2.y, p1.bg_l_maxx + p1.y, p2.bg_r_maxx + p2.y)
            if face==2 : l = CalcMinL(p1.bg_r_minx + p1.y, p2.bg_l_minx + p2.y, p1.bg_r_maxx + p1.y, p2.bg_l_maxx + p2.y)
            if face==3 : l= CalcMinL(p1.bg_d_minx + p1.x, p2.bg_u_minx + p2.x, p1.bg_d_maxx + p1.x, p2.bg_u_maxx + p2.x)
            if face==4 : l = CalcMinL(p1.bg_u_minx + p1.x, p2.bg_d_minx + p2.x, p1.bg_u_maxx + p1.x, p2.bg_d_maxx + p2.x)
            if face==5 : l = CalcMinL(p1.bg_b_minx + p1.x, p2.bg_f_minx + p2.x, p1.bg_b_maxx + p1.x, p2.bg_f_maxx + p2.x)
            if face==6 : l = CalcMinL(p1.bg_f_minx + p1.x, p2.bg_b_minx + p2.x, p1.bg_f_maxx + p1.x, p2.bg_b_maxx + p2.x)
        if xy==1 :
            if face==1 : l=CalcMinL(p1.bg_l_miny + p1.z, p2.bg_r_miny + p2.z, p1.bg_l_maxy + p1.z, p2.bg_r_maxy + p2.z)
            if face==2 : l=CalcMinL(p1.bg_r_miny + p1.z, p2.bg_l_miny + p2.z, p1.bg_r_maxy + p1.z, p2.bg_l_maxy + p2.z)
            if face==3 : l=CalcMinL(p1.bg_d_miny + p1.y, p2.bg_u_miny + p2.y, p1.bg_d_maxy + p1.y, p2.bg_u_maxy + p2.y)
            if face==4 : l=CalcMinL(p1.bg_u_miny + p1.y, p2.bg_d_miny + p2.y, p1.bg_u_maxy + p1.y, p2.bg_d_maxy + p2.y)
            if face==5 : l=CalcMinL(p1.bg_b_miny + p1.z, p2.bg_f_miny + p2.z, p1.bg_b_maxy + p1.z, p2.bg_f_maxy + p2.z)
            if face==6 : l=CalcMinL(p1.bg_f_miny + p1.z, p2.bg_b_miny + p2.z, p1.bg_f_maxy + p1.z, p2.bg_b_maxy + p2.z)
        Result = l
        return Result
    #// 左面1, // 右面2, // 下面3, // 上面4, // 后面5, // 前面6 // X0, Y1
    if xy==0 :
        if face==1 : l = p1.bg_l_maxx - p1.bg_l_minx
        if face==2 : l = p1.bg_r_maxx - p1.bg_r_minx
        if face==3 : l = p1.bg_d_maxx - p1.bg_d_minx
        if face==4 : l = p1.bg_u_maxx - p1.bg_u_minx
        if face==5 : l = p1.bg_b_maxx - p1.bg_b_minx
        if face==6 : l = p1.bg_f_maxx - p1.bg_f_minx
    if xy==1 :
        if face==1 : l = p1.bg_l_maxy - p1.bg_l_miny;
        if face==2 : l = p1.bg_r_maxy - p1.bg_r_miny;
        if face==3 : l = p1.bg_d_maxy - p1.bg_d_miny;
        if face==4 : l = p1.bg_u_maxy - p1.bg_u_miny;
        if face==5 : l = p1.bg_b_maxy - p1.bg_b_miny;
        if face==6 : l = p1.bg_f_maxy - p1.bg_f_miny;
        Result = l
        return Result
    return l
def CalcHoleUnit_CalcHoleList(listEx, mIIHoleCalcRule):
    global mHoleFaceTwice
    def SetHoleFaceItem(p1,p2):
        p1.holeface = p2.holeface
        p1.l_item0 = p2.l_item0
        p1.r_item0 = p2.r_item0
        p1.u_item0 = p2.u_item0
        p1.d_item0 = p2.d_item0
        p1.l_item = p2.l_item
        p1.r_item = p2.r_item
        p1.u_item = p2.u_item
        p1.d_item = p2.d_item
    def PCI_GL(p):
        Result = p.gl
        ## 'Result=',Result
        if p.isxx ==1 :
            Result = Delphi_Round(p.gl * math.cos(p.var_args[0] * math.pi / 180)) #// 左右斜
        return Result
    def IsNoCalc(p):
        Result = 0
        if p.bdxmlid != '':
            Result = 1
        if p.holeinfo_flag == 0:
            Result = 2
        return Result
    def IsLSIntersection(a1, b1, a2, b2):
        const.min = 50
        Result = 1
        if b1 < a1 :
            a1,b1 = b1,a1
        if b2 < a2:
            a2, b2 =b2, a2
        if (a2 <= a1) and (b2 >= b1):
            return
        if ((a2 + min) >= a1) and ((a2 + min) >= b1) :
            if (b2 > a1) and (b2 > b1):
                Result=0
        if ((b2 - min) <= a1) and ((b2 - min) <= b1) :
            if (a2 < a1) and (b2 < b1) :
                Result = 0
        return Result
    # 靠背对齐
    # 靠背对齐 - 三排孔
    # 前后端等距
    # 动态计算孔位接触面
    # 'listEx:',len(listEx)
    for i in range(0,len(listEx)):
        p1= listEx[i]
        p1.holefac = 0
        p1.l_item = None
        p1.r_item = None
        p1.u_item = None
        p1.d_item = None
        p1.l_item0 = None
        p1.r_item0 = None
        p1.u_item0 = None
        p1.d_item0 = None
        p1.holeinfo_flag= -1
        if p1.holeinfo=='' : continue
        j = p1.holeinfo.find('M="')
        if j > 0:
            p1.holeinfo_flag = int(p1.holeinfo[j + 3]) - 48
    #// 动态计算有孔的面
    mHoleFaceTwice = 0
    # u'动态计算有孔的面'
    for i in range(0, len(listEx)):
        p1 = listEx[i]
        # p1.m
        #sys.exit(1)
        if IsNoCalc(p1) > 0 : continue
        for j in range(0, len(listEx)):
            if i == j : continue
            p1 = listEx[i]
            p2 = listEx[j]
            if (IsNoCalc(p2) > 1) or (p1.space_id != p2.space_id) or (p1.sozflag != p2.sozflag) : continue
            # mCItem1 = TMyCalcItem()
            # mCItem2 = TMyCalcItem()
            p1, p2 =SubSpaceAItem(p1, p2, mCItem1, mCItem2)
            ## 'self_p=',mCItem1.self_p
            # di值0和1可以认为等价，为避免xml模块忘记写纹路
            di1 = p1.direct
            di2 = p2.direct
            if (p1.holeid >= 0) and (di1==0) : di1 = 1
            if (p2.holeid >= 0) and (di2==0) : di2 = 1
            ## 'p1.holeid:', p1.holeid, 'p2.holeid:', p2.holeid, 'di1=', di1, 'di2=', di2,'PCI_GL(p2):',p1.x,p2.x,PCI_GL(p2)
            if (abs(p1.x - p2.x - PCI_GL(p2)) < 2) and (p1.holeid >= 0) and (p2.holeid >= 0) : #// 左面
                #c = GetHoleConfig(p1.holeid, 0, p1, p2)
                CalcHoleFace_LeftFace(p1, p2, GetHoleConfig(p1.holeid, 0, p1, p2))
                ## '1111111'
            if (abs(p1.x + PCI_GL(p1) - p2.x) < 2) and (p1.holeid >= 0) and (p2.holeid >= 0) : # // 右面
                CalcHoleFace_RightFace(p1, p2, GetHoleConfig(p1.holeid, 1, p1, p2))
                ## '2222222'
            if (abs(p1.z - p2.z - p2.gh) < 2) and (p1.holeid >= 0) and (p2.holeid >= 0) : #// 下面
                CalcHoleFace_DownFace(p1, p2, GetHoleConfig(p1.holeid, 2, p1, p2))
                ## '3333333'
            if (abs(p1.z + p1.gh - p2.z) < 2) and (p1.holeid >= 0) and (p2.holeid >= 0) : #// 上面
                CalcHoleFace_UpFace(p1, p2, GetHoleConfig(p1.holeid, 3, p1, p2))
                ## '4444444'
            if (abs(p1.y - p2.gp - p2.y) < 2) and (p1.holeid >= 0) and (p2.holeid >= 0) : #// 后面
                CalcHoleFace_BackFace(p1, p2, GetHoleConfig(p1.holeid, 4, p1, p2))
                ## '5555555'
            if (abs(p1.y + p1.gp - p2.y) < 2) and (p1.holeid >= 0) and (p2.holeid >= 0) : #// 前面
                CalcHoleFace_FrontFace(p1, p2, GetHoleConfig(p1.holeid, 5, p1, p2))
                ## '6666666'
            SetHoleFaceItem(listEx[i], mCItem1)
            SetHoleFaceItem(listEx[j], mCItem2)
    #// 第二次计算
    mHoleFaceTwice = 1
    for i in range(0, len(listEx)):
        p1 = listEx[i]
        if IsNoCalc(p1) > 1 : continue
        for j in range(0, len(listEx)):
            if i == j : continue
            p1 = listEx[i]
            p2 = listEx[j]
            if (IsNoCalc(p2) > 1) or (p1.space_id != p2.space_id) or (p1.sozflag != p2.sozflag) : continue
            p1, p2 =SubSpaceAItem(p1, p2, mCItem1, mCItem2)
            #// di值0和1可以认为等价，为避免xml模块忘记写纹路
            di1 = p1.direct
            di2 = p2.direct
            if (p1.holeid >= 0) and (di1==0) : di1 = 1
            if (p2.holeid >= 0) and (di2==0) : di2 = 1
            if (abs(p1.x - p2.x - PCI_GL(p2)) < 2) and (p1.holeid >= 0) and (p2.holeid >= 0) : #// 左面
                CalcHoleFace_LeftFace(p1, p2, GetHoleConfig(p1.holeid, 0, p1, p2))
            if (abs(p1.x + PCI_GL(p1) - p2.x) < 2) and (p1.holeid >= 0) and (p2.holeid >= 0) : #// 右面
                CalcHoleFace_RightFace(p1, p2, GetHoleConfig(p1.holeid, 1, p1, p2))
            if (abs(p1.z - p2.z - p2.gh) < 2) and (p1.holeid >= 0) and (p2.holeid >= 0) : #// 下面
                CalcHoleFace_DownFace(p1, p2, GetHoleConfig(p1.holeid, 2, p1, p2))
            if (abs(p1.z + p1.gh - p2.z) < 2) and (p1.holeid >= 0) and (p2.holeid >= 0) : #// 上面
                CalcHoleFace_UpFace(p1, p2, GetHoleConfig(p1.holeid, 3, p1, p2))
            if (abs(p1.y - p2.gp - p2.y) < 2) and (p1.holeid >= 0) and (p2.holeid >= 0) : #// 后面
                CalcHoleFace_BackFace(p1, p2, GetHoleConfig(p1.holeid, 4, p1, p2))
            if (abs(p1.y + p1.gp - p2.y) < 2) and (p1.holeid >= 0) and (p2.holeid >= 0) : #// 前面
                CalcHoleFace_FrontFace(p1, p2, GetHoleConfig(p1.holeid, 5, p1, p2))
            SetHoleFaceItem(listEx[i], mCItem1)
            SetHoleFaceItem(listEx[j], mCItem2)
    # //动态计算孔位
    for i in range(0, len(listEx)):
        p1 = listEx[i]
        if IsNoCalc(p1) in [1,2]: continue
        # u'动态计算孔位'
        for j in range(0, len(listEx)):
            if i == j: continue
            p1 = listEx[i]
            p2 = listEx[j]
            # if len(mHPInfoList) == 1188 and j==106 and i==52:
            ## p1.guid
            ## 'p1.holeid:', p1.holeid, 'p2.holeid:', p2.holeid, 'name=', p1.name,p1.bl, p1.bp, p1.bh,'p1.x=',p1.x,'p1.y=',p1.y,'p1.z=',p1.z,'p1.m=', p1.m, p1.v,'p1.space_id=',p1.space_id
            ##  'p2=', p2.name,'p2.x=',p2.x,'p2.y=',p2.y,'p2.z=',p2.z,  p2.bl, p2.bp, p2.bh,'p2.m=', p2.m, p2.v,'p2.space_id=',p2.space_id
            if (IsNoCalc(p2) > 1) or (p1.space_id != p2.space_id) or (p1.sozflag != p2.sozflag): continue
            p1, p2 = SubSpaceAItem(p1, p2, mCItem1, mCItem2)
            # // di值0和1可以认为等价，为避免xml模块忘记写纹路
            ## 'self_p=', p1.self_p
            di1 = p1.direct
            di2 = p2.direct
            if (p1.holeid >= 0) and (di1 == 0): di1 = 1
            if (p2.holeid >= 0) and (di2 == 0): di2 = 1
            # if ((len(mHPInfoList) ==1546) and (j==6) and i==0):
            #     # 'p1.holeid:', p1.holeid, 'p2.holeid:', p2.holeid, 'name=', p1.name,p1.bl, p1.bp, p1.bh,'p1.x=',p1.x,'p1.y=',p1.y,'p1.z=',p1.z,'p1.m=', p1.m, p1.v,
            #     print  'p2=', p2.name,'p2.x=',p2.x,'p2.y=',p2.y,'p2.z=',p2.z,  p2.bl, p2.bp, p2.bh,'p2.m=', p2.m, p2.v
            #     if p1.holeid >= 0:
            #         print 'p1p1p11p'
            #     if p2.holeid >= 0:
            #         print 'p2p2p22p'
            #     if (abs(p1.x + PCI_GL(p1) - p2.x) < 2) :
            #         print 'abs'
            #     exit(1)
            # 'di1=',p1.direct,'di2=',p2.direct
            if (abs(p1.x - p2.x - PCI_GL(p2)) < 2) and (p1.holeid >= 0) and (p2.holeid >= 0):  # // 左面
                CalcHole_LeftFace(p1, p2, GetHoleConfig(p1.holeid, 0, p1, p2))
                # print base_dir + '\\testdata\\' + 'mHPInfoList'
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug(('左面mHPInfoList='+str(len(mHPInfoList))+'i='+str(i)+'j='+str(j)+'\n').encode('gbk'))
                #print 'j='+str(j)+u'左面', len(mHPInfoList)
            if (abs(p1.x + PCI_GL(p1) - p2.x) < 2) and (p1.holeid >= 0) and (p2.holeid >= 0):  # // 右面
                CalcHole_RightFace(p1, p2, GetHoleConfig(p1.holeid, 1, p1, p2))
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug(('右面mHPInfoList='+str(len(mHPInfoList))+'i='+str(i)+'j='+str(j)+'\n').encode('gbk'))
                #print 'j='+str(j)+u'右面', len(mHPInfoList)
            if (abs(p1.z - p2.z - p2.gh) < 2) and (p1.holeid >= 0) and (p2.holeid >= 0):  # // 下面
                CalcHole_DownFace(p1, p2, GetHoleConfig(p1.holeid, 2, p1, p2))
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug(('下面mHPInfoList='+str(len(mHPInfoList))+'i='+str(i)+'j='+str(j)+'\n').encode('gbk'))
                #print 'j='+str(j)+u'下面', len(mHPInfoList)
            if (abs(p1.z + p1.gh - p2.z) < 2) and (p1.holeid >= 0) and (p2.holeid >= 0):  # // 上面
                CalcHole_UpFace(p1, p2, GetHoleConfig(p1.holeid, 3, p1, p2))
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug(('上面mHPInfoList='+str(len(mHPInfoList))+'i='+str(i)+'j='+str(j)+'\n').encode('gbk'))
                #print 'j='+str(j)+u'上面', len(mHPInfoList)
            if (abs(p1.y - p2.gp - p2.y) < 2) and (p1.holeid >= 0) and (p2.holeid >= 0):  # // 后面
                CalcHole_BackFace(p1, p2, GetHoleConfig(p1.holeid, 4, p1, p2))
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug(('后面mHPInfoList='+str(len(mHPInfoList))+'i='+str(i)+'j='+str(j)+'\n').encode('gbk'))
                #print 'j='+str(j)+u'后面', len(mHPInfoList)
            if (abs(p1.y + p1.gp - p2.y) < 2) and (p1.holeid >= 0) and (p2.holeid >= 0):  # // 前面
                CalcHole_FrontFace(p1, p2, GetHoleConfig(p1.holeid, 5, p1, p2))
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug(('前面mHPInfoList='+str(len(mHPInfoList))+'i='+str(i)+'j='+str(j)+'\n').encode('gbk'))
                #print 'j='+str(j)+u'前面', len(mHPInfoList)
            UpdateCalcItemResult(listEx[i], mCItem1)
            UpdateCalcItemResult(listEx[j], mCItem2)
            # 'mHPInfoListn=',len(mHPInfoList)
    #print '1', len(mHPInfoList)
    n = len(mHPInfoList)
    # 'n=', n
    #exit(1)
    #// 根据holeinfo配置信息生成孔位
    for i in range(0,len(listEx)):
        p1 = listEx[i]
        if (p1.holeinfo=='') : continue
        UpdateTempExpVariable(p1)
        #print p1.holeinfo
        xdoc ='<?xml version="1.0" encoding="utf-8"?>' + p1.holeinfo
        root = ET.fromstring(xdoc)
        for j in range(0,len(root)):
            n = root[j].get('F',-1)
            #print 'n=',n
            if n=='0' :
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug(('AddHoleSelf_A='+str(len(mHPInfoList))+'i='+str(i)+'j='+str(j)).decode('utf8').encode('gbk')+
                            'gl='+str(p1.gl)+'gp='+str(p1.gp)+'gh='+str(p1.gh)+'\n')
                #print 'j='+str(j)+u'前面', len(mHPInfoList)
                AddHoleSelf_A(p1, root[j])
            if n=='1' :
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug(('AddHoleSelf_B=' + str(len(mHPInfoList)) + 'i=' + str(i) + 'j=' + str(j)).decode(
                    'utf8').encode('gbk')+
                            'gl='+str(p1.gl)+'gp='+str(p1.gp)+'gh='+str(p1.gh)+'\n')
                AddHoleSelf_B(p1, root[j])
        xdoc = ''
    #print '2',len(mHPInfoList)
    # // 根据bdxml 计算孔位
    for i in range(0,len(listEx)):
        p1 = listEx[i]
        if p1.bdxmlid == '': continue
        for j in range(0,len(listEx)):
            if i == j: continue
            p1 = listEx[i]
            p2 = listEx[j]
            if (p1.space_id!=p2.space_id) or (p1.sozflag!=p2.sozflag) : continue
            p1, p2 = SubSpaceAItem(p1, p2, mCItem1, mCItem2)
            di1 = p1.direct
            di2 = p2.direct
            if (p1.holeid >= 0) and (di1==0) : di1=1
            if (p2.holeid >= 0) and (di2==0) : di2=1
            if (abs(p1.x - p2.x - PCI_GL(p2)) < 2) : #// 左面
                CalcBdxmlHole_LeftFace(p1, p2)
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug(('C左面mHPInfoList='+str(len(mHPInfoList))+'i='+str(i)+'j='+str(j)+'\n').encode('gbk'))
            if (abs(p1.x + PCI_GL(p1) - p2.x) < 2) : #// 右面
                CalcBdxmlHole_RightFace(p1, p2)
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug(('C右面mHPInfoList='+str(len(mHPInfoList))+'i='+str(i)+'j='+str(j)+'\n').encode('gbk'))
            if (abs(p1.z - p2.z - p2.gh) < 2) : #// 下面
                CalcBdxmlHole_DownFace(p1, p2)
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug(('C下面mHPInfoList='+str(len(mHPInfoList))+'i='+str(i)+'j='+str(j)+'\n').encode('gbk'))
            if (abs(p1.z + p1.gh - p2.z) < 2) : #// 上面
                CalcBdxmlHole_UpFace(p1, p2)
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug(('C上面mHPInfoList='+str(len(mHPInfoList))+'i='+str(i)+'j='+str(j)+'\n').encode('gbk'))
            if (abs(p1.y - p2.gp - p2.y) < 2) : #// 后面
                CalcBdxmlHole_BackFace(p1, p2)
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug(('C后面mHPInfoList='+str(len(mHPInfoList))+'i='+str(i)+'j='+str(j)+'\n').encode('gbk'))
            if (abs(p1.y + p1.gp - p2.y) < 2) : #// 前面
                CalcBdxmlHole_FrontFace(p1, p2)
                #with open(base_dir + '\\testdata\\' + 'mHPInfoList' + '.txt', 'a+') as f:
                log.debug(('C前面mHPInfoList='+str(len(mHPInfoList))+'i='+str(i)+'j='+str(j)+'\n').encode('gbk'))
            UpdateCalcItemResult(listEx[i], mCItem1)
            UpdateCalcItemResult(listEx[j], mCItem2)
    #print '3', len(mHPInfoList)
    #计算通孔
    # u'计算通孔'
    n = len(mHPInfoList)
    # # 'n=',n
    # i = 0
    # for phinfotest in mHPInfoList:
    #     i=i+1
    #     # i,'mHPInfoList='+str(len(mHPInfoList))\
    #           +',x='+str(phinfotest.x)+',y='+str(phinfotest.y) \
    # +',hd='+str(phinfotest.hd)+',holeid='+str(phinfotest.holeid)+',row='+str(phinfotest.row)\
    # +',offset='+str(phinfotest.offset)+',smallcap='+str(phinfotest.smallcap)\
    # +',holecap='+str(phinfotest.holecap)+',isii='+str(phinfotest.isii)+',b_bh='+str(phinfotest.b_bh)   \
    # +',xx='+str(phinfotest.xx)+',yy='+str(phinfotest.yy)\
    # +',face='+phinfotest.face+',r='+phinfotest.r+',sr='+phinfotest.sr+',sri='+phinfotest.sri+',htype='+phinfotest.htype+'\n'
    # i = 0
    for i in range(0,len(listEx)):
        p1 = listEx[i]
        #print mIIHoleCalcRule
        if str(int(Delphi_Round(p1.bh))) not in mIIHoleCalcRule:
             pass
        elif (mIIHoleCalcRule !=None) and (mIIHoleCalcRule[str(int(Delphi_Round(p1.bh)))]==2) :
            continue
        # if p1.bhole_index == [426,427,428,429,474,475,476,477,484,485,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]:
        #     print u'存在'
        for j in range(0,101):
            if (p1.ahole_index[j] >= 0) and (p1.ahole_index[j] < n):
                phinfo1 = mHPInfoList[p1.ahole_index[j]]
                if (phinfo1.isii != 0) or (phinfo1.htype != 'I') : continue
                for k in range(0,101):
                    if (p1.bhole_index[k] >= 0) and (p1.bhole_index[k] < n):
                        phinfo2 = mHPInfoList[p1.bhole_index[k]]
                        if (phinfo2.isii != 0) or (phinfo2.htype != 'I') : continue
                        if (phinfo1.x==phinfo2.x) and (phinfo1.y==phinfo2.y) and (phinfo1.r==phinfo2.r):
                            phinfo1.isii = 1
                            phinfo2.isii = 1
                            # if p1.bhole_index == [426, 427, 428, 429, 474, 475, 476, 477, 484, 485, -1, -1, -1, -1, -1,
                            #                       -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                            #                       -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                            #                       -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                            #                       -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                            #                       -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                            #                       -1]:
                                #print u'存在'
                                #print p1.bhole_index, 'k=', k, 'isii=', phinfo1.isii, 'phinfo2.htype=', phinfo2.htype, 'p1.bhole_index[k]=', \
                                #p1.bhole_index[k], 'bh=', p1.bh, mIIHoleCalcRule
                                #print 'j=', j, 'x1=', phinfo1.x, 'y1=', phinfo1.y, 'r1=', phinfo1.r, 'p1.ahole_index[j]=', \
                                #p1.ahole_index[j], p1.ahole_index
                                #print 'x2=', phinfo2.x, 'y2=', phinfo2.y, 'r2=', phinfo2.r
                            # if p1.bhole_index == [1196, 1197, 1198, 1199, 1216, 1217, 1218, 1219, 1230, 1231, 1238, 1239, 1250, 1251, 1262, 1263, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]:
                            # #if i==6 and len(mHPInfoList) > 1251:
                            #     print p1.bhole_index,'k=',k,'isii=',phinfo1.isii,'phinfo2.htype=',phinfo2.htype,'p1.bhole_index[k]=',p1.bhole_index[k],'bh=',p1.bh,mIIHoleCalcRule
                            #     print 'j=',j,'x1=',phinfo1.x,'y1=',phinfo1.y,'r1=',phinfo1.r,'p1.ahole_index[j]=',p1.ahole_index[j],p1.ahole_index
                            #     print 'x2=',phinfo2.x,'y2=',phinfo2.y,'r2=',phinfo2.r
                            #     exit(1)
                                # if k==0:
                                #     print 'isii=',phinfo2.isii,'htype=',phinfo2.htype
                                # print 'i=', i, 'name=', p1.name, 'p2.name=', p2.name
                            break
                        #print 'k=',k,'p1.bhole_index[k]=',p1.bhole_index[k],'isii=',phinfo2.isii
        # if p1.bhole_index == [426,427,428,429,474,475,476,477,484,485,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]:
        #     print u'存在结束'
            #exit(1)
def  AddKC_A(c, p1, p2, v0, v1, x0, y0, x1, y1, l, face, kcconfig_flag, bh):
    # if p2.name == u'右侧板' and p2.color == u'314#B蜡木':
    #     print u'右侧板2：', 'v0=', v0, 'v1=', v1,p1.name,p1.m,p1.v
    t0 = 0
    t1 = 0
    v0 = VectorTransform(v0, p1.m)
    v0 = VectorTransform(v0, MatrixInvert(p2.m))
    v1 = VectorTransform(v1, p1.m)
    v1 = VectorTransform(v1, MatrixInvert(p2.m))
    op= p2.self_p
    if op.direct in [1, 5] : #// 层板
        x0 = Delphi_Round(v0[0])
        y0 = Delphi_Round(v0[1])
        t0 = Delphi_Round(v0[2])
        x1 = Delphi_Round(v1[0])
        y1 = Delphi_Round(v1[1])
        t1 = Delphi_Round(v1[2])
    if op.direct in [4, 6] : #// 侧板
        x0 = Delphi_Round(v0[2])
        y0 = Delphi_Round(v0[1])
        t0 = Delphi_Round(v0[0])
        x1= Delphi_Round(v1[2])
        y1= Delphi_Round(v1[1])
        t1= Delphi_Round(v1[0])
    if op.direct in [2, 3] : #// 背板
        y0 = Delphi_Round(v0[0])
        x0 = Delphi_Round(v0[2])
        t0 = Delphi_Round(v0[1])
        y1 = Delphi_Round(v1[0])
        x1 = Delphi_Round(v1[2])
        t1 = Delphi_Round(v1[1])
    for i in range(0,101):
        if t1 > t0 :
            index = p2.bkc_index[i]
        else:
            index = p2.akc_index[i]
        if index == -1 :
            # if p2.name==u'右侧板' and p2.color==u'314#B蜡木':
            #     print u'右侧板1：','t1=',t1,'t0=',t0,'v0=',v0,'v1=',v1
            # if len(mKCInfoList) == 16:
            #     print 't1=',t1,'t0=',t0,'i=',i
            if t1 > t0 : p2.bkc_index[i] =len(mKCInfoList)
            else: p2.akc_index[i] = len(mKCInfoList)
            # if len(mKCInfoList) == 16:
            #     print 'bkc_index=',p2.bkc_index
            #     print 'akc_index=', p2.akc_index
            KCInfo = TKCInfo()
            mKCInfoList.append(KCInfo)
            KCInfo.kcid = c.id
            KCInfo.x0 = x0
            KCInfo.y0 = y0
            KCInfo.x1 = x1
            KCInfo.y1 = y1
            KCInfo.l = l
            KCInfo.w = Delphi_Round(bh) + c.w
            KCInfo.face = face
            KCInfo.device = c.device
            KCInfo.flag = kcconfig_flag
            KCInfo.cutter = c.cutter
            p2.kcconig_flag = kcconfig_flag.replace('$X', str(int(x0)))
            p2.kcconig_flag = p2.kcconig_flag.replace('$Y', str(int(y0)))
            p2.kcconig_flag = p2.kcconig_flag.replace('$L', str(int(l)))
            p2.kcconig_flag = p2.kcconig_flag.replace('$BH', str(int(round(bh))))
            KCInfo.flag = p2.kcconig_flag
            break
def  AddKC_B(c, p1, p2, v0, v1, x0, y0, x1, y1, l, face, kcconfig_flag, bh):
    t0 = 0
    t1 = 0
    v0 = VectorTransform(v0, p1.m)
    v0 = VectorTransform(v0, MatrixInvert(p2.m))
    v1 = VectorTransform(v1, p1.m)
    v1 = VectorTransform(v1, MatrixInvert(p2.m))
    op= p2.self_p
    if op.direct in [1, 5] : #// 层板
        x0 = Delphi_Round(v0[0])
        y0 = Delphi_Round(v0[1])
        t0 = Delphi_Round(v0[2])
        x1 = Delphi_Round(v1[0])
        y1 = Delphi_Round(v1[1])
        t1 = Delphi_Round(v1[2])
    if op.direct in [4, 6] : #// 侧板
        x0 = Delphi_Round(v0[2])
        y0 = Delphi_Round(v0[1])
        t0 = Delphi_Round(v0[0])
        x1= Delphi_Round(v1[2])
        y1= Delphi_Round(v1[1])
        t1= Delphi_Round(v1[0])
    if op.direct in [2, 3] : #// 背板
        y0 = Delphi_Round(v0[0])
        x0 = Delphi_Round(v0[2])
        t0 = Delphi_Round(v0[1])
        y1 = Delphi_Round(v1[0])
        x1 = Delphi_Round(v1[2])
        t1 = Delphi_Round(v1[1])
    for i in range(0,101):
        if t1 > t0 : index = p2.bkc_index[i]
        else: index = p2.akc_index[i]
        if index == -1 :
            # if p2.name==u'右侧板' and p2.color==u'314#B蜡木':
            #     print u'右侧板：','t1=',t1,'t0=',t0
            if t1 > t0 : p2.bkc_index[i] =len(mKCInfoList)
            else: p2.akc_index[i] = len(mKCInfoList)
            KCInfo= TKCInfo()
            mKCInfoList.append(KCInfo)
            KCInfo.kcid = c.id
            KCInfo.x0 = x0
            KCInfo.y0 = y0
            KCInfo.x1 = x1
            KCInfo.y1 = y1
            KCInfo.l = l
            KCInfo.w = Delphi_Round(bh) + c.w
            KCInfo.face = face
            KCInfo.device = c.device
            KCInfo.flag = kcconfig_flag
            KCInfo.cutter = c.cutter
            p2.kcconig_flag = kcconfig_flag.replace('$X', str(int(x0)))
            p2.kcconig_flag = p2.kcconig_flag.replace('$Y', str(int(y0)))
            p2.kcconig_flag = p2.kcconig_flag.replace('$L', str(int(l)))
            p2.kcconig_flag = p2.kcconig_flag.replace('$BH', str(int(round(bh))))
            KCInfo.flag = p2.kcconig_flag
            break
def CalcKC_BackFace(p1, p2, c):
    if (c==None): return
    di1 = p1.direct
    di2 = p2.direct
    if Delphi_not(di1) in [1,2,3,4,5,6] : di1 = 1
    if Delphi_not(di2) in [1,2,3,4,5,6] : di2 = 1
    if (di1 in [4, 6]) and (di2 in [2, 3]) and \
        (p1.x >= p2.x) and (p1.x + p1.gl <= p2.x + p2.gl) and \
        (p1.z + p1.gh // 2 >= p2.z) and (p1.z + p1.gh // 2 <= p2.z + p2.gh):
        #// 中立板与顶板接触，中立板是竖纹，底板横纹
        #// 纹理面开槽
        y = p1.x - p2.x
        x = p1.z - p2.z
        cy = c.y
        if p2.zero_y==2 : #// 右
            y = p1.x + p1.gl - p2.x
            cy = -c.y
        bh = Delphi_Round(p2.bh)
        AddKC_B(c, p1, p2, AffineVectorMake( c.y, 0, c.x), AffineVectorMake(c.y, bh, c.x + c.l + p1.gh), x + c.x, y + cy,
                x + c.x + p1.gh + c.l, y+cy,  p1.gh + c.l, 'Back', c.flag, p1.bh)
    if (di1 in [1, 5]) and (di2 in [2, 3]) and    \
        (p1.z >= p2.z) and (p1.z + p1.gh <= p2.z + p2.gh) and    \
        (p1.x + p1.gl // 2 >= p2.x) and (p1.x + p1.gl // 2 <= p2.x + p2.gl):
        #// 背板与侧板接触，背板竖纹，侧板竖纹
        #// 纹理面开槽
        x = p1.x - p2.x
        y = p1.z - p2.z
        cy = c.y
        if p2.zero_y==6 : #// 前
            y = p1.z + p1.gh - p2.z
            cy = -c.y
        bh = Delphi_Round(p2.bh)
        AddKC_B(c, p1, p2, AffineVectorMake(c.x, 0, c.y), AffineVectorMake(c.x + c.l + p1.gl, bh, c.y), y + cy, x + c.x,
                y + cy, x + c.x + p1.gl + c.l,  p1.gl + c.l, 'Back', c.flag, p1.bh)
def CalcKC_DownFace(p1, p2, c):
    if (c==None): return
    di1 = p1.direct
    di2 = p2.direct
    if Delphi_not(di1) in [1,2,3,4,5,6] : di1 = 1
    if Delphi_not(di2) in [1,2,3,4,5,6] : di2 = 1
    if (di1 in [4, 6]) and (di2 in [1, 5]) and \
        (p1.x >= p2.x) and (p1.x + p1.gl <= p2.x + p2.gl) and \
        (p1.y + p1.gp // 2 >= p2.y) and (p1.y + p1.gp // 2 <= p2.y + p2.gp):
        #// 层板与侧板接触，层板是横纹，侧板是竖纹
        #// 纹理面开槽
        y = p1.x - p2.x
        x = p1.y - p2.y
        cy = c.y
        if p2.zero_y==2 : #// 上
            y = p1.x + p1.gl - p2.x
            cy = -c.y
        bh = Delphi_Round(p2.bh)
        AddKC_B(c, p1, p2, AffineVectorMake( c.y, c.x, 0), AffineVectorMake(c.y, c.x + c.l + p1.gp, bh), y + cy, x + c.x, y + cy,
                x + c.x + p1.gp + c.l, p1.gp + c.l, 'Down', c.flag, p1.bh)
    if (di1 in [2, 3]) and (di2 in [1, 5]) and    \
        (p1.y >= p2.y) and (p1.y + p1.gp <= p2.y + p2.gp) and    \
        (p1.x + p1.gl // 2 >= p2.x) and (p1.x + p1.gl // 2 <= p2.x + p2.gl):
        #// 背板与侧板接触，背板竖纹，侧板竖纹
        #// 纹理面开槽
        x = p1.x - p2.x
        y = p1.y - p2.y
        cy = c.y
        if p2.zero_y==4 : #// 前
            y = p1.y + p1.gp - p2.y
            cy = -c.y
        bh = Delphi_Round(p2.bh)
        AddKC_B(c, p1, p2, AffineVectorMake(c.x, c.y, 0), AffineVectorMake(c.x + c.l + p1.gl, c.y, bh), x + c.x, y + cy,
                x + c.x + p1.gl + c.l, y + cy, p1.gl + c.l, 'Down', c.flag, p1.bh)
def CalcKC_FrontFace(p1, p2, c):
    if (c==None): return
    di1 = p1.direct
    di2 = p2.direct
    if Delphi_not(di1) in [1,2,3,4,5,6] : di1= 1
    if Delphi_not(di2) in [1,2,3,4,5,6] : di2 = 1
    if (di1 in [4, 6]) and (di2 in [2, 3]) and \
        (p1.x >= p2.x) and (p1.x + p1.gl <= p2.x + p2.gl) and \
        (p1.z + p1.gh // 2 >= p2.z) and (p1.z + p1.gh // 2 <= p2.z + p2.gh):
        #// 侧板与背板接触，侧板竖纹，背板竖纹
        #// 纹理面开槽
        y = p1.x - p2.x
        x = p1.z - p2.z
        cy = c.y
        if p2.zero_y==2 : #//  右
            y = p1.x + p1.gl - p2.x
            cy = -c.y
        bh = Delphi_Round(p2.bh)
        AddKC_A(c, p1, p2, AffineVectorMake( c.y, p1.gp, c.x), AffineVectorMake(c.y, p1.gp-bh, c.x + c.l + p1.gh), x + c.x, y + cy,
                x + c.x + p1.gh + c.l, y+cy,  p1.gh + c.l, 'Front', c.flag, p1.bh)
    if (di1 in [1, 5]) and (di2 in [2, 3]) and    \
        (p1.z >= p2.z) and (p1.z + p1.gh <= p2.z + p2.gh) and    \
        (p1.x + p1.gl // 2 >= p2.x) and (p1.x + p1.gl // 2 <= p2.x + p2.gl):
        #// 背板与侧板接触，背板竖纹，侧板竖纹
        #// 纹理面开槽
        x = p1.x - p2.x
        y = p1.z - p2.z
        cy = c.y
        if p2.zero_y==6 : #// 前
            y = p1.z + p1.gh - p2.z
            cy = -c.y
        bh = Delphi_Round(p2.bh)
        AddKC_A(c, p1, p2, AffineVectorMake(c.x, p1.gp, c.y), AffineVectorMake(c.x + c.l + p1.gl, p1.gp-bh, c.y), y + cy, x + c.x,
                y + cy, x + c.x + p1.gl + c.l,  p1.gl + c.l, 'Front', c.flag, p1.bh)
def CalcKC_LeftFace(p1, p2, c):
    if (c==None): return
    di1 = p1.direct
    di2 = p2.direct
    if Delphi_not(di1) in [1,2,3,4,5,6] : di1= 1
    if Delphi_not(di2) in [1,2,3,4,5,6] : di2 = 1
    if (di1 in [1, 5]) and (di2 in [4, 6]) and \
        (p1.z >= p2.z) and (p1.z + p1.gh <= p2.z + p2.gh) and \
        (p1.y + p1.gp // 2 >= p2.y) and (p1.y + p1.gp // 2 <= p2.y + p2.gp):
        # 'Left1'
        #// 层板与侧板接触，层板是横纹，侧板是竖纹
        #// 纹理面开槽
        y = p1.z - p2.z
        x = p1.y - p2.y
        cy = c.y
        if p2.zero_y==6 : #// 上
            y = p1.z + p1.gh - p2.z
            cy = -c.y
        bh = Delphi_Round(p2.bh)
        AddKC_B(c, p1, p2, AffineVectorMake(0, c.x, c.y), AffineVectorMake(bh, c.x + c.l + p1.gp, c.y), y + cy, x + c.x, y + cy,
                x + c.x + p1.gp + c.l, p1.gp + c.l, 'Left', c.flag, p1.bh)
    if (di1 in [2, 3]) and (di2 in [4, 6]) and    \
        (p1.y >= p2.y) and (p1.y + p1.gp <= p2.y + p2.gp) and    \
        (p1.z + p1.gh // 2 > p2.z) and (p1.z + p1.gh // 2 <= p2.z + p2.gh):
        #// 背板与侧板接触，背板竖纹，侧板竖纹
        #// 纹理面开槽
        x = p1.z - p2.z
        y = p1.y - p2.y
        cy = c.y
        if p2.zero_y==4 : #// 前
            y = p1.y + p1.gp - p2.y
            cy = -c.y
        # 'Left2'
        bh = Delphi_Round(p2.bh)
        AddKC_B(c, p1, p2, AffineVectorMake(0, c.y, c.x), AffineVectorMake(bh, c.y, c.x + c.l + p1.gh), x + c.x, y + cy,
                x + c.x + p1.gh + c.l, y + cy, p1.gh + c.l, 'Left', c.flag, p1.bh)
def CalcKC_RightFace(p1, p2, c):
    if (c==None): return
    di1 = p1.direct
    di2 = p2.direct
    if Delphi_not(di1) in [1,2,3,4,5,6] : di1 = 1
    if Delphi_not(di2) in [1,2,3,4,5,6] : di2 = 1
    if (di1 in [1, 5]) and (di2 in [4, 6]) and \
        (p1.z >= p2.z) and (p1.z + p1.gh <= p2.z + p2.gh) and \
        (p1.y + p1.gp // 2 >= p2.y) and (p1.y + p1.gp // 2 <= p2.y + p2.gp):
        #// 层板与侧板接触，层板是横纹，侧板是竖纹
        #// 纹理面开槽
        y = p1.z - p2.z
        x = p1.y - p2.y
        cy = c.y
        if p2.zero_y==6 : #// 上
            y = p1.z + p1.gh - p2.z
            cy = -c.y
        bh = Delphi_Round(p2.bh)
        # if p2.name == u'右侧板' and p2.color == u'314#B蜡木':
        #     print u'右侧板：', 'v0=', v0, 'v1=', v1, p1.name, p1.m, p1.v
        AddKC_A(c, p1, p2, AffineVectorMake(p1.gl, c.x, c.y), AffineVectorMake(p1.gl-bh, c.x + c.l + p1.gp, c.y), y + cy, x + c.x, y + cy,
                x + c.x + p1.gp + c.l, p1.gp + c.l, 'Right', c.flag, p1.bh)
    if (di1 in [2, 3]) and (di2 in [4, 6]) and    \
        (p1.y >= p2.y) and (p1.y + p1.gp <= p2.y + p2.gp) and    \
        (p1.z + p1.gh // 2 >= p2.z) and (p1.z + p1.gh // 2 <= p2.z + p2.gh):
        #// 背板与侧板接触，背板竖纹，侧板竖纹
        #// 纹理面开槽
        x = p1.z - p2.z
        y = p1.y - p2.y
        cy = c.y
        if p2.zero_y==4 : #// 前
            y = p1.y + p1.gp - p2.y
            cy = -c.y
        bh = Delphi_Round(p2.bh)
        AddKC_A(c, p1, p2, AffineVectorMake(p1.gl, c.y, c.x), AffineVectorMake(p1.gl-bh, c.y, c.x + c.l + p1.gh), x + c.x, y + cy,
                x + c.x + p1.gh + c.l, y + cy, p1.gh + c.l, 'Right', c.flag, p1.bh)
def CalcKC_UpFace(p1, p2, c):
    if (c==None): return
    di1 = p1.direct
    di2 = p2.direct
    if Delphi_not(di1) in [1,2,3,4,5,6] : di1 = 1
    if Delphi_not(di2) in [1,2,3,4,5,6] : di2 = 1
    if (di1 in [4, 6]) and (di2 in [1, 5]) and \
        (p1.x >= p2.x) and (p1.x + p1.gl <= p2.x + p2.gl) and \
        (p1.y + p1.gp // 2 >= p2.y) and (p1.y + p1.gp // 2 <= p2.y + p2.gp):
        #// 中立板与顶板接触，中立板是竖纹，底板横纹
        #// 纹理面开槽
        y = p1.x - p2.x
        x = p1.y - p2.y
        cy = c.y
        if p2.zero_y==2 : #// 上
            y = p1.x + p1.gl - p2.x
            cy = -c.y
        bh = Delphi_Round(p2.bh)
        AddKC_A(c, p1, p2, AffineVectorMake( c.y, c.x, p1.gh), AffineVectorMake(c.y,c.x+c.l+p1.gp,p1.gh-bh), y + cy, x + c.x, y + cy,
                x + c.x + p1.gp + c.l, p1.gp + c.l, 'Up', c.flag, p1.bh)
    if (di1 in [2, 3]) and (di2 in [1, 5]) and    \
        (p1.y >= p2.y) and (p1.y + p1.gp <= p2.y + p2.gp) and    \
        (p1.x + p1.gl // 2 >= p2.x) and (p1.x + p1.gl // 2 <= p2.x + p2.gl):
        #// 背板与侧板接触，背板竖纹，侧板竖纹
        #// 纹理面开槽
        x = p1.x - p2.x
        y = p1.y - p2.y
        cy = c.y
        if p2.zero_y==4 : #// 前
            y = p1.y + p1.gp - p2.y
            cy = -c.y
        bh = Delphi_Round(p2.bh)
        AddKC_A(c, p1, p2, AffineVectorMake(c.x, c.y, p1.gh), AffineVectorMake(c.x + c.l + p1.gl, c.y, p1.gh-bh), x + c.x, y + cy,
                x + c.x + p1.gl + c.l, y + cy, p1.gl + c.l, 'Up', c.flag, p1.bh)
def CI_KcFace(face, p):
    Result = face
    if p.space=='B':
        #//左右下上后前
        if face==0 : Result = 5  #//左封边->前封边
        if face==1 : Result = 4  #//右封边->后封边
        if face==4 : Result = 1  #//后封边->右封边
        if face==5 : Result = 0  #//前封边->左封边
    if p.space=='C' :
        #//左右下上后前
        if face==0 : Result = 4  #//左封边->后封边
        if face==1 : Result = 5  #//右封边->前封边
        if face==4 : Result = 0  #//后封边->左封边
        if face==5 : Result = 1  #//前封边->右封边
    return Result
def GetKCConfig(hashid, faceid, poi):
    # hashid,faceid,
    Result = None
    Kclist = kcconfigHash[hashid]
    # 'Kclist=',len(Kclist)
    di = poi.direct
    if (len(Kclist) > 0) and (di == 0) :
        di = 1# // 没有设定纹路，但是又需要计算孔位的模块，di值等价1
    for i in range(0,len(Kclist)):
        p = Kclist[i]
        # CI_KcFace(p.myface, poi)
        if CI_KcFace(p.myface, poi) == faceid:
            # 'hahah'
            t0 = poi.bg_l_maxx - poi.bg_l_minx
            t1 = poi.bg_l_maxy - poi.bg_l_miny
            if (CI_KcFace(p.myface, poi) == 0) and (((di in [1, 5]) and (t0 > p.min) and (t0 <= p.max)) or (
                    (di in [2, 3]) and (t1 > p.min) and (t1 <= p.max))) :    # // 左面
                # 'a'
                Result = p
                return Result
            t0 = poi.bg_r_maxx - poi.bg_r_minx
            t1 = poi.bg_r_maxy - poi.bg_r_miny
            if (CI_KcFace(p.myface, poi) == 1) and (((di in [1, 5]) and (t0 > p.min) and (t0 <= p.max)) or (
                    (di in [2, 3]) and (t1 > p.min) and (t1 <= p.max))) : #// 右面
                # 'b'
                Result = p
                return Result
            t0 = poi.bg_d_maxx - poi.bg_d_minx
            t1 = poi.bg_d_maxy - poi.bg_d_miny
            if (CI_KcFace(p.myface, poi) == 2) and (((di in [4, 6]) and (t1 > p.min) and (t1 <= p.max)) or (
                    (di in [2, 3]) and (t0 > p.min) and (t0 <= p.max))) : #// 下面
                # 'c'
                Result = p
                return Result
            t0 = poi.bg_u_maxx - poi.bg_u_minx
            t1 = poi.bg_u_maxy - poi.bg_u_miny
            if (CI_KcFace(p.myface, poi) == 3) and (((di in [4, 6]) and (t1 > p.min) and (t1 <= p.max)) or (
                    (di in [2, 3]) and (t0 > p.min) and (t0 <= p.max))) : #// 上面
                # 'd'
                Result = p
                return Result
            t0 = poi.bg_b_maxx - poi.bg_b_minx
            t1 = poi.bg_b_maxy - poi.bg_b_miny
            if (CI_KcFace(p.myface, poi) == 4) and (((di in [4, 6]) and (t1 > p.min) and (t1 <= p.max)) or (
                    (di in [1, 5]) and (t0 > p.min) and (t0 <= p.max))) : #// 后面
                # 'e'
                Result = p
                return Result
            t0 = poi.bg_f_maxx - poi.bg_f_minx
            t1 = poi.bg_f_maxy - poi.bg_f_miny
            if (CI_KcFace(p.myface, poi) == 5) and (((di in [4, 6]) and (t1 > p.min) and (t1 <= p.max)) or (
                    (di in [1, 5]) and (t0 > p.min) and (t0 <= p.max))) : #// 前面
                # 'f'
                Result = p
                return Result
    return TKCConfig()
def CalcHoleUnit_CalcKCList(listKc):
    #动态计算开槽
    for i in range(0,len(listKc)):
        p1 = listKc[i]
        if p1.bdxmlid != '': continue
        for j in range(0,len(listKc)):
            if i==j: continue
            p1 = listKc[i]
            p2 = listKc[j]
            if (p1.space_id != p2.space_id) or (p1.sozflag != p2.sozflag) : continue
            p1, p2 = SubSpaceAItem(p1, p2, mCItem1, mCItem2)
            if (p1.x < p2.x + p2.gl) and (p1.x > p2.x) and (p1.kcid >= 0) : #// 左面
                # u'左面'
                CalcKC_LeftFace(p1, p2, GetKCConfig(p1.kcid, 0, p1))
                #with open(base_dir + '\\testdata\\' + 'mKCInfoList' + '.txt', 'a+') as f:
                log.debug(('j='+str(j)+'左面mKCInfoList='+str(len(mKCInfoList))+'\n').encode('gbk'))
                #print 'j='+str(j)+u'左面', len(mKCInfoList)
            if (p1.x + p1.gl < p2.x + p2.gl) and (p1.x + p1.gl > p2.x) and (p1.kcid >= 0) : #// 右面
                # u'右面'
                CalcKC_RightFace(p1, p2, GetKCConfig(p1.kcid, 1, p1))
                #with open(base_dir + '\\testdata\\' + 'mKCInfoList' + '.txt', 'a+') as f:
                log.debug(('j='+str(j)+'右面mKCInfoList='+str(len(mKCInfoList))+'\n').encode('gbk'))
                #print 'j='+str(j)+u'右面', len(mKCInfoList)
            if (p1.z < p2.z + p2.gh) and (p1.z > p2.z) and (p1.kcid >= 0) : #// 下面
                CalcKC_DownFace(p1, p2, GetKCConfig(p1.kcid, 2, p1))
                #with open(base_dir + '\\testdata\\' + 'mKCInfoList' + '.txt', 'a+') as f:
                log.debug(('j='+str(j)+'下面mKCInfoList='+str(len(mKCInfoList))+'\n').encode('gbk'))
                #print 'j='+str(j)+u'下面', len(mKCInfoList)
            if (p1.z + p1.gh < p2.z + p2.gh) and (p1.z + p1.gh > p2.z) and (p1.kcid >= 0) : #// 上面
                # u'上面'
                CalcKC_UpFace(p1, p2, GetKCConfig(p1.kcid, 3, p1))
                #with open(base_dir + '\\testdata\\' + 'mKCInfoList' + '.txt', 'a+') as f:
                log.debug(('j='+str(j)+'上面mKCInfoList='+str(len(mKCInfoList))+'\n').encode('gbk'))
                #print 'j='+str(j)+u'上面', len(mKCInfoList)
            if (p1.y < p2.y + p2.gp) and (p1.y > p2.y) and (p1.kcid >= 0) : #// 后面
                # u'后面'
                CalcKC_BackFace(p1, p2, GetKCConfig(p1.kcid, 4, p1))
                #with open(base_dir + '\\testdata\\' + 'mKCInfoList' + '.txt', 'a+') as f:
                log.debug(('j='+str(j)+'后面mKCInfoList='+str(len(mKCInfoList))+'\n').encode('gbk'))
                #print 'j='+str(j)+u'后面', len(mKCInfoList)
            if (p1.y + p1.gp < p2.y + p2.gp) and (p1.y + p1.gp > p2.y) and (p1.kcid >= 0) : #// 前面
                # u'前面'
                CalcKC_FrontFace(p1, p2, GetKCConfig(p1.kcid, 5, p1))
                #with open(base_dir + '\\testdata\\' + 'mKCInfoList' + '.txt', 'a+') as f:
                log.debug(('j='+str(j)+'前面mKCInfoList='+str(len(mKCInfoList))+'\n').encode('gbk'))
                #print 'j='+str(j)+u'前面', len(mKCInfoList)
            UpdateCalcItemResult(listKc[i], mCItem1)
            UpdateCalcItemResult(listKc[j], mCItem2)
    #         if (j == 2) and (p2.z == 903) and (len(mKCInfoList) == 17):
    #             print (
    #             str(p2.akc_index[0]) + ',' + str(p2.akc_index[1]) + ',' + str(p2.akc_index[2]) + str(
    #         len(mKCInfoList)) + 'i=' + str(i))
    #
    # print (str(listKc[2].akc_index) + ',' + str(len(mKCInfoList)) )
    #//根据bdxml 计算开槽
    for i in range(0,len(listKc)):
        p1 = listKc[i]
        if p1.bdxmlid=='' : continue
        for j in range(0,len(listKc)):
            if i == j : continue
            p1 = listKc[i]
            p2 = listKc[j]
            if (p1.space_id != p2.space_id) or (p1.sozflag != p2.sozflag) : continue
            p1, p2 =SubSpaceAItem(p1, p2, mCItem1, mCItem2)
            if (p1.x < p2.x + p2.gl) and (p1.x > p2.x) and (p1.kcid >= 0) : #// 左面
                CalcKC_LeftFace(p1, p2, GetKCConfig(p1.kcid, 0, p1))
            if (p1.x + p1.gl < p2.x + p2.gl) and (p1.x + p1.gl > p2.x) and (p1.kcid >= 0) : #// 右面
                CalcKC_RightFace(p1, p2, GetKCConfig(p1.kcid, 1, p1))
            if (p1.z < p2.z + p2.gh) and (p1.z > p2.z) and (p1.kcid >= 0) : #// 下面
                CalcKC_DownFace(p1, p2, GetKCConfig(p1.kcid, 2, p1))
            if (p1.z + p1.gh < p2.z + p2.gh) and (p1.z + p1.gh > p2.z) and (p1.kcid >= 0) : #// 上面
                CalcKC_UpFace(p1, p2, GetKCConfig(p1.kcid, 3, p1))
            if (p1.y < p2.y + p2.gp) and (p1.y > p2.y + p2.gp) and (p1.kcid >= 0) : #// 后面
                CalcKC_BackFace(p1, p2, GetKCConfig(p1.kcid, 4, p1))
            if (p1.y + p1.gp < p2.y + p2.gp) and (p1.y + p1.gp > p2.y) and (p1.kcid >= 0) : #// 前面
                CalcKC_FrontFace(p1, p2, GetKCConfig(p1.kcid, 5, p1))
            UpdateCalcItemResult(listKc[i], mCItem1)
            UpdateCalcItemResult(listKc[j], mCItem2)
    #print 'mKCInfoList=',len(mKCInfoList)
def CalcItem2BomItem(p, p2):
    item = p
    Item2 = p2
    Result = Item2
    Item2['bl'] = item.bl
    Item2['bp'] = item.bp
    Item2['bh'] = item.bh
    Item2['pl'] = item.pl
    Item2['pd'] = item.pd
    Item2['ph'] = item.ph
    Item2['lx'] = item.lx
    Item2['ly'] = item.ly
    Item2['lz'] = item.lz
    Item2['x'] = item.x
    Item2['y'] = item.y
    Item2['z'] = item.z
    Item2['l'] = item.l
    Item2['p'] = item.p
    Item2['h'] = item.h
    Item2['gl'] = item.gl
    Item2['gp'] = item.gp
    Item2['gh'] = item.gh
    #// item2.direct:= item.direct
    Item2['holeid'] = item.holeid
    Item2['kcid'] = item.kcid
    for i in range(0,101):
        if i <= 15 : Item2['var_args'][i] = item.var_args[i]
        Item2['ahole_index'][i] = item.ahole_index[i]
        Item2['bhole_index'][i] = item.bhole_index[i]
        Item2['akc_index'][i] = item.akc_index[i]
        Item2['bkc_index'][i] = item.bkc_index[i]
        if i <= 5 : Item2['is_calc_holeconfig'][i] = item.is_calc_holeconfig[i]
    Item2['hole_back_cap'] = item.hole_back_cap
    Item2['hole_2_dist'] = item.hole_2_dist
    Item2['holeconfig_flag'] = item.holeconfig_flag
    Item2['kcconig_flag'] = item.kcconig_flag
    return Result
def CalcList2BomList(calclist, bomlist, is_dispose_calcitem=True):
    # 'calclist,calclist:',len(calclist)
    for i in range(0,len(bomlist)):
        CalcItem2BomItem(calclist[i], bomlist[i])
def CalcKCCombine(bomlist):
    for i in range(0,len(bomlist)):
        p = bomlist[i]
        #A面开槽
        for j in range(0,101):
            if p['akc_index'][j] < 0: break
            kcinfo0 = mKCInfoList[p['akc_index'][j]]
            if kcinfo0.kcid < 0: continue
            for k in range(100, j, -1):
                if p['akc_index'][k] < 0 : continue
                kcinfo1 = mKCInfoList[p['akc_index'][k]]
                if kcinfo1.kcid < 0 : continue
                if kcinfo0.flag != kcinfo1.flag : continue
                #// X方向在同一水平线上，合并开槽
                if (kcinfo0.x0 == kcinfo0.x1) and (kcinfo1.x0 == kcinfo1.x1) :
                    if abs(kcinfo0.y0 - kcinfo1.y1) < 3:
                        kcinfo0.y0 = kcinfo1.y0
                        kcinfo1.kcid = -1
                    if abs(kcinfo0.y1 - kcinfo1.y0) < 3:
                        kcinfo0.y1 = kcinfo1.y1
                        kcinfo1.kcid = -1
                #// Y方向在同一水平线上，合并开槽
                if (kcinfo0.y0 == kcinfo0.y1) and (kcinfo1.y0 == kcinfo1.y1) :
                    if abs(kcinfo0.x0 - kcinfo1.x1) < 3 :
                        kcinfo0.x0 = kcinfo1.x0
                        kcinfo1.kcid = -1
                    if abs(kcinfo0.x1 - kcinfo1.x0) < 3 :
                        kcinfo0.x1 = kcinfo1.x1
                        kcinfo1.kcid = -1
        #B面开槽
        for j in range(0, 101):
            if p['bkc_index'][j] < 0: break
            kcinfo0 = mKCInfoList[p['bkc_index'][j]]
            if kcinfo0.kcid < 0: continue
            for k in range(100, j, -1):
                if p['bkc_index'][k] < 0: continue
                kcinfo1 = mKCInfoList[p['bkc_index'][k]]
                if kcinfo1.kcid < 0: continue
                if kcinfo0.flag != kcinfo1.flag: continue
                # // X方向在同一水平线上，合并开槽
                if (kcinfo0.x0 == kcinfo0.x1) and (kcinfo1.x0 == kcinfo1.x1):
                    if abs(kcinfo0.y0 - kcinfo1.y1) < 3:
                        kcinfo0.y0 = kcinfo1.y0
                        kcinfo1.kcid = -1
                    if abs(kcinfo0.y1 - kcinfo1.y0) < 3:
                        kcinfo0.y1 = kcinfo1.y1
                        kcinfo1.kcid = -1
                # // Y方向在同一水平线上，合并开槽
                if (kcinfo0.y0 == kcinfo0.y1) and (kcinfo1.y0 == kcinfo1.y1):
                    if abs(kcinfo0.x0 - kcinfo1.x1) < 3:
                        kcinfo0.x0 = kcinfo1.x0
                        kcinfo1.kcid = -1
                    if abs(kcinfo0.x1 - kcinfo1.x0) < 3:
                        kcinfo0.x1 = kcinfo1.x1
                        kcinfo1.kcid = -1
        # 清除掉被合并的开槽
        for j in range(100, -1, -1):
            if p['akc_index'][j] >= 0:
                kcinfo0 = mKCInfoList[p['akc_index'][j]]
                if kcinfo0.kcid < 0: p['akc_index'][j] = -1
            if p['bkc_index'][j] >= 0:
                kcinfo0 = mKCInfoList[p['bkc_index'][j]]
                if kcinfo0.kcid < 0: p['bkc_index'][j] = -1
        for j in range(0,101):
            if p['akc_index'][j] >= 0: continue
            for k in range(j+1,101):
                if p['akc_index'][j] >= 0: continue
                p['akc_index'][j] =p['akc_index'][k]
                p['akc_index'][k] = -1
        for j in range(0,101):
            if p['bkc_index'][j] >= 0: continue
            for k in range(j+1,101):
                if p['bkc_index'][j] >= 0: continue
                p['bkc_index'][j] =p['bkc_index'][k]
                p['bkc_index'][k] = -1
def CalcHoleAndKc(mProductList,bomlist,workflowlist,mIIHoleCalcRule,mBDXMLList,gBGHash):
    global mHPInfoList,mKCInfoList,mHoleRow
    mHPInfoList, mKCInfoList = [],[]
    mHoleRow = 0
    tem_list = []
    calclist = []
    for i in range(0,len(mProductList)):
        tem_list = []
        calclist = []
        iddict = {}
        k = 0
        for j in range(0,len(bomlist)):
            p = bomlist[j]
            if p['cid'] != i or not p['isoutput']:
                continue
            tem_list.append(p)
            #print 'len of tem_list',len(tem_list)
            iddict[k] = j
            k = k + 1
        BomList2CalcList(tem_list,calclist,workflowlist,mBDXMLList,gBGHash)
        CalcHoleUnit_CalcHoleList(calclist, mIIHoleCalcRule)
        CalcHoleUnit_CalcKCList(calclist)
        CalcList2BomList(calclist,tem_list)
    CalcKCCombine(bomlist)
    return mHPInfoList,mKCInfoList
mHoleFaceTwice = 0  # // 第二次计算打孔面
mCItem1 = TMyCalcItem()
mCItem2 = TMyCalcItem()
mHPInfoList = []
mKCInfoList = []
mTmpExp = {'CA': '', 'CB': '', 'CC': '', 'CD': '', 'CE': '',
               'CF': '', 'CG': '', 'CH': '', 'CI': '', 'CJ': '', 'CK': '',
               'CL': '', 'CM': '', 'CN': '', 'CO': '', 'CP': ''}
mHoleRow = 0