#  -*- coding:utf-8 -*-
'''
vesion 1.0.1
2019/7/15
author:litao
'''
import os,sys
print(os.getcwd())
print(sys.path)
sys.path.append(os.getcwd()+'\\Python3\\PythontoBomJson')
from xmltojsonpackage import *
from funcCalcHoleAndKc import CalcHoleAndKc

log = logging.getLogger(base_dir+"\\Python\\Log\\all.log")
def load(xmlfile,mOrderName,orderdict,dxPopupGNOText,productgnolist):
    mProductList,bomlist,doorlist,slidinglist,mBDXMLList,JsonPrice,productdatadict = LoadXMLFile2Bom(xmlfile)
    print('len of bomlist',len(bomlist))
    print('len of mProductList', len(mProductList))
    print('len of doorlist', len(doorlist))
    print('len of slidinglist', len(slidinglist))
    print('len of mBDXMLList', len(mBDXMLList))
    # BomObjPath = base_dir + '\\Python\\bomobj.json'
    # basewjlistObjPath = base_dir + '\\Python\\basewjlist.json'
    # QuoConPath = base_dir + '\\Python\\QuoCon.json'
    # with open(BomObjPath, 'w+') as f:
    #      f.write(json.dumps(JsonPrice, ensure_ascii=False).encode('gbk'))
    InitBgMinAndMax(bomlist, gBGHash)
    CalcLgFlag(bomlist)
    basewjlist = CalcBomWj()
    mHPInfoList, mKCInfoList = CalcHoleAndKc(mProductList,bomlist,workflowlist, mIIHoleCalcRule, mBDXMLList,gBGHash)
    #print 'len of mHPInfoList',len(mHPInfoList)
    #print 'len of mKCInfoList',len(mKCInfoList)
    InitBgMinAndMax(bomlist,gBGHash)
    print('len of basewjlist1', len(basewjlist))
    #print json.dumps(basewjlist,ensure_ascii=False).encode('gbk')
    CalcHoleWj(bomlist, basewjlist, mHPInfoList,workflowlist,gBGHash,mKCInfoList)
    # print 'len of basewjlist2', len(basewjlist)
    # with open(basewjlistObjPath, 'w+') as f:
    #     f.write(json.dumps(basewjlist, ensure_ascii=False).encode('gbk'))
    desclist = []
    JsonPriceAddWujin(JsonPrice, basewjlist,desclist)
    #print 'len of bomlist', len(bomlist)
    #print 'len of desclist', len(desclist)
    Data = {}
    return mProductList, bomlist, Data, JsonPrice,desclist,productdatadict,slidinglist,doorlist
def JsonPriceAddWujin(JsonPrice, basewjlist, desclist):
    def addwujin(mymodles):
        for modle in mymodles:
            if (modle['desc'] not in desclist) and (modle['desc']!=''):
                desclist.append(modle['desc'])
            modle['基础五金'] = []
            for basewj in basewjlist:
                if modle['guid'] == basewj['guid']:# and modle['cid'] == basewj['cid'] and \
                #         modle['name'] == basewj['modlename'] and modle['gno'] == basewj['gno'] and modle['gcb'] == basewj['gcb'] \
                #     and modle['extra'] == basewj['extra'] and modle['subspace'] == basewj['subspace']:
                    modle['基础五金'].append(basewj)
                    if (basewj['desc'] not in desclist) and (basewj['desc'] != ''):
                        desclist.append(basewj['desc'])
            if '我的模块' in modle:
                addwujin(modle['我的模块'])
    for ALlPrice in JsonPrice['柜体列表']:
        addwujin(ALlPrice['我的模块'])
        #desclist.append(ALlPrice[u'类别'])
def functionxmltojson(xmlfile, mOrderName, orderdict, dxPopupGNOText, productgnolist):
    print('RootPath=',RootPath)
    TempPath = os.path.abspath(os.path.join(os.getcwd())) + '\\Temp'
    xmlfile = TempPath + '\\' + xmlfile.decode('gbk').encode('utf8')
    #gBGHash, gPluginsList, seqInfoHash, classseqInfoHash, workflowlist, gBoardMatList, gErpItemList, mIIHoleCalcRule,gROC = InitData()
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
    mProductList, bomlist, Data, JsonPrice, desclist, productdatadict,slidinglist, doorlist= load(xmlfile,
                        mOrderName,
                        orderdict,
                        dxPopupGNOText,
                        productgnolist)
    print('len of mProductList', len(mProductList))
    print('len of bomlist',len(bomlist))
    return JsonPrice,desclist,productdatadict,slidinglist,doorlist
