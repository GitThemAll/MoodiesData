import pandas as pd
from typing import List

class FeatureEngineer:
    def __init__(self) -> None:
        pass
    def execute(self,clean_orders: pd.DataFrame) -> pd.DataFrame:
        # 1. Tidy up raw orders (drop unwanted cols, normalize headers, parse timestamps)
        orders = self.prepare_orders(clean_orders)

        # 2. Deduplicate so that one row == one unique order
        orders = self.dedupe_orders(orders)

        # 3. Build per‐customer features (rows of dictionaries)
        features_df = self.build_feature_rows(orders)

        # 4. Fill any missing interval columns with -1 and return
        return self.finalize_features(features_df)


    def prepare_orders(self,df: pd.DataFrame) -> pd.DataFrame:
        """
        - Drop any accidental index column ("Unnamed: 0")
        - Strip whitespace from column names
        - Ensure "Created at" is a UTC timestamp
        """
        df = df.drop(columns=["Unnamed: 0"], errors="ignore")
        df.columns = df.columns.str.strip()
        df["Created at"] = pd.to_datetime(df["Created at"], utc=True)
        return df

    def dedupe_orders(self,orders_raw: pd.DataFrame) -> pd.DataFrame:
        """
        - Sort by Email, then by Created at
        - Drop duplicates so that each (Email, Created at) pair appears only once
        """
        deduped = (
            orders_raw
            .sort_values(["Email", "Created at"])
            .drop_duplicates(subset=["Email", "Created at"])
            .reset_index(drop=True)
        )
        return deduped


    def build_feature_rows(self,orders: pd.DataFrame) -> pd.DataFrame:
        """
        For each email group (in order of first-to-last purchase):
        - Skip customers with fewer than 2 orders
        - Compute:
            * num_orders (excluding their very last order)
            * total_spend (over kept orders)
            * avg_order_value
            * days_since_first_purchase (relative to TODAY)
            * days_since_second_last_purchase (relative to TODAY)
            * target_gap_days (gap between 2nd-last and last order)
            * interval_i_i+1 (gaps between consecutive kept orders, up to MAX_GAPS)
        """
        TODAY = pd.Timestamp.now(tz="UTC").normalize()
        MAX_GAPS = 10

        rows: List[dict] = []
        for email, grp in orders.groupby("Email", sort=False):
            dates = grp["Created at"].sort_values().reset_index(drop=True)

            # 1) Need at least two orders to compute a gap target
            if len(dates) < 2:
                continue

            # 2) target_gap = difference between last and second-last
            target_gap = (dates.iloc[-1] - dates.iloc[-2]).days
            
            # Compute all intervals between consecutive purchases
            all_gaps = dates.diff().dt.days.dropna().tolist()
            avg_interval = sum(all_gaps) / len(all_gaps) if all_gaps else 0

            num_orders = len(dates)
            total_spend = (
                grp.loc[
                    grp["Created at"].isin(dates),
                    "Total"
                ]
                .astype(float)
                .sum()
            )
            avg_order_value = total_spend / num_orders
            

            # 3) Drop the very last order so we avoid leakage
            dates_kept = dates.iloc[:-1]
            days_since_first = (TODAY - dates_kept.iloc[0]).days
            days_since_second_last = (TODAY - dates_kept.iloc[-1]).days

            # 4) Build a list of consecutive‐order gaps (in days)
            gaps = dates_kept.diff().dt.days.dropna().astype("Int64").tolist()
            # Pad or truncate to exactly MAX_GAPS
            gaps = (gaps + [pd.NA] * MAX_GAPS)[:MAX_GAPS]

            # 5) Assemble the single‐row dict
            row = {
                "email": email,
                "num_orders": num_orders,
                "total_spend": total_spend,
                "avg_order_value": avg_order_value,
                "avg_interval": avg_interval,
                "days_since_first_purchase": days_since_first,
                "days_since_second_last_purchase": days_since_second_last,
                "target_gap_days": target_gap,
            }
            # Add interval_1_2, interval_2_3, ..., up to interval_10_11
            for i, gap_val in enumerate(gaps):
                row[f"interval_{i+1}_{i+2}"] = gap_val

            rows.append(row)

        return pd.DataFrame(rows)

    def finalize_features(self,features_df: pd.DataFrame) -> pd.DataFrame:
        """
        - Identify any interval_* columns
        - Replace missing (NA) with -1
        - Return the cleaned DataFrame
        """
        interval_cols = [c for c in features_df.columns if c.startswith("interval_")]
        features_df[interval_cols] = features_df[interval_cols].fillna(-1)
        return features_df
