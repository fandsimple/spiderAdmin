#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import pdb
import sys
import django
import json
import requests
import time
import logging
import datetime
import xlrd
import xlwt

from django.db.models import Q

sys.path.append('/Users/fanding/gitProjects/stongerSpider/spiderAdmin')  # 将项目路径添加到系统搜寻路径当中
os.environ['DJANGO_SETTINGS_MODULE'] = 'spiderAdmin.settings'  # 设置项目的配置文件
django.setup()  # 加载项目配置

from spiderTask.models import CveItem


def get_data():
    logging.info('开始获取数据')

    today_year, today_month, today_day, = datetime.date.today().year, datetime.date.today().month, datetime.date.today().day
    allCveItem = CveItem.objects.filter(
        Q(createTime__year=today_year) & Q(createTime__month=today_month) & Q(createTime__day=today_day))
    # for civItem in allCveItem:
    #     pass

    # data_file = xlrd.open_workbook('/Users/fanding/Desktop/reslut1.xls')
    # all_data_sheet = data_file.sheet_by_name('总数据')
    # cols = all_data_sheet.ncols
    # header = []
    # for col_index in range(cols):
    #     header.append(all_data_sheet.cell_value(0, col_index))
    # print(header)
    # headers = ['vul_menace_type', 'verification_information', 'references', 'cwe_id', 'data_update_state', 'learn_more', 'cvsss3_base_score', 'revision_history', 'security_bulletin', 'cvsss2_attack_complexity', 'id', 'software_version', 'credit', 'vul_details_textual', 'original_bulletin', 'cvsss3_security', 'vendor_url', 'cvsss2_base_score', 'cvsss3_influence_score', 'contact_way', 'vul_from', 'cvsss2_security', 'cvsss2_utilizability', 'exploit_Info', 'poc_download_url', 'data_source', 'cvsss2_accredit', 'cve_id', 'release_date', 'cvsss3_utilizability', 'vul_reliability', 'assigning_cna', 'cvsss2_vector', 'product_link', 'collection_url', 'last_revised_date', 'source_message_content', 'affected_products', 'vul_impact', 'cvsss2_attack_vector', 'vendor_confirmed', 'vul_name_textual', 'cvsss2_influence_score', 'cvsss3_privilege_require', 'fix_available', 'alias', 'is_public_disclosure', 'operating_system', 'vul_solution', 'own_ids', 'vul_description_textual', 'vul_remote', 'cvsss3_vector', 'vul_cause', 'cvsss2_integrality', 'cvsss3_exploit_score', 'cvsss3_integrality', 'label', 'colletion_time', 'vul_local', 'affected_vendors', 'cvsss3_user_inactive', 'cvsss2_exploit_score', 'advisory_id', 'cvsss3_attack_complexity', 'cvsss3_scope', 'cvsss3_attack_vector', 'vul_type_textual', 'is_be_used', 'zero_day_time']

    write_excel(allCveItem)


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


