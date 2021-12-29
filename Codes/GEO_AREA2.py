# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 11:49:31 2020

@author: HyunJun
"""


with open('C:/Users/HyunJun/Desktop/Final_PJ/GOE_AREA/living_hole.bin', 'rb') as f:
    geo_temp = pickle.load(f)

with open('C:/Users/HyunJun/Desktop/Final_PJ/GOE_AREA/only_living.bin', 'rb') as f:
    living_area = pickle.load(f)

geodf_moonhwa = gpd.read_file('C:/Users/HyunJun/Desktop/Final_PJ/Final_PJ/Final_PJ/문화체육시설/문화체육시설.shp', encoding = 'euc-kr')
geodf_moonhwa = geodf_moonhwa.set_crs('WGS84')
geodf_moonhwa= geodf_moonhwa.to_crs('EPSG:4326')

with open('C:/Users/HyunJun/Desktop/Final_PJ/GOE_AREA/BASE_FINAL(10_14)_(2).bin', 'rb') as f:
    data = pickle.load(f)
data = data.reset_index()
data.drop(['index'], axis = 1, inplace = True)

################# DONG BASE에 문화센터 구멍 뚫기 #######################
moonhwa_buffer = geodf_moonhwa['geometry'].buffer(1 / 109.958489129649955)
moonhwa_buffer = moonhwa_buffer.to_crs('EPSG:4326')
mp = moonhwa_buffer.unary_union

boros = data['geometry']
boros = boros.convex_hull

temp = boros.difference(mp)

empty_po = list(temp[temp.is_empty].index)

step_1 = pd.concat([data[['GU_NM','DONG_NM']],temp], axis = 1)

hole_fi = pd.DataFrame(np.zeros((0,3)), columns = ['GU_NM','DONG_NM','geometry'])
for i in range(len(step_1)):
    if temp[i].is_empty:
        continue
    else:
        hole_fi = hole_fi.append({'GU_NM':step_1.loc[i,'GU_NM'],
                         'DONG_NM':step_1.loc[i,'DONG_NM'],
                         'geometry':step_1.loc[i,0]},
                        ignore_index = True)

plotting_only = hole_fi['geometry']
plotting_only = pd.DataFrame(plotting_only)
plotting_only = gpd.GeoDataFrame(plotting_only, geometry = 'geometry')
plotting_only.crs = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"

plotting_only.plot()

hole_fi = gpd.GeoDataFrame(hole_fi, geometry = 'geometry')
hole_fi.crs = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
hole_fi.area


################# 구멍 뚤린 동 지도와 주거지역 인터섹션 #######################
living_area.plot()

boros = hole_fi['geometry']
boros2 = living_area.unary_union

temp2 = list()
count = 0
for i in boros:
    count+=1
    temp = i.intersection(boros2)
    temp2.append(temp)
    print('{}/{}'.format(count,263))
