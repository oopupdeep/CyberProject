from flask import Flask
from flask import render_template
from TelnetClient import TelnetClient
from flask import request,url_for
from YamlReader import YamlReader
import json

app = Flask(__name__)
telnetClient = TelnetClient()
yamlReader = YamlReader()

@app.route("/")
def test_page():
    return render_template("static_routing.html")

# telnet远程登录路由器
@app.route("/telnet", methods=["POST"])
def telnet():
    host_ip = request.form.get("host_ip")
    username = request.form.get("username")
    password = request.form.get("password")
    msg = telnetClient.login(host_ip, username, password)
    return msg

@app.route("/readYaml")
def readYaml():
    data = yamlReader.get_yaml("YamlConfig/test_config.yaml")
    # data = yamlReader.get_yaml(file_data)
    return data

@app.route("/simpleExecuteRipConfig", methods=["POST"])
def simpleExecuteRipConfig():
    data = None
    msg = telnetClient.login("192.168.1.1", None, "CISCO")
    data = yamlReader.get_yaml("YamlConfig/rip/rip_configA.yaml")
    for lines in data:
        data = telnetClient.exec_cmd(lines)
        print(data)
    msg = telnetClient.login("192.168.1.2", None, "CISCO")
    data = yamlReader.get_yaml("YamlConfig/rip/rip_configB.yaml")
    for lines in data:
        data = telnetClient.exec_cmd(lines)
        print(data)
    msg = telnetClient.login("192.168.1.3", None, "CISCO")
    data = yamlReader.get_yaml("YamlConfig/rip/rip_configC.yaml")
    for lines in data:
        data = telnetClient.exec_cmd(lines)
        print(data)
    return "success"

@app.route("/simpleExecuteStaticConfig", methods=["POST"])
def simpleExecuteStaticConfig():
    data = None
    msg = telnetClient.login("192.168.1.1", None, "CISCO")
    data = yamlReader.get_yaml("YamlConfig/static_router/static_router1_config.yaml")
    for lines in data:
        data = telnetClient.exec_cmd(lines)
        print(data)
    msg = telnetClient.login("192.168.1.2", None, "CISCO")
    data = yamlReader.get_yaml("YamlConfig/static_router/static_router2_config.yaml")
    for lines in data:
        data = telnetClient.exec_cmd(lines)
        print(data)
    msg = telnetClient.login("192.168.1.3", None, "CISCO")
    data = yamlReader.get_yaml("YamlConfig/static_router/static_router3_config.yaml")
    for lines in data:
        data = telnetClient.exec_cmd(lines)
        print(data)
    msg = telnetClient.login("192.168.1.1", None, "CISCO")
    data = yamlReader.get_yaml("YamlConfig/static_router/static_router1_config1.yaml")
    for lines in data:
        data = telnetClient.exec_cmd(lines)
        print(data)
    msg = telnetClient.login("192.168.1.2", None, "CISCO")
    data = yamlReader.get_yaml("YamlConfig/static_router/static_router2_config1.yaml")
    for lines in data:
        data = telnetClient.exec_cmd(lines)
        print(data)
    msg = telnetClient.login("192.168.1.3", None, "CISCO")
    data = yamlReader.get_yaml("YamlConfig/static_router/static_router3_config1.yaml")
    for lines in data:
        data = telnetClient.exec_cmd(lines)
        print(data)
    return "success"

@app.route("/showYaml", methods=['POST'])
def showYaml():
    yaml_file_name = json.loads(request.get_data())["YamlName"]
    yaml_file = None
    if "static" in yaml_file_name:
        yaml_file = yamlReader.get_yaml("YamlConfig/static_router/{}".format(yaml_file_name))
    elif 'rip' in yaml_file_name:
        yaml_file = yamlReader.get_yaml("YamlConfig/rip/{}".format(yaml_file_name))
    elif 'ospf' in yaml_file_name:
        yaml_file = yamlReader.get_yaml("YamlConfig/rip/{}".format(yaml_file_name))
    print(json.dumps({"command":yaml_file}))
    return json.dumps({"command":yaml_file})



@app.route("/modifyYaml", methods=['POST'])
def modifyYaml():
    yaml_file = json.loads(request.get_data())["newFile"]
    file_name = json.loads(request.get_data())["option"]
    # yaml_file = yaml_file.split("\n")
    try:
        file = None
        if "static" in file_name:
            file = open("YamlConfig/static_router/{}".format(file_name),'w')
        elif 'rip' in file_name:
            file = open("YamlConfig/rip/{}".format(file_name),'w')
        elif 'ospf' in file_name:
            file = open("YamlConfig/ospf/{}".format(file_name),'w')
        file.write(yaml_file)
        file.close()
        return json.dumps({"msg":"成功！"})
    except:
        return json.dumps({"msg":"修改失败！"})

# @app.route("/executeRipConfig", methods=["POST"])
# def executeRipConfigA():
#     data = None
#     router_type = request.form.get("router_type")
#     if router_type == "executeRipConfigA":
#         data = yamlReader.get_yaml("YamlConfig/rip/rip_configA.yaml")
#     elif router_type == "executeRipConfigB":
#         data = yamlReader.get_yaml("YamlConfig/rip/rip_configB.yaml")
#     elif router_type == "executeRipConfigC":
#         data = yamlReader.get_yaml("YamlConfig/rip/rip_configC.yaml")
#     for lines in data:
#         data = telnetClient.exec_cmd(lines)
#         print(data)
#     return "success"

# @app.route("/executeRipConfigB", methods=["POST"])
# def executeRipConfigB():
#     data = yamlReader.get_yaml("YamlConfig/rip_configB.yaml")
#     for lines in data:
#         data = telnetClient.exec_cmd(lines)
#         print(data)
#     return "success"
#
# @app.route("/executeRipConfigC", methods=["POST"])
# def executeRipConfigC():
#     data = yamlReader.get_yaml("YamlConfig/rip_configC.yaml")
#     for lines in data:
#         data = telnetClient.exec_cmd(lines)
#         print(data)
#     return "success"

