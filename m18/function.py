
# 函数名，方法名
import re
import base.util
import base.javaclass as java
import base.configuration as config


# 参数转换
def parameter_convert(param) -> str:
    if param == '': return ''

    components = []
    temp = param
    for i, ch in enumerate(param):
        if ch == ',' and not base.util.is_letter_in_angle_brackets(i, ch, param):
            temp = temp[0:i] + '&' + temp[i + 1:]

    temps = temp.split('&')
    for item in temps:
        ma = re.match(r'(.*)<(.*)>(.*)', item, re.M | re.I)
        if ma and ma.group(1) and ma.group(2) and ma.group(3):
            param_type = ma.group(1)
            type_desc = ma.group(2).replace(',', ':')
            param_name = ma.group(3)
            components.append((param_type, type_desc, param_name))
            continue

        ma = re.match(r'(.*) (.*)', item, re.M | re.I)
        if ma and ma.group(1) and ma.group(2):
            param_type = ma.group(1)
            type_desc = ''
            param_name = ma.group(2)
            components.append((param_type, type_desc, param_name))
            continue

    res = ''
    for com in components:
        if com[0] == 'List':
            res += '_ ' + com[2] + ': [' + com[1] + '], '
        elif com[0] == 'Map':
            res += '_ ' + com[2] + ': [' + com[1] + '], '
        else:
            res += '_ ' + com[2] + ': ' + com[0] + ', '

    res = res.rstrip(' ')
    res = res.rstrip(',')
    res = res.replace('  ', ' ')

    return res


# 返回值
def return_type_convert(return_type) -> str:
    result = ''
    if return_type == 'void':
        result += ' {\n'
    else:
        if return_type in base.javaclass.class_reflect.keys():
            return_type = base.util.swift_class_from_java(return_type)
        result += ' -> ' + return_type + ' {\n'
    return result


class Function:
    _line = ''
    _info = {}
    _cls = ''

    def __init__(self, line, cls):
        self._line = line
        self._info = {}
        self._cls = cls

    def convert_function(self):

        if not self.is_function():
            return self._line

        ma = re.search(r'(.*[public|private]) (.*) (.*)\((.*)\) {\n', self._line, re.M | re.I)
        result = self._line
        if ma and ma.group(1) and ma.group(2) and ma.group(3):
            access_permission = ma.group(1)
            return_type = return_type_convert(ma.group(2))
            function_name = ma.group(3)
            parameters = parameter_convert(ma.group(4))
            result = access_permission + ' func ' + function_name + '(' + parameters + ')' + return_type

            funcs = config.functions[self._cls]
            funcs.append(function_name)
            config.functions[self._cls] = funcs

        return result


    # 是否为function
    def is_function(self):
        temp = self._line.strip(' ').lstrip(' ')
        if (temp.startswith('private') or temp.startswith('public')) and temp.endswith('{\n'):
            return True
        return False
