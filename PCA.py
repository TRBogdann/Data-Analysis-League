import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("./dataIN/data.csv")
print(df.info())
print(df.describe())

dropped=["gameId","blueWins","blueEliteMonsters","redEliteMonsters","redFirstBlood","blueGoldDiff","redGoldDiff","blueExperienceDiff","redExperienceDiff","blueCSPerMin","redCSPerMin","blueGoldPerMin","redGoldPerMin","blueDeaths","redDeaths","blueAvgLevel","redAvgLevel"]
print(df.shape)
test_df = df.dropna().astype(float)

t,ax = plt.subplots(figsize=(40,40))
sns.heatmap(test_df.corr(),annot=True,vmin=-1,vmax=1,cmap="YlGnBu")
plt.show()

y_df = test_df["blueWins"]
test_df = test_df.drop(columns=dropped)


# Centram datele in jurul originii
mean = test_df.mean()
test_df = test_df - mean

#distanta se poate contruii cu matricea de covariatie
# formula covariatie: C = (X.T*X)/(n-1)

cov= np.cov(test_df.to_numpy().T)

#determinare valori propri - vezi cursurile de algebra :))
# Determinare valori propri: det(cov-lambda*Im) = 0
# lambda - valoare prorie, cov - matrice covariatie, Im - matrice identitate m linii m coloane
# Determinare vectori propri det(cov-lambda*Im)vec = 0
# vec - vector propriu , lambda a fost deja aflat
eigenvalues, eigenvectors = np.linalg.eig(cov)
eigenvalues = np.real(eigenvalues)
eigenvectors = np.real(eigenvectors)
# Sortare valori propri si vectori

sorted_indices = np.argsort(eigenvalues)[::-1]
eigenvalues_sorted = eigenvalues[sorted_indices]
eigenvectors_sorted = eigenvectors[:, sorted_indices]

#Corelatie componente - atribute

corrDf = pd.DataFrame(eigenvectors_sorted,
                      index=test_df.columns,
                      columns=['PC'+str(i+1) for i in range(eigenvectors_sorted.shape[1]) ]
                      )

t,ax = plt.subplots(figsize=(30,30))
sns.heatmap(corrDf,vmin=-1,vmax=1,cmap="coolwarm",annot=True,ax=ax)
plt.show()

col = ['PC'+str(i+1) for i in range(len(eigenvectors_sorted))]

pc_df = pd.DataFrame(eigenvectors_sorted)
pc_df.columns = col
pc_df.index = test_df.columns
print(pc_df)
print(pc_df[["PC1","PC2","PC3"]])

#valorile propri reprezinta variatia
#aflam contributia componentelor ca ponderea valorilor proprii in suma acestora

ponderi = eigenvalues_sorted / np.sum(eigenvalues)

for it in ponderi:
    print(it)

plt.bar(pc_df.columns, ponderi, color ='blue')

plt.xlabel("Componenta")
plt.ylabel("Pondere")
plt.title("Analiza componente principale")
plt.show()

#pc1 pc2 pc3 reprezinta 97% din varianta.
#putem sa le folosim pentru a vizualiza datele
#date proiectate. Formula X_proiectat = X * p
#p matrice componente ales (in cazul asta pc1,pc2,pc3)

X_pca2 = pd.DataFrame(test_df.dot(pc_df[["PC1","PC2"]].to_numpy()))
X_pca = pd.DataFrame(test_df.dot(pc_df[["PC1",'PC2',"PC3"]].to_numpy()))
X_pca.columns = ["PC1","PC2","PC3"]
X_pca2.columns = ["PC1","PC2"]

X_pca2.index = y_df.index
X_pca.index = y_df.index

X_pca2.join(y_df).to_csv("./dataOUT/PCA2D.csv",index=False)
X_pca.join(y_df).to_csv("./dataOUT/PCA3D.csv",index=False)

plt.scatter(X_pca["PC1"], X_pca["PC2"],c=y_df,cmap='RdBu')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA Projection onto the First Two Principal Components')
plt.show()

plt.scatter(X_pca["PC1"], X_pca["PC3"],c=y_df,cmap='RdBu')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 3')
plt.title('PCA Projection onto the First Two Principal Components')
plt.show()

plt.scatter(X_pca["PC2"], X_pca["PC3"],c=y_df,cmap='RdBu')
plt.xlabel('Principal Component 2')
plt.ylabel('Principal Component 3')
plt.title('PCA Projection onto the First Two Principal Components')
plt.show()

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection='3d')
ax.scatter(X_pca["PC1"], X_pca["PC2"], X_pca["PC3"],c=y_df,cmap='RdBu')
plt.show()

