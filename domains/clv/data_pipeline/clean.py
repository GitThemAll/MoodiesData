from typing import List
from pandas import DataFrame
import pandas as pd


class CLVDataCleaner:
    """
    Cleans order and Klaviyo data for CLV modeling.
    Applies column selection, normalization, and missing value handling.
    """

    # Class-level constants for column names
    ORDER_COLUMNS: List[str] = [
        "Name", "Email", "Total", "Discount Amount", "Created at",
        "Lineitem quantity", "Lineitem price", "Refunded Amount"
    ]

    KLAVIYO_COLUMNS: List[str] = [
        "Email", "Email Marketing Consent", "First Active", "Last Active",
        "Profile Created On", "Date Added", "Last Open", "Last Click",
        "Predicted Customer Lifetime Value"
    ]

    def __init__(self) -> None:
        pass

    ### Order Data Cleaning Pipeline
    def clean_orders_for_training(self, orders_dataframe: DataFrame) -> DataFrame:
        selected_cols_dataframe = self._select_orders_columns(orders_dataframe)
        normalized_dataframe = self._normalize_orders_data(selected_cols_dataframe)
        combined_orders_dataframe = self._combine_multiple_order_rows(normalized_dataframe)
        return combined_orders_dataframe

    def _select_orders_columns(self, df: DataFrame) -> DataFrame:
        df = df.copy()
        return df[self.ORDER_COLUMNS]

    def _normalize_orders_data(self, df: DataFrame) -> DataFrame:
        df = df.copy()
        df["Created at"] = pd.to_datetime(df["Created at"], format="ISO8601", utc=True)

        cols_to_float: List[str] = [
            "Total", "Discount Amount", "Lineitem quantity", "Lineitem price", "Refunded Amount"
        ]
        for col in cols_to_float:
            df[col] = pd.to_numeric(df[col])

        df["Email"] = df["Email"].str.lower().str.strip()
        df = df[df["Email"].notna() & (df["Email"] != "")]
        return df

    def _combine_multiple_order_rows(self, df: DataFrame) -> DataFrame:
        df = df.copy()
        df["Lineitem_object"] = df.apply(
            lambda row: {
                "qty": int(row["Lineitem quantity"]),
                "price": float(row["Lineitem price"])
            },
            axis=1
        )
        lineitems_grouped = df.groupby(["Name", "Email"])["Lineitem_object"].agg(list).reset_index()
        first_rows = df.drop_duplicates(subset=["Name", "Email"], keep="first")

        merged_orders = pd.merge(
            first_rows.drop(columns=["Lineitem quantity", "Lineitem price", "Lineitem_object"]),
            lineitems_grouped,
            on=["Name", "Email"],
            how="left"
        )
        merged_orders.rename(columns={"Lineitem_object": "Lineitems"}, inplace=True)
        return merged_orders

    ### Klaviyo Data Cleaning Pipeline
    def clean_klaviyo_for_training(self, klaviyo_dataframe: DataFrame) -> DataFrame:
        selected_cols_dataframe = self._select_klaviyo_columns(klaviyo_dataframe)
        normalized_dataframe = self._normalize_klaviyo_data(selected_cols_dataframe)
        return normalized_dataframe

    def _select_klaviyo_columns(self, df: DataFrame) -> DataFrame:
        df = df.copy()
        df = df[self.KLAVIYO_COLUMNS]
        df["Email"] = df["Email"].str.lower().str.strip()
        return df

    def _normalize_klaviyo_data(self, df: DataFrame) -> DataFrame:
        df = df.copy()
        df["Email"] = df["Email"].str.lower().str.strip()
        date_cols = [
            "First Active", "Last Active", "Last Open",
            "Last Click", "Profile Created On", "Date Added"
        ]
        for col in date_cols:
            df[col] = pd.to_datetime(df[col])
        return df

    def fill_missing_values_after_merge(self, df: DataFrame) -> DataFrame:
        df = df.copy()
        fill_defaults = {
            "_days_since_first_active": 9999,
            "_days_since_last_active": 9999,
            "_days_profile_created_on": 9999,
            "_days_date_added": 9999,
            "_days_since_last_open": 9999,
            "_days_since_last_click": 9999,
            "email_consent_NEVER_SUBSCRIBED": False,
            "email_consent_SUBSCRIBED": False,
            "email_consent_UNSUBSCRIBED": False,
        }
        for col, val in fill_defaults.items():
            df[col].fillna(val, inplace=True)
        return df