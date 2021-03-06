#-*- coding:utf-8 -*-

# 传入地点和城市，返回含有地点的经纬度的dict
import requests


def geocoding_baidu(address, city):
    request_url = 'http://api.map.baidu.com/geocoder/v2/?ak=HAlmjEeWoe9FwN0u6pmqSZiYuXpmaDuV&output=json&address='+address+'&city='+city
    response = requests.get(request_url)
    if response.status_code == 200:
        status = response.json().get('status')
        if status == 0:
            return response.json()
        else:
            return None
    else:
        return None

if __name__ == '__main__':
    townstr = '41142200001300001##睢县寥堤乡,41142200001300002##睢县尚屯乡,41142200001300003##睢县董店乡,41142200001300004##睢县西陵寺镇,41142200001300005##睢县涧岗乡,41142200001300006##睢县尤吉屯乡,41142100001300001##民权县王庄寨镇,41142100001300002##民权县程庄镇,41142100001300003##民权县胡集乡,41142100001300004##民权县白云寺镇,41142100001300005##民权县双塔镇,41142100001300006##民权县野岗镇,41142100001300007##民权县王桥镇,41142100001300008##民权县颜集乡,41142100001300009##民权县龙塘镇,41142100001300010##民权县孙六镇,41142100001300011##民权县庄子镇,41142100001300012##民权县北关镇,41142100001300013##民权县伯党乡,41142100001300014##民权县花园乡,41142100001300015##民权县林七乡,41142100001300016##民权县人和镇,41142100001300017##民权县褚庙乡,41142300001300006##宁陵县刘楼乡,41142300001300007##宁陵县华堡镇,41142300001300008##宁陵县程楼乡,41142300001300010##宁陵县黄岗镇,41140200001300003##双八镇,41140200001300004##长征办事处,41140200001300002##王楼乡,41140200001300005##孙福集镇,41140200001300006##解放办事处,41140200001300007##观塘乡,41140200001300008##建设办事处,41140200001300009##刘口乡,41140200001300010##水池铺,41140200001300011##李庄乡,41140200001300012##谢集乡,41140300001300001##新城办事处,41140300001300002##文化办事处,41140300001300003##宋城办事处,41140300001300004##东方办事处,41140300001300005##古城办事处,41140300001300006##郭村镇,41140300001300007##宋集镇,41140300001300008##高辛镇,41140300001300009##李口镇,41140300001300010##路河镇,41140300001300011##冯桥镇,41140300001300012##闫集镇,41140300001300013##坞墙镇,41140300001300014##毛堌堆镇,41140300001300015##包公庙乡,41140300001300016##勒马乡,41140300001300017##临河店乡,41140300001300018##楼店乡,41142600001300001##车站镇,41142600001300002##火店镇,41142600001300003##北岭镇,41142600001300004##太平镇,41142600001300005##会亭镇,41142600001300006##韩道口镇,41142600001300007##杨集镇,41142600001300008##济阳镇,41142600001300009##罗庄镇,41142200001300013##河集乡,41142200001300014##长岗镇,41142200001300015##后台乡,41142200001300016##匡城乡,41142200001300017##孙聚寨乡,41142200001300018##潮庄镇'

    str_arr = townstr.split(",")
    for town in str_arr:
        sitecode = town.split("##")[0]
        sitename = town.split("##")[1]
        lng_lat = geocoding_baidu(sitename, "商丘市")
        if None is not lng_lat:
            lng = lng_lat.get('result').get("location").get("lng")
            lat = lng_lat.get('result').get("location").get("lat")
            sql = "update m_site t set t.longitude="+str(lng)[0:10]+", t.latitude="+str(lat)[0:9]+" where t.sitecode='"+sitecode+"'"
            print(sql)