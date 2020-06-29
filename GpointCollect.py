# -*- coding:utf-8 -*-

import json
import os
import re
import socket
from configparser import ConfigParser
from urllib import request

import arrow

import OperaFile
import wcf2xml
import xml2json
from const import Consts
from const import Urls
from get_logger import get_logger

cp = ConfigParser()
cp.read("resources/config.cfg")

logger = get_logger()

class GpointCollectAQI:
    def __init__(self):

        self.site_info_file = "data/GetStationConfigs"
        self.site_aqi = "data/GetAQIDataPublishLives"

        self.station_dict = {}
        self.load_site_info()

    def download_schedule(self, a, b, c):
        """
        a:已经下载的数据块
        b:数据块的大小
        c:远程文件的大小
       """
        per = 100.0 * a * b / c
        if per >= 100:
            per = 100
        logger.info('%.2f%%' % per)

    def send_socket(self, data, ip, port):
        for i in range(1, 4):
            try:
                datas = data.encode()
                lbytes = int.to_bytes(datas.__len__(), 4, byteorder='big')
                b = lbytes + datas

                tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                logger.info("准备创建tcp client【"+ip + str(port) + "】, " + str(i) + "次")
                # tcp_client.connect(('192.168.15.54', 9000))
                tcp_client.settimeout(20)
                tcp_client.connect((ip, port))
                logger.info("socket 连接成功：" + str(tcp_client.getsockname()) + "-->" + str(tcp_client.getpeername()))
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
                logger.info("socket 回复：" + buffer.decode(encoding="utf-8"))
                if json.loads(result).get("code") == "111":
                    logger.info("发送成功，结束")
                    return True
                logger.info("发送失败：" + str(i) + "次")
            except Exception as e:
                logger.error("发送tcp数据包异常", e)
        return False

    def isNumber(self, str):
        """
        判断是否为数字
        :param str:
        :return:
        """
        if None is str:
            return False
        pattern = re.compile('^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
        result = pattern.match(str)
        if result:
            return True
        else:
            return False

    def get_site_hour_aqi(self):
        """
        下载小时AQI,转换为xml,再转换为json保存文件,返回json对象
        :return:
        """
        # 保存地址
        file_path = self.site_aqi
        url = Urls.GET_SITE_AQI_URL
        # request.urlretrieve(url, "GetAQIDataPublishLives", download_schedule)
        request.urlretrieve(url, file_path)
        wcf2xml.wcf2xmlMain(file_path, file_path + "_xml")
        # logger.info(data._content)

        json_data = xml2json.data_from_xml_json(file_path + "_xml", Consts.SITE_AQI_ENTITY_TAG)
        # today = arrow.now().format("YYYYMMDD")
        # path = os.getcwd() + os.sep + "data" + os.sep + today
        path = os.getcwd() + os.sep
        # if not os.path.exists(path):
        #     os.makedirs(path)
        # TODO 数据暂时不保存
        # file_name = self.site_aqi + "_" + arrow.now().format("YYYYMMDDHH") + ".json"
        file_name = self.site_aqi + ".json"
        file_path = path + os.sep + file_name
        logger.info("保存AQI数据:%s" % (file_path))
        OperaFile.write_txt(filename=file_path, str=str(json_data))
        return json_data

    def get_site_air_data(self):
        # 判断时间，小时是否大于30
        # 读取上个时间发送的时间
        hour_last_time_file = "const/hour_last_time.txt"
        hour_last_time = OperaFile.read_txt(filename=hour_last_time_file)
        now = arrow.now()
        if now.minute < 30 or hour_last_time == now.format("YYYY-MM-DD HH:00:00"):
            logger.debug("分钟小于30或者采集时间(" + hour_last_time + ")等于当前时间，跳过")
            return

        try:
            logger.info("获取全国站点小时AQI...")

            json_data = self.get_site_hour_aqi()
            if json_data is not None and json_data.__len__() > 0:
                logger.info("采集成功:【"+str(json_data.__len__())+"】个,监测时间:" + str(json_data[0]["timepoint"]))
            else:
                logger.info("采集失败！")
            send_data_list = []
            equals_count = 0

            monitor_time = ""
            for d in json_data:
                try:
                    # 判断站点是否需要对应
                    site_code = d['stationcode']
                    if site_code not in Consts.FILTER_SITES:
                        site_code = self.station_dict.get(site_code, site_code)
                    if str(site_code).startswith('41'):
                        logger.debug("河南省的数据，跳过:" + str(d))
                        continue
                    send_data = {}
                    send_data["PM10"] = d.get('pm10') if self.isNumber(d.get('pm10')) else "0"
                    send_data["PM2_5"] = d.get('pm2_5') if self.isNumber(d.get('pm2_5')) else "0"
                    send_data["SO2"] = d.get('so2') if self.isNumber(d.get('so2')) else "0"
                    send_data["NO2"] = d.get('no2') if self.isNumber(d.get('no2')) else "0"
                    send_data["CO"] = d.get('co') if self.isNumber(d.get('co')) else "0"
                    # TODO 接口中 o3_24h 和 o3 两个值是反的，发送时o3_24h当做o3
                    send_data["O3"] = d.get('o3_24h') if self.isNumber(d.get('o3_24h')) else "0"
                    send_data["O3_8H"] = d.get('o3_8h') if self.isNumber(d.get('o3_8h')) else "0"
                    send_data["MONITORTIME"] = d.get('timepoint').replace('T', ' ')
                    send_data["SITECODE"] = site_code
                    send_data["DATASOURCES"] = "cnemc.cn"
                    if hour_last_time == send_data["MONITORTIME"]:
                        logger.debug("重复数据，不发送：" + str(send_data))
                        equals_count += 1
                        continue
                    monitor_time = send_data["MONITORTIME"]
                    send_data_list.append(send_data)
                except Exception as e:
                    logger.error("循环数据时异常", e)
            if len(send_data_list) <= 0:
                logger.info("有效数据：0，重复数据：" + str(equals_count))
                return
            send_status = self.send_data(send_data_list)
            if send_status:
                logger.info("发送成功，修改时间:" + monitor_time)
                # 发送成功后，保存最新的发送时间
                OperaFile.write_txt(filename=hour_last_time_file, str=monitor_time)
        except Exception as e:
            logger.error("采集全国站点AQI数据异常", e)

    def send_data(self, send_data_list):
        logger.info("发送数据：" + str(send_data_list.__len__()) + "个")
        send_data_json = {
            'appId': 'datacollect',
            'appKey': '123456789',
            'datatype': 'GPOINTAIR',
            'datakind': 'HourData'
        }
        # 循环 list，每次发送100个
        temp_list = []
        for temp in send_data_list:
            temp_list.append(temp)
            if temp_list.__len__() > 99:
                send_data_json['data'] = temp_list
                # 发送数据
                self.send_data_(send_data_json)
                temp_list = []

        # 发送数据
        send_data_json['data'] = temp_list
        return self.send_data_(send_data_json)

    def send_data_(self, send_data_json):
        flag = False
        ip_port = cp._sections.get("remote_address").get("ip_port")
        ip_port_arr = ip_port.split(",")
        for address in ip_port_arr:
            for i in range(0, 4):
                flag = self.send_socket(json.dumps(send_data_json), address.split(":")[0], int(address.split(":")[1]))
                if flag:
                    break
        return flag

    def get_site_info_xml(self):

        logger.info("下载站点信息xml...")
        url = Urls.GET_SITE_URL
        request.urlretrieve(url, self.site_info_file, self.download_schedule)
        # 下载之后执行一次加载站点信息
        self.load_site_info()


    def load_site_info(self):
        logger.info("加载站点基础信息...")
        wcf2xml.wcf2xmlMain(self.site_info_file, self.site_info_file + "_xml")
        # logger.info(data._content)

        json_data = xml2json.data_from_xml_json(self.site_info_file + "_xml", Consts.SITE_ENTITY_TAG)
        for d in json_data:
            self.station_dict[d['stationcode']] = d['uniquecode']
        logger.info("加载成功：" + str(len(self.station_dict)) + "个")
        file_name = "GetStationConfigs.json"
        path = os.getcwd() + os.sep + "data"
        file_path = path + os.sep + file_name
        logger.info("保存AQI数据:%s" % (file_path))
        OperaFile.write_txt(filename=file_path, str=str(json_data))
        return self.station_dict


# start
if __name__ == '__main__':
    gc = GpointCollectAQI()
    # 初始换静态变量
    gc.get_site_info_xml()

    gc.load_site_info()

    gc.get_site_air_data()
    """
        定义定时任务
    """
    # # 每15分钟执行一次小时数据AQI抓取
    # schedule.every(1).minute.do(gc.get_site_air_data)
    # # 每天下载一次站点信息xml
    # schedule.every().day.at("01:10").do(gc.get_site_info_xml)
    # for job in schedule.jobs:
    #     logger.info(str(job))
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    # pass
