import pandas as pd
import geopandas as gpd
import numpy as np
import pickle
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl
%matplotlib inline
mpl.rc('font', family='NanumGothic')

alone = pd.read_csv('C:/Users/user/Desktop/Final_PJ/중장년1인가구원본/동별1인가구수(40_65).csv', encoding = 'CP949', names = ['GU_NM','DONG_NM','CNT'])

with open('C:/Users/user/Desktop/Final_PJ/geo_score_final.bin', 'rb') as f:
    pop = pickle.load(f)

not_in_geo = list()
for i in list(alone['DONG_NM']):
    if i in list(pop['ADM_DR_NM']):
        continue
    else:
        dong = alone.loc[alone['DONG_NM']==i, 'DONG_NM'].item()
        gu = alone.loc[alone['DONG_NM']==i, 'GU_NM'].item()
        not_in_geo.append([gu,dong])
    
for i in list(alone['DONG_NM']):
    if '정름' in i:
        alone.loc[alone['DONG_NM']==i,'DONG_NM'] = alone.loc[alone['DONG_NM']==i,'DONG_NM'].item().replace('정름','정릉')




alone['geometry'] = np.zeros((len(alone),1))
dong_list = list(alone['DONG_NM'].unique())
dong_list.remove('신사동')
for i in dong_list:
    alone.loc[alone['DONG_NM'] == i, 'geometry'] = pop.loc[pop['ADM_DR_NM'] == i, 'geometry'].item()

alone.loc[alone['DONG_NM'] =='신사동', :]
pop.loc[pop['ADM_DR_NM']=='신사동', :]

alone.loc[78,'geometry'] = pop.loc[325, 'geometry']
alone.loc[12,'geometry'] = pop.loc[354, 'geometry']

with open('C:/Users/user/Desktop/Final_PJ/alone_final.bin', 'wb') as f:
    pickle.dump(alone, f)

alone_geodf = gpd.read_file('C:/Users/user/Desktop/Final_PJ/alone_final/alone_final.shp', encoding = 'utf-8-sig')

alone_geodf = alone_geodf.set_crs('EPSG:4326')

plt.rcParams["figure.figsize"] = (30,30)

fig, ax = plt.subplots(1, 1)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
column = 'CNT'
#step1.plot(column, ax=ax, legend=True, cax=cax, cmap='OrRd')
alone_geodf.plot(column, ax=ax, legend=True, cax=cax, cmap='OrRd')
ax.set_title("서울시 문화시설 밀집도")
ax.set_axis_off()
plt.show()


alone['score'] = np.zeros((len(alone),1))
max_x = alone['CNT'].max()
min_x = alone['CNT'].min()
alone['score'] = alone['CNT'].map(lambda x: (x-min_x)/(max_x-min_x))
