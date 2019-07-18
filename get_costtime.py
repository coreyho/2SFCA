from urllib.parse import quote
from urllib import request
from urllib import error
import xlwt
import json
import time
import random
import sys
from get_amap_poi import get_content

amap_web_key = '61766215afdf457d3e7cfd1fe13396cc'
coordinate_convert_url = "restapi.amap.com/v3/assistant/coordinate/convert?key=" + amap_web_key
direction_url = "restapi.amap.com/v3/direction/driving?key=" + amap_web_key


def coordinate_convert(lng, lat=None):
    '''

    :param lng: 经度（如只有一个输入参数，则为经纬度列表或字符串）
    :param lat: 纬度
    :return: 经纬度字符串如'116.487585177952,39.991754014757'
    '''
    if lat == None:
        if type(lng) == list:
            lat = float(lng[1]) if type(lng[1] == str) else lat = lng[1]
            lng = float(lng[0]) if type(lng[0] == str) else lng = lng[0]
        if type(lng) == str:
            lng = str.split(',')[0]
            lat = str.split(',')[1]
        else:
            return error
    url = coordinate_convert_url + '&locations=' + str(lng) + ',' + str(lat) + '&coordsys=gps'
    coord_json = json.loads(get_content(url).decode('utf-8'))
    if coord_json['status'] != 0:
        return error
    return coord_json['locations']


def get_cost(origin, *tujingd,destination):
    '''

    :param origin:起始地点的坐标，示例'116.487585177952,39.991754014757'
    :param destination:终点的坐标，示例'116.434446,39.90816'
    :return:行驶距离，耗费时间
    '''
    origin = coordinate_convert(origin)
    destination = coordinate_convert(destination)
    url = direction_url + '&origin=' + origin + '&destination=' + destination + '&extensions=base&strategy=0'
    cost = json.loads(get_content(url).decode('utf-8'))
    return cost['roote']['paths']['0']['distance'], cost['roote']['paths']['0']['duration']
