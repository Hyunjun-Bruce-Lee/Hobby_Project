import pandas as pd
import pickle
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import geopandas as gpd

with open('C:/Users/HyunJun/Desktop/Final_PJ/GOE_AREA/BASE_FINAL(10_14)_(2).bin', 'rb') as f:
    data = pickle.load(f)

#### 서울 원래 지도 - 문화 BUFFER
base_dir = 'C:/Users/HyunJun/Desktop/Final_PJ/Final_PJ/Final_PJ/'

geodf_moonhwa = gpd.read_file(base_dir + '문화체육시설/문화체육시설.shp', encoding = 'euc-kr')
geodf_moonhwa = geodf_moonhwa.set_crs('WGS84')
geodf_moonhwa= geodf_moonhwa.to_crs('EPSG:4326')

## 경도기준 1km = 1/88.74
## 위도기준 1km = 1 / 109.958489129649955
moonhwa_buffer = geodf_moonhwa['geometry'].buffer(1 / 109.958489129649955)
moonhwa_buffer = moonhwa_buffer.to_crs('EPSG:4326')
data = data.reset_index()
data.drop(['index'], axis = 1, inplace = True)
boros = data['geometry']
boros = boros.convex_hull
mp = moonhwa_buffer.unary_union
holes = boros.difference(mp)

for i in range(len(holes)):
    if holes[i].is_empty:
        holes[i] = data.loc[i,'geometry']
       
holes.geometry.area

holes.plot()

holes_final = pd.concat([data[['GU_NM','DONG_NM']],holes], axis = 1).rename(columns = {0:'geometry'})

###################################

with open('C:/Users/user/Desktop/Final_PJ/GEO_AREA/geoconcat.bin', 'rb') as f:
    geo = pickle.load(f)

geo = geo.set_crs('EPSG:5174')
## 2097, 5178(아에 다름), 5181(살짝 왼쪽 아래) 5174(선택)
geo = geo.to_crs('WGS84')


geo.keys()
## 2210, 2220, 2240 = 산지
## 3110, 3120 = 주택지 (3130 = 업무지)

geo_temp1 = geo[geo['UCB'] == '3110']
geo_temp2 = geo[geo['UCB'] == '3120']
geo_temp = pd.concat([geo_temp1, geo_temp2], axis = 0)
boros = data['geometry'].convex_hull
boros2 = geo_temp['geometry'].unary_union

temp = boros.intersection(boros2)

with open('C:/Users/user/Desktop/Final_PJ/GEO_AREA/only_living.bin', 'wb') as f:
    pickle.dump(temp,f)

plt.figure(figsize = (100,100))
temp.plot()


holes2 = holes.convex_hull

temp2 = temp.unary_union
temp3 = holes2.intersection(temp2)

temp3.is_empty


for i in range(len(temp3)):
    if temp3[i].is_empty:
        temp3[i] = data.loc[i,'geometry']

temp3.plot()

with open('C:/Users/user/Desktop/Final_PJ/GEO_AREA/living_hole.bin', 'wb') as f:
    pickle.dump(temp3,f)