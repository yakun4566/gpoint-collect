import json
import os

import arrow
import GpointCollect

def testArrow():
    now = arrow.now()

    now = now.shift(hours=-2)
    print(now.format("YYYY-MM-DD HH:00:00"))


def printSite():
    gc = GpointCollect.GpointCollectAQI()
    # gc.get_site_info_xml()
    site_info = gc.get_site_info()
    for site in site_info:
        print(site + ":" + site_info[site])

    pass
if __name__ == '__main__':
    today = arrow.now().format("YYYYMMDD")
    print(os.getcwd())
    path = os.getcwd() + os.sep + "data" + os.sep + today
    if not os.path.exists(path):
        os.makedirs(path)