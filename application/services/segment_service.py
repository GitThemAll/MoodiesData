import pandas as pd 
from pandas import DataFrame
import numpy as np
from domains.segment.data_pipeline.clean import clean_segmentation
from domains.segment.data_pipeline.feature_engineer import feature_engineering_segmentation

class segment_service:

    shopify_data : DataFrame
    klavioy_data : DataFrame
    shopify_data_path = "resources\data\processed\segment\orders_merge.csv"
    klaviyo_data_path = "resources\data\processed\segment\Klaviyo_everyone_email.csv"
    cleaned_shopify_path = "shopify_cleaned.csv"
    cleaned_klaviyo_path = "klaviyo_cleaned.csv"

    def __init__(self):
        self.set_data_static()
        pass

    def set_data_static(self):
        self.shopify_data = pd.read_csv(self.shopify_data_path, delimiter=",", quotechar='"', encoding="utf-8", low_memory=False)
        self.klavioy_data = pd.read_csv(self.klaviyo_data_path, delimiter=",", quotechar='"', encoding="utf-8", low_memory=False)
        self.cleaned_shopify = pd.read_csv(self.cleaned_shopify_path)
        self.cleaned_klaviyo = pd.read_csv(self.cleaned_klaviyo_path)
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
        feature_seg.set_datasets(self.cleaned_shopify, self.cleaned_klaviyo)
        feature_seg.feature_local_data()
    
