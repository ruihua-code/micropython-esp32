import socket
import ujson
from zrh_response_json import ZrhResponseJson

resJson = ZrhResponseJson()
text_plain = 'HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n'
text_html = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
application_json = 'HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n'


def do_socket():
    print("启动socket服务")
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind(('0.0.0.0', 80))
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
            elif request_method[0] == 'POST' or request_method[1] == '/cmd':
                try:
                    jsonParams = ujson.loads(request_params)
                    print("jsonParams type:", type(jsonParams))
                    print("params json:", jsonParams)
                    resJson.success("成功")
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
