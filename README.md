#### 功能
1. 采集全国标准站AQI，并发送到端口(10.0.16.11:60009)；
2. 数据来源：中国环境监测总站 (http://www.cnemc.cn/)
3. 数据解析用到python-wcfbin (https://github.com/ernw/python-wcfbin) 中的wcf2xml.py

#### 部署
- 部署位置：10.0.16.11 /home/resources/Projects/gpoint-collect/gpoint-collect
- 运行sh bin/start.sh

