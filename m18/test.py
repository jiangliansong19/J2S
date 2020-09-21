import base.configuration as config

pros = config.properties
array = []
pros['array'] = array

array.append('helo')
array.append('world')
pros["array"] = array

array = config.properties['array']
array.append('1111')
config.properties['array'] = array

print(config.properties)