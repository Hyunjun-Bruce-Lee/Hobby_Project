def get_k_means(data, random): # 데이터프레임 입력
    # elbow method
    x = np.array(data)
    distortions = []
    sil = {}
    for i in range(2, 21):
        km = KMeans(n_clusters = i,
                    init='k-means++',
                    n_init=50,
                    max_iter = 300,
                    tol = 1e-04,
                    random_state=random)
        km = km.fit(x)
        distortions.append(km.inertia_)
        y_km = km.predict(x)
        silhouette_vals = silhouette_samples(x,y_km, metric='euclidean')
        silhouette_avg = np.mean(silhouette_vals)
        # sil.append([i,silhouette_avg])
        sil[i] = silhouette_avg
    plt.plot(range(2,21), distortions, marker = 'o', markersize=10, color = 'RED')
    plt.xticks(fontsize = 30)
    plt.yticks(fontsize = 30)
    plt.xlabel('Number of Clusters', fontsize = 30)
    plt.ylabel('Distortion', fontsize = 30)
    plt.tight_layout()
    plt.title('MEANS', fontsize = 50)
    plt.show()
    print('가장 큰 실루엣 계수를 가지는 k:', sorted(sil.items(), key = lambda x: x[1], reverse=True)[0][0])