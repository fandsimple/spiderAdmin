from django.db import models

from datetime import datetime
from time import time
from django.db import models
import django.utils.timezone as timezone


class BaseMode(models.Model):
    class Meta:
        abstract = True

    def to_dict(self, *ignore_fileds):
        '''将一个 model 转换成一个 dict'''
        attr_dict = {}
        for field in self._meta.fields:  # 遍历所有字段
            name = field.attname  # 取出字段名称
            if name not in ignore_fileds:  # 检查是否是需要忽略的字段
                tem_attr = getattr(self, name)
                if isinstance(tem_attr, datetime):
                    attr_dict[name] = tem_attr.strftime("%Y-%m-%d %X")  # 获取字段对应的值
                else:
                    attr_dict[name] = getattr(self, name)  # 获取字段对应的值
        return attr_dict

    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class Task(BaseMode):
    class Meta:
        verbose_name_plural = '抓取任务'
        db_table = 'task'

    TASK_TYPE = (
        ('spider', '全量抓取'),
        ('spider_update', '部分抓取')
    )
    taskId = models.AutoField(primary_key=True, verbose_name='任务id')
    taskName = models.CharField(max_length=255, null=False, verbose_name='任务名')
    taskType = models.CharField(choices=TASK_TYPE, default='全量抓取', max_length=255, verbose_name='任务类型')
    taskStatus = models.CharField(max_length=255, editable=False, default='new', verbose_name='任务状态')
    parentTaskId = models.CharField(max_length=255, default='0', verbose_name='父任务id')
    taskIP = models.CharField(max_length=255, editable=False, default='0.0.0.0', verbose_name='任务执行时主机ip')
    taskRet = models.CharField(max_length=255, default='空', editable=False, verbose_name='任务执行结果')
    extra = models.CharField(max_length=255, editable=False, default='空', verbose_name='扩展属性')
    startUrls = models.TextField(null=True, default='空', verbose_name='配置入口链接')
    sourceUrls = models.TextField(null=True, default='空', verbose_name='配置详情链接')
    priority = models.IntegerField(default=1, verbose_name='任务执行优先级')
    startTime = models.DateTimeField(auto_now=True, verbose_name='任务开始时间')
    finishTime = models.DateTimeField(auto_now=True, verbose_name='任务结束时间')


class Proxy(BaseMode):
    class Meta:
        verbose_name_plural = '代理ip'
        db_table = 'proxy'

    proxyId = models.AutoField(primary_key=True, verbose_name='代理ID')
    ip = models.CharField(max_length=255, null=False, verbose_name='IP')
    port = models.CharField(max_length=10, null=False, verbose_name='端口号')
    country = models.CharField(max_length=255, null=False, verbose_name='国家')


class Log(BaseMode):
    class Meta:
        verbose_name_plural = '抓取日志'
        db_table = 'log'

    logId = models.BigAutoField(primary_key=True, verbose_name='日志ID')
    logDetail = models.TextField(null=True, verbose_name='日志详情')
    taskId = models.CharField(max_length=50, null=False, verbose_name='任务ID')
    level = models.CharField(max_length=20, null=False, verbose_name='错误级别')
    url = models.CharField(max_length=256, null=False, verbose_name='发生错误URL')
    spiderName = models.CharField(max_length=256, null=False, verbose_name='spider名字')
    ip = models.CharField(max_length=20, default='0.0.0.0', verbose_name='发生错误所在机器')
    extInfo = models.TextField(null=True, verbose_name='预留字段')


class Pic(BaseMode):
    class Meta:
        verbose_name_plural = '抓取图片'
        db_table = 'pic'

    picId = models.IntegerField(primary_key=True, verbose_name='图片ID')
    picUrlMd5 = models.CharField(max_length=256, null=False, verbose_name='图片链接MD5值')
    picUrl = models.CharField(max_length=256, null=False, verbose_name='图片链接')
    spiderName = models.CharField(max_length=256, null=False, verbose_name='spider名字')
    taskId = models.CharField(max_length=20, null=False, verbose_name='任务ID')
    picPath = models.CharField(max_length=256, null=False, verbose_name='图片在本机路径')
    picKey = models.CharField(max_length=256, null=False, verbose_name='上传到CDN上的key')


class LastestData(BaseMode):
    class Meta:
        verbose_name_plural = '最新数据记录'
        db_table = 'latest_data'

    latestDataId = models.AutoField(primary_key=True, verbose_name='id')
    sourceName = models.CharField(max_length=255, null=False, verbose_name='数据源名称')
    latestDataInfo = models.TextField(null=False, verbose_name='最新数据相关内容')


