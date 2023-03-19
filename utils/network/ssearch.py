from netifaces import interfaces, ifaddresses, AF_INET
from client import Client
from time import sleep


def find_server(port,self_interfaces=False,localhost = False, waittime=2):

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

    def ip_to_search(ip: str) -> list[str]:
        # validate
        if ip and isinstance(ip, str):
            ip_bytes = ip.split('.')
            if len(ip_bytes) == 4 and all((i.isnumeric() for i in ip_bytes)):
                # ip/24
                if ip == "127.0.0.1":
                    return [ip,]
                last_byte = int(ip_bytes[-1])
                if not last_byte:  # == 0 or None or ...False?)
                    return
                ip_begin = '.'.join(ip_bytes[:-1]) + '.'
                ip_to_test = [ip_begin + str(i) for i in range(1, 256) if i != last_byte]
                return ip_to_test


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
        sleep(waittime-0.1)
        # save connected clients
        serv_ip = [cl.sock.getpeername()[0] for cl in clients if cl.isconnected]
        return serv_ip

    def server_list(port, self_interfaces = False, localhost=False, waittime=2):
        interface = test_network(loc=localhost)

        if self_interfaces:
            return search_server(port,interface,waittime)

        s_list = []
        for iface in interface:
            ip_to_test = ip_to_search(iface)
            s_list += search_server(port,ip_to_test,waittime=waittime)
        return s_list

    return server_list(port=port,self_interfaces=self_interfaces,localhost=localhost,waittime=waittime)



port = 80
print(find_server(port=port, waittime=1, self_interfaces=False,localhost=False))

