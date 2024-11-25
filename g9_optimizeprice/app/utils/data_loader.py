# Script to load and preprocess data
import os
import pandas as pd
import json
from datetime import datetime

class DataLoader:
    def __init__(self, path) -> None:
        self.path = path
        self.data = self.load_data(path)

    def load_data(self, path):
        """
        Load data from path
        :param path: path to data
        :return: pandas dataframe
        """
        try:
            return pd.read_csv(path)
        except FileNotFoundError:
            print(f"File not found: {path}")
            return None
    
    def pre_process_travel_data(self, data):
        """
        Pre-process travel data
        :param data: pandas dataframe
        :return: pandas dataframe
        """
        data['startDate'] = pd.to_datetime(data['startDate'], unit='s')
        data['endDate'] = pd.to_datetime(data['endDate'], unit='s')
        data['day_of_week'] = data['startDate'].dt.dayofweek
        data['hour_of_day'] = data['startDate'].dt.hour
        data['month'] = data['startDate'].dt.month-1
        
        return data
        
    
