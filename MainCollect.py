# -*- coding:utf-8 -*-
import threading

import schedule
import time

import CityAQICollect
import GpointCollect
# schedule.logger = logger
from get_logger import get_logger

logger = get_logger()
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

if __name__ == '__main__':
    gc = GpointCollect.GpointCollectAQI()
    cac = CityAQICollect.CityAQICollect()

    # 启动时先采集一次数据

    gc.get_site_air_data()
    cac.get_city_hour_aqi()

    """
        定义定时任务
    """

    # 每1分钟执行一次小时站点数据AQI抓取
    schedule.every(1).minute.do(run_threaded, gc.get_site_air_data)
    # 每天1:10下载一次站点信息xml
    schedule.every().day.at("01:10").do(run_threaded, gc.get_site_info_xml)
    #
    schedule.every(1).minute.do(run_threaded, cac.get_city_hour_aqi)
    # 每天5:00采集城市日AQI数据
    schedule.every().day.at("05:00").do(run_threaded, cac.get_city_day_aqi)

    # 每隔一秒循环一次定义的任务
    for job in schedule.jobs:
        logger.info(str(job))
    while True:
        schedule.run_pending()
        time.sleep(1)




