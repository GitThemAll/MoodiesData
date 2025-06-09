import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

class NPDModel:
    def __init__(self) -> None:
        pass
    """
    Encapsulates the full Next-Purchase-Date pipeline:
      1. Merge features with last-order dates
      2. Split into X/y and train/test, fit & evaluate
      3. Retrain on all data & generate next-purchase predictions
    """
    def execute(self,clean_data: pd.DataFrame, feature_data: pd.DataFrame) -> pd.DataFrame:
        # 1. Prepare inputs: drop stray columns & get last-order dates
        df = self.merge_last_orders(clean_data, feature_data)

        # 2. Train/test split, fit RF, print R²
        rf, X_full = self.train_and_evaluate(df)

        # 3. Predict next-purchase gaps & dates, adjust past predictions
        return self.predict_and_finalize(df, rf, X_full)


    def merge_last_orders(self,clean_data: pd.DataFrame, feature_data: pd.DataFrame) -> pd.DataFrame:
        # Drop unwanted index columns
        feat = feature_data.drop(columns=["Unnamed: 0"], errors="ignore")
        orders = clean_data.drop(columns=["Unnamed: 0"], errors="ignore")

        # Ensure timestamps
        orders["Created at"] = pd.to_datetime(orders["Created at"], utc=True)

        # Reconstruct each customer's last order
        last_orders = (
            orders
            .groupby("Email")["Created at"]
            .last()
            .rename("last_order_date")
            .reset_index()
        )

        # Merge into feature table
        df = feat.merge(last_orders, left_on="email", right_on="Email", how="left")

        if df["last_order_date"].isna().any():
            raise ValueError("Some emails missing last_order_date after merge.")

        return df


    def train_and_evaluate(self,df: pd.DataFrame):
        # Prepare X and y
        DROP = ["target_gap_days", "email", "Email", "last_order_date","avg_interval"]
        X = df.drop(columns=DROP)
        y = df["target_gap_days"].astype(float)

        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Fit
        rf = RandomForestRegressor(
            n_estimators=600,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        rf.fit(X_train, y_train)

        # Evaluate
        train_r2 = r2_score(y_train, rf.predict(X_train))
        test_r2 = r2_score(y_test, rf.predict(X_test))
        print(f"Training R²: {train_r2:.3f}")
        print(f"Test (hold-out) R²: {test_r2:.3f}")

        # Return the trained model and the full-X for later prediction
        X_full = X
        return rf, X_full


    def predict_and_finalize(self,df: pd.DataFrame, rf: RandomForestRegressor, X: pd.DataFrame) -> pd.DataFrame:
        # Predict gap days
        gap_pred = rf.predict(X)
        gap_int = np.round(gap_pred).astype(int)
        df["predicted_days"] = gap_int

        # Compute raw next-purchase dates
        df["predicted_next_purchase_date"] = (
            df["last_order_date"] + pd.to_timedelta(gap_int, unit="D")
        )

        # If prediction falls in the past, reset to today + gap
        today = pd.Timestamp.now(tz="UTC").normalize()
        past_mask = df["predicted_next_purchase_date"] < today

        df.loc[past_mask, "predicted_next_purchase_date"] = (
            today + pd.to_timedelta(df.loc[past_mask, "predicted_days"].round().astype(int), unit="D")
        )
        print(df.columns)

        # Return only the columns we care about
        df["predicted_next_purchase_date"] = df["predicted_next_purchase_date"].dt.date
        return df[["email", "predicted_days",'total_spend', 'avg_order_value', "last_order_date","avg_interval","predicted_next_purchase_date"]]

