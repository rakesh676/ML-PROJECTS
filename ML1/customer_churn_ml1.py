# -*- coding: utf-8 -*-
"""customer churn ML1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KpGaDzpw7Ce882EFkKxzg7fOdrC1AIgc
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot  as plt
import seaborn as sns
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import pickle
from imblearn.over_sampling import SMOTE
from sklearn.tree import  DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC



data = pd.read_csv("/content/drive/MyDrive/ML DataSet/Telco-Customer-Churn.csv")
data.head()

data.drop(columns="customerID",inplace=True)

data.head(2)

data.info()

data.describe()

data[data['TotalCharges'] == " "] = 0

data['TotalCharges']=data["TotalCharges"].astype(float)

data.info()

data.duplicated().sum()

data.drop_duplicates(inplace=True)

data.describe()

corr = data[["SeniorCitizen" ,"tenure" ,	"MonthlyCharges",	"TotalCharges"]].corr()
plt.figure(figsize=(4,4))
sns.heatmap(corr,cmap="coolwarm",annot=True)
plt.show()

#LE = LabelEncoder()

obj_columns = data.select_dtypes(["object"]).columns

obj_columns

for i in obj_columns:
  print(data[i])

data.drop(index=data[data['gender'] == 0].index,inplace=True)

encoders = {}

for i in obj_columns:
  LE = LabelEncoder()
  print(data[i].value_counts())
  data[i] = LE.fit_transform(data[i])
  encoders[i] = LE

with open("encoders.pkl",'wb') as f:
  pickle.dump(encoders,f)

encoders

data.head()

corr_data = data.corr()
plt.figure(figsize=(20,15))
sns.heatmap(corr_data,annot=True,cmap="coolwarm")
plt.show()

data.drop(columns="TotalCharges",inplace=True)

x = data.drop(columns="Churn")
y = data['Churn']

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3,random_state=32)

y_train.value_counts()

smote = SMOTE(random_state=32)

x_train_smote,y_train_smote = smote.fit_resample(x_train,y_train)

y_train_smote.value_counts()

models = {
    "DecisionTree":DecisionTreeClassifier(random_state=32),
    "RandomForest":RandomForestClassifier(random_state=32),
    "SVC":SVC(random_state=32)
          }

scores = {}

for model_name,model in models.items():
  print(f"{model_name} is trained!")
  score = cross_val_score(model, x_train_smote, y_train_smote, cv=5, scoring='accuracy')
  scores[model_name] = score
  print(f"corss val accuracy of {model_name} is {np.mean(score)}")

print(scores)

random_f = RandomForestClassifier(random_state=32,max_depth=9,min_samples_split=10)

print(random_f.max_depth)

random_f.fit(x_train_smote,y_train_smote)

y_test_pred = random_f.predict(x_test)
acc_test = accuracy_score(y_test,y_test_pred)
print(f"accuracy of y_test is:{acc_test}")

y_train_pred = random_f.predict(x_train_smote)
acc_train = accuracy_score(y_train_smote,y_train_pred)
print(f"accuracy of y_train_smote:{acc_train}")

