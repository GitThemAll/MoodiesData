
from typing import List
from pandas import DataFrame


class CLVModelPreProcess:

    def __init__(self):
        pass

    def pre_process_data(self, data: DataFrame, target_months: List[str], target_variable: str) -> DataFrame:
        data_with_target = self._create_target_variable(data, target_variable, target_months)
        data_no_leakage = self._remove_leakage(data_with_target, target_months)
        return data_no_leakage

    ## Step 10
    def _create_target_variable(self, df: DataFrame, target_variable: str, target_months: List[str]):
        df[target_variable] = df[ 
            [
                f"total_spent_{m}"
                for m in target_months
                if f"total_spent_{m}" in df.columns
            ]
        ].sum(axis=1)
        return df

    ## Step 10
    def _remove_leakage(self, df: DataFrame, target_months: List[str]):
        # Remove columns that contain target months to prevent leakage
        df = df[[col for col in df.columns if not any(m in col for m in target_months)]]
        return df

    ## bool_to_int
    def bool_to_int(self, df: DataFrame) -> DataFrame:
        bool_cols = df.select_dtypes(include="bool").columns
        df[bool_cols] = df[bool_cols].astype(int)
        return df