#!/usr/bin/env python
# -*- coding:utf-8 -*-

# RabbitMQ类的初始化参数，包括broker_ip, port, username, password, vhost
from rabbit.RabbitMQ import RabbitMQ

args = ("123.160.220.40", 5627, "producer_country_aqi", "producer_country_aqi", "/")
mq = RabbitMQ(*args)  # 传入初始化参数
mq.connect()   # 调用connect方法，连接broker

# 调用put方法，向目标queue中发送数据， 第一个参数是data, 第二个参数是queue_name, 第三个参数是route_name
mq.put("111111111111111", "COUNTRY_CITY_AQI", "COUNTRY_CITY_AQI")

# 发完数据，主动关闭连接
mq.close()