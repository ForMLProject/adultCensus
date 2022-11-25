import yaml
from adult.exception import AdultException
from adult.constant import *
import os, sys
import pandas as pd
import dill

def read_yaml_file(file_path:str)->dict:
    """
    Reads a YAML file and returns the contents as a dictionary.
    file_path: str
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise AdultException(e,sys) from e

def load_data(file_path:str, schema_file_path:str)-> pd.DataFrame:
    try:
        schema_file = read_yaml_file(schema_file_path)
        schema_cols = schema_file[SCHEMA_COLUMNS_KEY]

        df = pd.read_csv(file_path)
        error_message = ""

        for col in df.columns:
            if col in list(schema_cols):
                df[col].astype(schema_cols[col])

            else:
                error_message = f"{[col]} is not in the schema"

        if len(error_message) > 0:
            raise Exception(error_message)

        return df
    except Exception as e:
        raise AdultException(e,sys) from e


