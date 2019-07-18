# -*- coding=utf-8 -*-
import pandas as pd
import numpy as np
import math


def cal_distance(log1, lat1, log2, lat2):
    dy = log1 - log2  # 经度差值

    dx = lat1 - lat2  # 纬度差值

    b = (lat1 + lat2) / 2.0  # 平均纬度

    lx = math.radians(dy) * 6367000.0 * math.cos(math.radians(b))  # 东西距离

    ly = 6367000.0 * math.radians(dx)  # 南北距离
    return math.sqrt(lx * lx + ly * ly)  # 用平面的矩形对角距离公式计算总距离


def get_od(path_o, path_d, endoding='utf-8'):
    with open(path_o, encoding=endoding) as f:
        o_data = pd.read_csv(f, encoding='utf-8')

    with open(path_d, encoding=endoding) as f:
        d_data = pd.read_csv(f, encoding='utf-8')

    o_coords = o_data[['OBJECTID', 'x', 'y']]
    d_coords = d_data[['OBJECTID', 'x', 'y']]

    distance = []
    for index2, row2 in o_coords.iterrows():
        for index1, row1 in d_coords.iterrows():
            dis = cal_distance(row1['x'], row1['y'], row2['x'], row2['y'])
            distance.append(dis)
    index_num = len(o_coords)
    column_num = len(d_coords)
    distances = np.array([distance]).reshape(index_num, column_num)
    index = [i + 1 for i in range(index_num)]
    column = [i + 1 for i in range(column_num)]
    pd_distance = pd.DataFrame(distances, index=index, columns=column)
    return pd_distance
