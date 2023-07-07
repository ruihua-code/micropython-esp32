'''
扫描指定蓝牙设备
'''
import bluetooth
from time import sleep
from micropython import const
import zrh_thread_var
from zrh_gpio import do_led
import gc

_IRQ_SCAN_RESULT = const(5)

# 小米手环mac
_XIAO_MI_MAC = const('D9:6E:B5:74:A8:E3')


def do_ble_central():
    # 初始化蓝牙
    bt = bluetooth.BLE()

    # 启用蓝牙
    bt.active(True)

    # 定义回调函数处理扫描结果
    def scan_callback(event, data):
        if event == _IRQ_SCAN_RESULT:
            _, addr, _, rssi, _ = data
            # 将地址转换为字符串格式
            _device_address = ":".join("{:02X}".format(b) for b in addr)
            if _XIAO_MI_MAC == _device_address:
                # print("*** 找到目标设备 ***", _device_address, rssi)
                if abs(rssi) > 40 and abs(rssi) < 70:
                    do_led(1)
                    # zrh_thread_var.ble_central_run = False
                else:
                    do_led(0)

    # 开始扫描外围设备，每隔1秒扫描1秒时间，无限期扫描
    # duration_ms 要无限期扫描，请将 *duration_ms* 设置为“0”。要停止扫描，请将 *duration_ms* 设置为“None”。
    # interval_us
    # window_us
    bt.gap_scan(0, 2000000, 2000000)
    bt.irq(scan_callback)

    # 等待扫描完成
    # time.sleep(30)

    # 停止扫描
    # bt.gap_scan(None)

    # 停止蓝牙模块
    # bt.active(False)

    while True:
        sleep(2)
        gc.collect()
        # micropython.mem_info()
        if zrh_thread_var.ble_central_run == False:
            # 停止扫描
            bt.gap_scan(None)

            # 停止蓝牙模块
            bt.active(False)
            do_led(0)
            break
