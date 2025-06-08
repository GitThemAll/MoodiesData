import pandas as pd 
from pandas import DataFrame
from domains.segment.dbscan_model import dbscan_model
import os

class dbscan_service:

    merged_dataset : DataFrame

    def __init__(self):
        try:
            # Load the dataset
            self.merged_dataset = pd.read_csv('order_klav_merge_customerLevel.csv')
        except FileNotFoundError:
            self.merged_dataset = None

    def train_model(self):
        if self.merged_dataset is None:
            return {
                "status": "error",
                "message": "Dataset not found: 'order_klav_merge_customerLevel.csv'"
            }

        try:
            # Initialize model and train
            model = dbscan_model()
            model.get_dataset_from_file(self.merged_dataset)
            model.train_dbscan_model_seg()

             #Save cluster summary
            output_path = os.path.join(
                "resources", "data", "processed", "segment", "dbscan_cluster_summary.csv"
            )
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            saved_path = model.summarize_clusters(output_path)

            return {
                "status": "success",
                "message": "DBSCAN model trained and cluster summary saved",
                "summary_path": saved_path
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
        
    def get_cluster_summary_json(self):
        """
        Return the cluster summary as a JSON-serializable dictionary for API use.
        """
        try:
            summary_path = os.path.join(
                "dbscan_cluster_summary.csv"
            )

            if not os.path.exists(summary_path):
                return {
                    "status": "error",
                    "message": "Cluster summary not found. Please train the model first."
                }

            df = pd.read_csv(summary_path)
            return {
                "status": "success",
                "data": df.to_dict(orient="records")
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
        
    def get_cluster_distribution_summary(self):
        try:
            summary_path = os.path.join(
                "customers_with_clusters.csv"
            )
            if not os.path.exists(summary_path):
                return {"status": "error", "message": "Customer cluster data not found."}

            df = pd.read_csv(summary_path)
            cluster_counts = df['DBSCAN_Cluster'].value_counts(normalize=True).sort_index() * 100

            # Example mapping (replace with your real segment naming logic)
            label_map = {
                0: "Regular",
                1: "High Value",
                2: "At Risk",
                3: "New"
            }

            color_map = {
                "Regular": "#88cc99",
                "High Value": "#9b8df2",
                "At Risk": "#f8c15c",
                "New": "#ff8c1a"
            }

            distribution = []
            for cluster_id, percent in cluster_counts.items():
                label = label_map.get(cluster_id, f"Cluster {cluster_id}")
                distribution.append({
                    "label": label,
                    "value": round(percent, 2),
                    "color": color_map.get(label, "#ccc")
                })

            return {"status": "success", "data": distribution}

        except Exception as e:
            return {"status": "error", "message": str(e)}
    