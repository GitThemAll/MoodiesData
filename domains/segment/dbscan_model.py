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
from sklearn.cluster import KMeans

class dbscan_model:  
    df : DataFrame
    scaler : StandardScaler
    pca : PCA
    x_reduced : np.ndarray
    labels : np.ndarray
    eps_range : np.ndarray
    min_samples_range : np.ndarray
    kmeans_model : KMeans
    kmeans_labels : np.ndarray
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca = PCA(n_components='mle', random_state=42)
        self.eps_range = np.arange(1.0, 10.0, 0.5)
        self.min_samples_range = range(3, 10)
    
    def model_x_value(self) -> list:
        return [
            "DaysSinceRecentOrder", "Nb Orders",
            "Nb items", "PayMeth_Bancontact", "PayMeth_Card", "PayMeth_Ideal",
            "PayMeth_Klarna", "PayMeth_Other", "PayMeth_Pay Later", "PayMeth_shopify payments", 
            "Always Free Shipping", "Max Discount Percentage",
            "Same SKU more than once", "Email Marketing Consent", "Accepts Marketing",
            "open", "Days since First Active", "Recent City_amersfoort",
            "Recent City_amsterdam", "Recent City_den haag", "Recent City_rotterdam",
            "Recent City_utrecht", "Recent Country_be", "Recent Country_nl",
            "EM-008", "EM-010", "ML-009", "MM-008", "MS-006", "SM-001", "SM-003", "SY-001", "YH-006", "YM-006"            
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
        self.save_labeled_customers()
        print(self.get_cluster_sizes())
        #self.remove_noise_and_retrain()

        # #kmeans
        # self.train_kmeans()
        # self.summarize_kmeans_clusters()
        # self.analyze_kmeans_balance()

        #hdbscan
        #self.apply_hdbscan(min_cluster_size=500, min_samples=150) 

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
        dbscan = DBSCAN(eps=2.7, min_samples=550) 
        #dbscan = DBSCAN(eps=9.5, min_samples=8) #not balanced
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
        output_path = 'resources/data/processed/segment/dbscan_cluster_summary.csv'
        # Add the cluster labels to the dataset
        self.df['DBSCAN_Cluster'] = self.labels
        # Filter out noise
        df_clusters = self.df[self.df['DBSCAN_Cluster'] != -1]
        # Restrict to only features used in training + cluster label
        selected_features = self.model_x_value() + ["DBSCAN_Cluster"]
        df_filtered = df_clusters[selected_features]
        # Group and average only training features
        cluster_summary = df_filtered.groupby("DBSCAN_Cluster").mean(numeric_only=True)
        # Save to CSV
        cluster_summary.to_csv(output_path, index=True)
    
    def assign_cluster_labels(self):
        """
        Adds the DBSCAN cluster labels to the original dataframe.
        """
        self.df['DBSCAN_Cluster'] = self.labels
        return self.df

    def save_labeled_customers(self, output_path='resources\data\processed\segment\customers_with_clusters.csv'):
        labeled_df = self.assign_cluster_labels()
        labeled_df.to_csv(output_path, index=False)
        return output_path

    def get_cluster_sizes(self):
        """
        Returns the number of customers in each cluster (including noise).
        """
        if 'DBSCAN_Cluster' not in self.df.columns:
            self.assign_cluster_labels()
        
        cluster_counts = self.df['DBSCAN_Cluster'].value_counts().sort_index()
        cluster_counts_df = cluster_counts.reset_index()
        cluster_counts_df.columns = ['Cluster', 'Num_Customers']
        return cluster_counts_df    
    
    def get_cluster_summary_json(self):
        if 'DBSCAN_Cluster' not in self.df.columns:
            self.assign_cluster_labels()
        
        df_clusters = self.df[self.df['DBSCAN_Cluster'] != -1]
        cluster_summary = df_clusters.groupby('DBSCAN_Cluster').mean(numeric_only=True).reset_index()
        return cluster_summary.to_dict(orient='records')
    
    def remove_noise_and_retrain(self):
        # Filter out noise
        self.df['DBSCAN_Cluster'] = self.labels
        self.df = self.df[self.df['DBSCAN_Cluster'] != -1]
        
        # Re-align PCA data
        self.x_reduced = self.x_reduced[self.df.index]
        
        # Optionally reset index
        self.df.reset_index(drop=True, inplace=True)

        # Re-run clustering
        self.scale_model()
        self.reduce_dimensions()
        self.apply_dbscan()

    # # #K-means            
    
    # def train_kmeans(self, n_clusters=4):
    #     x_scaled = self.scaler.fit_transform(self.scale_model())
    #     pca = PCA(n_components='mle') 
    #     X_pca = pca.fit_transform(x_scaled)
    #     self.kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, init='k-means++', n_init=10, max_iter=300)
    #     self.kmeans_labels = self.kmeans_model.fit_predict(X_pca)
    #     self.df['KMeans_Cluster'] = self.kmeans_labels

    #     score = silhouette_score(X_pca, self.kmeans_labels)
    #     print(f"KMeans Clustering with k={n_clusters}")
    #     print(f"Silhouette Score: {score:.3f}")
    #     return self.kmeans_labels

    # def get_clustered_df(self):
    #     return self.df
    
    # def summarize_kmeans_clusters(self):
    #     output_path = 'kmeans_cluster_summary.csv'
    #     summary = self.df.groupby('KMeans_Cluster').mean(numeric_only=True)
    #     summary.to_csv(output_path)
    #     return output_path

    # def analyze_kmeans_balance(self):
    #     if self.kmeans_labels is None:
    #         print(" KMeans has not been trained yet.")
    #         return

    #     # Count customers per cluster
    #     cluster_counts = self.df['KMeans_Cluster'].value_counts().sort_index()

    #     # Calculate balance ratio
    #     max_count = cluster_counts.max()
    #     min_count = cluster_counts.min()
    #     balance_ratio = min_count / max_count if max_count else 0

    #     # Display distribution
    #     print("\n KMeans Cluster Distribution:")
    #     print(cluster_counts)
    #     print(f"\n Cluster Balance Ratio: {balance_ratio:.2f}")

    def tune_dbscan(self, X, eps_values, min_samples_values):
        best_score = -1
        best_params = None
        best_labels = None

        for eps in eps_values:
            for min_samples in min_samples_values:
                model = DBSCAN(eps=eps, min_samples=min_samples)
                labels = model.fit_predict(X)

                # Exclude noise for scoring
                if len(set(labels)) > 1 and np.sum(labels != -1) > 0:
                    try:
                        score = silhouette_score(X[labels != -1], labels[labels != -1])
                        if score > best_score:
                            best_score = score
                            best_params = (eps, min_samples)
                            best_labels = labels
                    except:
                        continue

        return best_params, best_score, best_labels

    # def plot_clusters(self):
    #     self.df['DBSCAN_Cluster'] = self.apply_dbscan
    #     plt.figure(figsize=(8, 5))
    #     plt.scatter(self.reduce_dimensions[:, 0], self.reduce_dimensions[:, 1], c=self.apply_dbscan, cmap='plasma', s=30)
    #     plt.title('DBSCAN Clustering (PCA-reduced Data)')
    #     plt.xlabel('PC1')
    #     plt.ylabel('PC2')
    #     plt.colorbar(label='Cluster')
    #     plt.grid(True)
