import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def clustering(data:pd.DataFrame, do_pca:bool=True, n_clusters:int=3):
    if do_pca:
        pca = PCA(n_components=2)
        data = pca.fit_transform(data)
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(data)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    color_dict = {
        0: 'red', 
        1: 'blue', 
        2:'green'
        # 3:'black'
        }
    for cluster in range(2):
        cluster_sub_points = data[kmeans.labels_ == cluster]
        print("클러스터",cluster_sub_points)
        ax.scatter(cluster_sub_points[:, 0], cluster_sub_points[:, 1], c=color_dict[cluster], label='cluster_{}'.format(cluster))
    ax.set_title('K-means on circle data, K=2')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend() 
    ax.grid()
    return fig