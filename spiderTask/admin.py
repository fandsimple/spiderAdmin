from django.contrib import admin

from spiderTask.models import Task, Proxy, Pic, Log, LastestData, CveItemInfo, Translation, CveItemInfoAdd
# from daterange_filter.filter import DateRangeFilter

admin.site.site_header = 'Stronger Spider'
admin.site.site_title = 'Stronger Spider'


class BaseAdmin(admin.ModelAdmin):
    list_per_page = 1000  # 每页显示多少条
    actions_on_top = True  # 顶部操作显示
    actions_on_bottom = True  # 底部操作显示
    actions_selection_counter = True  # 选中条数显示
    empty_value_display = ' 空白 '  # 空白字段显示格式


# Task
@admin.register(Task)
class TaskAdmin(BaseAdmin):
    ordering = ('taskId',)
    list_display = (
        'taskId', 'taskName', 'taskType', 'taskStatus', 'parentTaskId', 'taskIP', 'taskRet', 'priority',
        'createTime', 'startTime', 'finishTime')  # 显示字段
    search_fields = ('taskId',)  # 搜索条件配置
    list_filter = ('taskType',)  # 过滤字段配置
    # list_editable = ['taskName']

    # list_display_links = ('id', 'caption') # 配置点击进入详情字段


# # Proxy
# @admin.register(Proxy)
# class ProxyAdmin(BaseAdmin):
#     ordering = ('updateTime',)
#     list_display = (
#         'proxyId', 'ip', 'port', 'country', 'updateTime')  # 显示字段
#     search_fields = ('ip', 'country', 'port')  # 搜索条件配置
#     list_filter = ('country',)  # 过滤字段配置
#     # list_editable = ['taskName']
#     # list_display_links = ('id', 'caption') # 配置点击进入详情字段


# # pic
# @admin.register(Pic)
# class PicAdmin(BaseAdmin):
#     ordering = ('updateTime',)
#     list_display = (
#         'picId', 'picUrlMd5', 'picUrl', 'spiderName', 'taskId', 'picPath', 'picKey', 'updateTime')  # 显示字段
#     search_fields = ('picUrl', 'spiderName', 'taskId', 'picKey')  # 搜索条件配置
#     list_filter = ('spiderName',)  # 过滤字段配置
#     # list_editable = ['taskName']
#     # list_display_links = ('id', 'caption') # 配置点击进入详情字段


# Log
@admin.register(Log)
class LogAdmin(BaseAdmin):
    ordering = ('logId',)
    list_display = (
        'logId', 'url', 'logDetail', 'taskId', 'level', 'spiderName', 'extInfo', 'ip', 'createTime',
        'updateTime')  # 显示字段
    search_fields = ("url", "taskId", "spiderName")  # 搜索条件配置
    list_filter = ('spiderName',)  # 过滤字段配置
    date_hierarchy = 'createTime'
    # list_editable = ['taskName']
    # list_display_links = ('id', 'caption') # 配置点击进入详情字段


# # CveItem
# @admin.register(CveItem)
# class CveItemAdmin(BaseAdmin):
#     ordering = ('cveId',)
#     list_display = (
#         'cveId', 'cveItemUrl', 'cveItemTitle', 'author', 'shortcut_cveDesc', 'cveCode', 'cveSource', 'pubTime', 'cveUpdateTime',
#         'cveScore', 'cveItemDetailUrl', 'cweIds', 'affectedProduct', 'affectedSystem', 'affection', 'referenceLink',
#         'sourceId', 'cveUseType', 'pocDownloadUrl', 'pocScript', 'isverify', 'updateTime', 'createTime')
#     # 显示字段
#     search_fields = ('cveItemUrl', 'cveCode', 'cveSource', 'cveScore', 'cveItemDetailUrl')  # 搜索条件配置
#     list_filter = ('cveSource',)  # 过滤字段配置
#     # list_editable = ['taskName']
#     # list_display_links = ('id', 'caption') # 配置点击进入详情字段
#     # 按日期月份筛选 该属性一般不用
#     date_hierarchy = 'pubTime'
#     # 按发布日期降序排序
#     ordering = ('-pubTime',)
#
#
#     # # 增加自定义按钮
#     # actions = ['make_copy', 'custom_button']
#     # def custom_button(self, request, queryset):
#     #     pass
#     # # 显示的文本，与django admin一致
#     # custom_button.short_description = '导出数据'
#     # # icon，参考element-ui icon与https://fontawesome.com
#     # custom_button.icon = 'fas fa-audio-description'
#     #
#     # # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
#     # custom_button.type = 'danger'
#     #
#     # # 给按钮追加自定义的颜色
#     # custom_button.style = 'color:black;'
#     # def make_copy(self, request, queryset):
#     #     pass
#     # make_copy.short_description = '复制员工'


