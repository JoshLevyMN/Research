#Import
import numpy as np
import sklearn
import pandas as pd
from scipy.stats import randint, expon 
from sklearn.svm import SVC
from sklearn.svm import NuSVC
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score, average_precision_score, f1_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from numpy import genfromtxt


#importing files to arrays
#1k Set 1Pre seperated training and test data
#X_data = pd.read_csv("C:\\Users\Research\Research Data\SSCurveData.csv")
#Y_data = pd.read_csv("C:\\Users\Research\Research Data\SSLabels.csv")
#1k Set 2
X_data = pd.read_csv("C:\\Users\Research\Research Data\SSCurveDataTest.csv")
Y_data = pd.read_csv("C:\\Users\Research\Research Data\SSLablesTest.csv")
#7k examples, not seperated
#X_data = pd.read_csv("C:\\Users\Research\Research Data\sevenkData.csv")
#Y_data = pd.read_csv("C:\\Users\Research\Research Data\sevenkLabels.csv")
#22k examples, not seperated
#X_data = pd.read_csv("C:\\Users\Research\Research Data\entykData.csv")
#Y_data = pd.read_csv("C:\\Users\Research\Research Data\entykLabels.csv")
#Full dataset
#X_data = pd.read_csv("C:\\Users\Research\Research Data\completeData.csv")
#Y_data = pd.read_csv("C:\\Users\Research\Research Data\completeLabels.csv")

#scaling and splitting data
#X_data = preprocessing.scale(X_data)
#Y_data = preprocessing.scale(Y_data)
print("done")

X_train, X_test, Y_train, Y_test = train_test_split(X_data, Y_data)

#Exhaustive grid search parameters
param_grid = {'C': [1,10, 100, 1000], 'kernel': ['rbf', 'poly', 'sigmoid', 'linear'], 'degree': [0, 1, 2, 3, 4, 5], 'gamma': [1e-3, 1e-4, 1e-5, 1e-6], 'coef0': [0,1,2,3,4,5]}
#param_grid = {'C': [1,10,100,1000], 'kernel': ['sigmoid'], 'gamma': [1e-3, 1e-4, 1e-5, 1e-6], }, {'C': [1,10,100,1000], 'kernel': ['poly'], 'gamma': [1e-3, 1e-4, 1e-5, 1e-6], 'degree': [1,2,3,4,5,6,7]}, {'C': [1,10,100,1000], 'kernel': ['linear']}
#Randomized grid search parameters
param_dist = {'C': expon(scale = 100), 
'gamma': expon(scale = .1), 
'kernel': ['rbf', 'poly', 'sigmoid', 'linear'], 
'degree': randint(1,100),
'coef0': randint(0,100)}
n_iter_search = 10


#Creating and training model
    #Regular model
#model = SVC(C= 10, gamma= .0001, kernel= 'rbf', verbose = True)
SVC = SVC(verbose = False)
    #Regular grid search
#model = GridSearchCV(SVC, param_grid=param_grid)
    #Randomized Grid search
model = RandomizedSearchCV(SVC, param_distributions=param_dist, n_iter=n_iter_search)

    #Training
model.fit(X_train, Y_train.values.ravel())

    #Cross Validation
scores = cross_val_score(model, X_data, Y_data.values.ravel(), cv = 5)

#scoring model
def score():
    predicted=model.predict(X_test)
#    print(((((len(predicted)-(sum(predicted)))/2)+sum(predicted)))/len(predicted))
    score = model.score(X_test, Y_test)
    print("normal score")
    print(score)

    print("accuracy_score")
    accscore=accuracy_score(Y_test, predicted)
    print(accscore)

    print("Cross validation score and 95% CI")
    print(scores.mean())
    print(scores.std()*2)

    print("f1 score")
    f1=f1_score(Y_test, predicted, average='binary')
    print(f1)

    aps=average_precision_score(Y_test, predicted)
    print("average_precision_score")
    print(aps)

    print("model hyperparameters")
    print(model.best_params_)

score()
