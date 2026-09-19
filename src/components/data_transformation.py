import os     
import sys
import numpy as np   
import pandas as pd              
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.base import BaseEstimator,TransformerMixin
from src.utils import save_object
    
    

@dataclass
class DataTransformerConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl")
 
  
class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformerConfig()
    
    def transform(self,X):
            X=pd.read_csv(X)
            X=X.drop(columns=["TWF","HDF","PWF","OSF","RNF","UDI","Product ID"])
            X["Temp_diff"]=X["Process temperature [K]"]-X['Air temperature [K]']
            X["Power"]=X["Torque [Nm]"]*X["Rotational speed [rpm]"]*(2*np.pi/60)
            X["Wear_risk"]=pd.cut(
            X["Tool wear [min]"],bins=[-1,50,150,250,np.inf],
            labels=["low","medium","high","critical"]
            )
            
            return X
            
    def get_data_transformation(self):
        try:
            numerical_columns=['Air temperature [K]','Process temperature [K]',
                               'Rotational speed [rpm]','Torque [Nm]','Tool wear [min]']
            categorical_colums=["Type","Wear_risk"]
            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy='median')),
                    ("scaler",StandardScaler())
                ]
            )
            logging.info("Numerical column scaling is completed")
            cat_pipeline=Pipeline(
                steps=[
                    ("Imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            logging.info("Categorical and Column encoding  complerted")
            preprocessor=ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_columns),
                    ("cat_pipeline",cat_pipeline,categorical_colums)
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=self.transform(train_path)
            test_df=self.transform(test_path)
            logging.info("Read train and test data Completed")
            logging.info("obtaining preprocessor object")
            preprocessing_obj=self.get_data_transformation()
            target_column="Machine failure"
            numerical_columns=['Air temperature [K]','Process temperature [K]',
                            'Rotational speed [rpm]','Torque [Nm]','Tool wear [min]']
            input_feature_train_df = train_df.drop(columns=[target_column])
            target_feature_train_df = train_df[target_column]

            input_feature_test_df = test_df.drop(columns=[target_column])
            target_feature_test_df = test_df[target_column]

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return train_arr, test_arr, self.data_transformation_config.preprocessor_obj_file_path

        except Exception as e:
            raise CustomException(e, sys)            
            
        
 