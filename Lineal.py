import json
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestClassifier
import pandas as pd


with open('users_IA_clases.json') as file:
    data_users_entrenamiento = json.load(file)

with open('users_IA_predecir.json') as file:
    data_users_prueba = json.load(file)

usuario = []
emails_phishing_recibidos = []
emails_phishing_clicados = []
vulnerable = []
Pb = []
solucion = 0
for usur in data_users_entrenamiento["usuarios"]:
    usuario.append(usur["usuario"])
    emails_phishing_recibidos.append(usur["emails_phishing_recibidos"])
    emails_phishing_clicados.append(usur["emails_phishing_clicados"])
    vulnerable.append(usur["vulnerable"])
    if (usur["emails_phishing_recibidos"] != 0):
        solucion = float(usur["emails_phishing_clicados"] / usur["emails_phishing_recibidos"]) * 100
    else:
        solucion = 0
    Pb.append(solucion)

print(Pb)
probabilidad_X_train2=pd.DataFrame({"Probabilidad":Pb})
probabilidad_y_train2=pd.DataFrame({"Vulnerable":vulnerable})




probabilidad_X_train =probabilidad_X_train2 [:-10]
probabilidad_X_test = probabilidad_X_train2[-10:]
probabilidad_y_train = probabilidad_y_train2[:-10]
probabilidad_y_test = probabilidad_y_train2[-10:]

regr = LinearRegression()
regr.fit(probabilidad_X_train, probabilidad_y_train)
print(regr.coef_)
probabilidad_y_pred = regr.predict(probabilidad_X_test)
print("Mean squared error: %.2f" % mean_squared_error(probabilidad_y_test, probabilidad_y_pred))
plt.scatter(probabilidad_X_test, probabilidad_y_test, color="black")
plt.plot(probabilidad_X_test, probabilidad_y_pred, color="blue", linewidth=3)
plt.xticks(())
plt.yticks(())
plt.show()
