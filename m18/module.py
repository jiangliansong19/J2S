import os
import base.util
from m18.m18_file import M18_file
from m18.language import Language
import base.configuration as config
import base.util


class Module:
    _java_root = ''
    _swift_root = ''
    _module_name = ''

    def __init__(self, java_root, swift_root, module_name):
        self._java_root = java_root
        self._swift_root = swift_root
        self._module_name = module_name

    def convert_module(self):
        src_path = self._java_root + '/' + self._module_name
        des_path = self._swift_root + '/' + self._module_name
        self.copy_dir_and_file(src_path, des_path)

    def copy_dir_and_file(self, src_path, des_path):
        if not os.path.exists(src_path):
            return
        if not os.path.exists(des_path):
            os.makedirs(des_path)
        for file_name in os.listdir(src_path):
            if base.util.should_file_be_ignored(file_name): continue
            a_src_path = os.path.join(src_path, file_name)
            a_des_path = os.path.join(des_path, file_name.replace('.java', '.swift'))
            if os.path.isdir(a_src_path):
                if not os.path.exists(a_des_path): os.makedirs(a_des_path)
                self.copy_dir_and_file(a_src_path, a_des_path)
            elif os.path.isfile(a_src_path):
                self.convert_file(a_src_path, a_des_path)

    def convert_file(self, src, des):
        print(src)
        if os.path.splitext(src)[-1] == '.java':
            cls = src.split('/')[-1].replace('.java', '')
            config.properties[cls] = []
            config.functions[cls] = []
            self.convert_java_file_content(src, des, cls)
        elif src.split('/')[-2] in config.language_file:
            self.convert_java_language(src, des)

    def convert_java_file_content(self, src, des, cls):
        m18_file = M18_file(src, des, cls)
        m18_file.dealWithM18()

    def convert_java_language(self, src, des):
        language = Language(src, des)
        language.lang_convert()



