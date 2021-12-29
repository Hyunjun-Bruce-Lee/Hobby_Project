import geopandas as gpd
import pandas as pd
import numpy as np
import math
import pickle


with open('C:/Users/user/Desktop/Final_PJ/pop_final.bin', 'rb')as f:
    pop = pickle.load(f)

geodf_moonhwa = gpd.read_file('C:/Users/user/Desktop/Final_PJ/문화체육시설/문화체육시설.shp', encoding = 'euc-kr')
geodf_moonhwa = geodf_moonhwa.set_crs('WGS84')
geodf_moonhwa= geodf_moonhwa.to_crs('EPSG:4326')

GU_CODE_DICT = {11230 :'강남구',11250 :'강동구',11090 :'강북구',11160 :'강서구',11210 :'관악구',11050 :'광진구',11170 :'구로구',
                11180 :'금천구',11110 :'노원구',11100 :'도봉구',11060 :'동대문구',11200 :'동작구',11140 :'마포구',11130 :'서대문구',11220 :'서초구',
                11040 :'성동구',11080 :'성북구',11240 :'송파구',11150 :'양천구',11190 :'영등포구',11030 :'용산구',11120 :'은평구',11010 :'종로구',
                11020 :'중구',11070 :'중랑구'}

pop['GU_CD'] = pop['ADM_DR_CD'].map(lambda x: x[:-2])
pop['GU_NM'] = pop['GU_CD'].map(lambda x: GU_CODE_DICT[int(x)])

pop.keys()
pop = pop[['GU_CD','GU_NM','ADM_DR_CD','ADM_DR_NM','geometry','centroid','pop','center']]

with open('C:/Users/user/Desktop/Final_PJ/pop_final.bin', 'wb')as f:
    pickle.dump(pop, f)

import matplotlib as mpl
%matplotlib inline
mpl.rc('font', family='NanumGothic')

def get_gu_map(x):
    GU = x
    temp = pop[pop['GU_NM'] == GU]
    temp2 = geodf_moonhwa[geodf_moonhwa['구'] == GU]
    fig, ax = plt.subplots(figsize=(16,16))
    temp['geometry'].plot(ax=ax, color='gray', edgecolor='black', linewidth=0.4)
    temp['centroid'].plot(ax=ax, color='#fb1cff', alpha=0.7, markersize=10)
    temp2['geometry'].plot(ax=ax, color='#21e5ff', alpha=0.7, markersize=10)
    plt.title(GU)

get_gu_map('중구')




########################
geodf_moonhwa = geodf_moonhwa.reset_index()
geodf_moonhwa.rename(columns = {'index':'no'}, inplace = True)

idx_list = list()
for name in geodf_moonhwa['콘텐츠명']:
    if '태릉' in name:
        idx = geodf_moonhwa[geodf_moonhwa['콘텐츠명'] == name].index.item()
        idx_list.append(idx)

geodf_moonhwa.drop(geodf_moonhwa.index[idx_list], inplace = True)


with open('C:/Users/user/Desktop/Final_PJ/geodf_moonhwa.bin', 'wb')as f:
    pickle.dump(geodf_moonhwa, f)
    
# B구 A동 의 물리적 접근성 = A동의 중점에서 B구 내의 모든 센터와의 거리 평균





import geopandas as gpd
from shapely.geometry import Point

## 중구 소공동 중점 ## 
temp = pop[pop['GU_NM'] == '중구']
temp_x, temp_y  = temp.loc[17,:]['centroid'].x,temp.loc[17,:]['centroid'].y
temp_loc = (temp_x, temp_y)

## 중구 태평로 1가 서울도서관
temp2 = geodf_moonhwa[geodf_moonhwa['구'] == '중구']
temp2_x, temp2_y = temp2.loc[83,:]['geometry'].x, temp2.loc[83,:]['geometry'].y
temp2_loc = (temp2_x, temp2_y)





#####
def haversine(coord1, coord2):
    import math
    # Coordinates in decimal degrees (e.g. 2.89078, 12.79797)
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    R = 6371000  # radius of Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    meters = R * c
    #km = meters / 1000.0
    #meters = round(meters)
    #km = round(km, 3)
    #print(f"Distance: {meters} m")
    #print(f"Distance: {km} km")
    return(meters)


haversine(temp_loc, temp2_loc)
haversine(temp2_loc,temp_loc)

i = 0
pop.keys()
GU_list = list(pop['GU_NM'].unique())
pop['GEO_DIST'] = np.zeros((len(pop),1))
for i in range(len(pop)):
    dong_centroid = (pop.loc[i,'centroid'].x, pop.loc[i,'centroid'].y)
    GU = pop.loc[i,'GU_NM']
    GU_venter_list = list(geodf_moonhwa[geodf_moonhwa['구'] == GU]['geometry'])
    dist_list = list()
    for j in GU_venter_list:
        center_loc = (j.x, j.y)
        dist = haversine(dong_centroid,center_loc)
        dist_list.append(dist)
    pop.loc[i,'GEO_DIST'] = np.array(dist_list).mean()


max_x = pop['GEO_DIST'].max()
min_x = pop['GEO_DIST'].min()
pop['GEO_SCORE'] = pop['GEO_DIST'].map(lambda x: (x - min_x)/(max_x - min_x))



with open('C:/Users/user/Desktop/Final_PJ/geo_score_final.bin', 'wb') as f:
    pickle.dump(pop, f)



with open('C:/Users/user/Desktop/Final_PJ/geo_score_final.bin', 'rb') as f:
    pop = pickle.load(f)



import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable

pop = pop.set_crs('EPSG:4326')

plt.rcParams["figure.figsize"] = (30,30)
fig, ax = plt.subplots(1, 1)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
column = 'GEO_SCORE'
pop.plot(column, ax=ax, legend=True, cax=cax, cmap='OrRd')
ax.set_title("접근성")
ax.set_axis_off()
plt.show()



amt_shp = gpd.read_file('C:/Users/user/Desktop/Final_PJ/amt_final_shp/MyGeometries.shp', encoding = 'euc-kr')

amt_shp.crs

plt.rcParams["figure.figsize"] = (30,30)
fig, ax = plt.subplots(1, 1)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
column = 'scale'
amt_shp.plot(column, ax=ax, legend=True, cax=cax, cmap='OrRd')
ax.set_title("수급자 비율")
ax.set_axis_off()
plt.show()

