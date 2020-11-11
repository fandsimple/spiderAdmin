import json

from django.http import HttpResponse

from spiderAdmin import settings


def render_json(data, code, msg):
    '''
    返回格式如下Response：
    result = {
        "code":code,
        "msg":msg,
        "data":data,
    }
    '''
    result = {
        "code": code,
        "msg": msg,
        "data": data,
    }
    if settings.DEBUG:
        result_json = json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True)
        return HttpResponse(result_json)
    result_json = json.dumps(result, ensure_ascii=False, separators=[':', ','])
    return HttpResponse(result_json)
