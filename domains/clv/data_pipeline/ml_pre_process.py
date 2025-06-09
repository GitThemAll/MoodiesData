import re
from pandas import DataFrame


class CLVModelPreProcess:
    """
    Pre-processing for CLV model: dynamic training and inference pipelines.
    """

    def __init__(self):
        pass

    def _get_month_codes(self, df: DataFrame):
        """
        Extract and sort unique YYYY-MM codes from column names.
        """
        pattern = re.compile(r".+_(\d{4}-\d{2})$")
        codes = sorted({pattern.match(col).group(1)
                        for col in df.columns
                        if pattern.match(col)})
        return codes

    def _get_last_n_month_codes(self, df: DataFrame, n: int):
        """
        Return the last n month codes (most recent).
        """
        codes = self._get_month_codes(df)
        if len(codes) < n:
            raise ValueError(f"Expected at least {n} months, found {len(codes)}")
        return codes[-n:]

    def _get_first_n_month_codes(self, df: DataFrame, n: int):
        """
        Return the first n month codes (oldest).
        """
        codes = self._get_month_codes(df)
        if len(codes) <= n:
            raise ValueError(f"Expected more than {n} months, found {len(codes)}")
        return codes[:n]

    def pre_process_data(
        self,
        data: DataFrame,
        target_variable: str,
        target_amount_of_months: int
    ) -> DataFrame:
        """
        Training pipeline:
        1) detect last 3 month codes dynamically
        2) create target variable by summing spend over those months
        3) drop target months to prevent leakage
        4) rename remaining month-related features to month_1 (most recent), month_2, ...
        """
        df = data.copy()
        # removes the last three month to avoid leakage during training
        target_months = self._get_last_n_month_codes(df, target_amount_of_months)

        df = self._create_target_variable(df, target_variable, target_months)
        df = self._remove_months(df, target_months)
        df = self._rename_month_columns(df)
        return df

    def pre_process_inference_data(
        self,
        data: DataFrame,
        target_amount_of_months: int
    ) -> DataFrame:
        """
        Inference pipeline:
        1) detect first 3 month codes dynamically
        2) drop those oldest months
        3) rename remaining month-related features to month_1 (most recent), month_2, ...
        """
        df = data.copy()
        # removes the first three month so that the models gets the same width data as during training
        drop_months = self._get_first_n_month_codes(df, target_amount_of_months)

        df = self._remove_months(df, drop_months)
        df = self._rename_month_columns(df)
        return df

    def _create_target_variable(
        self,
        df: DataFrame,
        target_variable: str,
        target_months: list
    ) -> DataFrame:
        """
        Sum spend over target_months into target_variable.
        """
        spend_cols = [f"total_spent_{m}" for m in target_months if f"total_spent_{m}" in df.columns]
        df[target_variable] = df[spend_cols].sum(axis=1)
        return df

    def _remove_months(
        self,
        df: DataFrame,
        months: list
    ) -> DataFrame:
        """
        Drop any column containing any of the specified month codes.
        """
        cols_to_keep = [col for col in df.columns if not any(f"_{m}" in col for m in months)]
        return df[cols_to_keep]

    def _rename_month_columns(self, df: DataFrame) -> DataFrame:
        """
        Rename columns ending with _YYYY-MM to _month_{i},
        where month_1 is the most recent, then month_2, etc.
        """
        pattern = re.compile(r"(.+)_(\d{4}-\d{2})$")
        month_cols = [col for col in df.columns if pattern.match(col)]
        codes = sorted({pattern.match(col).group(2) for col in month_cols}, reverse=True)
        code_to_idx = {code: idx+1 for idx, code in enumerate(codes)}
        rename_map = {}
        for col in month_cols:
            metric, code = pattern.match(col).groups()
            idx = code_to_idx[code]
            rename_map[col] = f"{metric}_month_{idx}"
        return df.rename(columns=rename_map)

    def bool_to_int(self, df: DataFrame) -> DataFrame:
        """
        Cast boolean columns to integer (0/1).
        """
        bool_cols = df.select_dtypes(include="bool").columns
        df[bool_cols] = df[bool_cols].astype(int)
        return df
