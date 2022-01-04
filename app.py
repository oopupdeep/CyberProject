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
    return returnList()


@app.route("/simpleExecuteStaticConfig", methods=["POST"])
def simpleExecuteStaticConfig():
    generalConfig(routerA, "YamlConfig/static_router/static_router1_config.yaml")
    generalConfig(routerB, "YamlConfig/static_router/static_router2_config.yaml")
    generalConfig(routerC, "YamlConfig/static_router/static_router3_config.yaml")
    generalConfig(routerA, "YamlConfig/static_router/static_router1_config1.yaml")
    generalConfig(routerB, "YamlConfig/static_router/static_router2_config1.yaml")
    generalConfig(routerC, "YamlConfig/static_router/static_router3_config1.yaml")
    return returnList()


@app.route("/simpleExecuteOspfConfig", methods=["POST"])
def simpleExecuteOspfConfig():
    generalConfig(routerA, "YamlConfig/ospf/ospf_configA.yaml")
    generalConfig(routerB, "YamlConfig/ospf/ospf_configB.yaml")
    generalConfig(routerC, "YamlConfig/ospf/ospf_configC.yaml")
    return returnList()


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
    return json.dumps({"command": yaml_file})


@app.route("/modifyYaml", methods=['POST'])
def modifyYaml():
    yaml_file = json.loads(request.get_data())["newFile"]
    file_name = json.loads(request.get_data())["option"]
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
    with open("YamlConfig/change_router_ip.yaml", 'r', encoding='utf-8') as file:
        lines = file.readlines()
    ip = f"ip address {routerip} 255.255.255.0"
    lines[len(lines) - 1] = ip
    with open("YamlConfig/change_router_ip.yaml", 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(line)

    if routerid == "0":
        generalConfig(routerA, "YamlConfig/change_router_ip.yaml")
        routerA = routerip
    elif routerid == "1":
        generalConfig(routerB, "YamlConfig/change_router_ip.yaml")
        routerB = routerip
    elif routerid == "2":
        generalConfig(routerC, "YamlConfig/change_router_ip.yaml")
        routerC = routerip
    print(routerid)
    print(routerip)
    return returnList()


# 根据topology的值执行对应的验证脚本并将结果返回到前端
@app.route("/checkTopology", methods=['POST'])
def checkTopology():
    topology = request.form.get("TYPE")
    result = None
    if topology == "static":
        result = generalConfig(routerA, "YamlConfig/check_topology/check_static.yaml")
    elif topology == "rip":
        result = generalConfig(routerB, "YamlConfig/check_topology/check_rip.yaml")
    elif topology == "ospf":
        result = generalConfig(routerA, "YamlConfig/check_topology/check_ospf.yaml")
    return json.dumps(result)


def generalConfig(ip_address, config_address):
    # 对ip对应的路由器执行脚本
    telnetClient.login(ip_address, None, "CISCO")
    data = yamlReader.get_yaml(config_address)
    result = ""
    for lines in data:
        data = telnetClient.exec_cmd(lines)
        result = result + data + '\n'
    return result


def returnInfo(ip_address):
    telnetClient.login(ip_address, None, "CISCO")
    telnetClient.exec_cmd("enable")
    telnetClient.exec_cmd("CISCO")
    output = telnetClient.exec_cmd("show ip interface brief").split()
    return output


# 配置拓扑后返回路由器信息
def returnList():
    output_a = returnInfo(routerA)
    index1_a = output_a.index('Serial0/0/0')
    index2_a = output_a.index('Serial0/0/1')
    output_b = returnInfo(routerB)
    index1_b = output_b.index('Serial0/0/0')
    index2_b = output_b.index('Serial0/0/1')
    output_c = returnInfo(routerC)
    index1_c = output_c.index('Serial0/0/0')
    index2_c = output_c.index('Serial0/0/1')
    lis = [{"id": 0,
            "name": "路由器A",
            "label": "RTA",
            "type": "router",
            "ip": routerA,
            "S0/0/0": output_a[index1_a + 1],
            "s0/0/1": output_a[index2_a + 1],
            "port": "未知",
            "ignore": "false",
            "flag": "true"}, {
               "id": 1,
               "name": "路由器B",
               "label": "RTB",
               "type": "router",
               "ip": routerB,
               "S0/0/0": output_b[index1_b + 1],
               "S0/0/1": output_b[index2_b + 1],
               "port": "22",
               "ignore": "true",
               "flag": "true"
           }, {
               "id": 2,
               "name": "路由器C",
               "label": "RTC",
               "type": "router",
               "ip": routerC,
               "S0/0/0": output_c[index1_c + 1],
               "S0/0/1": output_c[index2_c + 1],
               "port": "33",
               "ignore": "true",
               "flag": "true"
           }]
    return json.dumps(lis)
