import re
import base.configuration as config
import base.javaclass as base_cls
from m18.function import parameter_convert


def method_in_protocol(line, cls) -> str:
    if cls in config.protocols:
        ma = re.search(r'(\s*)(.*) (.*)\((.*)\);', line, re.I | re.M)
        if ma and ma.group(2) and ma.group(3):
            line = ma.group(1) + 'func ' + ma.group(3) + '(' + parameter_convert(ma.group(4)) + ')'
            if 'void' not in ma.group(2):
                line += ' -> ' + ma.group(2) + '\n'
            else:
                line += '\n'
    return line


def method_assert(line) -> str:
    if not 'assert' in line: return line
    match_obj = re.search(r'(\s*)assert (.*);(\s*)', line, re.I | re.M)
    if match_obj and match_obj.group(2):
        line = match_obj.group(1) + 'assert(' + match_obj.group(2) + ')' + match_obj.group(3)
    return line


def method_set_language(line):
    match_obj = re.search(r'R.string.(\w*)', line, re.I | re.M)
    if match_obj and match_obj.group(1):
        old = 'R.string.' + match_obj.group(1)
        new = 'M18LocalizedString("' + match_obj.group(1) + '")'
        line = line.replace(old, new)
    return line


#for (String stCode : stCodeList) {
def method_logics_for(line) -> str:
    temp = line.lstrip(' ').rstrip(' ')
    ma = re.search(r'for \((\w*) (\w*) : (\w*)\) {\n', temp, re.I | re.M)
    if ma and ma.group(1) and ma.group(2) and ma.group(3):
        new = 'for ' + ma.group(2) + ' in ' + ma.group(3) + ' {\n'
        line = line.replace(temp, new)
    return line


class Method:
    _line = ''
    _cls = ''

    def __init__(self, line, cls):
        self._line = line
        self._cls = cls

    def convert_method(self):

        line = self._line

        line = self.method_new_object(line)
        line = self.method_set_listener(line)
        line = self.method_other_format(line)
        line = method_set_language(line)
        line = method_assert(line)
        line = method_in_protocol(line, self._cls)
        line = method_logics_for(line)


        return line

    # 创建新的对象
    def method_new_object(self, line):
        if 'new ' in line:
            line = line.replace('new ', '')
        return line

    # 添加事件监听
    def method_set_listener(self, line):

        if not 'setOnClickListener' in line: return line

        match_obj = re.search(r'(.*).setOnClickListener\((.*) -> (.*)\);', line, re.M | re.I)
        if match_obj and match_obj.group(1) and match_obj.group(2) and match_obj.group(3):
            # ivBack?.addTarget(self, action:  # selector(ivBackClickAction), for: .touchUpInside)
            target = match_obj.group(2)
            method_name = match_obj.group(2) + '.' + match_obj.group(3).strip('()')
            if match_obj.group(2) == 'view':
                target = 'self'
                method_name = match_obj.group(3).strip('()')

            line = self.set_property_wrapped(match_obj.group(1)) + \
                   '.setOnClickListener(' + target + ', action: #selector(' + \
                   method_name + '), for: .touchUpInside)\n'
        return line

    def method_other_format(self, line):
        items = line.split('.')
        if len(items) >= 2:
            items[0] = self.set_property_wrapped(items[0])
            line = '.'.join(items)

        return line

    # 根据property，设置wrap和unwarp
    def set_property_wrapped(self, property):
        properties = config.properties[self._cls]
        if property.strip(' ') in properties:
            return property + '?'
        else:
            return property


# line = 'rvWmsData?.setLayoutManager(new LinearLayoutManager(mContext));'
# Method(line, '').method_in_protocol(line)
