
import socket
import threading

listenPort = 5000
ipAddress = '127.0.0.1'


class Receive(threading.Thread):

    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        try:
            while True:
                input = self.socket.recv(1024)
                print(input.decode("utf-8"))
        except Exception as e:
            print(e)


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ipAddress, listenPort))
    rec = s.recv(1024)
    print(rec.decode("utf-8"))
    name = input()
    s.send(name.encode("utf-8"))
    rec = s.recv(1024)
    print(rec.decode("utf-8"))
    r = Receive(s)
    r.start()
    msgToSend = input()
    while msgToSend != "再见":
        s.send(msgToSend.encode("utf-8"))
        msgToSend = input()
    else:
        s.send(msgToSend.encode("utf-8"))
