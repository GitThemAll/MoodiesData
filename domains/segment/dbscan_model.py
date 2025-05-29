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
        self.df = pd.read_csv('data//clean//customerLevel_kmeans.csv')
        return self.df
    def drop_correlated_columns(self):
        self.df.drop('Max Amount Orders', axis=1)  
        self.df[self.df['DaysSinceRecentOrder'] < 387]
    def scale_model(self):
        X = self.df.values
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        return X_scaled
    def reduce_dimensions(self):
        pca = PCA(n_components='mle')
        X_reduced = pca.fit_transform(self.scale_model(self))
        return X_reduced

    pass
