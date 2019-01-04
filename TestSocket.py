#-*- coding:utf-8 -*-
import json

import schedule
import time

import GpointCollect


def test_socket():
    send_data_json = {}
    send_data_json['appId'] = 'datacollect'
    send_data_json['appKey'] = '123456789'
    send_data_json['datatype'] = 'GPOINTAIR'
    send_data_json['datakind'] = 'HourData'
    send_data_json['data'] = []
    gc = GpointCollect.GpointCollectAQI()
    gc.send_socket(json.dumps(send_data_json))
if __name__ == '__main__':
    test_socket()
    schedule.every(0.5).minutes.do(test_socket)

    while True:
        schedule.run_pending()
        time.sleep(1)