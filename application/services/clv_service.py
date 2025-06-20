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
    Supports both training and inference pipelines via run_data_pipeline().
    """

    orders_data_path = os.path.join("resources", "data", "raw", "clv", "orders")
    klaviyo_data_path = os.path.join("resources", "data", "raw", "clv", "klaviyo")

    two_stage_model: TwoStageCLVModel = None

    def __init__(self):
        self.clv_data_cleaner = CLVDataCleaner()
        self.clv_feature_engineer = CLVFeatureEngineer()
        self.clv_model_pre_process = CLVModelPreProcess()

    def _load_orders_data(self, from_api=False) -> DataFrame:
        if from_api:
            raise NotImplementedError("Loading from API not yet implemented.")

        order_files = [
            os.path.join(self.orders_data_path, f)
            for f in os.listdir(self.orders_data_path)
            if f.endswith(".csv")
        ]
        orders_dfs = [pd.read_csv(file) for file in order_files]
        return pd.concat(orders_dfs, ignore_index=True)

    def _load_klaviyo_data(self, from_api=False) -> DataFrame:
        if from_api:
            raise NotImplementedError("Loading from API not yet implemented.")

        klaviyo_files = [
            os.path.join(self.klaviyo_data_path, f)
            for f in os.listdir(self.klaviyo_data_path)
            if f.endswith(".csv")
        ]
        df_list = [pd.read_csv(file) for file in klaviyo_files]
        return pd.concat(df_list, ignore_index=True)

    def run_data_pipeline(
        self,
        from_api: bool,
        mode: str,  # 'train' or 'inference'
        cutoff_date: date,
        model_target_variable: str,
        target_amount_of_months: int
    ) -> DataFrame:
        """
        Shared data loading & feature engineering, then branched pre-processing.

        mode='train': training pipeline (build target, drop last 3 months).
        mode='inference': inference pipeline (drop first 3 months).
        """
        # Load raw data
        orders_df = self._load_orders_data(from_api)
        klaviyo_df = self._load_klaviyo_data(from_api)

        # Clean
        cleaned_orders = self.clv_data_cleaner.clean_orders_for_training(orders_df)
        cleaned_klaviyo = self.clv_data_cleaner.clean_klaviyo_for_training(klaviyo_df)

        # Feature engineer
        feat_orders = self.clv_feature_engineer.feature_engineer_orders_data(
            cleaned_orders,
            cutoff_date=cutoff_date,
        )
        feat_klaviyo = self.clv_feature_engineer.feature_engineer_klaviyo_data(
            cleaned_klaviyo, cutoff_date=datetime.today()
        )
        combined = self.clv_feature_engineer.combine_data(feat_orders, feat_klaviyo)
        combined = self.clv_data_cleaner.fill_missing_values_after_merge(combined)

        # Branch to appropriate pre-processing
        if mode == "train":
            return self.clv_model_pre_process.pre_process_data(
                combined,
                target_variable=model_target_variable,
                target_amount_of_months=target_amount_of_months,
            )
        elif mode == "inference":
            return self.clv_model_pre_process.pre_process_inference_data(
                combined, target_amount_of_months=target_amount_of_months
            )

    def create_models(
        self, 
        training_data: DataFrame, 
        model_target_variable: str
    ) -> None:
        self.two_stage_model = TwoStageCLVModel(
            training_data=training_data,
            target=model_target_variable,
        )
        self.two_stage_model.train()

    def predict(self, customer_data: DataFrame) -> np.ndarray:
        # Ensure the input data is pre-processed
        return self.two_stage_model.predict(customer_data)

    def get_lifetime_clv(self) -> DataFrame:
        orders_df = self._load_orders_data(from_api=False)
        cleaned_orders = self.clv_data_cleaner.clean_orders_for_training(orders_df)
        lifetime_clv = cleaned_orders.groupby('Email', as_index=False)['Total'].sum()
        lifetime_clv = lifetime_clv.rename(columns={'Total': 'Lifetime CLV'})
        return lifetime_clv
