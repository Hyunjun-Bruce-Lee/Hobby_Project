import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
import pickle
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import geopandas as gpd

## 동별 지리정보 로드 pop파일 기준 ###
with open('C:/Users/HyunJun/Desktop/Final_PJ/pop_final1011.bin', 'rb') as f:
    base_gubun = pickle.load(f)

## 지도로 완전한지 확인
base_gubun = gpd.GeoDataFrame(base_gubun, geometry = 'geometry')
base_gubun.crs = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"

fig, ax = plt.subplots(figsize=(16,16))
base_gubun.plot(ax=ax, color='lightgray', edgecolor='grey', linewidth=0.4)

## 동별 지리정보만 있는 베이스 파일 생성 ##
base_gubun.keys()
base_gubun = base_gubun[['GU_CD', 'GU_NM', 'ADM_DR_CD', 'ADM_DR_NM', 'geometry', 'centroid']]
base_gubun.rename(columns = {'ADM_DR_CD':'DONG_CD', 'ADM_DR_NM':'DONG_NM'}, inplace = True)
## 구별 동별 이름으로 정렬 ##
base_gubun.sort_values(['GU_NM','DONG_NM'],inplace = True)
base_gubun.reset_index(inplace = True)
## 인덱스 재설정
base_gubun.drop(['index'], axis = 1, inplace = True)

## geo_score_final 기준으로 동별인구수, 거리 병합
with open('C:/Users/HyunJun/Desktop/Final_PJ/Final_PJ/메추라기/Final_PJ/geo_score_final.bin', 'rb')as f:
    geo = pickle.load(f)

geo.rename(columns = {'ADM_DR_CD':'DONG_CD', 'ADM_DR_NM':'DONG_NM'}, inplace = True)
geo.sort_values(['GU_NM','DONG_NM'],inplace = True)
geo.reset_index(inplace = True)
geo.drop(['index'], axis = 1, inplace = True)

## 배열 일치 확인
for i in range(424):
    if base_gubun.loc[i, 'DONG_NM'] != geo.loc[i,'DONG_NM']:
        print(i)

## 병합
base_gubun['GEO'] = geo['GEO_DIST']
base_gubun['TOTAL_POP'] = geo['pop']



## amt_final import 확인
with open('C:/Users/HyunJun/Desktop/Final_PJ/새 폴더/amt_final.bin', 'rb') as f:
    amt = pickle.load(f)

## 재정렬
amt.sort_values(['GU_NM','DONG_NM'],inplace = True)
## 인덱스 초기화
amt.reset_index(inplace = True)
amt.drop(['index'], axis = 1, inplace = True)
## 배열 일치 확인
for i in range(424):
    if base_gubun.loc[i, 'DONG_NM'] != amt.loc[i,'DONG_NM']:
        print(i)

## poor, rate 병합
base_gubun['POOR'] = amt['poor']
base_gubun['INCOME_RATE'] = amt['rate']

### BLUE SCORE 확인
blue = pd.read_csv('C:/Users/HyunJun/Desktop/Final_PJ/새 폴더/blues_index(임시).csv')
gu_list = list(blue['구'])

base_gubun['BLUE'] = np.zeros((len(base_gubun), 1))
for i in gu_list:
    temp_list = list(base_gubun[base_gubun['GU_NM']== i].index)
    for j in temp_list:
        base_gubun.loc[j,'BLUE'] = blue.loc[blue['구'] == i, 'idx'].item()


### alone data 확인
with open('C:/Users/HyunJun/Desktop/Final_PJ/새 폴더/alone_final.bin', 'rb') as f:
    alone = pickle.load(f)

alone.sort_values(['GU_NM','DONG_NM'],inplace = True)
alone.reset_index(inplace = True)
alone.drop(['index'], axis = 1, inplace = True)  

for i in range(424):
    if base_gubun.loc[i, 'DONG_NM'] != alone.loc[i,'DONG_NM']:
        print(i)

base_gubun['ALONE_CNT'] = alone['CNT']

base_gubun = gpd.GeoDataFrame(base_gubun, geometry = 'geometry')
base_gubun.crs = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"

fig, ax = plt.subplots(figsize=(16,16))
base_gubun.plot(ax=ax, color='lightgray', edgecolor='grey', linewidth=0.4)

with open('C:/Users/HyunJun/Desktop/Final_PJ/BASE_FINAL(10_14).bin', 'wb') as f:
    pickle.dump(base_gubun, f)
    
