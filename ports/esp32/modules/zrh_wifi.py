from zrh_wifi_ap import doAp
from time import sleep
import network
from zrh_wifi_nvs import getWifiNVS
from zrh_board_led import on_led

from zrh_domain import hostname


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    while not wlan.active(True):
        print("wait wlan")

    print("hostname:", hostname)
    # 使用域名方式访问（esp.local）
    wlan.config(dhcp_hostname=hostname)

    if not wlan.isconnected():
        print('--- 开始连接网格 ---')
        global wifiConfig
        try:
            wifiConfig = getWifiNVS()
            print("wifiConfig:", wifiConfig)
            wlan.connect(wifiConfig['ssid'], wifiConfig['password'])
        except OSError as e:
            print("读取wifi配置信息失败")

        connTimeOut = 0
        while not wlan.isconnected():
            print("连接失败，正在重新连接...")
            sleep(1)
            connTimeOut += 1
            # 连接网络15秒超时
            if (connTimeOut >= 10):
                print("--- 连接超时 ---")
                break
        if wlan.isconnected():
            # wifi连接成功，led长亮
            on_led()
            print('连网成功:', wlan.ifconfig())
        else:
            # wifi连接失败,展示红色灯
            # led_pwm_blue = PWM(Pin(5))
            # led_pwm_blue.duty(50)
            print("连接失败了,开启ap模式")
            doAp()
