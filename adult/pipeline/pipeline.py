import pandas as pd
import numpy as np
from adult.util.util import read_yaml_file, load_data, save_numpy_array_data, save_object
from adult.config import configuration
from adult.constant import *
from adult.components.data_ingestion import data_ingestion_component
from adult.components.data_validation import data_validation_component
from adult.components.data_transformation import data_transformation_component
from adult.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from adult.logger import logging
from adult.exception import AdultException
import sys

class pipeline:
    def __init__(self, config: configuration) -> None:
        try:
            self.pipeline_config = config
        except Exception as e:
            raise AdultException(e,sys) from e
        
    def start_data_ingestion(self)-> DataIngestionArtifact:
        try:
            logging.info(f"starting data ingestion at pipeline level")
            data_ingestion = data_ingestion_component(data_ingestion_config=self.pipeline_config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise AdultException(e,sys) from e

    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            logging.info(f"starting data validation at pipeline level")
            data_validation = data_validation_component(data_ingestion_artifact=data_ingestion_artifact,
                                                        data_validation_config=self.pipeline_config.get_data_validation_config())
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise AdultException(e,sys) from e

    def start_data_transformation(self, data_ingestion_artifact:DataIngestionArtifact, data_validation_artifact: DataValidationArtifact)->DataTransformationArtifact:
        try:
            logging.info(f"starting data transformation at pipeline level")
            data_transformation = data_transformation_component(data_ingestion_artifact=data_ingestion_artifact,
                                                                data_validation_artifact=data_validation_artifact,
                                                                data_transformation_config=self.pipeline_config.get_data_transformation_config())
            return data_transformation

        except Exception as e:
            raise AdultException(e,sys) from e

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                                        data_validation_artifact=data_validation_artifact)
        except Exception as e:
            raise AdultException(e,sys) from e

    def run(self):
        try:
            self.run_pipeline()
        except Exception as e:
            raise AdultException(e,sys) from e


        