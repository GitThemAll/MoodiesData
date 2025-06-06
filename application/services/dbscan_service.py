import pandas as pd 
from pandas import DataFrame

class dbscan_service:

    merged_dataset : DataFrame

    def __init__(self):
        self.merged_dataset = pd.read_csv('order_klav_merge_customerLevel.csv')
        pass
    pass