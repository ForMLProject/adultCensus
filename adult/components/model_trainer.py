from adult.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact, ModelTrainerArtifact
from adult.entity.config_entity import ModelTrainerConfig
import numpy as np
import pandas as pd
from adult.constant import *
from adult.util.util import read_yaml_file, load_data, save_numpy_array_data, save_object
from adult.logger import logging
from adult.exception import AdultException
import os,sys

class model_trainer:
    def __init__(self, data_transformation_artifact = DataTransformationArtifact,model_trainer_config = ModelTrainerConfig) -> None:
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
            
        except Exception as e:
            raise AdultException(e,sys) from e

        