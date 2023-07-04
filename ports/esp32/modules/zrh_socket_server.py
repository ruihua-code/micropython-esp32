import socket
import machine


def doSocket():
    print("启动socket服务")
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    while True:
        cl, addr = s.accept()
        print('client connected from', addr)
        data = cl.recv(1024)

        if len(data) > 0:
            # print("全部数据:", data.decode("utf-8"))
            # print("想要的路径:", data.decode("utf-8").split()[1])
            path = data.decode("utf-8").split()[1]
            # 路径作为参数
            if ('temperature' in path):
                # 获取温度和湿度
                temp = getTemp()
                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
                cl.send(str(temp.decode().split(",")[0]))
                showLedNumber(temp.decode().split(",")[0])

            elif ('humidity' in path):
                temp = getTemp()
                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
                cl.send(str(temp.decode().split(",")[1]))
                showLedNumber(temp.decode().split(",")[1])

            elif ('onLight' in path):
                onLight()
                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
                cl.send("ok")

            elif ('onWarmLight' in path):
                onWarmLight()
                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
                cl.send("ok")

            elif ('closeLed' in path):
                offall()
                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
                cl.send("ok")

            elif ('resetDevice' in path):
                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
                cl.send("ok")
                machine.reset()

        cl.close()
