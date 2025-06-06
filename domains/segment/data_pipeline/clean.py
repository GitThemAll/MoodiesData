import pandas as pd
from pandas import DataFrame
from datetime import date
import re

#This file clean orders and customers data sets and merge the file to customer level for behaviour analysis
class clean_segmentation: 
    file_path_klaviyo : str
    file_path_filled_orders : str
    file_path_merged : str
    shopify_df : DataFrame
    klaviyo_df : DataFrame
    df : DataFrame
    cutoff : pd.Timestamp

    def __init__(self):
        # self.file_path_klaviyo = "resources\data\processed\segment\Klaviyo_everyone_email.csv"
        # self.file_path_merged = "shopify_orders_from_mar_2024.csv"
        # self.file_path_filled_orders = "resources\data\processed\segment\orders_filled.csv"
        self.cutoff = pd.Timestamp('2024-03-01', tz='UTC')
        pass

    def set_datasets(self, shopify_data, klaviyo_data):
        self.shopify_df = shopify_data
        self.klaviyo_df = klaviyo_data

    def clean_local_data(self):
        self.fill_na_rows()
        self.read_dataset_columns_to_keep()
        self.drop_paid_dates_at_migration_time()
        self.product_include_discount_fee()
        self.replace_discount_amount_max()
        self.remove_na_lineItem()
        #klaviyo 
        self.clean_klaviyo_local()
        self.merge_klaviyo_orders()
        self.to_csv()

    
    def clean_api_data():
        pass

    def shopify_columns_to_keep(self):                
        return ['Name', 'Email', 'Paid at', 'Accepts Marketing', 'Shipping', 'Total','Discount Amount', 'Lineitem quantity',
               'Lineitem name', 'Lineitem price', 'Lineitem sku', 'Billing City','Billing Country', 'Payment Method', 'Id']   

    def klaviyo_columns_to_keep(self):
        return ['Email', 'Email Marketing Consent',
       'First Active', 'Last Active','Profile Created On', 'Date Added', 'Last Open', 'Last Click',
       'Initial Source','Last Source', 
       'Historic Customer Lifetime Value','Accepts Marketing','Last Purchase Date']

    def fill_na_rows(self):
        # self.shopify_df = pd.read_csv(self.file_path_filled_orders, delimiter=",", quotechar='"', encoding="utf-8", low_memory=False)
        self.shopify_df[self.shopify_df['Email'].notna()]
        self.shopify_df['Email'] = self.shopify_df['Email'].apply(lambda x: x if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', str(x)) else pd.NA)
        self.shopify_df.sort_values(by=['Name', 'Id'])  # Sort by Email and Payment Date
        self.shopify_df.ffill(inplace=True)  # Forward fill missing values   

    def read_dataset_columns_to_keep(self):
        # self.shopify_df = pd.read_csv(self.file_path_filled_orders, delimiter=",", quotechar='"', encoding="utf-8", low_memory=False)
        self.shopify_df = self.shopify_df[self.shopify_columns_to_keep()]
     
    def drop_paid_dates_at_migration_time(self): # MU migrated woocommerce data end of feb so all woocommerce orders are assigned to one day in shopify
        # Ensure 'Paid at' is in datetime format
        self.shopify_df['Paid at'] = pd.to_datetime(self.shopify_df['Paid at'], utc=True, errors='coerce')        
        # Filter: Keep rows where 'Paid at' is after Feb 2024
        self.shopify_df[self.shopify_df['Paid at'] >= self.cutoff]
    
    def product_include_discount_fee(self):
        fee_rows = self.shopify_df['Lineitem name'].str.contains('fee', case=False, na=False)
        # Update values for those rows to add the amount to discount
        self.shopify_df.loc[fee_rows, 'Discount Amount'] += self.shopify_df.loc[fee_rows, 'Lineitem price'].abs()
        self.shopify_df.loc[fee_rows, 'Lineitem quantity'] = 0
        self.shopify_df.loc[fee_rows, 'Lineitem name'] = 'NA'
        self.shopify_df.loc[fee_rows, 'Lineitem sku'] = 'NA'


    def replace_discount_amount_max(self):
        self.shopify_df['Discount Amount'] = self.shopify_df.groupby('Name')['Discount Amount'].transform('max')
    
    def remove_na_lineItem(self):
        self.shopify_df = self.shopify_df[self.shopify_df['Lineitem name'] != 'NA']

    # moved to featuring
    # def accepts_marketing_to_binary(self):
    #     self.df['Accepts Marketing'] = self.df['Accepts Marketing'].map({'yes': 1, 'no': 0})

    # def define_reference_date(self):
    #     reference_date = pd.Timestamp.today().normalize()
    #     self.df['Paid at'] = pd.to_datetime(self.df['Paid at'], errors='coerce').dt.tz_localize(None)
    #     self.df['Days Since today'] = (reference_date - self.df['Paid at']).dt.days
    #     self.df['DaysSinceRecentOrder'] = self.df.groupby('Email')['Days Since today'].transform('min')
    
    #Klaviyo data cleaning 
    def clean_klaviyo_local(self):
        # self.klaviyo_df = pd.read_csv(self.file_path_klaviyo, delimiter=",", quotechar='"', encoding="utf-8", low_memory=False)
        #remove sepecial charecters
        self.klaviyo_df['Email'] = self.klaviyo_df['Email'].apply(lambda x: x if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', str(x)) else pd.NA)
    
    def merge_klaviyo_orders(self):
        self.klaviyo_df = self.klaviyo_df[self.klaviyo_df['Email'].isin(self.klaviyo_df['Email'])]
        #self.klaviyo_df.to_csv("klaviyo_customers_test_merge.csv")

    def klaviyo_fix_date_columns(self):
        date = [
            "First Active",
            "Last Active",
            "Profile Created On",
            "Date Added",
            "Expected Date Of Next Order",
            "First Purchase Date",
            "Last Purchase Date",
            "Last Open",
            "Last Click"
        ]
        for col in date:
            self.klaviyo_df[col] = pd.to_datetime(self.klaviyo_df[col],errors='coerce', utc=True)
            self.klaviyo_df[col] = self.klaviyo_df[col].dt.tz_localize(None)
    
    def klaviyo_drop_columns(self):
        self.klaviyo_df = self.klaviyo_df[self.klaviyo_columns_to_keep()]
        return
    
    def to_csv(self):
        self.shopify_df.to_csv("shopify_cleaned.csv")
        self.klaviyo_df.to_csv("klaviyo_cleaned.csv")
    
