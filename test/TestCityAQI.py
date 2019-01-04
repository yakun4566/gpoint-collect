from urllib import request

import Logger
import wcf2xml
import xml2json
from const import Consts
from const import Urls
import OperaFile

logger = Logger.setup_logging(name=__name__)


def get_city_hour_aqi():
    site_aqi = "GetCityAQIPublishLives"
    logger.info("获取全国站点AQI...")
    url = Urls.GET_CITY_AQI_URL
    # request.urlretrieve(url, "GetAQIDataPublishLives", download_schedule)
    request.urlretrieve(url, site_aqi)
    wcf2xml.wcf2xmlMain(site_aqi, site_aqi + "_xml")
    # logger.info(data._content)

    json_data = xml2json.data_from_xml_json(site_aqi + "_xml", Consts.CITY_AQI_ENTITY_TAG)
    for j in json_data:
        logger.info(j)

def get_city_day_aqi():
    site_aqi = "GetCityDayAQIPublishLives"
    logger.info("获取全国站点AQI...")
    url = Urls.GET_CITY_DAY_AQI
    # request.urlretrieve(url, "GetAQIDataPublishLives", download_schedule)
    request.urlretrieve(url, site_aqi)
    wcf2xml.wcf2xmlMain(site_aqi, site_aqi + "_xml")
    # logger.info(data._content)

    json_data = xml2json.data_from_xml_json(site_aqi + "_xml", Consts.CITY_DAY_AQI_TAG)
    for j in json_data:
        print(j)
        OperaFile.write_line("CityDayAQI.txt", str(j) + "\n")
    pass

if __name__ == '__main__':
    get_city_day_aqi()

    pass

