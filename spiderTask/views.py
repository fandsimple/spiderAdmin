import pdb
import random
import time
import traceback
import datetime

from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db import transaction
from django.db.models import Q
from spiderAdmin.settings import GET_TASK_RULE
from spiderTask.common import render_json
from spiderTask.constant import STATE_OK, STATE_ERROR, TASK_NEW, TASK_RUNNING, TASK_SPIDER, \
    TASK_SPIDER_UPDATE, TASK_DONE
from spiderTask.models import Task, Proxy, LastestData, Log, CveItemInfo, CveItemInfoAdd

def index(request):  # 测试跑通
    return HttpResponse('hello')


# ***********************
# 获取任务
@transaction.atomic
def getTask(request):
    '''
    0：单纯按照优先级排序 序号大的先执行(系统默认配置)
    1：按照任务类型排序 更新任务 > 全量任务 按照任务添加顺序执行
    2：先按照任务类型排序，然后再按照优先级排序 更新任务 > 全量任务，序号大的先执行
    '''

    try:
        ip = request.POST.get('ip')
        if GET_TASK_RULE == 0:  # 完全按优先级排序
            taskNewList = Task.objects.select_for_update().filter(taskStatus=TASK_NEW).order_by('-priority')
            if not taskNewList:
                return render_json(data={}, code=STATE_OK, msg='data is null')
            taskNew = taskNewList.first()
            taskNew.taskStatus = TASK_RUNNING
            taskNew.taskIP = ip
            taskNew.save()
            return render_json(data=taskNew.to_dict(), code=STATE_OK, msg='success')
        elif GET_TASK_RULE == 1:  # 按照任务类型排序 更新任务 > 全量任务 按照任务添加顺序执行
            taskNewList = Task.objects.select_for_update().filter(
                Q(taskStatus=TASK_NEW) & Q(spiderType=TASK_SPIDER_UPDATE))
            if taskNewList:  # 有spider_update任务优先该任务
                taskNew = taskNewList.first()
                taskNew.taskStatus = TASK_RUNNING
                taskNew.save()
                return render_json(data=taskNew.to_dict(), code=STATE_OK, msg='success')
            taskNewList = Task.objects.select_for_update().filter(Q(taskStatus=TASK_NEW) & Q(spiderType=TASK_SPIDER))
            if taskNewList:  # 其次执行spider任务
                taskNew = taskNewList.first()
                taskNew.taskStatus = TASK_RUNNING
                taskNew.save()
                return render_json(data=taskNew.to_dict(), code=STATE_OK, msg='success')
            return render_json(data={}, code=STATE_OK, msg='data is null')

        elif GET_TASK_RULE == 2:  # 先按照任务类型排序，然后再按照优先级排序 更新任务 > 全量任务，序号大的先执行
            taskNewList = Task.objects.select_for_update().filter(
                Q(taskStatus=TASK_NEW) & Q(spiderType=TASK_SPIDER_UPDATE)).order_by('-priority')
            if taskNewList:  # 有spider_update任务优先该任务
                taskNew = taskNewList.first()
                taskNew.taskStatus = TASK_RUNNING
                taskNew.save()
                return render_json(data=taskNew.to_dict(), code=STATE_OK, msg='success')
            taskNewList = Task.objects.select_for_update().filter(
                Q(taskStatus=TASK_NEW) & Q(spiderType=TASK_SPIDER)).order_by('-priority')
            if taskNewList:  # 其次执行spider任务
                taskNew = taskNewList.first()
                taskNew.taskStatus = TASK_RUNNING
                taskNew.save()
                return render_json(data=taskNew.to_dict(), code=STATE_OK, msg='success')
            return render_json(data={}, code=STATE_OK, msg='data is null')
        else:
            return render_json(data={'msg': traceback.format_exc()}, code=STATE_ERROR, msg='config is wrong')
    except Exception as e:
        return render_json(data={'msg': traceback.format_exc()}, code=STATE_ERROR, msg='server is down')


# 添加任务
def addTask(request):
    taskNew = Task.objects.get(pk=1)
    return render_json(data=taskNew.to_dict(), code=200, msg='success')


def updateTaskDone(request):
    try:
        taskId = request.POST.get('taskId', '')
        taskObj = Task.objects.get(taskId=taskId)
        taskObj.taskStatus = TASK_DONE
        taskObj.save()
        return render_json(data=taskObj.to_dict(), code=STATE_OK, msg='sucess')
    except Exception as e:
        return render_json(data={}, code=STATE_ERROR, msg=traceback.format_exc())


