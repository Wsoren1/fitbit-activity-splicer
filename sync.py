import pandas as pd
import os 
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

tz_region = os.environ.get("timezone")

# GOAL: move all data in the takeout folder and enter it into a singular csv table, preprocessed as imports.  Converts to EST, which could be in a config file

working_dir = os.environ.get('source_dir')

def process_file(fpath):

    data_import = pd.read_csv(fpath)

    data_import['timestamp'] = pd.to_datetime(data_import['timestamp'])
    data_import['timestamp'] = data_import['timestamp'].dt.tz_convert(tz_region)

    data_import['date'] = data_import['timestamp'].dt.date

    return data_import

agg_data = pd.DataFrame()

for fname in os.listdir(working_dir):
    if '.csv' in fname and 'heart_rate_' in fname and 'variability' not in fname:
        processed_data = process_file(f'{working_dir}/{fname}')
        agg_data = pd.concat([agg_data, processed_data], ignore_index=True)

agg_data.to_csv('data/imports/processed_HR.csv')
