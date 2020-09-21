# 格式
import re


# 去除连续的多个\n
def delete_multiple_n(data) -> str:
    result = re.sub(r'\n\s*\n', '\n\n', data)
    return result


class Format:
    _data = ''

    def __init__(self, data):
        self._data = data

    def format(self) -> str:
        result = self._data
        result = delete_multiple_n(result)
        return result



