
import base.configuration as config
import base.util
from m18.module import Module

for module in config.module_names:
    base.util.deep_copy(config.java_project_root, config.java_project_temp, config.ignore_file)
    Module(config.java_project_temp, config.swift_project_root, module).convert_module()