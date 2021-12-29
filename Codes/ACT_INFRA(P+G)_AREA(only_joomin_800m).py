import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
import pickle
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable
from sklearn_extra.cluster import KMedoids
import pickle
import numpy as np
from random import randint
import geopandas as gpd
import sys


from matplotlib import colors
# AREA : 기존 문화체육시설에서 문화시설(구민회관 등) + 주민센터(800m buffer)
# INFRA : PLACE에 기존 AREA에 포함되었던 체육시설 포함, GREAN+PLACE(MIN_MAX조정 된)연산

base_dir = 'C:/Users/user/Desktop/Final_PJ/최종실행/INFRA(P+G)_AREA(only_joomin_800m)/'

gu_geo = gpd.read_file(base_dir + 'GUSHP/GuSHP.shp', encoding = 'utf-8-sig')

with open(base_dir + 'final_data.bin', 'rb') as f:
    base_data = pickle.load(f)

############### NEW_AMT 추가 #################
Q3 = base_data['AMT_MINMAX'].describe()['75%']
Q1 = base_data['AMT_MINMAX'].describe()['25%']

IQR = Q3 - Q1
lower = Q1 - 1.5*IQR
upper = Q3 + 1.5*IQR
base_data['NEW_AMT'] = base_data['AMT_MINMAX']
for i in base_data['NEW_AMT']:
    if i <= lower:
        base_data.loc[base_data['NEW_AMT'] == i, 'NEW_AMT'] = lower
    elif i >= upper:
        base_data.loc[base_data['NEW_AMT'] == i, 'NEW_AMT'] = upper

#############   AREA   ###############
##### 800m 버퍼  (주민센터 only) #####
with open(base_dir + 'temp_alpha_beta.bin','rb') as f:
    temp_living_alpha = pickle.load(f)
temp_living_alpha = pd.DataFrame(temp_living_alpha)

base_data['AREA'] = temp_living_alpha['cover_area']

### GET K ###
FEATURE = ['NEW_AMT', 'BODY', 'AREA','INFRA','RELATION']
clust_data = base_data[FEATURE]

# K medoids
get_k_medoids(clust_data,randint(0,2000))
# K means
#get_k_means(clust_data,randint(0,2000))

### GET REST ###
# param setting
c0_color,c1_color,c2_color,c3_color,c4_color = '#E68CFF', '#D86BFF','#FF8B6B', '#57CC04', '#74C5F7'
c5_color,c6_color,c7_color,c8_color,c9_color = '#FF8100', '#74C5F7','#FF8461','#31B8DE','#FF6262'
custom_colors = colors.ListedColormap([c0_color,c1_color,c2_color,c3_color,c4_color,c5_color,c6_color,c7_color,c8_color,c9_color])
custom_colors = colors.ListedColormap([red,yellow,blue,green,'#ffffff',purple,'#ffffff',yellow,red,red])

red = '#F15A5A'
yellow = '#F0C419'
green = '#4EBA6F'
blue = '#2D95BF'
purple = '#955BA5'

gu_geo = gu_geo.set_crs('EPSG:4326')
raw_data = base_data
#mean_k = 5
medoid_k = 10
scale = 'min_max'
color = custom_colors
weight_list = [1,1,1,1,1]

# K medoids
HOBBY_medoid = get_clust_medoid(raw_data,gu_geo)
medodid_used_data, medodid_z_score_data, medodid_cluster_z = HOBBY_medoid(clust_data, medoid_k, scale, color, randint(0,1000), weight_list)    

#medodid_used_data.to_csv('C:/Users/user/Desktop/Final_PJ/결과 노가다/3/used_data.csv', encoding = 'utf-8-sig')
#medodid_z_score_data.to_csv('C:/Users/user/Desktop/Final_PJ/결과 노가다/3/z_score_data.csv', encoding = 'utf=8=sig')
#medodid_cluster_z.to_csv('C:/Users/user/Desktop/Final_PJ/결과 노가다/3/clust_data.csv', encoding = 'utf-8-sig')

