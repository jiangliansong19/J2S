import os
import base.configuration as config
import re
import base.javaclass
import base.util
from m18.pre_convert import Pre_convert
from m18.function import Function
from m18.method import Method
from m18.property import Property
from m18.interface import Interface
from m18.last import Last
from m18.file_correct import File_correct
from m18.format import Format


class M18_file:
    _click_events = []
    _class_vars = []
    src = ''
    des = ''
    cls = ''

    def __init__(self, src, des, cls):
        self.src = src
        self.des = des
        self.cls = cls

    # 预处理
    def pre_convert(self):
        Pre_convert(self.src).content_convert()

    # 替换常量，特殊标识符
    def deal_constants(self, line):
        line = line.replace('View.GONE', 'UIView.GONE')
        line = line.replace('View.VISIBLE', 'UIView.VISIBLE')
        line = line.replace(' int', ' Int')
        line = line.replace('int ', 'Int ')
        line = line.replace(' boolean', ' Bool')
        line = line.replace('boolean ', 'Bool ')
        return line

    def deal_class_interface(self, line):
        line = Interface(line, self.cls).class_convert_class_name()
        return line

    def deal_vars(self, line):
        line = Property(line, self.cls).convert_property()
        return line

    def dealWithFuncName(self, line):
        if len(line) == 0 or line == '\n': return line
        line = Function(line, self.cls).convert_function()
        return line

    def deleteUnusefulLine(self, line):
        if "import" in line:
            return ""
        if "package" in line:
            return ""
        if "@Override" in line:
            return ""

        return line

    def deal_execut_method(self, line):
        line = Method(line, self.cls).convert_method()
        return line

    def swift_correct(self, line):

        # 点击事件等方法，添加前缀@objc
        for event in self._click_events:
            if event in line:
                line = line.replace(event, '@objc ' + event)

        return line

    def last_correct(self, line):

        line = Last(line, self.cls).convert()

        return line

    def dealWithM18(self):

        self.pre_convert()
        cls = self.src.split('/')[-1].replace('.java', '')
        config.properties[cls] = []
        config.functions[cls] = []

        src_data = base.util.getContent(self.src)
        file_data = "import Foundation\nimport UIKit\n"
        with open(self.src, "r", encoding="utf-8") as f:
            for line in f:
                line = self.deleteUnusefulLine(line)
                line = self.deal_constants(line)

                line = self.deal_class_interface(line)
                line = self.deal_vars(line)
                line = self.dealWithFuncName(line)
                line = self.deal_execut_method(line)
                line = self.last_correct(line)
                file_data += line

        file_data = File_correct(self.cls, self.src, file_data).correct()
        file_data = Format(file_data).format()
        with open(self.des, "w", encoding="utf-8") as f:
            f.write(file_data)


