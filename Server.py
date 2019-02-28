
import socket
import threading
import Client

listenPort = 5000
ipAddress = '127.0.0.1'


class UserInfo:
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name


class ServerThread(threading.Thread):

    def __init__(self, socket, *user):
        threading.Thread.__init__(self)
        self.socket = socket
        u = UserInfo("")
        self.user = u

    def getUser(self):
        return self.user

    def welcome(self, name):
        self.user.setName(name)
        Control.addClient(self)
        self.sendMsg("服务器消息：你好，" + self.user.getName())

    def sendMsg(self, msg):
        self.socket.send(msg.encode(encoding="utf-8"))

    def outputMsg(self, msg):
        print(self.user.getName() + "说：" + msg)
        Control.pushMsg(self.user, msg)

    def run(self):
        try:
            self.sendMsg("服务器消息：欢迎来到聊天室，请输入用户名：")
            name = self.socket.recv(1024)
            self.welcome(name.decode("utf-8"))
            input = self.socket.recv(1024)
            input = input.decode("utf-8")
            while input != "再见":
                self.outputMsg(input)
                input = self.socket.recv(1024)
                input = input.decode("utf-8")
            else:
                self.outputMsg(input)
                Control.logOut(self.user)
                Client.isGo = False

        except Exception as e:
            print(e)


class Control:

    stList = []
    clientNumber = 0

    @staticmethod
    def addClient(st):
        Control.stList.append(st)
        Control.clientNumber += 1
        user = st.getUser()
        name = user.getName()
        msg = name + " 上线了！ （目前聊天室人数：" + str(Control.clientNumber) + "）"
        for st in Control.stList:
            st.sendMsg(msg)

    @staticmethod
    def pushMsg(user, msg):
        msg = user.getName() + "说：" + msg
        for st in Control.stList:
            st.sendMsg(msg)

    @staticmethod
    def logOut(user):
        msg = user.getName() + "下线了。"
        Control.clientNumber -= 1;
        msg = msg + " （目前聊天室人数：" + str(Control.clientNumber) + "）"
        for st in Control.stList:
            st.sendMsg(msg)


def acceptConnections():
    print("服务器已创建，端口为" + str(listenPort))
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ipAddress, listenPort))
        while True:
            s.listen(30)
            sock, addr= s.accept()
            print("进入了一个客户连接：" + str(addr))
            t = ServerThread(sock)
            t.start()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    acceptConnections()


