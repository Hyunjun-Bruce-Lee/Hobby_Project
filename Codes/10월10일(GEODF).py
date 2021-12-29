import geopandas as gpd
import matplotlib.pyplot as plt

geodf = gpd.read_file('C:/Users/user/Desktop/Final_PJ/EMD_202005/EMD.shp', encoding = 'euc-kr')

geodf.keys()

geodf['EMD_KOR_NM']
E
## 서울 추출
geodf = geodf[geodf['EMD_CD'].astype(int) <= 11999999]

geodf
geodf.plot(figsize=(16,8))

## 좌표계 설정
geodf = geodf.to_crs('EPSG:5186')


geodf_moonhwa = gpd.read_file('C:/Users/user/Desktop/Final_PJ/문화체육시설/문화체육시설.shp', encoding = 'euc-kr')
geodf_moonhwa = geodf_moonhwa.set_crs('WGS84')
#geodf_moonhwa= geodf_moonhwa.to_crs('EPSG:5186')
geodf_moonhwa= geodf_moonhwa.to_crs('EPSG:4326')


fig, ax = plt.subplots(figsize=(16,16))
geodf.plot(ax=ax, color='lightgray', edgecolor='grey', linewidth=0.4)
geodf_moonhwa.plot(ax=ax, color='#07424A', alpha=0.7, markersize=1000)


import pandas as pd
import numpy as np
import pickle
import fiona

with open('C:/Users/user/Desktop/Final_PJ/센터동별cnt.bin', 'rb') as f:
    moonhwa_cnt = pickle.load(f)

moonhwa = pd.read_csv('C:/Users/user/Desktop/Final_PJ/문화체육시설.csv')
moonhwa.keys()

list(moonhwa_cnt.index)
list(geodf['EMD_KOR_NM'].unique())


with open('C:/Users/user/Desktop/Final_PJ/base.bin', 'rb') as f:
    base = pickle.load(f)

    
base['DONG_NM']



not_in_geo = list()
for i in list(moonhwa_cnt.index):
    if i in list(geodf['EMD_KOR_NM'].unique()):
        continue
    not_in_geo.append(i)


moonhwa_cnt['성수1가1동']

len(list(moonhwa_cnt.index))
len(not_in_geo)

len(list(geodf['EMD_KOR_NM']))

geodf

list(geodf['EMD_KOR_NM'])

'고덕동' in list(moonhwa_cnt.index)
'창신1동' in list(geodf['EMD_KOR_NM'])



fix_dong = {'성수1가': '성수동1가',
            '성수1가1동':'성수동1가',
            '대학동': '신림동',
            '창4동' : '창동',
            '낙성대동': '봉천동',
            '미성동' : '신림동',
            '목1동' : '목동',
            '번2동' : '번동',
            '중계1동' : '중계동' ,
            '독산4동' : '독산동',
            '망우본동' : '망우동',
            '등촌3동' : '등촌동',
            '문래동' : '문래동3가',
            '역삼1동' : '역삼동',
            '서초4동' : '서초동',
            '고척2동' : '고척동',
            '역삼2동' : '역삼동',
            '금호2가' : '금호동2가',
            '면목4동' : '면목동',
            '면목7동' : '면목동',
            '목5동' : '목동',
            '시흥2동' : '시흥동',
            '개포2동' : '개포동',
            '반포2동' : '반포동',
            '봉천본동' : '봉천동',
            '개봉3동' : '개봉동',
            '상계10동' : '상계동',
            '구로2동' : '구로동',
            '가양1동' : '마곡동',
            '창5동' : '창동',
            '고덕1동' : '고덕동',
            '시흥1동' : '시흥동',
            '면목2동' : '면목동',
            '구로5동' : '구로동',
            '천호1동' : '천호동',
            '중계4동' : '중계동',
            '공릉2동' : '공릉동',
            '도봉1동' : '도봉동',
            '화곡8동' : '화곡동',
            '암사2동' : '암사동',
            '방화3동' : '방화동',
            '이문2동' : '이문동',
            '조원동' :'신림동', 
            '대림3동' : '대림동',
            '마천1동' : '마천동',
            '자양4동' : '자양동',
            '화곡6동' : '화곡동',
            '홍은1동' : '홍은동',
            '시흥3동' : '시흥동',
            '노량진2동' : '노량진동',
            '월계2동' : '월계동',
            '화곡4동' : '화곡동',
            '중계본동' : '중계동',
            '대치4동' :'대치동',
            '독산3동' : '독산동',
            '명일1동': '명일동',
            '일원1동' : '일원동',
            '남가좌2동': '남가좌동',
            '신월4동' : '신월동',
            '신대방2동': '신대방동',
            '신정4동' : '신정동',
            '홍은2동' : '홍은동',
            '화곡3동' : '화곡동',
            '창1동' : '창동',
            '도봉2동' : '도봉동',
            '아현' : '아현동',
            '신정6동' : '신정동',
            '상도2동' : '상도동',
            '신월1동' : '신월동',
            '신월5동' : '신월동',
            '성수동' : '성수동1가',
            '삼양동' : '미아동',
            '잠실3동' : '잠실동'}

