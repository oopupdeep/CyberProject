from flask import Flask
from flask import render_template
from TelnetClient import TelnetClient
from flask import request, url_for
from YamlReader import YamlReader
import json

app = Flask(__name__)
telnetClient = TelnetClient()
yamlReader = YamlReader()

# 这里的IP用于telnet连接，请不要修改
# 路由器接口的IP见具体的yaml文件
routerA = "192.168.1.1"
routerB = "192.168.1.2"
routerC = "192.168.1.3"


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
    generalConfig(routerA, "YamlConfig/rip/rip_configA.yaml")
    generalConfig(routerB, "YamlConfig/rip/rip_configB.yaml")
    generalConfig(routerC, "YamlConfig/rip/rip_configC.yaml")
    lis = [{"id": 0,
            "name": "路由器A",
            "label": "RTA",
            "type": "router",
            "ip": routerA,
            "S0/0/0": "192.168.1.2/24",
            "port": "未知",
            "ignore": "false",
            "flag": "true"}, {
               "id": 1,
               "name": "路由器B",
               "label": "RTB",
               "type": "router",
               "ip": routerB,
               "S0/0/0": "192.168.1.2/24",
               "s0/0/1": "192.168.2.1/24",
               "port": "22",
               "ignore": "true",
               "flag": "true"
           }, {
               "id": 2,
               "name": "路由器C",
               "label": "RTC",
               "type": "router",
               "ip": routerC,
               "S0/0/0": "192.168.2.2/24",
               "port": "33",
               "ignore": "true",
               "flag": "true"
           }]
    return json.dumps(lis)


@app.route("/simpleExecuteStaticConfig", methods=["POST"])
def simpleExecuteStaticConfig():
    generalConfig(routerA, "YamlConfig/static_router/static_router1_config.yaml")
    generalConfig(routerB, "YamlConfig/static_router/static_router1_config.yaml")
    generalConfig(routerC, "YamlConfig/static_router/static_router1_config.yaml")
    generalConfig(routerA, "YamlConfig/static_router/static_router1_config1.yaml")
    generalConfig(routerB, "YamlConfig/static_router/static_router1_config2.yaml")
    generalConfig(routerC, "YamlConfig/static_router/static_router1_config3.yaml")
    lis = [{
        "id": 0,
        "name": "路由器A",
        "label": "RTA",
        "type": "router",
        "ip": routerA,
        "S0/0/0": "192.168.12.1/24",
        "port": "未知",
        "ignore": "false",
        "flag": "true"
    }, {
        "id": 1,
        "name": "路由器B",
        "label": "RTB",
        "type": "router",
        "ip": routerB,
        "S0/0/0": "192.168.12.2/24",
        "s0/0/1": "192.168.23.2/24",
        "port": "22",
        "ignore": "true",
        "flag": "true"
    }, {
        "id": 2,
        "name": "路由器C",
        "label": "RTC",
        "type": "router",
        "ip": routerC,
        "S0/0/0": "192.168.23.3/24",
        "port": "33",
        "ignore": "true",
        "flag": "true"
    }]
    return json.dumps(lis)


@app.route("/simpleExecuteOspfConfig", methods=["POST"])
def simpleExecuteOspfConfig():
    generalConfig(routerA, "YamlConfig/ospf/ospf_configA.yaml")
    generalConfig(routerB, "YamlConfig/ospf/ospf_configB.yaml")
    generalConfig(routerC, "YamlConfig/ospf/ospf_configC.yaml")
    lis = [{"id": 0,
            "name": "路由器A",
            "label": "RTA",
            "type": "router",
            "ip": routerA,
            "S0/0/0": "192.168.1.2/24",
            "port": "未知",
            "ignore": "false",
            "flag": "true"}, {
               "id": 1,
               "name": "路由器B",
               "label": "RTB",
               "type": "router",
               "ip": routerB,
               "S0/0/0": "192.168.1.2/24",
               "s0/0/1": "192.168.2.1/24",
               "port": "22",
               "ignore": "true",
               "flag": "true"
           }, {
               "id": 2,
               "name": "路由器C",
               "label": "RTC",
               "type": "router",
               "ip": routerC,
               "S0/0/0": "192.168.2.2/24",
               "port": "33",
               "ignore": "true",
               "flag": "true"
           }]
    msg = json.dumps(lis)
    return msg


