import pandas as pd 
from pandas import DataFrame
from domains.segment.dbscan_model import dbscan_model

class dbscan_service:

    merged_dataset : DataFrame

    def __init__(self):
        self.merged_dataset = pd.read_csv('order_klav_merge_customerLevel.csv')
        pass

    def train_model(self):
        dbscan = dbscan_model()
        dbscan.get_dataset_from_file(self.merged_dataset)
        dbscan.train_dbscan_model_seg()
    pass