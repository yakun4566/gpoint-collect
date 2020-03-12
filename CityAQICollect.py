import json
import time
from urllib import request

import arrow
import schedule

import OperaFile
import wcf2xml
import xml2json
from const import Consts
from const import Urls
from get_logger import get_logger
from rabbit.RabbitMQ import RabbitMQ

# transfromcode = ["131200:130700","210281:210281","211200:211200","320281:320281","320282:320282","320481:320481",
#                  "320482:320482","320581:320581","320582:320582","320583:320583","320584:320584","320585:320585",
#                  "320684:320684","321183:321183","330183:330183","330185:330185","330681:330600","330782:330681",
#                  "331300:330782","360600:360600","370181:370181","370281:370281","370282:370282","370283:370283",
#                  "370284:370284","370285:370285","370683:370683","370684:370684","370685:370685","370783:370783",
#                  "371081:371081","371082:371082","371083:371083","532301:532300","532522:532500","532621:532600",
#                  "532801:532800","532901:532900","533103:533100","533321:533300","533421:533400","632100:632100",
#                  "659001:659001","659004:659004"]
transfromcode = ["131200:130700","210281:210281","211200:211200","320281:320281","320282:320282","320481:320481",
                 "320482:320482","320581:320581","320582:320582","320583:320583","320584:320584","320585:320585",
                 "320684:320684","321183:321183","330183:330183","330185:330185","330681:330681","330782:330782",
                 "331300:330600","360600:360600","370181:370181","370281:370281","370282:370282","370283:370283",
                 "370284:370284","370285:370285","370683:370683","370684:370684","370685:370685","370783:370783",
                 "371081:371081","371082:371082","371083:371083","532301:532300","532522:532500","532621:532600",
                 "532801:532800","532901:532900","533103:533100","533321:533300","533421:533400","632100:632100",
                 "659001:659001","659004:659004"]
logger = get_logger()
class CityAQICollect():
    def __init__(self):
        self.station_dict = {}

    def get_city_hour_aqi(self):
        # 判断时间，小时是否大于30
        # 读取上个时间发送的时间
        hour_last_time_file = "const/city_hour_last_time.txt"
        hour_last_time = OperaFile.read_txt(filename=hour_last_time_file)
        now = arrow.now()
        if now.minute < 30 or hour_last_time == now.format("YYYY-MM-DD HH:00:00"):
            logger.debug("分钟小于30或者采集时间(" + hour_last_time + ")等于当前时间，跳过")
            return


        site_aqi = "GetCityAQIPublishLives"
        logger.info("获取全国城市小时AQI...")
        url = Urls.GET_CITY_AQI_URL
        # request.urlretrieve(url, "GetAQIDataPublishLives", download_schedule)
        filename = "data/" + site_aqi
        filename_xml = filename + "_xml"
        request.urlretrieve(url, filename)
        wcf2xml.wcf2xmlMain(filename, filename_xml)
        # logger.info(data._content)

        json_data = xml2json.data_from_xml_json(filename_xml, Consts.CITY_AQI_ENTITY_TAG)
        monitor_time = ''
        if json_data is not None and json_data.__len__() > 0:
            monitor_time = json_data[0]["timepoint"].replace('T', ' ')
            logger.info("获取成功，时间：" + str(monitor_time))
        else:
            logger.info("获取失败，时间：" + str(monitor_time))
        # for j in json_data:
        #     logger.info(j)
        self.send_data_by_rabbit(json_data, "hour")

        # 发送成功后，保存最新的发送时间
        OperaFile.write_txt(filename=hour_last_time_file, str=monitor_time)
        logger.info("获取全国城市小时AQI成功,time:" + monitor_time)
        return json_data

    def get_city_day_aqi(self):
        site_aqi = "GetCityDayAQIPublishLives"
        logger.info("获取全国城市日AQI...")
        url = Urls.GET_CITY_DAY_AQI
        # request.urlretrieve(url, "GetAQIDataPublishLives", download_schedule)

        filename = "data/" + site_aqi
        filename_xml = filename + "_xml"
        request.urlretrieve(url, filename)
        wcf2xml.wcf2xmlMain(filename, filename_xml)
        # logger.info(data._content)
        # logger.info(data._content)

        json_data = xml2json.data_from_xml_json(filename_xml, Consts.CITY_DAY_AQI_TAG)
        monitor_time = ''
        if json_data is not None and json_data.__len__() > 0:
            monitor_time = json_data[0]["timepoint"].replace('T', ' ')
            logger.info("获取成功，时间：" + str(monitor_time))
        else:
            logger.info("获取失败，时间：" + str(monitor_time))
        # for j in json_data:
            # print(j)
            # OperaFile.write_line("CityDayAQI.txt", str(j) + "\n")
        self.send_data_by_rabbit(json_data, "day")
        return json_data


    def get_city_aqi(self,url, type, tag):
        site_aqi = type
        logger.info("获取全国站点AQI...")
        url = url
        # request.urlretrieve(url, "GetAQIDataPublishLives", download_schedule)
        request.urlretrieve(url, "data/" + site_aqi)
        wcf2xml.wcf2xmlMain(site_aqi, "data/" + site_aqi + "_xml")
        # logger.info(data._content)

        json_data = xml2json.data_from_xml_json("data/" + site_aqi + "_xml", tag)
        # for j in json_data:
            # OperaFile.write_line("CityDayAQI.txt", str(j) + "\n")
        self.send_data_by_rabbit(json_data, "day")
        return json_data

    def send_data_by_rabbit(self, datas, type):
        args = ("10.0.16.17", 5627, "producer_country_aqi", "producer_country_aqi", "/")
        logger.info("发送 "+str(type) + " 类型数据，到MQ:" + str(args[0]))
        mq = RabbitMQ(*args)
        mq.connect()  # 调用connect方法，连接broker

        # 调用put方法，向目标queue中发送数据， 第一个参数是data, 第二个参数是queue_name, 第三个参数是route_name
        for data in datas:
            citycode = data.get("citycode")
            for code in transfromcode:
                if code.startswith(citycode):
                    transcode = code.split(":")[1]
                    data["citycode"] = transcode
                    break
                pass

            put_data = {'type': type, 'data': data}
            mq.put(json.dumps(put_data), '', "COUNTRY_CITY_AQI", "COUNTRY_CITY_AQI")
        # 发完数据，主动关闭连接
        mq.close()



if __name__ == '__main__':
    cac = CityAQICollect()
    cac.get_city_hour_aqi()
    # cac.get_city_day_aqi()

    # 初始换静态变量

    """
        定义定时任务
    """
    #
    schedule.every(1).minute.do(cac.get_city_hour_aqi)
    # 每天下载一次站点信息xml
    schedule.every().day.at("05:00").do(cac.get_city_day_aqi)
    for job in schedule.jobs:
        logger.info(str(job))
    while True:
        schedule.run_pending()
        time.sleep(1)

