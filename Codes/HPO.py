# -*- coding: utf-8 -*-
"""HPO.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1krkX8LC6iv2T_HJrkJ4pa-qosDy2fu24

**Enhanced Phishing Transactions Detection on Ethereum Network with Tree-based Ensembles: An Empirical Study**

* **Researchers:**
  * **Shikah Alsunaidi** (Information and Computer Science Department, KFUPM)
  * **Dr. Hamoud Aljamaan** (Information and Computer Science Department, KFUPM)
---

# ▶ **1. Imports**

---
"""

# Commented out IPython magic to ensure Python compatibility.
# import libraries section
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec
import seaborn as sns
# %matplotlib inline

# Stop warnings
import warnings as w
w.simplefilter(action='ignore',category=FutureWarning)

"""# ▶ **2. Global Functions**

---

## **2.1. Upload File Function**

---
"""

# This function takes the file name to upload it and return the dataframe
def upload_file(file_name):

  # Upload CSV file (ReducedDS.csv)
  from google.colab import files
  uploaded = files.upload()

  # Convert the uploaded data into dataframe
  import io
  df = pd.read_csv(io.BytesIO(uploaded[file_name]))

  return df

"""## **2.2. Write to File Function**

---

"""

# This function write the dataframe to excel file
def write_to_excel (mcc_DF, model, fileName):
  if model == "RF":
    df=pd.DataFrame(mcc_DF,columns=[model])
    df.to_csv(fileName,index = False)
  else:
    df = pd.read_csv(fileName)
    df[model]=mcc_DF
    df.to_csv(fileName,index = False)



"""# ▶ **3 Hyperparameters Optimization**

---

## **3.1. Upload Tuning Data**


---
"""

df = upload_file('tuning_DF.csv')
df

# divide the dataframe into data and lable
x=df.iloc[:,:-1]
y=df['class']
x.shape

"""## **3.2. Install and Import Optuna Lib**

---

* **Resources:**
  * https://optuna.org/
  * https://towardsdatascience.com/exploring-optuna-a-hyper-parameter-framework-using-logistic-regression-84bd622cd3a5


---
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install optuna

import optuna

"""## **3.3. Objective Functions**

---

#### **3.3.1. RF**

---
"""

#Step 1. Define an objective function to be maximized.
def objective(trial):
  from sklearn.ensemble import RandomForestClassifier

  from sklearn.model_selection import RepeatedStratifiedKFold
  from sklearn.model_selection import cross_validate

  from sklearn.metrics import make_scorer
  from sklearn.metrics import matthews_corrcoef

  from sklearn.pipeline import make_pipeline
  from sklearn.preprocessing import  StandardScaler


  scaler = StandardScaler()

  scoring = {'matthews_corrcoef': make_scorer(matthews_corrcoef)}
  rfold= RepeatedStratifiedKFold(n_splits=10, n_repeats=10)

  # Step 2. Setup values for the hyperparameters:

  rf_n_estimators = trial.suggest_int("rf_n_estimators", 50, 100)
  rf_random_state = trial.suggest_categorical("rf_random_state", [22,32,42])
  classifier_obj = RandomForestClassifier(n_estimators = rf_n_estimators, random_state = rf_random_state)

  pipeline = make_pipeline(scaler, classifier_obj)

  # Step 3: Scoring method:
  score=cross_validate(pipeline, x , y, cv=rfold,scoring=scoring, return_train_score=False)
  mcc = score['test_matthews_corrcoef'].mean()
  return mcc

# Step 4: Running it
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)

def get_Optimized_Parmaters():

  # Getting the best trial:
  print(f"The best trial is : \n{study.best_trial}")

  # Getting the best score:
  print(f"The best value is : \n{study.best_value}")

  # Getting the best parameters:
  print(f"The best parameters are : \n{study.best_params}")

  #Visualize the slice plot
  #optuna.visualization.plot_slice(study, params=['rf_n_estimators', 'rf_max_depth'])
  #optuna.visualization.plot_slice(study, params=['rf_n_estimators', 'rf_criterion',  'rf_n_estimators', 'rf_random_state', 'rf_max_depth', 'rf_min_samples_leaf'])
  optuna.visualization.plot_slice(study, params=['rf_n_estimators', 'rf_random_state'])

#RF
get_Optimized_Parmaters()

# Getting the best trial:
print(f"The best trial is : \n{study.best_trial}")

# Getting the best score:
print(f"The best value is : \n{study.best_value}")

# Getting the best parameters:
print(f"The best parameters are : \n{study.best_params}")

#Visualize the slice plot
optuna.visualization.plot_slice(study, params=['rf_n_estimators', 'rf_random_state'])

"""### **3.3.2. Ada**