list(moonhwa['동'].unique())

moonhwa[moonhwa['동'] == '잠실3동']

moonhwa.loc[moonhwa['동'] == '잠실3동', '동'] = '잠실3동'

moonhwa.to_csv('C:/Users/user/Desktop/Final_PJ/문화체육시설(법정동).csv')


fix_dong['잠실3동'].

for i in list(fix_dong.keys()):
    if i in list(moonhwa['동'].unique()):
        moonhwa.loc[moonhwa['동'] == i, '동'] = fix_dong[i]
        
moonhwa_cnt = pd.value_counts(moonhwa['동'].values)

list(moonhwa_cnt.index)
step1 = geodf[['EMD_KOR_NM','geometry']]
step1['CNT'] = np.zeros((len(step1),1))

moonhwa_cnt['가산동']

step1.loc[step1['EMD_KOR_NM']=='가산동', 'CNT']

for i in list(moonhwa_cnt.index):
    step1.loc[step1['EMD_KOR_NM']==i, 'CNT'] = moonhwa_cnt[i]

with open('C:/Users/user/Desktop/Final_PJ/문화센터개수(좌표포함).bin', 'wb') as f:
    pickle.dump(step1, f)
    
    


import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable
%matplotlib inline
mpl.rc('font', family='NanumGothic')
plt.rcParams["figure.figsize"] = (30,30)



step1[step1['EMD_KOR_NM'] == '공릉동']
step1.loc[step1['EMD_KOR_NM'] == '공릉동', 'CNT'] = 17-12


fig, ax = plt.subplots(1, 1)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
column = 'CNT'
#step1.plot(column, ax=ax, legend=True, cax=cax, cmap='OrRd')
step1.plot(column, ax=ax, legend=True, cax=cax, cmap='rainbow')
ax.set_title("서울시 문화시설 밀집도")
ax.set_axis_off()
plt.show()


fig, ax = plt.subplots(figsize=(16,16))
geodf.plot(ax=ax, color='lightgray', edgecolor='grey', linewidth=0.4)
geodf_moonhwa.plot(ax=ax, color='#07424A', alpha=0.7, markersize=1000)


### geo_score 가안 ###
## area = 면적
## center = 센터 수
area_score = (area - min(area))/(max(area) - min(area)) # 면적 정규화
center_score = (center - min(center))/(max(center) - min(center)) # 센터수 정규화
# 면적 = 200m^3 (면적 min = 0, max = 1000)
# 센터수 = 20개 (개수 min = 0, max = 100)

# 0~1

# Min_Max(면적) = (200 - 0)/(1000 - 0) = 0.5
# Min_Max(센터) = (20 - 0)/(100 - 0) = 0.5



geo_score = 1 - (area_score/center_score)
# 0에 가까울수록 문제없음
# 음수는 센터가 너무 많은
# 양수는 센터가 너무 없음
# A(area: 0.9, center:0.3)   /   B(area: 0.3, center:0.2)   /   C(area: 0.3, center:0.8) 
# ex) A(geo_score) = 2, B(geo_score) = 0.5, C(geo_score) = 0.-825
# A는 센터수가 너무 적다
# B는 적절하다고 판단.
# C는 센터 수가 너무 많다