@app.route("/showYaml", methods=['POST'])
def showYaml():
    yaml_file_name = json.loads(request.get_data())["YamlName"]
    yaml_file = None
    if "static" in yaml_file_name:
        yaml_file = yamlReader.get_yaml("YamlConfig/static_router/{}".format(yaml_file_name))
    elif 'rip' in yaml_file_name:
        yaml_file = yamlReader.get_yaml("YamlConfig/rip/{}".format(yaml_file_name))
    elif 'ospf' in yaml_file_name:
        yaml_file = yamlReader.get_yaml("YamlConfig/ospf/{}".format(yaml_file_name))
    print(json.dumps({"command": yaml_file}))
    return json.dumps({"command": yaml_file})


@app.route("/modifyYaml", methods=['POST'])
def modifyYaml():
    yaml_file = json.loads(request.get_data())["newFile"]
    file_name = json.loads(request.get_data())["option"]
    # yaml_file = yaml_file.split("\n")
    try:
        file = None
        if "static" in file_name:
            file = open("YamlConfig/static_router/{}".format(file_name), 'w')
        elif 'rip' in file_name:
            file = open("YamlConfig/rip/{}".format(file_name), 'w')
        elif 'ospf' in file_name:
            file = open("YamlConfig/ospf/{}".format(file_name), 'w')
        file.write(yaml_file)
        file.close()
        return json.dumps({"msg": "成功！"})
    except:
        return json.dumps({"msg": "修改失败！"})


@app.route("/changeIP", methods=['POST'])
def changeIP():
    global routerA, routerB, routerC
    routerid = request.form.get("ID")
    routerip = request.form.get("IP")
    lines = []
    with open("YamlConfig/change_router_ip.yaml", 'r', encoding='utf-8') as file:
        lines = file.readlines()
    ip = f"ip address {routerip} 255.255.255.0"
    lines[len(lines) - 1] = ip
    with open("YamlConfig/change_router_ip.yaml", 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(line)

    if routerid == "0":
        # 需要修改change_router_ip脚本
        generalConfig(routerA, "YamlConfig/change_router_ip.yaml")
        routerA = routerip
    elif routerid == "1":
        generalConfig(routerB, "YamlConfig/change_router_ip.yaml")
        routerB = routerip
    elif routerid == "2":
        generalConfig(routerC, "YamlConfig/change_router_ip.yaml")
        routerC = routerip
    lis = [{"id": 0,
            "name": "路由器A",
            "label": "RTA",
            "type": "router",
            "ip": routerA,
            "S0/0/0": "192.168.1.2/24",
            "port": "未知",
            "ignore": "false",
            "flag": "true"}, {
               "id": 1,
               "name": "路由器B",
               "label": "RTB",
               "type": "router",
               "ip": routerB,
               "S0/0/0": "192.168.1.2/24",
               "s0/0/1": "192.168.2.1/24",
               "port": "22",
               "ignore": "true",
               "flag": "true"
           }, {
               "id": 2,
               "name": "路由器C",
               "label": "RTC",
               "type": "router",
               "ip": routerC,
               "S0/0/0": "192.168.2.2/24",
               "port": "33",
               "ignore": "true",
               "flag": "true"
           }]
    return json.dumps(lis)


def generalConfig(ip_address, config_address):
    # 对ip对应的路由器执行脚本
    telnetClient.login(ip_address, None, "CISCO")
    data = yamlReader.get_yaml(config_address)
    for lines in data:
        data = telnetClient.exec_cmd(lines)
        print(data)
