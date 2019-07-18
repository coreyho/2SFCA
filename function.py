from urllib.request import urlopen
import json
import math


def coords_conv(log, lat):  # 经度在前，纬度在后
    coord = str(log) + ',' + str(lat)
    url1 = 'http://api.map.baidu.com/geoconv/v1/?coords='
    url2 = '&from=1&to=5&ak='
    ak = 'EOOqf3R5SQvBdHfKMgoSzNeuBRTWh7Xv'
    uri = url1 + str(coord) + url2 + ak
    req = urlopen(uri)
    res = req.read().decode()
    temp = json.loads(res)
    if temp['status'] == 0:
        log = temp['result'][0]['x']
        lat = temp['result'][0]['y']
        return log, lat
    return 0


def getduration(log1, lat1, log2, lat2):  # 纬度在前，经度在后
    origin = str(lat1) + ',' + str(log1)
    destination = str(lat2) + ',' + str(log2)
    url = 'http://api.map.baidu.com/routematrix/v2/driving?output=json'
    ak = 'EOOqf3R5SQvBdHfKMgoSzNeuBRTWh7Xv'
    uri = url + '&origins=' + origin + '&destinations=' + destination + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode()
    temp = json.loads(res)
    if temp['status'] == 0:
        distance = temp['result']['distance'][0]['value']
        duration = temp['result']['duration'][0]['value']
        return distance, duration
    return 0


def cal_distance(log1, lat1, log2, lat2):
    dy = log1 - log2  # 经度差值

    dx = lat1 - lat2  # 纬度差值

    b = (lat1 + lat2) / 2.0  # 平均纬度

    lx = math.radians(dy) * 6367000.0 * math.cos(math.radians(b))  # 东西距离

    ly = 6367000.0 * math.radians(dx)  # 南北距离
    return math.sqrt(lx * lx + ly * ly)  # 用平面的矩形对角距离公式计算总距离
