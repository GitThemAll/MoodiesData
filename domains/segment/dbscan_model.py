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
    labels : np.ndarray
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca = PCA(n_components='mle', random_state=42)
        pass    
    
    def model_x_value(self) -> list:
        return [
            "DaysSinceRecentOrder", "Nb Orders", "Amount Orders", "Avg Amount Orders",
            "Nb items", "Avg Nb items", "Avg item amount", "Max item amount", "PayMeth_Bancontact", "PayMeth_Card", "PayMeth_Ideal",
            "PayMeth_Klarna", "PayMeth_Other", "PayMeth_Pay Later", "PayMeth_shopify payments",
            "Always Discount", "Always Free Shipping", "Never Discount", "Never Free Shipping", "Max Discount Percentage",
            "Same SKU more than once", "Email Marketing Consent", "Accepts Marketing",
            "click", "open", "Days since First Active", "Days since Last Active",
            "Days since Profile Created On", "Recent City_amsterdam", "Recent City_den haag", "Recent City_rotterdam",
            "Recent City_utrecht", "Recent Country_be", "Recent Country_de", "Recent Country_nl"
        ]

    def train_dbscan_model_seg(self):
        self.drop_correlated_columns()
        self.scale_model()
        self.reduce_dimensions()
        self.apply_dbscan()
        self.decide_number_of_clusters()
        self.number_noise()
        self.evalutate_exclude_noise(self.labels)
        summary_path = self.summarize_clusters()
        print(f"Cluster summary saved to: {summary_path}")
        

    def get_dataset_from_file(self, dataset): 
        self.df = dataset
    
    def drop_correlated_columns(self):
        #self.df.drop('Max Amount Orders', axis=1)  
        self.df[self.df['DaysSinceRecentOrder'] < 387]

    def scale_model(self) -> StandardScaler:
        X = self.df[self.model_x_value()]
        return self.scaler.fit_transform(X)
    
    def reduce_dimensions(self) -> np.ndarray:        
        self.get_dataset_from_file(self.df)
        self.x_reduced = self.pca.fit_transform(self.scale_model())
        return self.x_reduced
    
    def apply_dbscan(self):
        dbscan = DBSCAN(eps=8, min_samples=20)    
        self.labels = dbscan.fit_predict(self.reduce_dimensions())
    
    def decide_number_of_clusters(self):
        return  len(set(self.labels)) - (1 if -1 in self.labels else 0)
    
    def number_noise(self) -> list:
        return list(self.labels).count(-1)
    
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
        self.df['DBSCAN_Cluster'] = self.labels
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
