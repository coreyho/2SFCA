from collections import namedtuple
import pandas as pd
from get_od import get_od

communities_file = '../data/人口/街道两实人口2015.csv'
hospital_file = '../data/养老/养老院.csv'
OD_file = '../data/计算结果/OD矩阵_街道_养老院.csv'
out_facilities = '../data/计算结果/养老院供需比.csv'
out_communities = '../data/计算结果/街道养老设施可达性.csv'


def f(x):
    if type(x) == str:
        x = int(x)
    if (type(x) == int) & (x > 0):
        if x >= 300:
            return '大型'
        elif x < 100:
            return '小型'
        else:
            return '中型'
    return None


'''读取数据'''

with open(communities_file, encoding='utf_8') as f1:
    communities = pd.read_csv(f1, index_col=0)

with open(hospital_file, encoding='utf_8') as f2:
    hospitals = pd.read_csv(f2, index_col=0)

od_pd = get_od(communities_file, hospital_file)
# od_pd.to_csv(OD_file)

hospitals['类型'] = hospitals['床位数'].map(f)
'''计算结果'''
# 大型养老机构
j_hospitals = hospitals[hospitals['类型'] == '大型']
# 选取小型养老机构
sq_hospitals = hospitals[hospitals['类型'] == '小型']
# 选取中型养老机构
pt_hospitals = hospitals[hospitals['类型'] == '中型']

# 小型养老机构OD矩阵
sq_od = od_pd.loc[:, sq_hospitals.index]
sq_od = sq_od.applymap(lambda x: x / 500 + 5)
# 大型养老机构OD矩阵
j_od = od_pd.loc[:, j_hospitals.index]
j_od = j_od.applymap(lambda x: x / 500 + 5)
# 中型养老机构OD矩阵
pt_od = od_pd.loc[:, pt_hospitals.index]
pt_od = pt_od.applymap(lambda x: x / 500 + 5)

od_pd = pd.merge(sq_od, j_od, left_index=True, right_index=True)
od_pd = pd.merge(od_pd, pt_od, left_index=True, right_index=True)
Threshold = namedtuple('Threshold', ['大型', '中型', '小型'])
threshold = Threshold(120, 60, 30)
columnslist = hospitals.columns.tolist().append('供需比')
hospitals.reindex(columns=columnslist)
for index in hospitals.index:
    vj = 0
    vij = 0
    if hospitals.loc[index, '类型'] == '大型':
        this_threshold = threshold.大型
    elif hospitals.loc[index, '类型'] == '中型':
        this_threshold = threshold.小型
    else:
        this_threshold = threshold.中型
    communities_id = od_pd.loc[:, index]
    communities_id = communities_id[communities_id < this_threshold].index.tolist()
    if len(communities_id) == 0:
        hospitals.loc[index, '供需比'] = 0
        continue
    for index2 in communities_id:
        vij = communities.loc[index2, 'AGE_60及上'] * (od_pd.loc[index2, index] ** (-1))
        vj += vij
    r = hospitals.loc[index, '床位数'] / vj
    hospitals.loc[index, '供需比'] = r

columnslist = communities.columns.tolist()
columnslist.extend(['大型可达性', '中型可达性', '小型可达性', '可达性'])
communities.reindex(columns=columnslist)
for index in communities.index:
    '''计算大型养老设施可达性'''
    mi = 0
    hospital_id = j_od.loc[index, :]
    hospital_id = hospital_id[hospital_id < threshold.大型].index.tolist()
    for index2 in hospital_id:
        mij = hospitals.loc[index2, '供需比'] * (od_pd.loc[index, index2] ** (-1))
        mi += mij
    communities.loc[index, '大型可达性'] = mi * 1000

    '''计算普通医院可达性'''
    mi = 0
    hospital_id = pt_od.ix[index, :]
    hospital_id = hospital_id[hospital_id < threshold.中型].index.tolist()
    for index3 in hospital_id:
        mij = hospitals.loc[index3, '供需比'] * (od_pd.loc[index, index3] ** (-1))
        mi += mij
    communities.loc[index, '中型可达性'] = mi * 1000
    '''计算卫生服务中心可达性'''
    mi = 0
    hospital_id = sq_od.ix[index, :]
    hospital_id = hospital_id[hospital_id < threshold.小型].index.tolist()
    for index4 in hospital_id:
        mij = hospitals.loc[index4, '供需比'] * (od_pd.loc[index, index4] ** (-1))
        mi += mij
    communities.loc[index, '小型可达性'] = mi * 1000

    communities['可达性'] = communities['大型可达性'] + communities['中型可达性'] + communities['小型可达性']

hospitals.to_csv(out_facilities)
communities.to_csv(out_communities)
