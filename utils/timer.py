#
# Timer run extend function
# start_timer(time_in_seconds, execute_function, *args_for_execute_function)

import time
from threading import Thread


class Timer:
    def __init__(self):
        self.timer_threads = {}
        self.timer_breaks = {}
        self.time_left = {}
        self.count = 1

    def _timer(self, thr_index, sec, after_func, *after_args):
        tm = time.time()
        for i in range(sec):
            if self.timer_breaks[thr_index]:
                after_func = None
                break
            # Поправка. Погрешность без ~ -1(отставание) сек. За 18 мин
            if time.time() - tm - i > 1:
                self.time_left[thr_index] -= 1
                continue

            # print(i,time.time() - tm)
            time.sleep(1)
            self.time_left[thr_index] -= 1
        if after_func:
            after_func(*after_args)

    def start_timer(self, sec_time, after_timer_func, *after_args):
        self.time_left.update({self.count: sec_time})
        self.timer_breaks.update({self.count: False})

        thr = Thread(target=self._timer, args=(self.count, sec_time, after_timer_func, *after_args))
        thr.start()

        self.timer_threads.update({self.count: thr})

        self.count += 1
        return thr

    def clean_timers(self):
        del_index = []
        for count, thr in self.timer_threads.items():
            if not thr.is_alive():  # _is_stopped:
                del_index.append(count)
        for idx in del_index:
            del self.time_left[idx]
            del self.timer_breaks[idx]
            del self.timer_threads[idx]

    def break_timer(self, index):
        if self.timer_breaks.get(index) is not None:
            self.timer_breaks[index] = True


'''
def func(tm):
    print(time.time() - tm)

t = Timer()

t.start_timer(100,func,time.time())
#t.start_timer(10,func,"oGOGo")
tr = True
'''
'''
while tr:
    time.sleep(1)
    print(t.time_left)
    if t.time_left == 99:
        tr = False
        break
'''