living = gpd.read_file('C:/Users/user/Desktop/Final_PJ/서울시_주거지역_위치정보/서울시_주거지역_위치정보.shp', encoding = 'euc-kr')

living['위도']
living['경도']



fig, ax = plt.subplots(1, 1)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
column = 'CNT'
step1.plot(column, ax=ax, legend=True, cax=cax, cmap='OrRd')
ax.set_title("서울시 문화시설 밀집도")
ax.set_axis_off()
plt.show()


with open('C:/Users/user/Desktop/Final_PJ/수급자.bin', 'rb') as f:
    amt = pickle.load(f)
    
amt.keys()
amt['`RSPOP_CNT`']

len(list(amt['`ADMI_NM`']))


not_in_geo = list()
for i in list(amt['`ADMI_NM`']):
    if i in list(temp['ADM_DR_NM']):
        continue
    not_in_geo.append(i)
    
len(not_in_geo)

'망우3동' in list(geodf['EMD_KOR_NM'])

len(list(geodf['EMD_KOR_NM']))


### 동별 인구 시각화
temp = gpd.read_file('C:/Users/user/Desktop/Final_PJ/새 폴더 - 복사본/seoul_neighborhoods.shp')

### 지도 베이스 (424개동)
with open('C:/Users/user/Desktop/Final_PJ/법정동.bin', 'rb') as f:
    temp = pickle.load(f)
    
for i in not_in_geo:
    if i in list(amt['`ADMI_NM`']):
        amt.loc[amt['`ADMI_NM`']==i, '`ADMI_NM`'] = i.replace('.','·')
        
not_in_geo = list()
for i in list(amt['`ADMI_NM`']):
    if i in list(temp['ADM_DR_NM']):
        continue
    not_in_geo.append(i)

len(amt['`ADMI_NM`'])
len(amt['`ADMI_NM`'].unique())
pd.value_counts(amt['`ADMI_NM`'].values)
pop = temp[['ADM_DR_CD','ADM_DR_NM','geometry']]
ttt = list(pop['ADM_DR_NM'].unique())
ttt.remove('신사동')

pop['pop'] = np.zeros((len(pop),1))
for i in ttt:
    pop.loc[pop['ADM_DR_NM'] == i, 'pop'] = amt.loc[amt['`ADMI_NM`'] == i, '`RSPOP_CNT`'].item()


amt.loc[amt['`ADMI_NM`'] == '신사동', :]

pop[pop['ADM_DR_NM'] == '신사동']

pop.loc[325,'pop'] = 23079
pop.loc[354, 'pop'] = 17639


## 325 = 관악구
pd.set_option('display.max_columns', None)
temp[temp['ADM_DR_NM'] == '신사동']


fig, ax = plt.subplots(1, 1)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
column = 'pop'
pop.plot(column, ax=ax, legend=True, cax=cax, cmap='OrRd')
ax.set_title("인구밀집도")
ax.set_axis_off()
plt.show()


### 

list(moonhwa_cnt.index)

step1.keys()
list(step1['EMD_KOR_NM'])
pop.keys()
list(pop['ADM_DR_NM'])


not_in_geo = list()
for i in list(moonhwa_cnt.index):
    if i in list(pop['ADM_DR_NM']):
        continue
    alpha = list(moonhwa.loc[moonhwa['동'] == i, '콘텐츠명'])
    not_in_geo.extend(alpha)
    
len(not_in_geo)
len(list(pop['ADM_DR_NM']))
len(list(moonhwa_cnt.index))

pd.DataFrame(not_in_geo).to_csv('C:/Users/user/Desktop/Final_PJ/노가다.csv')


in_geo = list()
for i in list(moonhwa_cnt.index):
    if i in list(pop['ADM_DR_NM']):
        in_geo.append(i)
len(in_geo)

117+118
len(moonhwa_cnt)


'서초3동' in list(pop['ADM_DR_NM'])
'서초동' in list(moonhwa['동'])
moonhwa.loc[113,:]


moonhwa.loc[moonhwa['동']=='서초동', :]

