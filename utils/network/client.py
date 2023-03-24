import socket
from threading import Thread


class Client:
    def __init__(self,address, port):
        self.sock = socket.socket()
        self.isconnected = False
        self.connect(address, port)


    # self.last_msg=''

    def __connect(self, adresse, _port):
        #print('client connect to ',adresse,_port)
        try:
            self.sock.connect((adresse, _port))
            self.isconnected = True
            self.recv_msg()

        except:
            #no route to host
            pass

    def connect(self, adresse, _port, waitsec = None):
        self.sock.settimeout(waitsec)
        thr = Thread(target=self.__connect, args=(adresse, _port))
        thr.start()

        #thr.join(timeout=waitsec)

    def send_message(self, message):
        msg = message.encode()
        self.sock.send(msg)


    # self.isconnected=True
    # self.recv_msg()

    def recv_msg(self):
        while self.isconnected:
            msg = self.sock.recv(1024)
            self.incoming_message(msg.decode())

    def incoming_message(self, message):
        print(message)





