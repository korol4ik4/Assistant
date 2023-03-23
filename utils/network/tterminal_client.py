from client import Client
from time import time

c = Client('127.0.0.1', 5555)
tm = time()
while not c.isconnected:
    #print('connect..')
    if time()-tm>3:
        raise ConnectionError
c.session()
print('session key ', c.session_key)

while c.isconnected:
    msg = input('>')
    if msg == 'exit':
        break
    c.send_message(msg)