# LastestData
@admin.register(LastestData)
class LastestDataAdmin(BaseAdmin):
    ordering = ('latestDataId',)
    list_display = (
        'latestDataId', 'sourceName', 'latestDataInfo', 'updateTime', 'createTime')  # 显示字段
    search_fields = ('latestDataInfo',)  # 搜索条件配置
    list_filter = ('sourceName',)  # 过滤字段配置
    # list_editable = ['taskName']
    # list_display_links = ('id', 'caption') # 配置点击进入详情字段
    date_hierarchy = 'createTime'


@admin.register(CveItemInfo)
class CveItemInfoAdmin(BaseAdmin):
    ordering = ('id',)
    list_display = (
    'orderId', 'data_source', 'collection_url', 'cve_id', 'release_date', 'last_revised_date', 'vul_name_textual',
    'affected_products', 'vul_from', 'cvsss3_base_score', 'cwe_id', 'own_ids', 'shortcut_vul_description_textual',
    'colletion_time', 'vul_menace_type', 'verification_information', 'references', 'data_update_state', 'learn_more',
    'revision_history', 'security_bulletin', 'cvsss2_attack_complexity', 'id', 'software_version', 'credit',
    'vul_details_textual', 'original_bulletin', 'cvsss3_security', 'vendor_url', 'cvsss2_base_score',
    'cvsss3_influence_score', 'contact_way', 'cvsss2_security', 'cvsss2_utilizability', 'exploit_Info',
    'poc_download_url', 'cvsss2_accredit', 'cvsss3_utilizability', 'vul_reliability', 'assigning_cna', 'cvsss2_vector',
    'product_link', 'source_message_content', 'vul_impact', 'cvsss2_attack_vector', 'vendor_confirmed',
    'cvsss2_influence_score', 'cvsss3_privilege_require', 'fix_available', 'alias', 'is_public_disclosure',
    'operating_system', 'vul_solution', 'vul_remote', 'cvsss3_vector', 'vul_cause', 'cvsss2_integrality',
    'cvsss3_exploit_score', 'cvsss3_integrality', 'label', 'vul_local', 'affected_vendors', 'cvsss3_user_inactive',
    'cvsss2_exploit_score', 'advisory_id', 'cvsss3_attack_complexity', 'cvsss3_scope', 'cvsss3_attack_vector',
    'vul_type_textual', 'is_be_used', 'zero_day_time', 'createTime', 'updateTime')  # 显示字段
    search_fields = ('cve_id', 'collection_url', 'vul_name_textual', 'vul_description_textual')  # 搜索条件配置
    # list_filter = ('data_source',('colletion_time', DateRangeFilter))  # 过滤字段配置
    list_filter = ('data_source',)  # 过滤字段配置
    # list_editable = ['taskName']
    list_display_links = ('cve_id', 'collection_url', 'vul_name_textual', 'shortcut_vul_description_textual')  # 配置点击进入详情字段
    # ordering = ('-release_date',)
    date_hierarchy = 'colletion_time'




@admin.register(Translation)
class TranslationAdmin(BaseAdmin):
    # ordering = ('id',)
    list_display = ('orderId', 'cnnvd_id', 'cve_id', 'own_ids', 'vul_description', 'vul_detail_translation')  # 显示字段
    # search_fields = ('orderId', 'cnnvd_id', 'cve_id', 'own_ids', 'vul_description', 'vul_detail_translation')  # 搜索条件配置
    # list_filter = ('data_source',('colletion_time', DateRangeFilter))  # 过滤字段配置
    # list_filter = ('data_source',)  # 过滤字段配置
    list_editable = ['vul_detail_translation']
    # list_display_links = ('cve_id', 'collection_url', 'vul_name_textual',)  # 配置点击进入详情字段
    # ordering = ('-release_date',)
    # date_hierarchy = 'colletion_time'


@admin.register(CveItemInfoAdd)
class CveItemInfoAddAdmin(BaseAdmin):
    ordering = ('id',)
    list_display = ('id', 'itemUrl', 'dataSource', 'desc', 'collections_time')  # 显示字段
    search_fields = ('id', 'itemUrl', 'dataSource', 'desc')  # 搜索条件配置
    list_filter = ('dataSource',)  # 过滤字段配置
    # list_filter = ('data_source',)  # 过滤字段配置
    list_editable = ['itemUrl', 'dataSource']
    # list_display_links = ('cve_id', 'collection_url', 'vul_name_textual',)  # 配置点击进入详情字段
    # ordering = ('-release_date',)
    date_hierarchy = 'collections_time'
