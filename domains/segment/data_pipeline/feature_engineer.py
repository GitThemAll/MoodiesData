import pandas as pd 
from pandas import DataFrame

class feature_engineering_segmentation:
    df : DataFrame
    df_payment_dummies : DataFrame
    def __init__(self):
        #self.file_path = "Data\\Processed Data\\orders_filled.csv"

        pass
    def order_features(self):
        self.df['Nb Orders'] = df.groupby('Email')['Id'].transform('nunique')
        self.df['Amount Orders'] = df.groupby('Email')['Total'].transform('sum')
        self.df['Avg Amount Orders'] = round(df.groupby('Email')['Total'].transform('mean'),2)
        self.df['Max Amount Orders'] = df.groupby('Email')['Total'].transform('max')
        self.df['Nb items'] = df.groupby('Email')['Lineitem quantity'].transform('sum')
        self.df['Avg Nb items'] = round(df.groupby('Email')['Lineitem quantity'].transform('mean'),0)
        self.df['Avg item amount'] = round(df.groupby('Email')['Lineitem price'].transform('mean'),2)
        self.df['Max item amount'] = df.groupby('Email')['Lineitem price'].transform('max')
    
    def categorize_payment(method): 
        if 'ideal' in method.lower():
            return 'Ideal'
        elif 'bancontact' in method.lower():
            return 'Bancontact'
        elif 'credit' in method.lower():
            return 'Card'
        elif 'kaart' in method.lower():
            return 'Card'
        elif '(card)' in method.lower():
            return 'Card'
        elif 'achteraf betalen' in method.lower():
            return 'Pay Later'
        elif 'betaal later' in method.lower():
            return 'Pay Later'
        elif 'pay later' in method.lower():
            return 'Pay Later'
        elif 'klarna' in method.lower():
            return 'Klarna'
        elif 'shopify payments' in method.lower():
            return 'shopify payments'
        else:
            return 'Other'
    
    def apply_payment_categorization(self):
        self.df['Payment Method New'] = self.df['Payment Method'].apply(self.categorize_payment)

    def payment_dummy_vars(self):
        self.df_payment_dummies = pd.get_dummies(self.df['Payment Method New'], prefix='PayMeth').astype(int)
        # Merge with the original DataFrame
        self.df = pd.concat([self.df, df_payment_dummies], axis=1)

    def group_by_email(self):
        df_payment_dummies_grouped = self.df.groupby('Email')[self.df_payment_dummies.columns].max().reset_index()
        # Merge back with the original DataFrame
        self.df = self.df.drop(columns=self.df_payment_dummies.columns).merge(df_payment_dummies_grouped, on='Email', how='left')
    
    def recent_countrry_per_email(self):
        # Get the most recent row per Email
        latest_info = self.df.loc[self.df.groupby('Email')['Paid at'].idxmax(), ['Email', 'Billing Country', 'Billing City']]
        # Rename columns
        latest_info.rename(columns={'Billing Country': 'Recent Country', 'Billing City': 'Recent City'}, inplace=True)
        # Merge back to the original dataframe to assign recent values
        self.df = self.df.merge(latest_info, on='Email', how='left')
    
    