from django.conf.urls import url

from spiderTask import views

urlpatterns = [
    # 测试跑通
    url('index/', views.index, name='index'),

    # 任务添加、获取
    url('addtask/', views.addTask, name='addtask'),
    url('gettask/', views.getTask, name='gettask'),
    url('updatetaskdone/', views.updateTaskDone, name='updatetaskdone'),



    # 代理逻辑
    url('addproxy/', views.addProxy, name='addproxy'),
    url('getproxy/', views.getProxy, name='getproxy'),

    # 保存数据
    url('savecveitem', views.saveCveItem, name='savecveitem'),
    # 获取最新数据信息
    url('getlatestinfo', views.getLatestInfo, name='getlatestinfo'),

    # 设置最新数据信息
    url('setlatestinfo', views.setLatestInfo, name='setlatestinfo'),

    # 设置日志
    url('seterrorlog', views.setErrorLog, name='seterrorlog'),

    # 设置日志
    url('saveitemadd', views.saveItemAdd, name='saveitemadd'),

    # 获取redis中的任务
    url('getredistask', views.getRedisTask, name='getredistask'),








]


