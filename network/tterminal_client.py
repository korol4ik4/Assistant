from client import Client
from time import time

import os

class TerminalTail:
    def __init__(self,*args,**kwargs):
        self.bg_color = 0 # default
        self.fg_color = 0 # default
        self.ascii_byte = 0 # additional byte

        self.input_col = 1
        self.input_row = 1
        self.input_store_col_nums = 10
        self.input_store_col = 4
        self.input_store_row = 1
        self.additional_store_col_nums = 10
        self.additional_store_col = 16
        self.additional_store_row = 1

        self.input_symbol = '>'
        self.input_separator = '-'
        self.input_store_symbol = '<'
        self.input_store_separator = '#'
        self.additional_store_symbol = ' '
        self.additional_store_separator = '*'

        for key, value in kwargs.items():
            if key in self.__dict__:
                self.__dict__[key] = value
        self.colorized = f'\033[{self.ascii_byte};{self.fg_color};{self.bg_color}m'

        self._additional_store = ''
        self._input_store =''


    def set_input(self,col=1, row=1, symbol ='>', separator =''):
        self.input_col = col
        self.input_row = row
        self.input_symbol = symbol

    def set_input_store(self,col_nums=5,col=3,row=1,symbol='<',separator = '#'):
        self.input_store_col_nums = col_nums
        self.input_store_col = col
        self.input_store_row = row
        self.input_store_symbol = symbol
        self.input_store_separator = separator

    def set_additional_store(self,col_nums=5,col=10,row=1,symbol=' ',separator = '*'):
        self.additional_store_col_nums = col_nums
        self.additional_store_col = col
        self.additional_store_row = row
        self.additional_store_symbol = symbol
        self.additional_store_separator = separator

    @staticmethod
    def get_color(color:str, ground='FG', bright=False):
        start_byte = 30  # black FG color
        colors = ('black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'white')
        if color not in colors:
            return

        if ground == 'FG':
            start_byte += 0
        elif ground == 'BG':
            start_byte += 10
        else:
            return

        if bright:
            start_byte += 60

        return start_byte + colors.index(color)

    def get_line(self, col=1, row=1 ,separator='',symbol=''):
        line = '\033[' + str(col) + ';' + str(row) + 'H'
        line += self.colorized
        if separator:
            t_size = self.terminal_size()
            if all(t_size):
                line += (separator * t_size[1])
            else:
                line += (separator * 20 + '\n')
            line += '\033[' + str(col+1) + ';' + str(row) + 'H'
            line += symbol
        return line

    def input_line(self):
        return self.get_line(self.input_col, self.input_row, self.input_separator, self.input_symbol)

    def input_store_line(self):
        return self.get_line(self.input_store_col,self.input_store_row,self.input_store_separator,self.input_store_symbol)

    def additional_line(self):
        return self.get_line(self.additional_store_col, self.additional_store_row, self.additional_store_separator, self.additional_store_symbol)

    @staticmethod
    def terminal_size():
        try:
            rows, columns = os.popen('stty size', 'r').read().split()
        except:
            return 0, 0
        if rows.isnumeric() and columns.isnumeric():
            rows,columns = int(rows), int(columns)
            return rows, columns
        return 0, 0

    def terminal_input(self):
        line = self.input_line()+'\033['+str(len(self.input_symbol))+'D'
        new_input = input(line)
        if self._input_store:
            self._input_store = new_input + '\n' + self.input_store_symbol + self._input_store
        else:
            self._input_store = new_input
        return new_input

    def addition(self, addit: str = ''):
        if self._additional_store:
            self._additional_store = addit + '\n' + self.additional_store_symbol + self._additional_store
        else:
            self._additional_store = addit
        add_it = self._additional_store.split('\n')
        if len(add_it) > self.additional_store_col_nums:
            self._additional_store = '\n'.join(add_it[:-1])
        print(self.additional_line() + self._additional_store)

    def input_store(self):
        store = self._input_store.split('\n')
        if len(store) > self.input_store_col_nums:
            self._input_store = '\n'.join(store[:-1])
        print(self.input_store_line()+self._input_store)


    def clear(self):
        print('\033[0;0;0m\033[0;0H\033[2J')


class TClient(Client):
    def __init__(self,*args,**kwargs):
        super(TClient, self).__init__(*args,**kwargs)
        self.tail = TerminalTail()
        tm = time()
        while not self.isconnected:
            # print('connect..')
            if time() - tm > 10:
                raise ConnectionError

    def incoming_message(self, message):
        self.tail.clear()
        self.tail.input_store()
        self.tail.addition(message)
        print(self.tail.input_line())
        print('\033[2A')
        #print('>')
        #print(self.tail.to_input_line())
        #self.tail.terminal_input()
        #self.tail.to_input_line()


    def run(self):

        while self.isconnected:
            self.tail.clear()
            self.tail.input_store()
            self.tail.addition()
            msg = self.tail.terminal_input()
            if msg == 'clear':
                self.tail._input_store=''
                self.tail._additional_store = ''
                self.tail.clear()
                continue

            self.send_message(msg)

            if msg == 'exit':
                break

        self.close()


c = TClient('127.0.0.1', 5555)
c.run()
