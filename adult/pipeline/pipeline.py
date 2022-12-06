import pandas as pd
import numpy as np
from adult.util.util import read_yaml_file, load_data, save_numpy_array_data, save_object
from adult.config import configuration
from adult.constant import *
from adult.components.data_ingestion import data_ingestion_component
from adult.components.data_validation import data_validation_component
from adult.components.data_transformation import data_transformation_component
from adult.components.model_trainer import model_trainer
from adult.components.model_evaluation import model_evaluation
from adult.components.model_pusher import ModelPusher
from adult.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelEvaluationArtifact, ModelPusherArtifact, ModelTrainerArtifact
from adult.logger import logging
from adult.exception import AdultException
from datetime import datetime
import sys, os

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
            return data_transformation.initiate_data_transformation()

        except Exception as e:
            raise AdultException(e,sys) from e

    def start_model_training(self, data_transformation_artifact:DataTransformationArtifact):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            model_training = model_trainer(data_transformation_artifact=self.data_transformation_artifact,
                                            model_trainer_config=self.pipeline_config.get_model_training_config())
            return model_training
        except Exception as e:
            raise AdultException(e,sys) from e
#we take them as inputs because attributes inside them are needed to call the evaluation function and it is likewise for all the function inputs in this project
    def start_model_evaluation(self, data_ingestion_artifact:DataIngestionArtifact, data_validation_artifact: DataValidationArtifact, model_trainer_artifact:ModelTrainerArtifact)->ModelEvaluationArtifact: 
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact

            ModelEvaluation = model_evaluation(data_ingestion_artifact=self.data_ingestion_artifact,
                                                data_validation_artifact=self.data_validation_artifact,
                                                model_trainer_artifact=self.model_trainer_artifact,
                                                model_evaluation_config=self.pipeline_config.get_model_evaluation_config)
            return ModelEvaluation
        except Exception as e:
            raise AdultException(e,sys) from e

    def start_model_pusher(self, model_evaluation_artifact: ModelEvaluationArtifact):
        try:
            self.model_evaluation_artifact = model_evaluation_artifact
            model_pusher = ModelPusher(model_pusher_config=self.pipeline_config.get_model_pusher_config(),
                                        model_evaluation_artifact=self.model_evaluation_artifact)
            return model_pusher
        except Exception as e:
            raise AdultException(e,sys) from e

        

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                                        data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_training(data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifact,
                                                                    data_validation_artifact=data_validation_artifact,
                                                                    model_trainer_artifact=model_trainer_artifact)
            
            model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)
                

        except Exception as e:
            raise AdultException(e,sys) from e

    def run(self):
        try:
            self.run_pipeline()
        except Exception as e:
            raise AdultException(e,sys) from e


        