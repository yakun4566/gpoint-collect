# -*- coding:utf-8 -*-
from urllib import request

import wcf2xml
import xml2json
from const import Consts
from const import Urls


class SiteInfoXml:
    def __init__(self):
        self.site_info_file = "GetStationConfigs"
        self.site_aqi = "GetAQIDataPublishLives"

        self.station_dict = {}
    def download_schedule(self, a, b, c):
        """
        a:已经下载的数据块
        b:数据块的大小
        c:远程文件的大小
       """
        per = 100.0 * a * b / c
        if per >= 100:
            per = 100
        print('%.2f%%' % per)
    def get_site_info_xml(self):
        print("下载站点信息xml...")
        url = Urls.GET_SITE_URL
        request.urlretrieve(url, self.site_info_file, self.download_schedule)

    def get_site_info(self):
        print("加载站点基础信息...")
        wcf2xml.wcf2xmlMain(self.site_info_file, self.site_info_file + "_xml")
        # self.logger.info(data._content)

        json_data = xml2json.data_from_xml_json(self.site_info_file + "_xml", Consts.SITE_ENTITY_TAG)
        for d in json_data:
            self.station_dict[d['stationcode']] = d['uniquecode']
            print(d['stationcode'] + "_" + d['uniquecode'])
        return self.station_dict


if __name__ == '__main__':
    siteInfoXml = SiteInfoXml()
    siteInfoXml.get_site_info()
