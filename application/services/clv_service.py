from datetime import date, datetime
import os
import numpy as np
import pandas as pd
from pandas import DataFrame
from domains.clv.data_pipeline.feature_engineer import CLVFeatureEngineer
from domains.clv.data_pipeline.clean import CLVDataCleaner
from domains.clv.data_pipeline.ml_pre_process import CLVModelPreProcess
from domains.clv.two_stage_model import TwoStageCLVModel


class ClvService:
    """
    A service class for handling Customer Lifetime Value (CLV) and serving it to the interface
    """

    orders_data_path = os.path.join("resources", "data", "raw", "clv", "orders")
    klaviyo_data_path = os.path.join("resources", "data", "raw", "clv", "klaviyo")

    clv_data_cleaner: CLVDataCleaner = None
    clv_feature_engineer: CLVFeatureEngineer = None
    clv_model_pre_process: CLVModelPreProcess = None

    reference_date = datetime.today()
    cutoff_date = date(2025, 1, 1)

    model_target_months = ["2025-01", "2025-02", "2025-03"]
    model_target_variable = "CLV_Jan_to_Mar_2025"

    def __init__(self):
        self.clv_data_cleaner: CLVDataCleaner = CLVDataCleaner()
        self.clv_feature_engineer: CLVFeatureEngineer = CLVFeatureEngineer()
        self.clv_model_pre_process: CLVModelPreProcess = CLVModelPreProcess()

    def _load_orders_data(self, from_api=False):
        if from_api:
            raise NotImplementedError("Loading from API not yet implemented.")

        order_files = [
            os.path.join(self.orders_data_path, f)
            for f in os.listdir(self.orders_data_path)
            if f.endswith(".csv")
        ]

        orders_dfs = [pd.read_csv(file) for file in order_files]
        orders_df = pd.concat(orders_dfs, ignore_index=True)
        return orders_df

    def _load_klaviyo_data(self, from_api=False):
        if from_api:
            raise NotImplementedError("Loading from API not yet implemented.")

        klaviyo_files = [
            os.path.join(self.klaviyo_data_path, f)
            for f in os.listdir(self.klaviyo_data_path)
            if f.endswith(".csv")
        ]

        df_list = [pd.read_csv(file) for file in klaviyo_files]
        klaviyo_df = pd.concat(df_list, ignore_index=True)
        return klaviyo_df

    def run_data_pipeline(self):
        orders_df = self._load_orders_data(from_api=False)
        klaviyo_df = self._load_klaviyo_data(from_api=False)
        orders_df.to_csv("raw_orders.csv")

        cleaned_orders = self.clv_data_cleaner.clean_orders_for_training(orders_df)

        cleaned_orders.to_csv("cleaned_orders.csv")
        cleaned_klaviyo = self.clv_data_cleaner.clean_klaviyo_for_training(klaviyo_df)

        feature_engineered_orders = (
            self.clv_feature_engineer.feature_engineer_orders_data(
                cleaned_orders,
                cutoff_date=self.cutoff_date,
            )
        )

        feature_engineered_orders.to_csv("feature_engineered_orders.csv")

        feature_engineered_klaviyo = (
            self.clv_feature_engineer.feature_engineer_klaviyo_data(
                cleaned_klaviyo, reference_date=datetime.today()
            )
        )

        combined_data = self.clv_feature_engineer.combine_data(
            feature_engineered_orders, feature_engineered_klaviyo
        )
        combined_data = self.clv_data_cleaner.fill_missing_values_after_merge(
            combined_data
        )
        combined_data.to_csv("combined.csv")
        pre_processed_data = self.clv_model_pre_process.pre_process_data(
            combined_data,
            target_months=self.model_target_months,
            target_variable=self.model_target_variable,
        )
        
        return pre_processed_data

    def create_models(self, training_data: DataFrame):
        two_stage_model = TwoStageCLVModel(
            training_data=training_data,
            target=self.model_target_variable,
        )
        two_stage_model.train()
        self.two_stage_classifier, self.two_stage_regressor = (
            two_stage_model.load_models()
        )

    def predict(self, customer_data: DataFrame) -> DataFrame:

        # Predict probability of purchase
        prob_buy: np.ndarray = self.two_stage_classifier.predict_proba(customer_data)[
            :, 1
        ]

        # Predict expected spend
        expected_spend: np.ndarray = self.two_stage_regressor.predict(customer_data)

        # Multiply to get expected CLV
        predicted_clv: np.ndarray = prob_buy * expected_spend

        return predicted_clv


clv_service = ClvService()
data = clv_service.run_data_pipeline()
train_model = clv_service.create_models(data)