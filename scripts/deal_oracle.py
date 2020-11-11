#!/usr/bin/env python
# -*- coding:utf-8 -*-

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
import re


sys.path.append('/root/cnnvd/code/stongerSpider/spiderAdmin/')  # 将项目路径添加到系统搜寻路径当中
os.environ['DJANGO_SETTINGS_MODULE'] = 'spiderAdmin.settings'  # 设置项目的配置文件
django.setup()  # 加载项目配置
from spiderTask.models import Translation


allDataList = Translation.objects.all()

for data in allDataList:
    desc = data.vul_description
    p_c_strList = re.findall('组件和版本信息如下：(\(.*--.*--.*\)?)', desc, re.DOTALL)
    # if len(p_c_strList) > 1 or len(p_c_strList) == 0:
    #     # for p_c_str in p_c_strList:
    #     #     resList = p_c_str.strip("（").strip('）').split('--')
    #     #     data.vul_detail_translation = desc + '\r\n' + resList[0] + ' ' + resList[1] + ' ' + resList[2] + '存在安全漏洞',
    #     pass
    # else:
    if len(p_c_strList) == 1:
        resList = p_c_strList[0].strip("(").strip(')').split('--')
        data.vul_detail_translation = desc + '\r\n' + resList[0] + ' ' + resList[1] + ' ' + resList[2] + '存在安全漏洞，该漏洞允许攻击者'
    data.save()
