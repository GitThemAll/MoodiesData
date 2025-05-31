import pandas as pd
class clean:
    file_path : str
    def __init__(self):
        self.file_path = "Data\\Processed Data\\orders_filled.csv"
        pass
    def columns_to_keep():                
        return ['Name', 'Email', 'Paid at', 'Accepts Marketing', 'Shipping', 'Total','Discount Amount', 'Lineitem quantity',
       'Lineitem name', 'Lineitem price', 'Lineitem sku', 'Billing City','Billing Country', 'Payment Method', 'Id']   
    
    def read_dataset(self):
        df = pd.read_csv(self.file_path, delimiter=",", quotechar='"', encoding="utf-8", low_memory=False)
        return df[self.columns_to_keep] 
     
    def drop_paid_dates_at_migration_time(self, df): # MU migrated woocommerce data end of feb so all woocommerce orders are assigned to one day in shopify
        # Ensure 'Paid at' is in datetime format
        df['Paid at'] = pd.to_datetime(df['Paid at'], utc=True, errors='coerce')
        cutoff = pd.Timestamp('2024-03-01', tz='UTC')
        # Filter: Keep rows where 'Paid at' is after Feb 2024
        df = df[df['Paid at'] >= cutoff]
        return df
    
    
    