# K means
#HOBBY_means = get_clust_means(raw_data,gu_geo)
#means_used_data, means_z_score_data, means_cluster_z = HOBBY_means(clust_data, mean_k, scale, color, randint(0,1000))



        plt.figure(figsize = (30,40))
        for i in range(0,5):
            temp = medodid_cluster_z.loc[medodid_cluster_z['cluster'] == i,:]
            bar_data = temp[FEATURE]
            plt.subplot(int("{}{}{}".format(5, 1, i+1)))
            colors = sns.color_palette('hls',len(FEATURE))
            plt.bar(FEATURE, list(bar_data.iloc[0,:]), color = colors)
            plt.title('Cluster_{}'.format(i), fontsize = 30)
            plt.axhline(y=0, color='b', linewidth=5)
            plt.axhline(y=0.675, color='r', linewidth=5)
            plt.axhline(y=-0.675, color='r', linewidth=5)
            plt.xticks(size = 30)
            plt.tight_layout()
            plt.grid()


        plt.figure(figsize = (30,40))
        for i in range(5,10):
            temp = medodid_cluster_z.loc[medodid_cluster_z['cluster'] == i,:]
            bar_data = temp[FEATURE]
            plt.subplot(int("{}{}{}".format(5, 1, i-4)))
            colors = sns.color_palette('hls',len(FEATURE))
            plt.bar(FEATURE, list(bar_data.iloc[0,:]), color = colors)
            plt.title('Cluster_{}'.format(i), fontsize = 30)
            plt.axhline(y=0, color='b', linewidth=5)
            plt.axhline(y=0.675, color='r', linewidth=5)
            plt.axhline(y=-0.675, color='r', linewidth=5)
            plt.xticks(size = 30)
            plt.tight_layout()
            plt.grid()


##### 시 단위 제시 구별 미수혜 지역 인구수 산출
def get_bad_gu(in_data):
    temp_data = pd.DataFrame(np.zeros((0,2)), columns = ['GU_NM', 'POP_COUNT'])
    input_data = in_data
    gu_list = list(input_data['GU_NM'].unique())
    good = [4,6]
    for i in gu_list:
        data = input_data.loc[input_data['GU_NM'] == i, :]
        data = data.reset_index(drop = True)
        count = 0
        for j in range(len(data)):
            if data.iloc[j,-1].item() in good:
                continue
            else:
                count += int(data.iloc[j,2].item())
        temp_data = temp_data.append({'GU_NM':i, 'POP_COUNT':count}, ignore_index = True)
    return temp_data


alone_complare = pd.concat([base_data[['GU_NM','DONG_NM','ALONE_CNT']],medodid_used_data['cluster']], axis = 1)

si_solution_rank = get_bad_gu(alone_complare)

si_solution_rank.to_csv('C:/Users/user/Desktop/Final_PJ/결과 노가다/3/SI_SOLUTION_RANK.csv', encoding = 'utf-8-sig')


#############################################################################

mod = sys.modules[__name__]
gu_list = list(base_data['GU_NM'].unique())

gu_solution_data = pd.concat([medodid_z_score_data,base_data['ALONE_CNT']], axis = 1)

for gu in gu_list:
    setattr(mod, 'data_{}'.format(gu),  gu_solution_data[gu_solution_data['GU_NM'] == gu])

