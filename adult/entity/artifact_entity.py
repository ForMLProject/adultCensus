from collections import namedtuple

DataIngestionArtifact = namedtuple("DataIngestionArtifact", 
                                    ["train_data_path","test_data_path","is_ingested","message"])

DataValidationArtifact = namedtuple("DataValidationArtifact",
                                    ["schema_file_path","report_file_path","report_page_file_path","is_validated","message"])

DataTransformationArtifact = namedtuple("DataTransformationArtifact",
                                        ["transformed_train_data_path", "transformed_test_data_path", "is_transformed", "preprocessed_file_path"])
