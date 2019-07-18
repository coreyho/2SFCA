# -*- coding: utf-8 -*-
import re
import pandas as pd
import math


def strtoint(x):
    return int(x)


def getnum(inputstr):
    if inputstr != inputstr:
        return 0
    if isinstance(inputstr, int):
        return inputstr
    thesum = sum(map(strtoint, re.findall(r"\d+\.?\d*", inputstr)))
    return thesum


def getgrade(str):
    if str != str:
        return ""
    a_1 = ""
    for i in str:
        if i not in a_1:
            a_1 += i
    return a_1


with open('F:/2017武汉地理国情论文/主城区医疗卫生属性.csv', encoding='utf-8') as f:
    raw_data = pd.read_csv(f, dtype='str', encoding='utf-8')
    raw_data['床位（牙椅）数'] = raw_data['床位（牙椅）数'].map(getnum)
    raw_data['执业医师数（助理医师）'] = raw_data['执业医师数（助理医师）'].map(getnum)
    raw_data['注册护士数'] = raw_data['注册护士数'].map(getnum)
    raw_data['等级'] = raw_data['等级'].map(getgrade)
    raw_data.to_csv('F:/2017武汉地理国情论文/主城区医疗卫生属性处理之后.csv', encoding='Gbk')
