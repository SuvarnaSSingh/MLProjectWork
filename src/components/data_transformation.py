import sys
from dataclass import dataclass 
import os
import numpy as np
import pandas as pd 
from  sklearn.compose import ColumnTransformer 
from  skearn.impute import SimpleImputer 
from sklearn.pipeline import Pipeline
from skearn.preprocessing import OneHotEncoder,StandardScaler

from src.Exception import CustomExpception
from scr.logger imprt Logging 

@dataclass
class DataTranspformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl")

 class DataTransformation:

   def __init__(self):
      self.data_transformation_config=DataTranspformationConfig()


   def get_data_transformer_object(self):
       
       ''' Function responsible for Data trnasformation'''
        try:
           numeical_columns=["writing_score","reading_Score"] 
           categorical_columns=[
            "gender","race_ethnicity",
            "parental_level_of_education",
            "lunch",
            "test_preparation_course"
           ]
           num_pipeline=Pipeline(
            steps=[("imputer",SimpleImputer(stratergy="median")) 
                   ,("scaler",StandardScaler())
                   
                   ]
           )
           cat_pipiline=Pipeline(
           steps=[("imputer",SimpleImputer(stratergy="most_frequent")) ,
                   ("one_hot_Encoder",OneHotEncoder()),
                   ("scaler",StandardScaler())
                            
                   ]
                )
           logging.info(f"Categorical columns":{categorical_columns})
           logging.info(f"Numberical columns":{numeical_columns})
               

            preprocessor=ColumnTransformer(
            [("num_pipeline",num_pipeline,numeical_columns),
            ("cat_pipeline",cat_pipiline,categorical_columns)
            ]
            )
           
          return preprocessor  
        except  Exception as e:
        raise CustomExpception(e,sys)  
   

    def initiate_data_transformation(self,train_data_path,test_data_path):
        try :
         train_df=pd.read_csv(train_data_path)
         test_df=pd.read_csv(test_data_path)
         logging.info("Read train and test data complete") 
         logging.info("Obtaining preprocessing object")
         preprocessing_obj= self.get_data_transformer_object()
         target_column_name="math_score"
         numeical_columns=["writing_score","reading_Score"] 
         input_feature_train_df= train_df.drop(columns=[target_column_name],axis=1)
         target_feature_train_df=train_df[target_column_name]

         input_feature_test_df= test_df.drop(columns=[target_column_name],axis=1)
         target_feature_test_df=test_df[target_column_name]