def write_excel(allData):
    f = xlwt.Workbook()  # 创建工作簿
    all_data_sheet = f.add_sheet(u'all_data', cell_overwrite_ok=True)  # 创建sheet
    headers = ['vul_menace_type', 'verification_information', 'references', 'cwe_id', 'data_update_state', 'learn_more',
               'cvsss3_base_score', 'revision_history', 'security_bulletin', 'cvsss2_attack_complexity', 'id',
               'software_version', 'credit', 'vul_details_textual', 'original_bulletin', 'cvsss3_security',
               'vendor_url', 'cvsss2_base_score', 'cvsss3_influence_score', 'contact_way', 'vul_from',
               'cvsss2_security', 'cvsss2_utilizability', 'exploit_Info', 'poc_download_url', 'data_source',
               'cvsss2_accredit', 'cve_id', 'release_date', 'cvsss3_utilizability', 'vul_reliability', 'assigning_cna',
               'cvsss2_vector', 'product_link', 'collection_url', 'last_revised_date', 'source_message_content',
               'affected_products', 'vul_impact', 'cvsss2_attack_vector', 'vendor_confirmed', 'vul_name_textual',
               'cvsss2_influence_score', 'cvsss3_privilege_require', 'fix_available', 'alias', 'is_public_disclosure',
               'operating_system', 'vul_solution', 'own_ids', 'vul_description_textual', 'vul_remote', 'cvsss3_vector',
               'vul_cause', 'cvsss2_integrality', 'cvsss3_exploit_score', 'cvsss3_integrality', 'label',
               'colletion_time', 'vul_local', 'affected_vendors', 'cvsss3_user_inactive', 'cvsss2_exploit_score',
               'advisory_id', 'cvsss3_attack_complexity', 'cvsss3_scope', 'cvsss3_attack_vector', 'vul_type_textual',
               'is_be_used', 'zero_day_time']

    for row_index in range(len(allData) + 1):
        if row_index == 0:  # 生成第一行
            for col_index in range(0, len(headers)):
                all_data_sheet.write(row_index, col_index, headers[col_index], set_style('Times New Roman', 220, True))
            continue
        all_data_sheet.write(row_index, get_col_index('cveSource'), allData[row_index - 1].cveSource)
        all_data_sheet.write(row_index, get_col_index('cveCode'), allData[row_index - 1].cveCode)
        all_data_sheet.write(row_index, get_col_index('pubTime'), allData[row_index - 1].pubTime.strftime('%Y-%m-%d'))
        all_data_sheet.write(row_index, get_col_index('cveItemUrl'), allData[row_index - 1].cveItemUrl)
        all_data_sheet.write(row_index, get_col_index('cveDesc'), allData[row_index - 1].cveDesc)
        all_data_sheet.write(row_index, get_col_index('createTime'), allData[row_index - 1].createTime.strftime('%Y-%m-%d'))
        all_data_sheet.write(row_index, get_col_index('cveScore'), allData[row_index - 1].cveScore)

    f.save('/Users/fanding/Desktop/test.xls')  # 保存文件


def get_col_index(dbFieldName):
    index_map = {'cveSource': 25, 'cveCode': 27, 'pubTime': 28, 'cveItemUrl': 34, 'cveDesc': 50, 'createTime': 58, 'cveScore': 6}
    return index_map[dbFieldName]


def get_index_Template():
    headers = ['vul_menace_type', 'verification_information', 'references', 'cwe_id', 'data_update_state',
               'learn_more',
               'cvsss3_base_score', 'revision_history', 'security_bulletin', 'cvsss2_attack_complexity', 'id',
               'software_version', 'credit', 'vul_details_textual', 'original_bulletin', 'cvsss3_security',
               'vendor_url', 'cvsss2_base_score', 'cvsss3_influence_score', 'contact_way', 'vul_from',
               'cvsss2_security', 'cvsss2_utilizability', 'exploit_Info', 'poc_download_url', 'data_source',
               'cvsss2_accredit', 'cve_id', 'release_date', 'cvsss3_utilizability', 'vul_reliability',
               'assigning_cna',
               'cvsss2_vector', 'product_link', 'collection_url', 'last_revised_date', 'source_message_content',
               'affected_products', 'vul_impact', 'cvsss2_attack_vector', 'vendor_confirmed', 'vul_name_textual',
               'cvsss2_influence_score', 'cvsss3_privilege_require', 'fix_available', 'alias',
               'is_public_disclosure',
               'operating_system', 'vul_solution', 'own_ids', 'vul_description_textual', 'vul_remote',
               'cvsss3_vector',
               'vul_cause', 'cvsss2_integrality', 'cvsss3_exploit_score', 'cvsss3_integrality', 'label',
               'colletion_time', 'vul_local', 'affected_vendors', 'cvsss3_user_inactive', 'cvsss2_exploit_score',
               'advisory_id', 'cvsss3_attack_complexity', 'cvsss3_scope', 'cvsss3_attack_vector',
               'vul_type_textual',
               'is_be_used', 'zero_day_time']
    resData = {}

    data = {'data_source': 'cveSource', 'cve_id': 'cveCode', 'release_date': 'pubTime',
            'collection_url': 'cveItemUrl', 'vul_description_textual': 'cveDesc', 'colletion_time': 'createTime',
            'cvsss3_base_score': 'cveScore'}
    for key, value in data.items():
        for i, resultValue in enumerate(headers):
            if key == resultValue:
                resData[value] = i
    print(resData)


if __name__ == '__main__':
    get_data()
    # get_index_Template()