'오륜동' in list(pop['ADM_DR_NM'])
    
beta = list(pop['ADM_DR_NM'])

with open('C:/Users/user/Desktop/Final_PJ/pop보유동list.bin', 'wb') as f:
    pickle.dump(beta, f)


alpha2 = moonhwa[moonhwa['콘텐츠명'].isin(not_in_geo)].reset_index()
alpha2.to_csv('C:/Users/user/Desktop/Final_PJ/노가다data.csv', encoding = 'utf-8-sig')


aaa = pd.read_csv('C:/Users/user/Desktop/Final_PJ/노가다data_fin.csv')

nogada = pd.read_csv('C:/Users/user/Desktop/Final_PJ/노가다 - 노가다.csv', names = ['index', 'name', 'dong'])

beta = pd.value_counts(nogada['dong'].values)

for i in list(nogada['name'].unique()):
    check = list(nogada.loc[nogada['name']==i,'dong'])
    if check == []:
        print('죠졋다')
    moonhwa.loc[moonhwa['콘텐츠명'] == i, '동'] = nogada.loc[nogada['name']==i,'dong'].item()

count = pd.value_counts(moonhwa['동'].values)

pop['center'] = np.zeros((len(pop),1))

for i in list(count.index):
    pop.loc[pop['ADM_DR_NM'] == i, 'center'] = count[i]


fig, ax = plt.subplots(1, 1)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
column = 'center'
pop.plot(column, ax=ax, legend=True, cax=cax, cmap='OrRd')
ax.set_title("센터")
ax.set_axis_off()
plt.show()

## A[인구/센터] + B{[X구내의 모든센터간 거리의 평균]/[구면적-녹지면적]}
###### A[인구/센터] + B[각 동별 중심에서 해당 구 내의 모든 센터간 거리] #######
## A,B = ?, ? (1:1, 2:1 ...)

## [X구내의 모든센터간 거리의 평균]/[구면적-녹지면적] = beta
## beta가 높을수록 bad

## 면적이 크면, 1단계 제일 넓은것 5단계 제일 작은것
## 1단계일떈 센터가 많으면서, 거리가 좁은거 가 좋은것 (면적 100, 센터 거리 개수 50)
## 5단계일땐 센터가 많으면서, 거리가 좁은거 가 좋은것 (면적 50, 센터 거리 개수 25)


## https://lovestudycom.tistory.com/entry/%EC%9C%84%EB%8F%84-%EA%B2%BD%EB%8F%84-%EA%B3%84%EC%82%B0%EB%B2%95
## 위도 경도 계산
with open('C:/Users/user/Desktop/Final_PJ/pop_final.bin', 'wb')as f:
    pickle.dump(pop, f)

with open('C:/Users/user/Desktop/Final_PJ/pop_final.bin', 'rb')as f:
    pop = pickle.load(f)

pop['geometry'] = pop['geometry'].set_crs('EPSG:5181')

pop['geometry'] = pop['geometry'].to_crs('EPSG:4326')

pop['centroid'] = pop['geometry'].centroid

with open('C:/Users/user/Desktop/Final_PJ/pop_final.bin', 'wb')as f:
    pickle.dump(pop, f)

with open('C:/Users/user/Desktop/Final_PJ/pop_final.bin', 'rb')as f:
    pop = pickle.load(f)
    
geodf_moonhwa = geodf_moonhwa.set_crs('WGS84')
geodf_moonhwa= geodf_moonhwa.to_crs('EPSG:4326')


fig, ax = plt.subplots(figsize=(16,16))
pop['geometry'].plot(ax=ax, color='gray', edgecolor='black', linewidth=0.4)
pop['centroid'].plot(ax=ax, color='#fb1cff', alpha=0.7, markersize=10)
geodf_moonhwa['geometry'].plot(ax=ax, color='#21e5ff', alpha=0.7, markersize=10)


pop['rp'] = pop['geometry'].representative_point()

fig, ax = plt.subplots(figsize=(16,16))
pop['geometry'].plot(ax=ax, color='lightgray', edgecolor='grey', linewidth=0.4)
pop['rp'].plot(ax=ax, color='#07424A', alpha=0.7, markersize=10)


