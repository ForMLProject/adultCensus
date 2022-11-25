from adult.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact
from adult.entity.config_entity import DataTransformationConfig
import numpy as np
import pandas as pd
from adult.constant import *
from adult.util.util import read_yaml_file, load_data
from adult.logger import logging
from adult.exception import AdultException
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
import os,sys

class data_transformation_component:
    def __init__(self, data_ingestion_artifact = DataIngestionArtifact, data_validation_artifact = DataValidationArtifact, data_transformation_config = DataTransformationConfig) -> None:
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise AdultException(e,sys) from e

    def get_transformed_object(self)->ColumnTransformer:
        try: 
            schema_data = self.data_validation_artifact.schema_file_path
            data_schema = read_yaml_file(schema_data)

            num_cols = data_schema[SCHEMA_NUMERICAL_COLUMNS]
            cat_cols = data_schema[SCHEMA_CATEGORICAL_COLUMNS]

            num_pipeline = make_pipeline(SimpleImputer(missing_values=np.nan, strategy="mean"),StandardScaler() )
            cat_pipeline = make_pipeline(SimpleImputer(missing_values=np.nan, strategy="most_frequent"), OneHotEncoder(sparse=False,handle_unknown='ignore'), StandardScaler(with_mean=False))

            logging.info(f"Numerical Columns are {num_cols}")
            logging.info(f"Categorical Columns are {cat_cols}")
            preprocessing = ColumnTransformer([("num_pipeline", num_pipeline(), num_cols),
                                                ("cat_cols", cat_pipeline(), cat_cols)])
            return preprocessing
        except Exception as e:
            raise AdultException(e,sys) from e        
        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info(f"Obtaining preprocessing object")
            

        except Exception as e:
            raise AdultException(e,sys) from e





