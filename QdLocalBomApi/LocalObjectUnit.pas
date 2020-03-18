unit LocalObjectUnit;

interface

uses Windows, Messages, SysUtils, superobject, IniFiles, MyUtils, MD5, Classes,
XMLIntf, QdXML, CalcHoleUnit, Lua, StrUtils, HTTPApp, ExpressUnit, XYZCalcPrice,
XMLDoc, MyXMLDocument, LuaLib, LuaObjUnit , ADODB, NPPlugin, Dialogs, VectorTypes,
PaxProgram, PaxCompiler,PaxRegister, PaxJavaScriptLanguage, XMLProgromFuncUnit,
VectorGeometry, IdHTTP, GDIPAPI, Contnrs, FMTBcd, QdSystem, math, ACTIVEX;

type
  TProductItem = class
    name, gno, des, gcb, color, mat, Extra: string;
    id, l, d, h, bh: Integer;
  end;

  TDoorItem = class
    xml, name, gno, des, gcb, extra, doortype, hingehole, doormemo, doorextra: string;
    l, d, h: Real;
    one_l, one_h: Real;
    num, xmlindex, slino, isframe, userdata: Integer;
  end;

type
  BomParam = record
    productid, cid, boardheight: Integer;
    blist: TList;
    xml: string;
    gno, gdes, gcb, extra, pname, subspace, sozflag, textureclass, pmat, pcolor, group: string[250];
    pid, pl, pd, ph: Integer;
    px, py, pz, space_x, space_y, space_z, space_id: Integer;
    outputtype: string;
    blockmemo, number_text:string;
    num,mark: Integer;
    rootnode:IXMLNode;
    xdoc:IXMLDocument;
    qdrootnode:IQdXMLNode;
    qdxdoc:IQdXMLDocument;
    parent:Pointer;
  end;
type
  PBomParam = ^BomParam;

type
  QuoParam = record
    productid, cid, boardheight: Integer;
    blist: TList;
    xml: string;
    gno, gdes, gcb, extra, pname, subspace, textureclass, pmat, pcolor, group: string[250];
    pid, pl, pd, ph: Integer;
    outputtype, pricecalctype: string[128];
    blockmemo, number_text: string;
    rootnode:IXMLNode;
    xdoc:IXMLDocument;
    num, mark: Integer;
  end;
type
  PQuoParam = ^QuoParam;

type
  BomOrderItem = record
    cid, id, pid, seq, classseq, mark, vp: Integer;
    code, name, mat, mat2, mat3, color, workflow: string;
    pl, pd, ph, space_x, space_y, space_z, space_id, gcl, gcd, gch, gcl2, gcd2, gch2: Integer;  //gcl, gcd, gch图形成品修正值
    tmp_soz: string;
    lx, ly, lz, x, y, z, l, p, h, gl, gp, gh, holeflag, linemax, holetype: Integer;
    ox, oy, oz: Real;
    childnum: Integer;
    desc, bomdes, bomwjdes, bomstddes, childbom, myclass, nodename, linecalc, bomstd, bg: string;
    direct, lgflag, holeid, kcid: Integer;
    num: Integer;
    lfb, llk, wfb, wlk, llfb, rrfb, ddfb, uufb, fb: double;
    holestr, kcstr: string;
    memo, gno, gdes, gcb, extra, fbstr, subspace, process, ls, myunit, bomtype, bdxmlid, user_fbstr: string;
    bl, bp, bh: double;                 //物料尺寸
    var_names: array[0..15] of string;
    var_args: array[0..15] of Integer;
    //$左收口宽度， $右收口宽度， $柱切角宽度， $柱切角深度， $梁切角深度， $梁切角高度， $左侧趟门位， $右侧趟门位
    value_lsk, value_rsk, value_zk, value_zs, value_ls, value_lg, value_ltm, value_rtm: Integer;
    a_hole_info, b_hole_info, holeinfo: string;
    isoutput, is_outline: boolean;
    outputtype: string;
    holeconfig_flag, kcconig_flag: string;
    bg_data: string;
    mBGParam:string;

    bg_filename, mpr_filename, bpp_filename, devcode: string;
    zero_y, direct_calctype, youge_holecalc: Integer; //zero_y封边靠档
    is_output_bgdata, is_output_mpr, is_output_bpp: Integer;

    //基础图形描述
    bg_l_minx, bg_l_maxx, bg_r_minx, bg_r_maxx, bg_l_miny, bg_l_maxy, bg_r_miny, bg_r_maxy: Integer;
    bg_d_minx, bg_d_maxx, bg_u_minx, bg_u_maxx, bg_d_miny, bg_d_maxy, bg_u_miny, bg_u_maxy: Integer;
    bg_b_minx, bg_b_maxx, bg_f_minx, bg_f_maxx, bg_b_miny, bg_b_maxy, bg_f_miny, bg_f_maxy: Integer;

    hole_back_cap, hole_2_dist: Integer; //第一个孔靠背的距离，两孔间距

    trans_ab: boolean;                  //AB面反转
    ahole_index: array[0..100] of Integer;
    bhole_index: array[0..100] of Integer;

    akc_index: array[0..100] of Integer;
    bkc_index: array[0..100] of Integer;

    is_calc_holeconfig: array[0..5] of Integer;

    parent:Pointer;
    basewj_price: Real;
    extend, group:string;
    packno: string;
    userdata: Pointer;
    userdefine: string;                 //XML自定义数据
    ////// ERP数据
    erpunit: string;
    erpmatcode, blockmemo, number_text: string;
  end;
type
  PBomOrderItem = ^BomOrderItem;

type
  SlidingBomRecord = record
    cid, id, pid, seq, num, mark, doornum, slino, xmlindex, isglass, is_buy, door_index, space_id: Integer;
    name: string;
    l, p, h, sliw, slih, doorw, doorh: Real;
    code, mat, mat2, mat3, color, direct, gno, gdes, gcb, extra, group, bomtype, memo, memo2, memo3, subspace, fbstr, doorname, myunit, dtype, bdfile, bdxmlid: string;
    doormemo: string;
    extend:string;
    ////// ERP数据
    erpunit: string;
    erpmatcode, blockmemo, number_text: string;
  end;
type
  PSlidingBomRecord = ^SlidingBomRecord;

  /////////////////////////////////////////////////////

type
  BomRuleRec = record
    id, bh: Integer;
    myclass1, myclass2, mat: string[48];
    lfb, llk, wfb, wlk: Real;
    holestr, kcstr: string[48];
    memo, fbstr: string[128];
    is_outline: Integer;
    llfb, rrfb, uufb, ddfb, fb: double;
    deleted: boolean;
  end;
type
  PBomRuleRec = ^BomRuleRec;

type
  Bom2RuleRec = record
    id, lmax, lmin, dmax, dmin, hmax, hmin: Integer;
    bclass: string[32];
    pname, name, l, p, h, mat, color: string[48];
    lfb, llk, wfb, wlk: Real;
    q: Integer;
    holestr, kcstr: string[48];
    ono, bomstd, bomtype, a_face, b_face: string[48];
    memo, fbstr: string[128];
    bg_filename, mpr_filename, bpp_filename, devcode, workflow: string[128];
    direct_calctype, youge_holecalc: Integer;
    llfb, rrfb, uufb, ddfb, fb: double;
    deleted: boolean;
  end;
type
  PBom2RuleRec = ^Bom2RuleRec;

type
  WJRuleRec = record
    myclass1, myclass2: string[48];
    lmin, lmax, pmin, pmax, hmin, hmax, lgflag: Integer;
    wjname, wjno, myunit, myunit2, mat, color: string[48];
    wjid, num: Integer;
    price: Real;
  end;
type
  PWJRuleRec = ^WJRuleRec;

type
  linecalc = record
    name: string[48];
    linemax: Integer;
  end;
type
  PLineCalc = ^linecalc;

type
  bomstd = record
    myclass1, myclass2, stdflag: string[48];
    lmin, lmax, dmin, dmax, hmin, hmax, level: Integer;
  end;
type
  PBomStd = ^bomstd;

type
  workflow = record
    name, bomstd, hole: string;
    id, board_cut, edge_banding, punching: Integer;
  end;
type
  PWorkflow = ^workflow;

type
  HoleWjItem = packed record
    id, holetype, num: Integer;
    hole, bcolor, wjname, mat, color, wjno: string;
    price: Real;
  end;
type
  PHoleWjItem = ^HoleWjItem;

type
  StrMap = packed record
    s1, s2, s3, no, oname, childbom, linecalc, HoleConfig, bomstd, bomtype, KCConfig: string[48];
    priceclass, bomclass: string[48];
    bg_filename, mpr_filename, bpp_filename, devcode, workflow: string[128];
    zero_y, direct_calctype, youge_holecalc: Integer;
    is_output_bgdata, is_output_mpr, is_output_bpp: Integer;
    direct: Integer;
  end;

type
  ReportOutputConfig = packed record
    bj_out_classname, bj_out_myclass, bj_out_name, bj_out_mat, bj_out_color: boolean;
    bj_out_size, bj_out_price, wl_out_classname, wl_out_myclass, wl_out_name: boolean;
    wl_out_mat, wl_out_color, wl_out_size, wl_out_kc, wl_out_fb, wl_out_memo, wl_out_hole: boolean;
  end;

type
  BoardMat = packed record
    id: Integer;
    name, color, alias, alias2, alias3: string[48];
    bh: Integer;
  end;
type
  PBoardMat = ^BoardMat;
//孔位五金
type
  HoleWjCfg = record
    holetype, bh, c, holenum, wjnum:Integer;
    hole, color, wjname, wjmat, wjcolor, wjcode:string;
end;
PHoleWjCfg = ^HoleWjCfg;

  /////////////////报价
type
  QuoOrderItem = record
    colNo: string;
    colName: string;
    colType: string;
    colL: Integer;
    colP: Integer;
    colH: Integer;
    colClass: string;
    colGT: string;
    colS: Real;
    colQ: Integer;
    colUnit: string;
    colMat, colMat2, colMat3: string;
    colClr: string;
    colJXPrice1: Real;
    colJXPrice2: Real;
    colJXPrice3: Real;
    colLSPrice1: Real;
    colLSPrice2: Real;
    colLSPrice3: Real;
    cost: Real;

    mytype: Integer;
    msg: string;
    id, seq, classseq, mark: Integer;
    priceid: Integer;
    myclass, gno, subspace, sale_type, pricetype, erpunit, erpmatcode: string;
    blockmemo, number_text, doorstyle, doormat, doorcolor: string;
  end;
type
  PQuoOrderItem = ^QuoOrderItem;

  //////////////诗尼曼ERP
type
  ErpMat = record
    id: Integer;
    name, mat, color: string[64];
    h: Integer;
    myclass, flag, myunit: string[48];
    deleted: boolean;
  end;
  PErpMat = ^ErpMat;

type
  TPluginEvent = procedure(Sender: TObject; value: Pointer) of object;

type
  PluginsDll = record
    name, dll: string;
    tickcount:Integer;
    handle: THandle;
    InitDll: procedure(p, adata: Pointer); stdcall;
    UninitDll: procedure; stdcall;
    ExportBomBoardData: function(ordername, gno, exportdir: pchar; templatename, excelname, datadir: pchar): Integer; stdcall;
    ExportBomWJData: function(ordername, gno, exportdir: pchar; templatename, excelname, datadir: pchar): Integer; stdcall;
    ExportBomDoorsData: function(ordername, gno, exportdir: pchar; templatename, excelname, datadir: pchar): Integer; stdcall;
    ExportBomData: function(ordername, gno, exportdir: pchar; templatename, excelname, datadir: pchar): Integer; stdcall;
    ExportPriceData: function(ordername, gno, exportdir: pchar; templatename, excelname, datadir: pchar): Integer; stdcall;
    ExportQuotaionData: function(ordername, gno, exportdir: pchar; templatename, excelname, datadir: pchar): Integer; stdcall;
    ExportAllData: function(ordername, gno, exportdir: pchar; templatename, excelname, datadir: pchar): Integer; stdcall;
    SetCallbackFunc: procedure(name: pchar; func, data: Pointer); stdcall;
    ExcelReportGetValue: function(ptype: pchar; p: Pointer; bh: Integer; DatasetName, ParName: pchar; ParValue: pchar): Integer; stdcall;
    ReportEnd: procedure(ret: Integer; report, filename: pchar); stdcall;
    IsSameItem: function(ptype: pchar; p1, p2: Pointer): Integer; stdcall;
    ProcessMultiReport: function(xml: pchar): Integer; stdcall;
  end;
type
  PPluginsDll = ^PluginsDll;

type
  MRItem = record                       //多报表
    template, mytype, prefix, suffix, path, srcdll: string;
    combine, visible, filter_kl, filter_fb, filter_hole: Integer;
  end;
type
  PMRItem = ^MRItem;

// 趟门 单门数量类型对象
type
  SlidingExp = record
    id, doornum, overlapnum: Integer;
    deleted: boolean;
    lkvalue: single;
    name : string;
    noexp :boolean;
  end;
type
  PSlidingExp = ^SlidingExp;

  // 趟门 门类型
type
  SlidingType = record
  id: Integer;
  deleted: boolean;
  name: string;
  end;
type
  PSlidingType = ^SlidingType;

// 趟门  趟门参数
type
  SlidingParam = record
    id: Integer;
    deleted: boolean;
    name, myclass, vboxtype, wjname:string;
    track, udbox, hbox : string;
    zndlun, memo, ddlun, diaolun, gddwlun, hddwlun, ls:string;  //groupname 换memo
    overlap, ddlw, fztlen, glassvalue1, glassvalue2 :single;       //ddlw 换 ddlpos    fztlen 换fztkd
    vboxjtw, uboxjtw, dboxjtw, hboxjtw, cpm_lmax, cpm_hmax: single;
    hboxvalue: single;
    laminating, is_xq: boolean;
  end;
type
  PSlidingParam = ^SlidingParam;

//趟门 上下横框参数
type
  UDBoxParam = record
    id  : Integer;
    deleted: boolean;
    name, wlupcode, wldncode, upname, dnname, wjname1 : string;
    ubheight, ubdepth, ubthick, dbheight, dbdepth, dbthick, uphole, downhole, upsize, downsize: single;
    wjname2, upmodel, dnmodel, upmemo, dnmemo, dnbdfile :string;
    upbdfile, frametype: string
  end;
type
  PUDBoxParam = ^UDBoxParam;

// 趟门 上下轨参数
type
  TrackParam = record
    id: Integer;
    deleted: boolean;
    height, depth, lkvalue1, lkvalue2, upsize, downsize :single;
    name, frametype, wlupcode,wldncode, upname,dnname, wjname1 : string;
    upmodel, upmemo, upbdfile  : string;
    wjname2, dnmodel, dnmemo, dnbdfile : string;
  end;
type
  PTrackParam = ^TrackParam;


// 趟门 中横框参数
type
  HBoxParam = record
    id, ishboxvalue, holenum : Integer;
    deleted: boolean;
    height, depth, thick, hole, holecap, size, holepos : single;      //holepos 为横中横，竖中横新加属性
    name, wlcode, bjcode, wjname, model, memo : string;
    bdfile, frametype: string;
  end;
type
  PHBoxParam = ^HBoxParam;

// 趟门  竖框参数
type
  VBoxParam = record
    id : Integer;
    deleted: boolean;
    height, depth, thick, panelvalue, udboxvalue, vboxvalue, size : single;
    name, wlcode, wjname, model, memo, bdfile: string;
  end;
type
  PVBoxParam = ^VBoxParam;

type
  PanelType = record
    id: Integer;
    deleted: boolean;
    name, wjname: string;
    jtvalue: single;
    isglass, isbaiye, iswhole: boolean;
    bktype, direct, pnl2d, slave, slave2, mk3d, memo, memo2, memo3, bdfile: string;
    lmin, lmax, wmax, wmin, mkl, mkh, thick: Integer;
  end;
type
  PPanelType = ^PanelType;

type
  Accessory = record
    id: Integer;
    deleted: boolean;
    name, myunit, wlcode, myclass, color, memo, memo2, memo3, bdfile: string;
    isglass, isbaiye, isuserselect: boolean;
  end;
type
  PAccessory = ^Accessory;
    
type
  SlidingColor = record
    id: Integer;
    deleted: boolean;
    name, myclass, code: string;
  end;
type
  PSlidingColor = ^SlidingColor;

type
  SlidingColorClass = record
    id: Integer;
    deleted: boolean;
    color, myclass, mat, color2, wlcode, bjcode, color3, color4: string;
    skcolor1, skcolor2, skcolor3, skcolor4:string;
  end;
type
  PSlidingColorClass = ^SlidingColorClass;

type
  SlidingColorClass2 = record
    id: Integer;
    deleted: boolean;
    bktype, color: string;
  end;
type
  PSlidingColorClass2 = ^SlidingColorClass2;

type
  SlidingShutterExp = record
    id: Integer;
    deleted: boolean;
    PanelType: string;
    height, width, heightcap, widthcap, minheight, minwidth, size: single;
  end;
type
  PSlidingShutterExp = ^SlidingShutterExp;

type
  SlidingMyClassGroup = record
    deleted: boolean;
    id, gid: Integer;
    name: string;
  end;

type
  SlidingWjBom = record
    deleted: boolean;
    id: Integer;
    name: string;
  end;
type
  PSlidingWjBom = ^SlidingWjBom;

type
  SlidingWjBomDetail = record
    deleted: boolean;
    id: Integer;
    bomname, name, l, d, num, bdfile: string;
  end;
type
  PSlidingWjBomDetail = ^SlidingWjBomDetail;

type SlidingPanelBom = record
  deleted: boolean;
  id: Integer;
  name:string;
end;
type PSlidingPanelBom = ^SlidingPanelBom;

type SlidingPanelBomDetail = record
  deleted:boolean;
  id:Integer;
  bomclass, bomname, l, w, h, mat, color, bomtype, memo, memo2, memo3, bdfile:string;
  lmin, lmax, hmin, hmax, num:Integer;
end;
type PSlidingPanelBomDetail = ^SlidingPanelBomDetail;

//自选配件
type
  OptionalAcc = record
    name :string;
    num: Integer;
  end;
type
  POptionalAcc = ^OptionalAcc;

//门转换表
type
  CfgTable = record
    name, bomname, frametype, munit: string;
    modle : Integer;
end;
type PCfgTable = ^CfgTable;

//趟门2横分格
type
  SlidingHfg2 = record
    id : Integer;
    fgtype, spszh, spmk, varlist, mxlist, image : string;
end;
type PSlidingHfg2 = ^SlidingHfg2;

{//趟门3横分格
type
  SlidingHfg3 = record
    id : Integer;
    fgtype, spszh, varlist, mxlist, image : string;
end;
type PSlidingHfg3 = ^SlidingHfg3;

//趟门4横分格
type
  SlidingHfg4 = record
    id : Integer;
    fgtype, spszh, varlist, mxlist, image : string;
end;
type PSlidingHfg4 = ^SlidingHfg4;

//趟门2竖分格
type
  SlidingSfg2 = record
    id : Integer;
    fgtype, spszh, spmk, varlist, mxlist, image : string;
end;
type PSlidingSfg2 = ^SlidingSfg2;

//趟门3竖分格
type
  SlidingSfg3 = record
    id : Integer;
    fgtype, spszh, spmk, varlist, mxlist, image : string;
end;
type PSlidingSfg3 = ^SlidingSfg3;

//趟门4竖分格
type
  SlidingSfg4 = record
    id : Integer;
    fgtype, spszh, spmk, varlist, mxlist, image : string;
end;
type PSlidingSfg4 = ^SlidingSfg4;}

type
  wldata = record
    ono, gno, hno, code, name, color, direct, myunit, memo, doorname, memo2, memo3, bdfile, detail: string;
    num, group, door_index, pnl_num, pnl_index: Integer;
    isglass: Integer;
    fzl: Real;
    l, w, h, l0, w0, l1, w1, l2, w2, hh1, ww1, bomsize: single;
  end;
type Pwldata = ^wldata;

//掩门
type
  doorwldata = record
    doorname, ono, gno, hno, code, name, color, direct, myunit, bomtype, fbstr, bdfile: string[128];
    memo, memo2, memo3, doormemo:string;
    num, group, door_index, pnl_num, pnl_index: Integer;
    isglass, is_buy: Integer;
    faceA, faceB, detail:string;  //json 格式的AB面孔
    l, w, h, l0, w0, l1, w1, l2, w2, hh1, ww1: double;
  end;
type Pdoorwldata = ^doorwldata;

type
  RectBox = record                      //过桥
    vh, selected: boolean;
    w0, h0, x0, y0, d0: single;         //可视
    w1, h1, x1, y1, d1: single;         //物料
    w2, h2, x2, y2, d2: single;         //投影
    boxtype, color: string;
  end;
type
  PRectBox = ^RectBox;

type
  RectPanel = record                    //面板
    selected: boolean;
    w0, h0, x0, y0, d0: single;         //可视
    w1, h1, x1, y1, d1: single;         //物料
    w2, h2, x2, y2, d2: single;         //投影
    PanelType, color, direct, memo, pricetype, color2, extradata: string;
    price, price2:single;
  end;
type
  PRectPanel = ^RectPanel;

type
  TDoorRect = class(TObject)
  public
    doorw, doorh, x0, y0, doorw2, doorh2: single;
    selected: boolean;
    mUDBoxParam: UDBoxParam;
    mVBoxParam: VBoxParam;
    mPanelType, mPanelColor: string;
    mVBoxColor: string;
    boxlist: TList;
    panellist: TList;
    mYPos: Integer;
    constructor Create();
    destructor Destroy; override;
    procedure ClearBoxList;
    procedure ClearPanelList;
    procedure CreateHBoxAndPanel(boxtype, boxcolor, pnltype, pnlcolor: string; num: Integer; h, d, thick: single;
      hh: array of single; pnls1, pnls2, di, memo: array of string);
    function SelectPanelByPos(x0, y0: single; multisel: boolean): PRectPanel;
    function SelectRectBoxByPos(x0, y0: single): PRectBox;
    function GetSelectedPanel: PRectPanel;
    procedure GetNearestRectBox(panel: PRectPanel; var boxup, boxdown: PRectBox);
    procedure CopyFromDoor(door: TDoorRect);
    function GetPanelPosInDoor(p: PRectPanel): Integer;
    function GetNearestUpPanel(p: PRectPanel): PRectPanel; overload;
    function GetNearestDownPanel(p: PRectPanel): PRectPanel; overload;
    function GetNearestUpPanel(p: PRectBox): PRectPanel; overload;
    function GetNearestDownPanel(p: PRectBox): PRectPanel; overload;
    function GetNearestUpBox(p: PRectPanel): PRectBox;
    function GetNearestDownBox(p: PRectPanel): PRectBox;
    procedure AddHBoxToPanel(pnl: PRectPanel; hbox: PHBoxParam; x0, y0: single; boxcolor: string);
    procedure UnselecetAllPanels;
  end;

//掩门
type
  DoorsColor = record
    id: Integer;
    deleted: boolean;
    name: string;
  end;
type
  PDoorsColor = ^DoorsColor;

type
  DoorsExp = record
    id: Integer;
    deleted: boolean;
    name: string;
    doornum, capnum: Integer;
    lkvalue: single;
  end;
type
  PDoorsExp = ^DoorsExp;

type
  DoorsType = record
    id: Integer;
    deleted: boolean;
    name, hinge, myclass, hinge1, hinge2: string;
    isframe: boolean;
    covertype: Integer;
    lkvalue, depth, eb_lkvalue, eb_ud_lkvalue: Real;
    color, defcolor, defdoorframe : string;
  end;
type
  PDoorsType = ^DoorsType;

type
  DoorsParam = record                   //掩门参数
    id: Integer;
    deleted: boolean;
    name, DoorsType, handle, wjname, hboxname, paneltype: string;
    cap, eb_cap: Real;
    vboxname, udboxname: string;
    vboxl, udboxl: string;
    vboxh, udboxh, vthick, udthick: Real;
    vboxjtw, udboxjtw, hboxjtw, udbox_hbox_value: Real;
    d3name, hbox3d, ubox3d, dbox3d: string;
    cpm_lmax, cpm_hmax: single;
    vdirect, vfbstr, uddirect, udfbstr, vmemo, udmemo, fbstr:string;
    iscalc_framebom, is_xq, cb_yyvalue, is_buy:Integer;
    frame_valuel, frame_valueh:single;
    bomtype, left_doorxml, right_doorxml, doorxml: string;
    bdfile, l_bdfile, r_bdfile, u_bdfile, d_bdfile:string;
    noframe_bom:Integer;
  end;
type
  PDoorsParam = ^DoorsParam;

type
  DoorsHandle = record
    id: Integer;
    deleted: boolean;
    name, wjname, xpos, ypos, width, height, depth, depthpos, bomtype, memo, holescript: string;
  end;
type
  PDoorsHandle = ^DoorsHandle;
//门铰分类
type
  DoorsHinge = record
    id: Integer;
    deleted: boolean;
    name, mytype, wjname, bomtype, memo, alias: string;
    min1, max1, num1: Integer;
    min2, max2, num2: Integer;
    min3, max3, num3: Integer;
    min4, max4, num4: Integer;
    min5, max5, num5: Integer;
    iszn, bh:Integer;
  end;
type
  PDoorsHinge = ^DoorsHinge;

//门铰
type
  DoorsCurHinge = record
    id: Integer;
    deleted: boolean;
    name, wjname, bomtype, memo, hingetype, installtype: string;
  end;
type
  PDoorsCurHinge = ^DoorsCurHinge;

//掩门
type
  DoorHBoxParam = record                    //过桥参数
    id: Integer;
    deleted: boolean;
    name, wjname, bomtype, memo, direct, fbstr, model, bdfile: string;
    height, depth, thick: Real;
  end;
type
  PDoorHBoxParam = ^DoorHBoxParam;

type
  DoorAccessory = record
    id: Integer;
    deleted: boolean;
    name, myunit, mytype, bomtype, color, memo, bdfile: string;
  end;
type
  PDoorAccessory = ^DoorAccessory;

type
  DoorsColorClass = record
    id: Integer;
    deleted: boolean;
    color, myclass, mat, color2, color3, color4: string;
  end;
type
  PDoorsColorClass = ^DoorsColorClass;

type
  DoorsColorClass2 = record
    id: Integer;
    deleted: boolean;
    bktype, color, bkcolor1, bkcolor2, bkcolor3, bkcolor4: string;
  end;
type
  PDoorsColorClass2 = ^DoorsColorClass2;

type
  DoorsShutterExp = record
    id: Integer;
    deleted: boolean;
    paneltype: string;
    height, width, heightcap, widthcap, minheight, minwidth: single;
  end;
type
  PDoorsShutterExp = ^DoorsShutterExp;

type
  DoorsWjBom = record
    deleted: boolean;
    id: Integer;
    name: string;
  end;
type
  PDoorsWjBom = ^DoorsWjBom;

type
  DoorsWjBomDetail = record
    deleted: boolean;
    id: Integer;
    bomname, name, l, d, num, opendirect, bktype: string;
    door_bh:Integer;
  end;
type
  PDoorsWjBomDetail = ^DoorsWjBomDetail;

type DoorsPanelBom = record
  deleted: boolean;
  id: Integer;
  name:string;
end;
type PDoorsPanelBom = ^DoorsPanelBom;

type DoorsPanelBomDetail = record
  deleted:boolean;
  id:Integer;
  bomclass, bomname, l, w, h, mat, color, bomtype, memo, bdfile:string;
  lmin, lmax, hmin, hmax, num:Integer;
end;
type PDoorsPanelBomDetail = ^DoorsPanelBomDetail;

type
  DoorsPrice = record
    deleted: boolean;
    id: Integer;
    name1, name2, mytype, direct: string;
    price, price2: single;
    price_a1, price_a2, price_b1, price_b2, price_c1, price_c2, price_d1, price_d2, price_e1, price_e2:single;
    lmax, lmin, hmax, hmin, start_num: Integer;
    pricetype, myunit, num, pricetable: string;
  end;
type
  PDoorsPrice = ^DoorsPrice;

type
  price_table = record
    name, mat, price1, price2, cost: string;
    price_a1, price_a2, price_b1, price_b2, price_c1, price_c2, price_d1, price_d2, price_e1, price_e2:string;
    bh:Integer;
    deleted: boolean;
  end;
type
  pprice_table = ^price_table;

type
  DoorXML = record
    id:Integer;
    name, xml:string;
    deleted: boolean;
  end;
type PDoorXML = ^DoorXML;



type HingeHole = record
  x, y, l, w, di:Integer;
  r:string;
  g:char;
end;
type PHingeHole = ^HingeHole;  

type
  DoorPanelType = record
    id: Integer;
    deleted: boolean;
    name, mytype, bomtype, bktype, direct, fbstr, pnl3d, memo, panelbom, memo2, memo3, bdfile: string;
    thick, ypos, is_buy: Integer;
    lfb, hfb: Real;
    iswhole: boolean;
    lmin, lmax, wmax, wmin: Integer;
  end;
type
  PDoorPanelType = ^DoorPanelType;

type
  DoorRectBox = record                      //过桥
    vh, selected: boolean;
    w0, h0, x0, y0, d0: single;         //可视
    w1, h1, x1, y1, d1: single;         //物料
    w2, h2, x2, y2, d2: single;         //投影
    boxtype, color: string;
  end;
type
  PDoorRectBox = ^DoorRectBox;

type
  DoorRectPanel = record                    //面板
    selected: boolean;
    w0, h0, x0, y0, d0: single;         //可视
    w1, h1, x1, y1, d1: single;         //物料
    w2, h2, x2, y2, d2: single;         //投影
    PanelType, color, direct, pricetype, color2: string;
    price, price2:single;
    thick:Integer;
  end;
type
  PDoorRectPanel = ^DoorRectPanel;

type
  TDoorDoorRect = class(TObject)
  public
    x0, y0, doorw, doorh, x1, y1, doorw1, doorh1: single;
    selected, hhdraw: boolean;
    mOpenDirect, mMemo: string;
    mDoorW, mDoorH, mVBoxW, mUDBoxH, mVBoxW0, mUDBoxH0: Real;
    mHandle, mHandlePos, mHandlePosX, mHandlePosY: string;
    mHandleX, mHandleY, mHandleW, mHandleH: Real;
    mHinge, mHingeCt, mHingeHoleExtra: string;
    mIsFrame: boolean;

    mHHArr:array of HingeHole;

    mPanelType, mPanelColor: string;
    boxlist: TList;
    panellist: TList;
    mYPos: Integer;
    mPParam: PDoorsParam;
    mHingeHoleDes, mHingeHoleParam:string;

    constructor Create();
    destructor Destroy; override;
    procedure ClearBoxList;
    procedure ClearPanelList;
    procedure CreateHBoxAndPanel(boxtype, boxcolor, pnltype, pnlcolor: string; num: Integer; h, d, thick: single;
      hh: array of single; pnls1, pnls2, di: array of string);
    procedure UnselecetAllPanels;
    function SelectPanelByPos(x0, y0: single; multisel: boolean): PDoorRectPanel;
    function SelectRectBoxByPos(x0, y0: single): PDoorRectBox;
    procedure CopyFromDoor(door: TDoorDoorRect);
    function GetSelectedPanel: PDoorRectPanel;
    function GetPanelPosInDoor(p: PDoorRectPanel): Integer;
    function GetNearestUpPanel(p: PDoorRectPanel): PDoorRectPanel; overload;
    function GetNearestDownPanel(p: PDoorRectPanel): PDoorRectPanel; overload;
    function GetNearestUpPanel(p: PDoorRectBox): PDoorRectPanel; overload;
    function GetNearestDownPanel(p: PDoorRectBox): PDoorRectPanel; overload;
    function GetNearestUpBox(p: PDoorRectPanel): PDoorRectBox;
    function GetNearestDownBox(p: PDoorRectPanel): PDoorRectBox;

    function GetVboxKCInfo:string;
    function GetHboxKCInfo(n:Integer; p: PDoorRectBox):string;
  end;

type
  TMyThread = class(TThread)
  protected
    procedure Execute; override;
  end;
    
type
  TLocalObject = class(TObject)
  PaxCompiler1: TPaxCompiler;
  PaxJavaScriptLanguage1: TPaxJavaScriptLanguage;
  PaxProgram1: TPaxProgram;
  xdoc: TXMLDocument;
  qry: TADOQuery;
  //mythread: TMyThread;
  private
    mHPInfoList, mKCInfoList: TList;
    mIIHoleCalcRule:ISuperObject;

    mC: array[0..15] of Integer;
    mVName, mVValue: array[0..15] of string;

    mQDFlag, mOrderFlag, mExportFlag, mQDBomFlag, mDataMerge, mExportMultiReport, mDoorPrecision, mCombineKc: Integer;
    mThridPartyButtonName: string;
    mPackServiceUrl: string;
    mSliDbStr, mDoorsDbStr: string;
    mProductList, mDoorList: TList;
    mXMLStringList: TStringList;
    
    HoleWjList: TList;
    mBDXMLList: TMyStringHash;

    mPicWidth, mPicHeight: Integer;
    mPicWidth2, mPicHeight2: Integer;

    mQuoIndex1, mQuoIndex2, mQuoIndex3, mQuoIndex: Integer;
    mQuoSliIndex, mQuoDoorIndex: Integer;
    mPercentGt, mPercentSli: Integer;




    mIsTotalPrice, mIsUpdateTreeList, mNoDrawTreeList: boolean;

    mOno, mDt, mCellphone: string;

    bomlist: TList;
    basewjlist: TList;
    slidinglist: TList;
    doorslist: TList;

    bomdeslist:TStringList;
    doordeslist:TStringList;
    slidingdeslist:TStringList;

    allBomList, allBomList2: TList;
    curAllBomList, curBjBomList, curWjBomList, curXCWjBomList, curSlBomList, curDlBomList: TList;

    bjBomList, bjBomList2: TList;
    wjBomList, wjBomList2: TList;
    xcwjBomList, xcwjBomList2: TList;
    slBomList, slBomList2: TList;
    dlBomList, dlBomList2: TList;

    mTempList: TList;
    b2erpBomList: TList;

    mBomIndexBj, mBomIndexWj, mBomIndexXCWj, mBomIndex, mBomIndexWjInfo, mAllWjIndex: Integer;
    mBomSliIndex: Integer;
    mTmpSlidinglist, mAllWjList: TList;
    mGraphNo, mBG: string;

    mIndexBB: Integer;
    mCurDoorIndex: Integer;

    mCalcItem:TMyCalcItem;

    mLua:TLua;

    mJoBarCode:ISuperObject;

    //$左收口宽度， $右收口宽度， $柱切角宽度， $柱切角深度， $梁切角深度， $梁切角高度， $左侧趟门位， $右侧趟门位
    value_lsk, value_rsk, value_zk, value_zs, value_ls, value_lg, value_ltm, value_rtm: Integer;

    //function XmlNode2BomItem(param0: PBomParam; var id, slino: Integer): Integer;
    procedure SetSysVariantValue(vname, value: string);
    procedure NewBomOrderItem(var p: PBomOrderItem);
    procedure InitVarArgs(var va: array of Integer; var vs: array of string);
    function CompileLuaProgram(jo:ISuperObject; code:string):string;
    procedure SetIsCalcHoleConfig(poi: PBomOrderItem; str: string);
    procedure SetBGParam(var poi: PBomOrderItem; str:string);
    procedure SetSysVariantValueForOrderItem(varstr: string; poi: PBomOrderItem);
    procedure Des2Des(p: Pointer);
    procedure GraphSizeToBomSize(l, p, h, direct: Integer; var bl, bp, bh: Integer);
    function TextureDirectChange(di: Integer): Integer;
    function ToBomStd(des: string; l, p, h: Integer): string;
    function ImportXomItemForBom(param0: PBomParam; var id, slino: Integer): Integer;
    procedure LoadFromXMLTemplate(xml: string; l, h:Integer; resize: boolean);
    function GetSlidingXomItemForBom(childxml:string; pl, ph: Integer):ISuperObject;
    function GetDoorsXomItemForBom(childxml:string; pl, ph: Integer):ISuperObject;
    function ImportSlidingXomItemForBom(cid, boardheight, mark: Integer; blist: TList; blockxml, gno, gdes, gcb, extra, pname, subspace, xml, pmat,
      pcolor: string; pid, pl, pd, ph: Integer; var id, slino: Integer; px, py, pz: Integer; outputtype: string): Integer;
    function ImportDoorsXomItemForBom(cid, boardheight, mark: Integer; blist: TList; blockxml, gno, gdes, gcb, extra, pname, subspace, xml, pmat,
      pcolor: string; pid, pl, pd, ph: Integer; var id, slino: Integer; px, py, pz: Integer; outputtype: string): Integer;

    procedure GraphSizeToBJSize(bjsize: string; p: Pointer);
    function ImportXomItemForQuo(param0: PQuoParam; var id, slino: Integer): Integer;
    function ImportSlidingXomItemForQuo(cid, boardheight, mark: Integer; blist: TList; gno, gdes, gcb, pname, subspace, xml, pmat,
      pcolor: string; pid, pl, pd, ph: Integer; var id, slino: Integer; outputtype: string): Integer;
    function ImportDoorsXomItemForQuo(cid, boardheight, mark: Integer; blist: TList; gno, gdes, gcb, pname, subspace, xml, pmat,
      pcolor: string; pid, pl, pd, ph: Integer; var id, slino: Integer; outputtype: string): Integer;
    function EnumXML(xml: Widestring): Widestring;
    function PolyLineToLength(str: string): Integer;
    function CompileProgram(jo:ISuperObject; code:string):string;
    function Xml2ChildNodes(const xml: string):IXMLNode;
    function ImportCloneItemForBom(exp:TExpress; program_str:string; clone_oi:PBomOrderItem; clonenode: IXMLNode; param0: PBomParam; var id, slino: Integer): Integer;
    function ImportCloneItemForQuo(exp:TExpress; program_str:string; clone_oi:PBomRecord; clonenode: IXMLNode; param0: PQuoParam; var id, slino: Integer): Integer;

    procedure InitBgMinAndMax;
    procedure InitBgMinAndMaxItem(var p: PBomOrderItem);
    procedure CalcBomWj;                //计算物料，基础五金
    procedure CalcLgFlag;               //计算连柜五金
    procedure CalcHoleAndKc;            //计算孔位信息和开槽信息
    procedure CalcKCCombine;            //开槽合并
    procedure CalcHoleWj;               //计算孔位五金
    procedure CalcLineCombine;          //计算线性物体合并
    procedure CalcSeq;                  //计算排序序号
    procedure UnloadBom(freedata:boolean=True);
    procedure InitSysVariantValue;
    function ToBGInfo(p: PBomOrderItem): string;
    function ToBGInfoX2D(p: PBomOrderItem): string;
    procedure TransAB(p: PBomOrderItem);
    function LoadChildBom(ppoi: PBomOrderItem; cid, boardheight: Integer; str: string; list: TList; pid, l, p, h: Integer; mat, color, memo, gno, gdes, gcb, myclass, bomstd: string; num: Integer): Integer;
    procedure GetBomUserDefine(p: PBomOrderItem); //根据自定义字段获取属性
    procedure GetQuoUserDefine(p: PBomRecord); //根据自定义字段获取属性
    procedure GetMatAlias(mat, color: string; bh: Integer; var alias, alias2, alias3:string);
    procedure BomList2CalcList(bomlist, calclist: TList; is_new_calcitem: boolean = True);
    procedure CalcList2BomList(calclist, bomlist: TList; is_dispose_calcitem: boolean = True);
    function BomItem2CalcItem(p:Pointer; item2:TMyCalcItem):TMyCalcItem;
    function CalcItem2BomItem(p, p2: Pointer): PBomOrderItem;
    procedure BDXML_BDXML(var xml: string; xml2: string); //合并bdxml
    procedure GetXptlist(poi: PBomOrderItem; var xptlist_isxx, xptlist_jx, xptlist_pl:Integer);
    procedure GetSpaceItem(p: Pointer; var space: string; var space_x, space_y, space_z: Integer);
    function GetWorkflowStr(workflow, bomstd, hole: string): string;
    function GetBomlistString: string;
    procedure ClearAllBomList;
  //趟门
  protected
    mIsSetDoors, mIsModify: boolean;
    mCopyDoor: Integer;
    procedure Copy(p1, p2: Pointer; name: string);
    function GetPanelType(bktype, name: string): PPanelType; overload;
    function GetSSExp(name: string): PSlidingShutterExp;
    function GetDoorYPos(n, doornum, overlapnum: Integer): Integer;
    procedure AddOneMx(door:TDoorRect; pnl:PRectPanel; nHasMzhb:boolean; list:TList);
    function ResetSubMxSize(mGridItem, j, k: Integer; oneMxs, FGObj, sJson:ISuperObject;door:TDoorRect):ISuperObject;
    function ResetMxSize(mGridItem, j, k: Integer; oneMxs, FGObj, sJson:ISuperObject;door:TDoorRect):ISuperObject;
    procedure GetPanelBom(list:TList; bomclass, mat, color, color2, color3:string; pnll, pnlh:single);
    function GetXMLBom: string;
    function NewWLData: Pointer;
    function EscapeBracket(name:string):string;
    function FindBkType(bktype: string): boolean;
    function GetDataValue(extradatajson: ISuperObject; SubMXList: ISuperObject): ISuperObject;
    function GetBomObj(extradatajson: ISuperObject): ISuperObject;
  //趟门
  public
    orderno, graphno, holeno, mObjStr:string;
    mDoorsList: TObjectList;
    mL, mD, mH, mAddLength, mDataMode: Integer;
    mSlidingExp: SlidingExp;
    mSlidingType: SlidingType;
    mSlidingParam: SlidingParam;
    mTrackParam: TrackParam;
    mUDBoxParam: UDBoxParam;
    mHBoxParam: HBoxParam;
    mVBoxParam: VBoxParam;
    mMyPanelType, mMyPanelColor: string;
    mMySlidingColor, mMyHBoxColor: string;
    mMyUpTrackColor, mMyDownTrackColor, mMyVBoxColor, mMyUpBoxColor, mMyDownBoxColor: string;
    mGridItem: Integer;
    mExtra, mXML:string;
    mSSExpList, mSlidingPriceList, mPriceTableList: TList;
    mSlidingMyClassGroupList, mSlidingWjBomList, mSlidingWjBomDetailList: TList;
    mSlidingColorList, mSlidingAccessoryList, mSlidingColorClassList, mSlidingColorClass2List: TList;
    //单门计算公式，门类型，趟门参数， 上下轨类型，上下横框类型，中横框类型， 竖框类型
    mSlidingExpList, mSlidingTypeList, mSlidingParamList, mTrackParamList,
      mUDBoxParamList, mHBoxParamList, mVBoxParamList, mPanelTypeList, mPanelBomList, mPanelBomDetailList: TList;
      mCfglist: TList;
    //自选配件
    OptionalAccList:TList;
    SlidingObjList, SfgParam:ISuperObject;
    //横分格  ， 竖分格
    SlidingHfg2List, SlidingHfg3List, SlidingHfg4List : TList;
    SlidingSfg2List, SlidingSfg3List, SlidingSfg4List :TList;
    //横中横， 竖中横
    HSHBoxParamList, SHBoxParamList:TList;

    mNoFZTPriceFlag, mNoCDWPriceFlag, mBomPriceFlag:Integer;
    
    procedure SlidingAndDoorInit;
    procedure UninitSlidingAndDoorList;
    procedure ClearSlidingAndDoorList;
    procedure RecalcDoor(door:TDoorRect; t1, t2, hh:single);
    function GetSlidingExp(name: string): PSlidingExp;virtual;
    function GetSlidingType(name: string): PSlidingType;virtual;
    function GetSlidingParam(name: string): PSlidingParam;virtual;
    function GetTrackParam(name: string): PTrackParam;virtual;
    function GetUDBoxParam(name: string): PUDBoxParam;virtual;
    function GetHBoxParam(name: string; nType: Integer =0): PHBoxParam;virtual;
    function GetVBoxParam(name: string): PVBoxParam;virtual;
    function GetAccessory(name: string): PAccessory;virtual;
    function GetSlidingColor(name: string): PSlidingColor;
    procedure SetSetDoors(b: boolean);
    function GetSlidingColorClass(myclass, color: string): PSlidingColorClass; overload;
    function GetSlidingColorClass(myclass, mat, color: string): PSlidingColorClass; overload;
  //掩门
  protected
    mLuaObj:TLuaObj;
    mIsChange, mLockControl: boolean;
    mLineColor : Cardinal;
    mIsVertical: boolean;
    mPExp: PDoorsExp;
    mPType: PDoorsType;
    mPParam: PDoorsParam;
    mPHBoxParam: PDoorHBoxParam;
    mDoorMyPanelType, mDoorMyPanelColor: string;
    mDoorMyDoorsColor, mDoorMyHBoxColor: string;
    mDoorMyVBoxColor: string;
    mDoorGridItem, mZNMJ: Integer;
    mDoorMemo, mExtend, mHingeHole:string;

    mColorList, mExpList, mTypeList, mParamList, mHandleList, mDoorHBoxParamList, mDoorPanelTypeList,
      mAccessoryList, mColorClassList, mShutterExpList, mWJBomList, mWJBomDetailList,
      mPriceList, mHingeList, mCurHingeList, mColorClass2List, mDoorPanelBomDetailList, mDoorPriceTableList,
      mDoorXMLList: TList;

    function GetDoorsExp(name: string): PDoorsExp;
    function GetDoorsParam(name1, name2: string): PDoorsParam;
    function GetDoorsType(name: string): PDoorsType;
    function GetDoorsHandle(name: string): PDoorsHandle;
    function GetDoorsHinge(mj: string; dt:PDoorsType): PDoorsHinge;
    function GetDoorsCurHinge(mj, mHinge: string): PDoorsCurHinge;
    function GetDoorHBoxParam(name: string): PDoorHBoxParam;
    function GetDoorPanelType(bktype, name: string): PDoorPanelType;
    function GetColorClass(myclass, color: string): PDoorsColorClass;
    function GetColorClass2(bktype, color: string): PDoorsColorClass2;
    function GetWjBom(name: string): PDoorsWjBom;
    function GetHingeNum(phinge: PDoorsHinge; l, d: Integer; opendirect: string): Integer;
    function GetCurHingeName(pcurhinge: PDoorsCurHinge; ct:string): string;
    function GetHingeName(phinge: PDoorsHinge; ct:string): string;
    function GetDoorsColor(name: string): PDoorsColor;
    function GetDoorSSExp(name: string): PDoorsShutterExp;
    function GetDimensionXml(x0, y0, x1, y1, offset, offset2: single): string;
    function GetDoorAccessory(name: string): PDoorAccessory;
    

    function GetJsonFaceA(door:TDoorDoorRect; var luaobj:TLuaObj; var lua:TLua; direct:string): string;   //获取当前门的门铰孔，拉手孔信息
    function GetJsonFaceB(door:TDoorDoorRect; var luaobj:TLuaObj; var lua:TLua; direct:string): string;
    function GetHandleHoleScript(s: string): string;
    procedure HingeHole2DoorObject(index:Integer = -1);

    function DoorGetXMLBom(): string;
    procedure GetParamXMLBom(list:TList; str:string; doorindex:Integer; x, z, l, h:double);
    procedure DoorGraphSizeToBomSize(l, p, h:double; direct: Integer; var bl, bp, bh: double);

  //掩门
  public
    mGuid : string;
    mLCap, mRCap, mUCap, mDCap: Integer;
    mLMFValue, mHMFValue, mMMFValue:Real;
    procedure DoorLoadFromXMLTemplate(xml: string; l, h:Integer; resize: boolean);
    procedure DoorRecalcDoor(door:TDoorDoorRect; t1, t2, tt1, tt2:single; m:Integer);
  //板材物料
  public
    mUserName: string;
    mOrderName, mDistributor, mAddress, mPhone, mFax, mMemo, mCustomerName, mCustomerCellPhone
      , mCustomerPhone, mCustomerAddress: string;
    mDateTime: TDateTime;

    mTempStr:string;
    mPluginHost:TPlugin;
    mExp, mTmpExp: TExpress;
    mJoNetQuo, mJoNetQuoData:ISuperObject;
    function LoadOneBomData(des: string):Integer;
    function OneBomData2Json(des: string):string;
    constructor Create;
    destructor Destroy; override;
    procedure ShowBomMessage(str:string);
    procedure RemoveInvisibleNode(root: IXMLNode);
    class function fromPygetobj(url:string):string;

    class procedure configseqInfoHash(jo:ISuperObject);       //from py 初始化 seqInfoHash
    class procedure configclassseqInfoHash(jo:ISuperObject);
    class procedure configgROC(jo:ISuperObject);
    class procedure configworkflow(jo:ISuperObject);

    class procedure InitBoardMatList(jo:ISuperObject);
    class procedure UninitBoardMatList();
    procedure InitHoleWjList(jo:ISuperObject);
    procedure UninitHoleWjList();

    class procedure InitQuoHash(jo: ISuperObject);
    class procedure ReleaseQuoHash;
    class procedure InitBomHash(jo: ISuperObject);
    class procedure ReleaseBomHash;
    procedure LoadXML2Bom(xml: string);
    procedure LoadXML2Quo(xml: string);
    function EnumChild(param0: PBomParam):Integer;
    function GetCloneItemForBom(exp:TExpress; program_str:string; clone_oi:PBomOrderItem; clonenode: IXMLNode; param0: PBomParam):Integer;
    function FindDesList(xml: string):ISuperObject;
    procedure InitGtConfig(const config:string);
    procedure InitSlidingConfig(const config:string);
    procedure InitDoorConfig(const config:string);
    //class procedure LoadMyLibrary;
    //class procedure FreeMyLibrary;
    class procedure InitErpList(list: TList; jo:ISuperObject);
    class procedure UninitErpList(list: TList);
    class procedure InitBGHash;
    class function SearchBGDir(dir: string): Integer;

    procedure InitData();
    procedure UninitData();
    procedure Uninit();
    procedure ClearTempList;
    class function GetXMLByLink(link: Widestring; qry:TADOQuery): Widestring;
    //procedure CallThread;
  published
    function GetXmlDes(const xml:string; const config:string):string;
    function Xml2JsonBom(const xml:string; const config:string):string;
  end;

var gLocalObject:TLocalObject;
var
  UrlIp:string ='http://129.204.134.85:8002/Qdbom' ;
  factoryDataPath:string = 'data';
implementation

{ TLocalObject }



var
  gCncDll           : THandle = 0;
  cncInitDll        : procedure(p, adata: Pointer); stdcall;
  cncUninitDll      : procedure; stdcall;
  cncBd2Dxf         : function(bdname, dxfname: pchar; l, h, bh: Integer; args: PINT; argsnum: Integer; str: pchar; tx, ty, tl, tw, ra, xoffset, yoffset: Integer): Integer; stdcall;
  cncBd2Mpr         : function(bdname, mprname: pchar; ab: Integer; l, h, bh: Integer; args: PINT; argsnum: Integer): Integer; stdcall;
  cncBd2Bpp         : function(bdname, bppname: pchar; ab: Integer; l, h, bh: Integer; args: PINT; argsnum: Integer): Integer; stdcall;
  cncBd2YougeData   : function(bdname: pchar; ab: Integer; l, h, bh: Integer; args: PINT; argsnum: Integer): pchar; stdcall;
  cncX2dToBdGraph   : function(x2dxml: pchar; gl, gp, gh, di: Integer; args: PINT; argsnum: Integer): pchar; stdcall;
  cncBDXml2Data     : function(xmlid, xml: pchar; l, h, bh: Integer; args: PINT; argsnum: Integer;
    pbgdata, paface, pbface, pa_yg, pb_yg, pa_mpr, pb_mpr, pab_bpp, pa_bpp, pb_bpp, p_dxf, pabinfo, pabkcinfo: pchar): Integer; stdcall;
  cncClearCache     : procedure; stdcall;

var
  gFormatPrecision  : Integer = 2;
  gFormatPrecision2 : Integer = 2;
  gQDBomFlag:Integer = 1;

var
  gBGHash: TMyStringHash;
  gErpItemList:TList;
  gPluginsList: TList;                //插件列表
  gCurPlugin: PPluginsDll = nil;
  gROC: ReportOutputConfig;
  gBoardMatList: TList;
  ruleHash, wjruleHash, childbomHash, holeconfigHash, kcconfigHash: THashedStringlist;
  linecalcList: TStringHash;
  bomstdList, workflowlist: TList;
  des2wuliao: TMyStringHash;
  seqInfoHash, classseqInfoHash: TStringHash;
  gLinkXML        : ISuperObject = nil;
  gFiledNameList  : ISuperObject = nil;
  desData, LuaData  : TMyStringHash;
constructor TLocalObject.Create;
  procedure ToBarCode(cjo:ISuperObject; code:string);
  var n1, n2, isformat:Integer;
  ws:WideString;
  begin
    cjo.I['IsCode'] := 0;
    if code='' then exit;
    isformat := 0;
    code := StringReplace(code, ' ', '', [rfReplaceAll]);
    ws := StringReplace(code, ';', '', [rfReplaceAll]);
    n1 := Pos('Format(''', ws);
    n2 := Pos(''',', ws);
    if (n1>0) and (n2>n1) then
    begin
      isformat := 1;
      cjo.S['format'] := MidStr(ws, n1+8, n2-n1-8);
    end;
    if isformat=0 then exit;
    n1 := Pos('[', ws);
    n2 := Pos(']', ws);
    if (n1>0) and (n2>n1) then
    begin
      cjo.I['IsCode'] := isformat;
      cjo.O['args'] := SO(MidStr(ws, n1, n2+1-n1));
    end;
  end;
var
  inif              : TIniFile;
  url, objstr, dllpath  : string;
  jo, cjo:ISuperObject;
  Buffer            : array[0..260] of Char;
  exepath, s, path:string;
  i, n :Integer;
  slist:   TStringList;
begin
  inherited;
  dllpath := 'lua51.dll';
  if not FileExists(dllpath) then
  begin
    s := GetEnvironmentVariable('QUICKDRAW_PATH');
    slist := TStringList.Create;
    slist.Text := StringReplace(s, ';', ''#13#10, [rfReplaceAll]);
    for i:=0 to slist.Count-1 do
    begin
      path := slist[i];
      n := Length(path);
      if path[n]='\' then path := path + dllpath;
      if path[n]<>'\' then path := path + '\' + dllpath;
      if FileExists(path) then
      begin
        dllpath := path;
        break;
      end;
    end;
    slist.Clear;
    FreeAndNil(slist);
  end;
  mLua := TLua.Create(False, dllpath);
  
  inif := TIniFile.Create(MyUtils.GetQuickDrawPath + 'qd.conf');
  mQDFlag := inif.ReadInteger('QuickDraw', 'QDFlag', 0);
  mOrderFlag := inif.ReadInteger('QuickDraw', 'QDOrderFlag', 0);
  mExportFlag := inif.ReadInteger('QuickDraw', 'ExportFlag', 0);
  gQDBomFlag := inif.ReadInteger('QuickDraw', 'QDBomFlag', 1); //mQDBomFlag=0 原来的bom，mQDBomFlag=1新的bom支持新的维护工具排序计算
  gFormatPrecision := inif.ReadInteger('QuickDraw', 'FormatPrecision', 2);
  gFormatPrecision2 := inif.ReadInteger('QuickDraw', 'FormatPrecision2', 2);
  mDataMerge := inif.ReadInteger('QuickDraw', 'DataMerge', 1);
  mExportMultiReport := inif.ReadInteger('QuickDraw', 'ExportMultiReport', 0);
  mDoorPrecision := inif.ReadInteger('QuickDraw', 'DoorPrecision', 0);
  mThridPartyButtonName := inif.ReadString('QuickDraw', 'ThridPartyButton', '');
  mIIHoleCalcRule := SO(inif.ReadString('孔位计算规则', '通孔计算', '{}'));

  mJoBarCode := TSuperObject.Create();
  cjo := TSuperObject.Create();
  ToBarCode(cjo, inif.ReadString('BarCode', 'A_MPR', ''));
  mJoBarCode.O['A_MPR'] := cjo;

  cjo := TSuperObject.Create();
  ToBarCode(cjo, inif.ReadString('BarCode', 'B_MPR', ''));
  mJoBarCode.O['B_MPR'] := cjo;

  cjo := TSuperObject.Create();
  ToBarCode(cjo, inif.ReadString('BarCode', 'AB_BPP', ''));
  mJoBarCode.O['AB_BPP'] := cjo;

  cjo := TSuperObject.Create();
  ToBarCode(cjo, inif.ReadString('BarCode', 'A_BPP', ''));
  mJoBarCode.O['A_BPP'] := cjo;

  cjo := TSuperObject.Create();
  ToBarCode(cjo, inif.ReadString('BarCode', 'B_BPP', ''));
  mJoBarCode.O['B_BPP'] := cjo;

  cjo := TSuperObject.Create();
  ToBarCode(cjo, inif.ReadString('BarCode', 'DXF', ''));
  mJoBarCode.O['DXF'] := cjo;

  cjo := TSuperObject.Create();
  ToBarCode(cjo, inif.ReadString('BarCode', 'BDFILE', ''));
  mJoBarCode.O['BDFILE'] := cjo;

  mPackServiceUrl := inif.ReadString('WebService', 'PackageService', '');
  inif.Free;

  inif := TIniFile.Create(MyUtils.GetQuickDrawPath + 'qd.ini');
  mPicWidth := inif.ReadInteger('SlidingDesign', 'PicWidth', 800);
  mPicHeight := inif.ReadInteger('SlidingDesign', 'PicHeight', 600);
  mPicWidth2 := inif.ReadInteger('SlidingDesign', 'PicWidth2', 700);
  mPicHeight2 := inif.ReadInteger('SlidingDesign', 'PicHeight2', 400);

  inif.Free;

  mSliDbStr := Format('Provider=Microsoft.Jet.OLEDB.4.0;Data Source=%s;Persist Security Info=False', [MyUtils.GetQuickDrawPath + 'data\sliding.mdb']);
  mDoorsDbStr := Format('Provider=Microsoft.Jet.OLEDB.4.0;Data Source=%s;Persist Security Info=False', [MyUtils.GetQuickDrawPath + 'data\doors.mdb']);

  mProductList := TList.Create;
  basewjlist := TList.Create;
  slidinglist := TList.Create;
  doorslist := TList.Create;
  
  mDoorList := TList.Create;
  allBomList := TList.Create;
  allBomList2 := TList.Create;
  curAllBomList := allBomList;

  bjBomList := TList.Create;
  bjBomList2 := TList.Create;
  curBjBomList := bjBomList;

  wjBomList := TList.Create;
  wjBomList2 := TList.Create;
  curWjBomList := wjBomList;

  xcwjBomList := TList.Create;
  xcwjBomList2 := TList.Create;
  curXCWjBomList := xcwjBomList;

  slBomList := TList.Create;
  slBomList2 := TList.Create;
  curSlBomList := slBomList;

  dlBomList := TList.Create;
  dlBomList2 := TList.Create;
  curDlBomList := dlBomList;

  mXMLStringList := TStringList.Create;

  mTmpSlidinglist := TList.Create;      //临时list存放趟门数据
  mAllWjList := TList.Create;

  mHPInfoList := TList.Create;          //
  mKCInfoList := TList.Create;

  //报价数据
  mQuoIndex1 := 0;
  mQuoIndex2 := 0;

  mJoNetQuo := TSuperObject.Create();
  
  mExp := TExpress.Create;

  mTmpExp := TExpress.Create;

  mCalcItem := TMyCalcItem.Create;

  mTempList := TList.Create;

  mBDXMLList := TMyStringHash.Create(1024);

  InitSysVariantValue;
end;


procedure TMyThread.Execute;
begin
  {CoInitialize(nil);
  gLocalObject.InitData();
  gLocalObject.SlidingAndDoorInit();
  CoUninitialize;}
end;

//procedure TLocalObject.CallThread;
//begin
//  mythread := TMyThread.Create(True);  // True表示挂起线程，暂不启动。默认为False
//  mythread.FreeOnTerminate := True; // 表示线程执行完毕后自动Free
//  mythread.Resume;  // 启动线程
//end;

procedure TLocalObject.InitSysVariantValue;
begin
  value_lsk := 0;
  value_rsk := 0;
  value_zk := 0;
  value_zs := 0;
  value_ls := 0;
  value_lg := 0;
  value_ltm := 0;
  value_rtm := 0;
end;

destructor TLocalObject.Destroy;
var
  i                 : Integer;
  item:TProductItem;
begin

  Uninit;
  allBomList2.Free;
  allBomList.Free;

  bjBomList.Free;
  wjBomList.Free;
  xcwjBomList.Free;
  bjBomList2.Free;
  wjBomList2.Free;
  xcwjBomList2.Free;

  FreeAndNil(slBomList);
  FreeAndNil(slBomList2);

  FreeAndNil(dlBomList);
  FreeAndNil(dlBomList2);

  FreeAndNil(mCalcItem);

  for i := 0 to mDoorList.Count - 1 do
  begin
    dispose(mDoorList[i]);
  end;
  mDoorList.Clear;
  mDoorList.Free;

  for i := 0 to mProductList.Count - 1 do
  begin
    item := TProductItem(mProductList[i]);
    item.Free;
  end;
  mProductList.Clear;
  mProductList.Free;
  
  for i := 0 to mHPInfoList.Count - 1 do
  begin
    dispose(mHPInfoList[i]);
  end;
  mHPInfoList.Clear;
  mHPInfoList.Free;

  for i := 0 to mKCInfoList.Count - 1 do
  begin
    dispose(mKCInfoList[i]);
  end;
  mKCInfoList.Clear;
  mKCInfoList.Free;

  mIIHoleCalcRule := nil;
  mJoBarCode := nil;

  mXMLStringList.Clear;
  mXMLStringList.Free;

  mBDXMLList.Clear;
  FreeAndNil(mBDXMLList);

  for i := 0 to mTempList.Count - 1 do
  begin
    dispose(mTempList[i]);
  end;
  mTempList.Clear;
  mTempList.Free;

  ClearTempList;
  FreeAndNil(mAllWjList);

  FreeAndNil(mExp);
  FreeAndNil(mTmpExp);

  mJoNetQuo := nil;
  mJoNetQuoData := nil;

  mLua.Free;
  inherited;
end;

procedure TLocalObject.UnloadBom(freedata:boolean=True);
var
  i,j                 : Integer;
  p                 : PBomOrderItem;
  item              : TProductItem;
  hpinfo            : THolePointInfo;
  KCInfo            : TKCInfo;
  poi       :PBomOrderItem;
begin
  if bomlist = nil then exit;

  //FormCreate 建立一次
  for i:=0 to mProductList.Count-1 do
  begin
    item := TProductItem(mProductList[i]);
    item.Free;
  end;
  mProductList.Clear;
  for i:=0 to mDoorList.Count-1 do
  begin
    dispose(mDoorList[i]);
  end;
  mDoorList.Clear;

  for i:=0 to allBomList.Count-1 do
  begin
    dispose(allBomList[i]);
  end;
  allBomList.Clear;
  
  for i:=0 to allBomList2.Count-1 do
  begin
    dispose(allBomList2[i]);
  end;
  allBomList2.Clear;
  
  curAllBomList := allBomList;

  bjBomList.Clear;
  bjBomList2.Clear;
  curBjBomList := bjBomList;

  wjBomList.Clear;
  wjBomList2.Clear;
  curWjBomList := wjBomList;

  xcwjBomList.Clear;
  xcwjBomList2.Clear;
  curXCWjBomList := xcwjBomList;

  slBomList.Clear;
  for i:=0 to slBomList2.Count-1 do
  begin
    dispose(slBomList2[i]);
  end;
  slBomList2.Clear;
  curSlBomList := slBomList;

  dlBomList.Clear;
  for i:=0 to dlBomList2.Count-1 do
  begin
    dispose(dlBomList2[i]);
  end;
  dlBomList2.Clear;
  curDlBomList := dlBomList;

  mXMLStringList.Clear;
  mTmpSlidinglist.Clear;
  mAllWjList.Clear;

  for i := 0 to mHPInfoList.Count - 1 do
  begin
    hpinfo:= THolePointInfo(mHPInfoList[i]);
    hpinfo.Free;
  end;
  mHPInfoList.Clear;

  for i := 0 to mKCInfoList.Count - 1 do
  begin
    KCInfo:= TKCInfo(mKCInfoList[i]);
    KCInfo.Free;
  end;
  mKCInfoList.Clear;

  for i := 0 to bomlist.Count - 1 do
  begin
    poi:= bomlist[i];
    poi.code:='';
    poi.name:='';
    poi.mat:='';
    poi.mat2:='';
    poi.mat3:='';
    poi.color:='';
    poi.workflow:='';
    poi.tmp_soz:='';
    poi.desc:='';
    poi.bomdes:='';
    poi.bomwjdes:='';
    poi.bomstddes:='';
    poi.childbom:='';
    poi.myclass:='';
    poi.nodename:='';
    poi.linecalc:='';
    poi.bomstd:='';
    poi.bg:='';

    poi.holestr:='';
    poi.kcstr:='';

    poi.memo:='';
    poi.gno:='';
    poi.gdes:='';
    poi.gcb:='';
    poi.extra:='';
    poi.bomdes:='';
    poi.fbstr:='';
    poi.subspace:='';
    poi.process:='';
    poi.ls:='';
    poi.myunit:='';
    poi.bomtype:='';
    poi.bdxmlid:='';
    poi.user_fbstr:='';

    for j := 0 to 15 do
    begin
    poi.var_names[j] := '';
    end;
    poi.a_hole_info:='';
    poi.b_hole_info:='';
    poi.holeinfo:='';

    poi.outputtype:='';
    poi.holeconfig_flag:='';
    poi.kcconig_flag:='';
    poi.bg_data:='';
    poi.mBGParam:='';

    poi.bg_filename:='';
    poi.mpr_filename:='';
    poi.bpp_filename:='';
    poi.devcode:='';

    poi.extend:='';
    poi.group:='';
    poi.packno:='';
    poi.userdefine:='';
    poi.erpunit:='';

    poi.erpmatcode:='';
    poi.blockmemo:='';
    poi.number_text:='';
    dispose(poi);
  end;
  bomlist.Clear;
  if freedata then
  begin
    bomlist.Free;
    bomlist := nil;
  end;

  for i := 0 to basewjlist.Count - 1 do
  begin
    poi := basewjlist[i];
    poi.code:='';
    poi.name:='';
    poi.mat:='';
    poi.mat2:='';
    poi.mat3:='';
    poi.color:='';
    poi.workflow:='';
    poi.tmp_soz:='';
    poi.desc:='';
    poi.bomdes:='';
    poi.bomwjdes:='';
    poi.bomstddes:='';
    poi.childbom:='';
    poi.myclass:='';
    poi.nodename:='';
    poi.linecalc:='';
    poi.bomstd:='';
    poi.bg:='';

    poi.holestr:='';
    poi.kcstr:='';

    poi.memo:='';
    poi.gno:='';
    poi.gdes:='';
    poi.gcb:='';
    poi.extra:='';
    poi.bomdes:='';
    poi.fbstr:='';
    poi.subspace:='';
    poi.process:='';
    poi.ls:='';
    poi.myunit:='';
    poi.bomtype:='';
    poi.bdxmlid:='';
    poi.user_fbstr:='';

    for j := 0 to 15 do
    begin
    poi.var_names[j] := '';
    end;
    poi.a_hole_info:='';
    poi.b_hole_info:='';
    poi.holeinfo:='';

    poi.outputtype:='';
    poi.holeconfig_flag:='';
    poi.kcconig_flag:='';
    poi.bg_data:='';
    poi.mBGParam:='';

    poi.bg_filename:='';
    poi.mpr_filename:='';
    poi.bpp_filename:='';
    poi.devcode:='';

    poi.extend:='';
    poi.group:='';
    poi.packno:='';
    poi.userdefine:='';
    poi.erpunit:='';

    poi.erpmatcode:='';
    poi.blockmemo:='';
    poi.number_text:='';
    dispose(poi);
  end;
  basewjlist.Clear;
  if freedata then
  begin
    basewjlist.Free;
    basewjlist := nil;
  end;

  for i := 0 to slidinglist.Count - 1 do
  begin
    dispose(slidinglist[i]);
  end;
  slidinglist.Clear;
  if freedata then
  begin
    slidinglist.Free;
    slidinglist := nil;
  end;

  for i := 0 to doorslist.Count - 1 do
  begin
    dispose(doorslist[i]);
  end;
  doorslist.Clear;
  if freedata then
  begin
    doorslist.Free;
    doorslist := nil;
  end;
end;

procedure TLocalObject.RemoveInvisibleNode(root: IXMLNode);
  procedure EnumChild(node: IXMLNode);
  var
    i               : Integer;
    cnode           : IXMLNode;
    str             : string;
  begin
    for i := node.ChildNodes.Count - 1 downto 0 do
    begin
      cnode := node.ChildNodes[i];
      if node.nodename = '我的模块' then
      begin
        str := GetAttributeValue(cnode, '显示方式', '', '');
        if str = '3' then
        begin
          node.ChildNodes.Remove(cnode);
          Continue;
        end;
      end;
      EnumChild(node.ChildNodes[i]);
    end;                                //for i
  end;
begin
  EnumChild(root);
end;

procedure TLocalObject.SetSysVariantValue(vname, value: string);
begin
  //$左收口宽度， $右收口宽度， $柱切角宽度， $柱切角深度， $梁切角深度， $梁切角高度， $左侧趟门位， $右侧趟门位
  //value_lsk, value_rsk, value_zk, value_zs, value_ls, value_lg, value_ltm, value_rtm: Integer;
  if vname = '$左收口宽度' then
    value_lsk := StrToInt(value);
  if vname = '$右收口宽度' then
    value_rsk := StrToInt(value);
  if vname = '$柱切角宽度' then
    value_zk := StrToInt(value);
  if vname = '$柱切角深度' then
    value_zs := StrToInt(value);
  if vname = '$梁切角深度' then
    value_ls := StrToInt(value);
  if vname = '$梁切角高度' then
    value_lg := StrToInt(value);
  if vname = '$左侧趟门位' then
    value_ltm := StrToInt(value);
  if vname = '$右侧趟门位' then
    value_rtm := StrToInt(value);
end;

procedure TLocalObject.NewBomOrderItem(var p: PBomOrderItem);
var
  i                 : Integer;
begin
  new(p);
  for i := 0 to 100 do
  begin
    p.ahole_index[i] := -1;
    p.bhole_index[i] := -1;
  end;
  for i := 0 to 100 do
  begin
    p.akc_index[i] := -1;
    p.bkc_index[i] := -1;
  end;
  p.pl := 0;
  p.pd := 0;
  p.ph := 0;
  p.trans_ab := False;
  p.vp := 0;

  p.hole_back_cap := 0;
  p.hole_2_dist := 0;

  p.cid := 0;
  p.id := 0;
  p.pid := -1;
  p.seq := 0;
  p.classseq := 0;
  p.pl := 0;
  p.pd := 0;
  p.ph := 0;
  p.lx := 0;
  p.ly := 0;
  p.lz := 0;
  p.x := 0;
  p.y := 0;
  p.z := 0;
  p.l := 0;
  p.p := 0;
  p.gl := 0;
  p.gp := 0;
  p.gh := 0;
  p.holeflag := 0;
  p.linemax := 0;
  p.ox := 0;
  p.oy := 0;
  p.oz := 0;
  p.childnum := 0;
  p.direct := 0;
  p.lgflag := 0;
  p.holeid := -1;
  p.kcid := -1;
  p.num := 1;
  p.lfb := 0;
  p.llk := 0;
  p.wfb := 0;
  p.wlk := 0;
  p.bl := 0;
  p.bp := 0;
  p.bh := 0;
  p.isoutput := True;
  p.value_lsk := 0;
  p.value_rsk := 0;
  p.value_zk := 0;
  p.value_zs := 0;
  p.value_ls := 0;
  p.value_lg := 0;
  p.value_ltm := 0;
  p.value_rtm := 0;
  p.hole_back_cap := 0;
  p.hole_2_dist := 0;
  p.is_outline := False;
  p.holetype := 0;

  p.llfb := 0;
  p.rrfb := 0;
  p.ddfb := 0;
  p.uufb := 0;
  p.fb := 0;

  p.bg_l_minx := 0;
  p.bg_l_maxx := 0;
  p.bg_r_minx := 0;
  p.bg_r_maxx := 0;

  p.bg_d_minx := 0;
  p.bg_d_maxx := 0;
  p.bg_u_minx := 0;
  p.bg_u_maxx := 0;

  p.bg_b_minx := 0;
  p.bg_b_maxx := 0;
  p.bg_f_minx := 0;
  p.bg_f_maxx := 0;

  p.bg_l_miny := 0;
  p.bg_l_maxy := 0;
  p.bg_r_miny := 0;
  p.bg_r_maxy := 0;

  p.bg_d_miny := 0;
  p.bg_d_maxy := 0;
  p.bg_u_miny := 0;
  p.bg_u_maxy := 0;

  p.bg_b_miny := 0;
  p.bg_b_maxy := 0;
  p.bg_f_miny := 0;
  p.bg_f_maxy := 0;

  p.workflow := '';

  p.zero_y := 0;
  for i := 0 to 5 do
  begin
    p.is_calc_holeconfig[i] := 0;
  end;
  for i := 0 to 15 do
  begin
    p.var_names[i] := '';
    p.var_args[i] := 0;
  end;

  p.mark := 0;

  p.space_x := 0;
  p.space_y := 0;
  p.space_z := 0;

  p.blockmemo := '';
  p.number_text := '';
end;

procedure TLocalObject.InitVarArgs(var va: array of Integer; var vs: array of string);
var
  i                 : Integer;
begin
  for i := 0 to Length(va) - 1 do
  begin
    va[i] := 0;
    vs[i] := '';
  end;
end;

function TLocalObject.CompileLuaProgram(jo:ISuperObject; code: string): string;
var
i:Integer;
s:string;
begin
  lua_pushinteger(mLua.LuaInstance, jo.I['X']);
  lua_setglobal(mLua.LuaInstance, 'LX');
  lua_pushinteger(mLua.LuaInstance, jo.I['Y']);
  lua_setglobal(mLua.LuaInstance, 'LY');
  lua_pushinteger(mLua.LuaInstance, jo.I['Z']);
  lua_setglobal(mLua.LuaInstance, 'LZ');
  lua_pushinteger(mLua.LuaInstance, jo.I['L']);
  lua_setglobal(mLua.LuaInstance, 'LL');
  lua_pushinteger(mLua.LuaInstance, jo.I['D']);
  lua_setglobal(mLua.LuaInstance, 'LD');
  lua_pushinteger(mLua.LuaInstance, jo.I['H']);
  lua_setglobal(mLua.LuaInstance, 'LH');
  lua_pushnumber(mLua.LuaInstance, jo.D['OZ']);
  lua_setglobal(mLua.LuaInstance, 'LOZ');
  for i:=0 to 15 do
  begin
    s := Format('C%s', [Chr(65 + i)]);
    lua_pushinteger(mLua.LuaInstance, jo.I['C'+IntToStr(i)]);
    lua_setglobal(mLua.LuaInstance, pchar(s));
  end;

  mLua.DoString(code);

  lua_getglobal(mLua.LuaInstance, 'XML');
  Result := lua_tostring(mLua.LuaInstance, -1);
  lua_settop(mLua.LuaInstance, 0);
end;

procedure TLocalObject.SetIsCalcHoleConfig(poi: PBomOrderItem;
  str: string);
var
  i                 : Integer;
  p                 : pchar;
begin
  p := pchar(str);
  for i := 0 to 5 do
  begin
    poi.is_calc_holeconfig[i] := 0;
  end;
  for i := 0 to Length(str) - 1 do
  begin
    if (i = 0) and (p[i] = '1') then poi.is_calc_holeconfig[i] := 1;
    if (i = 0) and (p[i] = '2') then poi.is_calc_holeconfig[i] := 2;

    if (i = 1) and (p[i] = '1') then poi.is_calc_holeconfig[i] := 1;
    if (i = 1) and (p[i] = '2') then poi.is_calc_holeconfig[i] := 2;

    if (i = 2) and (p[i] = '1') then poi.is_calc_holeconfig[i] := 1;
    if (i = 2) and (p[i] = '2') then poi.is_calc_holeconfig[i] := 2;

    if (i = 3) and (p[i] = '1') then poi.is_calc_holeconfig[i] := 1;
    if (i = 3) and (p[i] = '2') then poi.is_calc_holeconfig[i] := 2;

    if (i = 4) and (p[i] = '1') then poi.is_calc_holeconfig[i] := 1;
    if (i = 4) and (p[i] = '2') then poi.is_calc_holeconfig[i] := 2;

    if (i = 5) and (p[i] = '1') then poi.is_calc_holeconfig[i] := 1;
    if (i = 5) and (p[i] = '2') then poi.is_calc_holeconfig[i] := 2;
  end;
end;

procedure TLocalObject.SetBGParam(var poi: PBomOrderItem; str: string);
var n:Integer;
pp:PBomOrderItem;
begin
  poi.mBGParam := str;
  if poi.parent=nil then exit;
  n := Pos('^Inherit^:^1^', str);
  if n<=0 then exit;
  pp := poi.parent;
  str := StringReplace(pp.mBGParam, '^Inherit^:^1^ ', '', [rfReplaceAll]);
  poi.mBGParam := StringReplace(str, '{', '{^Inherit^:^1^ ', [rfReplaceAll]);
end;

procedure TLocalObject.SetSysVariantValueForOrderItem(varstr: string;
  poi: PBomOrderItem);
var
  n                 : Integer;
begin
  n := Pos('$左收口宽度', varstr);
  if n > 0 then poi.value_lsk := value_lsk;
  n := Pos('$右收口宽度', varstr);
  if n > 0 then poi.value_rsk := value_rsk;
  n := Pos('$柱切角宽度', varstr);
  if n > 0 then poi.value_zk := value_zk;
  n := Pos('$柱切角深度', varstr);
  if n > 0 then poi.value_zs := value_zs;
  n := Pos('$梁切角深度', varstr);
  if n > 0 then poi.value_ls := value_ls;
  n := Pos('$梁切角高度', varstr);
  if n > 0 then poi.value_lg := value_lg;
  n := Pos('$左侧趟门位', varstr);
  if n > 0 then poi.value_ltm := value_ltm;
  n := Pos('$右侧趟门位', varstr);
  if n > 0 then poi.value_rtm := value_rtm;
end;

function TLocalObject.OneBomData2Json(des: string):string;
begin
  Result:=desdata.ValueOf(des);
  if Result <> '' then exit;
end;

function TLocalObject.LoadOneBomData(des: string):Integer;
var
  list              : TList;
  key, str, objstr, url   : string;
  i, j, n                 : Integer;
  M                 : ^StrMap;
  prule             : PBomRuleRec;
  pwjrule           : PWJRuleRec;
  pcbomrule         : PBom2RuleRec;
  phole             : THoleConfig;
  pbs               : PBomStd;
  pkc               : TKCConfig;
  pwf               : PWorkflow;
  phwj              : PHoleWjItem;
  s1, s2:string;
  jo, cjo, ja:ISuperObject;
begin
  Result := 0;
  if (des='') or (des=',') then exit;
  {str := MyUtils.GetQuickDrawPath+'BomData\'+MD5.StrToMD5(des);
  if FileExists(str) then
  begin
    objstr := MyUtils.ReadStringFromFile(str);
  end else begin
     //url:=Format(UrlIp +'/bomdata/?des=%s&factorypath=%s&gQDBomFlag=%s',[HTTPEncode(UTF8Encode(des)),HTTPEncode(UTF8Encode(factoryDataPath)),HTTPEncode(UTF8Encode(inttostr(gQDBomFlag)))]);
     //objstr :=fromPygetobj(url);    //修改
     objstr :=OneBomData2Json(des);
     if not DirectoryExists(MyUtils.GetQuickDrawPath+'BomData') then
       CreateDirectory(pchar(MyUtils.GetQuickDrawPath+'BomData'), nil);
     MyUtils.WriteStringToFile(str, objstr);
  end; }
  objstr :=OneBomData2Json(des);
  if objstr='' then exit;

  jo := SO(objstr);

  ja := jo.O['des2wuliao'];

  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(M);
    M.s1 := cjo.S['s1'];
    M.s2 := cjo.S['s2'];
    M.s3 := cjo.S['s3'];
    M.direct := cjo.I['direct'];
    M.no := cjo.S['no'];
    M.oname := cjo.S['oname'];
    M.childbom := cjo.S['childbom'];
    M.priceclass := cjo.S['priceclass'];
    M.bomclass := cjo.S['bomclass'];
    M.linecalc := cjo.S['linecalc'];
    M.HoleConfig := cjo.S['HoleConfig'];
    M.bomstd := cjo.S['bomstd'];
    M.bomtype := cjo.S['bomtype'];
    M.KCConfig := cjo.S['KCConfig'];

    M.bg_filename := cjo.S['bg_filename'];
    M.mpr_filename := cjo.S['mpr_filename'];
    M.bpp_filename := cjo.S['bpp_filename'];
    M.devcode := cjo.S['devcode'];
    M.zero_y := cjo.I['zero_y'];
    M.is_output_bgdata := cjo.I['is_output_bgdata'];
    M.is_output_mpr := cjo.I['is_output_mpr'];
    M.is_output_bpp := cjo.I['is_output_bpp'];
    M.direct_calctype := cjo.I['direct_calctype'];
    M.youge_holecalc := cjo.I['youge_holecalc'];
    M.workflow := cjo.S['workflow'];
    key := cjo.S['key'];
    des2wuliao.Add(key, M);
  end;

  ja := jo.O['ruleHash'];
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(prule);
    prule.myclass1 := cjo.S['myclass1'];
    prule.myclass2 := cjo.S['myclass2'];
    prule.mat := cjo.S['mat'];
    prule.lfb := cjo.D['lfb'];
    prule.llk := cjo.D['llk'];
    prule.wfb := cjo.D['wfb'];
    prule.wlk := cjo.D['wlk'];
    prule.holestr := cjo.S['holestr'];
    prule.kcstr := cjo.S['kcstr'];
    prule.memo := cjo.S['memo'];
    prule.fbstr := cjo.S['fbstr'];
    prule.is_outline := cjo.I['is_outline'];
    prule.bh := cjo.I['bh'];

    prule.llfb := cjo.D['llfb'];
    prule.rrfb := cjo.D['rrfb'];
    prule.ddfb := cjo.D['ddfb'];
    prule.uufb := cjo.D['uufb'];
    prule.fb := cjo.D['fb'];

    key := cjo.S['key'];
    j := ruleHash.IndexOf(key);
    if j = -1 then
    begin
      list := TList.Create;
      ruleHash.AddObject(key, list);
    end
    else
      list := TList(ruleHash.Objects[j]);
    list.Add(prule);
  end;

  ja := jo.O['childbomHash'];
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pcbomrule);
    pcbomrule.id := cjo.I['id'];
    pcbomrule.name := cjo.S['name'];
    pcbomrule.mat := cjo.S['mat'];
    pcbomrule.color := cjo.S['color'];
    pcbomrule.lfb := cjo.D['lfb'];
    pcbomrule.llk := cjo.D['llk'];
    pcbomrule.wfb := cjo.D['wfb'];
    pcbomrule.wlk := cjo.D['wlk'];
    pcbomrule.holestr := cjo.S['holestr'];
    pcbomrule.kcstr := cjo.S['kcstr'];
    pcbomrule.memo := cjo.S['memo'];
    pcbomrule.ono := cjo.S['ono'];
    pcbomrule.bclass := cjo.S['bclass'];
    pcbomrule.fbstr := cjo.S['fbstr'];
    pcbomrule.bomstd := cjo.S['bomstd'];
    pcbomrule.bomtype := cjo.S['bomtype'];
    pcbomrule.a_face := cjo.S['a_face'];
    pcbomrule.b_face := cjo.S['b_face'];
    pcbomrule.bg_filename := cjo.S['bg_filename'];
    pcbomrule.mpr_filename := cjo.S['mpr_filename'];
    pcbomrule.bpp_filename := cjo.S['bpp_filename'];
    pcbomrule.devcode := cjo.S['devcode'];
    pcbomrule.direct_calctype := cjo.I['direct_calctype'];
    pcbomrule.workflow := cjo.S['workflow'];

    pcbomrule.l := cjo.S['l'];
    pcbomrule.p := cjo.S['p'];
    pcbomrule.h := cjo.S['h'];
    pcbomrule.q := cjo.I['q'];

    pcbomrule.llfb := cjo.D['llfb'];
    pcbomrule.rrfb := cjo.D['rrfb'];
    pcbomrule.ddfb := cjo.D['ddfb'];
    pcbomrule.uufb := cjo.D['uufb'];
    pcbomrule.fb := cjo.D['fb'];

    pcbomrule.lmax := cjo.I['lmax'];
    pcbomrule.lmin := cjo.I['lmin'];
    pcbomrule.dmax := cjo.I['dmax'];
    pcbomrule.dmin := cjo.I['dmin'];
    pcbomrule.hmax := cjo.I['hmax'];
    pcbomrule.hmin := cjo.I['hmin'];
    pcbomrule.deleted := cjo.B['deleted'];

    key := cjo.S['key'];
    j := childbomHash.IndexOf(key);
    if j = -1 then
    begin
      list := TList.Create;
      childbomHash.AddObject(pcbomrule.bclass, list);
    end
    else
      list := TList(childbomHash.Objects[j]);
    list.Add(pcbomrule);
  end;

  ja := jo.O['wjruleHash'];
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pwjrule);
    pwjrule.myclass1 := cjo.S['myclass1'];
    pwjrule.myclass2 := cjo.S['myclass2'];
    pwjrule.lmax := cjo.I['lmax'];
    pwjrule.lmin := cjo.I['lmin'];
    pwjrule.pmax := cjo.I['pmax'];
    pwjrule.pmin := cjo.I['pmin'];
    pwjrule.hmax := cjo.I['hmax'];
    pwjrule.hmin := cjo.I['hmin'];
    pwjrule.wjname := cjo.S['wjname'];
    pwjrule.wjno := cjo.S['wjno'];
    pwjrule.num := cjo.I['num'];
    pwjrule.myunit := cjo.S['myunit'];
    pwjrule.lgflag := cjo.I['lgflag'];
    pwjrule.myunit2 := cjo.S['myunit2'];
    pwjrule.mat := cjo.S['mat'];
    pwjrule.color := cjo.S['color'];
    pwjrule.wjid := cjo.I['wjid'];
    pwjrule.price := cjo.D['price'];

    key := cjo.S['key'];
    j := wjruleHash.IndexOf(key);
    if j = -1 then
    begin
      list := TList.Create;
      wjruleHash.AddObject(key, list);
    end
    else
      list := TList(wjruleHash.Objects[j]);
    list.Add(pwjrule);
  end;

  ja := jo.O['linecalcList'];
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    linecalcList.Add(cjo.S['name'], cjo.I['linemax']);
  end;

  ja := jo.O['holeconfigHash'];
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    phole := THoleConfig.Create;
    phole.id := cjo.I['id'];
    phole.name := cjo.S['name'];
    phole.flag := cjo.S['flag'];
    phole.flag2 := cjo.S['flag2'];
    phole.l_bigname := cjo.S['l_bigname'];
    phole.l_smallname := cjo.S['l_smallname'];
    phole.i_name := cjo.S['i_name'];
    phole.mx_name := cjo.S['mx_name'];
    phole.l_holedepth := cjo.I['l_holedepth'];
    phole.l_bigcap := cjo.I['l_bigcap'];
    phole.l_smallcap := cjo.I['l_smallcap'];
    phole.calctype := cjo.I['calctype'];
    phole.holecap := cjo.S['holecap'];
    phole.mx_calctype := cjo.I['mx_calctype'];
    phole.mx_cap := cjo.I['mx_cap'];
    phole.l_isoutput := cjo.I['l_isoutput'];
    phole.i_isoutput := cjo.I['i_isoutput'];
    phole.mx_isoutput := cjo.I['mx_isoutput'];
    phole.ismirror := cjo.I['ismirror'];

    phole.iscalc := cjo.I['iscalc'];
    phole.bigface := cjo.I['bigface'];
    phole.myface := cjo.I['myface'];

    phole.min := cjo.I['min'];
    phole.max := cjo.I['max'];
    phole.bh := cjo.I['bh'];

    phole.isoffset := cjo.I['isoffset'];
    phole.xo := cjo.S['xo'];
    phole.yo := cjo.S['yo'];
    phole.b_isoffset := cjo.I['b_isoffset'];
    phole.b_xo := cjo.S['b_xo'];
    phole.b_yo := cjo.S['b_yo'];

    phole.pkcap := cjo.I['pkcap'];
    phole.holenum := cjo.I['holenum'];

    phole.center_holenum := cjo.I['center_holenum'];
    phole.center_holecap := cjo.S['center_holecap'];

    phole.i_offsetvalue := cjo.D['i_offsetvalue'];

    phole.algorithm := cjo.I['algorithm'];
    key := cjo.S['key'];
    j := holeconfigHash.IndexOf(key);
    if j = -1 then
    begin
      list := TList.Create;
      holeconfigHash.AddObject(key, list);
    end
    else
      list := TList(holeconfigHash.Objects[j]);
    list.Add(phole);
  end;

  ja := jo.O['kcconfigHash'];
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    pkc := TKCConfig.Create;
    pkc.id := cjo.I['id'];
    pkc.name := cjo.S['name'];
    pkc.flag := cjo.S['flag'];
    pkc.myface := cjo.I['myface'];
    pkc.cutter := cjo.S['cutter'];

    pkc.min := cjo.I['min'];
    pkc.max := cjo.I['max'];
    pkc.x := cjo.I['x'];
    pkc.y := cjo.I['y'];
    pkc.l := cjo.I['l'];
    pkc.w := cjo.I['w'];
    pkc.device := cjo.I['device'];

    key := cjo.S['key'];
    j := kcconfigHash.IndexOf(key);
    if j = -1 then
    begin
      list := TList.Create;
      kcconfigHash.AddObject(key, list);
    end
    else
      list := TList(kcconfigHash.Objects[j]);
    list.Add(pkc);
  end;

  ja := jo.O['bomstdList'];
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pbs);
    pbs.myclass1 := cjo.S['myclass1'];
    pbs.myclass2 := cjo.S['myclass2'];
    pbs.lmax := cjo.I['lmax'];
    pbs.lmin := cjo.I['lmin'];
    pbs.dmax := cjo.I['dmax'];
    pbs.dmin := cjo.I['dmin'];
    pbs.hmax := cjo.I['hmax'];
    pbs.hmin := cjo.I['hmin'];
    pbs.stdflag := cjo.S['stdflag'];
    pbs.level := cjo.I['level'];
    bomstdList.Add(pbs);
  end;

  jo := nil;
  Result := 1;
end;

procedure TLocalObject.Des2Des(p: Pointer);
var
  M                 : ^StrMap;
  poi               : PBomOrderItem;
begin
  poi := p;
  if poi.desc='' then exit;
  M := des2wuliao.ValueOf(poi.desc, 1);
  if M=nil then //从数据库加载
  begin
    LoadOneBomData(poi.desc);
    M := des2wuliao.ValueOf(poi.desc, 1);
  end;
  if M <> nil then
  begin
    poi.desc := M.s1;
    poi.bomdes := M.s2;
    poi.bomwjdes := M.s3;
    //poi.code := m.no;
    poi.name := M.oname;
    poi.childbom := M.childbom;
    poi.myclass := M.bomclass;
    poi.linecalc := M.linecalc;
    poi.bomstddes := M.bomstd;
    poi.bomtype := M.bomtype;
    if M.linecalc <> '' then
    begin
      poi.linemax := linecalcList.ValueOf(poi.linecalc);
      if poi.linemax = -1 then poi.linecalc := '';
    end;
    if M.HoleConfig <> '' then poi.holeid := holeconfigHash.IndexOf(M.HoleConfig);
    if M.KCConfig <> '' then poi.kcid := kcconfigHash.IndexOf(M.KCConfig);

    poi.bg_filename := M.bg_filename;
    poi.mpr_filename := M.mpr_filename;
    poi.bpp_filename := M.bpp_filename;
    poi.devcode := M.devcode;
    poi.zero_y := M.zero_y;
    poi.direct_calctype := M.direct_calctype;
    poi.is_output_bgdata := M.is_output_bgdata;
    poi.is_output_mpr := M.is_output_mpr;
    poi.is_output_bpp := M.is_output_bpp;
    poi.youge_holecalc := M.youge_holecalc;
    poi.workflow := M.workflow;
  end;
end;

procedure TLocalObject.GraphSizeToBomSize(l, p, h, direct: Integer; var bl, bp,
  bh: Integer);
var
  t                 : Integer;
begin
  bl := l;
  bp := p;
  bh := h;
  if direct = 1 then                    //宽深高
  begin
    bl := l;
    bp := p;
    bh := h;
  end;
  if direct = 2 then                    //宽高深
  begin
    bl := l;
    bp := h;
    bh := p;
  end;
  if direct = 3 then                    //高宽深
  begin
    bl := h;
    bp := l;
    bh := p;
  end;
  if direct = 4 then                    //高深宽
  begin
    bl := h;
    bp := p;
    bh := l;
  end;
  if direct = 5 then                    //深宽高
  begin
    bl := p;
    bp := l;
    bh := h;
  end;
  if direct = 6 then                    //深高宽
  begin
    bl := p;
    bp := h;
    bh := l;
  end;
end;

function TLocalObject.TextureDirectChange(di: Integer): Integer;
begin
  Result := di;
  if di = 6 then Result := 4;
  if di = 2 then Result := 3;
  if di = 1 then Result := 5;
end;

function TLocalObject.ToBomStd(des: string; l, p, h: Integer): string;
var
  i                 : Integer;
  pbs               : PBomStd;
begin
  Result := '';
  for i := 0 to bomstdList.Count - 1 do
  begin
    pbs := bomstdList[i];
    if (pbs.myclass1 + ',' + pbs.myclass2) = des then
    begin
      if (pbs.lmax >= l) and (pbs.lmin <= l) and (pbs.dmax >= p)
        and (pbs.dmin <= p) and (pbs.hmax >= h) and (pbs.hmin <= h) then
      begin
        Result := pbs.stdflag;
        exit;
      end;
    end;
  end;
end;

procedure FBStr2Value(str: string; var l, w, llfb, rrfb, ddfb, uufb, ffb: double; var fb: string);
var
  n                 : Integer;
  wstr              : WideString;
  s                 : string;
begin
  wstr := str;
  n := Pos(WideString(','), wstr);
  if n > 0 then
  begin
    s := LeftStr(wstr, n - 1);
    l := MyStrToFloat(s);
    wstr := RightStr(wstr, Length(wstr) - n);
  end;
  n := Pos(WideString(','), wstr);
  if n > 0 then
  begin
    s := LeftStr(wstr, n - 1);
    w := MyStrToFloat(s);
    wstr := RightStr(wstr, Length(wstr) - n);
  end;
  n := Pos(WideString(','), wstr);
  if n > 0 then
  begin
    s := LeftStr(wstr, n - 1);
    llfb := MyStrToFloat(s);
    wstr := RightStr(wstr, Length(wstr) - n);
  end;
  n := Pos(WideString(','), wstr);
  if n > 0 then
  begin
    s := LeftStr(wstr, n - 1);
    rrfb := MyStrToFloat(s);
    wstr := RightStr(wstr, Length(wstr) - n);
  end;
  n := Pos(WideString(','), wstr);
  if n > 0 then
  begin
    s := LeftStr(wstr, n - 1);
    ddfb := MyStrToFloat(s);
    wstr := RightStr(wstr, Length(wstr) - n);
  end;
  n := Pos(WideString(','), wstr);
  if n > 0 then
  begin
    s := LeftStr(wstr, n - 1);
    uufb := MyStrToFloat(s);
    wstr := RightStr(wstr, Length(wstr) - n);
  end;
  n := Pos(WideString(','), wstr);
  if n > 0 then
  begin
    s := LeftStr(wstr, n - 1);
    ffb := MyStrToFloat(s);
    wstr := RightStr(wstr, Length(wstr) - n);
  end;
  fb := wstr;
end;

function TLocalObject.ImportXomItemForBom(param0: PBomParam; var id, slino: Integer): Integer;
var
  root, node, cnode, attri: IXMLNode;
  i, di, bp, bl, bh, childnum, k, autodirect: Integer;
  xx0, xx1, yy0, yy1, zz0, zz1: Integer;
  tmp_space_x, tmp_space_y, tmp_space_z: Integer;
  program_str, sizeprogram_str, value, vname, childxml, tmp_subspace, tmp_soz, textureclass, spaceflag: string;
  exp               : TExpress;
  poi               : PBomOrderItem;
  pslibom           : PSlidingBomRecord;
  sliw, slih, doorw, doorh: Real;
  doornum           : Integer;
  isdoor            : boolean;
  str, bg, dtype    : string;
  args              : array[0..15] of Integer;
  ls, varstr        : string;           //拉手信息
  DoorItem          : TDoorItem;
  product_item      : TProductItem;
  real_d, real_l, t : double;
  param             : BomParam;
  jo:ISuperObject;
begin
  Result := 0;
  //if (param0.outputtype = '报价') {or (param0.outputtype = '无')} then exit;

  ls := '';
  exp := TExpress.Create;
  exp.AddVariable('L', '', IntToStr(param0.pl), '', '');
  exp.AddVariable('P', '', IntToStr(param0.pd), '', '');
  exp.AddVariable('H', '', IntToStr(param0.ph), '', '');
  exp.AddVariable('BH', '', IntToStr(param0.boardheight), '', '');
  exp.mBHValue := param0.boardheight;
  param.blockmemo := '';

  isdoor := False;
  try
    root :=  param0.rootnode;
    str := GetAttributeValue(root, '模块备注', '', '');
    if (str <> '') then
    begin
      param0.blockmemo := str;
      param0.blockmemo := StringReplace(param0.blockmemo, '[宽]', IntToStr(param0.pl), [rfReplaceAll]);
      param0.blockmemo := StringReplace(param0.blockmemo, '[深]', IntToStr(param0.pd), [rfReplaceAll]);
      param0.blockmemo := StringReplace(param0.blockmemo, '[高]', IntToStr(param0.ph), [rfReplaceAll]);
    end;

    str := GetAttributeValue(root, '类别', '', '');
    if (str = '趟门,趟门') or (str = '掩门,掩门') then
    begin
      node := root.ChildNodes.FindNode('模板');
      if node<>nil then
      begin
        childxml := '';
        if (node.ChildNodes.Count > 0) then childxml := node.ChildNodes[0].xml;
        if (str = '趟门,趟门') then ImportSlidingXomItemForBom(param0.cid, param0.boardheight,param0.mark
          , param0.blist, root.XML, param0.gno, param0.gdes, param0.gcb, param0.extra, param0.pname, param0.subspace, childxml
          , param0.pmat, param0.pcolor, param0.pid, param0.pl, param0.pd, param0.ph, id, slino, param0.px
          , param0.py, param0.pz, param0.outputtype);
        if (str = '掩门,掩门') then ImportDoorsXomItemForBom(param0.cid, param0.boardheight,param0.mark, param0.blist
          , root.XML, param0.gno, param0.gdes, param0.gcb, param0.extra, param0.pname, param0.subspace, childxml, param0.pmat, param0.pcolor
          , param0.pid, param0.pl, param0.pd, param0.ph, id, slino, param0.px, param0.py, param0.pz, param0.outputtype);
        exit;
      end;
    end;

    node := root.ChildNodes.FindNode('BDXML');
    if node <> nil then
    begin
      for i := 0 to node.ChildNodes.Count - 1 do
      begin
        cnode := node.ChildNodes[i];
        if cnode.ChildNodes.Count <= 0 then
          mBDXMLList.Add(cnode.nodename, cnode.Text)
        else
          mBDXMLList.Add(cnode.nodename, cnode.ChildNodes[0].xml);
      end;
    end;

    node := root.ChildNodes.FindNode('变量列表');
    if node <> nil then
    begin
      for i := 0 to node.ChildNodes.Count - 1 do
      begin
        cnode := node.ChildNodes[i];
        vname := GetAttributeValue(cnode, '名称', '', '');
        value := GetAttributeValue(cnode, '值', '', '');
        SetSysVariantValue(vname, value);
        exp.AddVariable(vname, '', value, '', '');
      end;
    end;

    node := root.ChildNodes.FindNode('我的模块');
    if (node <> nil) and (not isdoor) then
    begin
      for i := 0 to node.ChildNodes.Count - 1 do
      begin
        cnode := node.ChildNodes[i];
        if (cnode.nodename <> '板件') and (cnode.nodename <> '五金') and (cnode.nodename <> '型材五金')
          and (cnode.nodename <> '模块') and (cnode.nodename <> '门板') then Continue;
        program_str := GetAttributeValue(cnode, 'Program', '', '');

        bg := GetAttributeValue(cnode, '基础图形', '', '');
        if (bg = 'BG::SPACE') then Continue;
        str := GetAttributeValue(cnode, '显示方式', '', '');
        if (str = '3') then Continue;

        NewBomOrderItem(poi);
        if cnode.nodename = '板件' then poi.myunit := '块';
        tmp_space_x := param0.space_x;
        tmp_space_y := param0.space_y;
        tmp_space_z := param0.space_z;

        textureclass := GetAttributeValue(cnode, '装饰类别', '', '');

        poi.number_text := GetAttributeValue(cnode, 'NumberText', '', '');
        if (poi.number_text='') then poi.number_text := param0.number_text;

        poi.pl := param0.pl;
        poi.pd := param0.pd;
        poi.ph := param0.ph;
        poi.bg := bg;
        poi.holeid := -1;               //打孔id
        poi.kcid := -1;                 //开槽id
        poi.cid := param0.cid;
        poi.isoutput := True;
        InitVarArgs(poi.var_args, poi.var_names);
        poi.nodename := cnode.nodename;
        poi.id := id;
        poi.pid := param0.pid;
        poi.subspace := param0.subspace;
        poi.space_x := param0.space_x;
        poi.space_y := param0.space_y;
        poi.space_z := param0.space_z;
        poi.space_id := param0.space_id;
        poi.parent := param0.parent;
        tmp_subspace := GetAttributeValue(cnode, '子空间', '', '');
        if tmp_subspace = 'A' then tmp_subspace := '';
        poi.subspace := param0.subspace + tmp_subspace;
        if tmp_subspace <> '' then poi.isoutput := False;

        poi.name := GetAttributeValue(cnode, '名称', '', '');
        varstr := '';
        poi.x := param0.px + 0;
        poi.y := param0.py + 0;
        poi.z := param0.pz + 0;

        xx0 := GetAttributeValue(cnode, 'XX0', 0, 0);
        xx1 := GetAttributeValue(cnode, 'XX1', 0, 0);
        yy0 := GetAttributeValue(cnode, 'YY0', 0, 0);
        yy1 := GetAttributeValue(cnode, 'YY1', 0, 0);
        zz0 := GetAttributeValue(cnode, 'ZZ0', 0, 0);
        zz1 := GetAttributeValue(cnode, 'ZZ1', 0, 0);

        varstr := GetAttributeValue(cnode, 'X', '', '');
        exp.SetSubject(varstr);
        poi.lx := exp.ToValueInt + xx0;
        poi.x := param0.px + poi.lx;

        varstr := GetAttributeValue(cnode, 'Y', '', '');
        exp.SetSubject(varstr);
        poi.ly := exp.ToValueInt + yy0;
        poi.y := param0.py + poi.ly;

        varstr := GetAttributeValue(cnode, 'Z', '', '');
        exp.SetSubject(varstr);
        poi.lz := exp.ToValueInt + zz0;
        poi.z := param0.pz + poi.lz;

        poi.ox := GetAttributeValue(cnode, 'OX', 0.0, 0.0);
        poi.oy := GetAttributeValue(cnode, 'OY', 0.0, 0.0);
        poi.oz := GetAttributeValue(cnode, 'OZ', 0.0, 0.0);

        varstr := GetAttributeValue(cnode, '宽', '', '');
        exp.SetSubject(varstr);
        poi.l := exp.ToValueInt + xx1 + (0 - xx0);
        if (tmp_subspace <> '') then
        begin
          tmp_space_x := poi.x;
          tmp_space_y := poi.y;
          tmp_space_z := poi.z;
        end;
        if (tmp_subspace = 'B') or (tmp_subspace = 'C') then
        begin
          product_item := mProductList[param0.cid];
          product_item.l := product_item.l + poi.l;
        end;

        varstr := GetAttributeValue(cnode, 'GCL', '0', '0');
        poi.gcl := MyStrToInt(varstr);
        poi.gcl2 := poi.gcl;
        varstr := GetAttributeValue(cnode, 'GCD', '0', '0');
        poi.gcd := MyStrToInt(varstr);
        poi.gcd2 := poi.gcd;
        varstr := GetAttributeValue(cnode, 'GCH', '0', '0');
        poi.gch := MyStrToInt(varstr);
        poi.gch2 := poi.gch;

        varstr := GetAttributeValue(cnode, '深', '', '');
        exp.SetSubject(varstr);
        poi.p := exp.ToValueInt + yy1 + (0 - yy0);

        varstr := GetAttributeValue(cnode, '高', '', '');
        exp.SetSubject(varstr);
        poi.h := exp.ToValueInt + zz1 + (0 - zz0);

        poi.holeflag := 0;
        str := GetAttributeValue(cnode, 'HoleFlag', '', '');
        if str<>'' then
        begin
          exp.SetSubject(str);
          poi.holeflag := exp.ToValueInt;
        end;
        for k := 0 to 15 do             //所有16个参数
        begin
          args[k] := 0;
          str := GetAttributeValue(cnode, '参数' + IntToStr(k), '', '');
          if (str <> '') then
          begin
            MyVariant(str, vname, value);
            exp.SetSubject(value);
            args[k] := exp.ToValueInt;
            poi.var_args[k] := args[k];
            poi.var_names[k] := vname;
            varstr := varstr + '+' + vname;
          end;
        end;
        //size高级编程
        sizeprogram_str := GetAttributeValue(cnode, 'SizeProgram', '', '');
        if ExtractFileExt(sizeprogram_str)='.lua' then
        begin
          sizeprogram_str := LuaData.ValueOf(sizeprogram_str);
          jo := SO(Format('{"X":"%d","Y":"%d","Z":"%d","L":"%d","D":"%d","H":"%d","OZ":"%f"}', [poi.x, poi.y, poi.z, poi.l, poi.p, poi.h, poi.oz]));
          for k:=0 to 15 do
          begin
            jo.I['C'+IntToStr(k)] := poi.var_args[k];
          end;
          str := CompileLuaProgram(jo, sizeprogram_str);
          jo := SO(str);
          if jo<>nil then
          begin
            poi.x := jo.I['X'];
            poi.y := jo.I['Y'];
            poi.z := jo.I['Z'];
            poi.l := jo.I['L'];
            poi.p := jo.I['D'];
            poi.h := jo.I['H'];
            poi.oz := jo.D['OZ'];
          end;
        end;

        attri := cnode.AttributeNodes.FindNode('DI');
        if attri <> nil then di := StrToInt(attri.Text);
        poi.direct := di;
        attri := cnode.AttributeNodes.FindNode('材料');
        if attri <> nil then poi.mat := attri.Text else if textureclass=param0.textureclass then poi.mat := param0.pmat;
        attri := cnode.AttributeNodes.FindNode('颜色');
        if attri <> nil then poi.color := attri.Text else if textureclass=param0.textureclass then poi.color := param0.pcolor;
        attri := cnode.AttributeNodes.FindNode('类别');
        if attri <> nil then poi.desc := attri.Text;
        attri := cnode.AttributeNodes.FindNode('编码');
        if attri <> nil then poi.code := attri.Text;
        attri := cnode.AttributeNodes.FindNode('工艺');
        if attri <> nil then poi.process := attri.Text;
        attri := cnode.AttributeNodes.FindNode('UI');
        if (attri <> nil) then
        begin
          if attri.Text = '拉手' then
            ls := ls + poi.name + ',';
          if attri.Text = '拉手集合' then
          begin
            poi.memo := poi.memo + ls;
            poi.ls := ls;
          end;
        end;
        poi.lgflag := 0;
        attri := cnode.AttributeNodes.FindNode('LgwjFlag');
        if (attri <> nil) and (attri.Text = '1') then poi.lgflag := 1;
        poi.holetype := 0;
        attri := cnode.AttributeNodes.FindNode('HoleType');
        if (attri <> nil) and (attri.Text <> '') then poi.holetype := MyStrToInt(attri.Text);
        attri := cnode.AttributeNodes.FindNode('AutoDirect');
        if (attri <> nil) and (attri.Text <> '') then
          autodirect := MyStrToInt(attri.Text)
        else
          autodirect := 0;
        attri := cnode.AttributeNodes.FindNode('HC'); //动态判定HoleConfig是否要计算
        if attri <> nil then SetIsCalcHoleConfig(poi, attri.Text);
        attri := cnode.AttributeNodes.FindNode('BDXMLID');
        if (attri <> nil) and (attri.Text <> '') then poi.bdxmlid := attri.Text;
        attri := cnode.AttributeNodes.FindNode('HI');
        if (attri <> nil) and (attri.Text <> '') then poi.holeinfo := MyUtils.URLDecode(attri.Text);
        attri := cnode.AttributeNodes.FindNode('Extend');
        if (attri <> nil) and (attri.Text <> '') then poi.extend := MyUtils.URLDecode(attri.Text);
        attri := cnode.AttributeNodes.FindNode('Group');
        if (attri <> nil) and (attri.Text <> '') then poi.group := Format('%s-%s', [attri.Text, MyUtils.GetGUID]);
        attri := cnode.AttributeNodes.FindNode('图形参数');
        if (attri <> nil) and (attri.Text <> '') then SetBGParam(poi, attri.Text);

        poi.lfb := 0;
        poi.llk := 0;
        poi.wfb := 0;
        poi.wlk := 0;
        poi.gno := param0.gno;
        poi.gdes := param0.gdes;
        poi.gcb := param0.gcb;
        poi.extra := param0.extra;
        attri := cnode.AttributeNodes.FindNode('FBSTR');
        if attri <> nil then poi.user_fbstr := attri.Text;
        if (poi.user_fbstr <> '') then FBStr2Value(poi.user_fbstr, poi.llk, poi.wlk, poi.llfb, poi.rrfb, poi.ddfb, poi.uufb, poi.fb, poi.fbstr);

        poi.value_lsk := 0;
        poi.value_rsk := 0;
        poi.value_zk := 0;
        poi.value_zs := 0;
        poi.value_ls := 0;
        poi.value_lg := 0;
        poi.value_ltm := 0;
        poi.value_rtm := 0;
        SetSysVariantValueForOrderItem(varstr, poi);

        childxml := '';
        if cnode.ChildNodes.Count > 0 then childxml := cnode.ChildNodes[0].xml;
        childnum := 0;
        poi.num := 1;
        attri := cnode.AttributeNodes.FindNode('Num');
        if (attri <> nil) and (attri.Text <> '') then poi.num := MyStrToInt(attri.Text) * param0.num;
        attri := cnode.AttributeNodes.FindNode('Mark');
        if (attri <> nil) and (attri.Text <> '') then poi.mark := MyStrToInt(attri.Text)
        else poi.mark:=0;
        attri := cnode.AttributeNodes.FindNode('Memo');
        if (attri <> nil) and (attri.Text <> '') then poi.memo := attri.Text;
        attri := cnode.AttributeNodes.FindNode('UD');
        if (attri <> nil) and (attri.Text <> '') then poi.userdefine := attri.Text;
        poi.holestr := '';
        poi.kcstr := '';
        attri := cnode.AttributeNodes.FindNode('VP');
        if (attri <> nil) and (attri.Text <> '') then poi.vp := MyStrToInt(attri.Text);
        poi.blockmemo := '';

        Result := Result + 1;
        Des2Des(poi);
        param0.blist.Add(poi);
        inc(id);

        real_l := poi.l;
        real_d := poi.p;
        if (tmp_subspace = 'L') then    //L面空间，进行旋转计算
        begin
          if (poi.var_args[0] = 1) then
          begin
            poi.oz := arctan((real_d - poi.var_args[2]) / (real_l - poi.var_args[1])) / PI * 180; //旋转角度
            poi.p := poi.var_args[3];   //深度
            t := sqrt((real_l - poi.var_args[1]) * (real_l - poi.var_args[1]) + (real_d - poi.var_args[2]) * (real_d - poi.var_args[2]));
            poi.l := Round(t);          //宽度
            poi.x := Round(poi.var_args[1] - poi.var_args[3] * (real_d - poi.var_args[2]) / t); //x
            poi.y := Round(real_d - poi.var_args[3] * (real_l - poi.var_args[1]) / t); //y
            if poi.var_args[4] <> 0 then poi.l := poi.var_args[4];
            poi.lx := poi.x;
            poi.ly := poi.y;
          end
          else
          begin
            poi.oz := 0;
          end;
        end;
        if (tmp_subspace = 'R') then    //R面空间，进行旋转计算
        begin
          if (poi.var_args[0] = 1) then
          begin
            poi.oz := -arctan((real_d - poi.var_args[2]) / (real_l - poi.var_args[1])) / PI * 180;
            poi.p := poi.var_args[3];
            t := sqrt((real_l - poi.var_args[1]) * (real_l - poi.var_args[1]) + (real_d - poi.var_args[2]) * (real_d - poi.var_args[2]));
            poi.l := Round(t);          //宽度
            poi.x := poi.x + Round(poi.var_args[3] * (real_d - poi.var_args[2]) / t); //x
            poi.y := Round(poi.var_args[2] - poi.var_args[3] * (real_l - poi.var_args[1]) / t); //y
            if poi.var_args[4] <> 0 then poi.l := poi.var_args[4];
            poi.lx := poi.x;
            poi.ly := poi.y;
          end
          else
          begin
            poi.oz := 0;
          end;
        end;

        poi.tmp_soz := param0.sozflag;
        tmp_soz := param0.sozflag;
        if tmp_subspace <> '' then tmp_soz := '';
        if (tmp_subspace = '') and (Trunc(poi.oz) <> 0) then tmp_soz := param0.sozflag + Format('@%d_%d', [Integer(poi), Trunc(poi.oz)]);

        childnum := 0;
        if childxml <> '' then
        begin
          spaceflag := GetAttributeValue(cnode, 'SpaceFlag', '', '');

          param := param0^;
          param.pname := poi.name;
          param.subspace := poi.subspace;
          param.sozflag := tmp_soz;
          param.xml := childxml;
          param.textureclass := textureclass;
          param.pmat := poi.mat;
          param.pcolor := poi.color;
          param.pid := id - 1;
          param.mark := poi.mark;
          param.pl := poi.l;
          param.pd := poi.p;
          param.ph := poi.h;
          param.px := poi.x;
          param.py := poi.y;
          param.pz := poi.z;
          param.space_x := tmp_space_x;
          param.space_y := tmp_space_y;
          param.space_z := tmp_space_z;
          if spaceflag='1' then param.space_id := poi.id else param.space_id := param0.space_id;
          param.num := poi.num;
          param.parent := poi;
          if poi.group<>'' then param.group := poi.group;
          if poi.blockmemo<>'' then param.blockmemo := poi.blockmemo;
          if poi.number_text<>'' then param.number_text := poi.number_text;
          attri := cnode.AttributeNodes.FindNode('输出类型');
          if (attri <> nil) and (attri.Text <> '') then param.outputtype := attri.Text;
          if cnode.ChildNodes.Count>0 then
          begin
            param.rootnode := cnode.ChildNodes[0];
            param.xdoc := param0.xdoc;
            childnum := ImportXomItemForBom(@param, id, slino);
          end;
        end;
        if poi.group='' then poi.group := param0.group;
        poi.blockmemo := param0.blockmemo;
        if program_str <> '' then       //产生克隆模块
        begin
          ImportCloneItemForBom(exp, program_str, poi, cnode, param0, id, slino);
        end;
        GraphSizeToBomSize(poi.l, poi.p, poi.h, di, bl, bp, bh);
        GraphSizeToBomSize(poi.gcl, poi.gcd, poi.gch, di, poi.gcl2, poi.gcd2, poi.gch2);
        if (autodirect = 1) and (bp > 1220) then //自动纹路转换
        begin
          di := TextureDirectChange(di);
          poi.direct := di;
          GraphSizeToBomSize(poi.l, poi.p, poi.h, di, bl, bp, bh);
          GraphSizeToBomSize(poi.gcl, poi.gcd, poi.gch, di, poi.gcl2, poi.gcd2, poi.gch2);
        end;
        poi.gl := poi.l;                 //xml数据
        poi.gp := poi.p;
        poi.gh := poi.h;

        poi.l := bl;                    //纹路转换后的数据
        poi.p := bp;
        poi.h := bh;
        poi.bl := bl - poi.lfb - poi.llk;           //去除封边后的数据
        poi.bp := bp - poi.wfb - poi.wlk;
        poi.bh := bh;
        poi.childnum := childnum;
        attri := cnode.AttributeNodes.FindNode('装饰类别');
        if (attri <> nil) and ((attri.Text = '趟门') or (attri.Text = '掩门') or (poi.myclass = '趟门,趟门') or (poi.myclass = '掩门,掩门')) then
          poi.isoutput := False;

        if (poi.bl < 1) or (poi.bp < 1) or (poi.bh < 1) then poi.isoutput := False; //过滤掉尺寸小于等于零的物料，xml情况复杂
        if (poi.bl > 1) and (poi.bp > 1) and (poi.bh <= 1) then poi.isoutput := False; //过滤掉一些尺寸为0的物料数据

        //尺寸判定
        poi.bomstd := ToBomStd(poi.bomstddes, poi.l, poi.p, poi.h);
        if childnum > 0 then poi.isoutput := False;

        attri := cnode.AttributeNodes.FindNode('输出类型');
        if attri <> nil then poi.outputtype := attri.Text;
      end;
    end;
  finally
    if Assigned(exp) then FreeAndNil(exp);
  end;
end;

procedure TLocalObject.LoadXML2Bom(xml: string);
var
  cid, id, i, j, l, d, h, bh, slino: Integer;
  name, mat, color, des, gcb, extra, spaceflag: string;
  root, node, cnode, attri: IXMLNode;
  p                 : TProductItem;
  poi, poi2         : PBomOrderItem;
  fs                : TFileStream;
  param             : BomParam;
  xdoc:IXMLDocument;
begin
  id := 1;
  slino := 1;
  UnloadBom(False);
  if not Assigned(bomlist) then bomlist := TList.Create;
  if not Assigned(basewjlist) then basewjlist := TList.Create;
  if not Assigned(slidinglist) then slidinglist := TList.Create;
  if not Assigned(doorslist) then doorslist := TList.Create;

  mBG := '';
  try
    xdoc := XMLDoc.LoadXMLData('<?xml version="1.0" encoding="gb2312"?>'+xml);
    node := xdoc.ChildNodes[1];   //第一级产品节点
    RemoveInvisibleNode(node);

    cid := 0;
    if (node.nodename <> '产品') or (node.ChildNodes.Count <= 0) then exit;

    InitSysVariantValue;              //初始化系统变量
    name := '';
    l := 0;
    d := 0;
    h := 0;
    bh := 18;
    mat := '';
    color := '';
    des := '';
    gcb := '';
    extra := '';
    if node.ChildNodes[0].nodename = '产品' then
    begin
      bh := GetAttributeValue(node.ChildNodes[0], '板材厚度', bh, bh);
      extra := GetAttributeValue(node.ChildNodes[0], 'Extra', '', '');
    end;
    attri := node.AttributeNodes.FindNode('名称');
    if attri <> nil then name := attri.Text;
      attri := node.AttributeNodes.FindNode('描述');
    if attri <> nil then des := attri.Text;
    attri := node.AttributeNodes.FindNode('CB'); //厂编
    if attri <> nil then gcb := attri.Text;
    attri := node.AttributeNodes.FindNode('宽');
    if attri <> nil then
      l := StrToInt(attri.Text);
    attri := node.AttributeNodes.FindNode('深');
    if attri <> nil then
      d := StrToInt(attri.Text);
    attri := node.AttributeNodes.FindNode('高');
    if attri <> nil then
      h := StrToInt(attri.Text);
    attri := node.AttributeNodes.FindNode('材料');
    if attri <> nil then
      mat := attri.Text;
    attri := node.AttributeNodes.FindNode('颜色');
    if attri <> nil then
      color := attri.Text;
    attri := node.AttributeNodes.FindNode('基础图形');
    if attri <> nil then
      mBG := attri.Text;
    spaceflag := GetAttributeValue(node, 'SpaceFlag', '', '');
    for j := 0 to 15 do
    begin
      mVName[j] := '';
      mVValue[j] := '';
      mC[j] := 0;
      attri := node.AttributeNodes.FindNode('参数' + IntToStr(j));
      if attri <> nil then
        MyVariant(attri.Text, mVName[i], mVValue[j]);
      mC[j] := MyStrToInt(mVValue[j]);
    end;
    p := TProductItem.Create;
    p.id := cid;
    p.name := name;
    p.gno := name;
    p.mat := mat;
    p.color := color;
    p.des := des;
    p.gcb := gcb;
    p.Extra := extra;
    p.l := l;
    p.d := d;
    p.h := h;
    p.bh := bh;
    inc(cid);
    mProductList.Add(p);

    param.productid := mProductList.Count-1;
    param.cid := cid - 1;
    param.boardheight := bh;
    param.blist := bomlist;
    param.gno := name;
    param.gdes := des;
    param.gcb := gcb;
    param.extra := extra;
    param.pname := '';
    param.subspace := '';
    param.sozflag := '';
    param.xml := node.ChildNodes[0].xml;
    param.textureclass := '';
    param.pmat := mat;
    param.pcolor := color;
    param.pid := -1;
    param.pl := l;
    param.pd := d;
    param.ph := h;
    param.px := 0;
    param.py := 0;
    param.pz := 0;
    param.space_x := 0;
    param.space_y := 0;
    param.space_z := 0;
    if spaceflag='1' then param.space_id := 0 else param.space_id := -1;
    param.outputtype := '';
    param.num := 1;
    param.parent := nil;
    param.blockmemo := '';
    param.number_text := '';
    param.rootnode := node.ChildNodes[0];
    param.xdoc := xdoc;
    ImportXomItemForBom(@param, id, slino);

    //拆分数量
    for i := bomlist.Count - 1 downto 0 do
    begin
      poi := bomlist[i];
      if poi.num > 1 then
      begin
        for j := 1 to poi.num - 1 do
        begin
          new(poi2);
          poi2^ := poi^;
          poi2.num := 1;
          bomlist.Add(poi2);
        end;
        poi.num := 1;
      end;
    end;

  finally
    xdoc := nil;
  end;
end;

function TLocalObject.ImportSlidingXomItemForBom(cid, boardheight, mark: Integer; blist: TList; blockxml, gno,
  gdes, gcb, extra, pname, subspace, xml, pmat, pcolor: string; pid, pl, pd,
  ph: Integer; var id, slino: Integer; px, py, pz: Integer; outputtype: string): Integer;
var
  i, di, bp, bl, bh, childnum, k: Integer;
  value, vname, childxml, doorextra: string;
  poi               : PBomOrderItem;
  pslibom           : PSlidingBomRecord;
  sliw, slih, doorw, doorh: Real;
  doornum           : Integer;
  isdoor            : boolean;
  str, bg, dtype    : string;
  ls, varstr        : string;           //拉手信息
  DoorItem          : TDoorItem;
  jo, ja, cjo:ISuperObject;
  pbuf:pchar;
  js, objstr:string;
begin
  Result := 0;
  exit;
  if (outputtype = '报价') {or (outputtype = '无')} then exit;

  ls := '';
  if Assigned(mPluginHost) then
  begin
    jo := TSuperObject.Create();
    jo.S['XML'] := xml;
    jo.I['L'] := pl;
    jo.I['H'] := ph;
    jo.I['DoorType'] := 1;
    objstr := jo.AsString;
    jo := nil;
    js := Format('OnUpdateDoorTemplate("%s");', [MyUtils.EncodeJSVariant(objstr)]);
    objstr := mPluginHost.GetBrowserWindowObject.Evaluate(pchar(js));
    if objstr<>'' then
    begin
      jo := SO(objstr);
      xml := jo.S['XML'];
    end;
    jo := nil;
  end;
  pbuf:=nil;
  //pbuf := Sli_XmlTemplate2Json(gSlidingWin, pchar(xml), pl, ph);

  if Assigned(mPluginHost) then
  begin
    jo := TSuperObject.Create();
    jo.I['DoorType'] := 1;
    objstr := jo.AsString;
    jo := nil;
    js := Format('OnUpdateDoorBomObject("%s", "%s");', [MyUtils.EncodeJSVariant(xml), MyUtils.EncodeJSVariant(objstr)]);
    objstr := mPluginHost.GetBrowserWindowObject.Evaluate(pchar(js));
    if objstr<>'' then
    begin
      pbuf := pchar(objstr);
    end;
  end;
  if pbuf=nil then
  begin
    //ShowMessage('推拉门数据丢失');
    exit;
  end;
  mXMLStringList.Add(xml);
  isdoor := False;

  try
    isdoor := True;
    jo := SO(string(pbuf));
    dtype := jo.S['门款类型'];
    sliw := jo.D['门洞宽'];
    slih := jo.D['门洞高'];
    doorw := jo.D['成品门宽'];
    doorh := jo.D['成品门高'];
    doornum := jo.I['扇数'];
    doorextra := jo.S['DoorExtra'];

    ja := jo.O['物料'];
    for i:=0 to ja.AsArray.Length-1 do
    begin
      cjo := ja.AsArray.O[i];
      new(pslibom);
      pslibom.xmlindex := mXMLStringList.Count - 1;
      pslibom.cid := cid;
      pslibom.slino := slino;
      pslibom.subspace := subspace;
      pslibom.id := id;
      pslibom.pid := pid;
      pslibom.space_id := -1;

      pslibom.sliw := sliw;
      pslibom.slih := slih;
      pslibom.doorw := doorw;
      pslibom.doorh := doorh;
      pslibom.doornum := doornum;
      pslibom.gno := gno;
      pslibom.gdes := gdes;
      pslibom.dtype := dtype;
      pslibom.gcb := gcb;
      pslibom.extra := extra;
      pslibom.mark := mark;

      pslibom.code := cjo.S['Code'];
      pslibom.name := cjo.S['Name'];
      pslibom.mat := cjo.S['Name'];
      pslibom.color := cjo.S['Color'];
      pslibom.l := cjo.D['L'];
      pslibom.p := cjo.D['W'];
      pslibom.h := cjo.D['H'];
      pslibom.num := cjo.I['Num'];
      pslibom.group := cjo.S['Group'];
      pslibom.myunit := cjo.S['Unit'];
      pslibom.doorname := cjo.S['DoorName'];
      pslibom.bomtype := cjo.S['Bomtype'];
      pslibom.memo := cjo.S['Memo'];
      pslibom.memo2 := cjo.S['Memo2'];
      pslibom.memo3 := cjo.S['Memo3'];
      pslibom.bdfile := cjo.S['BDFILE'];
      pslibom.doormemo := cjo.S['DoorMemo'];
      pslibom.door_index := cjo.I['DoorIndex'];
      pslibom.isglass := cjo.I['Glass'];
      pslibom.is_buy := cjo.I['IsBuy'];
      pslibom.direct := cjo.S['Di'];
      pslibom.fbstr := cjo.S['FBStr'];
      pslibom.bdxmlid := cjo.S['BDXMLID'];
      if pslibom.bdxmlid<>'' then
      begin
        mBDXMLList.Add(pslibom.bdxmlid, cjo.S['BDXML']);
      end;
      slidinglist.Add(pslibom);
      inc(id);
      cjo := nil;
    end;
    ja := nil;
    DoorItem := TDoorItem.Create;
    DoorItem.name := '';
    DoorItem.gno := gno;
    DoorItem.des := gdes;
    DoorItem.gcb := gcb;
    DoorItem.extra := extra;
    DoorItem.slino := slino;
    DoorItem.l := sliw;
    DoorItem.h := slih;
    DoorItem.d := 0;
    DoorItem.one_l := doorw;
    DoorItem.one_h := doorh;
    DoorItem.num := doornum;
    DoorItem.doorextra := doorextra;
    DoorItem.isframe := 1;
    DoorItem.doortype := '趟门';
    DoorItem.xmlindex := mXMLStringList.Count - 1;
    DoorItem.xml := blockxml;
    mDoorList.Add(DoorItem);
    inc(slino);
  finally
    jo := nil;
  end;
end;

function TLocalObject.ImportDoorsXomItemForBom(cid, boardheight, mark: Integer; blist: TList; blockxml, gno, gdes, gcb, extra,
  pname, subspace, xml, pmat, pcolor: string; pid, pl, pd, ph: Integer;
  var id, slino: Integer; px, py, pz: Integer; outputtype: string): Integer;
var
  i, di, bp, bl, bh, childnum, k: Integer;
  value, vname, childxml: string;
  poi               : PBomOrderItem;
  pslibom           : PSlidingBomRecord;
  sliw, slih, doorw, doorh: Real;
  doornum, isframe  : Integer;
  isdoor            : boolean;
  str, bg, dtype    : string;
  ls, varstr, extend, hingehole, doormemo, doorextra        : string;           //拉手信息
  DoorItem          : TDoorItem;
  jo, ja, cjo:ISuperObject;
  pbuf:pchar;
  js, objstr:string;
begin
  Result := 0;
  exit;
  if (outputtype = '报价') {or (outputtype = '无')} then exit;

  ls := '';
  if Assigned(mPluginHost) then
  begin
    jo := TSuperObject.Create();
    jo.S['XML'] := xml;
    jo.I['L'] := pl;
    jo.I['H'] := ph;
    jo.I['DoorType'] := 2;
    objstr := jo.AsString;
    jo := nil;
    js := Format('OnUpdateDoorTemplate("%s");', [MyUtils.EncodeJSVariant(objstr)]);
    objstr := mPluginHost.GetBrowserWindowObject.Evaluate(pchar(js));
    if objstr<>'' then
    begin
      jo := SO(objstr);
      xml := jo.S['XML'];
    end;
    jo := nil;
  end;
  pbuf := nil;
  //pbuf := Doors_XmlTemplate2Json(gDoorsWin, pchar(xml), pl, ph);

  if Assigned(mPluginHost) then
  begin
    jo := TSuperObject.Create();
    jo.I['DoorType'] := 2;
    objstr := jo.AsString;
    jo := nil;
    js := Format('OnUpdateDoorBomObject("%s", "%s");', [MyUtils.EncodeJSVariant(xml), MyUtils.EncodeJSVariant(objstr)]);
    objstr := mPluginHost.GetBrowserWindowObject.Evaluate(pchar(js));
    if objstr<>'' then
    begin
      pbuf := pchar(objstr);
    end;
  end;
  if pbuf=nil then
  begin
    //ShowMessage('掩门数据丢失');
    exit;
  end;
  mXMLStringList.Add(xml);
  isdoor := False;
  try
    isdoor := True;
    isframe := 0;
    jo := SO(string(pbuf));
    extend := jo.S['Extend'];
    dtype := jo.S['门框类型'];
    isframe := jo.I['是否带框'];
    hingehole := jo.S['HingeHole'];
    doormemo := jo.S['DoorMemo'];
    doorextra := jo.S['DoorExtra'];
    sliw := jo.D['门洞宽'];
    slih := jo.D['门洞高'];
    doorw := jo.D['成品门宽'];
    doorh := jo.D['成品门高'];
    doornum := jo.I['扇数'];

    ja := jo.O['物料'];
    for i:=0 to ja.AsArray.Length-1 do
    begin
      cjo := ja.AsArray.O[i];
      new(pslibom);
      pslibom.xmlindex := mXMLStringList.Count - 1;
      pslibom.cid := cid;
      pslibom.slino := slino;
      pslibom.subspace := subspace;
      pslibom.id := id;
      pslibom.pid := pid;
      pslibom.space_id := -1;

      pslibom.sliw := sliw;
      pslibom.slih := slih;
      pslibom.doorw := doorw;
      pslibom.doorh := doorh;
      pslibom.doornum := doornum;
      pslibom.gno := gno;
      pslibom.gdes := gdes;
      pslibom.dtype := dtype;
      pslibom.gcb := gcb;
      pslibom.extra := extra;
      pslibom.mark := mark;

      pslibom.code := cjo.S['Code'];
      pslibom.name := cjo.S['Name'];
      pslibom.mat := cjo.S['Name'];
      pslibom.color := cjo.S['Color'];
      pslibom.l := cjo.D['L'];
      pslibom.p := cjo.D['W'];
      pslibom.h := cjo.D['H'];
      pslibom.num := cjo.I['Num'];
      pslibom.group := cjo.S['Group'];
      pslibom.myunit := cjo.S['Unit'];
      pslibom.doorname := cjo.S['DoorName'];
      pslibom.bomtype := cjo.S['Bomtype'];
      pslibom.memo := cjo.S['Memo'];
      pslibom.memo2 := cjo.S['Memo2'];
      pslibom.memo3 := cjo.S['Memo3'];
      pslibom.bdfile := cjo.S['BDFILE'];
      pslibom.doormemo := cjo.S['DoorMemo'];
      pslibom.door_index := cjo.I['DoorIndex'];
      pslibom.isglass := cjo.I['Glass'];
      pslibom.is_buy := cjo.I['IsBuy'];
      pslibom.direct := cjo.S['Di'];
      pslibom.fbstr := cjo.S['FBStr'];
      pslibom.bdxmlid := cjo.S['BDXMLID'];
      if pslibom.bdxmlid<>'' then
      begin
        mBDXMLList.Add(pslibom.bdxmlid, cjo.S['BDXML']);
      end;
      doorslist.Add(pslibom);
      inc(id);
      cjo := nil;
    end;
    ja := nil;
    DoorItem := TDoorItem.Create;
    DoorItem.name := '';
    DoorItem.gno := gno;
    DoorItem.des := gdes;
    DoorItem.gcb := gcb;
    DoorItem.extra := extra;
    DoorItem.slino := slino;
    DoorItem.l := sliw;
    DoorItem.h := slih;
    DoorItem.d := 0;
    DoorItem.one_l := doorw;
    DoorItem.one_h := doorh;
    DoorItem.num := doornum;
    DoorItem.isframe := isframe;
    DoorItem.doortype := '掩门';
    DoorItem.xmlindex := mXMLStringList.Count - 1;
    DoorItem.xml := blockxml;
    DoorItem.hingehole := hingehole;
    DoorItem.doormemo := doormemo;
    DoorItem.doorextra := doorextra;
    mDoorList.Add(DoorItem);
    inc(slino);
  finally
    jo := nil;
  end;
end;

procedure TLocalObject.GraphSizeToBJSize(bjsize: string; p: Pointer);
var
  pbom              : ^BomRecord;
  ll, pp, hh, n     : Integer;
  s, s1             : string;
begin
  pbom := p;
  ll := 0;
  pp := 0;
  hh := 0;
  s := bjsize;
  n := Pos(',', s);
  if n > 0 then
  begin
    s1 := LeftStr(s, n - 1);
    ll := MyStrToInt(s1);
    s := RightStr(s, Length(s) - n);
  end;
  n := Pos(',', s);
  if n > 0 then
  begin
    s1 := LeftStr(s, n - 1);
    pp := MyStrToInt(s1);
    s := RightStr(s, Length(s) - n);
  end;
  hh := MyStrToInt(s);
  pbom.l := pbom.l + ll;
  pbom.p := pbom.p + pp;
  pbom.h := pbom.h + hh;
end;

function TLocalObject.ImportXomItemForQuo(param0: PQuoParam; var id, slino: Integer): Integer;
var
  root, node, cnode, attri: IXMLNode;
  i, k, di, bp, bl, bh, childnum: Integer;
  xx0, xx1, yy0, yy1, zz0, zz1: Integer;
  program_str, sizeprogram_str, value, vname, childxml, textureclass: string;
  exp               : TExpress;
  pbom              : PBomRecord;
  bg, str           : string;
  args              : array[0..15] of Integer;
  param: QuoParam;
  jo:ISuperObject;
begin
  Result := 0;
  if (param0.outputtype = '物料') {or (param0.outputtype = '无')} then exit;

  exp := TExpress.Create;
  exp.AddVariable('L', '', IntToStr(param0.pl), '', '');
  exp.AddVariable('P', '', IntToStr(param0.pd), '', '');
  exp.AddVariable('H', '', IntToStr(param0.ph), '', '');
  exp.AddVariable('BH', '', IntToStr(param0.boardheight), '', '');
  exp.mBHValue := param0.boardheight;

  param.blockmemo := '';

  try
    root := param0.rootnode;
    attri := root.AttributeNodes.FindNode('模块备注');
    if (attri <> nil) and (attri.Text <> '') then
    begin
      param0.blockmemo := attri.Text;
      param0.blockmemo := StringReplace(param0.blockmemo, '[宽]', IntToStr(param0.pl), [rfReplaceAll]);
      param0.blockmemo := StringReplace(param0.blockmemo, '[深]', IntToStr(param0.pd), [rfReplaceAll]);
      param0.blockmemo := StringReplace(param0.blockmemo, '[高]', IntToStr(param0.ph), [rfReplaceAll]);
    end;
    attri := root.AttributeNodes.FindNode('类别');
    if (attri <> nil) and ((attri.Text = '趟门,趟门') or (attri.Text = '掩门,掩门')) then
    begin
      node := root.ChildNodes.FindNode('模板');
      if node<>nil then
      begin
        childxml := '';
        if (node.ChildNodes.Count > 0) then childxml := node.ChildNodes[0].xml;
        if (attri.Text = '趟门,趟门') then ImportSlidingXomItemForQuo(param0.cid, param0.boardheight, param0.mark, param0.blist
          , param0.gno, param0.gdes, param0.gcb, param0.pname, param0.subspace, childxml, param0.pmat, param0.pcolor
          , param0.pid, param0.pl, param0.pd, param0.ph, id, slino, param0.outputtype);
        if (attri.Text = '掩门,掩门') then ImportDoorsXomItemForQuo(param0.cid, param0.boardheight, param0.mark, param0.blist
          , param0.gno, param0.gdes, param0.gcb, param0.pname, param0.subspace, childxml, param0.pmat, param0.pcolor
          , param0.pid, param0.pl, param0.pd, param0.ph, id, slino, param0.outputtype);
        exit;
      end;
    end;
    attri := root.AttributeNodes.FindNode('板材单价');
    if (attri <> nil) and (attri.Text <> '') and (param0.pricecalctype = '') then param0.pricecalctype := attri.Text;
    node := root.ChildNodes.FindNode('变量列表');
    if node <> nil then
    begin
      for i := 0 to node.ChildNodes.Count - 1 do
      begin
        cnode := node.ChildNodes[i];
        vname := '';
        attri := cnode.AttributeNodes.FindNode('名称');
        if attri <> nil then
          vname := attri.Text;
        value := '';
        attri := cnode.AttributeNodes.FindNode('值');
        if attri <> nil then
          value := attri.Text;
        exp.AddVariable(vname, '', value, '', '');
      end;
    end;
    node := root.ChildNodes.FindNode('我的模块');
    if node <> nil then
    begin
      for i := 0 to node.ChildNodes.Count - 1 do
      begin
        cnode := node.ChildNodes[i];
        if (cnode.nodename <> '板件') and (cnode.nodename <> '五金') and (cnode.nodename <> '型材五金')
          and (cnode.nodename <> '模块') and (cnode.nodename <> '门板') then Continue;

        if GetAttributeValue(cnode, '显示方式', '', '')='3' then continue;
        bg := GetAttributeValue(cnode, '基础图形', '', '');
        if bg='BG::SPACE' then continue;

        program_str := GetAttributeValue(cnode, 'Program', '', '');

        new(pbom);
        pbom.num := 1;

        textureclass := GetAttributeValue(cnode, '装饰类别', '', '');

        pbom.number_text := GetAttributeValue(cnode, 'NumberText', '', '');
        if pbom.number_text='' then pbom.number_text := param0.number_text;

        pbom.group := GetAttributeValue(cnode, 'Group', '', '');
        if pbom.group<>'' then pbom.group := Format('%s-%s', [pbom.group, MyUtils.GetGUID]);

        pbom.isoutput := True;
        pbom.id := id;
        pbom.pid := param0.pid;
        pbom.name := '';
        pbom.mat := '';
        pbom.texture := '';
        pbom.desc := '';
        pbom.l := 0;
        pbom.p := 0;
        pbom.h := 0;
        pbom.gno := param0.gno;
        pbom.gdes := param0.gdes;
        pbom.subspace := param0.subspace;
        pbom.bh := param0.boardheight;
        pbom.price_calctype := param0.pricecalctype;
        pbom.is_calc_cost := False;
        pbom.cost := 0;
        pbom.slino := -1;
        InitVarArgs(pbom.var_args, pbom.var_names);
        attri := cnode.AttributeNodes.FindNode('子空间');
        if attri <> nil then pbom.subspace := param0.subspace + attri.Text;

        pbom.name := GetAttributeValue(cnode, '名称', '', '');

        xx0 := GetAttributeValue(cnode, 'XX0', 0, 0);
        xx1 := GetAttributeValue(cnode, 'XX1', 0, 0);
        yy0 := GetAttributeValue(cnode, 'YY0', 0, 0);
        yy1 := GetAttributeValue(cnode, 'YY1', 0, 0);
        zz0 := GetAttributeValue(cnode, 'ZZ0', 0, 0);
        zz1 := GetAttributeValue(cnode, 'ZZ1', 0, 0);

        exp.SetSubject(GetAttributeValue(cnode, '宽', '', ''));
        pbom.l := exp.ToValueInt + xx1 + (0 - xx0);
        pbom.l := GetAttributeValue(cnode, 'RL', pbom.l, pbom.l);

        exp.SetSubject(GetAttributeValue(cnode, '深', '', ''));
        pbom.p := exp.ToValueInt + yy1 + (0 - yy0);

        exp.SetSubject(GetAttributeValue(cnode, '高', '', ''));
        pbom.h := exp.ToValueInt + zz1 + (0 - zz0);

        for k := 0 to 15 do             //所有16个参数
        begin
          args[k] := 0;
          attri := cnode.AttributeNodes.FindNode('参数' + IntToStr(k));
          if (attri <> nil) and (attri.Text <> '') then
          begin
            MyVariant(attri.Text, vname, value);
            exp.SetSubject(value);
            args[k] := exp.ToValueInt;
            pbom.var_args[k] := args[k];
            pbom.var_names[k] := vname;
          end;
        end;
        if bg = 'BG::DOORRECT' then     //外盖板
        begin
          pbom.l := pbom.l + args[0] + args[1];
          pbom.h := pbom.h + args[2] + args[3];
        end;

        //size高级编程
        sizeprogram_str := GetAttributeValue(cnode, 'SizeProgram', '', '');
        if ExtractFileExt(sizeprogram_str)='.lua' then
        begin
          sizeprogram_str := LuaData.ValueOf(sizeprogram_str);
          //sizeprogram_str := MyUtils.ReadStringFromFile(GetQuickDrawPath+'Program\'+sizeprogram_str);
          jo := SO(Format('{"X":"%d","Y":"%d","Z":"%d","L":"%d","D":"%d","H":"%d","OZ":"%f"}', [pbom.x, pbom.y, pbom.z, pbom.l, pbom.p, pbom.h, pbom.oz]));
          for k:=0 to 15 do
          begin
            jo.I['C'+IntToStr(k)] := pbom.var_args[k];
          end;
          str := CompileLuaProgram(jo, sizeprogram_str);
          jo := SO(str);
          if jo<>nil then
          begin
            pbom.x := jo.I['X'];
            pbom.y := jo.I['Y'];
            pbom.z := jo.I['Z'];
            pbom.l := jo.I['L'];
            pbom.p := jo.I['D'];
            pbom.h := jo.I['H'];
            pbom.oz := jo.D['OZ'];
          end;
        end;

        di := 0;
        attri := cnode.AttributeNodes.FindNode('DI');
        if attri <> nil then
          di := StrToInt(attri.Text);
        attri := cnode.AttributeNodes.FindNode('材料');
        if attri <> nil then pbom.mat := attri.Text else if textureclass=param0.textureclass then pbom.mat := param0.pmat;
        attri := cnode.AttributeNodes.FindNode('颜色');
        if attri <> nil then pbom.texture := attri.Text else if textureclass=param0.textureclass then pbom.texture := param0.pcolor;

        attri := cnode.AttributeNodes.FindNode('类别');
        if attri <> nil then
          pbom.desc := attri.Text;
        childxml := '';
        childnum := 0;
        if cnode.ChildNodes.Count > 0 then
          childxml := cnode.ChildNodes[0].xml;
        attri := cnode.AttributeNodes.FindNode('Num');
        if (attri <> nil) and (attri.Text <> '') then pbom.num := MyStrToInt(attri.Text) * param0.num;
        attri := cnode.AttributeNodes.FindNode('Mark');
        if (attri <> nil) and (attri.Text <> '') then pbom.mark := MyStrToInt(attri.Text)
        else pbom.mark := 0;
        attri := cnode.AttributeNodes.FindNode('BJSize');
        if (attri <> nil) and (attri.Text <> '') then GraphSizeToBJSize(attri.Text, pbom);
        attri := cnode.AttributeNodes.FindNode('UD');
        if (attri <> nil) and (attri.Text <> '') then pbom.userdefine := attri.Text;

        Result := Result + 1;
        param0.blist.Add(pbom);
        inc(id);

        childnum := 0;
        if childxml <> '' then
        begin
          param := param0^;
          if textureclass<>'' then param.textureclass := textureclass;
          param.pname := pbom.name;
          param.subspace := pbom.subspace;
          param.xml := childxml;
          param.pmat := pbom.mat;
          param.mark := pbom.mark;
          param.pcolor := pbom.texture;
          param.pid := id - 1;
          param.pl := pbom.l;
          param.pd := pbom.p;
          param.ph := pbom.h;
          param.num := pbom.num;
          if pbom.number_text<>'' then param.number_text := pbom.number_text;
          attri := cnode.AttributeNodes.FindNode('输出类型');
          if (attri <> nil) and (attri.Text <> '') then param.outputtype := attri.Text;
          if cnode.ChildNodes.Count>0 then
          begin
            param.rootnode := cnode.ChildNodes[0];
            param.xdoc := param0.xdoc;
            childnum := ImportXomItemForQuo(@param, id, slino);
          end;
        end;
        pbom.blockmemo := param0.blockmemo;
        if program_str <> '' then       //产生克隆模块
        begin
          ImportCloneItemForQuo(exp, program_str, pbom, cnode, param0, id, slino);
        end;
        GraphSizeToBomSize(pbom.l, pbom.p, pbom.h, di, bl, bp, bh);
        pbom.l := bl;
        pbom.p := bp;
        pbom.h := bh;
        if bh <= 36 then pbom.bh := bh; //小于等于36认为是板材厚度
        pbom.childnum := childnum;
        if (pbom.l > 1) and (pbom.p > 1) and (pbom.h <= 1) then pbom.isoutput := False;
        attri := cnode.AttributeNodes.FindNode('输出类型');
        if (attri <> nil) and ((attri.Text = '物料') or (attri.Text = '无')) then
          pbom.isoutput := False;
        attri := cnode.AttributeNodes.FindNode('装饰类别');
        if (attri <> nil) and ((attri.Text = '趟门') or (attri.Text = '掩门') or (pbom.myclass = '趟门,趟门') or (pbom.myclass = '掩门,掩门')) then
          pbom.isoutput := False;

        if (pbom.l < 1) or (pbom.p < 1) or (pbom.h < 1) then pbom.isoutput := False; //过滤掉尺寸小于等于零的物料，xml情况复杂
        if (pbom.l > 1) and (pbom.p > 1) and (pbom.h <= 1) then pbom.isoutput := False; //过滤掉一些尺寸为0的物料数据
      end;
    end;
  finally
    if Assigned(exp) then FreeAndNil(exp);
  end;
end;

function TLocalObject.ImportSlidingXomItemForQuo(cid, boardheight, mark: Integer; blist: TList; gno, gdes, gcb,
  pname, subspace, xml, pmat, pcolor: string; pid, pl, pd, ph: Integer;
  var id, slino: Integer; outputtype: string): Integer;
var
  i, k, di, bp, bl, bh, childnum: Integer;
  value, vname, childxml: string;
  pbom              : ^BomRecord;
  bg, str           : string;
  jo, ja, cjo:ISuperObject;
  pbuf:pchar;
begin
  Result := 0;
  if (outputtype = '物料') {or (outputtype = '无')} then exit;
  exit;
  //pbuf := Sli_XmlTemplate2Json(gSlidingWin, pchar(xml), pl, ph);
  if pbuf=nil then
  begin
    //ShowBomMessage('推拉门数据丢失');
    exit;
  end;

  try
    jo := SO(string(pbuf));

    ja := jo.O['报价'];
    for i:=0 to ja.AsArray.Length-1 do
    begin
      cjo := ja.AsArray.O[i];
      if cjo.D['Price1']<0 then continue;
      new(pbom);
      pbom.isoutput := True;
      pbom.id := id;
      pbom.pid := pid;
      pbom.gno := gno;
      pbom.gdes := gdes;
      pbom.subspace := subspace;
      pbom.num := 1;
      pbom.is_calc_cost := False;
      pbom.cost := 0;
      pbom.slino := slino;
      pbom.mark := mark;
      pbom.code := cjo.S['Code'];
      pbom.name := cjo.S['Name'];
      pbom.mat := cjo.S['Mat'];
      pbom.texture := cjo.S['Color'];
      pbom.square := cjo.D['Size'];
      pbom.price := cjo.D['Price1'];
      pbom.price2 := cjo.D['Price2'];
      pbom.totalprice := cjo.D['TotalPrice1'];
      pbom.totalprice2 := cjo.D['TotalPrice2'];
      pbom.l := Round(cjo.D['宽']);
      pbom.p := Round(cjo.D['深']);
      pbom.h := Round(cjo.D['高']);
      pbom.num := cjo.I['Num'];

      Result := Result + 1;
      slidingQuolist.Add(pbom);
      inc(id);

      cjo := nil;
    end;
    inc(slino);
    ja := nil;
  finally
    jo := nil;
  end;
end;

function TLocalObject.ImportDoorsXomItemForQuo(cid, boardheight, mark: Integer; blist: TList; gno, gdes, gcb,
  pname, subspace, xml, pmat, pcolor: string; pid, pl, pd, ph: Integer;
  var id, slino: Integer; outputtype: string): Integer;
var
  i, k, di, bp, bl, bh, childnum: Integer;
  value, vname, childxml: string;
  pbom              : ^BomRecord;
  bg, str           : string;
  jo, ja, cjo:ISuperObject;
  pbuf:pchar;
begin
  Result := 0;
  if (outputtype = '物料') {or (outputtype = '无')} then exit;
  exit;
  pbuf :=nil;
  //pbuf := Doors_XmlTemplate2Json(gDoorsWin, pchar(xml), pl, ph);
  if pbuf=nil then
  begin
    //ShowBomMessage('掩门数据丢失');
    exit;
  end;
  try
    jo := SO(string(pbuf));

    ja := jo.O['报价'];
    for i:=0 to ja.AsArray.Length-1 do
    begin
      cjo := ja.AsArray.O[i];
      if cjo.D['Price1']<0 then continue;
      new(pbom);
      pbom.isoutput := True;
      pbom.id := id;
      pbom.pid := pid;
      pbom.gno := gno;
      pbom.gdes := gdes;
      pbom.subspace := subspace;
      pbom.num := 1;
      pbom.is_calc_cost := False;
      pbom.cost := 0;
      pbom.slino := slino;
      pbom.mark := mark;
      pbom.code := cjo.S['Code'];
      pbom.name := cjo.S['Name'];
      pbom.mat := cjo.S['Mat'];
      pbom.texture := cjo.S['Color'];
      pbom.square := cjo.D['Size'];
      pbom.price := cjo.D['Price1'];
      pbom.price2 := cjo.D['Price2'];
      pbom.totalprice := cjo.D['TotalPrice1'];
      pbom.totalprice2 := cjo.D['TotalPrice2'];
      pbom.l := Round(cjo.D['宽']);
      pbom.p := Round(cjo.D['深']);
      pbom.h := Round(cjo.D['高']);
      pbom.num := cjo.I['Num'];

      Result := Result + 1;
      doorsQuolist.Add(pbom);
      inc(id);

      cjo := nil;
    end;
    inc(slino);
    ja := nil;
  finally
    jo := nil;
  end;
end;

function TLocalObject.Xml2ChildNodes(const xml: string): IXMLNode;
var xdoc:IXMLDocument;
begin
  Result := nil;
  if xml='' then exit;
  xdoc := XMLDoc.LoadXMLData('<?xml version="1.0" encoding="gb2312"?>'+xml);
  Result := xdoc.ChildNodes[1].CloneNode(True);
  xdoc := nil;
end;

function TLocalObject.ImportCloneItemForBom(exp:TExpress; program_str:string; clone_oi:PBomOrderItem; clonenode: IXMLNode; param0: PBomParam; var id,
  slino: Integer): Integer;
  procedure UpdateAttribute(txdoc:IXMLDocument; cnode:IXMLNode; name, value:string);
  var attri:IXMLNode;
  begin
    if name='' then exit;
      attri := cnode.AttributeNodes.FindNode(name);
      if attri=nil then
      begin
        attri := txdoc.CreateNode(name, ntAttribute);
        cnode.AttributeNodes.Add(attri);
      end;
      attri.Text := value;
  end;
  procedure S2S(str: string; var s1, s2: string);
  var
    ws                : WideString;
    n                 : Integer;
  begin
    s1 := '';
    s2 := '';
    ws := str;
    n := Pos('=', ws);
    s1 := LeftStr(ws, n - 1);
    s2 := RightStr(ws, Length(ws) - n);
    s1 := trim(s1);
    s2 := trim(s2);
    s2 := StringReplace(s2, '^', ',', [rfReplaceAll]);
  end;
var
  root, node, cnode, attri, tmpnode: IXMLNode;
  i, di, bp, bl, bh, childnum, k, autodirect: Integer;
  xx0, xx1, yy0, yy1, zz0, zz1: Integer;
  tmp_space_x, tmp_space_y, tmp_space_z: Integer;
  value, vname, childxml, tmp_subspace, tmp_soz, spaceflag: string;
  poi               : PBomOrderItem;
  pslibom           : PSlidingBomRecord;
  sliw, slih, doorw, doorh: Real;
  doornum           : Integer;
  isdoor            : boolean;
  str, bg, dtype    : string;
  args              : array[0..15] of Integer;
  ls, varstr        : string;           //拉手信息
  DoorItem          : TDoorItem;
  product_item      : TProductItem;
  real_d, real_l, t : double;
  param             : BomParam;

var
  wstr, ln, vstr          : Widestring;
  n:Integer;
  s1, s2, nodename, linkpath, textureclass, ext          : string;
  jo:ISuperObject;
begin
  param.blockmemo := '';

  ext := ExtractFileExt(program_str);
  program_str := LuaData.ValueOf(program_str);
  //program_str := MyUtils.ReadStringFromFile(MyUtils.GetQuickDrawPath+'Program\'+program_str);
  jo := SO(Format('{"X":"%d","Y":"%d","Z":"%d","L":"%d","D":"%d","H":"%d"}'
    , [clone_oi.x, clone_oi.y, clone_oi.z, clone_oi.l, clone_oi.p, clone_oi.h]));
  for i:=0 to 15 do
  begin
    jo.I['C'+IntToStr(i)] := clone_oi.var_args[i];
  end;
  if ext='.lua' then
    wstr := CompileLuaProgram(jo, program_str)
  else wstr := CompileProgram(jo, program_str);
  jo := nil;
  try
    n := Pos(';', wstr);
    while n > 0 do
    begin
      cnode := clonenode.CloneNode(True);
      nodename := cnode.NodeName;

      ln := LeftStr(wstr, n - 1);
      wstr := RightStr(wstr, Length(wstr) - n);
      //分解行
      n := Pos(',', ln);
      while n>0 do
      begin
        vstr := LeftStr(ln, n - 1);
        S2S(vstr, s1, s2);
        if s1='NN' then nodename := s2 else UpdateAttribute(param0.xdoc, cnode, s1, s2);
        ln := RightStr(ln, Length(ln) - n);
        n := Pos(',', ln);
      end;
      if (n<=0) and (ln<>'') then
      begin
        S2S(ln, s1, s2);
        if s1='NN' then nodename := s2 else UpdateAttribute(param0.xdoc, cnode, s1, s2);
      end;

      n := Pos(';', wstr);

      if (nodename <> '板件') and (nodename <> '五金') and (nodename <> '型材五金')
        and (nodename <> '模块') and (nodename <> '门板') then Continue;

      linkpath := '';
      attri := cnode.AttributeNodes.FindNode('链接');
      if attri <> nil then linkpath := attri.Text;

      attri := cnode.AttributeNodes.FindNode('基础图形');
      bg := '';
      if attri <> nil then bg := attri.Text;
      if (bg = 'BG::SPACE') then Continue;
      attri := cnode.AttributeNodes.FindNode('显示方式');
      if (attri <> nil) and (attri.Text = '3') then Continue;

      NewBomOrderItem(poi);
      if nodename = '板件' then poi.myunit := '块';

      textureclass := '';
      attri := cnode.AttributeNodes.FindNode('装饰类别');
      if attri<>nil then textureclass := attri.Text;

      tmp_space_x := param0.space_x;
      tmp_space_y := param0.space_y;
      tmp_space_z := param0.space_z;
      poi.pl := param0.pl;
      poi.pd := param0.pd;
      poi.ph := param0.ph;
      poi.bg := bg;
      poi.holeid := -1;                 //打孔id
      poi.kcid := -1;                   //开槽id
      poi.cid := param0.cid;
      poi.isoutput := True;
      InitVarArgs(poi.var_args, poi.var_names);
      poi.nodename := nodename;
      poi.id := id;
      poi.pid := param0.pid;
      poi.subspace := param0.subspace;
      poi.space_x := param0.space_x;
      poi.space_y := param0.space_y;
      poi.space_z := param0.space_z;
      poi.space_id := param0.space_id;
      poi.parent := param0.parent;
      tmp_subspace := '';
      attri := cnode.AttributeNodes.FindNode('子空间');
      if attri <> nil then
      begin
        tmp_subspace := attri.Text;
        if tmp_subspace = 'A' then tmp_subspace := '';
        poi.subspace := param0.subspace + tmp_subspace;
        if attri.Text <> '' then poi.isoutput := False;
      end;
      attri := cnode.AttributeNodes.FindNode('名称');
      if attri <> nil then poi.name := attri.Text;
      varstr := '';
      poi.x := param0.px + 0;
      poi.y := param0.py + 0;
      poi.z := param0.pz + 0;

      xx0 := 0;
      xx1 := 0;
      yy0 := 0;
      yy1 := 0;
      zz0 := 0;
      zz1 := 0;
      attri := cnode.AttributeNodes.FindNode('XX0');
      if attri <> nil then xx0 := MyStrToInt(attri.Text);
      attri := cnode.AttributeNodes.FindNode('XX1');
      if attri <> nil then xx1 := MyStrToInt(attri.Text);
      attri := cnode.AttributeNodes.FindNode('YY0');
      if attri <> nil then yy0 := MyStrToInt(attri.Text);
      attri := cnode.AttributeNodes.FindNode('YY1');
      if attri <> nil then yy1 := MyStrToInt(attri.Text);
      attri := cnode.AttributeNodes.FindNode('ZZ0');
      if attri <> nil then zz0 := MyStrToInt(attri.Text);
      attri := cnode.AttributeNodes.FindNode('ZZ1');
      if attri <> nil then zz1 := MyStrToInt(attri.Text);

      attri := cnode.AttributeNodes.FindNode('X');
      if attri <> nil then
      begin
        if varstr = '' then
          varstr := attri.Text
        else
          varstr := varstr + '+' + attri.Text;
        exp.SetSubject(attri.Text);
        poi.lx := exp.ToValueInt + xx0;
        poi.x := param0.px + poi.lx;
      end;
      attri := cnode.AttributeNodes.FindNode('Y');
      if attri <> nil then
      begin
        if varstr = '' then
          varstr := attri.Text
        else
          varstr := varstr + '+' + attri.Text;
        exp.SetSubject(attri.Text);
        poi.ly := exp.ToValueInt + yy0;
        poi.y := param0.py + poi.ly;
      end;
      attri := cnode.AttributeNodes.FindNode('Z');
      if attri <> nil then
      begin
        if varstr = '' then
          varstr := attri.Text
        else
          varstr := varstr + '+' + attri.Text;
        exp.SetSubject(attri.Text);
        poi.lz := exp.ToValueInt + zz0;
        poi.z := param0.pz + poi.lz;
      end;
      poi.ox := 0;
      poi.oy := 0;
      poi.oz := 0;
      attri := cnode.AttributeNodes.FindNode('OX');
      if attri <> nil then
      begin
        exp.SetSubject(attri.Text);
        poi.ox := exp.ToValueInt;
      end;
      attri := cnode.AttributeNodes.FindNode('OY');
      if attri <> nil then
      begin
        exp.SetSubject(attri.Text);
        poi.oy := exp.ToValueInt;
      end;
      attri := cnode.AttributeNodes.FindNode('OZ');
      if attri <> nil then
      begin
        exp.SetSubject(attri.Text);
        poi.oz := exp.ToValueInt;
      end;
      attri := cnode.AttributeNodes.FindNode('宽');
      if attri <> nil then
      begin
        if varstr = '' then
          varstr := attri.Text
        else
          varstr := varstr + '+' + attri.Text;
        exp.SetSubject(attri.Text);
        poi.l := exp.ToValueInt + xx1 + (0 - xx0);
        if (tmp_subspace <> '') then
        begin
          tmp_space_x := poi.x;
          tmp_space_y := poi.y;
          tmp_space_z := poi.z;
        end;
        if (tmp_subspace = 'B') or (tmp_subspace = 'C') then
        begin
          product_item := mProductList[param0.cid];
          product_item.l := product_item.l + poi.l;
        end;
      end;
      attri := cnode.AttributeNodes.FindNode('RL');
      if (attri <> nil) and (attri.Text <> '') then poi.l := MyStrToInt(attri.Text);
      attri := cnode.AttributeNodes.FindNode('深');
      if attri <> nil then
      begin
        if varstr = '' then
          varstr := attri.Text
        else
          varstr := varstr + '+' + attri.Text;
        exp.SetSubject(attri.Text);
        poi.p := exp.ToValueInt + yy1 + (0 - yy0);
      end;
      attri := cnode.AttributeNodes.FindNode('高');
      if attri <> nil then
      begin
        if varstr = '' then
          varstr := attri.Text
        else
          varstr := varstr + '+' + attri.Text;
        exp.SetSubject(attri.Text);
        poi.h := exp.ToValueInt + zz1 + (0 - zz0);
      end;
      poi.holeflag := 0;
      attri := cnode.AttributeNodes.FindNode('HoleFlag');
      if attri <> nil then
      begin
        exp.SetSubject(attri.Text);
        poi.holeflag := exp.ToValueInt;
      end;
      for k := 0 to 15 do               //所有16个参数
      begin
        args[k] := 0;
        attri := cnode.AttributeNodes.FindNode('参数' + IntToStr(k));
        if (attri <> nil) and (attri.Text <> '') then
        begin
          MyVariant(attri.Text, vname, value);
          exp.SetSubject(value);
          args[k] := exp.ToValueInt;
          poi.var_args[k] := args[k];
          poi.var_names[k] := vname;
          varstr := varstr + '+' + vname;
        end;
      end;
      if bg = 'BG::DOORRECT' then       //外盖板
      begin
        poi.l := poi.l + args[0] + args[1];
        poi.h := poi.h + args[2] + args[3];
      end;
      if bg = 'BG::BLOCK_X' then        //BG::BLOCK_X
      begin
        if poi.var_args[0] = 2 then
        begin
          if poi.var_args[1] = 1 then
          begin
            poi.p := Round(sqrt(poi.var_args[3] * poi.var_args[3] + poi.var_args[4] * poi.var_args[4]));
          end
          else if poi.var_args[1] = 2 then
          begin
            poi.l := Round(sqrt(poi.var_args[3] * poi.var_args[3] + poi.var_args[4] * poi.var_args[4]));
          end;
        end;
      end;
      attri := cnode.AttributeNodes.FindNode('DI');
      if attri <> nil then di := StrToInt(attri.Text);
      poi.direct := di;
      attri := cnode.AttributeNodes.FindNode('材料');
      if attri <> nil then poi.mat := attri.Text else if textureclass=param0.textureclass then poi.mat := param0.pmat;
      attri := cnode.AttributeNodes.FindNode('颜色');
      if attri <> nil then poi.color := attri.Text else if textureclass=param0.textureclass then poi.color := param0.pcolor;
      attri := cnode.AttributeNodes.FindNode('类别');
      if attri <> nil then poi.desc := attri.Text;
      attri := cnode.AttributeNodes.FindNode('编码');
      if attri <> nil then poi.code := attri.Text;
      attri := cnode.AttributeNodes.FindNode('工艺');
      if attri <> nil then poi.process := attri.Text;
      attri := cnode.AttributeNodes.FindNode('UI');
      if (attri <> nil) then
      begin
        if attri.Text = '拉手' then
          ls := ls + poi.name + ',';
        if attri.Text = '拉手集合' then
        begin
          poi.memo := poi.memo + ls;
          poi.ls := ls;
        end;
      end;
      poi.lgflag := 0;
      attri := cnode.AttributeNodes.FindNode('LgwjFlag');
      if (attri <> nil) and (attri.Text = '1') then poi.lgflag := 1;
      poi.holetype := 0;
      attri := cnode.AttributeNodes.FindNode('HoleType');
      if (attri <> nil) and (attri.Text <> '') then poi.holetype := MyStrToInt(attri.Text);
      attri := cnode.AttributeNodes.FindNode('AutoDirect');
      if (attri <> nil) and (attri.Text <> '') then
        autodirect := MyStrToInt(attri.Text)
      else
        autodirect := 0;
      attri := cnode.AttributeNodes.FindNode('HC'); //动态判定HoleConfig是否要计算
      if attri <> nil then SetIsCalcHoleConfig(poi, attri.Text);
      attri := cnode.AttributeNodes.FindNode('BDXMLID');
      if (attri <> nil) and (attri.Text <> '') then poi.bdxmlid := attri.Text;
      attri := cnode.AttributeNodes.FindNode('HI');
      if (attri <> nil) and (attri.Text <> '') then poi.holeinfo := MyUtils.URLDecode(attri.Text);
      attri := cnode.AttributeNodes.FindNode('Extend');
      if (attri <> nil) and (attri.Text <> '') then poi.extend := MyUtils.URLDecode(attri.Text);
      attri := cnode.AttributeNodes.FindNode('Group');
      if (attri <> nil) and (attri.Text <> '') then poi.group := Format('%s-%s', [attri.Text, MyUtils.GetGUID]);
      attri := cnode.AttributeNodes.FindNode('图形参数');
      if (attri <> nil) and (attri.Text <> '') then SetBGParam(poi, attri.Text);

      poi.lfb := 0;
      poi.llk := 0;
      poi.wfb := 0;
      poi.wlk := 0;
      poi.gno := param0.gno;
      poi.gdes := param0.gdes;
      poi.gcb := param0.gcb;
      attri := cnode.AttributeNodes.FindNode('FBSTR');
      if attri <> nil then poi.user_fbstr := attri.Text;
      if (poi.user_fbstr <> '') then FBStr2Value(poi.user_fbstr, poi.llk, poi.wlk, poi.llfb, poi.rrfb, poi.ddfb, poi.uufb, poi.fb, poi.fbstr);

      poi.value_lsk := 0;
      poi.value_rsk := 0;
      poi.value_zk := 0;
      poi.value_zs := 0;
      poi.value_ls := 0;
      poi.value_lg := 0;
      poi.value_ltm := 0;
      poi.value_rtm := 0;
      SetSysVariantValueForOrderItem(varstr, poi);

      childnum := 0;
      poi.num := 1;
      attri := cnode.AttributeNodes.FindNode('Num');
      if (attri <> nil) and (attri.Text <> '') then poi.num := MyStrToInt(attri.Text) * param0.num;
      attri := cnode.AttributeNodes.FindNode('Mark');
      if (attri <> nil) and (attri.Text <> '') then poi.mark := MyStrToInt(attri.Text)
      else poi.mark := 0;
      attri := cnode.AttributeNodes.FindNode('Memo');
      if (attri <> nil) and (attri.Text <> '') then poi.memo := attri.Text;
      attri := cnode.AttributeNodes.FindNode('UD');
      if (attri <> nil) and (attri.Text <> '') then poi.userdefine := attri.Text;
      poi.holestr := '';
      poi.kcstr := '';

      Result := Result + 1;
      Des2Des(poi);
      param0.blist.Add(poi);
      inc(id);

      real_l := poi.l;
      real_d := poi.p;
      if (tmp_subspace = 'L') then      //L面空间，进行旋转计算
      begin
        if (poi.var_args[0] = 1) then
        begin
          poi.oz := arctan((real_d - poi.var_args[2]) / (real_l - poi.var_args[1])) / PI * 180; //旋转角度
          poi.p := poi.var_args[3];     //深度
          t := sqrt((real_l - poi.var_args[1]) * (real_l - poi.var_args[1]) + (real_d - poi.var_args[2]) * (real_d - poi.var_args[2]));
          poi.l := Round(t);            //宽度
          poi.x := Round(poi.var_args[1] - poi.var_args[3] * (real_d - poi.var_args[2]) / t); //x
          poi.y := Round(real_d - poi.var_args[3] * (real_l - poi.var_args[1]) / t); //y
          if poi.var_args[4] <> 0 then poi.l := poi.var_args[4];
          poi.lx := poi.x;
          poi.ly := poi.y;
        end
        else
        begin
          poi.oz := 0;
        end;
      end;
      if (tmp_subspace = 'R') then      //R面空间，进行旋转计算
      begin
        if (poi.var_args[0] = 1) then
        begin
          poi.oz := -arctan((real_d - poi.var_args[2]) / (real_l - poi.var_args[1])) / PI * 180;
          poi.p := poi.var_args[3];
          t := sqrt((real_l - poi.var_args[1]) * (real_l - poi.var_args[1]) + (real_d - poi.var_args[2]) * (real_d - poi.var_args[2]));
          poi.l := Round(t);            //宽度
          poi.x := poi.x + Round(poi.var_args[3] * (real_d - poi.var_args[2]) / t); //x
          poi.y := Round(poi.var_args[2] - poi.var_args[3] * (real_l - poi.var_args[1]) / t); //y
          if poi.var_args[4] <> 0 then poi.l := poi.var_args[4];
          poi.lx := poi.x;
          poi.ly := poi.y;
        end
        else
        begin
          poi.oz := 0;
        end;
      end;

      poi.tmp_soz := param0.sozflag;
      tmp_soz := param0.sozflag;
      if tmp_subspace <> '' then tmp_soz := '';
      if (tmp_subspace = '') and (Trunc(poi.oz) <> 0) then tmp_soz := param0.sozflag + Format('@%d_%d', [Integer(poi), Trunc(poi.oz)]);

      childnum := 0;

      childxml := '';
      if linkpath<>'' then
      begin
        childxml := EnumXML(GetXMLByLink(linkpath, qry));
        tmpnode := Xml2ChildNodes(childxml);
        if tmpnode<>nil then
        begin
          cnode.ChildNodes.Clear;
          cnode.ChildNodes.Add(tmpnode);
        end;
      end else begin
        if cnode.ChildNodes.Count > 0 then childxml := cnode.ChildNodes.Nodes[0].xml;
      end;
      if childxml <> '' then
      begin
        spaceflag := GetAttributeValue(cnode, 'SpaceFlag', '', '');

        param := param0^;
        param.pname := poi.name;
        param.subspace := poi.subspace;
        param.sozflag := tmp_soz;
        param.xml := childxml;
        param.textureclass := textureclass;
        param.pmat := poi.mat;
        param.pcolor := poi.color;
        param.pid := id - 1;
        param.pl := poi.l;
        param.pd := poi.p;
        param.ph := poi.h;
        param.px := poi.x;
        param.py := poi.y;
        param.pz := poi.z;
        param.space_x := tmp_space_x;
        param.space_y := tmp_space_y;
        param.space_z := tmp_space_z;
        if spaceflag='1' then param.space_id := poi.id else param.space_id := param0.space_id;
        param.num := poi.num;
        param.parent := poi;
        if poi.group<>'' then param.group := poi.group;
        attri := cnode.AttributeNodes.FindNode('输出类型');
        if (attri <> nil) and (attri.Text <> '') then param.outputtype := attri.Text;
        if cnode.ChildNodes.Count>0 then
        begin
          param.rootnode := cnode.ChildNodes[0];
          param.xdoc := param0.xdoc;
          childnum := ImportXomItemForBom(@param, id, slino);
        end;
      end;
      if poi.group='' then poi.group := param0.group;
      poi.blockmemo := param0.blockmemo;
      GraphSizeToBomSize(poi.l, poi.p, poi.h, di, bl, bp, bh);
      if (autodirect = 1) and (bp > 1220) then //自动纹路转换
      begin
        di := TextureDirectChange(di);
        poi.direct := di;
        GraphSizeToBomSize(poi.l, poi.p, poi.h, di, bl, bp, bh);
      end;
      poi.gl := poi.l;
      poi.gp := poi.p;
      poi.gh := poi.h;

      poi.l := bl;
      poi.p := bp;
      poi.h := bh;
      poi.bl := bl - poi.lfb - poi.llk;
      poi.bp := bp - poi.wfb - poi.wlk;
      poi.bh := bh;
      poi.childnum := childnum;
      attri := cnode.AttributeNodes.FindNode('装饰类别');
      if (attri <> nil) and ((attri.Text = '趟门') or (attri.Text = '掩门') or (poi.myclass = '趟门,趟门') or (poi.myclass = '掩门,掩门')) then
        poi.isoutput := False;

      if (poi.bl < 1) or (poi.bp < 1) or (poi.bh < 1) then poi.isoutput := False; //过滤掉尺寸小于等于零的物料，xml情况复杂
      if (poi.bl > 1) and (poi.bp > 1) and (poi.bh <= 1) then poi.isoutput := False; //过滤掉一些尺寸为0的物料数据

      //尺寸判定
      poi.bomstd := ToBomStd(poi.bomstddes, poi.l, poi.p, poi.h);
      if childnum > 0 then poi.isoutput := False;

      attri := cnode.AttributeNodes.FindNode('输出类型');
      if attri <> nil then poi.outputtype := attri.Text;
    end;
  except
  end;
end;

function TLocalObject.EnumXML(xml: Widestring): Widestring;
var xdoc:IXMLDocument;
  procedure EnumNode(blocknode:IXMLNode);
  var i, j:Integer;
  node, cnode, tmpnode, attri:IXMLNode;
  str:string;
  begin
    for i:=0 to blocknode.ChildNodes.Count-1 do
    begin
      node := blocknode.ChildNodes[i];
      if node.NodeName='我的模块' then
      begin
        for j:=0 to node.ChildNodes.Count-1 do
        begin
          cnode := node.ChildNodes[j];
          attri := cnode.AttributeNodes.FindNode('链接');
          if (attri = nil) or (attri.Text='') then continue;
          str := GetXMLByLink(attri.Text, qry);
          if str='' then continue;
          tmpnode := CreateNodeByXML(str, xdoc);
          cnode.ChildNodes.Add(tmpnode);
        end;  //for j
      end; //if
      EnumNode(node);
    end; //for i
  end;
var root:IXMLNode;
begin
  Result := '';
  if xml = '' then exit;

  try
    xdoc := XMLDoc.LoadXMLData('<?xml version="1.0" encoding="gb2312"?>'+xml);
    root := xdoc.ChildNodes[1];
    EnumNode(root);
    Result := root.XML;
  finally
    xdoc := nil;
  end;
end;

function TLocalObject.PolyLineToLength(str: string): Integer;
var
  i, n, N1, num, v1, v2, v3: Integer;
  s1, s2, s3        : string;
  bgpt              : array of TVector3i;
  l                 : double;
begin
  l := 0;

  //把存储的字符串转化为多边线
  //n:vx,vy,vz;vx,vy,vz;
  n := Pos(':', str);
  if n <= 0 then exit;
  s1 := LeftStr(str, n - 1);
  num := MyStrToInt(s1);
  if num <= 1 then exit;
  SetLength(bgpt, num);
  for i := 0 to num - 1 do
  begin
    bgpt[i][0] := 0;
    bgpt[i][1] := 0;
    bgpt[i][2] := 0;
  end;

  i := 0;
  s1 := RightStr(str, Length(str) - n);
  n := Pos(';', s1);
  while n > 0 do
  begin
    s2 := LeftStr(s1, n - 1);

    N1 := Pos(',', s2);
    s3 := LeftStr(s2, N1 - 1);
    v1 := MyStrToInt(s3);

    s2 := RightStr(s2, Length(s2) - N1);
    N1 := Pos(',', s2);
    s3 := LeftStr(s2, N1 - 1);
    v2 := MyStrToInt(s3);

    s3 := RightStr(s2, Length(s2) - N1);
    v3 := MyStrToInt(s3);

    if i < num then
    begin
      bgpt[i][0] := v1;
      bgpt[i][1] := v2;
      bgpt[i][2] := v3;
    end;

    s1 := RightStr(s1, Length(s1) - n);
    n := Pos(';', s1);
    inc(i);
  end;
  for i := 1 to Length(bgpt) - 1 do
  begin
    l := l + P2PDist(bgpt[i - 1][0], bgpt[i - 1][1], bgpt[i][0], bgpt[i][1]);
  end;
  Result := Round(l);
end;

function TLocalObject.CompileProgram(jo:ISuperObject; code: string): string;
var x, y, z, l, d, h:Integer;
  c:array[0..15] of Integer;
  function Compile(code:string):string;
  var xml, s:string;
  i:Integer;
  begin
    PaxCompiler1.Reset;
    PaxCompiler1.RegisterLanguage(PaxJavaScriptLanguage1);
    PaxCompiler1.RegisterHeader(0, 'function S2I(s:string):Integer;', @S2I);
    PaxCompiler1.RegisterHeader(0, 'function I2S(i:Integer):string;', @I2S);
    PaxCompiler1.RegisterHeader(0, 'function S2D(s:string):double;', @S2D);
    PaxCompiler1.RegisterHeader(0, 'function D2S(v:double):string;', @D2S);
    PaxCompiler1.RegisterHeader(0, 'function TC(s:string):string;', @TC);
    PaxCompiler1.RegisterHeader(0, 'function ReadFile(const FileName: string): string;', @ReadFile);

    PaxCompiler1.RegisterVariable(0, 'LX', _typeINTEGER, @x);
    PaxCompiler1.RegisterVariable(0, 'LY', _typeINTEGER, @y);
    PaxCompiler1.RegisterVariable(0, 'LZ', _typeINTEGER, @z);
    PaxCompiler1.RegisterVariable(0, 'LL', _typeINTEGER, @l);
    PaxCompiler1.RegisterVariable(0, 'LD', _typeINTEGER, @d);
    PaxCompiler1.RegisterVariable(0, 'LH', _typeINTEGER, @h);
    PaxCompiler1.RegisterVariable(0, 'XML', _typeSTRING, @XML);
    for i:=0 to 15 do
    begin
      s := Format('C%s', [Chr(65 + i)]);
      PaxCompiler1.RegisterVariable(0, pchar(s), _typeINTEGER, @c[i]);
    end;

    PaxCompiler1.AddModule('1', PaxJavaScriptLanguage1.LanguageName);
    PaxCompiler1.AddCode('1', CC(code));

    if PaxCompiler1.Compile(PaxProgram1) then
    begin
      PaxProgram1.Run;
    end;
    Result := MyUtils.URLDecode(xml);
  end;
var
i:Integer;
begin
  x := jo.I['X'];
  y := jo.I['Y'];
  z := jo.I['Z'];
  l := jo.I['L'];
  d := jo.I['D'];
  h := jo.I['H'];
  for i:=0 to 15 do
  begin
    c[i] := jo.I['C'+IntToStr(i)];
  end;
  Result := Compile(code);
  Result := StringReplace(Result, #13, '', [rfReplaceAll]);
  Result := StringReplace(Result, #10, '', [rfReplaceAll]);
end;

function TLocalObject.ImportCloneItemForQuo(exp: TExpress; program_str: string; clone_oi: PBomRecord;
  clonenode: IXMLNode; param0: PQuoParam; var id, slino: Integer): Integer;
  procedure S2S(str: string; var s1, s2: string);
  var
    ws                : WideString;
    n                 : Integer;
  begin
    s1 := '';
    s2 := '';
    ws := str;
    n := Pos('=', ws);
    s1 := LeftStr(ws, n - 1);
    s2 := RightStr(ws, Length(ws) - n);
    s1 := trim(s1);
    s2 := trim(s2);
    s2 := StringReplace(s2, '^', ',', [rfReplaceAll]);
  end;
var
  root, node, cnode, attri, tmpnode: IXMLNode;
  i, k, di, bp, bl, bh, childnum: Integer;
  xx0, xx1, yy0, yy1, zz0, zz1: Integer;
  value, vname, childxml: string;
  pbom              : ^BomRecord;
  bg, str           : string;
  args              : array[0..15] of Integer;
  param: QuoParam;

var
  wstr, ln, vstr          : Widestring;
  n:Integer;
  s1, s2, nodename, textureclass, linkpath, ext          : string;
  jo:ISuperObject;
begin
  param.blockmemo := '';

  ext := ExtractFileExt(program_str);
  program_str := MyUtils.ReadStringFromFile(MyUtils.GetQuickDrawPath+'Program\'+program_str);
  jo := SO(Format('{"X":"%d","Y":"%d","Z":"%d","L":"%d","D":"%d","H":"%d"}'
    , [clone_oi.x, clone_oi.y, clone_oi.z, clone_oi.l, clone_oi.p, clone_oi.h]));
  for i:=0 to 15 do
  begin
    jo.I['C'+IntToStr(i)] := clone_oi.var_args[i];
  end;
  if ext='.lua' then
    wstr := CompileLuaProgram(jo, program_str)
  else wstr := CompileProgram(jo, program_str);
  jo := nil;
  try
    n := Pos(';', wstr);
    while n > 0 do
    begin
      cnode := clonenode.CloneNode(True);
      nodename := cnode.NodeName;

      ln := LeftStr(wstr, n - 1);
      wstr := RightStr(wstr, Length(wstr) - n);
      //分解行
      n := Pos(',', ln);
      while n>0 do
      begin
        vstr := LeftStr(ln, n - 1);
        S2S(vstr, s1, s2);
        if s1='NN' then nodename := s2 else UpdateAttribute(param0.xdoc, cnode, s1, s2);
        ln := RightStr(ln, Length(ln) - n);
        n := Pos(',', ln);
      end;
      if (n<=0) and (ln<>'') then
      begin
        S2S(ln, s1, s2);
        if s1='NN' then nodename := s2 else UpdateAttribute(param0.xdoc, cnode, s1, s2);
      end;

      n := Pos(';', wstr);

      if (nodename <> '板件') and (nodename <> '五金') and (nodename <> '型材五金')
        and (nodename <> '模块') and (nodename <> '门板') then Continue;

      bg := GetAttributeValue(cnode, '基础图形', '', '');
      if (bg = 'BG::SPACE') then Continue;

      bg := GetAttributeValue(cnode, '基础图形', '', '');
      if (GetAttributeValue(cnode, '显示方式', '', '') = '3') then Continue;
      new(pbom);
      pbom.num := 1;

      textureclass := GetAttributeValue(cnode, '装饰类别', '', '');

      pbom.isoutput := True;
      pbom.id := id;
      pbom.pid := param0.pid;
      pbom.name := '';
      pbom.mat := '';
      pbom.texture := '';
      pbom.desc := '';
      pbom.l := 0;
      pbom.p := 0;
      pbom.h := 0;
      pbom.gno := param0.gno;
      pbom.gdes := param0.gdes;
      pbom.subspace := param0.subspace;
      pbom.bh := param0.boardheight;
      pbom.price_calctype := param0.pricecalctype;
      pbom.is_calc_cost := False;
      pbom.cost := 0;
      pbom.slino := -1;
      attri := cnode.AttributeNodes.FindNode('子空间');
      if attri <> nil then
      begin
        pbom.subspace := param0.subspace + attri.Text;
      end;
      attri := cnode.AttributeNodes.FindNode('名称');
      if attri <> nil then
      begin
        pbom.name := attri.Text;
      end;

      xx0 := 0;
      xx1 := 0;
      yy0 := 0;
      yy1 := 0;
      zz0 := 0;
      zz1 := 0;
      attri := cnode.AttributeNodes.FindNode('XX0');
      if attri <> nil then xx0 := MyStrToInt(attri.Text);
      attri := cnode.AttributeNodes.FindNode('XX1');
      if attri <> nil then xx1 := MyStrToInt(attri.Text);
      attri := cnode.AttributeNodes.FindNode('YY0');
      if attri <> nil then yy0 := MyStrToInt(attri.Text);
      attri := cnode.AttributeNodes.FindNode('YY1');
      if attri <> nil then yy1 := MyStrToInt(attri.Text);
      attri := cnode.AttributeNodes.FindNode('ZZ0');
      if attri <> nil then zz0 := MyStrToInt(attri.Text);
      attri := cnode.AttributeNodes.FindNode('ZZ1');
      if attri <> nil then zz1 := MyStrToInt(attri.Text);

      attri := cnode.AttributeNodes.FindNode('宽');
      if attri <> nil then
      begin
        exp.SetSubject(attri.Text);
        pbom.l := exp.ToValueInt + xx1 + (0 - xx0);
      end;
      attri := cnode.AttributeNodes.FindNode('RL');
      if (attri <> nil) and (attri.Text <> '') then pbom.l := MyStrToInt(attri.Text);
      attri := cnode.AttributeNodes.FindNode('深');
      if attri <> nil then
      begin
        exp.SetSubject(attri.Text);
        pbom.p := exp.ToValueInt + yy1 + (0 - yy0);
      end;
      attri := cnode.AttributeNodes.FindNode('高');
      if attri <> nil then
      begin
        exp.SetSubject(attri.Text);
        pbom.h := exp.ToValueInt + zz1 + (0 - zz0);
      end;
      for k := 0 to 15 do             //所有16个参数
      begin
        args[k] := 0;
        attri := cnode.AttributeNodes.FindNode('参数' + IntToStr(k));
        if (attri <> nil) and (attri.Text <> '') then
        begin
          MyVariant(attri.Text, vname, value);
          exp.SetSubject(value);
          args[k] := exp.ToValueInt;
          pbom.var_args[k] := args[k];
          pbom.var_names[k] := vname;
        end;
      end;
      if bg = 'BG::DOORRECT' then     //外盖板
      begin
        pbom.l := pbom.l + args[0] + args[1];
        pbom.h := pbom.h + args[2] + args[3];
      end;
      if bg = 'BG::RECT_X_CENGBAN_FB' then //前后倾斜层板
      begin
        pbom.p := Round(sqrt(pbom.p * pbom.p + pbom.h * pbom.h));
        pbom.h := args[0];
        pbom.bh := args[0];
        bh := args[0];
      end;
      if bg = 'BG::RECT_X_CENGBAN_LR' then //左右倾斜层板
      begin
        pbom.l := Round(sqrt(pbom.l * pbom.l + pbom.h * pbom.h));
        pbom.h := args[0];
        pbom.bh := args[0];
        bh := args[0];
      end;
      if bg = 'BG::POLYLINE' then     //线性物体
      begin
        attri := cnode.AttributeNodes.FindNode('POLYLINE');
        if (attri <> nil) and (attri.Text <> '') then
        begin
          pbom.l := PolyLineToLength(attri.Text);
          Swap(pbom.p, pbom.h);
        end;
      end;
      di := 0;
      attri := cnode.AttributeNodes.FindNode('DI');
      if attri <> nil then
        di := StrToInt(attri.Text);
      attri := cnode.AttributeNodes.FindNode('材料');
      if attri <> nil then pbom.mat := attri.Text else if textureclass=param0.textureclass then pbom.mat := param0.pmat;
      attri := cnode.AttributeNodes.FindNode('颜色');
      if attri <> nil then pbom.texture := attri.Text else if textureclass=param0.textureclass then pbom.texture := param0.pcolor;

       attri := cnode.AttributeNodes.FindNode('类别');
      if attri <> nil then
        pbom.desc := attri.Text;
      childnum := 0;
      attri := cnode.AttributeNodes.FindNode('Num');
      if (attri <> nil) and (attri.Text <> '') then pbom.num := MyStrToInt(attri.Text) * param0.num;
      attri := cnode.AttributeNodes.FindNode('Mark');
      if (attri <> nil) and (attri.Text <> '') then pbom.mark := MyStrToInt(attri.Text)
      else pbom.mark := 0;
      attri := cnode.AttributeNodes.FindNode('BJSize');
      if (attri <> nil) and (attri.Text <> '') then GraphSizeToBJSize(attri.Text, pbom);
      attri := cnode.AttributeNodes.FindNode('UD');
      if (attri <> nil) and (attri.Text <> '') then pbom.userdefine := attri.Text;
      linkpath := GetAttributeValue(cnode, '链接', '', '');

      Result := Result + 1;
      param0.blist.Add(pbom);
      inc(id);

      childnum := 0;
      childxml := '';
      if linkpath<>'' then
      begin
        childxml := EnumXML(GetXMLByLink(linkpath, qry));
        tmpnode := Xml2ChildNodes(childxml);
        if tmpnode<>nil then
        begin
          cnode.ChildNodes.Clear;
          cnode.ChildNodes.Add(tmpnode);
        end;
      end;
      if childxml <> '' then
      begin
        param := param0^;
        if textureclass<>'' then param.textureclass := textureclass;
        param.pname := pbom.name;
        param.subspace := pbom.subspace;
        param.xml := childxml;
        param.pmat := pbom.mat;
        param.pcolor := pbom.texture;
        param.pid := id - 1;
        param.pl := pbom.l;
        param.pd := pbom.p;
        param.ph := pbom.h;
        param.num := pbom.num;
        attri := cnode.AttributeNodes.FindNode('输出类型');
        if (attri <> nil) and (attri.Text <> '') then param.outputtype := attri.Text;
        if cnode.ChildNodes.Count>0 then
        begin
          param.rootnode := cnode.ChildNodes[0];
          param.xdoc := param0.xdoc;
          childnum := ImportXomItemForQuo(@param, id, slino);
        end;
      end;
      pbom.blockmemo := param0.blockmemo;
      GraphSizeToBomSize(pbom.l, pbom.p, pbom.h, di, bl, bp, bh);
      pbom.l := bl;
      pbom.p := bp;
      pbom.h := bh;
      if bh <= 36 then pbom.bh := bh; //小于等于36认为是板材厚度
      pbom.childnum := childnum;
      if (pbom.l > 1) and (pbom.p > 1) and (pbom.h <= 1) then pbom.isoutput := False;
      attri := cnode.AttributeNodes.FindNode('输出类型');
      if (attri <> nil) and ((attri.Text = '物料') or (attri.Text = '无')) then
        pbom.isoutput := False;
      attri := cnode.AttributeNodes.FindNode('装饰类别');
      if (attri <> nil) and ((attri.Text = '趟门') or (attri.Text = '掩门') or (pbom.myclass = '趟门,趟门') or (pbom.myclass = '掩门,掩门')) then
        pbom.isoutput := False;

      if (pbom.l < 1) or (pbom.p < 1) or (pbom.h < 1) then pbom.isoutput := False; //过滤掉尺寸小于等于零的物料，xml情况复杂
      if (pbom.l > 1) and (pbom.p > 1) and (pbom.h <= 1) then pbom.isoutput := False; //过滤掉一些尺寸为0的物料数据
    end;
  except
  end;
end;

class function TLocalObject.fromPygetobj(url:string):string;
var
  strstream :TStringStream;
  str,files,xml,name  :string;
  jo:ISuperObject;
  i,n,resultflag:Integer;
  idhtp :TIdHTTP;
begin
  result:='';
  jo := TSuperObject.Create();
  idhtp:= TIdHTTP.Create(nil);
  try
    try
      strstream := TStringStream.Create('');
      idhtp.Get(url,strstream);
      str := strstream.DataString;
      str := utf8decode(str);
      jo := SO(str) ;
      resultflag:=jo.I['result'];
    except
      resultflag :=0;
    end;
  finally
    if resultflag = 0 then
    begin
    str:='';
    end;
    result:= str;
    idhtp.Free;
    strstream.Free;
    jo := nil;
  end;
end;

procedure TLocalObject.LoadXML2Quo(xml: string);
var
  cid, id, i, l, d, h, j, slino, bh: Integer;
  pbom, pbom2       : ^BomRecord;
  p                 : Pointer;
  name, mat, color, des, gcb, extra: string;
  root, node, cnode, attri: IXMLNode;
  param             : QuoParam;
  xdoc:IXMLDocument;
begin
  id := 1;
  slino := 1;
  XYZCalcPrice.UnloadBom(False);
  if not Assigned(XYZCalcPrice.bomQuolist) then XYZCalcPrice.bomQuolist := TList.Create;
  if not Assigned(slidingQuolist) then slidingQuolist := TList.Create;
  if not Assigned(doorsQuolist) then doorsQuolist := TList.Create;
  mBG := '';

  try
    xdoc := XMLDoc.LoadXMLData('<?xml version="1.0" encoding="gb2312"?>'+xml);
    node := xdoc.ChildNodes[1];
    RemoveInvisibleNode(node);
    cid := 0;

    if node.nodename <> '产品' then exit;
    name := '';
    l := 0;
    d := 0;
    h := 0;
    bh := 18;
    mat := '';
    color := '';
    des := '';
    gcb := '';
    extra := '';
    if node.ChildNodes[0].nodename = '产品' then
    begin
      bh := GetAttributeValue(node.ChildNodes[0], '板材厚度', bh, bh);
      extra := GetAttributeValue(node.ChildNodes[0], 'Extra', '', '');
    end;
    attri := node.AttributeNodes.FindNode('Extra');
    if attri <> nil then extra := attri.Text;
    attri := node.AttributeNodes.FindNode('名称');
    if attri <> nil then name := attri.Text;
    attri := node.AttributeNodes.FindNode('描述');
    if attri <> nil then des := attri.Text;
    attri := node.AttributeNodes.FindNode('CB');
    if attri <> nil then gcb := attri.Text;
    attri := node.AttributeNodes.FindNode('宽');
    if attri <> nil then l := StrToInt(attri.Text);
    attri := node.AttributeNodes.FindNode('深');
    if attri <> nil then
      d := StrToInt(attri.Text);
    attri := node.AttributeNodes.FindNode('高');
    if attri <> nil then
      h := StrToInt(attri.Text);
    attri := node.AttributeNodes.FindNode('材料');
    if attri <> nil then
      mat := attri.Text;
    attri := node.AttributeNodes.FindNode('颜色');
    if attri <> nil then
      color := attri.Text;
    attri := node.AttributeNodes.FindNode('基础图形');
    if attri <> nil then
      mBG := attri.Text;
    for j := 0 to 15 do
    begin
      mVName[j] := '';
      mVValue[j] := '';
      mC[j] := 0;
      attri := node.AttributeNodes.FindNode('参数' + IntToStr(j));
      if attri <> nil then
        MyVariant(attri.Text, mVName[i], mVValue[j]);
      mC[j] := MyStrToInt(mVValue[j]);
    end;
    inc(cid);
    if node.ChildNodes.Count > 0 then
    begin
      param.productid := mProductList.Count-1;
      param.cid := cid - 1;
      param.boardheight := bh;
      param.blist := XYZCalcPrice.bomQuolist;
      param.gno := name;
      param.gdes := des;
      param.gcb := gcb;
      param.extra := extra;
      param.pname := '';
      param.subspace := '';
      param.xml := node.ChildNodes[0].xml;
      param.pmat := mat;
      param.pcolor := color;
      param.pid := -1;
      param.pl := l;
      param.pd := d;
      param.ph := h;
      param.outputtype := '';
      param.pricecalctype := '';
      param.num := 1;
      param.blockmemo := '';
      param.number_text := '';
      param.rootnode := node.ChildNodes[0];
      param.xdoc := xdoc;
      ImportXomItemForQuo(@param, id, slino);
    end;

    //拆分数据
    for i := XYZCalcPrice.bomQuolist.Count - 1 downto 0 do
    begin
      pbom := XYZCalcPrice.bomQuolist[i];
      if pbom.num > 1 then
      begin
        for j := 1 to pbom.num - 1 do
        begin
          new(pbom2);
          pbom2^ := pbom^;
          pbom2.num := 1;
          XYZCalcPrice.bomQuolist.Add(pbom2);
        end;
        pbom.num := 1;
      end;
    end;
  finally
    xdoc := nil;
  end;
  qry := TADOQuery.Create(nil);
  //XYZCalcPrice.qry := qry;
  for i := 0 to XYZCalcPrice.bomQuolist.Count - 1 do
  begin
    p := XYZCalcPrice.bomQuolist[i];
    XYZCalcPrice.Des2Des(p);
  end;
end;

class function TLocalObject.GetXMLByLink(link: Widestring; qry:TADOQuery): Widestring;
var sql, filename:string;
  url, objstr, name :string;
  i, n, seq :Integer;
  jo, ja, cjo:ISuperObject;
begin
  Result := '';
  if link='' then exit;
  Result := gLinkXML.S[link];
  {if Result<>'' then exit;
  try
    url:=Format(UrlIp +'/xmlbylink/?link=%s&factorypath=%s',[HTTPEncode(UTF8Encode(link)),HTTPEncode(UTF8Encode(factoryDataPath))]);
    objstr := fromPygetobj(url);    //修改
    if objstr='' then exit;
    jo := TSuperObject.Create();
    jo := SO(objstr) ;
    ja := jo.O['XMLByLink'];
    n := ja.AsArray.Length;
    for i:=0 to n-1 do
    begin
      cjo := ja.AsArray.O[i];
      gLinkXML.S[cjo.S['path']] := cjo.S['XML'];
      Result := gLinkXML.S[link];
    end;
    jo :=nil;
    //qry.Close;
  except
  end;}
  if Result<>'' then exit;
  filename := StringReplace(link, '模板目录\', GetDataPath, [rfReplaceAll]);
  filename := ChangeFileExt(filename, '.xmlitem');
  if FileExists(filename) then
  begin
    gLinkXML.S[link] := MyUtils.ReadStringFromFile(filename);
    Result := gLinkXML.S[link];
  end;
end;

class procedure TLocalObject.InitBGHash;
begin
  gBGHash.Clear;
  SearchBGDir(MyUtils.GetQuickDrawPath + 'BaseGraph');
end;

class function TLocalObject.SearchBGDir(dir: string): Integer;
var
  vSearchRec        : TSearchRec;
  i, c, n           : Integer;
  filename          : WideString;
  ext, xml, bg      : string;
begin
  c := 0;
  i := FindFirst(dir + string('\*.*'), faAnyFile, vSearchRec);
  while (i = 0) do
  begin
    if vSearchRec.FindData.cFileName[0] = '.' then
    begin
      i := FindNext(vSearchRec);
      Continue;
    end;

    if (vSearchRec.FindData.dwFileAttributes and FILE_ATTRIBUTE_DIRECTORY) <> 0 then
    begin
      //n := SearchBGDir(dir + string('\') + string(vSearchRec.FindData.cFileName));
      //c := n + c;
      i := FindNext(vSearchRec);
      Continue;
    end;

    filename := vSearchRec.FindData.cFileName;
    ext := RightStr(filename, 3);
    if StrLower(pchar(ext)) = 'x2d' then
    begin
      xml := ReadStringFromFile(dir + '\' + filename);
      if Pos('V="1"', xml) > 0 then
      begin
        bg := ChangeFileExt(filename, '');
        gBGHash.Add(bg, xml);
      end;
      inc(c);
    end;
    i := FindNext(vSearchRec);
  end;
  FindClose(vSearchRec);
  Result := c;
end;

class procedure TLocalObject.InitErpList(list: TList; jo:ISuperObject );
var
  url, objstr, name :string;
  ja, cjo:ISuperObject;
  p                 : PErpMat;
  i, n, seq           : Integer;
  str               : string[64];
  dbname:string;
begin
  if jo.S['ErpItem'] = '' then exit;
  ja := jo.O['ErpItem'];
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(p);
    p.id := cjo.I['ID'];
    p.name := cjo.S['name'];
    p.mat := cjo.S['mat'];
    p.color := cjo.S['color'];
    p.h := cjo.I['h'];
    p.flag := cjo.S['flag'];
    p.myclass := cjo.S['myclass'];
    p.myunit := cjo.S['unit'];
    list.Add(p);
  end;
  jo:=nil;
end;

class procedure TLocalObject.UninitErpList(list: TList);
var
  i                 : Integer;
begin
  for i := 0 to list.Count - 1 do
  begin
    dispose(list[i]);
  end;
end;

class procedure TLocalObject.InitQuoHash(jo: ISuperObject);    //q:TADOQuery; connstr: string
begin
  XYZCalcPrice.InitHash(UrlIp, factoryDataPath, jo);    //q, connstr,
end;

class procedure TLocalObject.ReleaseQuoHash;
begin
  XYZCalcPrice.ReleaseHash;
end;

class procedure TLocalObject.InitBomHash(jo: ISuperObject);          //q:TADOQuery; connstr: string
type
  MyString = record
    wjno, wjname: string;
  end;
type
  PMyString = ^MyString;
var
  list              : TList;
  key, str          : string;
  i                 : Integer;
  M                 : ^StrMap;
  prule             : PBomRuleRec;
  pwjrule           : PWJRuleRec;
  pcbomrule         : PBom2RuleRec;
  pms               : PMyString;
  phole             : THoleConfig;
  pbs               : PBomStd;
  pkc               : TKCConfig;
  pwf               : PWorkflow;
  phwj              : PHoleWjItem;
  inif              : TIniFile;
begin
  ruleHash := THashedStringlist.Create;
  wjruleHash := THashedStringlist.Create;
  childbomHash := THashedStringlist.Create;
  holeconfigHash := THashedStringlist.Create;
  kcconfigHash := THashedStringlist.Create;
  des2wuliao := TMyStringHash.Create(4096);
  seqInfoHash := TStringHash.Create(4096);
  classseqInfoHash := TStringHash.Create(4096);
  linecalcList := TStringHash.Create(4096);
  bomstdList := TList.Create;
  workflowlist := TList.Create;
  //holeWjList := TList.Create;

  gROC.bj_out_classname := True;
  gROC.bj_out_myclass := False;
  gROC.bj_out_name := False;
  gROC.bj_out_mat := True;
  gROC.bj_out_color := True;
  gROC.bj_out_size := True;
  gROC.bj_out_price := True;
  gROC.wl_out_classname := True;
  gROC.wl_out_myclass := False;
  gROC.wl_out_name := True;
  gROC.wl_out_mat := True;
  gROC.wl_out_color := True;
  gROC.wl_out_size := True;
  gROC.wl_out_kc := True;
  gROC.wl_out_fb := True;
  gROC.wl_out_memo := True;
  gROC.wl_out_hole := True;
  configseqInfoHash(jo);
  configclassseqInfoHash(jo);
  //configgROC(jo);
  configworkflow(jo);
end;

class procedure TLocalObject.ReleaseBomHash;
var
  list              : TList;
  i, j              : Integer;
  M                 : ^StrMap;
  prule             : PBomRuleRec;
  pcbomrule         : PBom2RuleRec;
  pwjrule           : PWJRuleRec;
  //pexp              :PSlidingExp;
begin
  //释放物料减量规则表
  for i := 0 to ruleHash.Count - 1 do
  begin
    list := TList(ruleHash.Objects[i]);
    for j := 0 to list.Count - 1 do
    begin
      prule := list[j];
      dispose(prule);
    end;
    list.Free;
  end;
  ruleHash.Clear;
  ruleHash.Free;

  for i := 0 to wjruleHash.Count - 1 do
  begin
    list := TList(wjruleHash.Objects[i]);
    for j := 0 to list.Count - 1 do
    begin
      pwjrule := list[j];
      dispose(pwjrule);
    end;
    list.Free;
  end;
  wjruleHash.Clear;
  wjruleHash.Free;

  for i := 0 to childbomHash.Count - 1 do
  begin
    list := TList(childbomHash.Objects[i]);
    for j := 0 to list.Count - 1 do
    begin
      pcbomrule := list[j];
      dispose(pcbomrule);
    end;
    list.Free;
  end;
  childbomHash.Clear;
  childbomHash.Free;

  for i := 0 to holeconfigHash.Count - 1 do
  begin
    list := TList(holeconfigHash.Objects[i]);
    for j := 0 to list.Count - 1 do
    begin
      dispose(list[j]);
    end;
    list.Free;
  end;
  holeconfigHash.Clear;
  holeconfigHash.Free;

  for i := 0 to kcconfigHash.Count - 1 do
  begin
    list := TList(kcconfigHash.Objects[i]);
    for j := 0 to list.Count - 1 do
    begin
      dispose(list[j]);
    end;
    list.Free;
  end;
  kcconfigHash.Clear;
  kcconfigHash.Free;

  des2wuliao.Clear;
  FreeAndNil(des2wuliao);

  linecalcList.Clear;
  FreeAndNil(linecalcList);

  for i := 0 to bomstdList.Count - 1 do
  begin
    dispose(bomstdList[i]);
  end;
  bomstdList.Clear;
  bomstdList.Free;

  for i := 0 to workflowlist.Count - 1 do
  begin
    dispose(workflowlist[i]);
  end;
  workflowlist.Clear;
  workflowlist.Free;

  {for i := 0 to holeWjList.Count - 1 do
  begin
    dispose(holeWjList[i]);
  end;
  holeWjList.Clear;
  holeWjList.Free;}

  seqInfoHash.Clear;
  seqInfoHash.Free;
  seqInfoHash := nil;

  classseqInfoHash.Clear;
  classseqInfoHash.Free;
  classseqInfoHash := nil;
end;

class procedure TLocalObject.InitBoardMatList(jo:ISuperObject);
var
  p                 : PBoardMat;
  url, objstr :string;
  i, n, seq :Integer;
  ja, cjo:ISuperObject;
begin
  gBoardMatList := TList.Create;
  if jo.S['boardmat'] = '' then exit;
  ja := jo.O['boardmat'];
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(p);
    p.name := cjo.S['name'];
    p.bh := cjo.I['bh'];
    p.alias := cjo.S['alias'];
    p.alias2 := cjo.S['alias2'];
    p.alias3 := cjo.S['alias3'];
    p.color := cjo.S['color'];
    gBoardMatList.Add(p);
  end;
  jo:=nil;
end;


class procedure TLocalObject.UninitBoardMatList;
var
  i                 : Integer;
  p                 : PBoardMat;
begin
  for i := 0 to gBoardMatList.Count - 1 do
  begin
    p := gBoardMatList[i];
    p.name := '';
    p.alias := '';
    p.alias2 := '';
    p.alias3 := '';
    p.color := '';
    dispose(p);
  end;
  gBoardMatList.Clear;
  FreeAndNil(gBoardMatList);
end;

class procedure TLocalObject.configseqInfoHash(jo:ISuperObject);
Var
  url, objstr, bomname :string;
  i, n, bomseq :Integer;
  ja, cjo:ISuperObject;
begin
  //url:=Format(UrlIp+'/seqinfo/?factorypath=%s',[HTTPEncode(UTF8Encode(factoryDataPath))]);      //修改
  //objstr :=fromPygetobj(url);    //修改
  //if objstr='' then exit;
  //jo := TSuperObject.Create();
  //jo := SO(objstr) ;

  ja := jo.O['seqinfo'];
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    bomname :=cjo.S['bomname'];
    bomseq :=cjo.I['bomseq'];
    seqInfoHash.Add(bomname, bomseq);
  end;
  jo:=nil;
end;

class procedure TLocalObject.configclassseqInfoHash(jo:ISuperObject);
Var
  url, objstr, name :string;
  i, n, seq :Integer;
  ja, cjo:ISuperObject;
begin
  //url:=Format(UrlIp+'/classseqinfo/?factorypath=%s',[HTTPEncode(UTF8Encode(factoryDataPath))]);      //修改
  //objstr :=fromPygetobj(url);    //修改
  if objstr='' then exit;
  jo := TSuperObject.Create();
  jo := SO(objstr) ;
  ja := jo.O['classseqinfo'];
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    name :=cjo.S['name'];
    seq :=cjo.I['seq'];
    classseqInfoHash.Add(name, seq);
  end;
  jo:=nil;
end;

class procedure TLocalObject.configgROC(jo:ISuperObject);
Var
  url, objstr, name :string;
  i, n, seq :Integer;
  ja, cjo:ISuperObject;
begin
  url:=Format(UrlIp+'/reportsconfig/?factorypath=%s',[HTTPEncode(UTF8Encode(factoryDataPath))]);      //修改
  objstr :=fromPygetobj(url);    //修改
  if objstr='' then exit;
  jo := TSuperObject.Create();
  jo := SO(objstr) ;
  ja := jo.O['reportsconfig'];
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    gROC.bj_out_classname := cjo.B['bj_out_classname'];
    gROC.bj_out_myclass := cjo.B['bj_out_myclass'];
    gROC.bj_out_name := cjo.B['bj_out_name'];
    gROC.bj_out_mat := cjo.B['bj_out_mat'];
    gROC.bj_out_color := cjo.B['bj_out_color'];
    gROC.bj_out_size := cjo.B['bj_out_size'];
    gROC.bj_out_price := cjo.B['bj_out_price'];

    gROC.wl_out_classname := cjo.B['wl_out_classname'];
    gROC.wl_out_myclass := cjo.B['wl_out_myclass'];
    gROC.wl_out_name := cjo.B['wl_out_name'];
    gROC.wl_out_mat := cjo.B['wl_out_mat'];
    gROC.wl_out_color := cjo.B['wl_out_color'];
    gROC.wl_out_size := cjo.B['wl_out_size'];
    gROC.wl_out_kc := cjo.B['wl_out_kc'];
    gROC.wl_out_fb := cjo.B['wl_out_fb'];
    gROC.wl_out_memo := cjo.B['wl_out_memo'];
    gROC.wl_out_hole := cjo.B['wl_out_hole'];
  end;
  jo:=nil;
end;

class procedure TLocalObject.configworkflow(jo:ISuperObject);
Var
  url, objstr, name :string;
  i, n, seq :Integer;
  ja, cjo:ISuperObject;
  pwf               : PWorkflow;
begin
  //url:=Format(UrlIp+'/workflow/?factorypath=%s',[HTTPEncode(UTF8Encode(factoryDataPath))]);      //修改
  //objstr :=fromPygetobj(url);    //修改
  //if objstr='' then exit;
  //jo := TSuperObject.Create();
  //jo := SO(objstr) ;
  ja := jo.O['workflow'];
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pwf);
    pwf.id := cjo.I['ID'];
    pwf.name := cjo.S['name'];
    pwf.bomstd := cjo.S['bomstd'];
    pwf.hole := cjo.S['hole'];
    pwf.board_cut := cjo.I['board_cut'];
    pwf.edge_banding := cjo.I['edge_banding'];
    pwf.punching := cjo.I['punching'];
    workflowlist.Add(pwf);
  end;
  jo:=nil;
end;
procedure TLocalObject.SlidingAndDoorInit;
begin
  bomlist := TList.Create;
  bomdeslist := TStringList.Create;
  doordeslist := TStringList.Create;
  slidingdeslist := TStringList.Create;
  //趟门
  mSlidingColorList := TList.Create;
  mSlidingExpList := TList.Create;
  mSlidingTypeList := TList.Create;
  mSlidingParamList := TList.Create;
  mHBoxParamList := TList.Create;
  mTrackParamList := TList.Create;
  mUDBoxParamList := TList.Create;
  mVBoxParamList := TList.Create;
  mPanelTypeList := TList.Create;
  mSlidingAccessoryList := TList.Create;
  mSlidingColorClassList := TList.Create;
  mSlidingMyClassGroupList := TList.Create;
  mSlidingWjBomList := TList.Create;
  mSlidingWjBomDetailList := TList.Create;
  mSSExpList := TList.Create;
  mSlidingPriceList := TList.Create;
  mSlidingColorClass2List := TList.Create;
  mPanelBomDetailList := TList.Create;
  mPriceTableList := TList.Create;
  mDoorsList := TObjectList.Create(True);
  mIsSetDoors := False;
  mIsModify := False;
  OptionalAccList := TList.Create; // 自选配件列表
  SlidingObjList := TSuperObject.Create();
  SfgParam := TSuperObject.Create();
  mCfglist := TList.Create; //门转换表
  SlidingHfg2List := TList.Create;
  SlidingHfg3List := TList.Create;
  SlidingHfg4List := TList.Create;
  SlidingSfg2List := TList.Create;
  SlidingSfg3List := TList.Create;
  SlidingSfg4List := TList.Create;
  HSHBoxParamList := TList.Create;
  SHBoxParamList := TList.Create;
  //掩门
  mColorList := TList.Create;
  mExpList := TList.Create;
  mTypeList := TList.Create;
  mParamList := TList.Create;
  mHandleList := TList.Create;
  mDoorHBoxParamList := TList.Create;
  mDoorPanelTypeList := TList.Create;
  mAccessoryList := TList.Create;
  mColorClassList := TList.Create;
  mShutterExpList := TList.Create;
  mWJBomList := TList.Create;
  mWJBomDetailList := TList.Create;
  mPriceList := TList.Create;
  mHingeList := TList.Create;
  mCurHingeList := TList.Create;
  mColorClass2List := TList.Create;
  mDoorPanelBomDetailList := TList.Create;
  mDoorXMLList := TList.Create;
end;

procedure TLocalObject.InitData();
var connstr:string;
qry:TADOQuery;
jo:ISuperObject;
begin
  qry := TADOQuery.Create(nil);

  //载入库
  //LoadMyLibrary;
  //初始化导出报表的插件TexttoXls.dll
  //InitIConvertXls;
  //初始化基础图形库
  gBGHash := TMyStringHash.Create(1024);
  InitBGHash;
  //初始化插件
  //InitPluginsList();

  //初始化ERP转换表

  //初始化模块列表
  gLinkXML := TSuperObject.Create();
  gFiledNameList := TSuperObject.Create();
  desData := TMyStringHash.Create(1024);
  LuaData := TMyStringHash.Create(1024);
  jo := TSuperObject.Create();
  gFiledNameList.O['Bom'] := jo;
  jo := TSuperObject.Create();
  gFiledNameList.O['GetDeviceOutputString'] := jo;

  connstr := Format('Provider=Microsoft.Jet.OLEDB.4.0;Data Source=%sdata.mdb;Persist Security Info=False'
    , [MyUtils.GetDataPath]);

  //InitQuoHash();             //qry, connstr

  connstr := Format('Provider=Microsoft.Jet.OLEDB.4.0;Data Source=%sXScriptDb.mdb;Persist Security Info=False'
    , [MyUtils.GetDataPath]);

  FreeAndNil(qry);
end;

procedure TLocalObject.Uninit;
var
  i                 : Integer;
  poi, poi2         : ^BomOrderItem;
begin

  bjBomList.Clear;
  wjBomList.Clear;

  bjBomList2.Clear;
  wjBomList2.Clear;

  slBomList.Clear;
  for i := 0 to slBomList2.Count - 1 do
  begin
    dispose(slBomList2[i]);
  end;
  slBomList2.Clear;

  dlBomList.Clear;
  for i := 0 to dlBomList2.Count - 1 do
  begin
    dispose(dlBomList2[i]);
  end;
  dlBomList2.Clear;

  UnloadBom;

  if XYZCalcPrice.bomQuolist <> nil then
    XYZCalcPrice.UnloadBom;
end;
procedure TLocalObject.ClearAllBomList;
Var
  i,j       :Integer;
  poi       :PBomOrderItem;
  mp        :TProductItem;
  pbom      :PBomRecord;
  list :TList;
  pcbomrule :PBom2RuleRec;
  pwjrule   : PWJRuleRec;
  prule:    PBomRuleRec;
  pbs       : PBomStd;
begin
  for i := 0 to bomlist.Count - 1 do
  begin
    poi:= bomlist[i];
    poi.code:='';
    poi.name:='';
    poi.mat:='';
    poi.mat2:='';
    poi.mat3:='';
    poi.color:='';
    poi.workflow:='';
    poi.tmp_soz:='';
    poi.desc:='';
    poi.bomdes:='';
    poi.bomwjdes:='';
    poi.bomstddes:='';
    poi.childbom:='';
    poi.myclass:='';
    poi.nodename:='';
    poi.linecalc:='';
    poi.bomstd:='';
    poi.bg:='';

    poi.holestr:='';
    poi.kcstr:='';

    poi.memo:='';
    poi.gno:='';
    poi.gdes:='';
    poi.gcb:='';
    poi.extra:='';
    poi.bomdes:='';
    poi.fbstr:='';
    poi.subspace:='';
    poi.process:='';
    poi.ls:='';
    poi.myunit:='';
    poi.bomtype:='';
    poi.bdxmlid:='';
    poi.user_fbstr:='';

    for j := 0 to 15 do
    begin
    poi.var_names[j] := '';
    end;
    poi.a_hole_info:='';
    poi.b_hole_info:='';
    poi.holeinfo:='';

    poi.outputtype:='';
    poi.holeconfig_flag:='';
    poi.kcconig_flag:='';
    poi.bg_data:='';
    poi.mBGParam:='';

    poi.bg_filename:='';
    poi.mpr_filename:='';
    poi.bpp_filename:='';
    poi.devcode:='';

    poi.extend:='';
    poi.group:='';
    poi.packno:='';
    poi.userdefine:='';
    poi.erpunit:='';

    poi.erpmatcode:='';
    poi.blockmemo:='';
    poi.number_text:='';
    dispose(poi);
  end;
  bomlist.Clear;


  for i := 0 to basewjlist.count -1 do
  begin
    poi := basewjlist[i];
    poi.code:='';
    poi.name:='';
    poi.mat:='';
    poi.mat2:='';
    poi.mat3:='';
    poi.color:='';
    poi.workflow:='';
    poi.tmp_soz:='';
    poi.desc:='';
    poi.bomdes:='';
    poi.bomwjdes:='';
    poi.bomstddes:='';
    poi.childbom:='';
    poi.myclass:='';
    poi.nodename:='';
    poi.linecalc:='';
    poi.bomstd:='';
    poi.bg:='';

    poi.holestr:='';
    poi.kcstr:='';

    poi.memo:='';
    poi.gno:='';
    poi.gdes:='';
    poi.gcb:='';
    poi.extra:='';
    poi.bomdes:='';
    poi.fbstr:='';
    poi.subspace:='';
    poi.process:='';
    poi.ls:='';
    poi.myunit:='';
    poi.bomtype:='';
    poi.bdxmlid:='';
    poi.user_fbstr:='';

    for j := 0 to 15 do
    begin
    poi.var_names[j] := '';
    end;
    poi.a_hole_info:='';
    poi.b_hole_info:='';
    poi.holeinfo:='';

    poi.outputtype:='';
    poi.holeconfig_flag:='';
    poi.kcconig_flag:='';
    poi.bg_data:='';
    poi.mBGParam:='';

    poi.bg_filename:='';
    poi.mpr_filename:='';
    poi.bpp_filename:='';
    poi.devcode:='';

    poi.extend:='';
    poi.group:='';
    poi.packno:='';
    poi.userdefine:='';
    poi.erpunit:='';

    poi.erpmatcode:='';
    poi.blockmemo:='';
    poi.number_text:='';
    dispose(poi);
  end;
  basewjlist.Clear;

  desdata.Clear;
  LuaData.Clear;

  {for i := 0 to childbomHash.Count - 1 do
  begin
    list := TList(childbomHash.Objects[i]);
    for j := 0 to list.Count - 1 do
    begin
      pcbomrule := list[j];
      pcbomrule.bclass :='';
      pcbomrule.pname :='';
      pcbomrule.name :='';
      pcbomrule.l :='';
      pcbomrule.p :='';
      pcbomrule.h :='';
      pcbomrule.mat :='';
      pcbomrule.color :='';
      pcbomrule.holestr :='';
      pcbomrule.kcstr :='';
      pcbomrule.ono :='';
      pcbomrule.bomstd :='';
      pcbomrule.bomtype :='';
      pcbomrule.a_face :='';
      pcbomrule.b_face :='';
      pcbomrule.memo :='';
      pcbomrule.fbstr :='';
      pcbomrule.bg_filename :='';
      pcbomrule.mpr_filename :='';
      pcbomrule.bpp_filename :='';
      pcbomrule.devcode :='';
      pcbomrule.workflow :='';
      dispose(pcbomrule);
    end;
    list.Free;
  end;
  childbomHash.Clear;
  for i := 0 to wjruleHash.Count - 1 do
  begin
    list := TList(wjruleHash.Objects[i]);
    for j := 0 to list.Count - 1 do
    begin
      pwjrule := list[j];
      pwjrule.myclass1:='';
      pwjrule.myclass2:='';
      pwjrule.wjname :='';
      pwjrule.wjno :='';
      pwjrule.myunit :='';
      pwjrule.myunit2 :='';
      pwjrule.mat:='';
      pwjrule.color:='';
      dispose(pwjrule);
    end;
    list.Free;
  end;
  wjruleHash.Clear;
  for i := 0 to ruleHash.Count - 1 do
  begin
    list := TList(ruleHash.Objects[i]);
    for j := 0 to list.Count - 1 do
    begin
      prule := list[j];
      prule.myclass1:='';
      prule.myclass2:='';
      prule.mat:='';
      prule.holestr:='';
      prule.kcstr:='';
      prule.memo:='';
      prule.fbstr:='';
      dispose(prule);
    end;
    list.Free;
  end;
  ruleHash.Clear;
  for i := 0 to bomstdList.Count - 1 do
  begin
    pbs := bomstdList[i];
    pbs.myclass1 := '';
    pbs.myclass2 := '';
    pbs.stdflag := '';
    dispose(pbs);
  end;
  bomstdList.Clear;

  for i := 0 to holeconfigHash.Count - 1 do
  begin
    list := TList(holeconfigHash.Objects[i]);
    for j := 0 to list.Count - 1 do
    begin
      dispose(list[j]);
    end;
    list.Free;
  end;
  holeconfigHash.Clear;

  for i := 0 to kcconfigHash.Count - 1 do
  begin
    list := TList(kcconfigHash.Objects[i]);
    for j := 0 to list.Count - 1 do
    begin
      dispose(list[j]);
    end;
    list.Free;
  end;
  kcconfigHash.Clear;

  des2wuliao.Clear;}
  //linecalcList.Clear;
end;

procedure TLocalObject.UninitData();
begin
  if Assigned(HoleWjList) then UninitHoleWjList();
  if Assigned(gBoardMatList) then UninitBoardMatList();
  if Assigned(ruleHash) then ReleaseBomHash;
  if Assigned(XYZCalcPrice.ptableList) then ReleaseQuoHash;
  if Assigned(gErpItemList) then UninitErpList(gErpItemList);
  gLinkXML := nil;
  gFiledNameList := nil;
  gBGHash.Clear;
  FreeAndNil(gBGHash);
  desdata.Clear;
  FreeAndNil(desdata);
  LuaData.Clear;
  FreeAndNil(LuaData);
end;

procedure TLocalObject.InitBgMinAndMax;
var
  i                 : Integer;
  p                 : PBomOrderItem;
  bg                : string;
begin
  for i := 0 to bomlist.Count - 1 do
  begin
    p := bomlist[i];
    bg := p.bg;
    if p.bg <> 'BG::RECT' then p.bg := StringReplace(p.bg, '::', '_', [rfReplaceAll]);

    p.bg_l_minx := 0;
    p.bg_l_maxx := p.gp;
    p.bg_l_miny := 0;
    p.bg_l_maxy := p.gh;

    p.bg_d_minx := 0;
    p.bg_d_maxx := p.gl;
    p.bg_d_miny := 0;
    p.bg_d_maxy := p.gp;

    p.bg_b_minx := 0;
    p.bg_b_maxx := p.gl;
    p.bg_b_miny := 0;
    p.bg_b_maxy := p.gh;

    p.bg_r_minx := p.bg_l_minx;
    p.bg_r_maxx := p.bg_l_maxx;
    p.bg_r_miny := p.bg_l_miny;
    p.bg_r_maxy := p.bg_l_maxy;

    p.bg_u_minx := p.bg_d_minx;
    p.bg_u_maxx := p.bg_d_maxx;
    p.bg_u_miny := p.bg_d_miny;
    p.bg_u_maxy := p.bg_d_maxy;

    p.bg_f_minx := p.bg_b_minx;
    p.bg_f_maxx := p.bg_b_maxx;
    p.bg_f_miny := p.bg_b_miny;
    p.bg_f_maxy := p.bg_b_maxy;
    InitBgMinAndMaxItem(p);

    p.bg := bg;
  end;
end;

procedure TLocalObject.InitBgMinAndMaxItem(var p: PBomOrderItem);
var
  root, node, cnode, attri: IXMLNode;
  i, j              : Integer;
  xml, str          : string;
  minx, miny, maxx, maxy: Integer;
  pt                : ^TGPPoint;
  procedure AddList;
  var
    i               : Integer;
  begin
    for i := 0 to mTempList.Count - 1 do
    begin
      dispose(mTempList[i]);
    end;
    mTempList.Clear;
    for i := 0 to node.ChildNodes.Count - 1 do
    begin
      cnode := node.ChildNodes[i];
      if cnode.nodename <> 'Point' then Continue;
      new(pt);
      attri := cnode.AttributeNodes.FindNode('X');
      str := attri.Text;
      mExp.SetSubject(str);
      pt.x := mExp.ToValueInt;
      attri := cnode.AttributeNodes.FindNode('Y');
      str := attri.Text;
      mExp.SetSubject(str);
      pt.y := mExp.ToValueInt;
      mTempList.Add(pt);
    end;
  end;
  procedure GetMinAndMax;
  var
    i               : Integer;
  begin
    pt := mTempList[0];
    minx := pt.x;
    miny := pt.y;
    maxx := pt.x;
    maxy := pt.y;
    for i := 0 to mTempList.Count - 1 do
    begin
      pt := mTempList[i];
      if minx > pt.x then minx := pt.x;
      if maxx < pt.x then maxx := pt.x;
      if miny > pt.y then miny := pt.y;
      if maxy < pt.y then maxy := pt.y;
    end;
  end;
  procedure GetMinAndMax_FromX(var min0, max0, min1, max1: Integer);
  var
    i               : Integer;
  begin
    for i := 0 to mTempList.Count - 1 do
    begin
      pt := mTempList[i];
      if miny = pt.y then
      begin
        min0 := pt.x;
        max0 := pt.x;
      end;
      if maxy = pt.y then
      begin
        min1 := pt.x;
        max1 := pt.x;
      end;
    end;
    for i := 0 to mTempList.Count - 1 do
    begin
      pt := mTempList[i];
      if miny = pt.y then
      begin
        if (min0 > pt.x) then min0 := pt.x;
        if (max0 < pt.x) then max0 := pt.x;
      end;
      if maxy = pt.y then
      begin
        if (min1 > pt.x) then min1 := pt.x;
        if (max1 < pt.x) then max1 := pt.x;
      end;
    end;
  end;
  procedure GetMinAndMax_FromY(var min0, max0, min1, max1: Integer);
  var
    i               : Integer;
  begin
    for i := 0 to mTempList.Count - 1 do
    begin
      pt := mTempList[i];
      if minx = pt.x then
      begin
        min0 := pt.y;
        max0 := pt.y
      end;
      if maxx = pt.x then
      begin
        min1 := pt.y;
        max1 := pt.y;
      end;
    end;
    for i := 0 to mTempList.Count - 1 do
    begin
      pt := mTempList[i];
      if minx = pt.x then
      begin
        if (min0 > pt.y) then min0 := pt.y;
        if (max0 < pt.y) then
          max0 := pt.y
      end;
      if maxx = pt.x then
      begin
        if (min1 > pt.y) then min1 := pt.y;
        if (max1 < pt.y) then max1 := pt.y;
      end;
    end;
  end;
begin
  xml := gBGHash.ValueOf(bgname(p.bg));
  if xml = '' then exit;

  try
    mExp.AddVariable('CA', '', IntToStr(p.var_args[0]), '', '');
    mExp.AddVariable('CB', '', IntToStr(p.var_args[1]), '', '');
    mExp.AddVariable('CC', '', IntToStr(p.var_args[2]), '', '');
    mExp.AddVariable('CD', '', IntToStr(p.var_args[3]), '', '');
    mExp.AddVariable('CE', '', IntToStr(p.var_args[4]), '', '');
    mExp.AddVariable('CF', '', IntToStr(p.var_args[5]), '', '');
    mExp.AddVariable('CG', '', IntToStr(p.var_args[6]), '', '');
    mExp.AddVariable('CH', '', IntToStr(p.var_args[7]), '', '');

    mExp.AddVariable('CI', '', IntToStr(p.var_args[8]), '', '');
    mExp.AddVariable('CJ', '', IntToStr(p.var_args[9]), '', '');
    mExp.AddVariable('CK', '', IntToStr(p.var_args[10]), '', '');
    mExp.AddVariable('CL', '', IntToStr(p.var_args[11]), '', '');
    mExp.AddVariable('CM', '', IntToStr(p.var_args[12]), '', '');
    mExp.AddVariable('CN', '', IntToStr(p.var_args[13]), '', '');
    mExp.AddVariable('CO', '', IntToStr(p.var_args[14]), '', '');
    mExp.AddVariable('CP', '', IntToStr(p.var_args[15]), '', '');

    xdoc.Active := False;
    xdoc.xml.Text := xml;
    xdoc.Active := True;
    root := xdoc.ChildNodes[1];         //Graph
    node := root.ChildNodes.FindNode('PlaneXY'); //PlaneXY
    if node <> nil then
    begin
      mExp.AddVariable('L', '', IntToStr(p.gl), '', '');
      mExp.AddVariable('W', '', IntToStr(p.gp), '', '');
      attri := node.AttributeNodes.FindNode('Type');
      if attri.Text = 'Polygon' then
      begin
        AddList;
        if mTempList.Count >= 4 then
        begin
          GetMinAndMax;
          GetMinAndMax_FromY(p.bg_l_minx, p.bg_l_maxx, p.bg_r_minx, p.bg_r_maxx);
          GetMinAndMax_FromX(p.bg_b_minx, p.bg_b_maxx, p.bg_f_minx, p.bg_f_maxx);
        end;
      end;
    end;
    node := root.ChildNodes.FindNode('PlaneXZ'); //PlaneXZ
    if node <> nil then
    begin
      mExp.AddVariable('L', '', IntToStr(p.gl), '', '');
      mExp.AddVariable('W', '', IntToStr(p.gh), '', '');
      attri := node.AttributeNodes.FindNode('Type');
      if attri.Text = 'Polygon' then
      begin
        AddList;
        if mTempList.Count >= 4 then
        begin
          GetMinAndMax;
          GetMinAndMax_FromY(p.bg_l_miny, p.bg_l_maxy, p.bg_r_miny, p.bg_r_maxy);
          GetMinAndMax_FromX(p.bg_d_minx, p.bg_d_maxx, p.bg_u_minx, p.bg_u_maxx);
        end;
      end;
    end;
    node := root.ChildNodes.FindNode('PlaneYZ'); //PlaneYZ
    if node <> nil then
    begin
      mExp.AddVariable('L', '', IntToStr(p.gp), '', '');
      mExp.AddVariable('W', '', IntToStr(p.gh), '', '');
      attri := node.AttributeNodes.FindNode('Type');
      if attri.Text = 'Polygon' then
      begin
        AddList;
        if mTempList.Count >= 4 then
        begin
          GetMinAndMax;
          GetMinAndMax_FromX(p.bg_d_miny, p.bg_d_maxy, p.bg_u_miny, p.bg_u_maxy);
          GetMinAndMax_FromY(p.bg_b_miny, p.bg_b_maxy, p.bg_f_miny, p.bg_f_maxy);
        end;
      end;
    end;
    xdoc.Active := False;
    xdoc.xml.Text := '';
  except
  end;
end;

procedure TLocalObject.CalcBomWj;
var
  prule             : PBomRuleRec;
  pwjrule           : PWJRuleRec;
  i, j, t, k        : Integer;
  p, p2             : PBomOrderItem;
  list              : TList;
  f                 : Real;
  function MyRound(f: Real): Integer;
  var
    i               : Integer;
  begin
    i := Round(f);
    if (f - i) < 0.0001 then
      Result := i
    else
      Result := i + 1;
  end;
begin
  for i := 0 to bomlist.Count - 1 do
  begin
    p := bomlist[i];
    if (p.bomwjdes <> ',') and (p.bomwjdes <> '') then
    begin
      //计算基础五金
      j := wjruleHash.IndexOf(p.bomwjdes);
      if j <> -1 then
      begin
        list := TList(wjruleHash.Objects[j]);
        for j := 0 to list.Count - 1 do
        begin
          pwjrule := list[j];
          if ((pwjrule.lgflag = 0) or (p.lgflag = pwjrule.lgflag))
            and ((p.bl >= pwjrule.lmin) and ((p.bl <= pwjrule.lmax) or (pwjrule.lmax = 0)))
            and ((p.bp >= pwjrule.pmin) and ((p.bp <= pwjrule.pmax) or (pwjrule.pmax = 0)))
            and ((p.bh >= pwjrule.hmin) and ((p.bh <= pwjrule.hmax) or (pwjrule.hmax = 0))) then
          begin
            NewBomOrderItem(p2);
            p2.classseq := 10000;
            p2.seq := pwjrule.wjid;
            p2.cid := p.cid;
            p2.nodename := '五金';
            p2.name := pwjrule.wjname;
            p2.code := pwjrule.wjno;
            p2.gno := p.gno;
            p2.gcb := p.gcb;
            p2.mark := p.mark;
            p2.extra := p.extra;
            p2.subspace := p.subspace;
            p2.l := 1;
            p2.p := 1;
            p2.h := 1;
            p2.bl := 1;
            p2.bp := 1;
            p2.bh := 1;
            p2.direct := 0;
            p2.desc := pwjrule.wjname;
            p2.myunit := pwjrule.myunit2;
            p2.mat := pwjrule.mat;
            p2.mat := StringReplace(p2.mat, '[P]', p.mat, [rfReplaceAll]);
            p2.color := pwjrule.color;
            p2.color := StringReplace(p2.color, '[P]', p.color, [rfReplaceAll]);
            if pwjrule.myunit = '单件' then
              p2.num := pwjrule.num
            else if pwjrule.myunit = '宽度(每米)' then
            begin
              f := p.bl / 1000;
              t := MyRound(f);
              p2.num := pwjrule.num * t;
            end
            else if pwjrule.myunit = '深度(每米)' then
            begin
              f := p.bp / 1000;
              t := MyRound(f);
              p2.num := pwjrule.num * t;
            end
            else if pwjrule.myunit = '高度(每米)' then
            begin
              f := p.bh / 1000;
              t := MyRound(f);
              p2.num := pwjrule.num * t;
            end
            else if pwjrule.myunit = '面积(每平米)' then
            begin
              f := p.bl * p.bp / 1000 / 1000;
              t := MyRound(f);
              p2.num := pwjrule.num * t;
            end;
            p2.basewj_price := pwjrule.price;
            basewjlist.Add(p2);
          end;
        end;
      end;
    end;

    if (p.bomdes <> ',') and (p.bomdes <> '') then
    begin
      //工艺减量
      j := ruleHash.IndexOf(p.bomdes);
      if j <> -1 then
      begin
        list := TList(ruleHash.Objects[j]);
        for j := 0 to list.Count - 1 do
        begin
          prule := list[j];
          //*表示任意材料
          if ((prule.mat = '*') or (prule.mat = p.mat)) and ((prule.bh = 0) or (prule.bh = Round(p.bh))) then
          begin
            if p.lfb = 0 then p.lfb := prule.lfb;
            if p.llk = 0 then           //非手动设置计算
            begin
              p.llk := prule.llk;
              p.bl := p.bl - p.lfb - p.llk;
            end;
            if p.wfb = 0 then p.wfb := prule.wfb;
            if p.wlk = 0 then           //非手动设置计算
            begin
              p.wlk := prule.wlk;
              p.bp := p.bp - p.wfb - p.wlk;
            end;
            p.holestr := prule.holestr;
            p.kcstr := prule.kcstr;
            p.memo := prule.memo + p.memo;
            for k := 0 to 15 do
            begin
              p.memo := StringReplace(p.memo, Format('[$C%s]', [Chr(65 + k)]), IntToStr(p.var_args[k]), [rfReplaceAll]);
              p.kcstr := StringReplace(p.kcstr, Format('[$C%s]', [Chr(65 + k)]), IntToStr(p.var_args[k]), [rfReplaceAll]);
            end;
            if p.user_fbstr = '' then
            begin
              p.llfb := prule.llfb;
              p.rrfb := prule.rrfb;
              p.ddfb := prule.ddfb;
              p.uufb := prule.uufb;
              p.fb := prule.fb;
            end;
            if p.fbstr = '' then p.fbstr := prule.fbstr;
            p.is_outline := (prule.is_outline = 1);
            break;
          end;
        end;
      end;
    end;
  end;

  //根据产品来计算线性物体
{  for k:=0 to mProductList.Count-1 do
  begin
    //统计线性物体
    for i := 0 to bomlist.Count - 1 do
    begin
      p := bomlist[i];
      if p.cid<>k then continue;
      if not p.isoutput then continue;
      if (p.linecalc<>'') then
      begin
        for j:=i+1 to bomlist.Count-1 do
        begin
          p2 := bomlist[j];
          if p2.cid<>k then continue;
          if not p2.isoutput then continue;
          if (p.linecalc=p2.linecalc) then
          begin
            p2.bl := p2.bl+p.bl;
            p.isoutput := False;
            break;
          end;
        end;
      end;
    end;
  end;
  for i := 0 to bomlist.Count - 1 do
  begin
    p := bomlist[i];
    if not p.isoutput then continue;
    if (p.linecalc<>'') then
    begin
      p.num := Round(p.bl/p.linemax);
      if p.bl>(p.linemax*p.num) then p.num := p.num+1;
      p.l := p.linemax;
      p.bl := p.linemax;
    end;
  end;
  for i := 0 to bomlist.Count - 1 do
  begin
    p := bomlist[i];
    p.seq := seqInfoHash.ValueOf(p.name);
    p.classseq := classseqInfoHash.ValueOf(p.myclass);
  end;   }
{  for i := 0 to basewjlist.Count - 1 do
  begin
    p := basewjlist[i];
    p.seq := seqInfoHash.ValueOf(p.name);
    p.classseq := seqInfoHash.ValueOf(p.myclass);
  end;  }
end;

procedure TLocalObject.CalcLgFlag;
var
  i, j, t           : Integer;
  p, p2             : PBomOrderItem;
begin
  for i := 0 to bomlist.Count - 1 do
  begin
    p := bomlist[i];
    if p.lgflag <> 1 then Continue;
    for j := 0 to bomlist.Count - 1 do
    begin
      if i = j then Continue;
      p2 := bomlist[j];
      if p2.lgflag <> 1 then Continue;
      if p.subspace <> p2.subspace then Continue;

      t := p.z + (p.gh div 2);
      if not ((t > p2.z) and (t < p2.z + p2.gh)) then Continue;
      if ((p.x + p.gl + 9) > p2.x) and ((p.x + p.gl + 9) < (p2.x + p2.gl)) then
      begin
        p.lgflag := 2;
        p2.lgflag := 0;
      end;
    end;
  end;
  for i := 0 to bomlist.Count - 1 do
  begin
    p := bomlist[i];
    if p.lgflag = 1 then p.lgflag := 0;
    if p.lgflag = 2 then p.lgflag := 1;
  end;
end;

procedure TLocalObject.CalcHoleAndKc;
var
  list, calclist    : TList;
  i, j,k              : Integer;
  gno,str1,str2               : string;
  p                 : PBomOrderItem;
  item              : TMyCalcItem;
begin
  list := TList.Create;
  calclist := TList.Create;

  for i := 0 to mHPInfoList.Count - 1 do
  begin
    dispose(mHPInfoList[i]);
  end;
  mHPInfoList.Clear;
  for i := 0 to mKCInfoList.Count - 1 do
  begin
    dispose(mKCInfoList[i]);
  end;
  mKCInfoList.Clear;

  CalcHoleUnit.InitValue;
  for i := 0 to mProductList.Count - 1 do
  begin
    list.Clear;

    //找出订单的物料
    for j := 0 to bomlist.Count - 1 do
    begin
      p := bomlist[j];
      if (p.cid <> i) or (not p.isoutput) then Continue;
      list.Add(p);
    end;

    BomList2CalcList(list, calclist);
    CalcHoleUnit.CalcHoleList(calclist);
    CalcHoleUnit.CalcKCList(calclist);
    CalcList2BomList(calclist, list);
  end;                                  //for i
  list.Clear;
  FreeAndNil(list);

  for i := 0 to calclist.Count - 1 do
  begin
    item:=calclist[i];
    item.Free;
  end;
  calclist.Clear;
  FreeAndNil(calclist);

  //合并开槽
  if mCombineKc =1 then CalcKCCombine;

end;

procedure TLocalObject.CalcKCCombine;
var
  p                 : PBomOrderItem;
  i, j, k           : Integer;
  kcinfo0, kcinfo1  : TKCInfo;
begin
  for i := 0 to bomlist.Count - 1 do
  begin
    p := bomlist[i];
    //A面开槽
    for j := 0 to 100 do
    begin
      if p.akc_index[j] < 0 then break;
      kcinfo0 := mKCInfoList[p.akc_index[j]];
      if kcinfo0.kcid < 0 then Continue;
      for k := 100 downto j + 1 do
      begin
        if p.akc_index[k] < 0 then Continue;
        kcinfo1 := mKCInfoList[p.akc_index[k]];
        if kcinfo1.kcid < 0 then Continue;
        if kcinfo0.flag <> kcinfo1.flag then Continue;
        //X方向在同一水平线上，合并开槽
        if (kcinfo0.x0 = kcinfo0.x1) and (kcinfo1.x0 = kcinfo1.x1) then
        begin
          if abs(kcinfo0.y0 - kcinfo1.y1) < 3 then
          begin
            kcinfo0.y0 := kcinfo1.y0;
            kcinfo1.kcid := -1;
          end;
          if abs(kcinfo0.y1 - kcinfo1.y0) < 3 then
          begin
            kcinfo0.y1 := kcinfo1.y1;
            kcinfo1.kcid := -1;
          end;
        end;
        //Y方向在同一水平线上，合并开槽
        if (kcinfo0.y0 = kcinfo0.y1) and (kcinfo1.y0 = kcinfo1.y1) then
        begin
          if abs(kcinfo0.x0 - kcinfo1.x1) < 3 then
          begin
            kcinfo0.x0 := kcinfo1.x0;
            kcinfo1.kcid := -1;
          end;
          if abs(kcinfo0.x1 - kcinfo1.x0) < 3 then
          begin
            kcinfo0.x1 := kcinfo1.x1;
            kcinfo1.kcid := -1;
          end;
        end;
      end;                              //for k
    end;                                //for j

    //B面开槽
    for j := 0 to 100 do
    begin
      if p.bkc_index[j] < 0 then break;
      kcinfo0 := mKCInfoList[p.bkc_index[j]];
      if kcinfo0.kcid < 0 then Continue;
      for k := 100 downto j + 1 do
      begin
        if p.bkc_index[k] < 0 then Continue;
        kcinfo1 := mKCInfoList[p.bkc_index[k]];
        if kcinfo1.kcid < 0 then Continue;
        if kcinfo0.flag <> kcinfo1.flag then Continue;
        //X方向在同一水平线上，合并开槽
        if (kcinfo0.x0 = kcinfo0.x1) and (kcinfo1.x0 = kcinfo1.x1) then
        begin
          if abs(kcinfo0.y0 - kcinfo1.y1) < 3 then
          begin
            kcinfo0.y0 := kcinfo1.y0;
            kcinfo1.kcid := -1;
          end;
          if abs(kcinfo0.y1 - kcinfo1.y0) < 3 then
          begin
            kcinfo0.y1 := kcinfo1.y1;
            kcinfo1.kcid := -1;
          end;
        end;
        //Y方向在同一水平线上，合并开槽
        if (kcinfo0.y0 = kcinfo0.y1) and (kcinfo1.y0 = kcinfo1.y1) then
        begin
          if abs(kcinfo0.x0 - kcinfo1.x1) < 3 then
          begin
            kcinfo0.x0 := kcinfo1.x0;
            kcinfo1.kcid := -1;
          end;
          if abs(kcinfo0.x1 - kcinfo1.x0) < 3 then
          begin
            kcinfo0.x1 := kcinfo1.x1;
            kcinfo1.kcid := -1;
          end;
        end;
      end;                              //for k
    end;                                //for j

    //清除掉被合并的开槽
    for j := 100 downto 0 do
    begin
      if p.akc_index[j] >= 0 then
      begin
        kcinfo0 := mKCInfoList[p.akc_index[j]];
        if kcinfo0.kcid < 0 then p.akc_index[j] := -1;
      end;
      if p.bkc_index[j] >= 0 then
      begin
        kcinfo0 := mKCInfoList[p.bkc_index[j]];
        if kcinfo0.kcid < 0 then p.bkc_index[j] := -1;
      end;
    end;                                //for j
    for j := 0 to 100 do
    begin
      if p.akc_index[j] >= 0 then Continue;
      for k := j + 1 to 100 do
      begin
        if p.akc_index[k] < 0 then Continue;
        p.akc_index[j] := p.akc_index[k];
        p.akc_index[k] := -1;
      end;
    end;                                //for j
    for j := 0 to 100 do
    begin
      if p.bkc_index[j] >= 0 then Continue;
      for k := j + 1 to 100 do
      begin
        if p.bkc_index[k] < 0 then Continue;
        p.bkc_index[j] := p.bkc_index[k];
        p.bkc_index[k] := -1;
      end;
    end;                                //for j
  end;                                  //for
end;

procedure TLocalObject.InitHoleWjList(jo:ISuperObject);
var
  cfg                 : PHoleWjCfg;
  url, objstr :string;
  i, n, seq :Integer;
  ja, cjo:ISuperObject;

begin
  HoleWjList := TList.Create;
  //showmessage(jo.S['HoleWjFContent']);
  if jo.S['HoleWjFContent'] = '' then exit;
  ja := SO(jo.S['HoleWjFContent']);
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(cfg);
    cfg.c := 0;
    cfg.holetype := 0;
    if (cjo.S['孔位类型']='B') then cfg.holetype := 1;
    if (cjo.S['孔位类型']='I+I') then cfg.holetype := 2;
    cfg.bh := cjo.I['B板厚'];
    cfg.holenum := cjo.I['孔数量'];
    cfg.hole := cjo.S['孔位标识'];
    cfg.color := cjo.S['板材颜色'];
    cfg.wjname := cjo.S['五金名称'];
    cfg.wjmat := cjo.S['五金材料'];
    cfg.wjcolor := cjo.S['五金颜色'];
    cfg.wjcode := cjo.S['五金编号'];
    cfg.wjnum := cjo.I['五金数量'];
    HoleWjList.Add(cfg);
  end;
  //showmessage('HoleWjList='+inttostr(HoleWjList.count));
  ja := nil;
end;

procedure TLocalObject.UninitHoleWjList();
var
  cfg:PHoleWjCfg;
  i: Integer;
begin
  for i:=0 to HoleWjList.Count-1 do
  begin
    cfg := HoleWjList[i];
    cfg.hole := '';
    cfg.color := '';
    cfg.wjname := '';
    cfg.wjmat := '';
    cfg.wjcolor := '';
    cfg.wjcode := '';
    dispose(cfg);
  end;
  HoleWjList.Clear;
  FreeAndNil(HoleWjList);
end;

procedure TLocalObject.CalcHoleWj;
  procedure AddWj(p: PBomOrderItem; r: string; b_bh:Integer=0; isii:Integer=0);
  var
    p2              : PBomOrderItem;
    //phwj            : PHoleWjItem;
    i, n               : Integer;
    cfg:PHoleWjCfg;
  begin
    n := HoleWjList.Count;
    for i:=0 to n-1 do
    begin
      cfg := HoleWjList[i];
      if (isii<>0) and (cfg.holetype=1) then continue;
      if (isii<>1) and (cfg.holetype=2) then continue;
      if ((b_bh=0) or (cfg.bh=0) or (cfg.bh=b_bh)) and
        (cfg.hole = r) and ((cfg.color = '') or (cfg.color = p.color)) then
      begin
        cfg.c := cfg.c+1;
        if (cfg.holenum>0) then
        begin
          if cfg.holenum>cfg.c then continue;
        end;
        cfg.c := 0;
        NewBomOrderItem(p2);
        p2.classseq := 10000;
        p2.seq := i;
        p2.cid := p.cid;
        p2.nodename := '五金';
        p2.name := cfg.wjname;
        p2.gno := p.gno;
        p2.gcb := p.gcb;
        p2.mark := p.mark;
        p2.extra := p.extra;
        p2.subspace := p.subspace;
        p2.l := 1;
        p2.p := 1;
        p2.h := 1;
        p2.bl := 1;
        p2.bp := 1;
        p2.bh := 1;
        p2.direct := 0;
        p2.desc := cfg.wjname;
        p2.mat := cfg.wjmat;
        p2.mat := StringReplace(p2.mat, '[P]', p.mat, [rfReplaceAll]);
        p2.color := cfg.wjcolor;
        p2.color := StringReplace(p2.color, '[P]', p.color, [rfReplaceAll]);
        p2.num := cfg.wjnum;
        p2.basewj_price := 0;
        //p2.basewj_price := phwj.price;
        p2.code := cfg.wjcode;
        basewjlist.Add(p2);
      end;
    end;
  end;
var
  i, j, k, n              : Integer;
  p                 : PBomOrderItem;
  phinfo            : THolePointInfo;
  xml, xml2, url         : string;
  ll, pp, hh, flag  : Integer;
  calcitem          : TMyCalcItem;
  root, nodeA, nodeB, cnode, attri: IXMLNode;
  objstr:string;
  xdoc:IXMLDocument;
  cfg:PHoleWjCfg;
  jo, ja, cjo:ISuperObject;
begin
  //url:=Format(UrlIp+'/HoleWj/?factorypath=%s',[HTTPEncode(UTF8Encode(factoryDataPath))]);      //修改
  //objstr :=fromPygetobj(url);    //修改
  //if objstr ='' then
  //begin
  //  ShowBomMessage('缺少孔位五金配置表');
  //  exit;
  //end;
  //objstr := MyUtils.ReadStringFromFile(MyUtils.GetQuickDrawPath+'data\QDData\孔位五金.cfg');
  //jo := TSuperObject.Create();
  //jo := SO(objstr);
  //showmessage('holewujin='+inttostr(HoleWjList.count));
  calcitem := TMyCalcItem.Create;
  for i := 0 to bomlist.Count - 1 do
  begin
    p := bomlist[i];
    if not p.isoutput then Continue;
    for j := 0 to 100 do
    begin
      if p.ahole_index[j] >= 0 then
      begin
        phinfo := mHPInfoList[p.ahole_index[j]];
        AddWj(p, phinfo.r, phinfo.b_bh, phinfo.isii);
      end else break;
    end;                                //for j
    for j := 0 to 100 do
    begin
      if p.bhole_index[j] >= 0 then
      begin
        phinfo := mHPInfoList[p.bhole_index[j]];
        if phinfo.isii=0 then AddWj(p, phinfo.r, phinfo.b_bh, phinfo.isii);
      end else break;
    end;                                //for j
    //自定义孔位
    flag := 0;
    if (p.bdxmlid <> '') and (mBDXMLList.ValueOf(p.bdxmlid) <> '') then flag := 1;
    if (p.bg_filename <> '') and (fileexists(p.bg_filename)) then flag := 2;
    if flag in [1, 2] then              //自定义板件
    begin
      if flag = 1 then
      begin
        xml := mBDXMLList.ValueOf(p.bdxmlid);
        xml2 := CalcHoleUnit.SaveBD(BomItem2CalcItem(p, calcitem), ll, pp, hh, False);
        BDXML_BDXML(xml, xml2);
        xml := '<?xml version="1.0" encoding="gb2312"?>' + xml;
      end;                              //
      if flag = 2 then
      begin
        xml := ReadStringFromFile(p.bg_filename);
      end;                              //
      try
        xdoc := XMLDoc.LoadXMLData(xml);
        root := xdoc.ChildNodes[1];     //bdxml
        nodeA := root.ChildNodes.FindNode('FaceA');
        nodeB := root.ChildNodes.FindNode('FaceB');
        for j := nodeA.ChildNodes.Count - 1 downto 0 do
        begin
          cnode := nodeA.ChildNodes[j];
          if (cnode.nodename = 'BHole') then
          begin
            attri := cnode.AttributeNodes.FindNode('R');
            if attri <> nil then
            begin
              AddWj(p, attri.Text, Round(p.bh), 0);
              n := GetAttributeValue(cnode, 'Holenum_X', 0, 0);
              for k:=1 to n-1 do
              begin
                AddWj(p, attri.Text, Round(p.bh), 0);
              end; //for k
              n := GetAttributeValue(cnode, 'Holenum_Y', 0, 0);
              for k:=1 to n-1 do
              begin
                AddWj(p, attri.Text, Round(p.bh), 0);
              end;  //for k
            end; //if
          end; //if
        end; //for j
        for j := nodeB.ChildNodes.Count - 1 downto 0 do
        begin
          cnode := nodeB.ChildNodes[j];
          if (cnode.nodename = 'BHole') then
          begin
            attri := cnode.AttributeNodes.FindNode('R');
            if attri <> nil then
            begin
              AddWj(p, attri.Text, Round(p.bh), 0);
              n := GetAttributeValue(cnode, 'Holenum_X', 0, 0);
              for k:=1 to n-1 do
              begin
                AddWj(p, attri.Text, Round(p.bh), 0);
              end;  //for k
              n := GetAttributeValue(cnode, 'Holenum_Y', 0, 0);
              for k:=1 to n-1 do
              begin
                AddWj(p, attri.Text, Round(p.bh), 0);
              end;   //for k
            end;  //if
          end;   //if
        end;   //for j
      finally
        xdoc := nil;
      end;                              //try
    end;                                //if flag in [1,2] then
  end;                                  //for i

  FreeAndNil(calcitem);
end;

procedure TLocalObject.CalcLineCombine;
var
  i, j, t, k        : Integer;
  p, p2             : PBomOrderItem;
begin
  //根据产品来计算线性物体
  for k := 0 to mProductList.Count - 1 do
  begin
    //统计线性物体
    for i := 0 to bomlist.Count - 1 do
    begin
      p := bomlist[i];
      if p.cid <> k then Continue;
      if not p.isoutput then Continue;
      if (p.linecalc <> '') then
      begin
        for j := i + 1 to bomlist.Count - 1 do
        begin
          p2 := bomlist[j];
          if p2.cid <> k then Continue;
          if not p2.isoutput then Continue;
          if (p.linecalc = p2.linecalc) then
          begin
            p2.bl := p2.bl + p.bl;
            p.isoutput := False;
            break;
          end;
        end;
      end;
    end;
  end;
  for i := 0 to bomlist.Count - 1 do
  begin
    p := bomlist[i];
    if not p.isoutput then Continue;
    if (p.linecalc <> '') then
    begin
      if p.linemax = 99999 then
      begin
        p.num := 1;
        p.l := Round(p.bl);
      end
      else
      begin
        p.num := Round(p.bl / p.linemax);
        if p.bl > (p.linemax * p.num) then p.num := p.num + 1;
        p.l := p.linemax;
        p.bl := p.linemax;
      end;
    end;
  end;
end;

procedure TLocalObject.CalcSeq;
var
  i                 : Integer;
  p                 : PBomOrderItem;
begin
  for i := 0 to bomlist.Count - 1 do
  begin
    p := bomlist[i];
    p.seq := seqInfoHash.ValueOf(p.name);
    p.classseq := classseqInfoHash.ValueOf(p.myclass);
  end;
  {  for i := 0 to basewjlist.Count - 1 do
    begin
      p := basewjlist[i];
      p.seq := seqInfoHash.ValueOf(p.name);
      p.classseq := seqInfoHash.ValueOf(p.myclass);
    end;  }
end;

function TLocalObject.ToBGInfoX2D(p: PBomOrderItem): string;
type
  Line = record
    x0, y0, x1, y1, r: double;
  end;
var
  root, node, cnode, cnode0, attri: IXMLNode;
  l, w, ll, pp, hh  : Integer;
  i, j, angle       : Integer;
  sx, sy            : string;
  xml               : string;
  r                 : Integer;
  x0, y0, x1, y1, t1, t2, xx0, yy0, xx1, yy1: double;
  di                : Integer;
  pline, pline0     : ^Line;
  list              : TList;
  phinfo            : THolePointInfo;
begin
  Result := '';
  l := p.l;
  w := p.p;
  xml := gBGHash.ValueOf(bgname(p.bg));
  if xml = '' then exit;

  list := TList.Create;
  try
    xdoc.Active := False;
    xdoc.xml.Text := xml;
    xdoc.Active := True;
    root := xdoc.ChildNodes[1];         //Graph
    node := root.ChildNodes.FindNode('PlaneXY'); //PlaneXY
    if node <> nil then
    begin
      attri := node.AttributeNodes.FindNode('Type');
      if attri.Text <> 'Polygon' then node := nil;
    end;
    if node = nil then
    begin
      node := root.ChildNodes.FindNode('PlaneXZ'); //PlaneXZ
      if node <> nil then
      begin
        attri := node.AttributeNodes.FindNode('Type');
        if attri.Text <> 'Polygon' then node := nil;
      end;
    end;
    if node = nil then
    begin
      node := root.ChildNodes.FindNode('PlaneYZ'); //PlaneYZ
      if node <> nil then
      begin
        attri := node.AttributeNodes.FindNode('Type');
        if attri.Text <> 'Polygon' then node := nil;
      end;
    end;
    if node <> nil then
    begin
      attri := node.AttributeNodes.FindNode('X');
      if attri <> nil then sx := attri.Text;
      attri := node.AttributeNodes.FindNode('Y');
      if attri <> nil then sy := attri.Text;
      x0 := 0;
      y0 := 0;
      di := 1;                          //横纹
      if (p.direct = 3) or (p.direct = 4) or (p.direct = 5) then di := 0; //竖纹
      GraphSizeToBomSize(Round(p.l), Round(p.p), Round(p.h), p.direct, ll, pp, hh);
      if node.nodename = 'PlaneXY' then
      begin
        l := ll;
        w := pp;
        if di = 1 then
        begin
          l := p.gl;
          w := p.gp;
        end;
      end;
      if node.nodename = 'PlaneXZ' then
      begin
        l := ll;
        w := hh;
        if di = 1 then
        begin
          l := p.gl;
          w := p.gh;
        end;
      end;
      if node.nodename = 'PlaneYZ' then
      begin
        l := pp;
        w := hh;
        if di = 1 then
        begin
          l := p.gp;
          w := p.gh;
        end;
      end;
      mExp.AddVariable('L', '', IntToStr(l), '', '');
      mExp.AddVariable('W', '', IntToStr(w), '', '');
      mExp.AddVariable('CA', '', IntToStr(p.var_args[0]), '', '');
      mExp.AddVariable('CB', '', IntToStr(p.var_args[1]), '', '');
      mExp.AddVariable('CC', '', IntToStr(p.var_args[2]), '', '');
      mExp.AddVariable('CD', '', IntToStr(p.var_args[3]), '', '');
      mExp.AddVariable('CE', '', IntToStr(p.var_args[4]), '', '');
      mExp.AddVariable('CF', '', IntToStr(p.var_args[5]), '', '');
      mExp.AddVariable('CG', '', IntToStr(p.var_args[6]), '', '');
      mExp.AddVariable('CH', '', IntToStr(p.var_args[7]), '', '');

      mExp.AddVariable('CI', '', IntToStr(p.var_args[8]), '', '');
      mExp.AddVariable('CJ', '', IntToStr(p.var_args[9]), '', '');
      mExp.AddVariable('CK', '', IntToStr(p.var_args[10]), '', '');
      mExp.AddVariable('CL', '', IntToStr(p.var_args[11]), '', '');
      mExp.AddVariable('CM', '', IntToStr(p.var_args[12]), '', '');
      mExp.AddVariable('CN', '', IntToStr(p.var_args[13]), '', '');
      mExp.AddVariable('CO', '', IntToStr(p.var_args[14]), '', '');
      mExp.AddVariable('CP', '', IntToStr(p.var_args[15]), '', '');

      for i := 1 to node.ChildNodes.Count do
      begin
        cnode0 := node.ChildNodes[i - 1];
        attri := cnode0.AttributeNodes.FindNode('X');
        sx := attri.Text;
        mExp.SetSubject(sx);
        x0 := mExp.ToValueFloat;

        attri := cnode0.AttributeNodes.FindNode('Y');
        sy := attri.Text;
        mExp.SetSubject(sy);
        y0 := mExp.ToValueFloat;

        if i = node.ChildNodes.Count then
          cnode := node.ChildNodes[0]
        else
          cnode := node.ChildNodes[i];
        attri := cnode.AttributeNodes.FindNode('X');
        sx := attri.Text;
        mExp.SetSubject(sx);
        x1 := mExp.ToValueFloat;

        attri := cnode.AttributeNodes.FindNode('Y');
        sy := attri.Text;
        mExp.SetSubject(sy);
        y1 := mExp.ToValueFloat;

        xx0 := 0;
        yy0 := 0;
        xx1 := 0;
        yy1 := 0;
        attri := cnode0.AttributeNodes.FindNode('XA');
        if (attri <> nil) and (attri.Text <> '') then xx0 := StrToFloat(attri.Text);
        attri := cnode0.AttributeNodes.FindNode('YA');
        if (attri <> nil) and (attri.Text <> '') then yy0 := StrToFloat(attri.Text);
        attri := cnode.AttributeNodes.FindNode('XA');
        if (attri <> nil) and (attri.Text <> '') then xx1 := StrToFloat(attri.Text);
        attri := cnode.AttributeNodes.FindNode('YA');
        if (attri <> nil) and (attri.Text <> '') then yy1 := StrToFloat(attri.Text);

        if di = 1 then
        begin
          t1 := x0;
          t2 := y0;
          x0 := p.p - t2;
          y0 := t1;

          t1 := x1;
          t2 := y1;
          x1 := p.p - t2;
          y1 := t1;
          Swap(xx0, yy0);
          Swap(xx1, yy1);
        end;

        if (cnode0.nodename = 'Point') then
        begin
          if not ((x0 = x1) and (y0 = y1)) then
          begin
            new(pline);
            pline.x0 := x0 + xx0;
            pline.y0 := y0 + yy0;
            if list.Count > 0 then
            begin
              pline0 := list[list.Count - 1];
              pline.x0 := pline0.x1;
              pline.y0 := pline0.y1;
            end;
            pline.x1 := x1 + xx1;
            pline.y1 := y1 + yy1;
            pline.r := 0;
            list.Add(pline);
          end;
        end;
        if cnode0.nodename = 'Arc' then
        begin
          angle := 0;
          attri := cnode0.AttributeNodes.FindNode('Angle');
          if (attri <> nil) then
          begin
            angle := StrToInt(attri.Text);
            if angle >= 0 then
              angle := -1
            else
              angle := 1;
          end;
          mExp.SetSubject(attri.Text);
          attri := cnode0.AttributeNodes.FindNode('R');
          mExp.SetSubject(attri.Text);
          r := angle * mExp.ToValueInt;
          if not ((x0 = x1) and (y0 = y1)) then
          begin
            new(pline);
            pline.x0 := x0 + xx0;
            pline.y0 := y0 + yy0;
            if list.Count > 0 then
            begin
              pline0 := list[list.Count - 1];
              pline.x0 := pline0.x1;
              pline.y0 := pline0.y1;
            end;
            pline.x1 := x1 + xx1;
            pline.y1 := y1 + yy1;
            pline.r := r;
            list.Add(pline);
          end;
        end;
      end;
    end;

    xdoc.Active := False;
    xdoc.xml.Text := '';
  except
  end;
  p.a_hole_info := '';
  p.b_hole_info := '';
  //AB面数据输出
  for i := 0 to 100 do
  begin
    if p.ahole_index[i] >= 0 then
    begin
      phinfo := mHPInfoList[p.ahole_index[i]];
      if di = 1 then
        p.a_hole_info := p.a_hole_info + Format('(%d,%d,%s,%d),', [p.p - phinfo.y, phinfo.x, phinfo.r, phinfo.offset])
      else
        p.a_hole_info := p.a_hole_info + Format('(%d,%d,%s,%d),', [phinfo.x, phinfo.y, phinfo.r, phinfo.offset]);
    end;
    if p.bhole_index[i] >= 0 then
    begin
      phinfo := mHPInfoList[p.bhole_index[i]];
      if di = 1 then
        p.b_hole_info := p.b_hole_info + Format('(%d,%d,%s,%d),', [p.p - phinfo.y, phinfo.x, phinfo.r, phinfo.offset])
      else
        p.b_hole_info := p.b_hole_info + Format('(%d,%d,%s,%d),', [phinfo.x, phinfo.y, phinfo.r, phinfo.offset]);
    end;
  end;
  if (p.is_outline) or (p.is_output_bgdata = 1) then
  begin
    for i := 0 to list.Count - 1 do
    begin
      pline := list[i];
      Result := Result + Format('(%.1f,%.1f,%.1f,%.1f,%.1f),', [pline.x0, pline.y0, pline.x1, pline.y1, pline.r]);
      dispose(list[i]);
    end;
  end;
  list.Clear;
end;

function TLocalObject.ToBGInfo(p: PBomOrderItem): string;
var
  str, bg           : string;
begin
  Result := '';
  bg := p.bg;
  if p.bg <> 'BG::RECT' then
    p.bg := StringReplace(p.bg, '::', '_', [rfReplaceAll]);

  if p.bg <> 'BG::RECT' then
  begin
    str := ToBGInfoX2D(p);
  end;
  p.bg := bg;
  Result := str;
end;

procedure TLocalObject.TransAB(p: PBomOrderItem);
var
  str               : string;
  i, t              : Integer;
  phinfo            : THolePointInfo;
begin
  p.trans_ab := False;
  str := p.a_hole_info;
  p.a_hole_info := p.b_hole_info;
  p.b_hole_info := str;

  for i := 0 to 100 do
  begin
    t := p.ahole_index[i];
    p.ahole_index[i] := p.bhole_index[i];
    p.bhole_index[i] := t;

    if p.ahole_index[i] >= 0 then
    begin
      phinfo := mHPInfoList[p.ahole_index[i]];
      phinfo.x := p.gl - phinfo.x;
    end;
    if p.bhole_index[i] >= 0 then
    begin
      phinfo := mHPInfoList[p.bhole_index[i]];
      phinfo.x := p.gl - phinfo.x;
    end;

    t := p.akc_index[i];
    p.akc_index[i] := p.bkc_index[i];
    p.bkc_index[i] := t;
  end;
end;

function TLocalObject.LoadChildBom(ppoi: PBomOrderItem; cid, boardheight: Integer; str: string; list: TList; pid, l, p,
  h: Integer; mat, color, memo, gno, gdes, gcb, myclass, bomstd: string; num: Integer): Integer;
var
  clist             : TList;
  pcbomrule         : PBom2RuleRec;
  i, j, k, id, il, ip, ih: Integer;
  sl, sp, sh        : string;
  p2                : PBomOrderItem;
  exp               : TExpress;
begin
  Result := 0;
  if str = '' then exit;
  i := childbomHash.IndexOf(str);
  if i = -1 then exit;
  clist := TList(childbomHash.Objects[i]);
  id := pid * 100;
  exp := TExpress.Create;
  exp.AddVariable('L', '', IntToStr(l), '', '');
  exp.AddVariable('P', '', IntToStr(p), '', '');
  exp.AddVariable('H', '', IntToStr(h), '', '');
  exp.AddVariable('BH', '', IntToStr(boardheight), '', '');
  exp.mBHValue := boardheight;

  for i := 0 to clist.Count - 1 do
  begin
    pcbomrule := clist[i];
    Result := Result + 1;               //2014-02-15
    if not ((pcbomrule.lmin <= l) and (pcbomrule.lmax >= l) and (pcbomrule.dmin <= p) and (pcbomrule.dmax >= p)
      and (pcbomrule.hmin <= h) and (pcbomrule.hmax >= h)) then Continue;
    //    if mat <> '' then
    //      if ((pcbomrule.mat <> '') and ((pcbomrule.mat <> mat) and (pcbomrule.mat <> '*'))) then Continue;
    sl := pcbomrule.l;
    sp := pcbomrule.p;
    sh := pcbomrule.h;
    exp.SetSubject(sl);
    il := exp.ToValueInt;
    exp.SetSubject(sp);
    ip := exp.ToValueInt;
    exp.SetSubject(sh);
    ih := exp.ToValueInt;
    for j := 0 to pcbomrule.q - 1 do
    begin
      NewBomOrderItem(p2);
      for k := 0 to 15 do
      begin
        p2.var_names[k] := ppoi.var_names[k];
        p2.var_args[k] := ppoi.var_args[k];
      end;
      p2.cid := cid;
      p2.nodename := pcbomrule.bomtype;
      p2.direct := 0;
      p2.code := pcbomrule.ono;
      p2.holestr := pcbomrule.holestr;
      p2.kcstr := pcbomrule.kcstr;
      p2.memo := '';
      p2.num := 1 * num;
      p2.isoutput := True;
      p2.myclass := myclass;
      p2.bomtype := pcbomrule.bomtype;
      p2.id := id;
      p2.pid := pid;
      p2.name := pcbomrule.name;
      p2.x := 0;
      p2.y := 0;
      p2.z := 0;
      p2.gl := il;
      p2.gp := ip;
      p2.gh := ih;
      p2.l := il;
      p2.p := ip;
      p2.h := ih;
      p2.ox := 0;
      p2.oy := 0;
      p2.oz := 0;
      p2.parent := nil;
      if pcbomrule.color <> '' then
        p2.color := pcbomrule.color
      else
        p2.color := color;
      p2.childnum := 0;
      p2.mat := mat;
      if pcbomrule.mat <> '*' then p2.mat := pcbomrule.mat;
      p2.lfb := pcbomrule.lfb;
      p2.llk := pcbomrule.llk;
      p2.wfb := pcbomrule.wfb;
      p2.wlk := pcbomrule.wlk;
      p2.bl := il - p2.lfb - p2.llk;
      p2.bp := ip - p2.wfb - p2.wlk;
      p2.bh := ih;
      p2.direct := 0;
      p2.memo := pcbomrule.memo;
      p2.memo := StringReplace(p2.memo, '[P]', memo, [rfReplaceAll]);
      for k := 0 to 15 do
      begin
        p2.memo := StringReplace(p2.memo, Format('[$C%s]', [Chr(65 + k)]), IntToStr(p2.var_args[k]), [rfReplaceAll]);
        p2.kcstr := StringReplace(p2.kcstr, Format('[$C%s]', [Chr(65 + k)]), IntToStr(p2.var_args[k]), [rfReplaceAll]);
      end;
      p2.fbstr := pcbomrule.fbstr;
      p2.desc := pcbomrule.name;
      p2.gdes := gdes;
      p2.gno := gno;
      p2.gcb := gcb;
      p2.extra := ppoi.extra;
      p2.a_hole_info := pcbomrule.a_face;
      p2.b_hole_info := pcbomrule.b_face;
      p2.holeid := -1;
      p2.kcid := -1;
      p2.bomstd := pcbomrule.bomstd;
      if bomstd <> '' then p2.bomstd := bomstd; //继承父模块的判定规则
      p2.holetype := 1;
      p2.bg_filename := pcbomrule.bg_filename;
      p2.mpr_filename := pcbomrule.mpr_filename;
      p2.bpp_filename := pcbomrule.bpp_filename;
      if p2.bg_filename <> '' then
        p2.is_output_bgdata := 1
      else
        p2.is_output_bgdata := 0;
      if p2.mpr_filename <> '' then
        p2.is_output_mpr := 1
      else
        p2.is_output_mpr := 0;
      if p2.bpp_filename <> '' then
        p2.is_output_bpp := 1
      else
        p2.is_output_bpp := 0;
      p2.direct_calctype := 1;
      if pcbomrule.direct_calctype = 1 then p2.direct_calctype := 2;
      p2.youge_holecalc := 0;
      p2.workflow := pcbomrule.workflow;

      p2.llfb := pcbomrule.llfb;
      p2.rrfb := pcbomrule.rrfb;
      p2.ddfb := pcbomrule.ddfb;
      p2.uufb := pcbomrule.uufb;
      p2.fb := pcbomrule.fb;

      p2.extend := ppoi.extend;
      p2.group := ppoi.group;
      p2.blockmemo := ppoi.blockmemo;
      p2.devcode := pcbomrule.devcode;
      p2.number_text := ppoi.number_text;
      //result := result + 1;    //2014-02-15
      list.Add(p2);
      inc(id);
    end;
  end;
  FreeAndNil(exp);
end;

procedure TLocalObject.GetBomUserDefine(p: PBomOrderItem);
var
  wstr, s1, s2      : WideString;
  N1, n2            : Integer;
begin
  if p.userdefine = '' then exit;
  wstr := p.userdefine;
  N1 := Pos(';', wstr);
  while N1 > 0 do
  begin
    s1 := LeftStr(wstr, N1 - 1);
    n2 := Pos(':', s1);
    if n2 > 0 then
    begin
      s2 := RightStr(s1, Length(s1) - n2);
      s1 := LeftStr(s1, n2 - 1);
      if s1 = 'Na' then p.name := s2;
      if s1 = 'Cl' then p.color := s2;
      if s1 = 'Mt' then p.mat := s2;
      //if s1='Fb' then p.fbstr := s2;
    end;
    wstr := RightStr(wstr, Length(wstr) - N1);
    N1 := Pos(';', wstr);
  end;
end;

procedure TLocalObject.GetQuoUserDefine(p: PBomRecord);
var
  wstr, s1, s2      : WideString;
  N1, n2            : Integer;
begin
  if p.userdefine = '' then exit;
  wstr := p.userdefine;
  N1 := Pos(';', wstr);
  while N1 > 0 do
  begin
    s1 := LeftStr(wstr, N1 - 1);
    n2 := Pos(':', s1);
    if n2 > 0 then
    begin
      s2 := RightStr(s1, Length(s1) - n2);
      s1 := LeftStr(s1, n2 - 1);
      if s1 = 'Na' then p.outputname := s2;
      if s1 = 'Cl' then p.texture := s2;
      if s1 = 'Mt' then p.mat := s2;
    end;
    wstr := RightStr(wstr, Length(wstr) - N1);
    N1 := Pos(';', wstr);
  end;
end;

procedure TLocalObject.GetMatAlias(mat, color: string; bh: Integer; var alias, alias2, alias3:string);
var
  i                 : Integer;
  p                 : PBoardMat;
begin
  alias := mat;
  alias2 := '';
  alias3 := '';
  for i := 0 to gBoardMatList.Count - 1 do
  begin
    p := gBoardMatList[i];
    if p.color='' then continue;
    if (p.name = mat) and (p.color=color) and ((p.bh=0) or (p.bh = bh)) then
    begin
      alias := p.alias;
      alias2 := p.alias2;
      alias3 := p.alias3;
      exit;
    end;
  end;
  for i := 0 to gBoardMatList.Count - 1 do
  begin
    p := gBoardMatList[i];
    if p.color<>'' then continue;
    if (p.name = mat) and ((p.bh=0) or (p.bh = bh)) then
    begin
      alias := p.alias;
      alias2 := p.alias2;
      alias3 := p.alias3;
      exit;
    end;
  end;
end;

procedure TLocalObject.BomList2CalcList(bomlist, calclist: TList; is_new_calcitem: boolean = True);
var
  i                 : Integer;
  item              : TMyCalcItem;
begin
  if is_new_calcitem then               //自动清除calclist
  begin
    for i := 0 to calclist.Count - 1 do
    begin
      item := calclist[i];
      item.Free;
    end;
    calclist.Clear;
  end;

  for i := 0 to bomlist.Count - 1 do
  begin
    if is_new_calcitem then             //自动新增calclist
    begin
      item := TMyCalcItem.Create;
      calclist.Add(item);
    end;
    BomItem2CalcItem(bomlist[i], calclist[i]);

  end;
end;

procedure TLocalObject.CalcList2BomList(calclist, bomlist: TList; is_dispose_calcitem: boolean = True);
var
  i                 : Integer;
  item              : TMyCalcItem;
begin
  for i := 0 to bomlist.Count - 1 do
  begin
    CalcItem2BomItem(calclist[i], bomlist[i]);
  end;

  if is_dispose_calcitem then           //自动清除calclist
  begin
    for i := 0 to calclist.Count - 1 do
    begin
      item:=calclist[i];
      item.Free;
    end;
    calclist.Clear;
  end;
end;

function TLocalObject.CalcItem2BomItem(p, p2: Pointer): PBomOrderItem;
var
  Item2             : PBomOrderItem;
  item              : TMyCalcItem;
  i                 : Integer;
begin
  item := p;
  Item2 := p2;
  Result := Item2;

  Item2.bl := item.bl;
  Item2.bp := item.bp;
  Item2.bh := item.bh;

  Item2.pl := item.pl;
  Item2.pd := item.pd;
  Item2.ph := item.ph;

  Item2.lx := item.lx;
  Item2.ly := item.ly;
  Item2.lz := item.lz;
  Item2.x := item.x;
  Item2.y := item.y;
  Item2.z := item.z;

  Item2.l := item.l;
  Item2.p := item.p;
  Item2.h := item.h;
  Item2.gl := item.gl;
  Item2.gp := item.gp;
  Item2.gh := item.gh;

  //item2.direct := item.direct;
  Item2.holeid := item.holeid;
  Item2.kcid := item.kcid;

  for i := 0 to 100 do
  begin
    if i <= 15 then Item2.var_args[i] := item.var_args[i];

    Item2.ahole_index[i] := item.ahole_index[i];
    Item2.bhole_index[i] := item.bhole_index[i];

    Item2.akc_index[i] := item.akc_index[i];
    Item2.bkc_index[i] := item.bkc_index[i];

    if i <= 5 then Item2.is_calc_holeconfig[i] := item.is_calc_holeconfig[i];
  end;

  //基础图形描述
{  item2.bg_l_minx := item.bg_l_minx;
  item2.bg_l_maxx := item.bg_l_maxx;
  item2.bg_r_minx := item.bg_r_minx;
  item2.bg_r_maxx := item.bg_r_maxx;
  item2.bg_l_miny := item.bg_l_miny;
  item2.bg_l_maxy := item.bg_l_maxy;
  item2.bg_r_miny := item.bg_r_miny;
  item2.bg_r_maxy := item.bg_r_maxy;
  item2.bg_d_minx := item.bg_d_minx;
  item2.bg_d_maxx := item.bg_d_maxx;
  item2.bg_u_minx := item.bg_u_minx;
  item2.bg_u_maxx := item.bg_u_maxx;
  item2.bg_d_miny := item.bg_d_miny;
  item2.bg_d_maxy := item.bg_d_maxy;
  item2.bg_u_miny := item.bg_u_miny;
  item2.bg_u_maxy := item.bg_u_maxy;
  item2.bg_b_minx := item.bg_b_minx;
  item2.bg_b_maxx := item.bg_b_maxx;
  item2.bg_f_minx := item.bg_f_minx;
  item2.bg_f_maxx := item.bg_f_maxx;
  item2.bg_b_miny := item.bg_b_miny;
  item2.bg_b_maxy := item.bg_b_maxy;
  item2.bg_f_miny := item.bg_f_miny;
  item2.bg_f_maxy := item.bg_f_maxy; }

  Item2.hole_back_cap := item.hole_back_cap;
  Item2.hole_2_dist := item.hole_2_dist;

  //  item2.zero_y := item.zero_y;

  //  item2.bg := item.bg;
  Item2.holeconfig_flag := item.holeconfig_flag;
  Item2.kcconig_flag := item.kcconig_flag;
end;

procedure GetWorldMatrix(p:PBomOrderItem; var m:TMatrix);
  function GetLocalMatrix:TMatrix;
  var
    m, rm, tm:TMatrix;
    oz:double;
  begin
    rm := IdentityHmgMatrix;
    tm := CreateTranslationMatrix(VectorMake(p.lx, p.ly, p.lz));
    oz := 0;
    oz := p.oz;
    if abs(oz)>0.001 then
    begin
      oz := -oz*PI/180;
      rm := CreateRotationMatrixZ(oz);
    end;
    if p.vp=1 then //俯视
    begin
      m := CreateRotationMatrixX(DegToRad(90));
      rm := MatrixMultiply(rm, m);
      m := CreateTranslationMatrix(VectorMake(0, p.gh, 0));
      tm := MatrixMultiply(tm, m);
    end;
    if p.vp=2 then //左侧(B面)
    begin
      m := CreateRotationMatrixZ(DegToRad(-90));
      rm := MatrixMultiply(rm, m);
      m := CreateTranslationMatrix(VectorMake(0, p.gl, 0));
      tm := MatrixMultiply(tm, m);
    end;
    if p.vp=3 then //右侧(C面)
    begin
      m := CreateRotationMatrixZ(DegToRad(90));
      rm := MatrixMultiply(rm, m);
      m := CreateTranslationMatrix(VectorMake(p.gl, 0, 0));
      tm := MatrixMultiply(tm, m);
    end;
    if p.vp=4 then //仰视
    begin
      m := CreateRotationMatrixX(DegToRad(-90));
      rm := MatrixMultiply(rm, m);
      m := CreateTranslationMatrix(VectorMake(0, 0, p.gh));
      tm := MatrixMultiply(tm, m);
    end;
    if p.vp=5 then //反向
    begin
      m := CreateRotationMatrixZ(DegToRad(180));
      rm := MatrixMultiply(rm, m);
      m := CreateTranslationMatrix(VectorMake(p.gl, p.gp, 0));
      tm := MatrixMultiply(tm, m);
    end;
    Result := MatrixMultiply(rm, tm);
  end;
var pm:TMatrix;
begin
  m := GetLocalMatrix;

  if p.parent=nil then exit;
  GetWorldMatrix(p.parent, pm);
  m := MatrixMultiply(m, pm);
end;

function TLocalObject.BomItem2CalcItem(p:Pointer; item2:TMyCalcItem):TMyCalcItem;
var
  item              : PBomOrderItem;
  i, j, n, flag     : Integer;
  bdxml, str        : string;
  root, node, cnode, attri: IXMLNode;
begin
  item := p;

  Result := Item2;

  GetWorldMatrix(item, item2.m);
  Item2.space := '';
  Item2.space_x := 0;
  Item2.space_y := 0;
  Item2.space_z := 0;
  GetXptlist(item, Item2.isxx, Item2.xptlist_jx, Item2.xptlist_pl);
  if item.tmp_soz = '' then
    Item2.sozflag := ''
  else
    Item2.sozflag := MD5.StrToMD5(item.tmp_soz);
  GetSpaceItem(item, Item2.space, Item2.space_x, Item2.space_y, Item2.space_z);

  Item2.bl := item.bl;
  Item2.bp := item.bp;
  Item2.bh := item.bh;

  Item2.pl := item.pl;
  Item2.pd := item.pd;
  Item2.ph := item.ph;

  Item2.lx := item.lx;
  Item2.ly := item.ly;
  Item2.lz := item.lz;
  Item2.x := item.x - Item2.space_x;
  Item2.y := item.y - Item2.space_y;
  Item2.z := item.z - Item2.space_z;
  Item2.space_id := item.space_id;

  Item2.l := item.l;
  Item2.p := item.p;
  Item2.h := item.h;
  Item2.gl := item.gl;
  Item2.gp := item.gp;
  Item2.gh := item.gh;

  Item2.direct := item.direct;
  Item2.o_direct := item.direct;
  Item2.holeid := item.holeid;
  Item2.kcid := item.kcid;

  for i := 0 to 100 do
  begin
    if i <= 15 then Item2.var_args[i] := item.var_args[i];

    Item2.ahole_index[i] := item.ahole_index[i];
    Item2.bhole_index[i] := item.bhole_index[i];

    Item2.akc_index[i] := item.akc_index[i];
    Item2.bkc_index[i] := item.bkc_index[i];

    if i <= 5 then Item2.is_calc_holeconfig[i] := item.is_calc_holeconfig[i];
    if i <= 5 then Item2.is_holeface_touch[i] := 0;
  end;

  //基础图形描述
  Item2.bg_l_minx := item.bg_l_minx;
  Item2.bg_l_maxx := item.bg_l_maxx;
  Item2.bg_r_minx := item.bg_r_minx;
  Item2.bg_r_maxx := item.bg_r_maxx;
  Item2.bg_l_miny := item.bg_l_miny;
  Item2.bg_l_maxy := item.bg_l_maxy;
  Item2.bg_r_miny := item.bg_r_miny;
  Item2.bg_r_maxy := item.bg_r_maxy;
  Item2.bg_d_minx := item.bg_d_minx;
  Item2.bg_d_maxx := item.bg_d_maxx;
  Item2.bg_u_minx := item.bg_u_minx;
  Item2.bg_u_maxx := item.bg_u_maxx;
  Item2.bg_d_miny := item.bg_d_miny;
  Item2.bg_d_maxy := item.bg_d_maxy;
  Item2.bg_u_miny := item.bg_u_miny;
  Item2.bg_u_maxy := item.bg_u_maxy;
  Item2.bg_b_minx := item.bg_b_minx;
  Item2.bg_b_maxx := item.bg_b_maxx;
  Item2.bg_f_minx := item.bg_f_minx;
  Item2.bg_f_maxx := item.bg_f_maxx;
  Item2.bg_b_miny := item.bg_b_miny;
  Item2.bg_b_maxy := item.bg_b_maxy;
  Item2.bg_f_miny := item.bg_f_miny;
  Item2.bg_f_maxy := item.bg_f_maxy;

  Item2.hole_back_cap := item.hole_back_cap;
  Item2.hole_2_dist := item.hole_2_dist;

  Item2.zero_y := item.zero_y;

  Item2.bg := item.bg;
  Item2.mat := item.mat;
  Item2.color := item.color;
  Item2.bdxmlid := item.bdxmlid;
  Item2.holeconfig_flag := item.holeconfig_flag;
  Item2.kcconig_flag := item.kcconig_flag;
  Item2.devcode := item.devcode;
  Item2.data := p;
  str := Format('Workflow="%s" JXS="%s" TIME="%s" ORDER="%s" GNO="%s" DESNO="%s" CBNO="%s" USER="%s" TYPE="%s" NAME="%s" FBSTR="%s" SIZE="%s" UNIT="%s" PackNo="%s"'
    , [GetWorkflowStr(item.workflow, item.bomstd, ''), mDistributor, FormatDateTime('yyyy-mm-dd', mDateTime), mOrderName
    , item.gno, item.gdes, item.gcb, mUserName, item.myclass, item.name, item.fbstr
      , Format('%d*%d*%d', [Round(item.bl), Round(item.bp), Round(item.bh)])
    , item.myunit, item.packno]);
  Item2.bdinfo := Format('%s MEMO="%s" Mat="%s" Color="%s" HoleStr="%s" KcStr="%s" HoleFlag="%s" KcFlag="%s" BomStd="%s" JXSPHONE="%s" JXSADDR="%s" CLIENT="%s" CLIENTPHONE="%s" CLIENTMOBILEPHONE="%s" CLIENTADDR="%s"'
    , [str, item.memo, item.mat, item.color, item.holestr, item.kcstr, item.holeconfig_flag, item.kcconig_flag, item.bomstd
    , mPhone, mAddress, mCustomerName, mCustomerPhone, mCustomerCellPhone, mCustomerAddress]);

  Item2.llfb := item.llfb;
  Item2.rrfb := item.rrfb;
  Item2.ddfb := item.ddfb;
  Item2.uufb := item.uufb;
  Item2.fb := item.fb;

  Item2.holeinfo := item.holeinfo;

  flag := 0;
  bdxml := '';
  if Item2.bdxmlid <> '' then
  begin
    bdxml := mBDXMLList.ValueOf(Item2.bdxmlid);
    flag := 1;
  end;
  if (item.bg_filename <> '') and (fileexists(item.bg_filename)) then
  begin
    bdxml := ReadStringFromFile(item.bg_filename);
    bdxml := MyUtils.ClearXMLDocTag(bdxml);
    flag := 2;
  end;
  if bdxml = '' then exit;

  mExp.AddVariable('L', '', IntToStr(Item2.gl), '', '');
  mExp.AddVariable('W', '', IntToStr(Item2.gp), '', '');
  if flag = 1 then
  begin
    if Item2.direct in [1, 5] then      //层板
    begin
      mExp.AddVariable('L', '', IntToStr(Item2.gl), '', '');
      mExp.AddVariable('W', '', IntToStr(Item2.gp), '', '');
    end;
    if Item2.direct in [2, 3] then      //背板
    begin
      mExp.AddVariable('L', '', IntToStr(Item2.gl), '', '');
      mExp.AddVariable('W', '', IntToStr(Item2.gh), '', '');
    end;
    if Item2.direct in [4, 6] then      //侧板
    begin
      mExp.AddVariable('L', '', IntToStr(Item2.gp), '', '');
      mExp.AddVariable('W', '', IntToStr(Item2.gh), '', '');
    end;
    mExp.AddVariable('CA', '', IntToStr(Item2.var_args[0]), '', '');
    mExp.AddVariable('CB', '', IntToStr(Item2.var_args[1]), '', '');
    mExp.AddVariable('CC', '', IntToStr(Item2.var_args[2]), '', '');
    mExp.AddVariable('CD', '', IntToStr(Item2.var_args[3]), '', '');
    mExp.AddVariable('CE', '', IntToStr(Item2.var_args[4]), '', '');
    mExp.AddVariable('CF', '', IntToStr(Item2.var_args[5]), '', '');
    mExp.AddVariable('CG', '', IntToStr(Item2.var_args[6]), '', '');
    mExp.AddVariable('CH', '', IntToStr(Item2.var_args[7]), '', '');

    mExp.AddVariable('CI', '', IntToStr(Item2.var_args[8]), '', '');
    mExp.AddVariable('CJ', '', IntToStr(Item2.var_args[9]), '', '');
    mExp.AddVariable('CK', '', IntToStr(Item2.var_args[10]), '', '');
    mExp.AddVariable('CL', '', IntToStr(Item2.var_args[11]), '', '');
    mExp.AddVariable('CM', '', IntToStr(Item2.var_args[12]), '', '');
    mExp.AddVariable('CN', '', IntToStr(Item2.var_args[13]), '', '');
    mExp.AddVariable('CO', '', IntToStr(Item2.var_args[14]), '', '');
    mExp.AddVariable('CP', '', IntToStr(Item2.var_args[15]), '', '');
  end;

  try
    xdoc.Active := False;
    xdoc.xml.Clear;
    xdoc.Active := True;
    xdoc.Encoding := 'gb2312';
    xdoc.Version := '1.0';
    xdoc.xml.Add(bdxml);
    xdoc.Active := True;
    root := xdoc.ChildNodes[1];         //bdxml
    node := root.ChildNodes.FindNode('Graph');
    if node <> nil then
    begin
      attri := node.AttributeNodes.FindNode('XX');
      if (attri <> nil) then Item2.isxx := MyStrToInt(attri.Text);
    end;
    n := 0;
    for i := 0 to root.ChildNodes.Count - 1 do
    begin
      node := root.ChildNodes[i];
      if (node.nodename <> 'FaceA') and (node.nodename <> 'FaceB') then Continue;
      for j := 0 to node.ChildNodes.Count - 1 do
      begin
        cnode := node.ChildNodes[j];
        if cnode.nodename <> 'BHole' then Continue;
        inc(n);
      end;
    end;
    SetLength(Item2.bhpt, n);
    n := 0;
    for i := 0 to root.ChildNodes.Count - 1 do
    begin
      node := root.ChildNodes[i];
      if (node.nodename <> 'FaceA') and (node.nodename <> 'FaceB') then Continue;
      for j := 0 to node.ChildNodes.Count - 1 do
      begin
        cnode := node.ChildNodes[j];
        if cnode.nodename <> 'BHole' then Continue;

        attri := cnode.AttributeNodes.FindNode('X');
        if attri <> nil then Item2.bhpt[n].sx := attri.Text;
        attri := cnode.AttributeNodes.FindNode('Y');
        if attri <> nil then Item2.bhpt[n].sy := attri.Text;
        attri := cnode.AttributeNodes.FindNode('R');
        if attri <> nil then Item2.bhpt[n].sr := attri.Text;
        attri := cnode.AttributeNodes.FindNode('Rb');
        if attri <> nil then Item2.bhpt[n].srb := attri.Text;

        Item2.bhpt[n].sri := Item2.bhpt[n].srb;
        attri := cnode.AttributeNodes.FindNode('X1');
        if (attri <> nil) and (attri.Text <> '') then Item2.bhpt[n].sri := attri.Text;
        attri := cnode.AttributeNodes.FindNode('HDirect');
        if attri <> nil then Item2.bhpt[n].hdirect := attri.Text;

        if attri <> nil then Item2.bhpt[n].face := node.nodename;
        attri := cnode.AttributeNodes.FindNode('Hole_Xcap');
        if attri <> nil then
        begin
          item2.bhpt[n].hole_xcap := Trunc(mExp.SimpleExpressToValue(attri.Text, 2));
          //mExp.SetSubject(attri.Text);
          //Item2.bhpt[n].hole_xcap := mExp.ToValueInt;
        end;
        attri := cnode.AttributeNodes.FindNode('Hole_Ycap');
        if attri <> nil then
        begin
          item2.bhpt[n].hole_ycap := Trunc(mExp.SimpleExpressToValue(attri.Text, 2));
          //mExp.SetSubject(attri.Text);
          //Item2.bhpt[n].hole_ycap := mExp.ToValueInt;
        end;
        attri := cnode.AttributeNodes.FindNode('Holenum_X');
        if attri <> nil then Item2.bhpt[n].holenum_x := MyStrToInt(attri.Text);
        attri := cnode.AttributeNodes.FindNode('Holenum_Y');
        if attri <> nil then Item2.bhpt[n].holenum_y := MyStrToInt(attri.Text);
        attri := cnode.AttributeNodes.FindNode('Hole_Z');
        if attri <> nil then Item2.bhpt[n].hole_z := MyStrToInt(attri.Text);

        mExp.SetSubject(Item2.bhpt[n].sx);
        Item2.bhpt[n].x := mExp.ToValueFloat;
        mExp.SetSubject(Item2.bhpt[n].sy);
        Item2.bhpt[n].y := mExp.ToValueFloat;
        mExp.SetSubject(Item2.bhpt[n].sr);
        Item2.bhpt[n].r := mExp.ToValueFloat;
        mExp.SetSubject(Item2.bhpt[n].srb);
        Item2.bhpt[n].rb := mExp.ToValueFloat;
        mExp.SetSubject(Item2.bhpt[n].sri);
        Item2.bhpt[n].ri := mExp.ToValueFloat;
        inc(n);
      end;
    end;

    xdoc.Active := False;
    xdoc.xml.Text := '';
  except
  end;
end;


procedure TLocalObject.BDXML_BDXML(var xml: string; xml2: string);
var
  i, j, isauto_acut, isauto_bcut: Integer;
  root, nodeA, nodeB, cnode: IXMLNode;
  root2, nodeA2, nodeB2, cnode2: IXMLNode;
  xdoc, xdoc2       : IXMLDocument;
  attri             : IXMLNode;
begin
  isauto_acut := 0;
  isauto_bcut := 0;
  try
    xml := MyUtils.ClearXMLDocTag(xml);
    xdoc := XMLDoc.LoadXMLData('<?xml version="1.0" encoding="gb2312"?>'+xml);
    root := xdoc.ChildNodes[1];         //bdxml
    nodeA := root.ChildNodes.FindNode('FaceA');
    nodeB := root.ChildNodes.FindNode('FaceB');
    for i := nodeA.ChildNodes.Count - 1 downto 0 do
    begin
      cnode := nodeA.ChildNodes[i];
      if (cnode.nodename = 'VHole') or (cnode.nodename = 'Cut') then
      begin
        attri := cnode.AttributeNodes.FindNode('NotAuto');
        if (cnode.nodename = 'Cut') and (attri <> nil) and (attri.Text = '1') then isauto_acut := 1; //有自动开槽
        if not ((attri <> nil) and (attri.Text = '1')) then //非自动孔删除
          nodeA.ChildNodes.Remove(cnode);
      end;
    end;
    for i := nodeB.ChildNodes.Count - 1 downto 0 do
    begin
      cnode := nodeB.ChildNodes[i];
      if (cnode.nodename = 'VHole') or (cnode.nodename = 'Cut') then
      begin
        attri := cnode.AttributeNodes.FindNode('NotAuto');
        if (cnode.nodename = 'Cut') and (attri <> nil) and (attri.Text = '1') then isauto_bcut := 1; //有自动开槽
        if not ((attri <> nil) and (attri.Text = '1')) then //非自动孔删除
          nodeB.ChildNodes.Remove(cnode);
      end;
    end;

    xml2 := MyUtils.ClearXMLDocTag(xml2);
    xdoc2 := XMLDoc.LoadXMLData('<?xml version="1.0" encoding="gb2312"?>'+xml2);
    root2 := xdoc2.ChildNodes[1];       //bdxml
    nodeA2 := root2.ChildNodes.FindNode('FaceA');
    nodeB2 := root2.ChildNodes.FindNode('FaceB');
    for i := nodeA2.ChildNodes.Count - 1 downto 0 do
    begin
      cnode2 := nodeA2.ChildNodes[i];
      if (cnode2.nodename = 'VHole') or (cnode2.nodename = 'Cut') then
      begin
        attri := cnode2.AttributeNodes.FindNode('NotAuto');
        if (isauto_acut = 1) and (cnode2.nodename = 'Cut') and (not ((attri <> nil) and (attri.Text = '1'))) then //有自定义开槽的时候把自动计算的开槽清除掉
        begin
          Continue;
        end;
        cnode := cnode2.clonenode(True);
        nodeA.ChildNodes.Add(cnode);
      end;
    end;
    for i := nodeB2.ChildNodes.Count - 1 downto 0 do
    begin
      cnode2 := nodeB2.ChildNodes[i];
      if (cnode2.nodename = 'VHole') or (cnode2.nodename = 'Cut') then
      begin
        attri := cnode2.AttributeNodes.FindNode('NotAuto');
        if (isauto_bcut = 1) and (cnode2.nodename = 'Cut') and (not ((attri <> nil) and (attri.Text = '1'))) then //有自定义开槽的时候把自动计算的开槽清除掉
        begin
          Continue;
        end;
        cnode := cnode2.clonenode(True);
        nodeB.ChildNodes.Add(cnode);
      end;
    end;
    xml := root.xml;
  finally
    xdoc := nil;
    xdoc2 := nil;
  end;
end;

procedure TLocalObject.GetXptlist(poi: PBomOrderItem; var xptlist_isxx, xptlist_jx, xptlist_pl:Integer);
const def_bgparam = '{^PL^:^0^,^Cut^:^0^,^DJ^:^0^,^JX^:^0^,^CutA^:^0.0000^,^CutB^:^0.0000^,^BarH^:^0.0000^,^Points^:^^}';
var
root, node, cnode, attri:IXMLNode;
i, j, pl:Integer;
  xml, str, paramstr               : string;
jo:ISuperObject;
s1, s2:string;
begin
  xptlist_isxx := 0;
  xptlist_jx := 0;
  xptlist_pl := 1;
  xml := gBGHash.ValueOf(BGName(poi.bg));
  if (xml = '') and (poi.bg<>'BG::RECT') then exit;

  try
    if xml<>'' then
    begin
      xdoc.Active := False;
      xdoc.xml.Text := xml;
      xdoc.Active := True;
      root := xdoc.ChildNodes[1];    //Graph
      attri := root.AttributeNodes.FindNode('Param');
      if attri<>nil then paramstr := attri.Text;
      for j:=0 to root.ChildNodes.Count-1 do
      begin
        node := root.ChildNodes[j];
        str := '';
        attri := node.AttributeNodes.FindNode('Type');
        if attri<>nil then str := attri.Text;
        if (str='Polygon') and (node.NodeName='PlaneXY') then xptlist_pl := 1;
        if (str='Polygon') and (node.NodeName='PlaneXZ') then xptlist_pl := 2;
        if (str='Polygon') and (node.NodeName='PlaneYZ') then xptlist_pl := 3;
      end;
      xdoc.Active := False;
      xdoc.xml.Text := '';
    end;
  except
  end;

  if not ((poi.mBGParam='') or (poi.mBGParam=def_bgparam)) then paramstr := poi.mBGParam;

  try
    str := StringReplace(paramstr, '^Inherit^:^1^ ', '', [rfReplaceAll]);
    str := StringReplace(str, '^', '"', [rfReplaceAll]);
    jo := SO(str);
    pl := jo.I['PL'];
    if pl<>0 then xptlist_pl := pl;

    xptlist_jx := jo.I['JX'];
  finally
    jo := nil;
  end;
end;

procedure TLocalObject.GetSpaceItem(p: Pointer; var space: string;
  var space_x, space_y, space_z: Integer);
var
  poi               : PBomOrderItem;
begin
  poi := p;
  space := poi.subspace;
  space_x := poi.space_x;
  space_y := poi.space_y;
  space_z := poi.space_z;
end;

function TLocalObject.GetWorkflowStr(workflow, bomstd, hole: string): string;
var
  i                 : Integer;
  pwf               : PWorkflow;
begin
  Result := '';
  for i := 0 to workflowlist.Count - 1 do
  begin
    pwf := workflowlist[i];
    if (pwf.name = workflow) and ((pwf.bomstd = '*') or (pwf.bomstd = bomstd)) and ((pwf.hole = '*') or (pwf.hole = hole)) then
    begin
      Result := Result + Format('%d,%d,%d,%d', [pwf.id, pwf.board_cut, pwf.edge_banding, pwf.punching]);
      exit;
    end;
  end;
end;

procedure TLocalObject.ShowBomMessage(str: string);
var js, objstr:string;
begin
  if Assigned(mPluginHost) then
  begin
    js := Format('OnShowBomMessage("%s");', [MyUtils.EncodeJSVariant(str)]);
    objstr := mPluginHost.GetBrowserWindowObject.Evaluate(pchar(js));
  end else begin
    ShowMessage(str);
  end;
end;

function TLocalObject.GetBomlistString;
  function NanToZero(num:real):real;
  begin
    if isnan(num) then Result:=0
    else Result :=num;
  end;
Var
  connstr, str, s1, s2, str1,str2,var_args,var_names,is_calc_holeconfig,akc,bkc,ahole,bhole: string;
  i, j, k, childnum : Integer;
  pbom              : PBomRecord;
  p                 : PBomOrderItem;
  mp                :TProductItem;
  bomlistjo, cjo, ja : ISuperObject;
begin
  result :='';
  bomlistjo := TSuperObject.Create();
  ja := TSuperObject.Create(stArray);
  for i := 0 to mProductList.count -1 do
  begin
    mp := mProductList[i];
    cjo := TSuperObject.Create();
    cjo.S['name'] :=mp.name;
    cjo.S['gno'] :=mp.gno;
    cjo.S['des'] :=mp.des;
    cjo.S['gcb'] :=mp.gcb;
    cjo.S['color'] :=mp.color;
    cjo.S['mat'] :=mp.mat;
    cjo.S['Extra'] :=mp.Extra;
    cjo.I['id'] :=mp.id;
    cjo.I['l'] :=mp.l;
    cjo.I['d'] :=mp.d;
    cjo.I['h'] :=mp.h;
    cjo.I['bh'] :=mp.bh;
    ja.AsArray.Add(cjo);
  end;
  bomlistjo.O['mProductList'] := ja;
  ja := TSuperObject.Create(stArray);
  for i := 0 to bomlist.Count - 1 do
  begin
    p := bomlist[i];
    if ((p.outputtype = '物料') or (p.outputtype = '无')) then Continue;
    if p.desc = '' then Continue;
    if (p.bl < 1) or (p.bp < 1) or (p.bh < 1) then Continue;
    cjo := TSuperObject.Create();
    cjo.I['num'] := p.num;
    cjo.S['mat'] := p.mat;
    cjo.S['gno'] := p.gno;
    cjo.S['bomstddes'] := p.bomstddes;
    cjo.I['x'] := p.x;
    cjo.I['y'] := p.y;
    cjo.I['z'] := p.z;
    cjo.I['pl'] := p.pl;
    cjo.I['pd'] := p.pd;
    cjo.I['ph'] := p.ph;
    cjo.I['l'] := p.l;
    cjo.I['p'] := p.p;
    cjo.I['h'] := p.h;
    cjo.I['gl'] := p.gl;
    cjo.I['gp'] := p.gp;
    cjo.I['gh'] := p.gh;
    cjo.D['bl'] := p.bl;
    cjo.D['bp'] := p.bp;
    cjo.D['bh'] := p.bh;
    cjo.S['nodename'] := p.nodename;
    cjo.S['name'] := p.name;
    cjo.I['id'] := p.id;
    cjo.S['desc'] := p.desc;
    cjo.S['bomtype'] := p.bomtype;
    cjo.S['myclass'] := p.myclass;
    cjo.S['myunit'] := p.myunit;
    cjo.S['color'] := p.color;
    cjo.I['direct'] := p.direct;

    cjo.I['cid'] := p.cid;
    cjo.I['pid'] := p.pid;
    cjo.I['seq'] := p.seq;
    cjo.I['classseq'] := p.classseq;
    cjo.I['mark'] := p.mark;
    cjo.I['vp'] := p.vp;
    cjo.S['code'] := p.code;
    cjo.S['mat2'] := p.mat2;
    cjo.S['mat3'] := p.mat3;
    cjo.S['workflow'] := p.workflow;
    cjo.I['space_x'] := p.space_x;
    cjo.I['space_y'] := p.space_y;
    cjo.I['space_z'] := p.space_z;
    cjo.I['space_id'] := p.space_id;
    cjo.I['gcl'] := p.gcl;
    cjo.I['gcd'] := p.gcd;
    cjo.I['gch'] := p.gch;
    cjo.I['gcl2'] := p.gcl2;
    cjo.I['gcd2'] := p.gcd2;
    cjo.I['gch2'] := p.gch2;
    cjo.S['tmp_soz'] := p.tmp_soz;
    cjo.I['lx'] := p.lx;
    cjo.I['ly'] := p.ly;
    cjo.I['lz'] := p.lz;
    cjo.I['holeflag'] := p.holeflag;
    cjo.I['linemax'] := p.linemax;
    cjo.I['holetype'] := p.holetype;
    cjo.D['ox'] := NanToZero(p.ox);
    cjo.D['oy'] := NanToZero(p.oy);
    cjo.D['oz'] := NanToZero(p.oz);
    cjo.I['childnum'] := p.childnum;
    cjo.S['bomdes'] := p.bomdes;
    cjo.S['bomwjdes'] := p.bomwjdes;
    cjo.S['childbom'] := p.childbom;
    cjo.S['linecalc'] := p.linecalc;
    cjo.S['bomstd'] := p.bomstd;
    cjo.S['bg'] := p.bg;
    cjo.I['lgflag'] := p.lgflag;
    cjo.I['holeid'] := p.holeid;
    cjo.I['kcid'] := p.kcid;
    cjo.D['lfb'] := p.lfb;
    cjo.D['llk'] := p.llk;
    cjo.D['wfb'] := p.wfb;
    cjo.D['wlk'] := p.wlk;
    cjo.D['llfb'] := p.llfb;
    cjo.D['rrfb'] := p.rrfb;
    cjo.D['ddfb'] := p.ddfb;
    cjo.D['uufb'] := p.uufb;
    cjo.D['fb'] := p.fb;
    cjo.S['memo'] := p.memo;
    cjo.S['kcstr'] := p.kcstr;
    cjo.S['holestr'] := p.holestr;
    cjo.S['gdes'] := p.gdes;
    cjo.S['gcb'] := p.gcb;
    cjo.S['extra'] := p.extra;
    cjo.S['fbstr'] := p.fbstr;
    cjo.S['subspace'] := p.subspace;
    cjo.S['process'] := p.process;
    cjo.S['ls'] := p.ls;
    cjo.S['bdxmlid'] := p.bdxmlid;
    cjo.S['user_fbstr'] := p.user_fbstr;
    cjo.I['value_lsk'] := p.value_lsk;
    cjo.I['value_rsk'] := p.value_rsk;
    cjo.I['value_zk'] := p.value_zk;
    cjo.I['value_zs'] := p.value_zs;
    cjo.I['value_ls'] := p.value_ls;
    cjo.I['value_lg'] := p.value_lg;
    cjo.I['value_ltm'] := p.value_ltm;
    cjo.I['value_rtm'] := p.value_rtm;
    cjo.S['a_hole_info'] := p.a_hole_info;
    cjo.S['b_hole_info'] := p.b_hole_info;
    cjo.S['holeinfo'] := p.holeinfo;
    cjo.B['isoutput'] := p.isoutput;
    cjo.B['is_outline'] := p.is_outline;
    cjo.S['outputtype'] := p.outputtype;
    cjo.S['holeconfig_flag'] := p.holeconfig_flag;
    cjo.S['kcconig_flag'] := p.kcconig_flag;
    cjo.S['bg_data'] := p.bg_data;
    cjo.S['mBGParam'] := p.mBGParam;
    cjo.S['bg_filename'] := p.bg_filename;
    cjo.S['mpr_filename'] := p.mpr_filename;
    cjo.S['bpp_filename'] := p.bpp_filename;
    cjo.S['devcode'] := p.devcode;
    cjo.I['zero_y'] := p.zero_y;
    cjo.I['direct_calctype'] := p.direct_calctype;
    cjo.I['youge_holecalc'] := p.youge_holecalc;
    cjo.I['is_output_bgdata'] := p.is_output_bgdata;
    cjo.I['is_output_mpr'] := p.is_output_mpr;
    cjo.I['is_output_bpp'] := p.is_output_bpp;
    cjo.I['bg_l_minx'] := p.bg_l_minx;
    cjo.I['bg_l_maxx'] := p.bg_l_maxx;
    cjo.I['bg_r_minx'] := p.bg_r_minx;
    cjo.I['bg_r_maxx'] := p.bg_r_maxx;
    cjo.I['bg_l_miny'] := p.bg_l_miny;
    cjo.I['bg_l_maxy'] := p.bg_l_maxy;
    cjo.I['bg_r_miny'] := p.bg_r_miny;
    cjo.I['bg_r_maxy'] := p.bg_r_maxy;
    cjo.I['bg_d_minx'] := p.bg_d_minx;
    cjo.I['bg_d_maxx'] := p.bg_d_maxx;
    cjo.I['bg_u_minx'] := p.bg_u_minx;
    cjo.I['bg_u_maxx'] := p.bg_u_maxx;
    cjo.I['bg_d_miny'] := p.bg_d_miny;
    cjo.I['bg_d_maxy'] := p.bg_d_maxy;
    cjo.I['bg_u_miny'] := p.bg_u_miny;
    cjo.I['bg_u_maxy'] := p.bg_u_maxy;
    cjo.I['bg_b_minx'] := p.bg_b_minx;
    cjo.I['bg_b_maxx'] := p.bg_b_maxx;
    cjo.I['bg_f_minx'] := p.bg_f_minx;
    cjo.I['bg_f_maxx'] := p.bg_f_maxx;
    cjo.I['bg_b_miny'] := p.bg_b_miny;
    cjo.I['bg_b_miny'] := p.bg_b_miny;
    cjo.I['bg_f_miny'] := p.bg_f_miny;
    cjo.I['bg_f_maxy'] := p.bg_f_maxy;
    cjo.I['hole_back_cap'] := p.hole_back_cap;
    cjo.I['hole_2_dist'] := p.hole_2_dist;
    cjo.B['trans_ab'] := p.trans_ab;
    cjo.S['ahole_index'] := ahole;
    cjo.S['bhole_index'] := bhole;
    cjo.S['akc_index'] := akc;
    cjo.S['bkc_index'] := bkc;
    cjo.S['is_calc_holeconfig'] := is_calc_holeconfig;
    cjo.D['basewj_price'] := NanToZero(p.basewj_price);
    cjo.S['extend'] := p.extend;
    cjo.S['group'] := p.group;
    cjo.S['packno'] := p.packno;
    cjo.S['userdefine'] := p.userdefine;
    cjo.S['erpunit'] := p.erpunit;
    cjo.S['erpmatcode'] := p.erpmatcode;
    cjo.S['blockmemo'] := p.blockmemo;
    cjo.S['number_text'] := p.number_text;
    ja.AsArray.Add(cjo);
  end;
  bomlistjo.O['bomlist'] := ja;
  ja := TSuperObject.Create(stArray);
  for i := 0 to basewjlist.count -1 do
  begin
    p := basewjlist[i];
    cjo := TSuperObject.Create();
    cjo.S['name'] := p.name;
    cjo.S['outputname'] := p.name;
    cjo.S['myunit'] := p.myunit;
    cjo.S['gno'] := p.gno;
    cjo.S['gdes'] := p.gdes;
    cjo.I['square'] := 1;
    cjo.I['cost'] := 0;
    cjo.B['isoutput'] := True;
    cjo.B['isnotstd'] := True;
    cjo.B['is_calc_cost'] := False;
    cjo.I['num'] := 1;
    cjo.S['pricetype'] := '单件';
    cjo.S['myclass'] := '五金';
    cjo.D['price'] := NanToZero(p.basewj_price);
    cjo.D['price2'] := NanToZero(p.basewj_price);

    cjo.D['totalprice'] := NanToZero(p.basewj_price);
    cjo.D['totalprice2'] := NanToZero(p.basewj_price);
    ja.AsArray.Add(cjo);
  end;
  bomlistjo.O['basewjlist'] := ja;
  result := bomlistjo.AsString;
  bomlistjo:=nil;
end;

procedure GetNodeattris(node: IXMLNode; Var MBData: ISuperObject);
  function getattris(cnode: IXMLNode):ISuperObject;
  Var
    i : Integer;
    attri : IXMLNode;
  begin
    Result := TSuperObject.Create();
    for i:=0 to cnode.AttributeNodes.Count-1 do
    begin
      attri := cnode.AttributeNodes[i];
      Result.S[attri.NodeName]:=attri.Text;
    end;
  end;
Var
  n, j : Integer;
  attri, cnode:IXMLNode;
  cjo,ja : ISuperObject;
begin
  for j:=0 to node.ChildNodes.Count-1 do
  begin
    cnode := node.ChildNodes[j];
    if (MBData.O[cnode.nodename] <> nil) then ja:= MBData.O[cnode.nodename]
    else ja := TSuperObject.Create(stArray);
    ja.AsArray.Add(getattris(cnode));
    MBData.O[cnode.nodename] := ja;
    if cnode.ChildNodes.Count > 0 then
    begin
      n :=ja.AsArray.Length;
      cjo:= ja.AsArray.O[n-1];
      getnodeattris(cnode, cjo);
    end;
  end;
  ja:=nil;
  cjo:=nil;
end;

function TLocalObject.GetSlidingColor(name: string): PSlidingColor;
var
  i                 : Integer;
  p                 : PSlidingColor;
begin
  Result := nil;
  for i := 0 to mSlidingColorList.Count - 1 do
  begin
    p := mSlidingColorList[i];
    if (p.name = name) then
    begin
      Result := p;
      break;
    end;
  end;
end;

procedure TLocalObject.SetSetDoors(b: boolean);
begin
  self.mIsSetDoors := b;
end;

function TLocalObject.GetSlidingColorClass(myclass, mat,
  color: string): PSlidingColorClass;
var
  i                 : Integer;
  p                 : PSlidingColorClass;
begin
  Result := nil;
  for i := 0 to mSlidingColorClassList.Count - 1 do
  begin
    p := mSlidingColorClassList[i];
    if (p.myclass = myclass) and (p.color = color) and (p.mat=mat) then
    begin
      Result := p;
      break;
    end;
  end;
end;

function TLocalObject.GetSlidingColorClass(myclass,
  color: string): PSlidingColorClass;
var
  i                 : Integer;
  p                 : PSlidingColorClass;
begin
  Result := nil;
  for i := 0 to mSlidingColorClassList.Count - 1 do
  begin
    p := mSlidingColorClassList[i];
    if (p.myclass = myclass) and (p.color = color) then
    begin
      Result := p;
      break;
    end;
  end;
end;

procedure TLocalObject.ClearSlidingAndDoorList;
var
  pcolor            : PSlidingColor;
  pexp              : PSlidingExp;
  pstype            : PSlidingType;
  psp               : PSlidingParam;
  ptrack            : PTrackParam;
  pudbox            : PUDBoxParam;
  phbox             : PHBoxParam;
  pvbox             : PVBoxParam;
  pnltype           : PPanelType;
  pa                : PAccessory;
  pcolorclass       : PSlidingColorClass;
  pcolorclass2      : PSlidingColorClass2;
  i,j                 : Integer;
  pgroup            : ^SlidingMyClassGroup;
  pbom              : PSlidingWjBom;
  pbomdetail        : PSlidingWjBomDetail;
  pssexp            : PSlidingShutterExp;
  pnlbomdetail      :PSlidingPanelBomDetail;
  hfg3 : PSlidingHfg2;
  hfg4 : PSlidingHfg2;
  hfg2 : PSlidingHfg2;
  sfg2 : PSlidingHfg2;
  sfg3 : PSlidingHfg2;
  sfg4 : PSlidingHfg2;
  opa:  POptionalAcc;

  pdoorcolor            : PDoorsColor;
  pdoorexp              : PDoorsExp;
  ptype             : PDoorsType;
  pparam            : PDoorsParam;
  php               : PDoorHBoxParam;
  ppt               : PDoorPanelType;
  doorpa                : PDoorAccessory;
  doorpcolorclass       : PDoorsColorClass;
  pshutterexp       : PDoorsShutterExp;
  pwjbom            : PDoorsWjBom;
  pwjbomdetail      : PDoorsWjBomDetail;
  pprice            : PDoorsPrice;
  phandle           : PDoorsHandle;
  phinge            : PDoorsHinge;
  pcurhinge         : PDoorsCurHinge;
  tmp               : TADOQuery;
  id                : Integer;
  doorpcolorclass2      : PDoorsColorClass2;
  ppbdetail:    PDoorsPanelBomDetail;
  pxml:PDoorXML;
  cfg : PCfgTable;
  poi : PBomOrderItem;
begin
  for i := 0 to mSlidingColorList.Count - 1 do
  begin
    pcolor := mSlidingColorList[i];
	  pcolor.name := '';
	  pcolor.myclass := '';
	  pcolor.code := '';
    dispose(pcolor);
  end;
  mSlidingColorList.Clear;

  for i := 0 to mSlidingExpList.Count - 1 do
  begin
    pexp := mSlidingExpList[i];
	  pexp.name := '';
    dispose(pexp);
  end;
  mSlidingExpList.Clear;

  for i := 0 to mSlidingTypeList.Count - 1 do
  begin
    pstype := mSlidingTypeList[i];
	  pstype.name := '';
    dispose(pstype);
  end;
  mSlidingTypeList.Clear;

  for i := 0 to mSlidingParamList.Count - 1 do
  begin
    psp := mSlidingParamList[i];
	  psp.name := '';
	  psp.myclass := '';
	  psp.vboxtype := '';
	  psp.wjname := '';
	  psp.track := '';
	  psp.udbox := '';
	  psp.hbox := '';
	  psp.zndlun := '';
	  psp.ddlun := '';
	  psp.diaolun := '';
	  psp.gddwlun := '';
	  psp.hddwlun := '';
	  psp.ls := '';
	  psp.memo := '';
    dispose(psp);
  end;
  mSlidingParamList.Clear;

  for i := 0 to mHBoxParamList.Count - 1 do
  begin
    phbox := mHBoxParamList[i];
	  phbox.name := '';
	  phbox.wlcode := '';
	  phbox.bjcode := '';
	  phbox.wjname := '';
	  phbox.model := '';
	  phbox.memo := '';
	  phbox.bdfile := '';
    dispose(phbox);
  end;
  mHBoxParamList.Clear;

  for i := 0 to mTrackParamList.Count - 1 do
  begin
    ptrack := mTrackParamList[i];
	  ptrack.name := '';
	  ptrack.wlupcode := '';
	  ptrack.wldncode := '';
	  ptrack.upname := '';
	  ptrack.dnname := '';
	  ptrack.wjname1 := '';
	  ptrack.wjname2 := '';
	  ptrack.upmodel := '';
	  ptrack.dnmodel := '';
	  ptrack.upmemo := '';
	  ptrack.dnmemo := '';
	  ptrack.upbdfile := '';
	  ptrack.dnbdfile := '';
    dispose(ptrack);
  end;
  mTrackParamList.Clear;

  for i := 0 to mUDBoxParamList.Count - 1 do
  begin
    pudbox := mUDBoxParamList[i];
	  pudbox.name := '';
	  pudbox.wlupcode := '';
	  pudbox.wldncode := '';
	  pudbox.upname := '';
	  pudbox.dnname := '';
	  pudbox.wjname1 := '';
	  pudbox.wjname2 := '';
	  pudbox.upmodel := '';
	  pudbox.dnmodel := '';
	  pudbox.upmemo := '';
	  pudbox.dnmemo := '';
	  pudbox.upbdfile := '';
	  pudbox.dnbdfile := '';
    dispose(pudbox);
  end;
  mUDBoxParamList.Clear;

  for i := 0 to mVBoxParamList.Count - 1 do
  begin
    pvbox := mVBoxParamList[i];
	  pvbox.name := '';
	  pvbox.wlcode := '';
	  pvbox.wjname := '';
	  pvbox.model := '';
	  pvbox.memo := '';
	  pvbox.bdfile := '';
    dispose(pvbox);
  end;
  mVBoxParamList.Clear;

  for i := 0 to mPanelTypeList.Count - 1 do
  begin
    pnltype := mPanelTypeList[i];
	  pnltype.name := '';
	  pnltype.wjname := '';
	  pnltype.bktype := '';
	  pnltype.direct := '';
	  pnltype.pnl2d := '';
	  pnltype.slave := '';
	  pnltype.slave2 := '';
	  pnltype.mk3d := '';
	  pnltype.memo := '';
	  pnltype.memo2 := '';
	  pnltype.memo3 := '';
	  pnltype.bdfile := '';
    dispose(pnltype);
  end;
  mPanelTypeList.Clear;

  for i := 0 to mSlidingAccessoryList.Count - 1 do
  begin
    pa := mSlidingAccessoryList[i];
	  pa.name := '';
	  pa.myunit := '';
	  pa.wlcode := '';
	  pa.myclass := '';
	  pa.color := '';
	  pa.memo := '';
	  pa.memo2 := '';
	  pa.memo3 := '';
	  pa.bdfile := '';
    dispose(pa);
  end;
  mSlidingAccessoryList.Clear;

  for i := 0 to mSlidingColorClassList.Count - 1 do
  begin
    pcolorclass := mSlidingColorClassList[i];
	  pcolorclass.color := '';
	  pcolorclass.myclass := '';
	  pcolorclass.mat := '';
	  pcolorclass.color2 := '';
	  pcolorclass.wlcode := '';
	  pcolorclass.bjcode := '';
	  pcolorclass.color3 := '';
	  pcolorclass.color4 := '';
	  pcolorclass.skcolor1 := '';
	  pcolorclass.skcolor2 := '';
	  pcolorclass.skcolor3 := '';
	  pcolorclass.skcolor4 := '';
    dispose(pcolorclass);
  end;
  mSlidingColorClassList.Clear;
  for i := 0 to mSlidingColorClass2List.Count - 1 do
  begin
	  pcolorclass2 := mSlidingColorClass2List[i];
    pcolorclass2.bktype := '';
    pcolorclass2.color := '';
    dispose(pcolorclass2);
  end;
  mSlidingColorClass2List.Clear;

  for i := 0 to mSlidingMyClassGroupList.Count - 1 do
  begin
    pgroup := mSlidingMyClassGroupList[i];
	  pgroup.name := '';
    dispose(pgroup);
  end;
  mSlidingMyClassGroupList.Clear;

  for i := 0 to mSlidingWjBomList.Count - 1 do
  begin
    pbom := mSlidingWjBomList[i];
	  pbom.name := '';
    dispose(pbom);
  end;
  mSlidingWjBomList.Clear;

  for i := 0 to mSlidingWjBomDetailList.Count - 1 do
  begin
    pbomdetail := mSlidingWjBomDetailList[i];
	  pbomdetail.bomname := '';
	  pbomdetail.name := '';
	  pbomdetail.l := '';
	  pbomdetail.d := '';
	  pbomdetail.num := '';
	  pbomdetail.bdfile := '';
    dispose(pbomdetail);
  end;
  mSlidingWjBomDetailList.Clear;

  for i := 0 to mPanelBomDetailList.Count - 1 do
  begin
	  pnlbomdetail := mPanelBomDetailList[i];
    pnlbomdetail.bomclass := '';
    pnlbomdetail.bomname := '';
    pnlbomdetail.l := '';
    pnlbomdetail.w := '';
    pnlbomdetail.h := '';
    pnlbomdetail.mat := '';
    pnlbomdetail.color := '';
    pnlbomdetail.bomtype := '';
    pnlbomdetail.memo := '';
    pnlbomdetail.memo2 := '';
    pnlbomdetail.memo3 := '';
    pnlbomdetail.bdfile := '';
    dispose(pnlbomdetail);
  end;
  mPanelBomDetailList.Clear;

  for i := 0 to mSSExpList.Count - 1 do
  begin
    pssexp := mSSExpList[i];
	  pssexp.PanelType := '';
    dispose(pssexp);
  end;
  mSSExpList.Clear;

  //门转换表
  for i := 0 to mCfglist.Count - 1 do
  begin
	  cfg := mCfglist[i];
    cfg.name := '';
    cfg.frametype := '';
    cfg.bomname := '';
    cfg.munit := '';
    dispose(cfg);
  end;
  mCfglist.Clear;
  
  //自选配件
  for i := 0 to OptionalAccList.Count - 1 do
  begin
    opa := OptionalAccList[i];
	  opa.name := '';
    dispose(opa);
  end;
  OptionalAccList.Clear;

  //趟门2横分格
  for i := 0 to SlidingHfg2List.Count - 1 do
  begin
    hfg2 := SlidingHfg2List[i];
	  hfg2.fgtype := '';
    hfg2.spszh := '';
    hfg2.spmk := '';
    hfg2.varlist := '';
    hfg2.mxlist := '';
    hfg2.image := '';
    dispose(hfg2);
  end;
  SlidingHfg2List.Clear;

  //趟门3横分格
  for i := 0 to SlidingHfg3List.Count - 1 do
  begin
    hfg3 := SlidingHfg3List[i];
	  hfg3.fgtype := '';
    hfg3.spszh := '';
    hfg3.varlist := '';
    hfg3.mxlist := '';
    hfg3.image := '';
    dispose(hfg3);
  end;
  SlidingHfg3List.Clear;

  //趟门4横分格
  for i := 0 to SlidingHfg4List.Count - 1 do
  begin
    hfg4 := SlidingHfg4List[i];
	  hfg4.fgtype := '';
    hfg4.spszh := '';
    hfg4.varlist := '';
    hfg4.mxlist := '';
    hfg4.image := '';
    dispose(hfg4);
  end;
  SlidingHfg3List.Clear;

  //趟门2竖分格
  for i := 0 to SlidingSfg2List.Count - 1 do
  begin
    Sfg2 := SlidingSfg2List[i];
	  Sfg2.fgtype := '';
    Sfg2.spszh := '';
    Sfg2.varlist := '';
    Sfg2.mxlist := '';
    Sfg2.image := '';
    dispose(Sfg2);
  end;
  SlidingSfg2List.Clear;

  //趟门3竖分格
  for i := 0 to SlidingSfg3List.Count - 1 do
  begin
    Sfg3 := SlidingSfg3List[i];
	  Sfg3.fgtype := '';
    Sfg3.spszh := '';
    Sfg3.varlist := '';
    Sfg3.mxlist := '';
    Sfg3.image := '';
    dispose(Sfg3);
  end;
  SlidingSfg3List.Clear;

  //趟门4竖分格
  for i := 0 to SlidingSfg4List.Count - 1 do
  begin
    Sfg4 := SlidingSfg4List[i];
	  Sfg4.fgtype := '';
    Sfg4.spszh := '';
    Sfg4.varlist := '';
    Sfg4.mxlist := '';
    Sfg4.image := '';
    dispose(Sfg4);
  end;
  SlidingSfg4List.Clear;

  //横中横
  for i := 0 to HSHBoxParamList.Count - 1 do
  begin
    phbox := HSHBoxParamList[i];
    phbox.name := '';
    phbox.wlcode := '';
    phbox.bjcode := '';
    phbox.wjname := '';
    phbox.model := '';
    phbox.memo := '';
    phbox.bdfile := '';
    phbox.frametype := '';
    dispose(phbox);
  end;
  HSHBoxParamList.Clear;

  //竖中横
  for i := 0 to SHBoxParamList.Count - 1 do
  begin
    phbox := SHBoxParamList[i];
    phbox.name := '';
    phbox.wlcode := '';
    phbox.bjcode := '';
    phbox.wjname := '';
    phbox.model := '';
    phbox.memo := '';
    phbox.bdfile := '';
    phbox.frametype := '';
    dispose(phbox);
  end;
  SHBoxParamList.Clear;

  bomdeslist.Clear;
  doordeslist.Clear;
  slidingdeslist.Clear;

  //掩门
  for i := 0 to mExpList.Count - 1 do
  begin
	  pdoorexp := mExpList[i];
    pdoorexp.name := '';
    dispose(pdoorexp);
  end;
  mExpList.Clear;

  for i := 0 to mTypeList.Count - 1 do
  begin
	  ptype := mTypeList[i];
    ptype.name := '';
    ptype.hinge := '';
    ptype.myclass := '';
    ptype.hinge1 := '';
    ptype.hinge2 := '';
    dispose(ptype);
  end;
  mTypeList.Clear;

  for i := 0 to mParamList.Count - 1 do
  begin
	  pparam := mParamList[i];
    pparam.name := '';
    pparam.DoorsType := '';
    pparam.handle := '';
    pparam.wjname := '';
    pparam.hboxname := '';
    pparam.paneltype := '';
    pparam.vboxname := '';
    pparam.udboxname := '';
    pparam.vboxl := '';
    pparam.udboxl := '';
    pparam.d3name := '';
    pparam.hbox3d := '';
    pparam.ubox3d := '';
    pparam.dbox3d := '';
    pparam.vdirect := '';
    pparam.vfbstr := '';
    pparam.uddirect := '';
    pparam.udfbstr := '';
    pparam.vmemo := '';
    pparam.udmemo := '';
    pparam.fbstr := '';
    pparam.bomtype := '';
    pparam.left_doorxml := '';
    pparam.right_doorxml := '';
    pparam.doorxml := '';
    pparam.bdfile := '';
    pparam.l_bdfile := '';
    pparam.r_bdfile := '';
    pparam.u_bdfile := '';
    pparam.d_bdfile := '';
    dispose(pparam);
  end;
  mParamList.Clear;

  for i := 0 to mHandleList.Count - 1 do
  begin
	  phandle := mHandleList[i];
    phandle.name := '';
    phandle.wjname := '';
    phandle.xpos := '';
    phandle.ypos := '';
    phandle.width := '';
    phandle.height := '';
    phandle.depth := '';
    phandle.depthpos := '';
    phandle.bomtype := '';
    phandle.memo := '';
    phandle.holescript := '';
    dispose(phandle);
  end;
  mHandleList.Clear;

  for i := 0 to mHingeList.Count - 1 do
  begin
	  phinge := mHingeList[i];
    phinge.name := '';
    phinge.mytype := '';
    phinge.wjname := '';
    phinge.bomtype := '';
    phinge.memo := '';
    phinge.alias := '';
    dispose(phinge);
  end;
  mHingeList.Clear;

  for i := 0 to mCurHingeList.Count - 1 do
  begin
	  pcurhinge := mCurHingeList[i];
    pcurhinge.name := '';
    pcurhinge.wjname := '';
    pcurhinge.bomtype := '';
    pcurhinge.memo := '';
    pcurhinge.hingetype := '';
    dispose(pcurhinge);
  end;
  mCurHingeList.Clear;

  for i := 0 to mDoorHBoxParamList.Count - 1 do
  begin
	  php := mDoorHBoxParamList[i];
    php.name := '';
    php.wjname := '';
    php.bomtype := '';
    php.memo := '';
    php.direct := '';
    php.fbstr := '';
    php.model := '';
    php.bdfile := '';
    dispose(php);
  end;
  mDoorHBoxParamList.Clear;

  for i := 0 to mDoorPanelTypeList.Count - 1 do
  begin
	  ppt := mDoorPanelTypeList[i];
    ppt.name := '';
    ppt.mytype := '';
    ppt.bomtype := '';
    ppt.bktype := '';
    ppt.direct := '';
    ppt.fbstr := '';
    ppt.pnl3d := '';
    ppt.memo := '';
    ppt.panelbom := '';
    ppt.memo2 := '';
    ppt.memo3 := '';
    ppt.bdfile := '';
    dispose(ppt);
  end;
  mDoorPanelTypeList.Clear;

  for i := 0 to mAccessoryList.Count - 1 do
  begin
	  doorpa := mAccessoryList[i];
    doorpa.name := '';
    doorpa.myunit := '';
    doorpa.mytype := '';
    doorpa.bomtype := '';
    doorpa.color := '';
    doorpa.memo := '';
    doorpa.bdfile := '';
    dispose(doorpa);
  end;
  mAccessoryList.Clear;

  for i := 0 to mColorList.Count - 1 do
  begin
	  pdoorcolor := mColorList[i];
    pdoorcolor.name := '';
    dispose(pdoorcolor);
  end;
  mColorList.Clear;

  for i := 0 to mColorClassList.Count - 1 do
  begin
	  doorpcolorclass := mColorClassList[i];
    doorpcolorclass.color := '';
    doorpcolorclass.myclass := '';
    doorpcolorclass.mat := '';
    doorpcolorclass.color2 := '';
    doorpcolorclass.color3 := '';
    doorpcolorclass.color4 := '';
    dispose(doorpcolorclass);
  end;
  mColorClassList.Clear;

  for i := 0 to mColorClass2List.Count - 1 do
  begin
	  doorpcolorclass2 := mColorClass2List[i];
    doorpcolorclass2.bktype := '';
    doorpcolorclass2.color := '';
    doorpcolorclass2.bkcolor1 := '';
    doorpcolorclass2.bkcolor2 := '';
    doorpcolorclass2.bkcolor3 := '';
    doorpcolorclass2.bkcolor4 := '';
    dispose(doorpcolorclass2);
  end;
  mColorClass2List.Clear;

  for i := 0 to mShutterExpList.Count - 1 do
  begin
	  pshutterexp := mShutterExpList[i];
    pshutterexp.paneltype := '';
    dispose(pshutterexp);
  end;
  mShutterExpList.Clear;


  for i := 0 to mWJBomList.Count - 1 do
  begin
	  pwjbom := mWJBomList[i];
    pwjbom.name := '';
    dispose(pwjbom);
  end;
  mWJBomList.Clear;

  for i := 0 to mWJBomDetailList.Count - 1 do
  begin
	  pwjbomdetail := mWJBomDetailList[i];
    pwjbomdetail.bomname := '';
    pwjbomdetail.name := '';
    pwjbomdetail.l := '';
    pwjbomdetail.d := '';
    pwjbomdetail.num := '';
    pwjbomdetail.opendirect := '';
    pwjbomdetail.bktype := '';
    dispose(pwjbomdetail);
  end;
  mWJBomDetailList.Clear;

  for i := 0 to mDoorPanelBomDetailList.Count - 1 do
  begin
	  ppbdetail := mDoorPanelBomDetailList[i];
    ppbdetail.bomclass := '';
    ppbdetail.bomname := '';
    ppbdetail.l := '';
    ppbdetail.w := '';
    ppbdetail.h := '';
    ppbdetail.mat := '';
    ppbdetail.color := '';
    ppbdetail.bomtype := '';
    ppbdetail.memo := '';
    ppbdetail.bdfile := '';
    dispose(ppbdetail);
  end;
  mDoorPanelBomDetailList.Clear;

  for i := 0 to mDoorXMLList.Count - 1 do
  begin
	  pxml := mDoorXMLList[i];
    pxml.name := '';
    pxml.xml := '';
    dispose(pxml);
  end;
  mDoorXMLList.Clear;

  for i := 0 to bomlist.Count - 1 do
  begin
    poi:= bomlist[i];
    poi.code:='';
    poi.name:='';
    poi.mat:='';
    poi.mat2:='';
    poi.mat3:='';
    poi.color:='';
    poi.workflow:='';
    poi.tmp_soz:='';
    poi.desc:='';
    poi.bomdes:='';
    poi.bomwjdes:='';
    poi.bomstddes:='';
    poi.childbom:='';
    poi.myclass:='';
    poi.nodename:='';
    poi.linecalc:='';
    poi.bomstd:='';
    poi.bg:='';

    poi.holestr:='';
    poi.kcstr:='';

    poi.memo:='';
    poi.gno:='';
    poi.gdes:='';
    poi.gcb:='';
    poi.extra:='';
    poi.bomdes:='';
    poi.fbstr:='';
    poi.subspace:='';
    poi.process:='';
    poi.ls:='';
    poi.myunit:='';
    poi.bomtype:='';
    poi.bdxmlid:='';
    poi.user_fbstr:='';

    for j := 0 to 15 do
    begin
    poi.var_names[j] := '';
    end;
    poi.a_hole_info:='';
    poi.b_hole_info:='';
    poi.holeinfo:='';

    poi.outputtype:='';
    poi.holeconfig_flag:='';
    poi.kcconig_flag:='';
    poi.bg_data:='';
    poi.mBGParam:='';

    poi.bg_filename:='';
    poi.mpr_filename:='';
    poi.bpp_filename:='';
    poi.devcode:='';

    poi.extend:='';
    poi.group:='';
    poi.packno:='';
    poi.userdefine:='';
    poi.erpunit:='';

    poi.erpmatcode:='';
    poi.blockmemo:='';
    poi.number_text:='';
    dispose(poi);
  end;
  bomlist.Clear;

  SlidingObjList.O['掩门,掩门'] :=nil;
  SlidingObjList.O['趟门,趟门'] :=nil;
end;

procedure TLocalObject.UninitSlidingAndDoorList;
var
  pcolor            : PSlidingColor;
  pexp              : PSlidingExp;
  pstype            : PSlidingType;
  psp               : PSlidingParam;
  ptrack            : PTrackParam;
  pudbox            : PUDBoxParam;
  phbox             : PHBoxParam;
  pvbox             : PVBoxParam;
  pnltype           : PPanelType;
  pa                : PAccessory;
  pcolorclass       : PSlidingColorClass;
  pcolorclass2      : PSlidingColorClass2;
  i,j                 : Integer;
  pgroup            : ^SlidingMyClassGroup;
  pbom              : PSlidingWjBom;
  pbomdetail        : PSlidingWjBomDetail;
  pssexp            : PSlidingShutterExp;
  pnlbomdetail      :PSlidingPanelBomDetail;
  hfg3 : PSlidingHfg2;
  hfg4 : PSlidingHfg2;
  hfg2 : PSlidingHfg2;
  sfg2 : PSlidingHfg2;
  sfg3 : PSlidingHfg2;
  sfg4 : PSlidingHfg2;
  opa:  POptionalAcc;

  pdoorcolor            : PDoorsColor;
  pdoorexp              : PDoorsExp;
  ptype             : PDoorsType;
  pparam            : PDoorsParam;
  php               : PDoorHBoxParam;
  ppt               : PDoorPanelType;
  doorpa                : PDoorAccessory;
  doorpcolorclass       : PDoorsColorClass;
  pshutterexp       : PDoorsShutterExp;
  pwjbom            : PDoorsWjBom;
  pwjbomdetail      : PDoorsWjBomDetail;
  pprice            : PDoorsPrice;
  phandle           : PDoorsHandle;
  phinge            : PDoorsHinge;
  pcurhinge         : PDoorsCurHinge;
  tmp               : TADOQuery;
  id                : Integer;
  doorpcolorclass2      : PDoorsColorClass2;
  ppbdetail:    PDoorsPanelBomDetail;
  pxml:PDoorXML;
  cfg : PCfgTable;
  poi : PBomOrderItem;
begin
  for i := 0 to mSlidingExpList.Count - 1 do
  begin
    pexp := mSlidingExpList[i];
	  pexp.name := '';
    dispose(pexp);
  end;
  mSlidingExpList.Clear;
  FreeAndNil(mSlidingExpList);

  for i := 0 to mSlidingTypeList.Count - 1 do
  begin
    pstype := mSlidingTypeList[i];
	  pstype.name := '';
    dispose(pstype);
  end;
  mSlidingTypeList.Clear;
  FreeAndNil(mSlidingTypeList);

  for i := 0 to mSlidingParamList.Count - 1 do
  begin
    psp := mSlidingParamList[i];
	  psp.name := '';
	  psp.myclass := '';
	  psp.vboxtype := '';
	  psp.wjname := '';
	  psp.track := '';
	  psp.udbox := '';
	  psp.hbox := '';
	  psp.zndlun := '';
	  psp.ddlun := '';
	  psp.diaolun := '';
	  psp.gddwlun := '';
	  psp.hddwlun := '';
	  psp.ls := '';
	  psp.memo := '';
    dispose(psp);
  end;
  mSlidingParamList.Clear;
  FreeAndNil(mSlidingParamList);

  for i := 0 to mHBoxParamList.Count - 1 do
  begin
    phbox := mHBoxParamList[i];
	  phbox.name := '';
	  phbox.wlcode := '';
	  phbox.bjcode := '';
	  phbox.wjname := '';
	  phbox.model := '';
	  phbox.memo := '';
	  phbox.bdfile := '';
    dispose(phbox);
  end;
  mHBoxParamList.Clear;
  FreeAndNil(mHBoxParamList);

  for i := 0 to mTrackParamList.Count - 1 do
  begin
    ptrack := mTrackParamList[i];
	  ptrack.name := '';
	  ptrack.wlupcode := '';
	  ptrack.wldncode := '';
	  ptrack.upname := '';
	  ptrack.dnname := '';
	  ptrack.wjname1 := '';
	  ptrack.wjname2 := '';
	  ptrack.upmodel := '';
	  ptrack.dnmodel := '';
	  ptrack.upmemo := '';
	  ptrack.dnmemo := '';
	  ptrack.upbdfile := '';
	  ptrack.dnbdfile := '';
    dispose(ptrack);
  end;
  mTrackParamList.Clear;
  FreeAndNil(mTrackParamList);

  for i := 0 to mUDBoxParamList.Count - 1 do
  begin
    pudbox := mUDBoxParamList[i];
	  pudbox.name := '';
	  pudbox.wlupcode := '';
	  pudbox.wldncode := '';
	  pudbox.upname := '';
	  pudbox.dnname := '';
	  pudbox.wjname1 := '';
	  pudbox.wjname2 := '';
	  pudbox.upmodel := '';
	  pudbox.dnmodel := '';
	  pudbox.upmemo := '';
	  pudbox.dnmemo := '';
	  pudbox.upbdfile := '';
	  pudbox.dnbdfile := '';
    dispose(pudbox);
  end;
  mUDBoxParamList.Clear;
  FreeAndNil(mUDBoxParamList);

  for i := 0 to mVBoxParamList.Count - 1 do
  begin
    pvbox := mVBoxParamList[i];
	  pvbox.name := '';
	  pvbox.wlcode := '';
	  pvbox.wjname := '';
	  pvbox.model := '';
	  pvbox.memo := '';
	  pvbox.bdfile := '';
    dispose(pvbox);
  end;
  mVBoxParamList.Clear;
  FreeAndNil(mVBoxParamList);

  for i := 0 to mSlidingColorList.Count - 1 do
  begin
    pcolor := mSlidingColorList[i];
	  pcolor.name := '';
	  pcolor.myclass := '';
	  pcolor.code := '';
    dispose(pcolor);
  end;
  mSlidingColorList.Clear;
  FreeAndNil(mSlidingColorList);

  for i := 0 to mPanelTypeList.Count - 1 do
  begin
    pnltype := mPanelTypeList[i];
	  pnltype.name := '';
	  pnltype.wjname := '';
	  pnltype.bktype := '';
	  pnltype.direct := '';
	  pnltype.pnl2d := '';
	  pnltype.slave := '';
	  pnltype.slave2 := '';
	  pnltype.mk3d := '';
	  pnltype.memo := '';
	  pnltype.memo2 := '';
	  pnltype.memo3 := '';
	  pnltype.bdfile := '';
    dispose(pnltype);
  end;
  mPanelTypeList.Clear;
  FreeAndNil(mPanelTypeList);

  for i := 0 to mSlidingAccessoryList.Count - 1 do
  begin
    pa := mSlidingAccessoryList[i];
	  pa.name := '';
	  pa.myunit := '';
	  pa.wlcode := '';
	  pa.myclass := '';
	  pa.color := '';
	  pa.memo := '';
	  pa.memo2 := '';
	  pa.memo3 := '';
	  pa.bdfile := '';
    dispose(pa);
  end;
  mSlidingAccessoryList.Clear;
  FreeAndNil(mSlidingAccessoryList);

  for i := 0 to mSlidingColorClassList.Count - 1 do
  begin
    pcolorclass := mSlidingColorClassList[i];
	  pcolorclass.color := '';
	  pcolorclass.myclass := '';
	  pcolorclass.mat := '';
	  pcolorclass.color2 := '';
	  pcolorclass.wlcode := '';
	  pcolorclass.bjcode := '';
	  pcolorclass.color3 := '';
	  pcolorclass.color4 := '';
	  pcolorclass.skcolor1 := '';
	  pcolorclass.skcolor2 := '';
	  pcolorclass.skcolor3 := '';
	  pcolorclass.skcolor4 := '';
    dispose(pcolorclass);
  end;
  mSlidingColorClassList.Clear;
  FreeAndNil(mSlidingColorClassList);

  for i := 0 to mSSExpList.Count - 1 do
  begin
    pssexp := mSSExpList[i];
	  pssexp.PanelType := '';
    dispose(pssexp);
  end;
  mSSExpList.Clear;
  FreeAndNil(mSSExpList);
  
  for i := 0 to mSlidingColorClass2List.Count - 1 do
  begin
	  pcolorclass2 := mSlidingColorClass2List[i];
    pcolorclass2.bktype := '';
    pcolorclass2.color := '';
    dispose(pcolorclass2);
  end;
  mSlidingColorClass2List.Clear;
  FreeAndNil(mSlidingColorClass2List);

  for i := 0 to mSlidingMyClassGroupList.Count - 1 do
  begin
    pgroup := mSlidingMyClassGroupList[i];
	  pgroup.name := '';
    dispose(pgroup);
  end;
  mSlidingMyClassGroupList.Clear;
  FreeAndNil(mSlidingMyClassGroupList);

  for i := 0 to mSlidingWjBomList.Count - 1 do
  begin
    pbom := mSlidingWjBomList[i];
	  pbom.name := '';
    dispose(pbom);
  end;
  mSlidingWjBomList.Clear;
  FreeAndNil(mSlidingWjBomList);

  for i := 0 to mSlidingWjBomDetailList.Count - 1 do
  begin
    pbomdetail := mSlidingWjBomDetailList[i];
	  pbomdetail.bomname := '';
	  pbomdetail.name := '';
	  pbomdetail.l := '';
	  pbomdetail.d := '';
	  pbomdetail.num := '';
	  pbomdetail.bdfile := '';
    dispose(pbomdetail);
  end;
  mSlidingWjBomDetailList.Clear;
  FreeAndNil(mSlidingWjBomDetailList);

  for i := 0 to mPanelBomDetailList.Count - 1 do
  begin
	  pnlbomdetail := mPanelBomDetailList[i];
    pnlbomdetail.bomclass := '';
    pnlbomdetail.bomname := '';
    pnlbomdetail.l := '';
    pnlbomdetail.w := '';
    pnlbomdetail.h := '';
    pnlbomdetail.mat := '';
    pnlbomdetail.color := '';
    pnlbomdetail.bomtype := '';
    pnlbomdetail.memo := '';
    pnlbomdetail.memo2 := '';
    pnlbomdetail.memo3 := '';
    pnlbomdetail.bdfile := '';
    dispose(pnlbomdetail);
  end;
  mPanelBomDetailList.Clear;
  FreeAndNil(mPanelBomDetailList);
  //门转换表
  for i := 0 to mCfglist.Count - 1 do
  begin
	  cfg := mCfglist[i];
    cfg.name := '';
    cfg.frametype := '';
    cfg.bomname := '';
    cfg.munit := '';
    dispose(cfg);
  end;
  mCfglist.Clear;
  FreeAndNil(mCfglist);

  //自选配件
  for i := 0 to OptionalAccList.Count - 1 do
  begin
    opa := OptionalAccList[i];
	  opa.name := '';
    dispose(opa);
  end;
  OptionalAccList.Clear;
  FreeAndNil(OptionalAccList);

  //趟门2横分格
  for i := 0 to SlidingHfg2List.Count - 1 do
  begin
    hfg2 := SlidingHfg2List[i];
	  hfg2.fgtype := '';
    hfg2.spszh := '';
    hfg2.spmk := '';
    hfg2.varlist := '';
    hfg2.mxlist := '';
    hfg2.image := '';
    dispose(hfg2);
  end;
  SlidingHfg2List.Clear;
  FreeAndNil(SlidingHfg2List);

  //趟门3横分格
  for i := 0 to SlidingHfg3List.Count - 1 do
  begin
    hfg3 := SlidingHfg3List[i];
	  hfg3.fgtype := '';
    hfg3.spszh := '';
    hfg3.varlist := '';
    hfg3.mxlist := '';
    hfg3.image := '';
    dispose(hfg3);
  end;
  SlidingHfg3List.Clear;
  FreeAndNil(SlidingHfg3List);

  //趟门4横分格
  for i := 0 to SlidingHfg4List.Count - 1 do
  begin
    hfg4 := SlidingHfg4List[i];
	  hfg4.fgtype := '';
    hfg4.spszh := '';
    hfg4.varlist := '';
    hfg4.mxlist := '';
    hfg4.image := '';
    dispose(hfg4);
  end;
  SlidingHfg4List.Clear;
  FreeAndNil(SlidingHfg4List);

  //趟门2竖分格
  for i := 0 to SlidingSfg2List.Count - 1 do
  begin
    Sfg2 := SlidingSfg2List[i];
	  Sfg2.fgtype := '';
    Sfg2.spszh := '';
    Sfg2.varlist := '';
    Sfg2.mxlist := '';
    Sfg2.image := '';
    dispose(Sfg2);
  end;
  SlidingSfg2List.Clear;
  FreeAndNil(SlidingSfg2List);

  //趟门3竖分格
  for i := 0 to SlidingSfg3List.Count - 1 do
  begin
    Sfg3 := SlidingSfg3List[i];
	  Sfg3.fgtype := '';
    Sfg3.spszh := '';
    Sfg3.varlist := '';
    Sfg3.mxlist := '';
    Sfg3.image := '';
    dispose(Sfg3);
  end;
  SlidingSfg3List.Clear;
  FreeAndNil(SlidingSfg3List);

  //趟门4竖分格
  for i := 0 to SlidingSfg4List.Count - 1 do
  begin
    Sfg4 := SlidingSfg4List[i];
	  Sfg4.fgtype := '';
    Sfg4.spszh := '';
    Sfg4.varlist := '';
    Sfg4.mxlist := '';
    Sfg4.image := '';
    dispose(Sfg4);
  end;
  SlidingSfg4List.Clear;
  FreeAndNil(SlidingSfg4List);

  //横中横
  for i := 0 to HSHBoxParamList.Count - 1 do
  begin
    phbox := HSHBoxParamList[i];
    phbox.name := '';
    phbox.wlcode := '';
    phbox.bjcode := '';
    phbox.wjname := '';
    phbox.model := '';
    phbox.memo := '';
    phbox.bdfile := '';
    phbox.frametype := '';
    dispose(phbox);
  end;
  HSHBoxParamList.Clear;
  FreeAndNil(HSHBoxParamList);

  //竖中横
  for i := 0 to SHBoxParamList.Count - 1 do
  begin
    phbox := SHBoxParamList[i];
    phbox.name := '';
    phbox.wlcode := '';
    phbox.bjcode := '';
    phbox.wjname := '';
    phbox.model := '';
    phbox.memo := '';
    phbox.bdfile := '';
    phbox.frametype := '';
    dispose(phbox);
  end;
  SHBoxParamList.Clear;
  FreeAndNil(SHBoxParamList);

  bomdeslist.Clear;
  bomdeslist.Free;

  doordeslist.Clear;
  doordeslist.Free;

  slidingdeslist.Clear;
  slidingdeslist.Free;

  //掩门
  for i := 0 to mColorList.Count - 1 do
  begin
	  pdoorcolor := mColorList[i];
    pdoorcolor.name := '';
    dispose(pdoorcolor);
  end;
  mColorList.Clear;
  FreeAndNil(mColorList);

  for i := 0 to mExpList.Count - 1 do
  begin
	  pdoorexp := mExpList[i];
    pdoorexp.name := '';
    dispose(pdoorexp);
  end;
  mExpList.Clear;
  FreeAndNil(mExpList);

  for i := 0 to mTypeList.Count - 1 do
  begin
	  ptype := mTypeList[i];
    ptype.name := '';
    ptype.hinge := '';
    ptype.myclass := '';
    ptype.hinge1 := '';
    ptype.hinge2 := '';
    dispose(ptype);
  end;
  mTypeList.Clear;
  FreeAndNil(mTypeList);

  for i := 0 to mParamList.Count - 1 do
  begin
	  pparam := mParamList[i];
    pparam.name := '';
    pparam.DoorsType := '';
    pparam.handle := '';
    pparam.wjname := '';
    pparam.hboxname := '';
    pparam.paneltype := '';
    pparam.vboxname := '';
    pparam.udboxname := '';
    pparam.vboxl := '';
    pparam.udboxl := '';
    pparam.d3name := '';
    pparam.hbox3d := '';
    pparam.ubox3d := '';
    pparam.dbox3d := '';
    pparam.vdirect := '';
    pparam.vfbstr := '';
    pparam.uddirect := '';
    pparam.udfbstr := '';
    pparam.vmemo := '';
    pparam.udmemo := '';
    pparam.fbstr := '';
    pparam.bomtype := '';
    pparam.left_doorxml := '';
    pparam.right_doorxml := '';
    pparam.doorxml := '';
    pparam.bdfile := '';
    pparam.l_bdfile := '';
    pparam.r_bdfile := '';
    pparam.u_bdfile := '';
    pparam.d_bdfile := '';
    dispose(pparam);
  end;
  mParamList.Clear;
  FreeAndNil(mParamList);

  for i := 0 to mHandleList.Count - 1 do
  begin
	  phandle := mHandleList[i];
    phandle.name := '';
    phandle.wjname := '';
    phandle.xpos := '';
    phandle.ypos := '';
    phandle.width := '';
    phandle.height := '';
    phandle.depth := '';
    phandle.depthpos := '';
    phandle.bomtype := '';
    phandle.memo := '';
    phandle.holescript := '';
    dispose(phandle);
  end;
  mHandleList.Clear;
  FreeAndNil(mHandleList);

  for i := 0 to mHingeList.Count - 1 do
  begin
	  phinge := mHingeList[i];
    phinge.name := '';
    phinge.mytype := '';
    phinge.wjname := '';
    phinge.bomtype := '';
    phinge.memo := '';
    phinge.alias := '';
    dispose(phinge);
  end;
  mHingeList.Clear;
  FreeAndNil(mHingeList);

  for i := 0 to mCurHingeList.Count - 1 do
  begin
	  pcurhinge := mCurHingeList[i];
    pcurhinge.name := '';
    pcurhinge.wjname := '';
    pcurhinge.bomtype := '';
    pcurhinge.memo := '';
    pcurhinge.hingetype:='';
    pcurhinge.installtype:='';
    dispose(pcurhinge);
  end;
  mCurHingeList.Clear;
  FreeAndNil(mCurHingeList);

  for i := 0 to mDoorHBoxParamList.Count - 1 do
  begin
	  php := mDoorHBoxParamList[i];
    php.name := '';
    php.wjname := '';
    php.bomtype := '';
    php.memo := '';
    php.direct := '';
    php.fbstr := '';
    php.model := '';
    php.bdfile := '';
    dispose(php);
  end;
  mDoorHBoxParamList.Clear;
  FreeAndNil(mDoorHBoxParamList);

  for i := 0 to mDoorPanelTypeList.Count - 1 do
  begin
	  ppt := mDoorPanelTypeList[i];
    ppt.name := '';
    ppt.mytype := '';
    ppt.bomtype := '';
    ppt.bktype := '';
    ppt.direct := '';
    ppt.fbstr := '';
    ppt.pnl3d := '';
    ppt.memo := '';
    ppt.panelbom := '';
    ppt.memo2 := '';
    ppt.memo3 := '';
    ppt.bdfile := '';
    dispose(ppt);
  end;
  mDoorPanelTypeList.Clear;
  FreeAndNil(mDoorPanelTypeList);

  for i := 0 to mAccessoryList.Count - 1 do
  begin
	  doorpa := mAccessoryList[i];
    doorpa.name := '';
    doorpa.myunit := '';
    doorpa.mytype := '';
    doorpa.bomtype := '';
    doorpa.color := '';
    doorpa.memo := '';
    doorpa.bdfile := '';
    dispose(doorpa);
  end;
  mAccessoryList.Clear;
  FreeAndNil(mAccessoryList);

  for i := 0 to mColorClassList.Count - 1 do
  begin
	  doorpcolorclass := mColorClassList[i];
    doorpcolorclass.color := '';
    doorpcolorclass.myclass := '';
    doorpcolorclass.mat := '';
    doorpcolorclass.color2 := '';
    doorpcolorclass.color3 := '';
    doorpcolorclass.color4 := '';
    dispose(doorpcolorclass);
  end;
  mColorClassList.Clear;
  FreeAndNil(mColorClassList);

  for i := 0 to mColorClass2List.Count - 1 do
  begin
	  doorpcolorclass2 := mColorClass2List[i];
    doorpcolorclass2.bktype := '';
    doorpcolorclass2.color := '';
    doorpcolorclass2.bkcolor1 := '';
    doorpcolorclass2.bkcolor2 := '';
    doorpcolorclass2.bkcolor3 := '';
    doorpcolorclass2.bkcolor4 := '';
    dispose(doorpcolorclass2);
  end;
  mColorClass2List.Clear;
  FreeAndNil(mColorClass2List);

  for i := 0 to mShutterExpList.Count - 1 do
  begin
	  pshutterexp := mShutterExpList[i];
    pshutterexp.paneltype := '';
    dispose(pshutterexp);
  end;
  mShutterExpList.Clear;
  FreeAndNil(mShutterExpList);

  for i := 0 to mWJBomList.Count - 1 do
  begin
	  pwjbom := mWJBomList[i];
    pwjbom.name := '';
    dispose(pwjbom);
  end;
  mWJBomList.Clear;
  FreeAndNil(mWJBomList);

  for i := 0 to mWJBomDetailList.Count - 1 do
  begin
	  pwjbomdetail := mWJBomDetailList[i];
    pwjbomdetail.bomname := '';
    pwjbomdetail.name := '';
    pwjbomdetail.l := '';
    pwjbomdetail.d := '';
    pwjbomdetail.num := '';
    pwjbomdetail.opendirect := '';
    pwjbomdetail.bktype := '';
    dispose(pwjbomdetail);
  end;
  mWJBomDetailList.Clear;
  FreeAndNil(mWJBomDetailList);
  
  for i := 0 to mDoorPanelBomDetailList.Count - 1 do
  begin
	  ppbdetail := mDoorPanelBomDetailList[i];
    ppbdetail.bomclass := '';
    ppbdetail.bomname := '';
    ppbdetail.l := '';
    ppbdetail.w := '';
    ppbdetail.h := '';
    ppbdetail.mat := '';
    ppbdetail.color := '';
    ppbdetail.bomtype := '';
    ppbdetail.memo := '';
    ppbdetail.bdfile := '';
    dispose(ppbdetail);
  end;
  mDoorPanelBomDetailList.Clear;
  FreeAndNil(mDoorPanelBomDetailList);

  for i := 0 to mDoorXMLList.Count - 1 do
  begin
	  pxml := mDoorXMLList[i];
    pxml.name := '';
    pxml.xml := '';
    dispose(pxml);
  end;
  mDoorXMLList.Clear;
  FreeAndNil(mDoorXMLList);

  for i := 0 to bomlist.Count - 1 do
  begin
    poi:= bomlist[i];
    poi.code:='';
    poi.name:='';
    poi.mat:='';
    poi.mat2:='';
    poi.mat3:='';
    poi.color:='';
    poi.workflow:='';
    poi.tmp_soz:='';
    poi.desc:='';
    poi.bomdes:='';
    poi.bomwjdes:='';
    poi.bomstddes:='';
    poi.childbom:='';
    poi.myclass:='';
    poi.nodename:='';
    poi.linecalc:='';
    poi.bomstd:='';
    poi.bg:='';

    poi.holestr:='';
    poi.kcstr:='';

    poi.memo:='';
    poi.gno:='';
    poi.gdes:='';
    poi.gcb:='';
    poi.extra:='';
    poi.bomdes:='';
    poi.fbstr:='';
    poi.subspace:='';
    poi.process:='';
    poi.ls:='';
    poi.myunit:='';
    poi.bomtype:='';
    poi.bdxmlid:='';
    poi.user_fbstr:='';

    for j := 0 to 15 do
    begin
    poi.var_names[j] := '';
    end;
    poi.a_hole_info:='';
    poi.b_hole_info:='';
    poi.holeinfo:='';

    poi.outputtype:='';
    poi.holeconfig_flag:='';
    poi.kcconig_flag:='';
    poi.bg_data:='';
    poi.mBGParam:='';

    poi.bg_filename:='';
    poi.mpr_filename:='';
    poi.bpp_filename:='';
    poi.devcode:='';

    poi.extend:='';
    poi.group:='';
    poi.packno:='';
    poi.userdefine:='';
    poi.erpunit:='';

    poi.erpmatcode:='';
    poi.blockmemo:='';
    poi.number_text:='';
    dispose(poi);
  end;
  bomlist.Clear;
  FreeAndNil(bomlist);
  
  SlidingObjList:=nil;
  SfgParam := nil;

end;

function TLocalObject.GetSlidingExp(name: string): PSlidingExp;
var
  p                 : PSlidingExp;
  i                 : Integer;
begin
  Result := nil;
  for i := 0 to mSlidingExpList.Count - 1 do
  begin
    p := mSlidingExpList[i];
    if p.name = name then
    begin
      Result := p;
    end;
  end;
end;

function TLocalObject.GetSlidingParam(name: string): PSlidingParam;
var
  p                 : PSlidingParam;
  i                 : Integer;
begin
  Result := nil;
  for i := 0 to mSlidingParamList.Count - 1 do
  begin
    p := mSlidingParamList[i];
    if p.name = name then
    begin
      Result := p;
    end;
  end;
end;

function TLocalObject.GetSlidingType(name: string): PSlidingType;
var
  p                 : PSlidingType;
  i                 : Integer;
begin
  Result := nil;
  for i := 0 to mSlidingTypeList.Count - 1 do
  begin
    p := mSlidingTypeList[i];
    if p.name = name then
    begin
      Result := p;
    end;
  end;
end;

function TLocalObject.GetTrackParam(name: string): PTrackParam;
var
  p                 : PTrackParam;
  i                 : Integer;
begin
  Result := nil;
  for i := 0 to mTrackParamList.Count - 1 do
  begin
    p := mTrackParamList[i];
    if p.name = name then
    begin
      Result := p;
    end;
  end;
end;

function TLocalObject.GetUDBoxParam(name: string): PUDBoxParam;
var
  p                 : PUDBoxParam;
  i                 : Integer;
begin
  Result := nil;
  for i := 0 to mUDBoxParamList.Count - 1 do
  begin
    p := mUDBoxParamList[i];
    if p.name = name then
    begin
      Result := p;
    end;
  end;
end;

function TLocalObject.GetHBoxParam(name: string; nType: Integer =0): PHBoxParam;
var
  p                 : PHBoxParam;
  i                 : Integer;
begin
  //ntype = 1 竖中横 SHBoxParam； ntype = 2 横中横 HSHBoxParamList
  Result := nil;
  if nType = 1 then
  begin
    for i := 0 to HSHBoxParamList.Count - 1 do
    begin
      p := HSHBoxParamList[i];
      if p.name = name then
      begin
        Result := p;
      end;
    end;
  end
  else if (nType = 2) then
  begin
    for i := 0 to SHBoxParamList.Count - 1 do
    begin
      p := SHBoxParamList[i];
      if p.name = name then
      begin
        Result := p;
      end;
    end;
  end
  else
  begin
    for i := 0 to mHBoxParamList.Count - 1 do
    begin
      p := mHBoxParamList[i];
      if p.name = name then
      begin
        Result := p;
      end;
    end;
  end;
end;

function TLocalObject.GetVBoxParam(name: string): PVBoxParam;
var
  p                 : PVBoxParam;
  i                 : Integer;
begin
  Result := nil;
  for i := 0 to mVBoxParamList.Count - 1 do
  begin
    p := mVBoxParamList[i];
    if p.name = name then
    begin
      Result := p;
    end;
  end;
end;

{ TDoorDoorRect }

procedure TDoorDoorRect.ClearBoxList;
var
  i                 : Integer;
  p                 : PDoorRectBox;
begin
  for i := 0 to boxlist.Count - 1 do
  begin
    p := boxlist[i];
	  p.boxtype := '';
	  p.color := '';
    dispose(p);
  end;
  boxlist.Clear;
end;

procedure TDoorDoorRect.ClearPanelList;
var
  i                 : Integer;
  p                 : PDoorRectPanel;
begin
  for i := 0 to panellist.Count - 1 do
  begin
    p := panellist[i];
	  p.PanelType := '';
	  p.color := '';
	  p.direct := '';
	  p.pricetype := '';
	  p.color2 := '';
    dispose(p);
  end;
  panellist.Clear;
end;

procedure TDoorDoorRect.CopyFromDoor(door: TDoorDoorRect);
var
  i                 : Integer;
  box1, box2        : PDoorRectBox;
  pnl1, pnl2        : PDoorRectPanel;
begin
  self.ClearBoxList;
  self.ClearPanelList;
  self.mUDBoxH := door.mUDBoxH;
  self.mPParam := door.mPParam;
  self.mVBoxW := door.mVBoxW;

  self.mPanelType := door.mPanelType;
  self.mPanelColor := door.mPanelColor;
  self.mHandle := door.mHandle;
  self.mHandlePos := door.mHandlePos;
  if (door.mOpenDirect = '左') or (door.mOpenDirect = '右') then
  begin
    self.mHandlePosY := door.mHandlePosY;
    self.mHandleY := door.mHandleY;
  end;
  if (door.mOpenDirect = '上') or (door.mOpenDirect = '下') then
  begin
    self.mHandlePosX := door.mHandlePosX;
    self.mHandleX := door.mHandleX;
  end;
  for i := 0 to door.boxlist.Count - 1 do
  begin
    box1 := door.boxlist[i];
    new(box2);
    box2.vh := box1.vh;
    box2.selected := False;
    box2.w0 := box1.w0;
    box2.h0 := box1.h0;
    box2.x0 := box1.x0 + self.x0 - door.x0;
    box2.y0 := box1.y0;
    box2.d0 := box1.d0;
    box2.w1 := box1.w1;
    box2.h1 := box1.h1;
    box2.x1 := box1.x1 + self.x0 - door.x0;
    box2.y1 := box1.y1;
    box2.d1 := box1.d1;
    box2.w2 := box1.w2;
    box2.h2 := box1.h2;
    box2.x2 := box1.x2 + self.x0 - door.x0;
    box2.y2 := box1.y2;
    box2.d2 := box1.d2;
    box2.boxtype := box1.boxtype;
    box2.color := box1.color;
    self.boxlist.Add(box2);
  end;
  for i := 0 to door.panellist.Count - 1 do
  begin
    pnl1 := door.panellist[i];
    new(pnl2);
    pnl2.selected := False;
    pnl2.x0 := pnl1.x0 + self.x0 - door.x0;
    pnl2.y0 := pnl1.y0;
    pnl2.w0 := pnl1.w0;
    pnl2.h0 := pnl1.h0;
    pnl2.d0 := pnl1.d0;
    pnl2.x1 := pnl1.x1 + self.x0 - door.x0;
    pnl2.y1 := pnl1.y1;
    pnl2.w1 := pnl1.w1;
    pnl2.h1 := pnl1.h1;
    pnl2.d1 := pnl1.d1;
    pnl2.x2 := pnl1.x2 + self.x0 - door.x0;
    pnl2.y2 := pnl1.y2;
    pnl2.w2 := pnl1.w2;
    pnl2.h2 := pnl1.h2;
    pnl2.d2 := pnl1.d2;
    pnl2.PanelType := pnl1.PanelType;
    pnl2.color := pnl1.color;
    pnl2.direct := pnl1.direct;
    self.panellist.Add(pnl2);
  end;
end;

function TDoorDoorRect.GetSelectedPanel: PDoorRectPanel;
var
  i                 : Integer;
  p                 : PDoorRectPanel;
begin
  Result := nil;
  for i := 0 to panellist.Count - 1 do
  begin
    p := panellist[i];
    if p.selected then
      Result := p;
  end;
end;

function TDoorDoorRect.GetVboxKCInfo: string;
var d0, d1, h0, i:Integer;
pnl               : PDoorRectPanel;
begin
  Result := '';
  d0 := 0;
  d1 := 0;
  h0 := 0;
  for i := 0 to panellist.Count - 1 do
  begin
    pnl := panellist[i];
    if d0=0 then
    begin
      d0 := pnl.thick;
      h0 := Round(pnl.h0);
    end else if (d1=0) and (pnl.thick<>d0) then
    begin
      d1 := pnl.thick;
    end;
  end;
  if (d0>0) and (d1>0) and (d0<>d1) then
  begin
    Result := Format('%d*%d_%d', [h0, d0, d1]);
  end else
  if d0>0 then
  begin
    Result := Format('%d*%d', [h0, d0]);
  end;
end;

function TDoorDoorRect.GetHboxKCInfo(n: Integer; p: PDoorRectBox): string;
var
pnl, pnl1               : PDoorRectPanel;
begin
  Result := '';
  if (n=0) and (panellist.Count>0) then//下横框
  begin
    pnl := panellist[0];
    Result := Format('%d', [pnl.thick]);
  end;
  if (n=1) and (p<>nil) and (panellist.Count>0) then//中横框
  begin
    pnl := GetNearestDownPanel(p);
    pnl1 := GetNearestUpPanel(p);
    if (pnl<>nil) and (pnl1<>nil) then
    begin
      Result := Format('%d_%d', [pnl.thick, pnl1.thick]);
    end;
  end;
  if (n=2) and (panellist.Count>0) then//上横框
  begin
    pnl := panellist[panellist.Count-1];
    Result := Format('%d', [pnl.thick]);
  end;
end;

function TDoorDoorRect.GetNearestDownBox(p: PDoorRectPanel): PDoorRectBox;
var
  i                 : Integer;
  rb                : PDoorRectBox;
  t                 : single;
begin
  Result := nil;
  t := self.doorh;
  for i := 0 to boxlist.Count - 1 do
  begin
    rb := boxlist[i];
    if ((p.y0 + p.h0 - rb.y0) > 0) and ((p.y0 + p.h0 - rb.y0) < t) then
    begin
      t := (p.y0 + p.h0 - rb.y0);
      Result := rb;
    end;
  end;
end;

function TDoorDoorRect.GetNearestDownPanel(p: PDoorRectBox): PDoorRectPanel;
var
  i                 : Integer;
  pnl               : PDoorRectPanel;
  t                 : single;
begin
  Result := nil;
  t := self.doorh;
  for i := 0 to panellist.Count - 1 do
  begin
    pnl := panellist[i];
    if ((p.y0 + p.h0 - pnl.y0) > 0) and ((p.y0 + p.h0 - pnl.y0) < t) then
    begin
      t := (p.y0 + p.h0 - pnl.y0);
      Result := pnl;
    end;
  end;
end;

function TDoorDoorRect.GetNearestDownPanel(p: PDoorRectPanel): PDoorRectPanel;
var
  i                 : Integer;
  pnl               : PDoorRectPanel;
  t                 : single;
begin
  Result := nil;
  t := self.doorh;
  for i := 0 to panellist.Count - 1 do
  begin
    pnl := panellist[i];
    if p = pnl then continue;
    if ((p.y0 + p.h0 - pnl.y0) > 0) and ((p.y0 + p.h0 - pnl.y0) < t) then
    begin
      t := (p.y0 + p.h0 - pnl.y0);
      Result := pnl;
    end;
  end;
end;

function TDoorDoorRect.GetNearestUpBox(p: PDoorRectPanel): PDoorRectBox;
var
  i                 : Integer;
  rb                : PDoorRectBox;
  t                 : single;
begin
  Result := nil;
  t := self.doorh;
  for i := 0 to boxlist.Count - 1 do
  begin
    rb := boxlist[i];
    if ((rb.y0 - p.y0) > 0) and ((rb.y0 - p.y0) < t) then
    begin
      t := (rb.y0 - p.y0);
      Result := rb;
    end;
  end;
end;

function TDoorDoorRect.GetNearestUpPanel(p: PDoorRectPanel): PDoorRectPanel;
var
  i                 : Integer;
  pnl               : PDoorRectPanel;
  t                 : single;
begin
  Result := nil;
  t := self.doorh;
  for i := 0 to panellist.Count - 1 do
  begin
    pnl := panellist[i];
    if p = pnl then continue;
    if ((pnl.y0 - p.y0) > 0) and ((pnl.y0 - p.y0) < t) then
    begin
      t := (pnl.y0 - p.y0);
      Result := pnl;
    end;
  end;
end;

function TDoorDoorRect.GetNearestUpPanel(p: PDoorRectBox): PDoorRectPanel;
var
  i                 : Integer;
  pnl               : PDoorRectPanel;
  t                 : single;
begin
  Result := nil;
  t := self.doorh;
  for i := 0 to panellist.Count - 1 do
  begin
    pnl := panellist[i];
    if ((pnl.y0 - p.y0) > 0) and ((pnl.y0 - p.y0) < t) then
    begin
      t := (pnl.y0 - p.y0);
      Result := pnl;
    end;
  end;
end;

function TDoorDoorRect.GetPanelPosInDoor(p: PDoorRectPanel): Integer;
var
  i                 : Integer;
  pnl               : PDoorRectPanel;
  b1, b2            : boolean;
begin
  Result := -1;
  b1 := False;
  b2 := False;
  for i := 0 to panellist.Count - 1 do
  begin
    pnl := panellist[i];
    if pnl = p then continue;
    if pnl.y1 > p.y1 then
      b1 := True;
    if pnl.y1 < p.y1 then
      b2 := True;
  end;
  if b1 then Result := 1;               //上格有面板
  if b2 then Result := 2;               //下格有面板
  if (b1) and (b2) then
    Result := 0;
end;

constructor TDoorDoorRect.Create;
var i:Integer;
begin
  boxlist := TList.Create;
  panellist := TList.Create;
  mHandleX := -1;
  mHandleY := -1;
  mHandleW := -1;
  mHandleH := -1;
  mPParam := nil;
  SetLength(mHHArr, 0);
end;

procedure TDoorDoorRect.UnselecetAllPanels;
var
  i                 : Integer;
  p                 : PDoorRectPanel;
begin
  for i := 0 to panellist.Count - 1 do
  begin
    p := panellist[i];
    p.selected := False;
  end;
end;

function TDoorDoorRect.SelectPanelByPos(x0, y0: single;
  multisel: boolean): PDoorRectPanel;
var
  i                 : Integer;
  p                 : PDoorRectPanel;
begin
  Result := nil;
  for i := 0 to panellist.Count - 1 do
  begin
    p := panellist[i];
    if not multisel then
      p.selected := False;
    if (p.x0 < x0) and (p.x0 + p.w0 > x0) and (p.y0 < y0) and (p.y0 + p.h0 > y0) then
    begin
      p.selected := True;
      Result := p;
    end;
  end;
end;

function TDoorDoorRect.SelectRectBoxByPos(x0, y0: single): PDoorRectBox;
var
  i                 : Integer;
  p                 : PDoorRectBox;
begin
  Result := nil;
  for i := 0 to boxlist.Count - 1 do
  begin
    p := boxlist[i];
    p.selected := False;
    if (p.x0 < x0) and (p.x0 + p.w0 > x0) and (p.y0 < y0) and (p.y0 + p.h0 > y0) then
    begin
      p.selected := True;
      Result := p;
    end;
  end;
end;

procedure TDoorDoorRect.CreateHBoxAndPanel(boxtype, boxcolor, pnltype,
  pnlcolor: string; num: Integer; h, d, thick: single; hh: array of single;
  pnls1, pnls2, di: array of string);
var
  i                 : Integer;
  p                 : PDoorRectBox;
  Y                 : single;
  panel             : PDoorRectPanel;
begin
  ClearBoxList;
  ClearPanelList;

  Y := self.y0 + mPParam.udthick + hh[0];
  for i := 0 to num - 2 do
  begin
    new(p);
    p.vh := True;
    p.selected := False;
    p.w0 := self.doorw - (self.mVBoxW * 2);
    p.w1 := self.doorw - (mPParam.vthick * 2);
    p.w2 := self.doorw;
    p.d0 := d;
    p.d1 := d;
    p.d2 := d;
    p.h0 := h;
    p.h1 := thick;
    p.h2 := 0;
    p.x0 := self.x0 + (self.mVBoxW);
    p.x1 := self.x0 + (mPParam.vthick);
    p.x2 := self.x0;
    //计算过桥y位置
    p.y1 := Y;
    p.y0 := Y - (h - thick) / 2;
    p.y2 := Y + thick / 2;
    Y := Y + hh[i + 1] + thick;
    p.boxtype := boxtype;
    p.color := boxcolor;
    boxlist.Add(p);
  end;
  if num = 1 then                       //单格面板
  begin
    new(panel);
    panel.selected := False;
    panel.w0 := self.doorw - (self.mVBoxW * 2);
    panel.w1 := self.doorw - (mPParam.vthick * 2);
    panel.w2 := self.doorw;
    panel.d0 := d;
    panel.d1 := d;
    panel.d2 := d;
    panel.h0 := doorh - self.mUDBoxH * 2;
    panel.h1 := doorh - mPParam.udthick * 2;
    panel.h2 := doorh;

    panel.x0 := self.x0 + (self.mVBoxW);
    panel.x1 := self.x0 + (mPParam.vthick);
    panel.x2 := self.x0;
    panel.y0 := self.y0 + self.mUDBoxH;
    panel.y1 := self.y0 + mPParam.udthick;
    panel.y2 := self.y0;

    panel.PanelType := pnls1[0];
    panel.color := pnls2[0];
    panel.direct := di[0];
    panellist.Add(panel);
  end;
  if num > 1 then                       //多格面板
  begin
    Y := self.y0 + mPParam.udthick;
    for i := 0 to num - 1 do
    begin
      new(panel);
      panel.selected := False;
      panel.w0 := self.doorw - (self.mVBoxW * 2);
      panel.w1 := self.doorw - (mPParam.vthick * 2);
      panel.w2 := self.doorw;
      panel.d0 := d;
      panel.d1 := d;
      panel.d2 := d;
      panel.h0 := hh[i];
      panel.h1 := hh[i];
      panel.h2 := hh[i];
      if i = 0 then
      begin
        panel.h0 := hh[i] - (self.mUDBoxH - mPParam.udthick) - (h - thick) / 2;
        panel.h2 := hh[i] + (mPParam.udthick) + (thick) / 2;
      end
      else if i = num - 1 then
      begin
        panel.h0 := hh[i] - (self.mUDBoxH - mPParam.udthick) - (h - thick) / 2;
        panel.h2 := hh[i] + (mPParam.udthick) + (thick) / 2;
      end
      else
      begin
        panel.h0 := hh[i] - (h - thick);
        panel.h2 := hh[i] + thick;
      end;
      panel.x0 := self.x0 + (self.mVBoxW);
      panel.x1 := self.x0 + (mPParam.vthick);
      panel.x2 := self.x0;
      //计算面板y位置
      if i = 0 then
      begin
        panel.y0 := self.y0 + self.mUDBoxH;
        panel.y1 := self.y0 + mPParam.udthick;
        panel.y2 := self.y0;
      end
      else
      begin
        panel.y0 := Y + (h - thick) / 2;
        panel.y1 := Y;
      end;
      Y := Y + hh[i] + thick;
      panel.PanelType := pnls1[i];
      panel.color := pnls2[i];
      panel.direct := di[i];
      panellist.Add(panel);
    end;
  end;
end;

destructor TDoorDoorRect.Destroy;
begin
  ClearBoxList;
  ClearPanelList;
  FreeAndNil(boxlist);
  FreeAndNil(panellist);
  SetLength(mHHArr, 0);
  inherited;
end;
//掩门
function TLocalObject.GetDoorsExp(name: string): PDoorsExp;
var
  p                 : PDoorsExp;
  i                 : Integer;
begin
  Result := nil;
  for i := 0 to mExpList.Count - 1 do
  begin
    p := mExpList[i];
    if p.name = name then
    begin
      Result := p;
      break;
    end;
  end;
end;
//掩门
function TLocalObject.GetDoorsParam(name1, name2: string): PDoorsParam;
var
  p                 : PDoorsParam;
  i                 : Integer;
begin
  Result := nil;
  for i := 0 to mParamList.Count - 1 do
  begin
    p := mParamList[i];
    if (p.name = name2) and (p.DoorsType = name1) then
    begin
      Result := p;
      break;
    end;
  end;
end;
//掩门
function TLocalObject.GetDoorsType(name: string): PDoorsType;
var
  p                 : PDoorsType;
  i                 : Integer;
begin
  Result := nil;
  for i := 0 to mTypeList.Count - 1 do
  begin
    p := mTypeList[i];
    if p.name = name then
    begin
      Result := p;
      break;
    end;
  end;
end;

function TLocalObject.GetDoorsHandle(name: string): PDoorsHandle;
var
  i                 : Integer;
  p                 : PDoorsHandle;
begin
  Result := nil;
  if name = '' then exit;
  for i := 0 to mHandleList.Count - 1 do
  begin
    p := mHandleList[i];
    if p.name = name then
    begin
      Result := p;
      break;
    end;
  end;
end;
//门铰
function TLocalObject.GetDoorsCurHinge(mj, mHinge: string): PDoorsCurHinge;
var
  i                 : Integer;
  p                 : PDoorsCurHinge;
begin
  Result := nil;
  if mj = '' then exit;

  for i := 0 to mCurHingeList.Count - 1 do
  begin
    p := mCurHingeList[i];
    if (p.name = mj) then
    begin
      if (p.hingetype = mHinge ) then
      begin
        Result := p;
        break;
      end;
    end;
  end;
end;
//门铰分类
function TLocalObject.GetDoorsHinge(mj: string; dt:PDoorsType): PDoorsHinge;
var
  i                 : Integer;
  p                 : PDoorsHinge;
begin
  Result := nil;
  if dt=nil then exit;
  if mj = '' then exit;

  for i := 0 to mHingeList.Count - 1 do
  begin
    p := mHingeList[i];
    if (p.name = mj) then
    begin
      Result := p;
      break;
    end;
  end;
end;

//掩门
function TLocalObject.GetDoorHBoxParam(name: string): PDoorHBoxParam;
var
  p                 : PDoorHBoxParam;
  i                 : Integer;
begin
  Result := nil;
  for i := 0 to mDoorHBoxParamList.Count - 1 do
  begin
    p := mDoorHBoxParamList[i];
    if p.name = name then
    begin
      Result := p;
    end;
  end;
end;
//掩门
function TLocalObject.GetDoorPanelType(bktype, name: string): PDoorPanelType;
var
  p                 : PDoorPanelType;
  i                 : Integer;
begin
  Result := nil;
  for i := 0 to mDoorPanelTypeList.Count - 1 do
  begin
    p := mDoorPanelTypeList[i];
    if (p.name = name) and (p.bktype = '*') then
    begin
      Result := p;
      exit;
    end;
    if (p.name = name) and (p.bktype = bktype) then
    begin
      Result := p;
      exit;
    end;
  end;
end;
//掩门
function TLocalObject.GetColorClass(myclass,
  color: string): PDoorsColorClass;
var
  i                 : Integer;
  p                 : PDoorsColorClass;
begin
  Result := nil;
  for i := 0 to mColorClassList.Count - 1 do
  begin
    p := mColorClassList[i];
    if (p.myclass = myclass) and (p.color = color) then
    begin
      Result := p;
      break;
    end;
  end;
end;

function TLocalObject.GetAccessory(name: string): PAccessory;
var
  p                 : PAccessory;
  i                 : Integer;
begin
  Result := nil;
  for i := 0 to mSlidingAccessoryList.Count - 1 do
  begin
    p := mSlidingAccessoryList[i];
    if p.name = name then
    begin
      Result := p;
    end;
  end;
end;

//趟门 重新计算门
procedure TLocalObject.RecalcDoor(door: TDoorRect; t1, t2, hh:single);
var j:Integer;
rb                : PRectBox;
  pnl               : PRectPanel;
begin
{    if mGridItem=1 then t1 := hh;     //两均分，下格固定
    if mGridItem=2 then t1 := hh/2;   //三均分，中间格固定
    if mGridItem=5 then t1 := hh;     //======
    if mGridItem=6 then t1 := hh/2;   //两均分，上格固定
    if mGridItem=7 then t1 := hh;   //三均分(上两格固定)
    if mGridItem=8 then t1 := hh;   //三均分(下两格固定)    }

  if (mGridItem=6) and (door.panellist.Count=2) then   //两均分(下格固定)
  begin
    t2 := hh;
    for j:=0 to door.boxlist.Count-1 do
    begin
      rb := door.boxlist[j];
      rb.y0 := rb.y0 + t2*(0+0);
      rb.y1 := rb.y1 + t2*(0+0);
      rb.y2 := rb.y2 + t2*(0+0);
    end;
    for j:=0 to door.panellist.Count-1 do
    begin
      pnl := door.panellist[j];
      if j=1 then
      begin
        pnl.h0 := pnl.h0 + t2;
        pnl.y0 := pnl.y0;
        pnl.h1 := pnl.h1 + t2;
        pnl.y1 := pnl.y1;
        pnl.h2 := pnl.h2 + t2;
        pnl.y2 := pnl.y2;
      end;
    end;
  end
  else if (mGridItem=7) and (door.panellist.Count=2) then  //两均分，上格固定
  begin
    t2 := hh;
    for j:=0 to door.boxlist.Count-1 do
    begin
      rb := door.boxlist[j];
      rb.y0 := rb.y0 + t2*(0+1);
      rb.y1 := rb.y1 + t2*(0+1);
      rb.y2 := rb.y2 + t2*(0+1);
    end;
    for j:=0 to door.panellist.Count-1 do
    begin
      pnl := door.panellist[j];
      if j=1 then
      begin
        pnl.h0 := pnl.h0;
        pnl.y0 := pnl.y0 + t2;
        pnl.h1 := pnl.h1;
        pnl.y1 := pnl.y1 + t2;
        pnl.h2 := pnl.h2;
        pnl.y2 := pnl.y2 + t2;
      end else if j=0 then
      begin
        pnl.h0 := pnl.h0 + t2;
        pnl.y0 := pnl.y0;
        pnl.h1 := pnl.h1 + t2;
        pnl.y1 := pnl.y1;
        pnl.h2 := pnl.h2 + t2;
        pnl.y2 := pnl.y2;
     end;
    end;
  end
  else if (mGridItem=8) and (door.panellist.Count=3) then  //三格，中间格固定
  begin
    t2 := hh/2;
    for j:=0 to door.boxlist.Count-1 do
    begin
      rb := door.boxlist[j];
      rb.y0 := rb.y0 + t2*(0+1);
      rb.y1 := rb.y1 + t2*(0+1);
      rb.y2 := rb.y2 + t2*(0+1);
    end;
    for j:=0 to door.panellist.Count-1 do
    begin
      pnl := door.panellist[j];
      if j=1 then
      begin
        pnl.h0 := pnl.h0;
        pnl.y0 := pnl.y0 + t2;
        pnl.h1 := pnl.h1;
        pnl.y1 := pnl.y1 + t2;
        pnl.h2 := pnl.h2;
        pnl.y2 := pnl.y2 + t2;
      end else if j=0 then
      begin
        pnl.h0 := pnl.h0 + t2;
        pnl.y0 := pnl.y0;
        pnl.h1 := pnl.h1 + t2;
        pnl.y1 := pnl.y1;
        pnl.h2 := pnl.h2 + t2;
        pnl.y2 := pnl.y2;
      end else if j=2 then
      begin
        pnl.h0 := pnl.h0 + t2;
        pnl.y0 := pnl.y0 + t2;
        pnl.h1 := pnl.h1 + t2;
        pnl.y1 := pnl.y1 + t2;
        pnl.h2 := pnl.h2 + t2;
        pnl.y2 := pnl.y2 + t2;
      end;
    end;
  end
  else if (mGridItem=9) and (door.panellist.Count=3) then  //三均分(上两格固定)
  begin
    t2 := hh;
    for j:=0 to door.boxlist.Count-1 do
    begin
      rb := door.boxlist[j];
      rb.y0 := rb.y0 + t2*(0+1);
      rb.y1 := rb.y1 + t2*(0+1);
      rb.y2 := rb.y2 + t2*(0+1);
    end;
    for j:=0 to door.panellist.Count-1 do
    begin
      pnl := door.panellist[j];
      if j>0 then
      begin
        pnl.h0 := pnl.h0;
        pnl.y0 := pnl.y0 + t2;
        pnl.h1 := pnl.h1;
        pnl.y1 := pnl.y1 + t2;
        pnl.h2 := pnl.h2;
        pnl.y2 := pnl.y2 + t2;
      end else if j=0 then
      begin
        pnl.h0 := pnl.h0 + t2;
        pnl.y0 := pnl.y0;
        pnl.h1 := pnl.h1 + t2;
        pnl.y1 := pnl.y1;
        pnl.h2 := pnl.h2 + t2;
        pnl.y2 := pnl.y2;
      end;
    end;
  end
  else if (mGridItem=10) and (door.panellist.Count=3) then  //三均分(下两格固定)    }
  begin
    t2 := hh;
    for j:=0 to door.boxlist.Count-1 do
    begin
      rb := door.boxlist[j];
      rb.y0 := rb.y0 + t2*(0+0);
      rb.y1 := rb.y1 + t2*(0+0);
      rb.y2 := rb.y2 + t2*(0+0);
    end;
    for j:=0 to door.panellist.Count-1 do
    begin
      pnl := door.panellist[j];
      if j>1 then
      begin
        pnl.h0 := pnl.h0 + t2;
        pnl.y0 := pnl.y0;
        pnl.h1 := pnl.h1 + t2;
        pnl.y1 := pnl.y1;
        pnl.h2 := pnl.h2 + t2;
        pnl.y2 := pnl.y2;
      end else if j=0 then
      begin
        pnl.h0 := pnl.h0;
        pnl.y0 := pnl.y0;
        pnl.h1 := pnl.h1;
        pnl.y1 := pnl.y1;
        pnl.h2 := pnl.h2;
        pnl.y2 := pnl.y2;
      end;
    end;
  end else begin
    t2 := hh/(door.panellist.Count);
    for j:=0 to door.boxlist.Count-1 do
    begin
        rb := door.boxlist[j];
        rb.y0 := rb.y0 + t2*(j+1);
        rb.y1 := rb.y1 + t2*(j+1);
        rb.y2 := rb.y2 + t2*(j+1);
    end;
    for j:=0 to door.panellist.Count-1 do
    begin
        pnl := door.panellist[j];
        pnl.h0 := pnl.h0 + t2;
        pnl.y0 := pnl.y0 + t2*j;
        pnl.h1 := pnl.h1 + t2;
        pnl.y1 := pnl.y1 + t2*j;
        pnl.h2 := pnl.h2 + t2;
        pnl.y2 := pnl.y2 + t2*j;
    end;
  end;
end;

procedure TLocalObject.Copy(p1, p2: Pointer; name: string);
var
  pcolor1, pcolor2  : PSlidingColor;
  pexp1, pexp2      : PSlidingExp;
  pstype1, pstype2  : PSlidingType;
  psp1, psp2        : PSlidingParam;
  ptrack1, ptrack2  : PTrackParam;
  pudbox1, pudbox2  : PUDBoxParam;
  phbox1, phbox2    : PHBoxParam;
  pvbox1, pvbox2    : PVBoxParam;
begin
  if name = 'SlidingColor' then
  begin
    pcolor1 := p2;
    pcolor2 := p1;
    pcolor1.name := pcolor2.name;
    pcolor1.myclass := pcolor2.myclass;
    pcolor1.code := pcolor2.code;
    pcolor1^ := pcolor2^;
  end;
  if name = 'SlidingExp' then
  begin
    pexp1 := p2;
    pexp2 := p1;
    pexp1.name := pexp2.name;
    pexp1.doornum := pexp2.doornum;
    pexp1.overlapnum := pexp2.overlapnum;
    pexp1.lkvalue := pexp2.lkvalue;
    pexp1.noexp := pexp2.noexp;
    pexp1^ := pexp2^;
  end;
  if name = 'SlidingType' then
  begin
    pstype1 := p2;
    pstype2 := p1;
    pstype1.name := pstype2.name;
    pstype1^ := pstype2^;
  end;
  if name = 'SlidingParam' then
  begin
    psp1 := p2;
    psp2 := p1;
    psp1.name := psp2.name;
    psp1.myclass := psp2.myclass;
    psp1.vboxtype := psp2.vboxtype;
    psp1.overlap := psp2.overlap;
    psp1.ddlw := psp2.ddlw;
    psp1.fztlen := psp2.fztlen;
    psp1.glassvalue1 := psp2.glassvalue1;
    psp1.glassvalue2 := psp2.glassvalue2;
    psp1.track := psp2.track;
    psp1.udbox := psp2.udbox;
    psp1.zndlun := psp2.zndlun;
    psp1.ddlun := psp2.ddlun;
    psp1.diaolun := psp2.diaolun;
    psp1.gddwlun := psp2.gddwlun;
    psp1.hddwlun := psp2.hddwlun;
    psp1.ls := psp2.ls;
    psp1.hbox := psp2.hbox;
    psp1.wjname := psp2.wjname;
    psp1.vboxjtw := psp2.vboxjtw;
    psp1.uboxjtw := psp2.uboxjtw;
    psp1.dboxjtw := psp2.dboxjtw;
    psp1.hboxjtw := psp2.hboxjtw;
    psp1.laminating := psp2.laminating;
    psp1.cpm_lmax := psp2.cpm_lmax;
    psp1.cpm_hmax := psp2.cpm_hmax;
    psp1.is_xq := psp2.is_xq;
    psp1^ := psp2^;
  end;
  if name = 'TrackParam' then
  begin
    ptrack1 := p2;
    ptrack2 := p1;
    ptrack1.name := ptrack2.name;
    ptrack1.height := ptrack2.height;
    ptrack1.depth := ptrack2.depth;
    ptrack1.lkvalue1 := ptrack2.lkvalue1;
    ptrack1.lkvalue2 := ptrack2.lkvalue2;
    ptrack1.wlupcode := ptrack2.wlupcode;
    ptrack1.wldncode := ptrack2.wldncode;
    ptrack1.upname := ptrack2.upname;
    ptrack1.dnname := ptrack2.dnname;
    ptrack1.wjname1 := ptrack2.wjname1;
    ptrack1.wjname2 := ptrack2.wjname2;
    ptrack1.upsize := ptrack2.upsize;
    ptrack1.downsize := ptrack2.downsize;
    ptrack1.upmodel := ptrack2.upmodel;
    ptrack1.dnmodel := ptrack2.dnmodel;
    ptrack1.upmemo := ptrack2.upmemo;
    ptrack1.dnmemo := ptrack2.dnmemo;
    ptrack1^ := ptrack2^;
  end;
  if name = 'UDBoxParam' then
  begin
    pudbox1 := p2;
    pudbox2 := p1;
    pudbox1.name := pudbox2.name;
    pudbox1.ubheight := pudbox2.ubheight;
    pudbox1.ubdepth := pudbox2.ubdepth;
    pudbox1.ubthick := pudbox2.ubthick;
    pudbox1.dbheight := pudbox2.dbheight;
    pudbox1.dbdepth := pudbox2.dbdepth;
    pudbox1.dbthick := pudbox2.dbthick;
    pudbox1.wlupcode := pudbox2.wlupcode;
    pudbox1.wldncode := pudbox2.wldncode;
    pudbox1.upname := pudbox2.upname;
    pudbox1.dnname := pudbox2.dnname;
    pudbox1.wjname1 := pudbox2.wjname1;
    pudbox1.wjname2 := pudbox2.wjname2;
    pudbox1.uphole := pudbox2.uphole;
    pudbox1.downhole := pudbox2.downhole;
    pudbox1.upsize := pudbox2.upsize;
    pudbox1.downsize := pudbox2.downsize;
    pudbox1.upmodel := pudbox2.upmodel;
    pudbox1.dnmodel := pudbox2.dnmodel;
    pudbox1.upmemo := pudbox2.upmemo;
    pudbox1.dnmemo := pudbox2.dnmemo;
    pudbox1^ := pudbox2^;
  end;
  if name = 'HBoxParam' then
  begin
    phbox1 := p2;
    phbox2 := p1;
    phbox1.name := phbox2.name;
    phbox1.height := phbox2.height;
    phbox1.depth := phbox2.depth;
    phbox1.thick := phbox2.thick;
    phbox1.wlcode := phbox2.wlcode;
    phbox1.bjcode := phbox2.bjcode;
    phbox1.wjname := phbox2.wjname;
    phbox1.hole := phbox2.hole;
    phbox1.size := phbox2.size;
    phbox1.model := phbox2.model;
    phbox1.memo := phbox2.memo;
    phbox1^ := phbox2^;
  end;
  if name = 'VBoxParam' then
  begin
    pvbox1 := p2;
    pvbox2 := p1;
    pvbox1.name := pvbox2.name;
    pvbox1.height := pvbox2.height;
    pvbox1.depth := pvbox2.depth;
    pvbox1.thick := pvbox2.thick;
    pvbox1.panelvalue := pvbox2.panelvalue;
    pvbox1.wlcode := pvbox2.wlcode;
    pvbox1.wjname := pvbox2.wjname;
    pvbox1.udboxvalue := pvbox2.udboxvalue;
    pvbox1.vboxvalue := pvbox2.vboxvalue;
    pvbox1.size := pvbox2.size;
    pvbox1.model := pvbox2.model;
    pvbox1.memo := pvbox2.memo;
    pvbox1^ := pvbox2^;
  end;
end;

function TLocalObject.GetPanelType(bktype, name: string): PPanelType;
var
  p                 : PPanelType;
  i                 : Integer;
begin
  Result := nil;
  for i := 0 to mPanelTypeList.Count - 1 do
  begin
    p := mPanelTypeList[i];
    if (p.name = name) and (p.bktype = '*') then
    begin
      Result := p;
      exit;
    end;
    if (p.name = name) and (p.bktype = bktype) then
    begin
      Result := p;
      exit;
    end;
  end;
end;

function TLocalObject.GetSSExp(name: string): PSlidingShutterExp;
var
  p                 : PSlidingShutterExp;
  i                 : Integer;
begin
  Result := nil;
  for i := 0 to mSSExpList.Count - 1 do
  begin
    p := mSSExpList[i];
    if p.PanelType = name then
    begin
      Result := p;
    end;
  end;
end;

function TLocalObject.GetDoorYPos(n, doornum,
  overlapnum: Integer): Integer;
begin
  Result := 0;
  if doornum = 1 then
  begin
    Result := 0;
  end;
  if (doornum = 2) then
  begin
    if n = 1 then
      Result := 50;
  end;
  if (doornum = 3) then
  begin
    if (n = 0) or (n = 2) then
      Result := 50;
  end;
  if (doornum = 4) then
  begin
    if overlapnum = 2 then
    begin
      if (n = 1) or (n = 2) then
        Result := 50;
    end;
    if overlapnum = 3 then
    begin
      if (n = 1) or (n = 3) then
        Result := 50;
    end;
  end;
  if doornum = 5 then
  begin
    if overlapnum = 4 then
    begin
      if (n = 1) or (n = 3) then
        Result := 50;
    end;
  end;
  if doornum = 6 then
  begin
    if (n = 0) or (n = 2) or (n = 4) then
      Result := 50;
  end;
  if doornum = 7 then
  begin
    if (n = 0) or (n = 3) or (n = 6) then
      Result := 50;
  end;
  if doornum = 8 then
  begin
    if (n = 0) or (n = 3) or (n = 4) or (n = 7) then
      Result := 50;
  end;
end;

function SortRectBoxByY(Item1, Item2: Pointer): Integer;
var
  p1, p2            : PRectBox;
begin
  p1 := Item1;
  p2 := Item2;
  Result := 0;
  if p1.y0 > p2.y0 then
    Result := 1;
  if p1.y0 < p2.y0 then
    Result := -1;
end;

function SortRectPanelByY(Item1, Item2: Pointer): Integer;
var
  p1, p2            : PRectPanel;
begin
  p1 := Item1;
  p2 := Item2;
  Result := 0;
  if p1.y0 > p2.y0 then
    Result := 1;
  if p1.y0 < p2.y0 then
    Result := -1;
end;

{ TDoorRect }

procedure TDoorRect.AddHBoxToPanel(pnl: PRectPanel; hbox: PHBoxParam; x0, y0: single; boxcolor: string);
var
  p                 : PRectPanel;
  pbox              : PRectBox;
begin
  new(pbox);
  pbox.vh := True;
  pbox.selected := False;
  pbox.w0 := self.doorw - (mVBoxParam.height * 2);
  pbox.w1 := self.doorw - (mVBoxParam.thick * 2);
  pbox.w2 := self.doorw;
  pbox.d0 := hbox.depth;
  pbox.d1 := hbox.depth;
  pbox.d2 := hbox.depth;
  pbox.h0 := hbox.height;
  pbox.h1 := hbox.thick;
  pbox.h2 := 0;
  pbox.x0 := self.x0 + (mVBoxParam.height);
  pbox.x1 := self.x0 + (mVBoxParam.thick);
  pbox.x2 := self.x0;
  //计算过桥y位置
  pbox.y1 := y0 - hbox.thick / 2;
  pbox.y0 := y0 - hbox.height / 2;
  pbox.y2 := y0;
  pbox.boxtype := hbox.name;
  pbox.color := boxcolor;
  boxlist.Add(pbox);

  new(p);
  p.selected := False;
  p.w0 := pnl.w0;
  p.h0 := pnl.h0;
  p.x0 := pnl.x0;
  p.y0 := pnl.y0;
  p.d0 := pnl.d0;
  p.w1 := pnl.w1;
  p.h1 := pnl.h1;
  p.x1 := pnl.x1;
  p.y1 := pnl.y1;
  p.d1 := pnl.d1;
  p.w2 := pnl.w2;
  p.h2 := pnl.h2;
  p.x2 := pnl.x2;
  p.y2 := pnl.y2;
  p.d2 := pnl.d2;
  p.PanelType := pnl.PanelType;
  p.color := pnl.color;
  p.direct := pnl.direct;
  self.panellist.Add(p);

  pnl.h0 := y0 - hbox.height / 2 - pnl.y0;
  pnl.h1 := y0 - hbox.thick / 2 - pnl.y1;
  pnl.h2 := y0 - pnl.y2;

  p.y0 := pnl.y0 + pnl.h0 + hbox.height;
  p.y1 := pnl.y1 + pnl.h1 + hbox.thick;
  p.y2 := pnl.y2 + pnl.h2;
  p.h0 := p.h0 - pnl.h0 - hbox.height;
  p.h1 := p.h1 - pnl.h1 - hbox.thick;
  p.h2 := p.h2 - pnl.h2;
end;

procedure TDoorRect.ClearBoxList;
var
  i                 : Integer;
  p                 : PRectBox;
begin
  for i := 0 to boxlist.Count - 1 do
  begin
    p := boxlist[i];
	  p.boxtype := '';
    p.color := '';
    dispose(p);
  end;
  boxlist.Clear;
end;

procedure TDoorRect.ClearPanelList;
var
  i                 : Integer;
  p                 : PRectPanel;
begin
  for i := 0 to panellist.Count - 1 do
  begin
    p := panellist[i];
    p.PanelType := '';
    p.color := '';
    p.direct := '';
    p.memo := '';
    p.pricetype := '';
    p.color2 := '';
    p.extradata := '';
    dispose(p);
  end;
  panellist.Clear;
end;

procedure TDoorRect.CopyFromDoor(door: TDoorRect);
var
  i                 : Integer;
  box1, box2        : PRectBox;
  pnl1, pnl2        : PRectPanel;
begin
  self.ClearBoxList;
  self.ClearPanelList;
  self.mUDBoxParam.name := door.mUDBoxParam.name;
  self.mUDBoxParam.ubheight := door.mUDBoxParam.ubheight;
  self.mUDBoxParam.ubdepth := door.mUDBoxParam.ubdepth;
  self.mUDBoxParam.ubthick := door.mUDBoxParam.ubthick;
  self.mUDBoxParam.dbheight := door.mUDBoxParam.dbheight;
  self.mUDBoxParam.dbdepth := door.mUDBoxParam.dbdepth;
  self.mUDBoxParam.dbthick := door.mUDBoxParam.dbthick;

  self.mVBoxParam.name := door.mVBoxParam.name;
  self.mVBoxParam.height := door.mVBoxParam.height;
  self.mVBoxParam.depth := door.mVBoxParam.depth;
  self.mVBoxParam.thick := door.mVBoxParam.thick;

  self.mPanelType := door.mPanelType;
  self.mPanelColor := door.mPanelColor;
  self.mVBoxColor := door.mVBoxColor;
  for i := 0 to door.boxlist.Count - 1 do
  begin
    box1 := door.boxlist[i];
    new(box2);
    box2.vh := box1.vh;
    box2.selected := False;
    box2.w0 := box1.w0;
    box2.h0 := box1.h0;
    box2.x0 := box1.x0 + self.x0 - door.x0;
    box2.y0 := box1.y0;
    box2.d0 := box1.d0;
    box2.w1 := box1.w1;
    box2.h1 := box1.h1;
    box2.x1 := box1.x1 + self.x0 - door.x0;
    box2.y1 := box1.y1;
    box2.d1 := box1.d1;
    box2.w2 := box1.w2;
    box2.h2 := box1.h2;
    box2.x2 := box1.x2 + self.x0 - door.x0;
    box2.y2 := box1.y2;
    box2.d2 := box1.d2;
    box2.boxtype := box1.boxtype;
    box2.color := box1.color;
    self.boxlist.Add(box2);
  end;
  for i := 0 to door.panellist.Count - 1 do
  begin
    pnl1 := door.panellist[i];
    new(pnl2);
    pnl2.selected := False;
    pnl2.x0 := pnl1.x0 + self.x0 - door.x0;
    pnl2.y0 := pnl1.y0;
    pnl2.w0 := pnl1.w0;
    pnl2.h0 := pnl1.h0;
    pnl2.d0 := pnl1.d0;
    pnl2.x1 := pnl1.x1 + self.x0 - door.x0;
    pnl2.y1 := pnl1.y1;
    pnl2.w1 := pnl1.w1;
    pnl2.h1 := pnl1.h1;
    pnl2.d1 := pnl1.d1;
    pnl2.x2 := pnl1.x2 + self.x0 - door.x0;
    pnl2.y2 := pnl1.y2;
    pnl2.w2 := pnl1.w2;
    pnl2.h2 := pnl1.h2;
    pnl2.d2 := pnl1.d2;
    pnl2.PanelType := pnl1.PanelType;
    pnl2.color := pnl1.color;
    pnl2.direct := pnl1.direct;
    self.panellist.Add(pnl2);
  end;
end;

constructor TDoorRect.Create;
begin
  boxlist := TList.Create;
  panellist := TList.Create;
end;

procedure TDoorRect.CreateHBoxAndPanel(boxtype, boxcolor, pnltype,
  pnlcolor: string; num: Integer; h, d, thick: single; hh: array of single;
  pnls1, pnls2, di, memo: array of string);
var
  i                 : Integer;
  p                 : PRectBox;
  y                 : single;
  panel             : PRectPanel;
begin
  ClearBoxList;
  ClearPanelList;

  y := mUDBoxParam.dbthick + hh[0];
  for i := 0 to num - 2 do
  begin
    new(p);
    p.vh := True;
    p.selected := False;
    p.w0 := self.doorw - (mVBoxParam.height * 2);
    p.w1 := self.doorw - (mVBoxParam.thick * 2);
    p.w2 := self.doorw2;
    p.d0 := d;
    p.d1 := d;
    p.d2 := d;
    p.h0 := h;
    p.h1 := thick;
    p.h2 := 0;
    p.x0 := self.x0 + (mVBoxParam.height);
    p.x1 := self.x0 + (mVBoxParam.thick);
    p.x2 := self.x0;
    //计算过桥y位置
    p.y1 := y;
    p.y0 := y - (h - thick) / 2;
    p.y2 := y + thick / 2;
    y := y + hh[i + 1] + thick;
    p.boxtype := boxtype;
    p.color := boxcolor;
    boxlist.Add(p);
  end;
  if num = 1 then                       //单格面板
  begin
    new(panel);
    panel.selected := False;
    panel.w0 := self.doorw - (mVBoxParam.height * 2);
    panel.w1 := self.doorw - (mVBoxParam.thick * 2);
    panel.w2 := self.doorw2;
    panel.d0 := d;
    panel.d1 := d;
    panel.d2 := d;
    panel.h0 := doorh - mVBoxParam.panelvalue - mUDBoxParam.ubheight - mUDBoxParam.dbheight;
    panel.h1 := doorh - mVBoxParam.panelvalue - mUDBoxParam.ubthick - mUDBoxParam.dbthick;
    panel.h2 := doorh2;

    panel.x0 := self.x0 + (mVBoxParam.height);
    panel.x1 := self.x0 + (mVBoxParam.thick);
    panel.x2 := self.x0;
    panel.y0 := mUDBoxParam.dbheight;
    panel.y1 := mUDBoxParam.dbthick;
    panel.y2 := 0;

    panel.PanelType := pnls1[0];
    panel.color := pnls2[0];
    panel.direct := di[0];
    panel.memo := memo[0];
    panellist.Add(panel);
  end;
  if num > 1 then                       //多格面板
  begin
    y := mUDBoxParam.dbthick;
    for i := 0 to num - 1 do
    begin
      new(panel);
      panel.selected := False;
      panel.w0 := self.doorw - (mVBoxParam.height * 2);
      panel.w1 := self.doorw - (mVBoxParam.thick * 2);
      panel.w2 := self.doorw2;
      panel.d0 := d;
      panel.d1 := d;
      panel.d2 := d;
      panel.h0 := hh[i];
      panel.h1 := hh[i];
      panel.h2 := hh[i];
      if i = 0 then
      begin
        panel.h0 := hh[i] - (mUDBoxParam.dbheight - mUDBoxParam.dbthick) - (h - thick) / 2;
        panel.h2 := hh[i] + (mUDBoxParam.dbthick) + (thick) / 2 + (doorh2 - doorh) / num; //顶底轮位均分到各个面板
      end
      else if i = num - 1 then
      begin
        panel.h0 := hh[i] - (mUDBoxParam.ubheight - mUDBoxParam.ubthick) - (h - thick) / 2;
        panel.h2 := hh[i] + (mUDBoxParam.ubthick) + (thick) / 2 + (doorh2 - doorh) / num; //顶底轮位均分到各个面板
      end
      else
      begin
        panel.h0 := hh[i] - (h - thick);
        panel.h2 := hh[i] + thick + (doorh2 - doorh) / num; //顶底轮位均分到各个面板
      end;
      panel.x0 := self.x0 + (mVBoxParam.height);
      panel.x1 := self.x0 + (mVBoxParam.thick);
      panel.x2 := self.x0;
      //计算面板y位置
      if i = 0 then
      begin
        panel.y0 := mUDBoxParam.dbheight;
        panel.y1 := mUDBoxParam.dbthick;
        panel.y2 := 0;
      end
      else
      begin
        panel.y0 := y + (h - thick) / 2;
        panel.y1 := y;
        panel.y2 := y - thick/2;
      end;
      y := y + hh[i] + thick;
      panel.PanelType := pnls1[i];
      panel.color := pnls2[i];
      panel.direct := di[i];
      panel.memo := memo[i];
      panellist.Add(panel);
    end;
  end;
end;

destructor TDoorRect.Destroy;
begin
  ClearBoxList;
  ClearPanelList;
  FreeAndNil(boxlist);
  FreeAndNil(panellist);
  inherited;
end;

function TDoorRect.GetNearestDownBox(p: PRectPanel): PRectBox;
var
  i                 : Integer;
  rb                : PRectBox;
  t                 : single;
begin
  Result := nil;
  t := self.doorh;
  for i := 0 to boxlist.Count - 1 do
  begin
    rb := boxlist[i];
    if ((p.y0 + p.h0 - rb.y0) > 0) and ((p.y0 + p.h0 - rb.y0) < t) then
    begin
      t := (p.y0 + p.h0 - rb.y0);
      Result := rb;
    end;
  end;
end;

function TDoorRect.GetNearestDownPanel(p: PRectPanel): PRectPanel;
var
  i                 : Integer;
  pnl               : PRectPanel;
  t                 : single;
begin
  Result := nil;
  t := self.doorh;
  for i := 0 to panellist.Count - 1 do
  begin
    pnl := panellist[i];
    if p = pnl then continue;
    if ((p.y0 + p.h0 - pnl.y0) > 0) and ((p.y0 + p.h0 - pnl.y0) < t) then
    begin
      t := (p.y0 + p.h0 - pnl.y0);
      Result := pnl;
    end;
  end;
end;

function TDoorRect.GetNearestDownPanel(p: PRectBox): PRectPanel;
var
  i                 : Integer;
  pnl               : PRectPanel;
  t                 : single;
begin
  Result := nil;
  t := self.doorh;
  for i := 0 to panellist.Count - 1 do
  begin
    pnl := panellist[i];
    if ((p.y0 + p.h0 - pnl.y0) > 0) and ((p.y0 + p.h0 - pnl.y0) < t) then
    begin
      t := (p.y0 + p.h0 - pnl.y0);
      Result := pnl;
    end;
  end;
end;

function TDoorRect.GetNearestUpPanel(p: PRectBox): PRectPanel;
var
  i                 : Integer;
  pnl               : PRectPanel;
  t                 : single;
begin
  Result := nil;
  t := self.doorh;
  for i := 0 to panellist.Count - 1 do
  begin
    pnl := panellist[i];
    if ((pnl.y0 - p.y0) > 0) and ((pnl.y0 - p.y0) < t) then
    begin
      t := (pnl.y0 - p.y0);
      Result := pnl;
    end;
  end;
end;

procedure TDoorRect.GetNearestRectBox(panel: PRectPanel; var boxup,
  boxdown: PRectBox);
var
  i                 : Integer;
  p                 : PRectBox;
begin
  boxup := nil;
  boxdown := nil;
  for i := 0 to boxlist.Count - 1 do
  begin
    p := boxlist[i];
    //面板之下
    if abs(p.y0 - panel.y1) < 3 then
    begin
      boxdown := p;
    end;
    //面板之上
    if abs(p.y0 - panel.h1 - panel.y1) < 3 then
    begin
      boxup := p;
    end;
  end;
end;

function TDoorRect.GetNearestUpBox(p: PRectPanel): PRectBox;
var
  i                 : Integer;
  rb                : PRectBox;
  t                 : single;
begin
  Result := nil;
  t := self.doorh;
  for i := 0 to boxlist.Count - 1 do
  begin
    rb := boxlist[i];
    if ((rb.y0 - p.y0) > 0) and ((rb.y0 - p.y0) < t) then
    begin
      t := (rb.y0 - p.y0);
      Result := rb;
    end;
  end;
end;

function TDoorRect.GetNearestUpPanel(p: PRectPanel): PRectPanel;
var
  i                 : Integer;
  pnl               : PRectPanel;
  t                 : single;
begin
  Result := nil;
  t := self.doorh;
  for i := 0 to panellist.Count - 1 do
  begin
    pnl := panellist[i];
    if p = pnl then continue;
    if ((pnl.y0 - p.y0) > 0) and ((pnl.y0 - p.y0) < t) then
    begin
      t := (pnl.y0 - p.y0);
      Result := pnl;
    end;
  end;
end;

function TDoorRect.GetPanelPosInDoor(p: PRectPanel): Integer;
var
  i                 : Integer;
  pnl               : PRectPanel;
  b1, b2            : boolean;
begin
  Result := -1;
  b1 := False;
  b2 := False;
  for i := 0 to panellist.Count - 1 do
  begin
    pnl := panellist[i];
    if pnl = p then continue;
    if pnl.y1 > p.y1 then
      b1 := True;
    if pnl.y1 < p.y1 then
      b2 := True;
  end;
  if b1 then Result := 1;               //上格有面板
  if b2 then Result := 2;               //下格有面板
  if (b1) and (b2) then
    Result := 0;
end;

function TDoorRect.GetSelectedPanel: PRectPanel;
var
  i                 : Integer;
  p                 : PRectPanel;
begin
  Result := nil;
  for i := 0 to panellist.Count - 1 do
  begin
    p := panellist[i];
    if p.selected then
      Result := p;
  end;
end;

function TDoorRect.SelectPanelByPos(x0, y0: single; multisel: boolean): PRectPanel;
var
  i                 : Integer;
  p                 : PRectPanel;
begin
  Result := nil;
  for i := 0 to panellist.Count - 1 do
  begin
    p := panellist[i];
    if not multisel then
      p.selected := False;
    if (p.x0 < x0) and (p.x0 + p.w0 > x0) and (p.y0 < y0) and (p.y0 + p.h0 > y0) then
    begin
      p.selected := True;
      Result := p;
    end;
  end;
end;

procedure TDoorRect.UnselecetAllPanels;
var
  i                 : Integer;
  p                 : PRectPanel;
begin
  for i := 0 to panellist.Count - 1 do
  begin
    p := panellist[i];
    p.selected := False;
  end;
end;

function TDoorRect.SelectRectBoxByPos(x0, y0: single): PRectBox;
var
  i                 : Integer;
  p                 : PRectBox;
begin
  Result := nil;
  for i := 0 to boxlist.Count - 1 do
  begin
    p := boxlist[i];
    p.selected := False;
    if (p.x0 < x0) and (p.x0 + p.w0 > x0) and (p.y0 < y0) and (p.y0 + p.h0 > y0) then
    begin
      p.selected := True;
      Result := p;
    end;
  end;
end;

procedure TLocalObject.LoadFromXMLTemplate(xml: string; l, h:Integer; resize: boolean);
var
  root, Node, cnode, cnode2, attri: IXMLNode;
  i, j, m              : Integer;
  door              : TDoorRect;
  rb                : PRectBox;
  pnl               : PRectPanel;
  ll, hh, t1, t2:single;

  pcolor            : PSlidingColor;
  pexp              : PSlidingExp;
  pstype            : PSlidingType;
  psp               : PSlidingParam;
  ptrack            : PTrackParam;
  pudbox            : PUDBoxParam;
  phbox             : PHBoxParam;
  pvbox             : PVBoxParam;
  pnltype           : PPanelType;
  pa                : PAccessory;
  pcolorclass       : PSlidingColorClass;
  opa:  POptionalAcc;
  xdoc:IXMLDocument;
begin
  mDoorsList.Clear;
  OptionalAccList.Clear;
  ll := 0;
  hh := 0;
  mAddLength := 0;            //延长导轨
  mDataMode := 0;             //
  mXML := xml;
  if xml = '' then exit;
  try
    //xdoc.XML.Clear;
    //xdoc.Active := True;
    //xdoc.Encoding := 'utf8';
    //xdoc.Version := '1.0';
    //xdoc.Active := True;
    //xdoc.xml.Add(xml);
    //xdoc.Active := True;
    xdoc := XMLDoc.LoadXMLData('<?xml version="1.0" encoding="gb2312"?>'+xml);
    root := xdoc.ChildNodes[1];
    attri := root.AttributeNodes.FindNode('门洞宽');
    if (attri <> nil) and (resize) then mL := StrToInt(attri.text);
    attri := root.AttributeNodes.FindNode('门洞高');
    if (attri <> nil) and (resize) then mH := StrToInt(attri.text);
    attri := root.AttributeNodes.FindNode('延长导轨');
    if (attri <> nil) and (attri.Text<>'') then mAddLength := StrToInt(attri.text);
    attri := root.AttributeNodes.FindNode('单门数量类型');
    if attri <> nil then pexp := GetSlidingExp(attri.text);
    attri := root.AttributeNodes.FindNode('门类型');
    if attri <> nil then pstype := GetSlidingType(attri.text);
    attri := root.AttributeNodes.FindNode('边框类型');
    if attri <> nil then psp := GetSlidingParam(attri.text);
    attri := root.AttributeNodes.FindNode('上下横框类型');
    if attri <> nil then pudbox := GetUDBoxParam(attri.text);
    attri := root.AttributeNodes.FindNode('上下轨类型');
    if attri <> nil then ptrack := GetTrackParam(attri.text);
    attri := root.AttributeNodes.FindNode('中横框类型');
    if attri <> nil then phbox := GetHBoxParam(attri.text);
    if psp <> nil then pvbox := GetVBoxParam(psp.vboxtype);
    attri := root.AttributeNodes.FindNode('门板类型');
    if attri <> nil then mMyPanelType := attri.text;
    attri := root.AttributeNodes.FindNode('门颜色');
    if attri <> nil then mMySlidingColor := attri.text;
    attri := root.AttributeNodes.FindNode('竖框颜色');
    if attri <> nil then mMyVBoxColor := attri.text;
    attri := root.AttributeNodes.FindNode('上横框颜色');
    if attri <> nil then mMyUpBoxColor := attri.text;
    attri := root.AttributeNodes.FindNode('下横框颜色');
    if attri <> nil then mMyDownBoxColor := attri.text;
    attri := root.AttributeNodes.FindNode('上轨颜色');
    if attri <> nil then mMyUpTrackColor := attri.text;
    attri := root.AttributeNodes.FindNode('下轨颜色');
    if attri <> nil then mMyDownTrackColor := attri.text;
    attri := root.AttributeNodes.FindNode('中横框颜色');
    if attri <> nil then mMyHBoxColor := attri.text;
    attri := root.AttributeNodes.FindNode('门板颜色');
    if attri <> nil then mMyPanelColor := attri.text;
    attri := root.AttributeNodes.FindNode('DataMode');
    if (attri<>nil) then mDataMode := MyStrToInt(attri.Text);
    attri := root.AttributeNodes.FindNode('Extra');
    if (attri<>nil) then mExtra := attri.Text else mExtra := '';

    mGridItem := 0;
    attri := root.AttributeNodes.FindNode('均分');
    if attri <> nil then
      mGridItem := StrToInt(attri.text);
    if (pexp = nil) or (pstype = nil) or (psp = nil) or (pudbox = nil)
      or (ptrack = nil) or (phbox = nil) or (pvbox = nil) then
    begin
      xdoc.Active := False;
      mCopyDoor := -1;
      exit;
    end;
    if l<>0 then ll := l-mL;
    if h<>0 then hh := h-mH;
    if pexp.noexp then
    begin
      ll := 0;
      hh := 0;
    end;

    if pexp <> nil then Copy(pexp, @mSlidingExp, 'SlidingExp');
    if psp <> nil then Copy(psp, @mSlidingParam, 'SlidingParam');
    if pstype <> nil then Copy(pstype, @mSlidingType, 'SlidingType');
    if ptrack <> nil then Copy(ptrack, @mTrackParam, 'TrackParam');
    if pudbox <> nil then Copy(pudbox, @mUDBoxParam, 'UDBoxParam');
    if phbox <> nil then Copy(phbox, @mHBoxParam, 'HBoxParam');
    if pvbox <> nil then Copy(pvbox, @mVBoxParam, 'VBoxParam');

    m := 0;
    t1 := hh/(mGridItem+1);
    if mGridItem=5 then t1 := hh;     //======
    if mGridItem=6 then t1 := hh;     //两均分，下格固定
    if mGridItem=7 then t1 := hh;   //两均分，上格固定
    if mGridItem=8 then t1 := hh/2;   //三均分，中间格固定
    if mGridItem=9 then t1 := hh;   //三均分(上两格固定)
    if mGridItem=10 then t1 := hh;   //三均分(下两格固定)
    for i := 0 to root.ChildNodes.Count - 1 do
    begin
      Node := root.ChildNodes[i];
      if Node.NodeName <> '配件' then continue;
      new(opa);
      attri := Node.AttributeNodes.FindNode('名称');
      if attri <> nil then opa.name := attri.text;
      attri := Node.AttributeNodes.FindNode('数量');
      if attri <> nil then opa.num := strtoint(attri.text);
      OptionalAccList.Add(opa);
    end;
    mDoorsList.Clear;
    m := -1;
    t1 := ll/mSlidingExp.doornum;  //计算需要补回的门洞差值
    for i := 0 to root.ChildNodes.Count - 1 do
    begin
      Node := root.ChildNodes[i];
      if Node.NodeName <> '单门' then continue;
      inc(m);
      door := TDoorRect.Create;
      door.mYPos := GetDoorYPos(m, mSlidingExp.doornum, mSlidingExp.overlapnum);
      mDoorsList.Add(door);
      attri := Node.AttributeNodes.FindNode('宽');
      door.doorw := MyStrToFloat(attri.text)+t1;    //补差值
      attri := Node.AttributeNodes.FindNode('高');
      door.doorh := MyStrToFloat(attri.text) + hh;
      attri := Node.AttributeNodes.FindNode('X0');
      door.x0 := MyStrToFloat(attri.text) + t1*m;     //补差值
      attri := Node.AttributeNodes.FindNode('Y0');
      door.y0 := MyStrToFloat(attri.text);
      attri := Node.AttributeNodes.FindNode('竖框类型');
      pvbox := GetVBoxParam(attri.text);
      if pvbox <> nil then Copy(pvbox, @door.mVBoxParam, 'VBoxParam');
      attri := Node.AttributeNodes.FindNode('竖框颜色');
      door.mVBoxColor := attri.text;
      attri := Node.AttributeNodes.FindNode('上下横框类型');
      pudbox := GetUDBoxParam(attri.text);
      if pudbox <> nil then Copy(pudbox, @door.mUDBoxParam, 'UDBoxParam');
      for j := 0 to Node.ChildNodes.Count - 1 do      //更新中横框
      begin
        cnode := Node.ChildNodes[j];
        if cnode.NodeName <> '中横框' then continue;
        new(rb);
        rb.selected := False;
        door.boxlist.Add(rb);
        attri := cnode.AttributeNodes.FindNode('类型');
        rb.boxtype := attri.text;
        attri := cnode.AttributeNodes.FindNode('颜色');
        rb.color := attri.text;
        rb.vh := True;
        attri := cnode.AttributeNodes.FindNode('vh');
        if attri.text = 'False' then
          rb.vh := False;
        attri := cnode.AttributeNodes.FindNode('w0');
        rb.w0 := MyStrToFloat(attri.text) + t1;
        attri := cnode.AttributeNodes.FindNode('h0');
        rb.h0 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('x0');
        rb.x0 := MyStrToFloat(attri.text) + t1*m;
        attri := cnode.AttributeNodes.FindNode('y0');
        rb.y0 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('d0');
        rb.d0 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('w1');
        rb.w1 := MyStrToFloat(attri.text) + t1;
        attri := cnode.AttributeNodes.FindNode('h1');
        rb.h1 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('x1');
        rb.x1 := MyStrToFloat(attri.text) + t1*m;
        attri := cnode.AttributeNodes.FindNode('y1');
        rb.y1 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('d1');
        rb.d1 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('w2');
        rb.w2 := MyStrToFloat(attri.text) + t1;
        attri := cnode.AttributeNodes.FindNode('h2');
        rb.h2 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('x2');
        rb.x2 := MyStrToFloat(attri.text) + t1*m;
        attri := cnode.AttributeNodes.FindNode('y2');
        rb.y2 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('d2');
        rb.d2 := MyStrToFloat(attri.text);
      end;
      for j := 0 to Node.ChildNodes.Count - 1 do        //更新门板
      begin
        cnode := Node.ChildNodes[j];
        if cnode.NodeName <> '门板' then continue;
        new(pnl);
        pnl.selected := False;
        door.panellist.Add(pnl);
        attri := cnode.AttributeNodes.FindNode('类型');
        pnl.PanelType := attri.text;
        attri := cnode.AttributeNodes.FindNode('颜色');
        pnl.color := attri.text;
        attri := cnode.AttributeNodes.FindNode('颜色2');
        if attri<>nil then pnl.color2 := attri.text;
        attri := cnode.AttributeNodes.FindNode('纹路');
        pnl.direct := attri.text;
        attri := cnode.AttributeNodes.FindNode('备注');
        if attri <> nil then
          pnl.memo := attri.text;
        attri := cnode.AttributeNodes.FindNode('ExtraData');
        if attri <> nil then
          pnl.extradata := attri.text;
        attri := cnode.AttributeNodes.FindNode('w0');
        pnl.w0 := MyStrToFloat(attri.text) + t1;
        attri := cnode.AttributeNodes.FindNode('h0');
        pnl.h0 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('x0');
        pnl.x0 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('y0');
        pnl.y0 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('d0');
        pnl.d0 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('w1');
        pnl.w1 := MyStrToFloat(attri.text) + t1;
        attri := cnode.AttributeNodes.FindNode('h1');
        pnl.h1 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('x1');
        pnl.x1 := MyStrToFloat(attri.text) + t1*m;
        attri := cnode.AttributeNodes.FindNode('y1');
        pnl.y1 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('d1');
        pnl.d1 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('w2');
        pnl.w2 := MyStrToFloat(attri.text) + t1;
        attri := cnode.AttributeNodes.FindNode('h2');
        pnl.h2 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('x2');
        pnl.x2 := MyStrToFloat(attri.text) + t1*m;
        attri := cnode.AttributeNodes.FindNode('y2');
        pnl.y2 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('d2');
        pnl.d2 := MyStrToFloat(attri.text);
      end;
      door.boxlist.Sort(SortRectBoxByY);
      door.panellist.Sort(SortRectPanelByY);
      RecalcDoor(door, t1, t2, hh);
    end;
    self.mIsSetDoors := True;
    mIsModify := False;
  except
  end;
  mCopyDoor := -1;
end;

function TLocalObject.EscapeBracket(name: string): string;
var n:Integer;
begin
  n := Pos('(', WideString(name));
  if n>0 then name := LeftStr(WideString(name), n-1);
  Result := name;
end;

function TLocalObject.FindBkType(bktype: string): boolean;
var
  i                 : Integer;
  psp               : PSlidingParam;
begin
  Result := False;
  for i := 0 to mSlidingParamList.Count - 1 do
  begin
    psp := mSlidingParamList[i];
    if psp.deleted then continue;
    if psp.name = bktype then
    begin
      Result := True;
      exit;
    end;
  end;
end;

function TLocalObject.GetDataValue(extradatajson: ISuperObject; SubMXList: ISuperObject): ISuperObject;
  Procedure Copylist(list1: TList; list2:TList);
  Var
    i:Integer;
  begin
    list1.clear;
    for i:=0 to list2.count-1 do
    begin
      list1.add(list2[i]);
    end;
  end;
  Procedure GetCurValue( L, H: string;CurcfgObj:PSlidingHfg2; exp:TExpress);
  Var
    CurcfgObjja,menxinja,cjo, cjo1 :ISuperObject;
    i, k, j : Integer;
    iter: TSuperObjectIter;
    Entry: TSuperAvlEntry;
    lname, lvalue : string;
  begin
    CurcfgObjja:= SO(CurcfgObj.varlist); //变量列表
    menxinja:= SO(CurcfgObj.mxlist); //门芯列表
    //showmessage(CurcfgObjja.AsString);
    exp.AddVariable('L', '', L, '', '');
    exp.AddVariable('H', '', H, '', '');
    for i:= 0 to CurcfgObjja.AsArray.length -1 do
    begin
      cjo := CurcfgObjja.AsArray.O[i];
      exp.AddVariable(cjo.S['名称'], '', cjo.S['值'], '', '');
    end;
    for k:=0 to menxinja.AsArray.length -1 do
    begin
      cjo1 := menxinja.AsArray.O[k];
      if ObjectFindFirst(cjo1, iter) then
      begin
        repeat
          //ShowMessageFmt('%s - %s', [iter.key, iter.val.AsString]);
          lname :=iter.key;
          if (lname = '颜色') or (lname = '材料') or (lname = '名称') then continue;
          lvalue := iter.val.AsString;
          exp.SetSubject(lvalue);
          cjo1.D[lname] := exp.ToValueFloat;
          //ShowMessageFmt('%s - %s', [iter.key, floattostr(cjo1.D[lname])]);
        until not ObjectFindNext(iter);
      end;
      ObjectFindClose(iter);
    end;
    CurcfgObj.mxlist:=menxinja.AsString;
  end;
  function GetSheetOject(name, bktype:string):PPanelType;
  var
  pnltype                 : PPanelType;
  i                 : Integer;
  begin
    Result := nil;
    for i := 0 to mPanelTypeList.Count - 1 do
    begin
      pnltype := mPanelTypeList[i];
      if (pnltype.name = name) and (pnltype.bktype = bktype) then
      begin
        Result := pnltype;
      end;
    end;
  end;
Var
  i,j,n,n1,n2 : Integer;
  xml, name, menxinstring, childmenxinstring, HBoxcolor : string;
  cfgobj, JSBoxp: TList;
  bfind,b1find : boolean;
  CurcfgObj :PSlidingHfg2;
  cSBoxp : PHBoxParam;
  CurcfgObjja, ja, outobjm, pdata, pdata2, pdata3, cjo, cjo1, menxinja, sub, sfobj, cSBoxpJson :ISuperObject;
  exp               : TExpress;
  pnltype :     PPanelType;
begin
  Result := nil;
  exp := TExpress.Create;
  cfgobj := TList.Create;
  if extradatajson.I['nType'] = 2 then
  begin
    if extradatajson.I['direc'] = 1 then
    begin
      xml := SfgParam.S['HTxml'];
      Copylist(cfgobj, SlidingHfg2List);
    end
    else
    begin
      xml := SfgParam.S['Txml'];
      Copylist(cfgobj, SlidingSfg2List);
    end;
  end;
  if extradatajson.I['nType'] = 3 then
  begin
    if extradatajson.I['direc'] = 1 then
    begin
      xml := SfgParam.S['HSxml'];
      Copylist(cfgobj, SlidingHfg3List);
    end
    else
    begin
      xml := SfgParam.S['Sxml'];
      Copylist(cfgobj, SlidingSfg3List);
    end;
  end;
   if extradatajson.I['nType'] = 4 then
  begin
    if extradatajson.I['direc'] = 1 then
    begin
      xml := SfgParam.S['HFxml'];
      Copylist(cfgobj, SlidingHfg4List);
    end
    else
    begin
      xml := SfgParam.S['Fxml'];
      Copylist(cfgobj, SlidingSfg4List);
    end;
  end;
  bfind := False;
  for i:=0 to cfgobj.count-1 do
  begin
    CurcfgObj := cfgobj[i];
    if extradatajson.S['name'] = CurcfgObj.spszh then
    begin
      bfind := True;
      break;
    end;
  end;
  if (not bfind) then // 没有对应的模板公式。
  begin
    outobjm := TSuperObject.Create();
    outobjm.S['xml']:= xml;
    outobjm.O['CurcfgObj']:= nil;
    outobjm.S['cSBoxp']:= '';
    result:= outobjm;
    exit;
  end;
  //'根据竖中横名称 - - 查询对应竖中横的3个变量的值'
  JSBoxp := TList.Create;
  Copylist(JSBoxp, SHBoxParamList);  //竖中横框参数表
  if (extradatajson.I['direc'] = 1) then Copylist(JSBoxp, HSHBoxParamList);// 横中横框参数
  ja := extradatajson.O['变量列表'];       
  //将横中横参数或竖中横参数中的数据添加到xml 的变量列表
  for i:=0 to JSBoxp.count-1 do
  begin
    cSBoxp := JSBoxp[i];
    if extradatajson.S['name'] = cSBoxp.name then
    begin
      pdata := TSuperObject.Create();
      pdata2 := TSuperObject.Create();
      pdata3 := TSuperObject.Create();
      pdata.S['名称'] := '$竖中横宽度';
      pdata.D['值'] := cSBoxp.height;
      pdata.S['是否显示'] := '0';
      pdata.S['可选值'] := '';

      pdata2.S['名称'] := '$竖中横厚度';
      pdata2.D['值'] := cSBoxp.depth;
      pdata2.S['是否显示'] := '0';
      pdata2.S['可选值'] := '';

      pdata3.S['名称'] := '$槽芯厚度';
      pdata3.D['值'] := cSBoxp.thick;
      pdata3.S['是否显示'] := '0';
      pdata3.S['可选值'] := '';

      if (extradatajson.I['direc'] = 1) then
      begin
        pdata.S['名称'] := '横度';
        pdata.D['值'] := cSBoxp.height;
        pdata.S['是否显示'] := '0';
        pdata.S['可选值'] := '';

        pdata2.S['名称'] := '$横中横厚度';
        pdata2.D['值'] := cSBoxp.height;
        pdata2.S['是否显示'] := '0';
        pdata2.S['可选值'] := '';

        pdata3.S['名称'] := '$槽芯厚度';
        pdata3.D['值'] := cSBoxp.height;
        pdata3.S['是否显示'] := '0';
        pdata3.S['可选值'] := '';
        ja.AsArray.Add(pdata);
        ja.AsArray.Add(pdata2);
        ja.AsArray.Add(pdata3);
        pdata:=nil;
        pdata2:=nil;
        pdata3:=nil;
        break;
      end;
      ja.AsArray.Add(pdata);
      ja.AsArray.Add(pdata2);
      ja.AsArray.Add(pdata3);
      pdata:=nil;
      pdata2:=nil;
      pdata3:=nil;
      break;
    end;
  end;
  n := ja.AsArray.Length;     //变量列表

  CurcfgObjja:= SO(CurcfgObj.varlist);  //替换 趟门2横分格或其他 中的变量列表
  if ja.AsArray.Length <> 0 then
  begin
    for i:=0 to n-1 do
    begin
      cjo :=ja.AsArray.O[i];;
      name := cjo.S['名称'];
      bfind := False;
      for j:=0 to CurcfgObjja.AsArray.Length-1 do
      begin
        cjo1:= CurcfgObjja.AsArray.O[j];
        if (cjo1.S['名称'] = name) then
        begin
          cjo1.D['值'] := cjo.D['值'];
          bfind := True;
          break;
        end;
      end;
      if (not bfind) then
      begin
        cjo.S['是否显示'] := '0';
        cjo.S['可选值'] := '';
        CurcfgObjja.AsArray.Add(cjo);
      end;
    end;
  end;
  //开始处理门芯列表字段  材料颜色
  {
    1.字段ExtraData 中 门芯列表为空， 【趟门2横分格或其他】 中的门芯列表材料或颜色等于xml
    字段ExtraData的材料颜色。
    2. 字段ExtraData 中 门芯列表不为空：
       2.1  字段ExtraData中 门芯列表的单个门芯，材料颜色为空，【趟门2横分格或其他】 中的门芯列表材料或颜色等于xml
    字段ExtraData的材料颜色。
      否则趟门2横分格或其他】 中的门芯列表材料或颜色 等于  字段ExtraData中 门芯列表的单个门芯，材料颜色
      2.2  段ExtraData 中 门芯列表 含有子门芯， 添加子门芯
      2.3  门芯列表中 如果名称为竖中横例外，【趟门2横分格或其他】 中的门芯列表材料取 字段ExtraData的名称
      如果   竖中横的门芯， 颜色不为空， 则为【趟门2横分格或其他】 中的门芯列表颜色
      否则 【趟门2横分格或其他】 中的门芯列表颜色 取  字段ExtraData的颜色。
  }
  CurcfgObj.varlist:=CurcfgObjja.AsString;
  menxinstring := extradatajson.S['门芯列表'];
  n2 := length(menxinstring);
  if n2 = 0 then
  begin
     menxinja:= SO(CurcfgObj.mxlist);
     for i:=0 to menxinja.AsArray.Length-1 do
     begin
       cjo:= menxinja.AsArray.O[i];
       if cjo.S['材料'] = '' then cjo.S['材料'] := extradatajson.S['材料'];
       if cjo.S['颜色'] = '' then cjo.S['颜色'] := extradatajson.S['颜色'];
       n1 := Pos('中横',cjo.S['名称']);
       if (n1 > 0) then cjo.S['材料'] := extradatajson.S['材料'];
     end;
  end
  else
  begin
    ja := extradatajson.O['门芯列表'];
    n := ja.AsArray.Length;
    if n <> 0 then
    begin
      menxinja:= SO(CurcfgObj.mxlist);
      HBoxcolor := '' ;// 中横颜色
      for i:=0 to menxinja.AsArray.Length-1 do
      begin
        bfind := False;
        b1find := False;
        cjo:= menxinja.AsArray.O[i];
        for j:=0 to n-1 do
        begin
          cjo1:= ja.AsArray.O[j];   //   extradatajson门芯列表
          if cjo.S['名称'] = cjo1.S['名称'] then
          begin
            if cjo1.S['材料'] <> '' then cjo.S['材料'] := cjo1.S['材料']
            else cjo.S['材料'] := extradatajson.S['材料'];
            if cjo1.S['颜色'] <> '' then cjo.S['颜色'] := cjo1.S['颜色']
            else cjo.S['颜色'] := extradatajson.S['颜色'];
            childmenxinstring := cjo1.S['子门芯'];
            if length(childmenxinstring) <>0 then
            begin
              sub := TSuperObject.Create();
              sub.S['名称'] := cjo1.S['名称'];
              sub.I['index'] := j;
              sub.O['子门芯'] := SO(cjo1.S['子门芯']);
              SubMXList.AsArray.Add(sub);      //添加子门芯
            end;
            bfind :=True;
          end;
          n1 := Pos('中横',cjo1.S['名称']);
          if (n1 > 0) and (not b1find) then
          begin
            HBoxcolor := cjo1.S['颜色'];
            b1find := True;
          end;
          if bfind and b1find then break;
        end;
        n1 := Pos('中横',cjo.S['名称']);     //竖中横
        if (n1 > 0) then
        begin
          cjo.S['材料'] := extradatajson.S['name'];
          if HBoxcolor <> '' then cjo.S['颜色'] := HBoxcolor
          else cjo.S['颜色'] := extradatajson.S['颜色'];
        end;
      end;
    end;
  end;

  CurcfgObj.mxlist:=menxinja.AsString; //整理新门芯数据
  GetCurValue(extradatajson.S['L'], extradatajson.S['H'], CurcfgObj, exp); //计算门芯公式
  menxinja:= SO(CurcfgObj.mxlist);   //整理新门芯数据
  //添加纹路  根据门板类型cfg的name，边框类型
  for i:=0 to menxinja.AsArray.Length-1 do
  begin
    cjo:= menxinja.AsArray.O[i];
    pnltype := GetSheetOject(cjo.S['材料'], extradatajson.S['边框类型']);
    if pnltype <> nil then
    begin
      cjo.S['direct']:=pnltype.direct;
    end;
    cjo.I['direc']:=extradatajson.I['direc'];
  end;
  sfobj:= TSuperObject.Create();
  sfobj.I['id']:= CurcfgObj.id;
  sfobj.S['fgtype']:= CurcfgObj.fgtype;
  sfobj.S['spszh']:= CurcfgObj.spszh;
  sfobj.S['spmk']:= CurcfgObj.spmk;
  sfobj.S['image']:= CurcfgObj.image;
  sfobj.O['varlist']:= SO(CurcfgObj.varlist);
  sfobj.O['mxlist']:= menxinja;
  cSBoxpJson:=TSuperObject.Create();
  cSBoxpJson.I['id'] := cSBoxp.id;
  cSBoxpJson.D['height'] := cSBoxp.height;
  cSBoxpJson.D['depth'] := cSBoxp.depth;
  cSBoxpJson.D['thick'] := cSBoxp.thick;
  cSBoxpJson.D['holepos'] := cSBoxp.holepos;
  cSBoxpJson.D['holenum'] := cSBoxp.holenum;
  cSBoxpJson.D['holecap'] := cSBoxp.holecap;
  cSBoxpJson.D['size'] := cSBoxp.size;
  cSBoxpJson.D['ishboxvalue'] := cSBoxp.ishboxvalue;
  cSBoxpJson.S['name'] := cSBoxp.name;
  cSBoxpJson.S['wlcode'] := cSBoxp.wlcode;
  cSBoxpJson.S['bjcode'] := cSBoxp.bjcode;
  cSBoxpJson.S['wjname'] := cSBoxp.wjname;
  cSBoxpJson.S['model'] := cSBoxp.model;
  cSBoxpJson.S['memo'] := cSBoxp.memo;
  cSBoxpJson.S['bdfile'] := cSBoxp.bdfile;
  cSBoxpJson.S['frametype'] := cSBoxp.frametype;

  outobjm := TSuperObject.Create();
  outobjm.S['xml']:= xml;
  outobjm.O['CurcfgObj']:= sfobj;
  outobjm.O['cSBoxp']:= cSBoxpJson;

  Result := outobjm;
end;
// extradatajson : extradata 字段数据
function TLocalObject.GetBomObj(extradatajson: ISuperObject): ISuperObject;
Var
  i, j :Integer;
  name : string;
  SubMXList, sub, ja, subSubMXList, tobj, cjo : ISuperObject;
begin
  Result:=nil;
  SubMXList := TSuperObject.Create(stArray);    //子门芯列表
  tobj := GetDataValue(extradatajson, SubMXList);
  if SubMXList.AsArray.length <> 0 then  //计算子门芯
  begin
    for i:=0 to SubMXList.AsArray.length-1 do
    begin
      sub :=SubMXList.AsArray.O[i];
      subSubMXList := TSuperObject.Create(stArray);
      sub.O['subtobj']:= GetDataValue(sub.O['子门芯'], subSubMXList);
    end;
    ja :=tobj.O['CurcfgObj'].O['门芯列表'];
    for j:=0 to ja.AsArray.length-1 do
    begin
      cjo:=ja.AsArray.O[i];
      name := cjo.S['名称'];
      for i:=0 to SubMXList.AsArray.length-1 do
      begin
        sub :=SubMXList.AsArray.O[i];
        if sub.S['名称'] = name then
        begin
          cjo.O['subtobj'] := sub.O['subtobj'];
        end;
      end;
    end;
  end;
  Result:=tobj;
end;

procedure TLocalObject.GetPanelBom(list:TList; bomclass, mat, color, color2, color3:string; pnll, pnlh:single);
  var i:Integer;
  p:PSlidingPanelBomDetail;
  pwl         : ^wldata;
  begin
    for i:=0 to mPanelBomDetailList.Count-1 do
    begin
      p := mPanelBomDetailList[i];
      if (p.bomclass=bomclass) and (p.lmin<pnll) and (p.lmax>=pnll) and (p.hmin<pnlh) and (p.hmax>=pnlh) then
      begin
        pwl := NewWLData;
        pwl.name := p.bomname;
        pwl.code := '';
        pwl.color := StringReplace(p.color, '$门板颜色', color, [rfReplaceAll]);
        pwl.color := StringReplace(p.color, '$门芯颜色', color, [rfReplaceAll]);
        pwl.color := StringReplace(pwl.color, '$附加物料颜色', color2, [rfReplaceAll]);
        pwl.color := StringReplace(pwl.color, '$边框颜色', color3, [rfReplaceAll]);
        pwl.memo := p.memo;
        pwl.memo2 := p.memo2;
        pwl.memo3 := p.memo3;
        mExp.SetSubject(p.l);
        pwl.l := mExp.ToValueFloat;
        mExp.SetSubject(p.w);
        pwl.w := mExp.ToValueFloat;
        mExp.SetSubject(p.h);
        pwl.h := mExp.ToValueFloat;
        pwl.group := 2;
        if p.bomtype='型材五金' then
          pwl.group := 1;
        if p.bomtype='五金' then
          pwl.group := 3;
        if p.bomtype='玻璃' then
        begin
          pwl.isglass := 1;
        end;
        pwl.num := p.num;
        pwl.bdfile := p.bdfile;
        list.Add(pwl);
      end;
    end;
  end;


procedure TLocalObject.AddOneMx(door:TDoorRect;pnl:PRectPanel; nHasMzhb:boolean; list:TList);
  procedure Copy(dst, src: Pointer);
  var
    p1, p2          : ^wldata;
  begin
    p1 := dst;
    p2 := src;
    p1^ := p2^;
  end;
  function ToColor(c, c1, c2, c3, c4:string):string;
  begin
    Result := c;
    if c='$竖框配件颜色1' then Result := c1;
    if c='$竖框配件颜色2' then Result := c2;
    if c='$竖框配件颜色3' then Result := c3;
    if c='$竖框配件颜色4' then Result := c4;
  end;
Var
  jtvalue, glvalue1, glvalue2, t: single;
  isglass, isbaiye  : boolean;
  h, w, h1, w1, h0, w0, h2, w2:single;
  pnltype:PPanelType;
  i, j, k, n, m, posindex:Integer;
  pssexp:PSlidingShutterExp;
  pa                : PAccessory;
  pcolorclass       : PSlidingColorClass;
  pbomdetail        : PSlidingWjBomDetail;
  skcolor1, skcolor2, skcolor3, skcolor4, str:string;
  pwl, pwl2 :Pwldata;
  cjo, detailobj,cjo1, cjo2 : ISuperObject;
  ww: Real;
begin
  ww := (mSlidingParam.fztlen*2)/mDoorsList.Count;
  mExp.AddVariable('$门板高度0', '', FloatToStr(pnl.h0), '', '');
  mExp.AddVariable('$门板宽度0', '', FloatToStr(pnl.w0), '', '');
  mExp.AddVariable('$门板高度', '', FloatToStr(pnl.h1), '', '');
  mExp.AddVariable('$门板宽度', '', FloatToStr(pnl.w1), '', '');
  jtvalue := 0;          //表示胶条位
  isglass := False;
  isbaiye := False;
  w1 := 0;
  h1 := 0;
  pnltype := GetPanelType(mSlidingParam.name, pnl.PanelType);      //门板类型.cfg
  if pnltype <> nil then
  begin
	  GetPanelBom(list, pnltype.slave, pnl.PanelType, pnl.color, pnl.color2, mMyVBoxColor, pnl.w1, pnl.h1);
	  jtvalue := pnltype.jtvalue * 2;
	  isglass := pnltype.isglass;
	  isbaiye := pnltype.isbaiye;
	  w1 := pnltype.mkl;
	  h1 := pnltype.mkh;
  end;
  glvalue1 := 0;
  glvalue2 := 0;   // glvalue2 是与玻璃有关的减量值，这两个值都跟玻璃板有关
  //当板材为玻璃的时候，需要减掉趟门的玻璃位
  if isglass then
  begin
	  glvalue1 := mSlidingParam.vboxjtw * 2;
   	posindex := door.GetPanelPosInDoor(pnl);
	  if (posindex = 1) then               //最下格
	    glvalue2 := mSlidingParam.hboxjtw + mSlidingParam.dboxjtw
	  else if (posindex = 2) then               //最上格
	    glvalue2 := mSlidingParam.hboxjtw + mSlidingParam.uboxjtw
	  else if (posindex = 0) then               //中间格
	    glvalue2 := mSlidingParam.hboxjtw * 2
	  else glvalue2 := mSlidingParam.dboxjtw + mSlidingParam.uboxjtw;
	//        glvalue1 := mSlidingParam.glassvalue1;
	//        glvalue2 := mSlidingParam.glassvalue2;
  end;
  pssexp := self.GetSSExp(pnl.PanelType);
  if (not isglass) and (isbaiye) and (pssexp <> nil) then
  begin
    cjo:= TSuperObject.Create();
    cjo1:= TSuperObject.Create();
    cjo2:= TSuperObject.Create();
    detailobj := TSuperObject.Create();
    h := pnl.h1 - h1;    //物料
    w := pnl.w1 - w1;
    h0 := pnl.h0 - h1;;    //可见
    w0 := pnl.w0 - w1;
    h2 := pnl.h2 - h1;;    //投影
    w2 := pnl.w2 - w1;
    if pssexp.height <> 0 then         //表示单条百叶的高度
    begin
      //物料尺寸百叶
      n := Trunc((h - jtvalue - glvalue2) / pssexp.height);  //（当前整块板的高度-胶条位-glvalue）/ 单条百叶的高度 这个n表示这块板由n条百叶拼接而成
      t := (h - jtvalue - glvalue2) - pssexp.height * n;
      if t > pssexp.minheight then
      begin
      n := n + 1;
      end
      else
      t := 0;
      pwl := NewWLData;
      pwl.name := pnl.PanelType; //'门板';
      pwl.color := pnl.color;
      pwl.memo := pnl.memo;
      pwl.code := '';
      pwl.l := (w - jtvalue - glvalue1);
      pwl.w := (h - jtvalue - glvalue2);
      pwl.l1:= pnl.w1;
      pwl.w1:= pnl.h1;
      pwl.hh1 := w1+jtvalue + glvalue1;
      pwl.ww1 := h1+ jtvalue + glvalue2;
      pwl.fzl := ww;
      cjo.I['num']:=n;
      cjo.S['l']:= Format('%.2f',[(w - jtvalue - glvalue1)]);
      cjo.S['w']:= Format('%.2f',[pssexp.height]);
      if t <> 0 then cjo.S['lw']:= Format('%.2f',[t])
      else cjo.S['lw']:= '0';
      detailobj.O['物料']:=cjo;

      //可视尺寸百叶
      n := Trunc((h0 - jtvalue - glvalue2) / pssexp.height);  //（当前整块板的高度-胶条位-glvalue）/ 单条百叶的高度 这个n表示这块板由n条百叶拼接而成
      t := (h0 - jtvalue - glvalue2) - pssexp.height * n;
      if t > pssexp.minheight then
      begin
      n := n + 1;
      end
      else
      t := 0;
      pwl.l0 := pnl.w0;
      pwl.w0 := pnl.h0;
      cjo1.I['num']:=n;
      cjo1.S['l']:= Format('%.2f',[(w0- jtvalue - glvalue1)]);
      cjo1.S['w']:= Format('%.2f',[pssexp.height]);
      if t <> 0 then cjo1.S['lw']:= Format('%.2f',[t])
      else cjo1.S['lw']:= '0';
      detailobj.O['可视']:=cjo1;

      //投影尺寸百叶
      n := Trunc((h2 - jtvalue - glvalue2) / pssexp.height);  //（当前整块板的高度-胶条位-glvalue）/ 单条百叶的高度 这个n表示这块板由n条百叶拼接而成
      t := (h2 - jtvalue - glvalue2) - pssexp.height * n;
      if t > pssexp.minheight then
      begin
      n := n + 1;
      end
      else
      t := 0;
      pwl.l2 := pnl.w2;
      pwl.w2 := pnl.h2;
      cjo2.I['num']:=n;
      cjo2.S['l']:= Format('%.2f',[(w2- jtvalue - glvalue1)]);
      cjo2.S['w']:= Format('%.2f',[pssexp.height]);
      if t <> 0 then cjo2.S['lw']:= Format('%.2f',[t])
      else cjo2.S['lw']:= '0';
      detailobj.O['投影']:=cjo2;

      str := detailobj.AsString;
      cjo:=nil;
      cjo1:=nil;
      cjo2:=nil;
      pwl.detail := StringReplace(str, '"', '^', [rfReplaceAll]);
      pcolorclass := GetSlidingColorClass('门板', pnl.PanelType, pnl.color);
      if pcolorclass <> nil then
      pwl.code := pwl.code+pcolorclass.wlcode;
      pwl.direct := pnl.direct;
      pwl.num := 1;
      pwl.group := 2;
      pwl.bomsize := pssexp.size;
      pwl.door_index := i+1;
      pwl.pnl_num := door.panellist.Count;
      pwl.pnl_index := j;
      if pnltype<>nil then
      begin
       pwl.h := pnltype.thick;
       pwl.memo := pnltype.memo;
       pwl.memo2 := pnltype.memo2;
       pwl.memo3 := pnltype.memo3;
       pwl.bdfile := pnltype.bdfile;
      end;
      pwl.myunit := '块';
      list.Add(pwl);
      if (pnltype <> nil) and (pnltype.slave <> '') and (not nHasMzhb) then
      begin
        //GetPanelBom(list, pnltype.slave, pnl.PanelType, pnl.color, pnl.w1, pnl.h1);
        pwl2 := NewWLData;
        Copy(pwl2, pwl);
        pwl.name := StringReplace(pwl.name, pnltype.slave, '', [rfReplaceAll]);
        pwl2.code := pwl.code + '+';
        pwl2.name := pnltype.slave;
        pwl2.color := pnltype.slave;
        pwl2.memo := pnltype.memo;
        list.Add(pwl2);
        if pnltype.slave2 <> '' then
        begin
          pwl2 := NewWLData;
          Copy(pwl2, pwl);
          pwl2.code := pwl.code + '+';
          pwl2.name := pnltype.slave2;
          pwl2.color := pnltype.slave2;
          pwl2.memo := pnltype.memo;
          list.Add(pwl2);
        end;
      end;
	  end
    else if pssexp.width <> 0 then          //
    begin
      //物料尺寸
      n := Trunc((w - jtvalue - glvalue1) / pssexp.width);  //
      t := (w - jtvalue - glvalue1) - pssexp.width * n;
      if t > pssexp.minwidth then
      begin
      n := n + 1;
      end
      else
      t := 0;
      pwl := NewWLData;
      pwl.name := pnl.PanelType; //'门板';
      pwl.color := pnl.color;
      pwl.memo := pnl.memo;
      pwl.code := '';
      pwl.fzl := ww;
      pwl.l := (h - jtvalue - glvalue2)+ww;
      pwl.w := (w - jtvalue - glvalue1);
      pwl.l1:= pnl.h1+ww;
      pwl.w1:= pnl.w1;
      pwl.hh1 := h1+ jtvalue + glvalue2;
      pwl.ww1 := w1+ jtvalue + glvalue1;
      cjo.I['num']:=n;
      cjo.S['l']:= Format('%.2f',[w - jtvalue - glvalue1]);
      cjo.S['w']:= Format('%.2f',[pssexp.width]);
      if t <> 0 then cjo.S['lw']:= Format('%.2f',[t])
      else cjo.S['lw']:= '0';
      detailobj.O['物料']:=cjo;

      //可视化尺寸百叶
      n := Trunc((w0 - jtvalue - glvalue1) / pssexp.width);  //
      t := (w0 - jtvalue - glvalue1) - pssexp.width * n;
      if t > pssexp.minwidth then
      begin
      n := n + 1;
      end
      else
      t := 0;
      pwl.l0 := pnl.h0+ww;
      pwl.w0 := pnl.w0;
      cjo1.I['num']:=n;
      cjo1.S['l']:= Format('%.2f',[w0- jtvalue - glvalue1]);
      cjo1.S['w']:= Format('%.2f',[pssexp.width]);
      if t <> 0 then cjo1.S['lw']:= Format('%.2f',[t])
      else cjo1.S['lw']:= '0';
      detailobj.O['可视']:=cjo1;
      //投影尺寸百叶
      n := Trunc((w2 - jtvalue - glvalue1) / pssexp.width);  //
      t := (w2 - jtvalue - glvalue1) - pssexp.width * n;
      if t > pssexp.minwidth then
      begin
      n := n + 1;
      end
      else
      t := 0;
      pwl.l2 := pnl.h2+ww;
      pwl.w2 := pnl.w2;

      cjo2.I['num']:=n;
      cjo2.S['l']:= Format('%.2f',[w2- jtvalue - glvalue1]);
      cjo2.S['w']:= Format('%.2f',[pssexp.width]);
      if t <> 0 then cjo2.S['lw']:= Format('%.2f',[t])
      else cjo2.S['lw']:= '0';
      detailobj.O['投影']:=cjo2;
      str := detailobj.AsString;
      cjo:=nil;
      cjo1:=nil;
      cjo2:=nil;
      pwl.detail := StringReplace(str, '"', '^', [rfReplaceAll]);
      pcolorclass := GetSlidingColorClass('门板', pnl.PanelType, pnl.color);
      if pcolorclass <> nil then
      pwl.code := pwl.code+pcolorclass.wlcode;
      pwl.direct := pnl.direct;
      pwl.bomsize := pssexp.size;
      pwl.num := 1;
      pwl.group := 2;
      pwl.door_index := i+1;
      pwl.pnl_num := door.panellist.Count;
      pwl.pnl_index := j;
      if pnltype<>nil then
      begin
        pwl.h := pnltype.thick;
        pwl.memo := pnltype.memo;
        pwl.memo2 := pnltype.memo2;
        pwl.memo3 := pnltype.memo3;
        pwl.bdfile := pnltype.bdfile;
      end;
      pwl.myunit := '块';
      list.Add(pwl);
      if (pnltype <> nil) and (pnltype.slave <> '') and (not nHasMzhb) then
      begin
        //GetPanelBom(list, pnltype.slave, pnl.PanelType, pnl.color, pnl.w1, pnl.h1);
        pwl2 := NewWLData;
        Copy(pwl2, pwl);
        pwl.name := StringReplace(pwl.name, pnltype.slave, '', [rfReplaceAll]);
        pwl2.code := pwl.code + '+';
        pwl2.name := pnltype.slave;
        pwl2.color := pnltype.slave;
        pwl2.memo := pnltype.memo;
        list.Add(pwl2);
        if pnltype.slave2 <> '' then
        begin
          pwl2 := NewWLData;
          Copy(pwl2, pwl);
          pwl2.code := pwl.code + '+';
          pwl2.name := pnltype.slave2;
          pwl2.color := pnltype.slave2;
          pwl2.memo := pnltype.memo;
          list.Add(pwl2);
        end;
      end;
    end;
  end;                              //if (not isglass) and (isbaiye) then
  if (not ((not isglass) and (isbaiye))) then //玻璃 or 木板     非百叶
  begin
	pwl := NewWLData;
	pwl.name := pnl.PanelType;      //'门板';
	pwl.color := pnl.color;
	pwl.memo := pnl.memo;
	pwl.code := '';
	if pnl.direct = '横纹' then
	begin
    pwl.fzl := ww;
	  pwl.l := (pnl.w1 - jtvalue - glvalue1) - w1+ww;
	  pwl.w := (pnl.h1 - jtvalue - glvalue2) - h1;
    pwl.hh1 := w1+ jtvalue + glvalue1;
    pwl.ww1 := h1+ jtvalue + glvalue2;
    pwl.l1:= pnl.w1;
    pwl.w1:= pnl.h1;
    pwl.l0:= pnl.w0+ww;   // 可视尺寸
    pwl.w0:= pnl.h0;
    pwl.l2:= pnl.w2+ww;   // 投影尺寸
    pwl.w2:= pnl.h2;
	end
	else
	begin
    pwl.fzl := ww;
	  pwl.w := (pnl.w1 - jtvalue - glvalue1) - w1;
	  pwl.l := (pnl.h1 - jtvalue - glvalue2) - h1;
    pwl.l1:= pnl.w1;
    pwl.w1:= pnl.h1;
    pwl.ww1 := w1+ jtvalue + glvalue1;
    pwl.hh1 := h1+ jtvalue + glvalue2;

    pwl.w0:= (pnl.w0);   // 可视尺寸
    pwl.l0:= (pnl.h0);
    pwl.w2:= (pnl.w2);   // 投影尺寸
    pwl.l2:= (pnl.h2);
	end;
	pcolorclass := GetSlidingColorClass('门板', pnl.PanelType, pnl.color);
	if pcolorclass <> nil then
	  pwl.code := pwl.code+pcolorclass.wlcode;
	pwl.direct := pnl.direct;
	pwl.num := 1;
	pwl.group := 2;
	pwl.door_index := i+1;
	pwl.pnl_num := door.panellist.Count;
	pwl.pnl_index := j;
	if pnltype<>nil then
	begin
	  pwl.h := pnltype.thick;
	  pwl.memo := pnltype.memo;
	  pwl.memo2 := pnltype.memo2;
	  pwl.memo3 := pnltype.memo3;
	  pwl.bdfile := pnltype.bdfile;
	end;
	if isglass then pwl.isglass := 1;
	pwl.myunit := '块';
	//mExp.AddVariable('$门板高度', '', FloatToStr(pwl.l), '');
	//mExp.AddVariable('$门板宽度', '', FloatToStr(pwl.w), '');
	list.Add(pwl);
	if (pnltype <> nil) and (pnltype.slave <> '') and (not nHasMzhb) then
	begin
	  //GetPanelBom(list, pnltype.slave, pnl.PanelType, pnl.color, pnl.w1, pnl.h1);
	  pwl2 := NewWLData;
	  Copy(pwl2, pwl);
	  pwl.name := StringReplace(pwl.name, pnltype.slave, '', [rfReplaceAll]);
	  pwl2.code := pwl.code + '+';
	  pwl2.name := pnltype.slave;
	  pwl2.color := pnltype.slave;
	  pwl2.memo := pnltype.memo;
	  list.Add(pwl2);
	  if pnltype.slave2 <> '' then
	  begin
		pwl2 := NewWLData;
		Copy(pwl2, pwl);
		pwl2.code := pwl.code + '+';
		pwl2.name := pnltype.slave2;
		pwl2.color := pnltype.slave2;
		pwl2.memo := pnltype.memo;
		list.Add(pwl2);
	  end;
	end;
	//添加门板的关联五金  无门转换表时的逻辑
	if (pnltype <> nil) and (pnltype.wjname <> '') and (not nHasMzhb) then
	begin
	  for m := 0 to mSlidingWjBomDetailList.Count - 1 do
	  begin
		pbomdetail := mSlidingWjBomDetailList[m];
		if pbomdetail.bomname = pnltype.wjname then
		begin
		  pwl := NewWLData;
		  pwl.name := pbomdetail.name;
		  mExp.SetSubject(pbomdetail.l);
		  pwl.l := mExp.ToValueFloat;
		  mExp.SetSubject(pbomdetail.d);
		  pwl.w := mExp.ToValueFloat;
		  mExp.SetSubject(pbomdetail.num);
		  pwl.num := mExp.ToValueInt;
		  pa := GetAccessory(pwl.name);
		  pwl.group := 3;
		  pwl.door_index := i+1;
		  pwl.pnl_num := door.panellist.Count;
		  pwl.pnl_index := j;
		  if pa <> nil then
		  begin
			pwl.memo := pa.memo;
			pwl.memo2 := pa.memo2;
			pwl.memo3 := pa.memo3;
			pwl.bdfile := pa.bdfile;
			pwl.color := ToColor(pa.color, skcolor1, skcolor2, skcolor3, skcolor4);
			pwl.code := pa.wlcode;
			pwl.myunit := pa.myunit;
			if pa.isglass then pwl.isglass := 1 else pwl.isglass := 0;
			pcolorclass := GetSlidingColorClass('配件', pwl.color);
			if pcolorclass <> nil then
			  pwl.code := pwl.code + '' + pcolorclass.wlcode;
			if pa.myclass = '型材' then pwl.group := 1;
			if pa.myclass = '门板' then
			begin
			  pwl.group := 2;
			  pwl.color := pnl.color;
			end;
		  end;                      //pa
		  list.Add(pwl);
		end;                        //if pbom
	  end;                          //for
	end;
  end;                            //if  添加门板的关联五金
  //添加门板的关联五金    有门转换表时的逻辑
  if (pnltype <> nil) and (pnltype.wjname <> '') and (nHasMzhb) then
  begin
	for m := 0 to mSlidingWjBomDetailList.Count - 1 do
	begin
	  pbomdetail := mSlidingWjBomDetailList[m];
	  if pbomdetail.bomname = pnltype.wjname then
	  begin
		  pwl := NewWLData;
		  pwl.name := pbomdetail.name;
		  mExp.SetSubject(pbomdetail.l);
		  pwl.l := mExp.ToValueFloat;
		  mExp.SetSubject(pbomdetail.d);
		  pwl.w := mExp.ToValueFloat;
		  mExp.SetSubject(pbomdetail.num);
		  pwl.num := mExp.ToValueInt;
		  pa := GetAccessory(pwl.name);
		  pwl.group := 3;
		  pwl.door_index := i+1;
		  pwl.pnl_num := door.panellist.Count;
		  pwl.pnl_index := j;
		  if pa <> nil then
		  begin
		    pwl.memo := pa.memo;
		    pwl.memo2 := pa.memo2;
		    pwl.memo3 := pa.memo3;
		    pwl.bdfile := pa.bdfile;
		    pwl.color := ToColor(pa.color, skcolor1, skcolor2, skcolor3, skcolor4);
		    pwl.code := pa.wlcode;
		    pwl.myunit := pa.myunit;
		    if pa.isglass then pwl.isglass := 1 else pwl.isglass := 0;
		    pcolorclass := GetSlidingColorClass('配件', pwl.color);
		    if pcolorclass <> nil then pwl.code := pwl.code + '' + pcolorclass.wlcode;
		    if pa.myclass = '型材' then pwl.group := 1;
		    if pa.myclass = '门板' then
		    begin
			  pwl.group := 2;
			  pwl.color := pnl.color;
		    end;
		  end;                      //pa
		list.Add(pwl);
	  end;
	end;
  end;
end;

function TLocalObject.NewWLData: Pointer;
  var
    pwl             : ^wldata;
  begin
    new(pwl);
    pwl.ono := self.orderno;
    pwl.gno := self.graphno;
    pwl.hno := self.holeno;
    pwl.num := 1;
    pwl.fzl := 0;
    pwl.l0 := 0;       //可视
    pwl.w0 := 0;      //可视
    pwl.l := 0;
    pwl.ww1 := 0;      //差值
    pwl.hh1 := 0;      //差值
    pwl.w1 := 0;      //未减差值物料
    pwl.l1 := 0;      //未减差值物料
    pwl.w := 0;      //物料
    pwl.h := 0;      //物料
    pwl.w2 := 0;      //投影
    pwl.l2 := 0;      //投影
    pwl.code := '';
    pwl.color := '';
    pwl.group := 0;
    pwl.isglass := 0;
    pwl.bomsize := 0;
    pwl.door_index := 0;
    pwl.pnl_num := 0;
    pwl.pnl_index := 0;
    pwl.detail:='';
    pwl.doorname := mSlidingParam.name;
    Result := pwl;
end;

function TLocalObject.GetXMLBom: string;
  procedure Copy(dst, src: Pointer);
  var
    p1, p2          : ^wldata;
  begin
    p1 := dst;
    p2 := src;
    p1^ := p2^;
  end;

  function MyIntToBcd(v: Integer): TBcd;
  begin
    Result := IntegerToBcd(v);
  end;
  function MyFloatToBcd(v: single): TBcd;
  var
    str             : string;
  begin
    str := Format('%.1f', [v]);
    Result := StrToBcd(str);
  end;
  function ToColor(c, c1, c2, c3, c4:string):string;
  begin
    Result := c;
    if c='$竖框配件颜色1' then Result := c1;
    if c='$竖框配件颜色2' then Result := c2;
    if c='$竖框配件颜色3' then Result := c3;
    if c='$竖框配件颜色4' then Result := c4;
  end;
 
  function GetBomCfg(pwl:Pwldata):PCfgTable;
  var cfg:PCfgTable;
  i, n, t:Integer;
  s, ss:string;
  begin
    Result := nil;
    n := mCfglist.Count;
    for i:=0 to n-1 do
    begin
      cfg := mCfglist[i];
      if cfg.modle<>mDataMode then continue;
      if cfg.name<>pwl.name then continue;
      if cfg.bomname='' then continue;
      s := cfg.frametype + ',';
      ss := pwl.doorname + ',';
      t := Pos(ss, s);
      if t<1 then continue;
      Result := cfg;
      break;
    end;
  end;
  procedure addBox(newMx : PRectBox; door: TDoorRect; i, nType: Integer; list: TList);
  Var
    m : Integer;
    pwl : Pwldata;
    phbox : PHBoxParam;
    pcolorclass : PSlidingColorClass;
    pbomdetail        : PSlidingWjBomDetail;
    pa                : PAccessory;
    skcolor1, skcolor2, skcolor3, skcolor4: string; 
  begin
    pwl := NewWLData;
    pwl.name := newMx.boxtype;
    pwl.color := newMx.color;
    phbox := GetHBoxParam(newMx.boxtype, nType);       //横中横
    if phbox <> nil then
    begin
      pwl.memo := phbox.memo;
      pwl.bdfile := phbox.bdfile;
      pwl.code := phbox.wlcode;
      pwl.w := 0;
      pwl.h := 0;
      pwl.bomsize := phbox.size;
    end;
    pcolorclass := GetSlidingColorClass('中横框', pwl.color);
    if pcolorclass <> nil then
      pwl.code := pwl.code+pcolorclass.wlcode;
    pwl.num := 1;
    pwl.l := (door.doorw - door.mVBoxParam.height * 2);
    if (phbox<>nil) and (phbox.ishboxvalue=1) then
    begin
      pwl.l := pwl.l + mSlidingParam.hboxvalue;
    end;
    if (nType = 2) or (nType = 1) then
    begin
      pwl.l := newMx.h0;
      if (phbox<>nil) and (phbox.ishboxvalue=1) then
      begin
        pwl.l := pwl.l + mSlidingParam.hboxvalue;
      end;
    end;
    pwl.group := 1;
    pwl.door_index := i+1;
    pwl.myunit := '根';
    list.Add(pwl);
    mExp.AddVariable('$中横框长度', '', FloatToStr(pwl.l), '', '');
    if phbox.wjname <> '' then        //下横框五金
    begin
      for m := 0 to mSlidingWjBomDetailList.Count - 1 do
      begin
        pbomdetail := mSlidingWjBomDetailList[m];
        if pbomdetail.bomname = phbox.wjname then
        begin
          pwl := NewWLData;
          pwl.name := pbomdetail.name;
          mExp.SetSubject(pbomdetail.l);
          pwl.l := mExp.ToValueFloat;
          mExp.SetSubject(pbomdetail.d);
          pwl.w := mExp.ToValueFloat;
          mExp.SetSubject(pbomdetail.num);
          pwl.num := mExp.ToValueInt;
          pa := GetAccessory(pwl.name);
          pwl.group := 3;
          pwl.door_index := i+1;
          if pa <> nil then
          begin
            pwl.memo := pa.memo;
            pwl.memo2 := pa.memo2;
            pwl.memo3 := pa.memo3;
            pwl.bdfile := pa.bdfile;
            pwl.color := ToColor(pa.color, skcolor1, skcolor2, skcolor3, skcolor4);
            pwl.code := pa.wlcode;
            pwl.myunit := pa.myunit;
            if pa.isglass then pwl.isglass := 1 else pwl.isglass := 0;
            pcolorclass := GetSlidingColorClass('配件', pwl.color);
            if pcolorclass <> nil then
              pwl.code := pwl.code + '' + pcolorclass.wlcode;
            if pa.myclass = '型材' then pwl.group := 1;
            if pa.myclass = '门板' then pwl.group := 2;
          end;
          list.Add(pwl);
        end;
      end;
    end;
  end;
var
  i, j, k, n, m, posindex, nType, subfg: Integer;
  door              : TDoorRect;
  rb, newMx          : PRectBox;
  pnl, newpnl         : PRectPanel;
  jtvalue, glvalue1, glvalue2, t: single;
  pwl, pwl2         : Pwldata;
  list, list2       : TList;
  isglass, isbaiye  : boolean;
  str, wjname       : string;
  h, w, h1, w1:single;

  pcolor            : PSlidingColor;
  pexp              : PSlidingExp;
  pstype            : PSlidingType;
  psp               : PSlidingParam;
  ptrack            : PTrackParam;
  pudbox            : PUDBoxParam;
  phbox             : PHBoxParam;
  pvbox             : PVBoxParam;
  pnltype           : PPanelType;
  pa                : PAccessory;
  pcolorclass       : PSlidingColorClass;
  pbomdetail        : PSlidingWjBomDetail;
  pssexp            : PSlidingShutterExp;
  skcolor1, skcolor2, skcolor3, skcolor4:string;
  opa :POptionalAcc;
  cfg : PCfgTable;
  nHasMzhb : boolean;
  sJsonstring : string;
  sJson, FGObj, ja, oneMxs, lObj, childja, subMxs: ISuperObject;
  ww:Real;  //是否计算防撞条
begin
  list := TList.Create;
  list2 := TList.Create;
  mExp.ClearVarList;
  mExp.AddVariable('$门洞高度', '', IntToStr(mH), '', '');
  mExp.AddVariable('$门洞宽度', '', IntToStr(mL), '', '');
  mExp.AddVariable('$重叠数', '', IntToStr(mSlidingExp.overlapnum), '', '');
  mExp.AddVariable('$门扇数', '', IntToStr(mSlidingExp.doornum), '', '');
  nHasMzhb := False;
  if mCfglist.count <> 0 then nHasMzhb:= True;
  if mDoorsList.Count > 0 then
  begin
    door := TDoorRect(mDoorsList[0]);
    if mNoCDWPriceFlag=0 then door.doorw:= door.doorw + mSlidingExp.overlapnum*mSlidingParam.overlap;
    if mNoFZTPriceFlag = 0 then
    mExp.AddVariable('$成品门宽度', '', FloatToStr(door.doorw), '', '');
    mExp.AddVariable('$成品门高度', '', FloatToStr(door.doorh), '', '');

    pcolorclass := GetSlidingColorClass('竖框', mSlidingParam.vboxtype,door.mVBoxColor);
    if pcolorclass<>nil then
    begin
      skcolor1 := pcolorclass.skcolor1;
      skcolor2 := pcolorclass.skcolor2;
      skcolor3 := pcolorclass.skcolor3;
      skcolor4 := pcolorclass.skcolor4;
    end;
  end;
  //上轨
  if (mDataMode=0) and (mTrackParam.wlupcode <> '') then
  begin
    pwl := NewWLData;
    pwl.name := mTrackParam.upname;
    pwl.code := mTrackParam.wlupcode;
    pwl.color := mMyUpTrackColor;
    pwl.l := mL - mTrackParam.lkvalue1;
    if mAddLength>0 then pwl.l := pwl.l + mAddLength;
    pwl.w := 0;
    pwl.h := 0;
    pwl.bomsize := mTrackParam.upsize;
    pcolorclass := GetSlidingColorClass('上轨',pwl.name, pwl.color);       //20191109修改
    if pcolorclass <> nil then
      pwl.code := pwl.code + '' + pcolorclass.wlcode;
    pwl.num := 1;
    pwl.group := 1;
    pwl.memo := mTrackParam.upmemo;
    pwl.myunit := '条';
    pwl.bdfile := mTrackParam.upbdfile;
    list.Add(pwl);
    mExp.AddVariable('$上轨长度', '', FloatToStr(pwl.l), '', '');
  end;
  //下轨
  if (mDataMode=0) and (mTrackParam.wldncode <> '') then
  begin
    pwl := NewWLData;
    pwl.name := mTrackParam.dnname;
    pwl.code := mTrackParam.wldncode;
    pwl.color := mMyDownTrackColor;
    pwl.l := mL - mTrackParam.lkvalue2;
    if mAddLength>0 then pwl.l := pwl.l + mAddLength;
    pwl.w := 0;
    pwl.h := 0;
    pwl.bomsize := mTrackParam.downsize;
    pcolorclass := GetSlidingColorClass('下轨',pwl.name, pwl.color);    //20191109修改
    if pcolorclass <> nil then
      pwl.code := pwl.code + '' + pcolorclass.wlcode;
    pwl.num := 1;
    pwl.group := 1;
    pwl.memo := mTrackParam.dnmemo;
    pwl.myunit := '条';
    pwl.bdfile := mTrackParam.dnbdfile;
    list.Add(pwl);
    mExp.AddVariable('$下轨长度', '', FloatToStr(pwl.l), '', '');
  end;

  //趟门关联的五金
  wjname := mSlidingParam.wjname;
  if (mDataMode=0) and (wjname <> '') then
  begin
    for m := 0 to mSlidingWjBomDetailList.Count - 1 do
    begin
      pbomdetail := mSlidingWjBomDetailList[m];
      if pbomdetail.bomname = wjname then
      begin
        pwl := NewWLData;
        pwl.name := pbomdetail.name;
        mExp.SetSubject(pbomdetail.l);
        pwl.l := mExp.ToValueFloat;
        mExp.SetSubject(pbomdetail.d);
        pwl.w := mExp.ToValueFloat;
        mExp.SetSubject(pbomdetail.num);
        pwl.num := mExp.ToValueInt;
        pa := GetAccessory(pwl.name);
        pwl.group := 3;
        if pa <> nil then
        begin
          pwl.memo := pa.memo;
          pwl.memo2 := pa.memo2;
          pwl.memo3 := pa.memo3;
          pwl.bdfile := pa.bdfile;
          pwl.color := ToColor(pa.color, skcolor1, skcolor2, skcolor3, skcolor4);
          pwl.code := pa.wlcode;
          pcolorclass := GetSlidingColorClass('配件', pa.name, pwl.color);
          if pcolorclass <> nil then
            pwl.code := pwl.code + '' + pcolorclass.wlcode;
          pwl.myunit := pa.myunit;
          if pa.isglass then pwl.isglass := 1 else pwl.isglass := 0;
          if pa.myclass = '型材' then pwl.group := 1;
          if pa.myclass = '门板' then pwl.group := 2;
        end;
        list.Add(pwl);
      end;
    end;
  end;
  if (mDataMode=0) and (mTrackParam.wjname1 <> '') then     //上轨五金
  begin
    for m := 0 to mSlidingWjBomDetailList.Count - 1 do
    begin
      pbomdetail := mSlidingWjBomDetailList[m];
      if pbomdetail.bomname = mTrackParam.wjname1 then
      begin
        pwl := NewWLData;
        pwl.name := pbomdetail.name;
        mExp.SetSubject(pbomdetail.l);
        pwl.l := mExp.ToValueFloat;
        mExp.SetSubject(pbomdetail.d);
        pwl.w := mExp.ToValueFloat;
        mExp.SetSubject(pbomdetail.num);
        pwl.num := mExp.ToValueInt;
        pa := GetAccessory(pwl.name);
        pwl.group := 3;
        if pa <> nil then
        begin
          pwl.memo := pa.memo;
          pwl.memo2 := pa.memo2;
          pwl.memo3 := pa.memo3;
          pwl.bdfile := pa.bdfile;
          pwl.color := ToColor(pa.color, skcolor1, skcolor2, skcolor3, skcolor4);
          pwl.code := pa.wlcode;
          pwl.myunit := pa.myunit;
          if pa.isglass then pwl.isglass := 1 else pwl.isglass := 0;
          pcolorclass := GetSlidingColorClass('配件', pwl.color);
          if pcolorclass <> nil then
            pwl.code := pwl.code + '' + pcolorclass.wlcode;
          if pa.myclass = '型材' then pwl.group := 1;
          if pa.myclass = '门板' then pwl.group := 2;
        end;
        list.Add(pwl);
      end;
    end;
  end;
  if (mDataMode=0) and (mTrackParam.wjname2 <> '') then     //下轨五金
  begin
    for m := 0 to mSlidingWjBomDetailList.Count - 1 do
    begin
      pbomdetail := mSlidingWjBomDetailList[m];
      if pbomdetail.bomname = mTrackParam.wjname2 then
      begin
        pwl := NewWLData;
        pwl.name := pbomdetail.name;
        mExp.SetSubject(pbomdetail.l);
        pwl.l := mExp.ToValueFloat;
        mExp.SetSubject(pbomdetail.d);
        pwl.w := mExp.ToValueFloat;
        mExp.SetSubject(pbomdetail.num);
        pwl.num := mExp.ToValueInt;
        pa := GetAccessory(pwl.name);
        pwl.group := 3;
        if pa <> nil then
        begin
          pwl.memo := pa.memo;
          pwl.memo2 := pa.memo2;
          pwl.memo3 := pa.memo3;
          pwl.bdfile := pa.bdfile;
          pwl.color := ToColor(pa.color, skcolor1, skcolor2, skcolor3, skcolor4);
          pwl.code := pa.wlcode;
          pwl.myunit := pa.myunit;
          if pa.isglass then pwl.isglass := 1 else pwl.isglass := 0;
          pcolorclass := GetSlidingColorClass('配件', pwl.color);
          if pcolorclass <> nil then
            pwl.code := pwl.code + '' + pcolorclass.wlcode;
          if pa.myclass = '型材' then pwl.group := 1;
          if pa.myclass = '门板' then pwl.group := 2;
        end;
        list.Add(pwl);
      end;
    end;
  end;

  //竖框
  for i := 0 to mDoorsList.Count - 1 do
  begin
    if (mDataMode=1) then break;
    door := TDoorRect(mDoorsList[i]);
    pwl := NewWLData;
    pwl.name := door.mVBoxParam.name;
    pwl.color := door.mVBoxColor;
    pvbox := self.GetVBoxParam(pwl.name);
    if pvbox <> nil then
    begin
      pwl.memo := pvbox.memo;
      pwl.bdfile := pvbox.bdfile;
      pwl.code := pvbox.wlcode;
      pwl.w := 0;
      pwl.h := 0;
    end;
    pcolorclass := GetSlidingColorClass('竖框', pwl.color);
    if pcolorclass <> nil then
      pwl.code := pwl.code + '' + pcolorclass.wlcode;
    pwl.num := 2;
    pwl.l := door.doorh - pvbox.vboxvalue;
    pwl.group := 1;
    pwl.myunit := '条';
    pwl.bomsize := pvbox.size;
    pwl.door_index := i+1;
    list.Add(pwl);
    mExp.AddVariable('$竖框长度', '', FloatToStr(pwl.l), '', '');

    if door.mVBoxParam.wjname <> '' then //竖框五金
    begin
      for m := 0 to mSlidingWjBomDetailList.Count - 1 do
      begin
        pbomdetail := mSlidingWjBomDetailList[m];
        if pbomdetail.bomname = door.mVBoxParam.wjname then
        begin
          pwl := NewWLData;
          pwl.name := pbomdetail.name;
          mExp.SetSubject(pbomdetail.l);
          pwl.l := mExp.ToValueFloat;
          mExp.SetSubject(pbomdetail.d);
          pwl.w := mExp.ToValueFloat;
          mExp.SetSubject(pbomdetail.num);
          pwl.num := mExp.ToValueInt;
          pa := GetAccessory(pwl.name);
          pwl.group := 3;
          pwl.door_index := i+1;
          if pa <> nil then
          begin
            pwl.memo := pa.memo;
            pwl.memo2 := pa.memo2;
            pwl.memo3 := pa.memo3;
            pwl.bdfile := pa.bdfile;
            pwl.color := ToColor(pa.color, skcolor1, skcolor2, skcolor3, skcolor4);
            pwl.code := pa.wlcode;
            pwl.myunit := pa.myunit;
            if pa.isglass then pwl.isglass := 1 else pwl.isglass := 0;
            pcolorclass := GetSlidingColorClass('配件', pwl.color);
            if pcolorclass <> nil then
              pwl.code := pwl.code + '' + pcolorclass.wlcode;
            if pa.myclass = '型材' then pwl.group := 1;
            if pa.myclass = '门板' then pwl.group := 2;
          end;
          list.Add(pwl);
        end;
      end;
    end;
  end;

  for i := 0 to mDoorsList.Count - 1 do
  begin
    if (mDataMode=1) then break;
    door := TDoorRect(mDoorsList[i]);
    //上下横框
    pwl := NewWLData;
    pwl.name := mUDBoxParam.upname;
    pwl.color := mMyUpBoxColor;
    pwl.code := mUDBoxParam.wlupcode;
    pwl.bdfile := mUDBoxParam.upbdfile;
    pcolorclass := GetSlidingColorClass('上横框',pwl.name, pwl.color);
    if pcolorclass <> nil then
      pwl.code := pwl.code + '' + pcolorclass.wlcode;
    pwl.w := 0;
    pwl.h := 0;
    pwl.num := 1;
    pwl.group := 1;
    pwl.l := (door.doorw - door.mVBoxParam.udboxvalue * 2);
    pwl.bomsize := mUDBoxParam.upsize;
    pwl.memo := mUDBoxParam.upmemo;
    pwl.door_index := i+1;
    pwl.myunit := '条';
    list.Add(pwl);
    mExp.AddVariable('$上横框长度', '', FloatToStr(pwl.l), '', '');
    pwl := NewWLData;
    pwl.name := mUDBoxParam.dnname;
    pwl.color := mMyDownBoxColor;
    pcolor := GetSlidingColor(pwl.color);
    pwl.code := mUDBoxParam.wldncode;
    pwl.bdfile := mUDBoxParam.dnbdfile;
    pcolorclass := GetSlidingColorClass('下横框',pwl.name, pwl.color);
    if pcolorclass <> nil then
      pwl.code := pwl.code + '' + pcolorclass.wlcode;
    pwl.w := 0;
    pwl.h := 0;
    pwl.num := 1;
    pwl.l := (door.doorw - door.mVBoxParam.udboxvalue * 2);
    pwl.bomsize := mUDBoxParam.downsize;
    pwl.group := 1;
    pwl.memo := mUDBoxParam.dnmemo;
    pwl.door_index := i+1;
    pwl.myunit := '条';
    list.Add(pwl);
    mExp.AddVariable('$下横框长度', '', FloatToStr(pwl.l), '', '');

    if door.mUDBoxParam.wjname1 <> '' then //上横框五金
    begin
      for m := 0 to mSlidingWjBomDetailList.Count - 1 do
      begin
        pbomdetail := mSlidingWjBomDetailList[m];
        if pbomdetail.bomname = door.mUDBoxParam.wjname1 then
        begin
          pwl := NewWLData;
          pwl.name := pbomdetail.name;
          mExp.SetSubject(pbomdetail.l);
          pwl.l := mExp.ToValueFloat;
          mExp.SetSubject(pbomdetail.d);
          pwl.w := mExp.ToValueFloat;
          mExp.SetSubject(pbomdetail.num);
          pwl.num := mExp.ToValueInt;
          pa := GetAccessory(pwl.name);
          pwl.group := 3;
          pwl.door_index := i+1;
          if pa <> nil then
          begin
            pwl.memo := pa.memo;
            pwl.memo2 := pa.memo2;
            pwl.memo3 := pa.memo3;
            pwl.bdfile := pa.bdfile;
            pwl.color := ToColor(pa.color, skcolor1, skcolor2, skcolor3, skcolor4);
            pwl.code := pa.wlcode;
            pwl.myunit := pa.myunit;
            if pa.isglass then pwl.isglass := 1 else pwl.isglass := 0;
            pcolorclass := GetSlidingColorClass('配件', pwl.color);
            if pcolorclass <> nil then
              pwl.code := pwl.code + '' + pcolorclass.wlcode;
            if pa.myclass = '型材' then pwl.group := 1;
            if pa.myclass = '门板' then pwl.group := 2;
          end;
          list.Add(pwl);
        end;
      end;
    end;
    if door.mUDBoxParam.wjname2 <> '' then //下横框五金
    begin
      for m := 0 to mSlidingWjBomDetailList.Count - 1 do
      begin
        pbomdetail := mSlidingWjBomDetailList[m];
        if pbomdetail.bomname = door.mUDBoxParam.wjname2 then
        begin
          pwl := NewWLData;
          pwl.name := pbomdetail.name;
          mExp.SetSubject(pbomdetail.l);
          pwl.l := mExp.ToValueFloat;
          mExp.SetSubject(pbomdetail.d);
          pwl.w := mExp.ToValueFloat;
          mExp.SetSubject(pbomdetail.num);
          pwl.num := mExp.ToValueInt;
          pa := GetAccessory(pwl.name);
          pwl.group := 3;
          pwl.door_index := i+1;
          if pa <> nil then
          begin
            pwl.memo := pa.memo;
            pwl.memo2 := pa.memo2;
            pwl.memo3 := pa.memo3;
            pwl.bdfile := pa.bdfile;
            pwl.color := ToColor(pa.color, skcolor1, skcolor2, skcolor3, skcolor4);
            pwl.code := pa.wlcode;
            pwl.myunit := pa.myunit;
            if pa.isglass then pwl.isglass := 1 else pwl.isglass := 0;
            pcolorclass := GetSlidingColorClass('配件', pwl.color);
            if pcolorclass <> nil then
              pwl.code := pwl.code + '' + pcolorclass.wlcode;
            if pa.myclass = '型材' then pwl.group := 1;
            if pa.myclass = '门板' then pwl.group := 2;
          end;
          list.Add(pwl);
        end;
      end;
    end;
  end;
  for i := 0 to mDoorsList.Count - 1 do
  begin
    if (mDataMode=1) then break;
    door := TDoorRect(mDoorsList[i]);
    for j := 0 to door.boxlist.Count - 1 do
    begin
      rb := door.boxlist[j];
      if rb.h0<=0 then continue;
      nType := 0;
      addBox(rb, door, i, nType, list);
    end;
  end;

  for i := 0 to mDoorsList.Count - 1 do
  begin
    if (mDataMode=1) then break;
    door := TDoorRect(mDoorsList[i]);
    for j := 0 to door.panellist.Count - 1 do
    begin
      pnl := door.panellist[j];
      //有竖格门芯再此 从门板中ExtraData字段提取竖格门芯
      if (pnl.extradata <> '') and (length(pnl.extradata) > 5) then
      begin
        sJsonstring := StringReplace(pnl.extradata, '^', '"', [rfReplaceAll]);
        sJson := SO(sJsonstring);
        sJson.S['L'] := floattostr(pnl.w1);
        sJson.S['H'] := floattostr(pnl.h1);
        FGObj:=GetBomObj(sJson);
        ja:= FGObj.O['CurcfgObj'].O['mxlist']; //门芯列表
        for k:=0 to ja.AsArray.length-1 do
        begin
          oneMxs:= ja.AsArray.O[k];
          if ((oneMxs.O['subtobj'] <> nil) and (Length(oneMxs.AsString) > 5)) then
          begin
            childja := oneMxs.O['subtobj'].O['CurcfgObj'].O['mxlist'];
            for subfg:=0 to childja.AsArray.length-1 do
            begin
              subMxs := childja.AsArray.O[subfg];
              new(newpnl);
              newpnl.d0:=subMxs.D['深'];
              newpnl.d1:=subMxs.D['深'];
              newpnl.d2:=subMxs.D['深'];
              newpnl.h0:=subMxs.D['高'];
              newpnl.h1:=subMxs.D['高'];
              newpnl.h2:=subMxs.D['高'];
              newpnl.w0:=subMxs.D['宽'];
              newpnl.w1:=subMxs.D['宽'];
              newpnl.w2:=subMxs.D['宽'];
              newpnl.x0:=subMxs.D['x'];
              newpnl.x1:=subMxs.D['x'];
              newpnl.x2:=subMxs.D['x'];
              newpnl.y0:=subMxs.D['y'];
              newpnl.y1:=subMxs.D['y'];
              newpnl.y2:=subMxs.D['y'];
              newpnl.memo := '';
              newpnl.PanelType := oneMxs.S['材料'];
              newpnl.direct := oneMxs.S['direct'];
              newpnl.color := oneMxs.S['颜色'];
              newpnl.color2 :='';
              if Pos('门芯', oneMxs.S['名称']) =1 then
              begin
                // 根据门芯的物料尺寸 - 门芯的进槽值  = 门芯的见光尺寸
                // mGridItem 几均分
                // 几单门
                // k 门芯列表的第几项
                // 第 k 门芯对象
                // FGObj 总数据
                // sJson ExtraData字段
                // door 门对象
                //lObj := ResetSubMxSize(mGridItem, j, k, oneMxs, FGObj, sJson, door);
                lObj := ResetMxSize(mGridItem, j, k, oneMxs, FGObj, sJson, door);
                newpnl.h0 := newpnl.h0 - lObj.D['ch0'];
                newpnl.w0 := newpnl.w0 - lObj.D['cw0'];
                AddOneMx(door, newpnl, nHasMzhb, list);
              end
              else
              begin
                new(newMx);
                newMx.d0:=subMxs.D['深'];
                newMx.d1:=subMxs.D['深'];
                newMx.d2:=subMxs.D['深'];
                newMx.h0:=subMxs.D['高'];
                newMx.h1:=subMxs.D['高'];
                newMx.h2:=subMxs.D['高'];
                newMx.w0:=subMxs.D['宽'];
                newMx.w1:=subMxs.D['宽'];
                newMx.w2:=subMxs.D['宽'];
                newMx.x0:=subMxs.D['x'];
                newMx.x1:=subMxs.D['x'];
                newMx.x2:=subMxs.D['x'];
                newMx.y0:=subMxs.D['y'];
                newMx.y1:=subMxs.D['y'];
                newMx.y2:=subMxs.D['y'];
                newMx.h0:=oneMxs.D['高'];
                newMx.h1:=oneMxs.D['高'];
                newMx.h2:=oneMxs.D['高'];
                nType := 1;
                if (FGObj.O['CurcfgObj'].I['direc'] = 1) then
                begin
                  nType := 2;  // 横切
                  newMx.h0 := pnl.w0;
                  newMx.h1 := pnl.w0;
                  newMx.h2 := pnl.w0;
                end;
                addBox(newMx, door, i, nType, list);
              end;
            end;
          end
          else
          begin
            new(newpnl);
            newpnl.d0:=oneMxs.D['深'];
            newpnl.d1:=oneMxs.D['深'];
            newpnl.d2:=oneMxs.D['深'];
            newpnl.h0:=oneMxs.D['高'];
            newpnl.h1:=oneMxs.D['高'];
            newpnl.h2:=oneMxs.D['高'];
            newpnl.w0:=oneMxs.D['宽'];
            newpnl.w1:=oneMxs.D['宽'];
            newpnl.w2:=oneMxs.D['宽'];
            newpnl.x0:=oneMxs.D['x'];
            newpnl.x1:=oneMxs.D['x'];
            newpnl.x2:=oneMxs.D['x'];
            newpnl.y0:=oneMxs.D['y'];
            newpnl.y1:=oneMxs.D['y'];
            newpnl.y2:=oneMxs.D['y'];
            newpnl.memo := '';
            newpnl.PanelType := oneMxs.S['材料'];
            newpnl.direct := oneMxs.S['direct'];
            newpnl.color := oneMxs.S['颜色'];
            newpnl.color2 :='';
            if Pos('门芯', oneMxs.S['名称']) =1 then
            begin
              // 根据门芯的物料尺寸 - 门芯的进槽值  = 门芯的见光尺寸
              // mGridItem 几均分
              // 几单门
              // k 门芯列表的第几项
              // 第 k 门芯对象
              // FGObj 总数据
              // sJson ExtraData字段
              // door 门对象
              //lObj := ResetSubMxSize(mGridItem, j, k, oneMxs, FGObj, sJson, door);
              lObj := ResetMxSize(mGridItem, j, k, oneMxs, FGObj, sJson, door);
              newpnl.h0 := newpnl.h0 - lObj.D['ch0'];
              newpnl.w0 := newpnl.w0 - lObj.D['cw0'];
              AddOneMx(door, newpnl, nHasMzhb, list);
            end
            else
            begin
              new(newMx);
              newMx.d0:=oneMxs.D['深'];
              newMx.d1:=oneMxs.D['深'];
              newMx.d2:=oneMxs.D['深'];
              newMx.h0:=oneMxs.D['高'];
              newMx.h1:=oneMxs.D['高'];
              newMx.h2:=oneMxs.D['高'];
              newMx.w0:=oneMxs.D['宽'];
              newMx.w1:=oneMxs.D['宽'];
              newMx.w2:=oneMxs.D['宽'];
              newMx.x0:=oneMxs.D['x'];
              newMx.x1:=oneMxs.D['x'];
              newMx.x2:=oneMxs.D['x'];
              newMx.y0:=oneMxs.D['y'];
              newMx.y1:=oneMxs.D['y'];
              newMx.y2:=oneMxs.D['y'];
              newMx.h0:=pnl.h0;
              newMx.h1:=pnl.h0;
              newMx.h2:=pnl.h0;
              nType := 1;
              if (FGObj.O['CurcfgObj'].I['direc'] = 1) then
              begin
                nType := 2;  // 横切
                newMx.h0 := pnl.w0;
                newMx.h1 := pnl.w0;
                newMx.h2 := pnl.w0;
              end;
              addBox(newMx, door, i, nType, list);        // newMx rb, door 门， i， 第几个门， nType
            end;
          end;
        end;
      end
      else AddOneMx(door, pnl, nHasMzhb, list);
    end;
  end;
  //定款门按照单门输出
  for i := 0 to mDoorsList.Count - 1 do
  begin
    if (mDataMode=0) then break;
    door := TDoorRect(mDoorsList[i]);

    pwl := NewWLData;
    pwl.name := mSlidingParam.name;
    pwl.color := door.mVBoxColor;
    pwl.num := 1;
    pwl.memo := mSlidingParam.memo;
    pwl.l := door.doorh;
    pwl.w := door.doorw;
    pwl.group := 2;
    list.Add(pwl);
  end;

  //自选配件
  for i := 0 to OptionalAccList.Count - 1 do
  begin
    opa := OptionalAccList[i];
    pwl := NewWLData;
    pwl.name := opa.name;
    pwl.code := pwl.code;
    pwl.color := '';
    pcolorclass := GetSlidingColorClass('配件', pwl.color);
    if pcolorclass <> nil then
      pwl.code := pwl.code + '' + pcolorclass.wlcode;
    pwl.l := 0;
    pwl.w := 0;
    pwl.h := 0;
    pwl.num := opa.num;
    pwl.group := 3;
    pa := GetAccessory(pwl.name);
    if pa <> nil then
    begin
      pwl.memo := pa.memo;
      pwl.memo2 := pa.memo2;
      pwl.memo3 := pa.memo3;
      pwl.bdfile := pa.bdfile;
      pwl.color := ToColor(pa.color, skcolor1, skcolor2, skcolor3, skcolor4);
      pwl.code := pa.wlcode;
      pwl.myunit := pa.myunit;
      if pa.isglass then pwl.isglass := 1 else pwl.isglass := 0;
      pcolorclass := GetSlidingColorClass('配件', pwl.color);
      if pcolorclass <> nil then pwl.code := pwl.code + '' + pcolorclass.wlcode;
      if pa.myclass = '型材' then pwl.group := 1;
      if pa.myclass = '门板' then pwl.group := 2;
    end;
    //pwl.myunit := '条';
    list.Add(pwl);
    mExp.AddVariable('$上轨长度', '', FloatToStr(pwl.l), '', '');
  end;
  for i := 0 to list2.Count - 1 do
  begin
    list.Add(list2[i]);
  end;
  list2.Clear;
  Result := '';
  j := 0;
  for i := 0 to list.Count - 1 do
  begin
    pwl := list[i];
    if mCfglist.count <> 0 then
    begin
      cfg := GetBomCfg(pwl);
      if cfg=nil then continue;
      pwl.name :=cfg.bomname;
      pwl.myunit :=cfg.munit;
    end;
    if pwl.num <= 0 then continue;
    inc(j);
    // EscapeBracket
    str := Format('<Item DoorName="%s" DoorIndex="%d" PanelNum="%d" PanelIndex="%d" Code="%s" Name="%s" Color="%s" '+
    'Di="%s" Num="%d" L="%.2f" W="%.2f" HH1="%.2f" WW1="%.2f" L0="%.2f" W0="%.2f" L1="%.2f" W1="%.2f" L2="%.2f" '+
    'W2="%.2f" H="%.2f" Unit="%s" Group="%d" Memo="%s" Memo2="%s" Memo3="%s" Bomsize="%.2f" Glass="%d" BDFILE="%s" Fzl="%.2f" Detail="%s"/>'
      , [pwl.doorname, pwl.door_index, pwl.pnl_num, pwl.pnl_index, pwl.code, pwl.name, pwl.color, pwl.direct, pwl.num, pwl.l, pwl.w,pwl.hh1, pwl.ww1, pwl.l0, pwl.w0,pwl.l1, pwl.w1,pwl.l2, pwl.w2, pwl.h, pwl.myunit, pwl.group, pwl.memo, pwl.memo2, pwl.memo3, pwl.bomsize, pwl.isglass, pwl.bdfile,pwl.fzl, pwl.detail]);
    Result := Result + str;
  end;
  for i := 0 to list.Count - 1 do
  begin
    pwl := list[i];
	  pwl.ono := '';
	  pwl.gno := '';
	  pwl.hno := '';
	  pwl.code := '';
	  pwl.name := '';
	  pwl.color := '';
	  pwl.direct := '';
	  pwl.myunit := '';
	  pwl.memo := '';
	  pwl.doorname := '';
	  pwl.memo2 := '';
	  pwl.memo3 := '';
	  pwl.bdfile := '';
    pwl.detail := '';
    dispose(pwl);
  end;
  list.Clear;
  FreeAndNil(list);
  list2.Clear;
  FreeAndNil(list2);
end;
// 计算门芯的 插件进值， 用来计算 见光参数。
function TLocalObject.ResetSubMxSize(mGridItem, j, k: Integer; oneMxs, FGObj, sJson:ISuperObject;door:TDoorRect):ISuperObject;
Var
  outData, hbox, hsubbox : ISuperObject;
  nIndex, nSubIndex :Integer;
  ss1, subss1: string;
  U1, D1, M1, S1, SM1, tmp: single;
  ch0, cw0: single;
begin
  Result := nil;
  outData:= TSuperObject.Create();
  outData.D['cw0'] := 0;
  outData.D['ch0'] := 0;

  //if (mUDBoxParam = nil) and (mVBoxParam = nil) then
  //begin
  //  Result:= outData;
  //  exit;
  //end;
  //子分格一定是竖分格
  ss1:= oneMxs.S['名称'];
  nindex := strtoint(RightStr(ss1,1));
  hbox := FGObj.O['cSBoxp'];
  hsubbox := oneMxs.O['subtobj'].O['cSBoxp'];   //Fg = k
  U1 := mUDBoxParam.ubheight - mUDBoxParam.ubthick;

  D1 := mUDBoxParam.dbheight - mUDBoxParam.dbheight;

  M1 := (hbox.D['height'] - hbox.D['thick']) / 2;

  S1 := (mVBoxParam.height) - (mVBoxParam.thick);

  SM1 := (hsubbox.D['height'] - hsubbox.D['thick']) / 2;

  ch0 := 0;
  cw0 := 0;
  if (FGObj.O['CurcfgObj'].I['direc'] = 1) then // 外层是横分格
  begin
    tmp := SM1;
    SM1 := M1;
    M1 := tmp;
  end;
  if (mGridItem = 0) then // 0 单分格
  begin
    // 最上格的时候减量为上横插槽值和横中横插槽值
    if (sJson.I['nType'] = 2) then
    begin
      if (nIndex = 1) then ch0 := D1 + SM1
      else ch0 := U1 + SM1
    end
    else if (sJson.I['nType'] = 3) then
    begin
      if (nIndex = 1)then ch0 := D1 + SM1
      else if (nIndex = 2) then ch0 := SM1 + SM1
      else ch0 := U1 + SM1
    end
    else if (sJson.I['nType'] = 4) then
    begin
      if (nIndex = 1) then ch0 := D1 + SM1
      else if ((nIndex = 2) or (nIndex = 3)) then ch0 := SM1 + SM1
      else ch0 := U1 + SM1
    end;
  end
  else   // 两均分 // 三均分 // 四均分 // 五均分
  begin
    // j =  PanelIndex
    if ((j = 0) and (nIndex = 1)) then ch0 := D1 + SM1
    else if ((j = mGridItem) and (nIndex = sJson.I['nType'])) then
      ch0 := U1 + SM1
    else
      ch0 := SM1 + SM1
  end;
  if ((nSubIndex = 1) or (nSubIndex = sJson.I['nType'])) then
    cw0 := S1 + M1   // 第一个竖列，或者最后一竖列都是 竖框 +一个中横框减量
  else
    cw0 := M1 + M1;
  outData.D['cw0'] := cw0;
  outData.D['ch0'] := ch0;
  Result := outData;
end;
function TLocalObject.ResetMxSize(mGridItem, j, k: Integer; oneMxs, FGObj, sJson:ISuperObject;door:TDoorRect):ISuperObject;
Var
  outData, hbox, hsubbox : ISuperObject;
  nIndex, nSubIndex :Integer;
  ss1, subss1: string;
  U1, D1, M1, S1, SM1, tmp: single;
  ch0, cw0: single;
begin
  Result := nil;
  outData:= TSuperObject.Create();
  outData.D['cw0'] := 0;
  outData.D['ch0'] := 0;

  //if (mUDBoxParam = nil) and (mVBoxParam = nil) then
  //begin
  //  Result:= outData;
  //  exit;
  //end;
  //子分格一定是竖分格
  ss1:= oneMxs.S['名称'];
  if ss1= '' then nindex :=0
  else nindex :=strtoint(RightStr(ss1,1));
  hbox := FGObj.O['cSBoxp'];

  U1 := mUDBoxParam.ubheight - mUDBoxParam.ubthick;

  D1 := mUDBoxParam.dbheight - mUDBoxParam.dbheight;

  M1 := (hbox.D['height'] - hbox.D['thick']) / 2;

  S1 := (mVBoxParam.height) - (mVBoxParam.thick);

  ch0 := 0;
  cw0 := 0;
  if (FGObj.O['CurcfgObj'].I['direc'] = 1) then // 当前横分格
  begin
    if ((j = 0) and (nIndex = 1)) then
      ch0 := D1 + M1
    else if ((j = mGridItem) and (nIndex = sJson.I['nType'])) then
      ch0 := U1 + M1
    else
      ch0 := M1 + M1;
    cw0:= S1 * 2;
  end
  else 
  begin
    // 0 单分格
    if (mGridItem = 0) then ch0 := D1 + U1
    else
    begin
      if ((j = 0) and (nIndex = 1)) then ch0 := D1 + M1
      else if ((j = mGridItem) and (nIndex = sJson.I['nType'])) then
        ch0 := U1 + M1
      else
        ch0 := M1 + M1;
    end;

    if ((nIndex = 1) or (nIndex = sJson.I['nType'])) then cw0 := S1 + M1
    else cw0 := M1 + M1;
  end;
  outData.D['cw0'] := cw0;
  outData.D['ch0'] := ch0;
  Result := outData;
end;
//计算趟门物料
function TLocalObject.GetSlidingXomItemForBom(childxml:string; pl, ph: Integer):ISuperObject;
  function XML2JsonObj(xml:string):ISuperObject;
  var
    cjo, ja           : ISuperObject;
    //xdoc              : TXMLDocument;
    root, node, attri : IXMLNode;
    i, j              : Integer;
    xdoc:  IXMLDocument;
  begin
    Result := nil;
    try
      xdoc := XMLDoc.LoadXMLData('<?xml version="1.0" encoding="gb2312"?>'+xml);

      ja := TSuperObject.Create(stArray);
      root := xdoc.ChildNodes[1];
      for i := 0 to root.ChildNodes.Count - 1 do
      begin
        node := root.ChildNodes[i];
        cjo := TSuperObject.Create(stObject);
        cjo.I['#'] := i+1;
        for j := 0 to node.AttributeNodes.Count - 1 do
        begin
          attri := node.AttributeNodes[j];
          if attri.Text = '' then continue;
          cjo.S[attri.NodeName] := attri.Text;
          if (attri.NodeName ='Name') and (slidingdeslist.IndexOf(attri.Text) = -1) then
          slidingdeslist.Add(attri.Text);
        end;
        ja.AsArray.Add(cjo);
        cjo := nil;
      end;
      xdoc.Active := False;
      Result := ja;
    except
    end;
  end;
var xml:string;
jo, ja:ISuperObject;
i:Integer;
doorw, doorh:double;
door:TDoorRect;
begin
  Result :=nil;
  LoadFromXMLTemplate(childxml, pl, ph, True);
  SetSetDoors(True);

  doorw := mL;
  doorh := mH;
  if mDoorsList.Count>0 then
  begin
    door := TDoorRect(mDoorsList[0]);
    doorw := door.doorw;
    doorh := door.doorh;
  end;
  jo := TSuperObject.Create(stObject);
  jo.S['门框类型'] := mSlidingParam.name;
  jo.D['重叠尺寸'] := mSlidingExp.overlapnum*mSlidingParam.overlap;
  jo.D['门洞宽'] := mL;
  jo.D['门洞高'] := mH;
  jo.D['成品门宽'] := doorw;
  jo.D['成品门高'] := doorh;
  jo.I['扇数'] := mDoorsList.Count;        //单门的数量
  jo.S['DoorExtra'] := mExtra;
  jo.I['DoorType'] := 1;
  xml := Format('<Data>%s</Data>', [GetXMLBom()]);
  ja := XML2JsonObj(xml);
  jo.O['物料'] := ja;
  Result := jo;
  ja := nil;
  jo :=nil;
  SetSetDoors(False);
end;
//掩门
procedure TLocalObject.GetParamXMLBom(list: TList; str: string; doorindex:Integer; x, z, l,
  h: double);
  function NewWLData: Pointer;
  var
    pwl             : ^Doorwldata;
  begin
    new(pwl);
    FillChar(pwl^, sizeof(wldata), 0);
    pwl.ono := '';
    pwl.gno := '';
    pwl.hno := '';
    pwl.name := '';
    pwl.direct := '';
    pwl.myunit := '';
    pwl.bomtype := '';
    pwl.num := 1;
    pwl.l := 0;
    pwl.w := 0;
    pwl.h := 0;
    pwl.code := '';
    pwl.color := '';
    pwl.group := 0;
    pwl.isglass := 0;
    pwl.fbstr := '';
    pwl.memo := '';
    pwl.memo2 := '';
    pwl.memo3 := '';
    pwl.doormemo := '';
    pwl.bdfile := '';
    pwl.doorname := mPParam.name;
    pwl.is_buy := 0;
    pwl.door_index := 0;
    Result := pwl;
  end;
var p:PDoorXML;
i, t, di:Integer;
xml:string;
root, node, cnode, attri:IXMLNode;
vname, vvar:string;
ll, dd, hh:double;
pwl             : ^Doorwldata;
xdoc:IXMLDocument;
begin
  xml := '';
  for i:=0 to mDoorXMLList.Count-1 do
  begin
    p := mDoorXMLList[i];
    if str=p.name then
    begin
      xml := p.xml;
      break;
    end;
  end;
  if xml = '' then exit;
  try
    mExp.ClearVarList;
    xdoc := XMLDoc.LoadXMLData(xml);
    root := xdoc.ChildNodes[1];
    node := root.ChildNodes.FindNode('变量列表');
    if node<>nil then
    begin
      for i:=0 to node.ChildNodes.Count-1 do
      begin
        cnode := node.ChildNodes[i];
        vname := '';
        vvar := '';
        attri := cnode.AttributeNodes.FindNode('名称');
        if attri<>nil then vname := attri.Text;
        attri := cnode.AttributeNodes.FindNode('值');
        if attri<>nil then vvar := attri.Text;
        mExp.AddVariable(vname, '', vvar, '', '');
      end;
    end;
    mExp.AddVariable('L', '', Format('%.4f', [l]), '', '');
    mExp.AddVariable('H', '', Format('%.4f', [h]), '', '');
    node := root.ChildNodes.FindNode('我的模块');
    if node<>nil then
    begin
      for i:=0 to node.ChildNodes.Count-1 do
      begin
        cnode := node.ChildNodes[i];
        attri := cnode.AttributeNodes.FindNode('输出类型');
        if (attri<>nil) and ((attri.Text='报价') or (attri.Text='无')) then continue;

        di := 0;
        attri := cnode.AttributeNodes.FindNode('DI');
        if attri<>nil then di := MyStrToInt(attri.Text);
        ll := 0;
        dd := 0;
        hh := 0;
        attri := cnode.AttributeNodes.FindNode('宽');
        if attri<>nil then
        begin
          mExp.SetSubject(attri.Text);
          ll := mExp.ToValueFloat;
        end;
        attri := cnode.AttributeNodes.FindNode('深');
        if attri<>nil then
        begin
          mExp.SetSubject(attri.Text);
          dd := mExp.ToValueFloat;
        end;
        attri := cnode.AttributeNodes.FindNode('高');
        if attri<>nil then
        begin
          mExp.SetSubject(attri.Text);
          hh := mExp.ToValueFloat;
        end;
        pwl := NewWLData;
        attri := cnode.AttributeNodes.FindNode('名称');
        if attri<>nil then pwl.name := attri.Text;
        DoorGraphSizeToBomSize(ll, dd, hh, di, pwl.l, pwl.w, pwl.h);
        attri := cnode.AttributeNodes.FindNode('Num');
        if attri<>nil then pwl.num := MyStrToInt(attri.Text);
        attri := cnode.AttributeNodes.FindNode('颜色');
        if attri<>nil then pwl.color := attri.Text;
        pwl.color := StringReplace(pwl.color, '$边框颜色', mMyVBoxColor, [rfReplaceAll]);
        attri := cnode.AttributeNodes.FindNode('备注');
        if attri<>nil then pwl.memo := attri.Text;
        attri := cnode.AttributeNodes.FindNode('BOMTYPE');
        if attri<>nil then pwl.bomtype := attri.Text;
        pwl.group := 2;
        if pwl.bomtype='玻璃' then pwl.isglass := 1;
        if (pwl.bomtype='木板') or (pwl.bomtype='玻璃') or (pwl.bomtype='百叶') or (pwl.bomtype='板材') then pwl.bomtype := '板材';
        if pwl.bomtype='型材五金' then pwl.group := 1;
        if pwl.bomtype='五金' then pwl.group := 3;
        pwl.door_index := doorindex;
        list.Add(pwl);
      end;
    end;
  finally
    xdoc := nil;
  end;
end;

procedure TLocalObject.DoorGraphSizeToBomSize(l, p, h: double;
  direct: Integer; var bl, bp, bh: double);
var
  t                 : Integer;
begin
  bl := l;
  bp := p;
  bh := h;
  if direct = 1 then                    //宽深高
  begin
    bl := l;
    bp := p;
    bh := h;
  end;
  if direct = 2 then                    //宽高深
  begin
    bl := l;
    bp := h;
    bh := p;
  end;
  if direct = 3 then                    //高宽深
  begin
    bl := h;
    bp := l;
    bh := p;
  end;
  if direct = 4 then                    //高深宽
  begin
    bl := h;
    bp := p;
    bh := l;
  end;
  if direct = 5 then                    //深宽高
  begin
    bl := p;
    bp := l;
    bh := h;
  end;
  if direct = 6 then                    //深高宽
  begin
    bl := p;
    bp := h;
    bh := l;
  end;
end;
//掩门
function TLocalObject.GetDoorsColor(name: string): PDoorsColor;
var
  i                 : Integer;
  p                 : PDoorsColor;
begin
  Result := nil;
  for i := 0 to mColorList.Count - 1 do
  begin
    p := mColorList[i];
    if (p.name = name) then
    begin
      Result := p;
      break;
    end;
  end;
end;
//掩门
function TLocalObject.GetDoorSSExp(name: string): PDoorsShutterExp;
var
  p                 : PDoorsShutterExp;
  i                 : Integer;
begin
  Result := nil;
  for i := 0 to mShutterExpList.Count - 1 do
  begin
    p := mShutterExpList[i];
    if p.PanelType = name then
    begin
      Result := p;
    end;
  end;
end;
//掩门
function TLocalObject.GetDimensionXml(x0, y0, x1, y1,
  offset, offset2: single): string;
begin
  Result := Format('<Dim X0="%.2f" Y0="%.2f" X1="%.2f" Y1="%.2f" OFFSET="%d" OFFSET2="%d" LineColor="%d" 类型="" 字体类型="%s" 字体大小="%d" 字体颜色="%d"/>'
    , [x0, y0, x1, y1, Round(offset), Round(offset), mLineColor, 'Arial', 0, mLineColor]);
end;
//掩门
function TLocalObject.GetDoorAccessory(name: string): PDoorAccessory;
var
  i                 : Integer;
  pa                : PDoorAccessory;
begin
  Result := nil;
  for i := 0 to self.mAccessoryList.Count - 1 do
  begin
    pa := mAccessoryList[i];
    if pa.name = name then
    begin
      Result := pa;
      exit;
    end;
  end;
end;

//掩门
function TLocalObject.GetHingeNum(phinge: PDoorsHinge; l, d: Integer;
  opendirect: string): Integer;
begin
  Result := 1;
  if (opendirect = '左') or (opendirect = '右') then
  begin
    if (d > phinge.min1) and (d < phinge.max1) then
    begin
      Result := phinge.num1;
    end;
    if (d > phinge.min2) and (d < phinge.max2) then
    begin
      Result := phinge.num2;
    end;
    if (d > phinge.min3) and (d < phinge.max3) then
    begin
      Result := phinge.num3;
    end;
    if (d > phinge.min4) and (d < phinge.max4) then
    begin
      Result := phinge.num4;
    end;
    if (d > phinge.min5) and (d < phinge.max5) then
    begin
      Result := phinge.num5;
    end;
  end
  else
  begin
    if (l > phinge.min1) and (l < phinge.max1) then
    begin
      Result := phinge.num1;
    end;
    if (l > phinge.min2) and (l < phinge.max2) then
    begin
      Result := phinge.num2;
    end;
    if (l > phinge.min3) and (l < phinge.max3) then
    begin
      Result := phinge.num3;
    end;
    if (l > phinge.min4) and (l < phinge.max4) then
    begin
      Result := phinge.num4;
    end;
    if (l > phinge.min5) and (l < phinge.max5) then
    begin
      Result := phinge.num5;
    end;
  end;
end;

function TLocalObject.GetCurHingeName(pcurhinge: PDoorsCurHinge;
  ct: string): string;
begin
  Result := pcurhinge.name;
end;

//掩门
function TLocalObject.GetHingeName(phinge: PDoorsHinge;
  ct: string): string;
var
jo:ISuperObject;
i, znmj:Integer;
na, t, zn:string;
begin
  Result := phinge.name;
  if phinge.alias='' then exit;
  try
    jo := SO(phinge.alias);
    for i:=0 to 99 do
    begin
      if jo.S['Na'+IntToStr(i+1)]='' then continue;
      na := jo.S['Na'+IntToStr(i+1)];
      t := jo.S['T'+IntToStr(i+1)];
      zn := jo.S['Zn'+IntToStr(i+1)];
      if zn='True' then znmj := 1 else znmj := 0;
      if (ct=t) and (mZNMJ=znmj) then
      begin
        Result := na;
        break;
      end;
    end;
  finally
    jo := nil;
  end;
end;

//掩门
function TLocalObject.GetColorClass2(bktype,color: string): PDoorsColorClass2;
var i:Integer;
p:PDoorsColorClass2;
begin
  Result := nil;
  for i:=0 to mColorClass2List.Count-1 do
  begin
    p := mColorClass2List[i];
    if (p.bktype=bktype) and (p.color=color) then
    begin
      Result := p;
      exit;
    end;
  end;
end;
//掩门
function TLocalObject.GetWjBom(name: string): PDoorsWjBom;
var
  i                 : Integer;
  pwjbom            : PDoorsWjBom;
begin
  Result := nil;
  for i := 0 to mWJBomList.Count - 1 do
  begin
    pwjbom := mWJBomList[i];
    if pwjbom.name = name then
    begin
      Result := pwjbom;
      exit;
    end;
  end;
end;
//掩门
function TLocalObject.GetJsonFaceA(door:TDoorDoorRect; var luaobj: TLuaObj; var lua: TLua;
  direct: string): string;
var
jo, ja, cjo:ISuperObject;
objstr, sx, sy:string;
i, n:Integer;
l:Real;
begin
  Result := '[]';
  with door do
  begin
  if mHingeHoleDes='' then exit;
  if (mOpenDirect='右') or (mOpenDirect='左') then l := mDoorH;
  if (mOpenDirect='上') or (mOpenDirect='下') then l := mDoorW;
  objstr := luaobj.GetHingeHoleBD(lua.LuaInstance, mHingeHoleDes, l, mOpenDirect, mHingeHoleParam);
  if objstr = '{}' then
  begin
    exit;
  end;
  jo := SO(objstr);

  n := jo['Num'].AsInteger;

  ja := TSuperObject.Create(stArray);
  for i:=0 to n-1 do
  begin
    cjo := TSuperObject.Create(stObject);
    cjo.S['Type'] := 'VHole';
    if mOpenDirect='右' then
    begin
      if direct<>'横纹' then
      begin
        sy := Format('W-%d', [jo.I['Offset']]);
        sx := jo.S['V'+IntToStr(i)];
      end else begin
        sx := Format('L-%d', [jo.I['Offset']]);
        sy := jo.S['V'+IntToStr(i)];
      end;
    end;
    if mOpenDirect='左' then
    begin
      if direct<>'横纹' then
      begin
        sy := Format('%d', [jo.I['Offset']]);
        sx := jo.S['V'+IntToStr(i)];
      end else begin
        sx := Format('%d', [jo.I['Offset']]);
        sy := jo.S['V'+IntToStr(i)];
      end;
    end;
    if mOpenDirect='上' then
    begin
      if direct<>'横纹' then
      begin
        sy := jo.S['V'+IntToStr(i)];
        sx := Format('L-%d', [jo.I['Offset']]);
      end else begin
        sx := jo.S['V'+IntToStr(i)];
        sy := Format('W-%d', [jo.I['Offset']]);
      end;
    end;
    if mOpenDirect='下' then
    begin
      if direct<>'横纹' then
      begin
        sy := jo.S['V'+IntToStr(i)];
        sx := Format('%d', [jo.I['Offset']]);
      end else begin
        sx := jo.S['V'+IntToStr(i)];
        sy := Format('%d', [jo.I['Offset']]);
      end;
    end;
    cjo.S['Y'] := sy;
    cjo.S['X'] := sx;
    cjo.S['R'] := jo.S['R'];
    if jo.S['Face']='' then cjo.S['Face'] := 'A' else cjo.S['Face'] := jo.S['Face'];
    ja.AsArray.Add(cjo);
    cjo := nil;
  end;
  jo := nil;
  objstr := ja.AsString;
  ja := nil;
  Result := StringReplace(objstr, '"', '^', [rfReplaceAll]);
  end;
end;

//掩门
function TLocalObject.GetJsonFaceB(door:TDoorDoorRect; var luaobj: TLuaObj; var lua: TLua;direct: string): string;
var objstr, sign, sx, sy:string;
ja, cjo:ISuperObject;
i, len:Integer;
begin
  Result := '[]';
  sign := '';
  with door do
  begin
  if mHandlePos<>'' then
  begin
    objstr := StringReplace(mHandlePos, '^', '"', [rfReplaceAll]);
    ja := SO(objstr);
    sign := GetHandleHoleScript(door.mHandle);//ja.S['Sign'];
    ja := nil;
  end;
  if sign<>'' then
  begin
    objstr := luaobj.GetHandleHoleBD(lua.LuaInstance, sign, mHandleW, mHandleH, mOpenDirect);
    if objstr<>'' then
    begin
      ja := SO(objstr);
      len := ja.AsArray.Length;
      for i:=0 to len-1 do
      begin
        cjo := ja.AsArray.O[i];
        cjo.S['Type'] := 'VHole';
        if mOpenDirect='右' then
        begin
          if direct<>'横纹' then
          begin
            sy := Format('%d', [Round(mHandleX+cjo.D['X'])]);
            sx := Format('%d', [Round(mHandleY+cjo.D['Y'])]);
          end else begin
            sx := Format('%d', [Round(mHandleX+cjo.D['X'])]);
            sy := Format('%d', [Round(mHandleY+cjo.D['Y'])]);
          end;
        end;
        if mOpenDirect='左' then
        begin
          if direct<>'横纹' then
          begin
            sy := Format('%d', [Round(mHandleX+cjo.D['X'])]);
            sx := Format('%d', [Round(mHandleY+cjo.D['Y'])]);
          end else begin
            sx := Format('%d', [Round(mHandleX+cjo.D['X'])]);
            sy := Format('%d', [Round(mHandleY+cjo.D['Y'])]);
          end;
        end;
        if mOpenDirect='上' then
        begin
          if direct<>'横纹' then
          begin
            sx := Format('%d', [Round(mHandleY+cjo.D['Y'])]);
            sy := Format('%d', [Round(mHandleX+cjo.D['X'])]);
          end else begin
            sy := Format('%d', [Round(mHandleY+cjo.D['Y'])]);
            sx := Format('%d', [Round(mHandleX+cjo.D['X'])]);
          end;
        end;
        if mOpenDirect='下' then
        begin
          if direct<>'横纹' then
          begin
            sx := Format('%d', [Round(mHandleY+cjo.D['Y'])]);
            sy := Format('%d', [Round(mHandleX+cjo.D['X'])]);
          end else begin
            sy := Format('%d', [Round(mHandleY+cjo.D['Y'])]);
            sx := Format('%d', [Round(mHandleX+cjo.D['X'])]);
          end;
        end;
        cjo.S['Y'] := sy;
        cjo.S['X'] := sx;
        if cjo.S['Face']='' then cjo.S['Face'] := 'B';
        cjo := nil;
      end;
      objstr := ja.AsString;
      Result := StringReplace(objstr, '"', '^', [rfReplaceAll]);
      ja := nil;
    end;
  end;
  end;
end;
//掩门
function TLocalObject.GetHandleHoleScript(s: string): string;
var i:Integer;
p:PDoorsHandle;
begin
  Result := '';
  for i:=0 to mHandleList.Count-1 do
  begin
    p := mHandleList[i];
    if p.name=s then
    begin
      Result := p.holescript;
      exit;
    end;
  end;
end;
//掩门
procedure TLocalObject.HingeHole2DoorObject(index:Integer);
var str, s:string;
i, j, n:Integer;
door:TDoorDoorRect;
jo:ISuperObject;
l:Real;
begin
  for i:=0 to mDoorsList.Count-1 do
  begin
    if (index>=0) and (index<>i) then continue;
    door := TDoorDoorRect(mDoorsList[i]);
    SetLength(door.mHHArr, 0);
    if door.mHingeHoleDes='' then continue;
    l := -1;
    if (door.mOpenDirect='左') or (door.mOpenDirect='右') then l := door.mDoorH;
    if (door.mOpenDirect='上') or (door.mOpenDirect='下') then l := door.mDoorW;
    if l<0 then continue;
    str := mLuaObj.GetHingeHoleGraph(mLua.LuaInstance, door.mHingeHoleDes, l, door.mOpenDirect, door.mHingeHoleParam);

    jo := SO(str);
    n := jo['Num'].AsInteger;
    if n<=0 then continue;

    SetLength(door.mHHArr, n);
    for j:=0 to n-1 do
    begin
      door.mHHArr[j].r := jo['R'].AsString;
      s := jo['G'].AsString;
      door.mHHArr[j].g := s[1];
      door.mHHArr[j].di := jo['DI'].AsInteger;

      door.mHHArr[j].y := jo['V'+IntToStr(j)].AsInteger;
      door.mHHArr[j].x := jo['Offset'].AsInteger;
      door.mHHArr[j].l := jo['L'].AsInteger;
      door.mHHArr[j].w := jo['W'].AsInteger;
    end;
  end;
end;

//掩门
function TLocalObject.DoorGetXMLBom(): string;
  function NewWLData: Pointer;
  var
    pwl             : Pdoorwldata;
  begin
    new(pwl);
    FillChar(pwl^, sizeof(wldata), 0);
    pwl.ono := '';
    pwl.gno := '';
    pwl.hno := '';
    pwl.name := '';
    pwl.direct := '';
    pwl.myunit := '';
    pwl.bomtype := '';
    pwl.num := 1;
    pwl.l := 0;
    pwl.w := 0;
    pwl.h := 0;
    pwl.code := '';
    pwl.color := '';
    pwl.group := 0;
    pwl.isglass := 0;
    pwl.fbstr := '';
    pwl.memo := '';
    pwl.memo2 := '';
    pwl.memo3 := '';
    pwl.doormemo := '';
    pwl.bdfile := '';
    pwl.doorname := mPParam.name;
    pwl.is_buy := 0;
    pwl.door_index := 0;
    pwl.pnl_num := 0;
    pwl.pnl_index := 0;
    Result := pwl;
  end;
  procedure FreeWLData(p:Pointer);
  var
    pwl             : Pdoorwldata;
  begin
    pwl := p;
    pwl.memo := '';
    pwl.memo2 := '';
    pwl.memo3 := '';
    pwl.doormemo := '';
    pwl.faceA := '';
    pwl.faceB := '';
    dispose(pwl);
  end;
  procedure Copy(dst, src: Pointer);
  var
    pwl1, pwl2      : Pdoorwldata;
  begin
    pwl1 := dst;
    pwl2 := src;
    pwl1^ := pwl2^;
    pwl1.memo := pwl2.memo;
    pwl1.memo2 := pwl2.memo2;
    pwl1.memo3 := pwl2.memo3;
    pwl1.doormemo := pwl2.doormemo;
  end;
  procedure AddWjBom(var list: TList; name: string; door_bh:Integer; opendirect, bktype:string);
  var
    i               : Integer;
    pwjbom          : PDoorsWjBom;
    pwjbomdetail    : PDoorsWjBomDetail;
    pwl       : Pdoorwldata;
    pa              : PDoorAccessory;
    pcolorclass2:PDoorsColorClass2;
  begin
    pwjbom := GetWjBom(name);
    if pwjbom <> nil then
    begin
      for i := 0 to mWJBomDetailList.Count - 1 do
      begin
        pwjbomdetail := mWJBomDetailList[i];
        if (pwjbomdetail.bomname = pwjbom.name)
          and ((pwjbomdetail.door_bh=0) or (pwjbomdetail.door_bh=door_bh))
          and ((pwjbomdetail.opendirect='') or (pwjbomdetail.opendirect=opendirect))
          and ((pwjbomdetail.bktype='') or (pwjbomdetail.bktype=bktype)) then
        begin
          pwl := NewWLData;
          pwl.name := pwjbomdetail.name;
          mExp.SetSubject(pwjbomdetail.l);
          pwl.l := mExp.ToValueFloat;
          mExp.SetSubject(pwjbomdetail.d);
          pwl.h := mExp.ToValueFloat;
          mExp.SetSubject(pwjbomdetail.num);
          pwl.num := mExp.ToValueInt;
          pwl.group := 3;
          pa := GetDoorAccessory(pwl.name);
          if pa <> nil then
          begin
            pwl.color := pa.color;
            pwl.memo := pa.memo;
            pwl.bdfile := pa.bdfile;
            pcolorclass2 := GetColorClass2(mPParam.name, mMyVBoxColor);
            if pcolorclass2 <> nil then
            begin
              if pa.color = '$边框配件颜色1' then
                pwl.color := pcolorclass2.bkcolor1;
              if pa.color = '$边框配件颜色2' then
                pwl.color := pcolorclass2.bkcolor2;
              if pa.color = '$边框配件颜色3' then
                pwl.color := pcolorclass2.bkcolor3;
              if pa.color = '$边框配件颜色4' then
                pwl.color := pcolorclass2.bkcolor4;
            end;///          end;
            pwl.group := 2;
            pwl.bomtype := pa.bomtype;
            if (pa.bomtype='木板') or (pa.bomtype='玻璃') or (pa.bomtype='百叶') or (pa.bomtype='板材') then
              pwl.bomtype := '板材';
            if pa.bomtype='型材五金' then
              pwl.group := 1;
            if pa.bomtype='五金' then
              pwl.group := 3;
            if pa.bomtype='玻璃' then
            begin
              pwl.isglass := 1;
            end;
          end;
          list.Add(pwl);
        end;
      end;
    end;
  end;

  procedure GetPanelBom(list:TList; bomclass, mat, color, color2, color3:string; pnll, pnlh:single);
  var i:Integer;
  p:PDoorsPanelBomDetail;
  pwl         : Pdoorwldata;
  begin
    for i:=0 to mPanelBomDetailList.Count-1 do
    begin
      p := mPanelBomDetailList[i];
      if (p.bomclass=bomclass) and (p.lmin<pnll) and (p.lmax>=pnll) and (p.hmin<pnlh) and (p.hmax>=pnlh) then
      begin
        pwl := NewWLData;
        pwl.name := p.bomname;
        pwl.bdfile := p.bdfile;
        pwl.code := '';
        pwl.color := StringReplace(p.color, '$门板颜色', color, [rfReplaceAll]);
        pwl.color := StringReplace(p.color, '$门芯颜色', color, [rfReplaceAll]);
        pwl.color := StringReplace(pwl.color, '$附加物料颜色', color2, [rfReplaceAll]);
        pwl.color := StringReplace(pwl.color, '$边框颜色', color3, [rfReplaceAll]);
        pwl.memo := p.memo;
        mExp.SetSubject(p.l);
        pwl.l := mExp.ToValueFloat;
        mExp.SetSubject(p.w);
        pwl.w := mExp.ToValueFloat;
        mExp.SetSubject(p.h);
        pwl.h := mExp.ToValueFloat;
        pwl.group := 2;
        pwl.bomtype := '型材五金';
        if (p.bomtype='木板') or (p.bomtype='玻璃') or (p.bomtype='百叶') or (p.bomtype='板材') then
          pwl.bomtype := '板材';
        if p.bomtype='型材五金' then
          pwl.group := 1;
        if p.bomtype='五金' then
          pwl.group := 3;
        if p.bomtype='玻璃' then
        begin
          pwl.isglass := 1;
        end;
        pwl.num := p.num;
        list.Add(pwl);
      end;
    end;
  end;
var
  i, j, pos, n, k, bh, ihige     : Integer;
  door0, door, door1       : TDoorDoorRect;
  pwl, pwl2         : Pdoorwldata;
  rb                : PDoorRectBox;
  pnl               : PDoorRectPanel;
  list              : TList;
  pnltype           : PDoorPanelType;
  mytype, str       : string;
  glvalue1, glvalue2, t: Real;
  hbox              : PDoorHBoxParam;
  phandle           : PDoorsHandle;
  phinge            : PDoorsHinge;
  pcurhinge         : PDoorsCurHinge;
  pssexp:PDoorsShutterExp;
  pcolorclass:PDoorsColorClass;
  h, w, h0, w0, h2, w2:single;
  opa :POptionalAcc;  //自选配件
  hExrobj, ja, cjo,cjo1,cjo2, detailobj: ISuperObject;
begin
  Result := '';
  //if not mIsSetDoors then exit;
  list := TList.Create;

  mExp.ClearVarList;
  mExp.AddVariable('$门洞高度', '', IntToStr(mH), '', '');
  mExp.AddVariable('$门洞宽度', '', IntToStr(mL), '', '');
  mExp.AddVariable('$重叠数', '', IntToStr(mPExp.capnum), '', '');
  mExp.AddVariable('$门扇数', '', IntToStr(mPExp.doornum), '', '');
  if mDoorsList.Count > 0 then
  begin
    door := TDoorDoorRect(mDoorsList[0]);
    mExp.AddVariable('$成品门宽度', '', FloatToStr(door.doorw), '', '');
    mExp.AddVariable('$成品门高度', '', FloatToStr(door.doorh), '', '');
  end;

  if mDataMode=0 then AddWjBom(list, mPParam.wjname, 0, '', mPParam.name);

  for i := 0 to mDoorsList.Count - 1 do
  begin
    if mDataMode=1 then break;
    door0 := nil;
    door1 := nil;
    if i>0 then door0 := TDoorDoorRect(mDoorsList[i-1]);
    if i<mDoorsList.Count - 1 then door1 := TDoorDoorRect(mDoorsList[i+1]);
    door := TDoorDoorRect(mDoorsList[i]);
    for j := 0 to door.panellist.Count - 1 do
    begin
      pnl := door.panellist[j];
      pnltype := GetDoorPanelType(mPParam.name, pnl.PanelType);
      if pnltype <> nil then pnl.thick := pnltype.thick else pnl.thick := 0;
    end;
    ////
    if (door1<>nil) and (mPParam.left_doorxml<>'') and (door.mOpenDirect='左') and (door1.mOpenDirect='右') then
    begin
      GetParamXMLBom(list, mPParam.left_doorxml, i+1, door.x1 - mLCap, door.y1 - mDCap, door.doorw, door.doorh);
    end
    else if (door0<>nil) and (mPParam.right_doorxml<>'') and (door0.mOpenDirect='左') and (door.mOpenDirect='右') then
    begin
      GetParamXMLBom(list, mPParam.right_doorxml, i+1, door.x1 - mLCap, door.y1 - mDCap, door.doorw, door.doorh);
    end
    else if (mPParam.doorxml<>'') then
    begin
      GetParamXMLBom(list, mPParam.doorxml, i+1, door.x1 - mLCap, door.y1 - mDCap, door.doorw, door.doorh);
    end;

    bh := Round(mPType.depth);
    if (mPType.isframe) then
    begin
      pwl := NewWLData;
      pwl.name := mPParam.name;
      pwl.l := door.doorw;
      pwl.w := door.doorh;
      pwl.h := mPType.depth;
      pwl.color := mMyVBoxColor;
      pwl.group := 4;
      pwl.memo := '';
      pwl.doormemo := door.mMemo;
      pwl.bomtype := '门框';
      //pwl.memo := mPParam.vmemo;
      pwl.direct := mPParam.vdirect;
      pwl.fbstr := mPParam.vfbstr;
      pwl.door_index := i+1;
      if mPParam.noframe_bom=0 then
      begin
      list.Add(pwl);
      end
      else FreeWLData(pwl);
    end else begin
      if door.panellist.Count>0 then
      begin
        pnl := door.panellist[0];
        pnltype := GetDoorPanelType(mPParam.name, pnl.PanelType);
        if pnltype <> nil then bh := pnltype.thick;
      end;
    end;

    mExp.AddVariable('$成品门宽度', '', FloatToStr(door.doorw), '', '');
    mExp.AddVariable('$成品门高度', '', FloatToStr(door.doorh), '', '');
    phandle := GetDoorsHandle(door.mHandle);
    if phandle <> nil then
    begin
      pwl := NewWLData;
      pwl.name := phandle.name;
      pwl.l := 1;
      pwl.w := 1;
      pwl.h := 1;
      pwl.color := '';
      pwl.group := 3;
      pwl.memo := phandle.memo;
      pwl.bomtype := phandle.bomtype;
      pwl.door_index := i+1;
      list.Add(pwl);
      AddWjBom(list, phandle.wjname, bh, door.mOpenDirect, mPParam.name);
    end;
    if length(door.mHingeHoleExtra) > 5 then
    begin
      str := StringReplace(door.mHingeHoleExtra, '^', '"', [rfReplaceAll]);
      hExrobj := SO(str);
      if hExrobj.O['门铰'] <> nil then
      begin
        ja := hExrobj.O['门铰'];
        n := ja.AsArray.Length;
        for ihige:=0 to n-1 do
        begin
          cjo := ja.AsArray.O[ihige];
          str := cjo.S['门铰类型'];
          pcurhinge := GetDoorsCurHinge(str, door.mHinge);
          if pcurhinge <> nil then
          begin
            pwl := NewWLData;
            pwl.name := GetCurHingeName(pcurhinge, door.mHingeCt);
            pwl.l := 1;
            pwl.w := 1;
            pwl.h := 1;
            pwl.color := '';
            pwl.group := 3;
            pwl.memo := pcurhinge.memo;
            pwl.memo2 :='';
            pwl.num := 1;
            pwl.bomtype := pcurhinge.bomtype;
            pwl.door_index := i+1;
            list.Add(pwl);
            for j := 0 to pwl.num - 1 do
              AddWjBom(list, pcurhinge.wjname, bh, door.mOpenDirect, mPParam.name);
          end;
        end;
      end;
    end
    else
    begin
      phinge := GetDoorsHinge(door.mHinge, mPType);
      if phinge <> nil then
      begin
        pwl := NewWLData;
        pwl.name := GetHingeName(phinge, door.mHingeCt);
        pwl.l := 1;
        pwl.w := 1;
        pwl.h := 1;
        pwl.color := '';
        pwl.group := 3;
        pwl.memo := phinge.memo;
        pwl.memo2 := door.mHingeHoleExtra;
        pwl.num := GetHingeNum(phinge, Round(door.mDoorW), Round(door.mDoorH), door.mOpenDirect);
        pwl.bomtype := phinge.bomtype;
        pwl.door_index := i+1;
        list.Add(pwl);
        for j := 0 to pwl.num - 1 do
          AddWjBom(list, phinge.wjname, bh, door.mOpenDirect, mPParam.name);
      end;
    end;

    if mPType.isframe then
    begin
      if mPParam.iscalc_framebom=1 then //计算横框竖框物料
      begin
        pwl := NewWLData;
        pwl.name := mPParam.vboxname;
        mExp.SetSubject(mPParam.vboxl);
        if phandle <> nil then
          pwl.memo := phandle.name;
        pwl.l := mExp.ToValueFloat;
        pwl.w := mPParam.vboxh;
        pwl.color := mMyVBoxColor;
        pwl.group := 1;
        pwl.h := mPType.depth;
        pwl.memo := mPParam.vmemo;
        pwl.memo := StringReplace(pwl.memo, '$竖框槽位信息', door.GetVboxKCInfo, [rfReplaceAll]);
        pwl.bomtype := mPParam.bomtype;
        pwl.direct := mPParam.vdirect;
        pwl.fbstr := mPParam.vfbstr;
        pwl.bdfile := mPParam.l_bdfile;
        pwl.is_buy := mPParam.is_buy;
        pwl.door_index := i+1;
        if mPParam.vdirect='横纹' then Swap(pwl.l, pwl.w);
        pwl2 := NewWLData;
        Copy(pwl2, pwl);
        pwl2.bdfile := mPParam.r_bdfile;
        if mPParam.noframe_bom=0 then list.Add(pwl) else FreeWLData(pwl);
        if mPParam.noframe_bom=0 then list.Add(pwl2) else FreeWLData(pwl2);

        pwl := NewWLData;
        pwl.name := mPParam.udboxname;
        mExp.SetSubject(mPParam.udboxl);
        pwl.l := mExp.ToValueFloat;

        pwl.w := mPParam.udboxh;
        pwl.color := mMyVBoxColor;
        pwl.group := 1;
        pwl.h := mPType.depth;
        pwl.memo := mPParam.udmemo;
        pwl.memo := StringReplace(pwl.memo, '$横框槽位信息', door.GetHboxKCInfo(0, nil), [rfReplaceAll]);
        pwl.bomtype := mPParam.bomtype;
        pwl.direct := mPParam.uddirect;
        pwl.fbstr := mPParam.udfbstr;
        if mPParam.uddirect='横纹' then Swap(pwl.l, pwl.w);
        pwl.bdfile := mPParam.u_bdfile;
        pwl.is_buy := mPParam.is_buy;
        pwl.door_index := i+1;
        pwl2 := NewWLData;
        Copy(pwl2, pwl);
        pwl.memo := mPParam.udmemo;
        pwl.memo := StringReplace(pwl.memo, '$横框槽位信息', door.GetHboxKCInfo(2, nil), [rfReplaceAll]);
        pwl.bdfile := mPParam.d_bdfile;
        if mPParam.noframe_bom=0 then list.Add(pwl) else FreeWLData(pwl);
        if mPParam.noframe_bom=0 then list.Add(pwl2) else FreeWLData(pwl2);
      end else begin
        pwl := NewWLData;
        pwl.name := mPParam.name;
        if phandle <> nil then
          pwl.memo := phandle.name;
        pwl.l := door.doorh-mPParam.frame_valueh;
        pwl.w := door.doorw-mPParam.frame_valuel;
        pwl.color := mMyVBoxColor;
        pwl.group := 1;
        pwl.h := mPType.depth;
        pwl.memo := mPParam.vmemo;
        pwl.bomtype := mPParam.bomtype;
        pwl.fbstr := mPParam.fbstr;
        pwl.bdfile := mPParam.bdfile;
        pwl.is_buy := mPParam.is_buy;
        pwl.door_index := i+1;
        if mPParam.noframe_bom=0 then list.Add(pwl) else FreeWLData(pwl);
      end;

      for j := 0 to door.boxlist.Count - 1 do
      begin
        rb := door.boxlist[j];
        if rb.h0<=0 then continue;
        pwl := NewWLData;
        pwl.name := rb.boxtype;
        pwl.color := rb.color;
        mExp.SetSubject(mPParam.udboxl);
        pwl.l := mExp.ToValueFloat - mPParam.udbox_hbox_value;
        pwl.w := rb.h0;
        pwl.h := rb.d0;
        pwl.group := 1;
        pwl.door_index := i+1;
        hbox := GetDoorHBoxParam(rb.boxtype);
        if hbox <> nil then
        begin
          pwl.direct := hbox.direct;
          if hbox.direct='横纹' then Swap(pwl.l, pwl.w);
          pwl.fbstr := hbox.fbstr;
          pwl.memo := hbox.memo;
          pwl.memo := StringReplace(pwl.memo, '$横框槽位信息', door.GetHboxKCInfo(1, rb), [rfReplaceAll]);
          pwl.bomtype := hbox.bomtype;
          pwl.bdfile := hbox.bdfile;
        end;
        list.Add(pwl);
        if hbox <> nil then
          AddWjBom(list, hbox.wjname, bh, door.mOpenDirect, mPParam.name);
      end;

      for j := 0 to door.panellist.Count - 1 do
      begin
        pnl := door.panellist[j];
        mExp.AddVariable('$门板高度0', '', FloatToStr(pnl.h0), '', '');
        mExp.AddVariable('$门板宽度0', '', FloatToStr(pnl.w0), '', '');
        mExp.AddVariable('$门板高度', '', FloatToStr(pnl.h1), '', '');
        mExp.AddVariable('$门板宽度', '', FloatToStr(pnl.w1), '', '');
        pnltype := GetDoorPanelType(mPParam.name, pnl.PanelType);
        mytype := '';
        if pnltype <> nil then
        begin
          mytype := pnltype.mytype;
          GetPanelBom(list, pnltype.panelbom, pnl.PanelType, pnl.color, pnl.color2, mMyVBoxColor, pnl.w1, pnl.h1);
        end;
        glvalue1 := 0;
        glvalue2 := 0;
        if mytype = '玻璃' then
        begin
          glvalue1 := mPParam.vboxjtw * 2;
          pos := door.GetPanelPosInDoor(pnl);
          if (pos = 1) then             //最下格
            glvalue2 := mPParam.hboxjtw + mPParam.udboxjtw;
          if (pos = 2) then             //最上格
            glvalue2 := mPParam.hboxjtw + mPParam.udboxjtw;
          if (pos = 0) then             //中间格
            glvalue2 := mPParam.hboxjtw * 2;
          if (pos = -1) then
            glvalue2 := mPParam.udboxjtw * 2;
        end;
        if mytype = '百叶' then
        begin
          cjo := TSuperObject.Create();
          cjo1 := TSuperObject.Create();
          cjo2 := TSuperObject.Create();
          pssexp := self.GetDoorSSExp(pnl.PanelType);
          h := pnl.h1;
          w := pnl.w1;
          h0 := pnl.h0;    //可见
          w0 := pnl.w0;
          h2 := pnl.h2;    //投影
          w2 := pnl.w2;
          if pssexp.height <> 0 then
          begin
            //物料百叶尺寸
            n := Trunc((h - 0 - glvalue2) / pssexp.height);
            t := (h - 0 - glvalue2) - pssexp.height * n;
            if t > pssexp.minheight then
            begin
              n := n + 1;
            end
            else
              t := 0;
            pwl := NewWLData;
            pwl.name := pnl.PanelType; //'门芯';
            pwl.color := pnl.color;
            pwl.code := '';
            pwl.l := (w - 0 - glvalue1);   //物料尺寸
            pwl.w := h - 0 - glvalue2;
            pwl.l1 := w;   //物料尺寸
            pwl.w1 := h;
            pwl.hh1 := glvalue1;    //差值
            pwl.ww1 := glvalue2; 
            cjo:=nil;
            cjo.I['num']:=n;
            cjo.S['l']:= Format('%.2f',[(w - 0 - glvalue1)]);
            cjo.S['w']:= Format('%.2f',[pssexp.height]);
            if t <> 0 then cjo.S['lw']:= Format('%.2f',[t])
            else cjo.S['lw']:= '0';
            detailobj.O['物料']:=cjo;

            //可视尺寸百叶
            n := Trunc((h0 - 0 - glvalue2) / pssexp.height);
            t := (h0 - 0 - glvalue2) - pssexp.height * n;
            if t > pssexp.minheight then
            begin
              n := n + 1;
            end
            else
              t := 0;
            pwl.l0 := w0;   //可见尺寸
            pwl.w0 := h0;
            cjo.I['num']:=n;
            cjo.S['l']:= Format('%.2f',[(w0- 0 - glvalue1)]);
            cjo.S['w']:= Format('%.2f',[pssexp.height]);
            if t <> 0 then cjo.S['lw']:= Format('%.2f',[t])
            else cjo.S['lw']:= '0';
            detailobj.O['可视']:=cjo;

            //投影尺寸百叶
            n := Trunc((h2 - 0 - glvalue2) / pssexp.height);
            t := (h2 - 0 - glvalue2) - pssexp.height * n;
            if t > pssexp.minheight then
            begin
              n := n + 1;
            end
            else
              t := 0;
            pwl.l2 := w2;   //物料尺寸
            pwl.w2 := h2;
            cjo.I['num']:=n;
            cjo.S['l']:= Format('%.2f',[(w2- 0 - glvalue1)]);    //普通的
            cjo.S['w']:= Format('%.2f',[pssexp.height]);
            if t <> 0 then cjo.S['lw']:= Format('%.2f',[t])
            else cjo.S['lw']:= '0';
            detailobj.O['投影']:=cjo;
            str := detailobj.AsString;
            cjo:=nil;
            cjo1:=nil;
            cjo2:=nil;

            pcolorclass := GetColorClass('门芯', pnl.color);
            pwl.direct := pnl.direct;
            pwl.num := 1;
            pwl.group := 2;
            pwl.door_index := i+1;
            pwl.pnl_num := door.panellist.Count;
            pwl.pnl_index := j;
            if pnltype <> nil then
            begin
              pwl.memo := pnltype.memo;
              pwl.memo2 := pnltype.memo2;
              pwl.memo3 := pnltype.memo3;
              pwl.h := pnltype.thick;
              pwl.w := pwl.w - pnltype.lfb;
              pwl.l := pwl.l - pnltype.hfb;
              pwl.bomtype := pnltype.bomtype;
              pwl.fbstr := pnltype.fbstr;
              pwl.bdfile := pnltype.bdfile;
              pwl.is_buy := pnltype.is_buy;
            end;
            //pwl.myunit := '块';
            list.Add(pwl);
          end
          else if pssexp.width <> 0 then
          begin
            pwl := NewWLData;
            pwl.name := pnl.PanelType; //'门芯';
            pwl.color := pnl.color;
            pwl.code := '';
            //物料尺寸
            n := Trunc((w - 0 - glvalue1) / pssexp.width);
            t := (w - 0 - glvalue1) - pssexp.width * n;
            if t > pssexp.minwidth then
            begin
              n := n + 1;
            end
            else
              t := 0;
            pwl.l := (h - 0 - glvalue2);
            pwl.w := w - 0 - glvalue1;
            pwl.l1 := h;
            pwl.w1 := w;
            pwl.hh1 := glvalue2;
            pwl.ww1 := glvalue1;
            cjo.I['num']:=n;
            cjo.S['l']:= Format('%.2f',[w - 0 - glvalue1]);
            cjo.S['w']:= Format('%.2f',[pssexp.width]);
            if t <> 0 then cjo.S['lw']:= Format('%.2f',[t])
            else cjo.S['lw']:= '0';
            detailobj.O['物料']:=cjo;

            //可见尺寸
            n := Trunc((w0 - 0 - glvalue1) / pssexp.width);
            t := (w0 - 0 - glvalue1) - pssexp.width * n;
            if t > pssexp.minwidth then
            begin
              n := n + 1;
            end
            else
              t := 0;
            pwl.l0 := h0;
            pwl.w0 := w0;

            cjo1.I['num']:=n;
            cjo1.S['l']:= Format('%.2f',[w0- 0 - glvalue1]);
            cjo1.S['w']:= Format('%.2f',[pssexp.width]);
            if t <> 0 then cjo1.S['lw']:= Format('%.2f',[t])
            else cjo1.S['lw']:= '0';
            detailobj.O['可见']:=cjo1;

            //投影尺寸
            n := Trunc((w2 - 0 - glvalue1) / pssexp.width);
            t := (w2 - 0 - glvalue1) - pssexp.width * n;
            if t > pssexp.minwidth then
            begin
              n := n + 1;
            end
            else
              t := 0;
            pwl.l2 := h2;
            pwl.w2 := w2;

            cjo2.I['num']:=n;
            cjo2.S['l']:= Format('%.2f',[w2- 0 - glvalue1]);
            cjo2.S['w']:= Format('%.2f',[pssexp.width]);
            if t <> 0 then cjo2.S['lw']:= Format('%.2f',[t])
            else cjo2.S['lw']:= '0';
            detailobj.O['投影']:=cjo2;
            str := detailobj.AsString;
            cjo:=nil;
            cjo1:=nil;
            cjo2:=nil;
            pwl.detail := StringReplace(str, '"', '^', [rfReplaceAll]);

            pcolorclass := GetColorClass('门芯', pnl.color);
            pwl.direct := pnl.direct;
            pwl.num := 1;
            pwl.group := 2;
            pwl.door_index := i+1;
            pwl.pnl_num := door.panellist.Count;
            pwl.pnl_index := j;
            if pnltype <> nil then
            begin
              pwl.memo := pnltype.memo;
              pwl.memo2 := pnltype.memo2;
              pwl.memo3 := pnltype.memo3;
              pwl.h := pnltype.thick;
              pwl.w := pwl.w - pnltype.lfb;
              pwl.l := pwl.l - pnltype.hfb;
              pwl.bomtype := pnltype.bomtype;
              pwl.fbstr := pnltype.fbstr;
              pwl.bdfile := pnltype.bdfile;
              pwl.is_buy := pnltype.is_buy;
            end;
            //pwl.myunit := '块';
            list.Add(pwl);
          end;
        end
        else
        begin
          pwl := NewWLData;
          pwl.group := 2;
          pwl.name := pnl.PanelType;
          pwl.direct := pnl.direct;
          pwl.color := pnl.color;
          pwl.w := pnl.w1 - glvalue1;
          pwl.l := pnl.h1 - glvalue2;
          pwl.ww1:= glvalue1;
          pwl.hh1 := glvalue2;
          pwl.w1 := pnl.w1;
          pwl.l1 := pnl.h1;
          pwl.w0 := pnl.w0;
          pwl.l0 := pnl.h0;
          pwl.w2 := pnl.w2;
          pwl.l2 := pnl.h2;


          pwl.door_index := i+1;
          pwl.pnl_num := door.panellist.Count;
          pwl.pnl_index := j;
          if mytype='玻璃' then pwl.isglass := 1;
          if pnltype <> nil then
          begin
            pwl.memo := pnltype.memo;
            pwl.memo2 := pnltype.memo2;
            pwl.memo3 := pnltype.memo3;
            pwl.h := pnltype.thick;
            pwl.w := pwl.w - pnltype.lfb;
            pwl.l := pwl.l - pnltype.hfb;
            if pnltype.direct = '横纹' then Swap(pwl.l, pwl.w);
            pwl.bomtype := pnltype.bomtype;
            pwl.fbstr := pnltype.fbstr;
            pwl.bdfile := pnltype.bdfile;
            pwl.is_buy := pnltype.is_buy;
          end;
          list.Add(pwl);
        end;
      end;
    end                                 //frame
    else
    begin
      for j := 0 to door.panellist.Count - 1 do
      begin
        pnl := door.panellist[j];
        pnltype := GetDoorPanelType(mPParam.name, pnl.PanelType);
        mytype := '';
        if pnltype <> nil then
        begin
          mytype := pnltype.mytype;
          GetPanelBom(list, pnltype.panelbom, pnl.PanelType, pnl.color, pnl.color2, mMyVBoxColor, pnl.w1, pnl.h1);
        end;
        glvalue1 := 0;
        glvalue2 := 0;
        pwl := NewWLData;
        pwl.faceA := GetJsonFaceA(door, mLuaObj, mLua, pnl.direct);
        pwl.faceB := GetJsonFaceB(door, mLuaObj, mLua, pnl.direct);
        pwl.group := 2;
        pwl.name := pnl.PanelType;
        pwl.direct := pnl.direct;
        pwl.color := pnl.color;
        pwl.w := pnl.w1 - glvalue1;
        pwl.l := pnl.h1 - glvalue2;
        pwl.ww1:= glvalue1;
        pwl.hh1 := glvalue2;
        pwl.w1 := pnl.w1;
        pwl.l1 := pnl.h1;
        pwl.w0 := pnl.w0;
        pwl.l0 := pnl.h0;
        pwl.w2 := pnl.w2;
        pwl.l2 := pnl.h2;

        pwl.door_index := i+1;
        pwl.pnl_num := door.panellist.Count;
        pwl.pnl_index := j;
        if mytype='玻璃' then pwl.isglass := 1;
        if pnltype <> nil then
        begin
          pwl.memo := pnltype.memo;
          pwl.memo2 := pnltype.memo2;
          pwl.memo3 := pnltype.memo3;
          pwl.h := pnltype.thick;
          pwl.w := pwl.w - pnltype.lfb;
          pwl.l := pwl.l - pnltype.hfb;
          if pnltype.direct = '横纹' then Swap(pwl.l, pwl.w);
          pwl.bomtype := pnltype.bomtype;
          pwl.fbstr := pnltype.fbstr;
          pwl.bdfile := pnltype.bdfile;
          pwl.is_buy := pnltype.is_buy;
        end;
        if door.panellist.Count=1 then pwl.doormemo := door.mMemo;
        if phandle <> nil then
          pwl.memo := phandle.name;
        list.Add(pwl);
      end;
    end;
  end;

  //定款门按照单门输出
  for i := 0 to mDoorsList.Count - 1 do
  begin
    if (mDataMode=0) then break;
    door := TDoorDoorRect(mDoorsList[i]);

    pwl := NewWLData;
    pwl.name := mPParam.name;
    pwl.color := mMyVBoxColor;
    pwl.num := 1;
    pwl.memo := mPParam.vmemo;
    pwl.l := door.doorh;
    pwl.w := door.doorw;
    pwl.group := 2;
    pwl.bomtype := '门框';
    list.Add(pwl);
  end;

  //自选配件
  for i := 0 to OptionalAccList.Count - 1 do
  begin
    opa := OptionalAccList[i];
    pwl := NewWLData;
    pwl.name := opa.name;
    pwl.code := pwl.code;
    pwl.color := '';
    pwl.l := 0;
    pwl.w := 0;
    pwl.h := 0;
    pwl.num := opa.num;
    pwl.group := 3;
    pwl.bomtype := '五金';
    list.Add(pwl);
  end;

  Result := '';
  j := 0;
  for i := 0 to list.Count - 1 do
  begin
    pwl := list[i];
    if pwl.num <= 0 then continue;
    inc(j);
    //EscapeBracket
    str := Format('<Item DoorName="%s" DoorMemo="%s" DoorIndex="%d" PanelNum="%d" PanelIndex="%d" Code="%s" Name="%s" Color="%s" Di="%s" Num="%d" L="%.2f" W="%.2f" L0="%.2f" W0="%.2f"' +
      ' L1="%.2f" W1="%.2f" L2="%.2f" W2="%.2f" HH="%.2f" WW="%.2f" H="%.2f" Detail="%s" '
        , [pwl.doorname, pwl.doormemo, pwl.door_index, pwl.pnl_num, pwl.pnl_index, pwl.code, pwl.name, pwl.color, pwl.direct, pwl.num, pwl.l, pwl.w, pwl.l0, pwl.w0, pwl.l1, pwl.w1, pwl.l2, pwl.w2,pwl.hh1, pwl.ww1, pwl.h, pwl.detail]);
    str := str+Format('Unit="%s" Group="%d" Bomtype="%s" FBStr="%s" Memo="%s" Memo2="%s" Memo3="%s" Glass="%d" BDFILE="%s" IsBuy="%d" FaceA="%s" FaceB="%s"/>'
        , [pwl.myunit, pwl.group, pwl.bomtype, pwl.fbstr, pwl.memo, pwl.memo2, pwl.memo3, pwl.isglass, pwl.bdfile, pwl.is_buy, pwl.faceA, pwl.faceB]);
    Result := Result + str;
  end;

  for i := 0 to list.Count - 1 do
  begin
    FreeWLData(list[i]);
  end;
  list.Clear;
  FreeAndNil(list);
end;
//掩门
procedure TLocalObject.DoorRecalcDoor(door:TDoorDoorRect; t1, t2, tt1, tt2:single; m:Integer);
var n, j:Integer;
  rb                : PRectBox;
  pnl               : PRectPanel;
begin
{
单格
两均分
三均分
四均分
五均分
====================
两均分(下格固定)
两均分(上格固定)
三均分(中间格固定)
三均分(上两格固定)
三均分(下两格固定)
}

  if (mGridItem=6) and (door.panellist.Count=2) then    //两均分(下格固定)
  begin
    for j:=0 to door.boxlist.Count-1 do
    begin
      rb := door.boxlist[j];
      rb.y0 := rb.y0 + (t2/1)*(0+0) + tt2*m;
      rb.y1 := rb.y1 + (t2/1)*(0+0) + tt2*m;
      rb.y2 := rb.y2 + (t2/1)*(0+0) + tt2*m;
      rb.x0 := rb.x0 + tt1*m;
      rb.x1 := rb.x1 + tt1*m;
      rb.x2 := rb.x2 + tt1*m;
      rb.w0 := rb.w0 + t1;
      rb.w1 := rb.w1 + t1;
      rb.w2 := rb.w2 + t1;
    end;
    for j:=0 to door.panellist.Count-1 do
    begin
      pnl := door.panellist[j];
      n := 0;
      if j=1 then pnl.h0 := pnl.h0 + (t2/1);
      pnl.y0 := pnl.y0 + (t2/1)*n + tt2*m;
      if j=1 then pnl.h1 := pnl.h1 + (t2/1);
      pnl.y1 := pnl.y1 + (t2/1)*n + tt2*m;
      if j=1 then pnl.h2 := pnl.h2 + (t2/1);
      pnl.y2 := pnl.y2 + (t2/1)*n + tt2*m;
      pnl.x0 := pnl.x0 + tt1*m;
      pnl.x1 := pnl.x1 + tt1*m;
      pnl.x2 := pnl.x2 + tt1*m;
      pnl.w0 := pnl.w0 + t1;
      pnl.w1 := pnl.w1 + t1;
      pnl.w2 := pnl.w2 + t1;
    end;
  end
  else if (mGridItem=8) and (door.panellist.Count=3) then    //三格，中间格保持不变
  begin
    for j:=0 to door.boxlist.Count-1 do
    begin
       rb := door.boxlist[j];
       rb.y0 := rb.y0 + (t2/2)*(0+1) + tt2*m;
       rb.y1 := rb.y1 + (t2/2)*(0+1) + tt2*m;
       rb.y2 := rb.y2 + (t2/2)*(0+1) + tt2*m;
       rb.x0 := rb.x0 + tt1*m;
       rb.x1 := rb.x1 + tt1*m;
       rb.x2 := rb.x2 + tt1*m;
       rb.w0 := rb.w0 + t1;
       rb.w1 := rb.w1 + t1;
       rb.w2 := rb.w2 + t1;
     end;
     for j:=0 to door.panellist.Count-1 do
     begin
       pnl := door.panellist[j];
       n := j;
       if j=2 then n := 1;
       if j<>1 then pnl.h0 := pnl.h0 + (t2/2);
       pnl.y0 := pnl.y0 + (t2/2)*n + tt2*m;
       if j<>1 then pnl.h1 := pnl.h1 + (t2/2);
       pnl.y1 := pnl.y1 + (t2/2)*n + tt2*m;
       if j<>1 then pnl.h2 := pnl.h2 + (t2/2);
       pnl.y2 := pnl.y2 + (t2/2)*n + tt2*m;
       pnl.x0 := pnl.x0 + tt1*m;
       pnl.x1 := pnl.x1 + tt1*m;
       pnl.x2 := pnl.x2 + tt1*m;
       pnl.w0 := pnl.w0 + t1;
       pnl.w1 := pnl.w1 + t1;
       pnl.w2 := pnl.w2 + t1;
     end;
   end else if (mGridItem=7) and (door.panellist.Count=2) then     //两均分(上格固定)
   begin
      for j:=0 to door.boxlist.Count-1 do
      begin
        rb := door.boxlist[j];
        rb.y0 := rb.y0 + (t2/1)*(0+1) + tt2*m;
        rb.y1 := rb.y1 + (t2/1)*(0+1) + tt2*m;
        rb.y2 := rb.y2 + (t2/1)*(0+1) + tt2*m;
        rb.x0 := rb.x0 + tt1*m;
        rb.x1 := rb.x1 + tt1*m;
        rb.x2 := rb.x2 + tt1*m;
        rb.w0 := rb.w0 + t1;
        rb.w1 := rb.w1 + t1;
        rb.w2 := rb.w2 + t1;
      end;
      for j:=0 to door.panellist.Count-1 do
      begin
        pnl := door.panellist[j];
        n := 0;
        if j=1 then n := 1;
        if j=0 then pnl.h0 := pnl.h0 + (t2/1);
        pnl.y0 := pnl.y0 + (t2/1)*n + tt2*m;
        if j=0 then pnl.h1 := pnl.h1 + (t2/1);
        pnl.y1 := pnl.y1 + (t2/1)*n + tt2*m;
        if j=0 then pnl.h2 := pnl.h2 + (t2/1);
        pnl.y2 := pnl.y2 + (t2/1)*n + tt2*m;
        pnl.x0 := pnl.x0 + tt1*m;
        pnl.x1 := pnl.x1 + tt1*m;
        pnl.x2 := pnl.x2 + tt1*m;
        pnl.w0 := pnl.w0 + t1;
        pnl.w1 := pnl.w1 + t1;
        pnl.w2 := pnl.w2 + t1;
      end;
   end else if (mGridItem=9) and (door.panellist.Count=3) then      //三均分(上两格固定)
   begin
    for j:=0 to door.boxlist.Count-1 do
    begin
       rb := door.boxlist[j];
       rb.y0 := rb.y0 + (t2/1)*(0+1) + tt2*m;
       rb.y1 := rb.y1 + (t2/1)*(0+1) + tt2*m;
       rb.y2 := rb.y2 + (t2/1)*(0+1) + tt2*m;
       rb.x0 := rb.x0 + tt1*m;
       rb.x1 := rb.x1 + tt1*m;
       rb.x2 := rb.x2 + tt1*m;
       rb.w0 := rb.w0 + t1;
       rb.w1 := rb.w1 + t1;
       rb.w2 := rb.w2 + t1;
     end;
     for j:=0 to door.panellist.Count-1 do
     begin
       pnl := door.panellist[j];
       n := 0;
       if j>0 then n := 1;
       if j=0 then pnl.h0 := pnl.h0 + (t2/1);
       pnl.y0 := pnl.y0 + (t2/1)*n + tt2*m;
       if j=0 then pnl.h1 := pnl.h1 + (t2/1);
       pnl.y1 := pnl.y1 + (t2/1)*n + tt2*m;
       if j=0 then pnl.h2 := pnl.h2 + (t2/1);
       pnl.y2 := pnl.y2 + (t2/1)*n + tt2*m;
       pnl.x0 := pnl.x0 + tt1*m;
       pnl.x1 := pnl.x1 + tt1*m;
       pnl.x2 := pnl.x2 + tt1*m;
       pnl.w0 := pnl.w0 + t1;
       pnl.w1 := pnl.w1 + t1;
       pnl.w2 := pnl.w2 + t1;
     end;
   end else if (mGridItem=10) and (door.panellist.Count=3) then     //三均分(上两格固定)
   begin
    for j:=0 to door.boxlist.Count-1 do
    begin
       rb := door.boxlist[j];
       rb.y0 := rb.y0 + (t2/1)*(0+0) + tt2*m;
       rb.y1 := rb.y1 + (t2/1)*(0+0) + tt2*m;
       rb.y2 := rb.y2 + (t2/1)*(0+0) + tt2*m;
       rb.x0 := rb.x0 + tt1*m;
       rb.x1 := rb.x1 + tt1*m;
       rb.x2 := rb.x2 + tt1*m;
       rb.w0 := rb.w0 + t1;
       rb.w1 := rb.w1 + t1;
       rb.w2 := rb.w2 + t1;
     end;
     for j:=0 to door.panellist.Count-1 do
     begin
       pnl := door.panellist[j];
       n := 0;
       if j=2 then pnl.h0 := pnl.h0 + (t2/1);
       pnl.y0 := pnl.y0 + (t2/1)*n + tt2*m;
       if j=2 then pnl.h1 := pnl.h1 + (t2/1);
       pnl.y1 := pnl.y1 + (t2/1)*n + tt2*m;
       if j=2 then pnl.h2 := pnl.h2 + (t2/1);
       pnl.y2 := pnl.y2 + (t2/1)*n + tt2*m;
       pnl.x0 := pnl.x0 + tt1*m;
       pnl.x1 := pnl.x1 + tt1*m;
       pnl.x2 := pnl.x2 + tt1*m;
       pnl.w0 := pnl.w0 + t1;
       pnl.w1 := pnl.w1 + t1;
       pnl.w2 := pnl.w2 + t1;
     end;
   end else begin
     for j:=0 to door.boxlist.Count-1 do
     begin
       rb := door.boxlist[j];
       rb.y0 := rb.y0 + (t2/door.panellist.Count)*(j+1) + tt2*m;
       rb.y1 := rb.y1 + (t2/door.panellist.Count)*(j+1) + tt2*m;
       rb.y2 := rb.y2 + (t2/door.panellist.Count)*(j+1) + tt2*m;
       rb.x0 := rb.x0 + tt1*m;
       rb.x1 := rb.x1 + tt1*m;
       rb.x2 := rb.x2 + tt1*m;
       rb.w0 := rb.w0 + t1;
       rb.w1 := rb.w1 + t1;
       rb.w2 := rb.w2 + t1;
     end;
     for j:=0 to door.panellist.Count-1 do
     begin
       pnl := door.panellist[j];
       pnl.h0 := pnl.h0 + (t2/door.panellist.Count);
       pnl.y0 := pnl.y0 + (t2/door.panellist.Count)*j + tt2*m;
       pnl.h1 := pnl.h1 + (t2/door.panellist.Count);
       pnl.y1 := pnl.y1 + (t2/door.panellist.Count)*j + tt2*m;
       pnl.h2 := pnl.h2 + (t2/door.panellist.Count);
       pnl.y2 := pnl.y2 + (t2/door.panellist.Count)*j + tt2*m;
       pnl.x0 := pnl.x0 + tt1*m;
       pnl.x1 := pnl.x1 + tt1*m;
       pnl.x2 := pnl.x2 + tt1*m;
       pnl.w0 := pnl.w0 + t1;
       pnl.w1 := pnl.w1 + t1;
       pnl.w2 := pnl.w2 + t1;
     end;
   end;
end;
//掩门
procedure TLocalObject.DoorLoadFromXMLTemplate(xml: string; l, h:Integer; resize: boolean);
var
  root, Node, cnode, cnode2, attri: IXMLNode;
  i, j, m, n           : Integer;
  door              : TDoorDoorRect;
  rb                : PDoorRectBox;
  pnl               : PDoorRectPanel;
  ll, hh, t1, t2, tt1, tt2, t:single;

  pcolor            : PDoorsColor;
  pexp              : PDoorsExp;
  ptype             : PDoorsType;
  pparam            : PDoorsParam;
  php               : PDoorHBoxParam;
  ppt               : PDoorPanelType;
  pa                : PDoorAccessory;
  pcolorclass       : PDoorsColorClass;
  pshutterexp       : PDoorsShutterExp;
  pwjbom            : PDoorsWjBom;
  pwjbomdetail      : PDoorsWjBomDetail;
  pprice            : PDoorsPrice;
  phandle           : PDoorsHandle;
  phinge            : PDoorsHinge;
  str, objstr               : string;
  jo:ISuperObject;
  al_y, al, x                 : Integer;
  xdoc:IXMLDocument;
  opa:  POptionalAcc;
begin
  OptionalAccList.Clear;
  mXml := xml;
  mGuid := '';
  mHingeHole := '';
  mDoorMemo := '';
  if xml = '' then exit;
  ll := 0;
  hh := 0;
  mLMFValue := 0;

  mHMFValue := 0;

  mMMFValue := -1;

  mDataMode := 0;

  mLockControl := True;
  try
    xdoc := XMLDoc.LoadXMLData('<?xml version="1.0" encoding="gb2312"?>'+xml);
    root := xdoc.ChildNodes[1];
    attri := root.AttributeNodes.FindNode('guid');
    if (attri=nil) or (attri.Text='') then mGuid := MyUtils.GetGUID else mGuid := attri.text;
    attri := root.AttributeNodes.FindNode('门洞宽');
    if resize then mL := StrToInt(attri.text);
    attri := root.AttributeNodes.FindNode('门洞高');
    if resize then mH := StrToInt(attri.text);
    attri := root.AttributeNodes.FindNode('L门缝');
    if attri<>nil then mLMFValue := StrToFloat(attri.text);
    attri := root.AttributeNodes.FindNode('H门缝');
    if attri<>nil then mHMFValue := StrToFloat(attri.text);
    attri := root.AttributeNodes.FindNode('M门缝');
    if attri<>nil then mMMFValue := StrToFloat(attri.text);
    attri := root.AttributeNodes.FindNode('单门数量类型');
    mPExp := GetDoorsExp(attri.text);
    attri := root.AttributeNodes.FindNode('DataMode');
    if (attri<>nil) then mDataMode := MyStrToInt(attri.Text);

    attri := root.AttributeNodes.FindNode('Extra');
    if (attri<>nil) then mExtra := attri.Text else mExtra := '';

    attri := root.AttributeNodes.FindNode('门类型');
    str := attri.text;
    mPType := GetDoorsType(attri.text);
    attri := root.AttributeNodes.FindNode('门框类型');
    mPParam := GetDoorsParam(str, attri.text);
    attri := root.AttributeNodes.FindNode('中横框类型');
    mPHBoxParam := GetDoorHBoxParam(attri.text);
    attri := root.AttributeNodes.FindNode('门芯类型');
    mMyPanelType := attri.text;
    attri := root.AttributeNodes.FindNode('门颜色');
    mDoorMyDoorsColor := attri.text;
    attri := root.AttributeNodes.FindNode('门框颜色');
    mDoorMyVBoxColor := attri.text;
    attri := root.AttributeNodes.FindNode('中横框颜色');
    mDoorMyHBoxColor := attri.text;
    attri := root.AttributeNodes.FindNode('门芯颜色');
    mDoorMyPanelColor := attri.text;
    attri := root.AttributeNodes.FindNode('ZNMJ');    //是否阻尼门铰
    if (attri<>nil) and (attri.Text='1') then mZNMJ := 1 else mZNMJ := 0;
    mGridItem := 0;
    attri := root.AttributeNodes.FindNode('均分');
    if attri <> nil then
      mGridItem := StrToInt(attri.text);
    if (mPExp = nil) or (mPType = nil) or (mPParam = nil) then
    begin
      mCopyDoor := -1;
      exit;
    end;

    mLCap := 0;
    attri := root.AttributeNodes.FindNode('左盖');
    if attri <> nil then
      mLCap := StrToInt(attri.text);
    attri := root.AttributeNodes.FindNode('右盖');
    mRCap := 0;
    if attri <> nil then
      mRCap := StrToInt(attri.text);
    attri := root.AttributeNodes.FindNode('上盖');
    mUCap := 0;
    if attri <> nil then
      mUCap := StrToInt(attri.text);
    mDCap := 0;
    attri := root.AttributeNodes.FindNode('下盖');
    if attri <> nil then
      mDCap := StrToInt(attri.text);
    mIsVertical := False;
    attri := root.AttributeNodes.FindNode('是否竖排');
    if (attri <> nil) and (attri.text = 'True') then
      mIsVertical := True;
    attri := root.AttributeNodes.FindNode('DoorMemo');
    if (attri <> nil) then mDoorMemo := attri.Text else mDoorMemo := '';
    attri := root.AttributeNodes.FindNode('Extend');
    if (attri <> nil) then mExtend := MyUtils.URLDecode(attri.Text);
    attri := root.AttributeNodes.FindNode('HingeHole');
    if (attri <> nil) then mHingeHole := attri.Text else mHingeHole := '';

    if l<>0 then ll := l-(mL);
    if h<>0 then hh := h-(mH);
    mL := Round(mL+ll);
    mH := Round(mH+hh);
 
    m := 0;
    t1 := ll/mPExp.doornum;  //计算需要补回的门洞差值
    t2 := hh;
    tt1 := t1;
    tt2 := 0;
    if mIsVertical then
    begin
      t1 := ll;
      t2 := hh/mPExp.doornum;
      tt1 := 0;
      tt2 := t2;
    end;

    for i := 0 to root.ChildNodes.Count - 1 do
    begin
      Node := root.ChildNodes[i];
      if Node.NodeName <> '配件' then continue;
      new(opa);
      attri := Node.AttributeNodes.FindNode('名称');
      if attri <> nil then opa.name := attri.text;
      attri := Node.AttributeNodes.FindNode('数量');
      if attri <> nil then opa.num := strtoint(attri.text);
      OptionalAccList.Add(opa);
    end;

    mDoorsList.Clear;
    m := -1;
    for i := 0 to root.ChildNodes.Count - 1 do
    begin
      Node := root.ChildNodes[i];
      if Node.NodeName <> '单门' then continue;
      inc(m);
      door := TDoorDoorRect.Create;
      door.mPParam := mPParam;
      mDoorsList.Add(door);
      attri := Node.AttributeNodes.FindNode('宽');
      door.doorw := MyStrToFloat(attri.text) + t1;
      door.doorw1 := door.doorw;
      door.mDoorW := door.doorw;
      attri := Node.AttributeNodes.FindNode('DW1');
      if attri <> nil then
        door.doorw1 := MyStrToFloat(attri.text) + t1;
      attri := Node.AttributeNodes.FindNode('高');
      door.doorh := MyStrToFloat(attri.text) + t2;
      door.doorh1 := door.doorh;
      attri := Node.AttributeNodes.FindNode('DH1');
      if attri <> nil then
        door.doorh1 := MyStrToFloat(attri.text) + t2;
      door.mDoorH := door.doorh;

      attri := Node.AttributeNodes.FindNode('X0');
      door.x0 := MyStrToFloat(attri.text) + tt1*m;
      door.x1 := door.x0;
      attri := Node.AttributeNodes.FindNode('Y0');
      door.y0 := MyStrToFloat(attri.text) + tt2*m;
      door.y1 := door.y0;
      attri := Node.AttributeNodes.FindNode('X1');
      if attri <> nil then door.x1 := StrToFloat(attri.text) + tt1*m;
      attri := Node.AttributeNodes.FindNode('Y1');
      if attri <> nil then door.y1 := StrToFloat(attri.text) + tt2*m;

      attri := Node.AttributeNodes.FindNode('打开方向');
      door.mOpenDirect := attri.text;
      attri := Node.AttributeNodes.FindNode('拉手');
      door.mHandle := attri.text;
      attri := Node.AttributeNodes.FindNode('门铰');
      door.mHinge := attri.text;
      //20200309      mHingeHoleExtra 非空 则通过这个计算门铰及五金
      attri := Node.AttributeNodes.FindNode('HingeHoleExtra');
      door.mHingeHoleExtra := attri.text;
      attri := Node.AttributeNodes.FindNode('门铰CT');
      if attri<>nil then door.mHingeCt := attri.text;
      attri := Node.AttributeNodes.FindNode('HandleX');
      door.mHandleX := MyStrToFloat(attri.text);
      attri := Node.AttributeNodes.FindNode('HandleY');
      door.mHandleY := MyStrToFloat(attri.text);
      attri := Node.AttributeNodes.FindNode('HandleW');
      door.mHandleW := MyStrToFloat(attri.text);
      attri := Node.AttributeNodes.FindNode('HandleH');
      door.mHandleH := MyStrToFloat(attri.text);
      attri := Node.AttributeNodes.FindNode('HandlePos');
      if attri <> nil then door.mHandlePos := attri.text;
      attri := Node.AttributeNodes.FindNode('HandlePosX');
      if attri <> nil then door.mHandlePosX := attri.text;
      attri := Node.AttributeNodes.FindNode('HandlePosY');
      if attri <> nil then door.mHandlePosY := attri.text;
      attri := Node.AttributeNodes.FindNode('Memo');
      if (attri <> nil) and (attri.Text<>'') then door.mMemo := attri.text;
      attri := Node.AttributeNodes.FindNode('HingeHoleDes');
      if (attri <> nil) then door.mHingeHoleDes := attri.Text else door.mHingeHoleDes := '';
      attri := Node.AttributeNodes.FindNode('HingeHoleParam');
      if (attri <> nil) then door.mHingeHoleParam := attri.Text else door.mHingeHoleParam := '';
      attri := Node.AttributeNodes.FindNode('HingeHoleExtra');
      if (attri <> nil) then door.mHingeHoleExtra := attri.Text else door.mHingeHoleExtra := '';

      if (door.mHandlePos<>'') and (door.mHandlePos[1]='{') then
      begin
        objstr := StringReplace(door.mHandlePos, '^', '"', [rfReplaceAll]);
        jo := SO(objstr);
        al := jo.I['AL'];
        al_y := jo.I['AL_Y'];
        x := jo.I['X'];
        if (door.mOpenDirect = '左') or (door.mOpenDirect = '右') then
        begin
          if (door.mOpenDirect = '左') then door.mHandleX := door.doorw - x - door.mHandleW;
          if (door.mOpenDirect = '右') then door.mHandleX := x;
          if al=0 then door.mHandleY := al_y;
          if al=1 then door.mHandleY := door.doorh/2.0+al_y - door.mHandleH/2;
          if al=2 then door.mHandleY := door.doorh-al_y - door.mHandleH;
        end;
        if (door.mOpenDirect = '上') or (door.mOpenDirect = '下') then
        begin
          if (door.mOpenDirect = '下') then door.mHandleY := door.doorh - x - door.mHandleH;
          if (door.mOpenDirect = '上') then door.mHandleY := x;
          if al=0 then door.mHandleX := al_y;
          if al=1 then door.mHandleX := door.doorw/2.0+al_y - door.mHandleW/2;
         if al=2 then door.mHandleX := door.doorw-al_y - door.mHandleW;
        end;
        jo := nil;
      end else begin
        mExp.AddVariable('$成品门宽度', '', FloatToStr(door.doorw), '', '');
        mExp.AddVariable('$成品门高度', '', FloatToStr(door.doorh), '', '');
        if (door.mOpenDirect = '左') then
        begin
          mExp.SetSubject(door.mHandlePosX);
          door.mHandleX := mExp.ToValueFloat;
          door.mHandleX := door.doorw - door.mHandleX - door.mHandleW;
          mExp.SetSubject(door.mHandlePosY);
          door.mHandleY := mExp.ToValueFloat * door.doorh - door.mHandleH / 2;
        end;
        if (door.mOpenDirect = '右') then
        begin
          mExp.SetSubject(door.mHandlePosX);
          door.mHandleX := mExp.ToValueFloat;
          mExp.SetSubject(door.mHandlePosY);
          door.mHandleY := mExp.ToValueFloat * door.doorh - door.mHandleH / 2;
        end;
        if (door.mOpenDirect = '上') then
        begin
          mExp.SetSubject(door.mHandlePosY);
          door.mHandleX := mExp.ToValueFloat * door.doorw - door.mHandleW / 2;
          mExp.SetSubject(door.mHandlePosX);
          door.mHandleY := mExp.ToValueFloat;
        end;
        if (door.mOpenDirect = '下') then
        begin
          mExp.SetSubject(door.mHandlePosY);
          door.mHandleX := mExp.ToValueFloat * door.doorw - door.mHandleW / 2;
          mExp.SetSubject(door.mHandlePosX);
          door.mHandleY := mExp.ToValueFloat;
          door.mHandleY := door.doorh - door.mHandleY - door.mHandleH;
        end;
      end;

      door.mIsFrame := mPType.isframe;
      door.mVBoxW := mPParam.vboxh;
      door.mUDBoxH := mPParam.udboxh;

      for j := 0 to Node.ChildNodes.Count - 1 do
      begin
        cnode := Node.ChildNodes[j];
        if cnode.NodeName <> '中横框' then continue;
        new(rb);
        rb.selected := False;
        door.boxlist.Add(rb);
        attri := cnode.AttributeNodes.FindNode('类型');
        rb.boxtype := attri.text;
        attri := cnode.AttributeNodes.FindNode('颜色');
        rb.color := attri.text;
        rb.vh := True;
        attri := cnode.AttributeNodes.FindNode('vh');
        if attri.text = 'False' then
          rb.vh := False;
        attri := cnode.AttributeNodes.FindNode('w0');
        rb.w0 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('h0');
        rb.h0 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('x0');
        rb.x0 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('y0');
        rb.y0 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('d0');
        rb.d0 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('w1');
        rb.w1 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('h1');
        rb.h1 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('x1');
        rb.x1 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('y1');
        rb.y1 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('d1');
        rb.d1 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('w2');
        rb.w2 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('h2');
        rb.h2 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('x2');
        rb.x2 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('y2');
        rb.y2 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('d2');
        rb.d2 := MyStrToFloat(attri.text);
      end;
      for j := 0 to Node.ChildNodes.Count - 1 do
      begin
        cnode := Node.ChildNodes[j];
        if cnode.NodeName <> '门芯' then continue;
        new(pnl);
        pnl.selected := False;
        door.panellist.Add(pnl);
        attri := cnode.AttributeNodes.FindNode('类型');
        pnl.PanelType := attri.text;
        attri := cnode.AttributeNodes.FindNode('颜色');
        pnl.color := attri.text;
        attri := cnode.AttributeNodes.FindNode('颜色2');
        if attri<>nil then pnl.color2 := attri.text;
        attri := cnode.AttributeNodes.FindNode('纹路');
        pnl.direct := attri.text;
        attri := cnode.AttributeNodes.FindNode('w0');
        pnl.w0 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('h0');
        pnl.h0 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('x0');
        pnl.x0 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('y0');
        pnl.y0 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('d0');
        pnl.d0 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('w1');
        pnl.w1 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('h1');
        pnl.h1 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('x1');
        pnl.x1 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('y1');
        pnl.y1 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('d1');
        pnl.d1 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('w2');
        pnl.w2 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('h2');
        pnl.h2 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('x2');
        pnl.x2 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('y2');
        pnl.y2 := MyStrToFloat(attri.text);
        attri := cnode.AttributeNodes.FindNode('d2');
        pnl.d2 := MyStrToFloat(attri.text);
      end;
      door.boxlist.Sort(SortRectBoxByY);
      door.panellist.Sort(SortRectPanelByY);
      DoorRecalcDoor(door, t1, t2, tt1, tt2, m);
    end;
    mIsSetDoors := True;
    mIsModify := False;
    HingeHole2DoorObject;
  finally
    xdoc := nil;
  end;
  mLockControl := False;
  mCopyDoor := -1;
end;
//掩门
function TLocalObject.GetDoorsXomItemForBom(childxml:string; pl, ph: Integer):ISuperObject;
  function BD2XML(const xml:string; jo:ISuperObject):string;
  var
    xdoc:IXMLDocument;
    root, nodeA, nodeB, cnode, attri : IXMLNode;
    objstr:string;
    cjo, ja           : ISuperObject;
    i              : Integer;
  begin
    Result := '';
    try
      xdoc := XMLDoc.LoadXMLData(xml);
      root := xdoc.ChildNodes[1];
      attri := root.AttributeNodes.FindNode('L');
      if attri<>nil then attri.Text := IntToStr(Round(jo.D['L']));
      attri := root.AttributeNodes.FindNode('W');
      if attri<>nil then attri.Text := IntToStr(Round(jo.D['W']));
      attri := root.AttributeNodes.FindNode('BH');
      if attri<>nil then attri.Text := IntToStr(Round(jo.D['H']));
      nodeA := root.ChildNodes.FindNode('FaceA');
      if nodeA=nil then
      begin
        nodeA := xdoc.CreateNode('FaceA', ntElement);
        root.ChildNodes.Add(nodeA);
      end;
      nodeB := root.ChildNodes.FindNode('FaceB');
      if nodeB=nil then
      begin
        nodeB := xdoc.CreateNode('FaceB', ntElement);
        root.ChildNodes.Add(nodeB);
      end;
      if (jo.S['FaceA']<>'') then
      begin
        objstr := jo.S['FaceA'];
        objstr := StringReplace(objstr, '^', '"', [rfReplaceAll]);
        ja := SO(objstr);
        for i:=0 to ja.AsArray.Length-1 do
        begin
          cjo := ja.AsArray[i];
          cnode := xdoc.CreateNode(cjo.S['Type'], ntElement);
          if cjo.S['Face']='A' then nodeA.ChildNodes.Add(cnode)
          else if cjo.S['Face']='B' then nodeB.ChildNodes.Add(cnode)
          else begin
            cnode := nil;
            continue;
          end;
          UpdateAttribute(xdoc, cnode, 'X', cjo.S['X']);
          UpdateAttribute(xdoc, cnode, 'Y', cjo.S['Y']);
          UpdateAttribute(xdoc, cnode, 'R', cjo.S['R']);
          UpdateAttribute(xdoc, cnode, 'Rb', cjo.S['Rb']);
          UpdateAttribute(xdoc, cnode, 'HDirect', cjo.S['HDirect']);
          UpdateAttribute(xdoc, cnode, 'Face', cjo.S['Face']);
          UpdateAttribute(xdoc, cnode, 'Hole_Z', cjo.S['Hole_Z']);
          cjo := nil;
        end;
        ja := nil;
      end;
      if (jo.S['FaceB']<>'') then
      begin
        objstr := jo.S['FaceB'];
        objstr := StringReplace(objstr, '^', '"', [rfReplaceAll]);
        ja := SO(objstr);
        for i:=0 to ja.AsArray.Length-1 do
        begin
          cjo := ja.AsArray[i];
          cnode := xdoc.CreateNode(cjo.S['Type'], ntElement);
          if cjo.S['Face']='A' then nodeA.ChildNodes.Add(cnode)
          else if cjo.S['Face']='B' then nodeB.ChildNodes.Add(cnode)
          else begin
            cnode := nil;
            continue;
          end;
          UpdateAttribute(xdoc, cnode, 'X', cjo.S['X']);
          UpdateAttribute(xdoc, cnode, 'Y', cjo.S['Y']);
          UpdateAttribute(xdoc, cnode, 'R', cjo.S['R']);
          UpdateAttribute(xdoc, cnode, 'Rb', cjo.S['Rb']);
          UpdateAttribute(xdoc, cnode, 'HDirect', cjo.S['HDirect']);
          UpdateAttribute(xdoc, cnode, 'Face', cjo.S['Face']);
          UpdateAttribute(xdoc, cnode, 'Hole_Z', cjo.S['Hole_Z']);
          cjo := nil;
        end;
        ja := nil;
      end;
      Result := root.XML;
      Result := StringReplace(Result, ''#13#10, '', [rfReplaceAll]);
      Result := StringReplace(Result, ''#9, '', [rfReplaceAll]);
    finally
      xdoc := nil;
    end;
  end;
  function XML2JsonObj(const xml:string):ISuperObject;
  var
    cjo, ja           : ISuperObject;
    xdoc:IXMLDocument;
    root, node, attri : IXMLNode;
    i, j              : Integer;
  begin
    Result := nil;
    try
      xdoc := XMLDoc.LoadXMLData('<?xml version="1.0" encoding="gb2312"?>'+xml);
      ja := TSuperObject.Create(stArray);
      root := xdoc.ChildNodes[1];
      for i := 0 to root.ChildNodes.Count - 1 do
      begin
        node := root.ChildNodes[i];
        cjo := TSuperObject.Create(stObject);
        cjo.I['#'] := i+1;
        for j := 0 to node.AttributeNodes.Count - 1 do
        begin
          attri := node.AttributeNodes[j];
          if attri.Text = '' then continue;
          cjo.S[attri.NodeName] := attri.Text;
          if (attri.NodeName ='Name') and (doordeslist.IndexOf(attri.Text) = -1) then
          doordeslist.Add(attri.Text);
        end;
        ja.AsArray.Add(cjo);
        cjo := nil;
      end;
      //showmessage('lenofdoordeslist='+inttostr(doordeslist.count));
      Result := ja;
    finally
      xdoc := nil;
    end;
  end;
var xml, bdfile, bdxmlid:string;
jo, ja, cjo:ISuperObject;
t, i:Integer;
doorw, doorh:double;
door:TDoorDoorRect;
begin
  Result:= nil;
  DoorLoadFromXMLTemplate(childxml, pl, ph, True);
  SetSetDoors(True);
  t := 0;
  doorw := mL;
  doorh := mH;
  if mDoorsList.Count>0 then
  begin
    door := TDoorDoorRect(mDoorsList[0]);
    if door.mIsFrame then t := 1;
    doorw := door.doorw;
    doorh := door.doorh;
  end;

  jo := TSuperObject.Create(stObject);
  jo.S['Extend'] := mExtend;
  jo.S['门款类型'] := mPParam.name;
  jo.I['是否带框'] := t;
  jo.S['HingeHole'] := mHingeHole;
  jo.S['DoorMemo'] := mDoorMemo;
  jo.S['DoorExtra'] := mExtra;
  jo.D['门洞宽'] := mL;
  jo.D['门洞高'] := mH;
  jo.D['成品门宽'] := doorw;
  jo.D['成品门高'] := doorh;
  jo.I['扇数'] := mDoorsList.Count;
  jo.I['DoorType'] := 2;

  xml := Format('<Data>%s</Data>', [DoorGetXMLBom()]);
  ja := XML2JsonObj(xml);
  for i:=0 to ja.AsArray.Length-1 do
  begin
    cjo := ja.AsArray[i];
    bdfile := cjo.S['BDFILE'];
    bdfile := MyUtils.GetQuickDrawPath+bdfile;
    if FileExists(bdfile) then
    begin
      xml := MyUtils.ReadStringFromFile(bdfile);
      cjo.S['BDXML'] := BD2XML(xml, cjo);
      cjo.S['BDXMLID'] := MyUtils.GetGUID;
      cjo.S['BDFILE'] := '';
    end;
    cjo := nil;
  end;
  jo.O['物料'] := ja;
  Result := jo;
  ja := nil;
  jo :=nil;
  SetSetDoors(False);
end;


function TLocalObject.EnumChild(param0: PBomParam):Integer;
  var
    i ,bp, bl, bh, childnum, k              : Integer;
    pl, pd, ph : Integer;
    root, node, cnode, productnode, attri           : IXMLNode;
    str, varstr, childxml, program_str       : string;
    sizeprogram_str, tmp_subspace, value, vname : string;
    guid:string;
    cjo, ja, jo:ISuperObject;
    isdoor            : boolean;
    exp               : TExpress;
    poi               : PBomOrderItem;
    bg, dtype    : string;
    xx0, xx1, yy0, yy1, zz0, zz1: Integer;
    tmp_space_x, tmp_space_y, tmp_space_z: Integer;
    args              : array[0..15] of Integer;
    real_d, real_l, t : double;
    param             : BomParam;
    clonetype : string;
  begin
    exp := TExpress.Create;
    exp.AddVariable('L', '', IntToStr(param0.pl), '', '');
    exp.AddVariable('P', '', IntToStr(param0.pd), '', '');
    exp.AddVariable('H', '', IntToStr(param0.ph), '', '');
    exp.AddVariable('BH', '', IntToStr(param0.boardheight), '', '');
    isdoor := False;
    //try
      root := param0.rootnode;
      str := GetAttributeValue(root, '模块备注', '', '');
      if (str <> '') then
      begin
        param0.blockmemo := str;
        param0.blockmemo := StringReplace(param0.blockmemo, '[宽]', IntToStr(param0.pl), [rfReplaceAll]);
        param0.blockmemo := StringReplace(param0.blockmemo, '[深]', IntToStr(param0.pd), [rfReplaceAll]);
        param0.blockmemo := StringReplace(param0.blockmemo, '[高]', IntToStr(param0.ph), [rfReplaceAll]);
      end;
      str := GetAttributeValue(root, '类别', '', '');
      if (str = '趟门,趟门') or (str = '掩门,掩门') then
      begin
        node := root.ChildNodes.FindNode('模板');
        if node<>nil then
        begin
          if (node.ChildNodes.Count > 0) then childxml := node.ChildNodes[0].xml;
          if (str = '趟门,趟门') then cjo:= GetSlidingXomItemForBom(childxml, param0.pl, param0.ph);
          if (str = '掩门,掩门') then
          begin
          cjo:= GetDoorsXomItemForBom(childxml, param0.pl, param0.ph);
          end;
          if (cjo <> nil) then
          begin
            if SlidingObjList.O[str] <> nil then ja:= SlidingObjList.O[str]
            else ja := TSuperObject.Create(stArray);
            ja.AsArray.Add(cjo);
            SlidingObjList.O[str] := ja;
          end;
          cjo:=nil;
          exit;
        end;
      end;
      node := root.ChildNodes.FindNode('变量列表');
      if node <> nil then
      begin
        for i := 0 to node.ChildNodes.Count - 1 do
        begin
          cnode := node.ChildNodes[i];
          vname := GetAttributeValue(cnode, '名称', '', '');
          value := GetAttributeValue(cnode, '值', '', '');
          SetSysVariantValue(vname, value);
          exp.AddVariable(vname, '', value, '', '');
        end;
      end;
      node := root.ChildNodes.FindNode('我的模块');
      if (node <> nil) and (not isdoor) then
      begin
        for i := 0 to node.ChildNodes.Count - 1 do
        begin
          cnode := node.ChildNodes[i];
          if (cnode.nodename <> '板件') and (cnode.nodename <> '五金') and (cnode.nodename <> '型材五金')
            and (cnode.nodename <> '模块') and (cnode.nodename <> '门板') then Continue;
          program_str := GetAttributeValue(cnode, 'Program', '', '');
          
          //guid := GetAttributeValue(cnode, 'GUID', '', '');
          //if guid = 'DADD58DA8B2CE34900AA6DB40936FECF' then showmessage('hello1');

          bg := GetAttributeValue(cnode, '基础图形', '', '');
          if (bg = 'BG::SPACE') then Continue;
          str := GetAttributeValue(cnode, '显示方式', '', '');
          if (str = '3') then Continue;
          NewBomOrderItem(poi);
          tmp_space_x := param0.space_x;
          tmp_space_y := param0.space_y;
          tmp_space_z := param0.space_z;
          poi.pl := param0.pl;
          poi.pd := param0.pd;
          poi.ph := param0.ph;
          tmp_subspace := GetAttributeValue(cnode, '子空间', '', '');
          if tmp_subspace = 'A' then tmp_subspace := '';
          InitVarArgs(poi.var_args, poi.var_names);

          poi.x := param0.px + 0;
          poi.y := param0.py + 0;
          poi.z := param0.pz + 0;

          xx0 := GetAttributeValue(cnode, 'XX0', 0, 0);
          xx1 := GetAttributeValue(cnode, 'XX1', 0, 0);
          yy0 := GetAttributeValue(cnode, 'YY0', 0, 0);
          yy1 := GetAttributeValue(cnode, 'YY1', 0, 0);
          zz0 := GetAttributeValue(cnode, 'ZZ0', 0, 0);
          zz1 := GetAttributeValue(cnode, 'ZZ1', 0, 0);

          varstr := GetAttributeValue(cnode, 'X', '', '');
          exp.SetSubject(varstr);
          poi.lx := exp.ToValueInt + xx0;
          poi.x := param0.px + poi.lx;

          varstr := GetAttributeValue(cnode, 'Y', '', '');
          exp.SetSubject(varstr);
          poi.ly := exp.ToValueInt + yy0;
          poi.y := param0.py + poi.ly;

          varstr := GetAttributeValue(cnode, 'Z', '', '');
          exp.SetSubject(varstr);
          poi.lz := exp.ToValueInt + zz0;
          poi.z := param0.pz + poi.lz;

          poi.ox := GetAttributeValue(cnode, 'OX', 0.0, 0.0);
          poi.oy := GetAttributeValue(cnode, 'OY', 0.0, 0.0);
          poi.oz := GetAttributeValue(cnode, 'OZ', 0.0, 0.0);

          varstr := GetAttributeValue(cnode, '宽', '', '');
          exp.SetSubject(varstr);
          poi.l := exp.ToValueInt + xx1 + (0 - xx0);

          varstr := GetAttributeValue(cnode, '深', '', '');
          exp.SetSubject(varstr);
          poi.p := exp.ToValueInt + yy1 + (0 - yy0);

          varstr := GetAttributeValue(cnode, '高', '', '');
          exp.SetSubject(varstr);
          poi.h := exp.ToValueInt + zz1 + (0 - zz0);

          for k := 0 to 15 do             //所有16个参数
          begin
            args[k] := 0;
            str := GetAttributeValue(cnode, '参数' + IntToStr(k), '', '');
            if (str <> '') then
            begin
              MyVariant(str, vname, value);
              exp.SetSubject(value);
              args[k] := exp.ToValueInt;
              poi.var_args[k] := args[k];
              poi.var_names[k] := vname;
              varstr := varstr + '+' + vname;
            end;
          end;

          //size高级编程
          sizeprogram_str := GetAttributeValue(cnode, 'SizeProgram', '', '');
          if ExtractFileExt(sizeprogram_str)='.lua' then
          begin
            sizeprogram_str := LuaData.ValueOf(sizeprogram_str);
            //sizeprogram_str := MyUtils.ReadStringFromFile(GetQuickDrawPath+'Program\'+sizeprogram_str);
            jo := SO(Format('{"X":"%d","Y":"%d","Z":"%d","L":"%d","D":"%d","H":"%d","OZ":"%f"}', [poi.x, poi.y, poi.z, poi.l, poi.p, poi.h, poi.oz]));
            for k:=0 to 15 do
            begin
              jo.I['C'+IntToStr(k)] := poi.var_args[k];
            end;
            str := CompileLuaProgram(jo, sizeprogram_str);
            jo := SO(str);
            if jo<>nil then
            begin
              poi.x := jo.I['X'];
              poi.y := jo.I['Y'];
              poi.z := jo.I['Z'];
              poi.l := jo.I['L'];
              poi.p := jo.I['D'];
              poi.h := jo.I['H'];
              poi.oz := jo.D['OZ'];
            end;
          end;

          attri := cnode.AttributeNodes.FindNode('类别');
          if attri <> nil then poi.desc := attri.Text;
          if (poi.desc <>'') and (bomdeslist.indexof(poi.desc) = -1)  then
          begin
            if (poi.desc <> '掩门,掩门') and (poi.desc <> '趟门,趟门') then
            begin
              bomdeslist.add(poi.desc)
            end
          end;
          param0.blist.Add(poi);
          real_l := poi.l;
          real_d := poi.p;
          if (tmp_subspace = 'L') then    //L面空间，进行旋转计算
          begin
            if (poi.var_args[0] = 1) then
            begin
              poi.oz := arctan((real_d - poi.var_args[2]) / (real_l - poi.var_args[1])) / PI * 180; //旋转角度
              poi.p := poi.var_args[3];   //深度
              t := sqrt((real_l - poi.var_args[1]) * (real_l - poi.var_args[1]) + (real_d - poi.var_args[2]) * (real_d - poi.var_args[2]));
              poi.l := Round(t);          //宽度
              poi.x := Round(poi.var_args[1] - poi.var_args[3] * (real_d - poi.var_args[2]) / t); //x
              poi.y := Round(real_d - poi.var_args[3] * (real_l - poi.var_args[1]) / t); //y
              if poi.var_args[4] <> 0 then poi.l := poi.var_args[4];
              poi.lx := poi.x;
              poi.ly := poi.y;
            end
            else
            begin
              poi.oz := 0;
            end;
          end;
          if (tmp_subspace = 'R') then    //R面空间，进行旋转计算
          begin
            if (poi.var_args[0] = 1) then
            begin
              poi.oz := -arctan((real_d - poi.var_args[2]) / (real_l - poi.var_args[1])) / PI * 180;
              poi.p := poi.var_args[3];
              t := sqrt((real_l - poi.var_args[1]) * (real_l - poi.var_args[1]) + (real_d - poi.var_args[2]) * (real_d - poi.var_args[2]));
              poi.l := Round(t);          //宽度
              poi.x := poi.x + Round(poi.var_args[3] * (real_d - poi.var_args[2]) / t); //x
              poi.y := Round(poi.var_args[2] - poi.var_args[3] * (real_l - poi.var_args[1]) / t); //y
              if poi.var_args[4] <> 0 then poi.l := poi.var_args[4];
              poi.lx := poi.x;
              poi.ly := poi.y;
            end
            else
            begin
              poi.oz := 0;
            end;
          end;
          childxml := '';
          if cnode.ChildNodes.Count > 0 then childxml := cnode.ChildNodes[0].xml;
          childnum := 0;
          if childxml <> '' then
          begin
            param := param0^;
            param.pname := poi.name;
            param.subspace := poi.subspace;
            param.mark := poi.mark;
            param.pl := poi.l;
            param.pd := poi.p;
            param.ph := poi.h;
            param.px := poi.x;
            param.py := poi.y;
            param.pz := poi.z;
            param.space_x := tmp_space_x;
            param.space_y := tmp_space_y;
            param.space_z := tmp_space_z;
            param.num := poi.num;
            param.parent := poi;
            if cnode.ChildNodes.Count>0 then
            begin
              param.rootnode := cnode.ChildNodes[0];
              param.xdoc := param0.xdoc;
              childnum := EnumChild(@param);
            end;
          end;
          if program_str <> '' then       //产生克隆模块
          begin
            GetCloneItemForBom(exp, program_str, poi, cnode, param0);
          end;
        end;
      end;
    //finally
    //  if Assigned(exp) then FreeAndNil(exp);
    //end;                                //for i
  end;
function TLocalObject.GetCloneItemForBom(exp:TExpress; program_str:string; clone_oi:PBomOrderItem; clonenode: IXMLNode; param0: PBomParam):Integer;
  procedure S2S(str: string; var s1, s2: string);
  var
    ws                : WideString;
    n                 : Integer;
  begin
    s1 := '';
    s2 := '';
    ws := str;
    n := Pos('=', ws);
    s1 := LeftStr(ws, n - 1);
    s2 := RightStr(ws, Length(ws) - n);
    s1 := trim(s1);
    s2 := trim(s2);
    s2 := StringReplace(s2, '^', ',', [rfReplaceAll]);
  end;
  procedure UpdateAttribute(txdoc:IXMLDocument; cnode:IXMLNode; name, value:string);
  var attri:IXMLNode;
  begin
    if name='' then exit;
      attri := cnode.AttributeNodes.FindNode(name);
      if attri=nil then
      begin
        attri := txdoc.CreateNode(name, ntAttribute);
        cnode.AttributeNodes.Add(attri);
      end;
      attri.Text := value;
  end;
  var
  root, node, cnode, attri, tmpnode: IXMLNode;
  i, di, bp, bl, bh, childnum, k, autodirect: Integer;
  xx0, xx1, yy0, yy1, zz0, zz1: Integer;
  tmp_space_x, tmp_space_y, tmp_space_z: Integer;
  value, vname, childxml, tmp_subspace, tmp_soz, spaceflag: string;
  poi               : PBomOrderItem;
  sliw, slih, doorw, doorh: Real;
  doornum           : Integer;
  isdoor            : boolean;
  str, bg, dtype    : string;
  args              : array[0..15] of Integer;
  ls, varstr        : string;           //拉手信息
  real_d, real_l, t : double;
  param             : BomParam;

 var
  wstr, ln, vstr          : Widestring;
  n:Integer;
  s1, s2, nodename, linkpath, textureclass, ext          : string;
  jo:ISuperObject;
  begin
    param.blockmemo := '';
    ext := ExtractFileExt(program_str);
    program_str := LuaData.ValueOf(program_str);
    //program_str := MyUtils.ReadStringFromFile(MyUtils.GetQuickDrawPath+'Program\'+program_str);
    jo := SO(Format('{"X":"%d","Y":"%d","Z":"%d","L":"%d","D":"%d","H":"%d"}'
    , [clone_oi.x, clone_oi.y, clone_oi.z, clone_oi.l, clone_oi.p, clone_oi.h]));
    for i:=0 to 15 do
    begin
      jo.I['C'+IntToStr(i)] := clone_oi.var_args[i];
    end;
    if ext='.lua' then
      wstr := CompileLuaProgram(jo, program_str)
    else wstr := CompileProgram(jo, program_str);
    jo := nil;
    try
      n := Pos(';', wstr);
      while n > 0 do
      begin
        cnode := clonenode.CloneNode(True);
        nodename := cnode.NodeName;

        ln := LeftStr(wstr, n - 1);
        wstr := RightStr(wstr, Length(wstr) - n);
        //分解行
        n := Pos(',', ln);
        while n>0 do
        begin
          vstr := LeftStr(ln, n - 1);
          S2S(vstr, s1, s2);
          if s1='NN' then nodename := s2 else UpdateAttribute(param0.xdoc, cnode, s1, s2);
          ln := RightStr(ln, Length(ln) - n);
          n := Pos(',', ln);
        end;
        if (n<=0) and (ln<>'') then
        begin
          S2S(ln, s1, s2);
          if s1='NN' then nodename := s2 else UpdateAttribute(param0.xdoc, cnode, s1, s2);
        end;

        n := Pos(';', wstr);

        if (nodename <> '板件') and (nodename <> '五金') and (nodename <> '型材五金')
        and (nodename <> '模块') and (nodename <> '门板') then Continue;

        linkpath := '';
        attri := cnode.AttributeNodes.FindNode('链接');
        if attri <> nil then linkpath := attri.Text;
        attri := cnode.AttributeNodes.FindNode('基础图形');
        bg := '';
        if attri <> nil then bg := attri.Text;
        if (bg = 'BG::SPACE') then Continue;
        attri := cnode.AttributeNodes.FindNode('显示方式');
        if (attri <> nil) and (attri.Text = '3') then Continue;
        NewBomOrderItem(poi);
        poi.pl := param0.pl;
        poi.pd := param0.pd;
        poi.ph := param0.ph;
        tmp_subspace := GetAttributeValue(cnode, '子空间', '', '');
        if tmp_subspace = 'A' then tmp_subspace := '';
        InitVarArgs(poi.var_args, poi.var_names);

        poi.x := param0.px + 0;
        poi.y := param0.py + 0;
        poi.z := param0.pz + 0;

        xx0 := GetAttributeValue(cnode, 'XX0', 0, 0);
        xx1 := GetAttributeValue(cnode, 'XX1', 0, 0);
        yy0 := GetAttributeValue(cnode, 'YY0', 0, 0);
        yy1 := GetAttributeValue(cnode, 'YY1', 0, 0);
        zz0 := GetAttributeValue(cnode, 'ZZ0', 0, 0);
        zz1 := GetAttributeValue(cnode, 'ZZ1', 0, 0);

        varstr := GetAttributeValue(cnode, 'X', '', '');
        exp.SetSubject(varstr);
        poi.lx := exp.ToValueInt + xx0;
        poi.x := param0.px + poi.lx;

        varstr := GetAttributeValue(cnode, 'Y', '', '');
        exp.SetSubject(varstr);
        poi.ly := exp.ToValueInt + yy0;
        poi.y := param0.py + poi.ly;

        varstr := GetAttributeValue(cnode, 'Z', '', '');
        exp.SetSubject(varstr);
        poi.lz := exp.ToValueInt + zz0;
        poi.z := param0.pz + poi.lz;

        poi.ox := GetAttributeValue(cnode, 'OX', 0.0, 0.0);
        poi.oy := GetAttributeValue(cnode, 'OY', 0.0, 0.0);
        poi.oz := GetAttributeValue(cnode, 'OZ', 0.0, 0.0);

        varstr := GetAttributeValue(cnode, '宽', '', '');
        exp.SetSubject(varstr);
        poi.l := exp.ToValueInt + xx1 + (0 - xx0);

        varstr := GetAttributeValue(cnode, '深', '', '');
        exp.SetSubject(varstr);
        poi.p := exp.ToValueInt + yy1 + (0 - yy0);

        varstr := GetAttributeValue(cnode, '高', '', '');
        exp.SetSubject(varstr);
        poi.h := exp.ToValueInt + zz1 + (0 - zz0);

        for k := 0 to 15 do             //所有16个参数
        begin
          args[k] := 0;
          str := GetAttributeValue(cnode, '参数' + IntToStr(k), '', '');
          if (str <> '') then
          begin
            MyVariant(str, vname, value);
            exp.SetSubject(value);
            args[k] := exp.ToValueInt;
            poi.var_args[k] := args[k];
            poi.var_names[k] := vname;
            varstr := varstr + '+' + vname;
          end;
        end;


        attri := cnode.AttributeNodes.FindNode('类别');
        if attri <> nil then poi.desc := attri.Text;
        if (poi.desc <>'') and (bomdeslist.indexof(poi.desc) = -1)  then
        begin
          bomdeslist.add(poi.desc)
        end;
        if (tmp_subspace = 'L') then    //L面空间，进行旋转计算
        begin
          if (poi.var_args[0] = 1) then
          begin
            poi.oz := arctan((real_d - poi.var_args[2]) / (real_l - poi.var_args[1])) / PI * 180; //旋转角度
            poi.p := poi.var_args[3];   //深度
            t := sqrt((real_l - poi.var_args[1]) * (real_l - poi.var_args[1]) + (real_d - poi.var_args[2]) * (real_d - poi.var_args[2]));
            poi.l := Round(t);          //宽度
            poi.x := Round(poi.var_args[1] - poi.var_args[3] * (real_d - poi.var_args[2]) / t); //x
            poi.y := Round(real_d - poi.var_args[3] * (real_l - poi.var_args[1]) / t); //y
            if poi.var_args[4] <> 0 then poi.l := poi.var_args[4];
            poi.lx := poi.x;
            poi.ly := poi.y;
          end
          else
          begin
            poi.oz := 0;
          end;
        end;
        if (tmp_subspace = 'R') then    //R面空间，进行旋转计算
        begin
          if (poi.var_args[0] = 1) then
          begin
            poi.oz := -arctan((real_d - poi.var_args[2]) / (real_l - poi.var_args[1])) / PI * 180;
            poi.p := poi.var_args[3];
            t := sqrt((real_l - poi.var_args[1]) * (real_l - poi.var_args[1]) + (real_d - poi.var_args[2]) * (real_d - poi.var_args[2]));
            poi.l := Round(t);          //宽度
            poi.x := poi.x + Round(poi.var_args[3] * (real_d - poi.var_args[2]) / t); //x
            poi.y := Round(poi.var_args[2] - poi.var_args[3] * (real_l - poi.var_args[1]) / t); //y
            if poi.var_args[4] <> 0 then poi.l := poi.var_args[4];
            poi.lx := poi.x;
            poi.ly := poi.y;
          end
          else
          begin
            poi.oz := 0;
          end;
        end;
        childxml := '';
        if linkpath<>'' then
          begin
          childxml := EnumXML(GetXMLByLink(linkpath, qry));
          tmpnode := Xml2ChildNodes(childxml);
          if tmpnode<>nil then
          begin
            cnode.ChildNodes.Clear;
            cnode.ChildNodes.Add(tmpnode);
          end;
        end else begin
          if cnode.ChildNodes.Count > 0 then childxml := cnode.ChildNodes.Nodes[0].xml;
        end;
        if childxml <> '' then
        begin
          param := param0^;
          param.pname := poi.name;
          param.subspace := poi.subspace;
          param.mark := poi.mark;
          param.pl := poi.l;
          param.pd := poi.p;
          param.ph := poi.h;
          param.px := poi.x;
          param.py := poi.y;
          param.pz := poi.z;
    
          param.num := poi.num;
          param.parent := poi;
          if poi.group<>'' then param.group := poi.group;
          if poi.blockmemo<>'' then param.blockmemo := poi.blockmemo;
          if poi.number_text<>'' then param.number_text := poi.number_text;
          attri := cnode.AttributeNodes.FindNode('输出类型');
          if (attri <> nil) and (attri.Text <> '') then param.outputtype := attri.Text;
          if cnode.ChildNodes.Count>0 then
          begin
            param.rootnode := cnode.ChildNodes[0];
            param.xdoc := param0.xdoc;
            childnum := EnumChild(@param);
          end;
        end;
      end;
    except
    end;
  end;
function TLocalObject.FindDesList(xml: string):ISuperObject;
Var
  l, d, h, bh : Integer;
  param             : BomParam;
  root, attri: IXMLNode;
  xdoc:  IXMLDocument;
begin
  Result :=nil;
  if not Assigned(bomlist) then bomlist := TList.Create;
  xdoc := XMLDoc.LoadXMLData('<?xml version="1.0" encoding="gb2312"?>'+xml);
  root := xdoc.ChildNodes[1];   //第一级产品节点
  if (root.nodename <> '产品') or (root.ChildNodes.Count <= 0) then exit;
  try
    l := 0;
    d := 0;
    h := 0;
    bh := 18;
    if root.ChildNodes[0].nodename = '产品' then
    begin
      bh := GetAttributeValue(root.ChildNodes[0], '板材厚度', bh, bh);
    end;
    attri := root.AttributeNodes.FindNode('宽');
    if attri <> nil then
      l := StrToInt(attri.Text);
    attri := root.AttributeNodes.FindNode('深');
    if attri <> nil then
      d := StrToInt(attri.Text);
    attri := root.AttributeNodes.FindNode('高');
    if attri <> nil then
      h := StrToInt(attri.Text);
    param.blist := bomlist;
    param.pl := l;
    param.pd := d;
    param.ph := h;
    param.px := 0;
    param.py := 0;
    param.pz := 0;
    param.boardheight := bh;
    param.rootnode := root.ChildNodes[0];
    param.xdoc := xdoc;
    EnumChild(@param);
    Result:=SlidingObjList;
  except
  end;
end;
procedure TLocalObject.InitGtConfig(const config:string);
Var
  i,j, n, linknums : Integer;
  luaname, luastring, linkname : String;
  jo, cjo, ja : ISuperObject;
  jts, linkjts:TSuperTableString;
  item: TSuperAvlEntry;

begin
  jo := TSuperObject.Create();
  jo:=SO(config).O['gtconfig'];
  if jo.O['luaobj'] <> nil then
  begin
    cjo :=jo.O['luaobj'];
    jts := cjo.AsObject;
    n := jts.GetNames.AsArray.Length;
    for i:=0 to n-1 do
    begin
      luaname:= jts.GetNames.AsArray.S[i];
      if luaname = 'linkpath' then
      begin
        if cjo.O['linkpath'] <> nil then
        begin
          linkjts := cjo.O['linkpath'].AsObject;
          linknums := linkjts.GetNames.AsArray.Length;
          for j:=0 to linknums-1 do
          begin
            linkname:= linkjts.GetNames.AsArray.S[j];
            gLinkXML.S[linkname]:=linkjts.S[linkname];
          end;
        end;
        Continue;
      end;
      luastring:=jts.S[luaname];
      LuaData.Add(luaname, luastring);
    end;
  end;
end;
procedure TLocalObject.InitSlidingConfig(const config:string);
Var
  i, n, id : Integer;
  jo, cjo, ja : ISuperObject;
  key, SlidingExpString, SlidingTypeString, SlidingParamString : string;
  UDBoxParamString, TrackParamString, HBoxParamString, VBoxParamString :string;
  SlidingWjBomDetailString, SlidingColorString, PanelTypeString : string;
  SlidingAccessoryString, SlidingColorClassString, SSExpString: string;
  PanelBomDetailString, PCfglistString: string;
  pexp :   PSlidingExp;
  pstype : PSlidingType;
  psp :    PSlidingParam;
  pudbox : PUDBoxParam;
  ptrack : PTrackParam;
  phbox :  pHBoxParam;
  pvbox :  PVBoxParam;
  pnltype           : PPanelType;
  pbomdetail        : PSlidingWjBomDetail;
  pa                : PAccessory;
  pssexp            : PSlidingShutterExp;
  pspbdetail:PSlidingPanelBomDetail;
  pcolor : PSlidingColor;
  pcolorclass :PSlidingColorClass;
  cfg : PCfgTable;
  hfg3 : PSlidingHfg2;
  hfg4 : PSlidingHfg2;
  hfg2 : PSlidingHfg2;
  sfg2 : PSlidingHfg2;
  sfg3 : PSlidingHfg2;
  sfg4 : PSlidingHfg2;
begin
  jo := TSuperObject.Create();
  jo:=SO(config).O['tmconfig'];
  mNoFZTPriceFlag:=0;
  mNoCDWPriceFlag:=0;
  mNoFZTPriceFlag:= jo.I['mNoFZTPriceFlag'];
  mNoCDWPriceFlag:= jo.I['mNoCDWPriceFlag'];
  SlidingExpString := jo.S['SlidingExp'];
  ja := SO(SlidingExpString);
  n := ja.AsArray.Length;
  //单门数量类型
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pexp);
    pexp.id := cjo.I['id'];
    pexp.doornum := cjo.I['doornum'];
    pexp.deleted := False;
    pexp.overlapnum := cjo.I['overlapnum'];
    pexp.lkvalue := cjo.I['lkvalue'];
    pexp.name := cjo.S['name'];
    pexp.noexp := cjo.B['noexp'];
    key:=cjo.S['name'];
    mSlidingExpList.Add(pexp);
  end;

  //门类型
  SlidingTypeString:= jo.S['SlidingType'];
  ja := SO(SlidingTypeString);
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pstype);
    pstype.id := cjo.I['id'];
    pstype.name := cjo.S['name'];
    pstype.deleted := False;
    key:=cjo.S['name'];
    mSlidingTypeList.Add(pstype);
  end;
  //边框类型
  SlidingParamString:= jo.S['SlidingParam'];
  ja := SO(SlidingParamString);
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(psp);
    psp.deleted := False;
    psp.id := cjo.I['id'];
    psp.overlap := cjo.I['overlap'];
    psp.ddlw := cjo.I['ddlpos'];
    psp.fztlen := cjo.I['fztkd'];
    psp.glassvalue1 := cjo.I['glassvalue1'];
    psp.glassvalue2 := cjo.I['glassvalue2'];
    psp.vboxjtw := cjo.I['vboxjtw'];
    psp.uboxjtw := cjo.I['uboxjtw'];
    psp.dboxjtw := cjo.I['dboxjtw'];
    psp.hboxjtw := cjo.I['hboxjtw'];
    psp.cpm_lmax := cjo.I['cpm_lmax'];
    psp.cpm_hmax := cjo.I['cpm_hmax'];
    psp.hboxvalue := cjo.I['hboxvalue'];

    psp.name := cjo.S['name'];
    psp.vboxtype := cjo.S['vboxtype'];
    psp.myclass := cjo.S['doortype'];
    psp.track := cjo.S['track'];
    psp.udbox := cjo.S['udbox'];
    psp.zndlun := cjo.S['zndlun'];
    psp.ddlun := cjo.S['ddlun'];
    psp.diaolun := cjo.S['diaolun'];
    psp.gddwlun := cjo.S['gddwlun'];
    psp.hddwlun := cjo.S['hddwlun'];
    psp.ls := cjo.S['ls'];
    psp.wjname := cjo.S['wjname'];
    psp.hbox := cjo.S['hbox'];
    psp.memo := cjo.S['groupname'];
    psp.laminating := cjo.B['laminating'];
    psp.is_xq := cjo.B['is_xq'];
    key:=cjo.S['name'];
    mSlidingParamList.Add(psp);
  end;
  //上下横框类型
  UDBoxParamString:= jo.S['UDBoxParam'];
  ja := SO(UDBoxParamString);
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pudbox);
    pudbox.deleted := False;
    pudbox.id := cjo.I['id'];
    pudbox.ubheight := cjo.I['upboxheight'];
    pudbox.ubdepth := cjo.I['upboxdepth'];
    pudbox.ubthick := cjo.I['upboxthick'];
    pudbox.dbheight := cjo.I['downboxheight'];
    pudbox.dbdepth := cjo.I['downboxdepth'];
    pudbox.dbthick := cjo.I['downboxthick'];
    pudbox.uphole := cjo.I['upholepos'];
    pudbox.downhole := cjo.I['downholepos'];
    pudbox.upsize := cjo.I['upsize'];
    pudbox.downsize := cjo.I['downsize'];
    pudbox.name := cjo.S['name'];
    pudbox.wlupcode := cjo.S['wlupcode'];
    pudbox.wldncode := cjo.S['wldncode'];
    pudbox.upname := cjo.S['upname'];
    pudbox.dnname := cjo.S['dnname'];
    pudbox.wjname1 := cjo.S['wjname1'];
    pudbox.wjname2 := cjo.S['wjname2'];
    pudbox.upmodel := cjo.S['upmodel'];
    pudbox.dnmodel := cjo.S['dnmodel'];
    pudbox.upmemo := cjo.S['upmemo'];
    pudbox.dnmemo := cjo.S['dnmemo'];
    pudbox.dnbdfile := cjo.S['dnbdfile'];
    pudbox.upbdfile := cjo.S['upbdfile'];
    pudbox.frametype := cjo.S['边框类型'];
    key:=cjo.S['name'];
    mUDBoxParamList.Add(pudbox);
  end;
  //趟门上下轨参数
  TrackParamString:= jo.S['TrackParam'];
  ja := SO(TrackParamString);
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(ptrack);
    ptrack.deleted := False;
    ptrack.id := cjo.I['id'];
    ptrack.height := cjo.I['height'];
    ptrack.depth := cjo.I['depth'];
    ptrack.name := cjo.S['name'];
    ptrack.frametype := cjo.S['边框类型'];
    ptrack.lkvalue1 := cjo.I['lkvalue1'];
    ptrack.wlupcode := cjo.S['wlupcode'];
    ptrack.upname := cjo.S['upname'];
    ptrack.wjname1 := cjo.S['wjname1'];
    ptrack.upsize := cjo.I['upsize'];
    ptrack.upmodel := cjo.S['upmodel'];
    ptrack.upmemo := cjo.S['upmemo'];
    ptrack.upbdfile := cjo.S['upbdfile'];
    ptrack.lkvalue2 := cjo.I['lkvalue2'];
    ptrack.wldncode := cjo.S['wldncode'];
    ptrack.dnname := cjo.S['dnname'];
    ptrack.wjname2 := cjo.S['wjname2'];
    ptrack.downsize := cjo.I['downsize'];
    ptrack.dnmodel := cjo.S['dnmodel'];
    ptrack.dnmemo := cjo.S['dnmemo'];
    ptrack.dnbdfile := cjo.S['dnbdfile'];
    key:=cjo.S['name'];
    mTrackParamList.Add(ptrack);
  end;
  //趟门 中横框
  HBoxParamString:= jo.S['HBoxParam'];
  ja := SO(HBoxParamString);
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(phbox);
    phbox.deleted := False;
    phbox.id := cjo.I['id'];
    phbox.height := cjo.I['height'];
    phbox.depth := cjo.I['depth'];
    phbox.thick := cjo.I['thick'];
    phbox.hole := cjo.I['holepos'];
    phbox.holenum := cjo.I['holenum'];
    phbox.holecap := cjo.I['holecap'];
    phbox.size := cjo.I['size'];
    phbox.ishboxvalue := cjo.I['ishboxvalue'];
    phbox.name := cjo.S['name'];
    phbox.wlcode := cjo.S['wlcode'];
    phbox.bjcode := cjo.S['bjcode'];
    phbox.wjname := cjo.S['wjname'];
    phbox.model := cjo.S['model'];
    phbox.memo := cjo.S['memo'];
    phbox.bdfile := cjo.S['bdfile'];
    phbox.frametype := cjo.S['边框类型'];
    key:=cjo.S['name'];
    mHBoxParamList.Add(phbox);
  end;
  // 趟门 竖框参数
  VBoxParamString:= jo.S['VBoxParam'];
  ja := SO(VBoxParamString);
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pvbox);
    pvbox.deleted := False;
    pvbox.id := cjo.I['id'];
    pvbox.height := cjo.I['height'];
    pvbox.depth := cjo.I['depth'];
    pvbox.thick := cjo.I['thick'];
    pvbox.panelvalue := cjo.I['panelvalue'];
    pvbox.udboxvalue := cjo.I['udboxvalue'];
    pvbox.vboxvalue := cjo.I['vboxvalue'];
    pvbox.size := cjo.I['size'];
    pvbox.name := cjo.S['name'];
    pvbox.wlcode := cjo.S['wlcode'];
    pvbox.wjname := cjo.S['wjname'];
    pvbox.model := cjo.S['model'];
    pvbox.memo := cjo.S['memo'];
    pvbox.bdfile := cjo.S['bdfile'];
    key:=cjo.S['name'];
    mVBoxParamList.Add(pvbox);
  end;

  id:=0;
  //颜色分类2
  SlidingColorString:= jo.S['SlidingColor'];
  ja := SO(SlidingColorString);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pcolor);
    inc(id);
    pcolor.id := id;
    pcolor.deleted := False;
    pcolor.name := cjo.S['name'];
    pcolor.myclass := cjo.S['myclass'];
    pcolor.code := cjo.S['code'];
    mSlidingColorList.Add(pcolor);
  end;
   //门板类型
  PanelTypeString:= jo.S['PanelType'];
  ja := SO(PanelTypeString);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pnltype);
    inc(id);
    pnltype.id := id;
    pnltype.deleted := False;
    pnltype.name := cjo.S['name'];
    pnltype.jtvalue := cjo.I['jtvalue'];
    pnltype.wjname := cjo.S['wjname'];
    pnltype.isglass := cjo.B['isglass'];
    pnltype.isbaiye := cjo.B['isbaiye'];
    pnltype.iswhole := cjo.B['iswhole'];
    pnltype.bktype := cjo.S['bktype'];
    pnltype.direct := cjo.S['direct'];
    pnltype.lmax := cjo.I['lmax'];
    pnltype.lmin := cjo.I['lmin'];
    pnltype.wmax := cjo.I['wmax'];
    pnltype.wmin := cjo.I['wmin'];
    if (pnltype.bktype <> '*') and (not FindBkType(pnltype.bktype)) then
      pnltype.deleted := True;
    pnltype.pnl2d := cjo.S['panel2d'];
    pnltype.slave := cjo.S['slaVe'];
    pnltype.slave2 := cjo.S['slaVe2'];
    pnltype.mk3d := cjo.S['mk3d'];
    pnltype.mkl := cjo.I['mkl'];
    pnltype.mkh := cjo.I['mkh'];
    pnltype.thick := cjo.I['thick'];
    pnltype.memo := cjo.S['memo'];
    pnltype.memo2 := cjo.S['memo2'];
    pnltype.memo3 := cjo.S['memo3'];
    pnltype.bdfile := cjo.S['bdfile'];
    mPanelTypeList.Add(pnltype);
  end;

  //五金配件
  SlidingAccessoryString:= jo.S['SlidingAccessory'];
  ja := SO(SlidingAccessoryString);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pa);
    inc(id);
    pa.id := id;
    pa.deleted := False;
    pa.name := cjo.S['name'];
    pa.myunit := cjo.S['unit'];
    pa.wlcode := cjo.S['wlcode'];
    pa.myclass := cjo.S['myclass'];
    pa.isglass := cjo.B['isglass'];
    pa.isbaiye := cjo.B['isbaiye'];
    pa.isuserselect := cjo.B['isuserselect'];
    pa.color := cjo.S['color'];
    pa.memo := cjo.S['memo'];
    pa.memo2 := cjo.S['memo2'];
    pa.memo3 := cjo.S['memo3'];
    pa.bdfile := cjo.S['bdfile'];
    mSlidingAccessoryList.Add(pa);
  end;
  //颜色分类
  SlidingColorClassString:= jo.S['SlidingColorClass'];
  ja := SO(SlidingColorClassString);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pcolorclass);
    inc(id);
    pcolorclass.id := id;
    pcolorclass.deleted := False;
    pcolorclass.color := cjo.S['color'];
    pcolorclass.myclass := cjo.S['myclass'];
    pcolorclass.mat := cjo.S['mat'];
    pcolorclass.color2 := cjo.S['color2'];
    pcolorclass.wlcode := cjo.S['wlcode'];
    pcolorclass.bjcode := cjo.S['bjcode'];
    pcolorclass.color3 := cjo.S['color3'];
    pcolorclass.color4 := cjo.S['color4'];
    pcolorclass.skcolor1 := cjo.S['skcolor1'];
    pcolorclass.skcolor2 := cjo.S['skcolor2'];
    pcolorclass.skcolor3 := cjo.S['skcolor2'];
    pcolorclass.skcolor4 := cjo.S['skcolor4'];
    mSlidingColorClassList.Add(pcolorclass);
  end;
  //百叶板计算公式
  SSExpString:= jo.S['SSExp'];
  ja := SO(SSExpString);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pssexp);
    pssexp.deleted := False;
    pssexp.PanelType := cjo.S['paneltype'];
    pssexp.height := cjo.D['height'];
    pssexp.width := cjo.D['width'];
    pssexp.heightcap := cjo.D['heightcap'];
    pssexp.widthcap := cjo.D['widthcap'];
    pssexp.minheight := cjo.D['minheight'];
    pssexp.minwidth := cjo.D['minwidth'];
    pssexp.size := cjo.D['size'];
    mSSExpList.Add(pssexp);
  end;
   //五金配件分类数据
  SlidingWjBomDetailString:= jo.S['SlidingWjBomDetail'];
  ja := SO(SlidingWjBomDetailString);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pbomdetail);
    inc(id);
    pbomdetail.id := id;
    pbomdetail.deleted := False;
    pbomdetail.name := cjo.S['name'];
    pbomdetail.bomname :=cjo.S['bomname'];
    pbomdetail.l := cjo.S['l'];
    pbomdetail.d :=cjo.S['d'];
    pbomdetail.num := cjo.S['num'];
    mSlidingWjBomDetailList.Add(pbomdetail);
  end;
  //门板附加物料
  PanelBomDetailString:= jo.S['PanelBomDetail'];
  ja := SO(PanelBomDetailString);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pspbdetail);
    inc(id);
    pspbdetail.id := id;
    pspbdetail.deleted := False;
    pspbdetail.bomclass :=cjo.S['bomclass'];
    pspbdetail.bomname :=cjo.S['bomname'];
    pspbdetail.l := cjo.S['l'];
    pspbdetail.w := cjo.S['w'];
    pspbdetail.h := cjo.S['h'];
    pspbdetail.mat := cjo.S['mat'];
    pspbdetail.color := cjo.S['color'];
    pspbdetail.bomtype := cjo.S['bomtype'];
    pspbdetail.memo := cjo.S['memo'];
    pspbdetail.memo2 := cjo.S['memo2'];
    pspbdetail.memo3 := cjo.S['memo3'];
    pspbdetail.lmin := cjo.I['lmin'];
    pspbdetail.lmax := cjo.I['lmax'];
    pspbdetail.hmin := cjo.I['hmin'];
    pspbdetail.hmax := cjo.I['hmax'];
    pspbdetail.num := cjo.I['num'];
    pspbdetail.bdfile := cjo.S['bdfile'];
    mPanelBomDetailList.Add(pspbdetail);
  end;
  //门转换表
  PCfglistString:= jo.S['Cfglist'];
  ja := SO(PCfglistString);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(cfg);
    cfg.name :=cjo.S['名称'];
    cfg.modle :=cjo.I['模式'];
    cfg.frametype := cjo.S['边框类型'];
    cfg.bomname := cjo.S['物料名称'];
    cfg.munit := cjo.S['单位'];
    mCfglist.Add(cfg);
  end;
  // xml
  SfgParam:= jo.O['SfgParam'];
  //趟门2横分格
  ja := SO(jo.S['Hfg2']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(hfg2);
    inc(id);
    hfg2.id := id;
    hfg2.fgtype :=cjo.S['分格类型'];
    hfg2.spszh := cjo.S['适配竖中横'];
    hfg2.spmk := cjo.S['适配门框'];
    hfg2.varlist := cjo.S['变量列表'];
    hfg2.mxlist := cjo.S['门芯列表'];
    hfg2.image := cjo.S['image'];
    SlidingHfg2List.Add(hfg2);
  end;
  //趟门3横分格
  ja := SO(jo.S['Hfg3']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(hfg3);
    inc(id);
    hfg3.id := id;
    hfg3.fgtype :=cjo.S['分格类型'];
    hfg3.spszh := cjo.S['适配竖中横'];
    hfg3.varlist := cjo.S['变量列表'];
    hfg3.mxlist := cjo.S['门芯列表'];
    hfg3.image := cjo.S['image'];
    SlidingHfg3List.Add(hfg3);
  end;
  //趟门4横分格
  ja := SO(jo.S['Hfg4']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(hfg4);
    inc(id);
    hfg4.id := id;
    hfg4.fgtype :=cjo.S['分格类型'];
    hfg4.spszh := cjo.S['适配竖中横'];
    hfg4.varlist := cjo.S['变量列表'];
    hfg4.mxlist := cjo.S['门芯列表'];
    hfg4.image := cjo.S['image'];
    SlidingHfg4List.Add(hfg4);
  end;
  //趟门2竖分格
  ja := SO(jo.S['Sfg2']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(Sfg2);
    inc(id);
    Sfg2.id := id;
    Sfg2.fgtype :=cjo.S['分格类型'];
    Sfg2.spszh := cjo.S['适配竖中横'];
    Sfg2.varlist := cjo.S['变量列表'];
    Sfg2.mxlist := cjo.S['门芯列表'];
    Sfg2.image := cjo.S['image'];
    SlidingSfg2List.Add(Sfg2);
  end;
  //趟门3竖分格
  ja := SO(jo.S['Sfg3']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(Sfg3);
    inc(id);
    Sfg3.id := id;
    Sfg3.fgtype :=cjo.S['分格类型'];
    Sfg3.spszh := cjo.S['适配竖中横'];
    Sfg3.varlist := cjo.S['变量列表'];
    Sfg3.mxlist := cjo.S['门芯列表'];
    Sfg3.image := cjo.S['image'];
    SlidingSfg3List.Add(Sfg3);
  end;
  //趟门4竖分格
  ja := SO(jo.S['Sfg4']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(Sfg4);
    inc(id);
    Sfg4.id := id;
    Sfg4.fgtype :=cjo.S['分格类型'];
    Sfg4.spszh := cjo.S['适配竖中横'];
    Sfg4.varlist := cjo.S['变量列表'];
    Sfg4.mxlist := cjo.S['门芯列表'];
    Sfg4.image := cjo.S['image'];
    SlidingSfg4List.Add(Sfg4);
  end;
  //横中横
  ja := SO(jo.S['HSHBoxParam']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(phbox);
    inc(id);
    phbox.id := id;
    phbox.height :=cjo.D['height'];
    phbox.depth :=cjo.D['depth'];
    phbox.thick :=cjo.D['thick'];
    phbox.holepos :=cjo.D['holepos'];
    phbox.holenum :=cjo.I['holenum'];
    phbox.holecap :=cjo.D['holecap'];
    phbox.size :=cjo.D['size'];
    phbox.ishboxvalue :=cjo.I['ishboxvalue'];

    phbox.name := cjo.S['name'];
    phbox.wlcode := cjo.S['wlcode'];
    phbox.bjcode := cjo.S['bjcode'];
    phbox.wjname := cjo.S['wjname'];
    phbox.model := cjo.S['model'];
    phbox.memo := cjo.S['memo'];
    phbox.bdfile := cjo.S['bdfile'];
    phbox.frametype := cjo.S['边框类型'];
    HSHBoxParamList.Add(phbox);
  end;
  //竖中横
  ja := SO(jo.S['SHBoxParam']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(phbox);
    inc(id);
    phbox.id := id;
    phbox.height :=cjo.D['height'];
    phbox.depth :=cjo.D['depth'];
    phbox.thick :=cjo.D['thick'];
    phbox.holepos :=cjo.D['holepos'];
    phbox.holenum :=cjo.I['holenum'];
    phbox.holecap :=cjo.D['holecap'];
    phbox.size :=cjo.D['size'];
    phbox.ishboxvalue :=cjo.I['ishboxvalue'];
    phbox.name := cjo.S['name'];
    phbox.wlcode := cjo.S['wlcode'];
    phbox.bjcode := cjo.S['bjcode'];
    phbox.wjname := cjo.S['wjname'];
    phbox.model := cjo.S['model'];
    phbox.memo := cjo.S['memo'];
    phbox.bdfile := cjo.S['bdfile'];
    phbox.frametype := cjo.S['边框类型'];
    SHBoxParamList.Add(phbox);
  end;
  id := 0;
  jo:=nil;
end;
//初始化掩门配置
procedure TLocalObject.InitDoorConfig(const config:string);
Var
  i, n, id : Integer;
  jo, cjo, ja : ISuperObject;
  pexp       : PDoorsExp;
  ptype      : PDoorsType;
  pparam            : PDoorsParam;
  php               : PDoorHBoxParam;
  ppt               : PDoorPanelType;
  pa                : PDoorAccessory;
  pcolorclass       : PDoorsColorClass;
  pshutterexp       : PDoorsShutterExp;
  pwjbom            : PDoorsWjBom;
  pwjbomdetail      : PDoorsWjBomDetail;
  phandle           : PDoorsHandle;
  phinge            : PDoorsHinge;
  pcurhinge         : PDoorsCurHinge;
  pcolorclass2      : PDoorsColorClass2;
  ppbdetail:    PDoorsPanelBomDetail;
  pxml:PDoorXML;
begin
  jo := TSuperObject.Create();
  jo:=SO(config).O['ymconfig'];;
  ja := SO(jo.S['mExpList']);
  n := ja.AsArray.Length;
  //单门数量类型
  id :=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pexp);
    inc(id);
    pexp.id := id;
    pexp.doornum := cjo.I['doornum'];
    pexp.deleted := False;
    pexp.capnum := cjo.I['capnum'];
    pexp.lkvalue := cjo.I['lkvalue'];
    pexp.name := cjo.S['name'];
    mExpList.Add(pexp);
  end;
  //门类型
  ja := SO(jo.S['mTypeList']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(ptype);
    inc(id);
    ptype.id := id;
    ptype.deleted := False;
    ptype.name := cjo.S['name'];
    ptype.isframe := cjo.B['isframe'];
    ptype.covertype := cjo.I['covertype'];
    ptype.hinge :=  cjo.S['hinge'];
    ptype.hinge1 :=  cjo.S['hinge1'];
    ptype.myclass :=  cjo.S['myclass'];
    ptype.lkvalue :=  cjo.D['lkvalue'];
    ptype.depth :=  cjo.D['depth'];
    ptype.hinge2 :=  cjo.S['hinge2'];
    ptype.eb_lkvalue :=  cjo.D['eb_lkvalue'];
    ptype.eb_ud_lkvalue :=  cjo.D['eb_ud_lkvalue'];
    ptype.color :=  cjo.S['颜色'];
    ptype.defcolor :=  cjo.S['默认颜色'];
    ptype.defdoorframe :=  cjo.S['默认门框'];
    mTypeList.Add(ptype);
  end;
  //掩门参数 门框类型
  ja := SO(jo.S['mParamList']);
  n := ja.AsArray.Length;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pparam);
    pparam.id := id;
    pparam.deleted := False;
    pparam.name := cjo.S['name'];
    pparam.DoorsType := cjo.S['doorstype'];
    pparam.Handle := cjo.S['handle'];
    pparam.wjname := cjo.S['wjname'];
    pparam.hboxname := cjo.S['hboxname'];
    pparam.PanelType := cjo.S['paneltype'];
    pparam.cap := cjo.D['cap'];
    pparam.eb_cap := cjo.D['eb_cap'];
    pparam.vboxname := cjo.S['vboxname'];
    pparam.udboxname := cjo.S['udboxname'];
    pparam.vboxl := cjo.S['vboxl'];
    pparam.udboxl := cjo.S['udboxl'];
    
    pparam.vboxh := cjo.D['vboxh'];
    pparam.udboxh := cjo.D['udboxh'];
    pparam.vthick := cjo.D['vthick'];
    pparam.udthick := cjo.D['udthick'];
    pparam.vboxjtw := cjo.D['vboxjtw'];
    pparam.udboxjtw := cjo.D['udboxjtw'];
    pparam.hboxjtw := cjo.D['hboxjtw'];
    pparam.d3name := cjo.S['d3name'];
    pparam.hbox3d := cjo.S['hbox3d'];
    pparam.ubox3d := cjo.S['ubox3d'];
    pparam.dbox3d := cjo.S['dbox3d'];
    
    pparam.bomtype := cjo.S['bomtype'];
    
    pparam.vdirect := cjo.S['vdirect'];
    pparam.vfbstr := cjo.S['vfbstr'];
    pparam.uddirect := cjo.S['uddirect'];
    pparam.udfbstr := cjo.S['udfbstr'];
    
    pparam.vmemo := cjo.S['vmemo'];
    pparam.udmemo := cjo.S['udmemo'];
    
    pparam.iscalc_framebom := cjo.I['iscalc_framebom'];
    pparam.fbstr := cjo.S['fbstr'];
    pparam.frame_valuel := cjo.D['frame_valuel'];
    pparam.frame_valueh := cjo.D['frame_valueh'];
    pparam.udbox_hbox_value := cjo.D['udbox_hbox_value'];
    pparam.is_xq := cjo.I['is_xq'];
    pparam.cb_yyvalue := cjo.I['cb_yyvalue'];
    pparam.is_buy := cjo.I['is_buy'];
    
    pparam.bdfile := cjo.S['bdfile'];
    pparam.l_bdfile := cjo.S['l_bdfile'];
    pparam.r_bdfile := cjo.S['r_bdfile'];
    pparam.u_bdfile := cjo.S['u_bdfile'];
    pparam.d_bdfile := cjo.S['d_bdfile'];
    
    pparam.left_doorxml := cjo.S['left_doorxml'];
    pparam.right_doorxml := cjo.S['right_doorxml'];
    pparam.doorxml := cjo.S['doorxml'];
    pparam.noframe_bom := cjo.I['noframe_bom'];
    mParamList.Add(pparam);
  end;
  //门拉手
  ja := SO(jo.S['mHandleList']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(phandle);
    inc(id);
    phandle.id := id;
    phandle.deleted := False;
    phandle.name := cjo.S['name'];
    phandle.wjname := cjo.S['wjname'];
    phandle.xpos := cjo.S['xpos'];
    phandle.ypos := cjo.S['ypos'];
    phandle.width := cjo.S['width'];
    phandle.height := cjo.S['height'];
    phandle.depth := cjo.S['depth'];
    phandle.depthpos := cjo.S['depthpos'];
    phandle.bomtype := cjo.S['bomtype'];
    phandle.memo := cjo.S['memo'];
    phandle.holescript := cjo.S['holescript'];
    mHandleList.Add(phandle);
  end;
  //门铰分类
  ja := SO(jo.S['mHingeList']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(phinge);
    phinge.id:= id;
    phinge.deleted:= False;
    phinge.name:= cjo.S['name'];
    phinge.mytype:= cjo.S['mytype'];
    phinge.wjname:= cjo.S['wjname'];
    phinge.min1:= cjo.I['min1'];
    phinge.max1:= cjo.I['max1'];
    phinge.num1:= cjo.I['num1'];

    phinge.min2:= cjo.I['min2'];
    phinge.max2:= cjo.I['max2'];
    phinge.num2:= cjo.I['num2'];

    phinge.min3:= cjo.I['min3'];
    phinge.max3:= cjo.I['max3'];
    phinge.num3:= cjo.I['num3'];

    phinge.min4:= cjo.I['min4'];
    phinge.max4:= cjo.I['max4'];
    phinge.num4:= cjo.I['num4'];
    
    phinge.min5:= cjo.I['min5'];
    phinge.max5:= cjo.I['max5'];
    phinge.num5:= cjo.I['num5'];
    phinge.bomtype:= cjo.S['bomtype'];
    phinge.memo:= cjo.S['memo'];
    
    phinge.iszn:= cjo.I['iszn'];
    phinge.bh:= cjo.I['bh'];

    phinge.alias:= cjo.S['alias'];
    mHingeList.Add(phinge);
  end;

  //门铰
  ja := SO(jo.S['mCurHingeList']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pcurhinge);
    pcurhinge.id:= id;
    pcurhinge.deleted:= False;
    pcurhinge.name:= cjo.S['name'];
    pcurhinge.wjname:= cjo.S['wjname'];
    pcurhinge.bomtype:= cjo.S['bomtype'];
    pcurhinge.memo:= cjo.S['memo'];
    pcurhinge.installtype:= cjo.S['安装方式'];
    pcurhinge.hingetype:= cjo.S['hingetype'];
    mCurHingeList.Add(pcurhinge);
  end;

  //中横框
  ja := SO(jo.S['mDoorHBoxParamList']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(php);
    inc(id);
    php.id:= id;
    php.deleted:= False;
    php.name:= cjo.S['name'];
    php.height:= cjo.D['height'];
    php.depth:= cjo.D['depth'];
    php.thick:= cjo.D['thick'];
    php.wjname:= cjo.S['wjname'];
    php.bomtype:= cjo.S['bomtype'];
    php.memo:= cjo.S['memo'];
    php.direct:= cjo.S['direct'];
    php.fbstr:= cjo.S['fbstr'];
    php.model:= cjo.S['model'];
    php.bdfile:= cjo.S['bdfile'];
    mDoorHBoxParamList.Add(php);
  end;
  //门芯类型
  ja := SO(jo.S['mDoorPanelTypeList']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(ppt);
    inc(id);
    ppt.id:= id;
    ppt.deleted:= False;
    ppt.name:= cjo.S['name'];
    ppt.mytype:= cjo.S['mytype'];
    ppt.thick:= cjo.I['thick'];
    ppt.lfb:= cjo.D['lfb'];
    ppt.hfb:= cjo.D['hfb'];
    ppt.bomtype:= cjo.S['bomtype'];
    ppt.iswhole:= cjo.B['iswhole'];
    ppt.bktype:= cjo.S['bktype'];
    ppt.lmax:= cjo.I['lmax'];
    ppt.lmin:= cjo.I['lmin'];
    ppt.wmax:= cjo.I['wmax'];
    ppt.wmin:= cjo.I['wmin'];
    ppt.is_buy:= cjo.I['is_buy'];
    ppt.direct:= cjo.S['direct'];
    ppt.fbstr:= cjo.S['fbstr'];
    ppt.pnl3d:= cjo.S['pnl3d'];
    ppt.memo:= cjo.S['memo'];
    ppt.panelbom:= cjo.S['panelbom'];
    ppt.ypos:= cjo.I['ypos'];
    ppt.memo2:= cjo.S['memo2'];
    ppt.memo3:= cjo.S['memo3'];
    ppt.bdfile:= cjo.S['bdfile'];
    mDoorPanelTypeList.Add(ppt);
  end;
  //五金配件
  ja := SO(jo.S['mAccessoryList']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pa);
    inc(id);
    pa.id:= id;
    pa.deleted:= False;
    pa.name:= cjo.S['name'];
    pa.myunit:= cjo.S['unit'];
    pa.mytype:= cjo.S['mytype'];
    pa.bomtype:= cjo.S['bomtype'];
    pa.color:= cjo.S['color'];
    pa.memo:= cjo.S['memo'];
    pa.bdfile:= cjo.S['bdfile'];
    mAccessoryList.Add(pa);
  end;

  //颜色分类
  ja := SO(jo.S['mColorClassList']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pcolorclass);
    inc(id);
    pcolorclass.id:= id;
    pcolorclass.deleted:= False;
    pcolorclass.color:= cjo.S['color'];
    pcolorclass.myclass:= cjo.S['myclass'];
    pcolorclass.mat:= cjo.S['mat'];
    pcolorclass.color2:= cjo.S['color2'];
    pcolorclass.color3:= cjo.S['color3'];
    pcolorclass.color4:= cjo.S['color4'];
    mColorClassList.Add(pcolorclass);
  end;

  //颜色分类2
  ja := SO(jo.S['mColorClass2List']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pcolorclass2);
    inc(id);
    pcolorclass2.id:= id;
    pcolorclass2.deleted:= False;
    pcolorclass2.color:= cjo.S['color'];
    pcolorclass2.bktype:= cjo.S['bktype'];
    pcolorclass2.bkcolor1:= cjo.S['bkcolor1'];
    pcolorclass2.bkcolor2:= cjo.S['bkcolor2'];
    pcolorclass2.bkcolor3:= cjo.S['bkcolor3'];
    pcolorclass2.bkcolor4:= cjo.S['bkcolor4'];
    mColorClass2List.Add(pcolorclass2);
  end;
  //百叶板配置
  ja := SO(jo.S['mShutterExpList']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pshutterexp);
    pshutterexp.deleted:= False;
    pshutterexp.PanelType:= cjo.S['paneltype'];
    pshutterexp.height:= cjo.D['height'];
    pshutterexp.width:= cjo.D['width'];
    pshutterexp.heightcap:= cjo.D['heightcap'];
    pshutterexp.widthcap:= cjo.D['widthcap'];
    pshutterexp.minheight:= cjo.D['minheight'];
    pshutterexp.minwidth:= cjo.D['minwidth'];
    mShutterExpList.Add(pshutterexp);
  end;
  //五金配件分类
  ja := SO(jo.S['mWJBomList']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pwjbom);
    inc(id);
    pwjbom.id := id;
    pwjbom.deleted := False;
    pwjbom.name := cjo.S['name'];
    mWJBomList.Add(pwjbom);
  end;
  //五金配件分类数据
  ja := SO(jo.S['mWJBomDetailList']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pwjbomdetail);
    inc(id);
    pwjbomdetail.id:= id;
    pwjbomdetail.deleted:= False;
    pwjbomdetail.name:= cjo.S['name'];
    pwjbomdetail.bomname:= cjo.S['bomname'];
    pwjbomdetail.l:= cjo.S['l'];
    pwjbomdetail.d:= cjo.S['d'];
    pwjbomdetail.num:= cjo.S['num'];
    pwjbomdetail.door_bh:= cjo.I['door_bh'];
    pwjbomdetail.opendirect:= cjo.S['opendirect'];
    pwjbomdetail.bktype:= cjo.S['bktype'];
    mWJBomDetailList.Add(pwjbomdetail);
  end;
  //门芯附加物料
  ja := SO(jo.S['mDoorPanelBomDetailList']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(ppbdetail);
    inc(id);
    ppbdetail.id:= id;
    ppbdetail.deleted:= False;
    ppbdetail.bomclass:= cjo.S['bomclass'];
    ppbdetail.bomname:= cjo.S['bomname'];
    ppbdetail.l:= cjo.S['l'];
    ppbdetail.w:= cjo.S['w'];
    ppbdetail.h:= cjo.S['h'];
    ppbdetail.mat:= cjo.S['mat'];
    ppbdetail.color:= cjo.S['color'];
    ppbdetail.bomtype:= cjo.S['bomtype'];
    ppbdetail.memo:= cjo.S['memo'];
    ppbdetail.lmin:= cjo.I['lmin'];
    ppbdetail.lmax:= cjo.I['lmax'];
    ppbdetail.hmin:= cjo.I['hmin'];
    ppbdetail.hmax:= cjo.I['hmax'];
    ppbdetail.num:= cjo.I['num'];
    ppbdetail.bdfile:= cjo.S['bdfile'];
    mDoorPanelBomDetailList.Add(ppbdetail);
  end;
  //XML单门结构
  ja := SO(jo.S['mDoorXMLList']);
  n := ja.AsArray.Length;
  id:=0;
  for i:=0 to n-1 do
  begin
    cjo := ja.AsArray.O[i];
    new(pxml);
    inc(id);
    pxml.id := id;
    pxml.deleted := False;
    pxml.name := cjo.S['name'];
    pxml.xml := cjo.S['xml'];
    mDoorXMLList.Add(pxml);
  end;
  id := 0;
  jo:=nil;
end;
//趟门掩门计算，类别字段收集，趟门掩门数据收集
function TLocalObject.GetXmlDes(const xml: string; const config:string): string;
Var
i : Integer;
node:  IXMLNode;
xdoc:  IXMLDocument;
jsonstr : string;
cjo, doorandsliding :ISuperObject;
begin
  result := '';
  if not Assigned(bomdeslist) then bomdeslist := TStringList.Create;
  if not Assigned(doordeslist) then doordeslist := TStringList.Create;
  if not Assigned(slidingdeslist) then slidingdeslist := TStringList.Create;

  bomdeslist.Clear;
  doordeslist.Clear;
  slidingdeslist.Clear;

  InitGtConfig(config);       //初始化柜体配置数据 --- 高级编程lua文件 + 链接对应数据库数据
  InitSlidingConfig(config);  // 初始化趟门配置数据
  InitDoorConfig(config);     // 初始化掩门配置数据

  //try
    if xml <> '' then
    begin
      doorandsliding:=FindDesList(xml);
      if slidingdeslist.count > 0 then jsonstr :='{"slidingdeslist":['+Format('"%s"', [slidingdeslist[0]])
      else jsonstr :='{"slidingdeslist":[';
      for i:=1 to slidingdeslist.count-1 do
      begin
        jsonstr:= jsonstr+Format(',"%s"', [slidingdeslist[i]]);
      end;
      jsonstr:= jsonstr+'],';
      if doordeslist.count > 0 then jsonstr :=jsonstr+'"doordeslist":['+Format('"%s"', [doordeslist[0]])
      else jsonstr :=jsonstr+'"doordeslist":[';
      for i:=1 to doordeslist.count-1 do
      begin
        jsonstr:= jsonstr+Format(',"%s"', [doordeslist[i]]);
      end;
      jsonstr:= jsonstr+'],';
      if bomdeslist.count > 0 then jsonstr :=jsonstr+'"bomdeslist":['+Format('"%s"', [bomdeslist[0]])
      else jsonstr :=jsonstr+'"bomdeslist":[';
      for i:=1 to bomdeslist.count-1 do
      begin
        jsonstr:= jsonstr+Format(',"%s"', [bomdeslist[i]]);
      end;
      jsonstr:= jsonstr+'],';
      if (doorandsliding = nil) then
      begin
        doorandsliding := TSuperObject.Create();
        doorandsliding.S['掩门,掩门']:='[]';
        doorandsliding.S['趟门,趟门']:='[]'
      end
      else
      begin
        if doorandsliding.S['掩门,掩门'] = '' then doorandsliding.S['掩门,掩门']:='[]';
        if doorandsliding.S['趟门,趟门'] = '' then doorandsliding.S['趟门,趟门']:='[]';
      end;
      jsonstr:=jsonstr+'"door":'+doorandsliding.S['掩门,掩门'];
      jsonstr:=jsonstr+',"sliding":'+doorandsliding.S['趟门,趟门'];
      jsonstr:= jsonstr+'}';
      Result:=jsonstr;
    end;
  //except
  //end;
  ClearSlidingAndDoorList;   //释放趟门，掩门对象
end;
//柜体计算
function TLocalObject.Xml2JsonBom(const xml, config: string): string;
Var
  s1, s2, des, desstring: string;
  i, j, childnum, k, n: Integer;
  p                 : PBomOrderItem;
  pslibom           : PSlidingBomRecord;
  phinfo, phinfo2   : THolePointInfo;
  product_item      : TProductItem;
  cjo, ja, jo : ISuperObject;
  jts:TSuperTableString;
  item: TSuperAvlEntry;
begin
  result := '0';
  cjo:=SO(config).O['gtconfig'];
  if not Assigned(HoleWjList) then InitHoleWjList(cjo);   //孔位五金数据
  if not Assigned(ruleHash) then InitBomHash(cjo);    //初始化 变量
  if not Assigned(gBoardMatList) then InitBoardMatList(cjo);   //物料报表的材料别名转换 用到的材料表
  if not Assigned(gErpItemList) then       //感觉用不上
  begin
    gErpItemList := TList.Create;
    InitErpList(gErpItemList, cjo);
  end;

  jts:= cjo.O['desdata'].AsObject;         //初始化类别字段数据库数据
  n := jts.GetNames.AsArray.Length;
  for i:=0 to n-1 do
  begin
    des:= jts.GetNames.AsArray.S[i];
    desstring:=jts.S[des];
    desdata.Add(des, desstring);
  end;
  mUserName := cjo.S['username'];
  mOrderName :=cjo.S['ordername'];
  mDistributor := cjo.S['distributor'];
  mAddress := cjo.S['address'];
  mPhone := cjo.S['phone'];
  mFax := cjo.S['fax'];
  mMemo := cjo.S['memo'];
  mCustomerName := cjo.S['customername'];
  mCustomerCellPhone := cjo.S['cutomercellphone'];
  mCustomerPhone :=cjo.S['customerphone'] ;
  mCustomerAddress := cjo.S['customeraddress'];
  if cjo.S['dt'] ='' then mDateTime :=0
  else mDateTime := strtofloat(cjo.S['dt']);
  cjo :=nil;
  try
  //  if xml <> '' then
  //  begin
      LoadXML2Bom(xml);             //计算柜子
      //LoadXML2Quo(xml);
  //   end;
  except
  //  result :=GetBomlistString;
  //  exit;
  end;

  InitBgMinAndMax;
    //初始化BomCalcHoleUnit
  CalcHoleUnit.mHPInfoList := mHPInfoList;
  CalcHoleUnit.mKCInfoList := mKCInfoList;
  CalcHoleUnit.mBGHash := gBGHash;
  CalcHoleUnit.mTmpExp := mTmpExp;
  CalcHoleUnit.holeconfigHash := holeconfigHash;
  CalcHoleUnit.kcconfigHash := kcconfigHash;
  CalcHoleUnit.cncX2dToBdGraph := cncX2dToBdGraph;
  CalcHoleUnit.mIIHoleCalcRule := mIIHoleCalcRule;
  CalcLgFlag;
  CalcBomWj;
  CalcHoleAndKc;
  CalcHoleWj;

  //左右翻板，需要进行AB面反转
  for i := 0 to bomlist.Count - 1 do
  begin
    p := bomlist[i];
    p.bg_data := ToBGInfo(p);
    if p.bg <> 'BG::RECT' then Continue;
    if p.trans_ab then TransAB(p);
    //if (p.direct=1) or (p.direct=5) then TransAB_NoChange(p);   //横板-层板类
    //if (p.direct=2) or (p.direct=3) then TransAB_NoChange(p);   //竖横板-背板类

    //AB面数据输出
    for j := 0 to 100 do
    begin
      if p.ahole_index[j] >= 0 then
      begin
        phinfo := mHPInfoList[p.ahole_index[j]];
        if (p.direct = 5) or (p.direct = 3) or (p.direct = 4) then //侧板-竖纹，背板-竖纹
        begin
          p.a_hole_info := p.a_hole_info + Format('(%d,%d,%s,%d),', [phinfo.x, phinfo.y, phinfo.r, phinfo.offset]);
        end;
        if (p.direct = 2) or (p.direct = 1) or (p.direct = 6) then //层板-横纹
        begin
          p.a_hole_info := p.a_hole_info + Format('(%d,%d,%s,%d),', [phinfo.y, phinfo.x, phinfo.r, phinfo.offset]);
        end;
      end;
      if p.bhole_index[j] >= 0 then
      begin
        phinfo := mHPInfoList[p.bhole_index[j]];
        if (p.direct = 5) or (p.direct = 3) or (p.direct = 4) then //侧板-竖纹，背板-竖纹
        begin
          p.b_hole_info := p.b_hole_info + Format('(%d,%d,%s,%d),', [phinfo.x, phinfo.y, phinfo.r, phinfo.offset]);
        end;
        if (p.direct = 2) or (p.direct = 1) or (p.direct = 6) then //层板-横纹
        begin
          p.b_hole_info := p.b_hole_info + Format('(%d,%d,%s,%d),', [phinfo.y, phinfo.x, phinfo.r, phinfo.offset]);
        end;
      end;
    end;

    s1 := '';
    s2 := '';
    if p.hole_back_cap > 0 then s1 := IntToStr(p.hole_back_cap);
    if p.hole_2_dist > 0 then s2 := IntToStr(p.hole_2_dist);
    p.holeconfig_flag := StringReplace(p.holeconfig_flag, '$X', s1, [rfReplaceAll]);
    p.holeconfig_flag := StringReplace(p.holeconfig_flag, '$D', s2, [rfReplaceAll]);
  end;
  //计算物料分解
  for i := 0 to bomlist.Count - 1 do
  begin
    p := bomlist[i];
    if ((p.outputtype = '物料') or (p.outputtype = '无')) then p.isoutput := False;
    if (p.outputtype = '报价物料') then p.isoutput := True;
    if p.desc = '' then p.isoutput := False;
    if p.childbom = '' then Continue;
    product_item := mProductList[p.cid];
    childnum := LoadChildBom(p, p.cid, product_item.bh, p.childbom, bomlist, p.id, p.l, p.p, p.h, p.mat, p.color, p.memo, p.gno, p.gdes, p.gcb, p.myclass, p.bomstd, p.num);
    if childnum > 0 then p.isoutput := False;
  end;
  CalcLineCombine;
  CalcSeq;

  //计算是否有通孔
  for i := 0 to bomlist.Count - 1 do
  begin
    p := bomlist[i];
    if (mIIHoleCalcRule<>nil) and (mIIHoleCalcRule.I[IntToStr(Round(p.bh))]=2) then continue;
    for j := 0 to 100 do
    begin
      if p.ahole_index[j] >= 0 then
      begin
        phinfo := mHPInfoList[p.ahole_index[j]];
        if phinfo.htype = 'I' then      //垂直孔
        begin
          for k := 0 to 100 do
          begin
            if p.bhole_index[k] >= 0 then
            begin
              phinfo2 := mHPInfoList[p.bhole_index[k]];
              if (phinfo2.htype = 'I') and (phinfo.x = phinfo2.x) and (phinfo.y = phinfo2.y) and (phinfo.r = phinfo2.r) then //垂直孔
              begin
                phinfo.htype := 'I+I';
                phinfo2.htype := 'I+I';
                break;
              end;                      //if
            end;                        // if
          end;                          //for k
        end;                            // if phinfo.htype='I' then //垂直孔
      end;
    end;
  end;
  //自定义 名称、材料、颜色
  for i := 0 to bomlist.Count - 1 do
  begin
    p := bomlist[i];
    GetBomUserDefine(p);
  end;
  //物料报表的材料别名转换[用于报价]
  for i := 0 to bomlist.Count - 1 do
  begin
    p := bomlist[i];
    GetMatAlias(p.mat, p.color, p.h, p.mat, p.mat2, p.mat3);
  end;
  result :=GetBomlistString;
  ClearAllBomList;
  //WriteStringToFile(GetQuickDrawPath()+'123.txt',result);
end;


procedure TLocalObject.ClearTempList;
var
  i                 : Integer;
begin
  for i := 0 to mAllWjList.Count - 1 do
  begin
    dispose(mAllWjList[i]);
  end;
  mAllWjList.Clear;
end;

initialization
  gLocalObject := TLocalObject.Create;
  //gLocalObject.InitData();
  //gLocalObject.SlidingAndDoorInit();
  //gLocalObject.CallThread();

finalization
  FreeAndNil(gLocalObject);
  CoUninitialize;

end.


