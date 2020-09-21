
# 语言文件
import re
import os
import base.configuration as config


# < string name = "m18erptrdg_message_save_success" > 保存成功 < / string >
# "preTaxUnitPrice" = "税前单价";
def lang_convert_line(line: str) -> str:
    line = line.replace(' ', '')
    line = line.replace('<resources>', '')
    line = line.replace('</resources>', '')
    if '\n' in line:
        line = line.strip('\n')
    match_obj = re.match(r'<stringname=\"(.*?)\">(.*)</string>', line, re.M | re.I)
    if match_obj and match_obj.group(1) and match_obj.group(2):
        line = '"' + match_obj.group(1) + '\" = \"' + match_obj.group(2) + '";'
    return line


class Language:
    _src = ''
    _des = ''

    def __init__(self, src, des):
        self._src = src
        self._des = des

    def lang_convert(self):

        if not self._src.endswith('strings.xml'):
            return

        des_dir_item = config.language_file[self._src.split('/')[-2]]
        des_dir = '/'.join(self._des.split('/')[0:-2]) + '/' + des_dir_item
        if not os.path.exists(des_dir):
            os.makedirs(des_dir)

        self._des = des_dir + '/' + 'Localizable.strings'
        data = ''
        with open(self._src, "r", encoding="utf-8") as f:
            for line in f:
                line = lang_convert_line(line)
                data += line + '\n'
        with open(self._des, "w", encoding="utf-8") as f:
            f.write(data)
