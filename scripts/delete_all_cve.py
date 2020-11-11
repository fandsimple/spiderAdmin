#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import pdb
import sys
import django
import json
import requests
import time

sys.path.append('/Users/fanding/gitProjects/stongerSpider/spiderAdmin')  # 将项目路径添加到系统搜寻路径当中
os.environ['DJANGO_SETTINGS_MODULE'] = 'spiderAdmin.settings'  # 设置项目的配置文件
django.setup()  # 加载项目配置

from spiderTask.models import CveItemInfo

if __name__ == '__main__':
    # 删除 cve_item表中所有数据
    res = CveItemInfo.objects.all().delete()
    print('*** delete sucess ***')

