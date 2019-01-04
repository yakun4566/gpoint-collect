from configparser import ConfigParser


#初始化类
cp = ConfigParser()
cp.read("../resources/config.cfg")


#得到所有的section，以列表的形式返回
# section = cp.sections()[0]
# print(section)
#
# #得到该section的所有option
# print(cp.options(section))
#
# #得到该section的所有键值对
# print(cp.items(section))
#
# #得到该section中的option的值，返回为string类型
# print(cp.get(section, "ip_port"))
ip_port = cp._sections.get("remote_address").get("ip_port")
ip_port_arr= ip_port.split(",")
for address in ip_port_arr:
    print(address.split(":")[0])
    print(address.split(":")[1])

