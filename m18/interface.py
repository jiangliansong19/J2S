
# 类的声明，继承，实现，抽象类

import re
import base.configuration as config


def only_extends(obj) -> str:
    if 'extends' not in obj or 'implements' in obj:
        return obj
    ma = re.search(r'(.*) extends (.*)', obj, re.M | re.I)
    if ma and ma.group(1):
        if 'Fragment' in obj:
            obj = ma.group(1) + ' : UIViewController {'
        else:
            obj = ma.group(1) + ' {'
    return obj


def only_implements(obj) -> str:
    if 'extends' in obj or 'implements' not in obj:
        return obj
    ma = re.search(r'(.*) implements (.*)', obj, re.M | re.I)
    if ma and ma.group(1) and ma.group(2):
        obj = ma.group(1) + ' : ' + ma.group(2) + ' {'
    return obj


# java的interface转换为protocol
def only_interface(obj, cls) -> str:
    if 'Interface' not in obj:
        return obj
    ma = re.search(r'(.*) Interface (.*) {', obj, re.M | re.I)
    if ma and ma.group(1) and ma.group(2):
        if cls in config.protocols:
            return ''
        else:
            obj = 'protocol ' + ma.group(2) + ' #protocol#' + '\n'
            config.protocols.append(ma.group(2))
    return obj


def extends_implements(obj) -> str:
    if 'extends' not in obj or 'implements' not in obj:
        return obj
    ma = re.match(r'([publicrvate]*) class (\w*) extends (.*) implements (.*) {', obj, re.I | re.M)
    if ma and ma.group(1) and ma.group(2) and ma.group(3) and ma.group(4):
        class_key = ma.group(1)
        class_name = ma.group(2)
        super_class_name = ma.group(3)
        implements = ma.group(4)
        obj = class_key + ' class ' + class_name + ': ' + super_class_name + ', ' + implements + ' {'
    return obj


class Interface:
    _line = ''
    _cls = ''

    def __init__(self, line, cls):
        self._line = line
        self._cls = cls

    def class_convert_class_name(self):
        result = self._line
        result = only_extends(result)
        result = only_implements(result)
        result = extends_implements(result)
        result = only_interface(result, self._cls)

        return result


# line = 'public class STFooterPresenter implements STFooterContract.Presenter {'
# Interface(line, '').class_convert_class_name()