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
# AREA : 기존 문화체육시설에서 문화시설(구민회관 등) + 주민센터(800m buffer)
# INFRA : PLACE에 기존 AREA에 포함되었던 체육시설 포함, GREAN+PLACE(MIN_MAX조정 된)연산

base_dir = 'C:/Users/user/Desktop/Final_PJ/최종실행/INFRA(P+G)_AREA(only_joomin_800m_noRATE)/'

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

#############   AREA   ###################
##### 800m 버퍼  (주민센터 only) #########
#### 주거지역 면적 나누기 X 순수 면적 ####
with open(base_dir + 'temp_living_data.bin','rb') as f:
    temp_living = pickle.load(f)
(temp_living[['GU_NM','DONG_NM']] == base_data[['GU_NM','DONG_NM']]).sum()

temp_living['new_area'] = temp_living['geometry'].area

temp_living = temp_living['new_area']
# 높은게 좋은걸로 변환
temp_living = temp_living.max()- temp_living
base_data['AREA'] = scaler(pd.DataFrame(temp_living))

base_data['AREA'].describe()

plt.boxplot(base_data['AREA'])

######## INFRA (PLACE + GREEN) #######
with open(base_dir + 'BASE_FOR_INFRA(P+G).bin', 'rb') as f:
    new_infra = pickle.load(f)
a = np.array(scaler(pd.DataFrame(new_infra['GREEN'])))
b = np.array(scaler(pd.DataFrame(new_infra['PLACE'])))
new_infra['INFRA'] =  (a+b) - 0.5*abs(a - b)
base_data['INFRA'] = new_infra['INFRA']

### GET K ###
base_data.keys()

FEATURE = ['NEW_AMT', 'BODY', 'AREA','INFRA','RELATION']
clust_data = base_data[FEATURE]

# K medoids
get_k_medoids(clust_data,randint(0,2000))
# K means
#get_k_means(clust_data,randint(0,2000))

### GET REST ###
# param setting
gu_geo = gu_geo.set_crs('EPSG:4326')
raw_data = base_data
mean_k = 5
medoid_k = 7
scale = 'min_max'
color = 'rainbow'
weight_list = [1,1,1,1,1]

# K medoids
HOBBY_medoid = get_clust_medoid(raw_data,gu_geo)
medodid_used_data, medodid_z_score_data, medodid_cluster_z = HOBBY_medoid(clust_data, medoid_k, scale, color, randint(0,1000), weight_list)    

# K means
#HOBBY_means = get_clust_means(raw_data,gu_geo)
#means_used_data, means_z_score_data, means_cluster_z = HOBBY_means(clust_data, mean_k, scale, color, randint(0,1000))


#############################################################################

medodid_used_data.value_counts('cluster')

medodid_cluster_z


means_used_data[means_used_data['cluster']== 4].describe()
means_used_data['cluster'].value_counts()

temp =means_used_data[means_used_data['cluster']== 4]


temp_alpha = scaler(base[FEATURE])

for i in FEATURE:
    print('{}, {}'.format(i,temp_alpha[i].std()))

means_z_score_data


####################################

mod = sys.modules[__name__]
gu_list = list(base['GU_NM'].unique())

for gu in gu_list:
    setattr(mod, 'data_{}'.format(gu),  z_score_data[z_score_data['GU_NM'] == gu] )


def get_score(in_data):
    input_data = in_data
    temp_df = pd.DataFrame(np.zeros((0,2)), columns = ['cluster','score'])
    clust_list = list(input_data['cluster'].unique())
    for i in clust_list:
        data = input_data.loc[input_data['cluster']==i]
        if i == 0:
            score = (data['POOR_RATE']*poor_0_w + data['ALONE_RATE']*alone_0_w).sum()
            temp_df = temp_df.append({'cluster':i,'score':score}, ignore_index = True)
        elif i == 1:
            score = (data['BLUE']*blue_1_w + data['POOR_RATE']*poor_1_w + data['ALONE_RATE']*alone_1_w).sum()
            temp_df = temp_df.append({'cluster':i,'score':score}, ignore_index = True)
        elif i == 2:
            score = data['GEO'].sum()
            temp_df = temp_df.append({'cluster':i,'score':score}, ignore_index = True)
        elif i == 3:
            score = data['GEO'].sum()
            temp_df = temp_df.append({'cluster':i,'score':score}, ignore_index = True)
        elif i == 4:
            score = (data['PARMACY']*parmacy_4_w + data['POOR_RATE']*poor_4_w + data['ALONE_RATE']*alone_4_w).sum()
            temp_df = temp_df.append({'cluster':i,'score':score}, ignore_index = True)
        elif i == 5:
            score = data['BLUE'].sum()
            temp_df = temp_df.append({'cluster':i,'score':score}, ignore_index = True)
    return temp_df


final_score = dict()
for gu in gu_list:
    temp = getattr(mod, 'data_{}'.format(gu))
    final_score[gu] = get_score(temp)

FEATURE
i = 'RELATION'
sns.kdeplot(base[i])
plt.title(i, fontsize = 40)


base['AREA_RATE'].describe()
base.loc[base['DONG_NM'] == '', 'AREA_RATE']
