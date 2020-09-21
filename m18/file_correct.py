
import re
import base.configuration as config


def protocol_correct(content, cls) -> str:
    if cls not in config.protocols:
        return content
    temp = content.replace('{', '')
    temp = temp.replace('}', '')
    temp = temp.replace('#protocol#', '{')
    temp = temp + '\n}'
    return temp

class File_correct:

    _cls = ''
    _src = ''
    _data = ''

    def __init__(self, cls, src, data):
        self._cls = cls
        self._data = data
        self._src = src

    def correct(self) -> str:
        temp = protocol_correct(self._data, self._cls)

        return temp