class CveItemInfo(BaseMode):
    class Meta:
        verbose_name_plural = 'cve漏洞信息库'
        db_table = 'cve_item_info'

    orderId = models.BigAutoField(primary_key=True, verbose_name='序号')
    vul_menace_type = models.CharField(max_length=256, null=True, verbose_name='受影响系统', default='')
    verification_information = models.CharField(max_length=100, null=True, verbose_name='验证', default='')
    references = models.TextField(null=True, verbose_name='参考网址（去重合并）', default='')
    cwe_id = models.CharField(max_length=255, null=True, verbose_name='CWE编号(通用漏洞类型描述规范)', default='')
    data_update_state = models.CharField(max_length=50, null=True, verbose_name='数据更新状态(新增A(add),更新U(update))', default='')
    learn_more = models.CharField(max_length=255, null=True, verbose_name='了解更多的链接（暂时存储，未使用）', default='')
    cvsss3_base_score = models.CharField(max_length=255, null=True, verbose_name='CVSS Severity 3.0基础评分', default='')
    revision_history = models.TextField(null=True, verbose_name='修订漏洞的记录（存储方式待定，暂时存储，未使用）', default='')
    security_bulletin = models.TextField(null=True, verbose_name='安全公告（暂时存储，未使用）', default='')
    cvsss2_attack_complexity = models.TextField(null=True, verbose_name='CVSS Severity 2.0攻击复杂性', default='')
    id = models.CharField(max_length=100, null=True, verbose_name='数据库中序号', default='')
    software_version = models.TextField(null=True, verbose_name='受影响的软件版本(暂时存储，未使用)', default='')
    credit = models.TextField(null=True, verbose_name='漏洞贡献者', default='')
    vul_details_textual = models.CharField(max_length=256, null=True, verbose_name='未知', default='')
    original_bulletin = models.TextField(null=True, verbose_name='原始公告', default='')
    cvsss3_security = models.TextField(null=True, verbose_name='CVSS Severity 3.0保密性', default='')
    vendor_url = models.CharField(max_length=255, null=True, verbose_name='厂商主页：供应商网址', default='')
    cvsss2_base_score = models.TextField(null=True, verbose_name='CVSS Severity 2.0基础评分', default='')
    cvsss3_influence_score = models.TextField(max_length=256, null=True, verbose_name='CVSS Severity 3.0影响分数', default='')
    contact_way = models.TextField(null=True, verbose_name='联系方式', default='')
    vul_from = models.TextField(null=True, verbose_name='漏洞来源', default='')
    cvsss2_security = models.TextField(null=True, verbose_name='CVSS Severity 2.0保密性', default='')
    cvsss2_utilizability = models.TextField(null=True, verbose_name='CVSS Severity 2.0可利用性', default='')
    exploit_Info = models.TextField(null=True, verbose_name='漏洞利用方法', default='')
    poc_download_url = models.TextField(null=True, verbose_name='poc下载地址', default='')
    data_source = models.CharField(max_length=56, null=False, verbose_name='数据源名称', default='')
    cvsss2_accredit = models.TextField(null=True, verbose_name='CVSS Severity 2.0授权', default='')
    cve_id = models.CharField(max_length=100, null=True, verbose_name='CVE编号', default='')
    release_date = models.DateField(null=False, verbose_name='cve发布时间', default='')
    cvsss3_utilizability = models.TextField(null=True, verbose_name='CVSS Severity 3.0可利用性', default='')
    vul_reliability = models.CharField(max_length=1000, null=True, verbose_name='危害等级', default='')
    assigning_cna = models.CharField(max_length=500, null=True, verbose_name='分配CNA编号的厂商（暂时存储，未使用）', default='')
    cvsss2_vector = models.TextField(null=True, verbose_name='CVSS Severity 2.0向量:如(AV:N/AC:M/Au:N/C:C/I:C/A:C)', default='')
    product_link = models.CharField(max_length=500, null=True, verbose_name='产品下载链接', default='')
    collection_url = models.TextField(null=True, verbose_name='采集网址所属数据源', default='')
    last_revised_date = models.CharField(max_length=50, null=True, verbose_name='cve更新时间', default='')
    source_message_content = models.CharField(max_length=500, null=True, verbose_name='源信息内容', default='')
    affected_products = models.TextField(null=True, verbose_name='受影响实体（多个）：受影响的产品', default='')
    vul_impact = models.TextField(null=True, verbose_name='未知', default='')
    cvsss2_attack_vector = models.TextField(null=True, verbose_name='CVSS Severity 2.0攻击向量', default='')
    vendor_confirmed = models.CharField(max_length=50, null=True, verbose_name='厂商是否确认(厂商是否公认该漏洞)：Yes/No', default='')
    vul_name_textual = models.TextField(null=True, verbose_name='漏洞名称原文', default='')
    cvsss2_influence_score = models.TextField(null=True, verbose_name='CVSS Severity 2.0影响分数', default='')
    cvsss3_privilege_require = models.TextField(null=True, verbose_name='CVSS Severity 3.0特权要求', default='')
    fix_available = models.CharField(max_length=50, null=True, verbose_name='漏洞是否修复:Yes/No', default='')
    alias = models.CharField(max_length=100, null=True, verbose_name='别名', default='')
    is_public_disclosure = models.CharField(max_length=100, null=True, verbose_name='是否公开披露', default='')
    operating_system = models.CharField(max_length=200, null=True, verbose_name='操作系统（受影响产品是在什么系统中运行)', default='')
    vul_solution = models.TextField(null=True, verbose_name='未知', default='')
    own_ids = models.TextField(null=True, verbose_name='源网站Id', default='')
    vul_description_textual = models.TextField(null=True, verbose_name='漏洞简介原文', default='')
    vul_remote = models.CharField(max_length=50, null=True, verbose_name='漏洞是否为远程:Yes/No', default='')
    cvsss3_vector = models.TextField(null=True,verbose_name='CVSS Severity 3.0向量:如(CVSS:3.0/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:N/)', default='')
    vul_cause = models.CharField(max_length=255, null=True, verbose_name='漏洞出现的原因', default='')
    cvsss2_integrality = models.TextField(null=True, verbose_name='CVSS Severity 2.0完整性', default='')
    cvsss3_exploit_score = models.TextField(null=True, verbose_name='CVSS Severity 3.0利用分数', default='')
    cvsss3_integrality = models.TextField(null=True, verbose_name='CVSS Severity 3.0完整性', default='')
    label = models.CharField(max_length=100, null=True, verbose_name='标签', default='')
    colletion_time = models.DateField(auto_now_add=True, verbose_name='搜集数据时间')
    vul_local = models.CharField(max_length=50, null=True, verbose_name='漏洞是否为本地:Yes/No', default='')
    affected_vendors = models.TextField(null=True, verbose_name='厂商名称（多个）/受影响的厂商', default='')
    cvsss3_user_inactive = models.TextField(null=True, verbose_name='CVSS Severity 3.0用户交互', default='')
    cvsss2_exploit_score = models.TextField(null=True, verbose_name='CVSS Severity 2.0利用分数', default='')
    advisory_id = models.CharField(max_length=255, null=True, verbose_name='漏洞的安全公告编号（暂时存储，未使用）', default='')
    cvsss3_attack_complexity = models.TextField(max_length=256, null=True, verbose_name='CVSS Severity 3.0攻击复杂性', default='')
    cvsss3_scope = models.TextField(null=True, verbose_name='CVSS Severity 3.0范围', default='')
    cvsss3_attack_vector = models.TextField(null=True, verbose_name='CVSS Severity 3.0攻击向量', default='')
    vul_type_textual = models.TextField(null=True, verbose_name='未知', default='')
    is_be_used = models.CharField(max_length=100, null=True, verbose_name='漏洞是否被利用', default='')
    zero_day_time = models.CharField(max_length=500, null=True, verbose_name='0day时间', default='')

    def shortcut_vul_description_textual(self):
        if len(str(self.vul_description_textual)) > 50:
            return self.vul_description_textual[:50] + "......" + self.vul_description_textual[-10:]
        else:
            return self.vul_description_textual

    # 设置截断的intro在排序时遵循原来的字段
    shortcut_vul_description_textual.admin_order_field = 'vul_description_textual'
    # 给截断的intro设置别名
    shortcut_vul_description_textual.short_description = "漏洞简介原文"

class Translation(BaseMode):
    class Meta:
        verbose_name_plural = '翻译'
        db_table = 'translation'

    orderId = models.BigAutoField(primary_key=True, verbose_name='序号')
    cnnvd_id = models.CharField(max_length=50, null=True, verbose_name='cnnvdId', default='')
    cve_id = models.CharField(max_length=50, null=True, verbose_name='cveId', default='')
    own_ids =models.CharField(max_length=256, null=True, verbose_name='原网站Id', default='')
    vul_description = models.TextField(null=True, verbose_name='漏洞描述原文', default='')
    vul_detail_translation = models.TextField(null=True, verbose_name='漏洞描述翻译', default='')


class CveItemInfoAdd(BaseMode):
    class Meta:
        verbose_name_plural = '待跟踪cve'
        db_table = 'cveiteminfoadd'

    id = models.BigAutoField(primary_key=True, verbose_name='序号')
    itemUrl = models.CharField(max_length=500, null=False, verbose_name='itemUrl', default='')
    dataSource =models.CharField(max_length=256, null=False, verbose_name='数据源', default='')
    desc = models.TextField(null=True, verbose_name='备注', default='')
    collections_time = models.DateField(auto_now_add=True, verbose_name='搜集数据时间')



