'''
扫描指定蓝牙设备
'''
import bluetooth
from micropython import const
import gc
import uasyncio as asyncio
from time import sleep
from zrh_gpio import do_led

_IRQ_SCAN_RESULT = const(5)

# 小米手环mac
_XIAO_MI_MAC = const('D9:6E:B5:74:A8:E3')
# 初始化蓝牙
_bt = bluetooth.BLE()
_task = None
_loop = None


async def start_ble_central():
    # 启用蓝牙
    _bt.active(True)

    # 定义回调函数处理扫描结果
    def scan_callback(event, data):
        if event == _IRQ_SCAN_RESULT:
            _, addr, _, rssi, _ = data
            # 将地址转换为字符串格式
            _device_address = ":".join("{:02X}".format(b) for b in addr)
            if _XIAO_MI_MAC == _device_address:
                if abs(rssi) > 40 and abs(rssi) < 70:
                    print("*** 找到目标设备 ***", _device_address, rssi)
                    do_led(1)
                    gc.collect()
                else:
                    do_led(0)

    # 开始扫描外围设备，每隔1秒扫描1秒时间，无限期扫描
    # duration_ms 要无限期扫描，请将 *duration_ms* 设置为“0”。要停止扫描，请将 *duration_ms* 设置为“None”。
    # interval_us
    # window_us
    _bt.gap_scan(0, 2000000, 2000000)
    _bt.irq(scan_callback)
    while _bt.active():
        print("ble scaning...", _bt.active(), _task)
        await asyncio.sleep_ms(500)


def stop_ble_central():
    print("stop scan")
    _bt.gap_scan(None)
    # 停止蓝牙模块
    _bt.active(False)
    print("wait end....")
    _task.run_until_complete(start_ble_central())
    _task.cancel()
    _loop.close()


def do_ble_central():
    # 创建事件循环对象
    global _loop
    _loop = asyncio.get_event_loop()
    # 运行协程函数
    global _task
    _task = asyncio.create_task(start_ble_central())
