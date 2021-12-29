### min_max scaler ###
def scaler(data):
    feature_list = list(data.keys())
    for fet in feature_list:
        max_x = data[fet].max()
        min_x = data[fet].min()
        data[fet] = data[fet].map(lambda x: (x-min_x)/(max_x-min_x))
    return data


### class ###
class get_clust_medoid:
    def __init__(self,base_data,gu_data,R_data = pd.DataFrame(), G_data = pd.DataFrame()):
        self.B_data = base_data
        self.R_data = R_data
        self.gu_data = gu_data
        self.G_data = G_data
    def __call__(self, clust_data, k, param, c, random_no,  weight_list = None):
        if param == 'min_max':
            clust_data = scaler(clust_data)
        elif param == 'z_score':
            clust_data = z_scaler(clust_data)
        elif param == None:
            clust_data = clust_data
        
        if weight_list == None:
            pass
        else:
            for i,j in zip(weight_list,clust_data.keys()):
                clust_data[j] = clust_data[j]*i
            
    
        ###
        best_inertia = None
        temp_rand = random_no
        for j in range(100):
            best_rand = 0
            temp_rand = randint(0,2000)
            km = KMedoids(n_clusters = k,
                          init='k-medoids++',
                          max_iter = 300,
                          random_state=temp_rand)
            km = km.fit(clust_data)
            
            if best_inertia is None or km.inertia_ <= best_inertia:
                best_inertia = km.inertia_
                best_rand = temp_rand
        ###
        
        base_feature = ['GU_NM','DONG_NM','geometry']
        aditional_feature = list(clust_data.keys())
        K_K = KMedoids(n_clusters = k, init = 'k-medoids++', max_iter = 300, random_state=best_rand)
        K_K.fit(clust_data)
        
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
        #cax = divider.append_axes("right", size="5%", pad=0.1)
        column = 'cluster'
        self.R_data.plot(column, ax=ax, legend=True, cmap= c, categorical = True, edgecolor='black', linewidth=0.4)
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
                ####
                 score_list.append(temp[f].mean())
            z_score = z_score.append(pd.Series(score_list, index=z_score.columns), ignore_index=True)
        
        #plt.figure(figsize = (30,90))
        #for i in range(k):
        #    temp = z_score.loc[z_score['cluster'] == i,:]
        #    bar_data = temp[aditional_feature]
        #    plt.subplot(int("{}{}{}".format(k, 1, i+1)))
        #    colors = sns.color_palette('hls',len(aditional_feature))
        #    plt.bar(aditional_feature, list(bar_data.iloc[0,:]), color = colors)
        #    plt.axhline(y=0, color='b', linewidth=5)
        #    plt.axhline(y=0.4, color='r', linewidth=5)
        #    plt.axhline(y=-0.4, color='r', linewidth=5)
        #    plt.xticks(size = 30)
        #    plt.tight_layout()
        #    plt.grid()
        
        return self.R_data, self.G_data, z_score