# *** 添加代理 ***
def addProxy(request):
    '''
    添加代理
    '''
    # 随机生成代理
    numList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    numList1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    for i in range(100):
        proxyId = i + 1 + 100
        ipList = []
        for i in range(4):
            if not i:
                num = ''.join(random.sample(numList1, 3))
                ipList.append(num)
                continue
            num = ''.join(random.sample(numList, 3))
            ipList.append(num)
        ip = '.'.join(ipList)

        port = random.randint(5000, 8000)
        countryList = ['bbt', 'xundaili']
        country = random.choice(countryList)

        proxy = Proxy()
        proxy.proxyId = proxyId
        proxy.ip = ip
        proxy.country = country
        proxy.port = port
        proxy.save()
    return HttpResponse('success')


def getProxy(request):
    country = request.Get.get('country', 'xundaili')
    proxys = Proxy.objects.filter(country=country).order_by('updateTime')[:5]
    return None


def saveCveItem(request):
    try:
        data = request.POST
        cveItemInfo = CveItemInfo()
        cveItemInfo.collection_url = data.get('cveItemUrl', '')
        cveItemInfo.vul_name_textual = data.get('cveItemTitle', '')
        cveItemInfo.vul_description_textual = data.get('cveDesc', '')
        cveItemInfo.cve_id = data.get('cveCode', '')
        cveItemInfo.data_source = data.get('cveSource', '')
        cveItemInfo.release_date = data.get('pubTime')
        cveItemInfo.last_revised_date = data.get('cveUpdateTime', '')
        cveItemInfo.cvsss3_base_score = data.get('cveScore', '')
        cveItemInfo.cwe_id = data.get('cweIds', '')
        cveItemInfo.vul_from = data.get('author', '')
        cveItemInfo.affected_products = data.get('affectedProduct', '')
        cveItemInfo.own_ids = data.get('sourceId', '')

        # cveItemInfo.affectedSystem = data.get('affectedSystem')
        # cveItemInfo.cveItemDetailUrl = data.get('cveItemDetailUrl')
        # cveItemInfo.affection = data.get('affection')
        # cveItemInfo.referenceLink = data.get('referenceLink')
        # cveItemInfo.cveUseType = data.get('cveUseType')
        # cveItemInfo.pocDownloadUrl = data.get('pocDownloadUrl')
        # cveItemInfo.pocScript = data.get('pocScript')
        # cveItemInfo.isverify = data.get('isverify')
        cveItemInfo.save()
        data = {
            'code': 200,
            'data': 'sucess'
        }
    except Exception as e:
        data = {
            'code': 500,
            'data': traceback.format_exc()
        }
    return JsonResponse(data, safe=False)


def getLatestInfo(request):
    data = request.POST
    sourceName = data.get('sourceName')

    if datetime.datetime.now().weekday() == 0:  # 星期一取上周五的最新记录
        pre_day = datetime.date.today() + datetime.timedelta(days=-3)
    else:
        pre_day = datetime.date.today() + datetime.timedelta(days=-1)
    print(pre_day)
    # pre_day = datetime.date.today() # 测试时打开，不测试时关闭
    preday_year, preday_month, preday_day = pre_day.year, pre_day.month, pre_day.day

    latestItem = LastestData.objects.filter(
        Q(sourceName=sourceName) & Q(createTime__year=preday_year) & Q(createTime__month=preday_month) & Q(
            createTime__day=preday_day))[0]

    latestItemInfoData = {
        'sourceName': latestItem.sourceName,
        'latestDataInfo': latestItem.latestDataInfo,
    }
    data = {
        "code": 200,
        "data": latestItemInfoData
    }
    return JsonResponse(data, safe=False)


def setLatestInfo(request):
    data = request.POST
    latestData = LastestData()
    latestData.sourceName = data.get('sourceName')
    latestData.latestDataInfo = data.get('latestDataInfo')
    latestData.save()

    data = {
        'code': 200,
        'data': 'sucess'
    }
    return JsonResponse(data, safe=False)


def setErrorLog(request):
    data = request.POST
    log = Log()
    log.ip = data.get('ip')
    log.level = data.get('level')
    log.logDetail = data.get('logDetail')
    log.taskId = data.get('taskId')
    log.url = data.get('url')
    log.spiderName = data.get('spiderName')
    log.save()
    data = {
        'code': 200,
        'data': 'sucess'
    }
    return JsonResponse(data, safe=False)


def saveItemAdd(request):
    data = request.POST
    itemAddData = CveItemInfoAdd()
    data = {
        'code': 200,
        'data': 'sucess'
    }
    return JsonResponse(data, safe=False)


def getRedisTask(request):
    cache.set('shukai', 'fanding', timeout=100)
    name = cache.get('shukai')
    return HttpResponse(name)