def XmltoJson(xml, GetNetworkQuoteConfigHandl, Path):
    global RootPath
    RootPath = Path
    #InitRootPathConfig(Path)  # 初始化根目录配置文件夹数据
    mProductList, bomlist, Desdoorlist, Desslidinglist, mBDXMLList, JsonPrice, productdatadict, \
    workflowlist, mIIHoleCalcRule, mBDXMLList, gBGHash = LoadXML2Bom(xml, Path)
    log.info('len of bomlist='+str(len(bomlist)))
    log.info('len of mProductList='+ str(len(mProductList)))
    log.info('len of Desdoorlist='+str(len(Desdoorlist)))
    log.info('len of Desslidinglist='+str(len(Desslidinglist)))
    log.info('len of mBDXMLList='+str(len(mBDXMLList)))
    InitBgMinAndMax(bomlist)
    CalcLgFlag(bomlist)
    basewjlist = CalcBomWj()
    mHPInfoList, mKCInfoList = CalcHoleAndKc(mProductList, bomlist, workflowlist, mIIHoleCalcRule, mBDXMLList, gBGHash)
    log.info('len of basewjlist1='+str(len(basewjlist)))
    CalcHoleWj(bomlist, basewjlist, mHPInfoList, workflowlist, gBGHash, mKCInfoList)
    desclist = []
    JsonPriceAddWujin(JsonPrice, basewjlist, desclist)
    priceconfig = GetNetworkQuoteConfigHandl(desclist, Desslidinglist, Desdoorlist)
    JsonPrice.update(priceconfig)
    return json.dumps(JsonPrice,encoding='utf8',ensure_ascii=False).encode('utf8')
