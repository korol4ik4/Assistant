import socket
from threading import Thread

from time import sleep
import rsa
import rsa.randnum
import utils.network.aes as aes


class Server:
    def __init__(self, port, addresse =''):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((addresse, port))
        self.sock.listen(1000)
        self.conns = []
        self.addrs = []
        self.count = 0
        self.conn_thread()
        self.istalk = True
        self.keys = {}

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
        except:
            print('ошибка :D или выход')

    def session(self, conn, addr):
        # print('server recv data',addr)
        adress = str(addr)
        client_online = True
        #
        while client_online and self.istalk:
            ckey = conn.recv(1024)
            if ckey:
                # print(ckey)
                try:
                    ckey = rsa.key.PublicKey.load_pkcs1(ckey)
                except:
                    conn.close()
                    client_online = False
                    break
                if ckey in self.keys.keys():
                    # знакомый
                    #print('Привет')
                    pass

                # сессионный ключ для этого клиента
                aes_key = rsa.randnum.read_random_bits(128)
                self.keys.update({ckey: (conn, aes_key)})
                # шифруем  aes ключ публичным ключом клиента
                encrypted_aes_key = rsa.encrypt(aes_key, ckey)
                # посылаем
                conn.send(encrypted_aes_key)
                # начинаем общение
                blocks = []
                while client_online and self.istalk:
                    encrypt_block = conn.recv(1024)
                    if encrypt_block:
                        # try:
                        block = aes.shot_decrypt(encrypt_block, aes_key)

                        blocks.append(block)

                        if block.decode().find('\0') > -1:
                            msg = b''.join(blocks)
                            blocks = []

                            self.incomming_message(msg.decode().strip('\0'), ckey)

                # except:

                # print('сервер: ошибка при получении / расшифровке ')

                # conn.close()
                # client_online = False
                # break

        conn.close()

    def send_message(self, msg, client_key):
        '''
        while self.last_msg[client_key]:
            pass
        self.last_msg.update({client_key:msg})
        '''
        self.send_string(msg, client_key)

    def send_string(self, msg, client_key):

        if client_key in self.keys.keys():
            conn, sess_key = self.keys[client_key]

        msg = msg.encode()
        enc_msg = aes.encrypt(msg, sess_key)
        # print(msg)
        for msg in enc_msg:
            conn.send(msg)
            sleep(0.1)

    def incomming_message(self, message, client_key):
        # print('incomm server ', message)
        self.new_message(message, client_key)
        '''
        if client_key not in self.last_msg.keys():
            self.last_msg.update({client_key:''})			
        if self.last_msg[client_key]:
            if self.last_msg[client_key] == message:
                print('сервер: мессага отправлена и принята ',message)
                self.last_msg.update({client_key:''})
            else:

                self.send_message(self.last_msg[client_key],client_key)
        else:				
            #print('сервер: сообщение от клиента', message)
            self.new_message(message,client_key)
            self.send_string(message, client_key=client_key)
    '''

    def new_message(self, message, mfrom):
        print(message, mfrom)

