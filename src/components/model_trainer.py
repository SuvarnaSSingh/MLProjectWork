import os
import sys
from src.exception import CustomException
from src.logger import logging

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from src.utils import save_obj,evaluate_models
from dataclasses import dataclass

from src.components.data_transformation import DataTranspformationConfig,DataTransformation

from src.utils import evaluate_models




@dataclass
class ModelTrainerConfig:
    train_model_file_path =os.path.join("artifacts","model.pkl")

class ModelTrainer:
  def __init__(self):
     self.model_trainer_config=ModelTrainerConfig()

  def initiate_Model_trainer(self,train_arr,test_arr):
     try:
        logging.info("Spliting Training and Test Input Data ")
        X_train,Y_train,X_test,Y_test=(
           train_arr[:,:-1],
           train_arr[:,-1],
           test_arr[:,:-1],
           test_arr[:,-1],
        )

        models={
           "Random Forest":RandomForestRegressor(),
           "Decision Tree" :DecisionTreeRegressor(),
           "Gradient Bossing":GradientBoostingRegressor(),
           "Lineear Regression":LinearRegression(),
           "K-Neightbour Classifier ":KNeighborsRegressor(),
           "XGClassifier":XGBRegressor(),
           "CatBoosting Classifier":CatBoostRegressor(verbose=False),
           "AdaBoos Classifier":AdaBoostRegressor()

        }
        
        model_report:dict=evaluate_models(X_train=X_train,Y_train=Y_train, X_test=X_test,Y_test=Y_test,
                                         models=models)
        
        # To get Best Model score from dict Models 

        best_model_score =max(sorted(model_report.values()))

        # To get best Model name from dict 

        best_model_name= list (model_report.keys())[
           list(model_report.values()).index(best_model_score)
        ]

        best_model = models[best_model_name]

        if best_model_score <0.6 :
           raise CustomException("No Model with more than 60 % score found")
        
        logging.info(f" Best Model :{best_model_name} ")
        save_obj(file_path=self.model_trainer_config.train_model_file_path,obj=best_model)

        predicted = best_model.predict(X_test)
        r2_score_var= r2_score(Y_test,predicted)
        return r2_score_var
       



     except Exception as e:
        raise CustomException(e,sys) 

       
