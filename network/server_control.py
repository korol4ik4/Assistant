
class ServerControl:
    def __init__(self, **kwargs):
        # table variable
        self.connect = []  # id = index
        self.thread = []
        self.session_key = []
        # ----
        # oneToMore
        self.public_key = []  # kid = index:
        self.sess_pub = {}  # id:kid
        # ----

    @staticmethod
    def attr_valid(**kwargs):
        if 'connect' not in kwargs.keys():
            raise Exception("connect is required attribute")
        # unknown attributes
        attrs = 'connect', 'thread' ,'session_key', 'public_key'
        for attr in kwargs.keys():
            if attr not in attrs:
                raise Exception(f'unknown attribute {attr}={kwargs[attr]}')

    def append_connect_thread(self,connect,thread):
        self.connect.append(connect)
        self.thread.append(thread)
        self.session_key.append(None)

    def update_keys(self,connect,session_key,public_key):
        if not connect or not session_key or not public_key:
            raise Exception(f'fail keys update : connect = {connect}, session_key = {session_key}, public_key = {public_key}')
        if connect not in self.connect:
            raise Exception(f"keys update fail, unknown connect {connect}")
        index = self.connect.index(connect)
        self.session_key[index] = session_key

        if public_key in self.public_key:
            pub_id =  self.public_key.index(public_key)
        else:
            self.public_key.append(public_key)
            pub_id = len(self.public_key) - 1
        self.sess_pub.update({index:pub_id})

    def get_line(self, index):
        if index > len(self.connect):
            return
        line = [self.connect[index], self.thread[index], self.session_key[index]]
        if not self.session_key[index]:
            line.append(None)
        else:
            pub_key = self.public_key[self.sess_pub[index]]
            line.append(pub_key)
        return line

    def del_line(self, index):
        if index > len(self.connect):
            return
        # удаление из списка
        self.connect.pop(index)
        self.thread.pop(index)
        self.session_key.pop(index)
        # удаление из промежуточной "таблицы"

        pub_key_index = self.sess_pub.pop(index)  # id:kid
        #print(index, pub_key_index, self.sess_pub)  # id:kid
        # удаляем публичный ключ если это последняя запись ссылающиеся на него
        if pub_key_index not in self.sess_pub.values():
            self.public_key.pop(pub_key_index)
            # нужно поправить self.sess_pub, так как все индексы  public_key выше pub_key_index сместились на -1
            # сначала values()
            for sid in self.sess_pub.keys():
                if self.sess_pub[sid] > pub_key_index:
                    self.sess_pub[sid] -= 1
        # а теперь ключи
        new_sess_pub = {}
        for sid, pid in self.sess_pub.items():
            if sid > index:
                sid -= 1
            new_sess_pub.update({sid:pid})
        self.sess_pub = new_sess_pub





    def get(self, **kwargs):

        if not kwargs:
            rows = []
            for i in range(len(self.connect)):
                rows.append(self.get_line(i))
            return rows

        self.attr_valid(**kwargs)
        connect = kwargs.get("connect")
        thread = kwargs.get("thread")
        session_key = kwargs.get("session_key")
        public_key = kwargs.get("public_key")

        if connect:
            if connect not in self.connect:
                return None
            id = self.connect.index(connect)
            return self.get_line(id)

        elif thread:
            if thread not in self.thread:
                return None
            id = self.thread.index(thread)
            return self.get_line(id)

        elif session_key:
            if session_key not in self.session_key:
                return None
            id = self.session_key.index(session_key)
            return self.get_line(id)

        elif public_key:
            if public_key not in self.public_key:
                return None
            pub_id = self.public_key.index(public_key)
            rows = []
            for id, pid in self.sess_pub.items():
                if pid == pub_id:
                    rows.append(self.get_line(id))
            return rows

    def close_id(self,id):
        if id >= len(self.connect):
            return
        try:
            self.thread[id].join(1)
            self.connect[id].close()
        except:
            pass
        self.del_line(id)

    def clean(self):
        for id,connect in enumerate(self.connect):
            if connect.sock:
                if connect.sock.fileno()<0:
                    self.close_id(id)
            else:
                self.close_id(id)

