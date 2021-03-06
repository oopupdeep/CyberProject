import telnetlib
import time

class TelnetClient:
    def __init__(self):
        self.tn = telnetlib.Telnet()

    def input(self, cmd):
        self.tn.write(cmd.encode('ascii') + b'\n')

    def get_output(self):
        time.sleep(0.1)
        return self.tn.read_very_eager().decode('ascii')

    def login(self, host_ip, username, password):
        try:
            self.tn.open(host_ip)
        except:
            return "连接失败"
        # self.tn.read_until(b'login: ')
        # self.input(username)
        self.tn.read_until(b'Password: ')
        self.input(password)
        login_result = self.get_output()
        print(login_result)
        if 'Login incorrect' in login_result:
            print('用户名或密码错误')
            return False
        print('登陆成功')
        return True

    def logout(self):
        self.input('exit')

    def exec_cmd(self, cmd):
        self.input(cmd)
        res = self.get_output()
        print("===================")
        print(res)
        print("===================")
        return res


if __name__ == '__main__':
    tc = TelnetClient()
    tc.login('192.168.1.1', 'root', 'CISCO')
    tc.exec_cmd('ifconfig')
    tc.exec_cmd('ll -a')
    tc.logout()



