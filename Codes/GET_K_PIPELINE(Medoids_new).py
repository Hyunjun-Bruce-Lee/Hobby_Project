
def get_k_medoids(data,random):
    x = np.array(data)
    distortions = list()
    random_seed = list()
    sil = {}
    best_inertia = None
    for i in range(2, 21):
        for j in range(50):
            best_rand = 0
            temp_rand = randint(0,2000)
            km = KMedoids(n_clusters = i,
                          init='k-medoids++',
                          max_iter = 300,
                          random_state=temp_rand)
            km = km.fit(x)
            
            if best_inertia is None or km.inertia_ <= best_inertia:
                best_inertia = km.inertia_
                best_rand = temp_rand
        
        km = KMedoids(n_clusters = i,
                      init='k-medoids++',
                      max_iter = 300,
                      random_state=best_rand)
        km = km.fit(x)
        distortions.append(km.inertia_)
        y_km = km.predict(x)
        silhouette_vals = silhouette_samples(x,y_km, metric='euclidean')
        silhouette_avg = np.mean(silhouette_vals)
        # sil.append([i,silhouette_avg])
        sil[i] = silhouette_avg
    plt.figure(figsize = (50,50))
    plt.plot(range(2,21), distortions, marker = 'o', markersize=10, color = 'RED')
    plt.xticks(fontsize = 30)
    plt.yticks(fontsize = 30)
    plt.xlabel('Number of Clusters', fontsize = 30)
    plt.ylabel('Distortion', fontsize = 30)
    plt.grid()
    plt.tight_layout()
    plt.title('MEDOIDS', fontsize = 50)
    plt.show()
    print('가장 큰 실루엣 계수를 가지는 k:', sorted(sil.items(), key = lambda x: x[1], reverse=True)[0][0])


