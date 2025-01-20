# Machine Learning Models
from sklearn.svm import SVC                          # Support Vector Machine
from sklearn.linear_model import LogisticRegression  # Logistic Regression
from sklearn.tree import DecisionTreeClassifier      # Decision Tree
from sklearn.ensemble import RandomForestClassifier  # Random Forest Classifier
from sklearn.naive_bayes import GaussianNB           # Naive Bayes (Gaussian)

# Data Splitting
from sklearn.model_selection import train_test_split  # Train-Test Split

# Evaluation Metrics
from sklearn.metrics import confusion_matrix          # Confusion Matrix
from sklearn.metrics import precision_score           # Precision
from sklearn.metrics import recall_score              # Recall
from sklearn.metrics import f1_score                  # F1-Score
from sklearn.metrics import accuracy_score            # Accuracy

import pandas as pd
import numpy as np

#SVM
#LogisticRegression
#DecisionTreeClassifier
#DecisionTreeRegressor
#RandomForestClassifier
#NaiveBayes

index=["EFA3D","EFA4D","LDA","PCA2D","PCA3D"]

Used = []
Model = []
Precision = []
Recall = []
F1Score = []
Accuracy = []
TruePos= []
FalsePos= []
FalseNeg = []
TrueNeg = []


def append(test_y,pred_y, model_name, used):
    cm = confusion_matrix(test_y, pred_y)
    precision = precision_score(test_y, pred_y, average='binary')
    recall = recall_score(test_y, pred_y, average='binary')
    f1 = f1_score(test_y, pred_y, average='binary')
    accuracy = accuracy_score(test_y, pred_y)

    Precision.append(precision)
    Model.append(model_name)
    Recall.append(recall)
    F1Score.append(f1)
    Accuracy.append(accuracy)
    TruePos.append(float(cm[0, 0]))
    FalsePos.append(float(cm[0, 1]))
    FalseNeg.append(float(cm[1, 0]))
    TrueNeg.append(float(cm[1, 1]))
    Used.append(used)

for it in index:
    df = pd.read_csv("./dataOUT/"+it+".csv")
    X = df.drop(columns=["blueWins"])
    y = df["blueWins"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.7, random_state=42)

    model = SVC(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    append(y_test, y_pred, "SVM",it)

    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    append(y_test, y_pred, "LogisticRegression",it)

    model = DecisionTreeClassifier(random_state=42,max_depth=10,min_samples_leaf=10)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    append(y_test, y_pred, "DecisionTreeClassifier",it)

    model = RandomForestClassifier(max_depth=5, n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    append(y_test, y_pred, "RandomForestClassifier",it)

    model = GaussianNB()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    append(y_test, y_pred, "GaussianNB",it)


dict ={
    "Used":Used,
    "Model":Model,
    "Accuracy": Accuracy,
    "Precision":Precision,
    "Recall":Recall,
    "F1Score":F1Score,
    "TruePos":TruePos,
    "FalsePos":FalsePos,
    "FalseNeg":FalseNeg,
    "TrueNeg":TrueNeg
}

df = pd.DataFrame(dict)
df.to_csv("./dataOUT/models.csv",index=False)
