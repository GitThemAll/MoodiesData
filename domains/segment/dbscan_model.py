import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import seaborn as sns
from sklearn.cluster import DBSCAN
import numpy as np
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors

class dbscan_model:  
    df : DataFrame
    scaler : StandardScaler
    pca : PCA
    x_reduced : np.ndarray

    def __init__(self):
        pass    
    
    def train_dbscan_model_seg(self):
        self.drop_correlated_columns()
        self.scale_model()
        self.reduce_dimensions()
        self.apply_dbscan()
        self.decide_number_of_clusters()
        self.number_noise()

    def get_dataset_from_file(self, dataset): 
        self.df = dataset
    
    def drop_correlated_columns(self):
        self.df.drop('Max Amount Orders', axis=1)  
        self.df[self.df['DaysSinceRecentOrder'] < 387]

    def scale_model(self):
        X = self.df.values
        return self.scaler.fit_transform(X)
    
    def reduce_dimensions(self):
        pca = PCA(n_components='mle', random_state=42)
        self.get_dataset_from_file()
        self.x_reduced = pca.fit_transform(self.scale_model)
    
    def apply_dbscan(self):
        dbscan = DBSCAN(eps=8, min_samples=20)    
        return dbscan.fit_predict(self.reduce_dimensions)
    
    def decide_number_of_clusters(self):
        return  len(set(self.apply_dbscan)) - (1 if -1 in self.apply_dbscan else 0)
    
    def number_noise(self) -> list:
        return list(self.apply_dbscan).count(-1)
    
    #add dbscan_labels to self
    def evalutate_exclude_noise(self, dbscan_labels):
        mask = dbscan_labels != -1
        n_clusters = len(set(dbscan_labels[mask]))
        if n_clusters > 1:
            sil_score = silhouette_score(self.x_reduced[mask], dbscan_labels[mask])
            print(f"Clusters found: {n_clusters}")
            print(f"Silhouette Score: {sil_score:.3f}")

    def summarize_clusters(self):
        output_path='dbscan_cluster_summary.csv'
        self.df['DBSCAN_Cluster'] = self.apply_dbscan()
        df_clusters = self.df[self.df['DBSCAN_Cluster'] != -1]
        cluster_summary = df_clusters.groupby('DBSCAN_Cluster').mean(numeric_only=True)
        cluster_summary.to_csv(output_path, index=True)
        return output_path

    # def plot_clusters(self):
    #     self.df['DBSCAN_Cluster'] = self.apply_dbscan
    #     plt.figure(figsize=(8, 5))
    #     plt.scatter(self.reduce_dimensions[:, 0], self.reduce_dimensions[:, 1], c=self.apply_dbscan, cmap='plasma', s=30)
    #     plt.title('DBSCAN Clustering (PCA-reduced Data)')
    #     plt.xlabel('PC1')
    #     plt.ylabel('PC2')
    #     plt.colorbar(label='Cluster')
    #     plt.grid(True)