---


"""

#Step 1. Define an objective function to be maximized.
def objective(trial):
  from sklearn.ensemble import AdaBoostClassifier

  from sklearn.model_selection import RepeatedStratifiedKFold
  from sklearn.model_selection import cross_validate

  from sklearn.metrics import make_scorer
  from sklearn.metrics import matthews_corrcoef


  from sklearn.pipeline import make_pipeline
  from sklearn.preprocessing import  StandardScaler


  scaler = StandardScaler()

  scoring = {'matthews_corrcoef': make_scorer(matthews_corrcoef)}
  rfold= RepeatedStratifiedKFold(n_splits=10, n_repeats=10)

  # Step 2. Setup values for the hyperparameters:

  Ada_n_estimators = trial.suggest_categorical("Ada_n_estimators", [100, 300,500,700,900])
  Ada_learning_rate = trial.suggest_float("Ada_learning_rate", 0.1,1)
  classifier_obj = AdaBoostClassifier(n_estimators = Ada_n_estimators, learning_rate = Ada_learning_rate)

  pipeline = make_pipeline(scaler, classifier_obj)

  # Step 3: Scoring method:
  score=cross_validate(pipeline, x , y, cv=rfold,scoring=scoring, return_train_score=False)
  mcc = score['test_matthews_corrcoef'].mean()
  return mcc

# Step 4: Running it
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)

def get_Optimized_Parmaters():

  # Getting the best trial:
  print(f"The best trial is : \n{study.best_trial}")

  # Getting the best score:
  print(f"The best value is : \n{study.best_value}")

  # Getting the best parameters:
  print(f"The best parameters are : \n{study.best_params}")

  #Visualize the slice plot
  optuna.visualization.plot_slice(study, params=['rf_n_estimators', 'Ada_learning_rate'])

optuna.visualization.plot_slice(study, params=['Ada_n_estimators', 'Ada_learning_rate'])

#Ada
get_Optimized_Parmaters()

# Getting the best trial:
print(f"The best trial is : \n{study.best_trial}")

# Getting the best score:
print(f"The best value is : \n{study.best_value}")

# Getting the best parameters:
print(f"The best parameters are : \n{study.best_params}")

#Visualize the slice plot
optuna.visualization.plot_slice(study, params=['rf_n_estimators', 'Ada_learning_rate'])

optuna.visualization.plot_slice(study, params=['Ada_n_estimators', 'Ada_learning_rate'])

"""### **3.3.3 ET**

---


"""

#Step 1. Define an objective function to be maximized.
def objective(trial):
  from sklearn.ensemble import ExtraTreesClassifier

  from sklearn.model_selection import RepeatedStratifiedKFold
  from sklearn.model_selection import cross_validate

  from sklearn.metrics import make_scorer
  from sklearn.metrics import matthews_corrcoef

  from sklearn.pipeline import make_pipeline
  from sklearn.preprocessing import  StandardScaler


  scaler = StandardScaler()

  scoring = {'matthews_corrcoef': make_scorer(matthews_corrcoef)}
  rfold= RepeatedStratifiedKFold(n_splits=10, n_repeats=10)

  # Step 2. Setup values for the hyperparameters:
  ET_n_estimators = trial.suggest_int("ET_n_estimators", 50, 100)
  ET_random_state = trial.suggest_categorical("ET_random_state", [22,32,42])
  classifier_obj = ExtraTreesClassifier(n_estimators = ET_n_estimators, random_state = ET_random_state)

  pipeline = make_pipeline(scaler, classifier_obj)

  # Step 3: Scoring method:
  score=cross_validate(pipeline, x , y, cv=rfold,scoring=scoring, return_train_score=False)
  mcc = score['test_matthews_corrcoef'].mean()
  return mcc

# Step 4: Running it
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)

def get_Optimized_Parmaters():

  # Getting the best trial:
  print(f"The best trial is : \n{study.best_trial}")

  # Getting the best score:
  print(f"The best value is : \n{study.best_value}")

  # Getting the best parameters:
  print(f"The best parameters are : \n{study.best_params}")

  #Visualize the slice plot
  optuna.visualization.plot_slice(study, params=['ET_n_estimators', 'ET_random_state'])

get_Optimized_Parmaters()

# Getting the best trial:
print(f"The best trial is : \n{study.best_trial}")

# Getting the best score:
print(f"The best value is : \n{study.best_value}")

# Getting the best parameters:
print(f"The best parameters are : \n{study.best_params}")

#Visualize the slice plot
optuna.visualization.plot_slice(study, params=['ET_n_estimators', 'ET_random_state'])

"""### **3.3.4. DT**