## parmacy
with open('C:/Users/HyunJun/Desktop/Final_PJ/Final_PJ/새 폴더/pharmacy_8m.pickle', 'rb') as f:
    paramcy_8 = pickle.load(f)
with open('C:/Users/HyunJun/Desktop/Final_PJ/Final_PJ/새 폴더/pharmacy_9m.pickle', 'rb') as f:
    paramcy_9 = pickle.load(f)
with open('C:/Users/HyunJun/Desktop/Final_PJ/Final_PJ/새 폴더/pharmacy_10m.pickle', 'rb') as f:
    paramcy_10 = pickle.load(f)

### 8월
not_inc_8 = list()
for i in list(base_gubun['DONG_NM']):
    if i in list(paramcy_8['dong']):
        continue
    else:
        not_inc_8.append(i)

for i in list(paramcy_8['dong']):
    if '.' in i:
        paramcy_8.loc[paramcy_8['dong']==i, 'dong'] = i.replace('.','·')


##### 9월
not_inc_9 = list()
for i in list(base_gubun['DONG_NM']):
    if i in list(paramcy_9['dong']):
        continue
    else:
        not_inc_9.append(i)

for i in list(paramcy_9['dong']):
    if '.' in i:
        paramcy_9.loc[paramcy_9['dong']==i, 'dong'] = i.replace('.','·')

##### 10월
not_inc_10 = list()
for i in list(base_gubun['DONG_NM']):
    if i in list(paramcy_10['dong']):
        continue
    else:
        not_inc_10.append(i)

for i in list(paramcy_10['dong']):
    if '.' in i:
        paramcy_10.loc[paramcy_10['dong']==i, 'dong'] = i.replace('.','·')
        
        
### 종합 확인
len(not_inc_8)
len(not_inc_9)
len(not_inc_10)


not_inc_8_9 = list()
for i in not_inc_8:
    if i in not_inc_9:
        not_inc_8_9.append(i)

not_inc_9_10 = list()
for i in not_inc_9:
    if i in not_inc_10:
        not_inc_9_10.append(i)

not_inc_10_8 = list()
for i in not_inc_10:
    if i in not_inc_8:
        not_inc_10_8.append(i)

not_inc_8_9
not_inc_9_10
not_inc_10_8

for i in not_inc_8:
    if i not in not_inc_8_9:
        print(i)

paramcy_10.groupby(['gu']).sum()
paramcy_10[paramcy_10['gu'] == '강남구']

temp_dict = dict()
for i in list(paramcy_9['gu'].unique()):
    temp_list = list(paramcy_9.loc[paramcy_9['gu'] == i, 'dong'].index)
    avg = paramcy_9.loc[temp_list, 'count'].mean()
    temp_dict[i] = round(avg) 

paramcy_9.keys()
paramcy_10.drop(['gov_code','age'], axis = 1, inplace = True)

## 장위3동 8월 에만 추가

gu = '중구'
dong = '장충동'
count =  12312
appending_dict = {'gu': gu,'dong': dong,'count':count}
paramcy_8 = paramcy_8.append(appending_dict, ignore_index = True)
paramcy_9 = paramcy_9.append(appending_dict, ignore_index = True)
paramcy_10 = paramcy_10.append(appending_dict, ignore_index = True)

paramcy_8.sort_values(['gu','dong'],inplace = True)
paramcy_9.sort_values(['gu','dong'],inplace = True)
paramcy_10.sort_values(['gu','dong'],inplace = True)

parmacy = round((paramcy_8['count'] + paramcy_9['count'] + paramcy_10['count'])/3)

base_gubun['PARMACY_ACT'] =  parmacy
base_gubun['PARMACY'] = base_gubun['PARMACY_ACT']/base_gubun['TOTAL_POP']

base_gubun[base_gubun['DONG_NM'] == '둔촌1동'].index
base_gubun.drop(26, axis = 0, inplace = True)

base_gubun['POOR_RATE'] = base_gubun['POOR']/base_gubun['TOTAL_POP']
base_gubun['ALONE_RATE'] = base_gubun['ALONE_CNT']/base_gubun['TOTAL_POP']

base_gubun.drop(['INCOME_RATE'], axis = 1, inplace = True)

with open('C:/Users/HyunJun/Desktop/Final_PJ/BASE_FINAL(10_14).bin', 'wb') as f:
    pickle.dump(base_gubun, f)