def get_score(in_data):
    input_data = in_data
    temp_df = pd.DataFrame(np.zeros((0,2)), columns = ['cluster','pop'])
    clust_list = list(input_data['cluster'].unique())
    for i in clust_list:
        data = input_data.loc[input_data['cluster']==i]
        if i == 0:
            score = data.loc[data['cluster'] == i, 'ALONE_CNT'].sum()
            temp_df = temp_df.append({'cluster':i,'pop':score}, ignore_index = True)
        elif i == 1:
            score = data.loc[data['cluster'] == i, 'ALONE_CNT'].sum()
            temp_df = temp_df.append({'cluster':i,'pop':score}, ignore_index = True)
        elif i == 2:
            score = data.loc[data['cluster'] == i, 'ALONE_CNT'].sum()
            temp_df = temp_df.append({'cluster':i,'pop':score}, ignore_index = True)
        elif i == 3:
            score = data.loc[data['cluster'] == i, 'ALONE_CNT'].sum()
            temp_df = temp_df.append({'cluster':i,'pop':score}, ignore_index = True)
        elif i == 4:
            continue
        elif i == 5:
            score = data.loc[data['cluster'] == i, 'ALONE_CNT'].sum()
            temp_df = temp_df.append({'cluster':i,'pop':score}, ignore_index = True)
        elif i == 6:
            continue
        elif i == 7:
            score = data.loc[data['cluster'] == i, 'ALONE_CNT'].sum()
            temp_df = temp_df.append({'cluster':i,'pop':score}, ignore_index = True)
        elif i == 8:
            score = data.loc[data['cluster'] == i, 'ALONE_CNT'].sum()
            temp_df = temp_df.append({'cluster':i,'pop':score}, ignore_index = True)
        elif i == 9:
            score = data.loc[data['cluster'] == i, 'ALONE_CNT'].sum()
            temp_df = temp_df.append({'cluster':i,'pop':score}, ignore_index = True)
    return temp_df


final_score = dict()
for gu in gu_list:
    temp = getattr(mod, 'data_{}'.format(gu))
    final_score[gu] = get_score(temp).sort_values(by = 'pop', ascending = False).reset_index(drop = True)

gu_solution_rank = pd.DataFrame(np.zeros((0,9)), columns = ['GU_NM','1st_cluster','1st_score','2nd_cluster','2nd_score','3rd_cluster','3rd_score','4th_cluster','4th_score'])
for i in gu_list:
    append_dict = dict()
    append_dict['GU_NM'] = i
    for j in range(len(final_score[i])):
        if j == 0:
            append_dict['1st_cluster'] = int(final_score[i].loc[j,'cluster'].item())
            append_dict['1st_score'] = final_score[i].loc[j,'pop'].item()
        elif j == 1:
            append_dict['2nd_cluster'] = int(final_score[i].loc[j,'cluster'].item())
            append_dict['2nd_score'] = final_score[i].loc[j,'pop'].item()
        elif j == 2:
            append_dict['3rd_cluster'] = int(final_score[i].loc[j,'cluster'].item())
            append_dict['3rd_score'] = final_score[i].loc[j,'pop'].item()
        elif j == 3:
            append_dict['4th_cluster'] = int(final_score[i].loc[j,'cluster'].item())
            append_dict['4th_score'] = final_score[i].loc[j,'pop'].item()
    gu_solution_rank = gu_solution_rank.append(append_dict, ignore_index = True)


gu_solution_rank.to_csv('C:/Users/user/Desktop/Final_PJ/결과 노가다/3/GU_SOLUTION_RANK.csv', encoding = 'utf-8-sig')


# 시단위 : 시차원에서 구에게 해줄것
#         1인가구 문제를 해결하기 위해서
#             1. 취약한 동개수 기반 파이 차트 제공(max 6개 각 피쳐 5개 + 문제 없는곳 1개)
#                   => 시차원에서 시전반의 환경을 개선할떄 어느부분에 집중해야 하는가
                  
#             2 .1인가구 인구 기반 구단위 우선순위 제공 (어느 클러스터든 문제가 있기에 동등하게 취급)
#                  => 구에 지원을해줄때 이순위를 참고해라

# 구단위 : 구 내의 동의 클러스터에 속한 인구수의 합으로 우선순위 제공
#             ->구내의 각 클러스터의 총 인구수로 순위 

# 동단위 : 실제 동에서의 운영 기획

