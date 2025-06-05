import pandas as pd 
from pandas import DataFrame
import numpy as np

class feature_engineering_segmentation:
    df : DataFrame
    df_payment_dummies : DataFrame
    shopify_df : DataFrame
    klaviyo_df : DataFrame

    def __init__(self):
        pass

    def feature_local_data(self):
        self.order_features()
        self.categorize_payment()
        self.apply_payment_categorization()
        self.payment_dummy_vars()
        self.group_by_email()
        self.recent_country_per_email()
        self.has_discount_column()
        self.create_sku_list()
        self.drop_columns()
        self.group_by_email()        
        pass        

    def order_features(self):
        self.shopify_df['Nb Orders'] = self.shopify_df.groupby('Email')['Id'].transform('nunique')
        self.shopify_df['Amount Orders'] = self.shopify_df.groupby('Email')['Total'].transform('sum')
        self.shopify_df['Avg Amount Orders'] = round(self.shopify_df.groupby('Email')['Total'].transform('mean'),2)
        self.shopify_df['Max Amount Orders'] = self.shopify_df.groupby('Email')['Total'].transform('max')
        self.shopify_df['Nb items'] = self.df.groupby('Email')['Lineitem quantity'].transform('sum')
        self.shopify_df['Avg Nb items'] = round(self.shopify_df.groupby('Email')['Lineitem quantity'].transform('mean'),0)
        self.shopify_df['Avg item amount'] = round(self.shopify_df.groupby('Email')['Lineitem price'].transform('mean'),2)
        self.shopify_df['Max item amount'] = self.shopify_df.groupby('Email')['Lineitem price'].transform('max')
    
    def categorize_payment(self, method): 
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
        self.shopify_df['Payment Method New'] = self.shopify_df['Payment Method'].apply(self.categorize_payment)

    def payment_dummy_vars(self):
        self.df_payment_dummies = pd.get_dummies(self.shopify_df['Payment Method New'], prefix='PayMeth').astype(int)
        # Merge with the original DataFrame
        self.shopify_df = pd.concat([self.shopify_df, self.df_payment_dummies], axis=1)

    def group_by_email(self):
        df_payment_dummies_grouped = self.shopify_df.groupby('Email')[self.df_payment_dummies.columns].max().reset_index()
        # Merge back with the original DataFrame
        self.shopify_df = self.shopify_df.drop(columns=self.df_payment_dummies.columns).merge(df_payment_dummies_grouped, on='Email', how='left')
    
    def recent_country_per_email(self):
        # Get the most recent row per Email
        latest_info = self.shopify_df.loc[self.df.groupby('Email')['Paid at'].idxmax(), ['Email', 'Billing Country', 'Billing City']]
        # Rename columns
        latest_info.rename(columns={'Billing Country': 'Recent Country', 'Billing City': 'Recent City'}, inplace=True)
        # Merge back to the original dataframe to assign recent values
        self.shopify_df = self.shopify_df.merge(latest_info, on='Email', how='left')
    
    def has_discount_column(self):
        self.shopify_df['Has Discount'] = self.np.where(self.shopify_df['Discount Amount'] > 0, 1, 0)
        # Condition 1: Total is 0 OR Condition 2: Total > Discount Amount, # Assign 1 if either condition is met, # Otherwise, compute the discount percentage
        self.shopify_df['Discount Per'] = self.np.where((self.shopify_df['Total'] == 0) | (self.shopify_df['Total'] < self.shopify_df['Discount Amount']), 1, round(self.shopify_df['Discount Amount'] / self.shopify_df['Total'],2))
        self.shopify_df['Free Shipping'] = self.np.where(self.shopify_df['Shipping'] == 0, 1, 0)
        self.shopify_df['Always Discount'] = self.shopify_df.groupby('Email')['Has Discount'].transform(lambda x: int((x == 1).all()))
        self.shopify_df['Always Free Shipping'] = self.shopify_df.groupby('Email')['Free Shipping'].transform(lambda x: int((x == 1).all()))
        self.shopify_df['Never Discount'] = self.shopify_df.groupby('Email')['Has Discount'].transform(lambda x: int((x == 0).all()))
        self.shopify_df['Never Free Shipping'] = self.shopify_df.groupby('Email')['Free Shipping'].transform(lambda x: int((x == 0).all()))
        self.shopify_df['Max Discount Percentage'] = self.shopify_df.groupby('Email')['Discount Per'].transform('max')

    def create_sku_list(self):
        df_SKU = self.shopify_df.groupby('Email', as_index=False).agg({'Lineitem sku': list})
        df_SKU.rename(columns={'Lineitem sku': 'List SKU'}, inplace=True)
        #check if sku apear more than once
        df_SKU['Same SKU more than once'] = df_SKU['List SKU'].apply(lambda x: any(x.count(sku) > 1 for sku in set(x)))
        df_SKU['Same SKU more than once'] = df_SKU['Same SKU more than once'].astype(int)
        #merge with original 
        self.shopify_df = self.shopify_df.merge(df_SKU, on='Email', how='left')
    
    def top_10_countries(self):
        pass
    def top_10_cities(self):
        pass
    def top_10_skus(self):
        pass

    def drop_columns(self):
        # Drop to columns
        drop1 = ['Payment Method', 'Lineitem quantity', 'Lineitem name', 'Lineitem price', 'Lineitem sku']
        self.shopify_df = self.shopify_df.drop(columns=drop1)
        drop2 = ['Name', 'Paid at', 'Accepts Marketing', 'Shipping', 'Total', 'Discount Amount', 'Billing City','Billing Country','Id', 'Days Since today', 'Payment Method New', 'Has Discount', 'Discount Per','Free Shipping']
        self.shopify_df = self.shopify_df.drop(columns=drop2)

    def group_by_email(self):
        self.shopify_df = self.shopify_df.groupby('Email', as_index=False).first()

    #klaviyo
    def categorize_source1(source):
        if pd.isna(source):  # If the value is NaN, return NaN
            return np.nan
        source = str(source).lower()  # Convert to lowercase for case-insensitive matching
        if 'google' in source or 'bing' in source or 'yahoo' in source or 'qwant' in source or 'duckduckgo' in source or 'ecosia' in source or 'startpage' in source :
            return 'Search Engin'
        elif 'facebook' in source or 'insta' in source or 'social' in source or 'linkedin' in source or 'pinterest' in source or 'influence' in source or 'youtube' in source or 'tiktok' in source:
            return 'Social Media'
        elif 'direct' in source or 'moodiesundies' in source or 'klarna' in source:
            return 'Direct'
        elif 'klav' in source or 'nieuwsbrief' in source or 'mail' in source:
            return 'Email'
        else:
            return 'Other'

    def categorize_colimns(self):
        self.klaviyo_df['Initial Source New'] = self.klaviyo_df['Initial Source'].apply(self.categorize_source1)
        self.klaviyo_df['Last Source New'] = self.klaviyo_df['Last Source'].apply(self.categorize_source1)

    def consent_mapping():
        return {
            'SUBSCRIBED': 1,
            'UNSUBSCRIBED': 0,
            'NEVER_SUBSCRIBED': 2
        }

    def feature_consent_mapping(self):
        self.klaviyo_df['Email Marketing Consent'] = self.klaviyo_df['Email Marketing Consent'].map(self.consent_mapping)
        self.klaviyo_df['Accepts Marketing'] = self.klaviyo_df['Accepts Marketing'].replace({True: 1, False: 0})

    def click_open_dates_presence(self):
        # Click/ Open if there is a date give value 1
        self.klaviyo_df['click'] = np.where(pd.notna(self.klaviyo_df['Last Click']), 1, 0)
        self.klaviyo_df['open'] = np.where(pd.notna(self.klaviyo_df['Last Open']), 1, 0)
    
    def days_since_reference_date(self):
        reference_date = pd.to_datetime('2025-03-10')
        date2 = ["First Active","Last Active","Profile Created On","Date Added"]
        for col in date2:
            self.klaviyo_df[col] = pd.to_datetime(self.klaviyo_df[col], errors='coerce').dt.tz_localize(None)
            self.klaviyo_df[f'Days since {col}'] = (reference_date - self.klaviyo_df[col]).dt.days
    
    def drop_unrelated_columns(self):
        drop2 = ["First Active","Last Active","Profile Created On","Date Added","Last Open", "Last Purchase Date", "Last Click"]
        self.klaviyo_df = self.klaviyo_df.drop(columns=drop2)
    

    