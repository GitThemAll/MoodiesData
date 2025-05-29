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
import hdbscan

class dbscan_model:  
    #df : dataframe()   
    def __init__(self):
        self.df = DataFrame()
    
    def get_dataset_from_file(self) -> DataFrame: 
        return pd.read_csv('data//clean//customerLevel_kmeans.csv')
    
    def drop_correlated_columns(self):
        self.df.drop('Max Amount Orders', axis=1)  
        self.df[self.df['DaysSinceRecentOrder'] < 387]

    def scale_model(self):
        X = self.df.values
        scaler = StandardScaler()
        return scaler.fit_transform(X)
    
    def reduce_dimensions(self):
        pca = PCA(n_components='mle', random_state=42)
        self.get_dataset_from_file()
        return pca.fit_transform(self.scale_model)
    
    def apply_dbscan(self):
        dbscan = DBSCAN(eps=8, min_samples=20)    
        return dbscan.fit_predict(self.reduce_dimensions)
    
    def decide_number_of_clusters(self):
        return  len(set(self.apply_dbscan)) - (1 if -1 in self.apply_dbscan else 0)
    
    def number_noise(self):
        return list(self.apply_dbscan).count(-1)

    def plot_clusters(self):
        self.df['DBSCAN_Cluster'] = self.apply_dbscan
        plt.figure(figsize=(8, 5))
        plt.scatter(self.reduce_dimensions[:, 0], self.reduce_dimensions[:, 1], c=self.apply_dbscan, cmap='plasma', s=30)
        plt.title('DBSCAN Clustering (PCA-reduced Data)')
        plt.xlabel('PC1')
        plt.ylabel('PC2')
        plt.colorbar(label='Cluster')
        plt.grid(True)
        plt.show()
    pass
