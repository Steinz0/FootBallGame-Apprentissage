import sys
sys.path.append('../..')
from extractData.fileExtract import get_features_y
from profAI import strategies as st
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

features, y = get_features_y(filename='../../extractData/order.txt')

knn = KNeighborsClassifier(n_neighbors=3)

knn.fit(features, y)

# print(knn.score(features, y))

knn_parameters = {'n_neighbors':[2,3,4,5,6,7,8,9,10]}
knn = KNeighborsClassifier()
clf = GridSearchCV(knn, knn_parameters)
clf.fit(features, y)

print(clf.best_params_)
print(clf.best_score_)

svm_parameters = {'kernel':('linear', 'rbf', 'sigmoid', 'poly'), 'C':[1, 10]}
svm = SVC()
clf2 = GridSearchCV(svm, svm_parameters)
clf2.fit(features, y)

print(clf2.best_params_)
print(clf2.best_score_)