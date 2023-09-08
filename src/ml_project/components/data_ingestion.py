import os
import sys 
from src.ml_project.exception import CustomExceptions
from src.ml_project.logger import logging
import pandas as pd
from src.ml_project.utils import read_sql_data
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

@dataclass
class DataIngestionConfig:
    train_data_path:str = os.path.join('artifacts','train.csv')
    test_data_path:str = os.path.join('artifacts','test.csv')
    raw_data_path:str = os.path.join('artifacts','raw_data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            #Reading the Code from mySQL
            logging.info("Reading data from mysql databases...")
            df = read_sql_data()
            logging.info("Reading completed from mysql databases...")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            df.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            df.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Data Ingestion is completed...")
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomExceptions(e,sys)
        




