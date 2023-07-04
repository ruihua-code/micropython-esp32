import socket
import network
from zrh_response_json import ZrhResponseJson
from zrh_wifi_html import html
import ujson
from zrh_wifi_nvs import setWifiNVS

resJson = ZrhResponseJson()
text_plain = 'HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n'
text_html = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
application_json = 'HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n'


# 解析url里面的ssid和password
def getUrlParams(url):
    arr = url.split("&password=")
    password = arr[1]
    arr2 = arr[0].split("ssid=")
    ssid = arr2[1]
    print(ssid, password)
    return {
        "ssid": ssid,
        "password": password
    }


# 启动socket TCP Server
def doAp():
    # 创建wifi热点，ssid=ESP-AP password=esp123456
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='ESP-AP', authmode=network.AUTH_WPA_WPA2_PSK,
              password='esp123456')

    while ap.active() == False:
        pass
    print('--- AP热点启动成功 ---')
    print(ap.ifconfig())

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind(('0.0.0.0', 8080))
    my_socket.listen(5)
    while True:
        client_socket, _ = my_socket.accept()
        data = client_socket.recv(1024)
        if len(data) > 0:
            data_arr = data.decode().split("\r\n")
            print("dataArr:", data_arr)

            # 请求参数
            request_params = data_arr[len(data_arr)-1]
            print("params:", request_params)

            request_method = data_arr[0].split(" ")

            print("method:", request_method)
            if len(request_method) == 1:
                print("什么请求都没有")
                return
            # 请求wifi配置页面
            if request_method[0] == "GET" and request_method[1] == "/wifi":
                print("访问wifi配置页面")
                client_socket.send(text_html)
                client_socket.send(html)
                print("页面访问完成")

            elif request_method[0] == 'POST' or request_method[1] == '/cmd':
                try:
                    jsonParams = ujson.loads(request_params)
                    print("jsonParams type:", type(jsonParams))
                    print("params json:", jsonParams)
                    # 检查接口关键key是否存在
                    if 'cmd' in jsonParams:
                        if jsonParams['cmd'] == 'SET_WIFI':
                            setWifiNVS(jsonParams['data']['ssid'],
                                       jsonParams['data']['password'])
                            resJson.success("wifi配置成功")
                        else:
                            resJson.success("成功")
                    else:
                        # 接口参数错误
                        resJson.error("失败,json参数错误")
                except Exception as e:
                    print("json error", e)
                    resJson.error("失败,json参数错误")
                client_socket.send(application_json)
                client_socket.send(resJson.json())

            else:
                # 其他未知请求，全部拒绝
                resJson.error("请求被拒绝")
                client_socket.send(application_json)
                client_socket.send(resJson.json())
            client_socket.close()
