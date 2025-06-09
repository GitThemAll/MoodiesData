import pandas as pd 
from pandas import DataFrame
from domains.segment.dbscan_model import dbscan_model
import os

class dbscan_service:

    merged_dataset : DataFrame

    def __init__(self):
        try:
            # Load the dataset
            self.merged_dataset = pd.read_csv('resources/data/processed/segment/order_klav_merge_customerLevel.csv')
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

             # Save cluster summary
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

    def get_cluster_distribution_summary(self):
        try:
            summary_path = os.path.join(
                "customers_with_clusters.csv"
            )
            if not os.path.exists(summary_path):
                return {"status": "error", "message": "Customer cluster data not found."}

            df = pd.read_csv(summary_path)
            cluster_counts = df['DBSCAN_Cluster'].value_counts(normalize=True).sort_index() * 100

            label_map = {
                0: "NL Dormant Value Buyers",
                1: "Low-Intent Pay-Later Shoppers",
                2: "Highly Engaged Dutch Customers",
                3: "Inactive Belgian Shoppers"
            }

            color_map = {
                "NL Dormant Value Buyers": "#8ecae6",
                "Low-Intent Pay-Later Shoppers": "#f9c74f",
                "Highly Engaged Dutch Customers": "#219ebc",
                "Inactive Belgian Shoppers": "#ffb703"
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

    def get_avg_items_per_cluster(self):
        try:
            file_path = os.path.join(
                "resources", "data", "processed", "segment", "customers_with_clusters.csv"
            )
            if not os.path.exists(file_path):
                return {"status": "error", "message": "Customer cluster data not found."}

            df = pd.read_csv(file_path)
            grouped = df.groupby("DBSCAN_Cluster")["Nb items"].mean().reset_index()

            cluster_labels = {
                0: "NL Dormant Value Buyers",
                1: "Low-Intent Pay-Later Shoppers",
                2: "Highly Engaged Dutch Customers",
                3: "Inactive Belgian Shoppers"
            }

            data = []
            for _, row in grouped.iterrows():
                cluster_id = int(row["DBSCAN_Cluster"])
                label = cluster_labels.get(cluster_id, f"Cluster {cluster_id}")
                data.append({
                    "label": label,
                    "avg_items": round(row["Nb items"], 2)
                })

            return {"status": "success", "data": data}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_cluster_distribution_by_city(self):
        try:
            file_path = os.path.join(
                "resources", "data", "processed", "segment", "customers_with_clusters.csv"
            )
            if not os.path.exists(file_path):
                return {"status": "error", "message": "Clustered customer data not found."}

            df = pd.read_csv(file_path)

            city_columns = [
                "Recent City_amersfoort",
                "Recent City_amsterdam",
                "Recent City_den haag",
                "Recent City_rotterdam",
                "Recent City_utrecht"
            ]

            cluster_labels = {
                0: "NL Dormant Value Buyers",
                1: "Low-Intent Pay-Later Shoppers",
                2: "Highly Engaged Dutch Customers",
                3: "Inactive Belgian Shoppers"
            }

            city_cluster_counts = []

            for city_col in city_columns:
                city_name = city_col.replace("Recent City_", "").replace("_", " ").title()
                city_df = df[df[city_col] == 1]

                cluster_counts = city_df["DBSCAN_Cluster"].value_counts().to_dict()

                entry = {"city": city_name}
                for cluster_id, label in cluster_labels.items():
                    entry[label] = cluster_counts.get(cluster_id, 0)
                city_cluster_counts.append(entry)

            return {"status": "success", "data": city_cluster_counts}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_cluster_distribution_by_country(self):
        try:
            file_path = os.path.join(
                "resources", "data", "processed", "segment", "customers_with_clusters.csv"
            )
            if not os.path.exists(file_path):
                return {"status": "error", "message": "Clustered customer data not found."}

            df = pd.read_csv(file_path)

            # Define one-hot encoded country columns
            country_columns = [
                "Recent Country_nl",
                "Recent Country_be"
            ]

            # Updated label map
            cluster_labels = {
                0: "NL Dormant Value Buyers",
                1: "Low-Intent Pay-Later Shoppers",
                2: "Highly Engaged Dutch Customers",
                3: "Inactive Belgian Shoppers"
            }

            country_cluster_counts = []

            for country_col in country_columns:
                country_name = country_col.replace("Recent Country_", "").upper()
                country_df = df[df[country_col] == 1]

                cluster_counts = country_df["DBSCAN_Cluster"].value_counts().to_dict()

                entry = {"country": country_name}
                for cluster_id, label in cluster_labels.items():
                    entry[label] = cluster_counts.get(cluster_id, 0)
                country_cluster_counts.append(entry)

            return {"status": "success", "data": country_cluster_counts}

        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    def get_cluster_dashboard_cards(self):
        try:
            file_path = os.path.join(
                "resources", "data", "processed", "segment", "customers_with_clusters.csv"
            )
            if not os.path.exists(file_path):
                return {"status": "error", "message": "Customer cluster data not found."}

            df = pd.read_csv(file_path)

            cluster_labels = {
                0: "NL Dormant Value Buyers",
                1: "Low-Intent Pay-Later Shoppers",
                2: "Highly Engaged Dutch Customers",
                3: "Inactive Belgian Shoppers"
            }

            results = []
            grouped = df.groupby("DBSCAN_Cluster")

            for cluster_id, group in grouped:
                label = cluster_labels.get(cluster_id, f"Cluster {cluster_id}")
                customer_count = len(group)
                total_revenue = group["Amount Orders"].sum()

                # Prevent division by zero
                accepted_marketing = group["Accepts Marketing"].sum()
                total_clicks = group["click"].sum()

                if accepted_marketing > 0:
                    conversion_rate = total_clicks / accepted_marketing
                else:
                    conversion_rate = 0.0

                results.append({
                    "label": label,
                    "customer_count": customer_count,
                    "total_revenue": f"${int(total_revenue):,}",
                    "conversion_rate": f"{round(conversion_rate * 100, 1)}%"
                })

            return {"status": "success", "data": results}

        except Exception as e:
            return {"status": "error", "message": str(e)}