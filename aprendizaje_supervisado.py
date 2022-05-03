import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

with open('users_IA_clases.json') as file:
    data_users_entrenamiento = json.load(file)

with open('users_IA_predecir.json') as file:
    data_users_prueba = json.load(file)

usuario = []
emails_phishing_recibidos = []
emails_phishing_clicados = []
vulnerable = []
probabilidad = []
solucion = 0

for usr in data_users_entrenamiento["usuarios"]:
    usuario.append(usr["usuario"])
    emails_phishing_recibidos.append(usr["emails_phishing_recibidos"])
    emails_phishing_clicados.append(usr["emails_phishing_clicados"])
    vulnerable.append(usr["vulnerable"])
    if usr["emails_phishing_recibidos"] != 0:
        solucion = float(usr["emails_phishing_clicados"] / usr["emails_phishing_recibidos"]) * 100
    else:
        solucion = 0
    probabilidad.append(solucion)

data_x = pd.DataFrame({"probabilidad": probabilidad})
data_y = pd.DataFrame({"vulnerable": vulnerable})

# REGRESION LINEAL

# Use only one feature
data_x = data_x[:, np.newaxis, 2]
# Split the data into training/testing sets
data_x_train = data_x[:-20]
data_x_test = data_x[-20:]
# Split the targets into training/testing sets
data_y_train = data_y[:-20]
data_y_test = data_y[-20:]
# Create linear regression object
regr = linear_model.LinearRegression()
# Train the model using the training sets
regr.fit(data_x_train, data_y_train)
print(regr.coef_)
# Make predictions using the testing set
data_y_pred = regr.predict(data_x_test)
# The mean squared error
print("Mean squared error: %.2f" % mean_squared_error(data_y_test, data_y_pred))
# Plot outputs
plt.scatter(data_x_test, data_y_test, color="black")
plt.plot(data_x_test, data_y_pred, color="blue", linewidth=3)
plt.xticks(())
plt.yticks(())
plt.show()

# DECISION TREE