def writetofile(bomlist, datapath):
    if not os.path.exists(base_dir + '\\'+datapath+'\\'):
        os.makedirs(base_dir + '\\'+datapath+'\\')
    DeleteDirectory(base_dir + '\\'+datapath+'\\')
    if not os.path.exists(base_dir + '\\'+datapath+'\\'):
        os.makedirs(base_dir + '\\'+datapath+'\\')
    for i in range(0, len(bomlist)):
        p = bomlist[i]
        # if p['desc'] ==u'掩门,掩门':
        #     print p['isoutput'] ,p['name']
        #     exit(1)
        # print p['name'],p['ahole_index']
        # if p['name'] == u'QS-03':
        #     print p['isoutput'], str(i) + 'p.bl:' + str(p['bl']) + 'p.bp:' + str(p['bp']) + 'p.bh:' + str(
        #         p['bh']) + 'guid=' + str(p['guid']) + p['bg']
        if p['is_outline'] == False:
            p['is_outline'] = '0'
        else:
            p['is_outline'] = '-1'
        if p['isoutput'] == False:
            p['isoutput'] = '0'
        else:
            p['isoutput'] = '-1'
        var_args = ''
        var_names = ''
        is_calc_holeconfig = ''
        akc = ''
        bkc = ''
        ahole = ''
        bhole = ''
        for j in range(0, 16):
            var_args = var_args + str(p['var_args'][j])
        for j in range(0, 16):
            var_names = var_names + str(p['var_names'][j])
        for j in range(0, 6):
            is_calc_holeconfig = is_calc_holeconfig + str(p['is_calc_holeconfig'][j])
        for j in range(0, 101):
            ahole = ahole + str(p['ahole_index'][j]) + ','
            bhole = bhole + str(p['bhole_index'][j]) + ','
            akc = akc + str(p['akc_index'][j]) + ','
            bkc = bkc + str(p['bkc_index'][j]) + ','
        with open(base_dir + '\\'+datapath+'\\' + 'isoutput' + str(i) + '.txt', 'w+') as f:
            # print i, p['name'], p['guid'], 'trans_ab=',p['trans_ab'], p['ahole_index']
            f.write(('isoutput:' + str(p['isoutput']) + p['name'] + 'p.num:' + str(p['num'])
                     + 'p.bl:' + str(int(p['bl'])) + 'p.bp:' + str(int(p['bp'])) + 'p.bh:' + str(p['bh'])
                     + ',gl=' + str(p['gl']) + ',gp=' + str(p['gp']) + ',gh=' + str(p['gh']) + '\n'
                     + 'cid=' + str(p['cid']) + ',seq=' + str(p['seq']) + '\n'
                     + 'classseq=' + str(p['classseq']) + ',mark=' + str(p['mark']) + ',vp=' + str(
                        p['vp']) + ',code=' + str(p['code']) + '\n'
                     + 'name=' + str(p['name']) + ',mat=' + str(p['mat']) + ',mat2=' + str(p['mat2']) + ',mat3=' + str(
                        p['mat3']) + '\n'
                     + 'color=' + str(p['color']) + ',workflow=' + str(p['workflow']) + ',pl=' + str(
                        p['pl']) + ',pd=' + str(p['pd']) + '\n'
                     + 'ph=' + str(p['ph']) + ',space_x=' + str(p['space_x']) + ',space_y=' + str(
                        p['space_y']) + ',space_z=' + str(p['space_z']) + '\n'
                     # + 'space_id=' + str(p['space_id'])
                     # + ',gcl=' + str(p['gcl']) + ',gcd=' + str(p['gcd']) + ',gch=' + str(p['gch']) + '\n'
                     # + 'gcl2=' + str(p['gcl2']) + ',gcd2=' + str(p['gcd2']) + ',gch2=' + str(p['gch2'])
                     # + ',tmp_soz=' + str(p['tmp_soz']) + '\n'
                     + 'lx=' + str(p['lx']) + ',ly=' + str(p['ly']) + ',lz=' + str(p['lz']) + ',x=' + str(p['x']) + '\n'
                     + 'y=' + str(p['y']) + ',z=' + str(p['z']) + ',l=' + str(p['l']) + ',p=' + str(p['p']) + '\n'
                     + 'h=' + str(p['h']) + ',gl=' + str(p['gl']) + ',gp=' + str(p['gp']) + ',gh=' + str(p['gh']) + '\n'
                     + 'holeflag=' + str(p['holeflag']) + ',linemax=' + str(p['linemax']) + ',holetype=' + str(
                        p['holetype']) + ',ox=' + str(int(float(p['ox']))) + '\n'
                     + 'oy=' + str(int(float(p['oy']))) + ',oz=' + str(int(float(p['oz']))) + ',childnum=' + str(
                        p['childnum']) + ',desc=' + str(p['desc']) + '\n'
                     + 'bomdes=' + str(p['bomdes']) + ',bomwjdes=' + str(p['bomwjdes']) + ',bomstddes=' + str(
                        p['bomstddes']) + ',childbom=' + str(p['childbom']) + '\n'
                     + 'myclass=' + str(p['myclass']) + ',nodename=' + str(p['nodename']) + ',linecalc=' + str(
                        p['linecalc']) + ',bomstd=' + str(p['bomstd']) + '\n'
                     + 'bg=' + str(p['bg']) + ',direct=' + str(p['direct']) + ',lgflag=' + str(
                        p['lgflag']) + ',num=' + str(p['num']) + '\n'
                     + 'lfb=' + str(p['lfb']) + ',llk=' + str(p['llk']) + ',wfb=' + str(p['wfb']) + ',wlk=' + str(
                        p['wlk']) + '\n'
                     + 'llfb=' + str(p['llfb']) + ',rrfb=' + str(p['rrfb']) + ',ddfb=' + str(
                        p['ddfb']) + ',uufb=' + str(
                        p['uufb']) + '\n'
                     + 'fb=' + str(p['fb']) + 'holestr=' + str(p['holestr']) + ',kcstr=' + str(
                        p['kcstr']) + ',memo=' + str(p['memo']) + ',gno=' + str(p['gno']) + '\n'
                     + 'gdes=' + str(p['gdes']) + ',gcb=' + str(p['gcb']) + ',extra=' + str(
                        p['extra']) + ',fbstr=' + str(p['fbstr']) + '\n'
                     + 'subspace=' + str(p['subspace']) + ',process=' + str(p['process']) + ',ls=' + str(
                        p['ls']) + ',myunit=' + str(p['myunit']) + '\n'
                     + 'bomtype=' + str(p['bomtype']) + ',bdxmlid=' + str(p['bdxmlid']) + ',user_fbstr=' + str(
                        p['user_fbstr']) + ',bl=' + str(p['bl']) + '\n'
                     + 'bp=' + str(p['bp']) + ',bh=' + str(
                        p['bh']) + ',var_names=' + var_names + ',var_args=' + var_args + ',value_lsk=' + str(
                        p['value_lsk']) + ',value_rsk=' + str(p['value_rsk']) + '\n'
                     + 'value_zk=' + str(p['value_zk']) + ',value_zs=' + str(p['value_zs']) + ',value_ls=' + str(
                        p['value_ls']) + ',value_lg=' + str(p['value_lg']) + '\n'
                     + 'value_ltm=' + str(p['value_ltm']) + ',value_rtm=' + str(p['value_rtm']) + ',a_hole_info=' + str(
                        p['a_hole_info']) + ',b_hole_info=' + str(p['b_hole_info']) + '\n'
                     + 'holeinfo=' + str(p['holeinfo']) + ',isoutput=' + str(p['isoutput']) + ',is_outline=' + str(
                        p['is_outline']) + ',outputtype=' + str(p['outputtype']) + '\n' + 'holeconfig_flag=' + str(
                        p['holeconfig_flag']) + ',kcconig_flag=' + str(p['kcconig_flag']) + ',bg_data=' + str(
                        p['bg_data']) + ',mBGParam=' + str(p['mBGParam']) + '\n'
                     # + 'bg_filename=' + str(p['bg_filename']) + ',mpr_filename=' + str(p['mpr_filename']) + ',bpp_filename=' + str(p['bpp_filename']) + ',devcode=' + str(p['devcode']) + '\n'
                     # + 'zero_y=' + str(p['zero_y']) + ',direct_calctype=' + str(p['direct_calctype']) + ',youge_holecalc=' + str(p['youge_holecalc']) + ',is_output_bgdata=' + str(p['is_output_bgdata']) + '\n'
                     # + 'is_output_mpr=' + str(p['is_output_mpr']) + ',is_output_bpp=' + str(p['is_output_bpp']) + '\n'
                     + 'bg_l_minx=' + str(p['bg_l_minx']) + '\n' + ',bg_l_maxx=' + str(p['bg_l_maxx']) + '\n'
                     + 'bg_l_minx=' + str(p['bg_l_miny']) + '\n' + ',bg_l_maxy=' + str(p['bg_l_maxy']) + '\n'
                     + 'bg_d_minx=' + str(p['bg_d_minx']) + '\n' + ',bg_d_maxx=' + str(p['bg_d_maxx']) + '\n'
                     + 'bg_d_miny=' + str(p['bg_d_miny']) + '\n' + ',bg_d_maxy=' + str(p['bg_d_maxy']) + '\n'
                     + 'bg_b_minx=' + str(p['bg_b_minx']) + '\n' + ',bg_b_maxx=' + str(p['bg_b_maxx']) + '\n'
                     + 'bg_b_miny=' + str(p['bg_b_miny']) + '\n' + ',bg_b_maxy=' + str(p['bg_b_maxy']) + '\n'
                     + 'bg_r_minx=' + str(p['bg_r_minx']) + '\n' + ',bg_r_maxx=' + str(p['bg_r_maxx']) + '\n'
                     + 'bg_r_miny=' + str(p['bg_r_miny']) + '\n' + ',bg_l_maxy=' + str(p['bg_r_maxy']) + '\n'
                     + 'bg_u_minx=' + str(p['bg_u_minx']) + '\n' + ',bg_u_maxx=' + str(p['bg_u_maxx']) + '\n'
                     + 'bg_u_miny=' + str(p['bg_u_miny']) + '\n' + ',bg_u_maxy=' + str(p['bg_u_maxy']) + '\n'
                     + 'bg_f_minx=' + str(p['bg_f_minx']) + '\n' + ',bg_f_maxx=' + str(p['bg_f_maxx']) + '\n'
                     + 'bg_f_miny=' + str(p['bg_f_miny']) + '\n' + ',bg_f_maxy=' + str(p['bg_f_maxy']) + '\n'
                     + 'lfb=' + str(p['lfb']) + ',llk=' + str(p['llk']) + ',wfb=' + str(p['wfb']) + ',wlk=' + str(
                        p['wlk'])
                     + '\n' + 'lx=' + str(p['lx']) + ',ly=' + str(p['ly']) + ',lz=' + str(p['lz'])
                     + '\n' + 'x=' + str(p['x']) + ',y=' + str(p['y']) + ',z=' + str(p['z'])
                     + '\n' + 'bg=' + p['bg'] + ',var_args=' + var_args + 'zero_y=' + str(p['zero_y']) + 'desc=' + p[
                         'desc']
                     + '\n' + 'classseq=' + str(p['classseq']) + ',seq=' + str(p['seq'])
                     + '\n' + 'is_calc_holeconfig=' + is_calc_holeconfig
                     + '\n' + ',ahole=' + ahole + '\n' + ',bhole=' + bhole + '\n' + ',akc=' + akc + '\n' + ',bkc=' + bkc).encode(
                'gbk'))  # +'bg
