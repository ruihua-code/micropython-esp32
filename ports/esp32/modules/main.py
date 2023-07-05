import _thread
from zrh_wifi import do_connect
from zrh_ble_central import do_ble_central
import zrh_thread_var
from time import sleep


def do_ble_central_thread(name):
    while True:
        if zrh_thread_var.ble_central_run == True:
            do_ble_central()
        sleep(2)


if __name__ == '__main__':
    _thread.start_new_thread(do_ble_central_thread, ('do_ble_central_thread',))
    _thread.start_new_thread(do_connect, ('do_connect_thread',))
    while True:
        pass
