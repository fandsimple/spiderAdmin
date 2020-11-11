import datetime


def many_to_dict(objectList, *ignore_fileds):
    resList = []
    for object in objectList:
        '''将一个 model 转换成一个 dict'''
        attr_dict = {}
        for field in object._meta.fields:  # 遍历所有字段
            name = field.attname  # 取出字段名称
            if name not in ignore_fileds:  # 检查是否是需要忽略的字段
                tem_attr = getattr(object, name)
                if isinstance(tem_attr, datetime):
                    attr_dict[name] = tem_attr.strftime("%Y-%m-%d %X")  # 获取字段对应的值
                else:
                    attr_dict[name] = getattr(object, name)  # 获取字段对应的值
        resList.append(attr_dict)
    return resList