def writebomquolist(bomQuolist):
    if not os.path.exists(base_dir + '\\'+datapath+'\\'):
        os.makedirs(base_dir + '\\'+datapath+'\\')
    for i in range(0, len(bomQuolist)):
        p = bomQuolist[i]
        var_args = ''
        var_names = ''
        for j in range(0, 16):
            var_args = var_args + str(p['var_args'][j])
        for j in range(0, 16):
            var_names = var_names + str(p['var_names'][j])
        with open(base_dir + '\\'+datapath+'\\' + 'isoutput' + str(i) + '.txt', 'w+') as f:
            # print i, p['name'], p['guid'], 'trans_ab=',p['trans_ab'], p['ahole_index']
            f.write(('isoutput:' + str(p['isoutput']) + p['name'] + 'p.num:' + str(p['num'])
                     + 'p.bl:' + str(int(p['bl'])) + 'p.bp:' + str(int(p['bp'])) + 'p.bh:' + str(p['bh'])
                     + ',gl=' + str(p['gl']) + ',gp=' + str(p['gp']) + ',gh=' + str(p['gh']) + '\n'
                     + 'cid=' + str(p['cid']) + ',seq=' + str(p['seq']) + '\n'
                     + 'classseq=' + str(p['classseq']) + ',mark=' + str(p['mark']) + ',vp=' + str(
                        p['vp']) + ',code=' + str(p['code']) + '\n'
                     + 'name=' + str(p['name']) + ',mat=' + str(p['mat']) + ',mat2=' + str(p['mat2']) + ',mat3=' + str(
                        p['mat3']) + '\n'
                     + 'color=' + str(p['color']) + ',workflow=' + str(p['workflow']) + ',pl=' + str(
                        p['pl']) + ',pd=' + str(p['pd']) + '\n'
                     + 'ph=' + str(p['ph']) + ',space_x=' + str(p['space_x']) + ',space_y=' + str(
                        p['space_y']) + ',space_z=' + str(p['space_z']) + '\n'
                     # + 'space_id=' + str(p['space_id'])
                     # + ',gcl=' + str(p['gcl']) + ',gcd=' + str(p['gcd']) + ',gch=' + str(p['gch']) + '\n'
                     # + 'gcl2=' + str(p['gcl2']) + ',gcd2=' + str(p['gcd2']) + ',gch2=' + str(p['gch2'])
                     # + ',tmp_soz=' + str(p['tmp_soz']) + '\n'
                     + 'lx=' + str(p['lx']) + ',ly=' + str(p['ly']) + ',lz=' + str(p['lz']) + ',x=' + str(p['x']) + '\n'
                     + 'y=' + str(p['y']) + ',z=' + str(p['z']) + ',l=' + str(p['l']) + ',p=' + str(p['p']) + '\n'
                     + 'h=' + str(p['h']) + ',gl=' + str(p['gl']) + ',gp=' + str(p['gp']) + ',gh=' + str(p['gh']) + '\n'
                     + 'holeflag=' + str(p['holeflag']) + ',linemax=' + str(p['linemax']) + ',holetype=' + str(
                        p['holetype']) + ',ox=' + str(int(float(p['ox']))) + '\n'
                     + 'oy=' + str(int(float(p['oy']))) + ',oz=' + str(int(float(p['oz']))) + ',childnum=' + str(
                        p['childnum']) + ',desc=' + str(p['desc']) + '\n'
                     + 'bomdes=' + str(p['bomdes']) + ',bomwjdes=' + str(p['bomwjdes']) + ',bomstddes=' + str(
                        p['bomstddes']) + ',childbom=' + str(p['childbom']) + '\n'
                     + 'myclass=' + str(p['myclass']) + ',nodename=' + str(p['nodename']) + ',linecalc=' + str(
                        p['linecalc']) + ',bomstd=' + str(p['bomstd']) + '\n'
                     + 'bg=' + str(p['bg']) + ',direct=' + str(p['direct']) + ',lgflag=' + str(
                        p['lgflag']) + ',num=' + str(p['num']) + '\n'
                     + 'lfb=' + str(p['lfb']) + ',llk=' + str(p['llk']) + ',wfb=' + str(p['wfb']) + ',wlk=' + str(
                        p['wlk']) + '\n'
                     + 'llfb=' + str(p['llfb']) + ',rrfb=' + str(p['rrfb']) + ',ddfb=' + str(
                        p['ddfb']) + ',uufb=' + str(
                        p['uufb']) + '\n'
                     + 'fb=' + str(p['fb']) + 'holestr=' + str(p['holestr']) + ',kcstr=' + str(
                        p['kcstr']) + ',memo=' + str(p['memo']) + ',gno=' + str(p['gno']) + '\n'
                     + 'gdes=' + str(p['gdes']) + ',gcb=' + str(p['gcb']) + ',extra=' + str(
                        p['extra']) + ',fbstr=' + str(p['fbstr']) + '\n'
                     + 'subspace=' + str(p['subspace']) + ',process=' + str(p['process']) + ',ls=' + str(
                        p['ls']) + ',myunit=' + str(p['myunit']) + '\n'
                     + 'bomtype=' + str(p['bomtype']) + ',bdxmlid=' + str(p['bdxmlid']) + ',user_fbstr=' + str(
                        p['user_fbstr']) + ',bl=' + str(p['bl']) + '\n'
                     + 'bp=' + str(p['bp']) + ',bh=' + str(
                        p['bh']) + ',var_names=' + var_names + ',var_args=' + var_args + ',value_lsk=' + str(
                        p['value_lsk']) + ',value_rsk=' + str(p['value_rsk']) + '\n'
                     + 'value_zk=' + str(p['value_zk']) + ',value_zs=' + str(p['value_zs']) + ',value_ls=' + str(
                        p['value_ls']) + ',value_lg=' + str(p['value_lg']) + '\n'
                     + 'value_ltm=' + str(p['value_ltm']) + ',value_rtm=' + str(p['value_rtm']) + ',a_hole_info=' + str(
                        p['a_hole_info']) + ',b_hole_info=' + str(p['b_hole_info']) + '\n'
                     + 'holeinfo=' + str(p['holeinfo']) + ',isoutput=' + str(p['isoutput']) + ',is_outline=' + str(
                        p['is_outline']) + ',outputtype=' + str(p['outputtype']) + '\n' + 'holeconfig_flag=' + str(
                        p['holeconfig_flag']) + ',kcconig_flag=' + str(p['kcconig_flag']) + ',bg_data=' + str(
                        p['bg_data']) + ',mBGParam=' + str(p['mBGParam']) + '\n'
                     # + 'bg_filename=' + str(p['bg_filename']) + ',mpr_filename=' + str(p['mpr_filename']) + ',bpp_filename=' + str(p['bpp_filename']) + ',devcode=' + str(p['devcode']) + '\n'
                     # + 'zero_y=' + str(p['zero_y']) + ',direct_calctype=' + str(p['direct_calctype']) + ',youge_holecalc=' + str(p['youge_holecalc']) + ',is_output_bgdata=' + str(p['is_output_bgdata']) + '\n'
                     # + 'is_output_mpr=' + str(p['is_output_mpr']) + ',is_output_bpp=' + str(p['is_output_bpp']) + '\n'
                     + 'bg_l_minx=' + str(p['bg_l_minx']) + '\n' + ',bg_l_maxx=' + str(p['bg_l_maxx']) + '\n'
                     + 'bg_l_minx=' + str(p['bg_l_miny']) + '\n' + ',bg_l_maxy=' + str(p['bg_l_maxy']) + '\n'
                     + 'bg_d_minx=' + str(p['bg_d_minx']) + '\n' + ',bg_d_maxx=' + str(p['bg_d_maxx']) + '\n'
                     + 'bg_d_miny=' + str(p['bg_d_miny']) + '\n' + ',bg_d_maxy=' + str(p['bg_d_maxy']) + '\n'
                     + 'bg_b_minx=' + str(p['bg_b_minx']) + '\n' + ',bg_b_maxx=' + str(p['bg_b_maxx']) + '\n'
                     + 'bg_b_miny=' + str(p['bg_b_miny']) + '\n' + ',bg_b_maxy=' + str(p['bg_b_maxy']) + '\n'
                     + 'bg_r_minx=' + str(p['bg_r_minx']) + '\n' + ',bg_r_maxx=' + str(p['bg_r_maxx']) + '\n'
                     + 'bg_r_miny=' + str(p['bg_r_miny']) + '\n' + ',bg_l_maxy=' + str(p['bg_r_maxy']) + '\n'
                     + 'bg_u_minx=' + str(p['bg_u_minx']) + '\n' + ',bg_u_maxx=' + str(p['bg_u_maxx']) + '\n'
                     + 'bg_u_miny=' + str(p['bg_u_miny']) + '\n' + ',bg_u_maxy=' + str(p['bg_u_maxy']) + '\n'
                     + 'bg_f_minx=' + str(p['bg_f_minx']) + '\n' + ',bg_f_maxx=' + str(p['bg_f_maxx']) + '\n'
                     + 'bg_f_miny=' + str(p['bg_f_miny']) + '\n' + ',bg_f_maxy=' + str(p['bg_f_maxy']) + '\n'
                     + 'lfb=' + str(p['lfb']) + ',llk=' + str(p['llk']) + ',wfb=' + str(p['wfb']) + ',wlk=' + str(
                        p['wlk'])
                     + '\n' + 'lx=' + str(p['lx']) + ',ly=' + str(p['ly']) + ',lz=' + str(p['lz'])
                     + '\n' + 'x=' + str(p['x']) + ',y=' + str(p['y']) + ',z=' + str(p['z'])
                     + '\n' + 'bg=' + p['bg'] + ',var_args=' + var_args + 'zero_y=' + str(p['zero_y']) + 'desc=' + p[
                         'desc']
                     + '\n' + 'classseq=' + str(p['classseq']) + ',seq=' + str(p['seq'])
                     + '\n' + 'is_calc_holeconfig=' + is_calc_holeconfig
                     + '\n' + ',ahole=' + ahole + '\n' + ',bhole=' + bhole + '\n' + ',akc=' + akc + '\n' + ',bkc=' + bkc).encode(
                'gbk'))  # +'bg
