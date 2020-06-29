import os
from urllib import request

import arrow

import Logger
import wcf2xml
import xml2json

class TestXianHE:
    def __init__(self):
        self.logger = Logger.setup_logging(default_path="resources/logging.yml", name=__name__)
        self.xianhe_hour = "GetHourData"
        self.xianhe_min = "GetMinuteData"

        self.station_dict = {}


    def get_site_hour_aqi(self):
        """
        下载小时AQI,转换为xml,再转换为json保存文件,返回json对象
        :return:
        """
        url = "http://117.78.41.224:8017/webapi/OtherDataService.svc"
        # request.urlretrieve(url, "GetAQIDataPublishLives", download_schedule)
        request.urlretrieve(url, self.xianhe_hour)
        wcf2xml.wcf2xmlMain(self.xianhe_hour, self.xianhe_hour + "_xml")
        # self.logger.info(data._content)

        json_data = xml2json.data_from_xml_json(self.xianhe_hour + "_xml", "")
        today = arrow.now().format("YYYYMMDD")
        path = os.getcwd() + os.sep + "data" + os.sep + today
        if not os.path.exists(path):
            os.makedirs(path)
        file_name = self.xianhe_hour + "_" + arrow.now().format("YYYYMMDDHH") + ".json"
        file_path = path + os.sep + file_name
        self.logger.info("保存AQI数据:%s" % (file_path))
        # OperaFile.write_txt(filename=file_path, str=str(json_data))
        return json_data