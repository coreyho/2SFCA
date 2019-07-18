from urllib.parse import quote
from urllib import request
from urllib import error
import xlwt
import json
import time
import random
import sys
from coordTransform_utils import gcj02_to_wgs84

amap_web_key = '61766215afdf457d3e7cfd1fe13396cc'
poi_search_url = "http://restapi.amap.com/v3/place/text"
# //restapi.amap.com/v3/place/text?key=您的key&keywords=地铁站&types=地铁站&city=武汉&children=&offset=20&page=1&extensions=all
poi_boundary_url = "https://ditu.amap.com/detail/get/detail"


# 根据城市名称和分类关键字获取poi数据
def getpois(adcode, keywords):
    i = 1
    poilist = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoi_page(adcode, keywords, i)
        result = json.loads(result)  # 将字符串转换为json
        if result['status'] == '0':
            print(result['info'])

            sys.exit()
        if result['count'] == '0':
            break
        hand(poilist, result)
        i = i + 1
        print("第" + str(i) + "页")
    return poilist


# 数据写入excel
def write_to_excel(poilist, cityname, classfield):
    # 一个Workbook对象，这就相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet(classfield, cell_overwrite_ok=True)
    # 第一行(列标题)
    sheet.write(0, 0, 'id')
    sheet.write(0, 1, 'name')
    sheet.write(0, 2, 'lng')
    sheet.write(0, 3, 'lat')
    sheet.write(0, 4, 'address')
    for i in range(len(poilist)):
        # 根据poi的id获取边界数据
        # bounlist = getDetail(poilist[i]['id'])
        # while (len(bounlist) < 4):
        # bounlist.append(0)
        # 每一行写入
        location = gcj02_to_wgs84(poilist[i]['location'].split(',')).split(',')
        sheet.write(i + 1, 0, poilist[i]['id'])
        sheet.write(i + 1, 1, poilist[i]['name'])
        sheet.write(i + 1, 2, location[0])
        sheet.write(i + 1, 3, location[1])
        sheet.write(i + 1, 4, poilist[i]['address'])

    # 最后，将以上操作保存到指定的Excel文件中
    book.save(r'd:\\' + cityname + classfield + '.xls')


# 将返回的poi数据装入集合返回
def hand(poilist, result):
    # result = json.loads(result)  # 将字符串转换为json
    pois = result['pois']
    for i in range(len(pois)):
        poilist.append(pois[i])


# 单页获取pois
def getpoi_page(cityname, types, page):
    req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&types=' + quote(
        types) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    data = ''
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data


# 根据id获取边界数据
def getDetail(id, sleeptime=60, times=0):
    print(id + '第' + str(1 + times) + '次')
    req_url = poi_boundary_url + "?id=" + id
    try:
        response = get_content(req_url)
    except error:
        time.sleep(sleeptime)
    data = response.decode('utf-8')
    detail_json = json.loads(data)  # 将字符串转换为json
    deep_list = []
    shape_list = []
    if detail_json['status'] != '1':
        if detail_json['status'] == '6':
            time.sleep(sleeptime)
            getDetail(id, sleeptime + random.randint(0, 30), times + 1)
        else:
            return [0, 0, 0, 0]

    if detail_json['data'].get('deep') != None:
        deep_list.append(detail_json['data']['deep']['area_total']) if detail_json['data']['deep'].get(
            'area_total') != None else deep_list.append(0)
        deep_list.append(detail_json['data']['deep']['volume_rate']) if detail_json['data']['deep'].get(
            'volume_rate') != None else deep_list.append(0)
    else:
        deep_list = [0, 0]

    if detail_json['data'].get('spec') != None:
        if detail_json['data']['spec'].get('mining_shape') != None:
            mining_json = detail_json['data']['spec']['mining_shape']
            shape_list.append(mining_json['area']) if mining_json.get('area') != None else shape_list.append(0)
            shape_list.append(mining_json['center']) if mining_json.get('center') != None else shape_list.append(0)
        else:
            shape_list = [0, 0]
    else:
        shape_list = [0, 0]

    return deep_list + shape_list


def get_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5478.400 QQBrowser/10.1.1550.400',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9'}
    req = request.Request(url=url, headers=headers)
    res = request.urlopen(req)
    data = res.read()
    return data


# 获取城市分类数据
cityname = "武汉"
types = "公园|广场|绿地"
pois = getpois(cityname, types)

# 将数据写入excel
write_to_excel(pois, cityname, '公园绿地广场')
print('写入成功')