def TestXmltoJson(xml, GetNetworkQuoteConfigHandl, Path):
    global RootPath
    RootPath = Path
    #InitRootPathConfig(Path)  # 初始化根目录配置文件夹数据
    mProductList, bomlist, Desdoorlist, Desslidinglist, mBDXMLList, JsonPrice, productdatadict, \
    workflowlist, mIIHoleCalcRule, mBDXMLList, gBGHash = LoadXML2Bom(xml, Path)
    log.info('len of bomlist=' + str(len(bomlist)))
    log.info('len of mProductList='+ str(len(mProductList)))
    log.info('len of Desdoorlist='+str(len(Desdoorlist)))
    log.info('len of Desslidinglist='+str(len(Desslidinglist)))
    log.info('len of mBDXMLList='+str(len(mBDXMLList)))
    # BomObjPath = base_dir + '\\Python\\bomobj.json'
    # basewjlistObjPath = base_dir + '\\Python\\basewjlist.json'
    # QuoConPath = base_dir + '\\Python\\QuoCon.json'
    # with open(BomObjPath, 'w+') as f:
    #      f.write(json.dumps(JsonPrice, ensure_ascii=False).encode('gbk'))
    InitBgMinAndMax(bomlist)
    CalcLgFlag(bomlist)
    basewjlist = CalcBomWj()
    mHPInfoList, mKCInfoList = CalcHoleAndKc(mProductList, bomlist, workflowlist, mIIHoleCalcRule, mBDXMLList, gBGHash)
    # print 'len of mHPInfoList',len(mHPInfoList)
    # print 'len of mKCInfoList',len(mKCInfoList)
    log.info('len of basewjlist1='+str(len(basewjlist)))
    # print json.dumps(basewjlist,ensure_ascii=False).encode('gbk')
    CalcHoleWj(bomlist, basewjlist, mHPInfoList, workflowlist, gBGHash, mKCInfoList)
    log.info('len of basewjlist2=' + str(len(basewjlist)))
    # print 'len of basewjlist2', len(basewjlist)
    # with open(basewjlistObjPath, 'w+') as f:
    #     f.write(json.dumps(basewjlist, ensure_ascii=False).encode('gbk'))
    desclist = []
    JsonPriceAddWujin(JsonPrice, basewjlist, desclist)
    #FindProperPriceRecord(bomQuolist)
    priceconfig = GetNetworkQuoteConfigHandl(desclist, Desslidinglist, Desdoorlist)
    writetofile(bomlist, 'bomlistdata')
    writetofile(basewjlist, 'wjlistdata')
    print(json.dumps(JsonPrice,encoding='utf8', ensure_ascii=False).encode('UTF8'))
    JsonPrice.update(priceconfig)
    return mProductList,bomlist,Desslidinglist,mXMLStringList,mDoorList,Desdoorlist,JsonPrice,basewjlist,desclist
