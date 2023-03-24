import socket
from threading import Thread


class Client:
    def __init__(self,address, port):
        self.sock = socket.socket()
        self.isconnected = False
        self.thr = None

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
        self.thr = Thread(target=self.__connect, args=(adresse, _port))
        self.thr.start()

        #thr.join(timeout=waitsec)

    def send_message(self, message):
        msg = message.encode()
        self.sock.send(msg)


    # self.isconnected=True
    # self.recv_msg()

    def recv_msg(self):
        while self.isconnected:
            try:
                msg = self.sock.recv(1024)
                self.incoming_message(msg.decode())
            except:
                break

    def close(self):
        self.isconnected = False
        self.sock.close()
        self.thr.join()


    def incoming_message(self, message):
        print(message)





