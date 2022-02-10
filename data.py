import json
from flatten_json import flatten
import pandas as pd
from data_update import update_zip_file

DATA_FILE = "./data/vcdb_1-of-1.json"


## Given a specified JSON filename, returns the JSON data contained in the file
def read_json_file(filename):
    f = open(filename, 'r')
    data = json.loads(f.read())
    f.close()
    return data

## Given some JSON data, returns a pandas dataframe object containing the fully flattened version of the provided JSON data
def get_flattened_dataframe(json_data):
    return pd.DataFrame([flatten(d, '.') for d in json_data])

## Provides a pandas dataframe of the flattened JSON data from file
def generate_flattened_dataframe():
    update_zip_file()
    data = read_json_file(DATA_FILE)
    df = get_flattened_dataframe(data)
    return df