
import re
import base.util
import base.configuration as config

class Protocol:
    __path = ''
    __content = ''

    def __init__(self, path):
        self.__path = path
        self.__content = base.util.getContent(self.__path)

    def content_convert(self):
        if not self.is_protocol():
            return self.__content

    def is_protocol(self):
        ma = re.search(r'public Interface (\w*) {\n', self.__content, re.I | re.M)
        if ma and ma.group(1):
            config.protocols.append(ma.group(1))
            return True
        return False

    def get_sub_protocol(self):
        all_obj = re.findall(r'Interface (\w*) ', self.__content, re.I | re.M)
        if len(all_obj) == 1:
            return None
        else:
            for item in all_obj:
                item_ma = re.search(r'Interface (\w*) (.*?) {\n(.*?)}\n',)


    # def get_protocol_functions(self):


path = '/Users/macremote/Documents/android/m18builder/m18erptrdg/src/main/java/com/multiable/m18erptrdg/contract/WmsGroupContract.java'
Protocol(path).get_sub_protocol()