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
                "resources", "data", "processed", "segment", "dbscan_cluster_summary.csv"
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
    