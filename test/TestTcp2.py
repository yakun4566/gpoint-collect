import json
import socket

import time

import Logger


class TestTcp2:
    def __init__(self):
        self.logger = Logger.setup_logging(default_path="resources/logging.yml", name=__name__)
    def send_socket(self, data, ip, port):
        for i in range(1, 4):
            try:
                tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.logger.info("准备创建tcp client, " + str(i) + "次")
                self.logger.info("发送数据" + str(data))
                # tcp_client.connect(('192.168.15.54', 9000))
                tcp_client.settimeout(20)
                tcp_client.connect((ip, port))
                # print("socket 连接成功：" + str(tcp_client.getsockname()) + "-->" + str(tcp_client.getpeername()))
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
                self.logger.info("socket 回复：" + buffer.decode(encoding="utf-8"))
                if json.loads(result).get("code") == "111":
                    # print("发送成功，结束")
                    return True
                # self.logger.info("发送失败：" + str(i) + "次")
            except Exception as e:
                self.logger.info("发送tcp数据包异常", e)
        return False


if __name__ == '__main__':
    send_data_json = {}
    send_data_json['appId'] = 'datacollect'
    send_data_json['appKey'] = '123456789'
    send_data_json['datatype'] = 'SMALLAIR'
    send_data_json['datakind'] = 'HourData'
    send_data = {}
    i = 0
    tcp = TestTcp2()

    while(True) :
        i+= 1
        send_data_list = []
        send_data["PM10"] = str(i)
        send_data["PM2_5"] = str(i)
        send_data["SO2"] = str(i)
        send_data["NO2"] = str(i)
        send_data["CO"] = str(i)
        # TODO 接口中 o3_24h 和 o3 两个值是反的，发送时o3_24h当做o3
        send_data["O3"] = ""
        send_data["O3_8H"] = str(i)
        send_data["MONITORTIME"] = "2019-03-20 11:49:07"
        send_data["SITECODE"] = str(i)
        send_data["DATASOURCES"] = "test"
        send_data_list.append(send_data)

        send_data_json['data'] = send_data_list

        tcp.send_socket(json.dumps(send_data_json), "123.160.220.40", 60015)

        time.sleep(1)