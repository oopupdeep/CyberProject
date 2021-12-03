from flask import Flask
from flask import render_template
from TelnetClient import TelnetClient
from flask import request
from YamlReader import YamlReader

app = Flask(__name__)
telnetClient = TelnetClient()
yamlReader = YamlReader()

@app.route("/")
def test_page():
    return render_template("test.html")

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

