import sys

from matplotlib import pyplot as plt
sys.path.append('../..')
from extractData.fileExtract import get_features_y
from profAI import strategies as st
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from IPython.display import Image
import pandas as pd
import dataframe_image as dfi
pd.set_option('display.max_colwidth', -1)

features, y = get_features_y(filename='../../extractData/order.txt')

params = []
score = []

knn_parameters = {'weights': ('uniform', 'distance'), 'algorithm': ('auto', 'ball_tree', 'kd_tree', 'brute'), 'n_neighbors':[2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50]}
knn = KNeighborsClassifier()
clf = GridSearchCV(knn, knn_parameters, n_jobs=-1, verbose=0, cv=2)
clf.fit(features, y)

# {'algorithm': 'auto', 'n_neighbors': 3, 'weights': 'distance'}
# 0.7103658536585366
print(clf.best_params_)
print(clf.best_score_)
params.append(clf.best_params_)
score.append(clf.best_score_)

svm_parameters = {'kernel':('linear', 'rbf', 'sigmoid', 'poly'), 'C':[1, 10]}
svm = SVC()
clf2 = GridSearchCV(svm, svm_parameters, verbose=3, cv=2)
clf2.fit(features, y)

# 0.667683  {'C': 1, 'kernel': 'linear'}
print(clf2.best_params_)
print(clf2.best_score_)
params.append(clf2.best_params_)
score.append(clf2.best_score_)

dt_parameters = {'criterion':('gini', 'entropy', 'log_loss'), 'max_depth':['None',2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50]}
dt = DecisionTreeClassifier()
clf7 = GridSearchCV(dt, dt_parameters, n_jobs=-1, verbose=0, cv=2)
clf7.fit(features, y)

print(clf7.best_params_)
print(clf7.best_score_)
params.append(clf7.best_params_)
score.append(clf7.best_score_)

rf_parameters = {'criterion':('gini', 'entropy', 'log_loss'), 'max_depth':['None',2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50], 'class_weight' : ('None', 'balanced', 'balanced_sample')}
rf = RandomForestClassifier()
clf3 = GridSearchCV(rf, rf_parameters, n_jobs=-1, verbose=0, cv=2)
clf3.fit(features, y)

# {'criterion': 'entropy', 'max_depth': 20}
# 0.7682926829268293
print(clf3.best_params_)
print(clf3.best_score_)
params.append(clf3.best_params_)
score.append(clf3.best_score_)

gb_parameters = {'loss':('log_loss', 'deviance', 'exponential'), 'n_estimators':[1,10,50,100,150,200,250,300,350,400,450,500], 'max_depth':[2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50]}
gb = GradientBoostingClassifier()
clf4 = GridSearchCV(gb, gb_parameters, n_jobs=-1, verbose=0, cv=2)
clf4.fit(features, y)

# {'loss': 'deviance', 'max_depth': 2, 'n_estimators': 50}
# 0.7103658536585366
print(clf4.best_params_)
print(clf4.best_score_)
params.append(clf4.best_params_)
score.append(clf4.best_score_)


data =  {'score': score, 'best_parameters': params}
tab = pd.DataFrame(data=data, index=['KNN', 'SVM', 'DecisionTree', 'RandomForest', 'Boosting'])
print(tab)
dfi.export(tab, 'gridSearch.png')