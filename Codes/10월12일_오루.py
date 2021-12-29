from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples


####
base.keys()
###

clust_data = base[['GEO_SCORE','AMT_SCORE','ALONE_SCORE','blue_pop']]

base.keys()

clust_data2 = clust_data[['GEO_SCORE','AMT_SCORE','ALONE_SCORE']]

clust_data3 = clust_data2[['GEO_SCORE','ALONE_SCORE']]

clust_data4 = clust_data[['AMT_SCORE','ALONE_SCORE','BLUE_SCORE']]


K_K = KMeans(n_clusters = 5, init = 'k-means++', n_init = 5, max_iter = 300, tol = 1e-4, random_state=0)
K_K.fit(clust_data)
K_K.predict(clust_data)


val_list = list()
for i in range(2,8):
    K_K = KMeans(n_clusters = i, init = 'k-means++', n_init = 5, max_iter = 300, tol = 1e-4, random_state=0)
    K_K.fit(clust_data)
    val_list.append(K_K.inertia_)
plt.plot(np.arange(2,8),val_list)


sh_list = list()
for i in range(2,8):
    K_K = KMeans(n_clusters = i, init = 'k-means++', n_init = 5, max_iter = 300, tol = 1e-4, random_state=0)
    K_K = K_K.fit(clust_data)
    K_K_Y = K_K.predict(clust_data)
    sh_vals = silhouette_samples(clust_data, K_K_Y, metric = 'euclidean')
    sh_list.append(np.mean(sh_vals))
plt.plot(np.arange(2,8), sh_list)

######################
GU_geodf = gpd.read_file('C:/Users/user/Desktop/Final_PJ/GUSHP/GuSHP.shp', encoding = 'utf-8-sig')
GU_geodf = GU_geodf.set_crs('EPSG:4326')

K_K = KMeans(n_clusters = 4, init = 'k-means++', n_init = 5, max_iter = 300, tol = 1e-4, random_state=0)
K_K.fit(clust_data)
K_K.predict(clust_data)

base['cluster'] = K_K.predict(clust_data)

pd.value_counts(base['cluster'].values)


pop['clust'] = np.zeros((len(pop), 1))

for i in dong_list:
    pop.loc[pop['ADM_DR_NM'] == i, 'clust'] = base.loc[base['DONG_NM']==i, 'cluster'].item()


base.loc[base['DONG_NM'] == '신사동', :]
pop.loc[pop['ADM_DR_NM'] == '신사동', :]

pop.loc[354,'clust'] = base.loc[354,'cluster'].item()
pop.loc[325,'clust'] = base.loc[325,'cluster'].item()

plt.rcParams["figure.figsize"] = (30,30)
fig, ax = plt.subplots(1, 1)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
column = 'clust'
pop.plot(column, ax=ax, legend=True, cax=cax, cmap='rainbow', edgecolor='black', linewidth=0.4)
GU_geodf.boundary.plot(ax= ax, edgecolor='black', linewidth=3)
ax.set_title("접근성")
ax.set_axis_off()
plt.show()
 
base.to_csv('C:/Users/user/Desktop/Final_PJ/cluster_(4F_4C).csv', encoding = 'utf-8-sig')


################
clust_0 = base[base['cluster'] == 0]

clust_0.keys()
clust_0['total'] = clust_0['GEO_SCORE']+clust_0['BLUE_SCORE']+clust_0['AMT_SCORE']+clust_0['ALONE_SCORE']

clust_3 = base[base['cluster'] == 3]
clust_3['total'] = clust_3['GEO_SCORE']+clust_3['BLUE_SCORE']+clust_3['AMT_SCORE']+clust_3['ALONE_SCORE']


fig, ax = plt.subplots(figsize=(16,16))
GU_geodf.boundary.plot(ax= ax, edgecolor='black', linewidth=3)
pop.plot(ax=ax, color='lightgray', edgecolor='grey', linewidth=0.4)
pop['centroid'].plot(ax=ax, color='#07424A', alpha=0.7, markersize=10)
geodf_moonhwa['geometry'].plot(ax=ax, color='#4a0707', alpha=0.7, markersize=10)

#####################

pop.keys()
gu_pop = pop[['GU_CD','GU_NM','pop']].groupby(['GU_CD','GU_NM'], as_index = False).sum()
    depress = pd.read_csv('C:/Users/user/Desktop/Final_PJ/Blue/blues.csv')
society = pd.read_csv('C:/Users/user/Desktop/Final_PJ/Blue/society.csv')
stress = pd.read_csv('C:/Users/user/Desktop/Final_PJ/Blue/stress.csv')
depress.sort_values(by = '지역', inplace = True)
depress['2019'] = depress['2019']/100
society.sort_values(by = 'gu', inplace = True)
society['score_p'] = society['score_p']/100
stress.sort_values(by = '지역', inplace = True)
stress['2019'] = stress['2019']/100
gu_pop.sort_values(by = 'GU_NM', inplace = True)


gu_pop['stress_pop'] = gu_pop['pop'] * stress['2019']
gu_pop['society_pop'] = gu_pop['pop'] * society['score_p']
gu_pop['blue_pop'] = gu_pop['pop'] * depress['2019']

plt.scatter(gu_pop['GU_NM'],gu_pop['stress_pop'])
plt.scatter(gu_pop['GU_NM'],gu_pop['society_pop'])
plt.scatter(gu_pop['GU_NM'],gu_pop['blue_pop'])
plt.grid()

gu_pop['geometry'] = 

GU_geodf[['stress_pop','society_pop','blue_pop']] = gu_pop[['stress_pop','society_pop','blue_pop']]
GU_geodf['emotion'] = GU_geodf['stress_pop'] + GU_geodf['society_pop'] + GU_geodf['blue_pop']
GU_geodf['emotion_P'] = ((GU_geodf['stress_pop'] + GU_geodf['society_pop'] + GU_geodf['blue_pop'])/3)/gu_pop['pop']
GU_geodf['emotion_P2'] = ((GU_geodf['stress_pop'] + GU_geodf['blue_pop'])/2)/gu_pop['pop']



plt.rcParams["figure.figsize"] = (30,30)
fig, ax = plt.subplots(1, 1)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
column = 'emotion_P2'
GU_geodf.boundary.plot(ax= ax, edgecolor='black', linewidth=3)
GU_geodf.plot(column, ax=ax, legend=True, cax=cax, cmap='OrRd')
ax.set_title("emotion_P2")
ax.set_axis_off()
plt.show()