def morf(x):
    if x >=1900:
        return 1900
    else:
        return x

base2 = base_data.copy()

base2['ALONE_CNT'] = base2['ALONE_CNT'].map(lambda x: morf(x))

draw_plot(base2,'ALONE_CNT')




def draw_plot(data, feature):
    plt.rcParams["figure.figsize"] = (30,30)
    fig, ax = plt.subplots(1, 1)
    column = feature
    data.plot(column, ax=ax, cmap= 'Blues')
    data['geometry'].boundary.plot(ax= ax, edgecolor='Black', linewidth=3, alpha = 0.1)
    gu_geo.boundary.plot(ax= ax, edgecolor='Black', linewidth=3, alpha = 0.8)
    ax.set_axis_off()
    plt.show()


FEATURE = ['NEW_AMT', 'BODY', 'AREA','INFRA','RELATION']
temp_data = base_data.copy() 
temp_data[FEATURE] = 1 - scaler(temp_data[FEATURE])

draw_plot(temp_data,'AREA')


temp_data.keys()
    
plt.rcParams["figure.figsize"] = (30,30)
fig, ax = plt.subplots(1, 1)
temp_data.loc[(temp_data['DONG_NM'] == '화곡1동') | 
              (temp_data['DONG_NM'] == '역삼1동') | 
              (temp_data['DONG_NM'] == '중화2동') | 
              (temp_data['DONG_NM'] == '대학동') |
              (temp_data['DONG_NM'] == '면목본동'),'geometry'].plot(ax = ax, color = 'red')
gu_geo.boundary.plot(ax= ax, edgecolor='Black', linewidth=3, alpha = 0.2)
ax.set_axis_off()
plt.show()




custom_colors = colors.ListedColormap(['#DD05F7','#5404D4', '#0722EB', '#0482D4', '#18F5E0', '#B5C7D3','#C77388','#A58D7F','#84898C'])
custom_colors = colors.ListedColormap(['r','y','b'])

clust_frame = medodid_used_data[(medodid_used_data['cluster'] == 0) | (medodid_used_data['cluster'] == 8) | (medodid_used_data['cluster'] == 9)]
custom_colors = colors.ListedColormap([c0_color,c8_color,c9_color])
clust_frame = medodid_used_data[(medodid_used_data['cluster'] == 4) | (medodid_used_data['cluster'] == 6)]
custom_colors = colors.ListedColormap([c4_color,c6_color])
clust_frame = medodid_used_data[(medodid_used_data['cluster'] == 5)]


def morf_no(x):
    if x ==4:
        return 0
    elif x == 6:
        return 10
    elif x == 9:
        return 10

clust_frame['cluster'] = clust_frame['cluster'].map(lambda x: morf_no(x))


plt.rcParams["figure.figsize"] = (30,30)
fig, ax = plt.subplots(1, 1)
column = 'cluster'
clust_frame.plot(column, ax=ax, cmap= custom_colors)
gu_geo.boundary.plot(ax= ax, edgecolor='Black', linewidth=3, alpha = 0.8)
ax.set_axis_off()
plt.show()



base_data['cluster'] = medodid_used_data['cluster']

def draw_plot(data, feature):
    plt.rcParams["figure.figsize"] = (30,30)
    fig, ax = plt.subplots(1, 1)
    column = feature
    data.plot(column, ax=ax, cmap= 'Blues')
    data['geometry'].boundary.plot(ax= ax, edgecolor='Black', linewidth=3, alpha = 0.1)
    gu_geo.boundary.plot(ax= ax, edgecolor='Black', linewidth=3, alpha = 0.8)
    ax.set_axis_off()
    plt.show()

plt.rcParams["figure.figsize"] = (30,30)
fig, ax = plt.subplots(1, 1)
for i in range(len(base_data)):
    base_data.loc[i,:].plot('cluster', ax=ax, cmap= 'Blues')
    
    
a = base_data.loc[i,:]
