import socket
from threading import Thread




class Server:
    def __init__(self, port, address =''):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((address, port))
        self.sock.listen(1000)
        self.count = 0
        self.conns = {}
        self.conn_thread()
        self.istalk = True


    # self.last_msg ={}

    def conn_thread(self):
        self.count += 1
        print('connect weit ', self.count)
        serv = Thread(target=self.connect, args=())
        serv.start()

    def connect(self):
        try:
            conn, addr = self.sock.accept()
            tlk = Thread(target=self.session, args=(conn, addr))
            tlk.start()
            if self.istalk:
                self.conn_thread()
            if not conn in self.conns:
                self.conns.update({conn:addr})
        except:
            print('ошибка :D или выход')

    def session(self, conn, addr):
        print(f'start session with {addr}')
        while self.istalk:
            msg = conn.recv(1024)
            self.incoming_message(msg.decode(),conn)
        conn.close()



    def send_message(self, message, conn):
        msg = message.encode()
        conn.send(msg)


    def incoming_message(self, message,conn):
        print('from ', conn)
        print(message)

