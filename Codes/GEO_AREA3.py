# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 11:49:31 2020

@author: HyunJun
"""

with open('C:/Users/user/Desktop/Final_PJ/GOE_AREA 3/GOE_AREA/only_living.bin', 'rb') as f:
    living_area = pickle.load(f)

geodf_moonhwa = gpd.read_file('C:/Users/user/Desktop/Final_PJ/GOE_AREA 3/GOE_AREA/문화체육시설/문화체육시설.shp', encoding = 'euc-kr')
geodf_moonhwa = geodf_moonhwa.loc[142:200,'geometry']
geodf_moonhwa = geodf_moonhwa.set_crs('WGS84')
geodf_moonhwa= geodf_moonhwa.to_crs('EPSG:4326')
geodf_moonhwa = pd.DataFrame(geodf_moonhwa)
geodf_moonhwa = geodf_moonhwa.reset_index(drop = True)

## 신규 주민센터 point 추가
new_point = pd.read_csv('C:/Users/user/Desktop/Final_PJ/GOE_AREA 3/GOE_AREA/JUMIN_JUSO_FINAL.csv',encoding = 'utf-8')

new_point = gpd.GeoDataFrame(new_point, geometry=gpd.points_from_xy(new_point.경도, new_point.위도))
geodf_moonhwa = pd.concat([geodf_moonhwa['geometry'], new_point['geometry']])
geodf_moonhwa = geodf_moonhwa.reset_index(drop = True)
geodf_moonhwa = gpd.GeoDataFrame(geodf_moonhwa, geometry = 'geometry')
geodf_moonhwa = geodf_moonhwa.set_crs('WGS84')
geodf_moonhwa = geodf_moonhwa.to_crs('EPSG:4326')

with open('C:/Users/user/Desktop/Final_PJ/GOE_AREA 3/GOE_AREA/BASE_FINAL(10_14)_(2).bin', 'rb') as f:
    data = pickle.load(f)
data = data.reset_index()
data.drop(['index'], axis = 1, inplace = True)

################# DONG BASE에 문화센터 구멍 뚫기 #######################
moonhwa_buffer = geodf_moonhwa['geometry'].buffer((1 / 109.958489129649955)*0.8)
moonhwa_buffer = moonhwa_buffer.to_crs('EPSG:4326')
mp = moonhwa_buffer.unary_union

boros = data['geometry']
boros = boros.convex_hull

temp = boros.difference(mp)

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


plt.rcParams["figure.figsize"] = (30,30)
fig, ax = plt.subplots(1, 1)
plotting_only.plot(ax = ax, color = '#0F4C81')
gu_geo.boundary.plot(ax= ax, edgecolor='Black', linewidth=5, alpha = 0.1)
ax.set_axis_off()
plt.show()



hole_fi = gpd.GeoDataFrame(hole_fi, geometry = 'geometry')
hole_fi.crs = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"

################# 구멍 뚤린 동 지도와 주거지역 인터섹션 #######################
plt.rcParams["figure.figsize"] = (30,30)
fig, ax = plt.subplots(1, 1)
living_area.plot(ax = ax, color = '#FAD148')
gu_geo.boundary.plot(ax= ax, edgecolor='Black', linewidth=5, alpha = 0.1)
ax.set_axis_off()
plt.show()

boros = hole_fi['geometry']
boros2 = living_area.unary_union

temp_alpha = boros.intersection(boros2)

temp2 = pd.concat([hole_fi[['GU_NM','DONG_NM']], temp_alpha], axis = 1)
temp2 = temp2.reset_index(drop = True)

temp2 = gpd.GeoDataFrame(temp2, geometry = 0)
mid_step = temp2[0]

final_hole = pd.DataFrame(np.zeros((0,3)), columns = ['GU_NM','DONG_NM','geometry'])
for i in range(len(temp2)):
    if mid_step[i].is_empty:
        continue
    else:
        final_hole = final_hole.append({'GU_NM':temp2.loc[i,'GU_NM'],
                         'DONG_NM':temp2.loc[i,'DONG_NM'],
                         'geometry':temp2.loc[i,0]},
                        ignore_index = True)
        
len(final_hole)
final_hole = gpd.GeoDataFrame(final_hole, geometry = 'geometry')
final_hole['AREA'] = final_hole.geometry.area

living_data = pd.concat([data[['GU_NM','DONG_NM']],living_area], axis = 1)
living_data.rename(columns = {0:'geometry'}, inplace = True)
living_data = gpd.GeoDataFrame(living_data, geometry = 'geometry')
living_data['all_area'] = living_data.geometry.area

gu_list = list(final_hole['GU_NM'].unique())
living_data['non_area'] = np.zeros((len(living_data),1))
for i in gu_list:
    dong_list = list(final_hole.loc[final_hole['GU_NM']==i,'DONG_NM'].unique())
    for j in dong_list:
        living_data.loc[(living_data['GU_NM']==i) & (living_data['DONG_NM']==j), 'non_area'] = final_hole.loc[(final_hole['GU_NM'] == i) & (final_hole['DONG_NM']==j), 'AREA'].item()

living_data['area_rate'] = living_data['non_area']/living_data['all_area']
living_data['cover_area'] = 1-living_data['area_rate']

plt.boxplot(living_data['cover_area'])

