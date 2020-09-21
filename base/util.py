import re
import os
import base.configuration as config
import base.javaclass as java


def getContent(file):
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            file_data += line
    return file_data


# 判断字母l，是否在尖括号内
def is_letter_in_angle_brackets(l, idx, str):

    c = 0
    for i, ch in enumerate(str):
        if ch == '<': c += 1
        if ch == '>': c -= 1
        if ch == l and i == idx: return c != 0

    return False


# 判断字符串是否为类名
def is_class_name(cls) -> bool:

    ma = re.match(r'([\w<>]*)', cls, re.I | re.M)
    if not ma or not ma.group(1):
        return False
    if cls in java.system_class:
        return True
    if cls in java.class_reflect.keys():
        return True
    if cls in java.extra_class:
        return True
    if cls in config.properties.keys():
        return True
    if cls in config.functions.keys():
        return True
    return False


# 类名转换
def swift_class_from_java(cls) -> str:
    java_class = cls
    swift_class = java_class
    if java_class in java.class_reflect:
        swift_class = java.class_reflect[java_class]
        return swift_class

    ma = re.match(r'(\w*)<(\w*)>', cls, re.I | re.M)
    if ma and ma.group(1) and ma.group(2):
        if 'map' in ma.group(1).lower():
            swift_class = '[' + ma.group(2) + ']'
        elif 'list' in ma.group(1).lower():
            swift_class = '[' + ma.group(2).replace(',', ':') + ']'
    return swift_class


# 深拷贝: 拷贝目录下所有子孙目录及子孙文件,
# ignores: 忽略文件的文件名，后缀等
def deep_copy(src_path, des_path, ignores=None):

    if ignores is None:
        ignores = []
    if not os.path.exists(src_path):
        return
    if not os.path.exists(des_path):
        os.makedirs(des_path)

    for file_name in os.listdir(src_path):
        if should_file_be_ignored(file_name):
            continue
        a_src_path = os.path.join(src_path, file_name)
        a_des_path = os.path.join(des_path, file_name)
        if os.path.isdir(a_src_path):
            deep_copy(a_src_path, a_des_path, ignores)
        elif os.path.isfile(a_src_path):
            os.system('cp ' + a_src_path + ' ' + a_des_path)


def should_file_be_ignored(file_name):
    ignores = config.ignore_file
    file_name_items = file_name.split('.')
    for item in file_name_items:
        if item in ignores:
            return True
    return False