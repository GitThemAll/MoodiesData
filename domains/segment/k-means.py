 #K-means
        # self.train_kmeans()
        # self.summarize_kmeans_clusters()
        # self.analyze_kmeans_balance()

# def apply_hdbscan(self, min_cluster_size=15, min_samples=10):
    #     clusterer = hdbscan.HDBSCAN(
    #         min_cluster_size=min_cluster_size,
    #         min_samples=min_samples,
    #         metric='euclidean',
    #         prediction_data=True
    #     )
    #     self.labels = clusterer.fit_predict(self.x_reduced)
    #     self.df['HDBSCAN_Cluster'] = self.labels
    #     return self.labels
    
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