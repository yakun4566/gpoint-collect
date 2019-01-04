import json
import logging
import socket

import re

import wcf2xml
import xml2json
from const import Consts

class TestTcp:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.site_info_file = "GetStationConfigs"
        self.site_aqi = "GetAQIDataPublishLives"

        self.station_dict = {}

    def send_socket(self,data):
        for i in range(0, 3):
            try:
                tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("准备创建tcp client, " + str(i) + "次")
                # tcp_client.connect(('192.168.15.54', 9000))
                tcp_client.settimeout(20)
                tcp_client.connect(('127.0.0.1', 60009))
                print("socket 连接成功：" + str(tcp_client.getsockname()) + "-->" + str(tcp_client.getpeername()))
                datas = data.encode()
                lbytes = int.to_bytes(datas.__len__(), 4, byteorder='big')
                b = lbytes + datas
                tcp_client.send(b)

                len_bytes = tcp_client.recv(4)
                len = int.from_bytes(len_bytes, byteorder='big')
                buffer = tcp_client.recv(len)
                # while True:
                #     # 每次最多接收1k字节:
                #     d = tcp_client.recv(1024)
                #     if d:
                #         buffer += d
                #     else:
                #         break
                tcp_client.close()
                result = buffer.decode(encoding="utf-8")
                print("socket 回复：" + buffer.decode(encoding="utf-8"))
                if json.loads(result).get("code") == "111":
                    print("发送成功，结束")
                    return True
                print("发送失败：" + str(i) + "次")
            except Exception as e:
                self.logger.error("发送tcp数据包异常", e)
        return False

if __name__ == '__main__':
    send_data_json = {}
    send_data_json['appId'] = 'datacollect'
    send_data_json['appKey'] = '123456789'
    send_data_json['datatype'] = 'SMALLAIR'
    send_data_json['datakind'] = 'HourData'




    tcp = TestTcp()
    send_data = {}
    send_data_list = []
    for i in range(0, 1650):
        send_data["PM10"] = ""
        send_data["PM2_5"] = ""
        send_data["SO2"] = ""
        send_data["NO2"] = ""
        send_data["CO"] = ""
        # TODO 接口中 o3_24h 和 o3 两个值是反的，发送时o3_24h当做o3
        send_data["O3"] = ""
        send_data["O3_8H"] = ""
        send_data["MONITORTIME"] = "2016-11-26 08:53:39"
        send_data["SITECODE"] = ""
        send_data["DATASOURCES"] = "cnemc.cn"
        send_data_list.append(send_data)
        if send_data_list.__len__() >= 100:
            send_data_json['data'] = send_data_list
            print("发送:" + str(len(send_data_json['data'])) + "个")
            tcp.send_socket(json.dumps(send_data_json))
            send_data_list = []
    send_data_json['data'] = send_data_list
    print("发送:" + str(len(send_data_json['data'])) + "个")
    tcp.send_socket(json.dumps(send_data_json))
    pass