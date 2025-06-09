import pandas as pd
class DataCleanerForNPD:
    def __init__(self) -> None:
        pass
    def execute(self,raw_data_path: str) -> pd.DataFrame:
        # 1. Load the CSV into a DataFrame
        df = self.load_raw_data(raw_data_path)
        
        # 2. Select only the columns we care about
        df = self.select_columns(df)
        
        # 3. Normalize each column (dates, numeric types, email cleanup)
        df = self.normalize_columns(df)
        
        # 4. Drop rows with missing/empty emails, reset index, format date
        df = self.filter_and_finalize(df)
        
        return df

    def load_raw_data(self,raw_data_path: str) -> pd.DataFrame:
        """
        Read the CSV file.
        """
        return pd.read_csv(raw_data_path)

    def select_columns(self,df: pd.DataFrame) -> pd.DataFrame:
        needed = [
            "Email",
            "Total",
            "Discount Amount",
            "Created at",
            "Lineitem quantity",
            "Lineitem price",
        ]
        return df[needed].copy()

    def normalize_columns(self,df: pd.DataFrame) -> pd.DataFrame:
        """
        1. Convert "Created at" to a UTC timestamp.
        2. Coerce "Total", "Discount Amount", and "Lineitem quantity" into numeric (float/int).
        3. Lowercase & strip whitespace from emails.
        """
        # a) Parse timestamps
        df["Created at"] = pd.to_datetime(df["Created at"], utc=True)

        # b) Convert certain columns to numeric types
        cols_to_numeric = ["Total", "Discount Amount", "Lineitem quantity"]
        for col in cols_to_numeric:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # c) Normalize email column
        df["Email"] = df["Email"].str.lower().str.strip()
        
        return df

    def filter_and_finalize(self,df: pd.DataFrame) -> pd.DataFrame:
        """
        1. Drop rows where Email is missing or empty.
        2. Reset the index so it’s consecutive.
        3. Re-format "Created at" to date‐only (yyyy-mm-dd).
        """
        # a) Keep only rows with a non-empty email
        df = df[df["Email"].notna() & (df["Email"] != "")].copy()
        
        # b) Reset the index
        df.reset_index(drop=True, inplace=True)

        # c) Convert "Created at" from full timestamp to date (yyyy-mm-dd)
        df["Created at"] = pd.to_datetime(df["Created at"].dt.date, format="%Y-%m-%d", utc=True)
        
        return df
