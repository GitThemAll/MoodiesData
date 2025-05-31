import pandas as pd 
from pandas import DataFrame

class feature_engineering_segmentation:
    df : DataFrame
    df_payment_dummies : DataFrame

    def __init__(self):
        #self.file_path = "Data\\Processed Data\\orders_filled.csv"

        pass
    def order_features(self):
        self.df['Nb Orders'] = self.df.groupby('Email')['Id'].transform('nunique')
        self.df['Amount Orders'] = self.df.groupby('Email')['Total'].transform('sum')
        self.df['Avg Amount Orders'] = round(self.df.groupby('Email')['Total'].transform('mean'),2)
        self.df['Max Amount Orders'] = self.df.groupby('Email')['Total'].transform('max')
        self.df['Nb items'] = self.df.groupby('Email')['Lineitem quantity'].transform('sum')
        self.df['Avg Nb items'] = round(self.df.groupby('Email')['Lineitem quantity'].transform('mean'),0)
        self.df['Avg item amount'] = round(self.df.groupby('Email')['Lineitem price'].transform('mean'),2)
        self.df['Max item amount'] = self.df.groupby('Email')['Lineitem price'].transform('max')
    
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
        self.df = pd.concat([self.df, self.df_payment_dummies], axis=1)

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
    
    def has_discount_column(self):
        self.df['Has Discount'] = self.np.where(self.df['Discount Amount'] > 0, 1, 0)
        # Condition 1: Total is 0 OR Condition 2: Total > Discount Amount, # Assign 1 if either condition is met, # Otherwise, compute the discount percentage
        self.df['Discount Per'] = self.np.where((self.df['Total'] == 0) | (self.df['Total'] < self.df['Discount Amount']), 1, round(self.df['Discount Amount'] / self.df['Total'],2))
        self.df['Free Shipping'] = self.np.where(self.df['Shipping'] == 0, 1, 0)
        self.df['Always Discount'] = self.df.groupby('Email')['Has Discount'].transform(lambda x: int((x == 1).all()))
        self.df['Always Free Shipping'] = self.df.groupby('Email')['Free Shipping'].transform(lambda x: int((x == 1).all()))
        self.df['Never Discount'] = self.df.groupby('Email')['Has Discount'].transform(lambda x: int((x == 0).all()))
        self.df['Never Free Shipping'] = self.df.groupby('Email')['Free Shipping'].transform(lambda x: int((x == 0).all()))
        self.df['Max Discount Percentage'] = self.df.groupby('Email')['Discount Per'].transform('max')

    def sku_list(self):
        df_SKU = self.df.groupby('Email', as_index=False).agg({'Lineitem sku': list})
        df_SKU.rename(columns={'Lineitem sku': 'List SKU'}, inplace=True)
        #check if sku apear more than once
        df_SKU['Same SKU more than once'] = df_SKU['List SKU'].apply(lambda x: any(x.count(sku) > 1 for sku in set(x)))
        df_SKU['Same SKU more than once'] = df_SKU['Same SKU more than once'].astype(int)
        #merge with original 
        self.df = self.df.merge(df_SKU, on='Email', how='left')
    
    def drop_columns(self):
        # Drop to columns
        drop1 = ['Payment Method', 'Lineitem quantity', 'Lineitem name', 'Lineitem price', 'Lineitem sku']
        self.df = self.df.drop(columns=drop1)
        drop2 = ['Name', 'Paid at', 'Accepts Marketing', 'Shipping', 'Total', 'Discount Amount', 'Billing City','Billing Country','Id', 'Days Since today', 'Payment Method New', 'Has Discount', 'Discount Per','Free Shipping']
        self.df = self.df.drop(columns=drop2)

    def group_by_email(self):
        self.df = self.df.groupby('Email', as_index=False).first()

    def top_10_countries(self):
        pass
    def top_10_cities(self):
        pass
    def top_10_skus(self):
        pass
    