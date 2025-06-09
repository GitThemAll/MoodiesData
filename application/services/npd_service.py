# services/npd_service.py
from flask import jsonify
from pathlib import Path
import pandas as pd
from domains.npd.data_pipeline.clean import DataCleanerForNPD
from domains.npd.data_pipeline.feature_engineer import FeatureEngineer
from domains.npd.random_forest_model import NPDModel

class NPDService:
    """Service layer around the NPD prediction pipeline."""

    def __init__(self):
        # build a proper Path object and store it on self
        self.orders_path = Path("./resources/data/raw/npd/orders_export_1.csv")

        # attach all pipeline pieces to self so other methods can see them
        self.data_cleaner_npd = DataCleanerForNPD()
        self.feature_engineer  = FeatureEngineer()
        self.npd_model         = NPDModel()

    def run_pipeline(self) -> pd.DataFrame:
        """Return a DataFrame with one row per customer and a `predicted_days`
        column, executing the three pipeline stages exactly once."""
        # use the instance attributes
        orders_df   = self.data_cleaner_npd.execute(self.orders_path)
        features_df = self.feature_engineer.execute(orders_df)
        return self.npd_model.execute(orders_df, features_df)

    def get_customer_predictions(self):
        """Return full per-customer prediction records (JSON)."""
        result_df = self.run_pipeline()
        return jsonify(result_df.to_dict(orient="records"))

    def get_customer_statistics(self):
        """Return simple summary stats (JSON)."""
        result_df = self.run_pipeline()
        pdays = result_df["predicted_days"]
        stats = {
            "highest_next_purchase_days": int(pdays.max()),
            "lowest_next_purchase_days":  int(pdays.min()),
            "average_next_purchase_days": int(pdays.mean()),
        }
        return jsonify(stats)
