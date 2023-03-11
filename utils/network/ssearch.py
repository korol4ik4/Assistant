from netifaces import interfaces, ifaddresses, AF_INET
from client import Client
from time import sleep


port = 5555
serv_ip =search_server(port,1)
clients = []
print(serv_ip)

for ip in serv_ip:
    cl = Client(ip, port)
    cl.ping()
    cl.send_message('ok')
    clients.append(cl)

print(clients)
#закрыть клиентов
for cl in clients:
    cl.isconnected=False  #  Для выхода из цикла чтения
    cl.send_message('exit')  # Посылаем серверу, он должен ответить, что снимет блокировку sock.recv
    cl.sock.close()

print('close')

class ClientManager:
    @staticmethod
    def test_network(loc=False) -> list:
        addresses = []
        for iname in interfaces():
            addrs = [addr['addr'] for addr in ifaddresses(iname).setdefault(AF_INET, [{'addr': None}])]
            for addr in addrs:
                if addr:
                    if loc:
                        addresses.append(addr)
                    elif not addr.startswith('127.'):
                        addresses.append(addr)
        return addresses

    @staticmethod
    def ip_to_search(ip: str) -> list[str]:
        # validate
        if ip and isinstance(ip, str):
            ip_bytes = ip.split('.')
            if len(ip_bytes) == 4 and all((i.isnumeric() for i in ip_bytes)):
                # ip/24
                last_byte = int(ip_bytes[-1])
                if not last_byte:  # == 0 or None or ...False?)
                    return
                ip_begin = '.'.join(ip_bytes[:-1]) + '.'
                ip_to_test = [ip_begin + str(i) for i in range(1, 256) if i != last_byte]
                return ip_to_test

    @staticmethod
    def search_server(port, ip_list=[], waittime=2):
        # test of connect, create one Client for every ip
        print('start connect..')
        clients = []
        for ip in ip_list:
            cl = Client()
            cl.connect(ip, port, waittime)
            clients.append(cl)
            # wait
        print('wait', waittime, ' sec')
        sleep(waittime)
        # save connected clients
        serv_ip = [cl.sock.getpeername()[0] for cl in clients if cl.isconnected]
        return serv_ip

    def __init__(self,port, *args, **kwargs):
        self.port = port
        self.connects = []
