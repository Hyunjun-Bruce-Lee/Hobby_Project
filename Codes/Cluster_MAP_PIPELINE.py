import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
import pickle
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.axes_grid1 import make_axes_locatable


##### DF 정렬 기준 ####
alone.sort_values(['GU_NM','DONG_NM'], inplace = True)
data.sort_values(['GU_NM','DONG_NM'],inplace = True)
data['geometry'] = alone['geometry']
data.keys()
base = data[['GU_CD', 'GU_NM', 'DONG_CD', 'DONG_NM', 'geometry']]


#### shp 파일 만들기 ####
base = geopandas.GeoDataFrame(base, geometry = 'geometry')
base.crs = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
base.to_file('BASE.shp', driver='ESRI Shapefile')

### min_max scaler ###
def scaler(data):
    feature_list = list(data.keys())
    for fet in feature_list:
        max_x = data[fet].max()
        min_x = data[fet].min()
        data[fet] = data[fet].map(lambda x: (x-min_x)/(max_x-min_x))
    return data


### class ###
class get_clust:
    def __init__(self,base_data,gu_data,R_data = pd.DataFrame(), G_data = pd.DataFrame()):
        self.B_data = base_data
        self.R_data = R_data
        self.gu_data = gu_data
        self.G_data = G_data
    def __call__(self, clust_data, k, param, c):
        if param == True:
            clust_data = scaler(clust_data)
        
        base_feature = ['GU_NM','DONG_NM','geometry']
        aditional_feature = list(clust_data.keys())
        K_K = KMeans(n_clusters = k, init = 'k-means++', n_init = 5, max_iter = 300, tol = 1e-4, random_state=0)
        K_K.fit(clust_data)
        K_K.predict(clust_data)
        
        base_feature.extend(aditional_feature)
        self.R_data = self.B_data[base_feature].copy()
        
        if param == True:
            for ii in aditional_feature:
                self.R_data[ii] = clust_data[ii]
        
        self.R_data['cluster'] = K_K.predict(clust_data)
        
        self.R_data = gpd.GeoDataFrame(self.R_data, geometry = 'geometry')
        self.R_data.crs = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
        
        plt.rcParams["figure.figsize"] = (30,30)
        fig, ax = plt.subplots(1, 1)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        column = 'cluster'
        self.R_data.plot(column, ax=ax, legend=True, cax = cax, cmap= c, edgecolor='black', linewidth=0.4)
        self.gu_data.boundary.plot(ax= ax, edgecolor='black', linewidth=3)
        ax.set_axis_off()
        plt.show()
        
        # z_score 계산
        self.G_data = self.R_data.copy()
        for i in aditional_feature:
            self.G_data[i] = (self.R_data[i] - self.R_data[i].mean(axis=0)) / self.R_data[i].std(axis=0)
        
        z_score_name = ['cluster']
        z_score_name.extend(aditional_feature)
        z_score = pd.DataFrame(np.zeros((0,len(aditional_feature)+1)), columns = z_score_name)
        for j in range(k):
            temp = self.G_data.loc[self.G_data['cluster'] == j,:]
            score_list = [j]
            for f in aditional_feature:
                 score_list.append(temp[f].sum())
            z_score = z_score.append(pd.Series(score_list, index=z_score.columns), ignore_index=True)
        
        plt.figure()
        for i in range(k):
            temp = z_score.loc[z_score['cluster'] == i,:]
            bar_data = temp[aditional_feature]
            plt.subplot(int(str(k)+str(1)+str(i+1)))
            colors = sns.color_palette('hls',len(aditional_feature))
            plt.bar(aditional_feature, list(bar_data.iloc[0,:]), color = colors)
            plt.axhline(y=0, color='r', linewidth=5)
            plt.xticks(size = 30)
            plt.tight_layout()
            plt.grid()
        
        return self.R_data, self.G_data, z_score


with open('C:/Users/HyunJun/Desktop/Final_PJ/Final_PJ/Final_PJ/FIANL_OUTPUT.bin', 'rb')as f:
    data = pickle.load(f)

base_data = gpd.read_file('C:/Users/HyunJun/Desktop/Final_PJ/Final_PJ/Final_PJ/BASE/BASE.shp', encoding = 'ansi')


GU_geodf = gpd.read_file('C:/Users/HyunJun/Desktop/Final_PJ/Final_PJ/Final_PJ/GUSHP/GuSHP.shp', encoding = 'utf-8-sig')
GU_geodf = GU_geodf.set_crs('EPSG:4326')


al = get_clust(data,GU_geodf)
used_data, z_score_data, cluster_z = al(c_data, 4, False)
