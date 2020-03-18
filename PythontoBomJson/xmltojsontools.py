#  -*- coding:utf-8 -*-
'''
vesion 1.0.1
2019/8/5
author:litao
'''
import pypyodbc
import os
from PythontoBomJson.useful_tools import base_dir
def check(childVarstr):
    if childVarstr[len(childVarstr)-1] =='-' or childVarstr[len(childVarstr)-1] =='+' or childVarstr[len(childVarstr)-1] =='*' or childVarstr[len(childVarstr)-1] =='/':
        childVarstr = childVarstr[0:len(childVarstr)-1]
    for i in range(0, len(childVarstr)):
        string = childVarstr[i]
        exp = ['-','+','*','/']
        if childVarstr[i] in exp and childVarstr[i+1] in exp:
            childVarstr = childVarstr[0:i]+childVarstr[i+1:]
            break
    return childVarstr
def Uncode(content):
    if isinstance(content, str):
        # s=u"中文"
        content = content
        return content
    else:
        # s="中文"
        try:
            content = content.decode('utf-8')
            return content
        except:
            ## content
            if content==None:
                return ''
            return content
def SetBGParam(poi, tucan):
    poi['mBGParam'] = tucan
    if poi['parent']==None : return
    n = tucan.find('^Inherit^:^1^')
    if n <= 0 : return
    pp = poi['parent']
    tucan= pp['mBGParam'].replace('^Inherit^:^1^ ', '')
    poi['mBGParam'] = tucan.replace('{', '{^Inherit^:^1^ ')
def creatxml(link, xmlfile):
    if isinstance(link, str):
        pass
    else:
        link = link.decode('utf-8')
    XSDBfile = base_dir.decode('gbk') + '\\data\\XScriptDb.mdb'
    conn = pypyodbc.win_connect_mdb(r'DRIVER={Microsoft Access Driver (*.mdb  *.accbd)};DBQ=' + XSDBfile)
    cur = conn.cursor()
    sql = "select xml from  xml_template where path='%s'" % (link)
    cur.execute(sql)
    t = cur.fetchall()
    if t == []:
        return ''
    else:
        xmlstr = t[0][0].encode('UTF8').replace('"', "'")
        ## json.dumps(xmlstr,encoding='utf8',ensure_ascii=False).encode('gb2312')
        f = open(xmlfile, 'wb')
        f.write('<场景>' + '\n  ' + xmlstr + '\n' + '</场景>')
        f.close
        return xmlfile
#def InitPSlidingBomRecord()