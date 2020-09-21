
# 属性，变量，静态变量
import re
import base.javaclass
import base.configuration as config


# public static final String DATE_NIL = "1900-01-01";
# var static final String DATA = "data";
# private static final String FIELD_NAME_CONTACT = "mainqu.manId";
def convert_static_property(line):
    temp = line.lstrip(' ')
    if temp.startswith('public static final') or temp.startswith('private static final'):
        ma = re.search(r'(public|private) static final (\w*) (.*)', temp, re.I | re.M)
        if ma and ma.group(2):
            temp = line.replace(ma.group(2), 'var')
            return temp
    return line


class Property:

    _line = ''
    _cls = ''

    def __init__(self, line, cls):
        self._line = line
        self._cls = cls

    def convert_property(self):

        result = self._line
        result = self.convert_bind_view_property(result)
        result = self.convert_normal_property(result)
        result = convert_static_property(result)

        return result

    # @BindView(R2.id.iv_back) ImageView ivBack;
    def convert_bind_view_property(self, line):

        ma = re.search(r'(.*)@BindView(.*) (.*) (.*);', line, re.M | re.I)
        if ma and ma.group(1) and ma.group(2) and ma.group(3):
            class_dict = base.javaclass.class_reflect
            class_name = class_dict.get(ma.group(3), ma.group(3))
            line = ma.group(1) + 'var ' + ma.group(4) + ': ' + class_name + '?\n'

            properties = config.properties[self._cls]
            properties.append(ma.group(4))
            config.properties[self._cls] = properties
        return line


    def convert_normal_property(self, line):

        ma = re.search(r'(\s*)(private|public) (\w*) (\w*);', line, re.M | re.I)
        if ma and ma.group(3) and ma.group(4):
            class_dict = base.javaclass.class_reflect
            class_name = class_dict.get(ma.group(3), ma.group(3))
            line = ma.group(1) + ma.group(2) + ' var ' + ma.group(4) + ': ' + class_name + '?\n'

            properties = config.properties[self._cls]
            properties.append(ma.group(4))
            config.properties[self._cls] = properties
        return line


