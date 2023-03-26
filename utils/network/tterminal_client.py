from client import Client
from time import time

class TClient(Client):
    def __init__(self,*args,**kwargs):
        super(TClient, self).__init__(*args,**kwargs)

    # def incoming_message(self, message):

c = Client('127.0.0.1', 5555)
tm = time()
while not c.isconnected:
    #print('connect..')
    if time()-tm>3:
        raise ConnectionError

while c.isconnected:
    msg = input('>')
    c.send_message(msg)
    if msg == 'exit':
        break
c.close()
