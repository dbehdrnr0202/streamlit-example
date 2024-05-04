import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import plotly.express as px

def clustering(data:pd.DataFrame, do_pca:bool=True, n_clusters:int=3):
    print(data)
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data.drop(columns=['방문지명']))
    pca = PCA(n_components=2)
    pca_data = pca.fit_transform(scaled_data)
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(pca_data)
    final_df = pd.DataFrame({"방문지명":data['방문지명'], "군집":pca_data[:,0], "pca1":pca_data[:,0], "pca2":pca_data[:,1]})
    final_df['군집'] = kmeans.labels_
    plt.rc('font', family='Malgun Gothic')
    plt.figure(figsize=(10, 6))
    for cluster in range(n_clusters):
        cluster_data = final_df[final_df['군집'] == cluster]
        plt.scatter(cluster_data.iloc[:, 0], cluster_data.iloc[:, 1], label=f'Cluster {cluster}')
        for i in range(len(cluster_data)):
            plt.text(cluster_data.iloc[i, 0], cluster_data.iloc[i, 1], cluster_data.iloc[i]['방문지명'],
                     fontsize=8, ha='right', va='bottom')
    fig = px.scatter(final_df, x=final_df['pca1'], y=final_df['pca2'], color=final_df['군집'], hover_name=final_df['방문지명'])
    plt.title('KMeans Clustering')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.grid(True)

    return fig