import base.configuration as config
import base.javaclass as base_class
import base.util
import re


# 给对象赋值
def set_value_to_object(obj) -> str:
    result = obj
    ma = re.match(r'(\s*)(\w*) (\w*) =', obj, re.I | re.M)
    if ma and ma.group(2) and ma.group(3):
        swift_class = base.util.swift_class_from_java(ma.group(2))
        new = ma.group(1) + 'var ' + ma.group(3) + ': ' + swift_class + ' ='
        result = re.sub(r'(.*) =', new, obj)
    ma = re.match(r'(\s*)(\w*)<([\w, ]*)> (\w*) =', obj, re.I | re.M)
    if ma and ma.group(2) and ma.group(3) and ma.group(4):
        java_class = ma.group(2) + '<' + ma.group(3) + '>'
        swift_class = base.util.swift_class_from_java(java_class)
        new = ma.group(1) + 'var ' + ma.group(4) + ': ' + swift_class + ' ='
        result = re.sub(r'(.*) =', new, obj)
    return result


# 双冒号语法 this::showUploadDialog
def double_colon(obj) -> str:
    result = obj
    if '::' not in obj:
        return result
    if 'this::' in obj:
        result = result.replace('this::', '')
    return result


# 强制类型转换
# user = (LookupResult) lfUser.getTag()
def class_type_transform(obj) -> str:
    result = obj
    match_obj = re.search(r'\((\w*)\) ([\w\(\)\.]*)', obj, re.I | re.M)
    if match_obj and match_obj.group(1) and match_obj.group(2):
        old = '(' + match_obj.group(1) + ') ' + match_obj.group(2)
        new = match_obj.group(2) + ' as ' + match_obj.group(1)
        result = result.replace(old, new)
    return result




class Last:
    _cls = ''
    _line = ''

    def __init__(self, obj, cls):
        self._cls = cls
        self._line = obj

    def convert(self) -> str:
        result = self._line
        result = set_value_to_object(result)
        result = double_colon(result)
        result = class_type_transform(result)
        return result

line = '            user = (LookupResult) lfUser.getTag();'
class_type_transform(line)
