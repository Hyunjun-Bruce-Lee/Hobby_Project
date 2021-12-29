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

gu_geo = gpd.read_file('C:/Users/user/Desktop/Final_PJ/GUSHP/GuSHP.shp', encoding = 'utf-8-sig')

with open('C:/Users/user/Desktop/Final_PJ/FINAL_CLUST/FINAL_CLUST/final_data.bin', 'rb') as f:
    base = pickle.load(f)

############### NEW_AMT 추가 #################
Q3 = base['AMT_MINMAX'].describe()['75%']
Q1 = base['AMT_MINMAX'].describe()['25%']

IQR = Q3 - Q1
lower = Q1 - 1.5*IQR
upper = Q3 + 1.5*IQR
base['NEW_AMT'] = base['AMT_MINMAX']
for i in base['NEW_AMT']:
    if i <= lower:
        base.loc[base['NEW_AMT'] == i, 'NEW_AMT'] = lower
    elif i >= upper:
        base.loc[base['NEW_AMT'] == i, 'NEW_AMT'] = upper


####################################
base['NEW_AMT'].describe()
base['NEW_AMT'].median()
#####################

### GET K ###
base.keys()

FEATURE = ['NEW_AMT', 'BODY', 'AREA_RATE','INFRA','RELATION']
clust_data = base[FEATURE]

# K means
get_k_means(clust_data,randint(0,2000))
# K medoids
get_k_medoids(clust_data,randint(0,2000))


### GET REST ###
# param setting
gu_geo = gu_geo.set_crs('EPSG:4326')
raw_data = base
mean_k = 5
medoid_k = 5
scale = 'min_max'
weight_list = None

# K medoids
HOBBY_medoid = get_clust_medoid(raw_data,gu_geo)
medodid_used_data, medodid_z_score_data, medodid_cluster_z = HOBBY_medoid(clust_data, medoid_k, scale, 'rainbow', randint(0,1000), weight_list)

# K means
HOBBY_means = get_clust_means(raw_data,gu_geo)
means_used_data, means_z_score_data, means_cluster_z = HOBBY_means(clust_data, mean_k, scale, 'rainbow', randint(0,1000))


medodid_used_data.value_counts('cluster')

medodid_z_score_data[]


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