def genLogDict(logDir, logFile, level ='INFO'):
    '''
    配置日志格式的字典
    '''
    logDict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
            },
            'standard': {
                'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            "default": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": os.path.join(logDir, logFile),
                'mode': 'w+',
                "maxBytes": 1024*1024*5,  # 5 MB
                "backupCount": 20,
            },
        },
        # "loggers": {
        #     "app_name": {
        #         "level": "INFO",
        #         "handlers": ["console"],
        #         "propagate": "no"
        #     }
        # },
        "root": {
            'handlers': ['default'],
            'level': level,
            'propagate': False
        }
    }
    return logDict
def initLogConf(level):
    """
    配置日志
    """
    baseDir = os.path.dirname(os.path.abspath(__file__))
    logDir = os.path.join(baseDir, "Log")
    if not os.path.exists(logDir):
        os.makedirs(logDir)  # 创建路径
    logFile = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
    logDict = genLogDict(logDir, logFile, level)
    logging.config.dictConfig(logDict)
if __name__ == '__main__':
    import logging.config
    import datetime
    initLogConf('INFO')
    log = logging.getLogger(__file__)
    sys.path.append(base_dir+'\\Python\\NetPriceConfig')
    import NetworkQuoteConfigData
    xmlguid = '55faeb80e99211e9ad1db0fc36268ae0'
    xmlfile = base_dir+'\\Python\\postxml\\#order_scene0_spaceB02FE0A39E6B1A504AD1BAC24A52CB55'
    if (not os.path.exists(base_dir+'\\Python\\postxml\\')):
        os.makedirs(base_dir+'\\Python\\postxml\\')
    # with open(base_dir+'\\Python\\postxml\\1.xml','w+') as f:
    #     f.write(xml)
    # base_dir = os.path.abspath(os.path.join(os.getcwd()))
    # with open(base_dir+u'\\data\\qddata\\孔位五金.cfg'.encode('gbk'),'r') as f:
    #     HoleWjFContent = f.read()
    # #HoleWjF = io.open(HoleWjFile, encoding='GB2312')
    # #HoleWjFContent = HoleWjF.read()
    # HoleWjFContent = json.loads(HoleWjFContent, encoding='gbk')
    # print HoleWjFContent
    mProductList,bomlist,Desslidinglist,mXMLStringList,mDoorList,Desdoorlist,JsonPrice,basewjlist,desclist  = TestXmltoJson(xmlfile,NetworkQuoteConfigData.GetNetworkQuoteConfigHandl,base_dir)
    '''
        LoadXMLFile2Quo 不需要 mBDXMLList
    '''
    print('len of mProductList=', len(mProductList))
    print('len of bomlist=', len(bomlist))
    print('len of basewjlist=', len(basewjlist))
    print('len of desclist=', len(desclist))
    print('len of Desslidinglist=', len(Desslidinglist))
    print('len of Desdoorlist=', len(Desdoorlist)) #服务器缺少报价配置数据
    print('len of mXMLStringList=', len(mXMLStringList))
    print(json.dumps(Desdoorlist,ensure_ascii=False))
    print('len of doorslist=', len(doorslist))
    with open(base_dir.decode('gbk')+'\\Python\\PythontoBomJson\\PriceJson\\'+xmlguid + '.txt', 'w+') as f:
        f.write(json.dumps(JsonPrice,encoding='utf8', ensure_ascii=False).encode('utf8'))
