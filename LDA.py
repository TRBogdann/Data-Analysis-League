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




df = pd.read_csv("./dataIN/data.csv")
print(df.info())


dropped=["gameId","blueWins","blueEliteMonsters","redEliteMonsters","redFirstBlood","blueGoldDiff","redGoldDiff","blueExperienceDiff","redExperienceDiff","blueCSPerMin","redCSPerMin","blueGoldPerMin","redGoldPerMin","blueDeaths","redDeaths","blueAvgLevel","redAvgLevel"]
print(df.shape)
test_df = df.dropna().astype(float)

y_df = test_df["blueWins"]
test_df = test_df.drop(columns=dropped)


# Centram datele in jurul originii
mean = test_df.mean()
test_df = test_df - mean

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
test_df.to_csv("./dataOUT/LDA.csv", index=False)