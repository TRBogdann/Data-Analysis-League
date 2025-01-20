import numpy as np
import pandas as pd
from factor_analyzer import FactorAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
from factor_analyzer.factor_analyzer import calculate_kmo, calculate_bartlett_sphericity
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.cluster import AgglomerativeClustering
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

df = pd.read_csv("./dataIN/data.csv")
print(df.info())

dragon_blue_wins = df[df["blueDragons"]==1]
dragon_red_wins = df[df["redDragons"]==1]
dragon_blue_wins = dragon_blue_wins[dragon_blue_wins["blueWins"]==1]
dragon_red_wins = dragon_red_wins[dragon_red_wins["blueWins"]==0]
dragon_matches = df[df["blueDragons"]==1].shape[0]+df[df["redDragons"]==1].shape[0]

print("Procent castig(Dragon 10 min): "+str((dragon_blue_wins.shape[0]+dragon_red_wins.shape[0])/dragon_matches))


dropped=["gameId","blueWins","blueEliteMonsters","redEliteMonsters","redFirstBlood","blueGoldDiff","redGoldDiff","blueExperienceDiff","redExperienceDiff","blueCSPerMin","redCSPerMin","blueGoldPerMin","redGoldPerMin","blueDeaths","redDeaths","blueAvgLevel","redAvgLevel"]
#comunalitati sub 60%
droppedComunalities =["blueWardsPlaced","blueWardsDestroyed","blueTowersDestroyed","blueHeralds","redTotalJungleMinionsKilled",
                      "redWardsPlaced","redWardsDestroyed","redTowersDestroyed","redHeralds","blueTotalJungleMinionsKilled","blueFirstBlood"]
filename = "EFA4D.csv"
#comunalitati sub 60% dupa ce am eliminat primele comunalitati - pentru a reduce numarul de factori
#droppedComunalities2 = ["blueTotalMinionsKilled","redTotalMinionsKilled"]
#filename = "EFA3D.csv"

print(df.shape)
efa_df = df.dropna().astype(float)

y_df = efa_df["blueWins"]
efa_df = efa_df.drop(columns=dropped)
efa_df = efa_df.drop(columns=droppedComunalities)
#efa_df = efa_df.drop(columns=droppedComunalities2)

#0. Data cleaning => Stergem Coloanele Numerice => Inlocuim datele lipsa cu None(Null)
# => Stergem Randurile cu date lipsa => Convertim randurile nenumerice la float




# Centram datele in jurul originii
mean = efa_df.mean()
efa_df = efa_df - mean
#I. Verificam daca se poate realiza analiza pe factori

chi_square_value, p_value = calculate_bartlett_sphericity(efa_df)

# Test Bartlett: H0:Nu exista factoriabilitate, H1:exista factoriabilitate
# Pt un grad de incredere de 95% => comparam p-value cu 0.05 (1-0.95)
# Daca p-value < 0.05 => Respingem H0 si Acceptam H1 => Putem realiza analiza pe factori pentru setul curent de date

print("Chi-Square: "+str(chi_square_value))
print("P-Value: "+str(p_value))

#Test KMO - arata gradul de factoriabilitate, indicele trebuie sa fie > 0.5

kmo_all, kmo_model = calculate_kmo(efa_df)
print("Indice KMO "+str(kmo_model))

#II. Realizam o prima analiza factoriala pentru determinarea numarului de factori seminficativi

fa = FactorAnalyzer(n_factors=efa_df.shape[1],rotation=None)
fa.fit(efa_df)

#Test 1 pentru determinarea numarului de factor: Criteriul lui Kaiser
#Numarul de factori seminificative este numarul de valori proprii mai mari ca 0
#Factori semnificativi criteriu Kaiser => 4
eigenvalues,eigenvectors = fa.get_eigenvalues()
significant = len([x for x in eigenvalues if x>=1])
print("Number of Significant Factors: "+ str(significant))

#Test 2 pentru determinarea numarului de factori: Grafic - Regula Cotului
#Factori semnificativi regula cotului => 3

plt.scatter(range(1,efa_df.shape[1]+1),eigenvalues)
plt.plot(range(1,efa_df.shape[1]+1),eigenvalues)
plt.title('Scree Plot')
plt.xlabel('Factors')
plt.ylabel('Eigenvalue')
plt.grid()
plt.show()

#III. Analiza Completa

fa = FactorAnalyzer(n_factors=significant,rotation="varimax")
fa.fit(efa_df)

#III.a) Influenta Factorilor Asupra Atributelor
t,ax = plt.subplots(figsize=(20,20))
corr_df = pd.DataFrame(fa.loadings_
                       ,index=efa_df.columns
                       ,columns=['F'+str(i+1) for i in range(significant)])

sns.heatmap(corr_df,annot=True,cmap="coolwarm",ax=ax,vmin=-1,vmax=1)
plt.show()

#III.b)Varinta explicata de factori - ultimul element reprezinta varianta cumulativa
#(in acest caz factorii explica 70% din varianta setului de date)
print("Factor Variance:")
print(fa.get_factor_variance())

#III c) comunalitati
communalities = fa.get_communalities()
print("Comunalities")
print(communalities)
plt.figure(figsize=(50,50))
plt.bar(efa_df.columns, communalities, color='skyblue', alpha=0.8)
plt.xlabel('Variables')
plt.ylabel('Communalities (Common Variance)')
plt.title('Communalities of Variables in EFA')
plt.ylim(0, 1)  # Communalities are proportions between 0 and 1
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

print("Loadings:")

efa = pd.DataFrame(fa.loadings_, columns=["F" + str(i + 1) for i in range(significant)])
print(corr_df)
X_efa = pd.DataFrame(efa_df.to_numpy().dot(efa[["F1","F2","F3","F4"]].to_numpy()), columns=["F1","F2","F3","F4"])

X_efa.index = y_df.index

plt.scatter(X_efa["F1"], X_efa["F2"],c=y_df,cmap='RdBu')
plt.xlabel('F1')
plt.ylabel('F2')
plt.title('Factor Analysis')
plt.show()



plt.scatter(X_efa["F1"], X_efa["F3"],c=y_df,cmap='RdBu')
plt.xlabel('F1')
plt.ylabel('F3')
plt.title('Factor Analysis')
plt.show()





plt.scatter(X_efa["F1"], X_efa["F4"],c=y_df,cmap='RdBu')
plt.xlabel('F1')
plt.ylabel('F4')
plt.title('Factor Analysis')
plt.show()

plt.scatter(X_efa["F3"], X_efa["F4"],c=y_df,cmap='RdBu')
plt.xlabel('F1')
plt.ylabel('F4')
plt.title('Factor Analysis')
plt.show()

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection='3d')
ax.scatter(X_efa["F1"], X_efa["F4"], X_efa["F3"],c=y_df,cmap='RdBu')
plt.show()

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection='3d')
ax.scatter(X_efa["F1"], X_efa["F2"], X_efa["F3"],c=y_df,cmap='RdBu')
plt.show()

X_efa["blueWins"] = y_df
X_efa.to_csv("./dataOUT/"+filename,index=False)
