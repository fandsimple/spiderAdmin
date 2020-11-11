#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Time    : 2020/2/17
@Author  : fanding
@File    : importCveItemToExcel.py
'''
# 从数据库中导出数据到excel数据表中
import xlwt
import pymysql
import pdb
import logging
import xlsxwriter
import datetime
import logging

class MYSQL:
    def __init__(self):
        pass

    def close(self):
        self._cursor.close()
        self._connect.close()

    def connectDB(self):
        try:
            self._connect = pymysql.Connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                passwd='root',
                db='spider',
                charset='utf8'
            )
            return 0
        except:
            return -1

    def export(self, table_name, output_path):
        self._cursor = self._connect.cursor()
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        # current_data_sql = 'select * from ' + table_name + ' where colletion_time="%s-%s-%s";' % (year, month, day)
        current_data_sql = 'select * from ' + table_name
        logging.info(current_data_sql)
        count = self._cursor.execute(current_data_sql)
        # select * from cve_item_info where colletion_time="2020-10-13";
        if count == 0:
            logging.info('数据表中没有数据，无法导出')
            return
        # 重置游标的位置
        self._cursor.scroll(0, mode='absolute')
        # 搜取所有结果
        results = self._cursor.fetchall()
        # 获取MYSQL里面的数据字段名称
        fields = self._cursor.description
        workbook = xlsxwriter.Workbook(output_path)
        sheet = workbook.add_worksheet("未整理标号表")
        # 写上字段信息
        ignore_fields = ['updateTime', 'createTime', 'orderId']
        for field in range(3, len(fields)):
            if fields[field][0] in ignore_fields:
                continue
            sheet.write_string(0, field, fields[field][0])
        # 获取并写入数据段信息
        for row in range(1, len(results) + 1):
            for col in range(0, len(fields)):
                if fields[col][0] in ignore_fields:
                    continue
                sheet.write_string(row, col, u'%s' % results[row - 1][col])
        workbook.close()


if __name__ == '__main__':
    mysql = MYSQL()
    flag = mysql.connectDB()
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    if flag == -1:
        print('数据库连接失败')
    else:
        print('数据库连接成功')
        mysql.export('translation', './dealfiles/translate/整理好的翻译-%s-%s-%s.xls' % (year, month, day))
    mysql.close()

# todo: 删除前三列优化