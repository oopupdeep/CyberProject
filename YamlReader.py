import yaml
import os

class YamlReader:
    def get_yaml(self,yaml_file):
        print("***获取yaml数据***")
        file = open(yaml_file, 'r', encoding='utf-8')
        file_data = file.read()
        print("***转化yaml数据为字典或列表***")
        data = yaml.load(file_data,Loader=yaml.FullLoader)
        return data




