import pandas as pd 
from pandas import DataFrame
import numpy as np
from domains.segment.data_pipeline.clean import clean_segmentation
from domains.segment.data_pipeline.feature_engineer import feature_engineering_segmentation

class segment_service:

    shopify_data : DataFrame
    klavioy_data : DataFrame

    def __init__(self):
        self.set_data_static()
        pass

    def set_data_static(self):
        self.shopify_data = pd.read_csv("resources\data\processed\segment\orders_merge.csv")
        self.klavioy_data = pd.read_csv("resources\data\processed\segment\Klaviyo_everyone_email.csv")
    
        #optional return array for sets
        # return {
        #     "shopify": self.shopify_data,
        #     "klaviyo": self.klaviyo_data
        # }
    
    def clean_data_static(self):
        clean_seg = clean_segmentation()
        clean_seg.set_datasets(self.shopify_data, self.klavioy_data)
        clean_seg.clean_local_data()
    
    def feature_data_static(self):
        feature_seg = feature_engineering_segmentation()
        feature_seg.set_datasets(self.shopify_data, self.klavioy_data)
        feature_seg.feature_local_data()
    
