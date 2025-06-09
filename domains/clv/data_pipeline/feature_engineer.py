import ast
from datetime import datetime, date
from pandas import DataFrame
import pandas as pd

class CLVFeatureEngineer:

    def __init__(self):
        pass
    
    ## step 8
    def combine_data(self, orders_df: DataFrame, klaviyo_df: DataFrame) -> DataFrame:
        merged_df = pd.merge(
            orders_df,
            klaviyo_df,
            on="Email",
            how="left"
        )
        return merged_df

    ## orders data feature engineering pipeline
    def feature_engineer_orders_data(self, orders_df: DataFrame, cutoff_date: datetime) -> DataFrame:
        cutoff_ts = pd.to_datetime(cutoff_date)
        tz = orders_df["Created at"].dt.tz
        if tz is not None:
            cutoff_ts = cutoff_ts.tz_localize(tz)

        summarized_line_items = self._summarize_orders(orders_df)
        orders_df = self._make_orders_one_raw_per_customer(summarized_line_items, cutoff_ts)
        return orders_df

    ## step 4
    def _summarize_orders(self, orders_df: DataFrame) -> DataFrame:
        def summarize_lineitems(items):
            discounted_items = [item for item in items if item["price"] < 0]
            regular_items = [item for item in items if item["price"] >= 0]

            discount_item_applied = len(discounted_items) > 0
            discount_item_value = sum(item["price"] for item in discounted_items)

            total_qty = sum(item["qty"] for item in regular_items)
            avg_item_price = (
                sum(item["qty"] * item["price"] for item in regular_items) / total_qty
                if total_qty > 0 else 0
            )

            return pd.Series({
                "total_qty": total_qty,
                "avg_item_price": avg_item_price,
                "discount_item_applied": discount_item_applied,
                "discount_item_value": discount_item_value
            })

        orders_df["Lineitems"] = orders_df["Lineitems"].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) else x
        )
        lineitem_summary = orders_df["Lineitems"].apply(summarize_lineitems)
        orders_df = pd.concat([orders_df, lineitem_summary], axis=1)
        orders_df.drop(columns=["Lineitems"], inplace=True)
        return orders_df
    
    ## step 5
    def _make_orders_one_raw_per_customer(self, orders_df: DataFrame, cutoff_date: pd.Timestamp) -> DataFrame:

        df_pre_cutoff = orders_df[orders_df["Created at"] < cutoff_date]
        orders_df["year_month"] = orders_df["Created at"].dt.to_period("M").astype(str)

        # Aggregate monthly metrics
        monthly_agg = orders_df.groupby(["Email", "year_month"]).agg(
            total_spent=("Total", "sum"),
            total_discount_amount=("Discount Amount", "sum"),
            total_refunded_amount=("Refunded Amount", "sum"),
            total_item_quantity=("total_qty", "sum"),
            avg_item_price=("avg_item_price", "mean"),
            discount_item_applied=("discount_item_applied", "max"),
            discount_item_value=("discount_item_value", "sum"),
            total_amount_of_orders=("Name", "nunique"),
            avg_order_value=("Total", "mean")
        ).reset_index()

        monthly_agg["average_item_qty_per_order"] = (
            monthly_agg["total_item_quantity"] / monthly_agg["total_amount_of_orders"]
        )

        # Pivot to wide format (Email as row index)
        monthly_pivot = monthly_agg.pivot(index="Email", columns="year_month")
        monthly_pivot.columns = [f"{metric}_{month}" for metric, month in monthly_pivot.columns]

        # Fix discount boolean columns
        discount_cols = [col for col in monthly_pivot.columns if "discount_item_applied" in col]
        monthly_pivot[discount_cols] = monthly_pivot[discount_cols].fillna(False).astype(bool)

        # Aggregate customer lifetime metrics
        lifetime_agg = df_pre_cutoff.groupby("Email").agg(
            lifetime_amount_items_pre_cutoff=("total_qty", "sum"),
            lifetime_amount_orders_pre_cutoff=("Name", "nunique"),
            lifetime_avg_order_value_pre_cutoff=("Total", "mean")
        ).reset_index()

        # Pre-2025 customer behavioral flags
        customer_flags = df_pre_cutoff.groupby("Email").agg(
            first_order_date_pre_cutoff=("Created at", "min"),
            last_order_date_pre_cutoff=("Created at", "max"),
            pre_cutoff_order_count=("Name", "nunique")
        ).reset_index()

        customer_flags["is_recurring_customer_pre_cutoff"] = customer_flags["pre_cutoff_order_count"] > 1
        customer_flags["days_since_last_order_pre_cutoff"] = (cutoff_date - customer_flags["last_order_date_pre_cutoff"]).dt.days
        customer_flags["days_since_first_order_pre_cutoff"] = (cutoff_date - customer_flags["first_order_date_pre_cutoff"]).dt.days

        # Combine all features
        final_df = monthly_pivot.reset_index()
        final_df = final_df.merge(lifetime_agg, on="Email", how="left")
        final_df = final_df.merge(
            customer_flags[["Email", "is_recurring_customer_pre_cutoff", "days_since_last_order_pre_cutoff", "days_since_first_order_pre_cutoff"]],
            on="Email", how="left"
        )

        # Fill missing values due to no pre-2025 history
        final_df["is_recurring_customer_pre_cutoff"] = final_df["is_recurring_customer_pre_cutoff"].fillna(False).astype(bool)
        final_df["days_since_last_order_pre_cutoff"] = final_df["days_since_last_order_pre_cutoff"].fillna(9999).astype(int)
        final_df["days_since_first_order_pre_cutoff"] = final_df["days_since_first_order_pre_cutoff"].fillna(9999).astype(int)
        return final_df

    ## klaviyo data feature engineering pipeline
    def feature_engineer_klaviyo_data(self, klaviyo_df: DataFrame, cutoff_date: datetime) -> DataFrame:
        cutoff_ts = pd.to_datetime(cutoff_date)
        dates_are_days_df = self._make_dates_days_since(klaviyo_df, cutoff_ts)
        return dates_are_days_df
    
    ## step 7
    def _make_dates_days_since(self, klaviyo_df: DataFrame, reference_date: pd.Timestamp) -> DataFrame:
        klaviyo_df["_days_since_first_active"] = (reference_date - klaviyo_df["First Active"]).dt.days
        klaviyo_df["_days_since_last_active"] = (reference_date - klaviyo_df["Last Active"]).dt.days
        klaviyo_df["_days_profile_created_on"] = (reference_date - klaviyo_df["Profile Created On"]).dt.days
        klaviyo_df["_days_date_added"] = (reference_date - klaviyo_df["Date Added"]).dt.days
        klaviyo_df["_days_since_last_open"] = (reference_date - klaviyo_df["Last Open"]).dt.days
        klaviyo_df["_days_since_last_click"] = (reference_date - klaviyo_df["Last Click"]).dt.days

        # Handle missing values
        klaviyo_df["_days_since_first_active"].fillna(9999, inplace=True)
        klaviyo_df["_days_since_last_active"].fillna(9999, inplace=True)
        klaviyo_df["_days_profile_created_on"].fillna(9999, inplace=True)
        klaviyo_df["_days_date_added"].fillna(9999, inplace=True)
        klaviyo_df["_days_since_last_open"].fillna(9999, inplace=True)
        klaviyo_df["_days_since_last_click"].fillna(9999, inplace=True)

        # One-hot encode Email Marketing Consent
        klaviyo_df = pd.get_dummies(
            klaviyo_df,
            columns=["Email Marketing Consent"],
            prefix="email_consent"
        )


        time_columns = [
            "_days_since_first_active", "_days_since_last_active", 
            "_days_profile_created_on", "_days_date_added",
            "_days_since_last_open", "_days_since_last_click"
        ]

        ## this is to ensure no negative values in time deltas because negative values are dates in the future meaning a data leakage
        for col in time_columns:
            klaviyo_df[col] = klaviyo_df[col].clip(lower=0)

        # Final columns to keep: email, engineered features, and encoded consent flags
        final_columns = ["Email", "_days_since_first_active", "_days_since_last_active", "_days_since_last_open", "_days_since_last_click", "_days_profile_created_on", "_days_date_added" ] + \
                        [col for col in klaviyo_df.columns if col.startswith("email_consent_")]

        return klaviyo_df[final_columns]
    