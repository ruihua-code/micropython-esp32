from esp32 import NVS


# 读取持久存储wifi配置信息
def getWifiNVS():
    wifiConfig = NVS("WIFI_CONFIG")
    ssidBuf = bytearray(12)
    passwordBuf = bytearray(12)
    wifiConfig.get_blob("ssid", ssidBuf)
    wifiConfig.get_blob("password", passwordBuf)
    return {
        "ssid": ssidBuf.decode(),
        "password": passwordBuf.decode()
    }


# wifi配置信息持久存储
def setWifiNVS(ssid, password):
    print("开始写入flash")
    wifiConfig = NVS("WIFI_CONFIG")
    wifiConfig.set_blob("ssid", ssid)
    wifiConfig.set_blob("password", password)
    wifiConfig.commit()
    print("--- wifi配置信息存储完成 ---")


# 清除wifi配置信息
def eraseWifiNVS():
    wifiConfig = NVS("WIFI_CONFIG")
    try:
        wifiConfig.erase_key("ssid")
        wifiConfig.erase_key("password")
    except OSError as e:
        print("清空wifi配置信息错误:", e)
