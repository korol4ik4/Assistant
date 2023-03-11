import socket
from threading import Thread

from time import sleep, time
import rsa
import aes

import hashlib


class Client:
    def __init__(self, *args):
        self.sock = socket.socket()
        ####

        self.pubkey, self.privkey = self.get_keys()
        # print(self.pubkey)
        ####
        self.session_key = ''
        self.isconnected = False
        if len(args) == 2:
            addresse, port = args
            self.connect(addresse, port)


    # self.last_msg=''

    def __connect(self, adresse, _port):
        #print('client connect to ',adresse,_port)
        try:
            self.sock.connect((adresse, _port))
            self.isconnected = True
        except:
            #no route to host
            pass

    def connect(self, adresse, _port, waitsec = None):
        self.sock.settimeout(waitsec)
        thr = Thread(target=self.__connect, args=(adresse, _port))
        thr.start()
        #thr.join(timeout=waitsec)

    @staticmethod
    def get_keys():
        try:
            with open('public_key', 'rb') as f:
                pubkey = rsa.key.PublicKey.load_pkcs1(f.read())
            with open('private_key', 'rb') as f:
                privkey = rsa.key.PrivateKey.load_pkcs1(f.read())

        except FileNotFoundError:
            try:
                pubkey, privkey = rsa.newkeys(512)
                dpub = pubkey.save_pkcs1()
                dpriv = privkey.save_pkcs1()
                with open('public_key', 'wb') as f:
                    f.write(dpub)
                with open('private_key', 'wb') as f:
                    f.write(dpriv)
            except:
                print(' don\'t save keys to files')
                return None, None
        except:
            print('don\'t create/load rsa keys')
            return None, None

        return pubkey, privkey

    def ping(self):
        try:
            data_key = self.pubkey.save_pkcs1()
            self.sock.send(data_key)
            encrypt_sess_key = self.sock.recv(1024)
            sess_key = rsa.decrypt(encrypt_sess_key, self.privkey)
            self.session_key = sess_key

            recv = Thread(target=self.recv_msg, args=())
            recv.start()
            # self.recv_msg()
            return True
        except:
            return False

    def send_message(self, msg):
        # ,delivery_chek=True):
        '''
        if delivery_chek:
            while self.last_msg:
                pass
            self.last_msg = msg
        '''
        msg = msg.encode()
        # print('vclient send ',msg)
        enc_msg = aes.encrypt(msg, self.session_key)
        # print(enc_msg)
        for msg in enc_msg:
            self.sock.send(msg)
            sleep(0.1)

    # self.isconnected=True
    # self.recv_msg()

    def recv_msg(self):
        blocks = []
        while self.isconnected:
            encrypt_block = self.sock.recv(1024)
            if encrypt_block:
                try:
                    block = aes.shot_decrypt(encrypt_block, self.session_key)
                    blocks.append(block)
                    if block.decode().find('\0') > -1:
                        msg = b''.join(blocks)
                        self.incomming_message(msg.decode().strip('\0'))
                        blocks = []
                except:
                    print('клиент: ошибка при получении / расшифровке ')
                    self.sock.close()
                    self.isconnected = False
                    break

    def incomming_message(self, message):
        # print('incomm ', message)
        self.new_message(message, 'server')
        '''
        if self.last_msg:
            if message == self.last_msg:
                print('клиент: мессага отправлена и принята ',message)
                self.last_msg = ''
            else:
                self.send_message(self.last_msg)
        else:
            #print('клиент: сообщение от сервера', message)
            self.new_message(message,'server')
            self.send_message(message,delivery_chek=False)
    '''

    def new_message(self, message, mfrom):
        print(message, mfrom)






