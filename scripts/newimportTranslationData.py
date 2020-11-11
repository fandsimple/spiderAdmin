#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Time    : 2020/2/17
@Author  : fanding
@File    : importCveItemToExcel.py
'''
# 从数据库中导出数据到excel数据表中

import xlrd
import pdb
import requests
import execjs
import json
import xlsxwriter
import logging
import sys
import os
import django
import time
import socket
import socks


sys.path.append('/root/cnnvd/code/stongerSpider/spiderAdmin/')  # 将项目路径添加到系统搜寻路径当中
os.environ['DJANGO_SETTINGS_MODULE'] = 'spiderAdmin.settings'  # 设置项目的配置文件
django.setup()  # 加载项目配置
from spiderTask.models import Translation


class Py4Js():
    def __init__(self):
        self.ctx = execjs.compile(""" 
    function TL(a) { 
    var k = ""; 
    var b = 406644; 
    var b1 = 3293161072;       
    var jd = "."; 
    var $b = "+-a^+6"; 
    var Zb = "+-3^+b+-f";    
    for (var e = [], f = 0, g = 0; g < a.length; g++) { 
        var m = a.charCodeAt(g); 
        128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
        e[f++] = m >> 18 | 240, 
        e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
        e[f++] = m >> 6 & 63 | 128), 
        e[f++] = m & 63 | 128) 
    } 
    a = b; 
    for (f = 0; f < e.length; f++) a += e[f], 
    a = RL(a, $b); 
    a = RL(a, Zb); 
    a ^= b1 || 0; 
    0 > a && (a = (a & 2147483647) + 2147483648); 
    a %= 1E6; 
    return a.toString() + jd + (a ^ b) 
  };      
  function RL(a, b) { 
    var t = "a"; 
    var Yb = "+"; 
    for (var c = 0; c < b.length - 2; c += 3) { 
        var d = b.charAt(c + 2), 
        d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
        d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
        a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
    } 
    return a 
  } 
 """)

    def getTk(self, text):
        return self.ctx.call("TL", text)

def translate(desStr):
    headers = {
        'authority': 'translate.google.cn',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'accept': '*/*',
        'x-client-data': 'CJW2yQEIpbbJAQjBtskBCKmdygEIl6zKAQiZtcoBCPbHygEI58jKAQjpyMoBCLTLygEIwtfKAQif2MoB',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://translate.google.cn/',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'NID=204=R54bjLuQrLFqk57rr2RdxRKmOgebINvfJFdI46JmyVpVUj_33uHLz3UpsSTv23nx-43w3lCqyNCd9uOE-Bv_FhtdKiwOSZva1nPWhOrcPgWLK6K67vLNC7Kdjzh3E0avt_nvLPdnKxlzkOoYAXcYV7bIVAvz3P1eLTPIm71G3NQ; _ga=GA1.3.848964483.1602648222; _gid=GA1.3.1623937456.1602648222',
    }
    js = Py4Js()
    params = (
        ('client', 'webapp'),
        ('sl', 'en'),
        ('tl', 'zh-CN'),
        ('hl', 'zh-CN'),
        ('dt', ['at', 'bd', 'ex', 'ld', 'md', 'qca', 'rw', 'rm', 'sos', 'ss', 't']),
        ('otf', '1'),
        ('pc', '1'),
        ('ssel', '3'),
        ('tsel', '3'),
        ('kc', '2'),
        ('tk', js.getTk(desStr)),
        ('q', desStr),
    )
    # socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 10808)
    # socket.socket = socks.socksocket


    proxies = {'http': 'socks5://localhost:10808', 'https': 'socks5://localhost:10808'}
    response = requests.get('https://translate.google.cn/translate_a/single', headers=headers, params=params,
                            proxies=proxies, verify=False)

    # response = requests.get('https://translate.google.cn/translate_a/single', headers=headers, params=params,verify=False)


    dataList = json.loads(response.text)[0]
    resStr = ''
    for data in dataList:
        if data[0]:
            resStr += data[0]
    return resStr


if __name__ == '__main__':
    # 获取一个Book对象
    book = xlrd.open_workbook("./dealfiles/translate/1106_t.xls")

    # 获取一个sheet对象的列表
    sheet = book.sheets()[0]

    # 遍历每一个sheet，输出这个sheet的名字（如果是新建的一个xls表，可能是sheet1、sheet2、sheet3）

    resultList = []
    rows = sheet.get_rows()
    for i, row in enumerate(rows):
        cnnvdId = row[0].value
        cveId = row[1].value
        ownId = row[2].value
        sourceDesc = row[3].value
        # 调用翻译接口，进行翻译
        try:
            translationDes = translate(sourceDesc)
        except:
            translationDes = '存在安全漏洞，该漏洞源于，该漏洞允许攻击者。'
        # translationDes = translate(sourceDesc)


        # translationDes = translate(sourceDesc)
        tr = Translation()
        tr.cnnvd_id = cnnvdId
        tr.cve_id = cveId
        tr.own_ids = ownId
        tr.vul_description = sourceDesc
        tr.vul_detail_translation = translationDes
        tr.save()
        time.sleep(0.5)
        print('完成%d条翻译' % i)