---


"""

#Step 1. Define an objective function to be maximized.
def objective(trial):
  from sklearn import tree

  from sklearn.model_selection import RepeatedStratifiedKFold
  from sklearn.model_selection import cross_validate

  from sklearn.metrics import make_scorer
  from sklearn.metrics import matthews_corrcoef

  from sklearn.pipeline import make_pipeline
  from sklearn.preprocessing import  StandardScaler


  scaler = StandardScaler()

  scoring = {'matthews_corrcoef': make_scorer(matthews_corrcoef)}
  rfold= RepeatedStratifiedKFold(n_splits=10, n_repeats=10)

  # Step 2. Setup values for the hyperparameters:

  DT_criterion = trial.suggest_categorical("DT_criterion", ['gini', 'entropy'])
  DT_random_state = trial.suggest_categorical("DT_random_state", [22,32,42])
  DT_max_depth = trial.suggest_int("DT_max_depth", 1,8)

  classifier_obj =tree.DecisionTreeClassifier(random_state = DT_random_state, criterion = DT_criterion, max_depth = DT_max_depth)

  pipeline = make_pipeline(scaler, classifier_obj)

  # Step 3: Scoring method:
  score=cross_validate(pipeline, x , y, cv=rfold,scoring=scoring, return_train_score=False)
  mcc = score['test_matthews_corrcoef'].mean()
  return mcc

# Step 4: Running it
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)

def get_Optimized_Parmaters():

  # Getting the best trial:
  print(f"The best trial is : \n{study.best_trial}")

  # Getting the best score:
  print(f"The best value is : \n{study.best_value}")

  # Getting the best parameters:
  print(f"The best parameters are : \n{study.best_params}")

  #Visualize the slice plot
  optuna.visualization.plot_slice(study, params=['DT_random_state', 'DT_criterion','DT_max_depth'])

get_Optimized_Parmaters()

# Getting the best trial:
print(f"The best trial is : \n{study.best_trial}")

# Getting the best score:
print(f"The best value is : \n{study.best_value}")

# Getting the best parameters:
print(f"The best parameters are : \n{study.best_params}")

#Visualize the slice plot
optuna.visualization.plot_slice(study, params=['DT_random_state', 'DT_criterion','DT_max_depth'])

"""### **3.3.5. GBM**

---


"""

#Step 1. Define an objective function to be maximized.
def objective(trial):
  from sklearn.ensemble import GradientBoostingClassifier

  from sklearn.model_selection import RepeatedStratifiedKFold
  from sklearn.model_selection import cross_validate

  from sklearn.metrics import make_scorer
  from sklearn.metrics import matthews_corrcoef

  from sklearn.pipeline import make_pipeline
  from sklearn.preprocessing import  StandardScaler


  scaler = StandardScaler()

  scoring = {'matthews_corrcoef': make_scorer(matthews_corrcoef)}
  rfold= RepeatedStratifiedKFold(n_splits=10, n_repeats=10)

  # Step 2. Setup values for the hyperparameters:

  GB_n_estimators = trial.suggest_categorical("GB_n_estimators", [50,100,500,1000])
  GB_learning_rate = trial.suggest_categorical("GB_learning_rate", [0.001,0.01,0.1])
  GB_min_samples_leaf = trial.suggest_categorical("GB_min_samples_leaf", [1,5,10])
  GB_max_depth=trial.suggest_categorical("GB_max_depth", [3,7,9])
  GB_loss=trial.suggest_categorical("GB_loss", ['deviance','exponential'])

  classifier_obj =GradientBoostingClassifier(n_estimators=GB_n_estimators,learning_rate=GB_learning_rate,min_samples_leaf=GB_min_samples_leaf,max_depth=GB_max_depth,loss=GB_loss)

  pipeline = make_pipeline(scaler, classifier_obj)

  # Step 3: Scoring method:
  score=cross_validate(pipeline, x , y, cv=rfold,scoring=scoring, return_train_score=False)
  mcc = score['test_matthews_corrcoef'].mean()
  return mcc

# Step 4: Running it
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)

def get_Optimized_Parmaters():

  # Getting the best trial:
  print(f"The best trial is : \n{study.best_trial}")

  # Getting the best score:
  print(f"The best value is : \n{study.best_value}")

  # Getting the best parameters:
  print(f"The best parameters are : \n{study.best_params}")

  #Visualize the slice plot
  optuna.visualization.plot_slice(study, params=['GB_n_estimators','GB_learning_rate','GB_min_samples_leaf','GB_max_depth','GB_loss'])

get_Optimized_Parmaters()

# Getting the best trial:
print(f"The best trial is : \n{study.best_trial}")

# Getting the best score:
print(f"The best value is : \n{study.best_value}")

# Getting the best parameters:
print(f"The best parameters are : \n{study.best_params}")

#Visualize the slice plot
optuna.visualization.plot_slice(study, params=['GB_n_estimators','GB_learning_rate','GB_min_samples_leaf','GB_max_depth','GB_loss'])

"""### **3.3.6. XGB**
 * https://xgboost.readthedocs.io/en/stable/python/python_api.html#module-xgboost.sklearn
