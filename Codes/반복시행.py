
GU_geodf = gpd.read_file('C:/Users/HyunJun/Desktop/Final_PJ/Final_PJ/Final_PJ/GUSHP/GuSHP.shp', encoding = 'utf-8-sig')
GU_geodf = GU_geodf.set_crs('EPSG:4326')

with open('C:/Users/HyunJun/Desktop/Final_PJ/BASE_FINAL(10_14)_(2).bin', 'rb') as f:
    data = pickle.load(f)
    
data['ALONE_RATE'] = data['ALONE_CNT']/data['TOTAL_POP']
scaler(data[['BLUE','ALONE_RATE']])['BLUE']

data['BLUE_TEMP_SCORE'] = scaler(data[['BLUE','INCOME_RATE']])['BLUE']*scaler(data[['BLUE','INCOME_RATE']])['INCOME_RATE'] +scaler(data[['BLUE','INCOME_RATE']])['BLUE']
data['BLUE_TEMP_SCORE'] = scaler(data[['BLUE','INCOME_RATE']])['BLUE']*scaler(data[['BLUE','INCOME_RATE']])['INCOME_RATE']



base_gubun = data

base_gubun = gpd.GeoDataFrame(base_gubun, geometry = 'geometry')
base_gubun.crs = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"


### GET K ###
base_gubun.keys()
WHOLE_FEATURE = ['GEO','TOTAL_POP', 'POOR', 'BLUE', 'ALONE_CNT', 
                'PARMACY_ACT','PARMACY', 'POOR_RATE', 'ALONE_RATE']
# 3 or 5 (True) / 4 or 6 (True = False)
FEATURE_LIST_1 = ['GEO','TOTAL_POP', 'POOR', 'BLUE', 'ALONE_CNT', 
                'PARMACY', 'POOR_RATE', 'ALONE_RATE']
# 4 (True = False)
FEATURE_LIST_2 = ['GEO', 'POOR', 'BLUE', 'ALONE_CNT', 
                'PARMACY', 'POOR_RATE', 'ALONE_RATE']
# 3,4,5 (True = False)
FEATURE_LIST_3 = ['GEO', 'BLUE','PARMACY', 'INCOME_RATE', 'ALONE_RATE']
# 3, 4 (True = False)
FEATURE_LIST_4 = ['GEO', 'BLUE', 'POOR_RATE', 'ALONE_RATE']
# 3,4 (T = F)
FEATURE_LIST_5 = ['GEO', 'PARMACY', 'INCOME_RATE', 'ALONE_RATE']

FEATURE_LIST_3 = ['GEO', 'BLUE_TEMP_SCORE','PARMACY', 'INCOME_RATE', 'ALONE_RATE']


## 땅땅땅 FEATURE LIST = ['GEO', 'BLUE','PARMACY_RATE', 'POOR_RATE', 'ALONE_RATE'] (RATE = 동별 인구수로 보정)
## 땅땅땅 K = 6 (엘보우만)
## 땅땅땅 MIN_MAX사용

base_gubun.rename(columns = {'접근성':'Accessibility','경제력':'Income Level','1인가구수':'Single Living','정신건강':'Mental wellness','신체건강':'Feasical wellness'}, inplace = True)
base_gubun.rename(columns = {'Feasical wellness':'Physical wellness'}, inplace = True)

FEATURE_LIST_3 = ['Accessibility', 'Income Level','Single Living', 'Mental wellness', 'Physical wellness']


clust_data = base_gubun[FEATURE_LIST_3]
get_k(clust_data)


### GET REST ###
GU_geodf = GU_geodf.set_crs('EPSG:4326')
raw_data = base_gubun
k = 6
scale = True

HOBBY = get_clust(raw_data,GU_geodf)
used_data, z_score_data, cluster_z = HOBBY(clust_data, k, scale, 'rainbow')

#scale = False
#HOBBY = get_clust(raw_data,GU_geodf)
#used_data, z_score_data, cluster_z = HOBBY(clust_data, k, scale)


search_df = used_data[used_data['cluster'] == 0]
search_df.keys()
search_df_step2 = search_df[['GU_NM', 'DONG_NM','ALONE_RATE','POOR_RATE']]
search_df_step2['score'] = search_df_step2['ALONE_RATE'] + search_df_step2['POOR_RATE']


alpha = cluster_z.loc[0,['POOR_RATE','ALONE_RATE']][0]
beta = cluster_z.loc[0,['POOR_RATE','ALONE_RATE']][1]

alpha_cal = alpha/(alpha+beta)
beta_cal = beta/(alpha+beta)
search_df_step2['score'] = search_df_step2['ALONE_RATE']*alpha_cal + search_df_step2['POOR_RATE']*beta_cal
search_df_step2.sort_values(['ALONE_RATE'],inplace = True, ascending=False)
search_df_step3 = search_df_step2.iloc[:10,:]
search_df_step3.sort_values(['POOR_RATE'],inplace = True, ascending=False)

gu_list = list(z_score_data['GU_NM'].unique())

import sys
mod = sys.modules[__name__]


for gu in gu_list:
    setattr(mod, 'data_{}'.format(gu),  z_score_data[z_score_data['GU_NM'] == gu] )

data_강남구
cluster_z

## 0 : POOR_RATE(3), ALONE_RATE(4)
## 1 : BLUE(1), POOR(3), ALONE(4)
## 2 : GEO 0 (100퍼센트라고 하고 *100)
## 3 : GEo 0 (100퍼센트라고 하고 *100)


poor_0 = cluster_z.iloc[0,4]
alone_0 = cluster_z.iloc[0,5]
poor_0_w = poor_0/(poor_0 + alone_0)
alone_0_w = alone_0/(poor_0 + alone_0)

blue_1 =  cluster_z.iloc[1,2]
poor_1 = cluster_z.iloc[1,4]
alone_1 = cluster_z.iloc[1,5]
blue_1_w = blue_1/(blue_1+poor_1+alone_1)
poor_1_w = poor_1/(blue_1+poor_1+alone_1)
alone_1_w = alone_1/(blue_1+poor_1+alone_1)

geo_2_w = 1

geo_3_w = 1

## 4 : PARMACY(2), POOR(3), ALONE(3)
## 5 : BLUE 1 (100#) 

parmacy_4 = cluster_z.iloc[4,3]
poor_4 = cluster_z.iloc[4,4]
alone_4 = cluster_z.iloc[4,5]
parmacy_4_w = parmacy_4/(parmacy_4+poor_4+alone_4)
poor_4_w = poor_4/(parmacy_4+poor_4+alone_4)
alone_4_w = alone_4/(parmacy_4+poor_4+alone_4)


blue_5 = 1
data_강동구['POOR_RATE']

data_강동구[data_강동구['cluster'] == 5].sum()

data = data_강남구
i = 0
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
    
    
    
data_은평구['cluster'].value_counts()

temp = used_data.loc[used_data['cluster'] == 2, 'GU_NM'].value_counts()
temp_alpha = scaler(base_gubun[['BLUE','INCOME_RATE']])
temp_alpha = pd.concat([base_gubun[['GU_NM','DONG_NM']],temp_alpha], axis = 1)
temp_alpha['score'] = temp_alpha['BLUE']*temp_alpha['INCOME_RATE'] + temp_alpha['BLUE']
temp_beta = temp_alpha[temp_alpha['GU_NM'] == '은평구']
temp_gamma = temp_alpha[temp_alpha['GU_NM'] == '용산구']
