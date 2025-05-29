import pandas as pd
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
    def __init__(self):
        self.df = pd.DataFrame()
    def get_dataset_from_file(self):
        return pd.read_csv('data//clean//customerLevel_kmeans.csv')
    def drop_correlated_columns(self):
        self.df.drop('Max Amount Orders', axis=1)  
        self.df[self.df['DaysSinceRecentOrder'] < 387]
    def scale_model(self):
        X = self.df.values
        scaler = StandardScaler()
        return scaler.fit_transform(X)
    def reduce_dimensions(self):
        pca = PCA(n_components='mle')
        return pca.fit_transform(self.scale_model(self))
    def apply_dbscan(self):
        dbscan = DBSCAN(eps=8, min_samples=20)    
        return dbscan.fit_predict(self.reduce_dimensions(self))
    def decide_number_of_clusters(self):
        return  len(set(self.apply_dbscan(self))) - (1 if -1 in self.apply_dbscan(self) else 0)
    def number_noise(self):
        return list(self.apply_dbscan(self)).count(-1)    
    pass
