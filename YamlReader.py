import yaml
import os

class YamlReader:
    def get_yaml(self,yaml_file):
        print("***获取yaml数据***")
        file = open(yaml_file, 'r', encoding='utf-8')
        file_data = file.readlines()
        print("***转化yaml数据为字典或列表***")
        return file_data

# testYamlReader
if __name__ == '__main__':
    reader = YamlReader()
    data = reader.get_yaml("YamlConfig/rip/rip_configA.yaml")
    for lines in data:
        # data = telnetClient.exec_cmd(lines)
        print(lines)



