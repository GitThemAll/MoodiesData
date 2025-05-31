import pandas as pd
from pandas import DataFrame
from datetime import date

#This file clean orders and customers data sets and merge the file to customer level for behaviour analysis

class clean_segmentation: 
    file_path : str
    df : DataFrame
    cutoff : pd.Timestamp

    def __init__(self):
        self.file_path = "Data\\Processed Data\\orders_filled.csv"
        self.cutoff = pd.Timestamp('2024-03-01', tz='UTC')
        pass

    def columns_to_keep():                
        return ['Name', 'Email', 'Paid at', 'Accepts Marketing', 'Shipping', 'Total','Discount Amount', 'Lineitem quantity',
       'Lineitem name', 'Lineitem price', 'Lineitem sku', 'Billing City','Billing Country', 'Payment Method', 'Id']   
    
    def read_dataset_columns_to_keep(self):
        self.df = pd.read_csv(self.file_path, delimiter=",", quotechar='"', encoding="utf-8", low_memory=False)
        self.df[self.columns_to_keep] 
     
    def drop_paid_dates_at_migration_time(self): # MU migrated woocommerce data end of feb so all woocommerce orders are assigned to one day in shopify
        # Ensure 'Paid at' is in datetime format
        self.df['Paid at'] = pd.to_datetime(self.df['Paid at'], utc=True, errors='coerce')        
        # Filter: Keep rows where 'Paid at' is after Feb 2024
        self.df[self.df['Paid at'] >= self.cutoff]
    
    def product_include_discount_fee(self):
        fee_rows = self.df['Lineitem name'].str.contains('fee', case=False, na=False)
        # Update values for those rows to add the amount to discount
        self.df.loc[fee_rows, 'Discount Amount'] += self.df.loc[fee_rows, 'Lineitem price'].abs()
        self.df.loc[fee_rows, 'Lineitem quantity'] = 0
        self.df.loc[fee_rows, 'Lineitem name'] = 'NA'
        self.df.loc[fee_rows, 'Lineitem sku'] = 'NA'

    def replace_discount_amount_max(self):
        self.df['Discount Amount'] = self.df.groupby('Name')['Discount Amount'].transform('max')
    
    def remove_na_lineItem(self):
        self.df = self.df[self.df['Lineitem name'] != 'NA']

    def accepts_marketing_to_binary(self):
        self.df['Accepts Marketing'] = self.df['Accepts Marketing'].map({'yes': 1, 'no': 0})

    def define_reference_date(self):
        reference_date = pd.Timestamp.today().normalize()
        self.df['Paid at'] = pd.to_datetime(self.df['Paid at'], errors='coerce').dt.tz_localize(None)
        self.df['Days Since today'] = (reference_date - self.df['Paid at']).dt.days
        self.df['DaysSinceRecentOrder'] = self.df.groupby('Email')['Days Since today'].transform('min')
    
    