---


"""

#Step 1. Define an objective function to be maximized.
def objective(trial):
  from xgboost import XGBClassifier

  from sklearn.model_selection import RepeatedStratifiedKFold
  from sklearn.model_selection import cross_validate

  from sklearn.metrics import make_scorer
  from sklearn.metrics import matthews_corrcoef

  from sklearn.pipeline import make_pipeline
  from sklearn.preprocessing import  StandardScaler


  scaler = StandardScaler()

  scoring = {'matthews_corrcoef': make_scorer(matthews_corrcoef)}
  rfold= RepeatedStratifiedKFold(n_splits=10, n_repeats=10)

  # Step 2. Setup values for the hyperparameters:

  XGB_n_estimators = trial.suggest_categorical("XGB_n_estimators", [100,300,500,700,900])
  XGB_learning_rate = trial.suggest_float("XGB_learning_rate", 0.1,0.7)
  XGB_max_depth=trial.suggest_int("XGB_max_depth", 3,7)
  XGB_random_state = trial.suggest_int("XGB_random_state", 0,42)

  classifier_obj =XGBClassifier(n_estimators=XGB_n_estimators,learning_rate=XGB_learning_rate,max_depth=XGB_max_depth, random_state=XGB_random_state)

  pipeline = make_pipeline(scaler, classifier_obj)

  # Step 3: Scoring method:
  score=cross_validate(pipeline, x , y, cv=rfold,scoring=scoring, return_train_score=False)
  mcc = score['test_matthews_corrcoef'].mean()
  return mcc

# Step 4: Running it
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)

def get_Optimized_Parmaters():

  # Getting the best trial:
  print(f"The best trial is : \n{study.best_trial}")

  # Getting the best score:
  print(f"The best value is : \n{study.best_value}")

  # Getting the best parameters:
  print(f"The best parameters are : \n{study.best_params}")

  #Visualize the slice plot
  optuna.visualization.plot_slice(study, params=['XGB_n_estimators','XGB_learning_rate','XGB_max_depth','XGB_random_state'])

get_Optimized_Parmaters()

# Getting the best trial:
print(f"The best trial is : \n{study.best_trial}")

# Getting the best score:
print(f"The best value is : \n{study.best_value}")

# Getting the best parameters:
print(f"The best parameters are : \n{study.best_params}")

#Visualize the slice plot
optuna.visualization.plot_slice(study, params=['XGB_n_estimators','XGB_learning_rate','XGB_max_depth','XGB_random_state'])

"""### **3.3.7. HGB**
* https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html
---


