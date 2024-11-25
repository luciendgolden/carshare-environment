import pandas as pd
import numpy as np
from hmmlearn import hmm

def train_hmm_models(file_path):
    # Define mappings
    customer_mapping = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6:6, 7:7}
    pred_demand_mapping = {'high': 0, 'stable': 1, 'low': 2}
    weather_mapping = {'rainy': 0, 'cloudy': 1, 'sunny': 2}

    column_names = ["customer_rating", "pred_demand", "weather"]
    df = pd.read_csv(file_path, header=None, names=column_names)

    df['customer_rating'] = df['customer_rating'].map(customer_mapping)
    df['pred_demand'] = df['pred_demand'].map(pred_demand_mapping)
    df['weather'] = df['weather'].map(weather_mapping)

    column_lists = [df[column].tolist() for column in df.columns]


    # Initialize lists for models and processed columns
    models = []
    columns = []

    # Train a model for each column
    for column_data in column_lists:
        column_data = np.array(column_data).reshape(-1, 1)
        columns.append(column_data)
        
        lengths = [len(column_data)]
        
        #model = hmm.GaussianHMM(n_components=2, n_iter=100)
        model = hmm.CategoricalHMM(n_components=3, n_iter=100)
        model.fit(column_data, lengths)
        models.append(model)

    return models, columns
