
# 预处理
import re


# 处理多余的换行


class Pre_convert:
    _path = ''

    def __init__(self, path):
        self._path = path

    def content_convert(self):
        file_data = ""
        with open(self._path, "r", encoding="utf-8") as f:
            for line in f:
                if '*' in line:
                    line = ''
                ma = re.search(r'(\w*)', line, re.I | re.M)
                if ma and ma.group(1):
                    temp_line = line.rstrip(' ')
                    if not (temp_line.endswith(';\n') or temp_line.endswith('{\n') or temp_line.endswith('}\n')):
                        line = re.sub(r'\n', '', line)
                file_data += line
        with open(self._path, "w", encoding="utf-8") as f:
            f.write(file_data)