"""

#Step 1. Define an objective function to be maximized.
def objective(trial):
  from sklearn.ensemble import HistGradientBoostingClassifier

  from sklearn.model_selection import RepeatedStratifiedKFold
  from sklearn.model_selection import cross_validate

  from sklearn.metrics import make_scorer
  from sklearn.metrics import matthews_corrcoef

  from sklearn.pipeline import make_pipeline
  from sklearn.preprocessing import  StandardScaler


  scaler = StandardScaler()

  scoring = {'matthews_corrcoef': make_scorer(matthews_corrcoef)}
  rfold= RepeatedStratifiedKFold(n_splits=10, n_repeats=10)

  # Step 2. Setup values for the hyperparameters:

  HGB_max_iter = trial.suggest_categorical("HGB_max_iter", [100,300,500,700,900])
  HGB_learning_rate = trial.suggest_float("HGB_learning_rate", 0.1,0.7)
  HGB_min_samples_leaf = trial.suggest_int('HGB_min_samples_leaf', 5,25)
  HGB_max_depth = trial.suggest_categorical("HGB_max_depth", [None,1,3,5,7])

  classifier_obj =HistGradientBoostingClassifier(max_iter = HGB_max_iter,learning_rate = HGB_learning_rate,
                                min_samples_leaf = HGB_min_samples_leaf, max_depth = HGB_max_depth)

  pipeline = make_pipeline(scaler, classifier_obj)

  # Step 3: Scoring method:
  score=cross_validate(pipeline, x , y, cv=rfold,scoring=scoring, return_train_score=False)
  mcc = score['test_matthews_corrcoef'].mean()
  return mcc

# Step 4: Running it
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)

def get_Optimized_Parmaters():

  # Getting the best trial:
  print(f"The best trial is : \n{study.best_trial}")

  # Getting the best score:
  print(f"The best value is : \n{study.best_value}")

  # Getting the best parameters:
  print(f"The best parameters are : \n{study.best_params}")

  #Visualize the slice plot
  optuna.visualization.plot_slice(study, params=['HGB_max_iter','HGB_learning_rate', 'HGB_min_samples_leaf', 'HGB_max_depth'])

get_Optimized_Parmaters()

# Getting the best trial:
print(f"The best trial is : \n{study.best_trial}")

# Getting the best score:
print(f"The best value is : \n{study.best_value}")

# Getting the best parameters:
print(f"The best parameters are : \n{study.best_params}")

#Visualize the slice plot
optuna.visualization.plot_slice(study, params=['HGB_max_iter','HGB_learning_rate', 'HGB_min_samples_leaf', 'HGB_max_depth'])

"""### **3.3.8. CAT**
* https://catboost.ai/en/docs/concepts/parameter-tuning
* https://catboost.ai/en/docs/concepts/loss-functions-classification
---


"""

pip install catboost

#Step 1. Define an objective function to be maximized.
def objective(trial):
  from catboost import CatBoostClassifier

  from sklearn.model_selection import RepeatedStratifiedKFold
  from sklearn.model_selection import cross_validate

  from sklearn.metrics import make_scorer
  from sklearn.metrics import matthews_corrcoef

  from sklearn.pipeline import make_pipeline
  from sklearn.preprocessing import  StandardScaler


  scaler = StandardScaler()

  scoring = {'matthews_corrcoef': make_scorer(matthews_corrcoef)}
  rfold= RepeatedStratifiedKFold(n_splits=10, n_repeats=10)

  # Step 2. Setup values for the hyperparameters:

  CAT_n_estimators = trial.suggest_categorical("CAT_n_estimators", [100,300,500,700,900])
  CAT_learning_rate = trial.suggest_float("CAT_learning_rate", 0.1,0.7)
  CAT_depth = trial.suggest_int('CAT_depth', 4,10)
  CAT_min_data_in_leaf = trial.suggest_int("CAT_min_data_in_leaf", 1,10)
  CAT_loss_function = trial.suggest_categorical("CAT_loss_function", ['Logloss','CrossEntropy'])

  classifier_obj =CatBoostClassifier(n_estimators = CAT_n_estimators, learning_rate = CAT_learning_rate,
                                     depth = CAT_depth, min_data_in_leaf = CAT_min_data_in_leaf,
                                     loss_function = CAT_loss_function, logging_level='Silent')

  pipeline = make_pipeline(scaler, classifier_obj)

  # Step 3: Scoring method:
  score=cross_validate(pipeline, x , y, cv=rfold,scoring=scoring, return_train_score=False)
  mcc = score['test_matthews_corrcoef'].mean()
  return mcc

# Step 4: Running it
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)

def get_Optimized_Parmaters():

  # Getting the best trial:
  print(f"The best trial is : \n{study.best_trial}")

  # Getting the best score:
  print(f"The best value is : \n{study.best_value}")

  # Getting the best parameters:
  print(f"The best parameters are : \n{study.best_params}")

  #Visualize the slice plot
  optuna.visualization.plot_slice(study, params=['CAT_n_estimators','CAT_learning_rate', 'CAT_depth', 'CAT_min_data_in_leaf', 'CAT_loss_function'])

get_Optimized_Parmaters()

# Getting the best trial:
print(f"The best trial is : \n{study.best_trial}")

# Getting the best score:
print(f"The best value is : \n{study.best_value}")

# Getting the best parameters:
print(f"The best parameters are : \n{study.best_params}")

#Visualize the slice plot
optuna.visualization.plot_slice(study, params=['CAT_n_estimators','CAT_learning_rate', 'CAT_depth', 'CAT_min_data_in_leaf', 'CAT_loss_function'])