#functionxmltojson(xmlfile)
#Data = {}
# Data['Order'] =orderdict
# Data['bomlist'] = bomlist
# Data['basewjlist'] = basewjlist
# with open('bomlist.json', 'w') as f:
#     f.write(json.dumps(Data,ensure_ascii=False).encode('gbk'))
# print 'len of basewjlist2', len(basewjlist)
# print 'len of bomlist', len(bomlist)
# # #// 左右翻板，需要进行AB面反转
# TranAB(bomlist,mHPInfoList, gBGHash)
# #
# for i in range(0, len(bomlist)):
#     p = bomlist[i]
#     # if (p['outputtype'] == u'报价') or (p['outputtype'] == u'无'):
#     #     p['isoutput'] = False
#     if (p['outputtype'] == u'报价物料'):
#         p['isoutput'] = True
#     if p['desc'] == '':
#         p['isoutput'] = False
#     if 'childbom' not in p or p['childbom'] == '':
#         continue
#     product_item = mProductList[p['cid']]
#     childnum = LoadChildBom(p, p['cid'], product_item['bh'], p['childbom'], bomlist, p['id'],
#                             p['l'], p['p'], p['h'], p['mat'], p['color'], p['memo'],
#                             p['gno'], p['gdes'], p['gcb'], p['myclass'], p['bomstd'], p['num'])
#     if childnum > 0:
#         p['isoutput'] = False
# CalcLineCombine(bomlist, mProductList)
# CalcSeq(bomlist)
# CalcIsTHole(bomlist,mIIHoleCalcRule,mHPInfoList,gBoardMatList)
# allBomList, bjBomList, wjBomList, xcwjBomList, allBomList2, bjBomList2, wjBomList2, xcwjBomList2,Data = UpdateBomList(bomlist, basewjlist, gROC, mHPInfoList)