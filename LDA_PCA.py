import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression




test_df = pd.read_csv("./dataOUT/PCA3D.csv")
y_df = test_df["blueWins"]

lda = LinearDiscriminantAnalysis(n_components=1)
test_df = lda.fit_transform(test_df,y_df)

# plot the scatterplot
plt.scatter(
    [x for x in range(test_df.shape[0])],test_df[:, 0],
    c=y_df,
    cmap='rainbow',
    alpha=0.7, edgecolors='b'
)
plt.show()

test_df = pd.DataFrame(test_df,columns=["LDA"])
test_df["blueWins"] = y_df
test_df.to_csv("./dataOUT/LDA_PCA.csv", index=False)